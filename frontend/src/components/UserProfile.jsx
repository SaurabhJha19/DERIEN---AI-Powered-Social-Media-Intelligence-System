import { useEffect, useState } from "react";
import {
  fetchUserSummary,
  fetchUserRiskDrivers,
} from "../services/api";

function UserProfile({ userId, onClose }) {
  const [summary, setSummary] = useState(null);
  const [drivers, setDrivers] = useState([]);

  useEffect(() => {
    fetchUserSummary(userId).then(setSummary);
    fetchUserRiskDrivers(userId).then(setDrivers);
  }, [userId]);

  if (!summary) return null;

  const riskColor =
    summary.risk_level === "High"
      ? "#ff4d4f"
      : summary.risk_level === "Medium"
      ? "#ffa940"
      : "#52c41a";

  return (
    <div
      style={{
        marginTop: "24px",
        backgroundColor: "#141414",
        borderRadius: "10px",
        padding: "20px",
        border: "1px solid #222",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <h3>User Profile — {summary.user_id}</h3>
        <button
          onClick={onClose}
          style={{ background: "none", border: "none", color: "#888" }}
        >
          Close
        </button>
      </div>

      {/* Summary */}
      <div style={{ marginTop: "16px" }}>
        <div>
          <strong>Risk Level:</strong>{" "}
          <span style={{ color: riskColor }}>
            {summary.risk_level}
          </span>
        </div>
        <div>
          <strong>Risk Score:</strong> {summary.risk_score}
        </div>
        <div>
          <strong>Total Posts:</strong> {summary.total_posts}
        </div>
        <div>
          <strong>Suspicious Posts:</strong>{" "}
          {summary.suspicious_posts}
        </div>
        <div>
          <strong>Network Degree:</strong>{" "}
          {summary.network_degree}
        </div>
      </div>

      {/* Risk Drivers */}
      <div style={{ marginTop: "20px" }}>
        <h4>Risk Drivers</h4>
        {drivers.length === 0 ? (
          <div style={{ color: "#888" }}>
            No indicators available.
          </div>
        ) : (
          <ul>
            {drivers.map((d, i) => (
              <li key={i}>
                {d.indicator_type} — {d.indicator_value} (
                {d.weight})
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default UserProfile;
