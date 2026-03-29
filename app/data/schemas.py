from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

class InputRecordIn(BaseModel):
    """Canonical model for incoming records after preprocessing and column mapping"""

    model_config = ConfigDict(str_strip_whitespace=False, extra="allow")

    external_id: str = Field(..., min_length=1, description="Source-system identifier")
    text: str = Field(..., min_length=1, description="Raw ticket text to be annotated")
    language: str = Field(..., description="Normalized language code: en or fr")

class InputRecordOut(BaseModel):
    """Inserted database row shape for Milestone 3 raw-ingestion feedback."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    external_id: str
    source_text: str
    source_language: str
    gold_label: Optional[str] = None
    created_at: Optional[datetime] = None


class LoadResult(BaseModel):
    total_rows: int
    inserted_rows: int
    failed_rows: int
    inserted: list[InputRecordOut] = Field(default_factory=list)
    errors: list[dict[str, Any]] = Field(default_factory=list)