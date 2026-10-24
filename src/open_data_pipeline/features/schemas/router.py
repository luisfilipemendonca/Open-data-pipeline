from typing import Annotated

from fastapi import APIRouter, Path

from open_data_pipeline.api.dependencies import DbDep, PaginationDep
from open_data_pipeline.api.schemas import PaginatedResponse
from open_data_pipeline.features.schemas.schemas import (
    CreateSchemaPayload,
    DetailsSchemaResponse,
    GetSchemaResponse,
    OutdatedSchemaCopiesResponse,
    SchemaResponse,
    UpdateSchemaPayload,
)
from open_data_pipeline.features.schemas.service import (
    create_schema,
    get_schema_details,
    get_schema_outdated_copies,
    get_schemas,
    update_schema,
)

router = APIRouter(prefix="/schemas", tags=["schemas"])


@router.post(path="/", response_model=SchemaResponse)
def create_schema_endpoint(payload: CreateSchemaPayload, db: DbDep) -> SchemaResponse:
    return create_schema(db=db, payload=payload)


@router.get(path="/", response_model=PaginatedResponse[GetSchemaResponse])
def get_schemas_endpoint(
    pagination: PaginationDep,
    db: DbDep,
) -> PaginatedResponse[GetSchemaResponse]:
    return get_schemas(db=db, page=pagination.page, page_size=pagination.page_size)


@router.get("/{schema_id}", response_model=DetailsSchemaResponse)
def get_schema_details_endpoint(
    db: DbDep, schema_id: Annotated[int, Path(ge=1)]
) -> DetailsSchemaResponse:
    return get_schema_details(db=db, schema_id=schema_id)


@router.get(
    "/{schema_id}/outdated_copies",
    response_model=PaginatedResponse[OutdatedSchemaCopiesResponse],
)
def get_schema_outdated_copies_endpoint(
    pagination: PaginationDep,
    db: DbDep,
    schema_id: Annotated[int, Path(ge=1)],
) -> PaginatedResponse[OutdatedSchemaCopiesResponse]:
    return get_schema_outdated_copies(
        db=db,
        page=pagination.page,
        page_size=pagination.page_size,
        schema_id=schema_id,
    )


@router.put("/{schema_id}", response_model=GetSchemaResponse)
def update_schema_endpoint(
    payload: UpdateSchemaPayload,
    db: DbDep,
    schema_id: Annotated[int, Path(ge=1)],
) -> GetSchemaResponse:
    return update_schema(db=db, schema_id=schema_id, payload=payload)
