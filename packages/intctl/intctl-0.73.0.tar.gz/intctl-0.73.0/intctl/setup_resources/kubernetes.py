import os
import subprocess
import time
from intctl.status import StatusManager
from .utils import Spinner


def run(cmd: str) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)




def ensure_namespace_exists(namespace: str) -> None:
    result = run(f"kubectl get namespace {namespace}")
    if result.returncode != 0:
        print(f"🔧 Namespace '{namespace}' not found. Creating it...")
        create = run(f"kubectl create namespace {namespace}")
        if create.returncode != 0:
            print("❌ Failed to create namespace.")
            print(create.stderr)
            raise RuntimeError("Namespace creation failed.")
        else:
            print(f"✅ Namespace '{namespace}' created.")



def create_kubernetes_cluster(cfg: dict, status: StatusManager) -> None:
    status.start("kubernetes")
    project = cfg["project_id"]
    region = cfg["region"]
    workspace = cfg["workspace_uuid"]
    cluster_name = f"int-{workspace}".lower()

    print(f"🔍 Checking if Kubernetes cluster '{cluster_name}' exists...")

    with Spinner(f"Checking if GKE cluster '{cluster_name}' exists..."):
        exists = run(
            f"gcloud container clusters describe {cluster_name} "
            f"--region={region} --project={project}"
        )
    if exists.returncode == 0:
        print(f"✅ Cluster '{cluster_name}' already exists in region '{region}'.")
        ensure_namespace_exists("intellithing")
        apply_rbac()
        status.complete("kubernetes")
        return


    print(f"🚀 Creating Autopilot GKE cluster '{cluster_name}' in {region}...")

    with Spinner(f"Creating GKE cluster '{cluster_name}'..."):
        result = run(
            f"gcloud container clusters create-auto {cluster_name} "
            f"--region={region} --project={project}"
        )

    if result.returncode == 0:
        print(f"✅ Cluster '{cluster_name}' created.")
        apply_rbac()
        status.complete("kubernetes")
        return

    print("❌ Failed to create GKE cluster.")
    print(result.stderr.strip())

    print(f"""
🔐 You might not have permission, or there may be quota/policy issues.

Please create the cluster manually using the following command:

  gcloud container clusters create-auto {cluster_name} \\
      --region={region} --project={project}

⏳ Waiting until the cluster '{cluster_name}' is created...
""")

    # Retry loop to poll for existence
    while True:
        time.sleep(10)
        with Spinner("Polling for GKE cluster creation..."):
            check = run(
                f"gcloud container clusters describe {cluster_name} "
                f"--region={region} --project={project}"
            )
        if check.returncode == 0:
            print(f"✅ Cluster '{cluster_name}' has been created.")
            ensure_namespace_exists("intellithing")
            apply_rbac()
            break
        else:
            print("⏳ Still waiting for cluster...")


    status.complete("kubernetes")


import json

def get_service_accounts_to_bind() -> list[tuple[str, str]]:
    result = run("kubectl get serviceaccounts --all-namespaces -o json")
    if result.returncode != 0:
        raise RuntimeError("Failed to fetch service accounts")

    sa_data = json.loads(result.stdout)
    to_bind = []

    for item in sa_data["items"]:
        name = item["metadata"]["name"]
        namespace = item["metadata"]["namespace"]

        # Optional: filter only namespaces you're watching
        if namespace in {"default", "intellithing"} and name == "default":
            to_bind.append((namespace, name))

    return to_bind


def apply_rbac():
    subjects = get_service_accounts_to_bind()

    if not subjects:
        raise RuntimeError("❌ No service accounts found to bind RBAC to.")

    print(f"🔐 Applying RBAC for service accounts: {subjects}")

    # Build YAML for all subjects
    subject_entries = "\n".join([
        f"""  - kind: ServiceAccount
    name: {name}
    namespace: {namespace}""" for namespace, name in subjects
    ])

    rbac_manifest = f"""
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: proxy-service-reader
rules:
  - apiGroups: [""]
    resources: ["services"]
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: proxy-service-reader-binding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: proxy-service-reader
subjects:
{subject_entries}
"""
    result = subprocess.run(
        ["kubectl", "apply", "-f", "-"],
        input=rbac_manifest,
        text=True,
        capture_output=True
    )

    if result.returncode == 0:
        print("✅ RBAC roles applied successfully.")
    else:
        print("❌ Failed to apply RBAC roles.")
        print(result.stderr)
        raise RuntimeError("RBAC setup failed.")
