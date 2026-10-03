"""
NASA Space Apps 2026 - Trend Detective: Bengal Water Paradox
Excel Detailed Numbers Generator

Compiles all divisional satellite observations (GRACE Water Storage & GPM IMERG Precipitation),
seasonal comparisons, historical divisional time series, and data dictionaries into a beautifully
formatted Excel workbook: 'bangladesh_water_analysis_detailed.xlsx'.
"""

import os
import sys
import json
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from analyze_divisions import get_division_geometries as get_grace_divisions, load_dataset as load_grace_ds, analyze_month as analyze_grace_month
from analyze_precipitation import load_dataset as load_precip_ds, detect_precip_variable, analyze_division_precip


def style_header(ws, row_idx: int, num_cols: int, bg_color: str = "1E293B", text_color: str = "FFFFFF"):
    fill = PatternFill(start_color=bg_color, end_color=bg_color, fill_type="solid")
    font = Font(name="Calibri", size=11, bold=True, color=text_color)
    alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    border = Border(
        top=Side(style="thin", color="CBD5E1"),
        bottom=Side(style="medium", color="0F172A"),
        left=Side(style="thin", color="CBD5E1"),
        right=Side(style="thin", color="CBD5E1")
    )
    for col in range(1, num_cols + 1):
        cell = ws.cell(row=row_idx, column=col)
        cell.fill = fill
        cell.font = font
        cell.alignment = alignment
        cell.border = border
    ws.row_dimensions[row_idx].height = 28


