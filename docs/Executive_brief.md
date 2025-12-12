
---

# **Executive Brief — Stabilizing Forecast Signals in Fresh Retail Environments**

---

## **Why This Matters in Fresh Retail**

Fresh categories behave differently from ambient grocery.
The FreshNet dataset reflects what operators experience daily:

* high volatility in unit demand
* frequent zero-sales days
* sharp lifts driven by promotions or weather
* stockouts that distort the forecast signal

When the forecast shifts abruptly week to week, teams must repeatedly reset:

* replenishment quantities
* production planning
* store-level ordering
* waste and markdown expectations

This rework slows execution and lowers confidence across planning teams.

This analysis was designed to answer a practical question:

> **Which forecasting approaches produce a stable, low-noise forward signal suitable for fresh operations?**

---

## **What the Evaluation Showed (FreshNet Context)**

FreshNet SKUs revealed **structure-dependent differences** in forecasting stability.
Some models consistently dampened noise within specific demand behaviors; others amplified it when misapplied.

---

## **Portfolio-Level Forecast Stability**

![Portfolio-Level Model Ranking](./model_score_ranking_exec.png)

**Figure:** Forecast model stability comparison (lower score = more stable, lower operational risk).

This plot shows:

* **Blue models** → consistently stable signal across many SKUs
* **Gray models** → acceptable for some SKUs, not ideal for volatile items
* **Red models** → produce unstable week-to-week swings, creating rework

*Observed stability varies by demand structure; no single model dominates all SKU behaviors.*

The stability threshold highlights where noise becomes operationally disruptive.

---

## **Key Insights From the FreshNet Evaluation**

### **1. A small group of models produced the most stable, low-bias signal**

These methods consistently absorbed volatility without overreacting **when applied in the appropriate demand context**:

* **Theta-family smoothing**
* **SES / Holt / Holt-Winters (exponential smoothing)**
* **Chronos2** for mixed or uncertain demand patterns
* **Croston variants** for intermittent and zero-heavy SKUs

These models form the **recommended baseline for fresh forecasting when applied in a structure-aware manner**.

---

### **2. Ambient-category heuristic models do not work for fresh**

Models like:

* naive carry-forward
* simple averages
* drift-based projections

created **false volatility** and **unstable directional signals**, which forced planners to repeatedly correct the forecast.

These methods should be avoided for fresh categories.

---

### **3. Machine learning requires real drivers to perform**

FreshNet data shows that ML methods such as LightGBM only outperform when provided with:

* discount depth
* stockout hours
* weather variables
* availability ratios

Without these drivers, ML becomes unstable — validating the need for **model-to-demand matching**, not model complexity.

---

## **Recommended Forecast Baseline for FreshNet**

> **Use smoothing-based models (Theta/SES/Holt) as the default signal for FreshNet SKUs.
> Use Croston-type methods for intermittent items.
> Use Chronos2 when SKUs show mixed or uncertain structure involving variability, trend, or soft seasonality.**

This approach:

* minimizes week-to-week swings
* reduces bias
* improves interpretability
* provides planners with a reliable directional signal

Exactly what fresh operations require.

> *Where operational simplicity requires a single global model, Chronos2 provides the most robust default across mixed and uncertain demand structures.*

---

## **Operational Impact for Fresh Retail**

A more stable forecast directly improves:

### **Order Stability**

Store and central planning remain aligned with fewer urgent corrections.

### **Waste Reduction**

Stable baselines prevent over-ordering during temporary spikes.

### **Production & Labor Planning**

Teams commit earlier and avoid recalculating workflows.

### **Exception Visibility**

True demand shifts stand out clearly because baseline noise is lower.

---

## **Leadership Takeaway**

**Stable forecasts create stable fresh-retail operations.
When forecasting models are selected with awareness of demand structure, the resulting signal supports stronger ordering discipline, lower waste, and more confident execution.**

---
