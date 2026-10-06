"""
NASA Space Apps 2026 - Trend Detective: Bengal Water Paradox
Divisional Precipitation Analysis Pipeline (GPM IMERG & NASA Satellite Precipitation)

Analyzes and visualizes division-level precipitation across Bangladesh on any fixed month.
Supports both the automated NASA satellite precipitation dataset ('nasa_precipitation_bangladesh.nc')
and official GPM IMERG Final Run V07B NetCDF4/HDF5 files.

Usage:
    python analyze_precipitation.py [--month YYYY-MM] [--output-dir DIR] [--nc-file PATH]
Example:
    python analyze_precipitation.py --month 2026-07
"""

import os
import sys
import argparse
import json
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
import xarray as xr
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import shapely
import pyproj

from download_nasa_precipitation import download_nasa_precipitation


def load_dataset(nc_file_path: str):
    """Load precipitation NetCDF dataset, auto-downloading if missing."""
    if not os.path.exists(nc_file_path):
        print(f"Precipitation dataset '{nc_file_path}' not found locally. Initiating automated download from NASA API...")
        download_nasa_precipitation(output_file=nc_file_path)

    ds = xr.open_dataset(nc_file_path)
    return ds


def detect_precip_variable(ds):
    """Identify the precipitation variable name across NASA POWER and GPM IMERG conventions."""
    candidates = ["precipitation", "precipitationCal", "precip", "PRECTOTCORR", "precipitationCal_cnt"]
    for c in candidates:
        if c in ds.data_vars:
            return c
    # Fallback to first 3D variable
    for var in ds.data_vars:
        if len(ds[var].dims) >= 2:
            return var
    raise KeyError(f"No suitable precipitation variable found in dataset. Variables: {list(ds.data_vars.keys())}")


def get_available_months(ds):
    """Return dictionary of { 'YYYY-MM': (time_index, pd.Timestamp) }."""
    months = {}
    time_coords = ds["time"].values
    for idx, t in enumerate(time_coords):
        dt = pd.to_datetime(t)
        key = dt.strftime("%Y-%m")
        months[key] = (idx, dt)
    return months


