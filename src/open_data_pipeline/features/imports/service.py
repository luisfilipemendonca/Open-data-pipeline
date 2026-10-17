from math import ceil
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy import exists, func, select
from sqlalchemy.orm import Session, joinedload

from open_data_pipeline.api.schemas import PaginatedResponse, PaginationResponse
from open_data_pipeline.features.imports.csv_reader import (
    CSV_MAX_ROWS_SIZE,
    import_csv,
    read_csv_headers,
    resolve_import_file_path,
    save_upload_file,
)
from open_data_pipeline.features.imports.exceptions import (
    ImportAlreadyProcessedException,
    ImportFileNotFoundException,
    ImportFileTooBigException,
    ImportMissingSchemaException,
    ImportNotFoundException,
    ImportSchemaHeadersMismatchException,
    InvalidFileDuplicatedHeaderException,
    InvalidFileException,
    InvalidFileHeadersException,
)
from open_data_pipeline.features.imports.field_inference import infer_fields
from open_data_pipeline.features.imports.file_validator import validate_file
from open_data_pipeline.features.imports.models import Import, ImportRow, Schema
from open_data_pipeline.features.imports.schemas import (
    GetImportRowResponse,
    ImportPreviewResponse,
    ImportResponse,
    ImportRowDataResponse,
    ImportStatus,
)
from open_data_pipeline.features.imports.validator import validate_row_fields
from open_data_pipeline.features.schemas.exceptions import NotFoundSchemaException
from open_data_pipeline.features.schemas.models import SchemaField
from open_data_pipeline.features.schemas.schemas import SchemaFieldValidator


def import_data(file: UploadFile, db: Session, schema_id: int) -> ImportResponse:
    if not validate_file(file):
        raise InvalidFileException()

    if not schema_id:
        raise ImportMissingSchemaException()

    base_schema = db.scalar(
        select(Schema).where(Schema.id == schema_id).options(joinedload(Schema.fields))
    )

    if not base_schema or not base_schema.is_base:
        raise NotFoundSchemaException()

    file_key, file_path = save_upload_file(file)

    try:
        csv_headers = read_csv_headers(file_path)

        if len(csv_headers) != len(base_schema.fields):
            raise ImportSchemaHeadersMismatchException()

        for field in base_schema.fields:
            if not field.name in csv_headers:
                raise ImportSchemaHeadersMismatchException()

        csv_rows = import_csv(file_path)
        schema_validator_fields = [
            SchemaFieldValidator(
                name=field.name, field_type=field.field_type, required=field.required
            )
            for field in base_schema.fields
        ]

        rows: list[ImportRow] = []
        is_import_valid = True

        for index, csv_row in enumerate(csv_rows):
            if index >= CSV_MAX_ROWS_SIZE - 1:
                raise ImportFileTooBigException()

            is_valid, errors = validate_row_fields(
                row=csv_row, fields=schema_validator_fields
            )

            if not is_valid:
                is_import_valid = False

            rows.append(
                ImportRow(
                    row_number=index + 1,
                    data=csv_row,
                    is_valid=is_valid,
                    errors=[error.model_dump() for error in errors],
                )
            )

        schema_copy = Schema(
            parent_schema_id=base_schema.id,
            parent_version=base_schema.version,
            fields=[
                SchemaField(
                    name=field.name,
                    field_type=field.field_type,
                    required=field.required,
                )
                for field in base_schema.fields
            ],
        )

        import_record = Import(
            status=ImportStatus.COMPLETED
            if is_import_valid
            else ImportStatus.COMPLETED_WITH_ERRORS,
            file_key=file_key,
            file_name=file.filename,
            rows=rows,
            schema=schema_copy,
        )

        db.add(import_record)
        db.commit()
        db.refresh(import_record)

        return ImportResponse(
            import_id=import_record.id,
            status=import_record.status,
            download_url=f"/api/imports/{import_record.id}/download",
            file_name=import_record.file_name,
        )
    except Exception:
        file_path.unlink(missing_ok=True)
        raise


def import_data_preview(file: UploadFile, db: Session) -> ImportPreviewResponse:
    if not validate_file(file):
        raise InvalidFileException()

    file_key, file_path = save_upload_file(file)
    csv_headers = read_csv_headers(file_path)

    if not csv_headers or not all(csv_header.strip() for csv_header in csv_headers):
        file_path.unlink(missing_ok=True)
        raise InvalidFileHeadersException()

    if len({csv_header.strip() for csv_header in csv_headers}) != len(csv_headers):
        file_path.unlink(missing_ok=True)
        raise InvalidFileDuplicatedHeaderException()

    csv_rows = import_csv(file_path)

    fields, rows = infer_fields(csv_headers, csv_rows)

    import_record = Import(
        status=ImportStatus.PENDING,
        file_key=file_key,
        file_name=Path(file.filename).name if file.filename else "",
    )
    db.add(import_record)
    db.commit()
    db.refresh(import_record)

    return ImportPreviewResponse(
        import_id=import_record.id,
        status=import_record.status,
        fields=fields,
        rows=rows,
        download_url=f"/api/imports/{import_record.id}/download",
    )


