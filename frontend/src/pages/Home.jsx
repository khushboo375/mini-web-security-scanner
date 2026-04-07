import React, { useState } from "react";
import { scanWebsite } from "../services/api";

function Home() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleScan = async () => {
    if (!url) return alert("Please enter a URL to scan");

    setLoading(true);
    setResult(null);

    try {
      const data = await scanWebsite(url); // fetch backend JSON
      console.log("Scan result from backend:", data); // debug
      setResult(data);
    } catch (err) {
      console.error("Scan failed:", err);
      setResult({ error: "Scan failed. See console for details." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Web Security Scanner</h1>

      <input
        type="text"
        placeholder="Enter URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        style={{ padding: "10px", width: "300px" }}
      />

      <br /><br />

      <button onClick={handleScan} style={{ padding: "10px 20px" }}>
        Scan
      </button>

      <br /><br />

      {loading && <p>Scanning... Please wait.</p>}

      {result && !result.error && (
      <div>
        <h2>Scan Result</h2>

        <p>
          <strong>Risk Score:</strong> {result.data.risk_score}
        </p>

        <p>
          <strong>Overall Severity:</strong> {result.data.overall_severity}
        </p>

        {result.data.vulnerabilities.map((v, index) => (
          <div key={index} style={{ marginBottom: "10px", border: "1px solid #ccc", padding: "10px" }}>
            <p><strong>Type:</strong> {v.type}</p>
            <p><strong>Severity:</strong> {v.severity}</p>
            <p><strong>Description:</strong> {v.description}</p>
            {v.fix && <p><strong>Fix:</strong> {v.fix}</p>}
          </div>
        ))}
      </div>
    )}

      {result && result.error && (
        <p style={{ color: "red" }}>{result.error}</p>
      )}
    </div>
  );
}

export default Home;