from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Identity,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from open_data_pipeline.db.base import Base
from open_data_pipeline.features.imports.schemas import ImportStatus
from open_data_pipeline.features.schemas.models import Schema


class Import(Base):
    __tablename__: str = "imports"

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    status: Mapped[ImportStatus] = mapped_column(
        Enum(ImportStatus, name="import_status"),
        nullable=False,
        default=ImportStatus.PENDING,
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
    file_key: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)

    rows: Mapped[list["ImportRow"]] = relationship(
        back_populates="import_record", passive_deletes=True
    )

    schema_id: Mapped[int | None] = mapped_column(
        ForeignKey(column="schemas.id", ondelete="SET NULL"),
        nullable=True,
        unique=True,
    )
    schema: Mapped["Schema | None"] = relationship(back_populates="import_record")


class ImportRow(Base):
    __tablename__: str = "import_rows"
    __table_args__ = (
        UniqueConstraint(
            "import_id", "row_number", name="uq_import_rows_import_id_row_number"
        ),
    )

    def __repr__(self) -> str:
        return f"row_number: {self.row_number}\n data: {self.data}\n"

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    import_id: Mapped[int] = mapped_column(
        ForeignKey("imports.id", ondelete="CASCADE"), nullable=False, index=True
    )
    row_number: Mapped[int] = mapped_column(Integer, nullable=False)
    data: Mapped[dict[str, str]] = mapped_column(JSONB, nullable=False)
    is_valid: Mapped[bool] = mapped_column(Boolean, nullable=False)
    errors: Mapped[list[dict[str, str]]] = mapped_column(
        JSONB, nullable=False, default=list
    )

    import_record: Mapped[Import] = relationship(back_populates="rows")
