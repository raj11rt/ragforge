from collections import defaultdict


class LeaderboardService:

    @staticmethod
    def build(results):
        if not results:
            return []

        grouped = defaultdict(lambda: {
            "scores": [],
            "relevancies": [],
            "faithfulness_scores": [],
            "precisions": [],
            "recalls": []
        })

        for r in results:
            key = (
                r.config_name,
                r.chunk_size,
                r.chunk_overlap,
                r.top_k,
            )
            # Use score/overall_score, default to 0.0 if None
            grouped[key]["scores"].append(r.score if r.score is not None else 0.0)
            grouped[key]["relevancies"].append(r.answer_relevancy if r.answer_relevancy is not None else 0.0)
            grouped[key]["faithfulness_scores"].append(r.faithfulness if r.faithfulness is not None else 0.0)
            grouped[key]["precisions"].append(r.context_precision if r.context_precision is not None else 0.0)
            grouped[key]["recalls"].append(r.context_recall if r.context_recall is not None else 0.0)

        leaderboard = []
        for key, data in grouped.items():
            n = len(data["scores"])
            leaderboard.append(
                {
                    "config_name": key[0],
                    "chunk_size": key[1],
                    "chunk_overlap": key[2],
                    "top_k": key[3],
                    "average_score": round(sum(data["scores"]) / n, 3) if n else 0.0,
                    "answer_relevancy": round(sum(data["relevancies"]) / n, 3) if n else 0.0,
                    "faithfulness": round(sum(data["faithfulness_scores"]) / n, 3) if n else 0.0,
                    "context_precision": round(sum(data["precisions"]) / n, 3) if n else 0.0,
                    "context_recall": round(sum(data["recalls"]) / n, 3) if n else 0.0,
                }
            )

        leaderboard.sort(
            key=lambda x: x["average_score"],
            reverse=True,
        )

        return leaderboard