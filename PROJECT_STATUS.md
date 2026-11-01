# Bengal Hydro Detective — Plain-Language Project Status & Findings Guide

**NASA Space Apps Challenge 2026 — Be an Earth System Trend Detective!**  
**Team:** Tenstral  
**Status:** PRELIMINARY — Subject to Peer Review and In-Situ Hydrometric Validation  
**Audience:** Non-statistician teammates, presenters, and reviewers  

---

## 1. What Is This Project and What Question Does It Answer?

Every summer, Bangladesh is submerged by enormous volumes of monsoon rainfall, nourishing rivers and occasionally causing catastrophic flooding. Yet farmers and local water managers in the northern agricultural heartland report that tubewells are running dry and water levels are dropping year after year. 

**This project answers a fundamental question:**  
> *Is Bangladesh genuinely losing water over the long term, and if so, how much, where is it happening, and is it caused by declining rainfall or human water use?*

To answer this without guessing, we built a reproducible scientific detection pipeline that audits **24 continuous years of NASA satellite observations** (April 2002 to July 2026). We combined:
1. **NASA/CSR GRACE and GRACE Follow-On satellite gravimetry:** Twin satellites that orbit Earth and literally weigh regional water mass from space, capturing all water combined—rivers, lakes, topsoil moisture, and deep underground aquifers.
2. **Satellite precipitation records:** GPM IMERG Final Run (radar/microwave satellite rainfall) and NASA POWER (reanalysis).
3. **NASA Land Surface Models (GLDAS Noah and VIC):** Computer simulations of how much water is held in the top 2 meters of soil.
4. **NASA Socioeconomic and Land Cover grids:** Mapping where people live and where irrigated crops grow.

---

## 2. Headline Findings by Region and Window

### A. The Geography of Water Loss (Where Is Water Changing?)
Water storage changes across Bangladesh are not uniform. The country is split into two distinct hydrological regimes:

1. **The Northwest Depletion Corridor (Rajshahi and Rangpur):**
   - The Northwest is the nation's primary water loss hotspot across all long-term evaluations.
   - **Full 24-Year Record (2002–2026):** Total water storage has declined at **-1.25 cm/year** (95% confidence interval: [-1.49, -1.01] cm/yr). That equals a net volumetric loss of **-0.39 billion cubic meters (km³) of water every year**. Over 24 years, this adds up to roughly **9.4 km³ of lost water** in this region alone.
   - **Historical Baseline (GRACE-1 era, 2002–2017):** Water storage declined at **-1.56 cm/year** ([-1.95, -1.15] cm/yr), or **-0.48 km³/year**.

2. **The Northeast and Central Regions (Dhaka, Sylhet, Mymensingh):**
   - **Central (Dhaka division):** Declining at **-0.47 cm/year** ([-0.62, -0.34] cm/yr, -0.08 km³/yr) over the full record.
   - **Northeast (Sylhet and Mymensingh):** Declining at **-0.56 cm/year** ([-0.70, -0.42] cm/yr, -0.12 km³/yr) over the full record.

3. **The Southern Delta (Khulna, Barishal, Chattogram):**
   - **Southwest:** **-0.05 cm/year** ([-0.17, +0.08] cm/yr)—mathematically indistinguishable from zero change.
   - **Southeast:** **-0.05 cm/year** ([-0.17, +0.06] cm/yr)—mathematically indistinguishable from zero change.
   - The south is buffered by massive tidal river networks, coastal mangrove wetlands (the Sundarbans), and less reliance on dry-season groundwater pumping.

4. **National Total (All Bangladesh Combined):**
   - Nationally, total water storage has declined at **-0.51 cm/year** ([-0.65, -0.37] cm/yr) over the full 24-year record, equal to **-0.63 km³ of lost water per year** across the country.

---

### B. The 3-Way Northwest Slope Transparency
Between the original GRACE satellites (which ended in June 2017) and the GRACE Follow-On satellites (which launched in June 2018), there was an 11-month gap with no satellite data. Because connecting two different satellites across a gap can be tricky, we report the Northwest trend three different ways so nothing is hidden:

| Method | Northwest TWS Slope | 95% Confidence Interval | What It Means |
|---|:---:|:---:|---|
| **1. Single Continuous Line** | **-1.25 cm/yr** | [-1.49, -1.01] cm/yr | Standard linear trend fit across the entire 24-year period (2002–2026). |
| **2. Step-Adjusted** | **-1.38 cm/yr** | [-1.63, -1.13] cm/yr | Adjusts for a +1.34 cm instrument calibration shift between the two satellite missions. |
| **3. Transition-Free (GRACE-1)** | **-1.56 cm/yr** | [-1.95, -1.15] cm/yr | The historical mission with zero satellite transition gaps (2002–2017). This is our most solid benchmark. |

*Takeaway:* No matter how you treat the satellite transition, the Northwest has lost water at a rate between **-1.25 and -1.56 cm every year**.

---

## 3. Which Findings Are Confirmed, Suggestive, or Below Detection Limit?

