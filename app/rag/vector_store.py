import chromadb

from app.rag.embedder import EmbeddingService


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

        ids = [f"chunk_{i}" for i in range(len(texts))]

        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def similarity_search(self, query: str, k: int = 4):
        embedding = self.embedding_model.embed_query(query)

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=k,
        )

        return results