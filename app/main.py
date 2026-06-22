from fastapi import FastAPI
from app.api.documents import router as document_router
from app.api.query import router as query_router

app = FastAPI(
    title="RAGForge",
    version="0.1.0",
    description="Automated RAG Optimization and Benchmarking Platform",
)

app.include_router(document_router, prefix="/documents", tags=["Documents"])
app.include_router(query_router, prefix="/query", tags=["Query"])


@app.get("/")
def root():
    return {
        "message": "RAGForge API is running"
    }