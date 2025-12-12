
---

# **Evidence Appendix — Why Smoothing Models and Chronos2 Form the Forecast Anchor in FreshNet**

---

## **A. Portfolio-Level Evidence**

All models were evaluated SKU-wise using the bias-aware scoring function:

```
Score = MAE + |Bias|
```

This penalizes models that appear accurate but drift directionally—
a critical failure mode in fresh categories where bias inflates waste or drives stockouts.

### **Observed portfolio stability patterns (↓ = more stable)**

**Tier A — Lower-Noise Forecast Models**

| Model Family                            | Mean Stability Score (↓ better) |
| --------------------------------------- | ------------------------------- |
| **DynamicOptimizedTheta**               | 66.89                           |
| **SimpleExponentialSmoothingOptimized** | 67.31                           |
| **Chronos2**                            | 67.65                           |
| **Theta**                               | 67.68                           |
| **DynamicTheta**                        | 67.69                           |
| **CrostonOptimized / CrostonClassic**   | 67.88–68.36                     |

**Tier B — Acceptable Secondary Models**

| Model         | Score |
| ------------- | ----- |
| WindowAverage | 68.59 |
| HoltWinters   | 71.40 |
| Holt          | 71.84 |

**Tier C — High-Noise / High-Drift Models**

| Model               | Score |
| ------------------- | ----- |
| SeasonalNaive       | 76.74 |
| **LightGBM**        | 83.91 |
| HistoricAverage     | 84.07 |
| Naive               | 88.83 |
| RandomWalkWithDrift | 92.74 |

### **Interpretation**

* Tier-A models produce **lower bias and reduced noise** at the portfolio level.
* ML (LightGBM), without drivers such as discount, weather, or stockout hours, becomes **unstable**, overreacting to recent noise.
* Naive and drift models exaggerate noise and create planning churn.

**Conclusion:**
FreshNet dynamics favor **noise-dampening methods over signal chasing**, particularly when demand structure is heterogeneous.

---

## **B. SKU-Level Model Decisions**

Winner share across all evaluated SKUs:

| Tier       | Model Families                                                     | Share     |
| ---------- | ------------------------------------------------------------------ | --------- |
| **Tier A** | **Theta-family**, **SES/Holt**, **Chronos2**, **Croston variants** | **~65%+** |
| Tier B     | WindowAverage, HistoricAverage                                     | ~20%      |
| **Tier C** | LightGBM, Naive, Drift                                             | ~15%      |

### **Interpretation**

* Winners did **not** cluster around ML models.
* The distribution is **skewed toward smoothing-based approaches**, particularly in volatile and intermittent SKUs.
* LightGBM wins primarily where behavior is quasi-linear **and** no external drivers are required.

These patterns reflect **model–structure alignment**, not algorithmic preference.

---

## **C. Behavioral Regime Analysis**

FreshNet SKUs were segmented into three behavioral regimes.
Below are **frequently observed stability winners** within each regime.

---

### **1) High-High Regime**

*(unstable timing + unstable magnitude)*

| Winning Families                                   |
| -------------------------------------------------- |
| **Theta-family models**                            |
| **SES/Holt smoothing**                             |
| **Chronos2**                                       |
| Croston variants (for sparse high-volatility SKUs) |

**Observed behavior**

* These models dampen volatility without flattening structure.
* They avoid overreacting after spikes.
* Chronos2 handles mixed signal patterns without strong oscillation.

LightGBM frequently overfit recent bursts, leading to poor forward stability.

---

### **2) Low-High Regime**

*(regular recurrence, unstable amplitude)*

| Winning Families |
| ---------------- |
| **Holt-Winters** |
| **Theta**        |
| **Chronos2**     |
| Croston variants |

**Observed behavior**

* Seasonal regularity supports Holt-Winters performance.
* Amplitude spikes are absorbed more effectively by smoothing models than ML.
* Chronos2 adapts without repeatedly resetting level after shocks.

---

### **3) Low-Low Regime**

*(stable, low-variance items)*

| Winning Families             |
| ---------------------------- |
| **SES/Holt/Theta**           |
| Historic Average (some SKUs) |
| Croston (intermittent)       |

**Observed behavior**

* Model choice has lower impact in this regime.
* Smoothing models converge to similar baselines.
* Chronos2 is neutral — neither dominant nor harmful.

---

## **D. Example SKU-Level Decisions (Traceable)**

| SKU Identifier    | Stable Winner             |
| ----------------- | ------------------------- |
| CID0_SID0_PID104… | **DynamicOptimizedTheta** |
| CID0_SID0_PID118… | **Chronos2**              |
| CID0_SID0_PID127… | **SES/Holt**              |
| CID0_SID0_PID319… | **CrostonSBA**            |
| CID0_SID0_PID229… | **Holt-Winters**          |

Purpose:

* guarantees reproducibility
* shows evidence of regime-matched decisions
* prevents subjective reinterpretation

---

# **What the Evidence Resolves**

---

## **Technically**

The evidence demonstrates that:

* Theta/SES models **reduce directional drift**, a critical failure mode.
* Chronos2 accommodates mixed structure without aggressive overreaction.
* Croston preserves stability for zero-heavy SKUs.
* LightGBM is unsuitable for fresh categories **without driver data**.

### Stability, when matched to structure, dominates complexity

---

## **Operationally**

A stable, structure-aligned anchor model reduces:

* excessive overrides
* store–planner misalignment
* week-to-week forecast resets
* spiraling exception handling

And enables:

* consistent ordering
* predictable labor and waste planning
* cleaner exception signals

---

## **Economically**

Structure-aligned stability reduces:

* re-forecasting cycles
* waste from positive bias
* stockouts from negative bias
* planning churn and meeting load

These are material cost centers in fresh operations.

---

# **Deployment Decision**

> **Use Theta-family smoothing and SES/Holt as the default signal where structure is stable.**
> **Use Croston methods for intermittent SKUs.**
> **Use Chronos2 when demand structure is mixed or uncertain.**
> **Introduce LightGBM only once driver data (discounts, stockout hours, weather) is integrated.**

Fallbacks are allowed **only** when:

1. a SKU is structurally deterministic (e.g., controlled replenishment)
2. the category is end-of-life
3. required signals are missing
4. governance mandates a deterministic forecast

All fallback choices must be recorded in the model selection ledger.

---

# **Closing Position**

This evidence shows **consistent, structure-conditional patterns**, not a single universally dominant model.

**Theta/SES, Croston, and Chronos2 remain operationally stable across FreshNet’s volatile, mixed-pattern, and intermittent regimes when applied appropriately.**

They produce forecasts that are not only accurate,
but **steady enough to support durable planning decisions**.

That is why they form the **anchor set for FreshNet forecasting**, under a regime-aware deployment standard.

---
