import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

def get_env_var(key: str, default: str = None) -> str:
    val = os.getenv(key)
    if val:
        return val
    try:
        import streamlit as st
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return default

DATABASE_URL = get_env_var("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing. Please set it in .env or Streamlit App Secrets.")

# SQLAlchemy 2.1+ defaults to psycopg (v3) for plain `postgresql://` URLs.
# Force psycopg2 dialect since that's what's installed (psycopg2-binary).
if DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)

engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=2,
    pool_pre_ping=True,
)

# Enable pgvector extension (idempotent — safe to run every startup)
with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
    conn.commit()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()