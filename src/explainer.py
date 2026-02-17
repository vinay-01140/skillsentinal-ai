import pandas as pd
import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURRENT_YEAR = datetime.now().year

# Load risk
risk_path = os.path.join(BASE_DIR, "reports", "skill_risk_scores.csv")
risk_df = pd.read_csv(risk_path)

# Load metadata
meta_path = os.path.join(BASE_DIR, "data", "skill_metadata.json")
with open(meta_path, "r") as f:
    birth_year = json.load(f)

# Load experience
exp_path = os.path.join(BASE_DIR, "data", "user_experience.json")
with open(exp_path, "r") as f:
    exp_data = json.load(f)


def explain(skill, trend, risk):

    year = birth_year.get(skill, CURRENT_YEAR - 5)
    age = CURRENT_YEAR - year

    exp = exp_data.get(skill, 0)

    reasons = []

    if trend in ["Declining", "Volatile"]:
        reasons.append(f"demand is {trend.lower()}")

    if age > 15:
        reasons.append(f"technology is {age} years old")

    if exp < 2:
        reasons.append("limited hands-on experience")

    if not reasons:
        reasons.append("strong market demand and relevance")

    return " and ".join(reasons)


print("\n📘 Skill Risk Explanations:\n")

for _, row in risk_df.sort_values("risk_score", ascending=False).head(5).iterrows():

    skill = row["skill"]
    trend = row["trend"]
    risk = row["risk_score"]

    reason = explain(skill, trend, risk)

    print(f"{skill} ({risk}%) → {reason}")
