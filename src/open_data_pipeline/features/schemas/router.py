from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from open_data_pipeline.db.session import get_db
from open_data_pipeline.features.schemas.schemas import CreateSchemaRequest
from open_data_pipeline.features.schemas.service import create_schema

router = APIRouter(prefix="/schemas", tags=["schemas"])


@router.post(path="/")
def create_schema_endpoint(payload: CreateSchemaRequest, db: Session = Depends(get_db)):
    return create_schema(db=db, payload=payload)
