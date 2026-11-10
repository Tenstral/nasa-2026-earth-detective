/**
 * NASA Space Apps 2026 - Trend Detective
 * assets/js/app.js
 * =====================================
 * Main application controller implementing Dr. James Acker's 5-step analytical workflow:
 *   Step 1: Select Data Variable(s)
 *   Step 2: Define Geographic Region
 *   Step 3: Select Time Window & Season
 *   Step 4: Generate & Inspect Time Series Visualization
 *   Step 5: Test for Statistical Significance (p < 0.05 + FDR audit)
 */

(function () {
  'use strict';

  // Global State
  const state = {
    variable: 'grace_tws',
    overlayVariable: null,
    spatialType: 'region', // 'region' or 'division'
    entity: 'NW',
    startYear: 2002,
    endYear: 2026,
    season: 'annual',
    showDeseasonalized: true,
    showTrendLine: true,
    showGap: true,
    showFloodMarkers: true,
    activeCaseId: null
  };

  let chartInstance = null;

  // DOM Elements cache
  const el = {};

  function initElements() {
    el.varCards = document.getElementById('var-cards-container');
    el.overlaySelect = document.getElementById('overlay-select');
    el.spatialToggle = document.getElementById('spatial-toggle');
    el.svgMap = document.getElementById('svg-map-container');
    el.regionsList = document.getElementById('regions-list-container');
    el.regionalCaveat = document.getElementById('regional-caveat');
    el.startYear = document.getElementById('start-year-select');
    el.endYear = document.getElementById('end-year-select');
    el.seasonSelect = document.getElementById('season-select');
    el.timePresets = document.getElementById('time-presets-container');
    el.chartCanvas = document.getElementById('timeseries-canvas');
    el.chartTitle = document.getElementById('chart-title');
    el.chartSubtitle = document.getElementById('chart-subtitle');
    el.toggleDeseason = document.getElementById('toggle-deseason');
    el.toggleTrendLine = document.getElementById('toggle-trendline');
    el.verdictBadge = document.getElementById('verdict-badge');
    el.statSlope = document.getElementById('stat-slope');
    el.statCi = document.getElementById('stat-ci');
    el.statP = document.getElementById('stat-p');
    el.statN = document.getElementById('stat-n');
    el.verdictExplanation = document.getElementById('verdict-explanation');
    el.impactBox = document.getElementById('impact-box');
    el.windowLesson = document.getElementById('window-length-lesson');
    el.gapCaution = document.getElementById('gap-caution');
    el.scienceToggle = document.getElementById('science-toggle');
    el.scienceBody = document.getElementById('science-body');
    el.scienceGrid = document.getElementById('science-grid');
    el.caseGrid = document.getElementById('case-cards-container');
    el.activeCaseBanner = document.getElementById('active-case-banner');
    el.caseBannerTitle = document.getElementById('case-banner-title');
    el.caseBannerPrompt = document.getElementById('case-banner-prompt');
    el.caseBannerTakeaway = document.getElementById('case-banner-takeaway');
    el.closeCaseBtn = document.getElementById('close-case-btn');
    el.modalOverlay = document.getElementById('modal-overlay');
    el.modalTitle = document.getElementById('modal-title');
    el.modalMeta = document.getElementById('modal-meta');
    el.modalDef = document.getElementById('modal-def');
    el.modalCaveats = document.getElementById('modal-caveats');
    el.modalCloseBtn = document.getElementById('modal-close-btn');
  }

  // Helper: Find metadata by ID
  function getVarMeta(varId) {
    return window.ED.catalog.variables.find(v => v.id === varId);
  }

  function getRegionMeta(regId) {
    return window.ED.catalog.regions.find(r => r.id === regId);
  }

  function getDivisionMeta(divId) {
    return window.ED.catalog.divisions.find(d => d.id === divId);
  }

  // 1. Render Case Cards
  function renderCases() {
    el.caseGrid.innerHTML = '';
    window.ED.cases.forEach(c => {
      const card = document.createElement('div');
      card.className = `case-card ${state.activeCaseId === c.id ? 'active' : ''}`;
      card.innerHTML = `
        <div>
          <div class="case-card-header">
            <span class="case-badge">${c.badge}</span>
            <span class="case-domain">${c.domain}</span>
          </div>
          <div class="case-title">${c.title}</div>
          <div class="case-tagline">${c.tagline}</div>
          <div class="case-question">“${c.question}”</div>
        </div>
      `;
      card.addEventListener('click', () => activateCase(c.id));
      el.caseGrid.appendChild(card);
    });
  }

  function activateCase(caseId) {
    const c = window.ED.cases.find(x => x.id === caseId);
    if (!c) return;

    state.activeCaseId = caseId;
    state.variable = c.config.variable;
    state.overlayVariable = c.config.overlayVariable;
    state.entity = c.config.region;
    state.spatialType = 'region';
    state.startYear = c.config.startYear;
    state.endYear = c.config.endYear;
    state.season = c.config.season;
    state.showDeseasonalized = c.config.deseasonalize;

    el.activeCaseBanner.classList.add('visible');
    el.caseBannerTitle.textContent = `${c.badge}: ${c.title}`;
    el.caseBannerPrompt.innerHTML = `<strong>Detective Mission:</strong> ${c.prompt}`;
    el.caseBannerTakeaway.innerHTML = `<strong>Scientific Insight:</strong> ${c.takeaway} <a href="#dossier-${caseId}" class="case-banner-dossier-link">📖 Read In-Depth Case Dossier ↓</a>`;

    syncControls();
    runWorkflow();
    renderCases();
  }

  // Expose globally for interactive dossier buttons
  window.ED.activateCase = function(caseId) {
    activateCase(caseId);
    const wb = document.querySelector('.workbench-layout');
    if (wb) {
      wb.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  function closeCase() {
    state.activeCaseId = null;
    el.activeCaseBanner.classList.remove('visible');
    renderCases();
  }

  // 2. Render Variable Selection Cards
  function renderVariables() {
    el.varCards.innerHTML = '';
    const vars = window.ED.catalog.variables;

    // Group variables by domain
    const domains = [
      { name: 'Water & Gravity', ids: ['grace_tws'] },
      { name: 'Precipitation & Reanalysis', ids: ['imerg_precip', 'power_precip'] },
      { name: 'Soil & Subsurface', ids: ['noah_sms_anom', 'vic_sms_anom', 'subsurface_residual'] },
      { name: 'Climate Extremes', ids: ['extreme_rx1day', 'extreme_days_ge_50'] },
      { name: 'Atmospheric Aerosols', ids: ['aod_550'] }
    ];

    domains.forEach(d => {
      const grpLabel = document.createElement('div');
      grpLabel.className = 'variable-group-label';
      grpLabel.textContent = d.name;
      el.varCards.appendChild(grpLabel);

      const grid = document.createElement('div');
      grid.className = 'variable-cards';

      d.ids.forEach(id => {
        const v = getVarMeta(id);
        if (!v) return;

        const card = document.createElement('div');
        card.className = `var-card ${state.variable === v.id ? 'selected' : ''}`;
        card.innerHTML = `
          <div class="var-name">${v.name}</div>
          <div class="var-meta">${v.sensor.split(' ')[0]} • ${v.unit}</div>
          <button class="var-info-btn" title="View Definition & Caveats">ⓘ</button>
        `;

        card.addEventListener('click', (e) => {
          if (e.target.classList.contains('var-info-btn')) return;
          state.variable = v.id;
          // If selected variable doesn't support divisions, reset to region
          if (!v.supports_divisions && state.spatialType === 'division') {
            state.spatialType = 'region';
            state.entity = 'NW';
          }
          syncControls();
          runWorkflow();
        });

        card.querySelector('.var-info-btn').addEventListener('click', (e) => {
          e.stopPropagation();
          showVarModal(v);
        });

        grid.appendChild(card);
      });

      el.varCards.appendChild(grid);
    });

    // Populate Secondary Overlay Selector
    el.overlaySelect.innerHTML = '<option value="">None (Single Variable)</option>';
    vars.forEach(v => {
      if (v.id !== state.variable) {
        const opt = document.createElement('option');
        opt.value = v.id;
        opt.textContent = `${v.name} (${v.unit})`;
        if (state.overlayVariable === v.id) opt.selected = true;
        el.overlaySelect.appendChild(opt);
      }
    });
  }

  function showVarModal(v) {
    el.modalTitle.textContent = v.name;
    el.modalMeta.textContent = `${v.domain} • ${v.sensor} • Units: ${v.unit}`;
    el.modalDef.textContent = v.definition;
    el.modalCaveats.textContent = v.caveats;
    el.modalOverlay.classList.add('visible');
  }

  // 3. Render Spatial Selector & SVG Map
  function renderSpatialControls() {
    const isDivision = state.spatialType === 'division';
    const curVar = getVarMeta(state.variable);

    // Disable division toggle if variable doesn't support it
    const divBtn = el.spatialToggle.querySelector('[data-type="division"]');
    if (!curVar.supports_divisions) {
      divBtn.style.opacity = '0.4';
      divBtn.style.cursor = 'not-allowed';
      divBtn.title = 'Divisional breakdown is available for GRACE and precipitation only';
    } else {
      divBtn.style.opacity = '1.0';
      divBtn.style.cursor = 'pointer';
      divBtn.title = '';
    }

    // Caveat banner
    if (isDivision && curVar.id === 'grace_tws') {
      el.regionalCaveat.classList.add('visible');
      el.regionalCaveat.innerHTML = '⚠️ <strong>Coarse Footprint:</strong> GRACE spatial resolution is ~300 km. Divisional estimates share neighboring mascons and are descriptive only.';
    } else {
      el.regionalCaveat.classList.remove('visible');
    }

    // Render List
    el.regionsList.innerHTML = '';
    if (!isDivision) {
      window.ED.catalog.regions.forEach(r => {
        const btn = document.createElement('button');
        btn.className = `region-btn ${state.entity === r.id ? 'selected' : ''}`;
        btn.innerHTML = `
          <span>${r.name}</span>
          <span class="region-tag">${r.id}</span>
        `;
        btn.addEventListener('click', () => {
          state.entity = r.id;
          syncControls();
          runWorkflow();
        });
        el.regionsList.appendChild(btn);
      });
    } else {
      window.ED.catalog.divisions.forEach(d => {
        const btn = document.createElement('button');
        btn.className = `region-btn ${state.entity === d.id ? 'selected' : ''}`;
        btn.innerHTML = `
          <span>${d.name}</span>
          <span class="region-tag">${d.region}</span>
        `;
        btn.addEventListener('click', () => {
          state.entity = d.id;
          syncControls();
          runWorkflow();
        });
        el.regionsList.appendChild(btn);
      });
    }

    renderSvgMap();
  }

  function renderSvgMap() {
    const paths = window.ED.map.svgPaths;
    const isDivision = state.spatialType === 'division';
    const regDivs = window.ED.map.regionDivisions;

    let svgHtml = `<svg viewBox="0 0 600 750" class="svg-map">`;

    for (const [divName, dPath] of Object.entries(paths)) {
      let isSelected = false;
      if (isDivision) {
        isSelected = state.entity === divName;
      } else {
        if (state.entity === 'National') {
          isSelected = true;
        } else if (regDivs[state.entity] && regDivs[state.entity].includes(divName)) {
          isSelected = true;
        }
      }

      svgHtml += `<path d="${dPath}" class="map-path ${isSelected ? 'selected' : ''}" data-div="${divName}"><title>${divName}</title></path>`;
    }

    svgHtml += `</svg>`;
    el.svgMap.innerHTML = svgHtml;

    // Attach click listeners to paths
    el.svgMap.querySelectorAll('.map-path').forEach(p => {
      p.addEventListener('click', () => {
        const clickedDiv = p.getAttribute('data-div');
        if (state.spatialType === 'division') {
          state.entity = clickedDiv;
        } else {
          const clickedReg = window.ED.map.divisionToRegion[clickedDiv];
          if (clickedReg) state.entity = clickedReg;
        }
        syncControls();
        runWorkflow();
      });
    });
  }

  // 4. Render Time Controls
  function renderTimeControls() {
    // Populate start and end year selects
    el.startYear.innerHTML = '';
    el.endYear.innerHTML = '';
    for (let yr = 2002; yr <= 2026; yr++) {
      el.startYear.innerHTML += `<option value="${yr}" ${yr === state.startYear ? 'selected' : ''}>${yr}</option>`;
      el.endYear.innerHTML += `<option value="${yr}" ${yr === state.endYear ? 'selected' : ''}>${yr}</option>`;
    }

    // Populate Season selector
    el.seasonSelect.innerHTML = '';
    window.ED.catalog.seasons.forEach(s => {
      el.seasonSelect.innerHTML += `<option value="${s.id}" ${s.id === state.season ? 'selected' : ''}>${s.label}</option>`;
    });

    // Populate Presets buttons
    el.timePresets.innerHTML = '';
    window.ED.catalog.canonicalWindows.forEach(w => {
      const btn = document.createElement('button');
      const isPresetActive = (state.startYear === parseInt(w.start.slice(0, 4)) && state.endYear === parseInt(w.end.slice(0, 4)));
      btn.className = `preset-btn ${isPresetActive ? 'selected' : ''}`;
      btn.textContent = w.label;
      btn.addEventListener('click', () => {
        state.startYear = parseInt(w.start.slice(0, 4));
        state.endYear = parseInt(w.end.slice(0, 4));
        state.season = 'annual';
        syncControls();
        runWorkflow();
      });
      el.timePresets.appendChild(btn);
    });
  }

  function syncControls() {
    renderVariables();
    renderSpatialControls();
    renderTimeControls();

    // Deseason toggle state
    if (state.showDeseasonalized) {
      el.toggleDeseason.classList.add('active');
    } else {
      el.toggleDeseason.classList.remove('active');
    }

    if (state.showTrendLine) {
      el.toggleTrendLine.classList.add('active');
    } else {
      el.toggleTrendLine.classList.remove('active');
    }
  }

  // 5. Data Extraction Helper
  function extractSeries(varId, entity, isDivision) {
    const vMeta = getVarMeta(varId);
    if (!vMeta) return [];

    // Extremes
    if (varId.startsWith('extreme_')) {
      const extList = window.ED.seriesExtremes[entity] || [];
      const prop = varId === 'extreme_rx1day' ? 'rx1day_mm' : (varId === 'extreme_days_ge_50' ? 'days_ge_50mm' : 'annual_total_mm');
      return extList.map(item => ({
        ym: `${item.year}-07`,
        year: item.year,
        month: 7,
        decimal_year: item.decimal_year,
        value: item[prop]
      }));
    }

    // AOD
    if (varId === 'aod_550') {
      const aodList = window.ED.seriesAOD.dhaka_aeronet || [];
      return aodList.map(item => ({
        ym: item.ym,
        year: item.year,
        month: item.month,
        decimal_year: item.decimal_year,
        value: item.aod_550
      }));
    }

    // Monthly Regional or Divisional series
    const seriesObj = isDivision ? window.ED.seriesDivisions[entity] : window.ED.seriesRegions[entity];
    if (!seriesObj) return [];

    let valArray = [];
    if (varId === 'grace_tws') valArray = seriesObj.tws;
    else if (varId === 'imerg_precip') valArray = seriesObj.imerg;
    else if (varId === 'power_precip') valArray = seriesObj.power;
    else if (varId === 'noah_sms_anom') valArray = seriesObj.noah_sms;
    else if (varId === 'vic_sms_anom') valArray = seriesObj.vic_sms;
    else if (varId === 'subsurface_residual') valArray = seriesObj.residual_mid;

    if (!valArray) return [];

    const out = [];
    for (let i = 0; i < seriesObj.ym.length; i++) {
      const ym = seriesObj.ym[i];
      const yr = parseInt(ym.slice(0, 4));
      const mo = parseInt(ym.slice(5, 7));
      out.push({
        ym: ym,
        year: yr,
        month: mo,
        decimal_year: seriesObj.t[i],
        value: valArray[i]
      });
    }
    return out;
  }

  // 6. Main Workflow Execution (5 Steps)
  function runWorkflow() {
    const isDivision = state.spatialType === 'division';
    const curVar = getVarMeta(state.variable);
    const regMeta = isDivision ? getDivisionMeta(state.entity) : getRegionMeta(state.entity);

    // Filter time bounds
    const rawData = extractSeries(state.variable, state.entity, isDivision);
    const inWindow = rawData.filter(d => d.year >= state.startYear && d.year <= state.endYear);

    // Process season & deseasonalization
    let processedPoints = [];
    let isSeasonalMode = state.season !== 'annual';

    if (isSeasonalMode) {
      // Scientifically valid seasonal aggregation: 1 point per year
      processedPoints = window.Stats.seasonalAggregate(inWindow, state.season, curVar.kind);
    } else {
      if (curVar.can_deseasonalize && state.showDeseasonalized) {
        const months = inWindow.map(d => d.month);
        const vals = inWindow.map(d => d.value);
        const desVals = window.Stats.deseasonalize(months, vals);
        processedPoints = inWindow.map((d, idx) => ({
          ym: d.ym,
          year: d.year,
          month: d.month,
          decimal_year: d.decimal_year,
          value: desVals[idx]
        })).filter(d => !isNaN(d.value));
      } else {
        processedPoints = inWindow.filter(d => d.value !== null && !isNaN(d.value));
      }
    }

    const tYears = processedPoints.map(d => d.decimal_year);
    const yVals = processedPoints.map(d => d.value);

    // Run Calibrated ESS-MK Test
    const statResult = window.Stats.essMannKendall(tYears, yVals, 0.05);

    // Overlay variable data (if active)
    let overlayPoints = [];
    let overlayResult = null;
    if (state.overlayVariable) {
      const oVar = getVarMeta(state.overlayVariable);
      const oRaw = extractSeries(state.overlayVariable, state.entity, isDivision);
      const oInWin = oRaw.filter(d => d.year >= state.startYear && d.year <= state.endYear);
      if (isSeasonalMode) {
        overlayPoints = window.Stats.seasonalAggregate(oInWin, state.season, oVar.kind);
      } else {
        if (oVar.can_deseasonalize && state.showDeseasonalized) {
          const m = oInWin.map(d => d.month);
          const v = oInWin.map(d => d.value);
          const dv = window.Stats.deseasonalize(m, v);
          overlayPoints = oInWin.map((d, idx) => ({
            decimal_year: d.decimal_year,
            value: dv[idx]
          })).filter(d => !isNaN(d.value));
        } else {
          overlayPoints = oInWin.filter(d => d.value !== null && !isNaN(d.value));
        }
      }
      if (overlayPoints.length >= 10) {
        overlayResult = window.Stats.essMannKendall(
          overlayPoints.map(d => d.decimal_year),
          overlayPoints.map(d => d.value),
          0.05
        );
      }
    }

    // Step 4: Render Chart
    renderChart(processedPoints, statResult, overlayPoints);

    // Step 5: Render Verdict Card
    renderVerdict(statResult, processedPoints.length, curVar, regMeta);
  }

  // 7. Render Chart.js Visualization
  function renderChart(points, statResult, overlayPoints) {
    const curVar = getVarMeta(state.variable);
    const isDivision = state.spatialType === 'division';
    const locName = isDivision ? state.entity : (getRegionMeta(state.entity)?.name || state.entity);

    el.chartTitle.textContent = `${curVar.name} — ${locName}`;
    el.chartSubtitle.textContent = `${state.startYear} to ${state.endYear} • Season: ${state.season.toUpperCase()} • ${points.length} observations`;

    const labels = points.map(p => p.ym || p.year);
    const obsData = points.map(p => ({ x: p.decimal_year, y: p.value }));

    // Theil-Sen regression line points
    let trendLineData = [];
    let ciLowLine = [];
    let ciHighLine = [];

    if (state.showTrendLine && !isNaN(statResult.slope)) {
      trendLineData = window.Stats.calcTrendLine(
        points.map(p => p.decimal_year),
        points.map(p => p.value),
        statResult.slope
      ).map(pt => ({ x: pt.t, y: pt.y }));

      ciLowLine = window.Stats.calcTrendLine(
        points.map(p => p.decimal_year),
        points.map(p => p.value),
        statResult.ci_low
      ).map(pt => ({ x: pt.t, y: pt.y }));

      ciHighLine = window.Stats.calcTrendLine(
        points.map(p => p.decimal_year),
        points.map(p => p.value),
        statResult.ci_high
      ).map(pt => ({ x: pt.t, y: pt.y }));
    }

    const datasets = [
      {
        label: `${curVar.name} (${curVar.unit})`,
        data: obsData,
        borderColor: '#2563eb',
        backgroundColor: '#3b82f6',
        pointRadius: points.length > 80 ? 1.5 : 3.5,
        borderWidth: 1.5,
        tension: 0.1,
        yAxisID: 'y'
      }
    ];

    if (state.showTrendLine && trendLineData.length > 0) {
      datasets.push({
        label: `Theil-Sen Trend (${statResult.slope > 0 ? '+' : ''}${statResult.slope.toFixed(3)} ${curVar.unit}/yr)`,
        data: trendLineData,
        borderColor: '#dc2626',
        borderWidth: 2.2,
        pointRadius: 0,
        fill: false,
        yAxisID: 'y'
      });

      // Shaded 95% Confidence Interval Fan
      datasets.push({
        label: `95% CI Slope Upper Bound`,
        data: ciHighLine,
        borderColor: 'transparent',
        backgroundColor: 'rgba(220, 38, 38, 0.08)',
        pointRadius: 0,
        fill: '+1',
        yAxisID: 'y'
      });
      datasets.push({
        label: `95% CI Slope Lower Bound`,
        data: ciLowLine,
        borderColor: 'transparent',
        backgroundColor: 'rgba(220, 38, 38, 0.08)',
        pointRadius: 0,
        fill: false,
        yAxisID: 'y'
      });
    }

    // Overlay variable
    if (state.overlayVariable && overlayPoints.length > 0) {
      const oVar = getVarMeta(state.overlayVariable);
      datasets.push({
        label: `${oVar.name} (${oVar.unit}) [Overlay]`,
        data: overlayPoints.map(p => ({ x: p.decimal_year, y: p.value })),
        borderColor: '#ea580c',
        backgroundColor: '#f97316',
        borderDash: [4, 4],
        borderWidth: 1.8,
        pointRadius: overlayPoints.length > 80 ? 1.0 : 3.0,
        yAxisID: 'y2'
      });
    }

    if (chartInstance) {
      chartInstance.destroy();
    }

    chartInstance = new Chart(el.chartCanvas, {
      type: 'line',
      data: { datasets: datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: 'nearest', intersect: false },
        scales: {
          x: {
            type: 'linear',
            title: { display: true, text: 'Decimal Year' },
            ticks: {
              callback: val => Math.round(val)
            }
          },
          y: {
            type: 'linear',
            display: true,
            position: 'left',
            title: { display: true, text: `${curVar.name} (${curVar.unit})` }
          },
          y2: {
            type: 'linear',
            display: !!state.overlayVariable,
            position: 'right',
            grid: { drawOnChartArea: false },
            title: {
              display: !!state.overlayVariable,
              text: state.overlayVariable ? `${getVarMeta(state.overlayVariable).name} (${getVarMeta(state.overlayVariable).unit})` : ''
            }
          }
        },
        plugins: {
          legend: {
            display: true,
            position: 'top',
            labels: {
              filter: item => !item.text.includes('Bound')
            }
          },
          tooltip: {
            callbacks: {
              title: items => `Year: ${items[0].parsed.x.toFixed(2)}`
            }
          }
        }
      }
    });
  }

  // 8. Render Statistical Significance Verdict Card
  function renderVerdict(stat, nObs, curVar, regMeta) {
    if (stat.error || isNaN(stat.slope)) {
      el.verdictBadge.className = 'verdict-badge null-trend';
      el.verdictBadge.textContent = 'INSUFFICIENT DATA';
      el.statSlope.textContent = '—';
      el.statCi.textContent = '—';
      el.statP.textContent = '—';
      el.statN.textContent = `${nObs}`;
      el.verdictExplanation.textContent = stat.error || 'Minimum observations not met.';
      el.impactBox.style.display = 'none';
      el.windowLesson.style.display = 'none';
      el.gapCaution.style.display = 'none';
      el.scienceBody.classList.remove('visible');
      return;
    }

    const isSignificant = (stat.p_value < 0.05) && (stat.ci_low * stat.ci_high > 0);
    const pStr = stat.p_value < 0.0001 ? '< 0.0001' : stat.p_value.toFixed(4);

    if (isSignificant) {
      el.verdictBadge.className = 'verdict-badge significant';
      el.verdictBadge.innerHTML = `✓ SIGNIFICANT TREND (p = ${pStr} &lt; 0.05)`;
    } else {
      el.verdictBadge.className = 'verdict-badge null-trend';
      el.verdictBadge.innerHTML = `○ NO DETECTABLE TREND (p = ${pStr} ≥ 0.05)`;
    }

    el.statSlope.textContent = `${stat.slope > 0 ? '+' : ''}${stat.slope.toFixed(3)} ${curVar.unit}/yr`;
    el.statCi.textContent = `[${stat.ci_low.toFixed(3)}, ${stat.ci_high.toFixed(3)}]`;
    el.statP.textContent = pStr;
    el.statN.textContent = `${stat.n} (n* = ${stat.n_star})`;

    // Check for exact canonical preset row (for FDR badge)
    let fdrBadgeHtml = '';
    const presetKey = `${state.startYear === 2002 && state.endYear === 2026 ? 'full_record' : (state.startYear === 2002 && state.endYear === 2017 ? 'grace_era' : (state.startYear === 2018 ? 'grace_fo_era' : 'recent_2020'))}_${state.entity}_${curVar.id === 'grace_tws' ? 'tws' : 'precip'}`;
    const presetMatch = window.ED.presets[presetKey];

    if (presetMatch && state.season === 'annual') {
      const qVal = presetMatch.bh_fdr_q_value < 0.0001 ? '< 0.0001' : presetMatch.bh_fdr_q_value.toFixed(4);
      fdrBadgeHtml = `<span style="display:inline-block;margin-left:8px;background:#e0e7ff;color:#3730a3;font-size:0.75rem;padding:2px 8px;border-radius:10px;font-weight:700;">Within-Window FDR q = ${qVal}</span>`;
    }

    // Plain Language Explanation
    let expText = '';
    if (isSignificant) {
      expText = `This trend meets Dr. James Acker's scientific significance standard (p &lt; 0.05). If there were really no underlying trend, an empirical slope this steep would occur by chance less than <strong>${(stat.p_value * 100).toFixed(1)}% of the time</strong>. ${fdrBadgeHtml}`;
    } else {
      expText = `This time series does not meet the standard threshold for statistical significance (p &ge; 0.05). As Dr. Acker emphasizes: <em>this does not mean a trend does not exist</em>—natural climate noise can mask gradual changes in short windows.`;
    }
    el.verdictExplanation.innerHTML = expText;

    // Physical Impact Conversion (for TWS)
    if (curVar.id === 'grace_tws' && regMeta && regMeta.cropland_pct) {
      el.impactBox.style.display = 'block';
      const area = state.entity === 'NW' ? 30984.4 : (state.entity === 'National' ? 148048.2 : 30000);
      const km3Lost = Math.abs(stat.slope * area * 1e-5);
      const billionLiters = Math.round(km3Lost * 1000);
      const pools = Math.round(billionLiters / 2.5); // 2.5 million liters per Olympic pool
      el.impactBox.innerHTML = `💧 <strong>Physical Water Impact:</strong> A rate of <strong>${stat.slope.toFixed(2)} cm/yr</strong> across ${locName(regMeta)} equates to approximately <strong>${billionLiters.toLocaleString()} billion liters</strong> (~${pools.toLocaleString()} Olympic swimming pools) of total water volume change per year.`;
    } else {
      el.impactBox.style.display = 'none';
    }

    // Dr. Acker's Window Length Lesson
    const mds = window.Stats.approxMDS(
      extractSeries(state.variable, state.entity, state.spatialType === 'division').map(d => d.decimal_year),
      extractSeries(state.variable, state.entity, state.spatialType === 'division').map(d => d.value),
      stat.slope,
      stat.gamma
    );

    const yearSpan = state.endYear - state.startYear;
    if (!isSignificant && yearSpan <= 10) {
      el.windowLesson.style.display = 'block';
      el.windowLesson.innerHTML = `
        <h4>⏱️ Dr. Acker's Lesson: Why Window Length Matters</h4>
        <p>In this short <strong>${yearSpan}-year window</strong>, statistical noise demands an approximate Minimum Detectable Slope of <strong>${mds ? mds.toFixed(2) : '1.7'} ${curVar.unit}/yr</strong> to reach significance. Try expanding the start year to <strong>2002</strong> to see how 24 years of observation reveal statistically significant trends.</p>
      `;
    } else {
      el.windowLesson.style.display = 'none';
    }

    // Gap Caution (for TWS across 2017–2018)
    if (curVar.has_gap && state.startYear <= 2017 && state.endYear >= 2018) {
      el.gapCaution.style.display = 'block';
      el.gapCaution.innerHTML = `
        ⚠️ <strong>Inter-Satellite Gap Notice:</strong> This analysis spans the July 2017 – May 2018 observation gap between GRACE and GRACE-FO. Multi-satellite trends can be sensitive to step offsets across mission gaps. <a href="report.html#timeseries" target="_blank" style="color:#2563eb;font-weight:600;">View 3-way sensitivity models in Research Report ↗</a>
      `;
    } else {
      el.gapCaution.style.display = 'none';
    }

    // Science Diagnostics Panel
    el.scienceGrid.innerHTML = `
      <div><strong>Kendall S:</strong> ${stat.s}</div>
      <div><strong>Standardized Z:</strong> ${stat.z.toFixed(3)}</div>
      <div><strong>Autocorr r1*:</strong> ${stat.r1_detrended}</div>
      <div><strong>ESS Inflation γ:</strong> ${stat.gamma}</div>
      <div><strong>Effective n*:</strong> ${stat.n_star} (n=${stat.n})</div>
      <div><strong>Method:</strong> Calibrated ESS-MK</div>
      <div><strong>Sensor:</strong> ${curVar.sensor}</div>
      <div><strong>Deseasonalized:</strong> ${curVar.can_deseasonalize && state.showDeseasonalized ? 'Yes (Calendar-Month Climatology)' : 'No (Raw/Annual)'}</div>
    `;
  }

  function locName(regMeta) {
    return regMeta ? (regMeta.name || regMeta.id) : state.entity;
  }

  // 9. Event Listeners & Bootstrapping
  function bindEvents() {
    el.overlaySelect.addEventListener('change', (e) => {
      state.overlayVariable = e.target.value || null;
      runWorkflow();
    });

    el.spatialToggle.querySelectorAll('.spatial-toggle-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const type = btn.getAttribute('data-type');
        const curVar = getVarMeta(state.variable);
        if (type === 'division' && !curVar.supports_divisions) return;

        state.spatialType = type;
        state.entity = type === 'division' ? 'Rajshahi' : 'NW';

        el.spatialToggle.querySelectorAll('.spatial-toggle-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        renderSpatialControls();
        runWorkflow();
      });
    });

    el.startYear.addEventListener('change', (e) => {
      state.startYear = parseInt(e.target.value);
      if (state.startYear > state.endYear) {
        state.endYear = state.startYear;
        el.endYear.value = state.endYear;
      }
      runWorkflow();
    });

    el.endYear.addEventListener('change', (e) => {
      state.endYear = parseInt(e.target.value);
      if (state.endYear < state.startYear) {
        state.startYear = state.endYear;
        el.startYear.value = state.startYear;
      }
      runWorkflow();
    });

    el.seasonSelect.addEventListener('change', (e) => {
      state.season = e.target.value;
      runWorkflow();
    });

    el.toggleDeseason.addEventListener('click', () => {
      state.showDeseasonalized = !state.showDeseasonalized;
      syncControls();
      runWorkflow();
    });

    el.toggleTrendLine.addEventListener('click', () => {
      state.showTrendLine = !state.showTrendLine;
      syncControls();
      runWorkflow();
    });

    el.scienceToggle.addEventListener('click', () => {
      el.scienceBody.classList.toggle('visible');
    });

    el.closeCaseBtn.addEventListener('click', closeCase);

    el.modalCloseBtn.addEventListener('click', () => {
      el.modalOverlay.classList.remove('visible');
    });

    el.modalOverlay.addEventListener('click', (e) => {
      if (e.target === el.modalOverlay) {
        el.modalOverlay.classList.remove('visible');
      }
    });
  }

  // Bootstrapping
  window.addEventListener('DOMContentLoaded', () => {
    initElements();
    renderCases();
    syncControls();
    bindEvents();
    runWorkflow();
  });

})();