In scientific auditing, words like "significant" have strict mathematical meanings. To prevent false alarms, we applied a strict rule: a finding is only called **Significant** if it passes False Discovery Rate screening ($q < 0.05$) AND its 95% confidence interval completely excludes zero.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        EVIDENCE CERTAINTY TIERS                        │
├────────────────────────────────────────────────────────────────────────┤
│ 1. CONFIRMED SIGNIFICANT TRENDS (FDR q < 0.05 & CI Excludes Zero)      │
│    • Northwest Total Water Storage: Full record (-1.25 cm/yr, q<0.0001)│
│    • Northwest Total Water Storage: Historical era (-1.56 cm/yr)       │
│    • Northeast Total Water Storage: Full record (-0.56 cm/yr, q<0.0001)│
│    • Central Total Water Storage: Full record (-0.47 cm/yr, q<0.0001)  │
│    • National Total Water Storage: Full record (-0.51 cm/yr, q=0.00008)│
│    • National Total Water Storage: Historical era (-0.68 cm/yr)        │
├────────────────────────────────────────────────────────────────────────┤
│ 2. METHOD-DEPENDENT / SENSITIVITY FINDINGS                             │
│    • Northwest in recent_2020 (2020–2026): Point slope is -2.93 cm/yr. │
│      Raw p = 0.0107, but within-window FDR q = 0.0772 (fails standard).│
│      Different statistical tests disagree; labeled METHOD-DEPENDENT.   │
├────────────────────────────────────────────────────────────────────────┤
│ 3. BELOW DETECTION LIMIT / NO DETECTABLE TREND                         │
│    • Southwest and Southeast Total Water Storage across all windows.   │
│    • Northwest in grace_fo_era (2018–2026): slope is -1.67 cm/yr,      │
│      but confidence interval [-3.32, +0.06] spans zero. Short record   │
│      noise means this rate is currently below our detection limit.     │
│    • ALL regional precipitation trends (GPM IMERG): rainfall has no    │
│      detectable multi-decadal upward or downward trend anywhere.       │
│    • Extreme precipitation indices (Rx1day, Rx5day, heavy rain days).  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 4. The Rainfall Story: Data Artifact vs. Reality

### A. The NASA POWER Reanalysis Artifact
Earlier project drafts reported that Bangladesh rainfall was surging upward by +29 to +86 mm every year. When we audited the raw data, we discovered this was a **data artifact**:
- Around 2014–2015, NASA POWER's underlying atmospheric model (MERRA-2) underwent an abrupt upward jump of **+45% to +84%** across Bangladesh.
- In the Northwest, annual totals jumped from ~1,580 mm/year before 2015 to ~2,330 mm/year after 2018.
- This sudden step change created false, runaway positive rainfall trends. The exact cause in NASA's assimilation system remains unverified.

### B. Ground Truth with GPM IMERG (Stationary Rainfall)
When we replaced the reanalysis data with NASA's dedicated rainfall satellite system (**GPM IMERG V07B Final Run**), the phantom rainfall increase disappeared:
- Nationally, annual rainfall has changed by only **+2.04 mm/year** ($p = 0.57$, FDR $q = 0.9342$), which is completely flat within natural year-to-year swings.
- In the Northwest, annual rainfall slope is **-2.6 mm/year** ($p = 0.38$), also showing no detectable change.
- Multi-year national rainfall averages **2,366 mm/year**, closely matching the official Bangladesh Meteorological Department (BMD) 30-year normal of **2,428 mm/year**.
- *Important Timing Note:* GPM IMERG Final data currently ends in September 2025 due to standard NASA processing latency, truncating the final 10 months of our 2026 analysis window.

### C. Extreme Rainfall and Floods
We also examined daily rainfall extremes (the wettest single day of the year, the wettest 5 consecutive days, and the number of days with torrential rain $\ge 50$ mm):
- **Stationary Extremes:** None of these extreme rainfall indices show a detectable long-term trend across Bangladesh between 2003 and 2024.
- **Why Floods Don't Stop the Depletion:** We cross-checked catastrophic historical floods (2004, 2007, 2017, 2020, 2022) against satellite storage:
  - Floods create huge, temporary water spikes (water storage surged by +41 cm in 2007 and +33 cm in 2004).
  - However, because the ground is already saturated, floodwaters cannot soak deep into the ground. Instead, they rush across the surface into major rivers and drain into the Bay of Bengal within 3 to 4 months.
  - By the very next dry season (March–May), intensive irrigation pumping removes more water than the flood left behind, returning storage right back to its downward trajectory.

---

## 5. The Storage Budget: What Does GLDAS Show?

Satellite gravimetry measures total water, but it cannot see whether water was lost from the topsoil or from deep underground aquifers. To find out, we looked at NASA's **GLDAS Land Surface Models** (Noah 2.1 and VIC 2.1), which simulate the top 2 meters of soil moisture based on weather and vegetation:

1. **Independent Soil Moisture Is Stable:**
   - Both independent models (Noah and VIC) show that topsoil moisture has **no statistically significant long-term decline** in the Northwest (GRACE-FO slope range: **+0.05 to +0.20 cm/year**).
