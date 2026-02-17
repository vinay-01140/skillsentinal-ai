import pandas as pd
import json
import re


# Load files
jobs = pd.read_csv("data/job_market/linkedin_job_postings.csv")
skills_df = pd.read_csv("data/job_market/job_skills.csv")


# Clean skill dict
with open("data/skills.json") as f:
    skill_map = json.load(f)


def normalize(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9,\s]", " ", text)
    return text


# Parse dates
jobs["first_seen"] = pd.to_datetime(jobs["first_seen"], errors="coerce")
jobs = jobs.dropna(subset=["first_seen"])

jobs["month"] = jobs["first_seen"].dt.to_period("M").astype(str)


# Merge
df = jobs.merge(skills_df, on="job_link", how="inner")


records = []


for _, row in df.iterrows():

    text = normalize(row["job_skills"])

    for skill, aliases in skill_map.items():
        for a in aliases:
            if a in text:
                records.append({
                    "skill": skill,
                    "month": row["month"]
                })
                break


trend_df = pd.DataFrame(records)

# Aggregate
trend = (
    trend_df
    .groupby(["skill", "month"])
    .size()
    .unstack(fill_value=0)
    .reset_index()
)

# Save
trend.to_csv(
    "data/job_market/skill_demand_by_month_real.csv",
    index=False
)

print("✅ Real trend dataset created")
