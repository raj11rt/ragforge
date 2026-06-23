class SimpleEvaluator:

    @staticmethod
    def evaluate_single(
        question: str,
        answer: str,
        expected_answer: str,
    ):
        answer_words = set(answer.lower().split())
        expected_words = set(expected_answer.lower().split())

        overlap = len(answer_words & expected_words)

        if len(expected_words) == 0:
            score = 0
        else:
            score = overlap / len(expected_words)

        return {
            "question": question,
            "score": round(score, 3),
        }