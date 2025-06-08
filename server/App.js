const express = require("express");
const cors = require("cors");
const { spawn } = require("child_process");
const http = require("http");
const { Server } = require("socket.io");

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: { origin: "http://localhost:3000", methods: ["GET", "POST"] }
});

app.use(cors());
app.use(express.json());
app.use('/known_faces', express.static('../AI-Modules/known_faces'));

// ✅ Updated /api/register to accept name and pass to Python
app.post("/api/register", (req, res) => {
  const { name } = req.body;
  if (!name) return res.status(400).json({ error: "Name is required" });

  const process = spawn("python", ["../AI-Modules/register.py", name]);

  process.stdout.on("data", (data) => console.log(`[REGISTER STDOUT]: ${data}`));
  process.stderr.on("data", (data) => console.error(`[REGISTER STDERR]: ${data}`));
  process.on("close", (code) => {
    res.json({ status: "Register completed", code });
  });
});

// ✅ Recognition route
app.post("/api/recognize", (req, res) => {
  const process = spawn("python", ["../AI-Modules/recognize.py"]);
  process.stdout.on("data", (data) => console.log(`[RECOGNIZE]: ${data}`));
  process.stderr.on("data", (data) => console.error(`[RECOGNIZE ERROR]: ${data}`));
  process.on("close", (code) => res.send({ status: "Recognition finished", code }));
});

// ✅ RAG Chat route
app.post("/api/chat", (req, res) => {
  const question = req.body.question;
  const process = spawn("python", ["../AI-Modules/rag-chat.py", question]);
  let response = "";

  process.stdout.on("data", (data) => response += data.toString());
  process.stderr.on("data", (data) => console.error(`[CHAT ERROR]: ${data}`));
  process.on("close", () => {
    res.json({ answer: response.trim() });
  });
});

// ✅ WebSocket setup
io.on("connection", (socket) => {
  console.log("WebSocket client connected");
  socket.emit("message", "Connected to WebSocket server.");
});

// ✅ Start server
const PORT = 5000;
server.listen(PORT, () => {
  console.log(`✅ Backend running at http://localhost:${PORT}`);
});
