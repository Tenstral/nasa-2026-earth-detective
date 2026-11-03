"""
NASA Space Apps 2026 – Bengal Hydro Detective
v3 Before-vs-After Significance Verdict Diff Generator
======================================================
Compares trend test results and headline verdicts before and after Task 1 significance calibration:
  - Before: Hamed-Rao modified Mann-Kendall with residual block-bootstrap CI (FPR 14-26%)
  - After: Calibrated Effective-Sample-Size (ESS) Mann-Kendall with duality-aligned Theil-Sen CI (FPR 5.0-5.8%, CI coverage 94.2-95.0%)
Generates:
  outputs/v3/full_record/verdicts_before_after.csv
  outputs/v3/full_record/verdicts_before_after.md
"""

from pathlib import Path
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUTS_V3 = REPO_ROOT / "outputs" / "v3" / "full_record"
BEFORE_CSV = OUTPUTS_V3 / "results_all_windows_before_calib.csv"
AFTER_CSV = OUTPUTS_V3 / "results_all_windows.csv"
OUT_CSV = OUTPUTS_V3 / "verdicts_before_after.csv"
OUT_MD = OUTPUTS_V3 / "verdicts_before_after.md"


def generate_before_after_verdicts():
    if not BEFORE_CSV.exists():
        raise FileNotFoundError(f"Missing {BEFORE_CSV}")
    if not AFTER_CSV.exists():
        raise FileNotFoundError(f"Missing {AFTER_CSV}")

    df_before = pd.read_csv(BEFORE_CSV)
    df_after = pd.read_csv(AFTER_CSV)

    # Merge on window, entity, variable, season
    merge_keys = ["window", "entity", "variable", "season"]
    merged = pd.merge(
        df_before,
        df_after,
        on=merge_keys,
        suffixes=("_before", "_after"),
    )

    rows = []
    for _, r in merged.iterrows():
        v_bef = r["verdict_before"]
        v_aft = r["verdict_after"]
        
        if v_bef == v_aft:
            status = f"Unchanged ({v_aft})"
        else:
            status = f"CHANGED: {v_bef} -> {v_aft}"

        rows.append({
            "window": r["window"],
            "entity": r["entity"],
            "entity_type": r["entity_type_after"],
            "variable": r["variable"],
            "season": r["season"],
            "slope_before": r["slope_before"],
            "ci_before": f"[{r['slope_ci_low_before']:+.2f}, {r['slope_ci_high_before']:+.2f}]",
            "p_val_before": r["p_value_before"],
            "q_val_before": r["bh_fdr_q_value_before"],
            "verdict_before": v_bef,
            "slope_after": r["slope_after"],
            "ci_after": f"[{r['slope_ci_low_after']:+.2f}, {r['slope_ci_high_after']:+.2f}]",
            "p_val_after": r["p_value_after"],
            "q_val_after": r["bh_fdr_q_value_after"],
            "verdict_after": v_aft,
            "verdict_status": status,
        })

    diff_df = pd.DataFrame(rows)
    diff_df.to_csv(OUT_CSV, index=False)

    # Build Markdown Table focusing on Regional Annual TWS and Precip
    reg_ann = diff_df[(diff_df["entity_type"] == "region") & (diff_df["season"] == "annual")].copy()

    md_lines = [
        "# Task 1 Calibration: Before-vs-After Significance Verdict Table",
        "",
        "**Status:** PRELIMINARY — Comparison of Significance Calibration across all 4 Windows",
        "- **Before Engine:** Hamed-Rao Modified Mann-Kendall with circular block-bootstrap CI (Uncalibrated; FPR 14–26%).",
        "- **After Engine:** Calibrated Effective-Sample-Size (ESS) Mann-Kendall with duality-aligned Theil-Sen CI (FPR 5.0–5.8%, CI coverage 94.2–95.0%).",
        "",
        "## Regional Annual Total Water Storage (TWS) Trends",
        "",
        "| Window | Region | Slope (cm/yr) | Before p | Before FDR q | Before Verdict | After p | After FDR q | After Calibrated 95% CI | After Calibrated Verdict | Status |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]

    for _, r in reg_ann[reg_ann["variable"] == "tws"].iterrows():
        p_bef_str = "< 0.0001" if r["p_val_before"] < 0.0001 else f"{r['p_val_before']:.4f}"
        q_bef_str = "< 0.0001" if r["q_val_before"] < 0.0001 else f"{r['q_val_before']:.4f}"
        p_aft_str = "< 0.0001" if r["p_val_after"] < 0.0001 else f"{r['p_val_after']:.4f}"
        q_aft_str = "< 0.0001" if r["q_val_after"] < 0.0001 else f"{r['q_val_after']:.4f}"

        badge = "**`Significant`**" if r["verdict_after"] == "Significant" else (
            "`Suggestive`" if r["verdict_after"] == "Suggestive" else "`No detectable trend`"
        )
        md_lines.append(
            f"| `{r['window']}` | **{r['entity']}** | {r['slope_after']:+.2f} | {p_bef_str} | {q_bef_str} | `{r['verdict_before']}` | "
            f"{p_aft_str} | {q_aft_str} | {r['ci_after']} | {badge} | {r['verdict_status']} |"
        )

    md_lines.extend([
        "",
        "## Regional Annual Precipitation Trends (Preliminary POWER Series)",
        "",
        "| Window | Region | Slope (mm/yr) | Before p | Before FDR q | Before Verdict | After p | After FDR q | After Calibrated 95% CI | After Calibrated Verdict | Status |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ])

    for _, r in reg_ann[reg_ann["variable"] == "precip"].iterrows():
        p_bef_str = "< 0.0001" if r["p_val_before"] < 0.0001 else f"{r['p_val_before']:.4f}"
        q_bef_str = "< 0.0001" if r["q_val_before"] < 0.0001 else f"{r['q_val_before']:.4f}"
        p_aft_str = "< 0.0001" if r["p_val_after"] < 0.0001 else f"{r['p_val_after']:.4f}"
        q_aft_str = "< 0.0001" if r["q_val_after"] < 0.0001 else f"{r['q_val_after']:.4f}"

        badge = "**`Significant`**" if r["verdict_after"] == "Significant" else (
            "`Suggestive`" if r["verdict_after"] == "Suggestive" else "`No detectable trend`"
        )
        md_lines.append(
            f"| `{r['window']}` | **{r['entity']}** | {r['slope_after']:+.1f} | {p_bef_str} | {q_bef_str} | `{r['verdict_before']}` | "
            f"{p_aft_str} | {q_aft_str} | {r['ci_after']} | {badge} | {r['verdict_status']} |"
        )

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"Generated Before/After comparison: {OUT_CSV.name} and {OUT_MD.name}")
    return diff_df


if __name__ == "__main__":
    generate_before_after_verdicts()
