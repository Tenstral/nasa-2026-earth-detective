"""
v3/build_webapp_data.py
=======================
Compiles and serializes all primary datasets into structured JavaScript files
under data/ for zero-dependency client-side execution in the browser.

Outputs:
  - data/catalog.js          (Variable definitions, regions, divisions, flood events, presets)
  - data/map.js              (Cleaned SVG paths and division centroids)
  - data/series_regions.js   (Monthly time series for 5 macro-regions + National)
  - data/series_divisions.js (Monthly time series for 8 administrative divisions)
  - data/series_extremes.js  (Annual ETCCDI extreme precipitation indices)
  - data/series_aod.js       (AERONET ground truth and MODIS satellite AOD)
  - data/presets.js          (FDR q-values and benchmark verdicts for canonical annual windows)
"""

import json
import sys
from pathlib import Path
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from v3.build_dashboard import build_map_paths

DATA_DIR = REPO_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def sanitize(val, decimals=4):
    """Sanitizes floats, NaNs, and rounds decimals."""
    if val is None or pd.isna(val) or np.isneginf(val) or np.isposinf(val):
        return None
    try:
        return round(float(val), decimals)
    except Exception:
        return None


def export_map_js():
    geojson_path = REPO_ROOT / "bangladesh_divisions.geojson"
    svg_paths, div_centers = build_map_paths(geojson_path)

    region_divisions = {
        "NW": ["Rajshahi", "Rangpur"],
        "NE": ["Sylhet", "Mymensingh"],
        "Central": ["Dhaka"],
        "SW": ["Khulna", "Barishal"],
        "SE": ["Chattogram"],
    }

    division_to_region = {}
    for r, divs in region_divisions.items():
        for d in divs:
            division_to_region[d] = r

    payload = {
        "svgPaths": svg_paths,
        "divCenters": div_centers,
        "regionDivisions": region_divisions,
        "divisionToRegion": division_to_region,
    }

    out_file = DATA_DIR / "map.js"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"window.ED = window.ED || {{}};\nwindow.ED.map = {json.dumps(payload, indent=2)};\n")
    print(f"[OK] Exported {out_file} ({out_file.stat().st_size:,} bytes)")


