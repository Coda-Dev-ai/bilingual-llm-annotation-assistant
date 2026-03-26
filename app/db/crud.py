"""Basic CRUD helpers for the local MVP database layer."""

from __future__ import annotations

from typing import Any

from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session, selectinload

try: 
    from .models import AnnotationResult, InputRecord, ReviewQueueItem
except ImportError: # pragma: no cover
    from models import AnnotationResult, InputRecord, ReviewQueueItem

def create_record(
        db: Session, 
        *, 
        external_id: str,
        source_text: str,
        language: str | None = None,
        gold_label: dict[str, Any] | None = None
) -> InputRecord:
    """Create a new input record in the database."""
    record = InputRecord(
        external_id=external_id,
        source_text=source_text,
        language=language,
        gold_label=gold_label
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def save_annotation(
        db: Session, 
        *, 
        input_record_id: int,
        language: str,
        issue_type: str,
        sentiment: str,
        urgency: str,
        summary_en: str,
        summary_localized: str,
        needs_human_review: bool,
        review_reason: str | None = None,
        prompt_version: str | None = None,
        model_name: str | None = None,
        raw_response: dict[str, Any] | None = None
) -> AnnotationResult:
    """Save a new annotation result in the database and create a corresponding review queue item if human review is needed."""
    annotation = AnnotationResult(
        input_record_id=input_record_id,
        language=language,
        issue_type=issue_type,
        sentiment=sentiment,
        urgency=urgency,
        summary_en=summary_en,
        summary_localized=summary_localized,
        needs_human_review=needs_human_review,
        review_reason=review_reason,
        prompt_version=prompt_version,
        model_name=model_name,
        raw_response=raw_response
    )
    db.add(annotation)
    db.commit()
    db.refresh(annotation)

    if needs_human_review:
        queue_item = ReviewQueueItem(
            input_record_id=input_record_id,
            annotation_result_id=annotation.id,
            reason=review_reason or "low_confidence",
            status="queued"
        )
        db.add(queue_item)
        db.commit()

    db.refresh(queue_item)
    return annotation

def fetch_queued_reviews(db: Session, *, limit: int = 100) -> list[ReviewQueueItem]:
    """Fetch a list of review queue items that are currently queued for human review."""
    stmt = (
        select(ReviewQueueItem)
        .where(ReviewQueueItem.status == "queued")
        .options(
            selectinload(ReviewQueueItem.input_record),
            selectinload(ReviewQueueItem.annotation_result)
        )
        .order_by(ReviewQueueItem.created_at.asc(), ReviewQueueItem.id.asc())
        .limit(limit)
    )
    results = db.execute(stmt).scalars().all()
    return results
    