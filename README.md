
---

# **Forecast Sandbox Lite — FreshNet Edition**

A reproducible sandbox for evaluating forecasting models on **fresh-retail SKU demand**, using a **bias-aware stability metric** and selecting a **structure-aligned, deployable model per SKU**.

Built on the **FreshRetailNet-50K** dataset — a large-scale, multi-store fresh retail forecasting corpus.

---

## **Primary Narrative**

The executive-level conclusions of this repository are presented in:

* **Executive_brief.md**

Supporting materials:

* **Technical_brief.md** — methodology and execution details
* **Appendix.md** — full quantitative evidence

All figures and conclusions are reproducible from the analysis and metrics folders.

---

## **Dataset Reference — FreshRetailNet-50K (Hugging Face)**

This sandbox uses the public dataset:

**Dataset:** FreshRetailNet-50K
**Publisher:** Dingdong Inc.
**Hugging Face Link:**
[https://huggingface.co/datasets/Dingdong-Inc/FreshRetailNet-50K](https://huggingface.co/datasets/Dingdong-Inc/FreshRetailNet-50K)

**Key dataset properties:**

* 50,000+ fresh SKU time series
* full product hierarchy: city → store → category → SKU
* sales, stockout hours, discount, promotion, temperature, precipitation, humidity, wind
* highly intermittent and volatile patterns typical of fresh operations
* multiple behavioral structures (smooth, erratic, intermittent, lumpy)

### **How This Dataset Is Used in the Sandbox**

* A **stratified SKU subset** was sampled to preserve the **original ADI–CV² distribution**.
* Each sampled SKU retains its **full historical trajectory**.
* **Sales values were scaled ×100** to remove decimal-range noise (e.g., 0.1 → 10).
* No raw dataset files are redistributed — only processed evaluation inputs.

To reproduce:
Users must download the dataset directly from Hugging Face.

---

## **What This Repository Provides**

This repository includes:

* classical smoothing models (SES, Holt, Holt-Winters, Theta)
* intermittent-demand models (Croston variants)
* moving-average baselines
* a global ML baseline (LightGBM)
* **Chronos2 — a foundation-model forecasting baseline**

Outputs include:

* SKU-wise metrics ledger
* complete model-selection audit
* forecasts for all evaluated models
* Streamlit dashboard for exploration

This is not a model zoo; it is a **governance-driven forecasting pipeline**.

---

## **Evaluation Principle**

```text
Score = MAE + |Bias|
```

This metric penalizes unstable or directionally misaligned forecasts — a major operational cost driver in fresh retail.

---

## **Key Findings (FreshNet v1.0)**

### **1. Forecast performance is structure-conditional.**

Different models perform better under different ADI–CV² demand structures.

---

### **2. Stability-oriented models perform best when aligned to structure.**

Across the evaluated FreshRetailNet subset, the following models consistently produced low-noise signals **when applied in appropriate regimes**:

* **DynamicOptimizedTheta**
* **SES / Holt / Holt-Winters**
* **SeasonalExpSmoothingOptimized**
* **Croston variants (SBA / Classic)**
* **Chronos2** — robust under mixed or uncertain demand structure

LightGBM improves only when meaningful covariates are included.

---

### **3. Foundation model (Chronos2) behaves as a structure-agnostic baseline.**

Chronos2 performs consistently across varied noise profiles, particularly where demand exhibits mixed patterns and regime certainty is low.

---

### **4. ML without drivers underperforms by design.**

FreshRetailNet-50K includes rich covariates (discount, weather, stockout signals).
When these drivers are withheld by design, LightGBM produces unstable forecasts — an expected outcome rather than a deficiency.

---

## **Repository Structure**

```text
/app                     → Streamlit UI
/data/processed          → subset + scaled FreshRetailNet-50K data
/metrics                 → forecasts, metrics, audit logs
/models                  → classical models + Chronos2 wrappers
/utils                   → helpers
run_pipeline.py          → orchestrates the full pipeline
```

---

## **How to Run**

### Pipeline

```bash
python run_pipeline.py
```

Outputs:

```
metrics/
    combined_metrics.csv
    best_models.csv
    model_selection_audit.csv
```

### Dashboard

```bash
streamlit run app/app.py
```

---

## **Why Stability Matters in Fresh Retail**

Volatile daily demand causes frequent directional shifts.
Each shift forces:

* replanning
* overrides
* waste corrections
* order rebalancing

A stable, structure-aligned forecast reduces resets and increases decision velocity.

---

## **Deployment**

Works on:

* **Hugging Face Spaces**
* **Docker**
* local Streamlit execution

Fully self-contained.

---

## **Summary**

This sandbox delivers:

1. a **structure-aligned, SKU-specific recommended model**
2. a **bias-aware, regime-informed evaluation framework**
3. a **comprehensive model-selection audit log**
4. foundation-model benchmarking via **Chronos2**
5. a reproducible, governance-ready forecasting pipeline


> **If a single forecasting model must be deployed across all SKUs due to operational or governance constraints, Chronos2 is the most appropriate default choice.**
> It provides consistent, bounded performance across heterogeneous demand structures and avoids the collapse modes observed when specialist models are misapplied.

---

## **Version**

**FreshNet Release — v1.0 (December 2025)**

---

