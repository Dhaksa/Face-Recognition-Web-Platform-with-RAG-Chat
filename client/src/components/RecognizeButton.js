import axios from "axios";

export default function RecognizeButton({ action }) {
  const handleClick = async () => {
    if (!["login", "logout"].includes(action)) {
      alert("Invalid action type.");
      return;
    }

    try {
      const res = await axios.post("http://localhost:5000/api/recognize", {
        action: action.toLowerCase(),
      });
      alert(`${action} process completed.`);
    } catch (error) {
      console.error("Recognition error:", error);
      alert("Error during face recognition.");
    }
  };

  return (
    <button onClick={handleClick}>
      {action === "login" ? "🔓 Login" : "🔒 Logout"}
    </button>
  );
}
