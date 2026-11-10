/**
 * NASA Space Apps 2026 - Trend Detective
 * assets/js/cases.js
 * =====================================
 * Pre-configured interactive case studies for guided investigation.
 * Each case file defines:
 *   - Title & subtitle
 *   - The Earth system mystery (question to solve)
 *   - Pre-filled workbench state (variable, region, time window, season, overlay)
 *   - Step-by-step detective prompts
 *   - Scientific takeaway & Dr. Acker alignment notes
 */

window.ED = window.ED || {};

window.ED.cases = [
  {
    id: "case-1",
    badge: "Case File #1",
    title: "Where Is the Northwest's Water Going?",
    tagline: "Total Water Storage vs. Satellite Rainfall in the Barind Tract",
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
    prompt: "Notice that Total Water Storage (blue line) plummets significantly (-1.25 cm/yr, p < 0.0001), while GPM IMERG satellite rainfall (orange dashed) shows no detectable trend (-1.91 mm/yr, p = 0.54). What does this tell you?",
    takeaway: "Water storage in Bangladesh's primary agricultural breadbasket is depleting without a corresponding drop in precipitation. This pattern is consistent with intensive irrigation abstraction for dry-season Boro rice cultivation across 74.2% of the region's cropland."
  },
  {
    id: "case-2",
    badge: "Case File #2 • Challenge Benchmark",
    title: "Is 8 Years Enough?",
    tagline: "Dr. James Acker's Core Lesson: Time Window Length & Detection Limits",
    domain: "Statistical Power & Time Series",
    question: "Does the GRACE-FO single-instrument satellite mission (2018–2026) prove that Northwest water storage has stopped declining?",
    config: {
      variable: "grace_tws",
      overlayVariable: null,
      region: "NW",
      startYear: 2018,
      endYear: 2026,
      season: "annual",
      deseasonalize: true
    },
    prompt: "In this 8-year window, p = 0.0549—just above the 0.05 threshold! The verdict is 'No detectable trend'. Now widen the start year back to 2002 and watch the verdict transform to 'Significant Trend' (p < 0.0001).",
    takeaway: "Dr. Acker notes: 'If p > 0.05, that does not mean a trend does not exist—sometimes a longer time series is all that is needed.' At 8 years, statistical power requires a steep slope to beat random noise. Over 24 years, the steady decline of -1.25 cm/yr is overwhelmingly significant."
  },
  {
    id: "case-3",
    badge: "Case File #3 • Data Verification",
    title: "The Reanalysis Trap",
    tagline: "Atmospheric Model Artifact vs. Satellite Radar Observations",
    domain: "Observational Audit",
    question: "Why did earlier climate models report that Bangladesh rainfall was surging, while satellite radars showed steady monsoon cycles?",
    config: {
      variable: "power_precip",
      overlayVariable: "imerg_precip",
      region: "National",
      startYear: 2002,
      endYear: 2026,
      season: "annual",
      deseasonalize: true
    },
    prompt: "Compare NASA POWER (atmospheric model reanalysis) against GPM IMERG (satellite radar/microwave). Look around 2015: POWER exhibits an abrupt upward step jump that IMERG does not see.",
    takeaway: "Always audit your data sources! NASA POWER MERRA-2 underwent observing system transitions around 2015 that introduced an artificial step artifact. Trend detectives must verify model reanalyses against physical satellite observations before claiming climate shifts."
  },
  {
    id: "case-4",
    badge: "Case File #4",
    title: "Soil or Deeper?",
    tagline: "Partitioning Root-Zone Moisture vs. Subsurface Residual",
    domain: "Hydrological Modeling",
    question: "Can topsoil drying explain the regional water decline, or does the loss reside in the deep subsurface?",
    config: {
      variable: "subsurface_residual",
      overlayVariable: "noah_sms_anom",
      region: "NW",
      startYear: 2002,
      endYear: 2026,
      season: "annual",
      deseasonalize: true
    },
    prompt: "GLDAS Noah simulates moisture in the top 2 meters of soil (orange). Total satellite water storage drops much faster, leaving a pronounced downward trend in the partitioned subsurface residual.",
    takeaway: "Root-zone soil moisture (0–2 m) explains only a minor fraction of the total gravimetric storage loss. The deficit is concentrated in the deep subsurface residual ('groundwater + surface water + model error residual')."
  },
  {
    id: "case-5",
    badge: "Case File #5",
    title: "Is Dhaka's Air Getting Hazier?",
    tagline: "NASA AERONET Ground Sun Photometer vs. Satellite Skies",
    domain: "Atmospheric Aerosols",
    question: "Are atmospheric aerosol levels (smoke, dust, and particulate haze) over Dhaka increasing over time?",
    config: {
      variable: "aod_550",
      overlayVariable: null,
      region: "National",
      startYear: 2012,
      endYear: 2024,
      season: "annual",
      deseasonalize: true
    },
    prompt: "Examine NASA AERONET ground-truth sun photometer measurements at Dhaka University (Level 1.5 cloud-cleared). Notice the positive slope in deseasonalized AOD (+0.012/year, p = 0.014).",
    takeaway: "Aerosol Optical Depth (AOD) shows an upward trend over central Dhaka across the 12-year ground monitoring record. Winter smog (DJF) regularly exceeds 1.1–1.3 AOD, driven by seasonal brick kiln operations and regional meteorological stagnation."
  },
  {
    id: "case-6",
    badge: "Case File #6",
    title: "Are Downpours Getting Stronger?",
    tagline: "ETCCDI Extreme 1-Day Downpours (Rx1day)",
    domain: "Climate Extremes",
    question: "Even if total rainfall is unchanged, are single-day extreme downpours becoming more intense?",
    config: {
      variable: "extreme_rx1day",
      overlayVariable: null,
      region: "National",
      startYear: 2003,
      endYear: 2024,
      season: "annual",
      deseasonalize: false
    },
    prompt: "Annual maximum 1-day rainfall fluctuates wildly from 50 mm up to > 115 mm in catastrophic flood years (2004, 2007, 2017, 2020, 2022). Test whether a secular trend has emerged.",
    takeaway: "Extreme downpours exhibit intense year-to-year volatility, but the 22-year record falls below the statistical detection threshold for a secular trend (p > 0.05). Trend detectives learn that high-variance extremes require longer observation baselines."
  }
];
