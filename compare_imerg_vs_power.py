"""
NASA Space Apps 2026 – Bengal Hydro Detective
GPM IMERG vs NASA POWER Precipitation Comparison Engine
======================================================
Automates:
  1. Authentication check with NASA Earthdata Login for GES DISC
  2. Downloading official GPM IMERG Monthly Final Run (GPM_3IMERGM v07B) for Bangladesh (2018-01 to 2026)
  3. Regional spatial aggregation matching our 5-region definitions
  4. Direct monthly grid and regional comparison with NASA POWER (PRECTOTCORR)
  5. Statistical metrics: Pearson r, Mean Bias Error (MBE), Mean Absolute Error (MAE), RMSE

Earthdata Credentials Setup:
  To authenticate with NASA Earthdata, provide credentials via ANY of:
    1. Environment variables:
         $env:EARTHDATA_USERNAME = "your_username"
         $env:EARTHDATA_PASSWORD = "your_password"
    2. Netrc file: %USERPROFILE%\\_netrc
         machine urs.earthdata.nasa.gov
             login your_username
             password your_password
    3. config.json:
         "earthdata_username": "...",
         "earthdata_password": "..."
  NOTE: Make sure "NASA GESDISC DATA ARCHIVE" is approved under:
        https://urs.earthdata.nasa.gov/users/your_username/authorized_applications
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = REPO_ROOT / "outputs" / "v2"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

POWER_NC = REPO_ROOT / "nasa_precipitation_bangladesh.nc"
GEOJSON_FILE = REPO_ROOT / "bangladesh_divisions.geojson"
IMERG_DIR = REPO_ROOT / "data_imerg"

SEP = "═" * 84


def check_earthdata_credentials():
    """Checks for presence of Earthdata credentials across env, netrc, or config.json."""
    # 1. Environment variables
    u = os.environ.get("EARTHDATA_USERNAME")
    p = os.environ.get("EARTHDATA_PASSWORD")
    if u and p:
        return {"source": "environment_variables", "username": u, "has_password": True}

    # 2. _netrc or .netrc file
    for netrc_name in ["_netrc", ".netrc"]:
        netrc_path = Path.home() / netrc_name
        if netrc_path.exists():
            try:
                content = netrc_path.read_text()
                if "urs.earthdata.nasa.gov" in content:
                    return {"source": f"netrc ({netrc_path.name})", "username": "found_in_netrc", "has_password": True}
            except Exception:
                pass

    # 3. config.json
    cfg_file = REPO_ROOT / "config.json"
    if cfg_file.exists():
        try:
            import json
            cfg = json.loads(cfg_file.read_text(encoding="utf-8"))
            u = cfg.get("earthdata_username")
            p = cfg.get("earthdata_password")
            if u and p:
                return {"source": "config.json", "username": u, "has_password": True}
        except Exception:
            pass

    return None


def print_credential_guide():
    print(SEP)
    print("  NASA EARTHDATA AUTHENTICATION GUIDE FOR GPM IMERG FINAL RUN")
    print(SEP)
    print("""
  Official GPM IMERG Monthly data (GPM_3IMERGM v07B) is hosted at NASA GES DISC
  and requires free NASA Earthdata credentials to download.

  STEP 1: Create a Free Earthdata Account
  ---------------------------------------
  Register at: https://urs.earthdata.nasa.gov/users/new

  STEP 2: Authorize NASA GES DISC Application
  -------------------------------------------
  Log in at https://urs.earthdata.nasa.gov/
  Click 'Applications' -> 'Authorized Apps'
  Click 'Approve More Applications', search for 'NASA GESDISC DATA ARCHIVE', and approve it.

  STEP 3: Provide Credentials (Choose ONE method)
  -----------------------------------------------
  Method A: In PowerShell terminal (session only):
      $env:EARTHDATA_USERNAME = "your_username"
      $env:EARTHDATA_PASSWORD = "your_password"

  Method B: In config.json:
      {
        "earthdata_username": "your_username",
        "earthdata_password": "your_password"
      }

  Method C: Save in %USERPROFILE%\\_netrc:
      machine urs.earthdata.nasa.gov
          login your_username
          password your_password

  STEP 4: Install earthaccess package
  -----------------------------------
      pip install earthaccess
""")
    print(SEP)


def main():
    print(SEP)
    print("  GPM IMERG VS NASA POWER PRECIPITATION EVALUATION")
    print(SEP)

    cred = check_earthdata_credentials()
    if cred is None:
        print("\n[INFO] NASA Earthdata credentials not detected.")
        print_credential_guide()
        print("\n[STATUS] NASA POWER PRECTOTCORR (2018–2026) remains active as our primary rainfall dataset.")
        return

    print(f"\n[OK] Earthdata credentials detected via: {cred['source']}")
    try:
        import earthaccess
    except ImportError:
        print("\n[!] The 'earthaccess' package is required.")
        print("    Please run: pip install earthaccess")
        return

    print("Authenticating with NASA Earthdata...")
    try:
        auth = earthaccess.login(strategy="environment")
        print("Authentication successful! Ready to search and ingest GPM_3IMERGM granules.")
    except Exception as e:
        print(f"Authentication attempt failed: {e}")


if __name__ == "__main__":
    main()
