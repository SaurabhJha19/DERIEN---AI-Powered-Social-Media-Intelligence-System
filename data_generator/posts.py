import random
from datetime import datetime, timedelta
from lexicon import DRUG_SLANG, DRUG_EMOJIS, CALL_TO_ACTION

SAFE_POSTS = [
    "Weekend vibes 🌞",
    "Enjoying the weather today",
    "Coffee and coding ☕"
]

RISK_TEMPLATES = [
    "DM for {slang} {emoji} | fast drop",
    "Quality {slang} available {emoji} message me",
    "{cta} for discreet {slang}"
]

def generate_posts(users, days=10, seed=42):
    random.seed(seed)
    posts = []
    post_id = 0

    for user in users:
        archetype = user["archetype"]
        bias = 0.8 if archetype in ["high_risk_trafficker", "burner"] else 0.2

        for day in range(days):
            posts_today = random.randint(1, 3)
            base_time = datetime.utcnow() - timedelta(days=day)

            for _ in range(posts_today):
                post_id += 1
                risky = random.random() < bias

                if risky:
                    slang = random.choice(DRUG_SLANG)["token"]
                    emoji = random.choice(DRUG_EMOJIS)["token"]
                    cta = random.choice(CALL_TO_ACTION)
                    text = random.choice(RISK_TEMPLATES).format(
                        slang=slang, emoji=emoji, cta=cta
                    )
                else:
                    text = random.choice(SAFE_POSTS)

                posts.append({
                    "post_id": f"p_{post_id}",
                    "user_id": user["user_id"],
                    "text": text,
                    "timestamp": (base_time + timedelta(minutes=random.randint(0, 1440))).isoformat(),
                    "likes": random.randint(0, 100),
                    "comments": random.randint(0, 20)
                })

    return posts
