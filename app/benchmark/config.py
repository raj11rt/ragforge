from pydantic import BaseModel


class BenchmarkConfig(BaseModel):
    chunk_size: int = 512
    chunk_overlap: int = 50
    embedding_model: str = (
        "models/gemini-embedding-001"
    )
    top_k: int = 4