from datetime import datetime, timezone
from sqlalchemy import Column, Float, Integer, String, DateTime, Text
from pgvector.sqlalchemy import Vector

from app.db.database import Base


class DocumentDB(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True)       # UUID string
    filename = Column(String, nullable=True)
    full_text = Column(Text)
    num_pages = Column(Integer, nullable=True)
    num_characters = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DocumentChunkDB(Base):
    __tablename__ = "document_chunks"

    id = Column(String, primary_key=True)           # UUID string
    document_id = Column(String, index=True)
    chunk_index = Column(Integer)
    content = Column(Text)
    embedding = Column(Vector(384))                  # pgvector: 384-dim for MiniLM / BGE-small
    embedding_model = Column(String)
    benchmark_tag = Column(String, nullable=True)   # NULL = permanent; set = temp benchmark chunk


class BenchmarkResultDB(Base):
    __tablename__ = "benchmark_results"

    id = Column(Integer, primary_key=True, index=True)

    config_name = Column(String)

    chunk_size = Column(Integer)
    chunk_overlap = Column(Integer)
    top_k = Column(Integer)

    question = Column(String)

    generated_answer = Column(String)
    score = Column(Float)
    answer_relevancy = Column(Float, nullable=True)
    faithfulness = Column(Float, nullable=True)
    context_precision = Column(Float, nullable=True)
    context_recall = Column(Float, nullable=True)
    overall_score = Column(Float, nullable=True)
    experiment_id = Column(Integer)


class ExperimentDB(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(String)

    name = Column(String)
    status = Column(String, default="PENDING")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))