def export_catalog_js():
    # Load flood events context
    floods_df = pd.read_csv(REPO_ROOT / "outputs/v3/extremes/flood_events_context.csv")
    flood_events = []
    for _, r in floods_df.iterrows():
        flood_events.append({
            "year": int(r["year"]),
            "flood_period": str(r["flood_period"]),
            "classification": str(r["ffwc_classification"]),
            "inundation_area_pct": str(r["inundation_area_pct"]),
            "districts_affected": str(r["districts_affected"]) if not pd.isna(r["districts_affected"]) else "",
            "national_monsoon_precip_mm": sanitize(r["national_monsoon_precip_mm"], 1),
            "national_monsoon_anom_pct": sanitize(r["national_monsoon_anom_pct"], 1),
            "post_monsoon_peak_cm": sanitize(r["post_monsoon_peak_cm"], 2),
            "source": str(r["source_document"]) if "source_document" in r and not pd.isna(r["source_document"]) else "",
            "url": str(r["source_url"]) if "source_url" in r and not pd.isna(r["source_url"]) else "",
            "notes": str(r["meteorological_driver"]) if "meteorological_driver" in r and not pd.isna(r["meteorological_driver"]) else ""
        })

    # Regions metadata from exposure table
    exp_df = pd.read_csv(REPO_ROOT / "outputs/v3/exposure/exposure_table.csv")
    regions = []
    for _, r in exp_df.iterrows():
        regions.append({
            "id": str(r["region"]),
            "name": {
                "NW": "Northwest (Rajshahi + Rangpur)",
                "NE": "Northeast (Sylhet + Mymensingh)",
                "Central": "Central (Dhaka)",
                "SW": "Southwest (Khulna + Barishal)",
                "SE": "Southeast (Chattogram)",
                "National": "National Composite (Bangladesh)"
            }.get(str(r["region"]), str(r["region"])),
            "population_2020_m": sanitize(r["pop_millions_2020"], 2),
            "pop_millions": sanitize(r["pop_millions_2020"], 2),
            "population_share_pct": sanitize(r["pop_share_pct"], 1),
            "cropland_pct": sanitize(r["cropland_pct_mcd12q1"], 1),
            "total_agricultural_pct": sanitize(r["total_agricultural_pct"], 1),
            "tws_slope_cm_yr": sanitize(r["tws_slope_cm_yr"], 3),
            "tws_ci_95": str(r["tws_ci_95"]),
            "tws_verdict": str(r["tws_verdict"]),
            "context": str(r["regional_context"])
        })

    divisions = [
        {"id": "Barishal", "name": "Barishal Division", "region": "SW", "population_2020_m": 9.33, "pop_millions": 9.33},
        {"id": "Chattogram", "name": "Chattogram Division", "region": "SE", "population_2020_m": 34.18, "pop_millions": 34.18},
        {"id": "Dhaka", "name": "Dhaka Division", "region": "Central", "population_2020_m": 45.64, "pop_millions": 45.64},
        {"id": "Khulna", "name": "Khulna Division", "region": "SW", "population_2020_m": 17.81, "pop_millions": 17.81},
        {"id": "Mymensingh", "name": "Mymensingh Division", "region": "NE", "population_2020_m": 12.64, "pop_millions": 12.64},
        {"id": "Rajshahi", "name": "Rajshahi Division", "region": "NW", "population_2020_m": 20.79, "pop_millions": 20.79},
        {"id": "Rangpur", "name": "Rangpur Division", "region": "NW", "population_2020_m": 18.02, "pop_millions": 18.02},
        {"id": "Sylhet", "name": "Sylhet Division", "region": "NE", "population_2020_m": 11.41, "pop_millions": 11.41},
    ]

    variables = [
        {
            "id": "grace_tws",
            "name": "Total Water Storage Anomaly (TWS)",
            "domain": "Water & Gravity",
            "sensor": "CSR GRACE / GRACE-FO RL06.3 Mascons",
            "unit": "cm",
            "unit_description": "Centimeters of equivalent water height (anomaly vs. 2004–2009 baseline)",
            "spatial_footprint": "~300 km mascon resolution (regional aggregate)",
            "temporal_range": "2002-04 to 2026-07 (monthly)",
            "definition": "Measures total changes in all terrestrial water storage—deep and shallow groundwater, soil moisture, surface water bodies, and wetlands—by detecting minute changes in Earth's gravitational pull.",
            "caveats": "Coarse spatial resolution (~300 km). Administrative division estimates share neighboring mascons and are descriptive only. Shaded 11-month observation gap (July 2017 to May 2018) separates the two satellite missions.",
            "supports_divisions": True,
            "has_gap": True,
            "can_deseasonalize": True,
            "kind": "mean"
        },
        {
            "id": "imerg_precip",
            "name": "Satellite Precipitation (GPM IMERG)",
            "domain": "Rainfall & Storms",
            "sensor": "GPM IMERG V07B Final Run",
            "unit": "mm/month",
            "unit_description": "Millimeters of rainfall per month",
            "spatial_footprint": "0.1° (~10 km) satellite radar & passive microwave",
            "temporal_range": "2002-01 to 2025-09 (monthly)",
            "definition": "NASA's premier multi-satellite precipitation estimate combining spaceborne dual-frequency precipitation radar, passive microwave constellations, and ground rain-gauge calibration.",
            "caveats": "Satellite microwave algorithms can underestimate light drizzle or saturate in intense mountain-front convective storms.",
            "supports_divisions": True,
            "has_gap": False,
            "can_deseasonalize": True,
            "kind": "sum"
        },
        {
            "id": "power_precip",
            "name": "Reanalysis Precipitation (NASA POWER)",
            "domain": "Rainfall & Storms (Atmospheric Model)",
            "sensor": "NASA POWER MERRA-2 PRECTOTCORR",
            "unit": "mm/month",
            "unit_description": "Millimeters of rainfall per month (reanalysis model)",
            "spatial_footprint": "0.5° × 0.625° global atmospheric model grid",
            "temporal_range": "2002-01 to 2026-07 (monthly)",
            "definition": "Global reanalysis rainfall produced by NASA's Goddard Earth Observing System (GEOS) atmospheric model with data assimilation.",
            "caveats": "⚠️ Critical Sensor Break Trap: Contains a known artificial step shift around 2015 caused by observing system transitions in the underlying MERRA-2 model. Used in Case File #3 to teach data verification.",
            "supports_divisions": True,
            "has_gap": False,
            "can_deseasonalize": True,
            "kind": "sum"
        },
        {
            "id": "noah_sms_anom",
            "name": "Root-Zone Soil Moisture Anomaly (Noah 2.1)",
            "domain": "Land Surface & Agriculture",
            "sensor": "GLDAS Noah 2.1 Land Surface Model",
            "unit": "cm",
            "unit_description": "Centimeters of equivalent water in the top 0–2.0 m soil column",
            "spatial_footprint": "0.25° (~25 km) land surface simulation",
            "temporal_range": "2002-04 to 2026-07 (monthly)",
            "definition": "Simulates water stored in the upper 2 meters of soil (the root zone) where vegetation and crops absorb water.",
            "caveats": "Does not simulate deep unconfined or confined \"aquifers\" below 2 meters depth. Computed for macro-regions only.",
            "supports_divisions": False,
            "has_gap": False,
            "can_deseasonalize": True,
            "kind": "mean"
        },
        {
            "id": "vic_sms_anom",
            "name": "Root-Zone Soil Moisture Anomaly (VIC 2.1)",
            "domain": "Land Surface & Agriculture",
            "sensor": "GLDAS VIC 2.1 Hydrological Model",
            "unit": "cm",
            "unit_description": "Centimeters of equivalent water in the top 0–2.0 m soil column",
            "spatial_footprint": "0.25° (~25 km) land surface simulation",
            "temporal_range": "2002-04 to 2026-07 (monthly)",
            "definition": "Independent land surface model utilizing variable infiltration capacity to simulate moisture storage in the plant root zone.",
            "caveats": "Independent physics from Noah; provides an ensemble model envelope for soil moisture uncertainty.",
            "supports_divisions": False,
            "has_gap": False,
            "can_deseasonalize": True,
            "kind": "mean"
        },
        {
            "id": "subsurface_residual",
            "name": "Partitioned Subsurface Residual",
            "domain": "Partitioned Subsurface Storage",
            "sensor": "CSR GRACE TWS − GLDAS ΔSMS (Noah/VIC Midpoint)",
            "unit": "cm",
            "unit_description": "Centimeters of equivalent water thickness (subsurface residual)",
            "spatial_footprint": "Macro-regional aggregate (NW, NE, Central, SW, SE, National)",
            "temporal_range": "2002-04 to 2026-07 (monthly)",
            "definition": "The storage anomaly remaining after subtracting simulated root-zone soil moisture from total satellite water storage. Strictly labeled: 'groundwater + surface water + model error residual'.",
            "caveats": "Because satellite gravimetry measures the total water column, subtracting soil moisture isolates deep storage changes plus any unmodeled surface water bodies and land surface model errors.",
            "supports_divisions": False,
            "has_gap": True,
            "can_deseasonalize": True,
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
            "supports_divisions": False,
            "has_gap": False,
            "can_deseasonalize": False,
            "kind": "mean"
        },
        {
            "id": "extreme_days_ge_50",
            "name": "Heavy Torrent Days (Rainfall ≥ 50 mm)",
            "domain": "Climate Extremes",
            "sensor": "GPM IMERG Daily Precipitation Derivative",
            "unit": "days/year",
            "unit_description": "Number of days with regional rainfall ≥ 50 mm/day",
            "spatial_footprint": "Macro-regional aggregate",
            "temporal_range": "2003 to 2024 (annual)",
            "definition": "Counts the frequency of severe torrential rainfall events capable of triggering flash floods and waterlogging.",
            "caveats": "Annual series (one observation per year).",
            "supports_divisions": False,
            "has_gap": False,
            "can_deseasonalize": False,
            "kind": "mean"
        },
        {
            "id": "modis_aod",
            "name": "Aerosol Optical Depth (MODIS Aqua Satellite)",
            "domain": "Atmosphere & Air Quality",
            "sensor": "NASA Aqua MODIS MYD08_M3 Level 3 (550 nm)",
            "unit": "dimensionless AOD",
            "unit_description": "Optical thickness at 550 nm (higher values indicate hazier, more polluted air)",
            "spatial_footprint": "1.0° (~100 km) satellite grid, area-averaged over Dhaka or National box",
            "temporal_range": "2002-07 to 2026-07 (monthly)",
            "definition": "Satellite-observed aerosol optical thickness capturing seasonal dust, smoke plumes, and winter smog across regional skies.",
            "caveats": "Cloud obscuration in peak monsoon may reduce valid satellite retrievals. 1° spatial resolution.",
            "supports_divisions": False,
            "has_gap": False,
            "can_deseasonalize": True,
            "kind": "mean"
        },
        {
            "id": "aeronet_aod",
            "name": "Aerosol Optical Depth (NASA AERONET Ground)",
            "domain": "Atmosphere & Air Quality",
            "sensor": "NASA AERONET Ground Sun Photometer (Dhaka University, Level 1.5)",
            "unit": "dimensionless AOD",
            "unit_description": "Optical thickness at 500/550 nm (direct ground-truth sun photometer)",
            "spatial_footprint": "Ground station point measurement at Dhaka University (23.728°N, 90.398°E)",
            "temporal_range": "2012-06 to 2024-07 (monthly)",
            "definition": "Direct ground-truth measurement of sunlight attenuation by airborne smoke, dust, and particulate pollution over central Dhaka.",
            "caveats": "Point measurement at Dhaka University; captures intense urban core emissions. Requires at least 3 valid observation days per month.",
            "supports_divisions": False,
            "has_gap": False,
            "can_deseasonalize": True,
            "kind": "mean"
        },
        {
            "id": "airs_temp",
            "name": "Near-Surface Air Temperature (NASA AIRS)",
            "domain": "Atmospheric Thermodynamics",
            "sensor": "NASA Aqua AIRS Level 3 (AIRS3STM v7.0 SurfAirTemp_A)",
            "unit": "°C",
            "unit_description": "Near-surface air temperature in degrees Celsius (converted from Kelvin; ~1:30 PM daytime overpass)",
            "spatial_footprint": "1.0° (~111 km) satellite infrared/microwave grid (5 macro-regions + National)",
            "temporal_range": "2002-09 to 2026-07 (monthly)",
            "definition": "Atmospheric Infrared Sounder (AIRS) hyperspectral sounding retrieval of daytime near-surface air temperature.",
            "caveats": "⚠️ Coarse 1.0° footprint (~111 km). Individual regions contain only 1–3 grid cell centers (Central: ~1.4 cells; National: ~9.9 cells). Divisional breakdown is disabled. Clear-sky sampling bias: cloud-cleared retrievals in heavy monsoon months are less representative.",
            "supports_divisions": False,
            "has_gap": False,
            "can_deseasonalize": True,
            "kind": "mean"
        },
        {
            "id": "airs_h2o",
            "name": "Total Column Water Vapor (NASA AIRS)",
            "domain": "Atmospheric Thermodynamics",
            "sensor": "NASA Aqua AIRS Level 3 (AIRS3STM v7.0 TotH2OVap_A)",
            "unit": "kg/m²",
            "unit_description": "Total integrated atmospheric column water vapor (precipitable water in kg/m² or mm)",
            "spatial_footprint": "1.0° (~111 km) satellite infrared/microwave grid (5 macro-regions + National)",
            "temporal_range": "2002-09 to 2026-07 (monthly)",
            "definition": "Total mass of water vapor in an atmospheric column from surface to top of atmosphere.",
            "caveats": "⚠️ Coarse 1.0° footprint (~111 km). Divisional breakdown is disabled. Clear-sky sampling bias in heavy monsoon cloud decks.",
            "supports_divisions": False,
            "has_gap": False,
            "can_deseasonalize": True,
            "kind": "mean"
        },
        {
            "id": "omi_no2",
            "name": "Tropospheric NO₂ Column (NASA OMI)",
            "domain": "Atmospheric Composition",
            "sensor": "NASA Aura OMI Level 3 (OMNO2d v004 Cloud-Screened)",
            "unit": "10¹⁵ molec/cm²",
            "unit_description": "Tropospheric nitrogen dioxide vertical column density in 10¹⁵ molecules per square centimeter",
            "spatial_footprint": "0.25° (~25 km) satellite ultraviolet/visible grid (5 macro-regions, National + 8 divisions)",
            "temporal_range": "2004-10 to 2026-07 (monthly)",
            "definition": "Satellite ultraviolet-visible spectrometer measurement of nitrogen dioxide in the tropospheric boundary layer, serving as a primary indicator of combustion emissions (traffic, brick kilns, industry).",
            "caveats": "Row anomaly on OMI (mitigated by cloud-screened quality filtering). Strong winter peak due to shallow planetary boundary layer and winter brick kiln operations.",
            "supports_divisions": True,
            "has_gap": False,
            "can_deseasonalize": True,
            "kind": "mean"
        }
    ]

    stakeholder_directives = {
        "NW": {
            "region_name": "Northwest Depletion Corridor (Rajshahi & Rangpur)",
            "satellite_metric": "-1.25 cm/year TWS decline (-0.39 km³/year). Rainfall shows no detectable trend (-1.91 mm/year).",
            "historical_context": "Depletion is consistent with intensive dry-season Boro rice cultivation on Pleistocene clay terraces that impede natural monsoon recharge.",
            "mandate": "BMDA must enforce smart-card volumetric pricing and halt unmetered deep tubewell permits. Expand surface water irrigation from Padma/Teesta rivers by 10% by 2030.",
            "farmer_dos": "Adopt Alternate Wetting and Drying (AWD) using PVC pipes (cuts water use by 15–30%). Plant short-duration drought-escaping T. Aman (BRRI dhan56/57) before July 24. Shift to winter crops (BARI chhola-5, BARI sarisha-10).",
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
            "farmer_dos": "Implement SALT contour hedgerows using nitrogen-fixing legumes every 4–6 meters to diffuse runoff. Cultivate flash-flood-tolerant BRRI dhan110.",
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
    }

    payload = {
        "variables": variables,
        "regions": regions,
        "divisions": divisions,
        "floodEvents": flood_events,
        "gapPeriod": {"start": "2017-07", "end": "2018-05", "label": "Inter-Satellite Mission Gap (11 months)"},
        "stakeholderDirectives": stakeholder_directives,
        "canonicalWindows": [
            {"id": "full_record", "label": "Full 24-Year Record", "start": "2002-04", "end": "2026-07"},
            {"id": "grace_era", "label": "GRACE-1 Baseline Era", "start": "2002-04", "end": "2017-06"},
            {"id": "grace_fo_era", "label": "GRACE-FO Single Era", "start": "2018-06", "end": "2026-07"},
            {"id": "recent_2020", "label": "Recent Overlap Era", "start": "2020-01", "end": "2026-07"},
        ],
        "seasons": [
            {"id": "annual", "label": "All Months (Deseasonalized)", "months": "1–12"},
            {"id": "monsoon", "label": "Monsoon Season (JJAS)", "months": "Jun–Sep"},
            {"id": "winter", "label": "Winter / Dry Season (DJF)", "months": "Dec–Feb"},
            {"id": "pre_monsoon", "label": "Pre-Monsoon Season (MAM)", "months": "Mar–May"},
            {"id": "post_monsoon", "label": "Post-Monsoon Season (ON)", "months": "Oct–Nov"},
        ]
    }

    out_file = DATA_DIR / "catalog.js"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"window.ED = window.ED || {{}};\nwindow.ED.catalog = {json.dumps(payload, indent=2)};\n")
    print(f"[OK] Exported {out_file} ({out_file.stat().st_size:,} bytes)")


