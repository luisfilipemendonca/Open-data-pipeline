from io import BytesIO

import pytest
from fastapi import UploadFile
from sqlalchemy.orm import Session

from open_data_pipeline.features.imports.exceptions import InvalidFileException
from open_data_pipeline.features.imports.schemas import ImportStatus
from open_data_pipeline.features.imports.service import import_data


def test_import_data_valid_file(db: Session):
    result = import_data(
        file=UploadFile(filename="test.csv", file=BytesIO(b"test")), db=db
    )

    assert result.import_id == 123
    assert result.status == ImportStatus.PENDING


def test_import_data_invalid_file(db: Session):
    with pytest.raises(InvalidFileException):
        _ = import_data(
            file=UploadFile(filename="test.txt", file=BytesIO(b"test")), db=db
        )
