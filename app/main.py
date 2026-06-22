from fastapi import FastAPI

app = FastAPI(
    title="RAGForge",
    version="0.1.0"
)

@app.get("/")
def root():
    return {
        "message": "RAGForge API Running"
    }