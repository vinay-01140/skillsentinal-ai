import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

risk_path = os.path.join(
    BASE_DIR,
    "reports",
    "skill_risk_scores.csv"
)

df = pd.read_csv(risk_path)

# Sort by risk (high to low)
ranked = df.sort_values(by="risk_score", ascending=False)

print("\n🔥 Top Risky Skills:\n")

for i, row in ranked.head(5).iterrows():
    print(f"{row['skill']} → Risk: {row['risk_score']}% ({row['trend']})")
