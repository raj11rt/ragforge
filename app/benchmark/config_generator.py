from app.benchmark.config import BenchmarkConfig


def generate_configs():
    return [

        BenchmarkConfig(
            chunk_size=512,
            chunk_overlap=50,
            top_k=4,
            embedding_model="sentence-transformers/all-MiniLM-L6-v2",
        ),

        BenchmarkConfig(
            chunk_size=512,
            chunk_overlap=50,
            top_k=4,
            embedding_model="BAAI/bge-small-en-v1.5",
        ),

        BenchmarkConfig(
            chunk_size=1024,
            chunk_overlap=100,
            top_k=5,
            embedding_model="sentence-transformers/all-MiniLM-L6-v2",
        ),

        BenchmarkConfig(
            chunk_size=1024,
            chunk_overlap=100,
            top_k=5,
            embedding_model="BAAI/bge-small-en-v1.5",
        ),
    ]