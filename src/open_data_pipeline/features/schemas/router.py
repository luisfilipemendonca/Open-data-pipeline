from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from open_data_pipeline.api.pagination import PaginationDep
from open_data_pipeline.api.schemas import PaginatedResponse
from open_data_pipeline.db.session import get_db
from open_data_pipeline.features.schemas.exceptions import (
    NOT_FOUND_SCHEMA_EXCEPTION,
    NotFoundSchemaException,
)
from open_data_pipeline.features.schemas.schemas import (
    CreateSchemaRequest,
    DetailsSchemaResponse,
    GetSchemaResponse,
    OutdatedSchemaCopiesResponse,
    SchemaResponse,
)
from open_data_pipeline.features.schemas.service import (
    create_schema,
    get_schema_details,
    get_schema_outdated_copies,
    get_schemas,
)

router = APIRouter(prefix="/schemas", tags=["schemas"])


@router.post(path="/", response_model=SchemaResponse)
def create_schema_endpoint(
    payload: CreateSchemaRequest, db: Session = Depends(get_db)
) -> SchemaResponse:
    return create_schema(db=db, payload=payload)


@router.get(path="/", response_model=PaginatedResponse[GetSchemaResponse])
def get_schemas_endpoint(
    pagination: PaginationDep,
    db: Session = Depends(get_db),
) -> PaginatedResponse[GetSchemaResponse]:
    return get_schemas(db=db, page=pagination.page, page_size=pagination.page_size)


@router.get("/{schema_id}", response_model=DetailsSchemaResponse)
def get_schema_details_endpoint(
    db: Session = Depends(get_db), schema_id: int = Path(ge=1)
) -> DetailsSchemaResponse:
    try:
        schema_details = get_schema_details(db=db, schema_id=schema_id)
        return schema_details
    except NotFoundSchemaException:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=NOT_FOUND_SCHEMA_EXCEPTION
        )


@router.get(
    "/{schema_id}/outdated_copies",
    response_model=PaginatedResponse[OutdatedSchemaCopiesResponse],
)
def get_schema_outdated_copies_endpoint(
    pagination: PaginationDep,
    db: Session = Depends(get_db),
    schema_id: int = Path(ge=1),
) -> PaginatedResponse[OutdatedSchemaCopiesResponse]:
    try:
        return get_schema_outdated_copies(
            db=db,
            page=pagination.page,
            page_size=pagination.page_size,
            schema_id=schema_id,
        )
    except NotFoundSchemaException:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=NOT_FOUND_SCHEMA_EXCEPTION
        )
