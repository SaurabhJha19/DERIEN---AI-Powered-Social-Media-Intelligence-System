function UserDetailPanel({ data, onClose }) {
  return (
    <div
      className="slide-up"
      style={{
        marginTop: "24px",
        backgroundColor: "#141414",
        borderRadius: "10px",
        padding: "20px",
        border: "1px solid #222",
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginBottom: "16px",
        }}
      >
        <h4>User Detail — {data.user_id}</h4>
        <button
          onClick={onClose}
          style={{
            background: "none",
            border: "none",
            color: "#888",
            cursor: "pointer",
          }}
        >
          Close
        </button>
      </div>

      <div style={{ display: "flex", gap: "20px", flexWrap: "wrap" }}>
        <Stat label="Content Score" value={data.content_score} />
        <Stat label="Behaviour Score" value={data.behaviour_score} />
        <Stat label="Network Score" value={data.network_score} />
        <Stat label="Total Score" value={data.total_score} />
        <Stat label="Risk Level" value={data.risk_level} />
      </div>

      <div style={{ marginTop: "16px", fontSize: "13px" }}>
        <strong>Related Posts:</strong>{" "}
        {data.posts.length > 0 ? data.posts.join(", ") : "None"}
      </div>
    </div>
  );
}

function Stat({ label, value }) {
  return (
    <div>
      <div style={{ fontSize: "11px", color: "#888" }}>{label}</div>
      <div style={{ fontSize: "18px" }}>{value ?? "—"}</div>
    </div>
  );
}

export default UserDetailPanel;