def get_division_geometries():
    """Extract official administrative division boundaries for all 8 Bangladesh divisions."""
    geojson_path = Path(__file__).parent / "bangladesh_divisions.geojson"
    geod = pyproj.Geod(ellps="WGS84")
    if geojson_path.exists():
        with open(geojson_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        divisions = {}
        for feat in data["features"]:
            name = feat["properties"]["name"]
            geom = shapely.geometry.shape(feat["geometry"])
            area_m2 = feat["properties"].get("area_m2")
            if not area_m2:
                area_m2 = abs(geod.geometry_area_perimeter(geom)[0])
            area_km2 = feat["properties"].get("area_km2", area_m2 / 1e6)
            divisions[name] = {
                "name": name,
                "raw_name": name,
                "geometry": geom,
                "area_km2": area_km2,
                "area_m2": area_m2
            }
        return divisions

    # Fallback to Natural Earth if GeoJSON is not available
    shp_path = shpreader.natural_earth("10m", "cultural", "admin_1_states_provinces")
    reader = shpreader.Reader(shp_path)
    divisions = {}

    for rec in reader.records():
        if rec.attributes.get("admin") == "Bangladesh":
            raw_name = rec.attributes.get("name")
            name_map = {
                "Chittagong": "Chattogram",
                "Barisal": "Barishal"
            }
            clean_name = name_map.get(raw_name, raw_name)
            area_m2 = abs(geod.geometry_area_perimeter(rec.geometry)[0])
            divisions[clean_name] = {
                "name": clean_name,
                "raw_name": raw_name,
                "geometry": rec.geometry,
                "area_km2": area_m2 / 1e6,
                "area_m2": area_m2
            }
    return divisions


def classify_rainfall(mean_mm: float) -> str:
    """Classify monthly precipitation condition according to meteorological standards."""
    if mean_mm < 25.0:
        return "Scanty / Drought"
    elif mean_mm < 100.0:
        return "Below Normal"
    elif mean_mm < 300.0:
        return "Moderate Monsoonal"
    elif mean_mm < 600.0:
        return "Heavy Monsoon"
    else:
        return "Extreme Deluge / Flood Risk"


def analyze_division_precip(ds, precip_var: str, time_idx: int, divisions: dict):
    """Calculate division-level precipitation statistics for a single month index."""
    # Slice Bangladesh bounding box: 20.4N to 26.8N, 88.0E to 92.8E
    sub = ds[precip_var].isel(time=time_idx).sel(
        lat=slice(20.4, 26.8) if ds["lat"].values[0] < ds["lat"].values[-1] else slice(26.8, 20.4),
        lon=slice(88.0, 92.8)
    )

    lon2d, lat2d = np.meshgrid(sub.lon.values, sub.lat.values)
    lat_rad = np.radians(lat2d)
    area_weights = np.cos(lat_rad)

    results = {}
    data_values = sub.values

    for name, div in divisions.items():
        geom = div["geometry"]
        mask = shapely.contains_xy(geom, lon2d, lat2d)
        cell_count = int(mask.sum())

        # If division boundary is between grid cell centers, fallback to intersects
        if cell_count == 0:
            mask = shapely.intersects_xy(geom, lon2d, lat2d)
            cell_count = int(mask.sum())

        if cell_count > 0:
            vals = data_values[mask]
            wts = area_weights[mask]
            w_mean = float(np.sum(vals * wts) / np.sum(wts))
            min_val = float(np.min(vals))
            max_val = float(np.max(vals))
            std_val = float(np.std(vals))
        else:
            w_mean = 0.0
            min_val = 0.0
            max_val = 0.0
            std_val = 0.0

        # Influx volume in km³:
        # Area (m²) * depth (m) * 1e-9 (1 mm = 0.001 m)
        vol_km3 = div["area_m2"] * (w_mean * 0.001) * 1e-9

        # Convert to daily rate (assuming ~30.4 days avg or exact month days)
        daily_rate_mm_day = w_mean / 30.0

        results[name] = {
            "name": name,
            "area_km2": round(div["area_km2"], 1),
            "cell_count": cell_count,
            "mean_precip_mm": round(w_mean, 1),
            "daily_rate_mm_day": round(daily_rate_mm_day, 2),
            "min_precip_mm": round(min_val, 1),
            "max_precip_mm": round(max_val, 1),
            "std_precip_mm": round(std_val, 1),
            "water_volume_km3": round(vol_km3, 3),
            "condition": classify_rainfall(w_mean)
        }
    return results


def plot_precip_choropleth(divisions: dict, results: dict, date_str: str, output_path: str):
    """Generate high-resolution choropleth map of Bangladesh precipitation by division."""
    fig = plt.figure(figsize=(9, 10))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([87.8, 93.0, 20.4, 26.8], crs=ccrs.PlateCarree())

    # Dynamically scale colorbar to rainfall range
    all_means = [r["mean_precip_mm"] for r in results.values()]
    max_precip = max(all_means)
    vmax = max(600, int(np.ceil(max_precip / 100.0) * 100))
    
    norm = mcolors.Normalize(vmin=0, vmax=vmax)
    cmap = plt.cm.YlGnBu

    for name, div in divisions.items():
        val = results[name]["mean_precip_mm"]
        color = cmap(norm(val))
        ax.add_geometries(
            [div["geometry"]],
            crs=ccrs.PlateCarree(),
            facecolor=color,
            edgecolor="#0f172a",
            linewidth=1.2
        )

        centroid = div["geometry"].centroid
        cx, cy = centroid.x, centroid.y
        if name == "Barishal":
            cy -= 0.1
        elif name == "Dhaka":
            cx -= 0.05
            cy -= 0.08
        elif name == "Mymensingh":
            cy += 0.08
        elif name == "Sylhet":
            cy += 0.1

        # Adjust text color for readability against dark blue
        text_color = "white" if val > (vmax * 0.65) else "#0f172a"
        bg_color = "black" if text_color == "white" else "white"

        ax.text(
            cx, cy,
            f"{name}\n{val:.0f} mm",
            transform=ccrs.PlateCarree(),
            ha="center", va="center",
            fontsize=8.5, fontweight="bold",
            color=text_color,
            bbox=dict(boxstyle="round,pad=0.2", facecolor=bg_color, alpha=0.6, edgecolor="none")
        )


    # Cartographic overlays
    ax.coastlines(resolution="10m", color="#1e293b", linewidth=1.0)
    ax.add_feature(cfeature.RIVERS, edgecolor="#0284c7", linewidth=0.8, alpha=0.7)

    gl = ax.gridlines(draw_labels=True, dms=False, x_inline=False, y_inline=False, alpha=0.25)
    gl.top_labels = False
    gl.right_labels = False

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, orientation="vertical", pad=0.04, shrink=0.8)
    cbar.set_label("Division Mean Monthly Precipitation (mm)", fontsize=10, labelpad=8)

    plt.title(
        f"Bangladesh Monthly Precipitation by Division\nNASA GPM IMERG / Satellite Influx — {date_str}",
        fontsize=12, fontweight="bold", pad=14
    )

    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_precip_ranking(results: dict, date_str: str, prev_date_str: str, output_path: str):
    """Generate horizontal bar chart ranking divisions from lowest to highest precipitation."""
    df = pd.DataFrame(list(results.values())).sort_values(by="mean_precip_mm", ascending=True)

    fig, ax = plt.subplots(figsize=(11, 6.2))

    # Color palette according to rainfall intensity
    colors = []
    for val in df["mean_precip_mm"]:
        if val < 50:
            colors.append("#ea580c")  # Orange / Dry
        elif val < 150:
            colors.append("#eab308")  # Yellow / Below normal
        elif val < 300:
            colors.append("#0ea5e9")  # Sky Blue / Normal
        elif val < 600:
            colors.append("#0284c7")  # Deep Blue / Heavy
        else:
            colors.append("#1e3a8a")  # Dark Blue / Extreme Deluge

    bars = ax.barh(df["name"], df["mean_precip_mm"], color=colors, edgecolor="#0f172a", height=0.62)

    # Annotate bars
    for bar, (_, row) in zip(bars, df.iterrows()):
        val = row["mean_precip_mm"]
        yoy = row.get("yoy_delta_mm", None)
        vol = row["water_volume_km3"]

        yoy_text = f" (YoY: {yoy:+.0f} mm)" if yoy is not None else ""
        label_text = f" {val:.0f} mm | {vol:.2f} km³{yoy_text} "

        ax.text(val + 5, bar.get_y() + bar.get_height() / 2, label_text,
                va="center", ha="left", fontsize=8.5, fontweight="600")

    ax.set_xlabel("Mean Monthly Precipitation (mm)", fontsize=11, fontweight="bold")
    ax.set_title(
        f"Divisional Precipitation Influx Ranking ({date_str})\n"
        f"Comparison baseline against {prev_date_str if prev_date_str else 'N/A'}",
        fontsize=12, fontweight="bold", pad=12
    )

    max_x = max(df["mean_precip_mm"].max() * 1.35, 100)
    ax.set_xlim(0, max_x)
    ax.grid(axis="x", linestyle=":", alpha=0.5)

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def generate_html_report(date_str: str, prev_date_str: str, results: dict,
                         choropleth_filename: str, ranking_filename: str,
                         output_html_path: str):
    """Generate standalone HTML report in the Trend Detective aesthetic."""
    df = pd.DataFrame(list(results.values())).sort_values(by="mean_precip_mm", ascending=False)

    total_area = sum(r["area_km2"] for r in results.values())
    national_mean = sum(r["mean_precip_mm"] * r["area_km2"] for r in results.values()) / total_area
    total_rain_vol = sum(r["water_volume_km3"] for r in results.values())

    table_rows = ""
    for _, r in df.iterrows():
        cond_color = "#dc2626" if "Drought" in r["condition"] or "Scanty" in r["condition"] \
                     else "#0284c7" if "Deluge" in r["condition"] or "Heavy" in r["condition"] \
                     else "#16a34a"
        yoy_str = f"{r.get('yoy_delta_mm', 0.0):+.1f} mm" if "yoy_delta_mm" in r else "N/A"
        yoy_color = "#0284c7" if r.get('yoy_delta_mm', 0.0) > 0 else "#dc2626"

        table_rows += f"""
        <tr>
            <td style="font-weight: 700; color: #0f172a;">{r['name']}</td>
            <td>{r['area_km2']:,} km²</td>
            <td style="font-weight: 700; color: #0284c7;">{r['mean_precip_mm']:.1f} mm</td>
            <td>{r['daily_rate_mm_day']:.2f} mm/day</td>
            <td>[{r['min_precip_mm']:.0f}, {r['max_precip_mm']:.0f}] mm</td>
            <td><strong>{r['water_volume_km3']:.3f} km³</strong></td>
            <td style="font-weight: 600; color: {yoy_color};">{yoy_str}</td>
            <td><span class="badge" style="background: {cond_color}20; color: {cond_color}; border: 1px solid {cond_color};">{r['condition']}</span></td>
        </tr>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NASA Earth Detective — Divisional Precipitation Influx Report ({date_str})</title>
    <link href="https://fonts.googleapis.com/css2?family=Architects+Daughter&family=Inter:wght@400;600;700&family=Permanent+Marker&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: #ffffff;
            --ink-dark: #1e293b;
            --ink-blue: #0284c7;
            --ink-green: #16a34a;
        }}
        body {{
            font-family: 'Inter', sans-serif;
            background: var(--bg-color);
            color: #f8fafc;
            margin: 0;
            padding: 24px;
            display: flex;
            justify-content: center;
        }}
        .container {{
            max-width: 1100px;
            width: 100%;
        }}
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #334155;
            padding-bottom: 16px;
            margin-bottom: 24px;
        }}
        h1 {{
            font-family: 'Permanent Marker', cursive;
            font-size: 2rem;
            margin: 0;
            color: #38bdf8;
        }}
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin-bottom: 28px;
        }}
        .kpi-card {{
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 16px 20px;
        }}
        .kpi-label {{
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #94a3b8;
        }}
        .kpi-val {{
            font-family: 'Permanent Marker', cursive;
            font-size: 1.8rem;
            margin-top: 6px;
            color: #38bdf8;
        }}
        .card {{
            background: var(--card-bg);
            color: var(--ink-dark);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        }}
        .section-title {{
            font-family: 'Architects Daughter', cursive;
            font-size: 1.4rem;
            font-weight: bold;
            margin-top: 0;
            margin-bottom: 16px;
            color: #1e293b;
            border-bottom: 2px dashed #cbd5e1;
            padding-bottom: 8px;
        }}
        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        img.report-img {{
            width: 100%;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.95rem;
            text-align: left;
        }}
        th {{
            background: #f1f5f9;
            padding: 12px 14px;
            font-weight: 700;
            color: #475569;
            border-bottom: 2px solid #cbd5e1;
        }}
        td {{
            padding: 12px 14px;
            border-bottom: 1px solid #e2e8f0;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
        }}
        .nav-bar {{
            display: flex;
            gap: 10px;
            margin-bottom: 24px;
            flex-wrap: wrap;
            align-items: center;
        }}
        .nav-pill {{
            padding: 8px 16px;
            border-radius: 8px;
            text-decoration: none;
            font-size: 0.85rem;
            font-weight: 600;
            background: #1e293b;
            color: #94a3b8;
            border: 1px solid #334155;
        }}
        .nav-pill:hover {{
            background: #334155;
            color: #f8fafc;
        }}
        .nav-pill.active {{
            background: #0284c7;
            color: #ffffff;
            border-color: #38bdf8;
        }}
        footer {{
            text-align: center;
            color: #64748b;
            font-size: 0.85rem;
            margin-top: 24px;
        }}
    </style>
</head>

<body>
    <div class="container">
        <header>
            <div>
                <div style="font-family: 'Architects Daughter', cursive; color: #94a3b8; font-size: 1rem;">Case File #026-BD // Atmospheric Precipitation Audit</div>
                <h1>The Bengal Water Paradox</h1>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 0.85rem; color: #94a3b8;">Observation Month</div>
                <div style="font-size: 1.25rem; font-weight: 700; color: #38bdf8;">{date_str}</div>
            </div>
        </header>

        <div class="nav-bar">
            <span style="font-size: 0.85rem; color: #94a3b8; font-weight: 600;">Explore Key Seasons:</span>
            <a href="divisional_precip_report_2025-12.html" class="nav-pill {'active' if 'December 2025' in date_str else ''}">❄️ Dec 2025 (Dry Winter)</a>
            <a href="divisional_precip_report_2026-03.html" class="nav-pill {'active' if 'March 2026' in date_str else ''}">🌱 Mar 2026 (Boro Irrigation)</a>
            <a href="divisional_precip_report_2026-07.html" class="nav-pill {'active' if 'July 2026' in date_str else ''}">🌊 Jul 2026 (Monsoon Peak)</a>
        </div>


        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">National Mean Precipitation</div>
                <div class="kpi-val">{national_mean:.1f} mm</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Total Water Influx from Rain</div>
                <div class="kpi-val">{total_rain_vol:.2f} km³</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Highest Rainfall Division</div>
                <div class="kpi-val" style="color: #0284c7;">{df.iloc[0]['name']} ({df.iloc[0]['mean_precip_mm']:.0f} mm)</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Driest Division</div>
                <div class="kpi-val" style="color: #ea580c;">{df.iloc[-1]['name']} ({df.iloc[-1]['mean_precip_mm']:.0f} mm)</div>
            </div>
        </div>

        <div class="card">
            <div class="section-title">Visual Evidence: Spatial Precipitation & Divisional Ranking</div>
            <div class="grid-2">
                <div>
                    <h4 style="margin: 0 0 10px 0; color: #475569;">Spatial Precipitation Choropleth</h4>
                    <img class="report-img" src="{choropleth_filename}" alt="Divisional Precipitation Map">
                </div>
                <div>
                    <h4 style="margin: 0 0 10px 0; color: #475569;">Precipitation Influx Ranking</h4>
                    <img class="report-img" src="{ranking_filename}" alt="Divisional Precipitation Ranking">
                </div>
            </div>
        </div>

        <div class="card">
            <div class="section-title">Divisional Atmospheric Influx Audit Table</div>
            <table>
                <thead>
                    <tr>
                        <th>Division</th>
                        <th>Land Area</th>
                        <th>Mean Rainfall</th>
                        <th>Daily Rate</th>
                        <th>Spread [Min, Max]</th>
                        <th>Total Rain Influx</th>
                        <th>YoY Change ({prev_date_str})</th>
                        <th>Condition</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </div>

        <footer>
            NASA Space Apps Challenge 2026 // Trend Detective • Data: NASA GPM IMERG & GMAO Satellite Precipitation
        </footer>
    </div>
</body>
</html>
"""
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)


