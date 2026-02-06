function FeatureCard({
  title,
  value,
  subtitle,
  status = "info",
  onClick = null,
}) {
  const colorMap = {
    high: "#ff4d4f",
    medium: "#ffa940",
    low: "#52c41a",
    info: "#00c2ff",
  };

  return (
    <div
      onClick={onClick}
      style={{
        backgroundColor: "#161616",
        borderRadius: "10px",
        padding: "20px",
        minWidth: "220px",
        minHeight: "120px",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        cursor: onClick ? "pointer" : "default",
        transition:
          "transform 0.2s ease, box-shadow 0.2s ease",
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = "translateY(-4px)";
        e.currentTarget.style.boxShadow =
          "0 8px 24px rgba(0,0,0,0.4)";
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = "none";
        e.currentTarget.style.boxShadow = "none";
      }}
    >
      {/* Title */}
      <div
        style={{
          fontSize: "12px",
          color: "#b3b3b3",
          letterSpacing: "1px",
        }}
      >
        {title.toUpperCase()}
      </div>

      {/* Main Value */}
      <div
        style={{
          fontSize: "32px",
          fontWeight: "bold",
          color: colorMap[status] || "#ffffff",
        }}
      >
        {value}
      </div>

      {/* Subtitle */}
      <div
        style={{
          fontSize: "12px",
          color: "#888",
        }}
      >
        {subtitle}
      </div>
    </div>
  );
}

export default FeatureCard;
