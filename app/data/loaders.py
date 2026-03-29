from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Iterable

CANONICAL_FIELDS = {"external_id", "text", "language"}
FIELD_ALIASES = {
    "external_id": "external_id",
    "id": "external_id",
    "ticket_id": "external_id",
    "record_id": "external_id",
    "message_id": "external_id",
    "text": "text",
    "message": "text",
    "body": "text",
    "content": "text",
    "ticket_text": "text",
    "source_text": "text",
    "language": "language",
    "lang": "language",
    "locale": "language",
    "source_language": "language",
}


class LoaderError(ValueError):
    pass


def _normalize_key(key: str) -> str:
    return key.strip().lower()


def map_columns(row: dict[str, Any]) -> dict[str, Any]:
    mapped: dict[str, Any] = {}
    extras: dict[str, Any] = {}

    for key, value in row.items():
        normalized_key = _normalize_key(str(key))
        canonical_key = FIELD_ALIASES.get(normalized_key)
        if canonical_key:
            mapped[canonical_key] = value
        else:
            extras[key] = value

    missing = CANONICAL_FIELDS - set(mapped)
    if missing:
        raise LoaderError(f"missing required field(s): {sorted(missing)}")

    if extras:
        mapped["_extras"] = extras

    return mapped


def load_csv(path: str | Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with open(path, "r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise LoaderError("CSV file has no header row")
        for row in reader:
            rows.append(map_columns(dict(row)))
    return rows


def _coerce_json_payload(payload: Any) -> Iterable[dict[str, Any]]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for candidate_key in ("records", "items", "data"):
            if isinstance(payload.get(candidate_key), list):
                return payload[candidate_key]
        return [payload]
    raise LoaderError("Unsupported JSON structure. Expected an object or list of objects.")


def load_json(path: str | Path) -> list[dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return [map_columns(dict(item)) for item in _coerce_json_payload(payload)]


def load_records(path: str | Path) -> list[dict[str, Any]]:
    path = Path(path)
    suffix = path.suffix.lower()

    if suffix == ".csv":
        return load_csv(path)
    if suffix == ".json":
        return load_json(path)

    raise LoaderError(f"Unsupported file type '{suffix}'. Expected .csv or .json")
 