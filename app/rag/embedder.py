from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingService:
    def __init__(
        self,
        model_name="sentence-transformers/all-MiniLM-L6-v2",
    ):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name
        )

    def get_embeddings(self):
        return self.embeddings