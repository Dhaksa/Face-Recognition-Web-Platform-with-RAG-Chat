import axios from "axios";
import { useState } from "react";

export default function ChatComponent() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const handleAsk = async () => {
    const res = await axios.post("http://localhost:5000/api/chat", { question });
    setAnswer(res.data.answer);
  };

  return (
    <div>
      <input value={question} onChange={e => setQuestion(e.target.value)} placeholder="Ask a question" />
      <button onClick={handleAsk}>Ask</button>
      <p>Bot: {answer}</p>
    </div>
  );
}
