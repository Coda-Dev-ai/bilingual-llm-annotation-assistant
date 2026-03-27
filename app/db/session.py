import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

FALLBACK_DATABASE_URL = "sqlite:///./bilingual_annotation_local_mvp.db"  # Local SQLite fallback for MVP

def get_database_url() -> str:
    """Return the configured database URL from the environment variable.
    
    Local MVP fallback: If DATABASE_URL is not set, default to a local SQLite database."""
    database_url = os.getenv("DATABASE_URL", FALLBACK_DATABASE_URL)
        
    return database_url

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""

    DATABASE_URL: str = get_database_url()
    
    # Create the SQLAlchemy engine and session factory
    engine = create_engine(
        DATABASE_URL, 
        future=True,
        pool_pre_ping=True,  # Check if connections are alive before using them
        echo=True
    )

    SessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
        future=True
    )
