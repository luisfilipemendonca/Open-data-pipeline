from http import HTTPStatus

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Path,
    Query,
    UploadFile,
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from open_data_pipeline.api.pagination import PaginationDep
from open_data_pipeline.api.schemas import PaginatedResponse
from open_data_pipeline.db.session import get_db
from open_data_pipeline.features.imports.exceptions import (
    ImportRowValidationException,
)
from open_data_pipeline.features.imports.schemas import (
    ImportPreviewResponse,
    ImportResponse,
    ImportRowResponse,
    UpdateImportRowBody,
)
from open_data_pipeline.features.imports.service import (
    delete_import,
    delete_import_row,
    download_import_file,
    get_import_rows,
    get_imports,
    import_data,
    import_data_preview,
    process_import,
    update_import_row,
)

router = APIRouter(prefix="/imports", tags=["imports"])


@router.post("/", response_model=ImportResponse, status_code=HTTPStatus.ACCEPTED)
def import_data_endpoint(
    schema_id: int = Form(),
    file: UploadFile = File(...),  # noqa: B008
    db: Session = Depends(get_db),  # noqa: B008
) -> ImportResponse:
    return import_data(file=file, db=db, schema_id=schema_id)


@router.post(
    "/preview", response_model=ImportPreviewResponse, status_code=HTTPStatus.CREATED
)
def import_data_preview_endpoint(
    db: Session = Depends(get_db), file: UploadFile = File(...)
) -> ImportPreviewResponse:
    return import_data_preview(file=file, db=db)


@router.get("/{import_id}/download")
def download_import_file_endpoint(
    db: Session = Depends(get_db),  # noqa: B008
    import_id: int = Path(ge=1),
) -> FileResponse:
    file_path, file_name = download_import_file(import_id=import_id, db=db)
    return FileResponse(path=file_path, filename=file_name, media_type="text/csv")


@router.delete("/{import_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_import_endpoint(
    db: Session = Depends(get_db), import_id: int = Path(ge=1)
) -> None:
    delete_import(import_id=import_id, db=db)


@router.get("/", response_model=PaginatedResponse[ImportResponse])
def get_imports_endpoint(
    pagination: PaginationDep,
    db: Session = Depends(get_db),
) -> PaginatedResponse[ImportResponse]:
    return get_imports(db=db, page=pagination.page, page_size=pagination.page_size)


@router.post("/{import_id}/process", response_model=ImportResponse)
def process_import_endpoint(db: Session = Depends(get_db), import_id: int = Path(ge=1)):
    return process_import(db=db, import_id=import_id)


@router.get("/{import_id}/rows", response_model=PaginatedResponse[ImportRowResponse])
def get_import_rows_endpoint(
    pagination: PaginationDep,
    db: Session = Depends(get_db),
    import_id: int = Path(ge=1),
    is_valid: bool | None = Query(default=None),
) -> PaginatedResponse[ImportRowResponse]:
    return get_import_rows(
        db=db,
        import_id=import_id,
        page=pagination.page,
        page_size=pagination.page_size,
        is_valid=is_valid,
    )


@router.put("/{import_id}/rows/{row_id}", response_model=ImportRowResponse)
def update_import_row_endpoint(
    payload: list[UpdateImportRowBody],
    db: Session = Depends(get_db),
    import_id: int = Path(ge=1),
    row_id: int = Path(ge=1),
) -> ImportRowResponse:
    try:
        return update_import_row(
            db=db, import_id=import_id, row_id=row_id, payload=payload
        )
    except ImportRowValidationException as exc:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=[error.model_dump() for error in exc.errors],
        )


@router.delete("/{import_id}/rows/{row_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_import_row_endpoint(
    db: Session = Depends(get_db), import_id: int = Path(ge=1), row_id: int = Path(ge=1)
) -> None:
    delete_import_row(db=db, import_id=import_id, row_id=row_id)
