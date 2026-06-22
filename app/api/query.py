from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.generator import GeneratorService
from app.rag.retriever import RetrieverService

router = APIRouter()


class QueryRequest(BaseModel):
    document_id: str
    question: str


@router.post("/")
def query_document(request: QueryRequest):
    results = RetrieverService().retrieve(
        query=request.question,
        document_id=request.document_id,
        k=4,
    )

    contexts = results["documents"][0]
    combined_context = "\n\n".join(contexts)

    answer = GeneratorService().generate(
        context=combined_context,
        question=request.question,
    )

    return {
        "answer": answer,
        "retrieved_chunks": len(contexts),
    }