def style_data_rows(ws, start_row: int, end_row: int, num_cols: int):
    thin_border = Border(
        top=Side(style="thin", color="E2E8F0"),
        bottom=Side(style="thin", color="E2E8F0"),
        left=Side(style="thin", color="E2E8F0"),
        right=Side(style="thin", color="E2E8F0")
    )
    for row in range(start_row, end_row + 1):
        is_even = (row % 2 == 0)
        row_fill = PatternFill(start_color="F8FAFC" if is_even else "FFFFFF",
                               end_color="F8FAFC" if is_even else "FFFFFF",
                               fill_type="solid")
        for col in range(1, num_cols + 1):
            cell = ws.cell(row=row, column=col)
            cell.border = thin_border
            if cell.fill.fill_type is None:
                cell.fill = row_fill
            if isinstance(cell.value, float):
                cell.alignment = Alignment(horizontal="right", vertical="center")
            elif isinstance(cell.value, int):
                cell.alignment = Alignment(horizontal="right", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center")
        ws.row_dimensions[row].height = 20


def auto_fit_columns(ws, min_width: int = 12, max_width: int = 40):
    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        max_len = 0
        for cell in col:
            val_str = str(cell.value or "")
            if "\n" in val_str:
                val_str = max(val_str.split("\n"), key=len)
            max_len = max(max_len, len(val_str))
        ws.column_dimensions[col_letter].width = max(min_width, min(max_len + 4, max_width))


def generate_excel_workbook(output_xlsx: str = "bangladesh_water_analysis_detailed.xlsx"):
    print("Initializing Excel report generation...")
    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    # 1. Load GRACE Dataset
    grace_ds = load_grace_ds("CSR_GRACE_GRACE-FO_RL0603_Mascons_all-corrections.nc")
    grace_divs = get_grace_divisions()

    # 2. Load Precipitation Dataset
    precip_ds = load_precip_ds("nasa_precipitation_bangladesh.nc")
    precip_var = detect_precip_variable(precip_ds)

    # Key seasons to audit
    seasons = [
        {"key": "2026-07", "label": "July 2026", "season_type": "Monsoon Peak", "prev_key": "2025-07"},
        {"key": "2026-03", "label": "March 2026", "season_type": "Boro Irrigation Peak", "prev_key": "2025-03"},
        {"key": "2025-12", "label": "December 2025", "season_type": "Dry Winter Baseline", "prev_key": "2024-12"}
    ]

    # Pre-calculate data for each season
    grace_seasons_data = {}
    precip_seasons_data = {}

    # Map month strings to indices
    grace_months = {pd.to_datetime(t).strftime("%Y-%m"): i for i, t in enumerate(grace_ds["time"].values)}
    precip_months = {pd.to_datetime(t).strftime("%Y-%m"): i for i, t in enumerate(precip_ds["time"].values)}

    for s in seasons:
        m_key = s["key"]
        prev_key = s["prev_key"]

        # GRACE
        g_idx = grace_months.get(m_key)
        g_prev_idx = grace_months.get(prev_key)
        g_cur = analyze_grace_month(grace_ds, g_idx, grace_divs)
        g_prv = analyze_grace_month(grace_ds, g_prev_idx, grace_divs) if g_prev_idx is not None else {}
        for name in g_cur:
            if name in g_prv:
                g_cur[name]["yoy_delta_cm"] = round(g_cur[name]["mean_anomaly_cm"] - g_prv[name]["mean_anomaly_cm"], 2)
                g_cur[name]["prev_mean_cm"] = g_prv[name]["mean_anomaly_cm"]
        grace_seasons_data[m_key] = g_cur

        # Precipitation
        p_idx = precip_months.get(m_key)
        p_prev_idx = precip_months.get(prev_key)
        p_cur = analyze_division_precip(precip_ds, precip_var, p_idx, grace_divs)
        p_prv = analyze_division_precip(precip_ds, precip_var, p_prev_idx, grace_divs) if p_prev_idx is not None else {}
        for name in p_cur:
            if name in p_prv:
                p_cur[name]["yoy_delta_mm"] = round(p_cur[name]["mean_precip_mm"] - p_prv[name]["mean_precip_mm"], 1)
                p_cur[name]["prev_mean_mm"] = p_prv[name]["mean_precip_mm"]
        precip_seasons_data[m_key] = p_cur

    # -------------------------------------------------------------
    # TAB 1: EXECUTIVE SUMMARY (Side-by-Side Dual Satellite Audit)
    # -------------------------------------------------------------
    print("Writing Sheet 1: Executive_Summary...")
    ws1 = wb.create_sheet(title="Executive_Summary")
    ws1.views.sheetView[0].showGridLines = True

    # Title block
    ws1["A1"] = "NASA SPACE APPS 2026 — TREND DETECTIVE: THE BENGAL WATER PARADOX"
    ws1["A1"].font = Font(name="Calibri", size=16, bold=True, color="0284C7")
    ws1["A2"] = "Cross-Comparison Audit: Satellite Precipitation Influx (GPM IMERG) vs. Subsurface Water Storage (GRACE Mascons)"
    ws1["A2"].font = Font(name="Calibri", size=11, italic=True, color="475569")

    headers1 = [
        "Observation Month", "Season Classification", "Division", "Land Area (km²)",
        "Precipitation (mm/mo)", "Rain Influx Vol (km³)", "Rain Condition",
        "Water Storage Anomaly (cm)", "Storage Vol Anomaly (km³)", "Storage Condition",
        "Precip YoY Δ (mm)", "Storage YoY Δ (cm)"
    ]
    ws1.append([])  # Row 3 blank
    ws1.append(headers1)  # Row 4
    style_header(ws1, 4, len(headers1), bg_color="0F172A")

    row_count = 4
    for s in seasons:
        m_key = s["key"]
        for div_name in sorted(grace_divs.keys()):
            row_count += 1
            g_data = grace_seasons_data[m_key][div_name]
            p_data = precip_seasons_data[m_key][div_name]
            ws1.append([
                s["label"],
                s["season_type"],
                div_name,
                g_data["area_km2"],
                p_data["mean_precip_mm"],
                p_data["water_volume_km3"],
                p_data["condition"],
                g_data["mean_anomaly_cm"],
                g_data["volume_km3"],
                g_data["status"],
                p_data.get("yoy_delta_mm", 0.0),
                g_data.get("yoy_delta_cm", 0.0)
            ])
            # Highlight status
            st_cell = ws1.cell(row=row_count, column=10)
            if "Severe Deficit" in str(st_cell.value):
                st_cell.fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
                st_cell.font = Font(color="991B1B", bold=True)
            elif "Surplus" in str(st_cell.value):
                st_cell.fill = PatternFill(start_color="E0F2FE", end_color="E0F2FE", fill_type="solid")
                st_cell.font = Font(color="0369A1", bold=True)

    style_data_rows(ws1, 5, row_count, len(headers1))
    auto_fit_columns(ws1)

    # -------------------------------------------------------------
    # TAB 2: GRACE TERRESTRIAL WATER STORAGE (Comprehensive Data)
    # -------------------------------------------------------------
    print("Writing Sheet 2: GRACE_Water_Storage...")
    ws2 = wb.create_sheet(title="GRACE_Water_Storage")
    ws2.views.sheetView[0].showGridLines = True

    ws2["A1"] = "NASA GRACE / GRACE-FO MASCON RL06.3 — DIVISIONAL TERRESTRIAL WATER STORAGE (TWS)"
    ws2["A1"].font = Font(name="Calibri", size=14, bold=True, color="0284C7")
    ws2["A2"] = "Liquid Water Equivalent (LWE) thickness anomalies in cm relative to 2004–2009 baseline (CSR RL06.3 0.25° Mascons)"
    ws2["A2"].font = Font(name="Calibri", size=10, italic=True, color="475569")

    headers2 = [
        "Observation Month", "Division", "Land Area (km²)", "Grid Cells Masked",
        "Mean Storage Anomaly (cm)", "Min Anomaly (cm)", "Max Anomaly (cm)", "Spread/Std (cm)",
        "Net Volume Anomaly (km³)", "Previous Year Mean (cm)", "YoY Change (cm)", "Classification"
    ]
    ws2.append([])
    ws2.append(headers2)
    style_header(ws2, 4, len(headers2), bg_color="1E3A8A")

    row_count = 4
    for s in seasons:
        m_key = s["key"]
        for div_name in sorted(grace_divs.keys()):
            row_count += 1
            g = grace_seasons_data[m_key][div_name]
            ws2.append([
                s["label"],
                div_name,
                g["area_km2"],
                g["cell_count"],
                g["mean_anomaly_cm"],
                g["min_anomaly_cm"],
                g["max_anomaly_cm"],
                g["std_anomaly_cm"],
                g["volume_km3"],
                g.get("prev_mean_cm", 0.0),
                g.get("yoy_delta_cm", 0.0),
                g["status"]
            ])

    style_data_rows(ws2, 5, row_count, len(headers2))
    auto_fit_columns(ws2)

    # -------------------------------------------------------------
    # TAB 3: GPM IMERG PRECIPITATION INFLUX (Detailed Rainfall)
    # -------------------------------------------------------------
    print("Writing Sheet 3: IMERG_Precipitation...")
    ws3 = wb.create_sheet(title="IMERG_Precipitation")
    ws3.views.sheetView[0].showGridLines = True

    ws3["A1"] = "NASA GPM IMERG / SATELLITE PRECIPITATION — DIVISIONAL ATMOSPHERIC INFLUX"
    ws3["A1"].font = Font(name="Calibri", size=14, bold=True, color="0284C7")
    ws3["A2"] = "Monthly total accumulated rainfall (mm) and volumetric influx into river basins (km³) via NASA POWER / GPM IMERG"
    ws3["A2"].font = Font(name="Calibri", size=10, italic=True, color="475569")

    headers3 = [
        "Observation Month", "Division", "Land Area (km²)", "Grid Cells Masked",
        "Mean Rainfall (mm)", "Daily Rate (mm/day)", "Min Rainfall (mm)", "Max Rainfall (mm)",
        "Spread/Std (mm)", "Water Volume Influx (km³)", "Previous Year (mm)", "YoY Change (mm)", "Rainfall Condition"
    ]
    ws3.append([])
    ws3.append(headers3)
    style_header(ws3, 4, len(headers3), bg_color="0369A1")

    row_count = 4
    for s in seasons:
        m_key = s["key"]
        for div_name in sorted(grace_divs.keys()):
            row_count += 1
            p = precip_seasons_data[m_key][div_name]
            ws3.append([
                s["label"],
                div_name,
                p["area_km2"],
                p["cell_count"],
                p["mean_precip_mm"],
                p["daily_rate_mm_day"],
                p["min_precip_mm"],
                p["max_precip_mm"],
                p["std_precip_mm"],
                p["water_volume_km3"],
                p.get("prev_mean_mm", 0.0),
                p.get("yoy_delta_mm", 0.0),
                p["condition"]
            ])

    style_data_rows(ws3, 5, row_count, len(headers3))
    auto_fit_columns(ws3)

    # -------------------------------------------------------------
    # TAB 4: HISTORICAL TIME SERIES (2020 - 2026 Monthly Trend)
    # -------------------------------------------------------------
    print("Writing Sheet 4: Historical_Trends_2020_2026...")
    ws4 = wb.create_sheet(title="Historical_Trends_2020_2026")
    ws4.views.sheetView[0].showGridLines = True

    ws4["A1"] = "HISTORICAL MONTHLY SATELLITE TIME-SERIES BY DIVISION (2020 – 2026)"
    ws4["A1"].font = Font(name="Calibri", size=14, bold=True, color="0284C7")
    ws4["A2"] = "Consecutive monthly series of GRACE Storage Anomalies (cm) and GPM Precipitation (mm) for trend decomposition"
    ws4["A2"].font = Font(name="Calibri", size=10, italic=True, color="475569")

    headers4 = ["Year-Month", "Year", "Month", "Division", "GRACE Storage Anomaly (cm)", "IMERG Precipitation (mm)", "Rainfall Volume (km³)"]
    ws4.append([])
    ws4.append(headers4)
    style_header(ws4, 4, len(headers4), bg_color="334155")

    # Sample monthly series from 2020-01 to 2026-07
    recent_months = [m for m in sorted(grace_months.keys()) if m >= "2020-01" and m <= "2026-07"]
    row_count = 4

    for m_str in recent_months:
        dt = pd.to_datetime(m_str)
        g_idx = grace_months[m_str]
        g_res = analyze_grace_month(grace_ds, g_idx, grace_divs)
        
        p_res = {}
        if m_str in precip_months:
            p_idx = precip_months[m_str]
            p_res = analyze_division_precip(precip_ds, precip_var, p_idx, grace_divs)

        for div_name in sorted(grace_divs.keys()):
            row_count += 1
            g_val = g_res[div_name]["mean_anomaly_cm"]
            p_val = p_res.get(div_name, {}).get("mean_precip_mm", 0.0)
            p_vol = p_res.get(div_name, {}).get("water_volume_km3", 0.0)

            ws4.append([
                m_str,
                dt.year,
                dt.month,
                div_name,
                g_val,
                p_val,
                p_vol
            ])

    style_data_rows(ws4, 5, row_count, len(headers4))
    auto_fit_columns(ws4)

    # -------------------------------------------------------------
    # TAB 5: DATA DICTIONARY & METHODOLOGY
    # -------------------------------------------------------------
    print("Writing Sheet 5: Data_Dictionary...")
    ws5 = wb.create_sheet(title="Data_Dictionary")
    ws5.views.sheetView[0].showGridLines = True

    ws5["A1"] = "DATA DICTIONARY, UNITS & METHODOLOGY"
    ws5["A1"].font = Font(name="Calibri", size=14, bold=True, color="0284C7")

    dict_data = [
        ("Field / Metric", "Dataset / Source", "Unit", "Definition & Scientific Method"),
        ("Precipitation (mm/mo)", "NASA GPM IMERG / POWER", "mm/month", "Total depth of liquid precipitation accumulated over the calendar month."),
        ("Daily Rate (mm/day)", "NASA GPM IMERG / POWER", "mm/day", "Average rainfall rate per 24 hours (Precipitation mm / days in month)."),
        ("Rain Influx Vol (km³)", "NASA GPM IMERG / POWER", "km³", "Physical volume of rain fallen on division: Area (m²) × Precip (m) × 10⁻⁹."),
        ("Water Storage Anomaly", "CSR GRACE/GRACE-FO Mascon RL06.3", "cm", "Liquid Water Equivalent (LWE) thickness deviation from 2004–2009 mean baseline."),
        ("Storage Vol Anomaly (km³)", "CSR GRACE/GRACE-FO Mascon RL06.3", "km³", "Volumetric water surplus or deficit: Division Area (m²) × LWE (m) × 10⁻⁹."),
        ("Spread / Std (cm or mm)", "Both Instruments", "cm / mm", "Standard deviation of pixel-level values within the division boundary."),
        ("YoY Delta (cm or mm)", "Both Instruments", "cm / mm", "Difference in anomaly/rainfall compared to the exact same month in previous year."),
        ("Spatial Masking", "Natural Earth 10m Admin-1", "N/A", "Vector polygon containment test using shapely.contains_xy at 10m coastline resolution."),
        ("Area Weighting", "Geodetic WGS84", "cos(lat)", "Cosine of latitude weighting applied to all grid cells to account for meridian convergence.")
    ]

    ws5.append([])
    for row in dict_data:
        ws5.append(list(row))

    style_header(ws5, 3, 4, bg_color="0F172A")
    style_data_rows(ws5, 4, 3 + len(dict_data) - 1, 4)
    auto_fit_columns(ws5)

    # Save to both target output path and workspace root
    wb.save(output_xlsx)
    print(f"Saved Excel Workbook: {output_xlsx}")

    # Also save copy in outputs/
    outputs_path = Path("outputs") / Path(output_xlsx).name
    if str(outputs_path) != output_xlsx:
        outputs_path.parent.mkdir(parents=True, exist_ok=True)
        wb.save(str(outputs_path))
        print(f"Saved Copy in Outputs: {outputs_path}")


if __name__ == "__main__":
    generate_excel_workbook()
