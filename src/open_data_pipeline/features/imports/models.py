from datetime import datetime

from sqlalchemy import DateTime, Enum, Identity, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from open_data_pipeline.db.base import Base
from open_data_pipeline.features.imports.schemas import ImportStatus


class Import(Base):
    __tablename__: str = "imports"

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    status: Mapped[ImportStatus] = mapped_column(
        Enum(ImportStatus, name="import_status"),
        nullable=False,
        default=ImportStatus.ANALYZING,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
