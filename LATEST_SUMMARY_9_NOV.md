# Project Update & Research Summary (November 9, 2026)

**Project:** Bengal Hydro Detective — NASA Space Apps Challenge 2026  
**Team:** Tenstral  
**Status:** Preliminary — Subject to In-Situ Validation  

---

## 1. What Was Added After Your Last Commit (`898e2cc`)

Following your October 29, 2026 commit (`898e2cc`, which added the NASA precipitation and GRACE Mascon downloader scripts), **Tariq Youhana Leon** (`Aurelian Kael` / `TariqYouhana`) contributed 27 commits across two major phases:

### Phase 1: The `v2` & `v3` Pipeline Expansion (Oct 31 – Nov 1, 2026)
1. **Full 24-Year Time Series Expansion (`v3/run_workstream0.py`, `v3/windows.py`):**
   - Expanded the analysis from a short post-2020 window to the full **24-year satellite record (April 2002 to July 2026, 257 observed months)**.
   - Structured the evaluation across 4 distinct time windows: `full_record` (2002–2026), `grace_era` (2002–2017), `grace_fo_era` (2018–2026), and `recent_2020` (2020–2026).
   - Grouped Bangladesh's 8 administrative divisions into **5 hydrologically meaningful macro-regions** (Northwest, Northeast, Central, Southwest, Southeast) plus a **National** composite, generating 336 structured statistical tests in `outputs/v3/full_record/results_all_windows.csv`.
2. **Primary Rainfall Replacement & Cross-Validation (`v3/imerg_pipeline.py`, `v3/rainfall_homogeneity_pipeline.py`):**
   - Downloaded and processed **NASA GPM IMERG V07B Final Run** monthly and daily satellite rainfall data (2002–2025).
   - Tested data homogeneity (Pettitt and SNHT change-point tests) comparing NASA POWER against GPM IMERG, uncovering a major artificial jump in NASA POWER around 2015 and establishing GPM IMERG as the primary rainfall dataset.
3. **Soil Moisture & Subsurface Partitioning (`v3/gldas_multi_model_processor.py`):**
   - Added 3 NASA GLDAS Land Surface Models (**Noah 2.1**, **VIC 2.1**, and **CLSM 2.2**) to subtract topsoil moisture ($\Delta\text{SMS}$), snow water, and canopy water from GRACE Total Water Storage ($\text{TWS}$), isolating the subsurface and surface residual (`groundwater + surface water + model error residual`).
4. **Cropland & Population Exposure (`v3/exposure_processor.py`):**
   - Added **MODIS Land Cover (`MCD12Q1`)** cropland percentages and **NASA SEDAC (`GPWv4`)** population data (scaled to the 2022 Bangladesh Census) to map human and agricultural exposure to water loss.
5. **Flood Events, Daily Extremes & Seasonal Recharge (`v3/imerg_daily_extremes_pipeline.py`, `v3/seasonal_recharge.py`, `v3/extremes_processor.py`):**
   - Computed daily extreme rainfall indices (max 1-day rain `Rx1day`, max 5-day rain `Rx5day`, and heavy rain days $\ge 50\text{ mm}$).
   - Calculated 22 years of monsoon water storage response ratios ($\Delta\text{TWS} / P_{\text{monsoon}}$) and analyzed storage behavior during 5 major historical floods (2004, 2007, 2017, 2020, 2022).
6. **Literature Benchmark (`v3/benchmark_builder.py`):**
   - Built a structured comparison table (`outputs/v3/benchmark/benchmark_table.md`) comparing the team's numbers against 6 peer-reviewed studies on Bangladesh water storage.

### Phase 2: The `fixes-review` Audit & Calibration (Nov 1 – Nov 2, 2026)
1. **Statistical Method Calibration (`v3/trend_engine.py`, `v3/gap_calibration.py`):**
   - Replaced the uncalibrated Hamed-Rao test (which had a 13%–17% false-positive rate on autocorrelated satellite data) with **Calibrated Effective Sample Size Mann-Kendall (ESS-MK)** using Hurwicz AR(1) bias correction and rank-aligned Theil-Sen 95% confidence intervals.
2. **Bug Fixes & Quarantine of Circular Data:**
   - Removed an accidental $12\times$ multiplier bug in daily extreme precipitation trends.
   - Separated **GLDAS CLSM 2.2** from the independent soil moisture budget because CLSM 2.2 directly assimilates GRACE data (which would make subtracting it from GRACE circular reasoning), keeping only independent models (**Noah 2.1** and **VIC 2.1**) for primary partitioning.
3. **Strict Language Rules & Automated Tests (`tests/`, `PROJECT_STATUS.md`, `NOTES.md`, `FIXES_REVIEW_REPORT.md`):**
   - Added 10 test modules checking statistical math, units, and wording, ensuring the reports state what satellite data is **"consistent with"** rather than making unsupported claims of direct proof.

