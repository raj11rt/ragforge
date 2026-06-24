from pydantic import BaseModel


class BenchmarkConfig(BaseModel):
    chunk_size: int = 512
    chunk_overlap: int = 50
    embedding_model: str = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    top_k: int = 4