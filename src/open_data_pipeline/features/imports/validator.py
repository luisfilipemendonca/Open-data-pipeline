from open_data_pipeline.features.imports.field_types import (
    validate_field_type,
)
from open_data_pipeline.features.imports.schemas import ImportRowError
from open_data_pipeline.features.schemas.schemas import SchemaFieldValidator

type ValidationResult = tuple[bool, list[ImportRowError]]


def validate_row_fields(
    row: dict[str, str], fields: list[SchemaFieldValidator]
) -> ValidationResult:
    errors: list[ImportRowError] = []

    for field in fields:
        stripped = row[field.name].strip()

        if not field.required and not stripped:
            continue

        if field.required and not stripped:
            errors.append(
                ImportRowError(
                    column=field.name, reason="Empty or only with white space value"
                )
            )
            continue

        validated = validate_field_type(stripped, field.field_type)

        if validated is None:
            errors.append(
                ImportRowError(column=field.name, reason="Field type is not supported")
            )
            continue

        is_valid, error_message = validated

        if not is_valid:
            errors.append(ImportRowError(column=field.name, reason=error_message))

    return (not errors, errors)
