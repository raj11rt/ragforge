from app.evaluation.evaluator import RagasEvaluator


def test_evaluate_single_returns_ragas_metrics():
    result = RagasEvaluator.evaluate_single(
        question="What is the capital of France?",
        answer="Paris is the capital of France.",
        expected_answer="The capital of France is Paris.",
        contexts=[
            "France is a country in Europe.",
            "Paris is the capital city of France.",
        ],
    )

    assert "question" in result
    assert "score" in result
    assert result["score"] >= 0.0
    assert result["score"] <= 1.0
    assert result["metrics"]["answer_relevancy"] >= 0.0
    assert result["metrics"]["faithfulness"] >= 0.0
    assert result["metrics"]["context_precision"] >= 0.0
    assert result["metrics"]["context_recall"] >= 0.0