def export_presets_js():
    res_df = pd.read_csv(REPO_ROOT / "outputs/v3/full_record/results_all_windows.csv")
    # Filter to annual series only (canonical presets)
    ann_df = res_df[res_df["season"] == "annual"].copy()

    presets = {}
    for _, r in ann_df.iterrows():
        key = f"{r['window']}_{r['entity']}_{r['variable']}"
        presets[key] = {
            "window": str(r["window"]),
            "entity": str(r["entity"]),
            "variable": str(r["variable"]),
            "n_obs": int(r["n_obs"]),
            "slope": sanitize(r["slope"], 4),
            "slope_ci_low": sanitize(r["slope_ci_low"], 4),
            "slope_ci_high": sanitize(r["slope_ci_high"], 4),
            "p_value": sanitize(r["p_value"], 6),
            "bh_fdr_q_value": sanitize(r["bh_fdr_q_value"], 6),
            "verdict": str(r["verdict"]),
            "gamma": sanitize(r["gamma"], 3),
            "r1_detrended": sanitize(r["r1_detrended"], 4),
            "n_star": sanitize(r["n_star"], 1),
            "unit": str(r["unit_primary"])
        }

    out_file = DATA_DIR / "presets.js"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"window.ED = window.ED || {{}};\nwindow.ED.presets = {json.dumps(presets, indent=2)};\n")
    print(f"[OK] Exported {out_file} ({len(presets)} canonical preset tests)")


