from app.db.database import SessionLocal
from app.db.experiment_repository import ExperimentRepository
from app.db.models import ExperimentDB


def test_experiment_creation_and_status_updates():
    db = SessionLocal()
    try:
        # Create a test experiment
        experiment = ExperimentRepository.create(
            db=db,
            document_id="test-doc-id-123",
            name="Test Experiment",
        )

        assert experiment.id is not None
        assert experiment.document_id == "test-doc-id-123"
        assert experiment.name == "Test Experiment"
        assert experiment.status == "PENDING"
        assert experiment.created_at is not None

        # Update the status to RUNNING
        updated = ExperimentRepository.update_status(db, experiment.id, "RUNNING")
        assert updated.status == "RUNNING"

        # Update the status to COMPLETED
        updated = ExperimentRepository.update_status(db, experiment.id, "COMPLETED")
        assert updated.status == "COMPLETED"

        # Retrieve experiment and check results
        retrieved = ExperimentRepository.get_by_id(db, experiment.id)
        assert retrieved.status == "COMPLETED"

    finally:
        # Clean up the test experiment
        if 'experiment' in locals():
            db.delete(experiment)
            db.commit()
        db.close()
