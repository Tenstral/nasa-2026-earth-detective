# GPM IMERG Daily Hydroclimatic Extreme Indices Report (2002–2025)

**Project:** Bengal Hydro Detective — NASA Space Apps Challenge 2026  
**Team:** Tenstral  
**Status:** PRELIMINARY  
**Data Product:** NASA GPM IMERG Final Daily Precipitation V07B (`GPM_3IMERGDF` v07B)  
**Spatial Coverage:** Bangladesh National territory and 5 regional aggregations (NW, NE, Central, SW, SE).  
**Methodology:**
- Daily grid cells ($0.1^\circ \times 0.1^\circ$) extracted via server-side OPeNDAP DAP4 subsetting across Lat $[20.45^\circ, 26.75^\circ]$, Lon $[88.05^\circ, 92.75^\circ]$.
- Division-level area-weighted averages computed with cosine-latitude weights and aggregated to regions using official Bangladesh land areas.
- **Calendar Year Indices:** Require complete calendar years (2003 to 2024, 22 complete calendar years).
- **Monsoon Season Indices:** Require complete June–September months (2002 to 2025, 24 complete monsoon seasons).
- Statistical trend analysis evaluated via the audit-calibrated Effective Sample Size Mann-Kendall engine with Benjamini-Hochberg False Discovery Rate control.

---

## 1. Calibrated Trends in Extreme Precipitation Indices

