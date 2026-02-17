import pandas as pd
import os

# --------------------------------------------------
# Resolve project root
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --------------------------------------------------
# Load aggregated skill demand data
# --------------------------------------------------
data_path = os.path.join(
    BASE_DIR,
    "data",
    "job_market",
    "skill_demand_by_month.csv"
)

df = pd.read_csv(data_path, index_col=0)

# Ensure numeric consistency
df = df.apply(pd.to_numeric, errors="coerce").fillna(0)

# --------------------------------------------------
# Validation checks
# --------------------------------------------------
report = {}

# 1. Skills with zero demand across all months
zero_demand_skills = df[df.sum(axis=1) == 0].index.tolist()
report["zero_demand_skills"] = zero_demand_skills

# 2. Sparse skills (appear in fewer than 3 months)
sparse_skills = df[df.astype(bool).sum(axis=1) < 3].index.tolist()
report["sparse_skills"] = sparse_skills

# 3. Date validation
try:
    df.columns = pd.to_datetime(df.columns)
    report["date_alignment"] = "Valid"
except Exception:
    report["date_alignment"] = "Invalid date format"

# 4. Sudden spike detection
spike_skills = []

for skill in df.index:
    series = df.loc[skill]

    if series.max() > 5 * series.mean() and series.mean() > 0:
        spike_skills.append(skill)

report["spike_skills"] = spike_skills

# --------------------------------------------------
# Create validation summary
# --------------------------------------------------
summary = {
    "total_skills": df.shape[0],
    "zero_demand_count": len(zero_demand_skills),
    "sparse_skill_count": len(sparse_skills),
    "spike_skill_count": len(spike_skills),
    "date_alignment": report["date_alignment"]
}

summary_df = pd.DataFrame([summary])

# --------------------------------------------------
# Save validation results
# --------------------------------------------------
output_dir = os.path.join(BASE_DIR, "reports")
os.makedirs(output_dir, exist_ok=True)

summary_path = os.path.join(output_dir, "data_validation_summary.csv")
summary_df.to_csv(summary_path, index=False)

print("✅ Data validation completed")
print("📄 Validation summary saved at:", summary_path)
