

# Face Recognition Web Platform with RAG Chat 

A full-stack browser-based platform to:

* 👤 Register user faces via webcam
* 🔍 Recognize faces in real-time
* 💬 Query face logs with a RAG-powered chatbot (LLM-based)

---

## 🧰 Tech Stack

| Layer    | Technology                      |
| -------- | ------------------------------- |
| Frontend | React.js                        |
| Backend  | Node.js (API + WebSocket)       |
| AI Layer | Python (Face Recognition + RAG) |
| Database | SQLite / CSV logs               |

---

## 🚀 Project Structure

```
Face-Recognition-Web-Platform-with-RAG-Chat/
│
├── AI-Modules/                 # Python scripts for AI processing
│   ├── register.py            # Face registration
│   ├── recognize.py           # Real-time recognition
│   └── rag-chat.py            # Chat with logs (RAG)
│
├── client/                    # React.js frontend
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── README.md
│
├── server/                    # Node.js backend
│   ├── known_faces/           # Saved face images
│   ├── App.js                 # API & WebSocket server
│   ├── faces.db               # SQLite database
│   ├── logs.csv               # CSV log storage
│   ├── package.json
│   └── node_modules/
│
├── .gitignore
├── package-lock.json
├── README.md                  # You’re reading this
```

---

## 📦 Installation & Run

1. **Clone the repo**

   ```bash
   git clone https://github.com/your-username/Face-Recognition-Web-Platform-with-RAG-Chat.git
   cd Face-Recognition-Web-Platform-with-RAG-Chat
   ```

2. **Install dependencies**

   ```bash
   cd client && npm install      # for frontend
   cd ../server && npm install   # for backend
   pip install -r requirements.txt  # for AI-Modules (you can create this file)
   ```

3. **Run everything**

   ```bash
   # Start frontend
   cd client && npm start

   # Start backend
   cd ../server && node App.js

   # Python scripts are auto-triggered via API (no need to run manually)
   ```

---

## 🧠 Features

* Face registration using webcam
* Real-time recognition with name display and logging
* Registration, login, logout tracked in `logs.csv`
* Chatbot powered by LLM + FAISS vector store (RAG)
* Log queries like:

  * "Who was the last person registered?"
  * "How many users logged out today?"
  * "When did Dhaks log in?"

---

## 🗃 Sample Logs

`logs.csv` (stored in `/server`):

```
Name, Action, Timestamp
Dhaks, Registered, 2025-06-07 11:03:12
Dhaks, Login,      2025-06-07 12:30:00
```

---

## 📊 Architecture

![image](https://github.com/user-attachments/assets/d53d077d-7b75-4891-89ca-2c624d260a0d)


---

## 📹 Demo

https://kumaragurudtsteam-my.sharepoint.com/:v:/g/personal/dhaksana_22ad_kct_ac_in/EWy208Z7x-tBk8Unslmif5kByVYKXnrtzC23-y_uPk9UEw?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=YUHyrm
---

## 📝 Notes

* Names must be unique during registration
* Supports multiple users on the same device
* Logs can be stored in both CSV and SQLite

---

### 🎓 Built by Dhaksana N

This project was developed as part of a hackathon conducted by [Katomaran](https://katomaran.com).

---

