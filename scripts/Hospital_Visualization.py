import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ---------- 1) Load CSVs (robust path) ----------
BASE = Path(__file__).resolve().parent.parent  # Patient-Safety-Project root
general_df = pd.read_csv(BASE / "data" / "cleaned_general_info.csv")
safety_df  = pd.read_csv(BASE / "data" / "cleaned_safety_scores.csv")

# Clean column headers
general_df.columns = general_df.columns.astype(str).str.strip()
safety_df.columns  = safety_df.columns.astype(str).str.strip()

# ---------- 2) Merge ----------
# If this line fails, change it to:
# merged_df = general_df.merge(safety_df, left_on="Facility ID", right_on="Facility_ID", how="inner")
merged_df = general_df.merge(safety_df, on="Facility ID", how="inner")
merged_df.columns = merged_df.columns.astype(str).str.strip()

# ---------- 3) Dynamically find needed columns ----------
state_col    = next(c for c in merged_df.columns if "state" in c.lower())
rating_col   = next(c for c in merged_df.columns if "rating" in c.lower())
measure_col  = next(c for c in merged_df.columns if ("measure" in c.lower() and "id" in c.lower()))
facility_col = next(c for c in merged_df.columns if ("facility" in c.lower() and "name" in c.lower()))
score_col    = next(c for c in merged_df.columns if c.strip().lower() == "score")

# ---------- 4) Normalize values + filter ----------
m = merged_df.copy()
m[state_col]   = m[state_col].astype(str).str.strip().str.upper()
m[rating_col]  = m[rating_col].astype(str).str.strip()
m[measure_col] = m[measure_col].astype(str).str.strip().str.upper()

TARGET_STATE   = "TX"
TARGET_MEASURE = "MORT_30_AMI"
TARGET_RATINGS = ["5", "5.0"]

viz_data = m[
    (m[state_col] == TARGET_STATE) &
    (m[rating_col].isin(TARGET_RATINGS)) &
    (m[measure_col] == TARGET_MEASURE)
].copy()

# ---------- 5) Score numeric + sort ----------
viz_data[score_col] = pd.to_numeric(viz_data[score_col], errors="coerce")
viz_data = viz_data.dropna(subset=[score_col]).sort_values(by=score_col, ascending=True)

if viz_data.empty:
    print("❌ No rows after filtering. Check these available values:")
    print("\nStates:\n", m[state_col].value_counts().head(15))
    print("\nRatings:\n", m[rating_col].value_counts().head(15))
    print("\nMeasures:\n", m[measure_col].value_counts().head(30))
    raise SystemExit

# Choose how many hospitals to plot
TOP_N = 20
top = viz_data.head(TOP_N).copy()

# ---------- 6) Find lowest & highest (within plotted data) ----------
min_row = top.loc[top[score_col].idxmin()]
max_row = top.loc[top[score_col].idxmax()]

# ---------- 7) Plot ----------
plt.figure(figsize=(12, 8))
ax = sns.barplot(x=score_col, y=facility_col, data=top, palette="coolwarm")

# Add extra space on right side so text never overlaps or gets cut off
xmax = top[score_col].max()
ax.set_xlim(0, xmax + 2)

# Add value labels to each bar (small offset)
for i, v in enumerate(top[score_col]):
    ax.text(v + 0.10, i, f"{v:.2f}", va="center", fontsize=9)

# Add "Lowest" and "Highest" annotations (bigger offset + new line with value)
min_idx = top.index.get_loc(min_row.name)
max_idx = top.index.get_loc(max_row.name)

ax.text(min_row[score_col] + 0.90, min_idx,
        f"✅ Lowest\n({min_row[score_col]:.2f})",
        va="center", fontsize=10, fontweight="bold")

ax.text(max_row[score_col] + 0.90, max_idx,
        f"⚠ Highest\n({max_row[score_col]:.2f})",
        va="center", fontsize=10, fontweight="bold")

plt.title("Top 5-Star Texas Hospitals\n30-Day Heart Attack Mortality Scores", fontsize=14, pad=12)
plt.xlabel("Mortality Score (Lower is Better)")
plt.ylabel("Facility Name")
plt.tight_layout()

out_file = BASE / "hospital_ranking_chart.png"
plt.savefig(out_file, dpi=300, bbox_inches="tight")
plt.show()

# ---------- 8) Print summary ----------
print(f"✅ Saved chart to: {out_file}")
print(f"Rows plotted: {len(top)} (out of {len(viz_data)} matching rows)")
print(f"Lowest score:  {min_row[facility_col]} -> {min_row[score_col]:.2f}")
print(f"Highest score: {max_row[facility_col]} -> {max_row[score_col]:.2f}")
