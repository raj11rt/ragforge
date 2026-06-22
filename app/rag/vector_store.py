from langchain_chroma import Chroma
from app.rag.embedder import EmbeddingService


class VectorStoreService:
    def __init__(self):
        self.embedding_function = EmbeddingService().get_embeddings()

    def create_store(self, texts):
        vector_store = Chroma.from_texts(
            texts=texts,
            embedding=self.embedding_function,
            persist_directory="./chroma_db"
        )
        return vector_store