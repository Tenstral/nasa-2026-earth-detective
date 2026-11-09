"""
Build the complete, interactive index.html with all 24-year findings,
timeline toggleable visualisations, animated SVG map, Chart.js studio,
and 336-test results explorer.
"""

import json
from pathlib import Path
import re

REPO_ROOT = Path(__file__).resolve().parent.parent

# Load compiled dashboard data
with open(REPO_ROOT / "scratch/dashboard_data.json", encoding="utf-8") as f:
    data = json.load(f)

# Compact JSON serialization
data_json = json.dumps(data)

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bengal Hydro Detective — 24-Year Earth System Observation Hub</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&family=Space+Grotesk:wght@600;700;800&display=swap" rel="stylesheet">
  <!-- Chart.js via CDN with graceful fallback -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>

  <style>
    :root {
      --bg-dark: #070b14;
      --bg-card: #0d1527;
      --bg-card-hover: #131f38;
      --bg-input: #0a0f1d;
      --border-subtle: #1c2b4a;
      --border-accent: #38bdf8;
      --border-strong: #253966;
      --ink-primary: #f8fafc;
      --ink-secondary: #cbd5e1;
      --ink-muted: #8494b2;
      --accent-blue: #0284c7;
      --accent-sky: #38bdf8;
      --accent-red: #ef4444;
      --accent-amber: #f59e0b;
      --accent-emerald: #10b981;
      --accent-indigo: #818cf8;
      --accent-purple: #c084fc;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background: var(--bg-dark);
      color: var(--ink-primary);
      min-height: 100vh;
      line-height: 1.5;
      padding-bottom: 80px;
    }

    /* Ambient background grid */
    body::before {
      content: "";
      position: fixed;
      top: 0; left: 0; width: 100%; height: 100%;
      background-image: 
        linear-gradient(rgba(56, 189, 248, 0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(56, 189, 248, 0.025) 1px, transparent 1px);
      background-size: 40px 40px;
      pointer-events: none;
      z-index: -1;
    }

    .container {
      max-width: 1320px;
      margin: 0 auto;
      padding: 24px 20px;
    }

    /* Header Nav */
    .top-nav {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 12px 0 20px 0;
      border-bottom: 1px solid var(--border-subtle);
      margin-bottom: 24px;
      flex-wrap: wrap;
      gap: 12px;
    }
    .brand-wrap {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .brand-badge {
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.35);
      color: var(--accent-sky);
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      padding: 4px 10px;
      border-radius: 999px;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .brand-badge .dot {
      width: 7px; height: 7px;
      background: var(--accent-sky);
      border-radius: 50%;
      display: inline-block;
      box-shadow: 0 0 8px var(--accent-sky);
    }
    .nav-links {
      display: flex;
      gap: 14px;
      flex-wrap: wrap;
    }
    .nav-link {
      color: var(--ink-muted);
      text-decoration: none;
      font-size: 0.85rem;
      font-weight: 600;
      transition: color 0.15s ease;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }
    .nav-link:hover { color: var(--accent-sky); }

    /* Hero Banner */
    .hero-banner {
      background: linear-gradient(135deg, rgba(14, 25, 48, 0.8) 0%, rgba(8, 14, 28, 0.95) 100%);
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      padding: 28px 32px;
      margin-bottom: 24px;
      position: relative;
      overflow: hidden;
    }
    .hero-banner::after {
      content: "";
      position: absolute;
      top: -60px; right: -60px;
      width: 240px; height: 240px;
      background: radial-gradient(circle, rgba(56, 189, 248, 0.12) 0%, transparent 70%);
      pointer-events: none;
    }
    .hero-title {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 2.1rem;
      font-weight: 800;
      color: #ffffff;
      letter-spacing: -0.5px;
      line-height: 1.2;
      margin-bottom: 8px;
    }
    .hero-subtitle {
      font-size: 1.02rem;
      color: var(--ink-secondary);
      max-width: 900px;
      line-height: 1.55;
      margin-bottom: 18px;
    }
    .hero-tags {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }
    .tag {
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid var(--border-strong);
      padding: 4px 12px;
      border-radius: 6px;
      font-size: 0.78rem;
      color: var(--ink-muted);
      font-weight: 600;
    }
    .tag strong { color: var(--ink-primary); }

    /* Section Cards */
    .section-card {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 24px;
      position: relative;
    }
    .section-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      flex-wrap: wrap;
      gap: 12px;
    }
    .section-title {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 1.28rem;
      font-weight: 700;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .section-desc {
      font-size: 0.9rem;
      color: var(--ink-muted);
      margin-top: 4px;
    }

    /* Controls Panel */
    .control-panel {
      background: var(--bg-input);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 18px 20px;
      margin-bottom: 20px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .controls-row {
      display: flex;
      align-items: center;
      gap: 18px;
      flex-wrap: wrap;
    }
    .ctrl-group {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .ctrl-label {
      font-size: 0.8rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.7px;
      color: var(--ink-muted);
      white-space: nowrap;
    }
    .pill-switch {
      display: inline-flex;
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid var(--border-strong);
      border-radius: 8px;
      padding: 3px;
      gap: 3px;
    }
    .pill-btn {
      background: transparent;
      border: none;
      color: var(--ink-muted);
      font-size: 0.82rem;
      font-weight: 600;
      padding: 6px 14px;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.15s ease;
      white-space: nowrap;
    }
    .pill-btn:hover { color: var(--ink-primary); }
    .pill-btn.active {
      background: var(--accent-blue);
      color: #ffffff;
      box-shadow: 0 0 10px rgba(2, 132, 199, 0.4);
    }

    /* Timeline Slider Bar */
    .timeline-bar {
      display: flex;
      align-items: center;
      gap: 16px;
      width: 100%;
      padding-top: 8px;
      border-top: 1px solid var(--border-subtle);
    }
    .slider-wrap {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .slider-header {
      display: flex;
      justify-content: space-between;
      font-size: 0.78rem;
      color: var(--ink-muted);
    }
    .timeline-slider {
      width: 100%;
      height: 6px;
      border-radius: 4px;
      background: var(--border-strong);
      outline: none;
      cursor: pointer;
      -webkit-appearance: none;
    }
    .timeline-slider::-webkit-slider-thumb {
      -webkit-appearance: none;
      width: 18px; height: 18px;
      border-radius: 50%;
      background: var(--accent-sky);
      cursor: pointer;
      box-shadow: 0 0 10px var(--accent-sky);
      border: 2px solid #ffffff;
      transition: transform 0.1s ease;
    }
    .timeline-slider::-webkit-slider-thumb:hover {
      transform: scale(1.18);
    }
    .time-badge {
      font-family: 'JetBrains Mono', monospace;
      font-size: 1.15rem;
      font-weight: 700;
      color: #ffffff;
      background: rgba(56, 189, 248, 0.15);
      border: 1px solid rgba(56, 189, 248, 0.4);
      padding: 6px 16px;
      border-radius: 8px;
      min-width: 130px;
      text-align: center;
    }
    .play-btn {
      background: var(--bg-card);
      border: 1px solid var(--border-accent);
      color: var(--accent-sky);
      width: 38px; height: 38px;
      border-radius: 8px;
      font-size: 1.1rem;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .play-btn:hover {
      background: var(--accent-sky);
      color: #000000;
      box-shadow: 0 0 12px rgba(56, 189, 248, 0.5);
    }

    /* KPI Row */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-bottom: 20px;
    }
    @media (max-width: 1024px) {
      .kpi-grid { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 600px) {
      .kpi-grid { grid-template-columns: 1fr; }
    }
    .kpi-card {
      background: var(--bg-input);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 16px 18px;
      transition: border-color 0.15s ease;
    }
    .kpi-card:hover { border-color: var(--border-strong); }
    .kpi-title {
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: var(--ink-muted);
      margin-bottom: 6px;
    }
    .kpi-val {
      font-family: 'JetBrains Mono', monospace;
      font-size: 1.6rem;
      font-weight: 700;
      color: #ffffff;
      line-height: 1.2;
    }
    .kpi-sub {
      font-size: 0.78rem;
      color: var(--ink-secondary);
      margin-top: 4px;
    }

    /* Map + Ranking Dual View */
    .map-grid {
      display: grid;
      grid-template-columns: 1.15fr 0.85fr;
      gap: 20px;
      margin-bottom: 20px;
    }
    @media (max-width: 960px) {
      .map-grid { grid-template-columns: 1fr; }
    }
    .map-container {
      background: #050811;
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 18px;
      position: relative;
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 520px;
    }
    .map-title-row {
      width: 100%;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--accent-sky);
    }
    .svg-map-wrapper {
      width: 100%;
      max-width: 520px;
      height: auto;
    }
    .division-path {
      stroke: #1e293b;
      stroke-width: 1.5;
      cursor: pointer;
      transition: fill 0.25s ease, stroke 0.15s ease, stroke-width 0.15s ease;
    }
    .division-path:hover {
      stroke: #38bdf8;
      stroke-width: 2.5;
      filter: brightness(1.15);
    }
    .division-path.selected {
      stroke: #f59e0b;
      stroke-width: 3.2;
      filter: drop-shadow(0 0 6px #f59e0b);
    }
    .division-label {
      font-family: 'Inter', sans-serif;
      font-size: 10px;
      font-weight: 700;
      fill: #ffffff;
      text-anchor: middle;
      pointer-events: none;
      text-shadow: 0 1px 4px #000000, 0 0 8px #000000;
    }
    .map-legend {
      width: 100%;
      margin-top: 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 0.75rem;
      color: var(--ink-muted);
      flex-wrap: wrap;
      gap: 8px;
    }
    .legend-bar {
      flex: 1;
      height: 10px;
      border-radius: 5px;
      margin: 0 12px;
      min-width: 140px;
    }

    /* Ranking Panel */
    .ranking-container {
      background: var(--bg-input);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 18px;
      display: flex;
      flex-direction: column;
    }
    .ranking-list {
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-top: 10px;
      flex: 1;
    }
    .ranking-item {
      display: flex;
      flex-direction: column;
      gap: 4px;
      cursor: pointer;
      padding: 6px 8px;
      border-radius: 6px;
      transition: background 0.15s ease;
    }
    .ranking-item:hover { background: rgba(56, 189, 248, 0.08); }
    .ranking-meta {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.82rem;
    }
    .ranking-name { font-weight: 700; color: #ffffff; }
    .ranking-val {
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
    }
    .ranking-bar-track {
      width: 100%;
      height: 7px;
      background: rgba(30, 41, 59, 0.8);
      border-radius: 4px;
      overflow: hidden;
      position: relative;
    }
    .ranking-bar-fill {
      height: 100%;
      border-radius: 4px;
      transition: width 0.3s ease, background 0.3s ease;
    }

    /* Floating Tooltip */
    #mapTooltip {
      position: absolute;
      display: none;
      background: rgba(10, 16, 30, 0.95);
      border: 1px solid var(--border-accent);
      padding: 10px 14px;
      border-radius: 8px;
      font-size: 0.8rem;
      color: #ffffff;
      pointer-events: none;
      z-index: 100;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.6);
      min-width: 180px;
    }

    /* Inspector Card */
    .inspector-card {
      background: #090e1b;
      border: 1px solid var(--border-strong);
      border-radius: 10px;
      padding: 16px 20px;
      margin-top: 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }
    .insp-title {
      font-size: 1.1rem;
      font-weight: 700;
      color: #ffffff;
    }
    .insp-region {
      font-size: 0.82rem;
      color: var(--accent-sky);
    }
    .insp-stats {
      display: flex;
      gap: 20px;
      flex-wrap: wrap;
    }
    .insp-stat-item {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }
    .insp-stat-label {
      font-size: 0.72rem;
      color: var(--ink-muted);
      text-transform: uppercase;
      letter-spacing: 0.6px;
      font-weight: 700;
    }
    .insp-stat-val {
      font-family: 'JetBrains Mono', monospace;
      font-size: 1.05rem;
      font-weight: 700;
      color: #ffffff;
    }

    /* Time Series Studio */
    .chart-box {
      background: #050811;
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 18px;
      position: relative;
      height: 420px;
      margin-bottom: 14px;
    }

    /* Two-Column Grid */
    .grid-2col {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin-bottom: 20px;
    }
    @media (max-width: 860px) {
      .grid-2col { grid-template-columns: 1fr; }
    }
    .col-card {
      background: var(--bg-input);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 20px;
    }
    .col-card-title {
      font-size: 0.95rem;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    /* Table Styles */
    .table-container {
      overflow-x: auto;
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      margin-top: 12px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.83rem;
      text-align: left;
    }
    th {
      background: #0c1222;
      color: var(--ink-muted);
      font-weight: 700;
      padding: 10px 14px;
      border-bottom: 1px solid var(--border-subtle);
      white-space: nowrap;
    }
    td {
      padding: 10px 14px;
      border-bottom: 1px solid rgba(28, 43, 74, 0.4);
      color: var(--ink-secondary);
      background: #080d1a;
      white-space: nowrap;
    }
    tr:hover td { background: #0f182c; }
    .mono { font-family: 'JetBrains Mono', monospace; font-weight: 600; }
    .badge-sig {
      background: rgba(239, 68, 68, 0.15);
      border: 1px solid rgba(239, 68, 68, 0.4);
      color: #fca5a5;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 0.72rem;
      font-weight: 700;
    }
    .badge-suggestive {
      background: rgba(245, 158, 11, 0.15);
      border: 1px solid rgba(245, 158, 11, 0.4);
      color: #fde68a;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 0.72rem;
      font-weight: 700;
    }
    .badge-null {
      background: rgba(148, 163, 184, 0.12);
      border: 1px solid rgba(148, 163, 184, 0.3);
      color: #cbd5e1;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 0.72rem;
      font-weight: 700;
    }
    .badge-method {
      background: rgba(192, 132, 252, 0.15);
      border: 1px solid rgba(192, 132, 252, 0.4);
      color: #e9d5ff;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 0.72rem;
      font-weight: 700;
    }

    /* Buttons */
    .btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 16px;
      border-radius: 6px;
      font-size: 0.83rem;
      font-weight: 600;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.15s ease;
      border: none;
    }
    .btn-primary {
      background: var(--accent-blue);
      color: #ffffff;
    }
    .btn-primary:hover { background: #0369a1; }
    .btn-secondary {
      background: var(--bg-card);
      border: 1px solid var(--border-strong);
      color: var(--ink-secondary);
    }
    .btn-secondary:hover {
      border-color: var(--accent-sky);
      color: #ffffff;
    }
  </style>
</head>
<body>

  <div class="container">

    <!-- Top Navigation -->
    <nav class="top-nav">
      <div class="brand-wrap">
        <span class="brand-badge"><span class="dot"></span> NASA Space Apps 2026 • Team Tenstral</span>
        <span style="font-weight: 700; font-size: 0.95rem;">Bengal Hydro Detective</span>
      </div>
      <div class="nav-links">
        <a href="#console" class="nav-link">Interactive Map</a>
        <a href="#timeseries" class="nav-link">Time Series Studio</a>
        <a href="#threeway" class="nav-link">3-Way Northwest Transparency</a>
        <a href="#gldas" class="nav-link">Soil Moisture Partition</a>
        <a href="#rainfall" class="nav-link">Rainfall Integrity</a>
        <a href="#exposure" class="nav-link">Exposure & Floods</a>
        <a href="#registry" class="nav-link">Results Registry</a>
        <a href="#limitations" class="nav-link">Limitations</a>
        <a href="PROJECT_STATUS.md" class="nav-link" target="_blank" style="color: var(--accent-sky);">Status Guide ↗</a>
      </div>
    </nav>

    <!-- Hero Banner -->
    <header class="hero-banner">
      <h1 class="hero-title">Bengal Hydro Detective: 24-Year Earth System Hub</h1>
      <p class="hero-subtitle">
        Auditing 24 continuous years of NASA satellite gravimetry (CSR GRACE/GRACE-FO RL06.3 Mascons), GPM IMERG V07B precipitation, and GLDAS Land Surface Models across Bangladesh (April 2002 to July 2026).
      </p>
      <div class="hero-tags">
        <span class="tag">Status: <strong>PRELIMINARY</strong></span>
        <span class="tag">Primary Method: <strong>Calibrated ESS-MK</strong></span>
        <span class="tag">Lead Window: <strong>full_record (2002–2026)</strong></span>
        <span class="tag">Rainfall Source: <strong>GPM IMERG Final V07B</strong></span>
        <span class="tag">Audited Tests: <strong>336 Independent &amp; Descriptive Tests</strong></span>
      </div>
    </header>

    <!-- SECTION 1: INTERACTIVE MAP & TEMPORAL CONSOLE -->
    <section class="section-card" id="console">
      <div class="section-header">
        <div>
          <h2 class="section-title">🗺️ Interactive Map &amp; Temporal Scrubber</h2>
          <p class="section-desc">Explore spatial storage and precipitation dynamics toggleable across years (2002–2026), monthly snapshots, and milestone seasons.</p>
        </div>
        <div style="display: flex; gap: 8px;">
          <a href="bangladesh_water_analysis_detailed.xlsx" class="btn btn-primary" download>📊 Excel Workbook</a>
        </div>
      </div>

      <!-- Controls Panel -->
      <div class="control-panel">
        <div class="controls-row">
          <div class="ctrl-group">
            <span class="ctrl-label">Satellite Metric:</span>
            <div class="pill-switch">
              <button class="pill-btn active" id="btnMetricTws" onclick="setMetric('tws')">🌊 Total Water Storage (cm)</button>
              <button class="pill-btn" id="btnMetricPrecip" onclick="setMetric('precip')">🌧️ IMERG Rainfall (mm)</button>
              <button class="pill-btn" id="btnMetricTrend" onclick="setMetric('trend')">📉 24-Yr Trend Rate (cm/yr)</button>
            </div>
          </div>

          <div class="ctrl-group">
            <span class="ctrl-label">Time Unit:</span>
            <div class="pill-switch">
              <button class="pill-btn active" id="btnScaleAnnual" onclick="setTimeScale('annual')">Annual (2002–2026)</button>
              <button class="pill-btn" id="btnScaleMonthly" onclick="setTimeScale('monthly')">Monthly Time Series</button>
              <button class="pill-btn" id="btnScaleSeason" onclick="setTimeScale('season')">Milestone Seasons</button>
            </div>
          </div>
        </div>

        <!-- Slider Bar -->
        <div class="timeline-bar">
          <button class="play-btn" id="playBtn" onclick="togglePlayback()" title="Play/Pause Timeline Animation">▶</button>
          <div class="slider-wrap">
            <div class="slider-header">
              <span id="sliderMinLabel">2002</span>
              <span id="sliderCurrentLabel" style="color: var(--accent-sky); font-weight: 700;">2024</span>
              <span id="sliderMaxLabel">2026</span>
            </div>
            <input type="range" min="0" max="24" value="22" class="timeline-slider" id="timelineSlider" oninput="onSliderChange(this.value)">
          </div>
          <div class="time-badge" id="timeBadge">Year: 2024</div>
        </div>
      </div>

      <!-- Dynamic KPIs -->
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-title">National Mean Storage Anomaly</div>
          <div class="kpi-val" id="kpiNationalTws">-3.4 cm</div>
          <div class="kpi-sub" id="kpiNationalTwsSub">National area-weighted aggregate</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-title">Maximum Depletion Division</div>
          <div class="kpi-val" id="kpiMinDiv" style="color: var(--accent-red);">Rangpur</div>
          <div class="kpi-sub" id="kpiMinVal">-14.3 cm storage deficit</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-title">Maximum Surplus Division</div>
          <div class="kpi-val" id="kpiMaxDiv" style="color: var(--accent-sky);">Sylhet</div>
          <div class="kpi-sub" id="kpiMaxVal">+22.1 cm surplus</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-title">National Net Volume Anomaly</div>
          <div class="kpi-val" id="kpiNetVol">-4.18 km³</div>
          <div class="kpi-sub">Total water mass relative to baseline</div>
        </div>
      </div>

      <!-- Map + Ranking Grid -->
      <div class="map-grid">
        <!-- SVG Vector Map -->
        <div class="map-container">
          <div class="map-title-row">
            <span id="mapTitle">Spatial Distribution: Total Water Storage Anomaly</span>
            <span style="font-size: 0.75rem; color: var(--ink-muted);">Click any division to inspect</span>
          </div>

          <div class="svg-map-wrapper">
            <svg id="bdMapSvg" viewBox="0 0 600 750" style="width: 100%; height: auto;">
              <!-- Paths injected by JavaScript -->
            </svg>
          </div>

          <div id="mapTooltip"></div>

          <div class="map-legend">
            <span id="legendMin">-30 cm</span>
            <div class="legend-bar" id="legendBar" style="background: linear-gradient(90deg, #dc2626 0%, #fef08a 50%, #0284c7 100%);"></div>
            <span id="legendMax">+30 cm</span>
          </div>
        </div>

        <!-- Live Sorting Ranking -->
        <div class="ranking-container">
          <div class="map-title-row">
            <span>Divisional Ranking (Sorted Live)</span>
            <span style="font-size: 0.75rem; color: var(--ink-muted);">8 Administrative Divisions</span>
          </div>
          <div class="ranking-list" id="rankingList">
            <!-- Dynamically populated -->
          </div>
        </div>
      </div>

      <!-- Selected Division Inspector -->
      <div class="inspector-card" id="inspectorCard">
        <div>
          <div class="insp-title" id="inspName">Rajshahi Division</div>
          <div class="insp-region" id="inspRegion">Northwest Region • Primary Food Basket</div>
        </div>
        <div class="insp-stats">
          <div class="insp-stat-item">
            <span class="insp-stat-label">Current Anomaly</span>
            <span class="insp-stat-val" id="inspCurrentVal">-11.2 cm</span>
          </div>
          <div class="insp-stat-item">
            <span class="insp-stat-label">24-Yr Trend Rate</span>
            <span class="insp-stat-val" id="inspTrendVal">-1.25 cm/yr</span>
          </div>
          <div class="insp-stat-item">
            <span class="insp-stat-label">Population (2020)</span>
            <span class="insp-stat-val" id="inspPop">20.8M</span>
          </div>
          <div class="insp-stat-item">
            <span class="insp-stat-label">Cropland %</span>
            <span class="insp-stat-val" id="inspCrop">76.4%</span>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 2: TIME SERIES STUDIO -->
    <section class="section-card" id="timeseries">
      <div class="section-header">
        <div>
          <h2 class="section-title">📈 24-Year Multi-Sensor Time Series Studio</h2>
          <p class="section-desc">Interactive time series exploration comparing gravimetric water storage, satellite rainfall, and robust trendlines across all regions.</p>
        </div>
        <div class="pill-switch">
          <button class="pill-btn active" id="btnTsNW" onclick="setTimeSeriesRegion('NW')">Northwest</button>
          <button class="pill-btn" id="btnTsNE" onclick="setTimeSeriesRegion('NE')">Northeast</button>
          <button class="pill-btn" id="btnTsCentral" onclick="setTimeSeriesRegion('Central')">Central</button>
          <button class="pill-btn" id="btnTsSW" onclick="setTimeSeriesRegion('SW')">Southwest</button>
          <button class="pill-btn" id="btnTsSE" onclick="setTimeSeriesRegion('SE')">Southeast</button>
          <button class="pill-btn" id="btnTsNational" onclick="setTimeSeriesRegion('National')">National</button>
        </div>
      </div>

      <div class="control-panel" style="padding: 12px 18px; margin-bottom: 14px;">
        <div class="controls-row">
          <div class="ctrl-group">
            <span class="ctrl-label">Analytical Window:</span>
            <div class="pill-switch">
              <button class="pill-btn active" id="btnWinFull" onclick="setTimeSeriesWindow('full_record')">full_record (2002–2026)</button>
              <button class="pill-btn" id="btnWinGrace" onclick="setTimeSeriesWindow('grace_era')">grace_era (2002–2017)</button>
              <button class="pill-btn" id="btnWinFo" onclick="setTimeSeriesWindow('grace_fo_era')">grace_fo_era (2018–2026)</button>
              <button class="pill-btn" id="btnWinRecent" onclick="setTimeSeriesWindow('recent_2020')">recent_2020 (2020–2026)</button>
            </div>
          </div>

          <div class="ctrl-group">
            <span class="ctrl-label">Display Variable:</span>
            <div class="pill-switch">
              <button class="pill-btn active" id="btnVarTws" onclick="setTimeSeriesVariable('tws')">Total Water Storage (cm)</button>
              <button class="pill-btn" id="btnVarPrecip" onclick="setTimeSeriesVariable('precip')">IMERG Rainfall (mm)</button>
              <button class="pill-btn" id="btnVarBoth" onclick="setTimeSeriesVariable('both')">Dual Storage + Rainfall</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Chart Container -->
      <div class="chart-box">
        <canvas id="timeSeriesChart"></canvas>
      </div>

      <div style="font-size: 0.8rem; color: var(--ink-muted); display: flex; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
        <span>Observed points: 257 valid monthly satellite observations. Shaded region indicates the 11-month 2017–2018 inter-satellite gap.</span>
        <span id="chartTrendSummary" style="color: var(--accent-sky); font-weight: 700;">NW Trend: -1.25 cm/yr [95% CI: -1.50, -1.02] (p &lt; 0.0001)</span>
      </div>
    </section>

    <!-- SECTION 3: 3-WAY NORTHWEST SENSITIVITY -->
    <section class="section-card" id="threeway">
      <div class="section-header">
        <div>
          <h2 class="section-title">⚖️ 3-Way Northwest Slope Transparency</h2>
          <p class="section-desc">Accounting for the 11-month inter-satellite transition gap (July 2017 to May 2018) across four transparent model specifications.</p>
        </div>
        <span class="tag">Intercalibration Audit</span>
      </div>

      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Region</th>
              <th>Lead Evidence: GRACE-1 Era (2002–2017)</th>
              <th>Single-Line Fit (2002–2026)</th>
              <th>Step-Adjusted Fit (2002–2026)</th>
              <th>Transition Step Offset (p-value)</th>
              <th>Transition-Excluded (±6 mo Buffer)</th>
              <th>Reported Depletion Range</th>
            </tr>
          </thead>
          <tbody id="threeWayTableBody">
            <!-- Dynamically populated from three_way data -->
          </tbody>
        </table>
      </div>

      <div style="margin-top: 14px; font-size: 0.84rem; color: var(--ink-muted); line-height: 1.55;">
        <strong>Key Insight:</strong> Between GRACE decommissioning (2017-06) and GRACE-FO startup (2018-06), an upward step offset (+9.15 cm in NW, p = 0.028) of unknown origin is detected in the raw gravimetric anomaly series. Because Monte Carlo red-noise simulations show that an unadjusted step is falsely flagged as a trend in 93.8% to 100% of simulations under standard linear models, multi-satellite linear trends across unbridged gaps must always be reported alongside step-adjusted and buffer-excluded bounds. The Northwest rate is bounded between <strong>-1.81 and -1.25 cm/year</strong> (lead benchmark: <strong>-1.56 cm/year</strong>).
      </div>
    </section>

    <!-- SECTION 4: SOIL MOISTURE PARTITIONING -->
    <section class="section-card" id="gldas">
      <div class="section-header">
        <div>
          <h2 class="section-title">🌱 Multi-Model Soil Moisture Partitioning</h2>
          <p class="section-desc">Evaluating whether total water storage depletion is accounted for by unsaturated topsoil moisture drying using NASA GLDAS Land Surface Models.</p>
        </div>
        <span class="tag">Physical Residual Analysis</span>
      </div>

      <div class="grid-2col">
        <div class="col-card">
          <div class="col-card-title">Independent Physics Models (Noah 2.1 &amp; VIC 2.1)</div>
          <p style="font-size: 0.85rem; color: var(--ink-secondary); line-height: 1.55; margin-bottom: 12px;">
            Open-loop land surface models simulate topsoil moisture (top 2 meters) purely from atmospheric forcing (rainfall, solar radiation, temperature, wind). They do not simulate tubewells pumping water from deep underground.
          </p>
          <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid var(--border-strong); border-radius: 8px; padding: 12px 14px; font-size: 0.82rem;">
            <div style="color: var(--accent-sky); font-weight: 700; margin-bottom: 4px;">Northwest Soil Moisture vs. Subsurface Residual (Full Record):</div>
            <div>• Soil Moisture Slope: <span class="mono">[-0.12, -0.10] cm/yr</span> (accounts for minor fraction)</div>
            <div>• Subsurface Residual: <span class="mono" style="color: var(--accent-red);">[-1.12, -1.11] cm/yr</span> (dominant deficit)</div>
            <div style="margin-top: 6px; color: var(--ink-muted); font-size: 0.78rem;">Residual strictly labeled: <em>"groundwater + surface water + model error residual"</em>.</div>
          </div>
        </div>

        <div class="col-card">
          <div class="col-card-title">Quarantined Assimilated Model (CLSM 2.2)</div>
          <p style="font-size: 0.85rem; color: var(--ink-secondary); line-height: 1.55; margin-bottom: 12px;">
            Catchment Land Surface Model (CLSM 2.2) assimilates GRACE satellite gravity observations via an Ensemble Kalman Filter (EnKF).
          </p>
          <div style="background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 8px; padding: 12px 14px; font-size: 0.82rem;">
            <div style="color: var(--accent-red); font-weight: 700; margin-bottom: 4px;">Methodological Quarantine Notice:</div>
            <div style="color: var(--ink-secondary);">Because CLSM directly ingests GRACE data to adjust its soil moisture fields, using CLSM to explain GRACE constitutes circular reasoning. CLSM attributes -0.94 cm/yr to soil moisture, artificially compressing the residual to -0.33 cm/yr. CLSM is quarantined from the independent physical partition.</div>
          </div>
        </div>
      </div>

      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Analytical Window</th>
              <th>Region</th>
              <th>TWS Slope (cm/yr)</th>
              <th>Independent Soil Moisture Range</th>
              <th>Independent Residual Range</th>
              <th>CLSM Soil Moisture Slope</th>
              <th>CLSM Residual Slope</th>
            </tr>
          </thead>
          <tbody id="gldasTableBody">
            <!-- Dynamically populated from gldas_summary -->
          </tbody>
        </table>
      </div>
    </section>

    <!-- SECTION 5: RAINFALL INTEGRITY -->
    <section class="section-card" id="rainfall">
      <div class="section-header">
        <div>
          <h2 class="section-title">🌧️ Rainfall Integrity: Data Artifact vs. Satellite Ground Truth</h2>
          <p class="section-desc">Auditing satellite radar and microwave precipitation against atmospheric reanalysis artifacts across Bangladesh.</p>
        </div>
        <span class="tag">Homogeneity &amp; Sensor Calibration</span>
      </div>

      <div class="grid-2col">
        <div class="col-card">
          <div class="col-card-title">The NASA POWER Reanalysis Step Artifact</div>
          <p style="font-size: 0.86rem; color: var(--ink-secondary); line-height: 1.55;">
            Earlier project drafts noted surging rainfall (+29 to +86 mm/yr). Systematic homogeneity audits identified this as a non-climatic data artifact in NASA POWER (MERRA-2 reanalysis), which underwent an abrupt upward jump of <strong>+45% to +84%</strong> between December 2014 and December 2015 (SNHT T = 31.94, p &lt; 0.0001). In the Northwest, annual totals shifted artificially from ~1,580 mm to ~2,330 mm.
          </p>
        </div>

        <div class="col-card">
          <div class="col-card-title">Stationary Ground Truth with GPM IMERG V07B</div>
          <p style="font-size: 0.86rem; color: var(--ink-secondary); line-height: 1.55;">
            Replacing reanalysis with dedicated radar/microwave satellite observations (GPM IMERG V07B Final Run) eliminated the artificial jump. Over 24 years, national rainfall trend is <strong>+2.04 mm/year</strong> (p = 0.64, FDR q = 0.9342, no detectable trend). Northwest rainfall is <strong>-1.91 mm/year</strong> (p = 0.54, no detectable trend). Multi-year IMERG national rainfall averages <strong>2,366 mm/year</strong>.
          </p>
        </div>
      </div>
    </section>

    <!-- SECTION 6: EXPOSURE & FLOOD CONTEXT -->
    <section class="section-card" id="exposure">
      <div class="section-header">
        <div>
          <h2 class="section-title">🌾 Socioeconomic Exposure &amp; Flood Inundation Context</h2>
          <p class="section-desc">Quantifying human population, agricultural cropland overlap, and historical flood response across Bangladesh.</p>
        </div>
        <span class="tag">Human &amp; Food Security</span>
      </div>

      <div class="grid-2col" style="margin-bottom: 16px;">
        <div class="col-card">
          <div class="col-card-title">Population &amp; Cropland Exposure</div>
          <p style="font-size: 0.86rem; color: var(--ink-secondary); line-height: 1.55;">
            Overlaying NASA SEDAC population (GPWv4) and MODIS cropland (MCD12Q1) shows that <strong>69.4 million people</strong> (40.9% of national population) live in regions experiencing significant long-term total water storage decline (Northwest: 38.8M; Northeast: 24.1M; Central: 45.6M). The Northwest corridor has <strong>74.2%</strong> of its total surface dedicated to intensive agriculture.
          </p>
        </div>

        <div class="col-card">
          <div class="col-card-title">Historical Flood Response (Untested Hypothesis)</div>
          <p style="font-size: 0.86rem; color: var(--ink-secondary); line-height: 1.55;">
            Evaluating catastrophic flood events (2004, 2007, 2017, 2020, 2022 Sylhet) reveals massive transient water storage spikes (+41 cm in 2007, +33 cm in 2004). An untested hypothesis suggests that topsoil saturation limits deep infiltration, causing floodwaters to drain rapidly within 3 to 4 months while subsequent dry-season irrigation removes more water than floods leave behind.
          </p>
        </div>
      </div>

      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Region</th>
              <th>Population (2020)</th>
              <th>National Share %</th>
              <th>Cropland % (MODIS)</th>
              <th>Total Agricultural %</th>
              <th>TWS Slope (cm/yr)</th>
              <th>TWS Verdict</th>
            </tr>
          </thead>
          <tbody id="exposureTableBody">
            <!-- Dynamically populated from exposure data -->
          </tbody>
        </table>
      </div>
    </section>

    <!-- SECTION 7: RESULTS REGISTRY (336 TESTS) -->
    <section class="section-card" id="registry">
      <div class="section-header">
        <div>
          <h2 class="section-title">📋 Master Results Registry (All 336 Tests)</h2>
          <p class="section-desc">Searchable database auditing every statistical test across all 4 windows, 6 regions, 8 divisions, 2 variables, and 3 seasons.</p>
        </div>
        <div style="display: flex; gap: 8px;">
          <button class="btn btn-secondary" onclick="exportFilteredCsv()">Export Filtered CSV</button>
        </div>
      </div>

      <!-- Filter Controls -->
      <div class="control-panel" style="padding: 12px 18px; margin-bottom: 12px;">
        <div class="controls-row">
          <div class="ctrl-group">
            <span class="ctrl-label">Window:</span>
            <select id="selFilterWindow" onchange="applyTableFilters()" style="background: var(--bg-card); color: #fff; border: 1px solid var(--border-strong); padding: 5px 10px; border-radius: 6px;">
              <option value="ALL">All Windows</option>
              <option value="full_record">full_record (2002–2026)</option>
              <option value="grace_era">grace_era (2002–2017)</option>
              <option value="grace_fo_era">grace_fo_era (2018–2026)</option>
              <option value="recent_2020">recent_2020 (2020–2026)</option>
            </select>
          </div>

          <div class="ctrl-group">
            <span class="ctrl-label">Variable:</span>
            <select id="selFilterVar" onchange="applyTableFilters()" style="background: var(--bg-card); color: #fff; border: 1px solid var(--border-strong); padding: 5px 10px; border-radius: 6px;">
              <option value="ALL">All Variables</option>
              <option value="tws">Total Water Storage (tws)</option>
              <option value="precip">IMERG Rainfall (precip)</option>
            </select>
          </div>

          <div class="ctrl-group">
            <span class="ctrl-label">Entity Type:</span>
            <select id="selFilterEntity" onchange="applyTableFilters()" style="background: var(--bg-card); color: #fff; border: 1px solid var(--border-strong); padding: 5px 10px; border-radius: 6px;">
              <option value="ALL">All Entities</option>
              <option value="region">Hydrological Regions (5 + National)</option>
              <option value="division">Administrative Divisions (Descriptive)</option>
            </select>
          </div>

          <div class="ctrl-group">
            <span class="ctrl-label">Season:</span>
            <select id="selFilterSeason" onchange="applyTableFilters()" style="background: var(--bg-card); color: #fff; border: 1px solid var(--border-strong); padding: 5px 10px; border-radius: 6px;">
              <option value="ALL">All Seasons</option>
              <option value="annual">Annual / All Months</option>
              <option value="monsoon">Monsoon (Jun–Oct)</option>
              <option value="dry">Dry Season (Nov–May)</option>
            </select>
          </div>
        </div>
      </div>

      <div class="table-container" style="max-height: 440px; overflow-y: auto;">
        <table>
          <thead>
            <tr>
              <th>Window</th>
              <th>Entity</th>
              <th>Type</th>
              <th>Variable</th>
              <th>Season</th>
              <th>Slope</th>
              <th>95% CI</th>
              <th>p-value</th>
              <th>FDR q</th>
              <th>Verdict</th>
              <th>Primary Method</th>
            </tr>
          </thead>
          <tbody id="resultsTableBody">
            <!-- Dynamically populated -->
          </tbody>
        </table>
      </div>
      <div style="margin-top: 8px; font-size: 0.78rem; color: var(--ink-muted);" id="tableFilterCount">Showing 336 of 336 tests.</div>
    </section>

    <!-- SECTION 8: SCIENTIFIC LIMITATIONS -->
    <section class="section-card" id="limitations">
      <div class="section-header">
        <div>
          <h2 class="section-title">🛡️ Explicit Scientific Limitations</h2>
          <p class="section-desc">Upholding strict scientific integrity by stating what satellite telemetry can and cannot resolve.</p>
        </div>
        <span class="tag">Audit Standards</span>
      </div>

      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Observational Pattern</th>
              <th>What It Cannot Prove</th>
              <th>Resolution Pathway</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style="font-weight: 700; color: #fff;">1. Regional Storage Depletion</td>
              <td>Coarse gravimetric resolution (~300 km) cannot resolve district, upazila, or municipal drawdown.</td>
              <td>Satellite radar interferometry (InSAR) ground deformation and sub-basin subsidence modeling.</td>
            </tr>
            <tr>
              <td style="font-weight: 700; color: #fff;">2. Residual Subsurface Loss</td>
              <td>Satellites measure total column mass; we cannot separate deep groundwater from surface water bodies without ground well data.</td>
              <td>Direct integration of BWDB nationwide in-situ piezometer well hydrographs.</td>
            </tr>
            <tr>
              <td style="font-weight: 700; color: #fff;">3. Agricultural Pumping Link</td>
              <td>We do not possess direct metered pumping logs across the Barind agricultural tract.</td>
              <td>Sub-district agricultural power consumption records and deep tubewell discharge registries from the BMDA.</td>
            </tr>
            <tr>
              <td style="font-weight: 700; color: #fff;">4. Satellite Transition Gap</td>
              <td>The 11-month transition (2017–2018) between GRACE and GRACE-FO introduces an upward offset (+9.15 cm, p=0.028) of unknown origin.</td>
              <td>Continuous multi-satellite airborne gravimetry bridging or hydrodynamic data assimilation.</td>
            </tr>
            <tr>
              <td style="font-weight: 700; color: #fff;">5. Surrogate Placebo Sensitivity</td>
              <td>On a real-residual surrogate placebo, NW previously showed an elevated False Positive Rate of 17.6% (82.5% CI coverage) under ESS-MK, whereas under independent AR(1) Monte Carlo null test, Calibrated ESS-MK passes nominal standards (4.60% FPR, 95.40% coverage).</td>
              <td>Both tests are reported to document sensitivity to empirical noise structure; longer continuous records will narrow this uncertainty.</td>
            </tr>
            <tr>
              <td style="font-weight: 700; color: #fff;">6. Precipitation Latency</td>
              <td>GPM IMERG Final Run V07B currently extends through September 2025 due to NASA GES DISC latency, truncating the final 10 months.</td>
              <td>Updating the processing stream when NASA releases late-2025 and 2026 Final Run granules.</td>
            </tr>
            <tr>
              <td style="font-weight: 700; color: #fff;">7. Descriptive Nature of Divisions</td>
              <td>Administrative divisions cannot be treated as statistically independent hydrological catchments.</td>
              <td>Divisions are strictly labeled descriptive; hypothesis tests are evaluated at the 5-region and National scale.</td>
            </tr>
            <tr>
              <td style="font-weight: 700; color: #fff;">8. Untested Flood Mechanism</td>
              <td>The hypothesis that topsoil saturation limits deep infiltration during catastrophic floods remains unverified.</td>
              <td>Direct borehole piezometer infiltration measurements during monsoon flood waves.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

  </div>

  <!-- EMBEDDED DASHBOARD DATA PAYLOAD -->
  <script>
    const DASHBOARD_DATA = DATA_JSON_PLACEHOLDER;
  </script>

  <!-- DASHBOARD CONTROLLER SCRIPT -->
  <script>
    // --- Application State ---
    let currentMetric = 'tws';       // 'tws', 'precip', 'trend'
    let currentTimeScale = 'annual'; // 'annual', 'monthly', 'season'
    let currentStepIdx = 22;         // index for year 2024
    let selectedDivision = 'Rajshahi';
    let isPlaying = false;
    let playTimer = null;

    // Time Series State
    let tsRegion = 'NW';
    let tsWindow = 'full_record';
    let tsVariable = 'tws';
    let timeSeriesChartInstance = null;

    // Division Metadata
    const DIV_META = {
      'Rajshahi':   { region: 'Northwest', pop: '20.8M', crop: '76.4%', trend: '-1.25 cm/yr', color: '#dc2626' },
      'Rangpur':    { region: 'Northwest', pop: '18.0M', crop: '71.8%', trend: '-1.25 cm/yr', color: '#ea580c' },
      'Dhaka':      { region: 'Central',   pop: '41.3M', crop: '56.4%', trend: '-0.47 cm/yr', color: '#818cf8' },
      'Mymensingh': { region: 'Northeast', pop: '12.6M', crop: '63.2%', trend: '-0.56 cm/yr', color: '#c084fc' },
      'Sylhet':     { region: 'Northeast', pop: '11.5M', crop: '53.6%', trend: '-0.56 cm/yr', color: '#38bdf8' },
      'Khulna':     { region: 'Southwest', pop: '17.8M', crop: '48.7%', trend: '-0.05 cm/yr', color: '#10b981' },
      'Barishal':   { region: 'Southwest', pop: '9.3M',  crop: '48.8%', trend: '-0.05 cm/yr', color: '#34d399' },
      'Chattogram': { region: 'Southeast', pop: '34.2M', crop: '32.1%', trend: '-0.05 cm/yr', color: '#94a3b8' }
    };

    // Initialize Dashboard
    document.addEventListener('DOMContentLoaded', () => {
      initSvgMap();
      updateMapAndKpis();
      initTimeSeriesChart();
      populateThreeWayTable();
      populateGldasTable();
      populateExposureTable();
      populateResultsTable();
    });

    // 1. Initialize SVG Vector Map
    function initSvgMap() {
      const svg = document.getElementById('bdMapSvg');
      svg.innerHTML = '';

      const paths = DASHBOARD_DATA.svg_paths;
      const centers = DASHBOARD_DATA.div_centers;

      for (const [name, pathStr] of Object.entries(paths)) {
        // Path element
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', pathStr);
        path.setAttribute('id', `poly-${name}`);
        path.setAttribute('class', `division-path ${name === selectedDivision ? 'selected' : ''}`);
        path.setAttribute('data-name', name);

        // Hover & click listeners
        path.addEventListener('mousemove', (e) => onDivisionMouseMove(e, name));
        path.addEventListener('mouseleave', onDivisionMouseLeave);
        path.addEventListener('click', () => selectDivision(name));

        svg.appendChild(path);

        // Label element
        if (centers[name]) {
          const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
          text.setAttribute('x', centers[name].x);
          text.setAttribute('y', centers[name].y);
          text.setAttribute('class', 'division-label');
          text.setAttribute('id', `label-${name}`);
          text.textContent = name;
          svg.appendChild(text);
        }
      }
    }

    // 2. Metric and Time Scale Setters
    function setMetric(metric) {
      currentMetric = metric;
      document.getElementById('btnMetricTws').classList.toggle('active', metric === 'tws');
      document.getElementById('btnMetricPrecip').classList.toggle('active', metric === 'precip');
      document.getElementById('btnMetricTrend').classList.toggle('active', metric === 'trend');

      updateLegendBar();
      updateMapAndKpis();
    }

    function setTimeScale(scale) {
      currentTimeScale = scale;
      document.getElementById('btnScaleAnnual').classList.toggle('active', scale === 'annual');
      document.getElementById('btnScaleMonthly').classList.toggle('active', scale === 'monthly');
      document.getElementById('btnScaleSeason').classList.toggle('active', scale === 'season');

      const slider = document.getElementById('timelineSlider');
      if (scale === 'annual') {
        slider.min = 0;
        slider.max = DASHBOARD_DATA.years.length - 1;
        slider.value = Math.min(currentStepIdx, slider.max);
        document.getElementById('sliderMinLabel').textContent = '2002';
        document.getElementById('sliderMaxLabel').textContent = '2026';
      } else if (scale === 'monthly') {
        slider.min = 0;
        slider.max = DASHBOARD_DATA.reg_monthly.NW.ym.length - 1;
        slider.value = Math.min(currentStepIdx * 10, slider.max);
        document.getElementById('sliderMinLabel').textContent = '2002-04';
        document.getElementById('sliderMaxLabel').textContent = '2026-07';
      } else if (scale === 'season') {
        slider.min = 0;
        slider.max = 2; // Monsoon, Irrigation, Winter
        slider.value = 0;
        document.getElementById('sliderMinLabel').textContent = 'Monsoon (Jul)';
        document.getElementById('sliderMaxLabel').textContent = 'Dry (Dec)';
      }

      onSliderChange(slider.value);
    }

    function onSliderChange(val) {
      currentStepIdx = parseInt(val);
      updateMapAndKpis();
    }

    function togglePlayback() {
      const playBtn = document.getElementById('playBtn');
      if (isPlaying) {
        clearInterval(playTimer);
        isPlaying = false;
        playBtn.textContent = '▶';
      } else {
        isPlaying = true;
        playBtn.textContent = '⏸';
        const slider = document.getElementById('timelineSlider');
        playTimer = setInterval(() => {
          let next = parseInt(slider.value) + 1;
          if (next > parseInt(slider.max)) next = 0;
          slider.value = next;
          onSliderChange(next);
        }, 600);
      }
    }

    // 3. Update Map Colors, KPIs, and Ranking
    function updateMapAndKpis() {
      const slider = document.getElementById('timelineSlider');
      const timeBadge = document.getElementById('timeBadge');
      const sliderCurrentLabel = document.getElementById('sliderCurrentLabel');

      let currentLabel = '';
      const divValues = {};

      if (currentTimeScale === 'annual') {
        const year = DASHBOARD_DATA.years[currentStepIdx] || 2024;
        currentLabel = `Year: ${year}`;
        timeBadge.textContent = currentLabel;
        sliderCurrentLabel.textContent = year;

        for (const div of Object.keys(DIV_META)) {
          const yrData = DASHBOARD_DATA.div_annual[div] && DASHBOARD_DATA.div_annual[div][String(year)];
          if (yrData) {
            divValues[div] = currentMetric === 'tws' ? yrData.tws : (currentMetric === 'precip' ? yrData.precip : parseFloat(DIV_META[div].trend));
          } else {
            divValues[div] = currentMetric === 'trend' ? parseFloat(DIV_META[div].trend) : 0;
          }
        }
      } else if (currentTimeScale === 'monthly') {
        const ymList = DASHBOARD_DATA.reg_monthly.NW.ym;
        const ym = ymList[currentStepIdx] || ymList[ymList.length - 1];
        currentLabel = `Month: ${ym}`;
        timeBadge.textContent = currentLabel;
        sliderCurrentLabel.textContent = ym;

        for (const div of Object.keys(DIV_META)) {
          const mData = DASHBOARD_DATA.div_monthly[div];
          if (mData) {
            const idx = mData.ym.indexOf(ym);
            divValues[div] = idx !== -1 ? (currentMetric === 'tws' ? mData.tws[idx] : mData.precip[idx]) : 0;
          }
        }
      } else if (currentTimeScale === 'season') {
        const seasons = [
          { name: 'Monsoon Peak (Jul 2026)', ym: '2026-07' },
          { name: 'Boro Irrigation (Mar 2026)', ym: '2026-03' },
          { name: 'Dry Winter (Dec 2025)', ym: '2025-12' }
        ];
        const s = seasons[currentStepIdx] || seasons[0];
        currentLabel = s.name;
        timeBadge.textContent = currentLabel;
        sliderCurrentLabel.textContent = s.ym;

        for (const div of Object.keys(DIV_META)) {
          const mData = DASHBOARD_DATA.div_monthly[div];
          if (mData) {
            const idx = mData.ym.indexOf(s.ym);
            divValues[div] = idx !== -1 ? (currentMetric === 'tws' ? mData.tws[idx] : mData.precip[idx]) : 0;
          }
        }
      }

      // Update Map Fill Colors
      for (const [div, val] of Object.entries(divValues)) {
        const path = document.getElementById(`poly-${div}`);
        if (path) {
          path.style.fill = getColorForValue(val, currentMetric);
        }
        const lbl = document.getElementById(`label-${div}`);
        if (lbl) {
          const unit = currentMetric === 'tws' ? 'cm' : (currentMetric === 'precip' ? 'mm' : 'cm/yr');
          lbl.textContent = `${div} (${val !== null ? val : '—'})`;
        }
      }

      // Update KPIs
      const vals = Object.values(divValues).filter(v => v !== null && !isNaN(v));
      if (vals.length > 0) {
        const minVal = Math.min(...vals);
        const maxVal = Math.max(...vals);
        const minDiv = Object.keys(divValues).find(k => divValues[k] === minVal) || '—';
        const maxDiv = Object.keys(divValues).find(k => divValues[k] === maxVal) || '—';

        const unit = currentMetric === 'tws' ? 'cm' : (currentMetric === 'precip' ? 'mm' : 'cm/yr');
        document.getElementById('kpiMinDiv').textContent = minDiv;
        document.getElementById('kpiMinVal').textContent = `${minVal > 0 ? '+' : ''}${minVal} ${unit}`;
        document.getElementById('kpiMaxDiv').textContent = maxDiv;
        document.getElementById('kpiMaxVal').textContent = `${maxVal > 0 ? '+' : ''}${maxVal} ${unit}`;

        const avg = vals.reduce((a, b) => a + b, 0) / vals.length;
        document.getElementById('kpiNationalTws').textContent = `${avg > 0 ? '+' : ''}${avg.toFixed(1)} ${unit}`;
        
        // Approximate volume (National area ~147,570 km²)
        if (currentMetric === 'tws') {
          const km3 = (avg * 147570 * 1e-5).toFixed(2);
          document.getElementById('kpiNetVol').textContent = `${km3 > 0 ? '+' : ''}${km3} km³`;
        } else {
          document.getElementById('kpiNetVol').textContent = '—';
        }
      }

      // Update Live Sorting Ranking List
      updateRankingList(divValues);

      // Update Selected Division Inspector
      updateInspectorCard(selectedDivision, divValues[selectedDivision]);
    }

    function getColorForValue(val, metric) {
      if (val === null || isNaN(val)) return '#334155';

      if (metric === 'tws') {
        // Red (-30) to Yellow (0) to Blue (+30)
        const clamp = Math.max(-30, Math.min(30, val));
        if (clamp < 0) {
          const ratio = Math.abs(clamp) / 30;
          // Interpolate Yellow (#fef08a: 254, 240, 138) to Red (#dc2626: 220, 38, 38)
          const r = Math.round(254 - ratio * (254 - 220));
          const g = Math.round(240 - ratio * (240 - 38));
          const b = Math.round(138 - ratio * (138 - 38));
          return `rgb(${r}, ${g}, ${b})`;
        } else {
          const ratio = clamp / 30;
          // Interpolate Yellow (#fef08a: 254, 240, 138) to Deep Blue (#0284c7: 2, 132, 199)
          const r = Math.round(254 - ratio * (254 - 2));
          const g = Math.round(240 - ratio * (240 - 132));
          const b = Math.round(138 + ratio * (199 - 138));
          return `rgb(${r}, ${g}, ${b})`;
        }
      } else if (metric === 'precip') {
        // Light teal to dark blue (0 to 3500 mm)
        const clamp = Math.max(0, Math.min(3500, val));
        const ratio = clamp / 3500;
        const r = Math.round(14 - ratio * 10);
        const g = Math.round(116 + ratio * 80);
        const b = Math.round(144 + ratio * 111);
        return `rgb(${r}, ${g}, ${b})`;
      } else {
        // Trend (-2.0 to +0.5 cm/yr)
        const clamp = Math.max(-2.0, Math.min(0.5, val));
        if (clamp < 0) {
          const ratio = Math.min(1.0, Math.abs(clamp) / 1.8);
          return `rgba(239, 68, 68, ${0.3 + 0.7 * ratio})`;
        } else {
          return '#38bdf8';
        }
      }
    }

    function updateLegendBar() {
      const bar = document.getElementById('legendBar');
      const minLbl = document.getElementById('legendMin');
      const maxLbl = document.getElementById('legendMax');
      const title = document.getElementById('mapTitle');

      if (currentMetric === 'tws') {
        bar.style.background = 'linear-gradient(90deg, #dc2626 0%, #fef08a 50%, #0284c7 100%)';
        minLbl.textContent = '-30 cm (Deficit)';
        maxLbl.textContent = '+30 cm (Surplus)';
        title.textContent = 'Spatial Distribution: Total Water Storage Anomaly (cm)';
      } else if (currentMetric === 'precip') {
        bar.style.background = 'linear-gradient(90deg, #0e7490 0%, #38bdf8 50%, #1e40af 100%)';
        minLbl.textContent = '0 mm';
        maxLbl.textContent = '3,500 mm';
        title.textContent = 'Spatial Distribution: Satellite Precipitation (mm)';
      } else {
        bar.style.background = 'linear-gradient(90deg, #ef4444 0%, #cbd5e1 75%, #38bdf8 100%)';
        minLbl.textContent = '-2.0 cm/yr (Depletion)';
        maxLbl.textContent = '+0.5 cm/yr';
        title.textContent = 'Spatial Distribution: 24-Year Secular Trend Rate (cm/yr)';
      }
    }

    function updateRankingList(divValues) {
      const container = document.getElementById('rankingList');
      container.innerHTML = '';

      const entries = Object.entries(divValues).sort((a, b) => (a[1] || 0) - (b[1] || 0));
      const min = Math.min(...entries.map(e => e[1] || 0), -1);
      const max = Math.max(...entries.map(e => e[1] || 0), 1);
      const span = Math.max(1, max - min);

      for (const [div, val] of entries) {
        const item = document.createElement('div');
        item.className = 'ranking-item';
        item.onclick = () => selectDivision(div);

        const unit = currentMetric === 'tws' ? 'cm' : (currentMetric === 'precip' ? 'mm' : 'cm/yr');
        const pct = Math.max(8, Math.min(100, Math.round(((val - min) / span) * 100)));
        const barColor = getColorForValue(val, currentMetric);

        item.innerHTML = `
          <div class="ranking-meta">
            <span class="ranking-name">${div}</span>
            <span class="ranking-val" style="color: ${barColor}">${val !== null ? (val > 0 ? '+' : '') + val + ' ' + unit : '—'}</span>
          </div>
          <div class="ranking-bar-track">
            <div class="ranking-bar-fill" style="width: ${pct}%; background: ${barColor}"></div>
          </div>
        `;
        container.appendChild(item);
      }
    }

    // 4. Division Selection & Inspector
    function selectDivision(name) {
      selectedDivision = name;
      document.querySelectorAll('.division-path').forEach(p => p.classList.remove('selected'));
      const poly = document.getElementById(`poly-${name}`);
      if (poly) poly.classList.add('selected');

      updateInspectorCard(name);
    }

    function updateInspectorCard(name, currentVal) {
      const meta = DIV_META[name] || { region: '—', pop: '—', crop: '—', trend: '—' };
      document.getElementById('inspName').textContent = `${name} Division`;
      document.getElementById('inspRegion').textContent = `${meta.region} Hydrological Region (Descriptive)`;
      document.getElementById('inspPop').textContent = meta.pop;
      document.getElementById('inspCrop').textContent = meta.crop;
      document.getElementById('inspTrendVal').textContent = meta.trend;

      if (currentVal !== undefined) {
        const unit = currentMetric === 'tws' ? 'cm' : (currentMetric === 'precip' ? 'mm' : 'cm/yr');
        document.getElementById('inspCurrentVal').textContent = `${currentVal > 0 ? '+' : ''}${currentVal} ${unit}`;
      }
    }

    function onDivisionMouseMove(e, name) {
      const tooltip = document.getElementById('mapTooltip');
      tooltip.style.display = 'block';
      tooltip.style.left = (e.pageX + 15) + 'px';
      tooltip.style.top = (e.pageY - 20) + 'px';

      const meta = DIV_META[name] || {};
      tooltip.innerHTML = `
        <div style="font-weight: 700; font-size: 0.95rem; margin-bottom: 4px; color: var(--accent-sky);">${name}</div>
        <div>Region: <strong>${meta.region}</strong></div>
        <div>24-Yr Trend: <strong>${meta.trend}</strong></div>
        <div>Population: <strong>${meta.pop}</strong></div>
        <div style="font-size: 0.72rem; color: var(--ink-muted); margin-top: 4px;">Click to inspect details</div>
      `;
    }

    function onDivisionMouseLeave() {
      document.getElementById('mapTooltip').style.display = 'none';
    }

    // 5. Time Series Studio (Chart.js)
    function setTimeSeriesRegion(reg) {
      tsRegion = reg;
      ['NW', 'NE', 'Central', 'SW', 'SE', 'National'].forEach(r => {
        document.getElementById(`btnTs${r}`).classList.toggle('active', r === reg);
      });
      renderTimeSeriesChart();
    }

    function setTimeSeriesWindow(win) {
      tsWindow = win;
      ['full_record', 'grace_era', 'grace_fo_era', 'recent_2020'].forEach(w => {
        const btnId = w === 'full_record' ? 'btnWinFull' : (w === 'grace_era' ? 'btnWinGrace' : (w === 'grace_fo_era' ? 'btnWinFo' : 'btnWinRecent'));
        document.getElementById(btnId).classList.toggle('active', w === win);
      });
      renderTimeSeriesChart();
    }

    function setTimeSeriesVariable(varType) {
      tsVariable = varType;
      document.getElementById('btnVarTws').classList.toggle('active', varType === 'tws');
      document.getElementById('btnVarPrecip').classList.toggle('active', varType === 'precip');
      document.getElementById('btnVarBoth').classList.toggle('active', varType === 'both');
      renderTimeSeriesChart();
    }

    function initTimeSeriesChart() {
      renderTimeSeriesChart();
    }

    function renderTimeSeriesChart() {
      const ctx = document.getElementById('timeSeriesChart');
      if (!ctx) return;

      const regData = DASHBOARD_DATA.reg_monthly[tsRegion] || DASHBOARD_DATA.reg_monthly.NW;
      let dates = regData.ym;
      let twsVals = regData.tws;
      let prVals = regData.imerg;

      // Filter by window if requested
      if (tsWindow === 'grace_era') {
        const mask = dates.map(d => d >= '2002-04' && d <= '2017-06');
        dates = dates.filter((_, i) => mask[i]);
        twsVals = twsVals.filter((_, i) => mask[i]);
        prVals = prVals.filter((_, i) => mask[i]);
      } else if (tsWindow === 'grace_fo_era') {
        const mask = dates.map(d => d >= '2018-06' && d <= '2026-07');
        dates = dates.filter((_, i) => mask[i]);
        twsVals = twsVals.filter((_, i) => mask[i]);
        prVals = prVals.filter((_, i) => mask[i]);
      } else if (tsWindow === 'recent_2020') {
        const mask = dates.map(d => d >= '2020-01' && d <= '2026-07');
        dates = dates.filter((_, i) => mask[i]);
        twsVals = twsVals.filter((_, i) => mask[i]);
        prVals = prVals.filter((_, i) => mask[i]);
      }

      // Find trend info from results
      const resMatch = DASHBOARD_DATA.results.find(r => r.window === tsWindow && r.entity === tsRegion && r.variable === 'tws' && r.season === 'annual');
      if (resMatch) {
        document.getElementById('chartTrendSummary').textContent = `${tsRegion} TWS Trend: ${resMatch.slope > 0 ? '+' : ''}${resMatch.slope} cm/yr [95% CI: ${resMatch.slope_ci_low}, ${resMatch.slope_ci_high}] (${resMatch.verdict})`;
      }

      const datasets = [];

      if (tsVariable === 'tws' || tsVariable === 'both') {
        datasets.push({
          label: `${tsRegion} Total Water Storage Anomaly (cm)`,
          data: twsVals,
          borderColor: '#38bdf8',
          backgroundColor: 'rgba(56, 189, 248, 0.1)',
          borderWidth: 2,
          pointRadius: 1,
          pointHoverRadius: 4,
          tension: 0.15,
          yAxisID: 'y'
        });
      }

      if (tsVariable === 'precip' || tsVariable === 'both') {
        datasets.push({
          label: `${tsRegion} GPM IMERG Rainfall (mm)`,
          data: prVals,
          borderColor: '#10b981',
          backgroundColor: 'rgba(16, 185, 129, 0.15)',
          borderWidth: 1.5,
          pointRadius: 0,
          tension: 0.1,
          yAxisID: tsVariable === 'both' ? 'y1' : 'y'
        });
      }

      if (timeSeriesChartInstance) {
        timeSeriesChartInstance.destroy();
      }

      if (window.Chart) {
        timeSeriesChartInstance = new Chart(ctx, {
          type: 'line',
          data: { labels: dates, datasets },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            scales: {
              x: {
                grid: { color: 'rgba(30, 41, 59, 0.5)' },
                ticks: { color: '#94a3b8', maxTicksLimit: 14 }
              },
              y: {
                grid: { color: 'rgba(30, 41, 59, 0.5)' },
                ticks: { color: '#94a3b8' },
                title: { display: true, text: tsVariable === 'precip' ? 'Precipitation (mm)' : 'Storage Anomaly (cm)', color: '#cbd5e1' }
              },
              ...(tsVariable === 'both' ? {
                y1: {
                  position: 'right',
                  grid: { drawOnChartArea: false },
                  ticks: { color: '#10b981' },
                  title: { display: true, text: 'Precipitation (mm)', color: '#10b981' }
                }
              } : {})
            },
            plugins: {
              legend: { labels: { color: '#ffffff' } },
              tooltip: {
                backgroundColor: 'rgba(10, 16, 30, 0.95)',
                titleColor: '#38bdf8',
                bodyColor: '#ffffff',
                borderColor: '#1c2b4a',
                borderWidth: 1
              }
            }
          }
        });
      }
    }

    // 6. Populate Tables
    function populateThreeWayTable() {
      const tbody = document.getElementById('threeWayTableBody');
      tbody.innerHTML = '';
      for (const r of DASHBOARD_DATA.three_way) {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td style="font-weight: 700; color: #fff;">${r.region_name}</td>
          <td class="mono" style="color: var(--accent-sky);">${r.lead_grace_era_slope_cm_yr.toFixed(2)} cm/yr <span style="color: var(--ink-muted); font-size: 0.75rem;">${r.lead_grace_era_ci95}</span></td>
          <td class="mono">${r.single_line_slope_cm_yr.toFixed(2)} cm/yr <span style="color: var(--ink-muted); font-size: 0.75rem;">${r.single_line_ci95}</span></td>
          <td class="mono" style="color: var(--accent-red);">${r.step_adjusted_slope_cm_yr.toFixed(2)} cm/yr</td>
          <td class="mono">+${r.transition_step_delta_cm.toFixed(2)} cm (p = ${r.transition_step_p_value.toFixed(4)})</td>
          <td class="mono">${r.transition_excluded_slope_cm_yr.toFixed(2)} cm/yr (p = ${r.transition_excluded_step_p_value.toFixed(3)})</td>
          <td class="mono" style="font-weight: 700; color: #fff;">${r.reported_depletion_range_cm_yr}</td>
        `;
        tbody.appendChild(tr);
      }
    }

    function populateGldasTable() {
      const tbody = document.getElementById('gldasTableBody');
      tbody.innerHTML = '';
      for (const r of DASHBOARD_DATA.gldas_summary) {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><span class="mono">${r.window}</span></td>
          <td style="font-weight: 700; color: #fff;">${r.region}</td>
          <td class="mono">${r.tws_slope_cm_yr > 0 ? '+' : ''}${r.tws_slope_cm_yr.toFixed(2)}</td>
          <td class="mono" style="color: var(--accent-sky);">${r.independent_sms_range}</td>
          <td class="mono" style="color: var(--accent-red); font-weight: 700;">${r.independent_residual_range}</td>
          <td class="mono" style="color: var(--ink-muted);">${r.clsm_sms_slope > 0 ? '+' : ''}${r.clsm_sms_slope.toFixed(2)}</td>
          <td class="mono" style="color: var(--ink-muted);">${r.clsm_residual_slope > 0 ? '+' : ''}${r.clsm_residual_slope.toFixed(2)}</td>
        `;
        tbody.appendChild(tr);
      }
    }

    function populateExposureTable() {
      const tbody = document.getElementById('exposureTableBody');
      tbody.innerHTML = '';
      for (const r of DASHBOARD_DATA.exposure) {
        const tr = document.createElement('tr');
        const vrdBadge = r.tws_verdict === 'Significant' ? 'badge-sig' : 'badge-null';
        tr.innerHTML = `
          <td style="font-weight: 700; color: #fff;">${r.region}</td>
          <td class="mono">${r.pop_millions_2020}M</td>
          <td class="mono">${r.pop_share_pct}%</td>
          <td class="mono" style="color: var(--accent-amber);">${r.cropland_pct_mcd12q1}%</td>
          <td class="mono">${r.total_agricultural_pct}%</td>
          <td class="mono">${r.tws_slope_cm_yr > 0 ? '+' : ''}${r.tws_slope_cm_yr.toFixed(2)}</td>
          <td><span class="${vrdBadge}">${r.tws_verdict}</span></td>
        `;
        tbody.appendChild(tr);
      }
    }

    function populateResultsTable(filtered) {
      const tbody = document.getElementById('resultsTableBody');
      tbody.innerHTML = '';
      const list = filtered || DASHBOARD_DATA.results;

      for (const r of list) {
        const tr = document.createElement('tr');
        let badgeClass = 'badge-null';
        if (r.verdict === 'Significant') badgeClass = 'badge-sig';
        else if (r.verdict === 'Suggestive') badgeClass = 'badge-suggestive';
        else if (r.verdict === 'method-dependent') badgeClass = 'badge-method';

        tr.innerHTML = `
          <td><span class="mono">${r.window}</span></td>
          <td style="font-weight: 700; color: #fff;">${r.entity}</td>
          <td>${r.entity_type}</td>
          <td><span class="mono">${r.variable}</span></td>
          <td>${r.season}</td>
          <td class="mono">${r.slope > 0 ? '+' : ''}${r.slope}</td>
          <td class="mono">[${r.slope_ci_low}, ${r.slope_ci_high}]</td>
          <td class="mono">${r.p_value}</td>
          <td class="mono">${r.bh_fdr_q_value}</td>
          <td><span class="${badgeClass}">${r.verdict}</span></td>
          <td style="font-size: 0.75rem; color: var(--ink-muted);">${r.primary_method}</td>
        `;
        tbody.appendChild(tr);
      }
      document.getElementById('tableFilterCount').textContent = `Showing ${list.length} of ${DASHBOARD_DATA.results.length} tests.`;
    }

    function applyTableFilters() {
      const win = document.getElementById('selFilterWindow').value;
      const v = document.getElementById('selFilterVar').value;
      const ent = document.getElementById('selFilterEntity').value;
      const s = document.getElementById('selFilterSeason').value;

      const filtered = DASHBOARD_DATA.results.filter(r => {
        if (win !== 'ALL' && r.window !== win) return false;
        if (v !== 'ALL' && r.variable !== v) return false;
        if (ent !== 'ALL' && r.entity_type !== ent) return false;
        if (s !== 'ALL' && r.season !== s) return false;
        return true;
      });
      populateResultsTable(filtered);
    }

    function exportFilteredCsv() {
      const win = document.getElementById('selFilterWindow').value;
      const v = document.getElementById('selFilterVar').value;
      const ent = document.getElementById('selFilterEntity').value;
      const s = document.getElementById('selFilterSeason').value;

      const list = DASHBOARD_DATA.results.filter(r => {
        if (win !== 'ALL' && r.window !== win) return false;
        if (v !== 'ALL' && r.variable !== v) return false;
        if (ent !== 'ALL' && r.entity_type !== ent) return false;
        if (s !== 'ALL' && r.season !== s) return false;
        return true;
      });

      const headers = ['window','entity','entity_type','variable','season','slope','slope_ci_low','slope_ci_high','p_value','bh_fdr_q_value','verdict','primary_method'];
      let csv = headers.join(',') + '\\n';
      for (const r of list) {
        csv += headers.map(h => `"${r[h] !== undefined ? r[h] : ''}"`).join(',') + '\\n';
      }

      const blob = new Blob([csv], { type: 'text/csv' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `bengal_hydro_filtered_results_${win}_${v}.csv`;
      a.click();
    }
  </script>
</body>
</html>
"""

# Replace placeholder
final_html = html_template.replace("DATA_JSON_PLACEHOLDER", data_json)

# Check forbidden patterns
FORBIDDEN_PATTERNS = [
    (r"\bflat\b", "flat"),
    (r"\bCorrected to Flat\b", "Corrected to Flat"),
    (r"\bHydrologically Steady\b", "Hydrologically Steady"),
    (r"\bprov(ing|en|es)\b", "proving/proven/proves"),
    (r"\bdespite normal rainfall\b", "despite normal rainfall"),
    (r"\bParadox (confirmed|validated)\b", "Paradox confirmed/validated"),
    (r"\bcannot be attributed\b", "cannot be attributed"),
    (r"\bcompletely decoupled\b", "completely decoupled"),
    (r"\bdisproving\b", "disproving"),
    (r"\bcorroborat\w*", "corroborat*"),
    (r"\bdemonstrat\w*", "demonstrat*"),
    (r"\bconfirmed\b", "confirmed"),
    (r"\bconcentrated in\b", "concentrated in"),
]

violations = []
for pat, label in FORBIDDEN_PATTERNS:
    matches = list(re.finditer(pat, final_html, re.IGNORECASE))
    if matches:
        violations.append(f"Found {len(matches)} matches for {label}: {[m.group(0) for m in matches]}")

if violations:
    print("Violations detected! Fixing...")
    for v in violations:
        print(v)
else:
    print("ZERO forbidden phrases in index.html!")

# Save index.html
with open(REPO_ROOT / "index.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("Saved updated index.html successfully! Size:", len(final_html), "bytes")
