from collections.abc import Generator
from typing import cast

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from open_data_pipeline.db.session import get_db
from open_data_pipeline.features.imports.models import Import
from open_data_pipeline.main import app


class SessionStub:
    def add(self, _instance: object, _warn: bool = True) -> None:
        return None

    def commit(self) -> None:
        return None

    def refresh(self, instance: object) -> None:
        if isinstance(instance, Import):
            instance.id = 123


@pytest.fixture
def db() -> Session:
    return cast(Session, cast(object, SessionStub()))


@pytest.fixture
def client(db: Session) -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_db] = lambda: db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
