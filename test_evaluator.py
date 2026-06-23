# test_evaluator.py

from app.evaluation.evaluator import SimpleEvaluator

result = SimpleEvaluator.evaluate_single(
    question="What is Python?",
    answer="Python is a programming language.",
    expected_answer="Python is a programming language."
)

print(result)