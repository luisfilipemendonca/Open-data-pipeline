from http import HTTPStatus

from fastapi import APIRouter, Depends, File, HTTPException, Path, Query, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from open_data_pipeline.db.session import get_db
from open_data_pipeline.features.imports.exceptions import (
    IMPORT_NOT_FOUND_EXCEPTION,
    INVALID_FILE_DUPLICATED_HEADER_EXCEPTION,
    INVALID_FILE_EXCEPTION,
    INVALID_FILE_HEADERS_EXCEPTION,
    ImportNotFoundException,
    InvalidFileDuplicatedHeaderException,
    InvalidFileException,
    InvalidFileHeadersException,
)
from open_data_pipeline.features.imports.schemas import (
    ImportPreviewResponse,
    ImportResponse,
    ImportsResponse,
)
from open_data_pipeline.features.imports.service import (
    delete_import,
    download_import_file,
    get_imports,
    import_data,
    import_data_preview,
)

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
    except InvalidFileDuplicatedHeaderException:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=INVALID_FILE_DUPLICATED_HEADER_EXCEPTION,
        )


@router.get("/{import_id}/download")
def download_import_file_endpoint(
    db: Session = Depends(get_db),  # noqa: B008
    import_id: int = Path(ge=1),
) -> FileResponse:
    try:
        file_path, file_name = download_import_file(import_id=import_id, db=db)

    except ImportNotFoundException:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=IMPORT_NOT_FOUND_EXCEPTION
        )

    return FileResponse(path=file_path, filename=file_name, media_type="text/csv")


@router.delete("/{import_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_import_endpoint(
    db: Session = Depends(get_db), import_id: int = Path(ge=1)
) -> None:
    try:
        delete_import(import_id=import_id, db=db)
    except ImportNotFoundException:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=IMPORT_NOT_FOUND_EXCEPTION
        )


@router.get("/", response_model=ImportsResponse)
def get_imports_endpoint(
    db: Session = Depends(get_db),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
) -> ImportsResponse:
    return get_imports(db=db, page=page, page_size=page_size)
