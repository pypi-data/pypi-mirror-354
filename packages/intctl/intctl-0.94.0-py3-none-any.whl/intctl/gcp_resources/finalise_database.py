# intctl/setup_resources/finalise_database.py

import asyncio
import os
import time
from pathlib import Path
import traceback # FIXED: Import the traceback module

# FIXED: Import IPTypes alongside Connector
from google.cloud.sql.connector import Connector, IPTypes

from google.auth.transport.requests import Request as AuthRequest
from google.cloud import secretmanager_v1
from google.auth import default
import asyncpg

from intctl.status import StatusManager
from intctl.utils.pathing import scripts_path
from .utils import Spinner


def finalise_database(cfg: dict, status: StatusManager) -> None:
    # --- NO CHANGES in the main body of the function ---
    status.start("cloudsql_instance_check")
    # ... (all the preceding steps are correct) ...
    workspace_uuid = cfg["workspace_uuid"]
    organization_uuid = cfg["organization_uuid"]
    region = cfg["region"]
    project_id = cfg["project_id"]
    credentials, _ = default()
    credentials.refresh(AuthRequest())
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
    status.start("fetch_db_credentials")
    def access_secret(name: str) -> str:
        client = secretmanager_v1.SecretManagerServiceClient(credentials=credentials)
        secret_name = f"projects/{project_id}/secrets/{name}/versions/latest"
        return client.access_secret_version(request={"name": secret_name}).payload.data.decode()
    try:
        user_secret = f"{organization_uuid}-{workspace_uuid}-pg-username"
        pass_secret = f"{organization_uuid}-{workspace_uuid}-pg-password"
        pg_user = access_secret(user_secret)
        pg_pass = access_secret(pass_secret)
        print("🔐 Fetched DB credentials from Secret Manager.")
        status.complete("fetch_db_credentials")
    except Exception as e:
        print(f"❌ Failed to fetch secrets: {e}")
        status.fail("fetch_db_credentials")
        return
    status.start("load_sql_script")
    sql_path = scripts_path("status.sql")
    if not sql_path.exists():
        print(f"❌ SQL file not found at {sql_path}")
        status.fail("load_sql_script")
        return
    try:
        sql = sql_path.read_text()
        print("📄 Loaded SQL script.")
        status.complete("load_sql_script")
    except Exception as e:
        print(f"❌ Failed to read SQL script: {e}")
        status.fail("load_sql_script")
        return
    status.start("run_sql_script")
    async def execute_sql():
        connector = Connector()
        conn: asyncpg.Connection = None
        try:
            instance_connection_name = f"{project_id}:{region}:{db_name}"
            conn = await connector.connect_async(
                instance_connection_name,
                "asyncpg",
                user=pg_user,
                password=pg_pass,
                db=db_name,
                ip_type=IPTypes.PRIVATE
            )
            await conn.execute(sql)
        finally:
            if conn:
                await conn.close()
            await connector.close_async()

    try:
        try:
            asyncio.run(execute_sql())
        except RuntimeError as e:
            if "already running" in str(e):
                print("⚠️ Event loop already running, falling back to manual scheduling...")
                import nest_asyncio
                nest_asyncio.apply()
                loop = asyncio.get_event_loop()
                loop.run_until_complete(execute_sql())
            else:
                raise
        print("✅ SQL script executed successfully.")
        status.complete("run_sql_script")
    except Exception as e:
        # --- THIS BLOCK IS NOW FIXED TO BE MORE INFORMATIVE ---
        print(f"❌ SQL execution failed. The error was suppressed but is now visible below.")
        print(f"   Exception Type: {type(e)}")
        print(f"   Exception Details: {e}")
        print("-" * 20 + " FULL TRACEBACK " + "-" * 20)
        traceback.print_exc() # This will print the full error stack to the console
        print("-" * 58)
        # --- END OF FIX ---
        status.fail("run_sql_script")