window.ED = window.ED || {};
window.ED.catalog = {
  "variables": [
    {
      "id": "grace_tws",
      "name": "Total Water Storage Anomaly (TWS)",
      "domain": "Water & Gravity",
      "sensor": "CSR GRACE / GRACE-FO RL06.3 Mascons",
      "unit": "cm",
      "unit_description": "Centimeters of equivalent water height (anomaly vs. 2004\u20132009 baseline)",
      "spatial_footprint": "~300 km mascon resolution (regional aggregate)",
      "temporal_range": "2002-04 to 2026-07 (monthly)",
      "definition": "Measures total changes in all terrestrial water storage\u2014deep and shallow groundwater, soil moisture, surface water bodies, and wetlands\u2014by detecting minute changes in Earth's gravitational pull.",
      "caveats": "Coarse spatial resolution (~300 km). Administrative division estimates share neighboring mascons and are descriptive only. Shaded 11-month observation gap (July 2017 to May 2018) separates the two satellite missions.",
      "supports_divisions": true,
      "has_gap": true,
      "can_deseasonalize": true,
      "kind": "mean"
    },
    {
      "id": "imerg_precip",
      "name": "Satellite Precipitation (GPM IMERG)",
      "domain": "Rainfall & Storms",
      "sensor": "GPM IMERG V07B Final Run",
      "unit": "mm/month",
      "unit_description": "Millimeters of rainfall per month",
      "spatial_footprint": "0.1\u00b0 (~10 km) satellite radar & passive microwave",
      "temporal_range": "2002-01 to 2025-09 (monthly)",
      "definition": "NASA's premier multi-satellite precipitation estimate combining spaceborne dual-frequency precipitation radar, passive microwave constellations, and ground rain-gauge calibration.",
      "caveats": "Satellite microwave algorithms can underestimate light drizzle or saturate in intense mountain-front convective storms.",
      "supports_divisions": true,
      "has_gap": false,
      "can_deseasonalize": true,
      "kind": "sum"
    },
    {
      "id": "power_precip",
      "name": "Reanalysis Precipitation (NASA POWER)",
      "domain": "Rainfall & Storms (Atmospheric Model)",
      "sensor": "NASA POWER MERRA-2 PRECTOTCORR",
      "unit": "mm/month",
      "unit_description": "Millimeters of rainfall per month (reanalysis model)",
      "spatial_footprint": "0.5\u00b0 \u00d7 0.625\u00b0 global atmospheric model grid",
      "temporal_range": "2002-01 to 2026-07 (monthly)",
      "definition": "Global reanalysis rainfall produced by NASA's Goddard Earth Observing System (GEOS) atmospheric model with data assimilation.",
      "caveats": "\u26a0\ufe0f Critical Sensor Break Trap: Contains a known artificial step shift around 2015 caused by observing system transitions in the underlying MERRA-2 model. Used in Case File #3 to teach data verification.",
      "supports_divisions": true,
      "has_gap": false,
      "can_deseasonalize": true,
      "kind": "sum"
    },
    {
      "id": "noah_sms_anom",
      "name": "Root-Zone Soil Moisture Anomaly (Noah 2.1)",
      "domain": "Land Surface & Agriculture",
      "sensor": "GLDAS Noah 2.1 Land Surface Model",
      "unit": "cm",
      "unit_description": "Centimeters of equivalent water in the top 0\u20132.0 m soil column",
      "spatial_footprint": "0.25\u00b0 (~25 km) land surface simulation",
      "temporal_range": "2002-04 to 2026-07 (monthly)",
      "definition": "Simulates water stored in the upper 2 meters of soil (the root zone) where vegetation and crops absorb water.",
      "caveats": "Does not simulate deep unconfined or confined aquifers below 2 meters depth. Computed for macro-regions only.",
      "supports_divisions": false,
      "has_gap": false,
      "can_deseasonalize": true,
      "kind": "mean"
    },
    {
      "id": "vic_sms_anom",
      "name": "Root-Zone Soil Moisture Anomaly (VIC 2.1)",
      "domain": "Land Surface & Agriculture",
      "sensor": "GLDAS VIC 2.1 Hydrological Model",
      "unit": "cm",
      "unit_description": "Centimeters of equivalent water in the top 0\u20132.0 m soil column",
      "spatial_footprint": "0.25\u00b0 (~25 km) land surface simulation",
      "temporal_range": "2002-04 to 2026-07 (monthly)",
      "definition": "Independent land surface model utilizing variable infiltration capacity to simulate moisture storage in the plant root zone.",
      "caveats": "Independent physics from Noah; provides an ensemble model envelope for soil moisture uncertainty.",
      "supports_divisions": false,
      "has_gap": false,
      "can_deseasonalize": true,
      "kind": "mean"
    },
    {
      "id": "subsurface_residual",
      "name": "Partitioned Subsurface Residual",
      "domain": "Partitioned Subsurface Storage",
      "sensor": "CSR GRACE TWS \u2212 GLDAS \u0394SMS (Noah/VIC Midpoint)",
      "unit": "cm",
      "unit_description": "Centimeters of equivalent water thickness (subsurface residual)",
      "spatial_footprint": "Macro-regional aggregate (NW, NE, Central, SW, SE, National)",
      "temporal_range": "2002-04 to 2026-07 (monthly)",
      "definition": "The storage anomaly remaining after subtracting simulated root-zone soil moisture from total satellite water storage. Strictly labeled: 'groundwater + surface water + model error residual'.",
      "caveats": "Because satellite gravimetry measures the total water column, subtracting soil moisture isolates deep storage changes plus any unmodeled surface water bodies and land surface model errors.",
      "supports_divisions": false,
      "has_gap": true,
      "can_deseasonalize": true,
      "kind": "mean"
    },
    {
      "id": "extreme_rx1day",
      "name": "Extreme 1-Day Downpour (Rx1day)",
      "domain": "Climate Extremes",
      "sensor": "GPM IMERG Daily Precipitation Derivative",
      "unit": "mm/day",
      "unit_description": "Maximum 1-day rainfall recorded in the calendar year",
      "spatial_footprint": "Macro-regional aggregate",
      "temporal_range": "2003 to 2024 (annual)",
      "definition": "World Meteorological Organization standard index for the single heaviest daily deluge of the year.",
      "caveats": "Annual series (one observation per calendar year). Tests whether peak storm intensity is shifting.",
      "supports_divisions": false,
      "has_gap": false,
      "can_deseasonalize": false,
      "kind": "mean"
    },
    {
      "id": "extreme_days_ge_50",
      "name": "Heavy Torrent Days (Rainfall \u2265 50 mm)",
      "domain": "Climate Extremes",
      "sensor": "GPM IMERG Daily Precipitation Derivative",
      "unit": "days/year",
      "unit_description": "Number of days with regional rainfall \u2265 50 mm/day",
      "spatial_footprint": "Macro-regional aggregate",
      "temporal_range": "2003 to 2024 (annual)",
      "definition": "Counts the frequency of severe torrential rainfall events capable of triggering flash floods and waterlogging.",
      "caveats": "Annual series (one observation per year).",
      "supports_divisions": false,
      "has_gap": false,
      "can_deseasonalize": false,
      "kind": "mean"
    },
    {
      "id": "aod_550",
      "name": "Aerosol Optical Depth 550 nm (AOD)",
      "domain": "Atmosphere & Air Quality",
      "sensor": "NASA AERONET Ground Station + MODIS Aqua Satellite",
      "unit": "dimensionless AOD",
      "unit_description": "Optical thickness at 550 nm (higher values indicate hazier, more polluted air)",
      "spatial_footprint": "Ground station point (AERONET Dhaka University) & 1.0\u00b0 satellite grid (MODIS)",
      "temporal_range": "2012 to 2024 (AERONET); 2002 to present (MODIS)",
      "definition": "Measures how much sunlight is prevented from reaching the ground by airborne particles such as seasonal winter smog, brick kiln emissions, and biomass burning.",
      "caveats": "Ground station measures directly above Dhaka University. Satellite MODIS observations are averaged over the 1\u00b0 capital bounding box.",
      "supports_divisions": false,
      "has_gap": false,
      "can_deseasonalize": true,
      "kind": "mean"
    }
  ],
  "regions": [
    {
      "id": "NW",
      "name": "Northwest (Rajshahi + Rangpur)",
      "population_2020_m": 38.81,
      "population_share_pct": 22.9,
      "cropland_pct": 74.2,
      "total_agricultural_pct": 82.7,
      "tws_slope_cm_yr": -1.255,
      "tws_ci_95": "[-1.50, -1.02]",
      "tws_verdict": "Significant",
      "context": "Primary national food basket; dominant Boro rice cultivation dependent on intensive irrigation abstraction."
    },
    {
      "id": "NE",
      "name": "Northeast (Sylhet + Mymensingh)",
      "population_2020_m": 24.05,
      "population_share_pct": 14.2,
      "cropland_pct": 58.6,
      "total_agricultural_pct": 69.8,
      "tws_slope_cm_yr": -0.555,
      "tws_ci_95": "[-0.70, -0.42]",
      "tws_verdict": "Significant",
      "context": "Extensive haor seasonal wetlands, tea estates, and rice floodplains; highly exposed to flash floods."
    },
    {
      "id": "Central",
      "name": "Central (Dhaka)",
      "population_2020_m": 45.64,
      "population_share_pct": 26.9,
      "cropland_pct": 56.4,
      "total_agricultural_pct": 66.2,
      "tws_slope_cm_yr": -0.473,
      "tws_ci_95": "[-0.62, -0.34]",
      "tws_verdict": "Significant",
      "context": "Highest population density; mega-urban industrial water demand combined with intensive peripheral agriculture."
    },
    {
      "id": "SW",
      "name": "Southwest (Khulna + Barishal)",
      "population_2020_m": 27.14,
      "population_share_pct": 16.0,
      "cropland_pct": 48.7,
      "total_agricultural_pct": 56.1,
      "tws_slope_cm_yr": -0.047,
      "tws_ci_95": "[-0.20, +0.10]",
      "tws_verdict": "No detectable trend",
      "context": "Coastal delta interface; Sundarbans mangrove forest (~40% of Khulna) and polder aquaculture/salinity constraints."
    },
    {
      "id": "SE",
      "name": "Southeast (Chattogram)",
      "population_2020_m": 34.18,
      "population_share_pct": 20.1,
      "cropland_pct": 32.1,
      "total_agricultural_pct": 46.7,
      "tws_slope_cm_yr": -0.052,
      "tws_ci_95": "[-0.17, +0.06]",
      "tws_verdict": "No detectable trend",
      "context": "Chittagong Hill Tracts forest topography, port economy, and coastal plains."
    },
    {
      "id": "National",
      "name": "National Composite (Bangladesh)",
      "population_2020_m": 169.83,
      "population_share_pct": 100.0,
      "cropland_pct": 57.8,
      "total_agricultural_pct": 68.1,
      "tws_slope_cm_yr": -0.512,
      "tws_ci_95": "[-0.66, -0.38]",
      "tws_verdict": "Significant",
      "context": "National aggregate across the entire Bengal delta territory."
    }
  ],
  "divisions": [
    {
      "id": "Barishal",
      "name": "Barishal Division",
      "region": "SW"
    },
    {
      "id": "Chattogram",
      "name": "Chattogram Division",
      "region": "SE"
    },
    {
      "id": "Dhaka",
      "name": "Dhaka Division",
      "region": "Central"
    },
    {
      "id": "Khulna",
      "name": "Khulna Division",
      "region": "SW"
    },
    {
      "id": "Mymensingh",
      "name": "Mymensingh Division",
      "region": "NE"
    },
    {
      "id": "Rajshahi",
      "name": "Rajshahi Division",
      "region": "NW"
    },
    {
      "id": "Rangpur",
      "name": "Rangpur Division",
      "region": "NW"
    },
    {
      "id": "Sylhet",
      "name": "Sylhet Division",
      "region": "NE"
    }
  ],
  "floodEvents": [
    {
      "year": 2004,
      "flood_period": "July\u2013August 2004",
      "classification": "Catastrophic Multi-Basin Flood (Brahmaputra & Ganges)",
      "inundation_area_pct": "~38%",
      "districts_affected": "39",
      "national_monsoon_precip_mm": 2020.9,
      "national_monsoon_anom_pct": 21.3,
      "post_monsoon_peak_cm": 33.1,
      "source": "FFWC/BWDB Annual Flood Report 2004, Executive Summary, p. 1",
      "url": "http://www.ffwc.gov.bd/images/annual04.pdf",
      "notes": "Concurrently intense Brahmaputra and Ganges monsoonal flood waves combined with sustained localized rainfall."
    },
    {
      "year": 2007,
      "flood_period": "July\u2013September 2007",
      "classification": "Prolonged Double-Peak Monsoon Flood",
      "inundation_area_pct": "~32% to 42%",
      "districts_affected": "40",
      "national_monsoon_precip_mm": 1996.2,
      "national_monsoon_anom_pct": 19.9,
      "post_monsoon_peak_cm": 40.99,
      "source": "FFWC/BWDB Annual Flood Report 2007, Executive Summary, p. 1\u20132",
      "url": "http://www.ffwc.gov.bd/images/annual07.pdf",
      "notes": "Two successive peak flood waves in late July and early September associated with extreme Himalayan transboundary inflow."
    },
    {
      "year": 2017,
      "flood_period": "April (Haor) & August 2017",
      "classification": "Devastating Pre-Monsoon Flash Flood + August Monsoon Flood",
      "inundation_area_pct": ">70% Haor basins (April); ~42% country (August)",
      "districts_affected": "6 Haor districts (April); 31 districts (August)",
      "national_monsoon_precip_mm": 1878.6,
      "national_monsoon_anom_pct": 12.8,
      "post_monsoon_peak_cm": null,
      "source": "FFWC/BWDB Annual Flood Report 2017, Executive Summary, p. 1\u20133",
      "url": "http://www.ffwc.gov.bd/images/annual17.pdf",
      "notes": "Extreme April rainfall in Meghalaya/Cherrapunji (>1,000 mm in 10 days) submerging standing Boro crops in Sylhet/Sunamganj haors; followed by heavy August northern riverine floods."
    },
    {
      "year": 2020,
      "flood_period": "June\u2013August 2020",
      "classification": "Historical Long-Duration Flood (~40+ days)",
      "inundation_area_pct": "~30% to 33%",
      "districts_affected": "39",
      "national_monsoon_precip_mm": 1809.2,
      "national_monsoon_anom_pct": 8.6,
      "post_monsoon_peak_cm": 28.39,
      "source": "FFWC/BWDB Annual Flood Report 2020, Executive Summary, p. 1\u20133",
      "url": "http://www.ffwc.gov.bd/images/annual20.pdf",
      "notes": "Record-sustained monsoonal precipitation across the upstream Brahmaputra basin (longest duration above danger level since 1998)."
    },
    {
      "year": 2022,
      "flood_period": "May\u2013June 2022",
      "classification": "Centennial Record Flash Flood (Meghna/Surma-Kushiyara Basin)",
      "inundation_area_pct": "Local: 94% Sunamganj, 84% Sylhet (~22\u201326% national)",
      "districts_affected": "18",
      "national_monsoon_precip_mm": 1363.6,
      "national_monsoon_anom_pct": -18.1,
      "post_monsoon_peak_cm": 16.43,
      "source": "FFWC/BWDB Annual Flood Report 2022, Executive Summary / Flash Flood Chapter, p. 1\u20135",
      "url": "http://www.ffwc.gov.bd/images/annual22.pdf",
      "notes": "Unprecedented extreme rainfall in Meghalaya/Cherrapunji (>972 mm in 24h on 17 June) causing catastrophic rapid flash inundation across Surma-Kushiyara river system."
    }
  ],
  "gapPeriod": {
    "start": "2017-07",
    "end": "2018-05",
    "label": "Inter-Satellite Mission Gap (11 months)"
  },
  "canonicalWindows": [
    {
      "id": "full_record",
      "label": "Full 24-Year Record",
      "start": "2002-04",
      "end": "2026-07"
    },
    {
      "id": "grace_era",
      "label": "GRACE-1 Baseline Era",
      "start": "2002-04",
      "end": "2017-06"
    },
    {
      "id": "grace_fo_era",
      "label": "GRACE-FO Single Era",
      "start": "2018-06",
      "end": "2026-07"
    },
    {
      "id": "recent_2020",
      "label": "Recent Overlap Era",
      "start": "2020-01",
      "end": "2026-07"
    }
  ],
  "seasons": [
    {
      "id": "annual",
      "label": "All Months (Deseasonalized)",
      "months": "1\u201312"
    },
    {
      "id": "monsoon",
      "label": "Monsoon Season (JJAS)",
      "months": "Jun\u2013Sep"
    },
    {
      "id": "winter",
      "label": "Winter / Dry Season (DJF)",
      "months": "Dec\u2013Feb"
    },
    {
      "id": "pre_monsoon",
      "label": "Pre-Monsoon Season (MAM)",
      "months": "Mar\u2013May"
    },
    {
      "id": "post_monsoon",
      "label": "Post-Monsoon Season (ON)",
      "months": "Oct\u2013Nov"
    }
  ]
};
