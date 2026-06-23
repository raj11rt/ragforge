from app.rag.chunker import DocumentChunker
from app.rag.schemas import ChunkingConfig


class PipelineBuilder:
    @staticmethod
    def build_documents(
        text: str,
        config,
        document_id: str,
    ):
        chunk_config = ChunkingConfig(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
        )

        chunker = DocumentChunker(chunk_config)

        return chunker.split_text(
            text=text,
            document_id=document_id,
        )