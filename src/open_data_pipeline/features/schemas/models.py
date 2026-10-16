from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Identity,
    Index,
    Integer,
    String,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from open_data_pipeline.db.base import Base
from open_data_pipeline.features.imports.field_types import FieldInferredType

if TYPE_CHECKING:
    from open_data_pipeline.features.imports.models import Import


class Schema(Base):
    __tablename__: str = "schemas"
    __table_args__ = (
        Index(
            "uq_schemas_name_is_base",
            "name",
            unique=True,
            postgresql_where=text("is_base"),
        ),
    )

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    parent_schema_id: Mapped[int | None] = mapped_column(
        ForeignKey(column="schemas.id", ondelete="RESTRICT"), nullable=True, index=True
    )
    is_base: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    parent_version: Mapped[int | None] = mapped_column(Integer, nullable=True)
    name: Mapped[str | None] = mapped_column(String, nullable=True)

    fields: Mapped[list["SchemaField"]] = relationship(
        back_populates="schema", passive_deletes=True
    )

    import_record: Mapped["Import | None"] = relationship(
        back_populates="schema", uselist=False
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


class SchemaField(Base):
    __tablename__: str = "schema_fields"
    __table_args__ = (
        UniqueConstraint("schema_id", "name", name="uq_schema_fields_schema_id_name"),
    )

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    schema_id: Mapped[int] = mapped_column(
        ForeignKey(column="schemas.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    field_type: Mapped[FieldInferredType] = mapped_column(
        "type", Enum(FieldInferredType, name="schema_field_type"), nullable=False
    )
    required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    schema: Mapped["Schema"] = relationship(back_populates="fields")
