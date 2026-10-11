from fastapi import UploadFile
from sqlalchemy.orm import Session

from open_data_pipeline.features.imports.exceptions import InvalidFileException
from open_data_pipeline.features.imports.file_validator import validate_file
from open_data_pipeline.features.imports.models import Import
from open_data_pipeline.features.imports.schemas import ImportResponse, ImportStatus


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
