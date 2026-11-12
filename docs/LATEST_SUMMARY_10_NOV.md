# Latest Project Changes & Validation Summary (November 10, 2026)

**Project:** Bengal Hydro Detective — NASA Space Apps Challenge 2026  
**Team:** Tenstral  
**Scope:** Changes merged after commit `d6258d1` through `0985f47` (PRs #3, #4, #5) and `upstream/fixes-review` (`9edb82a`)  

---

## 1. What Was Added Since November 9

1. **Interactive Dashboard Overhaul & Zero-Drift Builder (`index.html`, `v3/build_dashboard.py`):**
   - Overhauled `index.html` with a 24-year timeline scrubber, animated division/region SVG map, multi-sensor comparison studio, exploratory seasonal tabs, and pairwise region comparison views.
   - Added `v3/build_dashboard.py` and `tests/test_dashboard_build.py` to compile all CSV/JSON/GeoJSON outputs directly into `index.html`, preventing manual copy-paste drift.
2. **Pairwise Between-Region Slope Comparison & Calibration (`v3/region_comparison.py`, `outputs/v3/region_comparison/`):**
   - Tested all 10 regional pairs for both Total Water Storage (TWS) and GPM IMERG rainfall ($m = 20$ tests) using **Calibrated ESS-MK on paired difference series** ($d(t) = y_A(t) - y_B(t)$).
   - Audited 4 candidate methods across 20 pairs and added a **real-residual circular-shift placebo test** (`real_residual_placebo.json`) to flag pairs sensitive to multi-year empirical noise.
3. **Exploratory Seasonal Storage Response & Dry-Season Drawdown (`v3/seasonal_ratio_trend.py`, `v3/dry_season_drawdown.py`):**
   - Evaluated 22 monsoon seasons (2002–2025, dropping the 2017–2018 gap) for the **Seasonal Storage Response Ratio** ($\Delta\text{TWS} / P_{\text{monsoon}}$) and 23 annual cycles for **Dry-Season Drawdown** ($\text{TWS}_{\text{peak},y} - \text{TWS}_{\text{min},y+1}$), kept separate from the main 336-test table.
4. **Master Number Reconciliation & Pipeline Defaults (`PROJECT_STATUS.md`, `NOTES.md`, `run_all.py`):**
   - Fixed the exposed population total from an old `69.4M` artifact to the exact sum of the 3 depleting regions: **108.5 million people (63.9%)** (NW `38.81M` + NE `24.05M` + Central `45.64M`).
   - Standardized all tables (`exposure_table.csv`, `NOTES.md`, `README.md`) to use primary duality-aligned 95% CIs from `results_all_windows.csv` (e.g., NW full record `[-1.50, -1.02] cm/yr`, $q < 0.0001$).
   - Changed `run_all.py --rain-source` default from `power` to `imerg` and added an explicit warning if NASA POWER is selected.
   - Expanded `tests/test_forbidden_phrases.py` to block overclaiming terms (`paradox`, `recharge efficiency`, `stationary`, `stable`, unquoted `aquifer`).
5. **Regional Stakeholder Action Guide (`regional_action_report.md`):**
   - Added a 5-region guide connecting satellite findings to agricultural and water management practices (AWD irrigation, Barind smart metering, Haor flash-flood varieties, Dhaka rooftop MAR, coastal salinity management, and CHT watershed protection).
   - *Note:* Commit `9edb82a` on `upstream/fixes-review` further refines this file with 8 formal institutional citations (BRRI, IRRI, BMDA, BWDB, FAO, BNBC, UNDP, ICIMOD) and explicit methodological disclaimers (`tests/test_regional_report.py`).

---

## 2. High-Level Validity Check

The latest updates are **methodologically sound** and directly resolve the consistency gaps from the earlier version:

- **Honest Pairwise Calibration & Placebo Disclosure:** When the initial moving-block bootstrap ($b=3$) failed calibration (15.4% false-positive rate), it was archived (`calibration_report_v1_bootstrap_failed.json`) rather than hidden. The replacement method (**Candidate A: Difference-Series ESS-MK**) passes nominal AR(1) calibration across all 20 pairs (**FPR 3.60%–6.50%**, **95% CI coverage 93.50%–96.40%**). Crucially, the team also ran a harder **synchronized real-residual placebo test**, openly flagging that 8 of 10 TWS pairs have elevated false-positive rates (7.4%–46.4%) when multi-year empirical excursions shift across timeline boundaries.
- **No Interpolation Across Satellite Gaps:** In both the seasonal response ratio and dry-season drawdown pipelines, incomplete gap years (2017–2018) are dropped rather than artificially interpolated, and $\pm 6$-month buffer sensitivity runs are reported alongside main runs.
- **Strict Separation of Exploratory vs. Confirmatory Tests:** Exploratory seasonal and pairwise tests use their own Benjamini-Hochberg FDR families so they do not distort the primary 336-test master table (`results_all_windows.csv`).
- **Single Source of Truth Enforcement:** Automated tests (`76 passed` out of 78 in `tests/`) now verify that markdown tables and `index.html` match the CSV/JSON outputs without manual rounding drift.

---

## 3. Latest Key Findings

| Analysis Module | Key Verified Finding | Verdict / Statistical Note |
|---|---|---|
| **Between-Region TWS Differences** (`pairwise_region_differences.md`) | **9 of 10 regional pairs differ** under paired testing. **NW** (-1.255 cm/yr) declines faster than **NE** ($\Delta = -0.653$), **Central** ($\Delta = -0.722$), **SW** ($\Delta = -1.205$), and **SE** ($\Delta = -1.189$ cm/yr). **SW vs SE** shows no difference ($\Delta = +0.006$ cm/yr, $q = 0.77$). | **NE vs Central** shows a small paired difference ($\Delta = -0.072$ cm/yr) due to high spatial correlation ($\rho = 0.945$), but their single-region CIs overlap (`[-0.70, -0.42]` vs `[-0.62, -0.34]`). 8 of 10 pairs carry a `Fails real-residual placebo` caution flag. |
| **Between-Region Rainfall Differences** | **0 of 10 regional pairs differ** in GPM IMERG rainfall ($p \ge 0.14, q \ge 0.28$). | Regional storage divergence occurs without regional rainfall divergence. |
| **Seasonal Storage Response Ratio** ($\Delta\text{TWS} / P_{\text{monsoon}}$, 22 seasons) | Mean monsoon storage rebound is **32.5% nationally** (NW: 39.6%, Central: 42.2%, NE: 30.1%, SW: 33.0%, SE: 26.0%). | **No region passes FDR in the 22-season main run** (Central $+0.39\%/\text{yr}$ and National $+0.14\%/\text{yr}$ are `Suggestive`, $q = 0.11$; NW/NE/SW/SE show `No detectable trend`). Monsoon rebound per mm of rain has not weakened, but dry-season losses still outpace it. |
| **Dry-Season Drawdown** ($\text{Peak}_y - \text{Min}_{y+1}$, 23 cycles) | Mean annual drawdown is **53.2 cm nationally** (NW: 55.2 cm, NE: 58.5 cm, Central: 58.2 cm, SW: 48.7 cm, SE: 51.2 cm). | **No detectable trend in seasonal drawdown amplitude** in any region (all $p \ge 0.50, q = 1.00$; MDS $\approx 0.55–1.30$ cm/yr). Baseline storage is dropping year-over-year while the seasonal swing amplitude stays within detection limits. |
| **Exposed Population & Cropland** (`exposure_table.md`) | **108.5 million people (63.9%)** live in the 3 regions with significant long-term TWS decline. | **NW:** 38.81M people, **74.2% cropland**; **Central:** 45.64M people, **56.4% cropland**; **NE:** 24.05M people, **58.6% cropland**. |

---

## 4. Current Limitations & Next Steps

1. **Current Limitations Properly Bounded:**
   - **Real-Residual Placebo Sensitivity:** Pairwise TWS p-values pass parametric AR(1) calibration but are overconfident under synchronized empirical residual shifts (8 of 10 pairs fail placebo).
   - **Spatial Sharing (~300 km Footprint):** Adjacent macro-regions share gravity signal and coastal leakage, so pairwise differences reflect satellite series differences rather than isolated local pumping rates.
   - **No In-Situ Well or Pumping Data Yet:** Findings remain consistent with dry-season irrigation and urban extraction, but direct attribution still requires BWDB piezometer well records and BMDA/BADC irrigation logs.
2. **Immediate Next Action:**
   - Merge commit `9edb82a` from `upstream/fixes-review` into `main` so the citation-backed `regional_action_report.md`, `outputs/v3/source_candidates.md`, and `tests/test_regional_report.py` are included on the main branch.
