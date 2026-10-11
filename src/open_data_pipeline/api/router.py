from fastapi import APIRouter

from open_data_pipeline.features.health.router import router as health_router
from open_data_pipeline.features.imports.router import router as imports_router

router = APIRouter(prefix="/api")

router.include_router(health_router)
router.include_router(imports_router)
