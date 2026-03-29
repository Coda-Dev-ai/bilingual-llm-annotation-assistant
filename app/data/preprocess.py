from __future__ import annotations

import re
from typing import Any

_SUPPORTED_LANGUAGES = {"en", "fr"}
_LINE_BREAKS_RE = re.compile(r"\r\n?|\n")
_MULTI_NEWLINES_RE = re.compile(r"\n{3,}")


LANGUAGE_ALIASES = {
    "en": "en",
    "eng": "en",
    "english": "en",
    "en-ca": "en",
    "en-us": "en",
    "fr": "fr",
    "fra": "fr",
    "fre": "fr",
    "french": "fr",
    "fr-ca": "fr",
    "fr-fr": "fr",
    "français": "fr",
    "francais": "fr",
}


def trim_whitespace(value: Any) -> Any:
    if isinstance(value, str):
        return value.strip()
    return value


def normalize_line_breaks(text: str) -> str:
    normalized = _LINE_BREAKS_RE.sub("\n", text)
    normalized = _MULTI_NEWLINES_RE.sub("\n\n", normalized)
    return normalized.strip()


def coerce_language(value: Any) -> str:
    if value is None:
        return ""

    raw = str(value).strip().lower()
    normalized = LANGUAGE_ALIASES.get(raw, raw)
    return normalized


def preprocess_record(record: dict[str, Any]) -> dict[str, Any]:
    processed = dict(record)

    if "external_id" in processed:
        processed["external_id"] = trim_whitespace(processed.get("external_id"))

    if "text" in processed and processed.get("text") is not None:
        processed["text"] = normalize_line_breaks(str(processed["text"]))

    if "language" in processed:
        processed["language"] = coerce_language(processed.get("language"))

    return processed
