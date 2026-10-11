from http import HTTPStatus

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from open_data_pipeline.db.session import get_db
from open_data_pipeline.features.imports.exceptions import (
    INVALID_FILE_EXCEPTION,
    InvalidFileException,
)
from open_data_pipeline.features.imports.schemas import ImportResponse
from open_data_pipeline.features.imports.service import import_data

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
