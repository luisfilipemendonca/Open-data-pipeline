import math
from collections.abc import Callable
from enum import StrEnum
from typing import TypedDict

from pydantic import BaseModel

from open_data_pipeline.features.imports.field_types import (
    FieldTypes,
)


class CreateSchemaFieldValidation(BaseModel):
    validation_type: str
    validation_value: int


class IntegerValidation(StrEnum):
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"


INTEGER_VALIDATIONS = [validation for validation in IntegerValidation]


def _integer_validation_rules(validations: dict[str, int]) -> tuple[bool, str]:
    if "gt" in validations and "gte" in validations:
        return (False, "Validation type gt and gte are not allowed simultaneous")

    if "lt" in validations and "lte" in validations:
        return (False, "Validation type lt and lte are not allowed simultaneous")

    min_value = -math.inf
    max_value = math.inf

    if "gt" in validations:
        min_value = validations["gt"] + 1

    if "gte" in validations:
        min_value = validations["gte"]

    if "lt" in validations:
        max_value = validations["lt"] - 1

    if "lte" in validations:
        max_value = validations["lte"]

    if min_value > max_value:
        return (False, "Minimum and maximum values overlap, leaving no valid values.")

    return (True, "")


class FieldValidationConfig(TypedDict):
    validations: list[IntegerValidation]
    validation_rules: Callable[[dict[str, int]], tuple[bool, str]]


FIELD_TYPE_ALLOWED_VALIDATIONS: dict[FieldTypes, FieldValidationConfig] = {
    FieldTypes.INTEGER: {
        "validations": INTEGER_VALIDATIONS,
        "validation_rules": _integer_validation_rules,
    }
}


def validate_validations(
    field_type: FieldTypes, validations: list[CreateSchemaFieldValidation]
) -> tuple[bool, str]:
    validations_dictionary: dict[str, int] = {}

    for validation in validations:
        if validation.validation_type in validations_dictionary:
            return (False, f"Multiple validations of type {validation.validation_type}")

        validations_dictionary[validation.validation_type] = validation.validation_value

    if not field_type in FIELD_TYPE_ALLOWED_VALIDATIONS:
        return (False, f"Validations in {field_type} are not allowed")

    field_type_validations_config = FIELD_TYPE_ALLOWED_VALIDATIONS[field_type]

    for validation in validations_dictionary:
        if not validation in field_type_validations_config["validations"]:
            return (
                False,
                f"Validation of type {validation} is not allowed for field of type {field_type}",
            )

    are_rules_valid, error_message = field_type_validations_config["validation_rules"](
        validations_dictionary
    )

    return (are_rules_valid, error_message)