---

## 2. High-Level Validity Check of Leon's Work

Overall, **the scientific methodology and statistical results are valid and substantially stronger than the earlier version of the project.** Key reasons why the work holds up to scrutiny:

1. **Proper Handling of Satellite Autocorrelation and Gaps:**
   - Monthly water storage data is strongly autocorrelated (one wet or dry month influences the next), and the GRACE record has missing months (including an 11-month gap between GRACE and GRACE-FO in 2017–2018).
   - Standard trend tests produce high false-alarm rates on this kind of data. By validating the **Calibrated ESS-MK** method against 2,000 Monte Carlo red-noise simulations with the exact 257-month observation mask, the false-positive rate is kept within nominal bounds (**4.10% to 5.45%**, target 5%) and 95% confidence interval coverage is accurate (**94.55% to 95.95%**).
   - Applying **Benjamini-Hochberg False Discovery Rate (BH-FDR, $q < 0.05$)** prevents false positives when running 336 tests across regions and seasons.
2. **Correct Spatial Scale for GRACE Gravimetry:**
   - Because GRACE satellite mascons have a coarse native footprint (~300 km), treating individual administrative divisions as independent catchments is scientifically invalid. Grouping divisions into 5 larger geographic regions (and National) for hypothesis testing while labelling division-level numbers as descriptive only is the correct approach.
3. **Identifying the NASA POWER Rainfall Artifact:**
   - Earlier scripts using NASA POWER (`PRECTOTCORR`) suggested rainfall was rapidly increasing (+28 to +108 mm/yr). Cross-checking against **NASA GPM IMERG V07B** proved that NASA POWER had an artificial upward step jump of **+45% to +84%** around 2014–2015. Switching the primary rainfall source to GPM IMERG prevented a major scientific error.
4. **Avoiding Circularity in Soil Moisture Subtraction:**
   - Quarantining GLDAS CLSM 2.2 and using only open-loop models (Noah 2.1 and VIC 2.1) ensures that subtracting soil moisture from GRACE Total Water Storage is physically independent.
5. **Transparent Reporting of Satellite Transition Uncertainty:**
   - Instead of hiding the +9.15 cm upward step offset across the 2017–2018 gap between GRACE and GRACE-FO, the analysis reports Northwest water loss across three models: single-satellite GRACE-1 era (-1.56 cm/yr), full continuous fit (-1.25 cm/yr), and step-adjusted fit (-1.81 cm/yr).

---

## 3. Current Latest Findings (Verified Numbers)

### A. Regional Total Water Storage (TWS) Trends (2002–2026)

| Region | Divisions Covered | Full Record Trend (2002–2026) | 95% Confidence Interval | Volume Lost per Year | Statistical Verdict (FDR $q$) |
|---|---|:---:|:---:|:---:|---|
| **Northwest (NW)** | Rajshahi, Rangpur | **-1.25 cm/yr** | [-1.50, -1.02] cm/yr | **-0.39 km³/yr** (~9.5 km³ total) | **Significant decrease** ($q < 0.0001$) |
| **Northeast (NE)** | Sylhet, Mymensingh | **-0.56 cm/yr** | [-0.70, -0.42] cm/yr | **-0.12 km³/yr** | **Significant decrease** ($q < 0.0001$) |
| **Central** | Dhaka | **-0.47 cm/yr** | [-0.62, -0.34] cm/yr | **-0.08 km³/yr** | **Significant decrease** ($q < 0.0001$) |
| **Southwest (SW)** | Khulna, Barishal | **-0.05 cm/yr** | [-0.20, +0.10] cm/yr | -0.01 km³/yr | **No detectable trend** ($q = 0.8968$) |
| **Southeast (SE)** | Chattogram | **-0.05 cm/yr** | [-0.17, +0.06] cm/yr | -0.01 km³/yr | **No detectable trend** ($q = 0.8968$) |
| **National** | All 8 Divisions | **-0.51 cm/yr** | [-0.66, -0.38] cm/yr | **-0.63 km³/yr** | **Significant decrease** ($q < 0.0001$) |

*Note on the Northwest across eras:* During the single-satellite GRACE-1 baseline (2002–2017), Northwest storage declined at **-1.56 cm/yr** ([-1.96, -1.17] cm/yr, -0.49 km³/yr). Depending on how the 2017–2018 satellite gap is modeled, the 24-year Northwest decline ranges from **-1.81 to -1.25 cm/yr**.

