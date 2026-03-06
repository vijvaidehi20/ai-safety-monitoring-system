from langchain_ollama import ChatOllama
from rag.hybrid_retriever import get_hybrid_retriever


def generate_hypothetical_answer(query: str):
    llm = ChatOllama(model="llama3")

    prompt = f"""
Write a detailed hypothetical safety incident analysis 
for the following scenario.

Scenario:
{query}

Focus on safety rules, risk assessment, and possible actions.
"""

    response = llm.invoke(prompt).content
    return response


def get_hyde_results(query: str):
    hybrid_search = get_hybrid_retriever()

    # Step 1: Generate hypothetical document
    hypothetical_doc = generate_hypothetical_answer(query)

    # print("\n========== HYDE GENERATED DOCUMENT ==========\n")
    # print(hypothetical_doc)
    # print("\n=============================================\n")

    # Step 2: Use hypothetical document as retrieval query
    results = hybrid_search(hypothetical_doc)

    return results[:3]