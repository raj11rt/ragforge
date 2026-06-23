from app.rag.embedder import EmbeddingService


class BenchmarkRetriever:
    def __init__(self, collection):
        self.collection = collection
        self.embedding_model = EmbeddingService().get_embeddings()

    def retrieve(self, query: str, k: int):
        embedding = self.embedding_model.embed_query(query)

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=k,
        )

        return results["documents"][0]