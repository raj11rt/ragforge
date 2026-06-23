from collections import defaultdict


class LeaderboardService:

    @staticmethod
    def build(results):

        grouped = defaultdict(list)

        for r in results:

            key = (
                r.chunk_size,
                r.chunk_overlap,
                r.top_k,
            )

            grouped[key].append(r.score)

        leaderboard = []

        for key, scores in grouped.items():

            leaderboard.append(
                {
                    "chunk_size": key[0],
                    "chunk_overlap": key[1],
                    "top_k": key[2],
                    "average_score": round(
                        sum(scores) / len(scores),
                        3,
                    ),
                }
            )

        leaderboard.sort(
            key=lambda x: x["average_score"],
            reverse=True,
        )

        return leaderboard