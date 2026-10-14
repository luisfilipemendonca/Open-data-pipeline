from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from open_data_pipeline.db.session import get_db
from open_data_pipeline.features.schemas.schemas import (
    CreateSchemaRequest,
    CreateSchemaResponse,
)
from open_data_pipeline.features.schemas.service import create_schema

router = APIRouter(prefix="/schemas", tags=["schemas"])


@router.post(path="/", response_model=CreateSchemaResponse)
def create_schema_endpoint(
    payload: CreateSchemaRequest, db: Session = Depends(get_db)
) -> CreateSchemaResponse:
    return create_schema(db=db, payload=payload)
