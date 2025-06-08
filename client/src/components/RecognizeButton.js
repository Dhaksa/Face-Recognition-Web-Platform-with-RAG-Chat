import axios from "axios";

export default function RecognizeButton() {
  const handleClick = async () => {
    await axios.post("http://localhost:5000/api/recognize");
    alert("Started face recognition.");
  };
  return <button onClick={handleClick}>Recognize Faces</button>;
}
