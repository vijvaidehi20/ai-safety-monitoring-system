import json
import sys
import os

sys.path.append("app")

from rag.multiquery_retriever import get_multiquery_results

TOP_K = 5

with open("evaluation/rag_eval_dataset.json") as f:
    dataset = json.load(f)

precisions = []
recalls = []
mrr_scores = []

print("\n----- RAG Evaluation -----\n")

for item in dataset:

    query = item["query"]
    relevant_docs = set(item["relevant_docs"])

    results = get_multiquery_results(query)

    # get unique sources
    retrieved_sources = []
    seen = set()

    for doc in results:
        src = os.path.basename(doc.metadata.get("source", ""))

        if src not in seen:
            retrieved_sources.append(src)
            seen.add(src)

    retrieved_sources = retrieved_sources[:TOP_K]

    retrieved_set = set(retrieved_sources)

    # True positives
    tp = len(retrieved_set & relevant_docs)

    # Precision
    precision = tp / len(retrieved_sources) if retrieved_sources else 0

    # Recall
    recall = tp / len(relevant_docs) if relevant_docs else 0

    # MRR
    rr = 0
    for rank, doc in enumerate(retrieved_sources, start=1):
        if doc in relevant_docs:
            rr = 1 / rank
            break

    precisions.append(precision)
    recalls.append(recall)
    mrr_scores.append(rr)

    # Print per query evaluation
    # print("Query:", query)
    # print("Retrieved:", retrieved_sources)
    # print("Relevant:", list(relevant_docs))
    # print("Precision:", round(precision, 3))
    # print("Recall:", round(recall, 3))
    # print("RR:", round(rr, 3))
    # print("---------------")

# Final scores
avg_precision = sum(precisions) / len(precisions)
avg_recall = sum(recalls) / len(recalls)
avg_mrr = sum(mrr_scores) / len(mrr_scores)

print("\n===== FINAL SCORES =====")
print("Precision:", round(avg_precision, 3))
print("Recall:", round(avg_recall, 3))
print("MRR:", round(avg_mrr, 3))
print("========================")