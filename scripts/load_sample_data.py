from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from sqlalchemy import MetaData, Table, create_engine, insert
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from app.data.loaders import load_records
from app.data.preprocess import preprocess_record
from app.data.schemas import InputRecordOut, LoadResult
from app.data.validators import RecordValidationError, validate_record

DEFAULT_DATA_FILE = Path("data/raw/sample_tickets_en_fr.csv")
TABLE_NAME = "input_records"


def build_engine() -> Engine:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL environment variable is required")
    return create_engine(database_url, future=True)


def reflect_input_records_table(engine: Engine) -> Table:
    metadata = MetaData()
    return Table(TABLE_NAME, metadata, autoload_with=engine)


def insert_record(engine: Engine, table: Table, record: dict[str, Any]) -> InputRecordOut:
    payload = {
        "external_id": record["external_id"],
        "source_text": record["text"],
        "source_language": record["language"],
    }

    with engine.begin() as conn:
        result = conn.execute(insert(table).values(**payload))
        inserted_id = result.inserted_primary_key[0] if result.inserted_primary_key else None

        if inserted_id is not None:
            selected = conn.execute(table.select().where(table.c.id == inserted_id)).mappings().first()
            if selected:
                return InputRecordOut.model_validate(selected)

        fallback = {
            "id": inserted_id or -1,
            "external_id": payload["external_id"],
            "source_text": payload["source_text"],
            "source_language": payload["source_language"],
            "gold_label": None,
            "created_at": None,
        }
        return InputRecordOut.model_validate(fallback)


def run_load(file_path: Path) -> LoadResult:
    rows = load_records(file_path)
    engine = build_engine()
    table = reflect_input_records_table(engine)

    inserted: list[InputRecordOut] = []
    errors: list[dict[str, Any]] = []

    for index, raw_row in enumerate(rows, start=1):
        try:
            processed = preprocess_record(raw_row)
            validated = validate_record(processed)
            inserted_row = insert_record(engine, table, validated.model_dump())
            inserted.append(inserted_row)
        except (RecordValidationError, SQLAlchemyError, ValueError) as exc:
            errors.append({"row_number": index, "error": str(exc), "row": raw_row})

    return LoadResult(
        total_rows=len(rows),
        inserted_rows=len(inserted),
        failed_rows=len(errors),
        inserted=inserted,
        errors=errors,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Load sample bilingual support tickets into PostgreSQL")
    parser.add_argument(
        "--file",
        type=Path,
        default=DEFAULT_DATA_FILE,
        help="Path to a CSV or JSON file with external_id, text, language columns",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_load(args.file)
    print(json.dumps(result.model_dump(mode="json"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
