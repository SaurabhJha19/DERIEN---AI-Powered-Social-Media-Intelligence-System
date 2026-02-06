const BASE_URL = "http://127.0.0.1:8000";

export async function checkHealth() {
  const res = await fetch(`${BASE_URL}/health`);
  if (!res.ok) throw new Error("Backend not healthy");
  return res.json();
}

export async function fetchHighRiskUsers() {
  const res = await fetch(`${BASE_URL}/users/high-risk`);
  if (!res.ok) throw new Error("Failed to fetch users");
  return res.json();
}

export async function fetchHighRiskPosts() {
  const res = await fetch(`${BASE_URL}/posts/high-risk`);
  if (!res.ok) throw new Error("Failed to fetch posts");
  return res.json();
}

export async function fetchPostExplain(postId) {
  const res = await fetch(
    `${BASE_URL}/posts/${postId}/explain`
  );
  if (!res.ok) throw new Error("Failed to fetch explainability");
  return res.json();
}

export async function fetchNetworkGraph() {
  const res = await fetch(
    "http://127.0.0.1:8000/network/graph"
  );
  if (!res.ok) throw new Error("Network fetch failed");
  return res.json();
}

export async function fetchUserDetail(userId) {
  const res = await fetch(
    `http://127.0.0.1:8000/users/${userId}/detail`
  );
  if (!res.ok) throw new Error("Failed to fetch user detail");
  return res.json();
}
