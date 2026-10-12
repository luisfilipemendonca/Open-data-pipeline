from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum


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


class FieldInferredType(StrEnum):
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
    inferred_type: FieldInferredType


FIELD_TYPE_DETECTORS: list[FieldTypeDetector] = [
    FieldTypeDetector(detector=_is_integer, inferred_type=FieldInferredType.INTEGER),
    FieldTypeDetector(detector=_is_decimal, inferred_type=FieldInferredType.DECIMAL),
]

FIELD_TYPES_ORDER: list[FieldInferredType] = [
    FieldInferredType.STRING,
    FieldInferredType.DECIMAL,
    FieldInferredType.INTEGER,
]


def detect_field_type(value: str) -> FieldInferredType:
    for field_type_detector in FIELD_TYPE_DETECTORS:
        if field_type_detector.detector(value):
            return field_type_detector.inferred_type

    return FieldInferredType.STRING
