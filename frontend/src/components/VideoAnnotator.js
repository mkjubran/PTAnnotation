import React, { useEffect, useState } from "react";
import axios from 'axios';
import SecureVideoPlayer from "./SecureVideoPlayer";

function VideoAnnotator({ user }) {
  const [exercises, setExercises] = useState([]);
  const [exercise, setExercise] = useState("");
  const [videos, setVideos] = useState([]);
  const [video, setVideo] = useState("");
  const [labelNames, setLabelNames] = useState([]); // Q1–Q10 from DB
  const [labels, setLabels] = useState([]); // user-selected values

  useEffect(() => {
    axios.get("/api/annotations").then((res) => {
      // The keys are "E0", "E1", etc.
      setExercises(Object.keys(res.data));
    });
  }, []);

  useEffect(() => {
    if (exercise) {
      axios.get(`/api/videos/${exercise}`).then((res) => {
        setVideos(res.data);
        setVideo(res.data[0] || "");
      });
   }
  }, [exercise]);

  // Fetch label names from DB
  useEffect(() => {
    axios.get("/api/labels").then((res) => {
      setLabelNames(res.data);
      setLabels(new Array(res.data.length).fill(5)); // Default values
    });
  }, []);

  const handleLabelChange = (idx, val) => {
    const newLabels = [...labels];
    newLabels[idx] = Number(val);
    setLabels(newLabels);
  };

  const handleSubmit = () => {
    axios.post("http://pt-backend:5000/annotations", {
      exercise,
      video,
      user,
      labels
    }).then(() => alert("Annotation saved!"));
  };

  return (
    <div style={styles.container}>
      <div>
        <h3>Exercise:</h3>
        <select onChange={(e) => setExercise(e.target.value)} value={exercise}>
          <option value="">Select exercise</option>
          {exercises.map((ex) => (
            <option key={ex} value={ex}>{ex}</option>
          ))}
        </select>
        <h3>Video:</h3>
        <select onChange={(e) => setVideo(e.target.value)} value={video}>
          {videos.map((v) => (
            <option key={v} value={v}>{v}</option>
          ))}
        </select>

<h3>Labels:</h3>
{labelNames.map((label, idx) => (
  <div key={idx}>
        <p>{label.name}: {label.question}</p>
    <input
      type="range"
      min="0"
      max="10"
      value={labels[idx] || 0}
      onChange={(e) => handleLabelChange(idx, e.target.value)}
    /> {labels[idx] || 0}
  </div>
))}
        <button onClick={handleSubmit}>Save Annotation</button>
      </div>
      <div style={{ marginLeft: "2rem" }}>
  {/* Old video player commented out
        {video && exercise && (
          <video
            key={video}
            width="600"
            controls
            src={`/api/videos/${exercise}/${video}`}
            onContextMenu={(e) => e.preventDefault()}
          />
  */}
          {video && exercise && (
            <SecureVideoPlayer exercise={exercise} video={video} />
          )}

      </div>
    </div>
  );
}

const styles = {
  container: {
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "#e8efff"
  },
  form: {
    background: "#fff",
    padding: "2rem",
    borderRadius: "10px",
    boxShadow: "0 4px 20px rgba(0,0,0,0.1)",
    width: "300px",
    display: "flex",
    flexDirection: "column",
  },
  title: {
    textAlign: "center",
    marginBottom: "1.5rem",
    color: "#1f2937",
  },
  label: {
    marginBottom: "0.25rem",
    color: "#1f2937",
    fontWeight: "500",
  },
  input: {
    marginBottom: "1rem",
    padding: "0.5rem",
    borderRadius: "5px",
    border: "1px solid #d1d5db",
    fontSize: "1rem",
  },
  button: {
    background: "#3b82f6",
    color: "#fff",
    padding: "0.75rem",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
    fontSize: "1rem",
  },
};


export default VideoAnnotator;

