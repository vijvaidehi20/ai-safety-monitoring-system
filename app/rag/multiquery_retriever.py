from langchain_ollama import ChatOllama
from rag.hybrid_retriever import get_hybrid_retriever


def generate_query_variations(query: str):
    llm = ChatOllama(model="llama3")

    prompt = f"""
Generate 3 different rephrased search queries 
for retrieving safety-related documents.

Original query:
{query}

Return them as a numbered list.
"""

    response = llm.invoke(prompt).content

    lines = response.split("\n")
    variations = []

    for line in lines:
        if line.strip() and any(char.isdigit() for char in line[:3]):
            cleaned = line.split(".", 1)[-1].strip()
            variations.append(cleaned)

    # print("\nGenerated Query Variations:")
    # for v in variations:
    #     print("-", v)

    return variations


def get_multiquery_results(query: str):
    hybrid_search = get_hybrid_retriever()

    variations = generate_query_variations(query)

    all_results = []

    # Include original query too
    queries = [query] + variations

    for q in queries:
        results = hybrid_search(q)
        all_results.extend(results)

    # Deduplicate
    unique_docs = list({doc.page_content: doc for doc in all_results}.values())

    return unique_docs[:3]