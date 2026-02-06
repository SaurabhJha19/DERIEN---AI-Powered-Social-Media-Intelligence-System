import { useState } from "react";

function UserInvestigationView({ data, onClose }) {
  const [tab, setTab] = useState("overview");

  return (
    <div
      className="slide-up"
      style={{
        marginTop: "32px",
        backgroundColor: "#121212",
        borderRadius: "12px",
        border: "1px solid #222",
        padding: "24px",
      }}
    >
      {/* ===== HEADER ===== */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginBottom: "20px",
        }}
      >
        <div>
          <h3 style={{ marginBottom: "4px" }}>
            User Investigation — {data.user_id}
          </h3>
          <span
            style={{
              fontSize: "12px",
              color:
                data.risk_level === "High"
                  ? "#ff4d4f"
                  : data.risk_level === "Medium"
                  ? "#ffa940"
                  : "#52c41a",
            }}
          >
            {data.risk_level} Risk
          </span>
        </div>

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

      {/* ===== TABS ===== */}
      <TabBar active={tab} onChange={setTab} />

      {/* ===== CONTENT ===== */}
      <div style={{ marginTop: "20px" }}>
        {tab === "overview" && <OverviewTab data={data} />}
        {tab === "posts" && <PostsTab posts={data.posts} />}
        {tab === "network" && <NetworkTab score={data.network_score} />}
        {tab === "explain" && <ExplainTab data={data} />}
      </div>
    </div>
  );
}

/* =========================
   TAB BAR
========================= */

function TabBar({ active, onChange }) {
  const tabs = [
    { id: "overview", label: "Overview" },
    { id: "posts", label: "Posts" },
    { id: "network", label: "Network" },
    { id: "explain", label: "Explainability" },
  ];

  return (
    <div style={{ display: "flex", gap: "16px", fontSize: "13px" }}>
      {tabs.map((t) => (
        <div
          key={t.id}
          onClick={() => onChange(t.id)}
          style={{
            cursor: "pointer",
            paddingBottom: "6px",
            borderBottom:
              active === t.id ? "2px solid #00c2ff" : "none",
            color: active === t.id ? "#fff" : "#888",
          }}
        >
          {t.label}
        </div>
      ))}
    </div>
  );
}

/* =========================
   TABS
========================= */

function OverviewTab({ data }) {
  return (
    <div style={{ display: "flex", gap: "24px", flexWrap: "wrap" }}>
      <Stat label="Content Score" value={data.content_score} />
      <Stat label="Behaviour Score" value={data.behaviour_score} />
      <Stat label="Network Score" value={data.network_score} />
      <Stat label="Total Score" value={data.total_score} />
    </div>
  );
}

function PostsTab({ posts }) {
  return (
    <div style={{ fontSize: "13px" }}>
      {posts.length === 0
        ? "No associated posts"
        : posts.map((p) => <div key={p}>{p}</div>)}
    </div>
  );
}

function NetworkTab({ score }) {
  return (
    <div style={{ fontSize: "13px" }}>
      Network Influence Score: <strong>{score}</strong>
    </div>
  );
}

function ExplainTab({ data }) {
  return (
    <div style={{ fontSize: "13px", color: "#ccc" }}>
      This user is classified as{" "}
      <strong>{data.risk_level}</strong> risk based on:
      <ul>
        <li>Content patterns</li>
        <li>Behavioural anomalies</li>
        <li>Network associations</li>
      </ul>
    </div>
  );
}

function Stat({ label, value }) {
  return (
    <div>
      <div style={{ fontSize: "11px", color: "#888" }}>{label}</div>
      <div style={{ fontSize: "20px" }}>{value ?? "—"}</div>
    </div>
  );
}

export default UserInvestigationView;
