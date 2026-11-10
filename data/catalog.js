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
      "caveats": "Does not simulate deep unconfined or confined \"aquifers\" below 2 meters depth. Computed for macro-regions only.",
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
      "id": "modis_aod",
      "name": "Aerosol Optical Depth (MODIS Aqua Satellite)",
      "domain": "Atmosphere & Air Quality",
      "sensor": "NASA Aqua MODIS MYD08_M3 Level 3 (550 nm)",
      "unit": "dimensionless AOD",
      "unit_description": "Optical thickness at 550 nm (higher values indicate hazier, more polluted air)",
      "spatial_footprint": "1.0\u00b0 (~100 km) satellite grid, area-averaged over Dhaka or National box",
      "temporal_range": "2002-07 to 2026-07 (monthly)",
      "definition": "Satellite-observed aerosol optical thickness capturing seasonal dust, smoke plumes, and winter smog across regional skies.",
      "caveats": "Cloud obscuration in peak monsoon may reduce valid satellite retrievals. 1\u00b0 spatial resolution.",
      "supports_divisions": false,
      "has_gap": false,
      "can_deseasonalize": true,
      "kind": "mean"
    },
    {
      "id": "aeronet_aod",
      "name": "Aerosol Optical Depth (NASA AERONET Ground)",
      "domain": "Atmosphere & Air Quality",
      "sensor": "NASA AERONET Ground Sun Photometer (Dhaka University, Level 1.5)",
      "unit": "dimensionless AOD",
      "unit_description": "Optical thickness at 500/550 nm (direct ground-truth sun photometer)",
      "spatial_footprint": "Ground station point measurement at Dhaka University (23.728\u00b0N, 90.398\u00b0E)",
      "temporal_range": "2012-06 to 2024-07 (monthly)",
      "definition": "Direct ground-truth measurement of sunlight attenuation by airborne smoke, dust, and particulate pollution over central Dhaka.",
      "caveats": "Point measurement at Dhaka University; captures intense urban core emissions. Requires at least 3 valid observation days per month.",
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
  "stakeholderDirectives": {
    "NW": {
      "region_name": "Northwest Depletion Corridor (Rajshahi & Rangpur)",
      "satellite_metric": "-1.25 cm/year TWS decline (-0.39 km\u00b3/year). Rainfall shows no detectable trend (-1.91 mm/year).",
      "historical_context": "Depletion is consistent with intensive dry-season Boro rice cultivation on Pleistocene clay terraces that impede natural monsoon recharge.",
      "mandate": "BMDA must enforce smart-card volumetric pricing and halt unmetered deep tubewell permits. Expand surface water irrigation from Padma/Teesta rivers by 10% by 2030.",
      "farmer_dos": "Adopt Alternate Wetting and Drying (AWD) using PVC pipes (cuts water use by 15\u201330%). Plant short-duration drought-escaping T. Aman (BRRI dhan56/57) before July 24. Shift to winter crops (BARI chhola-5, BARI sarisha-10).",
      "farmer_donts": "Do not maintain continuous standing water in Boro paddies. Do not plant three-crop continuous cereal rotations. Do not delay T. Aman transplanting past July 24.",
      "citizen_action": "Convert upland plots to drought-hardy orchards (mango, jujube, dragon fruit). Install rooftop rainwater harvesting and farm recharge ponds."
    },
    "NE": {
      "region_name": "Northeast Haor Basin (Sylhet & Mymensingh)",
      "satellite_metric": "-0.56 cm/year TWS decline. Mean annual dry-season drawdown is massive (58.48 cm).",
      "historical_context": "Choked river corridors drain summer flash floods rapidly into the Bay of Bengal, leaving subsurface storage unrefilled for the dry season.",
      "mandate": "BWDB must construct and maintain engineered submersible embankments against early April flash floods. Dredge rivers and raise rural homestead mounds.",
      "farmer_dos": "Plant flash-flood-escaping Boro varieties (BRRI dhan110, 28, 58) for early April harvest. In floodplains, plant submergence-tolerant Aman (BRRI dhan51/52).",
      "farmer_donts": "Do not plant long-duration Boro (BRRI dhan29) in deep Haor bowls where April floods destroy unharvested crops. Avoid unlined earthen canals.",
      "citizen_action": "Construct floating agricultural beds (dhap) using water hyacinth. Raise pond embankments and install nylon netting to prevent fish loss."
    },
    "Central": {
      "region_name": "Central Megacity & Terrace (Dhaka Division)",
      "satellite_metric": "-0.47 cm/year TWS decline. Highest monsoon storage response ratio (42.2%).",
      "historical_context": "Relentless municipal and industrial groundwater extraction from the \"Dupi Tila\" aquifer formation beneath impervious Madhupur clay creates a deep metropolitan cone of depression.",
      "mandate": "Enforce Zero-Liquid-Discharge (ZLD) for Gazipur/Narayanganj textile factories. Mandate rooftop Managed Aquifer Recharge (\"MAR\") in municipal building codes.",
      "farmer_dos": "Practice contour mulching and intercrop pineapple with ginger and turmeric on the Madhupur Tract. Cultivate disease-resistant BRRI dhan114.",
      "farmer_donts": "Do not irrigate peri-urban vegetables with untreated industrial effluent from the Turag or Buriganga rivers. Do not clear-cut hillocks.",
      "citizen_action": "Establish urban rooftop gardens with rainwater harvesting and greywater recycling to cool buildings and reduce urban runoff."
    },
    "SW": {
      "region_name": "Southwest Estuarine Delta (Khulna & Barishal)",
      "satellite_metric": "No detectable trend in bulk mass (-0.05 cm/year), but severe dry-season river and soil salinity intrusion.",
      "historical_context": "Reduced dry-season freshwater river flow drives a brackish salinity wedge into shallow subsurface waters and polders, idling agricultural land in winter.",
      "mandate": "Operate coastal polder sluice gates dynamically to trap fresh monsoon river water internally before February salinity spikes. Enforce agro-ecological zoning.",
      "farmer_dos": "Cultivate salt-tolerant Boro rice (BINA dhan10, BINA dhan8, BRRI dhan67). Grow saline-tolerant sweet potato (BARI misti alu-6) on residual moisture.",
      "farmer_donts": "Do not plant salt-sensitive BRRI dhan28 in coastal mauzas. Do not breach polder embankments for brackish tiger shrimp (bagda) monoculture.",
      "citizen_action": "Construct raised bed-and-trench (Sorjan) systems to block capillary salt rise for vegetable cultivation. Maintain Pond Sand Filters for drinking water."
    },
    "SE": {
      "region_name": "Southeast Hill Tracts (Chattogram & CHT)",
      "satellite_metric": "No detectable trend in bulk mass (-0.05 cm/year), but the lowest monsoon retention in the country (only 26%).",
      "historical_context": "Steep Tertiary hill slopes cause 74% of heavy monsoon rain to sheet off instantly as rapid runoff, drying up natural hill springs by winter.",
      "mandate": "Provide land tenure security and micro-credit for Sloping Agricultural Land Technology (SALT). Legally protect Village Common Forests (VCFs).",
      "farmer_dos": "Implement SALT contour hedgerows using nitrogen-fixing legumes every 4\u20136 meters to diffuse runoff. Cultivate flash-flood-tolerant BRRI dhan110.",
      "farmer_donts": "Do not practice short-fallow slash-and-burn or till root crops vertically on steep slopes. Do not expand tobacco farming in river valleys.",
      "citizen_action": "Establish multistrata perennial fruit orchards. Protect headwater bamboo inside Village Common Forests to revive natural springs (chhara)."
    },
    "National": {
      "region_name": "National Macro-Regional Directives Summary",
      "satellite_metric": "-0.51 cm/year national TWS decline; 108.5M people live in depleting northern and central regions.",
      "historical_context": "National water management requires a regionalized approach: Northwest replenishment, Northeast flash flood escape, Central industrial water recycling, and Southern salinity barrier management.",
      "mandate": "Implement the Bangladesh Delta Plan 2100 with regional differentiation rather than uniform national water policies.",
      "farmer_dos": "Match crop choices to regional hydrological regimes: drought-tolerant crops in NW, flash-flood-escaping varieties in NE, and salt-tolerant cultivars in SW.",
      "farmer_donts": "Do not treat water resources as homogeneous across the country; avoid applying uniform dry-season pumping standards nationwide.",
      "citizen_action": "Support community water monitoring, local watershed protection, and rooftop rainwater harvesting across all divisions."
    }
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
