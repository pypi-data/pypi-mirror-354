# intctl/setup_resources/finalise_database.py

import asyncio
import os
import time
from pathlib import Path
import traceback
from google.cloud.sql.connector import Connector, IPTypes
from google.auth.transport.requests import Request as AuthRequest
from google.cloud import secretmanager_v1
from google.auth import default
import asyncpg
from intctl.status import StatusManager
from intctl.utils.pathing import scripts_path
from .utils import Spinner
import uuid
from textwrap import dedent

# Use an official, small, pre-built image that includes Python and gcloud SDK.
# This is our "debugging" image.
BASE_IMAGE_URI = "google/cloud-sdk:slim"


def create_database(cfg: dict, status: StatusManager) -> None:
    """
    Checks if the Cloud SQL instance is ready and creates the specific database
    within that instance if it doesn't already exist.
    """
    status.start("cloudsql_instance_check")
    
    workspace_uuid = cfg["workspace_uuid"]
    project_id = cfg["project_id"]
    
    db_name = f"intellithing-pg-{workspace_uuid}".replace("_", "-").lower()
    if not db_name[0].isalpha():
        db_name = "pg-" + db_name
    db_name = db_name[:80]

    print(f"🔎 Checking if SQL instance '{db_name}' exists...")
    while True:
        with Spinner(f"Checking Cloud SQL instance '{db_name}'..."):
            inst_check = os.system(
                f"gcloud sql instances describe {db_name} --project={project_id} >/dev/null 2>&1"
            )
        if inst_check == 0:
            print(f"✅ SQL instance '{db_name}' is available.")
            break
        print(f"⏳ Waiting for SQL instance '{db_name}' to be ready. This may take a minute...")
        time.sleep(10)
    status.complete("cloudsql_instance_check")

    status.start("cloudsql_database")
    print(f"🔎 Checking if database '{db_name}' exists...")
    while True:
        db_check = os.system(
            f"gcloud sql databases describe {db_name} --instance={db_name} --project={project_id} >/dev/null 2>&1"
        )
        if db_check == 0:
            print(f"✅ Database '{db_name}' already exists.")
            break
        print(f"🚧 Creating database '{db_name}'...")
        create = os.system(
            f"gcloud sql databases create {db_name} --instance={db_name} --project={project_id}"
        )
        if create == 0:
            print(f"✅ Database '{db_name}' created.")
            break
        print(f"❌ Failed to create database. Retrying in 10s...")
        time.sleep(10)
    status.complete("cloudsql_database")




