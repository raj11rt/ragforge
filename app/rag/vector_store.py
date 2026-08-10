import os
from uuid import uuid4

from sqlalchemy import text

from app.db.database import SessionLocal, engine
from app.db.models import DocumentChunkDB
from app.rag.embedder import EmbeddingService


class VectorStoreService:
    def __init__(
        self,
        embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        self.embedding_model_name = embedding_model_name
        self.embedding_model = EmbeddingService(
            model_name=embedding_model_name
        ).get_embeddings()

    # ------------------------------------------------------------------
    # Permanent document chunks (uploaded PDFs)
    # ------------------------------------------------------------------

    def add_documents(self, documents):
        """Embed and store document chunks permanently (benchmark_tag = NULL)."""
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        embeddings = self.embedding_model.embed_documents(texts)

        db = SessionLocal()
        try:
            for i, (text_content, metadata, embedding) in enumerate(
                zip(texts, metadatas, embeddings)
            ):
                chunk = DocumentChunkDB(
                    id=str(uuid4()),
                    document_id=metadata.get("document_id", ""),
                    chunk_index=metadata.get("chunk_index", i),
                    content=text_content,
                    embedding=embedding,
                    embedding_model=self.embedding_model_name,
                    benchmark_tag=None,
                )
                db.add(chunk)
            db.commit()
        finally:
            db.close()

    def similarity_search(self, query: str, document_id: str, k: int = 4):
        """Find top-k most similar permanent chunks for a document."""
        query_embedding = self.embedding_model.embed_query(query)

        db = SessionLocal()
        try:
            results = (
                db.query(DocumentChunkDB)
                .filter(
                    DocumentChunkDB.document_id == document_id,
                    DocumentChunkDB.benchmark_tag.is_(None),
                )
                .order_by(DocumentChunkDB.embedding.cosine_distance(query_embedding))
                .limit(k)
                .all()
            )
            texts = [r.content for r in results]
        finally:
            db.close()

        # Return in same shape as old ChromaDB results["documents"][0]
        return {"documents": [texts]}

    # ------------------------------------------------------------------
    # Temporary benchmark chunks (deleted after each benchmark config run)
    # ------------------------------------------------------------------

    def add_benchmark_chunks(self, documents, benchmark_tag: str):
        """Embed and store benchmark chunks with a tag (temporary)."""
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        embeddings = self.embedding_model.embed_documents(texts)

        db = SessionLocal()
        try:
            for i, (text_content, metadata, embedding) in enumerate(
                zip(texts, metadatas, embeddings)
            ):
                chunk = DocumentChunkDB(
                    id=str(uuid4()),
                    document_id=metadata.get("document_id", ""),
                    chunk_index=metadata.get("chunk_index", i),
                    content=text_content,
                    embedding=embedding,
                    embedding_model=self.embedding_model_name,
                    benchmark_tag=benchmark_tag,
                )
                db.add(chunk)
            db.commit()
        finally:
            db.close()

    def benchmark_search(self, query: str, benchmark_tag: str, k: int = 4):
        """Find top-k most similar chunks for a specific benchmark tag."""
        query_embedding = self.embedding_model.embed_query(query)

        db = SessionLocal()
        try:
            results = (
                db.query(DocumentChunkDB)
                .filter(DocumentChunkDB.benchmark_tag == benchmark_tag)
                .order_by(DocumentChunkDB.embedding.cosine_distance(query_embedding))
                .limit(k)
                .all()
            )
            texts = [r.content for r in results]
        finally:
            db.close()

        return texts

    def delete_benchmark_chunks(self, benchmark_tag: str):
        """Delete all temporary chunks for a benchmark run."""
        db = SessionLocal()
        try:
            db.query(DocumentChunkDB).filter(
                DocumentChunkDB.benchmark_tag == benchmark_tag
            ).delete()
            db.commit()
        finally:
            db.close()