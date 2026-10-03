"""
NASA Space Apps 2026 - Trend Detective: Bengal Water Paradox
Divisional Analysis MVP Pipeline

Extracts, analyzes, and visualizes Terrestrial Water Storage (TWS) anomalies
across Bangladesh administrative divisions for any specified month using CSR GRACE/GRACE-FO Mascons.

Usage:
    python analyze_divisions.py [--month YYYY-MM] [--output-dir DIR] [--nc-file PATH]
Example:
    python analyze_divisions.py --month 2026-07
"""

import os
import sys
import argparse
import json
import base64
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


def load_dataset(nc_file_path: str):
    """Load NetCDF and decode time attributes according to CF convention."""
    if not os.path.exists(nc_file_path):
        raise FileNotFoundError(f"NetCDF dataset not found at: {nc_file_path}")

    ds = xr.open_dataset(nc_file_path, decode_times=False)
    if "Units" in ds["time"].attrs and "units" not in ds["time"].attrs:
        ds["time"].attrs["units"] = ds["time"].attrs["Units"]
    ds = xr.decode_cf(ds)
    return ds


def get_available_months(ds):
    """Return dictionary of { 'YYYY-MM': time_index }."""
    months = {}
    for idx, t in enumerate(ds["time"].values):
        dt = pd.to_datetime(t)
        key = dt.strftime("%Y-%m")
        months[key] = (idx, dt)
    return months


def get_division_geometries():
    """Extract official administrative division boundaries for Bangladesh from Natural Earth."""
    shp_path = shpreader.natural_earth("10m", "cultural", "admin_1_states_provinces")
    reader = shpreader.Reader(shp_path)
    divisions = {}
    geod = pyproj.Geod(ellps="WGS84")

    for rec in reader.records():
        if rec.attributes.get("admin") == "Bangladesh":
            raw_name = rec.attributes.get("name")
            # Standardize names
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


def classify_status(anomaly_cm: float) -> str:
    """Classify water storage condition based on LWE anomaly magnitude."""
    if anomaly_cm <= -15.0:
        return "Severe Deficit"
    elif anomaly_cm <= -5.0:
        return "Moderate Deficit"
    elif anomaly_cm <= 5.0:
        return "Normal / Balanced"
    elif anomaly_cm <= 15.0:
        return "Moderate Surplus"
    else:
        return "High Surplus"


def analyze_month(ds, time_idx: int, divisions: dict):
    """Calculate division-level statistics for a single month index."""
    # Slice Bangladesh bounding box: 20.4N to 26.8N, 88.0E to 92.8E
    bd_sub = ds["lwe_thickness"].isel(time=time_idx).sel(lat=slice(20.4, 26.8), lon=slice(88.0, 92.8))
    
    lon2d, lat2d = np.meshgrid(bd_sub.lon.values, bd_sub.lat.values)
    lat_rad = np.radians(lat2d)
    area_weights = np.cos(lat_rad)
    
    results = {}
    data_values = bd_sub.values

    for name, div in divisions.items():
        geom = div["geometry"]
        mask = shapely.contains_xy(geom, lon2d, lat2d)
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

        # Calculate volume anomaly in km³:
        # Area (m²) * depth (m) * 1e-9 = km³ (1 cm = 0.01 m)
        vol_km3 = div["area_m2"] * (w_mean * 0.01) * 1e-9

        results[name] = {
            "name": name,
            "area_km2": round(div["area_km2"], 1),
            "cell_count": cell_count,
            "mean_anomaly_cm": round(w_mean, 2),
            "min_anomaly_cm": round(min_val, 2),
            "max_anomaly_cm": round(max_val, 2),
            "std_anomaly_cm": round(std_val, 2),
            "volume_km3": round(vol_km3, 3),
            "status": classify_status(w_mean)
        }
    return results


