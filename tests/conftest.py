import os
from collections.abc import Generator

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

load_dotenv()


@pytest.fixture
def integration_db() -> Generator[Session, None, None]:
    database_url = os.getenv("DATABASE_URL_TEST")

    if not database_url:
        raise RuntimeError("DATABASE_URL_TEST is not set")

    engine = create_engine(url=database_url)

    with engine.connect() as connection:
        transation = connection.begin()
        session_factory = sessionmaker(
            bind=connection,
            autoflush=False,
            autocommit=False,
            join_transaction_mode="create_savepoint",
        )

        with session_factory() as session:
            try:
                yield session

            finally:
                transation.rollback()
                session.close()

    engine.dispose()
