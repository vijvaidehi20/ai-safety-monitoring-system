# from langgraph.graph import StateGraph, END
# from typing import TypedDict, List
# from langchain_core.documents import Document

# from rag.multiquery_retriever import get_multiquery_results
# from rag.hyde_retriever import get_hyde_results
# from rag.risk_engine import calculate_risk
# from langchain_ollama import ChatOllama

# from alerts.alert_system import trigger_alert


# # ---- Define Graph State ----
# class GraphState(TypedDict):
#     query: str
#     event_data: dict
#     documents: List[Document]
#     risk_result: dict
#     explanation: str
#     alert: dict


# # ---- Node 1: Retrieval ----
# def retrieval_node(state: GraphState):
#     query = state["query"]

#     multi_docs = get_multiquery_results(query)
#     hyde_docs = get_hyde_results(query)

#     all_docs = multi_docs + hyde_docs
#     unique_docs = list({doc.page_content: doc for doc in all_docs}.values())

#     return {"documents": unique_docs[:3]}


# # ---- Node 2: Risk Engine ----
# def risk_node(state: GraphState):

#     event_data = state["event_data"]

#     risk_result = {
#         "level": "High",
#         "score": 10,
#         "breakdown": {
#             "night": True,
#             "lighting": "low",
#             "fall": True,
#             "crowd": True
#         }
#     }

#     return {"risk_result": risk_result}

# # ---- Node 3: Explanation ----
# def explanation_node(state: GraphState):

#     llm = ChatOllama(model="llama3")

#     context = "\n\n".join([doc.page_content for doc in state["documents"]])

#     risk_result = state["risk_result"]

#     event_data = state["event_data"]

#     prompt = f"""
#     You are a technical AI safety monitoring system.

#     Do not use conversational phrases.
#     Be formal and concise.

#     Context:
#     {context}

#     Scenario:
#     {state['query']}

#     Location:
#     Latitude: {event_data['latitude']}
#     Longitude: {event_data['longitude']}

#     Risk Level: {risk_result['level']}
#     Risk Score: {risk_result['score']}
#     Breakdown: {risk_result['breakdown']}

#     Explain why this risk assessment is correct.
#     Provide recommended actions.
#     """
    
#     response = llm.invoke(prompt)

#     return {"explanation": response.content}

# def risk_router(state: GraphState):
#     level = state["risk_result"]["level"]

#     if level == "High":
#         return "alert"
#     else:
#         return "explanation"

# # ---- Node 4: Alert Node ----
# def alert_node(state: GraphState):

#     print("\n🚨 ALERT NODE EXECUTING\n")
#     risk_result = state["risk_result"]
#     event_data = state["event_data"]

#     alert_status = trigger_alert(risk_result, event_data)

#     return {"alert": alert_status}

# # ---- Build Graph ----
# def build_graph():

#     workflow = StateGraph(GraphState)

#     workflow.add_node("retrieval", retrieval_node)
#     workflow.add_node("risk_engine", risk_node)
#     workflow.add_node("explanation", explanation_node)
#     workflow.add_node("alert", alert_node)

#     workflow.set_entry_point("retrieval")

#     workflow.add_edge("retrieval", "risk_engine")
#     workflow.add_conditional_edges(
#         "risk_engine",
#         risk_router
#     )
#     workflow.add_edge("alert", "explanation")
#     workflow.add_edge("explanation", END)

#     return workflow.compile()


from langgraph.graph import StateGraph, END

from .state import GraphState
from .nodes import retrieval_node, risk_node, explanation_node, alert_node, risk_router

def build_graph():

    workflow = StateGraph(GraphState)

    workflow.add_node("retrieval", retrieval_node)
    workflow.add_node("risk_engine", risk_node)
    workflow.add_node("explanation", explanation_node)
    workflow.add_node("alert", alert_node)

    workflow.set_entry_point("retrieval")

    workflow.add_edge("retrieval", "risk_engine")

    workflow.add_conditional_edges(
        "risk_engine",
        risk_router
    )

    workflow.add_edge("alert", "explanation")

    workflow.add_edge("explanation", END)

    return workflow.compile()

    