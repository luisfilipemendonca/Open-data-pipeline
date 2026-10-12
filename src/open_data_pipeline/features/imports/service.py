from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session

from open_data_pipeline.features.imports.csv_reader import (
    import_csv,
    read_csv_headers,
)
from open_data_pipeline.features.imports.exceptions import InvalidFileException
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


FILE_PATH = Path("tmp/imports/cd40adb3-0248-4bf1-bdf3-3a265cc9f05a.csv")


def import_data_preview(file: UploadFile, db: Session) -> ImportPreviewResponse:
    if not validate_file(file):
        raise InvalidFileException()

    import_record = Import(status=ImportStatus.ANALYZING)
    db.add(import_record)
    db.commit()
    db.refresh(import_record)

    # file_path = save_upload_file(file)
    csv_headers = read_csv_headers(FILE_PATH)
    csv_rows = import_csv(FILE_PATH)

    fields, rows = infer_fields(csv_headers, csv_rows)

    return ImportPreviewResponse(
        import_id=import_record.id,
        status=import_record.status,
        fields=fields,
        rows=rows,
        download_url="",
    )
