"""
NASA Space Apps Challenge 2026 — Team Tenstral
"Be An Earth System Trend Detective!"
Bengal Hydro Detective v2: End-to-End Analysis Pipeline
======================================================
Master entry point executing all analytical stages sequentially:
  1. Data Audit: Coverage, missing months, units, and fallback auditing.
  2. Spatial Aggregation: Geodesic area-weighted regional (5) and divisional (8) series.
  3. Trend Engine v2: Hamed-Rao modified Mann-Kendall and circular block-bootstrap Theil-Sen CIs.
  4. Sensitivity Analysis: Boundary perturbation (±1, ±2 yrs), rolling slopes, and window comparisons.
  5. Regional Comparison: Pairwise bootstrap slope difference tests and Benjamini-Hochberg FDR control.
  6. Rainfall vs Storage Coupling: 2×2 diagnostic matrix, lag cross-correlation, and seasonal budget.
  7. Visualization & Deliverables: Standardized results.csv, results.json, and publication-ready figures.
  8. Narrative Synthesis: Rule-based scientific interpretation in English and Bangla with limits.

Usage:
    python run_all.py
    python run_all.py --start 2020-01 --end 2026-07 --seed 42
"""

import argparse
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parent
V2_DIR = REPO_ROOT / "v2"
OUTPUTS_V2 = REPO_ROOT / "outputs" / "v2"

TASKS = [
    (1, "Data Audit", V2_DIR / "task1_data_audit.py"),
    (2, "Regional Series Aggregation", V2_DIR / "task2_regional_series.py"),
    (3, "Trend Engine v2 (Hamed-Rao + Block-Bootstrap)", V2_DIR / "task3_trend_engine.py"),
    (4, "Sensitivity & Robustness Analysis", V2_DIR / "task4_sensitivity.py"),
    (5, "Regional Comparison & FDR Control", V2_DIR / "task5_region_comparison.py"),
    (6, "Rain vs Storage Coupling & Budget", V2_DIR / "task6_rain_vs_storage.py"),
    (7, "Comprehensive Outputs & Figures Suite", V2_DIR / "task7_outputs.py"),
    (8, "Rule-Based Narrative Synthesis (EN & BN)", V2_DIR / "task8_narrative.py"),
]

BANNER = "═" * 84


def run_task(task_num: int, task_name: str, script_path: Path, env: dict) -> float:
    print("\n" + BANNER)
    print(f"  RUNNING TASK {task_num} / 8: {task_name.upper()}")
    print(f"  Script: {script_path.relative_to(REPO_ROOT)}")
    print(BANNER + "\n")
    
    t0 = time.time()
    cmd = [sys.executable, "-X", "utf8", str(script_path)]
    result = subprocess.run(cmd, cwd=str(REPO_ROOT), env=env)
    elapsed = time.time() - t0
    
    if result.returncode != 0:
        print(f"\n[ERROR] Task {task_num} ({task_name}) failed with exit code {result.returncode}!")
        sys.exit(result.returncode)
        
    print(f"\n[OK] Task {task_num} completed in {elapsed:.2f} seconds.")
    return elapsed


def main():
    parser = argparse.ArgumentParser(
        description="Bengal Hydro Detective v2 — NASA Space Apps 2026 Pipeline"
    )
    parser.add_argument("--start", type=str, default="2020-01", help="Primary start month (YYYY-MM)")
    parser.add_argument("--end", type=str, default="2026-07", help="Primary end month (YYYY-MM)")
    parser.add_argument("--seed", type=int, default=42, help="Fixed random seed for bootstrap replicability")
    parser.add_argument("--grace-nc", type=str, default=None, help="Path to CSR GRACE/GRACE-FO Mascon NetCDF")
    args = parser.parse_args()

    try:
        from v2.config_loader import get_grace_netcdf_path
    except ImportError:
        from config_loader import get_grace_netcdf_path

    grace_path = get_grace_netcdf_path(args.grace_nc)

    print(BANNER)
    print("  NASA SPACE APPS CHALLENGE 2026 — TEAM TENSTRAL")
    print("  'BE AN EARTH SYSTEM TREND DETECTIVE!'")
    print("  Bengal Hydro Detective v2 Pipeline Execution")
    print(f"  Primary Window : {args.start} to {args.end}")
    print(f"  Random Seed    : {args.seed} (deterministic bootstrap)")
    print(f"  GRACE NetCDF   : {grace_path if grace_path else '[ABSENT — Single Window (Primary) Active; No Duplicate Rows]'}")
    print(f"  Timestamp      : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Output Dir     : {OUTPUTS_V2}")
    print(BANNER)

    OUTPUTS_V2.mkdir(parents=True, exist_ok=True)

    # Set environment variables for parameters
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    env["ANALYSIS_START_DATE"] = args.start
    env["ANALYSIS_END_DATE"] = args.end
    env["ANALYSIS_RANDOM_SEED"] = str(args.seed)
    if grace_path:
        env["GRACE_NETCDF_PATH"] = str(grace_path)

    timings = {}
    t_start = time.time()

    for task_num, task_name, script_path in TASKS:
        elapsed = run_task(task_num, task_name, script_path, env)
        timings[task_name] = elapsed

    total_time = time.time() - t_start

    print("\n" + BANNER)
    print("  PIPELINE EXECUTION COMPLETE — ALL 8 TASKS SUCCESSFUL")
    print(BANNER)
    print("\n  Task Execution Times:")
    for name, el in timings.items():
        print(f"    • {name:<46}: {el:>6.2f} s")
    print(f"    {'TOTAL RUNTIME':<48}: {total_time:>6.2f} s\n")

    print("  Primary Deliverables in outputs/v2/:")
    print("    • results.csv                     : Unified table of all variables, regions, seasons, & windows")
    print("    • results.json                    : Full hierarchical structured JSON results")
    print("    • fig_slope_map.png               : Bangladesh choropleth map with hatched non-significant divisions")
    print("    • fig_timeseries_all_regions.png  : Comparative 5-panel regional series with 95% bootstrap bands")
    print("    • fig_2x2_classification.png      : Diagnostic Rainfall vs Storage quadrant scatter plot")
    print("    • fig_summary_table.png           : Rendered summary table for presentations")
    print("    • task8_narrative_en.txt          : Rule-based scientific interpretation (English)")
    print("    • task8_narrative_bn.txt          : Rule-based scientific interpretation (Bangla)")
    print(BANNER)


if __name__ == "__main__":
    main()