def export_series_regions_js():
    reg_df = pd.read_csv(REPO_ROOT / "outputs/v3/full_record/region_series_2002_2026.csv")
    part_df = pd.read_csv(REPO_ROOT / "outputs/v3/gldas_split/storage_partition_series_multi_model.csv")

    regions_data = {}
    regions = ["NW", "NE", "Central", "SW", "SE", "National"]

    for reg in regions:
        r_sub = reg_df[reg_df["region"] == reg].sort_values("ym").copy()
        p_sub = part_df[part_df["region"] == reg].set_index("ym")

        ym_list = r_sub["ym"].tolist()
        t_list = [sanitize(x, 4) for x in r_sub["decimal_year"]]
        tws_list = [sanitize(x, 3) for x in r_sub["grace_tws_cm"]]
        imerg_list = [sanitize(x, 2) for x in r_sub["imerg_precip_mm"]]
        power_list = [sanitize(x, 2) for x in r_sub["power_precip_mm"]]

        noah_sms = []
        vic_sms = []
        resid_mid = []
        resid_min = []
        resid_max = []

        for ym in ym_list:
            if ym in p_sub.index:
                row = p_sub.loc[ym]
                noah_sms.append(sanitize(row["noah_sms_anom_cm"], 3))
                vic_sms.append(sanitize(row["vic_sms_anom_cm"], 3))
                rmin = sanitize(row["independent_residual_min_cm"], 3)
                rmax = sanitize(row["independent_residual_max_cm"], 3)
                resid_min.append(rmin)
                resid_max.append(rmax)
                if rmin is not None and rmax is not None:
                    resid_mid.append(round((rmin + rmax) / 2.0, 3))
                else:
                    resid_mid.append(None)
            else:
                noah_sms.append(None)
                vic_sms.append(None)
                resid_mid.append(None)
                resid_min.append(None)
                resid_max.append(None)

        regions_data[reg] = {
            "ym": ym_list,
            "t": t_list,
            "tws": tws_list,
            "imerg": imerg_list,
            "power": power_list,
            "noah_sms": noah_sms,
            "vic_sms": vic_sms,
            "residual_mid": resid_mid,
            "residual_min": resid_min,
            "residual_max": resid_max,
        }

    out_file = DATA_DIR / "series_regions.js"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"window.ED = window.ED || {{}};\nwindow.ED.seriesRegions = {json.dumps(regions_data, separators=(',', ':'))};\n")
    print(f"[OK] Exported {out_file} ({out_file.stat().st_size:,} bytes)")


