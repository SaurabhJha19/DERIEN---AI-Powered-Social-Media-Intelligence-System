import { useEffect, useState } from "react";

import FeatureCard from "../components/FeatureCard";
import HighRiskUsersTable from "../components/HighRiskUsersTable";
import HighRiskPostsTable from "../components/HighRiskPostsTable";
import NetworkGraph from "../components/NetworkGraph";
import UserInvestigationView from "../components/UserInvestigationView";

import {
  fetchHighRiskUsers,
  fetchHighRiskPosts,
  fetchNetworkGraph,
  fetchUserDetail,
} from "../services/api";

function Landing() {
  const [userData, setUserData] = useState([]);
  const [postData, setPostData] = useState([]);
  const [graphData, setGraphData] = useState(null);

  const [view, setView] = useState(null); // users | posts | network
  const [mounted, setMounted] = useState(false);

  const [userDetail, setUserDetail] = useState(null);
      // eslint-disable-next-line react-hooks/exhaustive-deps

  useEffect(() => {
    let active = true;
    setMounted(true);

    fetchHighRiskUsers()
      .then((d) => active && setUserData(d))
      .catch(() => active && setUserData([]));

    fetchHighRiskPosts()
      .then((d) => active && setPostData(d))
      .catch(() => active && setPostData([]));

    fetchNetworkGraph()
      .then((d) => active && setGraphData(d))
      .catch(() => active && setGraphData(null));

    return () => {
      active = false;
    };
  }, []);

  const handleNodeClick = (userId) => {
    setUserDetail(null);
    fetchUserDetail(userId)
      .then(setUserDetail)
      .catch(() => setUserDetail(null));
  };

  return (
    <div style={{ padding: "40px", minHeight: "100vh" }}>
      {/* TITLE */}
      <div style={{ textAlign: "center", marginBottom: "40px" }}>
        <h1 style={{ letterSpacing: "4px" }}>DERIEN IS RUNNING</h1>
        <div style={{ fontSize: "13px", color: "#888" }}>
          OSINT-based Intelligence System
        </div>
      </div>

      {/* FEATURE CARDS */}
      <div
        className={mounted ? "fade-in" : ""}
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit, minmax(220px, 1fr))",
          gap: "20px",
        }}
      >
        <FeatureCard
          title="High-Risk Accounts"
          value={userData.length}
          subtitle="Accounts flagged as suspicious"
          status="high"
          onClick={() => setView("users")}
        />

        <FeatureCard
          title="Suspicious Posts"
          value={postData.length}
          subtitle="Posts with elevated risk"
          status="medium"
          onClick={() => setView("posts")}
        />

        <FeatureCard
          title="Network Intelligence"
          value="View"
          subtitle="Cluster & hub visualization"
          status="info"
          onClick={() => setView("network")}
        />

        <FeatureCard
          title="Explainable AI"
          value="Active"
          subtitle="Transparent risk indicators"
          status="info"
        />
      </div>

      {/* VIEWS */}
      {view === "users" && (
        <HighRiskUsersTable
          data={userData}
          onClose={() => setView(null)}
        />
      )}

      {view === "posts" && (
        <HighRiskPostsTable
          data={postData}
          onClose={() => setView(null)}
        />
      )}

      {view === "network" && graphData && (
        <NetworkGraph
          data={graphData}
          onNodeClick={handleNodeClick}
        />
      )}

      {/* USER INVESTIGATION */}
      {userDetail && (
        <UserInvestigationView
          data={userDetail}
          onClose={() => setUserDetail(null)}
        />
      )}
    </div>
  );
}

export default Landing;
