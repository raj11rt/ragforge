import chromadb

from app.rag.embedder import EmbeddingService
from uuid import uuid4

class VectorStoreService:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")

        self.collection = self.client.get_or_create_collection(
            name="documents"
        )

        self.embedding_model = EmbeddingService().get_embeddings()

    def add_documents(self, documents):
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]

        embeddings = self.embedding_model.embed_documents(texts)

        ids = [str(uuid4()) for _ in documents]

        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def similarity_search(
        self,
        query: str,
        document_id: str,
        k: int = 4,
    ):
        embedding = self.embedding_model.embed_query(query)

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=k,
            where={"document_id": document_id},
        )

        return results
    
    def create_temp_collection(
        self,
        collection_name: str,
    ):
        return self.client.get_or_create_collection(
            name=collection_name
        )
    