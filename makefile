run:
	uv run uvicorn open_data_pipeline.main:app --reload

test:
	uv run pytest

db-migrate:
	uv run alembic upgrade head

db-migrate-test:
	TEST_DATABASE_URL="$$(grep '^TEST_DATABASE_URL=' .env | cut -d '=' -f2-)" uv run alembic upgrade head