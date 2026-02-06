import psycopg2
from collections import defaultdict
from datetime import datetime

DB_CONFIG = {
    "dbname": "derien",
    "user": "postgres",
    "password": "HelloWorld101",
    "host": "localhost",
    "port": 5432
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def days_between(t1, t2):
    return abs((t1 - t2).days) + 1

def tokenize(text):
    return set(text.lower().split())

def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)

def run_behavioural_analysis():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT user_id, text, timestamp
        FROM posts
        ORDER BY user_id, timestamp;
    """)

    posts_by_user = defaultdict(list)

    for user_id, text, ts in cur.fetchall():
        posts_by_user[user_id].append((text, ts))

    for user_id, posts in posts_by_user.items():
        if len(posts) < 2:
            continue

        timestamps = [p[1] for p in posts]
        days = days_between(min(timestamps), max(timestamps))
        posts_per_day = len(posts) / days

        freq_score = 0.0
        freq_reason = None

        if posts_per_day >= 6:
            freq_score = 0.7
            freq_reason = "very_high_posting_frequency"
        elif posts_per_day >= 3:
            freq_score = 0.4
            freq_reason = "high_posting_frequency"

        similarity_hits = 0
        comparisons = 0

        tokenized = [tokenize(p[0]) for p in posts]

        for i in range(len(tokenized)):
            for j in range(i + 1, len(tokenized)):
                if jaccard(tokenized[i], tokenized[j]) > 0.7:
                    similarity_hits += 1
                comparisons += 1

        repetition_ratio = similarity_hits / comparisons if comparisons else 0

        rep_score = 0.0
        rep_reason = None

        if repetition_ratio > 0.6:
            rep_score = 0.6
            rep_reason = "high_content_repetition"

        behaviour_score = round(1 - ((1 - freq_score) * (1 - rep_score)), 3)

        if behaviour_score == 0:
            continue

        cur.execute(
            """
            INSERT INTO risk_scores (
                entity_type,
                entity_id,
                behaviour_score,
                total_score,
                risk_level
            )
            VALUES (%s, %s, %s, %s, %s);
            """,
            (
                "user",
                user_id,
                behaviour_score,
                behaviour_score,
                "Medium" if behaviour_score < 0.6 else "High"
            )
        )

    conn.commit()
    cur.close()
    conn.close()

    print("Behavioural analysis completed.")

if __name__ == "__main__":
    run_behavioural_analysis()
