def calculate_risk(event_data: dict):
    """
    Deterministic risk scoring based on predefined rules.
    """

    score = 0
    breakdown = {}

    # Night check
    if event_data.get("is_night"):
        score += 2
        breakdown["Night"] = 2
    else:
        breakdown["Night"] = 0

    # gesture
    if event_data.get("gesture_detected"):
        score += 3
        breakdown["Gesture"] = 3

    # Lighting check
    if event_data.get("lighting") == "low":
        score += 2
        breakdown["Lighting"] = 2
    else:
        breakdown["Lighting"] = 0

    # Fall check
    if event_data.get("fall_detected"):
        score += 3
        breakdown["Fall"] = 3
    else:
        breakdown["Fall"] = 0

    # Crowd check
    if event_data.get("people_count", 0) > 2:
        score += 2
        breakdown["Crowd"] = 2
    else:
        breakdown["Crowd"] = 0

    # Determine level
    if score <= 2:
        level = "Low"
    elif score <= 5:
        level = "Medium"
    else:
        level = "High"

    return {
        "score": score,
        "level": level,
        "breakdown": breakdown
    }