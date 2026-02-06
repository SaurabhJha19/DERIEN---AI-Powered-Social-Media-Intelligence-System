import psycopg2
import networkx as nx
from collections import defaultdict

DB_CONFIG = {
    "dbname": "derien",
    "user": "postgres",
    "password": "HelloWorld101",
    "host": "localhost",
    "port": 5432
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def build_graph(cur):
    G = nx.Graph()

    cur.execute("SELECT user_id FROM users;")
    for (user_id,) in cur.fetchall():
        G.add_node(user_id)

    cur.execute("""
        SELECT source_user, target_user
        FROM interactions;
    """)
    for src, tgt in cur.fetchall():
        if src and tgt:
            G.add_edge(src, tgt, type="interaction")

    cur.execute("""
        SELECT p1.user_id, p2.user_id
        FROM post_hashtags h1
        JOIN post_hashtags h2
          ON h1.hashtag = h2.hashtag
         AND h1.post_id <> h2.post_id
        JOIN posts p1 ON h1.post_id = p1.post_id
        JOIN posts p2 ON h2.post_id = p2.post_id;
    """)
    for u1, u2 in cur.fetchall():
        if u1 != u2:
            G.add_edge(u1, u2, type="hashtag")

    return G

def run_network_analysis():
    conn = get_connection()
    cur = conn.cursor()

    print("Building network graph...")
    G = build_graph(cur)

    if G.number_of_edges() == 0:
        print("No edges found. Network analysis skipped.")
        return

    degree_centrality = nx.degree_centrality(G)

    clusters = list(nx.connected_components(G))
    cluster_map = {}
    for idx, cluster in enumerate(clusters):
        for node in cluster:
            cluster_map[node] = idx

    cur.execute("""
        SELECT entity_id, behaviour_score
        FROM risk_scores
        WHERE entity_type = 'user';
    """)
    behaviour_risk = {u: s for u, s in cur.fetchall()}

    for user in G.nodes():
        deg = degree_centrality.get(user, 0)
        cluster_size = len(clusters[cluster_map[user]])

        hub_score = 0.6 if deg > 0.05 else 0.0
        cluster_score = 0.5 if cluster_size > 5 else 0.0

        burner_score = 0.0
        if deg < 0.02 and behaviour_risk.get(user, 0) > 0.4:
            burner_score = 0.4

        network_score = round(
            1 - ((1 - hub_score) * (1 - cluster_score) * (1 - burner_score)),
            3
        )

        if network_score == 0:
            continue

        risk_level = "Medium" if network_score < 0.6 else "High"

        cur.execute(
            """
            INSERT INTO risk_scores (
                entity_type,
                entity_id,
                network_score,
                total_score,
                risk_level
            )
            VALUES (%s, %s, %s, %s, %s);
            """,
            (
                "user",
                user,
                network_score,
                network_score,
                risk_level
            )
        )

    conn.commit()
    cur.close()
    conn.close()

    print("Network analysis completed.")

if __name__ == "__main__":
    run_network_analysis()
