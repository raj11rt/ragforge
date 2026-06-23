from pydantic import BaseModel


class LeaderboardEntry(BaseModel):
    chunk_size: int
    chunk_overlap: int
    top_k: int

    average_score: float