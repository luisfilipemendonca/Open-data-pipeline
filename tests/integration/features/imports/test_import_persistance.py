from io import BytesIO

from fastapi import UploadFile
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from open_data_pipeline.db.session import get_db
from open_data_pipeline.features.imports.exceptions import INVALID_FILE_EXCEPTION
from open_data_pipeline.features.imports.models import Import
from open_data_pipeline.features.imports.schemas import ImportResponse, ImportStatus
from open_data_pipeline.features.imports.service import import_data
from open_data_pipeline.main import app


def test_import_persistance(integration_db: Session) -> None:
    import_record = Import(status=ImportStatus.PENDING)

    integration_db.add(import_record)
    integration_db.commit()
    integration_db.refresh(import_record)

    persisted_record = integration_db.scalar(
        select(Import).where(Import.id == import_record.id)
    )

    assert persisted_record is not None
    assert persisted_record.id == import_record.id
    assert persisted_record.status == ImportStatus.PENDING


def test_import_data_persists_import(integration_db: Session) -> None:
    file = UploadFile(file=BytesIO(b"test"), filename="test.csv")

    service_response = import_data(file=file, db=integration_db)

    persisted_record = integration_db.scalar(
        select(Import).where(Import.id == service_response.import_id)
    )

    assert persisted_record is not None
    assert persisted_record.id == service_response.import_id
    assert persisted_record.status == ImportStatus.PENDING


def test_import_endpoint_persists_import(integration_db: Session) -> None:
    app.dependency_overrides[get_db] = lambda: integration_db

    try:
        with TestClient(app) as client:
            response = client.post(
                url="/api/imports",
                files={
                    "file": (
                        "integration_test.csv",
                        b"name,age\nJohn,30\nJane,25",
                        "text/csv",
                    )
                },
            )

        assert response.status_code == 202

        import_response = ImportResponse.model_validate(response.json())
        import_id = import_response.import_id
        persisted_record = integration_db.get(Import, import_id)

        assert persisted_record is not None
        assert persisted_record.id == import_id
        assert persisted_record.status == ImportStatus.PENDING
    finally:
        app.dependency_overrides.clear()


def test_import_rejects_invalid_file(integration_db: Session) -> None:
    app.dependency_overrides[get_db] = lambda: integration_db

    try:
        with TestClient(app) as client:
            response = client.post(
                url="/api/imports",
                files={"file": ("invalid.txt", b"invalid", "text/plain")},
            )

            assert response.status_code == 400
            assert response.json()["detail"] == INVALID_FILE_EXCEPTION

    finally:
        app.dependency_overrides.clear()
