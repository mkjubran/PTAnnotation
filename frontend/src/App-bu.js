// frontend/src/App.js
import React, { useState } from "react";
import Login from "./components/Login";
import VideoAnnotator from "./components/VideoAnnotator";

function App() {
  const [user, setUser] = useState(null); // store logged-in user

  return (
    <div>
      {!user ? (
        // Show login form if not logged in
        <Login onLoggedIn={(u) => setUser(u)} />
      ) : (
        // Show annotation interface if logged in
        <div>
          <header style={{ padding: "1rem", background: "#3b82f6", color: "white" }}>
            <h2>Welcome, {user.username}!</h2>
            <button
              style={{ float: "right", padding: "0.5rem 1rem", cursor: "pointer" }}
              onClick={() => setUser(null)}
            >
              Logout
            </button>
          </header>
          <VideoAnnotator username={user.username} />
        </div>
      )}
    </div>
  );
}

export default App;