def plot_choropleth(divisions: dict, results: dict, date_str: str, output_path: str):
    """Generate high-resolution choropleth map of Bangladesh divisions."""
    fig = plt.figure(figsize=(9, 10))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([87.8, 93.0, 20.4, 26.8], crs=ccrs.PlateCarree())

    norm = mcolors.Normalize(vmin=-25, vmax=25)
    cmap = plt.cm.RdBu

    for name, div in divisions.items():
        val = results[name]["mean_anomaly_cm"]
        color = cmap(norm(val))
        ax.add_geometries(
            [div["geometry"]],
            crs=ccrs.PlateCarree(),
            facecolor=color,
            edgecolor="#1e293b",
            linewidth=1.2
        )
        
        # Add division label and value annotation
        centroid = div["geometry"].centroid
        # Slight label nudges for tight geography
        cx, cy = centroid.x, centroid.y
        if name == "Barishal":
            cy -= 0.1
        elif name == "Dhaka":
            cx -= 0.1
            cy += 0.05
        elif name == "Sylhet":
            cy += 0.1

        ax.text(
            cx, cy,
            f"{name}\n{val:+.1f} cm",
            transform=ccrs.PlateCarree(),
            ha="center", va="center",
            fontsize=8.5, fontweight="bold",
            color="#0f172a" if abs(val) < 18 else "white",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.65, edgecolor="none")
        )

    # Cartographic features
    ax.coastlines(resolution="10m", color="#334155", linewidth=1.0)
    ax.add_feature(cfeature.RIVERS, edgecolor="#38bdf8", linewidth=0.7, alpha=0.6)
    
    gl = ax.gridlines(draw_labels=True, dms=False, x_inline=False, y_inline=False, alpha=0.25)
    gl.top_labels = False
    gl.right_labels = False

    # Colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(
        sm, ax=ax, orientation="vertical", pad=0.04, shrink=0.8, extend="both"
    )
    cbar.set_label("Division Mean Water Storage Anomaly (cm)", fontsize=10, labelpad=8)

    plt.title(
        f"Bangladesh Terrestrial Water Storage Anomaly by Division\nCSR GRACE / GRACE-FO Mascon — {date_str}",
        fontsize=12, fontweight="bold", pad=14
    )

    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_ranking(results: dict, date_str: str, prev_date_str: str, output_path: str):
    """Generate comparative ranking chart with Year-over-Year changes."""
    df = pd.DataFrame(list(results.values()))
    df = df.sort_values(by="mean_anomaly_cm", ascending=True)

    fig, ax = plt.subplots(figsize=(11, 6.2))

    colors = []
    for val in df["mean_anomaly_cm"]:
        if val <= -10:
            colors.append("#b91c1c")  # Red
        elif val < 0:
            colors.append("#f97316")  # Amber/Orange
        elif val < 10:
            colors.append("#38bdf8")  # Sky Blue
        else:
            colors.append("#0369a1")  # Darker Blue

    bars = ax.barh(df["name"], df["mean_anomaly_cm"], color=colors, edgecolor="#1e293b", height=0.62)
    ax.axvline(0, color="#475569", linestyle="--", linewidth=1.0, alpha=0.8)

    # Annotate bars with values and YoY delta
    for bar, (_, row) in zip(bars, df.iterrows()):
        val = row["mean_anomaly_cm"]
        yoy = row.get("yoy_delta_cm", None)
        vol = row["volume_km3"]
        
        yoy_text = f" (YoY: {yoy:+.1f} cm)" if yoy is not None else ""
        label_text = f" {val:+.1f} cm | {vol:+.2f} km³{yoy_text} "

        if val >= 0:
            ax.text(val + 0.4, bar.get_y() + bar.get_height() / 2, label_text,
                    va="center", ha="left", fontsize=8.5, fontweight="600")
        else:
            ax.text(val - 0.4, bar.get_y() + bar.get_height() / 2, label_text,
                    va="center", ha="right", fontsize=8.5, fontweight="600")

    ax.set_xlabel("Mean Liquid Water Equivalent Anomaly (cm)", fontsize=11, fontweight="bold")
    ax.set_title(
        f"Divisional Water Storage Anomaly Ranking ({date_str})\n"
        f"Comparison baseline against {prev_date_str if prev_date_str else 'N/A'}",
        fontsize=12, fontweight="bold", pad=12
    )
    
    # Expand x-limits to comfortably accommodate annotations without clipping
    min_x = min(df["mean_anomaly_cm"].min() - 22, -28)
    max_x = max(df["mean_anomaly_cm"].max() + 20, 28)
    ax.set_xlim(min_x, max_x)
    ax.grid(axis="x", linestyle=":", alpha=0.5)

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)



