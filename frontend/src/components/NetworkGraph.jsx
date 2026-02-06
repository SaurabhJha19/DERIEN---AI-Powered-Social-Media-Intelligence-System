import { useEffect, useRef } from "react";
import { Network } from "vis-network/standalone";

function NetworkGraph({ data, onNodeClick }) {
  const containerRef = useRef(null);
  const networkRef = useRef(null);

  useEffect(() => {
    if (!data) return;

    const nodes = data.nodes.map((n) => ({
      id: n.id,
      label: n.id,
      value: Math.max(n.risk * 20, 5),
      color: {
        background:
          n.level === "High"
            ? "#ff4d4f"
            : n.level === "Medium"
            ? "#ffa940"
            : "#52c41a",
      },
    }));

    const edges = data.edges;

    const network = new Network(
      containerRef.current,
      { nodes, edges },
      {
        physics: {
          stabilization: false,
          barnesHut: { gravitationalConstant: -8000 },
        },
        nodes: {
          shape: "dot",
          font: { color: "#ffffff" },
        },
        edges: {
          color: "#555",
          smooth: true,
        },
        interaction: {
          hover: true,
        },
      }
    );

    networkRef.current = network;

    // ---- cluster highlighting ----
    network.on("click", (params) => {
      if (params.nodes.length === 0) {
        resetHighlight(network);
        return;
      }

      const nodeId = params.nodes[0];
      highlightCluster(network, nodeId);

      if (onNodeClick) {
        onNodeClick(nodeId);
      }
    });

    return () => network.destroy();
  }, [data, onNodeClick]);

  return (
    <div style={{ marginTop: "40px" }}>
      <Legend />

      <div
        ref={containerRef}
        style={{
          height: "500px",
          borderRadius: "10px",
          backgroundColor: "#0e0e0e",
          border: "1px solid #222",
        }}
      />
    </div>
  );
}

/* =========================
   CLUSTER LOGIC
========================= */

function highlightCluster(network, nodeId) {
  const allNodes = network.body.data.nodes.get();
  const allEdges = network.body.data.edges.get();

  const connectedNodes = new Set(
    network.getConnectedNodes(nodeId)
  );
  connectedNodes.add(nodeId);

  allNodes.forEach((node) => {
    const isActive = connectedNodes.has(node.id);
    network.body.data.nodes.update({
      id: node.id,
      color: {
        background: isActive
          ? node.color.background
          : "#2a2a2a",
      },
    });
  });

  allEdges.forEach((edge) => {
    const isActive =
      connectedNodes.has(edge.from) &&
      connectedNodes.has(edge.to);

    network.body.data.edges.update({
      id: edge.id,
      color: isActive ? "#888" : "#1a1a1a",
    });
  });
}

function resetHighlight(network) {
  const allNodes = network.body.data.nodes.get();
  const allEdges = network.body.data.edges.get();

  allNodes.forEach((node) => {
    network.body.data.nodes.update({
      id: node.id,
      color: node.color,
    });
  });

  allEdges.forEach((edge) => {
    network.body.data.edges.update({
      id: edge.id,
      color: "#555",
    });
  });
}

/* =========================
   LEGEND
========================= */

function Legend() {
  return (
    <div
      style={{
        display: "flex",
        gap: "16px",
        fontSize: "12px",
        color: "#ccc",
        marginBottom: "12px",
      }}
    >
      <LegendItem color="#ff4d4f" label="High Risk" />
      <LegendItem color="#ffa940" label="Medium Risk" />
      <LegendItem color="#52c41a" label="Low Risk" />
      <LegendItem color="#999" label="Node Size = Risk Score" />
    </div>
  );
}

function LegendItem({ color, label }) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
      <div
        style={{
          width: "10px",
          height: "10px",
          borderRadius: "50%",
          backgroundColor: color,
        }}
      />
      <span>{label}</span>
    </div>
  );
}

export default NetworkGraph;
