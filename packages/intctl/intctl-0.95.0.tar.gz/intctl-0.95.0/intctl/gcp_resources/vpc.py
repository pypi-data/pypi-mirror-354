# intctl/setup_resources/vpc.py

import subprocess
import time
import json
import typer
from intctl.status import StatusManager
from .utils import Spinner

TEMP_SQL_FIREWALL_RULE_NAME = "temp-allow-intctl-db-setup"


def run(cmd: str) -> subprocess.CompletedProcess:
    """A helper function to run shell commands."""
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)


def create_temp_sql_firewall_rule(cfg: dict, status: StatusManager):
    """
    Creates a TEMPORARY firewall rule to allow ingress from Google's Private Service
    Access range, enabling the Cloud SQL Connector to work from outside the VPC.
    """
    project = cfg["project_id"]
    workspace = cfg["workspace_uuid"]
    vpc_name = f"intellithing-vpc-{workspace}".lower()
    source_range = "35.199.192.0/19" # Documented range for Google's internal access

    print(f"🔥 Creating TEMPORARY firewall rule '{TEMP_SQL_FIREWALL_RULE_NAME}'...")
    with Spinner(f"Creating firewall rule '{TEMP_SQL_FIREWALL_RULE_NAME}'..."):
        # This command is idempotent due to the nature of the main setup flow,
        # but if run in isolation, an --ignore-existing flag would be useful.
        result = run(
            f"gcloud compute firewall-rules create {TEMP_SQL_FIREWALL_RULE_NAME} "
            f"--network={vpc_name} "
            f"--allow=tcp:5432 " # PostgreSQL port
            f"--source-ranges={source_range} "
            f"--description='TEMPORARY rule to allow intctl DB setup via SQL Connector' "
            f"--project={project}"
        )

    if result.returncode != 0 and "already exists" not in result.stderr:
        print(f"❌ Failed to create temporary firewall rule '{TEMP_SQL_FIREWALL_RULE_NAME}'.")
        print(result.stderr)
        raise RuntimeError("Temporary firewall rule creation failed.")
    
    print(f"✅ Temporary firewall rule '{TEMP_SQL_FIREWALL_RULE_NAME}' is active.")

def delete_temp_sql_firewall_rule(cfg: dict, status: StatusManager):
    """
    Deletes the TEMPORARY firewall rule used for the initial database setup.
    This is a critical cleanup step for security.
    """
    project = cfg["project_id"]
    print(f"🧹 Deleting TEMPORARY firewall rule '{TEMP_SQL_FIREWALL_RULE_NAME}'...")
    with Spinner(f"Deleting firewall rule '{TEMP_SQL_FIREWALL_RULE_NAME}'..."):
        # --quiet suppresses the 'Are you sure?' prompt, perfect for scripting.
        # This command does not fail if the rule is already gone.
        result = run(
            f"gcloud compute firewall-rules delete {TEMP_SQL_FIREWALL_RULE_NAME} "
            f"--project={project} --quiet"
        )
    
    if result.returncode != 0:
        # This is a warning because the setup can continue, but it's a security risk.
        print(f"⚠️ WARNING: Failed to automatically delete temporary firewall rule '{TEMP_SQL_FIREWALL_RULE_NAME}'.")
        print("   Please delete it manually from the GCP console to secure your VPC.")
        print(result.stderr)
    else:
        print(f"✅ Temporary firewall rule '{TEMP_SQL_FIREWALL_RULE_NAME}' deleted successfully.")

