from sqlalchemy.orm import Session

from app.db.models import BenchmarkResultDB


class BenchmarkRepository:

    @staticmethod
    def save_result(
    db: Session,
    result,
    experiment_id: int,
    ):
        db_result = BenchmarkResultDB(
            config_name=result.config_name,
            chunk_size=result.chunk_size,
            chunk_overlap=result.chunk_overlap,
            top_k=result.top_k,
            question=result.question,
            generated_answer=result.generated_answer,
            score=result.score,
            experiment_id=experiment_id,
        )

        db.add(db_result)
        db.commit()