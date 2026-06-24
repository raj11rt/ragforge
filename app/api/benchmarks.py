from fastapi import APIRouter

from app.benchmark.runner import BenchmarkRunner
from app.benchmark.sample_questions import QUESTIONS

from app.db.database import SessionLocal
from app.db.experiment_repository import ExperimentRepository

router = APIRouter()


@router.post("/run")
def run_benchmark(
    document_id: str,
):
    db = SessionLocal()

    experiment = ExperimentRepository.create(
        db=db,
        document_id=document_id,
        name="Dashboard Benchmark Run",
    )

    results = BenchmarkRunner().run(
        document_id=document_id,
        questions=QUESTIONS,
        experiment_id=experiment.id,
    )

    db.close()

    return {
        "status": "completed",
        "experiment_id": experiment.id,
        "results_count": len(results),
    }