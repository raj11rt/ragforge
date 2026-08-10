import os
import time

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


class GeneratorService:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            groq_api_key=os.getenv("GROQ_API_KEY"),
            temperature=0,
        )

    def generate(self, context: str, question: str):
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

        for attempt in range(3):
            try:
                try:
                    response = self.llm.invoke(prompt)
                    return response.content

                except Exception as e:
                    return f"LLM_ERROR: {str(e)}"

            except Exception as e:
                print(f"\nAttempt {attempt + 1} failed")
                print(e)

                if attempt < 2:
                    print("Waiting 40 seconds before retrying...\n")
                    time.sleep(40)
                else:
                    raise