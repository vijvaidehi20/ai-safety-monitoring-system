from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)

from datasets import Dataset


def run_ragas(question, contexts, answer, ground_truth):

    data = {
        "question": [question],
        "contexts": [contexts],
        "answer": [answer],
        "ground_truth": [ground_truth]
    }

    dataset = Dataset.from_dict(data)

    result = evaluate(
        dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall
        ]
    )

    return result