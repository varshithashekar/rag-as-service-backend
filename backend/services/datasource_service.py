import os
import re

from backend.repositories import datasource_repository
from backend.repositories import file_status_repository

from backend.integrations.oci_storage_client import upload_object
from backend.integrations.oci_storage_client import object_storage

from backend.config import OCI_NAMESPACE, OCI_BUCKET_NAME


# ---------------------------------------------------------
# Upload File Service
# ---------------------------------------------------------
def upload_file(folder_name, file):

    # Step 1: create datasource in DB
    base_name = (folder_name or "").strip()

    if not base_name:
        base_name = "datasource"

    datasource_id = datasource_repository.create_datasource(
        base_name
    )

    # Step 2: folder name using datasource ID
    folder = _build_folder_name(
        base_name=base_name,
        datasource_id=datasource_id
    )

    object_name = f"{folder}/{file.filename}"

    # Step 3: calculate file size
    file_content = file.file.read()
    file_size = len(file_content)

    file.file.seek(0)

    # Step 4: upload file to OCI bucket
    upload_object(object_name, file.file)

    # Step 5: insert metadata in DB
    file_status_repository.insert_file_record(
        datasource_id,
        file.filename,
        object_name,
        os.path.splitext(file.filename)[1].replace(".", ""),
        file_size
    )

    return {
        "datasource_id": datasource_id,
        "file_name": file.filename,
        "folder": folder,
        "path": object_name
    }


# ---------------------------------------------------------
# List All Files in Bucket
# ---------------------------------------------------------
def list_bucket_files():

    response = object_storage.list_objects(
        namespace_name=OCI_NAMESPACE,
        bucket_name=OCI_BUCKET_NAME
    )

    files = []

    for obj in response.data.objects:

        path = obj.name

        if "/" in path:
            folder, file_name = path.split("/", 1)
        else:
            folder = ""
            file_name = path

        files.append({
            "folder": folder,
            "file_name": file_name,
            "path": path
        })

    return files


# ---------------------------------------------------------
# Get Files for Specific Folder
# ---------------------------------------------------------
def get_files_by_folder(folder_name):

    prefix = f"{folder_name}/"

    response = object_storage.list_objects(
        namespace_name=OCI_NAMESPACE,
        bucket_name=OCI_BUCKET_NAME,
        prefix=prefix
    )

    files = []

    for obj in response.data.objects:

        path = obj.name
        file_name = path.split("/")[-1]

        files.append({
            "folder": folder_name,
            "file_name": file_name,
            "path": path
        })

    return files


# ---------------------------------------------------------
# Validate file include/exclude regex filters
# ---------------------------------------------------------
def validate_file_filters(
    include_regex=None,
    exclude_regex=None,
    folder_name=None
):

    try:
        include_pattern = re.compile(include_regex) if include_regex else None
    except re.error as exc:
        raise ValueError(f"Invalid include regex: {exc}") from exc

    try:
        exclude_pattern = re.compile(exclude_regex) if exclude_regex else None
    except re.error as exc:
        raise ValueError(f"Invalid exclude regex: {exc}") from exc

    list_kwargs = {
        "namespace_name": OCI_NAMESPACE,
        "bucket_name": OCI_BUCKET_NAME
    }

    if folder_name:
        list_kwargs["prefix"] = f"{folder_name}/"

    response = object_storage.list_objects(**list_kwargs)

    included_files = []
    excluded_files = []

    for obj in response.data.objects:

        path = obj.name

        if "/" in path:
            folder, file_name = path.split("/", 1)
        else:
            folder = ""
            file_name = path

        file_info = {
            "folder": folder,
            "file_name": file_name,
            "path": path
        }

        matches_include = (
            include_pattern.search(path)
            if include_pattern else True
        )

        matches_exclude = (
            exclude_pattern.search(path)
            if exclude_pattern else False
        )

        if matches_exclude:
            file_info["reason"] = "exclude_regex"
            excluded_files.append(file_info)
            continue

        if matches_include:
            included_files.append(file_info)
        else:
            file_info["reason"] = "include_regex"
            excluded_files.append(file_info)

    return {
        "included_files": included_files,
        "excluded_files": excluded_files,
        "summary": {
            "evaluated_files": len(response.data.objects),
            "included": len(included_files),
            "excluded": len(excluded_files)
        }
    }


def _build_folder_name(base_name, datasource_id):

    sanitized = re.sub(r"[^A-Za-z0-9_-]+", "_", base_name)
    sanitized = sanitized.strip("_")

    if not sanitized:
        sanitized = "datasource"

    folder = f"{sanitized}_{datasource_id}"

    return folder
