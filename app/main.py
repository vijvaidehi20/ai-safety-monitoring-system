from agents.graph import build_graph
from vision.camera import run_camera_detection


def format_report(result):
    print("\n" + "="*60)
    print("        WOMEN SAFETY RISK ASSESSMENT REPORT")
    print("="*60)

    if "risk_result" in result:
        print(f"\nRisk Level  : {result['risk_result']['level']}")
        print(f"Risk Score  : {result['risk_result']['score']}")

        print("\nBreakdown:")
        for key, value in result["risk_result"]["breakdown"].items():
            print(f"  • {key:<20} : +{value}")

    if "explanation" in result:
        print("\nSystem Decision:\n")
        print(result["explanation"])

    print("="*60 + "\n")


if __name__ == "__main__":

    print("\nStarting Women Safety Monitoring System...")
    print("Press 'q' in camera window to capture event.\n")

    # Step 1: Capture event from webcam
    event_data = run_camera_detection()

    if not event_data:
        print("No event captured. Exiting.")
        exit()

    # Step 2: Build LangGraph
    graph = build_graph()

    # Step 3: Create structured query
    query = (
        "Potential emergency gesture or suspicious activity detected. "
        "Assess risk level and recommend action."
    )

    print("\nEVENT DATA PASSED TO GRAPH:")
    print(event_data)
    
    initial_state = {
        "query": query,
        "event_data": event_data
    }

    
    # Step 4: Run Graph
    result = graph.invoke(initial_state)

    # Step 5: Print Report
    format_report(result)