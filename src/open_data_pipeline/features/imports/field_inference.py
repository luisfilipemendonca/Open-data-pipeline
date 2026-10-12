from collections.abc import Iterator

from open_data_pipeline.features.imports.field_types import (
    FIELD_TYPES_ORDER,
    FieldInferredType,
    detect_field_type,
)
from open_data_pipeline.features.imports.schemas import ImportPreviewField

PREVIEW_ROWS_COUNT = 10


def infer_fields(
    headers: list[str], csv_rows: Iterator[dict[str, str]]
) -> tuple[list[ImportPreviewField], list[dict[str, str]]]:
    fields: list[ImportPreviewField] = [
        ImportPreviewField(
            name=header,
            inferred_type=FieldInferredType.STRING,
            required=True,
        )
        for header in headers
    ]

    field_types_set: dict[str, set[FieldInferredType]] = {
        field.name: set() for field in fields
    }

    field_required_dict: dict[str, bool] = {
        field.name: field.required for field in fields
    }

    processed_rows: list[dict[str, str]] = []

    for row in csv_rows:
        if len(processed_rows) >= PREVIEW_ROWS_COUNT:
            break

        for field in fields:
            value = row[field.name].strip()

            if value:
                inferred_type = detect_field_type(value)
                field_types_set[field.name].add(inferred_type)

            field_required_dict[field.name] = (
                field_required_dict[field.name] and value.strip() != ""
            )

        processed_rows.append(row)

    for field in fields:
        field.required = (
            field_required_dict[field.name] if len(processed_rows) > 0 else False
        )

        for inferred_type in FIELD_TYPES_ORDER:
            if inferred_type in field_types_set[field.name]:
                field.inferred_type = inferred_type
                break

    return fields, processed_rows
