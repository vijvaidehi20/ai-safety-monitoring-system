from langchain_ollama import ChatOllama
from rag.risk_engine import calculate_risk
from rag.multiquery_retriever import get_multiquery_results
from rag.hyde_retriever import get_hyde_results

def run_rag(query: str):
# def run_rag(query: str, event_data: dict):

    # Simulated event metadata (later this comes from OpenCV)
    event_data = {
        "is_night": True,
        "lighting": "low",
        "fall_detected": True,
        "people_count": 3
    }

    # Step 1: Deterministic scoring
    risk_result = calculate_risk(event_data)

    # Step 2: Retrieve context
    # retriever = get_retriever()
    # retrieved_docs = retriever.invoke(query)

    # hybrid_search = get_hybrid_retriever()
    # retrieved_docs = hybrid_search(query)

    # MultiQuery results
    multiquery_docs = get_multiquery_results(query)

    # HYDE results
    hyde_docs = get_hyde_results(query)

    # Merge & deduplicate
    all_docs = multiquery_docs + hyde_docs
    unique_docs = list({doc.page_content: doc for doc in all_docs}.values())

    retrieved_docs = unique_docs[:3]
    
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])

    # Step 3: LLM explains reasoning only
    llm = ChatOllama(model="llama3")

    prompt = f"""
    You are an AI safety assistant.

    Context:
    {context}

    Scenario:
    {query}

    The system has already calculated:

    Risk Level: {risk_result['level']}
    Risk Score: {risk_result['score']}
    Breakdown: {risk_result['breakdown']}

    Explain clearly why this risk level is appropriate.
    Then provide recommended actions.
    """

    explanation = llm.invoke(prompt)

    return {
        "Risk Level": risk_result["level"],
        "Risk Score": risk_result["score"],
        "Breakdown": risk_result["breakdown"],
        "LLM Explanation": explanation.content
    }