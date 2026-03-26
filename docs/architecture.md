# Local Architecture Summary

The local MVP uses a simple layered architecture designed for clarity and testability. Input records arrive as CSV or JSON files and are handled by a FastAPI backend. During ingestion, the backend validates required fields such as record ID, text, optional language, and optional gold labels. A preprocessing layer normalizes text, removes malformed rows, and fills in missing language tags through lightweight detection logic when needed. This keeps the downstream annotation prompt consistent across English and French inputs.

After preprocessing, records move into the annotation pipeline. The pipeline builds a structured prompt containing the input text, language, allowed labels, localization instructions, and the required JSON schema. A Hugging Face Inference client sends the prompt to the selected model and receives the response. The output parser and validation layer then enforce schema correctness using Pydantic models and rules for allowed label values. If the JSON is invalid or required fields are missing, retry or fallback logic is applied before the record is either accepted or flagged.

Once a valid response is available, confidence and review-routing rules determine whether the item should be auto-accepted or sent to a human review queue. Records are flagged when they show signs of ambiguity, unsupported labels, mixed English and French content, policy-sensitive wording, or weak confidence signals. This human-in-the-loop step is important because the project is meant to demonstrate safe automation, not blind automation.

All inputs, outputs, review decisions, and metadata are stored in Postgres. The database acts as the system of record for annotation results, audit trails, prompt versions, and evaluation inputs. Keeping prompt versions and review outcomes in storage makes it possible to compare performance over time and explain why a record was accepted or escalated.

A Streamlit frontend provides a lightweight local review interface. Reviewers can inspect flagged records, compare source text with the generated labels and summaries, and record final decisions. This UI does not need to be polished in the MVP; it exists to prove the review workflow and human override loop.

The evaluation layer reads stored outputs and optional gold labels to compute metrics such as issue-type accuracy, macro F1, sentiment accuracy, JSON validity rate, escalation rate, and per-language performance. The result is a local architecture with clear separation between ingestion, preprocessing, prompting, validation, review routing, persistence, and evaluation. It is intentionally small enough to build locally while still reflecting how a more production-ready annotation system would be structured.

## High Level Architecture Diagram

```text
                ┌──────────────────────┐
                │   CSV / JSON Input   │
                │  reviews / tickets   │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Preprocessing Layer  │
                │ clean, normalize,    │
                │ language detect      │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Prompting Engine     │
                │ LLM classification   │
                │ + localization rules │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Structured Output    │
                │ JSON validation      │
                │ retry/fallback logic │
                └──────────┬───────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
   ┌──────────────────────┐   ┌──────────────────────┐
   │ Auto-accepted items  │   │ Human review queue   │
   │ high-confidence      │   │ uncertain / flagged  │
   └──────────┬───────────┘   └──────────┬───────────┘
              │                          │
              └────────────┬─────────────┘
                           ▼
                ┌──────────────────────┐
                │ Results Store        │
                │ labels, prompts,     │
                │ outputs, review logs │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Evaluation Layer     │
                │ accuracy, agreement, │
                │ per-language metrics │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Dashboard / API      │
                │ review UI + metrics  │
                └──────────────────────┘

```

----------