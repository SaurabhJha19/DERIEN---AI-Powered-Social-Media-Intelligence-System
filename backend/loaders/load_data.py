import json
import psycopg2
from pathlib import Path

DB_CONFIG = {
    "dbname": "derien",
    "user": "postgres",
    "password": "HelloWorld101",
    "host": "localhost",
    "port": 5432
}

DATA_DIR = Path("../../data_generator/output")

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def load_json(filename):
    path = DATA_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def insert_users(cursor, users):
    for u in users:
        cursor.execute(
            """
            INSERT INTO users (
                user_id,
                username,
                bio,
                archetype,
                followers_count,
                following_count,
                created_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_id) DO NOTHING;
            """,
            (
                u["user_id"],
                u["username"],
                u.get("bio"),
                u.get("archetype"),
                u.get("followers_count"),
                u.get("following_count"),
                u["created_at"]
            )
        )

def insert_posts(cursor, posts):
    for p in posts:
        cursor.execute(
            """
            INSERT INTO posts (
                post_id,
                user_id,
                text,
                timestamp,
                likes,
                comments
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (post_id) DO NOTHING;
            """,
            (
                p["post_id"],
                p["user_id"],
                p["text"],
                p["timestamp"],
                p.get("likes", 0),
                p.get("comments", 0)
            )
        )

def insert_interactions(cursor, interactions):
    for i in interactions:
        cursor.execute(
            """
            INSERT INTO interactions (
                interaction_id,
                source_user,
                target_user,
                type,
                timestamp
            )
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (interaction_id) DO NOTHING;
            """,
            (
                i["interaction_id"],
                i["source_user"],
                i["target_user"],
                i["type"],
                i["timestamp"]
            )
        )

def insert_lexicon(cursor, lexicon):
    entries = []

    for item in lexicon.get("slang", []):
        entries.append({
            "token": item["token"],
            "type": "slang",
            "meaning": item["meaning"],
            "confidence": item["confidence"]
        })

    for item in lexicon.get("emojis", []):
        entries.append({
            "token": item["token"],
            "type": "emoji",
            "meaning": item["meaning"],
            "confidence": item["confidence"]
        })

    for e in entries:
        cursor.execute(
            """
            INSERT INTO lexicon (
                token,
                token_type,
                meaning,
                confidence
            )
            VALUES (%s, %s, %s, %s);
            """,
            (
                e["token"],
                e["type"],
                e["meaning"],
                e["confidence"]
            )
        )

def main():
    print("Loading JSON files...")
    users = load_json("users.json")
    posts = load_json("posts.json")
    interactions = load_json("interactions.json")
    lexicon = load_json("lexicon.json")

    print("Connecting to PostgreSQL...")
    conn = get_connection()
    cur = conn.cursor()

    print("Inserting users...")
    insert_users(cur, users)

    print("Inserting posts...")
    insert_posts(cur, posts)

    print("Inserting interactions...")
    insert_interactions(cur, interactions)

    print("Inserting lexicon...")
    insert_lexicon(cur, lexicon)

    conn.commit()
    cur.close()
    conn.close()

    print("Data successfully loaded into PostgreSQL.")

if __name__ == "__main__":
    main()
