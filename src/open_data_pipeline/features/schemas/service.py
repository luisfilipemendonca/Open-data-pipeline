from math import ceil

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from open_data_pipeline.api.schemas import PaginatedResponse, PaginationResponse
from open_data_pipeline.features.schemas.models import Schema, SchemaField
from open_data_pipeline.features.schemas.schemas import (
    CreateSchemaRequest,
    GetSchemaResponse,
    SchemaFieldsResponse,
    SchemaResponse,
)


def create_schema(db: Session, payload: CreateSchemaRequest) -> SchemaResponse:
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

    return SchemaResponse(
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
        created_at=schema.created_at,
        updated_at=schema.updated_at,
    )


def get_schemas(
    db: Session, page: int, page_size: int
) -> PaginatedResponse[GetSchemaResponse]:
    statement = (
        select(Schema)
        .where(Schema.is_base)
        .order_by(Schema.updated_at.desc(), Schema.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )

    schemas = db.scalars(statement).all()

    schemas_count = (
        db.scalar(select(func.count()).select_from(Schema).where(Schema.is_base)) or 0
    )

    total_pages = ceil(schemas_count / page_size)
    has_next_page = total_pages > page

    return PaginatedResponse(
        data=[
            GetSchemaResponse(
                id=schema.id,
                name=schema.name or "",
                version=schema.version,
                created_at=schema.created_at,
                updated_at=schema.updated_at,
            )
            for schema in schemas
        ],
        pagination=PaginationResponse(
            page=page,
            page_size=page_size,
            has_next_page=has_next_page,
            total=schemas_count,
            total_pages=total_pages,
        ),
    )