def generate_html_report(date_str: str, prev_date_str: str, results: dict,
                         choropleth_filename: str, ranking_filename: str,
                         output_html_path: str):
    """Generate a clean, standalone HTML executive report in the Trend Detective aesthetic."""
    df = pd.DataFrame(list(results.values())).sort_values(by="mean_anomaly_cm", ascending=True)

    # National average calculation
    total_area = sum(r["area_km2"] for r in results.values())
    national_mean = sum(r["mean_anomaly_cm"] * r["area_km2"] for r in results.values()) / total_area
    total_vol = sum(r["volume_km3"] for r in results.values())

    table_rows = ""
    for _, r in df.iterrows():
        status_color = "#dc2626" if "Deficit" in r["status"] else "#0284c7" if "Surplus" in r["status"] else "#16a34a"
        yoy_str = f"{r.get('yoy_delta_cm', 0.0):+.2f} cm" if "yoy_delta_cm" in r else "N/A"
        yoy_color = "#dc2626" if r.get('yoy_delta_cm', 0.0) < 0 else "#16a34a"

        table_rows += f"""
        <tr>
            <td style="font-weight: 700; color: #0f172a;">{r['name']}</td>
            <td>{r['area_km2']:,} km²</td>
            <td style="font-weight: 700; color: {status_color};">{r['mean_anomaly_cm']:+.2f} cm</td>
            <td>[{r['min_anomaly_cm']:+.1f}, {r['max_anomaly_cm']:+.1f}]</td>
            <td>{r['volume_km3']:+.3f} km³</td>
            <td style="font-weight: 600; color: {yoy_color};">{yoy_str}</td>
            <td><span class="badge" style="background: {status_color}20; color: {status_color}; border: 1px solid {status_color};">{r['status']}</span></td>
        </tr>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NASA Earth Detective — Divisional Water Storage Report ({date_str})</title>
    <link href="https://fonts.googleapis.com/css2?family=Architects+Daughter&family=Inter:wght@400;600;700&family=Permanent+Marker&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: #ffffff;
            --ink-dark: #1e293b;
            --ink-red: #dc2626;
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
            letter-spacing: 1px;
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
                <div style="font-family: 'Architects Daughter', cursive; color: #94a3b8; font-size: 1rem;">Case File #026-BD // Executive Report</div>
                <h1>The Bengal Water Paradox</h1>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 0.85rem; color: #94a3b8;">Observation Month</div>
                <div style="font-size: 1.25rem; font-weight: 700; color: #38bdf8;">{date_str}</div>
            </div>
        </header>

        <div class="nav-bar">
            <span style="font-size: 0.85rem; color: #94a3b8; font-weight: 600;">Explore Key Seasons:</span>
            <a href="divisional_report_2025-12.html" class="nav-pill {'active' if 'December 2025' in date_str else ''}">❄️ Dec 2025 (Dry Winter)</a>
            <a href="divisional_report_2026-03.html" class="nav-pill {'active' if 'March 2026' in date_str else ''}">🌱 Mar 2026 (Boro Irrigation)</a>
            <a href="divisional_report_2026-07.html" class="nav-pill {'active' if 'July 2026' in date_str else ''}">🌊 Jul 2026 (Monsoon Peak)</a>
        </div>


        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">National Mean Anomaly</div>
                <div class="kpi-val" style="color: {'#dc2626' if national_mean < 0 else '#38bdf8'};">{national_mean:+.2f} cm</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Net Water Volume Balance</div>
                <div class="kpi-val" style="color: {'#dc2626' if total_vol < 0 else '#38bdf8'};">{total_vol:+.2f} km³</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Most Depleted Division</div>
                <div class="kpi-val" style="color: #dc2626;">{df.iloc[0]['name']} ({df.iloc[0]['mean_anomaly_cm']:+.1f} cm)</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Highest Surplus Division</div>
                <div class="kpi-val" style="color: #0284c7;">{df.iloc[-1]['name']} ({df.iloc[-1]['mean_anomaly_cm']:+.1f} cm)</div>
            </div>
        </div>

        <div class="card">
            <div class="section-title">Visual Evidence: Spatial Choropleth & Divisional Ranking</div>
            <div class="grid-2">
                <div>
                    <h4 style="margin: 0 0 10px 0; color: #475569;">Spatial Choropleth Map</h4>
                    <img class="report-img" src="{choropleth_filename}" alt="Divisional Choropleth Map">
                </div>
                <div>
                    <h4 style="margin: 0 0 10px 0; color: #475569;">Comparative Anomaly Ranking</h4>
                    <img class="report-img" src="{ranking_filename}" alt="Divisional Ranking Chart">
                </div>
            </div>
        </div>

        <div class="card">
            <div class="section-title">Divisional Quantitative Audit Table</div>
            <table>
                <thead>
                    <tr>
                        <th>Division</th>
                        <th>Land Area</th>
                        <th>Mean LWE Anomaly</th>
                        <th>Range [Min, Max]</th>
                        <th>Net Volume Anomaly</th>
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
            NASA Space Apps Challenge 2026 // Trend Detective Pipeline • Data: CSR GRACE/GRACE-FO RL06.3 Mascons
        </footer>
    </div>
</body>
</html>
"""
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)


