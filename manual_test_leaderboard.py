from app.benchmark.runner import BenchmarkRunner
from app.benchmark.sample_questions import QUESTIONS
from app.benchmark.leaderboard import Leaderboard

document_id = input("Document ID: ")

results = BenchmarkRunner().run(
    document_id=document_id,
    questions=QUESTIONS,
)

board = Leaderboard.build(results)

for item in board:
    print(item)