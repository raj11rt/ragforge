from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String

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
    experiment_id = Column(Integer)

class ExperimentDB(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(String)

    name = Column(String)