import random
from datetime import datetime, timedelta

def generate_interactions(users, n=3000, seed=42):
    random.seed(seed)
    interactions = []

    for i in range(n):
        src = random.choice(users)["user_id"]
        tgt = random.choice(users)["user_id"]

        if src == tgt:
            continue

        interactions.append({
            "interaction_id": f"i_{i}",
            "source_user": src,
            "target_user": tgt,
            "type": random.choice(["comment", "mention", "like"]),
            "timestamp": (datetime.utcnow() - timedelta(days=random.randint(0, 10))).isoformat()
        })

    return interactions
