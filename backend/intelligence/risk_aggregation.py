import psycopg2
from collections import defaultdict

DB_CONFIG = {
    "dbname": "derien",
    "user": "postgres",
    "password": "HelloWorld101",
    "host": "localhost",
    "port": 5432
}

WEIGHTS = {
    "content": 0.4,
    "behaviour": 0.3,
    "network": 0.3
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def risk_level(score):
    if score >= 0.7:
        return "High"
    elif score >= 0.4:
        return "Medium"
    return "Low"

def aggregate(scores):
    combined = 1.0
    for score, weight in scores:
        combined *= (1 - weight * score)
    return round(1 - combined, 3)

def run_risk_aggregation():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT entity_id, content_score, behaviour_score, network_score
        FROM risk_scores
        WHERE entity_type = 'user';
    """)

    user_scores = defaultdict(lambda: {"content": 0, "behaviour": 0, "network": 0})

    for uid, c, b, n in cur.fetchall():
        if c is not None:
            user_scores[uid]["content"] = max(user_scores[uid]["content"], c)
        if b is not None:
            user_scores[uid]["behaviour"] = max(user_scores[uid]["behaviour"], b)
        if n is not None:
            user_scores[uid]["network"] = max(user_scores[uid]["network"], n)

    for uid, scores in user_scores.items():
        components = [
            (scores["content"], WEIGHTS["content"]),
            (scores["behaviour"], WEIGHTS["behaviour"]),
            (scores["network"], WEIGHTS["network"]),
        ]

        final_score = aggregate(components)
        level = risk_level(final_score)

        cur.execute(
            """
            INSERT INTO risk_scores (
                entity_type,
                entity_id,
                content_score,
                behaviour_score,
                network_score,
                total_score,
                risk_level
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """,
            (
                "user",
                uid,
                scores["content"],
                scores["behaviour"],
                scores["network"],
                final_score,
                level
            )
        )

    cur.execute("""
        SELECT post_id, content_score
        FROM posts
        WHERE content_score IS NOT NULL;
    """)

    for post_id, c in cur.fetchall():
        final_score = round(c, 3)
        level = risk_level(final_score)

        cur.execute(
            """
            INSERT INTO risk_scores (
                entity_type,
                entity_id,
                content_score,
                total_score,
                risk_level
            )
            VALUES (%s, %s, %s, %s, %s);
            """,
            (
                "post",
                post_id,
                c,
                final_score,
                level
            )
        )

    conn.commit()
    cur.close()
    conn.close()

    print("Risk aggregation completed.")

if __name__ == "__main__":
    run_risk_aggregation()
