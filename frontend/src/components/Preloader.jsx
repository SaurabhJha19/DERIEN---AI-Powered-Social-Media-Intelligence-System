import { useEffect, useState } from "react";
import { checkHealth } from "../services/api";

function Preloader({ onReady }) {
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState("checking"); // checking | success | error
  const [error, setError] = useState(null);

  useEffect(() => {
    let interval;
    let timeout;

    // Smooth loading animation (caps at 90%)
    interval = setInterval(() => {
      setProgress((prev) => (prev < 90 ? prev + 1 : prev));
    }, 30);

    // Failure timeout (5 seconds)
    timeout = setTimeout(() => {
      setStatus("error");
      setError("Backend not responding");
      clearInterval(interval);
    }, 5000);

    // Health check
    checkHealth()
      .then(() => {
        clearTimeout(timeout);
        clearInterval(interval);
        setProgress(100);
        setStatus("success");

        setTimeout(() => {
          onReady();
        }, 700);
      })
      .catch(() => {
        clearTimeout(timeout);
        clearInterval(interval);
        setStatus("error");
        setError("Unable to connect to backend");
      });

    return () => {
      clearInterval(interval);
      clearTimeout(timeout);
    };
  }, [onReady]);

  return (
    <div
      style={{
        height: "100vh",
        backgroundColor: "#0e0e0e",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        padding: "40px 0",
      }}
    >
      {/* Center Content */}
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        {/* Title */}
        <h1
          className="glow-text"
          style={{
            letterSpacing: "6px",
            marginBottom: "20px",
          }}
        >
          DERIEN PROJECT
        </h1>

        {/* Loading Bar */}
        <div
          style={{
            width: "300px",
            height: "6px",
            backgroundColor: "#222",
            borderRadius: "4px",
            overflow: "hidden",
          }}
        >
          <div
            style={{
              width: `${progress}%`,
              height: "100%",
              backgroundColor:
                status === "error" ? "#ff4d4f" : "#00c2ff",
              transition: "width 0.2s ease",
            }}
          />
        </div>
      </div>

      {/* Bottom Status */}
      <div
        style={{
          textAlign: "center",
          fontSize: "12px",
          color:
            status === "success"
              ? "#52c41a"
              : status === "error"
              ? "#ff4d4f"
              : "#b3b3b3",
        }}
      >
        {status === "checking" && "Checking backend connection…"}
        {status === "success" && "Backend connected"}
        {status === "error" && error}
      </div>
    </div>
  );
}

export default Preloader;
