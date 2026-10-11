from fastapi import FastAPI

from open_data_pipeline.api.router import router as api_router

app = FastAPI(title="Open Data Pipeline")

app.include_router(api_router)
