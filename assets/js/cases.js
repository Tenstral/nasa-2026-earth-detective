/**
 * NASA Space Apps 2026 - Trend Detective
 * assets/js/cases.js
 * =====================================
 * Pre-configured interactive case studies for guided investigation.
 */

window.ED = window.ED || {};

window.ED.cases = [
  {
    id: "case-1",
    badge: "Case File #1",
    title: "Where Is the Northwest's Water Going?",
    tagline: "Water Storage vs. Rainfall, Barind Tract",
    domain: "Water & Food Security",
    question: "Is Northwest Bangladesh losing water storage because monsoon rainfall is failing, or is storage dropping while rainfall shows no detectable trend?",
    config: {
      variable: "grace_tws",
      overlayVariable: "imerg_precip",
      region: "NW",
      startYear: 2002,
      endYear: 2026,
      season: "annual",
      deseasonalize: true
    },
    prompt: "Total Water Storage (blue line) drops (-1.25 cm/yr, p < 0.0001), while GPM IMERG satellite rainfall (orange dashed) shows no detectable trend (-1.91 mm/yr, p = 0.54). What does that suggest?",
    takeaway: "Water storage in Bangladesh's main grain-producing region is falling without a drop in rainfall, consistent with dry-season irrigation pumping for Boro rice across 74.2% of cropland."
  },
  {
    id: "case-2",
    badge: "Case File #2 • Benchmark",
    title: "Is 8 Years Enough?",
    tagline: "Time Window Length & Detection Limits",
    domain: "Statistical Power & Time Series",
    question: "Does the GRACE-FO satellite mission (2018–2026) prove that Northwest water storage has stopped declining?",
    config: {
      variable: "grace_tws",
      overlayVariable: null,
      region: "NW",
      startYear: 2018,
      endYear: 2026,
      season: "annual",
      deseasonalize: true
    },
    prompt: "In this 8-year window, p = 0.0549, just above 0.05, so the verdict is 'No detectable trend'. Widen the start year back to 2002 to see the verdict change to 'Significant Trend' (p < 0.0001).",
    takeaway: "Dr. Acker notes: 'If p > 0.05, that does not mean a trend does not exist; sometimes a longer time series is all that is needed.' At 8 years, a steep slope is needed to stand out from noise; over 24 years, the -1.25 cm/yr decline is clear."
  },
  {
    id: "case-3",
    badge: "Case File #3 • Verification",
    title: "The Reanalysis Trap",
    tagline: "Model Artifact vs. Satellite Radar",
    domain: "Observational Audit",
    question: "Why did earlier climate models show Bangladesh rainfall rising while satellite radars showed steady monsoons?",
    config: {
      variable: "power_precip",
      overlayVariable: "imerg_precip",
      region: "National",
      startYear: 2002,
      endYear: 2026,
      season: "annual",
      deseasonalize: true
    },
    prompt: "Compare NASA POWER (model reanalysis) with GPM IMERG (satellite radar/microwave). Around 2015, POWER shows a step jump that IMERG does not.",
    takeaway: "NASA POWER MERRA-2 changed observing inputs around 2015, introducing a step artifact. Check model reanalyses against direct satellite measurements before claiming climate shifts."
  },
  {
    id: "case-4",
    badge: "Case File #4",
    title: "Soil or Deeper?",
    tagline: "Root-Zone Soil vs. Subsurface Residual",
    domain: "Hydrological Modeling",
    question: "Does root-zone soil drying explain the regional water loss, or is the drop below the root zone?",
    config: {
      variable: "subsurface_residual",
      overlayVariable: "noah_sms_anom",
      region: "NW",
      startYear: 2002,
      endYear: 2026,
      season: "annual",
      deseasonalize: true
    },
    prompt: "GLDAS Noah models moisture in the top 2 meters of soil (orange). Total satellite water storage falls much faster, leaving a downward slope in the subsurface residual.",
    takeaway: "Root-zone soil moisture (0–2 m) accounts for only a small share of total storage loss. Most of the deficit appears in the partitioned subsurface residual ('groundwater + surface water + model error residual')."
  },
  {
    id: "case-5",
    badge: "Case File #5",
    title: "Is Dhaka's Air Getting Hazier?",
    tagline: "MODIS Aqua vs. AERONET Photometer",
    domain: "Atmospheric Aerosols",
    question: "Are aerosol levels (smoke, dust, and haze) over Dhaka rising when comparing satellite data with ground sensors?",
    config: {
      variable: "modis_aod",
      overlayVariable: "aeronet_aod",
      region: "Central",
      startYear: 2012,
      endYear: 2024,
      season: "annual",
      deseasonalize: true
    },
    prompt: "Compare NASA MODIS Aqua satellite data (blue) with Dhaka University AERONET ground photometer readings (orange dashed, 2012–2024). Widen the window to 2002–2026 to check the long-term slope.",
    takeaway: "Both sensors capture winter smog peaks (> 1.2 AOD) from brick kilns and stagnant air. Across 2002–2026, satellite AOD shows a significant upward slope (+0.0115 AOD/yr, p < 0.0001), matching Dr. James Acker's MODIS Aqua AOD case study."
  },
  {
    id: "case-6",
    badge: "Case File #6",
    title: "Are Downpours Getting Stronger?",
    tagline: "Extreme 1-Day Rainfall (Rx1day)",
    domain: "Climate Extremes",
    question: "Even if total rainfall has no detectable trend, are single-day heavy storms getting stronger?",
    config: {
      variable: "extreme_rx1day",
      overlayVariable: null,
      region: "National",
      startYear: 2003,
      endYear: 2024,
      season: "annual",
      deseasonalize: false
    },
    prompt: "Annual 1-day maximum rainfall swings from 50 mm up to > 115 mm in flood years (2004, 2007, 2017, 2020, 2022). Check whether a long-term trend is detectable.",
    takeaway: "Extreme downpours vary widely from year to year, so 22 annual points fall below the detection threshold (p > 0.05). High-variance extremes need longer baselines."
  },
  {
    id: "case-7",
    badge: "Case File #7",
    title: "Is Dhaka's Air Getting Dirtier?",
    tagline: "OMI NO₂ vs. MODIS AOD",
    domain: "Atmospheric Composition & Trace Gases",
    question: "Does satellite monitoring show rising nitrogen dioxide (NO₂) over Dhaka from vehicles and kilns, and how does it compare with aerosol haze?",
    config: {
      variable: "omi_no2",
      overlayVariable: "modis_aod",
      region: "Central",
      startYear: 2004,
      endYear: 2026,
      season: "annual",
      deseasonalize: true
    },
    prompt: "Watch how tropospheric NO₂ (blue) tracks fuel combustion, traffic, and brick kilns over Central Bangladesh alongside aerosol optical depth (orange dashed), especially during winter inversions.",
    takeaway: "OMI tropospheric NO₂ traces high-temperature combustion from traffic, brick kilns, and diesel generators. Central Bangladesh shows elevated NO₂ trapped under winter thermal inversions alongside regional aerosol haze."
  }
];
