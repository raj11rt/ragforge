from pydantic import BaseModel


class BenchmarkQuestion(BaseModel):
    question: str
    expected_answer: str


class BenchmarkResult(BaseModel):
    config_name: str
    question: str
    generated_answer: str