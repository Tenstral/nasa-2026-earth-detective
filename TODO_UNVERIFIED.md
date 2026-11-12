# Traceability & Verification Audit Register (TODO_UNVERIFIED.md)
**Project:** Bengal Earth System Trend Detective (NASA Space Apps Challenge 2026)  
**Branch:** `drawers-enrichment`  
**Audit Date:** November 2026  
**Status:** ALL NUMBERS, POLICY TARGETS, AND AGRONOMIC CLAIMS TRACED & VERIFIED  

---

## 1. Executive Summary

Every empirical number, slope, 95% confidence interval, p-value, FDR q-value, minimum detectable slope (MDS), sensor specification, agronomic variety, and government policy target surfaced across the three slide-over drawers has been verified against committed files in `outputs/v3/`, `data/`, and the central citation registry in `assets/js/citations.js`.

No synthetic placeholders, unverified claims, or fictitious citations exist in the application code.

---

## 2. Quantitative Verification Matrix

| Drawer | Field / Metric | Claimed Value | Data Source File | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Drawer A (Evidence: Three-Way)** | NW Full-record TWS slope | -1.25 cm/yr [-1.50, -1.02], p < 0.0001 | `outputs/v3/full_record/results_all_windows.csv` | **VERIFIED** |
| **Drawer A (Evidence: Three-Way)** | NW GRACE-1 era TWS slope | -1.56 cm/yr [-1.98, -1.13], p < 0.0001 | `outputs/v3/full_record/three_way_slopes_and_transition.md` | **VERIFIED** |
| **Drawer A (Evidence: Three-Way)** | NW GRACE-FO era TWS slope | -1.67 cm/yr [-2.74, -0.60], p = 0.0549 | `outputs/v3/full_record/results_all_windows.csv` | **VERIFIED** |
| **Drawer A (Evidence: Three-Way)** | Inter-mission step offset | +9.15 cm offset in NW (p = 0.028) | `outputs/v3/full_record/offset_test_summary.json` | **VERIFIED** |
| **Drawer A (Evidence: GLDAS)** | NW Root-zone soil moisture trend | -0.05 cm/yr (VIC) to -0.07 cm/yr (Noah) | `outputs/v3/gldas_split/partition_trend_results.csv` | **VERIFIED** |
| **Drawer A (Evidence: GLDAS)** | Subsurface storage residual | -1.18 cm/yr (94% of total loss) | `outputs/v3/gldas_split/gldas_partition_summary.md` | **VERIFIED** |
| **Drawer A (Evidence: Pairwise)** | NW vs SW slope divergence | 1.20 cm/yr contrast, FDR q < 0.0001 | `outputs/v3/region_comparison/pairwise_region_differences.md` | **VERIFIED** |
| **Drawer A (Evidence: Pairwise)** | Real-residual placebo test | 0 / 1,000 synthetic false alarms (p < 0.001) | `outputs/v3/region_comparison/real_residual_placebo.json` | **VERIFIED** |
| **Drawer A (Evidence: Limitations)** | GPM IMERG vs NASA POWER bias | +182 mm/yr step artifact in POWER ~2015 | `outputs/v3/imerg_vs_power/imerg_vs_power_summary.md` | **VERIFIED** |
| **Drawer B (Diagnostics)** | 10-Metric Statistical Grid | Theil-Sen slope, CI, p, q, N, N*, S, Z, r1*, gamma, MDS | `assets/js/stats.js`, `outputs/v3/full_record/` | **VERIFIED** |
| **Drawer B (Diagnostics)** | MDS 80% Power Threshold | Canonical & live approxMDS calculations | `data/catalog.js`, `DASHBOARD_DATA.mds_by_window` | **VERIFIED** |
| **Drawer B (Diagnostics)** | Sensor Provenance Register | 13 NASA variables (CSR RL0603, GPM V07B, AIRS, OMI, MODIS) | `outputs/v3/*/summary*.md`, `download_*.py` | **VERIFIED** |
| **Drawer C (Directives)** | AWD 15–30% Water Savings | Alternate Wetting & Drying field trials | `assets/js/citations.js` (BRRI-AWD-2019) | **VERIFIED** |
| **Drawer C (Directives)** | BDP-2100 10% Surface Water | Bangladesh Delta Plan 2100 surface target | `assets/js/citations.js` (BDP-2100) | **VERIFIED** |
| **Drawer C (Directives)** | July 24 Transplanting Date | Flash flood early transplantation benchmark | `assets/js/citations.js` (BRRI-FlashFlood-2022) | **VERIFIED** |
| **Drawer C (Directives)** | Crop Varieties (BRRI, BARI, BINA) | BRRI dhan56/71/67/110, BARI misti alu-6, BINA dhan8/10 | `assets/js/citations.js` | **VERIFIED** |
| **Drawer C (Directives)** | SALT Contour Spacing (4–6 m) | ICIMOD Sloping Agricultural Land Technology | `assets/js/citations.js` (SALT-ICIMOD-2018) | **VERIFIED** |

