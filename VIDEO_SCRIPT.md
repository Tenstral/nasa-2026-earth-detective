# Bengal Hydro Detective: Video Scripts

**Project:** Bengal Hydro Detective  
**Challenge:** NASA Space Apps Challenge 2026 — *Be An Earth System Trend Detective!*  
**Team:** Tenstral (East West University, Bangladesh)  
**Live Platform:** [tenstral-nasa26.pages.dev](https://tenstral-nasa26.pages.dev)  
**Status:** All findings PRELIMINARY

---

# Part 1: Official 240-Second Video Presentation Script

*Target duration: Exactly 240 seconds (4:00). Timed for local judging presentation.*

---

### [0:00 – 0:30] Segment 1: The Hook & Research Question
**Visual:** Split screen showing contrasting satellite imagery: dry, cracked terraces in the Northwest (Rajshahi/Rangpur) on the left, and expansive monsoon inundation across the Northeast Haor basin (Sylhet/Sunamganj) on the right.  
**Speaker 1:**  
"Across Bangladesh, ground reports present a striking contradiction. In the northwest, agricultural wells run dry, suction tubewells fail, and water tables drop during the dry season. Meanwhile, in the northeast, communities face massive monsoon inundation and early flash floods. Both regions exist under the exact same South Asian monsoon system.  
As NASA Earth System Trend Detectives, we asked: Where is Bangladesh's water going? Do rainfall and total water storage trends diverge across regions, and are those differences statistically detectable? To answer this, we built Bengal Hydro Detective."

---

### [0:30 – 1:00] Segment 2: Dual Earth Observations & Physical Partitioning
**Visual:** Transition to 3D satellite visualization: NASA GRACE/GRACE-FO twin satellites orbiting Earth, transitioning to GPM IMERG rainfall radar swaths, followed by GLDAS soil layers.  
**Speaker 2:**  
"To investigate rigorously, we pair two independent NASA observational platforms.  
For precipitation, we use NASA’s Global Precipitation Measurement IMERG V07B, spanning January 2002 to September 2025 at fine tenth-degree resolution.  
For total water storage, we use CSR GRACE and GRACE-FO RL0603 Mascons from April 2002 to July 2026. GRACE is the only platform capable of sensing vertically integrated mass anomalies—including deep subsurface water—at a three-hundred-kilometer footprint.  
To separate unsaturated topsoil from deep storage, we incorporate independent NASA GLDAS Noah and VIC land surface models, quarantining models that assimilate GRACE to prevent circular reasoning."

---

### [1:00 – 1:30] Segment 3: Calibrated Statistical Trend Engine
**Visual:** Screen recording of the STL decomposition animation stripping seasonal waveforms, followed by regression lines with confidence envelopes.  
**Speaker 3:**  
"In Bangladesh, powerful annual monsoon swings can easily mask subtle multi-decadal trends. Standard linear regression often mistakes seasonal cycles for secular change.  
We address this through a three-tier statistical protocol. First, we remove the cyclical monsoon amplitude. Second, we estimate robust rates of change using the Theil-Sen slope estimator. Third, we evaluate statistical significance using Calibrated Effective Sample Size Mann-Kendall tests with autoregressive pre-whitening and red-noise null validation.  
To prevent false discoveries, we enforce Benjamini-Hochberg False Discovery Rate control across families of 36 tests per window across four temporal frameworks: the full 24-year record, the GRACE era, the GRACE-FO era, and recent sensitivity windows."

---

### [1:30 – 2:00] Segment 4: Empirical Findings Across 5 Macro-Regions
**Visual:** Animated vector map of Bangladesh highlighting regional trends with confidence interval cards and trend trajectories.  
**Speaker 4:**  
"Our full 24-year analysis reveals significant regional divergence.  
In the Northwest, regional-mean total water storage is in significant decline at minus 1.25 centimeters per year, with a 95% confidence interval of minus 1.50 to minus 1.02 centimeters per year, losing approximately 0.39 cubic kilometers of water annually.  
The Northeast also declines significantly at minus 0.56 centimeters per year, and Central Bangladesh at minus 0.47 centimeters per year. Nationally, storage declines at minus 0.51 centimeters per year, or about 0.63 cubic kilometers per year.  
In contrast, the Southwest and Southeast show minus 0.05 centimeters per year, with no detectable trend.  
Crucially, GPM IMERG rainfall shows no detectable trend across any region in the country. In the Northwest, rainfall changes at minus 1.9 millimeters per year, but with a wide confidence interval from minus 11 to plus 4.5 millimeters per year."

---

### [2:00 – 2:30] Segment 5: Storage Partitioning, Exposure & Seasonal Baseline
**Visual:** Stacked area chart showing GLDAS soil moisture versus subsurface residual, overlaid with GPWv4 population density and MODIS cropland maps.  
**Speaker 1:**  
"What is driving this water loss? NASA GLDAS soil moisture modeling shows that topsoil drying accounts for only a minor fraction of the decline—between minus 0.12 and minus 0.10 centimeters per year, or about 8 to 10 percent. The remaining minus 1.12 centimeters per year is an unpartitioned residual in deep subsurface and surface storage.  
This storage depletion directly affects human systems. Approximately 108.5 million people—nearly 64 percent of Bangladesh’s population—live in regions experiencing significant storage decline, including the Northwest where 74.2 percent of land is intensively cultivated cropland.  
Furthermore, our seasonal analysis shows the annual storage swing remains consistent at 49 to 58 centimeters across all regions. The decline is not an expanding seasonal drop, but a downward shift in the long-term baseline."

---

### [2:30 – 3:00] Segment 6: Calibrated Between-Region Comparisons
**Visual:** Pairwise difference matrix and confidence intervals for regional slope comparisons.  
**Speaker 2:**  
"To confirm that regions truly diverge, we executed calibrated paired difference tests across all ten regional pairs.  
We find that the Northwest declines about 1.2 centimeters per year faster than the Southwest and Southeast, with non-overlapping confidence intervals. Northeast and Central decline about 0.5 centimeters per year faster than the southern regions. Southwest and Southeast are statistically indistinguishable, and no rainfall pair differs anywhere in Bangladesh.  
In accordance with scientific integrity, we report effect sizes and confidence intervals without exact p-values, because our circular-shift placebo checks show that pairwise p-values are overconfident."

---

### [3:00 – 3:30] Segment 7: Methodological Limitations & Epistemic Humility
**Visual:** Schematic showing satellite footprint, inter-satellite gap, and limitations checklist banner.  
**Speaker 3:**  
"A hallmark of our investigation is explicit scientific humility.  
First, GRACE integrates mass over footprints of several hundred kilometers. These are regional satellite series, not direct measurements of local water tables or individual village tubewells.  
Second, adjacent regions share signal boundaries, so spatial smoothing occurs.  
Third, a positive 9.15 centimeter step offset exists between the GRACE and GRACE-FO satellite missions. Depending on how this transition step is handled, the Northwest full-record slope spans minus 1.81 to minus 1.25 centimeters per year.  
Fourth, our satellite results have not yet been validated against in-situ well records from the Bangladesh Water Development Board.  
Finally, while the pattern of storage decline in the absence of rainfall trends is consistent with intensive dry-season agricultural water extraction, this satellite data alone does not prove causal attribution."

---

### [3:30 – 4:00] Segment 8: Detection Limits & The Interactive Decision Hub
**Visual:** Live walkthrough of the responsive web platform at `tenstral-nasa26.pages.dev`, showing the 24-year timeline scrubber, multi-sensor studio, and bilingual summary panels.  
**Speaker 4:**  
"Understanding detection limits is essential: 'no detectable trend' does not mean 'no change'. High natural rainfall variability widens confidence intervals, requiring multi-decadal records to detect trends. While the full 24-year Northwest minimum detectable slope is 0.32 centimeters per year, the threshold expands to 2.34 centimeters per year for recent six-year windows.  
We deployed these complete findings to our public decision-support hub at `tenstral-nasa26.pages.dev`. Stakeholders can scrub through 24 years of monthly observations, inspect multi-model partitions, and access bilingual stakeholder summaries in English and Bangla.  
We are Team Tenstral from East West University. Thank you."

---

# Part 2: Official 30-Second Global Judging Demo Pitch

*Target duration: Exactly 30 seconds. Fast-paced, high-impact summary for global screening.*

**[0:00 – 0:08] The Problem & Datasets:**  
"Under the same South Asian monsoon, is Bangladesh drying out or drowning? Using 24 years of NASA GRACE satellite gravity, GPM IMERG rainfall, and GLDAS land models, Bengal Hydro Detective evaluated multi-decadal water storage trajectories across Bangladesh."

**[0:08 – 0:20] The Core Findings:**  
"We discover that while satellite rainfall exhibits no detectable trend nationwide, total water storage declines significantly in the Northwest at minus 1.25 centimeters per year, and nationally at minus 0.51 centimeters per year, exposing 108.5 million people. Topsoil moisture explains less than 10 percent, leaving deep subsurface depletion as the dominant deficit."

**[0:20 – 0:30] Rigor & Impact:**  
"With calibrated false discovery rate control, step-offset modeling, and zero hand-typed statistics, explore our live 24-year decision hub at `tenstral-nasa26.pages.dev`. We are Team Tenstral."

---

# Recording & Video Production Checklist

- [ ] **Exact Word Limits:** Adhere strictly to the verbatim script timing (240s local, 30s global).
- [ ] **Wording Rules Compliance:** Verify complete compliance with project neutrality standards (use "total water storage" and "consistent with"; zero causal claims).
- [ ] **Screen Captures:** Use live captures of `tenstral-nasa26.pages.dev` showing the interactive map, 24-year timeline scrubber, and multi-model GLDAS charts.
- [ ] **Credit Visuals:** Ensure all NASA, JAXA, DLR, and GFZ data credits are visibly displayed on slides.
- [ ] **Privacy & Consent:** Confirm no minor faces appear in footage; display team credentials clearly.
