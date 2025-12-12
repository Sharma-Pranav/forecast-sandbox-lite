"""
Regime-Conditioned Forecasting Analysis
======================================

Reproduces all decision-grade evidence used in the consulting slides:

1. Demand structure segmentation
2. Model performance by structure
3. Portfolio-level mean loss
4. Tail-risk (P90) analysis
5. SKU win-rate vs portfolio loss disconnect
6. Chronos2 positioning (descriptive, not causal)

Inputs (from sandbox):
- combined_metrics.csv
- best_by_sku.csv

No assumptions beyond the data.
"""

import pandas as pd
import numpy as np

# ---------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------

DATA_DIR = "metrics"  # adjust if needed

COMBINED_PATH = f"{DATA_DIR}/combined_metrics.csv"
BEST_BY_SKU_PATH = f"{DATA_DIR}/best_by_sku.csv"

SCORE_COL = "score"
BIAS_COL = "bias"
MODEL_COL = "model"
BEST_MODEL_COL = "best_model"
SKU_COL = "id"

# optional if present
STRUCTURE_COLS = ["cv_bin", "adi_bin", "regime"]

# ---------------------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------------------

combined = pd.read_csv(COMBINED_PATH)
best_by_sku = pd.read_csv(BEST_BY_SKU_PATH)

# sanity
assert SCORE_COL in combined.columns
assert MODEL_COL in combined.columns

print("\nLoaded data:")
print(f"  combined_metrics rows: {len(combined):,}")
print(f"  best_by_sku rows: {len(best_by_sku):,}")
print(best_by_sku.head())
print(best_by_sku.columns)
# ---------------------------------------------------------------------
# 1. PORTFOLIO-LEVEL PERFORMANCE
# ---------------------------------------------------------------------

portfolio_summary = (
    combined
    .groupby(MODEL_COL)
    .agg(
        mean_score=(SCORE_COL, "mean"),
        p90_score=(SCORE_COL, lambda x: np.percentile(x, 90)),
        mean_abs_bias=(BIAS_COL, lambda x: np.mean(np.abs(x))),
        std_score=(SCORE_COL, "std")
    )
    .sort_values("mean_score")
)

print("\n=== Portfolio-Level Performance ===")
print(portfolio_summary.round(2))

# ---------------------------------------------------------------------
# 2. WIN-RATE (BEST-MODEL SHARE)
# ---------------------------------------------------------------------

win_rate = (
    best_by_sku
    .groupby(BEST_MODEL_COL)
    .size()
    .rename("sku_wins")
    .to_frame()
)

win_rate["win_share"] = win_rate["sku_wins"] / win_rate["sku_wins"].sum()

print("\n=== SKU Win Share ===")
print(win_rate.sort_values("win_share", ascending=False).round(3))

# ---------------------------------------------------------------------
# 3. WIN-RATE vs PORTFOLIO LOSS RELATIONSHIP
# ---------------------------------------------------------------------

win_vs_loss = (
    portfolio_summary
    .merge(win_rate, left_index=True, right_index=True, how="left")
    .fillna(0)
)

correlation = win_vs_loss["win_share"].corr(win_vs_loss["mean_score"])

print("\n=== Win-Rate vs Mean Score ===")
print(win_vs_loss[["mean_score", "win_share"]].round(3))
print(f"\nCorrelation (win_share vs mean_score): {correlation:.3f}")

# ---------------------------------------------------------------------
# 4. STRUCTURE-CONDITIONAL PERFORMANCE
# ---------------------------------------------------------------------

structure_cols = [c for c in STRUCTURE_COLS if c in combined.columns]

if structure_cols:
    print("\n=== Structure-Conditional Analysis ===")
    for col in structure_cols:
        print(f"\n-- Performance by {col} --")
        table = (
            combined
            .groupby([col, MODEL_COL])[SCORE_COL]
            .mean()
            .unstack()
        )
        print(table.round(2))
else:
    print("\nNo explicit structure columns found (cv_bin / regime).")

# ---------------------------------------------------------------------
# 5. TAIL-RISK DOMINANCE
# ---------------------------------------------------------------------

tail_ratio = (
    portfolio_summary["p90_score"] /
    portfolio_summary["mean_score"]
).rename("p90_to_mean_ratio")

print("\n=== Tail-Risk Ratio (P90 / Mean) ===")
print(tail_ratio.sort_values())

# ---------------------------------------------------------------------
# 6. CHRONOS2 DESCRIPTIVE POSITIONING
# ---------------------------------------------------------------------

if "chronos2" in portfolio_summary.index:
    chronos_row = portfolio_summary.loc["chronos2"]
    chronos_win = win_rate.loc["chronos2"] if "chronos2" in win_rate.index else None

    print("\n=== Chronos2 Positioning ===")
    print(chronos_row.round(2))
    if chronos_win is not None:
        print("\nChronos2 win share:")
        print(chronos_win.round(3))
else:
    print("\nChronos2 not found in model list.")

# ---------------------------------------------------------------------
# 7. OPTIONAL: EXPORT TABLES FOR SLIDES
# ---------------------------------------------------------------------

portfolio_summary.round(3).to_csv(f"{DATA_DIR}/analysis_portfolio_summary.csv")
win_vs_loss.round(3).to_csv(f"{DATA_DIR}/analysis_win_vs_loss.csv")

print("\nAnalysis tables exported:")
print("  analysis_portfolio_summary.csv")
print("  analysis_win_vs_loss.csv")
