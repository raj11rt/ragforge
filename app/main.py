from fastapi import FastAPI
from app.api.documents import router as document_router
from app.api.query import router as query_router
from app.api.leaderboard import router as leaderboard_router
from app.api.experiments import router as experiment_router
from app.api.benchmarks import router as benchmark_router

app = FastAPI(
    title="RAGForge",
    version="0.1.0",
    description="Automated RAG Optimization and Benchmarking Platform",
)

app.include_router(document_router, prefix="/documents", tags=["Documents"])
app.include_router(query_router, prefix="/query", tags=["Query"])
app.include_router(
    leaderboard_router,
    prefix="/leaderboard",
    tags=["Leaderboard"],
)
app.include_router(
    experiment_router,
    prefix="/experiments",
    tags=["Experiments"],
)
app.include_router(
    benchmark_router,
    prefix="/benchmarks",
    tags=["Benchmarks"],
)

@app.get("/")
def root():
    return {
        "message": "RAGForge API is running"
    }