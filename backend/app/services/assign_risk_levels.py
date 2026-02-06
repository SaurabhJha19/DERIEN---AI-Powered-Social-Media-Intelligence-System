from app.database import get_connection


def assign_user_risk_levels():
    conn = get_connection()
    cur = conn.cursor()

    # Compute percentiles
    cur.execute("""
        SELECT entity_id,
               NTILE(20) OVER (ORDER BY total_score DESC) AS bucket
        FROM risk_scores
        WHERE entity_type = 'user'
          AND total_score IS NOT NULL;
    """)

    rows = cur.fetchall()

    for entity_id, bucket in rows:
        if bucket == 1:
            level = "High"
        elif 2 <= bucket <= 4:
            level = "Medium"
        else:
            level = "Low"

        cur.execute(
            """
            UPDATE risk_scores
            SET risk_level = %s
            WHERE entity_type = 'user'
              AND entity_id = %s;
            """,
            (level, entity_id),
        )

    conn.commit()
    cur.close()
    conn.close()
