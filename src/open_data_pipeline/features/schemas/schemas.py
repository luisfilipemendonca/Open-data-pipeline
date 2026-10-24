from datetime import datetime
from typing import Self, TypedDict

from pydantic import BaseModel, Field, field_validator, model_validator

from open_data_pipeline.features.imports.field_types import FieldTypes
from open_data_pipeline.features.imports.schemas import (
    ImportPreviewField,
    ImportResponse,
)
from open_data_pipeline.features.schemas.validations import (
    CreateSchemaFieldValidation,
    validate_validations,
)


class CreateSchemaFieldRequest(BaseModel):
    name: str
    field_type: FieldTypes
    required: bool = False
    validations: list[CreateSchemaFieldValidation] | None = None

    @field_validator("name")
    @classmethod
    def name_most_not_be_blank(cls, value: str) -> str:
        stripped = value.strip()

        if not stripped:
            raise ValueError("Field name cannot be empty")

        return stripped

    @model_validator(mode="after")
    def validations_must_match_field_type(self) -> Self:
        if not self.validations:
            return self

        is_valid, error_message = validate_validations(
            field_type=self.field_type, validations=self.validations
        )

        if not is_valid:
            raise ValueError(error_message)

        return self


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


class SchemaFieldValidator(BaseModel):
    name: str
    field_type: FieldTypes
    required: bool
    validations: dict[str, int] | None


class SchemaFieldsResponse(BaseModel):
    id: int
    name: str
    field_type: FieldTypes
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


class DetailsSchemaResponse(BaseModel):
    id: int
    name: str
    version: int
    created_at: datetime
    updated_at: datetime
    outdated_count: int
    fields: list[ImportPreviewField]


class OutdatedSchemaCopiesResponse(BaseModel):
    id: int
    version: int
    created_at: datetime
    updated_at: datetime
    import_id: int | None
    import_file_name: str | None
