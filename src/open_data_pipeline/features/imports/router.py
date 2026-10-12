from http import HTTPStatus

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from open_data_pipeline.db.session import get_db
from open_data_pipeline.features.imports.exceptions import (
    INVALID_FILE_EXCEPTION,
    INVALID_FILE_HEADERS_EXCEPTION,
    InvalidFileException,
    InvalidFileHeadersException,
)
from open_data_pipeline.features.imports.schemas import (
    ImportPreviewResponse,
    ImportResponse,
)
from open_data_pipeline.features.imports.service import import_data, import_data_preview

router = APIRouter(prefix="/imports", tags=["imports"])


@router.post("/", response_model=ImportResponse, status_code=HTTPStatus.ACCEPTED)
def import_data_endpoint(
    file: UploadFile = File(...),  # noqa: B008
    db: Session = Depends(get_db),  # noqa: B008
) -> ImportResponse:
    try:
        return import_data(file=file, db=db)
    except InvalidFileException:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=INVALID_FILE_EXCEPTION
        )


@router.post(
    "/preview", response_model=ImportPreviewResponse, status_code=HTTPStatus.CREATED
)
def import_data_preview_endpoint(
    db: Session = Depends(get_db), file: UploadFile = File(...)
) -> ImportPreviewResponse:
    try:
        return import_data_preview(file=file, db=db)
    except InvalidFileException:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=INVALID_FILE_EXCEPTION
        )
    except InvalidFileHeadersException:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=INVALID_FILE_HEADERS_EXCEPTION
        )