def export_series_divisions_js():
    div_df = pd.read_csv(REPO_ROOT / "outputs/v3/full_record/division_series_2002_2026.csv")
    div_df["Division"] = div_df["Division"].str.strip()

    divisions_data = {}
    for div, grp in div_df.groupby("Division"):
        grp = grp.sort_values("ym").copy()
        divisions_data[div] = {
            "ym": grp["ym"].tolist(),
            "t": [sanitize(x, 4) for x in grp["decimal_year"]],
            "tws": [sanitize(x, 3) for x in grp["grace_tws_cm"]],
            "imerg": [sanitize(x, 2) for x in grp["imerg_precip_mm"]],
            "power": [sanitize(x, 2) for x in grp["power_precip_mm"]],
        }

    out_file = DATA_DIR / "series_divisions.js"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"window.ED = window.ED || {{}};\nwindow.ED.seriesDivisions = {json.dumps(divisions_data, separators=(',', ':'))};\n")
    print(f"[OK] Exported {out_file} ({out_file.stat().st_size:,} bytes)")


def export_series_extremes_js():
    ext_df = pd.read_csv(REPO_ROOT / "outputs/v3/extremes/imerg_extreme_indices_annual.csv")
    extremes_data = {}
    for reg, grp in ext_df.groupby("region"):
        grp = grp.sort_values("year")
        items = []
        for _, r in grp.iterrows():
            items.append({
                "year": int(r["year"]),
                "decimal_year": int(r["year"]) + 0.5,
                "annual_total_mm": sanitize(r["annual_total_mm"], 1),
                "rx1day_mm": sanitize(r["rx1day_mm"], 1),
                "rx5day_mm": sanitize(r["rx5day_mm"], 1),
                "days_ge_50mm": int(r["days_ge_50mm"]) if not pd.isna(r["days_ge_50mm"]) else 0,
            })
        extremes_data[reg] = items

    out_file = DATA_DIR / "series_extremes.js"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"window.ED = window.ED || {{}};\nwindow.ED.seriesExtremes = {json.dumps(extremes_data, indent=2)};\n")
    print(f"[OK] Exported {out_file} ({out_file.stat().st_size:,} bytes)")


