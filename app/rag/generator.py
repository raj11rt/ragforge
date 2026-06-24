import os
import time
from urllib import response

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