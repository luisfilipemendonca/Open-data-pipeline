from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session

from open_data_pipeline.features.imports.csv_reader import (
    import_csv,
    read_csv_headers,
    save_upload_file,
)
from open_data_pipeline.features.imports.exceptions import (
    InvalidFileException,
    InvalidFileHeadersException,
)
from open_data_pipeline.features.imports.field_inference import infer_fields
from open_data_pipeline.features.imports.file_validator import validate_file
from open_data_pipeline.features.imports.models import Import
from open_data_pipeline.features.imports.schemas import (
    ImportPreviewResponse,
    ImportResponse,
    ImportStatus,
)


def import_data(file: UploadFile, db: Session) -> ImportResponse:
    if not validate_file(file):
        raise InvalidFileException()

    import_record = Import(status=ImportStatus.PENDING)
    db.add(import_record)
    db.commit()
    db.refresh(import_record)

    return ImportResponse(
        import_id=import_record.id,
        status=import_record.status,
    )


def import_data_preview(file: UploadFile, db: Session) -> ImportPreviewResponse:
    if not validate_file(file):
        raise InvalidFileException()

    file_key, file_path = save_upload_file(file)
    csv_headers = read_csv_headers(file_path)

    if not csv_headers:
        file_path.unlink(missing_ok=True)
        raise InvalidFileHeadersException()

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