def print_terminal_table(date_str: str, prev_date_str: str, results: dict):
    """Print an attractive ASCII summary table in the terminal."""
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    df = pd.DataFrame(list(results.values())).sort_values(by="mean_precip_mm", ascending=False)

    print("\n" + "=" * 86)
    print(f"  NASA EARTH DETECTIVE // DIVISIONAL PRECIPITATION AUDIT ({date_str})")
    print(f"  Year-over-Year Comparison Baseline: {prev_date_str if prev_date_str else 'N/A'}")
    print("=" * 86)
    print(f"{'Division':<14} | {'Area (km2)':<11} | {'Precip (mm)':<12} | {'Rate (mm/d)':<11} | {'Volume (km3)':<13} | {'Condition'}")
    print("-" * 86)

    for _, r in df.iterrows():
        print(f"{r['name']:<14} | {r['area_km2']:<11,g} | {r['mean_precip_mm']:>11.1f} | {r['daily_rate_mm_day']:>11.2f} | {r['water_volume_km3']:>12.3f} | {r['condition']}")

    print("=" * 86 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Analyze Bangladesh precipitation by division on a fixed month.")
    parser.add_argument("--month", type=str, default="latest",
                        help="Target month in YYYY-MM format (e.g. 2026-07) or 'latest' (default).")
    parser.add_argument("--nc-file", type=str, default="nasa_precipitation_bangladesh.nc",
                        help="Path to NetCDF dataset (auto-downloaded from NASA if not found).")
    parser.add_argument("--output-dir", type=str, default="outputs",
                        help="Directory to save generated JSON, CSV, PNG, and HTML reports.")

    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading Precipitation dataset: {args.nc_file} ...")
    ds = load_dataset(args.nc_file)
    precip_var = detect_precip_variable(ds)
    months = get_available_months(ds)

    if args.month.lower() == "latest":
        target_month_key = list(months.keys())[-1]
    else:
        target_month_key = args.month
        if target_month_key not in months:
            available_preview = ", ".join(list(months.keys())[-6:])
            print(f"[Error] Month '{args.month}' not found in dataset. Recent months available: {available_preview}", file=sys.stderr)
            sys.exit(1)

    time_idx, target_dt = months[target_month_key]
    date_str = target_dt.strftime("%B %Y")
    print(f"Analyzing precipitation for: {target_month_key} ({date_str}) [Timestep {time_idx + 1} of {len(months)}]")

    # Find previous year's month for YoY comparison
    prev_year_key = f"{target_dt.year - 1}-{target_dt.month:02d}"
    prev_time_idx = None
    prev_date_str = ""
    if prev_year_key in months:
        prev_time_idx, prev_dt = months[prev_year_key]
        prev_date_str = prev_dt.strftime("%B %Y")

    print("Extracting divisional boundaries and masking grid cells...")
    divisions = get_division_geometries()

    current_results = analyze_division_precip(ds, precip_var, time_idx, divisions)

    if prev_time_idx is not None:
        prev_results = analyze_division_precip(ds, precip_var, prev_time_idx, divisions)
        for name in current_results:
            cur_p = current_results[name]["mean_precip_mm"]
            prv_p = prev_results[name]["mean_precip_mm"]
            current_results[name]["yoy_delta_mm"] = round(cur_p - prv_p, 1)
            current_results[name]["prev_year_precip_mm"] = round(prv_p, 1)

    # 1. Output Terminal Table
    print_terminal_table(date_str, prev_date_str, current_results)

    # File paths
    base_prefix = f"divisional_precip_{target_month_key}"
    json_path = out_dir / f"{base_prefix}.json"
    csv_path = out_dir / f"{base_prefix}.csv"
    choropleth_path = out_dir / f"divisional_precip_choropleth_{target_month_key}.png"
    ranking_path = out_dir / f"divisional_precip_ranking_{target_month_key}.png"
    html_path = out_dir / f"divisional_precip_report_{target_month_key}.html"

    # 2. Export JSON
    payload = {
        "metadata": {
            "dataset": "NASA Satellite Precipitation (GPM IMERG & GMAO)",
            "target_month": target_month_key,
            "target_date_label": date_str,
            "prev_year_month": prev_year_key if prev_time_idx is not None else None,
            "prev_year_label": prev_date_str if prev_time_idx is not None else None,
            "generated_at": datetime.now().isoformat(),
            "variable": "Monthly Total Accumulated Precipitation",
            "unit": "mm/month"
        },
        "divisions": current_results
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f" Exported JSON: {json_path}")

    # 3. Export CSV
    df = pd.DataFrame(list(current_results.values()))
    df.to_csv(csv_path, index=False)
    print(f" Exported CSV:  {csv_path}")

    # 4. Generate Choropleth Map
    print(" Rendering Divisional Precipitation Choropleth Map...")
    plot_precip_choropleth(divisions, current_results, date_str, str(choropleth_path))
    print(f" Saved Map:     {choropleth_path}")

    # 5. Generate Ranking Chart
    print(" Rendering Divisional Precipitation Ranking Chart...")
    plot_precip_ranking(current_results, date_str, prev_date_str, str(ranking_path))
    print(f" Saved Chart:   {ranking_path}")

    # 6. Generate Standalone HTML Report
    print(" Generating Standalone HTML Executive Report...")
    generate_html_report(
        date_str=date_str,
        prev_date_str=prev_date_str,
        results=current_results,
        choropleth_filename=choropleth_path.name,
        ranking_filename=ranking_path.name,
        output_html_path=str(html_path)
    )
    print(f" Saved Report:  {html_path}")
    print("\n Precipitation Pipeline completed successfully.")


if __name__ == "__main__":
    main()
