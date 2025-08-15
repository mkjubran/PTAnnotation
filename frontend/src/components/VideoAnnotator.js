// frontend/src/components/VideoAnnotator.js
import '../App.css';
import React, { useEffect, useState } from "react";
import axios from 'axios';
import SecureVideoPlayer from "./SecureVideoPlayer";

function VideoAnnotator({ username }) {
  const [exercises, setExercises] = useState([]);
  const [exercise, setExercise] = useState("");
  const [videos, setVideos] = useState([]);
  const [video, setVideo] = useState("");
  const [labelNames, setLabelNames] = useState([]); // [{name:'Q1', question:'...'}]
  const [labels, setLabels] = useState([]); // numeric values
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    axios.get("/api/annotations").then((res) => {
      setExercises(Object.keys(res.data));
    });
  }, []);

  useEffect(() => {
    if (exercise) {
      axios.get(`/api/videos/${exercise}`).then((res) => {
        setVideos(res.data);
        setVideo(res.data[0] || "");
      });
    } else {
      setVideos([]);
      setVideo("");
    }
  }, [exercise]);

  useEffect(() => {
    axios.get("/api/labels").then((res) => {
      setLabelNames(res.data);
      setLabels(new Array(res.data.length).fill(5));
    });
  }, []);

  const handleLabelChange = (idx, val) => {
    const next = [...labels];
    next[idx] = Number(val);
    setLabels(next);
  };

  const handleSubmit = async () => {
    if (!exercise || !video) {
      alert("Please choose an exercise and a video first.");
      return;
    }

    const answers = labelNames.map((ln, i) => ({
      question_name: ln.name,
      label_value: labels[i] ?? 0
    }));

    try {
      setSaving(true);
      await axios.post("/api/label_events", {
        username, // send logged-in username
        exercise,
        video,
        answers
      }, { withCredentials: true });
      alert("Annotation saved!");
    } catch (e) {
      alert("Failed to save (are you logged in?)");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div style={styles.container}>
      {/* Left column */}
      <div className="form-container">
        <h3>Exercise:</h3>
        <select onChange={(e) => setExercise(e.target.value)} value={exercise}>
          <option value="">Select exercise</option>
          {exercises.map((ex) => (
            <option key={ex} value={ex}>{ex}</option>
          ))}
        </select>

        <h3>Video:</h3>
        <select onChange={(e) => setVideo(e.target.value)} value={video} disabled={!exercise}>
          {videos.map((v) => (
            <option key={v} value={v}>{v}</option>
          ))}
        </select>
      </div>

      {/* Middle column */}
      <div className="video-pane">
        {video && exercise && (
          <SecureVideoPlayer exercise={exercise} video={video} />
        )}
      </div>

      {/* Right column */}
      <div style={{ overflowY: "auto" , padding: "0 10px" }}>
        <h3>Labels:</h3>
        <p>
          Taking into account the description and aim of the exercise and observing the
          whole exercise (all repetitions), please answer the questions choosing one of the
          following options:
          <br />
          1 = Never &nbsp; 2 = Rarely &nbsp; 3 = Sometimes &nbsp; 4 = Often &nbsp; 5 = Always
        </p>

        {labelNames.map((label, idx) => (
          <div key={idx} style={{ marginTop: "1.3rem", marginBottom: "0.1rem" }}>
            <p className="question-text">
              {label.name}: {label.question}
            </p>
            <div style={{ display:"flex", alignItems:"center", gap:"8px" }}>
              <input
                type="range"
                min="0"
                max="5"
                value={labels[idx] || 0}
                onChange={(e) => handleLabelChange(idx, e.target.value)}
                style={{ width: "80%" }}
              />
              <span style={{minWidth:24, textAlign:"center"}}>{labels[idx] || 0}</span>
            </div>
          </div>
        ))}
        <button onClick={handleSubmit} disabled={saving}>
          {saving ? "Saving..." : "Save Annotation"}
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    height: "100vh",
    display: "grid",
    gridTemplateColumns: "20% 40% 40%",
    gap: "1rem",
    background: "#e8efff",
    padding: "1rem",
    fontSize: "1.05rem"
  }
};

export default VideoAnnotator;

