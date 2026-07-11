from pydantic import BaseModel


class BenchmarkQuestion(BaseModel):
    question: str
    expected_answer: str


class BenchmarkResult(BaseModel):
    config_name: str
    chunk_size: int
    chunk_overlap: int
    top_k: int

    question: str
    generated_answer: str
    score: float
    answer_relevancy: float | None = None
    faithfulness: float | None = None
    context_precision: float | None = None
    context_recall: float | None = None
    overall_score: float | None = None
