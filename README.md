# Bengal Hydro Detective

**NASA Space Apps Challenge 2026 — Be an Earth System Trend Detective**  
**Team:** Tenstral

## About the Project
Bangladesh receives heavy monsoon rain every year, yet satellite data shows that water storage in the northern divisions is steadily dropping. Even during the rainy season, parts of the north stay in a water deficit while the south has plenty of water.

This project looks at satellite water storage and rainfall data from **2020 to 2026** across all **8 divisions of Bangladesh** to track how fast water levels are changing and where the problem is worst.

## Datasets Used
- **NASA GRACE / GRACE-FO Mascons:** Monthly satellite measurements showing changes in total water thickness (groundwater, soil moisture, and surface water combined).
- **NASA POWER / GPM IMERG:** Monthly satellite rainfall data for Bangladesh, downloaded automatically through the NASA POWER API.
- **Bangladesh Division Boundaries:** GeoJSON map boundaries used to calculate water and rainfall averages for each division.

## Key Findings (2020–2026)
After removing normal seasonal monsoon ups and downs across 79 months of data, we found a clear downward trend in water storage across the northern and central divisions:

| Division | Yearly Water Change | Trend |
|---|---|---|
| **Rangpur** | `-3.42 cm/yr` | Rapid downward trend |
| **Rajshahi** | `-2.40 cm/yr` | Rapid downward trend |
| **Mymensingh** | `-1.69 cm/yr` | Clear downward trend |
| **Dhaka** | `-1.19 cm/yr` | Moderate downward trend |
| **Sylhet** | `-0.44 cm/yr` | Stable (no clear trend) |
| **Khulna** | `-0.38 cm/yr` | Stable (no clear trend) |
| **Barishal** | `+0.30 cm/yr` | Stable (no clear trend) |
| **Chattogram** | `+0.39 cm/yr` | Slight upward trend |

## Main Files in This Repository
- `download_nasa_precipitation.py` — Downloads monthly rainfall data for Bangladesh (2020–2026) from NASA POWER.
- `download_grace_data.py` — Helper script to download the CSR GRACE water storage dataset.
- `analyze_divisions.py` — Calculates division-level water storage for a selected month and creates maps and reports.
- `analyze_precipitation.py` — Calculates division-level rainfall for a selected month and creates maps and reports.
- `analyze_trends.py` — Calculates the 2020–2026 yearly water change trends and generates the summary chart.
- `create_excel_report.py` — Compiles the division numbers into `bangladesh_water_analysis_detailed.xlsx`.
- `index.html` — Main web page to browse the maps, charts, and seasonal reports in the `outputs/` folder.

## How to Run

### Legacy Scripts (v1)
1. Install dependencies:
   `ash
   pip install -r requirements.txt
   `
2. Run legacy trend analysis:
   `ash
   python analyze_trends.py
   `
3. Open index.html in any browser to view legacy visuals.

---

## Bengal Hydro Detective v2 Pipeline (Rigorous Statistical Engine)

An end-to-end peer-review-grade statistical framework answering:
> *Do rainfall and total water storage trend differently across Bangladesh's regions, and are those differences statistically significant?*

### Core Architectural Features (v2)
- **5 Hydrologic Regions (Area-Weighted Geodesic Series)**:
  - **NW**: Rajshahi + Rangpur (Barind Tract agricultural belt; 30,984 km²)
  - **NE**: Sylhet + Mymensingh (Surma-Kushiyara floodplain / haor basin; 21,198 km²)
  - **Central**: Dhaka (Megacity deep aquifer interface; 17,131 km²)
  - **SW**: Khulna + Barishal (Deltaic / Sundarbans coastal zone; 28,153 km²)
  - **SE**: Chattogram (Chittagong Hill Tracts / coastal orographic zone; 24,887 km²)
- **Hamed-Rao Modified Mann-Kendall Test**: Corrects for temporal autocorrelation (lag-1 to lag-3) and calculates effective sample size (N*).
- **Theil-Sen Slope with Vectorized Circular Block-Bootstrap 95% CIs**: 9,999 resamples with block length b = 12 months, preserving multi-month hydrological memory.
- **Benjamini-Hochberg (BH) False Discovery Rate (FDR)**: Strict multiple hypothesis testing control across all 98 evaluations at q < 0.05.
- **Two-Sample Synchronized Difference Tests**: Bootstrap significance tests of slope differences across all 10 regional pairs.
- **2×2 Diagnostic Matrix & Bengal Water Paradox**: Classifies regions into Decoupled Depletion vs Hydrologically Balanced.
- **Rule-Based Scientific Narratives**: Dynamic text generation in English and Bangla (task8_narrative_en.txt and task8_narrative_bn.txt) with mandatory scientific limits statement.

### Key Scientific Findings
1. **The Bengal Water Paradox**: Atmospheric precipitation is statistically flat across all regions (p > 0.50 everywhere, slopes between +0.10 and -1.70 mm/yr). In contrast, total water storage is dropping rapidly in the **Northwest** (-2.93 cm/yr, -0.91 km³/yr, p = 0.0002) and in **Central / Dhaka** (-1.19 cm/yr, p = 0.031).
2. **Regional Divergence is Real**: Pairwise bootstrap tests confirm NW storage decline is significantly steeper than all other 4 regions (p < 0.0001, surviving FDR at q = 0.0012). Precipitation slopes do not diverge (p > 0.49).
3. **Severe Seasonal Asymmetry in NW**: NW experiences dry-season drawdown of -33.86 cm mean anomaly. Despite receiving 380 mm/month of monsoon rain, storage anomaly remains **negative** (-1.32 cm) even at the monsoon peak. Only 21.4% of seasonal monsoon rainfall is retained as storage swing.

### Running the Complete v2 Pipeline
Execute all 8 analytical tasks sequentially in ~60 seconds:
`ash
python run_all.py
`
Or customize parameters:
`ash
python run_all.py --start 2020-01 --end 2026-07 --seed 42 --grace-nc /path/to/CSR_GRACE.nc
`

### v2 Outputs & Figures (outputs/v2/)
- 
esults.csv & 
esults.json: Unified master dataset of all metrics, CIs, FDR q-values, and classifications.
- ig_slope_map.png: Bangladesh choropleth map with non-significant divisions (p >= 0.05) hatched with ////.
- ig_timeseries_all_regions.png: 5-panel comparative time series with Theil-Sen slope lines and 95% bootstrap bands.
- ig_2x2_classification.png: Diagnostic 2×2 quadrant matrix scatter plot.
- ig_summary_table.png: Rendered publication-quality summary table.
- 	ask6_year_by_year_monsoon_recharge.csv: Descriptive year-by-year monsoon rainfall vs storage swing budget.
- enchmark_table_template.csv / .md: Template comparing our rates against published literature rates.
- 	ask8_narrative_en.txt & 	ask8_narrative_bn.txt: Full rule-based scientific interpretation reports.
