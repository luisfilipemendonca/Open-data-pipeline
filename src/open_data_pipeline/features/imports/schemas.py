from enum import StrEnum

from pydantic import BaseModel


class ImportStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ImportResponse(BaseModel):
    import_id: int
    status: ImportStatus
