"""
NASA Space Apps 2026 - Trend Detective: Bengal Water Paradox
NASA Satellite Precipitation Downloader for Bangladesh

Downloads NASA satellite precipitation grid (derived from GPM IMERG & GMAO MERRA-2)
via the NASA POWER regional API covering Bangladesh (2000–2026) and compiles it into
a clean CF-compliant NetCDF dataset: 'nasa_precipitation_bangladesh.nc'.

No authentication required.
"""

import sys
import os
import calendar
import urllib.request
import json
from datetime import datetime

import numpy as np
import pandas as pd
import xarray as xr


def download_nasa_precipitation(output_file: str = "nasa_precipitation_bangladesh.nc", start_year: int = 2020, end_year: int = 2026):
    print(f"Fetching NASA Satellite Precipitation for Bangladesh ({start_year}–{end_year})...")
    
    # NASA POWER API regional bounding box for Bangladesh
    # Lat: 20.4N to 26.8N, Lon: 88.0E to 92.8E
    url = (
        f"https://power.larc.nasa.gov/api/temporal/monthly/regional"
        f"?parameters=PRECTOTCORR&community=AG"
        f"&longitude-min=88.0&longitude-max=92.8"
        f"&latitude-min=20.4&latitude-max=26.8"
        f"&start={start_year}&end={end_year}&format=JSON"
    )

    req = urllib.request.Request(url, headers={"User-Agent": "NASA-SpaceApps-TrendDetective/1.0"})
    with urllib.request.urlopen(req, timeout=90) as response:
        data = json.loads(response.read().decode("utf-8"))

    features = data.get("features", [])
    if not features:
        raise ValueError("No features returned by NASA POWER API.")

    # Unique coordinate lists
    lats = sorted(list(set(f["geometry"]["coordinates"][1] for f in features)))
    lons = sorted(list(set(f["geometry"]["coordinates"][0] for f in features)))

    # Discover valid months (skipping '13' annual averages and -999 missing values)
    sample_param = features[0]["properties"]["parameter"]["PRECTOTCORR"]
    month_keys = sorted([
        k for k, v in sample_param.items()
        if not k.endswith("13") and v != -999.0
    ])

    dates = [pd.to_datetime(k, format="%Y%m") for k in month_keys]
    
    n_times = len(dates)
    n_lats = len(lats)
    n_lons = len(lons)

    lat_map = {lat: i for i, lat in enumerate(lats)}
    lon_map = {lon: j for j, lon in enumerate(lons)}

    # Array 1: Daily rate (mm/day)
    rate_grid = np.full((n_times, n_lats, n_lons), np.nan, dtype=np.float32)
    # Array 2: Monthly accumulation (mm/month)
    monthly_accum_grid = np.full((n_times, n_lats, n_lons), np.nan, dtype=np.float32)

    for feat in features:
        flon, flat, _ = feat["geometry"]["coordinates"]
        i = lat_map[flat]
        j = lon_map[flon]
        p_dict = feat["properties"]["parameter"]["PRECTOTCORR"]

        for t_idx, m_key in enumerate(month_keys):
            val = p_dict.get(m_key, -999.0)
            if val != -999.0:
                rate_grid[t_idx, i, j] = val
                year = int(m_key[:4])
                month = int(m_key[4:])
                num_days = calendar.monthrange(year, month)[1]
                monthly_accum_grid[t_idx, i, j] = val * num_days

    # Build CF-compliant xarray Dataset
    ds = xr.Dataset(
        data_vars={
            "precipitation": (
                ["time", "lat", "lon"],
                monthly_accum_grid,
                {
                    "standard_name": "precipitation_amount",
                    "long_name": "Monthly Total Accumulated Precipitation",
                    "units": "mm/month",
                    "comment": "Calculated as daily mean rate * days in month"
                }
            ),
            "precipitation_rate": (
                ["time", "lat", "lon"],
                rate_grid,
                {
                    "standard_name": "precipitation_flux",
                    "long_name": "Daily Mean Precipitation Rate",
                    "units": "mm/day"
                }
            )
        },
        coords={
            "time": (["time"], dates, {"standard_name": "time", "axis": "T"}),
            "lat": (["lat"], lats, {"standard_name": "latitude", "units": "degrees_north", "axis": "Y"}),
            "lon": (["lon"], lons, {"standard_name": "longitude", "units": "degrees_east", "axis": "X"})
        },
        attrs={
            "title": "NASA Satellite Precipitation Grid for Bangladesh",
            "source": "NASA POWER (GPM IMERG & GMAO MERRA-2 Agroclimatology)",
            "spatial_resolution": "0.5 x 0.625 degree",
            "temporal_range": f"{month_keys[0]} to {month_keys[-1]}",
            "project": "NASA Space Apps 2026 - Trend Detective: Bengal Water Paradox",
            "created_at": datetime.now().isoformat()
        }
    )

    ds.to_netcdf(output_file)
    print(f"Saved NetCDF dataset to: {output_file} ({os.path.getsize(output_file):,} bytes)")
    print(f"Coverage: {len(dates)} months from {month_keys[0]} to {month_keys[-1]}")
    return output_file


if __name__ == "__main__":
    download_nasa_precipitation()
