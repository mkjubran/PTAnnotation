import '../App.css';
import React, { useRef, useEffect, useState } from "react";

function SecureVideoPlayer({ exercise, video }) {
  const videoRef = useRef(null);
  const [videoSrc, setVideoSrc] = useState("");

  // Only set the video source when both exercise and video are properly set
  // and when the video name matches the exercise pattern
  useEffect(() => {
    if (exercise && video && video.startsWith(exercise)) {
      setVideoSrc(`/api/videos/${exercise}/${video}`);
    } else {
      setVideoSrc(""); // Clear source if props don't match
    }
  }, [exercise, video]);

  const handlePlay = () => {
    if (videoRef.current && videoSrc) {
      videoRef.current.play();
    }
  };

  const handlePause = () => {
    if (videoRef.current) {
      videoRef.current.pause();
    }
  };

  return (
    <div>
      <video
        ref={videoRef}
        width="450"
        controls={false} // No default controls
        src={videoSrc}
        onContextMenu={(e) => e.preventDefault()} // Disable right click
      />
      {/* Add display: 'flex' and gap to the container div */}
      <div style={{ marginTop: "10px", display: "flex", gap: "10px" }}>
        <button onClick={handlePlay} disabled={!videoSrc}>▶ Play</button>
        <button onClick={handlePause}>⏸ Pause</button>
      </div>
    </div>
  );
}

export default SecureVideoPlayer;
