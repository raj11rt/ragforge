from app.rag.vector_store import VectorStoreService


class RetrieverService:
    def __init__(self):
        self.vector_store = VectorStoreService()

    def retrieve(
        self,
        query: str,
        document_id: str,
        k: int = 4,
    ):
        return self.vector_store.similarity_search(
            query=query,
            document_id=document_id,
            k=k,
        )