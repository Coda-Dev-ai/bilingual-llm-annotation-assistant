# Bilingual LLM Annotation Assistant

Bilingual LLM Annotation Assistant is a local-first French-English annotation workflow system for customer feedback and support text. 
It ingests CSV or JSON records, detects or accepts the source language, and uses an LLM to classify issue type, sentiment, and urgency. 
The system produces structured JSON outputs with localized summaries and applies validation rules to keep results consistent and auditable. 
It also routes uncertain, ambiguous, mixed-language, or policy-sensitive cases to a human review queue instead of auto-accepting weak outputs. 
The project is designed to demonstrate prompt engineering, multilingual annotation design, structured outputs, evaluation, and human-in-the-loop workflow thinking in a portfolio-ready implementation.

## MVP Scope

The local MVP focuses on:
- CSV/JSON ingestion for English and French text records
- preprocessing and optional language detection
- prompt-based annotation through Hugging Face Inference
- strict JSON validation with retry/fallback handling
- confidence and rule-based review routing
- Postgres storage for records, outputs, and review status
- a lightweight Streamlit review interface for flagged cases
- basic evaluation metrics for issue type, sentiment, JSON validity, and review rate

The MVP does **not** aim to solve production deployment, background job orchestration, advanced authentication, or enterprise-scale observability in the first version.

## Local Run Instructions

Local run steps will be added once the initial implementation is scaffolded.

Placeholder flow:
1. create the virtual environment with `uv`
2. install dependencies from `requirements.txt`
3. create and populate `.env`
4. start Postgres locally or through Docker
5. run the FastAPI backend
6. run the Streamlit review UI
