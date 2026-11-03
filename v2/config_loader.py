"""
NASA Space Apps 2026 – Bengal Hydro Detective
Central Configuration Loader & Validator
========================================
Resolves data paths dynamically via:
  1. Explicit CLI argument (--grace-nc)
  2. Environment variable (GRACE_NETCDF_PATH)
  3. config.json at repository root ("grace_netcdf_path")
  4. Known default filenames in repository root

Enforces strict rules:
  - No hardcoded personal or machine-specific paths
  - Fails loudly if a requested file/window is missing
  - Prevents writing duplicate-window rows when earlier data is absent
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = REPO_ROOT / "config.json"

DEFAULT_GRACE_FILENAMES = [
    "CSR_GRACE_GRACE-FO_RL0603_Mascons_all-corrections.nc",
    "CSR_GRACE_GRACE-FO_RL0602_Mascons_all-corrections.nc",
    "CSR_GRACE_RL0603_Mascons.nc",
    "grace_mascons_bangladesh.nc",
]


def load_config() -> dict:
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[WARNING] Could not parse config.json ({e}); using defaults.")
    return {}


def get_grace_netcdf_path(cli_override: Optional[str] = None) -> Optional[Path]:
    """
    Resolves the GRACE NetCDF file path in strict priority order.
    Returns Path object if existing, otherwise None.
    """
    # 1. CLI override
    if cli_override:
        p = Path(cli_override).expanduser().resolve()
        if p.exists():
            return p
        else:
            print(f"[!] Provided CLI --grace-nc does not exist: {p}")

    # 2. Environment variable
    env_path = os.environ.get("GRACE_NETCDF_PATH")
    if env_path:
        p = Path(env_path).expanduser().resolve()
        if p.exists():
            return p
        else:
            print(f"[!] GRACE_NETCDF_PATH from environment does not exist: {p}")

    # 3. config.json
    cfg = load_config()
    cfg_path = cfg.get("grace_netcdf_path")
    if cfg_path:
        p = Path(cfg_path).expanduser().resolve()
        if p.exists():
            return p
        else:
            print(f"[!] Path specified in config.json does not exist: {p}")

    # 4. Known repository root defaults
    for fn in DEFAULT_GRACE_FILENAMES:
        cand = REPO_ROOT / fn
        if cand.exists():
            return cand

    return None


def require_grace_netcdf(purpose: str = "GRACE-FO era analysis") -> Path:
    """
    Fails loudly with an explicit error banner if the GRACE NetCDF is missing.
    """
    p = get_grace_netcdf_path()
    if p is None:
        sep = "═" * 84
        msg = f"""
{sep}
  [FATAL CONFIGURATION ERROR] GRACE / GRACE-FO NetCDF IS MISSING!
  Required for: {purpose}
{sep}

  The requested analysis requires the full mission GRACE/GRACE-FO NetCDF dataset.
  The pipeline searched:
    1. CLI argument      : --grace-nc <path>
    2. Environment var   : GRACE_NETCDF_PATH
    3. config.json       : "grace_netcdf_path": "<path>"
    4. Repo directory    : CSR_GRACE_GRACE-FO_RL0603_Mascons_all-corrections.nc

  HOW TO RESOLVE:
    1. If you have the NetCDF file on your computer, set its path:
       - In config.json: "grace_netcdf_path": "C:/path/to/CSR_GRACE_GRACE-FO_RL0603_Mascons_all-corrections.nc"
       - Or export environment variable:
         PowerShell: $env:GRACE_NETCDF_PATH="C:/path/to/file.nc"
         Bash      : export GRACE_NETCDF_PATH="/path/to/file.nc"

    2. Download from official NASA PO.DAAC / UT-CSR mirrors:
       https://podaac.jpl.nasa.gov/dataset/TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06_V2
       or https://www2.csr.utexas.edu/grace/RL0603_mascons.html
{sep}
"""
        print(msg, file=sys.stderr)
        raise FileNotFoundError(f"GRACE NetCDF is missing. Cannot proceed with {purpose}.")
    return p


def get_analysis_windows(has_grace_netcdf: bool) -> list[str]:
    """
    Determines valid analysis windows.
    If GRACE NetCDF is absent, only 'primary' (2020-01 to 2026-07) is allowed.
    Never writes duplicate-window rows!
    """
    if has_grace_netcdf:
        return ["primary", "grace_fo"]
    else:
        return ["primary"]