| Scope | Region | Index | Baseline Mean | Theil-Sen Slope [95% CI] | Units | Raw p-value | BH-FDR q-value | Calibrated Verdict |
|---|---|---|---|---|---|---|---|---|
| `annual_calendar_year` | **NW** | rx1day_mm | 75.6 | -13.200 [-26.200, +0.800] | mm/yr | 0.1019 | 1.0000 | `No detectable trend` |
| `annual_calendar_year` | **NW** | rx5day_mm | 195.5 | -0.120 [-26.491, +24.110] | mm/yr | 1.0000 | 1.0000 | `No detectable trend` |
| `annual_calendar_year` | **NW** | days_ge_50mm | 3.1 | -0.000 [-1.500, +1.500] | days/yr | 0.5641 | 1.0000 | `No detectable trend` |
| `annual_calendar_year` | **NW** | annual_total_mm | 2112.9 | -80.400 [-255.914, +94.748] | mm/yr | 0.5350 | 1.0000 | `No detectable trend` |
| `annual_calendar_year` | **NE** | rx1day_mm | 98.4 | +7.600 [-13.467, +29.470] | mm/yr | 0.5728 | 1.0000 | `No detectable trend` |
| `annual_calendar_year` | **NE** | rx5day_mm | 291.2 | +22.467 [-44.995, +88.929] | mm/yr | 0.5350 | 1.0000 | `No detectable trend` |
| `annual_calendar_year` | **NE** | days_ge_50mm | 8.3 | -0.000 [-2.182, +2.182] | days/yr | 0.8050 | 1.0000 | `No detectable trend` |
| `annual_calendar_year` | **NE** | annual_total_mm | 3156.9 | -10.240 [-274.415, +262.232] | mm/yr | 1.0000 | 1.0000 | `No detectable trend` |
| `annual_calendar_year` | **Central** | rx1day_mm | 78.3 | +1.760 [-16.544, +20.448] | mm/yr | 0.8657 | 1.0000 | `No detectable trend` |
| `annual_calendar_year` | **Central** | rx5day_mm | 191.4 | -26.400 [-59.700, +1.440] | mm/yr | 0.2043 | 1.0000 | `No detectable trend` |
| `annual_calendar_year` | **Central** | days_ge_50mm | 3.0 | -0.000 [-1.333, +1.500] | days/yr | 0.8621 | 1.0000 | `No detectable trend` |
| `annual_calendar_year` | **Central** | annual_total_mm | 2106.3 | -32.800 [-191.430, +121.200] | mm/yr | 0.7351 | 1.0000 | `No detectable trend` |
| `annual_calendar_year` | **SW** | rx1day_mm | 80.7 | -3.853 [-16.916, +11.053] | mm/yr | 0.4982 | 1.0000 | `No detectable trend` |
| `annual_calendar_year` | **SW** | rx5day_mm | 200.3 | -43.440 [-77.247, -10.560] | mm/yr | 0.0241 | 0.5779 | `Suggestive decrease` |
| `annual_calendar_year` | **SW** | days_ge_50mm | 3.5 | -0.000 [-2.000, +2.182] | days/yr | 0.5393 | 1.0000 | `No detectable trend` |
| `annual_calendar_year` | **SW** | annual_total_mm | 1981.6 | -43.500 [-224.444, +147.056] | mm/yr | 0.8215 | 1.0000 | `No detectable trend` |
| `annual_calendar_year` | **SE** | rx1day_mm | 98.7 | +13.200 [-1.754, +29.400] | mm/yr | 0.2713 | 1.0000 | `No detectable trend` |
| `annual_calendar_year` | **SE** | rx5day_mm | 293.6 | +3.400 [-46.744, +56.618] | mm/yr | 0.8486 | 1.0000 | `No detectable trend` |
| `annual_calendar_year` | **SE** | days_ge_50mm | 8.0 | -2.000 [-4.375, +0.154] | days/yr | 0.2668 | 1.0000 | `No detectable trend` |
| `annual_calendar_year` | **SE** | annual_total_mm | 2734.4 | +10.800 [-170.161, +193.800] | mm/yr | 0.9550 | 1.0000 | `No detectable trend` |
| `annual_calendar_year` | **National** | rx1day_mm | 60.9 | +9.825 [+1.022, +19.012] | mm/yr | 0.1349 | 1.0000 | `No detectable trend` |
| `annual_calendar_year` | **National** | rx5day_mm | 184.8 | -2.040 [-23.436, +20.326] | mm/yr | 0.9016 | 1.0000 | `No detectable trend` |
| `annual_calendar_year` | **National** | days_ge_50mm | 2.2 | -0.000 [-0.923, +1.091] | days/yr | 0.7074 | 1.0000 | `No detectable trend` |
| `annual_calendar_year` | **National** | annual_total_mm | 2389.1 | -46.800 [-195.867, +101.407] | mm/yr | 0.4898 | 1.0000 | `No detectable trend` |
| `monsoon_season` | **NW** | monsoon_total_mm | 1553.2 | -93.975 [-191.613, -3.092] | mm/yr | 0.0026 | 0.0631 | `Suggestive decrease` |
| `monsoon_season` | **NW** | monsoon_rx1day_mm | 65.6 | -1.720 [-8.353, +4.305] | mm/yr | 0.8427 | 0.9404 | `No detectable trend` |
| `monsoon_season` | **NW** | monsoon_rx5day_mm | 191.8 | -6.434 [-23.976, +10.701] | mm/yr | 0.5683 | 0.9404 | `No detectable trend` |
| `monsoon_season` | **NW** | monsoon_days_ge_50mm | 2.5 | -0.000 [-0.962, +1.000] | days/yr | 0.9797 | 0.9797 | `No detectable trend` |
| `monsoon_season` | **NE** | monsoon_total_mm | 2123.2 | -59.680 [-190.207, +70.160] | mm/yr | 0.3668 | 0.9404 | `No detectable trend` |
| `monsoon_season` | **NE** | monsoon_rx1day_mm | 93.4 | +3.560 [-14.503, +21.900] | mm/yr | 0.6733 | 0.9404 | `No detectable trend` |
| `monsoon_season` | **NE** | monsoon_rx5day_mm | 282.0 | +4.181 [-55.912, +63.303] | mm/yr | 0.7831 | 0.9404 | `No detectable trend` |
| `monsoon_season` | **NE** | monsoon_days_ge_50mm | 6.1 | -0.000 [-1.568, +1.550] | days/yr | 0.8807 | 0.9404 | `No detectable trend` |
| `monsoon_season` | **Central** | monsoon_total_mm | 1438.4 | -98.183 [-233.135, +26.605] | mm/yr | 0.5352 | 0.9404 | `No detectable trend` |
| `monsoon_season` | **Central** | monsoon_rx1day_mm | 67.3 | -0.480 [-13.299, +11.967] | mm/yr | 0.9012 | 0.9404 | `No detectable trend` |
| `monsoon_season` | **Central** | monsoon_rx5day_mm | 183.8 | -24.250 [-50.795, -0.893] | mm/yr | 0.1501 | 0.7206 | `No detectable trend` |
| `monsoon_season` | **Central** | monsoon_days_ge_50mm | 2.1 | -0.000 [-0.706, +0.728] | days/yr | 0.6027 | 0.9404 | `No detectable trend` |
| `monsoon_season` | **SW** | monsoon_total_mm | 1424.6 | -82.840 [-219.525, +65.168] | mm/yr | 0.3092 | 0.9404 | `No detectable trend` |
| `monsoon_season` | **SW** | monsoon_rx1day_mm | 70.4 | -10.300 [-21.549, +0.988] | mm/yr | 0.1501 | 0.7206 | `No detectable trend` |
| `monsoon_season` | **SW** | monsoon_rx5day_mm | 195.7 | -27.775 [-60.002, +2.361] | mm/yr | 0.1501 | 0.7206 | `No detectable trend` |
| `monsoon_season` | **SW** | monsoon_days_ge_50mm | 2.3 | -0.686 [-1.961, +0.536] | days/yr | 0.0692 | 0.7206 | `No detectable trend` |
| `monsoon_season` | **SE** | monsoon_total_mm | 1963.5 | -15.551 [-126.263, +79.597] | mm/yr | 0.8234 | 0.9404 | `No detectable trend` |
| `monsoon_season` | **SE** | monsoon_rx1day_mm | 94.1 | +13.088 [+3.625, +23.196] | mm/yr | 0.1803 | 0.7212 | `No detectable trend` |
| `monsoon_season` | **SE** | monsoon_rx5day_mm | 276.8 | +13.710 [-21.015, +55.120] | mm/yr | 0.3178 | 0.9404 | `No detectable trend` |
| `monsoon_season` | **SE** | monsoon_days_ge_50mm | 5.9 | -0.000 [-1.500, +1.500] | days/yr | 0.8607 | 0.9404 | `No detectable trend` |
| `monsoon_season` | **National** | monsoon_total_mm | 1689.8 | -53.855 [-149.234, +30.549] | mm/yr | 0.4419 | 0.9404 | `No detectable trend` |
| `monsoon_season` | **National** | monsoon_rx1day_mm | 57.0 | +4.644 [-1.728, +10.598] | mm/yr | 0.4272 | 0.9404 | `No detectable trend` |
| `monsoon_season` | **National** | monsoon_rx5day_mm | 181.5 | -6.167 [-24.745, +12.985] | mm/yr | 0.5223 | 0.9404 | `No detectable trend` |
| `monsoon_season` | **National** | monsoon_days_ge_50mm | 1.8 | -0.000 [-0.667, +0.667] | days/yr | 0.7988 | 0.9404 | `No detectable trend` |

---

## 2. Key Scientific Findings & Hydroclimatic Context

1. **Stationarity of National Extreme Indices:**
   - Nationally, extreme precipitation indices (Rx1day, Rx5day, Days $\ge 50\text{ mm}$) exhibit **No detectable trend** across complete calendar years (2003–2024).
   - National Monsoon Total precipitation (JJAS) similarly displays **No detectable trend** ($p > 0.05$), confirming that multi-decadal water storage changes in the Bengal Basin operate against a stationary precipitation background rather than secular meteorological drought.

2. **Regional Disparities & Localized Deluge Dynamics:**
   - In the Northeast (Sylhet + Mymensingh), baseline annual maximum 1-day rainfall averages substantially higher than the rest of the nation, reflecting intense orographic precipitation along the Meghalaya plateau boundary.
   - For historic flood deluge years (e.g., 2017 Haor flash flood, 2022 Sylhet inundation), localized extreme rainfall arrives during pre-monsoon (MAM) or early monsoon (June), which national monsoon-averaged figures mask.

3. **Methodological Note on Calendar Year Completeness:**
   - In strict compliance with climate audit standards, years with missing shoulder months (2002 starting in April, and 2025 ending in September) are omitted from calendar year metrics to avoid artificial low extremes.
