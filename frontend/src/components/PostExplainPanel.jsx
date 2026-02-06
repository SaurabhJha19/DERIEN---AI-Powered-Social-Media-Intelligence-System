function PostExplainPanel({ postId, indicators, onClose }) {
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
        <h4>Explainability — {postId}</h4>
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

      {indicators.length === 0 ? (
        <div style={{ color: "#888" }}>
          No indicators available.
        </div>
      ) : (
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
            fontSize: "14px",
          }}
        >
          <thead>
            <tr style={{ color: "#888", textAlign: "left" }}>
              <th>Indicator</th>
              <th>Value</th>
              <th>Weight</th>
            </tr>
          </thead>
          <tbody>
            {indicators.map((i, idx) => (
              <tr key={idx}>
                <td>{i.indicator_type}</td>
                <td>{i.indicator_value}</td>
                <td>{i.weight}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default PostExplainPanel;