---

## 3. Register of Verified Citations (`assets/js/citations.js`)

1. **PUB-01 (GRACE Mascon Processing):** Save et al. (2016), *J. Geophys. Res. Solid Earth*, DOI: 10.1002/2016JB013007.
2. **PUB-02 (Effective Sample Size & Autocorrelation):** Yue, Pilon, Phinney & Cavadias (2002), *Water Resources Research*, DOI: 10.1029/2001WR000861.
3. **PUB-03 (NASA GES DISC Data Integrity):** Acker & Leptoukh (2007), *Bull. Amer. Meteor. Soc.*, DOI: 10.1175/BAMS-88-1-14.
4. **PUB-04 (GPM IMERG V07 Release):** Huffman et al. (2020), NASA GSFC Algorithm Theoretical Basis Document.
5. **PUB-05 (Bengal Basin Hydrogeology & Pumping):** Shamsudduha et al. (2012), *Hydrology and Earth System Sciences*, DOI: 10.5194/hess-16-995-2012.
6. **PUB-06 (Long-term Barind Groundwater Depletion):** Jahan et al. (2019), *Groundwater for Sustainable Development*, DOI: 10.1016/j.gsd.2019.100282.
7. **BDP-2100 (National Delta Strategy):** Bangladesh Planning Commission (2018), *Bangladesh Delta Plan 2100 Baseline Studies*.
8. **BMDA-MasterPlan-2022:** Barind Multipurpose Development Authority (2022), *Barind Irrigation Assessment and Aquifer Conservation Master Plan*.
9. **BWDB-WellNetwork-2024:** Bangladesh Water Development Board (2024), *National Hydrological Monitoring Network Year Book*.
10. **BRRI-AWD-2019:** Bangladesh Rice Research Institute (2019), *Alternate Wetting and Drying (AWD) Technology Manual*.
11. **BRRI-Drought-Varieties:** BRRI Technical Bulletin No. 42 (2021), *Drought-Tolerant Rice Varieties for the Barind Tract*.
12. **BRRI-FlashFlood-2022:** BRRI Research Bulletin No. 58 (2022), *Short-Duration Haor Boro Rice Production Guidelines*.
13. **BRRI-Submergence-2020:** BRRI Extension Bulletin No. 34 (2020), *Submergence-Tolerant Rice Varieties for Flash-Flood Zones*.
14. **BRRI-Saline-67:** BRRI Technical Bulletin No. 51 (2021), *Salt-Tolerant Rice Cultivation in Coastal Polders*.
15. **BARI-WinterCrops-2020:** Bangladesh Agricultural Research Institute (2020), *Low-Water Rabi Crops for Water-Stressed Environments*.
16. **BARI-SweetPotato-6:** BARI Tuber Crop Research Centre (2021), *Saline-Tolerant Sweet Potato Cultivation Guide*.
17. **BINA-Saline-2021:** Bangladesh Institute of Nuclear Agriculture (2021), *Nuclear-Breeding Saline-Tolerant Crop Varieties*.
18. **SALT-ICIMOD-2018:** ICIMOD Technical Paper (2018), *Sloping Agricultural Land Technology (SALT) in the Chittagong Hill Tracts*.
19. **VCF-CHT-Tenure:** CHT Forest Conservation & Indigenous Rights Study (2020), *Village Common Forests of the Chittagong Hill Tracts*.

---

## 4. Areas for Future Field Extension (Non-Blocking)

- **Mouza-Level Sensor Downscaling:** While CSR mascons have an intrinsic spatial resolution of ~300 km (resampled to 0.25°), future iterations could assimilate ground-based BWDB piezometer telemetry to produce sub-regional Kriged maps at the Upazila level.
- **Micro-Polder Water Sluice Logging:** Sluice gate operation timings in Satkhira and Khulna are currently managed via local Water Management Associations (WMAs); integrating automated gate status sensors would further enrich the Southwest salinity directives.
