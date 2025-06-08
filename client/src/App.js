import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

export default function App() {
  const [name, setName] = useState('');
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [log, setLog] = useState('');
  const [loading, setLoading] = useState(false);

  const handleRegister = async () => {
    if (!name) return alert("Enter a name");
    setLog('Registering...');
    try {
      const res = await axios.post('http://localhost:5000/api/register', { name });
      setLog(`✅ Registered ${name}.`);
    } catch (err) {
      setLog(`❌ Error: ${err.message}`);
    }
  };

  const handleRecognize = async () => {
    setLog('Recognizing...');
    try {
      const res = await axios.post('http://localhost:5000/api/recognize');
      setLog('✅ Recognition completed.');
    } catch (err) {
      setLog(`❌ Error: ${err.message}`);
    }
  };

  const handleChat = async () => {
    if (!question) return alert("Enter a question");
    setLoading(true);
    try {
      const res = await axios.post('http://localhost:5000/api/chat', { question });
      setAnswer(res.data.answer);
    } catch (err) {
      setAnswer("❌ Error fetching response.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>🎯 Face Recognition Platform</h1>

      <div className="card">
        <h2>Register</h2>
        <input
          type="text"
          placeholder="Enter your name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <button onClick={handleRegister}>Register</button>
      </div>

      <div className="card">
        <h2>Recognize</h2>
        <button onClick={handleRecognize}>Recognize Face</button>
      </div>

      <div className="card">
        <h2>Chat with Logs</h2>
        <input
          type="text"
          placeholder="Ask about registrations..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button onClick={handleChat}>Ask</button>
        {loading ? <p className="loading">⏳ Thinking...</p> : answer && <p className="answer">💬 {answer}</p>}
      </div>

      {log && <p className="log">{log}</p>}
    </div>
  );
}
