import { useEffect } from "react";
import io from "socket.io-client";

export default function SocketClient() {
  useEffect(() => {
    const socket = io("http://localhost:5000");
    socket.on("message", msg => {
      console.log("🧠 WebSocket:", msg);
    });
  }, []);
  return null;
}
