from app.benchmark.results import LeaderboardEntry


class Leaderboard:

    @staticmethod
    def build(results):
        grouped = {}

        for result in results:

            key = (
                result.chunk_size,
                result.chunk_overlap,
                result.top_k,
            )

            if key not in grouped:
                grouped[key] = []

            grouped[key].append(result.score)

        leaderboard = []

        for key, scores in grouped.items():

            leaderboard.append(
                LeaderboardEntry(
                    chunk_size=key[0],
                    chunk_overlap=key[1],
                    top_k=key[2],
                    average_score=round(
                        sum(scores) / len(scores),
                        3,
                    ),
                )
            )

        leaderboard.sort(
            key=lambda x: x.average_score,
            reverse=True,
        )

        return leaderboard