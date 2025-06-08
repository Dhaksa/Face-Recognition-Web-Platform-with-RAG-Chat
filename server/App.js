const express = require("express");
const cors = require("cors");
const { spawn } = require("child_process");
const http = require("http");
const { Server } = require("socket.io");
const path = require("path");

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: { origin: "http://localhost:3000", methods: ["GET", "POST"] }
});

app.use(cors());
app.use(express.json());

// Serve static known faces folder
app.use('/known_faces', express.static(path.join(__dirname, "known_faces")));

// === Register Endpoint ===
app.post("/api/register", (req, res) => {
  const { name } = req.body;
  if (!name) return res.status(400).json({ error: "Name is required" });

  const registerProcess = spawn("python", [path.join(__dirname, "../AI-Modules/register.py"), name]);

  registerProcess.stdout.on("data", data => console.log(`[REGISTER STDOUT]: ${data}`));
  registerProcess.stderr.on("data", data => console.error(`[REGISTER STDERR]: ${data}`));
  registerProcess.on("close", code => {
    if (code === 0) {
      res.json({ status: "✅ Register completed", code });
    } else {
      res.status(500).json({ error: "❌ Register process failed", code });
    }
  });
});

// === Login Endpoint ===
app.post("/api/login", (req, res) => {
  const loginProcess = spawn("python", [path.join(__dirname, "../AI-Modules/recognize.py"), "Login"]);

  loginProcess.stdout.on("data", data => console.log(`[LOGIN]: ${data}`));
  loginProcess.stderr.on("data", data => console.error(`[LOGIN ERROR]: ${data}`));
  loginProcess.on("close", code => {
    if (code === 0) {
      res.json({ status: "✅ Login done", code });
    } else {
      res.status(500).json({ error: "❌ Login failed", code });
    }
  });
});

// === Logout Endpoint ===
app.post("/api/logout", (req, res) => {
  const logoutProcess = spawn("python", [path.join(__dirname, "../AI-Modules/recognize.py"), "Logout"]);

  logoutProcess.stdout.on("data", data => console.log(`[LOGOUT]: ${data}`));
  logoutProcess.stderr.on("data", data => console.error(`[LOGOUT ERROR]: ${data}`));
  logoutProcess.on("close", code => {
    if (code === 0) {
      res.json({ status: "✅ Logout done", code });
    } else {
      res.status(500).json({ error: "❌ Logout failed", code });
    }
  });
});

// === RAG Chat Route ===
app.post("/api/chat", (req, res) => {
  const question = req.body.question;
  if (!question) return res.status(400).json({ error: "Question is required" });

  const chatProcess = spawn("python", [path.join(__dirname, "../AI-Modules/rag-chat.py"), question]);
  let response = "";

  chatProcess.stdout.on("data", data => response += data.toString());
  chatProcess.stderr.on("data", data => console.error(`[CHAT ERROR]: ${data}`));
  chatProcess.on("close", () => {
    res.json({ answer: response.trim() });
  });
});

// === WebSocket Server ===
io.on("connection", socket => {
  console.log("🟢 WebSocket client connected");
  socket.emit("message", "Connected to WebSocket server.");
});

// === Start Server ===
const PORT = 5000;
server.listen(PORT, () => {
  console.log(`✅ Backend running at http://localhost:${PORT}`);
});
