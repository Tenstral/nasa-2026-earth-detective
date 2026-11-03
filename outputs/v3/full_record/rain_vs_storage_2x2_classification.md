# Hydrological Coupling Matrix: Total Water Storage vs. Rainfall Trends (2002–2026)

**Status:** PRELIMINARY — Primary Full-Record Analytical Window (2002-04 to 2026-07)
- **TWS Storage Engine:** Calibrated Effective-Sample-Size (ESS) Mann-Kendall with Hurwicz bias correction and Fourier phase-randomized surrogate.
- **Primary Precipitation Record:** GPM IMERG V07B Final Run (2002–2025; decoupled from GRACE).

## 1. Regional Annual Classifications

| Region | TWS Slope (cm/yr) [95% CI] | TWS Verdict (FDR q) | IMERG Rain Slope (mm/yr) [95% CI] | Rain Verdict (FDR q) | Quadrant ID | Coupling Classification |
|---|---|---|---|---|---|---|
| **NW** | -1.25 [-1.50, -1.02] | `Significant` (q=< 0.0001) | -1.91 [-11.04, +4.48] | `No detectable trend` (q=0.8968) | **`Q1`** | Decoupled Depletion (Bengal Water Storage Paradox) |
| **NE** | -0.56 [-0.70, -0.42] | `Significant` (q=< 0.0001) | -0.59 [-15.38, +16.13] | `No detectable trend` (q=0.9342) | **`Q1`** | Decoupled Depletion (Bengal Water Storage Paradox) |
| **Central** | -0.47 [-0.62, -0.34] | `Significant` (q=< 0.0001) | +0.89 [-9.75, +12.72] | `No detectable trend` (q=0.9342) | **`Q1`** | Decoupled Depletion (Bengal Water Storage Paradox) |
| **SW** | -0.05 [-0.20, +0.10] | `No detectable trend` (q=0.8968) | +2.25 [-7.31, +14.56] | `No detectable trend` (q=0.8968) | `Q3` | No Detectable Trend / Below Detection Limit |
| **SE** | -0.05 [-0.17, +0.06] | `No detectable trend` (q=0.8968) | +1.76 [-9.35, +13.75] | `No detectable trend` (q=0.9342) | `Q3` | No Detectable Trend / Below Detection Limit |
| **National** | -0.51 [-0.66, -0.38] | `Significant` (q=< 0.0001) | +2.04 [-7.70, +12.45] | `No detectable trend` (q=0.9342) | **`Q1`** | Decoupled Depletion (Bengal Water Storage Paradox) |

## 2. Divisional Annual Indicators (Descriptive Only — Not Independent)

> [!NOTE]
> **Spatial Resolution Limitation:** Individual administrative divisions fall below the effective spatial resolution of GRACE gravimetry (~300 km / ~100,000 km²) and exhibit spatial autocorrelation. Division-level series are provided strictly as descriptive, non-independent indicators. Formal trend tests, FDR corrections, and quadrant classifications are made at the 5-region level (+ National) only.

| Division | TWS Slope (cm/yr) [95% CI] | Primary Rain Slope (mm/yr) [95% CI] | Status | Note |
|---|---|---|---|---|
| **Dhaka** | -0.47 [-0.62, -0.34] | +0.89 [-9.75, +12.72] | `Descriptive (not independent)` | Below GRACE mascon resolution |
| **Chattogram** | -0.05 [-0.17, +0.06] | +1.76 [-9.35, +13.75] | `Descriptive (not independent)` | Below GRACE mascon resolution |
| **Rajshahi** | -0.90 [-1.14, -0.69] | -0.89 [-9.30, +5.16] | `Descriptive (not independent)` | Below GRACE mascon resolution |
| **Rangpur** | -1.61 [-1.88, -1.35] | -3.37 [-14.02, +3.71] | `Descriptive (not independent)` | Below GRACE mascon resolution |
| **Khulna** | -0.17 [-0.28, -0.07] | +1.38 [-8.63, +11.61] | `Descriptive (not independent)` | Below GRACE mascon resolution |
| **Barishal** | +0.03 [-0.17, +0.21] | +5.52 [-4.78, +17.85] | `Descriptive (not independent)` | Below GRACE mascon resolution |
| **Sylhet** | -0.40 [-0.53, -0.28] | +0.18 [-16.85, +19.88] | `Descriptive (not independent)` | Below GRACE mascon resolution |
| **Mymensingh** | -0.69 [-0.86, -0.54] | -2.07 [-14.36, +8.40] | `Descriptive (not independent)` | Below GRACE mascon resolution |

## 3. Hydrological Interpretation

1. **Bengal Water Storage Paradox Pattern Observed:**
   - In the **Northwest, Northeast, Central, and National** composite, Total Water Storage exhibits statistically significant multi-decadal depletion (-0.47 to -1.25 cm/yr), while GPM IMERG precipitation shows no detectable trend (-1.9 to +2.0 mm/yr, p >= 0.51).
   - These regions fall into **Quadrant 1: Decoupled Depletion (Bengal Water Storage Paradox)**.
   - Because precipitation has remained stationary without secular decline, the observed storage depletion occurs in the absence of a detected precipitation deficit.
   - This observation is **consistent with, not proof of**, human water extraction exceeding natural replenishment capacity (such as intensive Boro dry-season groundwater abstraction).

2. **Coastal Delta Dynamics (Southwest & Southeast):**
   - In the **Southwest and Southeast**, both storage and precipitation exhibit no detectable trend over the 24-year satellite record (-0.05 cm/yr TWS; +1.8 to +2.3 mm/yr rain), falling into **Quadrant 3: No Detectable Trend / Below Detection Limit**.