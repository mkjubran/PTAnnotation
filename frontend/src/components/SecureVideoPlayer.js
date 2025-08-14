import React, { useRef } from "react";

function SecureVideoPlayer({ exercise, video }) {
  const videoRef = useRef(null);

  const handlePlay = () => {
    videoRef.current.play();
  };

  const handlePause = () => {
    videoRef.current.pause();
  };

  return (
    <div>
      <video
        ref={videoRef}
        width="450"
        controls={false} // No default controls
        src={`/api/videos/${exercise}/${video}`}
        onContextMenu={(e) => e.preventDefault()} // Disable right click
      />

      <div style={{ marginTop: "10px" }}>
        <button onClick={handlePlay}>▶ Play</button>
        <button onClick={handlePause}>⏸ Pause</button>
      </div>
    </div>
  );
}

export default SecureVideoPlayer;

