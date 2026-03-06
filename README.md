# 🚨 AI Safety Monitoring System

An AI-powered surveillance system that combines **Computer Vision + RAG (Retrieval Augmented Generation) + LangGraph agents** to detect suspicious activity in real time and trigger alerts.

The system monitors a camera feed, detects incidents such as **falls or suspicious gestures**, evaluates risk using **AI reasoning over safety protocols**, and sends alerts with captured evidence.

---

## 🎯 Features

- Real-time camera monitoring (OpenCV)
- Person detection using **YOLOv8**
- Gesture / fall detection
- **RAG-powered risk reasoning**
- LangGraph agent workflow
- Hybrid retrieval (Vector + BM25 + RRF)
- Incident image capture
- Telegram alert system
- Incident logging using JSON
- Streamlit monitoring dashboard

---

## 🧠 System Flow

Camera Feed → Person Detection → Incident Detection →  
RAG Reasoning → Risk Level → Alert → Incident Log → Dashboard

---

## ⚙️ Tech Stack

**Computer Vision**
- OpenCV
- YOLOv8 (Ultralytics)

**AI / RAG**
- LangChain
- LangGraph
- ChromaDB
- MultiQuery Retrieval
- HYDE Retrieval
- Hybrid Retrieval (BM25 + Vector + RRF)

**LLM**
- Ollama (Llama3)

**Monitoring**
- Streamlit Dashboard
- JSON Incident Logs

**Alerts**
- Telegram Bot API

---

## 📂 Project Structure
ai-safety-monitoring-system
│
├── app
│ ├── agents
│ ├── alerts
│ ├── dashboard
│ ├── rag
│ ├── utils
│ └── vision
│
├── chroma_db
├── incidents
├── logs
│ └── incidents.json
├── knowledge_base
└── sounds


---

## 🚀 Running the Project

### 1️⃣ Install dependencies
pip install -r requirements.txt

### 2️⃣ Start the monitoring system
python app/main.py

### 3️⃣ Run the dashboard
streamlit run app/dashboard/streamlit_app.py

---

## 📊 Dashboard

The Streamlit dashboard displays:

- system statistics  
- latest detected incident  
- incident history  
- incident image gallery  

---

## 📁 Incident Logging

Every detected event is stored in:
logs/incidents.json
Example:
{
"incident_id": "INC_20260307_004605",
"camera_id": "camera_1",
"people_count": 2,
"risk_level": "HIGH",
"image_path": "incidents/incident_20260307_004605.jpg",
"alert_sent": true
}

---

## 🔍 Knowledge Base

Safety reasoning is performed using documents inside:
knowledge_base/
These include safety protocols and legal references used by the RAG pipeline.

---

## 👩‍💻 Author

**Vaidehi Vij**  
