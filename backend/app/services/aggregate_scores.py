from app.database import get_connection
from app.config.scoring import WEIGHTS


def aggregate_user_scores():
    conn = get_connection()
    cur = conn.cursor()

    # Fetch normalized scores
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
        # ---- handle missing signals ----
        signals = {
            "content": content,
            "behaviour": behaviour,
            "network": network,
        }

        available = {
            k: v for k, v in signals.items() if v is not None
        }

        if not available:
            total_score = 0.0
            confidence = 0.0
        else:
            # ---- weighted aggregation ----
            weighted_sum = 0.0
            weight_sum = 0.0

            for k, v in available.items():
                w = WEIGHTS[k]
                weighted_sum += v * w
                weight_sum += w

            # normalize by used weights
            total_score = weighted_sum / weight_sum

            # ---- confidence score ----
            confidence = len(available) / len(signals)

        cur.execute(
            """
            UPDATE risk_scores
            SET total_score = %s,
                confidence = %s
            WHERE entity_type = 'user'
              AND entity_id = %s;
            """,
            (
                round(total_score, 4),
                round(confidence, 2),
                user_id,
            ),
        )

    conn.commit()
    cur.close()
    conn.close()
