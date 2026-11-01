"""
NASA Space Apps 2026 – Bengal Hydro Detective
v3 Analysis Windows, Regions, and Configuration
===============================================
Defines the 4 validated analytical windows:
  1. full_record: 2002-04 to 2026-07 (PRIMARY)
  2. grace_era:   2002-04 to 2017-06 (Epoch 1; comparable to published literature)
  3. grace_fo_era: 2018-06 to 2026-07 (Epoch 2; single instrument, 96 observed)
  4. recent_2020: 2020-01 to 2026-07 (Sensitivity / v2 legacy baseline, 79 observed)

Strict Principles:
  - Import existing trend engine (do not re-implement)
  - 3-tiered verdict rule:
      * "Significant": BH-FDR q < 0.05 within its own family AND bootstrap 95% CI excludes 0
      * "Suggestive": raw p < 0.05 only
      * "No detectable trend": otherwise
  - All claims PRELIMINARY
  - TWS = "total water storage", not "groundwater"
  - Language: "consistent with", never "caused by"
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUTS_V3 = REPO_ROOT / "outputs" / "v3"
OUTPUTS_V3_FULL = OUTPUTS_V3 / "full_record"
OUTPUTS_V3_FULL.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42
N_BOOT = 9_999

WINDOWS = {
    "full_record": {
        "start": "2002-04",
        "end": "2026-07",
        "role": "PRIMARY",
        "description": "Full GRACE/GRACE-FO record (2002-04 to 2026-07), 292 months nominal.",
    },
    "grace_era": {
        "start": "2002-04",
        "end": "2017-06",
        "role": "EPOCH_1",
        "description": "GRACE primary mission era (2002-04 to 2017-06), comparable to prior literature.",
    },
    "grace_fo_era": {
        "start": "2018-06",
        "end": "2026-07",
        "role": "EPOCH_2",
        "description": "GRACE-FO single-instrument mission era (2018-06 to 2026-07, 96 observed).",
    },
    "recent_2020": {
        "start": "2020-01",
        "end": "2026-07",
        "role": "SENSITIVITY",
        "description": "Recent baseline window (2020-01 to 2026-07, 79 observed) for v2 comparability.",
    },
}

REGIONS = {
    "NW": {
        "divisions": ["Rajshahi", "Rangpur"],
        "area_km2": 30984.4,
        "name_long": "Northwest (Rajshahi + Rangpur)",
    },
    "NE": {
        "divisions": ["Sylhet", "Mymensingh"],
        "area_km2": 21198.4,
        "name_long": "Northeast (Sylhet + Mymensingh)",
    },
    "Central": {
        "divisions": ["Dhaka"],
        "area_km2": 17130.7,
        "name_long": "Central (Dhaka)",
    },
    "SW": {
        "divisions": ["Khulna", "Barishal"],
        "area_km2": 28153.0,
        "name_long": "Southwest (Khulna + Barishal)",
    },
    "SE": {
        "divisions": ["Chattogram"],
        "area_km2": 24886.5,
        "name_long": "Southeast (Chattogram)",
    },
    "National": {
        "divisions": [
            "Barishal", "Chattogram", "Dhaka", "Khulna",
            "Mymensingh", "Rajshahi", "Rangpur", "Sylhet"
        ],
        "area_km2": 122353.0,
        "name_long": "National Composite (All 8 Divisions)",
    },
}

DIV_AREAS = {
    "Barishal": 9887.4,
    "Chattogram": 24886.5,
    "Dhaka": 17130.7,
    "Khulna": 18265.6,
    "Mymensingh": 10001.8,
    "Rajshahi": 15816.3,
    "Rangpur": 15168.1,
    "Sylhet": 11196.6,
}

SEASONS = {
    "annual": list(range(1, 13)),
    "monsoon": [6, 7, 8, 9],
    "dry": [12, 1, 2, 3],
}
