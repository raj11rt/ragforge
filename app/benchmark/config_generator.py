from app.benchmark.config import BenchmarkConfig


def generate_configs():
    return [
        BenchmarkConfig(
            chunk_size=512,
            chunk_overlap=50,
            top_k=4,
        )
    ]