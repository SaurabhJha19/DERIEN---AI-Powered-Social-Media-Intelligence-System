from app.database import get_connection
from app.utils.normalization import normalize
from app.utils.stats import fetch_stats


def normalize_user_scores():
    conn = get_connection()
    cur = conn.cursor()

    # ---- fetch stats ----
    content_mean, content_std = fetch_stats(cur, "content_score", "user")
    behaviour_mean, behaviour_std = fetch_stats(cur, "behaviour_score", "user")
    network_mean, network_std = fetch_stats(cur, "network_score", "user")

    # ---- fetch raw scores ----
    cur.execute("""
        SELECT entity_id,
               content_score,
               behaviour_score,
               network_score
        FROM risk_scores
        WHERE entity_type = 'user';
    """)

    rows = cur.fetchall()

    for user_id, content, behaviour, network in rows:
        norm_content = normalize(content, content_mean, content_std)
        norm_behaviour = normalize(behaviour, behaviour_mean, behaviour_std)
        norm_network = normalize(network, network_mean, network_std)

        cur.execute(
            """
            UPDATE risk_scores
            SET content_score = %s,
                behaviour_score = %s,
                network_score = %s
            WHERE entity_type = 'user'
              AND entity_id = %s;
            """,
            (
                norm_content,
                norm_behaviour,
                norm_network,
                user_id,
            ),
        )

    conn.commit()
    cur.close()
    conn.close()
