import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


class GeneratorService:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0,
        )

    def generate(self, context: str, question: str):
        prompt = f"""
You are a RAG assistant.

Answer ONLY from the provided context.
If the answer is not present, say:
"I could not find the answer in the provided document."

Context:
{context}

Question:
{question}
"""

        response = self.llm.invoke(prompt)

        return response.content