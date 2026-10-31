# Bengal Hydro Detective

**NASA Space Apps Challenge 2026 — Be an Earth System Trend Detective!**  
**Team:** Tenstral  
**Status: PRELIMINARY — Subject to Peer Review and Piezometric Validation**

---

> [!IMPORTANT]
> **PRELIMINARY SCIENTIFIC NOTICE & LIMITATIONS**  
> All findings presented in this repository are preliminary. Statistical analyses are computed from satellite records spanning January 2020 to July 2026 (robustness window: June 2018 to July 2026). Correlation does not imply causation. NASA GRACE/GRACE-FO mascon solutions have coarse spatial resolution (~300 km footprint) and reflect vertically integrated **Total Water Storage (TWS)** changes across surface water, soil moisture, and deeper aquifers combined. Findings must be validated against ground-based piezometric and hydrometric monitoring networks across Bangladesh.

---

## About the Project
Bangladesh receives heavy monsoon rainfall every year, yet satellite observations reveal that total water storage in the northern agricultural divisions is steadily and significantly declining. Even during the peak of the monsoon, parts of the northwest fail to reach positive net storage anomalies, while southern deltaic divisions exhibit no detectable downward trend.

This project investigates satellite-observed Total Water Storage and rainfall data from **2020 to 2026** across all **8 administrative divisions and 5 hydrological regions of Bangladesh** to determine whether rainfall and water storage trend differently, and whether regional differences are statistically significant.

---

## Datasets Used
- **NASA CSR GRACE / GRACE-FO RL06.3 Mascons:** Monthly satellite gravity measurements reporting total water storage anomalies in centimeters of equivalent water thickness (0.25° grid, pre-extracted and area-weighted per division).
- **NASA POWER Precipitation (PRECTOTCORR):** Monthly satellite-derived precipitation influx across Bangladesh, reported in annual-total millimeters per year (mm/yr) and percent change per decade (%/decade).
- **Bangladesh Administrative Geometries:** High-resolution GeoJSON boundaries used for geodesic area-weighted integration across all divisions (122,353 km² total national terrestrial domain).

---

## Key Division Findings (Primary Window: 2020–2026)
After deseasonalizing 79 months of continuous observations using a 12-month harmonic baseline, Theil-Sen robust slopes, Hamed-Rao modified Mann-Kendall tests (accounting for temporal autocorrelation), circular block bootstrap (9,999 resamples), and Benjamini-Hochberg False Discovery Rate (FDR) control were computed:

| Division | TWS Rate (cm/yr) | 95% Bootstrap CI [cm/yr] | Hamed-Rao p | BH-FDR q | Verdict Standard |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Rangpur** | **-3.42** | [-4.98, -1.68] | **0.0006** | **0.0049** | **Significant decrease** (Passes FDR & CI excludes 0) |
| **Rajshahi** | **-2.40** | [-3.97, -0.57] | **0.0033** | **0.0177** | **Significant decrease** (Passes FDR & CI excludes 0) |
| **Mymensingh** | **-1.69** | [-3.05, -0.19] | 0.0150 | 0.0709 | **Suggestive decrease** (Fails FDR q < 0.05) |
| **Dhaka** | **-1.19** | [-2.43, +0.10] | 0.0309 | 0.1281 | **Suggestive decrease** (Fails FDR & CI contains 0) |
| **Sylhet** | **-0.44** | [-1.43, +0.59] | 0.3340 | 0.6970 | **No detectable trend** |
| **Khulna** | **-0.38** | [-1.43, +0.47] | 0.4475 | 0.7725 | **No detectable trend** |
| **Barishal** | **+0.30** | [-1.02, +1.71] | 0.6766 | 0.9458 | **No detectable trend** |
| **Chattogram** | **+0.39** | [-0.39, +1.25] | 0.3106 | 0.6766 | **No detectable trend** |
| **National (Area-Weighted)** | **-1.02** | [-2.17, +0.26] | 0.1168 | 0.1985 | **No detectable trend** (Composite rate: -1.25 km³/yr) |

---

## Bengal Hydro Detective v2 Pipeline (Rigorous Statistical Engine)

An end-to-end peer-review-grade statistical framework answering:
> *Do rainfall and total water storage trend differently across Bangladesh's regions, and are those differences statistically significant?*

### Core Architectural Features (v2)
- **5 Hydrologic Regions & National Composite (Area-Weighted Geodesic Series)**:
  - **NW**: Rajshahi + Rangpur (Barind Tract agricultural granary; 30,984 km²)
  - **NE**: Sylhet + Mymensingh (Surma-Kushiyara floodplain / haor basin; 21,198 km²)
  - **Central**: Dhaka (Megacity deep aquifer interface; 17,131 km²)
  - **SW**: Khulna + Barishal (Deltaic / Sundarbans coastal zone; 28,153 km²)
  - **SE**: Chattogram (Chittagong Hill Tracts / coastal orographic zone; 24,887 km²)
  - **National**: All 8 divisions combined (122,353 km²)
