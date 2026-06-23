from app.benchmark.config import BenchmarkConfig


def generate_configs():
    configs = []

    chunk_sizes = [256, 512]
    overlaps = [0, 50]
    top_k_values = [3, 5]

    for chunk_size in chunk_sizes:
        for overlap in overlaps:
            for top_k in top_k_values:
                configs.append(
                    BenchmarkConfig(
                        chunk_size=chunk_size,
                        chunk_overlap=overlap,
                        top_k=top_k,
                    )
                )

    return configs