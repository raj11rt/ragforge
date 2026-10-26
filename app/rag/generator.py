import os
import time

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# Groq models in priority order (fallback chain).
# llama3-8b-8192 and llama-3.1-8b-instant were deprecated/removed for some accounts.
# See: https://console.groq.com/docs/models
GROQ_MODEL_FALLBACK_CHAIN = [
    "llama-3.1-8b-instant",       # Preferred – fast & lightweight
    "llama-3.3-70b-versatile",    # Fallback – larger but widely available
]


class GeneratorService:
    def __init__(self):
        groq_key = os.getenv("GROQ_API_KEY")
        if not groq_key:
            try:
                import streamlit as st
                if "GROQ_API_KEY" in st.secrets:
                    groq_key = st.secrets["GROQ_API_KEY"]
            except Exception:
                pass

        # Allow overriding the model via env var; otherwise use the fallback chain.
        configured_model = os.getenv("GROQ_MODEL", "").strip()
        self._model_chain = (
            [configured_model] + GROQ_MODEL_FALLBACK_CHAIN
            if configured_model
            else GROQ_MODEL_FALLBACK_CHAIN
        )
        self._groq_key = groq_key
        # Initialize with the first model in the chain.
        self.llm = self._build_llm(self._model_chain[0])

    def _build_llm(self, model: str) -> ChatGroq:
        return ChatGroq(
            model=model,
            groq_api_key=self._groq_key,
            temperature=0,
        )

    def generate(self, context: str, question: str) -> str:
        prompt = f"""
You are a RAG assistant.

Answer ONLY from the provided context.

If the answer is not present in the context, reply exactly:
"I could not find the answer in the provided document."

Context:
{context}

Question:
{question}
"""
        tried_models = list(self._model_chain)  # copy so we can pop

        for model in tried_models:
            llm = self._build_llm(model)
            for attempt in range(3):
                try:
                    response = llm.invoke(prompt)
                    return response.content

                except Exception as e:
                    error_msg = str(e)

                    # If the model is not found / no access, try next model immediately.
                    if "model_not_found" in error_msg or "does not exist" in error_msg:
                        print(f"[GeneratorService] Model '{model}' not found, trying next fallback...")
                        break  # break inner retry loop, move to next model

                    # For other transient errors, retry with backoff.
                    print(f"\n[GeneratorService] Attempt {attempt + 1} with model '{model}' failed: {e}")
                    if attempt < 2:
                        print("Waiting 40 seconds before retrying...\n")
                        time.sleep(40)
                    else:
                        break  # exhausted retries for this model, try next

        return "LLM_ERROR: All configured models are unavailable. Please check your GROQ_API_KEY and GROQ_MODEL settings."