- **Hamed-Rao Modified Mann-Kendall Test**: Corrects for serial autocorrelation (lag-1 to lag-3) and calculates effective sample size ($N^*$).
- **Theil-Sen Slope with Vectorized Circular Block-Bootstrap 95% CIs**: 9,999 resamples with block length $b = 12$ months, preserving seasonal inertia and multi-month hydrological memory.
- **Benjamini-Hochberg (BH) False Discovery Rate (FDR)**: Strict multiple hypothesis testing control across all 104 evaluations at $q < 0.05$.
- **Two-Sample Synchronized Difference Tests**: Paired circular block-bootstrap significance tests of slope differences across all regional pairs using synchronized resample indexing.
- **2×2 Diagnostic Matrix & Bengal Water Paradox**: Classifies regions into Decoupled Depletion vs Inconclusive vs No Detectable Trend.
- **Rule-Based Scientific Narratives**: Dynamic text generation in English and Bangla (`task8_narrative_en.txt` and `task8_narrative_bn.txt`) with mandatory scientific limitations statements.
- **Dual Analytical Windows**:
  - Primary Window: 2020-01 to 2026-07 (79 months)
  - GRACE-FO-Era Robustness Window: 2018-06 to 2026-07 (98 months)
  - Long-Term Rolling 5-Year Context Analysis: 2002–2026 (GRACE/GRACE-FO full record)

---

### Key Scientific Findings
1. **The Bengal Water Paradox**: Atmospheric precipitation exhibits **no detectable trend** across all regions (Hamed-Rao $p > 0.50$ everywhere; slopes ranging from $-20.50$ mm/yr [$-7.2$ %/decade] in the SW to $+11.84$ mm/yr [$+4.6$ %/decade] in Central; $+1.23$ mm/yr [$+0.5$ %/decade] in the NW). In stark contrast, total water storage shows severe, statistically confirmed depletion in the **Northwest** ($-2.93$ cm/yr, volumetric loss of $-1.01$ km³/yr, $p = 0.0002$, BH-FDR $q = 0.0018$, 95% CI strictly excluding zero).
2. **Regional Divergence is Statistically Significant**: Paired circular block-bootstrap tests confirm NW storage decline is significantly faster than the Southwest ($\Delta = -1.96$ cm/yr, exact bootstrap $p = 0.0001$, FDR $q = 0.0021$) and Southeast ($\Delta = -2.12$ cm/yr, $p = 0.0002$, FDR $q = 0.0021$). In contrast, zero precipitation differences survive FDR control (all $q \ge 0.05$).
3. **Central & Mymensingh Classification**: Central Bangladesh and Mymensingh exhibit suggestive downward trends (raw $p < 0.05$). However, because their FDR $q$-values exceed 0.05 and Central's bootstrap 95% CI includes zero (Central: $[-2.43, +0.09]$ cm/yr), they are formally classified as **Suggestive decrease / Inconclusive**, leaving Northwest as the sole confirmed Q1 Decoupled Depletion region.
4. **Seasonal Storage Swing & Partitioning**: In the Northwest, mean dry-season drawdown reaches $-33.50$ cm anomaly. Monsoon rainfall averages $392.4$ mm/month ($48.63$ km³ total volume), driving a seasonal storage swing of $9.94$ km³ ($32.07$ cm). Exploratory seasonal swing analysis indicates approximately ~20% ($20.4\%$) of monsoon rainfall influx manifests as seasonal storage swing, with the remainder partitioned into unobserved hydrological components including surface runoff, evapotranspiration, and river drainage.
5. **Year-by-Year Monsoon Recharge (N = 6)**: Exactly 6 complete monsoon seasons occur in the 2020–2026 record (2020 through 2025; 2026 ends in July). Reported descriptively with no trend test or change-point claimed due to the short sample size.

---

## How to Run

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Complete End-to-End v2 Pipeline
Execute all analytical tasks sequentially in ~60 seconds:
```bash
python run_all.py
```

Or customize execution parameters:
```bash
python run_all.py --start 2020-01 --end 2026-07 --seed 42 --grace-nc CSR_GRACE_GRACE-FO_RL0603_Mascons_all-corrections.nc
```

---

## Deliverables & Visualizations (`outputs/v2/`)
- `results.csv` & `results.json`: Unified master dataset containing all metrics, CIs, FDR $q$-values, and classifications.
- `fig_slope_map.png`: Bangladesh choropleth map with non-significant and suggestive divisions hatched with `////`.
- `fig_timeseries_all_regions.png`: 5-panel comparative regional time series with Theil-Sen slope lines and 95% bootstrap envelopes.
- `fig_timeseries_National.png`: Area-weighted composite national time series and trend.
- `fig_2x2_classification.png`: Diagnostic 2×2 quadrant matrix scatter plot.
- `fig_summary_table.png`: Rendered publication-quality executive summary table.
- `fig_context_rolling_5yr_slopes.png`: Long-term 2002–2026 rolling 5-year Theil-Sen slope context analysis marking the 2017–2018 mission gap.
- `task6_year_by_year_monsoon_recharge.csv`: Descriptive year-by-year monsoon rainfall vs storage swing budget ($N=6$).
- `benchmark_table_template.csv` & `.md`: Comparison template contrasting our rates against published literature rates.
- `task8_narrative_en.txt` & `task8_narrative_bn.txt`: Full rule-based scientific interpretation reports in English and Bangla.
