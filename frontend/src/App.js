import React, { useState } from "react";
import Login from "./components/Login";
import VideoAnnotator from "./components/VideoAnnotator";

function App() {
  const [user, setUser] = useState(null);

  return user ? (
    <VideoAnnotator user={user} />
  ) : (
    <Login onLogin={setUser} />
  );
}

export default App;

