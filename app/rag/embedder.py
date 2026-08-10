import os
import time
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()


class RateLimitedGoogleEmbeddings:
    def __init__(self, embeddings):
        self._embeddings = embeddings

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        batch_size = 16
        all_embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            for attempt in range(5):
                try:
                    res = self._embeddings.embed_documents(batch)
                    all_embeddings.extend(res)
                    time.sleep(0.5)  # Pause to avoid hitting Google 100 req/min limit
                    break
                except Exception as e:
                    if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                        wait_seconds = (attempt + 1) * 15
                        print(f"Rate limited by Google API (429). Retrying batch in {wait_seconds}s...")
                        time.sleep(wait_seconds)
                    else:
                        raise
        return all_embeddings

    def embed_query(self, text: str) -> list[float]:
        for attempt in range(5):
            try:
                return self._embeddings.embed_query(text)
            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    wait_seconds = (attempt + 1) * 15
                    print(f"Rate limited by Google API (429). Retrying query in {wait_seconds}s...")
                    time.sleep(wait_seconds)
                else:
                    raise


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

        raw_embeddings = GoogleGenerativeAIEmbeddings(
            model=model_name,
            google_api_key=api_key,
        )
        self.embeddings = RateLimitedGoogleEmbeddings(raw_embeddings)

    def get_embeddings(self):
        return self.embeddings
