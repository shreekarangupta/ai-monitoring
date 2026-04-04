import React, { useState } from "react";
import axios from "axios";
import "./App.css";

const BASE_URL = process.env.REACT_APP_BACKEND_URL;
fetch(`${backendUrl}/api/some-endpoint`, {
    method: 'POST',
    body: JSON.stringify(data)
})

function App() {
  const [cameraUrls, setCameraUrls] = useState([""]);
  const [cameraIds, setCameraIds] = useState([]);
  const [email, setEmail] = useState("");
  const [zoom, setZoom] = useState(1);
  const [loading, setLoading] = useState(false);

  const addCameraField = () => {
    setCameraUrls([...cameraUrls, ""]);
  };

  const handleChange = (index, value) => {
    const updated = [...cameraUrls];
    updated[index] = value;
    setCameraUrls(updated);
  };

  const submitCameras = async () => {
    setLoading(true);
    let ids = [];

    for (let url of cameraUrls) {
      if (!url) continue;
      const res = await axios.post(`${BASE_URL}/add_camera`, { url });
      ids.push(res.data.camera_id);
    }

    setCameraIds(ids);
    await axios.get(`${BASE_URL}/start`);
    setLoading(false);
  };

  const submitEmail = async () => {
    await axios.post(`${BASE_URL}/set_email`, { email });
    alert("✅ Email Saved!");
  };

  const stopMonitoring = async () => {
    await axios.get(`${BASE_URL}/stop`);
  };

  return (
    <div className="app">
      <div className="sidebar">
        <h2>⚡ AI CCTV</h2>

        <div className="card">
          <h4>📧 Alert Email</h4>
          <input
            placeholder="Enter email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <button className="btn primary" onClick={submitEmail}>
            Save Email
          </button>
        </div>

        <div className="card">
          <h4>📷 Cameras</h4>
          {cameraUrls.map((url, i) => (
            <input
              key={i}
              placeholder="http://192.168.x.x:8080/video"
              value={url}
              onChange={(e) => handleChange(i, e.target.value)}
            />
          ))}

          <button className="btn" onClick={addCameraField}>
            ➕ Add Camera
          </button>

          <button className="btn primary" onClick={submitCameras}>
            {loading ? "Starting..." : "▶ Start"}
          </button>

          <button className="btn danger" onClick={stopMonitoring}>
            ⏹ Stop
          </button>
        </div>

        <div className="card">
          <h4>🔍 Zoom</h4>
          <div className="zoom-controls">
            <button onClick={() => setZoom(zoom + 0.2)}>+</button>
            <button onClick={() => setZoom(zoom - 0.2)}>-</button>
          </div>
        </div>
      </div>

      <div className="main">
        <h1>Live Monitoring</h1>

        <div className="grid">
          {cameraIds.map((id) => (
            <div key={id} className="video-card">
              <div className="video-header">
                <span>Camera {id}</span>
                <span className="status">LIVE</span>
              </div>

              <img
                src={`${BASE_URL}/video/${id}`}
                alt="feed"
                style={{ transform: `scale(${zoom})` }}
              />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
