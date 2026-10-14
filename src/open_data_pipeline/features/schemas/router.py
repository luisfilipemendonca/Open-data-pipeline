from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from open_data_pipeline.api.schemas import PaginatedResponse
from open_data_pipeline.db.session import get_db
from open_data_pipeline.features.schemas.schemas import (
    CreateSchemaRequest,
    GetSchemaResponse,
    SchemaResponse,
)
from open_data_pipeline.features.schemas.service import create_schema, get_schemas

router = APIRouter(prefix="/schemas", tags=["schemas"])


@router.post(path="/", response_model=SchemaResponse)
def create_schema_endpoint(
    payload: CreateSchemaRequest, db: Session = Depends(get_db)
) -> SchemaResponse:
    return create_schema(db=db, payload=payload)


@router.get(path="/", response_model=PaginatedResponse[GetSchemaResponse])
def get_schemas_endpoint(
    db: Session = Depends(get_db),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
) -> PaginatedResponse[GetSchemaResponse]:
    return get_schemas(db=db, page=page, page_size=page_size)
