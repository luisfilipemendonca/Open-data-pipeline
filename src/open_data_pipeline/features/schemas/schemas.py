from datetime import datetime
from typing import Self

from pydantic import BaseModel, Field, field_validator, model_validator

from open_data_pipeline.features.imports.field_types import FieldInferredType
from open_data_pipeline.features.imports.schemas import ImportResponse


class CreateSchemaFieldRequest(BaseModel):
    name: str
    field_type: FieldInferredType
    required: bool = False

    @field_validator("name")
    @classmethod
    def name_most_not_be_blank(cls, value: str) -> str:
        stripped = value.strip()

        if not stripped:
            raise ValueError("Field name cannot be empty")

        return stripped


class CreateSchemaRequest(BaseModel):
    name: str
    fields: list[CreateSchemaFieldRequest] = Field(min_length=1)

    @field_validator("name")
    @classmethod
    def name_most_not_be_blank(cls, value: str) -> str:
        stripped = value.strip()

        if not stripped:
            raise ValueError("Schema name cannot be empty")

        return stripped

    @model_validator(mode="after")
    def field_names_must_be_unique(self) -> Self:
        names = [field.name for field in self.fields]

        if len(names) != len(set(names)):
            raise ValueError("Field names must be unique")

        return self


class SchemaFieldsResponse(BaseModel):
    id: int
    name: str
    field_type: FieldInferredType
    required: bool


class SchemaResponse(BaseModel):
    id: int
    parent_schema_id: int | None
    is_base: bool
    version: int
    parent_version: int | None
    name: str | None
    fields: list[SchemaFieldsResponse]
    import_record: ImportResponse | None
    created_at: datetime
    updated_at: datetime


class GetSchemaResponse(BaseModel):
    id: int
    name: str
    version: int
    created_at: datetime
    updated_at: datetime
