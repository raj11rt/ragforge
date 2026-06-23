from fastapi import APIRouter

from app.db.database import SessionLocal
from app.db.experiment_repository import (
    ExperimentRepository,
)

router = APIRouter()


@router.get("/")
def get_experiments():

    db = SessionLocal()

    experiments = (
        ExperimentRepository.get_all(db)
    )

    db.close()

    return experiments

@router.post("/")
def create_experiment(
    document_id: str,
    name: str,
):
    db = SessionLocal()

    experiment = (
        ExperimentRepository.create(
            db=db,
            document_id=document_id,
            name=name,
        )
    )

    db.close()

    return experiment

@router.get("/{experiment_id}")
def get_experiment(
    experiment_id: int,
):
    db = SessionLocal()

    experiment = (
        ExperimentRepository.get_by_id(
            db,
            experiment_id,
        )
    )

    db.close()

    return experiment

@router.get("/{experiment_id}/results")
def get_experiment_results(
    experiment_id: int,
):
    db = SessionLocal()

    results = (
        ExperimentRepository.get_results(
            db,
            experiment_id,
        )
    )

    db.close()

    return results