import pandas as pd
import os
import json
from datetime import datetime

# --------------------------------------------------
# Project context
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURRENT_YEAR = datetime.now().year

# --------------------------------------------------
# Load frozen trend intelligence
# --------------------------------------------------
trend_path = os.path.join(
    BASE_DIR,
    "data",
    "job_market",
    "skill_trend_comparison.csv"
)
trend_df = pd.read_csv(trend_path)

# --------------------------------------------------
# Load skill metadata (emergence years)
# --------------------------------------------------
meta_path = os.path.join(
    BASE_DIR,
    "data",
    "skill_metadata.json"
)
with open(meta_path, "r") as f:
    skill_birth_year = json.load(f)

# --------------------------------------------------
# Load user experience (dynamic per resume)
# --------------------------------------------------
exp_path = os.path.join(
    BASE_DIR,
    "data",
    "user_experience.json"
)

if os.path.exists(exp_path):
    with open(exp_path, "r") as f:
        user_experience = json.load(f)
else:
    user_experience = {}

# --------------------------------------------------
# Risk component scoring
# --------------------------------------------------
def trend_risk(trend):
    return {
        "Increasing": 10,
        "Stable": 30,
        "Volatile": 60,
        "Declining": 80
    }.get(trend, 50)

def age_risk(skill):
    birth_year = skill_birth_year.get(skill, CURRENT_YEAR - 5)
    age = CURRENT_YEAR - birth_year

    if age < 5:
        return 10
    elif age < 10:
        return 30
    elif age < 20:
        return 50
    else:
        return 70

def experience_mitigation(skill):
    exp = user_experience.get(skill, 0)

    if exp >= 5:
        return 30
    elif exp >= 3:
        return 20
    elif exp >= 1:
        return 10
    else:
        return 0

# --------------------------------------------------
# Composite risk computation
# --------------------------------------------------
risk_results = []

for _, row in trend_df.iterrows():
    skill = row["skill"]
    trend = row["final_trend"]

    base_risk = (
    0.5 * trend_risk(trend) +
    0.3 * age_risk(skill)
)

    mitigation = 0.2 * experience_mitigation(skill)

    risk_score = base_risk - mitigation

    risk_score = round(min(max(risk_score, 0), 100), 2)
    risk_results.append([skill, trend, risk_score])

# --------------------------------------------------
# Persist risk intelligence
# --------------------------------------------------
risk_df = pd.DataFrame(
    risk_results,
    columns=["skill", "trend", "risk_score"]
)

output_dir = os.path.join(BASE_DIR, "reports")
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "skill_risk_scores.csv")
risk_df.to_csv(output_path, index=False)

print("✅ Skill risk scoring completed")
print("📄 Risk report saved at:", output_path)
