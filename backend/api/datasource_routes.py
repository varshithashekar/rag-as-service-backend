from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel

from backend.services import datasource_service
from backend.core.response import success_response, error_response

router = APIRouter(prefix="/datasources", tags=["datasources"])


class FilterValidationRequest(BaseModel):
    include_regex: Optional[str] = None
    exclude_regex: Optional[str] = None
    folder_name: Optional[str] = None


# Upload file
@router.post("/upload")
async def upload_file(
    folder_name: str = Form(...),
    file: UploadFile = File(...)
):

    try:

        result = datasource_service.upload_file(
            folder_name,
            file
        )

        return success_response(result)

    except Exception as exc:

        return error_response(
            "UPLOAD_FAILED",
            str(exc)
        )


# List all bucket files
@router.get("/files")
def get_all_files():

    try:

        files = datasource_service.list_bucket_files()

        return success_response(files)

    except Exception as exc:

        return error_response(
            "LIST_FILES_FAILED",
            str(exc)
        )


# Get files inside a datasource folder
@router.get("/files/{folder_name}")
def get_files_by_folder(folder_name: str):

    try:

        files = datasource_service.get_files_by_folder(
            folder_name
        )

        return success_response(files)

    except Exception as exc:

        return error_response(
            "FOLDER_FILES_FAILED",
            str(exc)
        )


# Validate include/exclude regex filters
@router.post("/filters/validate")
def validate_filters(payload: FilterValidationRequest):

    try:

        result = datasource_service.validate_file_filters(
            include_regex=payload.include_regex,
            exclude_regex=payload.exclude_regex,
            folder_name=payload.folder_name
        )

        return success_response(result)

    except ValueError as exc:

        return error_response(
            "INVALID_REGEX",
            str(exc)
        )

    except Exception as exc:

        return error_response(
            "FILTER_VALIDATION_FAILED",
            str(exc)
        )
