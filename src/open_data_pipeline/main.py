from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from open_data_pipeline.api.exceptions import AppException, app_exception_handler
from open_data_pipeline.api.router import router as api_router

app = FastAPI(title="Open Data Pipeline")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppException, app_exception_handler)
app.include_router(api_router)
