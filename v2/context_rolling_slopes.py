"""
NASA Space Apps 2026 – Bengal Hydro Detective
Optional Context Analysis: Long-Term Rolling 5-Year TWS Slopes
=============================================================
STRICT SCIENTIFIC GUIDELINES:
  - Context ONLY; NOT used for headline claims.
  - GRACE/GRACE-FO satellite data only (no rainfall needed).
  - Calculates 5-year (60-month) rolling Theil-Sen slopes across the full mission record (2002–2026).
  - Marks the 11-month data gap between GRACE and GRACE-FO (June 2017 – June 2018).
  - Reports a bootstrap difference test comparing recent (post-2018-06) vs earlier (pre-2017-06) rolling 5-yr slopes.
  - Exploratory segmented regression break-point detection, labeled "CONTEXT ONLY".

Outputs:
  outputs/v2/fig_context_rolling_5yr_slopes.png
  outputs/v2/context_rolling_slopes_summary.json
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    from v2.config_loader import get_grace_netcdf_path, load_config
except ImportError:
    from config_loader import get_grace_netcdf_path, load_config

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "outputs" / "v2"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FIG_PATH = OUTPUT_DIR / "fig_context_rolling_5yr_slopes.png"
SUMMARY_PATH = OUTPUT_DIR / "context_rolling_slopes_summary.json"

REGIONS = ["NW", "NE", "Central", "SW", "SE"]
REG_COLORS = {
    "NW": "#dc2626",      # Crimson red
    "NE": "#8b5cf6",      # Vivid purple
    "Central": "#0284c7", # Sky blue
    "SW": "#059669",      # Emerald green
    "SE": "#ea580c",      # Amber orange
}

SEP = "═" * 84


def deseasonalise(y: np.ndarray, months: np.ndarray) -> np.ndarray:
    out = y.copy()
    for m in range(1, 13):
        mask = months == m
        if mask.sum() > 0:
            out[mask] -= np.nanmean(y[mask])
    return out


def compute_theil_sen_slope_fast(x: np.ndarray, y: np.ndarray) -> float:
    n = len(x)
    if n < 5:
        return np.nan
    idx_i, idx_j = np.triu_indices(n, k=1)
    dx = x[idx_j] - x[idx_i]
    dy = y[idx_j] - y[idx_i]
    valid = dx != 0
    if not np.any(valid):
        return np.nan
    slopes = dy[valid] / dx[valid]
    return float(np.median(slopes))


def segmented_regression_breakpoint(
    t_vals: np.ndarray, y_vals: np.ndarray, times_index: pd.DatetimeIndex
) -> dict:
    """
    Exploratory segmented regression: search for the break-point (every 6 months,
    2004-01 to 2023-01) that minimises the combined residual sum of squares of two
    OLS lines fitted before and after the candidate break.

    Returns a dict with the best break year-month, slopes before/after, and an
    exploratory note.  CONTEXT ONLY — not used for headline claims.
    """
    candidates = pd.date_range("2004-01-01", "2023-01-01", freq="6MS")
    best_rss = np.inf
    best_ym = None
    best_slope_before = np.nan
    best_slope_after = np.nan

    for bp in candidates:
        mask_before = times_index < bp
        mask_after = times_index >= bp
        if mask_before.sum() < 6 or mask_after.sum() < 6:
            continue
        tb, yb = t_vals[mask_before], y_vals[mask_before]
        ta, ya = t_vals[mask_after], y_vals[mask_after]

        # OLS fit for each segment
        def _ols_rss(tx, yx):
            A = np.column_stack([tx, np.ones_like(tx)])
            coef, _, _, _ = np.linalg.lstsq(A, yx, rcond=None)
            resid = yx - A @ coef
            return float(np.sum(resid ** 2)), float(coef[0])

        rss_b, sl_b = _ols_rss(tb, yb)
        rss_a, sl_a = _ols_rss(ta, ya)
        total_rss = rss_b + rss_a

        if total_rss < best_rss:
            best_rss = total_rss
            best_ym = bp.strftime("%Y-%m")
            best_slope_before = sl_b
            best_slope_after = sl_a

    return {
        "exploratory_segmented_regression_breakpoint_ym": best_ym,
        "exploratory_slope_before_cm_yr": float(best_slope_before),
        "exploratory_slope_after_cm_yr": float(best_slope_after),
        "exploratory_note": (
            "CONTEXT ONLY — segmented regression is exploratory; "
            "not used for headline claims"
        ),
    }


def run_context_analysis():
    print(SEP)
    print("  OPTIONAL CONTEXT ANALYSIS: FULL-MISSION ROLLING 5-YEAR TWS SLOPES")
    print("  GRACE/GRACE-FO Long-Term Context (2002–2026)  |  STATUS: CONTEXT ONLY")
    print(SEP)

    grace_path = get_grace_netcdf_path()
    if grace_path is None or not grace_path.exists():
        print("\n[LOUD NOTICE] GRACE NetCDF is not currently available.")
        print("  The Optional Context Figure requires the full mission NetCDF (2002–2026).")
        print("  To enable this optional visual:")
        print("    1. Place 'CSR_GRACE_GRACE-FO_RL0603_Mascons_all-corrections.nc' in repository root, OR")
        print("    2. Set 'grace_netcdf_path' in config.json, OR")
        print("    3. Export GRACE_NETCDF_PATH=/path/to/file.nc\n")
        print("  Headline results (2020-01 to 2026-07) remain complete and unaffected.")
        print(SEP)
        return

    print(f"\n[OK] Found GRACE NetCDF: {grace_path.name}")
    print("Extracting full mission monthly mascon record for Bangladesh regions...")

    # Load dataset
    import xarray as xr
    import shapely.geometry
    import pyproj

    with open(REPO_ROOT / "bangladesh_divisions.geojson", "r", encoding="utf-8") as f:
        gj = json.load(f)

    # Load regional groupings
    div_geoms = {feat["properties"]["name"]: shapely.geometry.shape(feat["geometry"]) for feat in gj["features"]}
    reg_divs = {
        "NW": ["Rajshahi", "Rangpur"],
        "NE": ["Sylhet", "Mymensingh"],
        "Central": ["Dhaka"],
        "SW": ["Khulna", "Barishal"],
        "SE": ["Chattogram"],
    }

    ds = xr.open_dataset(str(grace_path), decode_times=False)
    if "Units" in ds["time"].attrs and "units" not in ds["time"].attrs:
        ds["time"].attrs["units"] = ds["time"].attrs["Units"]
    ds = xr.decode_cf(ds)

    # --- Assert lwe_thickness units ---
    lwe_units = ds["lwe_thickness"].attrs.get(
        "units", ds["lwe_thickness"].attrs.get("Units", "NOT_FOUND")
    )
    print(f"  lwe_thickness units: '{lwe_units}'")
    if not ("cm" in str(lwe_units).lower() or "centimeter" in str(lwe_units).lower()):
        raise ValueError(
            f"lwe_thickness units are '{lwe_units}' — expected 'cm' or 'centimeter'. "
            "Check the NetCDF file; slopes and CIs assume centimetres."
        )

    times = pd.to_datetime(ds["time"].values)
    lwe = ds["lwe_thickness"].values  # (time, lat, lon)
    lats = ds["lat"].values
    lons = ds["lon"].values

    # Convert lons to -180..180 if needed
    if np.any(lons > 180):
        lons_180 = np.where(lons > 180, lons - 360, lons)
    else:
        lons_180 = lons

    # Crop to Bangladesh bounding box (+ buffer) for fast vectorized extraction
    lon_idx = (lons_180 >= 87.0) & (lons_180 <= 93.5)
    lat_idx = (lats >= 20.0) & (lats <= 27.5)

    sub_lons = lons_180[lon_idx]
    sub_lats = lats[lat_idx]
    sub_lwe = lwe[:, lat_idx, :][:, :, lon_idx]  # (time, sub_lat, sub_lon)

    lat_mesh, lon_mesh = np.meshgrid(sub_lats, sub_lons, indexing="ij")
    cos_lat = np.cos(np.deg2rad(lat_mesh))

    # Regional series extraction
    reg_series = {r: [] for r in REGIONS}
    for r_name, d_names in reg_divs.items():
        polys = [div_geoms[d] for d in d_names if d in div_geoms]
        from shapely.ops import unary_union
        reg_poly = unary_union(polys)

        # Build mask using vectorized contains_xy
        mask = shapely.contains_xy(reg_poly, lon_mesh, lat_mesh)

        if not np.any(mask):
            # Fallback centroid nearest
            c = reg_poly.centroid
            dist = (lat_mesh - c.y)**2 + (lon_mesh - c.x)**2
            min_idx = np.unravel_index(np.argmin(dist), dist.shape)
            mask[min_idx] = True

        weights = cos_lat * mask
        w_sum = np.sum(weights)

        ts = []
        for t_idx in range(len(times)):
            grid_t = sub_lwe[t_idx, :, :]
            val = np.sum(grid_t * weights) / w_sum
            ts.append(val)
        reg_series[r_name] = np.array(ts)

    df_full = pd.DataFrame(reg_series, index=times)
    df_full["year"] = df_full.index.year
    df_full["month"] = df_full.index.month

    # Calculate 5-year rolling slopes (60-month window)
    window_len = 60
    rolling_results = []
    recent_comparison = {}

    for r_name in REGIONS:
        y_raw = df_full[r_name].values
        months = df_full["month"].values
        y_deseas = deseasonalise(y_raw, months)
        t_years = df_full.index.year + (df_full.index.month - 0.5) / 12.0
        t_vals = t_years.values

        # Rolling 5-year slopes
        slopes_r = []
        slope_dates = []
        for start_idx in range(0, len(t_vals) - window_len + 1):
            end_idx = start_idx + window_len
            t_win = t_vals[start_idx:end_idx]
            y_win = y_deseas[start_idx:end_idx]
            mid_date = df_full.index[start_idx + window_len // 2]
            sl = compute_theil_sen_slope_fast(t_win, y_win)
            slopes_r.append(sl)
            slope_dates.append(mid_date)

        # Recent slope (2018-06 to 2026-07)
        mask_recent = (df_full.index >= "2018-06") & (df_full.index <= "2026-07")
        t_rec = t_vals[mask_recent]
        y_rec = y_deseas[mask_recent]
        recent_slope = compute_theil_sen_slope_fast(t_rec, y_rec)

        # Residual circular block-bootstrap CI for recent slope
        n_rec = len(t_rec)
        res_rec = stats.theilslopes(y_rec, t_rec)
        recent_slope = float(res_rec.slope)
        recent_intercept = float(res_rec.intercept)
        rec_residuals = y_rec - (recent_intercept + recent_slope * t_rec)
        rec_residuals -= np.mean(rec_residuals)

        boot_slopes = []
        rng = np.random.default_rng(42)
        b_len = 12
        res_circ = np.concatenate([rec_residuals, rec_residuals[: b_len - 1]])
        n_blocks = int(np.ceil(n_rec / b_len))
        for _ in range(2000):
            starts = rng.integers(0, n_rec, size=n_blocks)
            block_offsets = np.arange(b_len)
            boot_idx = (starts[:, None] + block_offsets[None, :]).reshape(-1)[:n_rec]
            boot_e = res_circ[boot_idx]
            boot_y = (recent_intercept + recent_slope * t_rec) + boot_e
            boot_sl = compute_theil_sen_slope_fast(t_rec, boot_y)
            boot_slopes.append(boot_sl)
        ci_low = float(np.percentile(boot_slopes, 2.5))
        ci_high = float(np.percentile(boot_slopes, 97.5))

        # Comparison with earlier rolling slopes (pre-2017-06) — bootstrap difference test
        pre_gap_mask = [d < pd.Timestamp("2017-06-01") for d in slope_dates]
        pre_slopes = np.array(slopes_r)[pre_gap_mask]

        post_gap_mask = [d > pd.Timestamp("2018-06-01") for d in slope_dates]
        recent_slopes_arr = np.array(slopes_r)[post_gap_mask]

        # Keep finite values only
        pre_slopes = pre_slopes[np.isfinite(pre_slopes)]
        recent_slopes_arr = recent_slopes_arr[np.isfinite(recent_slopes_arr)]

        median_pre = float(np.median(pre_slopes)) if len(pre_slopes) > 0 else np.nan
        min_pre = float(np.min(pre_slopes)) if len(pre_slopes) > 0 else np.nan
        max_pre = float(np.max(pre_slopes)) if len(pre_slopes) > 0 else np.nan

        observed_diff = float(np.mean(recent_slopes_arr) - np.mean(pre_slopes))

        rng2 = np.random.default_rng(123)
        B = 2000
        boot_diffs = []
        n_pre = len(pre_slopes)
        n_rec_arr = len(recent_slopes_arr)
        for _ in range(B):
            samp_rec = recent_slopes_arr[rng2.integers(0, n_rec_arr, size=n_rec_arr)]
            samp_pre = pre_slopes[rng2.integers(0, n_pre, size=n_pre)]
            boot_diffs.append(float(np.mean(samp_rec) - np.mean(samp_pre)))
        diff_ci_low = float(np.percentile(boot_diffs, 2.5))
        diff_ci_high = float(np.percentile(boot_diffs, 97.5))

        ci_includes_zero = (diff_ci_low <= 0 <= diff_ci_high)
        if ci_includes_zero:
            pace_verdict = (
                "No clear evidence of acceleration or deceleration "
                "(bootstrap 95% CI includes zero)"
            )
        elif diff_ci_high < 0:
            pace_verdict = (
                "Recent slopes lower (more negative) than earlier period "
                "(bootstrap CI excludes zero)"
            )
        else:
            pace_verdict = (
                "Recent slopes higher (less negative) than earlier period "
                "(bootstrap CI excludes zero)"
            )

        print(f"  [{r_name}] pace_verdict: {pace_verdict}")

        # Exploratory segmented regression
        seg_result = segmented_regression_breakpoint(t_vals, y_deseas, df_full.index)

        recent_comparison[r_name] = {
            "recent_slope_2018_2026_cm_yr": float(recent_slope),
            "recent_95ci_cm_yr": [ci_low, ci_high],
            "earlier_rolling_5yr_median_cm_yr": median_pre,
            "earlier_rolling_5yr_range_cm_yr": [min_pre, max_pre],
            "pace_diff_mean_cm_yr": observed_diff,
            "pace_diff_95ci_cm_yr": [diff_ci_low, diff_ci_high],
            "pace_verdict": pace_verdict,
            **seg_result,
        }

        for d, sl in zip(slope_dates, slopes_r):
            rolling_results.append({
                "region": r_name,
                "mid_date": d.strftime("%Y-%m"),
                "rolling_5yr_theil_sen_cm_yr": float(sl)
            })

    # Render figure
    fig, axes = plt.subplots(len(REGIONS), 1, figsize=(12, 14), sharex=True)
    for ax, r_name in zip(axes, REGIONS):
        df_r = pd.DataFrame([r for r in rolling_results if r["region"] == r_name])
        df_r["mid_date"] = pd.to_datetime(df_r["mid_date"])

        ax.plot(df_r["mid_date"], df_r["rolling_5yr_theil_sen_cm_yr"],
                color=REG_COLORS[r_name], linewidth=2.0, label=f"{r_name} 5-Year Rolling Slope")
        ax.axhline(0, color="#64748b", linestyle=":", linewidth=1.0)

        # Mark 2017-2018 gap
        ax.axvspan(pd.Timestamp("2017-06-01"), pd.Timestamp("2018-06-01"),
                   color="#cbd5e1", alpha=0.5, label="2017–18 Mission Transition Gap (11 mos)")

        # Benchmark horizontal line for recent 2018-2026 slope
        rec_info = recent_comparison[r_name]
        r_sl = rec_info["recent_slope_2018_2026_cm_yr"]
        ci_l, ci_h = rec_info["recent_95ci_cm_yr"]
        verdict_label = rec_info["pace_verdict"]
        if len(verdict_label) > 60:
            verdict_label = verdict_label[:57] + "..."
        ax.axhline(r_sl, color="#0f172a", linestyle="--", linewidth=1.6,
                   label=(
                       f"2018–2026 Rate: {r_sl:+.2f} cm/yr [{ci_l:+.2f}, {ci_h:+.2f}]\n"
                       f"  {verdict_label}"
                   ))

        ax.set_ylabel(f"{r_name}\n(cm / yr)", fontsize=9.5, fontweight="bold")
        ax.grid(True, linestyle=":", alpha=0.5)
        ax.legend(loc="upper left", fontsize=8.0, framealpha=0.9)

    axes[-1].set_xlabel("Window Mid-Point Year", fontsize=11, fontweight="bold")
    plt.suptitle(
        "LONG-TERM CONTEXT ONLY — NOT USED FOR HEADLINE CLAIMS\n"
        "5-Year Rolling Theil-Sen Slopes of Regional Total Water Storage (2002–2026)\n"
        "CSR GRACE/GRACE-FO Mascons • Shaded Area Marks GRACE to GRACE-FO Transition Gap",
        fontsize=12, fontweight="bold", y=0.99
    )

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(FIG_PATH, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  Saved figure: {FIG_PATH}")

    # Save summary
    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "status": "CONTEXT ONLY — NOT USED FOR HEADLINE CLAIMS",
            "regional_pace_comparison": recent_comparison
        }, f, indent=2)
    print(f"  Saved summary: {SUMMARY_PATH}")
    print(SEP)


if __name__ == "__main__":
    run_context_analysis()
