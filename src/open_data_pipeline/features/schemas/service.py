from math import ceil

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from open_data_pipeline.api.schemas import PaginatedResponse, PaginationResponse
from open_data_pipeline.features.imports.schemas import ImportPreviewField
from open_data_pipeline.features.schemas.exceptions import NotFoundSchemaException
from open_data_pipeline.features.schemas.models import Schema, SchemaField
from open_data_pipeline.features.schemas.schemas import (
    CreateSchemaRequest,
    DetailsSchemaResponse,
    GetSchemaResponse,
    OutdatedSchemaCopiesResponse,
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


def get_schema_details(db: Session, schema_id: int) -> DetailsSchemaResponse:
    schema = db.get(Schema, schema_id, options=[joinedload(Schema.fields)])

    if not schema or not schema.is_base:
        raise NotFoundSchemaException()

    outdated_versions_count = (
        db.scalar(
            select(func.count())
            .select_from(Schema)
            .where(
                Schema.parent_schema_id == schema_id,
                Schema.parent_version < schema.version,
            )
        )
        or 0
    )

    return DetailsSchemaResponse(
        id=schema.id,
        name=schema.name or "",
        version=schema.version,
        created_at=schema.created_at,
        updated_at=schema.updated_at,
        outdated_count=outdated_versions_count,
        fields=[
            ImportPreviewField(
                name=field.name,
                inferred_type=field.field_type,
                required=field.required,
            )
            for field in schema.fields
        ],
    )


def get_schema_outdated_copies(
    db: Session, page: int, page_size: int, schema_id: int
) -> PaginatedResponse[OutdatedSchemaCopiesResponse]:
    schema = db.get(Schema, schema_id)

    if not schema or not schema.is_base:
        raise NotFoundSchemaException()

    outdated_copies_statement = (
        select(Schema)
        .where(
            Schema.parent_schema_id == schema_id, Schema.parent_version < schema.version
        )
        .options(joinedload(Schema.import_record))
        .order_by(Schema.updated_at.desc(), Schema.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )

    outdated_copies = db.scalars(outdated_copies_statement).unique().all()

    outdated_copies_count = (
        db.scalar(
            select(func.count())
            .select_from(Schema)
            .where(
                Schema.parent_schema_id == schema_id,
                Schema.parent_version < schema.version,
            )
        )
        or 0
    )

    total_pages = ceil(outdated_copies_count / page_size)
    has_next_page = total_pages > page

    return PaginatedResponse(
        data=[
            OutdatedSchemaCopiesResponse(
                id=outdated_copy.id,
                version=outdated_copy.parent_version or 0,
                created_at=outdated_copy.created_at,
                updated_at=outdated_copy.updated_at,
                import_id=outdated_copy.import_record.id
                if outdated_copy.import_record
                else None,
                import_file_name=outdated_copy.import_record.file_name
                if outdated_copy.import_record
                else None,
            )
            for outdated_copy in outdated_copies
        ],
        pagination=PaginationResponse(
            page=page,
            total=outdated_copies_count,
            total_pages=total_pages,
            page_size=page_size,
            has_next_page=has_next_page,
        ),
    )
