# 🚨 AI Safety Monitoring System

An AI-powered video surveillance application that combines **Computer Vision, RAG (Retrieval-Augmented Generation), and LangGraph agents** to detect suspicious activity in real time and rapidly trigger alerts. 

The system monitors camera feeds, detects potentially dangerous incidents (such as falls or suspicious gestures), evaluates the risk using AI reasoning against documented safety protocols, and sends immediate alerts containing captured visual evidence.

---

## 🎯 Features

- **Real-time Monitoring:** Processes live camera streams using OpenCV.
- **Person & Pose Detection:** Powered by YOLOv8 for accurate bounding boxes and keypoints.
- **Incident Recognition:** Specialized detection for gestures, falls, and potential threats.
- **RAG-Powered Risk Reasoning:** Analyzes the detected incident context against established safety documents.
- **Advanced Retrieval:** Combines Vector Search, BM25, and Reciprocal Rank Fusion (RRF) with MultiQuery and HYDE techniques.
- **LangGraph Workflows:** Orchestrates AI agents for evaluating threats systematically.
- **Automated Alerts:** Sends instant notifications with images via Telegram API.
- **Incident Dashboard:** Real-time log visualization using Streamlit.
- **Persistent Logging:** Stores events structured in JSON files.

---

## 🧠 System Architecture & Data Flow

1. **Camera Feed:** Captured frame-by-frame.
2. **Computer Vision:** YOLOv8 detects persons and actions.
3. **Incident Detection:** System flags unusual positioning or behaviors.
4. **RAG Reasoning:** LangGraph agents fetch protocols via ChromaDB and evaluate the situation.
5. **Risk Classification:** Assigns a risk level (e.g., `LOW`, `MEDIUM`, `HIGH`).
6. **Action Execution:** If `HIGH` risk, coordinates an alert (Telegram) and captures images.
7. **Logging & Dashboard:** Saves JSON records and updates the Streamlit interface.

---

## ⚙️ Tech Stack

### Computer Vision
- **OpenCV**
- **YOLOv8** (Ultralytics)

### AI & RAG Pipeline
- **LangChain & LangGraph**
- **ChromaDB** (Vector Database)
- **Ollama** (Running LLaMA3 locally)

### Backend & Monitoring
- **Python 3.11+**
- **Streamlit** (Dashboard UI)
- **Telegram Bot API** (Notifications)

---

## 🚀 Setup & Installation

### 1️⃣ Clone the Repository & Setup Virtual Environment
```bash
git clone <your-repository-url>
cd women_safety_rag
python -m venv venv311
source venv311/bin/activate  # On Windows use `venv311\Scripts\activate`
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Configure Environment Variables
Create a `.env` file in the root directory and add your API keys:
```ini
# .env
TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
TELEGRAM_CHAT_ID="your_telegram_chat_id"
# Add any API keys necessary for your models if not using Ollama exclusively locally
```

### 4️⃣ Start the Core System
In your main terminal, start the backend monitoring process:
```bash
python app/main.py
```

### 5️⃣ Launch the Dashboard
In a separate terminal, run the monitoring dashboard:
```bash
streamlit run app/dashboard/streamlit_app.py
```

---

## 📁 System Directories

- `app/` - Main application logic, including CV, AI Agents, and RAG pipelines.
- `chroma_db/` - Persistent vector storage for document embeddings (ignored in git).
- `incidents/` - Directory where incident screenshot evidence is stored.
- `logs/` - JSON files storing structured system alerts.
- `knowledge_base/` - Documents, PDF guidelines, and safety rules used by the RAG pipeline.

### Example Logs (`logs/incidents.json`)
```json
{
  "incident_id": "INC_20260307_004605",
  "camera_id": "camera_1",
  "people_count": 2,
  "risk_level": "HIGH",
  "image_path": "incidents/incident_20260307_004605.jpg",
  "alert_sent": true
}
```

---

## 👩‍💻 Author

**Vaidehi Vij**