def export_series_aod_js():
    aod_data = {
        "dhaka_aeronet": [],
        "dhaka_modis": [],
        "bangladesh_modis": []
    }

    # 1. Dhaka AERONET
    aeronet_path = REPO_ROOT / "outputs/v3/aerosols/dhaka_aod_monthly.csv"
    if aeronet_path.exists():
        df = pd.read_csv(aeronet_path)
        for _, r in df.iterrows():
            yr = int(r["year"])
            mo = int(r["month"])
            dec_yr = round(yr + (mo - 0.5) / 12.0, 4)
            aod_data["dhaka_aeronet"].append({
                "ym": str(r["ym"]),
                "year": yr,
                "month": mo,
                "decimal_year": dec_yr,
                "aod_550": sanitize(r["aod_550"], 3),
                "n_days": int(r["n_days"]) if not pd.isna(r["n_days"]) else None,
                "source": "NASA_AERONET_Dhaka_University_L1.5"
            })

    # 2. Dhaka MODIS (if available)
    dhaka_modis_path = REPO_ROOT / "outputs/v3/aerosols/modis_aod_dhaka_monthly.csv"
    if dhaka_modis_path.exists():
        df = pd.read_csv(dhaka_modis_path)
        for _, r in df.iterrows():
            aod_data["dhaka_modis"].append({
                "ym": str(r["ym"]),
                "year": int(r["year"]),
                "month": int(r["month"]),
                "decimal_year": sanitize(r["decimal_year"], 4),
                "aod_550": sanitize(r["aod_550"], 3),
                "source": "NASA_MODIS_Aqua_MYD08_M3_Dhaka_Box"
            })

    # 3. Bangladesh MODIS (if available)
    bd_modis_path = REPO_ROOT / "outputs/v3/aerosols/modis_aod_bangladesh_monthly.csv"
    if bd_modis_path.exists():
        df = pd.read_csv(bd_modis_path)
        for _, r in df.iterrows():
            aod_data["bangladesh_modis"].append({
                "ym": str(r["ym"]),
                "year": int(r["year"]),
                "month": int(r["month"]),
                "decimal_year": sanitize(r["decimal_year"], 4),
                "aod_550": sanitize(r["aod_550"], 3),
                "source": "NASA_MODIS_Aqua_MYD08_M3_Bangladesh_National"
            })

    out_file = DATA_DIR / "series_aod.js"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"window.ED = window.ED || {{}};\nwindow.ED.seriesAOD = {json.dumps(aod_data, indent=2)};\n")
    print(f"[OK] Exported {out_file} (AERONET: {len(aod_data['dhaka_aeronet'])} mo, MODIS Dhaka: {len(aod_data['dhaka_modis'])} mo, MODIS BD: {len(aod_data['bangladesh_modis'])} mo)")


