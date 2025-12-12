
---

# **Forecast Sandbox — Technical Summary (FreshNet Edition)**

---

## **1. Purpose**

Forecasting difficulty in fresh retail is not driven only by demand uncertainty,
but by **instability in the forward signal**.

A model that swings direction week to week creates:

* recurring overrides
* repeated replanning cycles
* loss of alignment between planners, stores, and operations

The sandbox therefore answers one technical question:

> **Which forecasting approaches maintain directional stability across heterogeneous fresh-category demand behaviors?**

Evaluation is performed **per SKU**, not as a portfolio average, using a scoring function that explicitly penalizes drift and directional inconsistency.

---

## **2. Dataset Basis — FreshNet**

This evaluation uses the **FreshNet retail dataset**, which reflects the operational characteristics of fresh categories:

* highly volatile daily demand
* frequent zero-sales days
* stockout-induced distortions
* promotion and weather sensitivity
* abrupt shifts rather than smooth seasonal patterns

These dynamics make fresh forecasting fundamentally different from ambient categories.

A behavioral segmentation was created:

| Regime    | Description                             |
| --------- | --------------------------------------- |
| High-High | unstable frequency + unstable magnitude |
| Low-High  | regular timing + high variability       |
| Low-Low   | stable, low-variance items              |

The purpose of segmentation is **not accuracy benchmarking**, but **stability differentiation under heterogeneous demand behaviors**.

---

## **3. Execution Workflow**

The sandbox is fully orchestrated using:

```
python run_pipeline.py
```

This executes the following sequence:

```
prepare_data
prepare_data_lgbm
compute_baselines
lgbm_modeling
chronos_inference
combine_metrics
select_best_model
generate_first_insights
model_selection_audit
```

Outputs include:

* SKU-level model forecasts
* consolidated metric ledger
* per-regime evidence tables
* full audit log of model selection decisions

All results are **reproducible**, deterministic, and governed by transparent rules.

---

## **4. Scoring Function**

For each SKU and model:

```
score = MAE + |Bias|
```

Rationale:

* **MAE** penalizes magnitude error
* **Bias** penalizes directional misalignment

In fresh categories, bias is critical because:

* persistent positive bias inflates waste
* persistent negative bias triggers stockouts
* even moderate bias forces operational replanning

Two models with identical MAE may have **very different operational impact** if one produces drift and the other does not.

This scoring function explicitly enforces **directional stability**, rather than point accuracy alone.

---

## **5. Technical Findings (FreshNet)**

The portfolio-level ranking (lower = more stable) shows **structure-dependent differences** in model stability:

| Stability Tier                           | Model Families (representative, not universal)                                    |
| ---------------------------------------- | --------------------------------------------------------------------------------- |
| **Tier A — Stable Models**               | *DynamicOptimizedTheta, SES/Holt/Holt-Winters, Chronos2, Theta, Croston variants* |
| **Tier B — Acceptable Secondary Models** | *WindowAverage, HistoricAverage*                                                  |
| **Tier C — High-Noise Models (avoid)**   | *LightGBM (without drivers), Naive, Drift, RandomWalk*                            |

### Key outcomes

* **Smoothing-based models** produced the most stable forecasts **when aligned with appropriate demand regimes**.
* **Chronos2** performed consistently across SKUs exhibiting mixed or uncertain structure.
* **Croston variants** excelled in zero-heavy and intermittent demand profiles.
* **LightGBM**, without drivers such as discount, weather, and availability, became unstable in fresh environments.

These outcomes reflect **model–structure alignment**, not algorithmic superiority.

---

## **6. Technical Interpretation**

![Portfolio-Level Model Ranking](./model_score_ranking.png)

From the plot:

* **Tier-A models** (left cluster) generally maintain **lower bias** and **more consistent weekly direction**, conditional on demand structure.
* **Tier-B models** are usable but may oscillate under moderate volatility.
* **Tier-C models** amplify noise and introduce unnecessary churn.

### Why smoothing dominates in FreshNet

* fresh demand is inherently noisy; smoothing dampens false volatility
* Theta/SES capture level shifts without reacting to transient spikes
* Croston preserves stability in sparse and intermittent series
* Chronos2 adapts to mixed structure without aggressive overshooting
* ML methods require external drivers; without them, they overfit recent noise

In short:

> **Fresh demand rewards structure-aware stability, not raw complexity.**

---

## **7. Deployment Standard**

Based on FreshNet performance:

> **Adopt Theta/SES/Holt-Winters as the default forecasting signal for SKUs with stable or moderately volatile structure.**
> **Use Croston variants for intermittent SKUs.**
> **Use Chronos2 when demand structure is mixed, uncertain, or weakly seasonal.**

ML (LightGBM) becomes a **Phase-2 upgrade** once driver data is introduced:
discounts, stockout hours, weather, and availability ratios.

---

## **8. What This Resolves for Planning Teams**

A stable, structure-aligned forecast signal resolves several persistent operational issues:

### Before

* weekly overrides normalized
* churn in order recommendations
* ambiguous ownership of changes
* poor alignment between stores, DCs, and planners

### After

* overrides become exception-based
* decisions persist across cycles
* signal changes correlate with real conditions
* planners spend less time “fixing the number” and more time acting on it

This standard **stabilizes the execution posture** across the fresh network.

---

## **9. Defensibility Properties**

The system is technically defensible because:

* evaluation is performed **per SKU**, not at the portfolio mean
* stability scoring is **mathematically transparent**
* all steps are deterministic, auditable, and logged
* model selection follows **explicit, structure-aware rules**
* the plot provides **visual governance evidence**

This creates a **repeatable, explainable, non-heuristic** model-selection framework.

---

## **Closing Position**

Forecast Sandbox v1.0 is not a model shootout.

It is a **decision pipeline** engineered to identify forecasting methods that produce a **stable, low-noise signal when matched to demand structure**,
because stability—not marginal accuracy—determines operational reliability in fresh retail.

By anchoring on smoothing models (Theta/SES/Holt), augmenting with Croston for intermittency, and using Chronos2 when structure is uncertain,
the resulting forecast becomes not only accurate but **operationally trustworthy**.

**This stability is what reduces waste, improves store ordering, and increases execution confidence.**

---
