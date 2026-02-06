import { useState } from "react";
import { fetchPostExplain } from "../services/api";
import PostExplainPanel from "./PostExplainPanel";

function HighRiskPostsTable({ data, onClose }) {
  const [selectedPost, setSelectedPost] = useState(null);
  const [indicators, setIndicators] = useState([]);

  const handleRowClick = async (postId) => {
    setSelectedPost(postId);
    try {
      const result = await fetchPostExplain(postId);
      setIndicators(result);
    } catch {
      setIndicators([]);
    }
  };

  return (
    <div
      className="slide-up"
      style={{
        marginTop: "40px",
        backgroundColor: "#111",
        borderRadius: "10px",
        padding: "20px",
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginBottom: "16px",
        }}
      >
        <h3>Suspicious Posts</h3>
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

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          fontSize: "14px",
        }}
      >
        <thead>
          <tr style={{ color: "#888", textAlign: "left" }}>
            <th>Post ID</th>
            <th>Risk Score</th>
            <th>Level</th>
          </tr>
        </thead>
        <tbody>
          {data.map((p) => (
            <tr
              key={p.post_id}
              className="table-row-hover"
              onClick={() => handleRowClick(p.post_id)}
              style={{
                cursor: "pointer",
                backgroundColor:
                  selectedPost === p.post_id
                    ? "#1a1a1a"
                    : "transparent",
              }}
            >
              <td>{p.post_id}</td>
              <td>{p.score}</td>
              <td
                style={{
                  color:
                    p.risk_level === "High"
                      ? "#ff4d4f"
                      : "#ffa940",
                }}
              >
                {p.risk_level}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {selectedPost && (
        <PostExplainPanel
          postId={selectedPost}
          indicators={indicators}
          onClose={() => {
            setSelectedPost(null);
            setIndicators([]);
          }}
        />
      )}
    </div>
  );
}

export default HighRiskPostsTable;
