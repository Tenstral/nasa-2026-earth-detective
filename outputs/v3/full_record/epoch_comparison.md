# GRACE Era vs. GRACE-FO Era Epoch Comparison & Transition Reporting (Task 4)

**Status:** PRELIMINARY — Paired Epoch Difference Testing with Calibrated Significance Engine
- **Epoch 1:** GRACE Primary Mission (2002-04 to 2017-06; 161 valid observation months)
- **Epoch 2:** GRACE-FO Follow-On Mission (2018-06 to 2026-07; 96 valid observation months)
- **Engine:** Calibrated Effective-Sample-Size (ESS) Mann-Kendall with Hurwicz bias correction and Fourier phase-randomized surrogate; paired circular block bootstrap ($B = 9,999$) on slope differences.

---

## 1. Executive Summary: Core Headline Findings

1. **No Clear Evidence of Acceleration or Deceleration:**
   - Across all regions of Bangladesh, the 95% confidence interval for the paired slope difference $(\beta_{\text{Epoch 2}} - \beta_{\text{Epoch 1}})$ **includes zero** ($p \ge 0.60$ for NW, NE, Central, and National).
   - In the high-depletion Northwest, the slope difference is only **-0.10 cm/yr** (95% CI [-1.60, +1.43] cm/yr), indicating that water storage depletion is **continuing at a similar rate** across both satellite missions without clear evidence of acceleration or deceleration.

2. **Physical Explanation of the Full-Record Slope Dilution:**
   - In the Northwest, the full-record single-line slope (**-1.25 cm/yr**) is smaller in magnitude than **both** individual epoch slopes (**-1.56 cm/yr** in GRACE-1; **-1.67 cm/yr** in GRACE-FO).
   - This apparent flattening is driven entirely by an **upward transition step offset of +9.15 cm ($p = 0.028$)** occurring during the 11-month observation gap (2017-06 to 2018-06).
   - Drawing a single unadjusted regression line through two downward-sloping series separated by an upward jump creates a geometric lever that artificially flattens the long-term trend estimate.
   - When a ±6-month buffer around the transition gap is excluded, the step term ceases to be statistically significant (**+7.83 cm, $p = 0.171$**), yielding a transition-excluded slope of **-1.29 cm/yr**.
   - When step-adjusted, the NW depletion velocity is **-1.81 cm/yr**.

3. **Simulation Warning on Pure Step Offsets:**
   - Monte Carlo null simulations prove that injecting a pure +9.15 cm step offset into stationary red noise induces false trend rejections in **93.8% to 100% of simulations** under standard linear trend engines.
   - Consequently, the transition-free **`grace_era` (-1.56 cm/yr)** must serve as the primary, uncorrupted benchmark for long-term storage depletion, and multi-satellite linear trends across unbridged gaps must always be reported alongside three-way bounds.

---

## 2. Calibrated Epoch Comparison Table

| Region | Epoch 1: GRACE (2002–2017) [95% CI] | Epoch 1 Verdict | Epoch 2: GRACE-FO (2018–2026) [95% CI] | Epoch 2 Verdict | Slope Difference (Ep2 - Ep1) [95% CI] | Diff $p$-value | Calibrated Verdict |
|---|---|---|---|---|---|---|---|
| **NW** | **-1.56** [-2.03, -1.11] | `Significant` | **-1.67** [-3.22, -0.11] | `Suggestive` | -0.10 [-1.60, +1.43] | 0.9055 | **`Continuing at a similar rate`** |
| **NE** | **-0.72** [-0.99, -0.49] | `Significant` | **-0.79** [-1.78, +0.19] | `No detectable trend` | -0.06 [-0.95, +0.82] | 0.8733 | **`Continuing at a similar rate`** |
| **Central** | **-0.63** [-0.86, -0.42] | `Significant` | **-0.81** [-1.79, +0.20] | `No detectable trend` | -0.18 [-1.04, +0.67] | 0.6351 | **`Continuing at a similar rate`** |
| **SW** | **-0.13** [-0.28, +0.03] | `No detectable trend` | **+0.53** [-0.47, +1.53] | `No detectable trend` | +0.65 [-0.32, +1.58] | 0.1708 | `No clear evidence of change` |
| **SE** | **-0.12** [-0.27, +0.02] | `No detectable trend` | **+0.45** [-0.30, +1.22] | `No detectable trend` | +0.58 [-0.09, +1.22] | 0.0836 | `No clear evidence of change` |
| **National** | **-0.68** [-0.92, -0.45] | `Significant` | **-0.47** [-1.50, +0.53] | `No detectable trend` | +0.21 [-0.71, +1.13] | 0.6039 | **`Continuing at a similar rate`** |

---

## 3. Three-Way Slope Reporting & Depletion Bounds

To ensure transparency regarding satellite transition sensitivity, regional storage depletion is reported three ways alongside the clean single-mission baseline:

| Region | Single-Line Fit (2002–2026) | Step-Adjusted Fit (2002–2026) | Transition-Excluded (±6 mo Buffer) | Lead Evidence: GRACE-Era (2002–2017) | Reported Depletion Range |
|---|---|---|---|---|---|
| **NW** | -1.25 cm/yr ([-1.54, -0.96]) | -1.81 cm/yr | -1.29 cm/yr (p=0.171) | **-1.56 cm/yr** ([-2.03, -1.11]) | **-1.81 to -1.25 cm/yr** |
| **NE** | -0.56 cm/yr ([-0.70, -0.42]) | -1.04 cm/yr | -0.65 cm/yr (p=0.402) | **-0.72 cm/yr** ([-0.99, -0.49]) | **-1.04 to -0.56 cm/yr** |
| **Central** | -0.47 cm/yr ([-0.62, -0.34]) | -0.98 cm/yr | -0.59 cm/yr (p=0.385) | **-0.63 cm/yr** ([-0.86, -0.42]) | **-0.98 to -0.47 cm/yr** |
| **National** | -0.51 cm/yr ([-0.66, -0.38]) | -0.91 cm/yr | -0.58 cm/yr (p=0.486) | **-0.68 cm/yr** ([-0.92, -0.45]) | **-0.91 to -0.51 cm/yr** |

---

## 4. Minimum Detectable Slopes (MDS) by Analytical Window

| Window | Observation Length | Minimum Detectable Slope (MDS, 80% Power) | Interpretation of Null Results |
|---|---|---|---|
| `full_record` (2002–2026) | 24.2 years (257 valid mo) | **0.22 to 0.32 cm/yr** | Detects subtle multi-decadal trends; high statistical power |
| `grace_era` (2002–2017) | 15.2 years (161 valid mo) | **0.42 to 0.73 cm/yr** | Clean single-satellite baseline; primary lead evidence |
| `grace_fo_era` (2018–2026) | 8.1 years (96 valid mo) | **0.98 to 1.74 cm/yr** | Slopes < 1.0 cm/yr fall below detection limit |
| `recent_2020` (2020–2026) | 6.5 years (79 valid mo) | **1.28 to 2.34 cm/yr** | Short sensitivity baseline; non-significant trends represent **below detection limit**, not zero change |

> [!IMPORTANT]
> In `grace_fo_era` (8.1 years) and `recent_2020` (6.5 years), non-significant trend tests must never be worded as 'no change'. True depletion velocities of -0.5 to -0.8 cm/yr are below the statistical detection threshold of shorter satellite observation lengths.