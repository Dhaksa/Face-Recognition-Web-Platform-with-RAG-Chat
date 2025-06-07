# Face-Recognition-Web-Platform-with-RAG-Chat


A full-stack browser app for:
- 👤 Face registration via webcam
- 🧠 Real-time face recognition
- 💬 RAG-powered chatbot to query logs

## 🔧 Tech Stack
- Frontend: React.js  
- Backend: Node.js (API + WebSocket)  
- AI Modules: Python (Face recognition + RAG using OpenAI)  
- Logs: CSV/JSON/SQLite  

## 🚀 Setup

```bash
git clone https://github.com/your-username/face-recognition-platform.git
cd face-recognition-platform
````

* Install dependencies in `backend`, `frontend`, and `AI-Modules`
* Run:

  * `npm start` in `frontend`
  * `node index.js` in `backend`
  * Python scripts via API: `register.py`, `recognize.py`, `rag-chat.py`

## 📁 Logs

All events are saved in `logs.csv` with timestamp:

```
Name, Event, Timestamp
```

## 🏗 Architecture

![Architecture](./assets/architecture-diagram.png)

## 📹 Demo

🎥 [Watch Loom Demo](https://www.loom.com/share/sample-link)

## 📝 Assumptions

* Unique names used for face registration
* Multi-user support on single device
* Logs stored in CSV or SQLite

---

This project is a part of a hackathon run by [https://katomaran.com](https://katomaran.com)

```

---

Let me know if you want the diagram image or a GitHub repo scaffold too!
```
