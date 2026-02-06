import random
from datetime import datetime, timedelta
from archetypes import ARCHETYPES

def generate_users(n=200, seed=42):
    random.seed(seed)
    users = []

    archetype_keys = list(ARCHETYPES.keys())

    for i in range(n):
        archetype = random.choice(archetype_keys)
        profile = ARCHETYPES[archetype]

        age_days = profile.get("account_age_days", (60, 365))
        created_at = datetime.utcnow() - timedelta(days=random.randint(*age_days))

        users.append({
            "user_id": f"u_{1000+i}",
            "username": f"{archetype}_user_{i}",
            "bio": "Organic lifestyle" if archetype == "normal" else "DM for discreet delivery",
            "archetype": archetype,
            "followers_count": random.randint(20, 500),
            "following_count": random.randint(20, 400),
            "created_at": created_at.isoformat()
        })

    return users
