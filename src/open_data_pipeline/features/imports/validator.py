type ValidationResult = tuple[bool, list[str]]


def validate_row_fields(
    row: dict[str, str], required_fields: list[str]
) -> ValidationResult:
    reasons: list[str] = []

    for required_field in required_fields:
        if required_field not in row:
            reasons.append(f"Required field {required_field} not found in row")
        elif not row[required_field].strip():
            reasons.append(
                f"Required field {required_field} is empty or contains only whitespace"
            )

    return (not reasons, reasons)
