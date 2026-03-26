"""Minimal smoke test for the database layer.

Runs the following steps:
1. opens a connection
2. creates tables
3. inserts one input record
4. queries it back

Set DATABASE_URL for Postgres, or run as-is to use the SQLite fallback from session.py.
"""

from __future__ import annotations

from sqlalchemy import select

try:
    from .crud import create_record
    from .models import InputRecord
    from .session import Base, SessionLocal, engine
except ImportError:  # pragma: no cover - allows direct script execution
    from crud import create_record
    from models import InputRecord
    from session import Base, SessionLocal, engine


def main() -> None:
    with engine.connect() as connection:
        print("Connected to database:", connection.engine.url)

    Base.metadata.create_all(bind=engine)
    print("Tables created or already present.")

    with SessionLocal() as db:
        record = create_record(
            db,
            external_id="smoke-test-001",
            source_text="I was charged twice for my monthly subscription.",
            language="en",
            gold_label={"issue_type": "billing"},
        )
        print(f"Inserted record id={record.id}, external_id={record.external_id}")

        fetched = db.scalar(
            select(InputRecord).where(InputRecord.external_id == "smoke-test-001")
        )

        if fetched is None:
            raise RuntimeError("Smoke test failed: inserted record was not found.")

        print("Queried record back successfully:")
        print(
            {
                "id": fetched.id,
                "external_id": fetched.external_id,
                "language": fetched.language,
                "source_text": fetched.source_text,
            }
        )


if __name__ == "__main__":
    main()
