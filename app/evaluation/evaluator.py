import re
from typing import Iterable


class RagasEvaluator:
    @staticmethod
    def _normalize_tokens(text: str) -> set[str]:
        return set(re.findall(r"\b[\w']+\b", (text or "").lower()))

    @staticmethod
    def _token_overlap(text_a: str, text_b: str) -> float:
        tokens_a = RagasEvaluator._normalize_tokens(text_a)
        tokens_b = RagasEvaluator._normalize_tokens(text_b)

        if not tokens_a or not tokens_b:
            return 0.0

        return len(tokens_a & tokens_b) / len(tokens_b)

    @staticmethod
    def evaluate_single(
        question: str,
        answer: str,
        expected_answer: str,
        contexts: Iterable[str] | None = None,
    ):
        answer_terms = RagasEvaluator._normalize_tokens(answer)
        expected_terms = RagasEvaluator._normalize_tokens(expected_answer)
        question_terms = RagasEvaluator._normalize_tokens(question)

        reference_terms = expected_terms or answer_terms or question_terms

        answer_relevancy = RagasEvaluator._token_overlap(answer, expected_answer)
        if not answer_relevancy and question_terms:
            answer_relevancy = len(answer_terms & question_terms) / len(question_terms)

        if contexts:
            context_list = list(contexts)
            context_text = " ".join(context_list)
            context_terms = RagasEvaluator._normalize_tokens(context_text)
            faithfulness = (
                len(answer_terms & context_terms) / len(answer_terms)
                if answer_terms
                else 0.0
            )

            relevant_contexts = 0
            for context in context_list:
                if RagasEvaluator._normalize_tokens(context) & reference_terms:
                    relevant_contexts += 1

            context_precision = (
                relevant_contexts / len(context_list) if context_list else 0.0
            )

            context_tokens = set()
            for context in context_list:
                context_tokens.update(RagasEvaluator._normalize_tokens(context))

            context_recall = (
                len(reference_terms & context_tokens) / len(reference_terms)
                if reference_terms
                else 0.0
            )
        else:
            faithfulness = 0.0
            context_precision = 0.0
            context_recall = 0.0

        score = round(
            (answer_relevancy + faithfulness + context_precision + context_recall) / 4,
            3,
        )

        return {
            "question": question,
            "score": score,
            "metrics": {
                "answer_relevancy": round(answer_relevancy, 3),
                "faithfulness": round(faithfulness, 3),
                "context_precision": round(context_precision, 3),
                "context_recall": round(context_recall, 3),
            },
        }


class SimpleEvaluator(RagasEvaluator):
    pass
