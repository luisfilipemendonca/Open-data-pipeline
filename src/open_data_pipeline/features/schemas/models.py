from sqlalchemy import (
    Boolean,
    Enum,
    ForeignKey,
    Identity,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from open_data_pipeline.db.base import Base
from open_data_pipeline.features.imports.field_types import FieldInferredType


class Schema(Base):
    __tablename__: str = "schemas"

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

    import_record: Mapped["Import | None"] = relationship(  # pyright: ignore[reportUndefinedVariable]  # noqa: F821
        back_populates="schema", uselist=False
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