def download_import_file(import_id: int, db: Session) -> tuple[Path, str]:
    import_record = db.get(Import, import_id)

    if not import_record:
        raise ImportNotFoundException()

    file_path = resolve_import_file_path(import_record.file_key)

    if not file_path:
        raise ImportNotFoundException()

    file_name = (
        import_record.file_name.replace("\r", "").replace("\n", "").replace('"', "")
    )

    return file_path, file_name


def delete_import(import_id: int, db: Session) -> None:
    import_record = db.get(Import, import_id)

    if not import_record:
        raise ImportNotFoundException()

    file_path = resolve_import_file_path(import_record.file_key)

    if file_path:
        file_path.unlink(missing_ok=True)

    db.delete(import_record)
    db.commit()


def get_imports(
    db: Session, page: int, page_size: int
) -> PaginatedResponse[ImportResponse]:
    statement = (
        select(Import)
        .order_by(Import.created_at.desc(), Import.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    import_records = db.scalars(statement).all()

    import_records_count = db.scalar(select(func.count()).select_from(Import)) or 0

    total_pages = ceil(import_records_count / page_size)
    has_next_page = total_pages > page

    return PaginatedResponse(
        data=[
            ImportResponse(
                import_id=import_record.id,
                status=import_record.status,
                download_url=f"/api/imports/{import_record.id}/download",
                file_name=import_record.file_name,
            )
            for import_record in import_records
        ],
        pagination=PaginationResponse(
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next_page=has_next_page,
            total=import_records_count,
        ),
    )


def process_import(db: Session, import_id: int) -> ImportResponse:
    has_rows_statement = exists().where(ImportRow.import_id == Import.id)
    statement = select(Import, has_rows_statement).where(Import.id == import_id)

    result = db.execute(statement).one_or_none()

    if not result:
        raise ImportNotFoundException()

    import_record, has_import_rows = result

    if has_import_rows or import_record.status != ImportStatus.PENDING:
        raise ImportAlreadyProcessedException()

    file_path = resolve_import_file_path(import_record.file_key)

    if not file_path:
        raise ImportFileNotFoundException()

    csv_rows = import_csv(file_path)

    for index, csv_row in enumerate(csv_rows):
        if index >= CSV_MAX_ROWS_SIZE - 1:
            raise ImportFileTooBigException()

        db.add(
            ImportRow(
                import_id=import_record.id,
                row_number=index + 1,
                data=csv_row,
                is_valid=False,
                errors=[],
            )
        )

    db.commit()
    db.refresh(import_record)

    return ImportResponse(
        import_id=import_record.id,
        status=import_record.status,
        download_url=f"/api/imports/{import_record.id}/download",
        file_name=import_record.file_name,
    )


def get_import_rows(
    db: Session, import_id: int, page: int, page_size: int, is_valid: bool | None
) -> PaginatedResponse[GetImportRowResponse]:
    import_record = db.get(Import, import_id)

    if not import_record:
        raise ImportNotFoundException()

    conditions = [ImportRow.import_id == import_id]

    if is_valid is not None:
        conditions.append(ImportRow.is_valid == is_valid)

    import_rows_statement = (
        select(ImportRow)
        .where(*conditions)
        .order_by(ImportRow.row_number)
        .offset((page - 1) * page_size)
        .limit(page_size)
    )

    import_rows = db.scalars(import_rows_statement).all()

    import_rows_count = (
        db.scalar(select(func.count()).select_from(ImportRow).where(*conditions)) or 0
    )

    import_data: list[list[ImportRowDataResponse]] = []

    while len(import_data) < len(import_rows):
        import_data.append([])

    for index, row in enumerate(import_rows):
        for column, value in row.data.items():
            if not column:
                # empty values are being stored, need to inspect the import
                continue

            column_error = next(
                (error for error in row.errors if error["column"] == column), None
            )

            import_data[index].append(
                ImportRowDataResponse(
                    column=column,
                    value=value,
                    error=column_error["reason"] if column_error else None,
                )
            )

    total_pages = ceil(import_rows_count / page_size)
    has_next_page = page < total_pages

    return PaginatedResponse(
        data=[
            GetImportRowResponse(
                id=import_row.id,
                row_number=import_row.row_number,
                data=import_data[index],
                is_valid=import_row.is_valid,
            )
            for index, import_row in enumerate(import_rows)
        ],
        pagination=PaginationResponse(
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next_page=has_next_page,
            total=import_rows_count,
        ),
    )
