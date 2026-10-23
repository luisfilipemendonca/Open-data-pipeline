from collections.abc import Callable

from open_data_pipeline.features.imports.field_types import (
    FieldTypes,
    validate_field_type,
)
from open_data_pipeline.features.imports.schemas import ImportRowError
from open_data_pipeline.features.schemas.schemas import SchemaFieldValidator
from open_data_pipeline.features.schemas.validations import (
    IntegerValidation,
)

type ValidationResult = tuple[bool, list[ImportRowError]]


def greater_than_validator(value: int, validation_value: int) -> tuple[bool, str]:
    if value <= validation_value:
        return (False, f"Value should be greater than {validation_value}")

    return (True, "")


def greater_equal_than_validator(value: int, validation_value: int) -> tuple[bool, str]:
    if value < validation_value:
        return (False, f"Value should be greater or equal than {validation_value}")

    return (True, "")


def less_than_validator(value: int, validation_value: int) -> tuple[bool, str]:
    if value >= validation_value:
        return (False, f"Value should be smaller than {validation_value}")

    return (True, "")


def less_equal_than_validator(value: int, validation_value: int) -> tuple[bool, str]:
    if value > validation_value:
        return (False, f"Value should be smaller or equal than {validation_value}")

    return (True, "")


INTEGER_VALIDATION_VALIDATORS_TYPE = dict[str, Callable[[int, int], tuple[bool, str]]]

INTEGER_VALUE_VALIDATION_VALIDATORS: INTEGER_VALIDATION_VALIDATORS_TYPE = {
    IntegerValidation.GT: greater_than_validator,
    IntegerValidation.GTE: greater_equal_than_validator,
    IntegerValidation.LT: less_than_validator,
    IntegerValidation.LTE: less_equal_than_validator,
}

FIELD_VALUE_VALIDATION_VALIDATORS: dict[
    FieldTypes, INTEGER_VALIDATION_VALIDATORS_TYPE
] = {FieldTypes.INTEGER: INTEGER_VALUE_VALIDATION_VALIDATORS}


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
            continue

        if field.validations:
            field_validator = FIELD_VALUE_VALIDATION_VALIDATORS.get(field.field_type)

            if field_validator is None:
                errors.append(
                    ImportRowError(
                        column=field.name, reason="Field validation not supported"
                    )
                )
                continue

            for key, value in field.validations.items():
                validator = field_validator.get(key)

                if validator is None:
                    errors.append(
                        ImportRowError(
                            column=field.name, reason="Field validation not supported"
                        )
                    )
                    continue

                is_value_valid, error_message = validator(int(stripped), value)

                if not is_value_valid:
                    errors.append(
                        ImportRowError(column=field.name, reason=error_message)
                    )

    return (not errors, errors)
