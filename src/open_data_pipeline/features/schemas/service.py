from sqlalchemy.orm import Session

from open_data_pipeline.features.schemas.models import Schema, SchemaField
from open_data_pipeline.features.schemas.schemas import (
    CreateSchemaRequest,
    CreateSchemaResponse,
    SchemaFieldsResponse,
)


def create_schema(db: Session, payload: CreateSchemaRequest) -> CreateSchemaResponse:
    schema = Schema(
        name=payload.name,
        is_base=True,
        fields=[
            SchemaField(
                name=field.name, field_type=field.field_type, required=field.required
            )
            for field in payload.fields
        ],
    )

    db.add(schema)
    db.commit()
    db.refresh(schema)

    return CreateSchemaResponse(
        id=schema.id,
        parent_schema_id=schema.parent_schema_id,
        name=schema.name,
        is_base=schema.is_base,
        fields=[
            SchemaFieldsResponse(
                id=field.id,
                name=field.name,
                field_type=field.field_type,
                required=field.required,
            )
            for field in schema.fields
        ],
        import_record=None,
        parent_version=None,
        version=schema.version,
    )
