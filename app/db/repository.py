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
            score=getattr(result, "score", None),
            answer_relevancy=getattr(result, "answer_relevancy", None),
            faithfulness=getattr(result, "faithfulness", None),
            context_precision=getattr(result, "context_precision", None),
            context_recall=getattr(result, "context_recall", None),
            overall_score=getattr(result, "overall_score", None),
            experiment_id=experiment_id,
        )

        db.add(db_result)
        db.commit()