def print_terminal_table(date_str: str, prev_date_str: str, results: dict):
    """Print an attractive ASCII summary table directly in the terminal."""
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    df = pd.DataFrame(list(results.values())).sort_values(by="mean_anomaly_cm", ascending=True)

    print("\n" + "=" * 84)
    print(f"  NASA EARTH DETECTIVE // DIVISIONAL WATER STORAGE AUDIT ({date_str})")
    print(f"  Year-over-Year Comparison Baseline: {prev_date_str if prev_date_str else 'N/A'}")
    print("=" * 84)
    print(f"{'Division':<14} | {'Area (km2)':<11} | {'Mean (cm)':<10} | {'Volume (km3)':<13} | {'YoY Chg(cm)':<11} | {'Status'}")
    print("-" * 84)

    for _, r in df.iterrows():
        yoy_str = f"{r.get('yoy_delta_cm', 0.0):+.2f}" if "yoy_delta_cm" in r else "N/A"
        print(f"{r['name']:<14} | {r['area_km2']:<11,g} | {r['mean_anomaly_cm']:>+9.2f} | {r['volume_km3']:>+12.3f} | {yoy_str:>11} | {r['status']}")

    print("=" * 84 + "\n")



def main():
    parser = argparse.ArgumentParser(description="Analyze Bangladesh water storage by division on a fixed month.")
    parser.add_argument("--month", type=str, default="latest",
                        help="Target month in YYYY-MM format (e.g. 2026-07) or 'latest' (default).")
    parser.add_argument("--nc-file", type=str, default="CSR_GRACE_GRACE-FO_RL0603_Mascons_all-corrections.nc",
                        help="Path to CSR GRACE mascon NetCDF file.")
    parser.add_argument("--output-dir", type=str, default="outputs",
                        help="Directory to save generated JSON, CSV, PNG, and HTML reports.")

    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading GRACE NetCDF dataset: {args.nc_file} ...")
    ds = load_dataset(args.nc_file)
    months = get_available_months(ds)

    # Resolve target month
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
    print(f"Analyzing month: {target_month_key} ({date_str}) [Timestep {time_idx + 1} of {len(months)}]")

    # Find previous year's month for Year-over-Year (YoY) comparison
    prev_year_key = f"{target_dt.year - 1}-{target_dt.month:02d}"
    prev_time_idx = None
    prev_date_str = ""
    if prev_year_key in months:
        prev_time_idx, prev_dt = months[prev_year_key]
        prev_date_str = prev_dt.strftime("%B %Y")

    print("Extracting divisional boundaries and masking grid cells...")
    divisions = get_division_geometries()

    # Compute current month metrics
    current_results = analyze_month(ds, time_idx, divisions)

    # Compute previous year metrics and YoY deltas
    if prev_time_idx is not None:
        prev_results = analyze_month(ds, prev_time_idx, divisions)
        for name in current_results:
            cur_mean = current_results[name]["mean_anomaly_cm"]
            prv_mean = prev_results[name]["mean_anomaly_cm"]
            current_results[name]["yoy_delta_cm"] = round(cur_mean - prv_mean, 2)
            current_results[name]["prev_year_mean_cm"] = round(prv_mean, 2)

    # 1. Output Formatted Terminal Table
    print_terminal_table(date_str, prev_date_str, current_results)

    # File paths
    base_prefix = f"divisional_analysis_{target_month_key}"
    json_path = out_dir / f"{base_prefix}.json"
    csv_path = out_dir / f"{base_prefix}.csv"
    choropleth_path = out_dir / f"divisional_choropleth_{target_month_key}.png"
    ranking_path = out_dir / f"divisional_ranking_{target_month_key}.png"
    html_path = out_dir / f"divisional_report_{target_month_key}.html"

    # 2. Export JSON
    payload = {
        "metadata": {
            "dataset": "CSR GRACE/GRACE-FO RL06.3 Mascons",
            "target_month": target_month_key,
            "target_date_label": date_str,
            "prev_year_month": prev_year_key if prev_time_idx is not None else None,
            "prev_year_label": prev_date_str if prev_time_idx is not None else None,
            "generated_at": datetime.now().isoformat(),
            "variable": "Liquid Water Equivalent (LWE) thickness anomaly",
            "unit": "cm"
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

    # 4. Generate Choropleth Plot
    print(" Rendering Divisional Choropleth Map...")
    plot_choropleth(divisions, current_results, date_str, str(choropleth_path))
    print(f" Saved Map:     {choropleth_path}")

    # 5. Generate Ranking Chart
    print(" Rendering Divisional Ranking Chart...")
    plot_ranking(current_results, date_str, prev_date_str, str(ranking_path))
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
    print("\n MVP Pipeline completed successfully.")


if __name__ == "__main__":
    main()
