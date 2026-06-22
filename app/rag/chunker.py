from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.rag.schemas import ChunkingConfig


class DocumentChunker:
    def __init__(self, config: ChunkingConfig):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
        )

    def split_text(self, text: str, document_id: str):
        text_chunks = self.splitter.split_text(text)

        return [
            Document(
                page_content=chunk,
                metadata={
                    "document_id": document_id,
                    "chunk_index": index,
                },
            )
            for index, chunk in enumerate(text_chunks)
        ]