2. **The Residual Storage Deficit:**
   - When we subtract topsoil moisture and snow from total satellite storage ($\text{Residual} = \text{TWS} - \Delta\text{Soil Moisture} - \Delta\text{Snow}$), we isolate what is happening beneath the root zone.
   - We strictly label this quantity: `"groundwater + surface water + model error residual"`.
   - Across independent models, this residual declines at **-1.92 to -1.70 cm/year** during GRACE-FO, and **-1.12 to -1.11 cm/year** across the full 24-year record.
3. **What This Means Physically:**
   - Most of the water loss is **not accounted for by topsoil drying**. 
   - Because open-loop land surface models simulate rain and topsoil but do not simulate tubewells pumping water from deep underground, this residual pattern is **consistent with, not proof of**, human groundwater extraction for dry-season Boro rice irrigation.
   - *A Vital Methodological Clarification on CLSM 2.2:* A third model, GLDAS CLSM 2.2, is often cited in literature. However, CLSM 2.2 directly ingests (assimilates) GRACE satellite data. Using CLSM to explain GRACE would be circular reasoning. We report CLSM separately for context, but exclude it from the independent budget.

---

## 6. Honest Limitations & What Is Needed to Resolve Each

To uphold scientific integrity, here is what this study can and cannot prove:

| What We Observe | What It Cannot Prove | What Would Be Needed to Resolve It |
|---|---|---|
| **1. Regional Water Depletion** | Coarse resolution (~300 km) cannot pinpoint which specific upazila or municipal ward is losing water. | High-resolution satellite radar interferometry (InSAR) ground subsidence mapping. |
| **2. Residual Subsurface Loss** | Satellites measure mass, not borehole water levels; we cannot separate deep groundwater from surface water bodies and wetlands. | Direct integration of Bangladesh Water Development Board (BWDB) nationwide in-situ piezometer well hydrographs. |
| **3. Human Extraction Link** | We do not have direct monthly meter readings of agricultural well pumping across the Barind Tract. | Sub-district agricultural power consumption records and deep tubewell discharge logs from the Barind Multipurpose Development Authority (BMDA). |
| **4. Inter-Satellite Gap** | The 11-month transition (2017–2018) between GRACE and GRACE-FO creates minor step uncertainty. | Continuous multi-satellite airborne gravimetry bridging campaigns or hydrodynamic model assimilation. |
| **5. Rainfall Truncation** | High-quality GPM IMERG Final data currently ends in September 2025. | Updating the pipeline when NASA GES DISC releases late-2025 and 2026 Final Run granules. |

---

## 7. Deliverables & File Directory Guide

Use this guide to find exactly what you need for presentations, reports, or deep technical audits:

### A. Recommended for Presentations & Slide Decks
- `PROJECT_STATUS.md` *(this file)*: Complete plain-language project overview and master numbers.
- `README.md`: Formal project specification and workflow overview.
- `outputs/v3/full_record/fig1_full_record_tws_trends.png`: Clean 6-panel graph showing 24-year water storage trends for all regions with 95% confidence bands.
- `outputs/v3/exposure/fig_exposure_choropleth.png`: 2-panel map showing where 108.5 million people and 74% cropland overlap with the water depletion corridor.
- `outputs/v3/extremes/fig_imerg_extreme_indices_trends.png`: Visual evidence showing that daily extreme rainfall has remained stationary across 2002–2025.
- `outputs/v3/gldas_split/fig_storage_partition_multi_model.png`: 4-panel visual proof that topsoil moisture is steady while deep residual storage declines.

### B. Master Results Tables (For Spreadsheets & Citations)
- `outputs/v3/full_record/results_all_windows.csv`: Master statistical results file containing all 336 statistical tests across all 4 windows, 6 regions, and 8 divisions with FDR q-values.
- `outputs/v3/benchmark/benchmark_table.csv` & `.md`: Comparison of our rates against 6 published peer-reviewed studies.
- `outputs/v3/exposure/exposure_table.csv` & `.md`: Population and cropland exposure breakdown by region.
- `outputs/v3/extremes/imerg_extreme_indices_trends.csv` & `.md`: Exact trend numbers and confidence intervals for all extreme rainfall indices.
- `outputs/v3/gldas_split/gldas_multi_model_summary.csv` & `.md`: Complete multi-model soil moisture and residual storage numbers.

### C. Deep-Dive Audit Documentation (For Technical Inquiries)
- `NOTES.md`: Developer log detailing fixed parameters, calibration proofs, and before-and-after differences for all review findings.
- `outputs/v3/full_record/gap_calibration_report.json`: Monte Carlo simulation results proving that the ESS-Mann-Kendall test passes the 5% false-positive rate standard.
- `outputs/v3/full_record/three_way_slopes_and_transition.md`: Detailed math behind the 3-way Northwest slope estimation.
- `outputs/v3/imerg_vs_power/imerg_vs_power_summary.md`: Complete statistical breakdown of why NASA POWER was rejected and GPM IMERG was selected.
