# Register of Unaccessed, Screened, or Excluded Literature Studies

**Project:** Bengal Hydro Detective — NASA Space Apps Challenge 2026
**Team:** Tenstral

---

### Audit Criteria for Benchmark Inclusion
To maintain audit-grade scientific integrity, studies must satisfy four mandatory criteria:
1. Direct inspection of the original published text or DOI source (no memory-based or citation-network citations).
2. Spatial boundary explicitly covering Bangladesh territory or documented transboundary basins.
3. Quantitative reporting of water storage rates ($\Delta	ext{TWS}$ or $\Delta	ext{GWS}$) with stated units and analytical timeframes.
4. Documented observational or model dataset provenance.

### Screened and Excluded Candidates:

| Candidate Citation | Screening Status | Exclusion / Qualification Reason |
|---|---|---|
| **Rodell et al. (2018)**, *Nature* 557, 651–659 | **Retained as Context Only** | Study evaluates Region 13 (>1,000,000 km2 transboundary polygon). National Bangladesh rate cannot be disaggregated without spatial weight grids. Retained in benchmark as macro-regional context; excluded from direct quantitative difference testing. |
| **Ahmed et al. (2025)**, *arXiv:2503.22771* | **Retained as Methodological Benchmark** | Currently an un-peer-reviewed preprint. Evaluates machine learning downscaling of GLDAS GWS rather than secular trend estimation. Retained with explicit qualification; excluded from baseline rate benchmarking. |
| **Global GRACE Hydrology Compendiums** (e.g., Scanlon et al., 2018; Tapley et al., 2019) | **Excluded** | Reported statistics aggregate the entire Ganges-Brahmaputra-Meghna basin (1.7 million km2) across India, China, Nepal, Bhutan, and Bangladesh without disaggregated Bangladeshi administrative boundaries. |
| **Local In-Situ Piezometer Studies without Volumetric Scaling** | **Excluded** | Studies reporting only point groundwater head variations (meters below ground surface) without specific yield ($S_y$) or spatial kriging cannot be converted to equivalent water thickness (cm/yr or km3/yr) without speculative assumptions. |

### Notes on Unit Conversion Protocol:
- Converted rates in equivalent water thickness ($	ext{cm/yr}$) from volumetric rates ($	ext{km}^3/	ext{yr}$) follow:
  $$	ext{Rate (cm/yr)} = rac{	ext{Rate (km}^3	ext{/yr)} 	imes 10^5}{	ext{Documented Area (km}^2	ext{)}}$$
- No cell has been computed where the author's spatial surface area was unstated or ambiguously defined.