### B. Rainfall Trends (GPM IMERG V07B, 2002–2025)
- **Long-term rainfall is stable:** Over 24 years, national rainfall averages **2,366 mm/year** with a non-significant trend of **+2.04 mm/yr** (95% CI: [-7.70, +12.45] mm/yr, $p = 0.64$, `No detectable trend`).
- **Northwest rainfall is stable:** The Northwest averages **1,954 mm/year** with a non-significant trend of **-1.91 mm/yr** (95% CI: [-11.04, +4.48] mm/yr, $p = 0.54$, `No detectable trend`).
- **Daily extreme rainfall shows no long-term trend:** Annual maximum 1-day rainfall (`Rx1day`), 5-day rainfall (`Rx5day`), and heavy rain days ($\ge 50\text{ mm}$) show `No detectable trend` across all regions.

### C. Soil Moisture vs. Deeper Subsurface Loss (Northwest)
- Across the two independent NASA GLDAS models (**Noah 2.1** and **VIC 2.1**), top-2-meter soil moisture ($\Delta\text{SMS}$) in the Northwest changed by only **[-0.12, -0.10] cm/yr** over 2002–2026 (and **[+0.05, +0.20] cm/yr** during 2018–2026).
- Subtracting soil moisture from GRACE Total Water Storage leaves a subsurface residual (`groundwater + surface water + model error residual`) declining at **[-1.12, -1.11] cm/yr** over the full 24-year record (and **[-1.92, -1.70] cm/yr** during 2018–2026).
- **Conclusion:** Nearly 90% of the water loss in the Northwest is happening below the root zone (or in unmodeled surface water), not from topsoil drying.

---

## 4. New Impacts Found on Research

1. **Northern Water Loss Is Not Driven by Decreasing Rainfall:**
   - Because GPM IMERG shows no multi-decadal decline in rainfall across the Northwest, Northeast, or Central regions, long-term water storage loss is occurring even though annual monsoon rainfall remains stable.
