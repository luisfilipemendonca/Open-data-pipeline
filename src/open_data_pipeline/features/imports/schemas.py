from enum import StrEnum

from pydantic import BaseModel, ConfigDict

from open_data_pipeline.features.imports.field_types import (
    FieldInferredType,
)


class ImportStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    COMPLETED_WITH_ERRORS = "completed_with_errors"
    FAILED = "failed"


class ImportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    import_id: int
    status: ImportStatus
    download_url: str
    file_name: str


class ImportPreviewField(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    inferred_type: FieldInferredType
    required: bool


class ImportPreviewResponse(BaseModel):
    import_id: int
    status: ImportStatus
    download_url: str
    fields: list[ImportPreviewField]
    rows: list[dict[str, str]]


class ImportRowError(BaseModel):
    column: str
    reason: str


class ImportRowDataResponse(BaseModel):
    column: str
    value: str
    error: str | None


class ImportRowResponse(BaseModel):
    id: int
    row_number: int
    data: list[ImportRowDataResponse]
    is_valid: bool


class UpdateImportRowBody(BaseModel):
    column: str
    value: str
