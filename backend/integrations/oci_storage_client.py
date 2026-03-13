import os
import oci
from dotenv import load_dotenv

load_dotenv()

config = {
    "user": os.getenv("OCI_USER_OCID"),
    "fingerprint": os.getenv("OCI_FINGERPRINT"),
    "tenancy": os.getenv("OCI_TENANCY_OCID"),
    "region": os.getenv("OCI_REGION"),
    "key_file": os.getenv("OCI_PRIVATE_KEY_PATH")
}

oci.config.validate_config(config)

object_storage = oci.object_storage.ObjectStorageClient(config)


def upload_object(object_name, file_data):

    namespace = os.getenv("OCI_NAMESPACE")
    bucket_name = os.getenv("OCI_BUCKET_NAME")

    object_storage.put_object(
        namespace_name=namespace,
        bucket_name=bucket_name,
        object_name=object_name,
        put_object_body=file_data
    )