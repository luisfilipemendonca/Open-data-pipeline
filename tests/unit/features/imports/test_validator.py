from open_data_pipeline.features.imports.validator import validate_row_fields


def test_validate_row_fields():
    row = {"id": "1", "name": "John Doe", "email": "john.doe@example.com"}

    required_fields = ["id", "name", "email"]

    result = validate_row_fields(row, required_fields)

    assert result == (True, [])


def test_validate_row_fields_missing_required_field():
    row = {"id": "1", "name": "John Doe"}

    required_fields = ["id", "name", "email"]

    result = validate_row_fields(row, required_fields)

    assert result == (False, ["Required field email not found in row"])


def test_validate_row_fields_empty_required_field():
    row = {"id": "1", "name": "John Doe", "email": ""}

    required_fields = ["id", "name", "email"]

    result = validate_row_fields(row, required_fields)

    assert result == (
        False,
        ["Required field email is empty or contains only whitespace"],
    )


def test_validate_row_fields_whitespace_required_field():
    row = {"id": "1", "name": "John Doe", "email": "   "}

    required_fields = ["id", "name", "email"]

    result = validate_row_fields(row, required_fields)

    assert result == (
        False,
        ["Required field email is empty or contains only whitespace"],
    )


def test_validate_row_fields_multiple_required_fields_missing():
    row = {"id": "1"}

    required_fields = ["id", "name", "email"]

    result = validate_row_fields(row, required_fields)

    assert result == (
        False,
        [
            "Required field name not found in row",
            "Required field email not found in row",
        ],
    )


def test_validate_row_fields_multiple_required_fields_empty():
    row = {"id": "1", "name": "", "email": ""}

    required_fields = ["id", "name", "email"]

    result = validate_row_fields(row, required_fields)

    assert result == (
        False,
        [
            "Required field name is empty or contains only whitespace",
            "Required field email is empty or contains only whitespace",
        ],
    )
