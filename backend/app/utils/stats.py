def fetch_stats(cur, column: str, entity_type: str):
    """
    Returns (mean, std) for a given score column.
    """
    cur.execute(
        f"""
        SELECT
            AVG({column}) AS mean,
            STDDEV_POP({column}) AS std
        FROM risk_scores
        WHERE entity_type = %s
          AND {column} IS NOT NULL;
        """,
        (entity_type,)
    )

    row = cur.fetchone()
    mean = row[0] or 0.0
    std = row[1] or 0.0

    return mean, std
