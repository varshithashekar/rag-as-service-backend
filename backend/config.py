import os
from dotenv import load_dotenv

load_dotenv()

ORACLE_USER = os.getenv("ORACLE_USER")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")
ORACLE_DSN = os.getenv("ORACLE_DSN")

OCI_TENANCY_OCID = os.getenv("OCI_TENANCY_OCID")
OCI_USER_OCID = os.getenv("OCI_USER_OCID")
OCI_REGION = os.getenv("OCI_REGION")
OCI_FINGERPRINT = os.getenv("OCI_FINGERPRINT")
OCI_PRIVATE_KEY_PATH = os.getenv("OCI_PRIVATE_KEY_PATH")

OCI_BUCKET_NAME = os.getenv("OCI_BUCKET_NAME")
OCI_NAMESPACE = os.getenv("OCI_NAMESPACE")