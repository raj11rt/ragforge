from uuid import uuid4

from app.benchmark.config_generator import generate_configs
from app.benchmark.document_repository import DocumentRepository
from app.benchmark.pipeline_builder import PipelineBuilder
from app.benchmark.schemas import BenchmarkResult

from app.benchmark.benchmark_retriever import BenchmarkRetriever

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

            collection_name = f"benchmark_{uuid4().hex}"

            collection = vector_store.client.get_or_create_collection(
                name=collection_name
            )

            texts = [doc.page_content for doc in documents]
            metadatas = [doc.metadata for doc in documents]

            embeddings = vector_store.embedding_model.embed_documents(texts)

            ids = [f"{collection_name}_{i}" for i in range(len(texts))]

            collection.add(
                ids=ids,
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas,
            )

            retriever = BenchmarkRetriever(
                collection=collection,
                embedding_model=vector_store.embedding_model,
            )

            for question in questions:
                contexts = retriever.retrieve(
                    query=question.question,
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

            vector_store.client.delete_collection(collection_name)

        return results