2. **Scale of Human and Agricultural Exposure:**
   - By combining MODIS cropland maps and SEDAC population grids, the research shows that **108.5 million people (63.9% of Bangladesh's population)** live in the three regions experiencing significant long-term water storage loss:
     - **Northwest:** 38.81 million people; **74.2% of land is intensive cropland** (the highest in the country).
     - **Central (Dhaka):** 45.64 million people; **56.4% cropland** (compounded by heavy urban/industrial water demand).
     - **Northeast:** 24.05 million people; **58.6% cropland**.
3. **Why Major Floods Do Not Fix Long-Term Depletion:**
   - Across 22 monsoon seasons, seasonal water storage rebounds by an average of **54.0 cm** nationally, capturing roughly **32.6%** of monsoon rainfall ($\Delta\text{TWS} / P_{\text{monsoon}}$).
   - During extreme flood years (2004, 2007, 2017, 2020, 2022), total water storage spikes sharply (+33 cm in 2004; +41 cm in 2007; +28 cm in 2020), but the excess water drains out through rivers within 3 to 4 months.
   - In extreme deluge years like 2020, the storage response ratio drops to **27.5%** because once surface soil is saturated, extra floodwater runs off into rivers instead of soaking into deeper aquifers.

---

## 5. Current Limitations

1. **Coarse Spatial Resolution (~300 km):**
   - GRACE/GRACE-FO satellites measure regional gravity changes over ~300 km footprints. They cannot show water table drops at the district, upazila, or village level.
2. **Cannot Separate Groundwater from Surface Water Alone:**
   - Subtracting GLDAS soil moisture from GRACE leaves `groundwater + surface water + model error residual`. Without local observation wells (piezometers) or river gauge data, satellite gravity data alone cannot separate deep aquifer water from rivers, haors, and ponds.
3. **No Local Pumping or Irrigation Records Yet:**
   - While the 74.2% cropland coverage in the Northwest matches the geography of dry-season Boro rice farming, the repository does not yet include local tubewell pumping logs or irrigation statistics from BADC or BMDA.
4. **Satellite Gap Step Uncertainty (2017–2018):**
   - The 11-month gap between GRACE and GRACE-FO has a +9.15 cm step offset in the Northwest of unknown origin, creating a range of uncertainty (-1.81 to -1.25 cm/yr) across the 24-year record.
5. **Short-Window Detection Limits:**
   - In short 6-to-8-year windows (`grace_fo_era` 2018–2026 and `recent_2020` 2020–2026), statistical noise requires a trend of at least **0.98 to 2.34 cm/yr** to be detected with 80% power. Therefore, non-significant results in short recent windows mean the window is too short to be certain, not that water loss has stopped.
6. **IMERG Data Latency:**
   - NASA GPM IMERG Final Run V07B currently ends in **September 2025**, leaving a 10-month gap at the end of the GRACE-FO record (which runs through July 2026).

---

## 6. Alignment with Mam's Feedback & Future Working Directions

### How Leon's Work Mapped to Your Options A, B, C, and D

Mam noted that **Options A, B, C, and D are all good ideas**, that **external datasets are allowed with proper links and references**, and that **water management, agricultural planning, flood/rainwater management, and drinking water capacity** can all be connected—provided we scope what is realistic within our limited time.

Here is where the project now stands against Options A, B, C, and D:

| Mentor Brief Option | Current Status After Leon's Commits | What Was Done vs. What Remains |
|---|:---:|---|
| **Option A:** Isolate groundwater using soil moisture data | **Completed (Satellite/Model Level)** | Completed using NASA GLDAS Noah 2.1 & VIC 2.1 across 2002–2026 (`outputs/v3/gldas_split/`). Proved topsoil moisture is not the cause of the loss. |
| **Option B:** Connect water loss to dry-season farming | **Partially Completed** | Added MODIS `MCD12Q1` cropland fraction (74.2% in NW) and dry-season vs. monsoon trend splits (`outputs/v3/exposure/`). Still needs local Boro rice irrigation/pumping data (BBS/BADC). |
| **Option C:** Measure how rain refills the ground & flood behavior | **Completed (Satellite/Model Level)** | Added 22-year monsoon storage response ratios ($\Delta\text{TWS} / P_{\text{monsoon}}$, averaging 32.6%) and 5 historical flood recovery analyses (`outputs/v3/extremes/`). |
| **Option D:** Compare with local well data (BWDB) & build a practical planner dashboard | **Not Started (Next Priority)** | All current data is satellite/model-based. No BWDB/BADC well data has been added yet, and the interactive dashboard (`index.html` / `demo.html`) has not yet been updated with the v3 findings. |

---

### Recommended Next Steps (Action Plan for Limited Time)

Since Leon's commits have already built the satellite foundation for **Options A, B, and C**, we do not need to spend more time downloading or calibrating new NASA satellite datasets. Instead, we should use our remaining time to complete **Option D** and directly address Mam's feedback on **water management, flood/rainwater harvesting, agricultural planning, and drinking water capacity**:

#### Step 1: Add Cited Local Bangladesh Reference Data (Option D + Option B) — *1 to 2 Days*
Mam confirmed we can use non-NASA datasets if we keep clear links and references. We should integrate:
1. **BWDB / BADC Groundwater Well Benchmarks:** Use published Bangladesh Water Development Board (BWDB) groundwater table depth records (or published district-level hydrographs from Shamsudduha et al. / BWDB reports with source links) for Rajshahi, Rangpur, and Dhaka to compare directly against our GLDAS residual storage curves.
2. **BBS / BADC Boro Irrigation Statistics:** Add a small reference table of division-level Boro rice irrigated area and deep/shallow tubewell counts (from Bangladesh Bureau of Statistics Yearbook) with citations to anchor Option B.

#### Step 2: Frame the Practical Water Management & Drinking Water Module — *1 to 2 Days*
Using the existing v3 flood and recharge numbers (`outputs/v3/extremes/` and `outputs/v3/full_record/seasonal_recharge_24yr.csv`), translate our findings into concrete water management metrics requested by Mam:
1. **Floodwater & Rainwater Harvesting Potential (NW & Central):**
   - Our data shows that ~67% of monsoon rainfall and massive flood pulses (+28 to +41 cm in major flood years) quickly drain away as surface runoff because topsoil saturates.
   - Calculate simple, practical estimates for **Managed Aquifer Recharge (MAR)**, pond/canal re-excavation (such as in the Barind Tract), and rainwater harvesting needed to offset the **0.39 km³/year** deficit in the Northwest and **0.08 km³/year** deficit in Central (Dhaka).
2. **Agricultural Planning (Crop Switching & Irrigation Efficiency):**
   - Show how reducing dry-season Boro groundwater demand in the Northwest (74.2% cropland) by switching a percentage of area to lower-water crops (wheat, maize, pulses) or adopting Alternate Wetting and Drying (AWD) irrigation can reduce the -1.25 cm/yr storage loss.
3. **Drinking Water Capacity & Safe Water Supply:**
   - Connect the dry-season storage drop in the Northwest (Barind) and Central (Dhaka) to seasonal hand-tubewell failure (when water tables drop below suction limits in March–May) and show how storing monsoon rainwater/floodwater supports year-round drinking water capacity.

#### Step 3: Update the Interactive Planner Dashboard (`index.html`) — *2 Days*
- Update the existing web dashboard (`index.html` / `demo.html`) so local planners and judges can view:
  1. The 24-year regional water storage trends and 3-way Northwest sensitivity range.
  2. The GPM IMERG vs. NASA POWER comparison (showing why rainfall is stable).
  3. The GLDAS soil moisture vs. subsurface residual split.
  4. An interactive **"Water Management & Recharge Calculator"** tab covering flood/rainwater capture, agricultural crop water savings, and drinking water buffer capacity by region.
