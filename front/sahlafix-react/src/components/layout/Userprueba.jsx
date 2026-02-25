// src/components/TestAuth.jsx
import { useState } from "react";
import { registerUser, loginUser } from "../../api/auth";

export default function TestAuth() {
  const [message, setMessage] = useState("");

  const handleRegister = async () => {
    try {
      const res = await registerUser({
        email: "test@example.com",
        password: "123456",
        role: "user",
      });
      console.log(res);
      setMessage("Registro exitoso: " + JSON.stringify(res));
    } catch (err) {
      console.error(err);
      setMessage("Error: " + err.message);
    }
  };

  const handleLogin = async () => {
    try {
      const res = await loginUser({
        email: "test@example.com",
        password: "123456",
      });
      console.log(res);
      setMessage("Login exitoso: " + JSON.stringify(res));
      // guardar token para siguientes pruebas
      localStorage.setItem("token", res.token);
    } catch (err) {
      console.error(err);
      setMessage("Error: " + err.message);
    }
  };

  return (
    <div>
      <button onClick={handleRegister}>Probar Registro</button>
      <button onClick={handleLogin}>Probar Login</button>
      <p>{message}</p>
    </div>
  );
}