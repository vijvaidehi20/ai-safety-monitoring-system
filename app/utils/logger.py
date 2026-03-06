import json
import os
from datetime import datetime

LOG_FILE = "logs/incidents.json"


def generate_incident_id():
    now = datetime.now()
    return f"INC_{now.strftime('%Y%m%d_%H%M%S')}"


def log_incident(data):

    os.makedirs("logs", exist_ok=True)

    try:
        with open(LOG_FILE, "r") as f:
            incidents = json.load(f)
    except:
        incidents = []

    incidents.append(data)

    with open(LOG_FILE, "w") as f:
        json.dump(incidents, f, indent=4)


def update_alert_status(incident_id, method):
    import json
    from datetime import datetime

    LOG_FILE = "logs/incidents.json"

    with open(LOG_FILE, "r") as f:
        incidents = json.load(f)

    for incident in incidents:
        if incident["incident_id"] == incident_id:

            alert_time = datetime.now()

            incident["alert_sent"] = True
            incident["alert_method"] = method
            incident["alert_trigger_time"] = alert_time.strftime("%Y-%m-%d %H:%M:%S")
            incident["alert_delivery_status"] = "sent"

            # ---- Calculate response time ----
            escalation_time = datetime.strptime(
                incident["risk_escalation_time"],
                "%Y-%m-%d %H:%M:%S"
            )

            response_time = (alert_time - escalation_time).total_seconds()

            incident["response_time_sec"] = round(response_time, 2)

            break

    with open(LOG_FILE, "w") as f:
        json.dump(incidents, f, indent=4)

# What This Code Does

# Gets current time when alert is sent.
# alert_time = datetime.now()

# Reads risk escalation time from log
# incident["risk_escalation_time"]

# Converts it back to datetime
# datetime.strptime(...)

# Subtracts times
# alert_time - escalation_time

# Converts to seconds
# .total_seconds()

# Saves in JSON.


def update_alert_failure(incident_id):

    with open(LOG_FILE, "r") as f:
        incidents = json.load(f)

    for incident in incidents:
        if incident["incident_id"] == incident_id:
            incident["alert_delivery_status"] = "failed"
            break

    with open(LOG_FILE, "w") as f:
        json.dump(incidents, f, indent=4)