function HighRiskUsersTable({ data, onClose }) {
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
        <h3>High-Risk Accounts</h3>
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
            <th>User ID</th>
            <th>Risk Score</th>
            <th>Level</th>
          </tr>
        </thead>
        <tbody>
          {data.map((u) => (
            <tr
              key={u.user_id}
              className="table-row-hover"
            >
              <td>{u.user_id}</td>
              <td>{u.score}</td>
              <td
                style={{
                  color:
                    u.risk_level === "High"
                      ? "#ff4d4f"
                      : "#ffa940",
                }}
              >
                {u.risk_level}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default HighRiskUsersTable;
