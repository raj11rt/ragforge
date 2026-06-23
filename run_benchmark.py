from app.benchmark.runner import BenchmarkRunner
from app.benchmark.sample_questions import QUESTIONS

from app.db.database import SessionLocal
from app.db.experiment_repository import (
    ExperimentRepository,
)

document_id = input("Document ID: ")

db = SessionLocal()

experiment = ExperimentRepository.create(
    db=db,
    document_id=document_id,
    name="Manual Benchmark Run",
)

results = BenchmarkRunner().run(
    document_id=document_id,
    questions=QUESTIONS,
    experiment_id=experiment.id,
)

db.close()

for result in results:
    print(result)