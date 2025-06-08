import React, { useState } from "react";
import axios from "axios";

const RegisterButton = () => {
  const [name, setName] = useState("");

  const handleRegister = async () => {
    if (!name) return alert("Please enter a name");
    await axios.post("http://localhost:5000/api/register", { name });
    alert(`✅ Registration for ${name} started`);
  };

  return (
    <div>
      <input
        placeholder="Enter name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <button onClick={handleRegister}>Register Face</button>
    </div>
  );
};

export default RegisterButton;
