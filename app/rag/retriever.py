from app.rag.vector_store import VectorStoreService


class RetrieverService:
    def __init__(self):
        self.vector_store = VectorStoreService()

    def retrieve(self, query: str, k: int = 4):
        store = self.vector_store.load_store()
        return store.similarity_search(query, k=k)