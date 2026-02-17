import pandas as pd
import matplotlib.pyplot as plt
import os

# --------------------------------------------------
# Resolve project root to ensure execution consistency
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --------------------------------------------------
# Load aggregated skill demand data (Day 6 output)
# --------------------------------------------------
input_path = os.path.join(
    BASE_DIR,
    "data",
    "job_market",
    "skill_demand_by_month_final.csv"
)

df = pd.read_csv(input_path)

df = df.groupby("skill").sum(numeric_only=True)

df = df.apply(pd.to_numeric, errors="coerce").fillna(0)


# --------------------------------------------------
# Trend analysis: raw + smoothed comparison
# --------------------------------------------------
results = []

for skill in df.index:
    demand_series = df.loc[skill]
    # Require sufficient history for trend inference
    if len(demand_series) < 2:
        continue

    raw_start = demand_series.iloc[0]
    raw_end = demand_series.iloc[-1]

    if pd.isna(raw_start) or raw_start <= 0:
        continue

    # Raw percentage-based trend (interpretable)
    raw_change = ((raw_end - raw_start) / raw_start) * 100

    if raw_change > 10:
        raw_trend = "Increasing"
    elif raw_change < -10:
        raw_trend = "Declining"
    else:
        raw_trend = "Stable"

    # Smoothed trend to reduce short-term volatility
    smoothed = demand_series.rolling(window=3).mean().dropna()

    if len(smoothed) < 2:
        continue

    direction = smoothed.iloc[-1] - smoothed.iloc[0]

    if direction > 0:
        smooth_trend = "Increasing"
    elif direction < 0:
        smooth_trend = "Declining"
    else:
        smooth_trend = "Stable"

    # Final decision with confidence signal
    if raw_trend == smooth_trend:
        final_trend = raw_trend
        confidence = "High"
    else:
        final_trend = "Volatile"
        confidence = "Low"

    results.append([
        skill,
        round(raw_change, 2),
        raw_trend,
        smooth_trend,
        final_trend,
        confidence
    ])

# --------------------------------------------------
# Consolidate trend intelligence
# --------------------------------------------------
trend_df = pd.DataFrame(
    results,
    columns=[
        "skill",
        "raw_demand_change_percent",
        "raw_trend",
        "smoothed_trend",
        "final_trend",
        "confidence"
    ]
)

# --------------------------------------------------
# Persist trend results for downstream usage
# --------------------------------------------------
trend_output_path = os.path.join(
    BASE_DIR,
    "data",
    "job_market",
    "skill_trend_comparison.csv"
)

trend_df.to_csv(trend_output_path, index=False)

print("✅ Trend analysis completed")
print("📄 Trend data saved at:", trend_output_path)

# --------------------------------------------------
# Visualization: demand trends for representative skills
# --------------------------------------------------

# Convert columns to datetime for proper spacing
df.columns = pd.to_datetime(df.columns)

# Select top-demand skills
skills_to_plot = (
    df.sum(axis=1)
    .sort_values(ascending=False)
    .head(2)
    .index
    .tolist()
)

plt.figure(figsize=(14, 6))

for skill in skills_to_plot:
    plt.plot(
        df.columns,
        df.loc[skill],
        marker="o",
        label=skill
    )

plt.title("Job Market Skill Demand Trends")
plt.xlabel("Time")
plt.ylabel("Job Posting Count")
plt.legend()
plt.xticks(df.columns[::3], rotation=45)
plt.grid(True)

# Save visualization
report_dir = os.path.join(BASE_DIR, "reports")
os.makedirs(report_dir, exist_ok=True)

plot_path = os.path.join(report_dir, "skill_demand_trends.png")

plt.tight_layout()
plt.savefig(plot_path)
plt.show()

print("📊 Visualization saved at:", plot_path)