def execute_sql_job(cfg: dict, status: StatusManager):
    """
    Spawns a Kubernetes Job using a generic cloud-sdk image to execute the
    initialisation SQL from within the VPC.
    """
    status.start("execute_sql_job")

    # --- 1. Get Configuration ---
    project_id = cfg["project_id"]
    workspace_uuid = cfg["workspace_uuid"]
    organization_uuid = cfg["organization_uuid"]
    
    # The Cloud SQL instance name is the host for private IP connections
    db_instance_name = f"intellithing-pg-{workspace_uuid}".lower()
    if not db_instance_name[0].isalpha():
        db_instance_name = "pg-" + db_instance_name
    db_instance_name = db_instance_name[:80]
    db_name = db_instance_name # The database was created with the same name as the instance

    # Generate a unique suffix for this run's resources
    job_suffix = uuid.uuid4().hex[:8]
    job_name = f"sql-init-job-{job_suffix}"
    configmap_name = f"sql-runner-scripts-{job_suffix}"

    # --- 2. Define the Runner Scripts ---
    # Load the external SQL script content
    sql_script_path = scripts_path("status.sql")
    if not sql_script_path.exists():
        raise FileNotFoundError(f"SQL file not found at: {sql_script_path}")
    sql_script_content = sql_script_path.read_text()

    # Define the Python runner script that will execute inside the pod.
    # It connects directly to the DB, no connector needed.
    python_runner_script = dedent("""\
    import os
    import asyncio
    import traceback
    from google.auth import default
    from google.cloud import secretmanager_v1
    import asyncpg

    async def run_sql():
        try:
            # GCP clients will automatically use the mounted service account
            credentials, project_id = default()
            
            db_instance_name = os.environ["DB_INSTANCE_NAME"]
            db_name = os.environ["DB_NAME"]
            org_id = os.environ["ORG_ID"]
            ws_id = os.environ["WS_ID"]

            # --- Fetch Database Credentials ---
            client = secretmanager_v1.SecretManagerServiceClient(credentials=credentials)
            def get_secret(name):
                path = f"projects/{project_id}/secrets/{name}/versions/latest"
                return client.access_secret_version(request={"name": path}).payload.data.decode("UTF-8")

            print("Fetching database credentials...")
            user_secret_name = f"{org_id}-{ws_id}-pg-username"
            pass_secret_name = f"{org_id}-{ws_id}-pg-password"
            pg_user = get_secret(user_secret_name)
            pg_pass = get_secret(pass_secret_name)
            print("✅ Credentials fetched.")

            # --- Read the SQL script from the mounted ConfigMap ---
            with open("/app/status.sql") as f:
                sql_to_execute = f.read()

            # --- Connect Directly and Execute ---
            print(f"Connecting directly to database '{db_name}' on host '{db_instance_name}'...")
            conn = await asyncpg.connect(
                user=pg_user, password=pg_pass, database=db_name,
                host=db_instance_name, port=5432
            )
            
            try:
                print("Executing SQL script...")
                await conn.execute(sql_to_execute)
                print("✅✅✅ SQL SCRIPT EXECUTED SUCCESSFULLY ✅✅✅")
            finally:
                await conn.close()

        except Exception:
            print("❌ An error occurred during SQL execution.")
            traceback.print_exc()
            exit(1)

    if __name__ == "__main__":
        asyncio.run(run_sql())
    """)

    # --- 3. Define the Job Execution Logic ---
    # This shell script is the container's entrypoint.
    # It installs dependencies and then runs the python script.
    entrypoint_script = dedent("""\
    #!/bin/sh
    set -e
    echo "Installing Python dependencies..."
    pip install --quiet --no-cache-dir asyncpg google-cloud-secretmanager google-auth
    echo "Dependencies installed. Running SQL initialisation script..."
    python /app/runner.py
    """)

    # --- 4. Define the Kubernetes Job Manifest ---
    job_yaml = dedent(f"""\
    apiVersion: batch/v1
    kind: Job
    metadata:
      name: {job_name}
      namespace: intellithing
    spec:
      ttlSecondsAfterFinished: 300
      backoffLimit: 2
      template:
        spec:
          restartPolicy: Never
          containers:
          - name: sql-runner
            image: "{BASE_IMAGE_URI}"
            command: ["/bin/sh", "-c", "{entrypoint_script}"]
            env:
            - name: DB_INSTANCE_NAME
              value: "{db_instance_name}"
            - name: DB_NAME
              value: "{db_name}"
            - name: ORG_ID
              value: "{organization_uuid}"
            - name: WS_ID
              value: "{workspace_uuid}"
            volumeMounts:
            - name: scripts-volume
              mountPath: /app
            # The service account key is mounted from a secret
            - name: gcp-sa-key
              mountPath: /var/secrets/google
              readOnly: true
          # The GOOGLE_APPLICATION_CREDENTIALS env var points to the mounted key
          env:
          - name: GOOGLE_APPLICATION_CREDENTIALS
            value: /var/secrets/google/key.json
          volumes:
          - name: scripts-volume
            configMap:
              name: {configmap_name}
          - name: gcp-sa-key
            secret:
              secretName: gcp-creds
              items:
              - key: GCP_SERVICE_ACCOUNT_KEY
                path: key.json
    """)

    try:
        # Create a single ConfigMap with both scripts
        print(f"📜 Creating ConfigMap '{configmap_name}' for runner scripts...")
        run(
            f"kubectl create configmap {configmap_name} -n intellithing "
            f"--from-literal=runner.py='{python_runner_script}' "
            f"--from-literal=status.sql='{sql_script_content}'"
        )
        
        # Apply the Job manifest
        print(f"🚀 Deploying Kubernetes Job '{job_name}'...")
        run(f"echo '{job_yaml}' | kubectl apply -f -")

        # --- 5. Wait for Job and Verify ---
        print(f"⏳ Waiting for Job '{job_name}' to complete... (Timeout: 5 minutes)")
        run(f"kubectl wait --for=condition=complete job/{job_name} -n intellithing --timeout=5m")
        
        print("✅ Job completed. Verifying logs for success message...")
        pod_name = run(f"kubectl get pods -n intellithing --selector=job-name={job_name} -o jsonpath='{{.items[0].metadata.name}}'").stdout.strip()
        logs = run(f"kubectl logs {pod_name} -n intellithing").stdout

        if "✅✅✅ SQL SCRIPT EXECUTED SUCCESSFULLY ✅✅✅" in logs:
            print("🎉 SQL initialization successful!")
            status.complete("execute_sql_job")
        else:
            print("❌ Job completed, but success message was not found in logs."); print("--- POD LOGS ---"); print(logs); print("--- END POD LOGS ---")
            raise RuntimeError("SQL Job execution failed. Check logs for details.")

    finally:
        # --- 6. Cleanup ---
        print("🧹 Cleaning up Kubernetes resources...")
        run(f"kubectl delete job {job_name} -n intellithing --ignore-not-found=true", check=False)
        run(f"kubectl delete configmap {configmap_name} -n intellithing --ignore-not-found=true", check=False)