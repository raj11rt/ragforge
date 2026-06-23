from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.generator import GeneratorService
from app.rag.vector_store import VectorStoreService

router = APIRouter()


class QueryRequest(BaseModel):
    document_id: str
    question: str


@router.post("/")
def query(request: QueryRequest):
    vector_store = VectorStoreService()

    results = vector_store.similarity_search(
        query=request.question,
        document_id=request.document_id,
        k=4,
    )

    contexts = results["documents"][0]
    context = "\n\n".join(contexts)

    answer = GeneratorService().generate(
        context=context,
        question=request.question,
    )

    return {
        "answer": answer,
        "retrieved_chunks": len(contexts),
        "document_id": request.document_id,
    }