import cv2
from ultralytics import YOLO
import mediapipe as mp
from datetime import datetime
import numpy as np
import time
from utils.logger import log_incident, generate_incident_id
import os
from utils.logger import update_alert_status
from rag.pipeline import run_rag

os.makedirs("incidents", exist_ok=True)

# Load pretrained YOLO model
model = YOLO("yolov8n.pt")

# MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()


def detect_hands_raised(landmarks):
    """
    Detect both hands raised clearly above shoulders.
    """

    left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
    right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

    margin = 0.08  # strict threshold

    left_up = left_wrist.y < (left_shoulder.y - margin)
    right_up = right_wrist.y < (right_shoulder.y - margin)

    return left_up and right_up

def draw_panel_text(frame, text, position, color=(255,255,255), scale=0.6):
    """
    Draw text with black outline for visibility.
    """
    x, y = position

    # outline
    cv2.putText(frame, text, (x,y),
                cv2.FONT_HERSHEY_SIMPLEX,
                scale, (0,0,0), 4)

    # main text
    cv2.putText(frame, text, (x,y),
                cv2.FONT_HERSHEY_SIMPLEX,
                scale, color, 2)
    
# previous_risk_level = "LOW"
# alert_sent_for_event = False

def run_camera_detection():

    import os
    # filename = os.path.basename(event_data["frame_path"])
    from datetime import datetime
    
    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

    if not cap.isOpened():
        print("Camera not accessible")
        return None

    print("Press 'q' to capture event")

    fall_detected = False
    gesture_detected = False
    gesture_counter = 0
    people_count = 0

    flash_state = True
    last_flash_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (960, 540))

        # ---------------- YOLO Person Detection ----------------
        results = model.predict(frame, verbose=False)
        people_count = 0

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                confidence = float(box.conf[0])

                if model.names[cls_id] == "person" and confidence > 0.5:
                    people_count += 1

                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                    cv2.putText(frame, "Person", (x1, y1-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

        # ---------------- MediaPipe Pose ----------------
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pose_results = pose.process(rgb_frame)

        if pose_results.pose_landmarks:
            landmarks = pose_results.pose_landmarks.landmark

            if detect_hands_raised(landmarks):
                gesture_counter += 1
            else:
                gesture_counter = 0

        # Require gesture to stay stable for 15 frames
        if gesture_counter > 15:
            gesture_detected = True

        # ---------------- Lighting Detection ----------------
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = gray.mean()

        if brightness < 60:
            lighting = "Low"
        else:
            lighting = "Normal"

        # Flash toggle every 0.5 seconds
        if time.time() - last_flash_time > 0.5:
            flash_state = not flash_state
            last_flash_time = time.time()

        # ---------------- Display Info ----------------
        risk_level = "LOW"

        if fall_detected or gesture_detected:
            risk_level = "HIGH"
        elif people_count >= 3:
            risk_level = "MEDIUM"

        if risk_level == "HIGH" and flash_state:
            cv2.rectangle(frame, (0,0), (frame.shape[1], 60), (0,0,255), -1)

            cv2.putText(frame,
                "HIGH RISK ALERT - AUTHORITIES NOTIFIED",
                (220,40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255,255,255),
                2
            )

        # ---------------- DRAW INFO PANEL ----------------

        overlay = frame.copy()

        panel_x1 = 10
        panel_y1 = 55
        panel_x2 = 300
        panel_y2 = 240

        # dark rectangle
        cv2.rectangle(overlay, (panel_x1, panel_y1),
                    (panel_x2, panel_y2),
                    (0,0,0), -1)

        # transparency
        alpha = 0.55
        frame = cv2.addWeighted(overlay, alpha, frame, 1-alpha, 0)

        # panel text
        # draw_panel_text(frame, "AI SAFETY PANEL", (20,40), (0,255,255), 0.7)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        draw_panel_text(frame, f"Time: {current_time}", (20,80), (255,255,255))

        draw_panel_text(frame, f"People: {people_count}", (20,115), (0,255,0))

        draw_panel_text(frame, f"Gesture: {gesture_detected}", (20,150), (0,0,255))

        draw_panel_text(frame, f"Lighting: {lighting}", (20,185), (255,255,0))

        # risk color
        risk_color = (0,255,0)
        if risk_level == "HIGH":
            risk_color = (0,0,255)
        elif risk_level == "MEDIUM":
            risk_color = (0,165,255)

        draw_panel_text(frame, f"Risk: {risk_level}", (20,220), risk_color, 0.7)
        
        panel_width = 250
        panel = np.zeros((frame.shape[0], panel_width, 3), dtype=np.uint8)
        
        # cv2.imshow("Women Safety Camera", frame)
        combined = np.hstack((panel, frame))
        cv2.imshow("Women Safety Camera", combined)

        key = cv2.waitKey(1)

        # press 'f' to simulate fall
        if key == ord('f'):
            fall_detected = True
            print("Fall event triggered")
        
        # previous_risk_level = risk_level

        if key == ord('q'):
            current_time = datetime.now().hour

            event_data = {
                "is_night": current_time >= 20 or current_time <= 5,
                "lighting": lighting,
                "fall_detected": fall_detected,
                "gesture_detected": gesture_detected,
                "people_count": people_count,
                "latitude": 30.7333,
                "longitude": 76.7794
            }

            # Build query for RAG
            query = f"""
            Potential emergency detected.

            Lighting: {lighting}
            People detected: {people_count}
            Gesture detected: {gesture_detected}
            Fall detected: {fall_detected}

            Assess risk and recommend action.
            """

            rag_result = run_rag(query)

            rag_reasoning = rag_result["LLM Explanation"]

            # Save incident frame
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"incident_{timestamp}.jpg"
            filepath = os.path.join("incidents", filename)

            cv2.imwrite(filepath, frame)

            print(f"Incident frame saved: {filepath}")

            event_data["frame_path"] = filepath

            # --------------------------------------------------
            incident_id = generate_incident_id()
            event_data["incident_id"] = incident_id
            risk_escalation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            incident_data = {
                "incident_id": incident_id,
                "detection_start_time": risk_escalation_time,   # first detection
                "risk_escalation_time": risk_escalation_time,   # moment risk became HIGH
                "camera_id": "camera_1",
                "people_count": people_count,
                "gesture_detected": gesture_detected,
                "lighting": lighting,
                "risk_level": risk_level,
                "confidence": 1.0,  # placeholder (can later use YOLO confidence)
                "image_path": filepath,
                "rag_reasoning": rag_reasoning,
                "alert_sent": False,
                "alert_method": None,
                "alert_trigger_time": None,
                "alert_delivery_status": "pending"
            }
            # STEP 1 — log incident
            log_incident(incident_data)

            # STEP 2 — after telegram alert succeeds
            update_alert_status(event_data["incident_id"], "telegram")

            # --------------------------------------------------

            cap.release()
            cv2.destroyAllWindows()

            return event_data