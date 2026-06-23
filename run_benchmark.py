from app.benchmark.runner import BenchmarkRunner
from app.benchmark.sample_questions import QUESTIONS

document_id = input("Document ID: ")

results = BenchmarkRunner().run(
    document_id=document_id,
    questions=QUESTIONS,
)

for result in results:
    print(result)