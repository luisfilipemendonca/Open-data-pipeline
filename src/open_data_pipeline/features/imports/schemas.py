from enum import StrEnum

from pydantic import BaseModel, ConfigDict

from open_data_pipeline.features.imports.field_types import (
    FieldInferredType,
)


class ImportStatus(StrEnum):
    ANALYZING = "analyzing"
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ImportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    import_id: int
    status: ImportStatus
    download_url: str
    file_name: str


class ImportPreviewField(BaseModel):
    name: str
    inferred_type: FieldInferredType
    required: bool


class ImportPreviewResponse(BaseModel):
    import_id: int
    status: ImportStatus
    download_url: str
    fields: list[ImportPreviewField]
    rows: list[dict[str, str]]
