from app.db.models import ExperimentDB


class ExperimentRepository:

    @staticmethod
    def create(db, document_id: str, name: str):

        experiment = ExperimentDB(
            document_id=document_id,
            name=name,
        )

        db.add(experiment)
        db.commit()
        db.refresh(experiment)

        return experiment

    @staticmethod
    def get_all(db):
        return db.query(ExperimentDB).all()

    @staticmethod
    def get_by_id(db, experiment_id: int):
        return (
            db.query(ExperimentDB)
            .filter(
                ExperimentDB.id == experiment_id
            )
            .first()
        )
    
    @staticmethod
    def get_results(db, experiment_id: int):
        from app.db.models import BenchmarkResultDB

        return (
            db.query(BenchmarkResultDB)
            .filter(
                BenchmarkResultDB.experiment_id == experiment_id
            )
            .all()
        )