# Exposure Layer: Methods, Data Provenance, and Limitations Note

**Project:** Bengal Hydro Detective — NASA Space Apps Challenge 2026
**Team:** Tenstral
**Status:** PRELIMINARY

---

### 1. Data Provenance and Attribution

1. **Human Population Count:**
   - **Product:** NASA SEDAC Gridded Population of the World, Version 4 (GPWv4), Revision 11.
   - **Year:** 2020 single-year benchmark (un-trended static exposure baseline).
   - **Adjustment:** Harmonized against the official Bangladesh Bureau of Statistics (BBS) 2022 Population and Housing Census Post-Enumeration Check (PEC) adjusted totals (national total: 169.83 million).

2. **Cropland and Agricultural Land Cover:**
   - **Product:** MODIS Land Cover Type Yearly Global 500m (`MCD12Q1` v061), primary annual classification.
   - **Classes Evaluated:** Primary Croplands (Class 12: lands covered with temporary crops followed by harvest and a bare soil period) and Cropland/Natural Vegetation Mosaic (Class 14: mosaics of small-scale cultivated land with natural forest/shrubland).

3. **Precipitation Coupling:**
   - **Product:** GPM IMERG V07B Final Run (`GPM_3IMERGM`, 2002–2025; decoupled from GRACE).
   - **Role:** Independent meteorological verification that storage depletion occurs without concurrent rainfall deficits.

4. **Spatial Aggregation:**
   - Geodesic zonal statistics calculated across administrative boundaries and aggregated into the 5 core hydro-climatic regions (NW, NE, Central, SW, SE) plus National.

---

### 2. Methodological Constraints and Limitations

1. **Resolution Mismatch and Spatial Scale Guardrails:**
   - GRACE and GRACE-FO satellite gravimetry has an effective native spatial resolution of roughly $300\text{ km} \times 300\text{ km}$ (~$90,000\text{ km}^2$).
   - Consequently, **exposure claims are valid ONLY at the regional level** (e.g. Northwest vs Southern delta). Storage verdicts cannot be disaggregated to individual upazilas, districts, or localized villages.

2. **No Population Trend Claims:**
   - Because population data is benchmarked to the static 2020/2022 census horizon, no claims are made regarding population growth trends or causal population-driven depletion velocities.

3. **MODIS Rice Paddy Classification Uncertainties:**
   - Optical satellite land cover sensors (like MODIS) can occasionally conflate flooded seasonal rice paddies with seasonal wetlands or inland water bodies during peak inundation periods.
   - Cropland percentages are reported as regional averages and contextual indicators of irrigation intensity rather than exact field-level cadastral surveys.
