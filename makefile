run:
	uv run uvicorn open_data_pipeline.main:app --reload

test:
	uv run pytest