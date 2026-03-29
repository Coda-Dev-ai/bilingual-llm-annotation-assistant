from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from app.data.schemas import InputRecordIn

SUPPORTED_LANGUAGES = {"en", "fr"}


class RecordValidationError(ValueError):
    pass


def validate_not_empty_text(text: Any) -> None:
    if text is None or not str(text).strip():
        raise RecordValidationError("text must not be empty")


def validate_language(language: Any) -> None:
    if language not in SUPPORTED_LANGUAGES:
        raise RecordValidationError(
            f"unsupported language '{language}'. Expected one of: {sorted(SUPPORTED_LANGUAGES)}"
        )


def validate_record(record: dict[str, Any]) -> InputRecordIn:
    validate_not_empty_text(record.get("text"))
    validate_language(record.get("language"))

    try:
        return InputRecordIn.model_validate(record)
    except ValidationError as exc:
        raise RecordValidationError(str(exc)) from exc
