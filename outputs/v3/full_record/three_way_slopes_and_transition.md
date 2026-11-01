# GRACE to GRACE-FO Transition & Three-Way Slope Sensitivity Report

**Status:** PRELIMINARY — Robustness Analysis of Satellite Transition & Gap Artifacts

## 1. Executive Summary & Lead Evidence Framework

- **Primary Lead Evidence:** The **transition-free GRACE era (2002-04 to 2017-06)** serves as our cleanest, primary benchmark for long-term storage depletion, entirely unaffected by satellite instrument handover or sensor intercalibration offsets.
- **Transition Shift:** Between GRACE decommissioning (2017-06) and GRACE-FO initial observation (2018-06), an upward step offset is detected in the raw gravimetric anomaly series (+9.15 cm in NW, p = 0.028; +6.93 cm in Central, p = 0.047; +6.82 cm in NE, p = 0.051).
- **Buffer Sensitivity:** When a ±6-month transition buffer (2017-01 to 2018-11) is excluded, the step term ceases to be statistically significant in all regions (NW: +7.83 cm, p = 0.171; NE: +4.00 cm, p = 0.402; Central: +3.93 cm, p = 0.385; National: +3.09 cm, p = 0.486).
- **Single-Line Underestimation:** Because the +9.15 cm transition step acts as an upward shift midway through the record, a single continuous linear trend line through both satellite missions dilutes the apparent depletion rate (-1.25 cm/yr) relative to the uncorrupted single-satellite epoch (-1.56 cm/yr).
- **Pure Step Simulation Warning:** Monte Carlo null simulations demonstrate that a pure step offset (+9.15 cm) injected into stationary red noise (AR(1) phi=0.65) is falsely flagged as a statistically significant trend in **93.8% to 100% of simulations** under standard linear trend engines. Therefore, multi-satellite linear trends across unbridged gaps must always be reported alongside step-adjusted and transition-excluded bounds.

## 2. Three-Way Slope Comparison Table

| Region | Lead Evidence: GRACE-Era (2002–2017) | Single-Line Fit (2002–2026) | Step-Adjusted Fit (2002–2026) | Transition Offset (p-value) | Transition-Excluded (±6 mo Buffer) | Reported Depletion Range |
|---|---|---|---|---|---|---|
| **NW** | **-1.56 cm/yr** ([-2.03, -1.11]) | -1.25 cm/yr ([-1.54, -0.96]) | -1.81 cm/yr | +9.15 cm (p = 0.0280) | -1.29 cm/yr (p = 0.171) | **-1.81 to -1.25 cm/yr** |
| **NE** | **-0.72 cm/yr** ([-0.99, -0.49]) | -0.56 cm/yr ([-0.70, -0.42]) | -1.04 cm/yr | +6.82 cm (p = 0.0511) | -0.65 cm/yr (p = 0.402) | **-1.04 to -0.56 cm/yr** |
| **Central** | **-0.63 cm/yr** ([-0.86, -0.42]) | -0.47 cm/yr ([-0.62, -0.34]) | -0.98 cm/yr | +6.93 cm (p = 0.0472) | -0.59 cm/yr (p = 0.385) | **-0.98 to -0.47 cm/yr** |
| **National** | **-0.68 cm/yr** ([-0.92, -0.45]) | -0.51 cm/yr ([-0.66, -0.38]) | -0.91 cm/yr | +5.81 cm (p = 0.0713) | -0.58 cm/yr (p = 0.486) | **-0.91 to -0.51 cm/yr** |

## 3. Minimum Detectable Slopes (MDS) by Analytical Window

Power analysis with regional residual variance scaling demonstrates that the statistical power to detect subtle trends depends heavily on observation window length:

| Window | Observation Length | Minimum Detectable Slope (MDS, 80% Power) | Interpretation of Null Verdicts |
|---|---|---|---|
| `full_record` (2002–2026) | 24.2 years (257 valid mo) | **0.22 to 0.32 cm/yr** | Detects subtle multi-decadal trends; high statistical power |
| `grace_era` (2002–2017) | 15.2 years (163 valid mo) | **0.42 to 0.73 cm/yr** | Robust single-satellite baseline; clean lead evidence |
| `grace_fo_era` (2018–2026) | 8.1 years (94 valid mo) | **0.98 to 1.74 cm/yr** | Moderate power; trends < 1.0 cm/yr are below detection limit |
| `recent_2020` (2020–2026) | 6.5 years (79 valid mo) | **1.28 to 2.34 cm/yr** | Short sensitivity baseline; non-significant trends represent **below detection limit**, not proof of zero change |

> [!IMPORTANT]
> In the short recent windows (`grace_fo_era` and `recent_2020`), non-significant trend tests must never be characterized as 'no change' or 'flat'. True depletion rates of -0.5 to -0.8 cm/yr fall entirely below the 80% detection limit of the short-duration satellite sample size.