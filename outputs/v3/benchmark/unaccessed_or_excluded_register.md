# Register of Unaccessed, Screened, or Excluded Literature Studies

**Project:** Bengal Hydro Detective — NASA Space Apps Challenge 2026  
**Team:** Tenstral  
**Status:** PRELIMINARY

---

### Audit Criteria for Benchmark Inclusion & Direct Comparability
To maintain audit-grade scientific integrity, studies are evaluated under four strict criteria:
1. **Direct inspection of source text:** Verified from original peer-reviewed publication or registered DOI (no memory-based or unverified secondhand citations).
2. **Spatial domain boundary:** Explicitly delineated for Bangladesh national boundaries or sub-national divisions/regions. Studies aggregating transboundary macro-regions without Bangladeshi area weights are classified as context only.
3. **Target hydrological variable:** Must report Total Water Storage ($\Delta\text{TWS}$) to be directly comparable to satellite gravimetry. Studies estimating isolated Groundwater Storage ($\Delta\text{GWS}$) via hydrologic model subtraction or in-situ piezometers are classified as variable-mismatched.
4. **Temporal window overlap:** Timeframe must correspond to evaluated satellite epochs (e.g., GRACE-1 era 2002–2017 or full 2002–2026 record). Shorter sub-windows are classified as period-mismatched.

**Comparability Standard:** A study is marked `Comparable: Yes` **only** when variable ($\Delta\text{TWS}$), study period, and geographic domain all match.

---

### Screened and Excluded Candidates Register

| Candidate Citation | Screening Classification | Detailed Exclusion / Qualification Justification |
|---|---|---|
| **Purdy et al. (2019)**, *Frontiers in Environmental Science* 7, 155 | **Comparable: Yes** | Evaluates $\Delta\text{TWS}$ across Bangladesh National and Northwest regions over 2002–2016. Variable, period, and domain correspond directly to our `grace_era` evaluation. |
| **Shamsudduha et al. (2012)**, *Water Resources Research* 48, W02508 | **Comparable: No (Context Only)** | Evaluates $\Delta\text{GWS}$ residual and in-situ borehole hydrographs over 2003–2007. Excluded from direct quantitative comparison due to variable mismatch (GWS vs. total water storage) and temporal restriction to early 5-year satellite window. |
| **Ouyang et al. (2024)**, *Remote Sensing* 16, 3715 | **Comparable: No (Context Only)** | Evaluates $\Delta\text{GWS}$ and InSAR land subsidence over 2015–2022. Excluded from direct quantitative comparison due to variable mismatch ($\Delta\text{GWS}$ vs. total water storage) and distinct 7-year evaluation sub-window. |
| **Shamsudduha & Taylor (2020)**, *Earth System Dynamics* 11, 755–774 | **Comparable: No (Context Only)** | Evaluates the transboundary Ganges–Brahmaputra Basin (Aquifer No. 24, ~1.2 million km²). Excluded from direct comparison due to spatial domain mismatch (macro-basin vs. Bangladesh territory) and variable mismatch ($\Delta\text{GWS}$). |
| **Ahmed et al. (2025)**, *arXiv:2503.22771* | **Comparable: No (Methodological Benchmark)** | Evaluates 2 km machine learning downscaled GLDAS GWS discharge rates. Excluded from direct comparison due to metric mismatch (localized discharge hotspots up to 25 cm/yr vs. regional-mean secular slope across 30,753 km²). |
| **Rodell et al. (2018)**, *Nature* 557, 651–659 | **Comparable: No (Macro Context)** | Evaluates Region 13 (>1,000,000 km² covering Eastern India, Bangladesh, and Myanmar). Excluded from direct quantitative comparison due to transboundary macro-region aggregation without disaggregated Bangladesh administrative boundary weighting. |
| **Global GRACE Compendiums** (e.g., Scanlon et al., 2018; Tapley et al., 2019) | **Excluded** | Reported values aggregate the entire Ganges–Brahmaputra–Meghna basin (1.7 million km²) across India, China, Nepal, Bhutan, and Bangladesh without disaggregated Bangladeshi administrative boundaries. |
| **Local In-Situ Piezometer Studies without Volumetric Scaling** | **Excluded** | Studies reporting only point groundwater head variations (meters below surface) without aquifer specific yield ($S_y$) or spatial kriging cannot be converted to equivalent water thickness (cm/yr or km³/yr) without speculative assumptions. |

---

### Notes on Conversion Protocol
- Volumetric rates ($\text{km}^3/\text{yr}$) to equivalent water thickness ($\text{cm/yr}$) follow:
  $$\text{Rate (cm/yr)} = \frac{\text{Rate (km}^3\text{/yr)} \times 10^5}{\text{Documented Area (km}^2\text{)}}$$
- No comparison is made where the author's spatial surface area was unstated or ambiguously defined.