def export_series_airs_js():
    airs_temp_path = REPO_ROOT / "outputs/v3/airs/airs_temp_regions_monthly.csv"
    airs_h2o_path = REPO_ROOT / "outputs/v3/airs/airs_h2o_regions_monthly.csv"

    airs_data = {}
    regions = ["NW", "NE", "Central", "SW", "SE", "National"]

    if airs_temp_path.exists() and airs_h2o_path.exists():
        temp_df = pd.read_csv(airs_temp_path)
        h2o_df = pd.read_csv(airs_h2o_path)

        for reg in regions:
            t_sub = temp_df[temp_df["region"] == reg].sort_values("ym").copy()
            h_sub = h2o_df[h2o_df["region"] == reg].set_index("ym")

            ym_list = t_sub["ym"].tolist()
            t_list = [sanitize(x, 4) for x in t_sub["decimal_year"]]
            temp_list = [sanitize(x, 3) for x in t_sub["value"]]
            h2o_list = []
            for ym in ym_list:
                if ym in h_sub.index:
                    h2o_list.append(sanitize(h_sub.loc[ym, "value"], 2))
                else:
                    h2o_list.append(None)

            airs_data[reg] = {
                "ym": ym_list,
                "t": t_list,
                "airs_temp": temp_list,
                "airs_h2o": h2o_list,
            }

    out_file = DATA_DIR / "series_airs.js"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"window.ED = window.ED || {{}};\nwindow.ED.seriesAIRS = {json.dumps(airs_data, separators=(',', ':'))};\n")
    print(f"[OK] Exported {out_file} ({out_file.stat().st_size:,} bytes)")


