from pydantic import BaseModel


class ChunkingConfig(BaseModel):
    chunk_size: int = 512
    chunk_overlap: int = 50