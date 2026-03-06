from typing import TypedDict, List
from langchain_core.documents import Document

class GraphState(TypedDict):
    query: str
    event_data: dict
    documents: List[Document]
    risk_result: dict
    explanation: str
    alert: dict