from uuid import uuid4

from app.benchmark.config_generator import generate_configs
from app.benchmark.document_repository import DocumentRepository
from app.benchmark.pipeline_builder import PipelineBuilder
from app.benchmark.schemas import BenchmarkResult

from app.rag.generator import GeneratorService
from app.rag.vector_store import VectorStoreService
from app.evaluation.evaluator import RagasEvaluator

from app.db.database import SessionLocal
from app.db.repository import BenchmarkRepository


class BenchmarkRunner:
    def __init__(self):
        self.generator = GeneratorService()

    def run(self, document_id: str, questions: list, experiment_id: int):
        text = DocumentRepository.load_text(document_id)

        results = []
        db = SessionLocal()

        configs = generate_configs()

        for config in configs:
            documents = PipelineBuilder.build_documents(
                text=text,
                config=config,
                document_id=document_id,
            )

            vector_store = VectorStoreService(
                embedding_model_name=config.embedding_model
            )

            # Unique tag for this benchmark config run
            benchmark_tag = f"benchmark_{uuid4().hex}"

            # Insert chunks into Supabase with the benchmark tag
            vector_store.add_benchmark_chunks(
                documents=documents,
                benchmark_tag=benchmark_tag,
            )

            for question in questions:
                # Retrieve using pgvector similarity search by tag
                contexts = vector_store.benchmark_search(
                    query=question.question,
                    benchmark_tag=benchmark_tag,
                    k=config.top_k,
                )

                context = "\n\n".join(contexts)

                answer = self.generator.generate(
                    context=context,
                    question=question.question,
                )
                evaluation = RagasEvaluator.evaluate_single(
                    question=question.question,
                    answer=answer,
                    expected_answer=question.expected_answer,
                    contexts=contexts,
                )

                benchmark_result = BenchmarkResult(
                    config_name=(
                        f"{config.embedding_model} | "
                        f"chunk={config.chunk_size} | "
                        f"top_k={config.top_k}"
                    ),
                    chunk_size=config.chunk_size,
                    chunk_overlap=config.chunk_overlap,
                    top_k=config.top_k,
                    question=question.question,
                    generated_answer=answer,
                    score=evaluation["score"],
                    answer_relevancy=evaluation.get("metrics", {}).get(
                        "answer_relevancy"
                    ),
                    faithfulness=evaluation.get("metrics", {}).get("faithfulness"),
                    context_precision=evaluation.get("metrics", {}).get(
                        "context_precision"
                    ),
                    context_recall=evaluation.get("metrics", {}).get("context_recall"),
                    overall_score=evaluation.get("score"),
                )

                results.append(benchmark_result)

                BenchmarkRepository.save_result(
                    db=db,
                    result=benchmark_result,
                    experiment_id=experiment_id,
                )

            # Clean up temp benchmark chunks from Supabase
            vector_store.delete_benchmark_chunks(benchmark_tag)

        db.close()
        return results
