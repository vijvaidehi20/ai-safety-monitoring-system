import requests
import datetime
import uuid
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def trigger_alert(risk_result, event_data):

    frame_path = event_data.get("frame_path", None)
    filename = os.path.basename(event_data.get("frame_path", "No image"))
    
    incident_id = str(uuid.uuid4())[:8]
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = f"""
    🚨 WOMEN SAFETY ALERT

    Incident ID: {incident_id}
    Time: {timestamp}

    Risk Level: {risk_result['level']}
    People Nearby: {event_data['people_count']}

    Location:
    {event_data['latitude']}, {event_data['longitude']}

    Evidence: {filename}
    """

    # url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    # payload = {
    #     "chat_id": CHAT_ID,
    #     "text": message
    # }

    # if risk_result['level'].lower() == "high":
    #     os.system("afplay sounds/siren.mp3")

    print("Sending Telegram alert...")
    if frame_path and os.path.exists(frame_path):

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

        with open(frame_path, "rb") as photo:

            payload = {
                "chat_id": CHAT_ID,
                "caption": message
            }

            files = {
                "photo": photo
            }

            response = requests.post(url, data=payload, files=files)

    else:
        # fallback if image missing
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        payload = {
            "chat_id": CHAT_ID,
            "text": message
        }

        response = requests.post(url, data=payload)

    print("Telegram response:", response.json())

    return {"alert_status": "sent"}