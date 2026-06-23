from app.benchmark.config_generator import generate_configs
from app.benchmark.schemas import BenchmarkResult

from app.rag.generator import GeneratorService
from app.rag.vector_store import VectorStoreService


class BenchmarkRunner:
    def __init__(self):
        self.generator = GeneratorService()
        self.vector_store = VectorStoreService()

    def run(
        self,
        document_id: str,
        questions: list,
    ):
        results = []

        configs = generate_configs()

        for config in configs:

            for question in questions:

                retrieved = self.vector_store.similarity_search(
                    query=question.question,
                    document_id=document_id,
                    k=config.top_k,
                )

                contexts = retrieved["documents"][0]

                context = "\n\n".join(contexts)

                answer = self.generator.generate(
                    context=context,
                    question=question.question,
                )

                results.append(
                    BenchmarkResult(
                        config_name=str(config),
                        question=question.question,
                        generated_answer=answer,
                    )
                )

        return results