def export_series_omi_js():
    omi_reg_path = REPO_ROOT / "outputs/v3/omi/omi_no2_regions_monthly.csv"
    omi_div_path = REPO_ROOT / "outputs/v3/omi/omi_no2_divisions_monthly.csv"

    omi_data = {
        "regions": {},
        "divisions": {}
    }

    if omi_reg_path.exists():
        reg_df = pd.read_csv(omi_reg_path)
        for reg, grp in reg_df.groupby("region"):
            grp = grp.sort_values("ym").copy()
            reg_entry = {
                "ym": grp["ym"].tolist(),
                "t": [sanitize(x, 4) for x in grp["decimal_year"]],
                "omi_no2": [sanitize(x, 3) for x in grp["value"]],
            }
            omi_data["regions"][reg] = reg_entry
            omi_data[reg] = reg_entry

    if omi_div_path.exists():
        div_df = pd.read_csv(omi_div_path)
        for div, grp in div_df.groupby("division"):
            grp = grp.sort_values("ym").copy()
            div_entry = {
                "ym": grp["ym"].tolist(),
                "t": [sanitize(x, 4) for x in grp["decimal_year"]],
                "omi_no2": [sanitize(x, 3) for x in grp["value"]],
            }
            omi_data["divisions"][div] = div_entry
            omi_data[div] = div_entry

    out_file = DATA_DIR / "series_omi.js"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"window.ED = window.ED || {{}};\nwindow.ED.seriesOMI = {json.dumps(omi_data, separators=(',', ':'))};\n")
    print(f"[OK] Exported {out_file} ({out_file.stat().st_size:,} bytes)")


def main():
    print("Building web application data payloads...")
    export_map_js()
    export_catalog_js()
    export_presets_js()
    export_series_regions_js()
    export_series_divisions_js()
    export_series_extremes_js()
    export_series_aod_js()
    export_series_airs_js()
    export_series_omi_js()
    print("[SUCCESS] All web application data files generated successfully in data/.")


if __name__ == "__main__":
    main()
