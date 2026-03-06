from agents.graph import build_graph

graph = build_graph()

event_data = {
    "is_night": True,
    "lighting": "low",
    "fall_detected": True,
    "gesture_detected": True,
    "people_count": 3,
    "latitude": 30.7333,
    "longitude": 76.7794
}

query = "A woman fell at night with multiple people nearby."

initial_state = {
    "query": query,
    "event_data": event_data
}

result = graph.invoke(initial_state)

print(result["explanation"])