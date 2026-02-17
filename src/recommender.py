import json
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load risk scores
risk_path = os.path.join(BASE_DIR, "reports", "skill_risk_scores.csv")
risk_df = pd.read_csv(risk_path)

# Load recommendation map
rec_path = os.path.join(BASE_DIR, "data", "recommendations.json")

with open(rec_path, "r") as f:
    rec_map = json.load(f)

# Get top risky skills
risky = risk_df.sort_values(
    by="risk_score", ascending=False
).head(5)

print("\n🎯 Skill Upgrade Recommendations:\n")

for _, row in risky.iterrows():
    skill = row["skill"]
    risk = row["risk_score"]

    suggestions = rec_map.get(skill, ["Explore advanced courses"])

    print(f"{skill} ({risk}%) → Learn: {', '.join(suggestions)}")
