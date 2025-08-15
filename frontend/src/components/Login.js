import '../App.css';
import React, { useState } from "react";
import axios from "axios";

const Login = ({ onLoggedIn }) => {
  const [username, setUsername] = useState(""); // username field
  const [password, setPassword] = useState(""); // password field
  const [err, setErr] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErr("");
    if (!username || !password) {
      setErr("Please enter both username and password.");
      return;
    }

    try {
      // send username & password to your backend API
      await axios.post("/api/login", { username, password }, { withCredentials: true });
      onLoggedIn?.({ username });
    } catch (e) {
      setErr("Invalid username or password");
    }
  };

  return (
    <div style={styles.container}>
      <form style={styles.form} onSubmit={handleSubmit}>
        <h2 style={styles.title}>PT Video Annotation System</h2>
        {err && <div style={{ color: "#b91c1c", marginBottom: "0.5rem" }}>{err}</div>}

        <label style={styles.label}>Username</label>
        <input
          style={styles.input}
          type="text"
          placeholder="Enter your username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <label style={styles.label}>Password</label>
        <input
          style={styles.input}
          type="password"
          placeholder="Enter your password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button style={styles.button} type="submit">Login</button>
      </form>
    </div>
  );
};

const styles = {
  container: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    height: "100vh",
    backgroundColor: "#e8efff"
  },
  form: {
    backgroundColor: "#fff",
    padding: "2rem",
    borderRadius: "8px",
    boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
    width: "100%",
    maxWidth: "400px"
  },
  title: {
    marginBottom: "1rem",
    textAlign: "center"
  },
  label: {
    display: "block",
    marginBottom: "0.25rem",
    fontWeight: "bold"
  },
  input: {
    width: "100%",
    padding: "0.5rem",
    marginBottom: "1rem",
    borderRadius: "4px",
    border: "1px solid #ccc"
  },
  button: {
    width: "100%",
    padding: "0.75rem",
    backgroundColor: "#3b82f6",
    color: "white",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer"
  }
};

export default Login;

