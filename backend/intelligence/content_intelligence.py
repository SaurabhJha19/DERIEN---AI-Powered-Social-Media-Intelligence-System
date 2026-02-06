import psycopg2
import re

DB_CONFIG = {
    "dbname": "derien",
    "user": "postgres",
    "password": "HelloWorld101",
    "host": "localhost",
    "port": 5432
}

CALL_TO_ACTION = ["dm", "message", "telegram", "snap", "contact"]

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def load_lexicon(cursor):
    cursor.execute("SELECT token, token_type, meaning, confidence FROM lexicon;")
    slang = []
    emojis = []

    for token, token_type, meaning, confidence in cursor.fetchall():
        if token_type == "slang":
            slang.append((token.lower(), confidence))
        elif token_type == "emoji":
            emojis.append((token, confidence))

    return slang, emojis

def normalize(text):
    return text.lower()

def analyze_post(text, slang, emojis):
    indicators = []

    clean_text = normalize(text)

    for token, weight in slang:
        if re.search(rf"\b{re.escape(token)}\b", clean_text):
            indicators.append(("slang", token, weight))

    for emoji, weight in emojis:
        if emoji in text:
            indicators.append(("emoji", emoji, weight))

    for cta in CALL_TO_ACTION:
        if re.search(rf"\b{cta}\b", clean_text):
            indicators.append(("call_to_action", cta, 0.6))

    return indicators


def calculate_score(indicators):
    score = 1.0
    for _, _, weight in indicators:
        score *= (1 - weight)
    return round(1 - score, 3)


def run_content_intelligence():
    conn = get_connection()
    cur = conn.cursor()

    slang, emojis = load_lexicon(cur)

    cur.execute("SELECT post_id, text FROM posts;")
    posts = cur.fetchall()

    for post_id, text in posts:
        indicators = analyze_post(text, slang, emojis)

        if not indicators:
            continue

        score = calculate_score(indicators)

        cur.execute(
            "UPDATE posts SET content_score = %s WHERE post_id = %s;",
            (score, post_id)
        )

        for indicator_type, value, weight in indicators:
            cur.execute(
                """
                INSERT INTO post_indicators (
                    post_id,
                    indicator_type,
                    indicator_value,
                    weight
                )
                VALUES (%s, %s, %s, %s);
                """,
                (post_id, indicator_type, value, weight)
            )

    conn.commit()
    cur.close()
    conn.close()

    print("Content Intelligence processing completed.")

if __name__ == "__main__":
    run_content_intelligence()
