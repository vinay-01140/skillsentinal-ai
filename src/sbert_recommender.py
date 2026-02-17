import os
import pandas as pd
import json
from sentence_transformers import SentenceTransformer, util

# ----------------------------
# Project Paths
# ----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

risk_path = os.path.join(BASE_DIR, "reports", "skill_risk_scores.csv")
skills_path = os.path.join(BASE_DIR, "data", "skills.json")

# ----------------------------
# Load Data
# ----------------------------
risk_df = pd.read_csv(risk_path)

with open(skills_path, "r") as f:
    skill_dict = json.load(f)

all_skills = list(skill_dict.keys())

# ----------------------------
# Load SBERT Model
# ----------------------------
print("Loading SBERT model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# ----------------------------
# Encode Skills
# ----------------------------
print("Encoding skills...")
skill_embeddings = model.encode(all_skills, convert_to_tensor=True)

# ----------------------------
# Get Top Risky Skills
# ----------------------------
risky = risk_df.sort_values(
    by="risk_score", ascending=False
).head(5)

print("\n🤖 AI-Based Skill Recommendations:\n")

# ----------------------------
# Recommend Using Similarity
# ----------------------------
for _, row in risky.iterrows():

    risky_skill = row["skill"]
    risk = row["risk_score"]

    query_embedding = model.encode(
        risky_skill, convert_to_tensor=True
    )

    scores = util.cos_sim(query_embedding, skill_embeddings)[0]

    top_matches = scores.argsort(descending=True)[1:4]

    recommendations = [
        all_skills[i] for i in top_matches
    ]

    print(
        f"{risky_skill} ({risk}%) → Learn: "
        + ", ".join(recommendations)
    )
