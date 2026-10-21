from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum

BOOL_VALUES = ("true", "false", "1", "0", "yes", "no")


def _is_unsigned_integer(value: str) -> bool:
    return bool(value) and value.isascii() and value.isdigit()


def _is_integer(value: str) -> bool:
    if value.startswith(("+", "-")):
        value = value[1:]

    return _is_unsigned_integer(value)


def _is_decimal(value: str) -> bool:
    if value.startswith(("+", "-")):
        value = value[1:]

    integer_part, dot, decimal_part = value.partition(".")

    return (
        bool(dot)
        and _is_unsigned_integer(integer_part)
        and _is_unsigned_integer(decimal_part)
    )


def _is_decimal_or_integer(value: str) -> bool:
    return _is_decimal(value) or _is_integer(value)


def _is_boolean(value: str) -> bool:
    parsed = value.strip().lower()

    return parsed in BOOL_VALUES


def _is_string(value: str) -> bool:
    return True


class FieldTypes(StrEnum):
    STRING = "string"
    INTEGER = "integer"
    DECIMAL = "decimal"
    BOOLEAN = "boolean"
    DATE = "date"
    TIME = "time"
    DATETIME = "datetime"


@dataclass(frozen=True)
class FieldTypeDetector:
    detector: Callable[[str], bool]
    inferred_type: FieldTypes


@dataclass(frozen=True)
class FieldTypeValidator:
    validator: Callable[[str], bool]
    error_message: str


FIELD_TYPE_VALIDATOR_MAP: dict[FieldTypes, FieldTypeValidator] = {
    FieldTypes.INTEGER: FieldTypeValidator(
        validator=_is_integer, error_message="Field is not of integer type"
    ),
    FieldTypes.DECIMAL: FieldTypeValidator(
        validator=_is_decimal_or_integer, error_message="Field is not of decimal type"
    ),
    FieldTypes.BOOLEAN: FieldTypeValidator(
        validator=_is_boolean, error_message="Field is not of boolean type"
    ),
    FieldTypes.STRING: FieldTypeValidator(
        validator=_is_string, error_message="Field is not of string type"
    ),
}

FIELD_TYPE_DETECTORS: list[FieldTypeDetector] = [
    FieldTypeDetector(detector=_is_integer, inferred_type=FieldTypes.INTEGER),
    FieldTypeDetector(detector=_is_decimal, inferred_type=FieldTypes.DECIMAL),
    FieldTypeDetector(detector=_is_boolean, inferred_type=FieldTypes.BOOLEAN),
]


FIELD_TYPES_ORDER: list[FieldTypes] = [
    FieldTypes.STRING,
    FieldTypes.DECIMAL,
    FieldTypes.INTEGER,
    FieldTypes.BOOLEAN,
]


def detect_field_type(value: str) -> FieldTypes:
    for field_type_detector in FIELD_TYPE_DETECTORS:
        if field_type_detector.detector(value):
            return field_type_detector.inferred_type

    return FieldTypes.STRING


def validate_field_type(value: str, field_type: FieldTypes) -> tuple[bool, str] | None:
    if field_type in FIELD_TYPE_VALIDATOR_MAP:
        stripped = value.strip()

        field_validator = FIELD_TYPE_VALIDATOR_MAP[field_type]

        return (field_validator.validator(stripped), field_validator.error_message)

    return None