def ensure_vpc_and_peering(cfg: dict, status: StatusManager):
    """
    Ensures a custom VPC, subnet, and VPC peering for Google services exist.

    This function is idempotent and performs the following steps:
    1. Creates a custom VPC network if it doesn't exist.
    2. Creates a subnet within that VPC.
    3. Reserves a global IP range for VPC peering with Google services.
    4. Establishes the VPC peering connection.
    5. Waits until the peering connection is ACTIVE and ready for use.
    """
    status.start("vpc_setup")
    
    project = cfg["project_id"]
    region = cfg["region"]
    workspace = cfg["workspace_uuid"]
    
    # Define dynamic resource names for consistency
    vpc_name = f"intellithing-vpc-{workspace}".lower()
    subnet_name = f"intellithing-subnet-{workspace}".lower()
    peering_range_name = "google-services-range" # A descriptive, static name is fine

    # --- Step 1: Create the VPC Network ---
    print(f"🔍 Checking if VPC '{vpc_name}' exists...")
    if run(f"gcloud compute networks describe {vpc_name} --project={project}").returncode != 0:
        print(f"🔧 Creating VPC '{vpc_name}'...")
        with Spinner(f"Creating VPC '{vpc_name}'..."):
            result = run(f"gcloud compute networks create {vpc_name} --subnet-mode=custom --project={project}")
            if result.returncode != 0:
                print(f"❌ Failed to create VPC '{vpc_name}'.")
                print(result.stderr)
                status.fail("vpc_setup")
                raise RuntimeError("VPC creation failed.")
        print(f"✅ VPC '{vpc_name}' created.")
    else:
        print(f"✅ VPC '{vpc_name}' already exists.")

    # --- Step 2: Create the Subnet ---
    print(f"🔍 Checking if subnet '{subnet_name}' exists...")
    if run(f"gcloud compute networks subnets describe {subnet_name} --region={region} --project={project}").returncode != 0:
        print(f"🔧 Creating subnet '{subnet_name}'...")
        with Spinner(f"Creating subnet '{subnet_name}'..."):
            result = run(
                f"gcloud compute networks subnets create {subnet_name} "
                f"--network={vpc_name} --region={region} --range=10.0.0.0/16 " # A /16 range provides ample space
                f"--project={project}"
            )
            if result.returncode != 0:
                print(f"❌ Failed to create subnet '{subnet_name}'.")
                print(result.stderr)
                status.fail("vpc_setup")
                raise RuntimeError("Subnet creation failed.")
        print(f"✅ Subnet '{subnet_name}' created.")
    else:
        print(f"✅ Subnet '{subnet_name}' already exists.")

    # --- Step 3: Reserve IP Range for Service Networking Peering ---
    print(f"🔍 Checking for reserved IP range '{peering_range_name}'...")
    if run(f"gcloud compute addresses describe {peering_range_name} --global --project={project}").returncode != 0:
        print(f"🔧 Reserving IP range '{peering_range_name}' for Google services...")
        with Spinner("Reserving IP range..."):
            result = run(
                f"gcloud compute addresses create {peering_range_name} "
                f"--global --prefix-length=16 --network={vpc_name} "
                f"--purpose=VPC_PEERING --project={project} "
                f"--description='Peering range for Cloud SQL and other Google services'"
            )
            if result.returncode != 0:
                print("❌ Failed to reserve IP range for VPC peering.")
                print(result.stderr)
                status.fail("vpc_setup")
                raise RuntimeError("IP range reservation failed.")
        print("✅ Reserved IP range for peering.")
    else:
        print(f"✅ Peering IP range '{peering_range_name}' already exists.")
        
    # --- Step 4: Establish VPC Peering Connection ---
    print("🔌 Ensuring VPC peering connection to Google services...")
    with Spinner("Connecting VPC peering..."):
        peer_connect = run(
            f"gcloud services vpc-peerings connect "
            f"--service=servicenetworking.googleapis.com "
            f"--network={vpc_name} --ranges={peering_range_name} --project={project}"
        )
    # This command fails if it already exists, so we check for that specific error.
    if peer_connect.returncode != 0 and "already exists" not in peer_connect.stderr:
        print("❌ Peering connection failed.")
        print(peer_connect.stderr)
        status.fail("vpc_setup")
        raise RuntimeError("VPC peering failed.")
    else:
        print("✅ Peering connection initiated or already exists.")

    # --- Step 5: Wait for Peering to become ACTIVE ---
    print("⏳ Waiting for VPC peering to become ACTIVE...")
    peering_is_active = False
    for i in range(30):  # Wait up to 5 minutes
        with Spinner(f"Checking peering status (attempt {i+1}/30)..."):
            peer_status = run(f"gcloud compute networks peerings list --network={vpc_name} --project={project} --format=json")
            if peer_status.returncode == 0 and peer_status.stdout.strip():
                try:
                    # FIXED: This block now correctly handles the nested JSON structure.
                    networks_list = json.loads(peer_status.stdout)
                    for network_obj in networks_list:
                        for peering in network_obj.get('peerings', []):
                            if peering.get('name') == 'servicenetworking-googleapis-com' and peering.get('state') == 'ACTIVE':
                                peering_is_active = True
                                break
                        if peering_is_active:
                            break
                except json.JSONDecodeError:
                    pass # Ignore parse errors and retry
        
        if peering_is_active:
            print("\n✅ VPC peering is ACTIVE.")
            break
        
        time.sleep(10)

    if not peering_is_active:
        print("\n❌ VPC peering did not become ACTIVE in the allotted time.")
        print("   Please check the GCP console for network peering status.")
        status.fail("vpc_setup")
        raise RuntimeError("VPC peering timed out.")

    status.complete("vpc_setup")