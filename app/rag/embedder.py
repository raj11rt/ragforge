import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()


class EmbeddingService:
    def __init__(
        self,
        model_name="models/gemini-embedding-001",
    ):
        api_key = os.getenv("GOOGLE_API_KEY")
        # Ensure model name is valid for Gemini API
        if not model_name.startswith("models/") and "gemini" in model_name:
            model_name = f"models/{model_name}"
        elif not ("gemini" in model_name or "embedding" in model_name):
            model_name = "models/gemini-embedding-001"

        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=model_name,
            google_api_key=api_key,
        )

    def get_embeddings(self):
        return self.embeddings