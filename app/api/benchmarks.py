import logging
from fastapi import APIRouter, BackgroundTasks

from app.benchmark.runner import BenchmarkRunner
from app.benchmark.sample_questions import QUESTIONS

from app.db.database import SessionLocal
from app.db.experiment_repository import ExperimentRepository

logger = logging.getLogger("ragforge.benchmarks")
router = APIRouter()


def run_benchmark_task(experiment_id: int, document_id: str):
    logger.info(f"Starting background benchmark for experiment {experiment_id} and document {document_id}")
    db = SessionLocal()
    try:
        ExperimentRepository.update_status(db, experiment_id, "RUNNING")
        
        # Instantiate runner and run the evaluation
        runner = BenchmarkRunner()
        results = runner.run(
            document_id=document_id,
            questions=QUESTIONS,
            experiment_id=experiment_id,
        )
        
        ExperimentRepository.update_status(db, experiment_id, "COMPLETED")
        logger.info(f"Finished background benchmark for experiment {experiment_id} successfully, generated {len(results)} results")
    except Exception as e:
        logger.exception(f"Error running benchmark for experiment {experiment_id}")
        try:
            ExperimentRepository.update_status(db, experiment_id, "FAILED")
        except Exception as db_err:
            logger.error(f"Failed to set status to FAILED in database: {db_err}")
    finally:
        db.close()


@router.post("/run")
def run_benchmark(
    document_id: str,
    background_tasks: BackgroundTasks,
):
    db = SessionLocal()

    experiment = ExperimentRepository.create(
        db=db,
        document_id=document_id,
        name="Dashboard Benchmark Run",
    )

    db.close()

    # Add task to background runner
    background_tasks.add_task(run_benchmark_task, experiment.id, document_id)

    return {
        "status": "pending",
        "experiment_id": experiment.id,
    }