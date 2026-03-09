from langchain_ollama import ChatOllama
from rag.multiquery_retriever import get_multiquery_results
from rag.hyde_retriever import get_hyde_results
from alerts.alert_system import trigger_alert
from utils.logger import update_alert_status
from utils.logger import update_alert_failure
from rag.risk_engine import calculate_risk

from .state import GraphState


# ---- Retrieval Node ----
def retrieval_node(state: GraphState):

    query = state["query"]

    multi_docs = get_multiquery_results(query)
    hyde_docs = get_hyde_results(query)

    all_docs = multi_docs + hyde_docs

    unique_docs = list({doc.page_content: doc for doc in all_docs}.values())

    return {"documents": unique_docs[:3]}


# ---- Risk Engine Node ----
def risk_node(state: GraphState):

    event_data = state["event_data"]

    risk_result = calculate_risk(event_data)

    return {"risk_result": risk_result}


# ---- Explanation Node ----
def explanation_node(state: GraphState):

    llm = ChatOllama(model="llama3")

    context = "\n\n".join([doc.page_content for doc in state["documents"]])

    risk_result = state["risk_result"]
    event_data = state["event_data"]

    prompt = f"""
    You are a technical AI safety monitoring system.

    Do not use conversational phrases.
    Be formal and concise.

    Context:
    {context}

    Scenario:
    {state['query']}

    Location:
    Latitude: {event_data['latitude']}
    Longitude: {event_data['longitude']}

    Risk Level: {risk_result['level']}
    Risk Score: {risk_result['score']}
    Breakdown: {risk_result['breakdown']}

    Explain why this risk assessment is correct.
    Provide recommended actions.
    """

    response = llm.invoke(prompt)

    # explanation = f"Risk assessment is based on deterministic rules. Level: {risk_result['level']}, Score: {risk_result['score']}, Breakdown: {risk_result['breakdown']}. Recommended: Monitor situation."

    return {"explanation": response.content}


# ---- Router ----
def risk_router(state: GraphState):

    level = state["risk_result"]["level"].strip().lower()

    if level in ["medium", "high"]:
        return "alert"

    return "explanation"

# ---- Alert Node ----
def alert_node(state: GraphState):

    risk_result = state["risk_result"]
    event_data = state["event_data"]

    try:
        alert_status = trigger_alert(risk_result, event_data)

        # Update incident log if alert succeeded
        update_alert_status(event_data["incident_id"], "telegram")

    except Exception as e:
        print("Telegram alert failed:", e)

        update_alert_failure(event_data["incident_id"])

        alert_status = "failed"

    return {"alert": alert_status}