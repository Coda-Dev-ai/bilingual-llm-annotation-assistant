import pytest

from app.data.validators import RecordValidationError, validate_record


def test_validate_record_accepts_valid_record():
    record = {
        "external_id": "abc-123",
        "text": "My package is late.",
        "language": "en"
    }

    validated = validate_record(record)

    assert validated.external_id == "abc-123"
    assert validated.text == "My package is late."
    assert validated.language == "en"


def test_validate_record_rejects_empty_text():
    record = {
        "external_id": "abc-124",
        "text": "   ",
        "language": "en"
    }

    with pytest.raises(RecordValidationError, match="text must not be empty"):
        validate_record(record)


def test_validate_record_rejects_unsupported_language():
    record = {
        "external_id": "abc-125",
        "text": "Hola",
        "language": "es"
    }

    with pytest.raises(RecordValidationError, match="unsupported language"):
        validate_record(record)