from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.rag.schemas import ChunkingConfig


class DocumentChunker:
    def __init__(self, config: ChunkingConfig):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
        )

    def split_text(self, text: str):
        return self.splitter.split_text(text)