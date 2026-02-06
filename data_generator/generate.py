# data_generator/generate.py
import json
import os

from users import generate_users
from posts import generate_posts
from interactions import generate_interactions
from lexicon import DRUG_SLANG, DRUG_EMOJIS

OUTPUT_DIR = "output"

def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def save(filename, data):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def main():
    ensure_output_dir()

    users = generate_users()
    posts = generate_posts(users)
    interactions = generate_interactions(users)

    save("users.json", users)
    save("posts.json", posts)
    save("interactions.json", interactions)
    save("lexicon.json", {
        "slang": DRUG_SLANG,
        "emojis": DRUG_EMOJIS
    })

    print(f"Synthetic dataset generated in ./{OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
