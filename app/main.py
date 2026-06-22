from fastapi import FastAPI
from app.api.documents import router as document_router

app = FastAPI(
    title="RAGForge",
    version="0.1.0",
    description="Automated RAG Optimization and Benchmarking Platform",
)

app.include_router(document_router, prefix="/documents", tags=["Documents"])


@app.get("/")
def root():
    return {
        "message": "RAGForge API is running"
    }