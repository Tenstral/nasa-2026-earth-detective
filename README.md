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
1. Install the required Python packages:
   ```bash
   pip install numpy pandas scipy xarray netCDF4 shapely pyproj matplotlib cartopy openpyxl
   ```
2. Download/update the rainfall data:
   ```bash
   python3 download_nasa_precipitation.py
   ```
3. Run the 2020–2026 trend analysis:
   ```bash
   python3 analyze_trends.py
   ```
4. Open `index.html` in any browser to view the reports and charts.
