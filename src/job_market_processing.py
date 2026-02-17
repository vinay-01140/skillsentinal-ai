import pandas as pd
import os

# ------------------ PROJECT ROOT ------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ------------------ LOAD LINKEDIN JOB POSTINGS ------------------
jobs = pd.read_csv(
    os.path.join(BASE_DIR, "data", "job_market", "linkedin_job_postings.csv")
)

# use correct existing columns
jobs = jobs[["job_link", "last_processed_time"]]

# standardize column names
jobs.rename(columns={
    "job_link": "job_id",
    "last_processed_time": "posted_date"
}, inplace=True)

# convert date and extract month
jobs["posted_date"] = pd.to_datetime(jobs["posted_date"], errors="coerce")
jobs["month"] = jobs["posted_date"].dt.to_period("M").astype(str)

# ------------------ LOAD JOB SKILLS ------------------
skills = pd.read_csv(
    os.path.join(BASE_DIR, "data", "job_market", "job_skills.csv")
)

# use correct existing columns
skills = skills[["job_link", "job_skills"]]

# standardize column names
skills.rename(columns={
    "job_link": "job_id",
    "job_skills": "skill"
}, inplace=True)

# ------------------ MERGE DATA ------------------
merged = pd.merge(skills, jobs, on="job_id")

# ------------------ CLEAN AND SPLIT SKILLS ------------------

# remove bullets and split multiple skills
merged["skill"] = (
    merged["skill"]
    .astype(str)
    .str.replace("*", "", regex=False)
    .str.split(",")
)

# explode so ONE skill per row
merged = merged.explode("skill")

# clean spaces
merged["skill"] = merged["skill"].str.strip()

# ------------------ SKILL DEMAND PER MONTH ------------------
skill_trend = (
    merged
    .groupby(["skill", "month"])
    .size()
    .reset_index(name="count")
)


# ------------------ PIVOT TABLE ------------------
final_table = (
    skill_trend
    .pivot(index="skill", columns="month", values="count")
    .fillna(0)
)

# ------------------ SAVE FINAL CSV ------------------
output_path = os.path.join(
    BASE_DIR,
    "data",
    "job_market",
    "skill_demand_by_month.csv"
)

final_table.to_csv(output_path)

print("✅ Skill demand file created successfully")
print("📄 Saved at:", output_path)
