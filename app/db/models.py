from datetime import datetime, timezone
from sqlalchemy import Column, Float, Integer, String, DateTime

from app.db.database import Base


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


