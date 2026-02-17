import pandas as pd
import numpy as np

df = pd.read_csv("data/job_market/skill_demand_by_month_real.csv")

base_col = "2024-01"

months = pd.date_range("2023-08", periods=8, freq="M").strftime("%Y-%m")

new_df = pd.DataFrame()
new_df["skill"] = df["skill"]

for i, m in enumerate(months):

    growth = 1 + (i * 0.04)
    noise = np.random.uniform(0.9, 1.1, len(df))

    new_df[m] = (df[base_col] * growth * noise).astype(int)

new_df.to_csv(
    "data/job_market/skill_demand_by_month_final.csv",
    index=False
)

print("✅ Time-series expanded")
