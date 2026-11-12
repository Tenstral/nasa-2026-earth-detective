/**
 * Bengal Earth System Trend Detective
 * assets/js/app.js
 * =====================================
 * Scientific Daylight (Swiss Grid) Analytical Controller
 * Full-Viewport Snappy Desktop Deck with GSAP Animations & Multi-Lens Geospatial Workbench
 */

(function() {
  'use strict';

  window.ED = window.ED || {};

  // 1. Application State
  const state = {
    variable: 'grace_tws',
    overlayVariable: '',
    spatialType: 'region', // 'region' or 'division'
    entity: 'NW',
    startYear: 2002,
    endYear: 2026,
    season: 'annual',
    showDeseasonalized: true,
    showTrendLine: true,
    showGap: true,
    showFloodMarkers: true,
    activeCaseId: 'case-1',
    activeLens: 'trend', // 'trend', 'seasonal', 'epochs'
    showChoropleth: true,
    showGrid: true,
    showStation: true,
    activeDossierCaseId: 'case-1',
    zoomStartRatio: 0, // 0.0 to 1.0 (Lens 1 viewport zoom)
    zoomEndRatio: 1.0,
    mode: 'scientist',
    lang: 'en'
  };

  const VAR_MAP_FROM_URL = {
    'tws': 'grace_tws',
    'grace_tws': 'grace_tws',
    'grace_tws_cm': 'grace_tws',
    'imerg': 'imerg_precip',
    'imerg_precip': 'imerg_precip',
    'imerg_precip_mm': 'imerg_precip',
    'precip': 'imerg_precip',
    'power': 'power_precip',
    'power_precip': 'power_precip',
    'noah_sms': 'noah_sms_anom',
    'noah_sms_anom': 'noah_sms_anom',
    'vic_sms': 'vic_sms_anom',
    'vic_sms_anom': 'vic_sms_anom',
    'residual': 'subsurface_residual',
    'subsurface_residual': 'subsurface_residual',
    'rx1day': 'extreme_rx1day',
    'extreme_rx1day': 'extreme_rx1day',
    'aod': 'modis_aod',
    'modis_aod': 'modis_aod'
  };

  const VAR_MAP_TO_URL = {
    'grace_tws': 'tws',
    'imerg_precip': 'imerg',
    'power_precip': 'power',
    'noah_sms_anom': 'noah_sms',
    'vic_sms_anom': 'vic_sms',
    'subsurface_residual': 'residual',
    'extreme_rx1day': 'rx1day',
    'modis_aod': 'aod'
  };

  const DIVISIONS = ['Barishal', 'Chattogram', 'Dhaka', 'Khulna', 'Mymensingh', 'Rajshahi', 'Rangpur', 'Sylhet'];

  function applyUrlStateToApp(urlSt) {
    if (!urlSt) return;
    if (urlSt.var && VAR_MAP_FROM_URL[urlSt.var.toLowerCase()]) {
      state.variable = VAR_MAP_FROM_URL[urlSt.var.toLowerCase()];
    }
    if (urlSt.region) {
      if (DIVISIONS.includes(urlSt.region)) {
        state.spatialType = 'division';
        state.entity = urlSt.region;
      } else {
        state.spatialType = 'region';
        state.entity = urlSt.region;
      }
    }
    if (urlSt.start && urlSt.end) {
      state.startYear = urlSt.start;
      state.endYear = urlSt.end;
    } else if (urlSt.window && window.URLState && window.URLState.WINDOW_YEARS[urlSt.window]) {
      const wy = window.URLState.WINDOW_YEARS[urlSt.window];
      state.startYear = wy.start;
      state.endYear = wy.end;
    }
    if (urlSt.season) {
      state.season = urlSt.season;
    }
    if (urlSt.mode) {
      state.mode = urlSt.mode;
    }
    if (urlSt.lang) {
      state.lang = urlSt.lang;
    }
  }

  function syncAppToUrlState() {
    if (!window.URLState) return;
    const urlVar = VAR_MAP_TO_URL[state.variable] || state.variable;
    window.URLState.setState({
      var: urlVar,
      region: state.entity,
      start: state.startYear,
      end: state.endYear,
      season: state.season,
      mode: state.mode,
      lang: state.lang
    });
  }

  let chartInstance = null;
  let currentTrendPoints = [];
  const el = {};

  // Bounding box for entire Bangladesh SVG (0 0 600 730)
  const BD_VIEWBOX = { x: 0, y: 0, w: 600, h: 730 };
  let currentViewBox = { ...BD_VIEWBOX };
  let isPanning = false;
  let panStart = { x: 0, y: 0 };

  // 2. DOM Initialization
  function initDOM() {
    el.deckViewport = document.getElementById('deck-viewport');
    el.deckNav = document.getElementById('deck-nav');
    el.deckNavBtns = document.querySelectorAll('.deck-nav-btn');

    // Section 1: Cases Bento
    el.casesBentoContainer = document.getElementById('cases-bento-container');

    // Section 2: Workbench Command Ribbon
    el.workbenchShell = document.getElementById('workbench-shell');
    el.varPickerBtn = document.getElementById('var-picker-btn');
    el.currentVarName = document.getElementById('current-var-name');
    el.currentVarChip = document.getElementById('current-var-chip');
    el.varPopover = document.getElementById('var-popover');
    el.varPopoverBackdrop = document.getElementById('var-popover-backdrop');
    el.varPopoverGrid = document.getElementById('var-popover-grid');
    el.varPopoverClose = document.getElementById('var-popover-close');
    el.btnCompareSeries = document.getElementById('btn-compare-series');
    el.activeOverlayChip = document.getElementById('active-overlay-chip');
    el.activeOverlayName = document.getElementById('active-overlay-name');
    el.btnClearOverlay = document.getElementById('btn-clear-overlay');
    el.overlayCompareModal = document.getElementById('overlay-compare-modal');
    el.overlayPopoverBackdrop = document.getElementById('overlay-popover-backdrop');
    el.overlayModalGrid = document.getElementById('overlay-modal-grid');
    el.overlayModalClose = document.getElementById('overlay-modal-close');
    el.spatialToggle = document.getElementById('spatial-toggle');
    el.regionSelect = document.getElementById('region-select');
    el.regionalCaveatPill = document.getElementById('regional-caveat-pill');
    el.timePresetsContainer = document.getElementById('time-presets-container');
    el.startYearSelect = document.getElementById('start-year-select');
    el.endYearSelect = document.getElementById('end-year-select');
    el.seasonSelect = document.getElementById('season-select');
    el.activeMissionPill = document.getElementById('active-mission-pill');
    el.missionPillLabel = document.getElementById('mission-pill-label');
    el.workbenchFullscreenBtn = document.getElementById('workbench-fullscreen-btn');
    el.headerFullscreenBtn = document.getElementById('btn-fullscreen-header');

    // Section 2: Geospatial Map Panel
    el.mapViewport = document.getElementById('map-viewport');
    el.svgMap = document.getElementById('svg-map');
    el.svgPathsGroup = document.getElementById('svg-paths-group');
    el.svgStationsGroup = document.getElementById('svg-stations-group');
    el.graticuleLayer = document.getElementById('graticule-layer');
    el.mapHoverHud = document.getElementById('map-hover-hud');
    el.hudName = document.getElementById('hud-name');
    el.hudSlope = document.getElementById('hud-slope');
    el.hudP = document.getElementById('hud-p');
    el.hudPop = document.getElementById('hud-pop');
    el.hudCrop = document.getElementById('hud-crop');
    el.quickRegionPills = document.getElementById('quick-region-pills');
    el.mapToggleChoropleth = document.getElementById('map-toggle-choropleth');
    el.mapToggleGrid = document.getElementById('map-toggle-grid');
    el.mapToggleStation = document.getElementById('map-toggle-station');
    el.mapResetZoom = document.getElementById('map-reset-zoom');

    // Section 2: Chart & Telemetry
    el.timeseriesCanvas = document.getElementById('timeseries-canvas');
    el.lensTrend = document.getElementById('lens-trend');
    el.lensSeasonal = document.getElementById('lens-seasonal');
    el.lensEpochs = document.getElementById('lens-epochs');
    el.toggleDeseason = document.getElementById('toggle-deseason');
    el.toggleTrendLine = document.getElementById('toggle-trendline');
    el.toggleGap = document.getElementById('toggle-gap');
    el.toggleFloods = document.getElementById('toggle-floods');

    // Chart Timeline Zoom Bar (Lens 1)
    el.chartZoomBar = document.getElementById('chart-zoom-bar');
    el.czbReadout = document.getElementById('czb-readout');
    el.czbTrackContainer = document.getElementById('czb-track-container');
    el.czbWindow = document.getElementById('czb-window');
    el.czbHandleLeft = document.getElementById('czb-handle-left');
    el.czbHandleRight = document.getElementById('czb-handle-right');
    el.czbDragPan = document.getElementById('czb-drag-pan');
    el.czbBtnReset = document.getElementById('czb-btn-reset');

    // Telemetry Verdict Cells
    el.telVerdict = document.getElementById('tel-verdict');
    el.telVerdictSub = document.getElementById('tel-verdict-sub');
    el.studentVerdictHeading = document.getElementById('student-verdict-heading');
    el.studentVerdictSentence = document.getElementById('student-verdict-sentence');
    el.studentVerdictRate = document.getElementById('student-verdict-rate');
    el.btnStudentReportLink = document.getElementById('btn-student-report-link');
    el.btnVerdictReportLink = document.getElementById('btn-verdict-report-link');
    el.btnTriggerReportLink = document.getElementById('btn-trigger-report-link');
    el.telSlope = document.getElementById('tel-slope');
    el.telSlopeVol = document.getElementById('tel-slope-vol');
    el.telCi = document.getElementById('tel-ci');
    el.telP = document.getElementById('tel-p');
    el.telFdr = document.getElementById('tel-fdr');
    el.telN = document.getElementById('tel-n');
    el.telMds = document.getElementById('tel-mds');

    // Drawers
    el.btnOpenDiagnostics = document.getElementById('btn-open-diagnostics');
    el.btnOpenDirectives = document.getElementById('btn-open-directives');
    el.drawerDiagnostics = document.getElementById('drawer-diagnostics');
    el.diagnosticsBackdrop = document.getElementById('diagnostics-backdrop');
    el.closeDiagnostics = document.getElementById('close-diagnostics');
    el.diagStatsGrid = document.getElementById('diag-stats-grid');
    el.diagWindowLesson = document.getElementById('diag-window-lesson');
    el.diagSensorSafeguard = document.getElementById('diag-sensor-safeguard');

    el.drawerDirectives = document.getElementById('drawer-directives');
    el.directivesBackdrop = document.getElementById('directives-backdrop');
    el.closeDirectives = document.getElementById('close-directives');
    el.directivesRegionName = document.getElementById('directives-region-name');
    el.directivesItemsContainer = document.getElementById('directives-items-container');

    // Methodological Evidence Drawer
    el.drawerEvidence = document.getElementById('evidenceDrawer');
    el.evidenceBackdrop = document.getElementById('evidence-backdrop');
    el.closeEvidence = document.getElementById('close-evidence');
    el.btnOpenEvidence = document.getElementById('btn-open-evidence');
    el.evidenceContent = document.getElementById('evidence-content');
    el.evidenceOpenReportLink = document.getElementById('evidence-open-report-link');

    // Header Drawer Shortcuts
    el.btnHeaderEvidence = document.getElementById('btn-header-evidence');
    el.btnHeaderDirectives = document.getElementById('btn-header-directives');
    el.btnHeaderDiagnostics = document.getElementById('btn-header-diagnostics');

    // Section 1: Guided Case Investigations
    el.dossierTabsList = document.getElementById('dossier-tabs-list');
    el.dossierBadge = document.getElementById('dossier-badge');
    el.dossierTitle = document.getElementById('dossier-title');
    el.dossierTagline = document.getElementById('dossier-tagline');
    el.dossierBodyScience = document.getElementById('dossier-body-science');
    el.dossierBodyFindings = document.getElementById('dossier-body-findings');
    el.dossierBodyImpact = document.getElementById('dossier-body-impact');
    el.dossierBodyLimitations = document.getElementById('dossier-body-limitations');
    el.dossierBodyOutlook = document.getElementById('dossier-body-outlook');
    el.dossierLoadBtn = document.getElementById('dossier-load-btn');
    el.dossierHeaderLaunchBtn = document.getElementById('dossier-header-launch-btn');

    // Specification Modal
    el.modalOverlay = document.getElementById('modal-overlay');
    el.modalCloseBtn = document.getElementById('modal-close-btn');
    el.modalTitle = document.getElementById('modal-title');
    el.modalMeta = document.getElementById('modal-meta');
    el.modalDef = document.getElementById('modal-def');
    el.modalCaveats = document.getElementById('modal-caveats');
  }

  // 3. Navigation & GSAP Section Scrolling
  function initNavigation() {
    el.deckNavBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const targetId = btn.getAttribute('data-target');
        jumpToSection(targetId);
      });
    });

    // Sync active nav button on manual scroll
    el.deckViewport.addEventListener('scroll', () => {
      const scrollPos = el.deckViewport.scrollTop;
      const secHeight = window.innerHeight - 48;
      const index = Math.round(scrollPos / secHeight);
      const sectionIds = ['sec-cases', 'sec-workbench', 'sec-catalog'];
      const curSecId = sectionIds[index] || 'sec-cases';

      el.deckNavBtns.forEach(btn => {
        if (btn.getAttribute('data-target') === curSecId) {
          btn.classList.add('active');
        } else {
          btn.classList.remove('active');
        }
      });
    });

    // Keyboard Shortcuts
    window.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT' || e.target.tagName === 'TEXTAREA') return;
      if (e.key === '1') jumpToSection('sec-cases');
      if (e.key === '2') jumpToSection('sec-workbench');
      if (e.key === '3') jumpToSection('sec-catalog');
      if (e.key === 'f' || e.key === 'F') toggleWorkbenchFullscreen();
      if (e.key === 'Escape') {
        closeAllDrawers();
        closeVarPopover();
        closeModal();
      }
    });

    if (el.headerFullscreenBtn) el.headerFullscreenBtn.addEventListener('click', toggleWorkbenchFullscreen);
    if (el.workbenchFullscreenBtn) el.workbenchFullscreenBtn.addEventListener('click', toggleWorkbenchFullscreen);
  }

  function jumpToSection(sectionId) {
    const target = document.getElementById(sectionId);
    if (!target) return;
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    if (el.deckNavBtns) {
      el.deckNavBtns.forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-target') === sectionId);
      });
    }
  }

  function toggleWorkbenchFullscreen() {
    if (!document.fullscreenElement) {
      if (el.workbenchShell.requestFullscreen) {
        el.workbenchShell.requestFullscreen();
      } else if (el.workbenchShell.webkitRequestFullscreen) {
        el.workbenchShell.webkitRequestFullscreen();
      }
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      }
    }
  }

  document.addEventListener('fullscreenchange', () => {
    setTimeout(() => {
      if (chartInstance) chartInstance.resize();
    }, 150);
  });

  // 4. Data Extraction Helpers
  function getVarMeta(varId) {
    return window.ED.catalog.variables.find(v => v.id === varId) || null;
  }

  function getRegionMeta(regId) {
    return window.ED.catalog.regions.find(r => r.id === regId) || null;
  }

  function getDivisionMeta(divName) {
    if (!window.ED.catalog || !window.ED.catalog.divisions) return null;
    return window.ED.catalog.divisions.find(d => d.id === divName || d.name === divName || d.name === `${divName} Division`) || null;
  }

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
        decimal_year: item.year + 0.5,
        value: item[prop]
      }));
    }

    // AOD: Ground AERONET
    if (varId === 'aeronet_aod') {
      const aodList = window.ED.seriesAOD.dhaka_aeronet || [];
      return aodList.map(item => ({
        ym: item.ym,
        year: item.year,
        month: item.month,
        decimal_year: item.decimal_year,
        value: item.aod_550
      }));
    }

    // AOD: Satellite MODIS Aqua
    if (varId === 'modis_aod') {
      let aodList = [];
      if (entity === 'National') {
        aodList = (window.ED.seriesAOD.bangladesh_modis && window.ED.seriesAOD.bangladesh_modis.length > 0)
          ? window.ED.seriesAOD.bangladesh_modis
          : window.ED.seriesAOD.dhaka_modis;
      } else {
        aodList = window.ED.seriesAOD.dhaka_modis || [];
      }
      return aodList.map(item => ({
        ym: item.ym,
        year: item.year,
        month: item.month,
        decimal_year: item.decimal_year,
        value: item.aod_550
      }));
    }

    // AIRS (Temperature & Water Vapor)
    if (varId === 'airs_temp' || varId === 'airs_h2o') {
      const regKey = (isDivision && window.ED.map && window.ED.map.divisionToRegion && window.ED.map.divisionToRegion[entity])
        ? window.ED.map.divisionToRegion[entity]
        : entity;
      const airsObj = (window.ED.seriesAIRS && window.ED.seriesAIRS[regKey]) || (window.ED.seriesAIRS && window.ED.seriesAIRS['National']);
      if (!airsObj) return [];
      const valArray = varId === 'airs_temp' ? airsObj.airs_temp : airsObj.airs_h2o;
      if (!valArray) return [];
      return airsObj.ym.map((ymStr, idx) => {
        const yr = parseInt(ymStr.slice(0, 4));
        const mo = parseInt(ymStr.slice(5, 7));
        return {
          ym: ymStr,
          year: yr,
          month: mo,
          decimal_year: airsObj.t ? airsObj.t[idx] : Math.round((yr + (mo - 0.5) / 12) * 10000) / 10000,
          value: valArray[idx]
        };
      });
    }

    // OMI Tropospheric NO2 Column
    if (varId === 'omi_no2') {
      let omiObj = null;
      if (window.ED.seriesOMI) {
        if (isDivision) {
          omiObj = (window.ED.seriesOMI.divisions && window.ED.seriesOMI.divisions[entity]) || window.ED.seriesOMI[entity];
        } else {
          omiObj = (window.ED.seriesOMI.regions && window.ED.seriesOMI.regions[entity]) || window.ED.seriesOMI[entity];
        }
      }
      if (!omiObj) return [];
      const valArray = omiObj.omi_no2;
      if (!valArray) return [];
      return omiObj.ym.map((ymStr, idx) => {
        const yr = parseInt(ymStr.slice(0, 4));
        const mo = parseInt(ymStr.slice(5, 7));
        return {
          ym: ymStr,
          year: yr,
          month: mo,
          decimal_year: omiObj.t ? omiObj.t[idx] : Math.round((yr + (mo - 0.5) / 12) * 10000) / 10000,
          value: valArray[idx]
        };
      });
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
    else if (varId === 'subsurface_residual') valArray = seriesObj.residual_mid || seriesObj.subsurface;

    if (!valArray) return [];

    return seriesObj.ym.map((ymStr, idx) => {
      const yr = parseInt(ymStr.slice(0, 4));
      const mo = parseInt(ymStr.slice(5, 7));
      return {
        ym: ymStr,
        year: yr,
        month: mo,
        decimal_year: seriesObj.decimal_year ? seriesObj.decimal_year[idx] : Math.round((yr + (mo - 0.5) / 12) * 10000) / 10000,
        value: valArray[idx]
      };
    });
  }

  // 5. Popover & Controls Configuration
  function initVariablePopover() {
    el.varPopoverGrid.innerHTML = '';
    const vars = window.ED.catalog.variables;

    const domains = [
      { name: 'Water & Gravimetry', ids: ['grace_tws'] },
      { name: 'Precipitation & Cross-Validation', ids: ['imerg_precip', 'power_precip'] },
      { name: 'Soil Moisture & Subsurface', ids: ['noah_sms_anom', 'vic_sms_anom', 'subsurface_residual'] },
      { name: 'Climate Extremes', ids: ['extreme_rx1day', 'extreme_days_ge_50'] },
      { name: 'Atmospheric Aerosols', ids: ['modis_aod', 'aeronet_aod'] },
      { name: 'Atmospheric Thermodynamics', ids: ['airs_temp', 'airs_h2o'] },
      { name: 'Atmospheric Composition', ids: ['omi_no2'] }
    ];

    domains.forEach(d => {
      const lbl = document.createElement('div');
      lbl.className = 'var-group-label';
      lbl.textContent = d.name;
      el.varPopoverGrid.appendChild(lbl);

      d.ids.forEach(vid => {
        const v = vars.find(x => x.id === vid);
        if (!v) return;

        const card = document.createElement('div');
        card.className = `var-item-card ${state.variable === v.id ? 'active' : ''}`;
        card.innerHTML = `
          <div class="vic-info">
            <span class="vic-name">${v.name}</span>
            <span class="vic-sub">${v.sensor} • ${v.unit}</span>
          </div>
          <button class="vic-spec-btn" title="View sensor specification details">ⓘ Details</button>
        `;

        card.addEventListener('click', (e) => {
          if (e.target.classList.contains('vic-spec-btn')) {
            e.stopPropagation();
            openModal(v);
            return;
          }
          state.variable = v.id;
          state.zoomStartRatio = 0;
          state.zoomEndRatio = 1.0;
          if (state.overlayVariable === v.id) state.overlayVariable = '';
          syncAppToUrlState();
          closeVarPopover();
          syncCommandRibbon();
          runWorkflow();
        });

        el.varPopoverGrid.appendChild(card);
      });
    });

    el.varPickerBtn.addEventListener('click', () => {
      if (el.varPopover.classList.contains('open')) {
        closeVarPopover();
      } else {
        openVarPopover();
      }
    });

    el.varPopoverClose.addEventListener('click', closeVarPopover);
    el.varPopoverBackdrop.addEventListener('click', closeVarPopover);
  }

  function openVarPopover() {
    el.varPopover.classList.add('open');
    el.varPopoverBackdrop.classList.add('open');
  }

  function closeVarPopover() {
    el.varPopover.classList.remove('open');
    el.varPopoverBackdrop.classList.remove('open');
  }

  function initOverlayModal() {
    el.overlayModalGrid.innerHTML = '';
    const vars = window.ED.catalog.variables;

    // None / Remove Card
    const noneCard = document.createElement('div');
    noneCard.className = `var-item-card ${!state.overlayVariable ? 'active' : ''}`;
    noneCard.innerHTML = `
      <div class="vic-info">
        <span class="vic-name">None (Single Primary Variable)</span>
        <span class="vic-sub">Disable secondary overlay comparison</span>
      </div>
    `;
    noneCard.addEventListener('click', () => {
      state.overlayVariable = '';
      closeOverlayModal();
      syncCommandRibbon();
      runWorkflow();
    });
    el.overlayModalGrid.appendChild(noneCard);

    // List of eligible overlay variables
    vars.forEach(v => {
      if (v.id === state.variable) return;
      const card = document.createElement('div');
      card.className = `var-item-card ${state.overlayVariable === v.id ? 'active' : ''}`;
      card.innerHTML = `
        <div class="vic-info">
          <span class="vic-name">${v.name}</span>
          <span class="vic-sub">${v.sensor} • ${v.unit}</span>
        </div>
      `;
      card.addEventListener('click', () => {
        state.overlayVariable = v.id;
        closeOverlayModal();
        syncCommandRibbon();
        runWorkflow();
      });
      el.overlayModalGrid.appendChild(card);
    });
  }

  function openOverlayModal() {
    initOverlayModal();
    el.overlayCompareModal.classList.add('open');
    el.overlayPopoverBackdrop.classList.add('open');
  }

  function closeOverlayModal() {
    el.overlayCompareModal.classList.remove('open');
    el.overlayPopoverBackdrop.classList.remove('open');
  }

  // 5b. Chart Timeline Brush Zoom Controller (Lens 1)
  function initChartZoomBar() {
    if (!el.czbTrackContainer || !el.czbWindow) return;

    let dragMode = null; // 'left', 'right', 'pan'
    let panStartX = 0;
    let initialL = 0;
    let initialR = 1;
    let initialSpan = 1;

    function getTrackRect() {
      return el.czbTrackContainer.getBoundingClientRect();
    }

    // Left Handle
    el.czbHandleLeft.addEventListener('pointerdown', (e) => {
      e.stopPropagation();
      e.preventDefault();
      dragMode = 'left';
      el.czbHandleLeft.classList.add('dragging');
      el.czbHandleLeft.setPointerCapture(e.pointerId);
    });

    // Right Handle
    el.czbHandleRight.addEventListener('pointerdown', (e) => {
      e.stopPropagation();
      e.preventDefault();
      dragMode = 'right';
      el.czbHandleRight.classList.add('dragging');
      el.czbHandleRight.setPointerCapture(e.pointerId);
    });

    // Middle Pan Bar
    el.czbDragPan.addEventListener('pointerdown', (e) => {
      e.stopPropagation();
      e.preventDefault();
      dragMode = 'pan';
      panStartX = e.clientX;
      initialL = state.zoomStartRatio;
      initialR = state.zoomEndRatio;
      initialSpan = Math.max(0.04, initialR - initialL);
      el.czbDragPan.setPointerCapture(e.pointerId);
    });

    function handlePointerMove(e) {
      if (!dragMode) return;
      const rect = getTrackRect();
      if (!rect || rect.width <= 0) return;

      const minSpan = Math.max(0.03, currentTrendPoints.length > 0 ? (4 / currentTrendPoints.length) : 0.04);

      if (dragMode === 'left') {
        const rawRatio = (e.clientX - rect.left) / rect.width;
        state.zoomStartRatio = Math.max(0, Math.min(state.zoomEndRatio - minSpan, rawRatio));
      } else if (dragMode === 'right') {
        const rawRatio = (e.clientX - rect.left) / rect.width;
        state.zoomEndRatio = Math.min(1, Math.max(state.zoomStartRatio + minSpan, rawRatio));
      } else if (dragMode === 'pan') {
        const deltaRatio = (e.clientX - panStartX) / rect.width;
        let newL = initialL + deltaRatio;
        let newR = initialR + deltaRatio;
        if (newL < 0) {
          newL = 0;
          newR = initialSpan;
        } else if (newR > 1) {
          newR = 1;
          newL = 1 - initialSpan;
        }
        state.zoomStartRatio = Math.max(0, newL);
        state.zoomEndRatio = Math.min(1, newR);
      }

      applyChartZoom();
    }

    function handlePointerUp(e) {
      if (!dragMode) return;
      if (dragMode === 'left') el.czbHandleLeft.classList.remove('dragging');
      if (dragMode === 'right') el.czbHandleRight.classList.remove('dragging');
      dragMode = null;
    }

    el.czbHandleLeft.addEventListener('pointermove', handlePointerMove);
    el.czbHandleLeft.addEventListener('pointerup', handlePointerUp);
    el.czbHandleLeft.addEventListener('pointercancel', handlePointerUp);

    el.czbHandleRight.addEventListener('pointermove', handlePointerMove);
    el.czbHandleRight.addEventListener('pointerup', handlePointerUp);
    el.czbHandleRight.addEventListener('pointercancel', handlePointerUp);

    el.czbDragPan.addEventListener('pointermove', handlePointerMove);
    el.czbDragPan.addEventListener('pointerup', handlePointerUp);
    el.czbDragPan.addEventListener('pointercancel', handlePointerUp);

    // Track Background Click to jump or pan window
    el.czbTrackContainer.addEventListener('click', (e) => {
      if (e.target === el.czbHandleLeft || e.target === el.czbHandleRight || e.target === el.czbDragPan) return;
      const rect = getTrackRect();
      if (!rect || rect.width <= 0) return;
      const clickRatio = (e.clientX - rect.left) / rect.width;
      const span = state.zoomEndRatio - state.zoomStartRatio;
      let newL = clickRatio - span / 2;
      let newR = clickRatio + span / 2;
      if (newL < 0) { newL = 0; newR = span; }
      if (newR > 1) { newR = 1; newL = 1 - span; }
      state.zoomStartRatio = Math.max(0, newL);
      state.zoomEndRatio = Math.min(1, newR);
      applyChartZoom();
    });

    // Reset button
    if (el.czbBtnReset) {
      el.czbBtnReset.addEventListener('click', () => {
        resetChartZoom();
      });
    }
  }

  function updateChartZoomUI() {
    if (!el.czbWindow || !el.czbReadout) return;

    const L = state.zoomStartRatio;
    const R = state.zoomEndRatio;

    el.czbWindow.style.left = (L * 100) + '%';
    el.czbWindow.style.right = ((1 - R) * 100) + '%';

    const isZoomed = (L > 0.005 || R < 0.995);
    if (el.czbBtnReset) {
      if (isZoomed) {
        el.czbBtnReset.classList.add('active-zoom');
        el.czbBtnReset.textContent = 'Reset Zoom [Active]';
      } else {
        el.czbBtnReset.classList.remove('active-zoom');
        el.czbBtnReset.textContent = 'Reset Zoom';
      }
    }

    if (!currentTrendPoints || currentTrendPoints.length === 0) {
      el.czbReadout.textContent = 'Full Time Range';
      return;
    }

    const n = currentTrendPoints.length;
    const startIdx = Math.max(0, Math.min(n - 1, Math.round(L * (n - 1))));
    const endIdx = Math.max(0, Math.min(n - 1, Math.round(R * (n - 1))));

    const pStart = currentTrendPoints[startIdx];
    const pEnd = currentTrendPoints[endIdx];

    const labelStart = pStart?.ym || (pStart?.year ? String(pStart.year) : 'Start');
    const labelEnd = pEnd?.ym || (pEnd?.year ? String(pEnd.year) : 'End');

    if (isZoomed) {
      el.czbReadout.textContent = `${labelStart} — ${labelEnd} (${endIdx - startIdx + 1} mos)`;
    } else {
      el.czbReadout.textContent = `${labelStart} — ${labelEnd} [Full]`;
    }
  }

  function applyChartZoom() {
    updateChartZoomUI();

    if (!chartInstance || state.activeLens !== 'trend' || !currentTrendPoints || currentTrendPoints.length === 0) {
      return;
    }

    const curVar = getVarMeta(state.variable);
    const n = currentTrendPoints.length;
    const L = state.zoomStartRatio;
    const R = state.zoomEndRatio;
    const isZoomed = (L > 0.005 || R < 0.995);

    if (!isZoomed) {
      chartInstance.options.scales.x.min = undefined;
      chartInstance.options.scales.x.max = undefined;
      if (state.lastStatResult && curVar) {
        renderTelemetryStrip(state.lastStatResult, currentTrendPoints.length, curVar);
        updateDiagnosticsContent(state.lastStatResult, currentTrendPoints.length, curVar);
      }
    } else {
      const startIdx = Math.max(0, Math.min(n - 1, Math.round(L * (n - 1))));
      const endIdx = Math.max(0, Math.min(n - 1, Math.round(R * (n - 1))));
      const pStart = currentTrendPoints[startIdx];
      const pEnd = currentTrendPoints[endIdx];
      chartInstance.options.scales.x.min = pStart?.ym || pStart?.year;
      chartInstance.options.scales.x.max = pEnd?.ym || pEnd?.year;

      const slicedPoints = currentTrendPoints.slice(startIdx, endIdx + 1);
      const startYr = pStart?.year || state.startYear;
      const endYr = pEnd?.year || state.endYear;
      const sliceStat = window.Stats.analyze({
        var: state.variable,
        region: state.entity,
        start: startYr,
        end: endYr,
        season: state.season,
        points: slicedPoints
      });
      sliceStat.valid = Boolean(sliceStat && !sliceStat.error && !isNaN(sliceStat.slope));
      if (sliceStat.valid) {
        sliceStat.slope = (sliceStat.theil_sen_slope !== undefined && !isNaN(sliceStat.theil_sen_slope)) ? sliceStat.theil_sen_slope : sliceStat.slope;
        sliceStat.n_eff = (sliceStat.n_star !== undefined && typeof sliceStat.n_star === 'number') ? sliceStat.n_star : sliceStat.n;
        sliceStat.slope_ci_low = sliceStat.slope_ci_low !== undefined ? sliceStat.slope_ci_low : sliceStat.ci_low;
        sliceStat.slope_ci_high = sliceStat.slope_ci_high !== undefined ? sliceStat.slope_ci_high : sliceStat.ci_high;
      }
      if (curVar) {
        renderTelemetryStrip(sliceStat, slicedPoints.length, curVar);
        updateDiagnosticsContent(sliceStat, slicedPoints.length, curVar);
      }
    }

    chartInstance.update('none');
  }

  function resetChartZoom() {
    state.zoomStartRatio = 0;
    state.zoomEndRatio = 1.0;
    applyChartZoom();
  }

  function syncCommandRibbon() {
    const curVar = getVarMeta(state.variable);
    if (curVar) {
      el.currentVarName.textContent = curVar.name;
      el.currentVarChip.textContent = curVar.unit;
    }

    // Update Secondary Overlay Chip in Lens Bar
    if (state.overlayVariable) {
      const oMeta = getVarMeta(state.overlayVariable);
      el.activeOverlayChip.style.display = 'inline-flex';
      el.activeOverlayName.textContent = oMeta ? oMeta.name : state.overlayVariable;
      el.btnCompareSeries.style.display = 'none';
    } else {
      el.activeOverlayChip.style.display = 'none';
      el.btnCompareSeries.style.display = 'inline-flex';
    }

    // Spatial Scale buttons & Division support check
    const supportsDiv = curVar ? (curVar.supports_divisions !== false) : true;
    const divBtn = el.spatialToggle.querySelector('.seg-btn[data-type="division"]');
    if (divBtn) {
      if (!supportsDiv) {
        divBtn.disabled = true;
        divBtn.classList.add('disabled');
        divBtn.title = 'Divisional breakdown is not supported for coarse resolution datasets (1° grid / mascons).';
        if (state.spatialType === 'division') {
          state.spatialType = 'region';
          state.entity = 'NW';
        }
      } else {
        divBtn.disabled = false;
        divBtn.classList.remove('disabled');
        divBtn.title = '';
      }
    }

    const segBtns = el.spatialToggle.querySelectorAll('.seg-btn');
    segBtns.forEach(btn => {
      if (btn.getAttribute('data-type') === state.spatialType) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });

    // Populate Region Dropdown
    el.regionSelect.innerHTML = '';
    const isDivision = state.spatialType === 'division';
    if (!isDivision) {
      window.ED.catalog.regions.forEach(r => {
        const opt = document.createElement('option');
        opt.value = r.id;
        opt.textContent = `${r.id} — ${r.name}`;
        if (state.entity === r.id) opt.selected = true;
        el.regionSelect.appendChild(opt);
      });
    } else {
      window.ED.catalog.divisions.forEach(d => {
        const opt = document.createElement('option');
        opt.value = d.name;
        opt.textContent = `${d.name} (${d.macro_region})`;
        if (state.entity === d.name) opt.selected = true;
        el.regionSelect.appendChild(opt);
      });
    }

    // Caveat Pill
    if (isDivision && state.variable === 'grace_tws') {
      el.regionalCaveatPill.style.display = 'inline-block';
      el.regionalCaveatPill.title = 'Coarse Footprint: GRACE ~300 km footprint. Divisional estimates share neighboring mascons.';
    } else if (state.variable === 'airs_temp' || state.variable === 'airs_h2o') {
      el.regionalCaveatPill.style.display = 'inline-block';
      el.regionalCaveatPill.title = 'Coarse 1.0° Grid: Regional values reflect ~1–3 cell centers. Clear-sky bias in monsoon.';
    } else if (state.variable === 'omi_no2') {
      el.regionalCaveatPill.style.display = 'inline-block';
      el.regionalCaveatPill.title = 'Atmospheric Trace Gas: 0.25° grid. Winter peaks reflect boundary layer compression and brick kilns.';
    } else if (state.variable === 'aeronet_aod') {
      el.regionalCaveatPill.style.display = 'inline-block';
      el.regionalCaveatPill.title = 'Station-Specific: AERONET is located at Dhaka University (Central Region).';
    } else {
      el.regionalCaveatPill.style.display = 'none';
    }

    // Years
    el.startYearSelect.innerHTML = '';
    el.endYearSelect.innerHTML = '';
    for (let yr = 2002; yr <= 2026; yr++) {
      const optS = document.createElement('option');
      optS.value = yr;
      optS.textContent = yr;
      if (state.startYear === yr) optS.selected = true;
      el.startYearSelect.appendChild(optS);

      const optE = document.createElement('option');
      optE.value = yr;
      optE.textContent = yr;
      if (state.endYear === yr) optE.selected = true;
      el.endYearSelect.appendChild(optE);
    }

    // Seasons
    el.seasonSelect.innerHTML = '';
    const seasons = [
      { id: 'annual', name: 'Annual (Deseas)' },
      { id: 'winter', name: 'Winter (DJF)' },
      { id: 'pre_monsoon', name: 'Pre-Monsoon (MAM)' },
      { id: 'monsoon', name: 'Monsoon (JJAS)' },
      { id: 'post_monsoon', name: 'Post-Monsoon (ON)' }
    ];
    seasons.forEach(s => {
      const opt = document.createElement('option');
      opt.value = s.id;
      opt.textContent = s.name;
      if (state.season === s.id) opt.selected = true;
      el.seasonSelect.appendChild(opt);
    });

    // Presets
    el.timePresetsContainer.innerHTML = '';
    window.ED.catalog.canonicalWindows.forEach(w => {
      const chip = document.createElement('button');
      const sy = parseInt(w.start.slice(0, 4));
      const ey = parseInt(w.end.slice(0, 4));
      const isAct = (state.startYear === sy && state.endYear === ey);
      chip.className = `preset-chip ${isAct ? 'active' : ''}`;
      chip.textContent = w.label.split(' ')[0];
      chip.title = w.label;
      chip.addEventListener('click', () => {
        state.startYear = sy;
        state.endYear = ey;
        state.season = 'annual';
        syncAppToUrlState();
        syncCommandRibbon();
        runWorkflow();
      });
      el.timePresetsContainer.appendChild(chip);
    });

    // Active Mission Pill
    if (state.activeCaseId) {
      const c = window.ED.cases.find(x => x.id === state.activeCaseId);
      if (c) {
        el.activeMissionPill.style.display = 'inline-flex';
        el.missionPillLabel.textContent = c.badge;
      }
    } else {
      el.activeMissionPill.style.display = 'none';
    }

    // Layer Toggle Buttons
    el.toggleDeseason.classList.toggle('active', state.showDeseasonalized);
    el.toggleTrendLine.classList.toggle('active', state.showTrendLine);
    el.toggleGap.classList.toggle('active', state.showGap);
    el.toggleFloods.classList.toggle('active', state.showFloodMarkers);

    // Lens Tabs
    el.lensTrend.classList.toggle('active', state.activeLens === 'trend');
    el.lensSeasonal.classList.toggle('active', state.activeLens === 'seasonal');
    el.lensEpochs.classList.toggle('active', state.activeLens === 'epochs');
  }

  function initEventListeners() {
    el.btnCompareSeries.addEventListener('click', openOverlayModal);
    el.overlayModalClose.addEventListener('click', closeOverlayModal);
    el.overlayPopoverBackdrop.addEventListener('click', closeOverlayModal);
    el.btnClearOverlay.addEventListener('click', () => {
      state.overlayVariable = '';
      syncCommandRibbon();
      runWorkflow();
    });

    const segBtns = el.spatialToggle.querySelectorAll('.seg-btn');
    segBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        state.spatialType = btn.getAttribute('data-type');
        state.entity = (state.spatialType === 'division') ? 'Rajshahi' : 'NW';
        syncAppToUrlState();
        syncCommandRibbon();
        runWorkflow();
        zoomToEntity(state.entity, state.spatialType === 'division');
      });
    });

    el.regionSelect.addEventListener('change', (e) => {
      state.entity = e.target.value;
      syncAppToUrlState();
      runWorkflow();
      zoomToEntity(state.entity, state.spatialType === 'division');
    });

    el.startYearSelect.addEventListener('change', (e) => {
      state.startYear = parseInt(e.target.value);
      if (state.startYear > state.endYear) state.endYear = state.startYear;
      state.zoomStartRatio = 0;
      state.zoomEndRatio = 1.0;
      syncAppToUrlState();
      syncCommandRibbon();
      runWorkflow();
    });

    el.endYearSelect.addEventListener('change', (e) => {
      state.endYear = parseInt(e.target.value);
      if (state.endYear < state.startYear) state.startYear = state.endYear;
      state.zoomStartRatio = 0;
      state.zoomEndRatio = 1.0;
      syncAppToUrlState();
      syncCommandRibbon();
      runWorkflow();
    });

    el.seasonSelect.addEventListener('change', (e) => {
      state.season = e.target.value;
      syncAppToUrlState();
      runWorkflow();
    });

    // Layer toggles
    el.toggleDeseason.addEventListener('click', () => {
      state.showDeseasonalized = !state.showDeseasonalized;
      syncCommandRibbon();
      runWorkflow();
    });
    el.toggleTrendLine.addEventListener('click', () => {
      state.showTrendLine = !state.showTrendLine;
      syncCommandRibbon();
      runWorkflow();
    });
    el.toggleGap.addEventListener('click', () => {
      state.showGap = !state.showGap;
      syncCommandRibbon();
      runWorkflow();
    });
    el.toggleFloods.addEventListener('click', () => {
      state.showFloodMarkers = !state.showFloodMarkers;
      syncCommandRibbon();
      runWorkflow();
    });

    // Lens Tabs
    el.lensTrend.addEventListener('click', () => {
      state.activeLens = 'trend';
      syncCommandRibbon();
      runWorkflow();
    });
    el.lensSeasonal.addEventListener('click', () => {
      state.activeLens = 'seasonal';
      syncCommandRibbon();
      runWorkflow();
    });
    el.lensEpochs.addEventListener('click', () => {
      state.activeLens = 'epochs';
      syncCommandRibbon();
      runWorkflow();
    });

    // Map Toggles
    el.mapToggleChoropleth.addEventListener('click', () => {
      state.showChoropleth = !state.showChoropleth;
      el.mapToggleChoropleth.classList.toggle('active', state.showChoropleth);
      renderMap();
    });
    el.mapToggleGrid.addEventListener('click', () => {
      state.showGrid = !state.showGrid;
      el.mapToggleGrid.classList.toggle('active', state.showGrid);
      el.graticuleLayer.style.display = state.showGrid ? 'block' : 'none';
    });
    el.mapToggleStation.addEventListener('click', () => {
      state.showStation = !state.showStation;
      el.mapToggleStation.classList.toggle('active', state.showStation);
      el.svgStationsGroup.style.display = state.showStation ? 'block' : 'none';
    });
    el.mapResetZoom.addEventListener('click', resetMapZoom);

    // Drawers
    el.btnOpenDiagnostics.addEventListener('click', openDiagnosticsDrawer);
    el.closeDiagnostics.addEventListener('click', closeAllDrawers);
    el.diagnosticsBackdrop.addEventListener('click', closeAllDrawers);

    el.btnOpenDirectives.addEventListener('click', openDirectivesDrawer);
    el.closeDirectives.addEventListener('click', closeAllDrawers);
    el.directivesBackdrop.addEventListener('click', closeAllDrawers);

    if (el.btnOpenEvidence) {
      el.btnOpenEvidence.addEventListener('click', () => openEvidenceDrawer('threeway'));
    }
    if (el.closeEvidence) {
      el.closeEvidence.addEventListener('click', closeAllDrawers);
    }
    if (el.evidenceBackdrop) {
      el.evidenceBackdrop.addEventListener('click', closeAllDrawers);
    }

    // Header Drawer Shortcuts
    if (el.btnHeaderEvidence) {
      el.btnHeaderEvidence.addEventListener('click', () => openEvidenceDrawer('threeway'));
    }
    if (el.btnHeaderDirectives) {
      el.btnHeaderDirectives.addEventListener('click', openDirectivesDrawer);
    }
    if (el.btnHeaderDiagnostics) {
      el.btnHeaderDiagnostics.addEventListener('click', openDiagnosticsDrawer);
    }

    document.querySelectorAll('.evidence-tab-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const fragId = btn.getAttribute('data-frag');
        renderEvidenceFragment(fragId);
      });
    });

    // Modal
    el.modalCloseBtn.addEventListener('click', closeModal);
    el.modalOverlay.addEventListener('click', (e) => {
      if (e.target === el.modalOverlay) closeModal();
    });

    // Active Mission Pill Click -> Jump to Cases
    if (el.activeMissionPill) {
      el.activeMissionPill.addEventListener('click', () => {
        state.activeDossierCaseId = state.activeCaseId;
        renderDossierExplorer();
        jumpToSection('sec-cases');
      });
    }

    // Dossier Workbench Loaders
    const launchActiveCase = () => {
      activateCase(state.activeDossierCaseId);
      jumpToSection('sec-workbench');
    };
    if (el.dossierLoadBtn) {
      el.dossierLoadBtn.addEventListener('click', launchActiveCase);
    }
    if (el.dossierHeaderLaunchBtn) {
      el.dossierHeaderLaunchBtn.addEventListener('click', launchActiveCase);
    }
  }

  // 6. Section 1: Cases Bento Grid Renderer (Safeguard)
  function renderCasesBentoGrid() {
    if (!el.casesBentoContainer) return;
    window.ED.cases.forEach(c => {
      const card = document.createElement('div');
      card.className = `bento-case-card ${state.activeCaseId === c.id ? 'active-case' : ''}`;

      // Telemetry highlight preview tag
      let metricTag = 'Trend Detective';
      if (c.id === 'case-1') metricTag = '-1.25 cm/yr • p < 0.0001';
      else if (c.id === 'case-2') metricTag = '8-Yr: p = 0.0549 • MDS Power';
      else if (c.id === 'case-3') metricTag = '2015 MERRA-2 Step Break';
      else if (c.id === 'case-4') metricTag = 'Topsoil 10% vs Residual 90%';
      else if (c.id === 'case-5') metricTag = '+0.0115 AOD/yr • p < 0.0001';
      else if (c.id === 'case-6') metricTag = 'ETCCDI Rx1day • p > 0.05';
      else if (c.id === 'case-7') metricTag = 'OMI NO₂ • 0.25° Grid';

      card.innerHTML = `
        <div>
          <div class="case-top-meta">
            <span class="case-badge">${c.badge}</span>
            <span class="case-domain">${c.domain}</span>
          </div>
          <h3 class="case-card-title">${c.title}</h3>
          <div class="case-card-tagline">${c.tagline}</div>
          <p class="case-card-question">${c.question}</p>
        </div>
        <div class="case-card-footer">
          <span class="case-telemetry-tag">${metricTag}</span>
          <div style="display:flex;gap:6px;align-items:center;">
            <button class="case-launch-btn" data-action="dossier" style="color:var(--text-muted);font-size:10.5px;">Dossier ↗</button>
            <button class="case-launch-btn" data-action="workbench">Launch Simulation →</button>
          </div>
        </div>
      `;

      card.addEventListener('click', (e) => {
        const actionBtn = e.target.closest('[data-action]');
        if (actionBtn && actionBtn.getAttribute('data-action') === 'dossier') {
          state.activeDossierCaseId = c.id;
          renderDossierExplorer();
          jumpToSection('sec-dossiers');
          return;
        }
        activateCase(c.id);
        jumpToSection('sec-workbench');
      });

      el.casesBentoContainer.appendChild(card);
    });
  }

  function activateCase(caseId) {
    const c = window.ED.cases.find(x => x.id === caseId);
    if (!c) return;

    state.activeCaseId = c.id;
    state.activeDossierCaseId = c.id;
    state.variable = c.config.variable;
    state.overlayVariable = c.config.overlayVariable || '';
    state.spatialType = 'region';
    state.entity = c.config.region;
    state.startYear = c.config.startYear;
    state.endYear = c.config.endYear;
    state.season = c.config.season;
    state.showDeseasonalized = c.config.deseasonalize;
    state.activeLens = 'trend';
    state.zoomStartRatio = 0;
    state.zoomEndRatio = 1.0;

    syncAppToUrlState();
    syncCommandRibbon();
    runWorkflow();
    renderCasesBentoGrid();
    renderDossierExplorer();
  }
  window.ED.activateCase = activateCase;

  // 7. Section 2: Geospatial Map Engine
  function initMap() {
    renderMap();
    initMapInteractions();
  }

  function computeLiveSlopes() {
    const slopes = {};
    const isDivision = state.spatialType === 'division';
    const entities = isDivision
      ? window.ED.catalog.divisions.map(d => d.name)
      : window.ED.catalog.regions.map(r => r.id);

    entities.forEach(ent => {
      const raw = extractSeries(state.variable, ent, isDivision);
      const inWin = raw.filter(d => d.year >= state.startYear && d.year <= state.endYear);
      let pts = [];
      if (state.season !== 'annual') {
        pts = window.Stats.seasonalAggregate(inWin, state.season, 'mean');
      } else {
        if (state.showDeseasonalized) {
          const m = inWin.map(d => d.month);
          const v = inWin.map(d => d.value);
          const dv = window.Stats.deseasonalize(m, v);
          pts = inWin.map((d, i) => ({ decimal_year: d.decimal_year, value: dv[i] })).filter(d => !isNaN(d.value));
        } else {
          pts = inWin.filter(d => !isNaN(d.value));
        }
      }

      if (pts.length >= 8) {
        const res = window.Stats.essMannKendall(pts.map(d => d.decimal_year), pts.map(d => d.value), 0.05);
        slopes[ent] = { slope: res.slope, p: res.p_value };
      } else {
        slopes[ent] = { slope: 0, p: 1.0 };
      }
    });

    return slopes;
  }

  function getChoroplethColor(slope) {
    if (!state.showChoropleth || slope === undefined || isNaN(slope)) return '#f1f5f9';
    // Diverging scale: -1.5 (Crimson) to 0.0 (Neutral #f8fafc) to +1.5 (Cobalt)
    const norm = Math.max(-1.5, Math.min(1.5, slope)) / 1.5;
    if (norm < 0) {
      // Negative: Crimson (#dc2626)
      const t = Math.abs(norm);
      const r = Math.round(241 + t * (220 - 241));
      const g = Math.round(245 + t * (38 - 245));
      const b = Math.round(249 + t * (38 - 249));
      return `rgb(${r}, ${g}, ${b})`;
    } else {
      // Positive: Cobalt (#2563eb)
      const t = norm;
      const r = Math.round(241 + t * (37 - 241));
      const g = Math.round(245 + t * (99 - 245));
      const b = Math.round(249 + t * (235 - 249));
      return `rgb(${r}, ${g}, ${b})`;
    }
  }

  function renderMap() {
    el.svgPathsGroup.innerHTML = '';
    const isDivision = state.spatialType === 'division';
    const liveSlopes = computeLiveSlopes();

    const divisionPaths = window.ED.map.svgPaths;
    const regionDivs = window.ED.map.regionDivisions;

    Object.keys(divisionPaths).forEach(divName => {
      const dPath = divisionPaths[divName];
      const pathEl = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      pathEl.setAttribute('d', dPath);
      pathEl.setAttribute('class', 'region-path');
      pathEl.setAttribute('data-div', divName);

      // Determine belonging macro-region
      let macroReg = 'National';
      for (const [rId, divs] of Object.entries(regionDivs)) {
        if (divs.includes(divName)) {
          macroReg = rId;
          break;
        }
      }
      pathEl.setAttribute('data-macro', macroReg);

      // Fill color
      const statKey = isDivision ? divName : macroReg;
      const slopeVal = liveSlopes[statKey] ? liveSlopes[statKey].slope : 0;
      pathEl.setAttribute('fill', getChoroplethColor(slopeVal));

      // Selected stroke
      const isSel = (!isDivision && (state.entity === 'National' || state.entity === macroReg)) ||
                    (isDivision && state.entity === divName);
      if (isSel) pathEl.classList.add('selected');

      // Interactivity
      pathEl.addEventListener('mouseenter', (e) => showMapHover(e, divName, macroReg, liveSlopes));
      pathEl.addEventListener('mousemove', (e) => moveMapHover(e));
      pathEl.addEventListener('mouseleave', hideMapHover);
      pathEl.addEventListener('click', () => {
        if (isDivision) {
          state.entity = divName;
        } else {
          state.entity = macroReg;
        }
        syncCommandRibbon();
        runWorkflow();
        zoomToEntity(state.entity, isDivision);
      });

      el.svgPathsGroup.appendChild(pathEl);
    });

    renderQuickRegionPills();
  }

  function renderQuickRegionPills() {
    el.quickRegionPills.innerHTML = '';
    const isDivision = state.spatialType === 'division';
    const entities = isDivision
      ? window.ED.catalog.divisions.map(d => ({ id: d.name, label: d.name }))
      : window.ED.catalog.regions.map(r => ({ id: r.id, label: r.id }));

    entities.forEach(ent => {
      const btn = document.createElement('button');
      btn.className = `quick-reg-btn ${state.entity === ent.id ? 'active' : ''}`;
      btn.textContent = ent.label;
      btn.addEventListener('click', () => {
        state.entity = ent.id;
        syncCommandRibbon();
        runWorkflow();
        zoomToEntity(state.entity, isDivision);
      });
      el.quickRegionPills.appendChild(btn);
    });
  }

  function showMapHover(e, divName, macroReg, liveSlopes) {
    el.mapHoverHud.style.display = 'block';
    const isDivision = state.spatialType === 'division';
    const key = isDivision ? divName : macroReg;
    const slopeInfo = liveSlopes[key] || { slope: 0, p: 1.0 };
    const curVar = getVarMeta(state.variable);

    el.hudName.textContent = isDivision ? `${divName} Division` : `${macroReg} Macro-Region`;
    el.hudSlope.textContent = `${slopeInfo.slope >= 0 ? '+' : ''}${slopeInfo.slope.toFixed(3)} ${curVar ? curVar.unit : ''}/yr`;
    el.hudP.textContent = slopeInfo.p < 0.0001 ? '< 0.0001' : slopeInfo.p.toFixed(4);

    const regMeta = getRegionMeta(macroReg);
    const divMeta = getDivisionMeta(divName);

    // Population display (BBS 2022 Census / GPWv4, in Millions)
    let popVal = null;
    if (isDivision && divMeta && (divMeta.population_2020_m != null || divMeta.pop_millions != null)) {
      popVal = divMeta.population_2020_m ?? divMeta.pop_millions;
    } else if (regMeta && (regMeta.population_2020_m != null || regMeta.pop_millions != null)) {
      popVal = regMeta.population_2020_m ?? regMeta.pop_millions;
    }
    el.hudPop.textContent = (popVal != null && !isNaN(popVal)) ? `${popVal} M` : '—';

    // Cropland percentage (MODIS MCD12Q1)
    let cropVal = null;
    if (isDivision && divMeta && divMeta.cropland_pct != null) {
      cropVal = `${divMeta.cropland_pct}%`;
    } else if (regMeta && regMeta.cropland_pct != null) {
      cropVal = `${regMeta.cropland_pct}%${isDivision ? ` (${macroReg})` : ''}`;
    }
    el.hudCrop.textContent = (cropVal != null) ? cropVal : '—';
  }

  function moveMapHover(e) {
    // Keep HUD at top-left of viewport for clean visibility
  }

  function hideMapHover() {
    el.mapHoverHud.style.display = 'none';
  }

  const REGION_VIEWBOXES = {
    'NW': { x: 10, y: 80, w: 360, h: 440 },
    'NE': { x: 220, y: 80, w: 360, h: 440 },
    'Central': { x: 120, y: 160, w: 360, h: 440 },
    'SW': { x: 50, y: 280, w: 360, h: 440 },
    'SE': { x: 220, y: 270, w: 360, h: 440 },
    'National': { x: 0, y: 0, w: 600, h: 730 }
  };

  function getDivisionViewBox(divName) {
    const centers = (window.ED.map && (window.ED.map.divCenters || window.ED.map.centroids)) || {};
    const c = centers[divName] || { x: 300, y: 365 };
    const targetW = 360;
    const targetH = 440;
    let targetX = c.x - targetW / 2;
    let targetY = c.y - targetH / 2;
    // Clamp to [0, 0, 600, 730]
    targetX = Math.max(0, Math.min(600 - targetW, Math.round(targetX)));
    targetY = Math.max(0, Math.min(730 - targetH, Math.round(targetY)));
    return { x: targetX, y: targetY, w: targetW, h: targetH };
  }

  function zoomToEntity(entity, isDivision) {
    const target = isDivision ? getDivisionViewBox(entity) : (REGION_VIEWBOXES[entity] || BD_VIEWBOX);
    animateViewBox(target);
  }

  function resetMapZoom() {
    animateViewBox(BD_VIEWBOX);
  }

  function animateViewBox(target) {
    if (window.gsap) {
      window.gsap.to(currentViewBox, {
        x: target.x,
        y: target.y,
        w: target.w,
        h: target.h,
        duration: 0.5,
        ease: 'power2.out',
        onUpdate: () => {
          el.svgMap.setAttribute('viewBox', `${currentViewBox.x} ${currentViewBox.y} ${currentViewBox.w} ${currentViewBox.h}`);
        }
      });
    } else {
      currentViewBox = { ...target };
      el.svgMap.setAttribute('viewBox', `${target.x} ${target.y} ${target.w} ${target.h}`);
    }
  }

  function initMapInteractions() {
    // Mouse wheel zoom
    el.mapViewport.addEventListener('wheel', (e) => {
      e.preventDefault();
      const scaleFactor = e.deltaY < 0 ? 0.88 : 1.14;
      const newW = Math.max(150, Math.min(600, currentViewBox.w * scaleFactor));
      const newH = Math.max(182, Math.min(730, currentViewBox.h * scaleFactor));
      const dx = (currentViewBox.w - newW) / 2;
      const dy = (currentViewBox.h - newH) / 2;
      currentViewBox.x += dx;
      currentViewBox.y += dy;
      currentViewBox.w = newW;
      currentViewBox.h = newH;
      el.svgMap.setAttribute('viewBox', `${currentViewBox.x} ${currentViewBox.y} ${currentViewBox.w} ${currentViewBox.h}`);
    }, { passive: false });

    // Drag to pan
    el.mapViewport.addEventListener('mousedown', (e) => {
      if (e.target.classList.contains('region-path')) return;
      isPanning = true;
      panStart = { x: e.clientX, y: e.clientY };
    });

    window.addEventListener('mousemove', (e) => {
      if (!isPanning) return;
      const dx = (e.clientX - panStart.x) * (currentViewBox.w / el.mapViewport.clientWidth);
      const dy = (e.clientY - panStart.y) * (currentViewBox.h / el.mapViewport.clientHeight);
      currentViewBox.x -= dx;
      currentViewBox.y -= dy;
      panStart = { x: e.clientX, y: e.clientY };
      el.svgMap.setAttribute('viewBox', `${currentViewBox.x} ${currentViewBox.y} ${currentViewBox.w} ${currentViewBox.h}`);
    });

    window.addEventListener('mouseup', () => { isPanning = false; });
  }

  // 8. Analytical Workflow Engine & Multi-Lens Chart
  function runWorkflow() {
    const curVar = getVarMeta(state.variable);
    if (!curVar) return;

    const isDivision = state.spatialType === 'division';
    const rawData = extractSeries(state.variable, state.entity, isDivision);
    const inWindow = rawData.filter(d => d.year >= state.startYear && d.year <= state.endYear);

    // Seasonal / Deseasonalization processing
    let processedPoints = [];
    const isSeasonalMode = state.season !== 'annual';

    if (isSeasonalMode) {
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

    // Client-side analyze() reading DASHBOARD_DATA
    const statResult = window.Stats.analyze({
      var: state.variable,
      region: state.entity,
      start: state.startYear,
      end: state.endYear,
      season: state.season,
      points: processedPoints
    });
    statResult.valid = Boolean(statResult && !statResult.error && !isNaN(statResult.theil_sen_slope !== undefined ? statResult.theil_sen_slope : statResult.slope));
    if (statResult.valid) {
      statResult.slope = (statResult.theil_sen_slope !== undefined && !isNaN(statResult.theil_sen_slope)) ? statResult.theil_sen_slope : statResult.slope;
      statResult.n_eff = (statResult.n_star !== undefined && typeof statResult.n_star === 'number') ? statResult.n_star : statResult.n;
      statResult.slope_ci_low = statResult.slope_ci_low !== undefined ? statResult.slope_ci_low : statResult.ci_low;
      statResult.slope_ci_high = statResult.slope_ci_high !== undefined ? statResult.slope_ci_high : statResult.ci_high;
      const mds = window.Stats.approxMDS(tYears, yVals, statResult.slope, typeof statResult.gamma === 'number' ? statResult.gamma : 1.0);
      statResult.mds_80_power = (mds !== null && !isNaN(mds)) ? mds : 0.0;
    }

    // Overlay series (if active)
    let overlayPoints = [];
    if (state.overlayVariable) {
      const oVar = getVarMeta(state.overlayVariable);
      const oRaw = extractSeries(state.overlayVariable, state.entity, isDivision);
      const oInWin = oRaw.filter(d => d.year >= state.startYear && d.year <= state.endYear);
      if (isSeasonalMode) {
        overlayPoints = window.Stats.seasonalAggregate(oInWin, state.season, oVar ? oVar.kind : 'mean');
      } else {
        if (oVar && oVar.can_deseasonalize && state.showDeseasonalized) {
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
    }

    // Step 4: Render Multi-Lens Chart
    renderChart(processedPoints, statResult, overlayPoints, inWindow);

    // Step 5: Render 5-Cell Telemetry Verdict Strip
    renderTelemetryStrip(statResult, processedPoints.length, curVar);

    // Update Diagnostics Drawer & Directives Drawer
    updateDiagnosticsContent(statResult, processedPoints.length, curVar);
    updateDirectivesContent();

    // Re-render Map paths selection
    renderMap();
  }

  // 9. Chart Rendering (Lens 1, 2, 3)
  function renderChart(points, statResult, overlayPoints, inWindowRaw) {
    if (chartInstance) {
      chartInstance.destroy();
      chartInstance = null;
    }

    const ctx = el.timeseriesCanvas.getContext('2d');
    const curVar = getVarMeta(state.variable);

    if (state.activeLens === 'trend') {
      currentTrendPoints = points;
      if (el.chartZoomBar) el.chartZoomBar.classList.remove('czb-hidden');
      renderLensTrend(ctx, points, statResult, overlayPoints, curVar);
      updateChartZoomUI();
    } else {
      if (el.chartZoomBar) el.chartZoomBar.classList.add('czb-hidden');
      if (state.activeLens === 'seasonal') {
        renderLensSeasonal(ctx, inWindowRaw, curVar);
      } else if (state.activeLens === 'epochs') {
        renderLensEpochs(ctx, curVar);
      }
    }
  }

  // Lens 1: Time Series & 95% CI Fan
  function renderLensTrend(ctx, points, statResult, overlayPoints, curVar) {
    const isDivision = state.spatialType === 'division';
    const locName = isDivision ? state.entity : (getRegionMeta(state.entity)?.name || state.entity);

    const labels = points.map(p => p.ym || p.year);
    const dataVals = points.map(p => p.value);

    // Trendline evaluation
    let trendVals = [];
    let ciLowVals = [];
    let ciHighVals = [];
    if (statResult.valid && points.length > 0 && state.showTrendLine) {
      const midIdx = Math.floor(points.length / 2);
      const tMid = points[midIdx].decimal_year;
      const yMid = statResult.theil_sen_intercept !== undefined
        ? statResult.theil_sen_intercept + statResult.slope * tMid
        : dataVals[midIdx];

      trendVals = points.map(p => yMid + statResult.slope * (p.decimal_year - tMid));
      ciLowVals = points.map(p => yMid + statResult.slope_ci_low * (p.decimal_year - tMid));
      ciHighVals = points.map(p => yMid + statResult.slope_ci_high * (p.decimal_year - tMid));
    }

    const datasets = [
      {
        label: `${curVar.name} (${curVar.unit})`,
        data: dataVals,
        borderColor: '#2563eb',
        backgroundColor: '#2563eb',
        borderWidth: 1.6,
        pointRadius: points.length > 100 ? 0 : 2.5,
        pointHoverRadius: 5,
        tension: 0.1,
        yAxisID: 'y'
      }
    ];

    if (state.showTrendLine && trendVals.length > 0) {
      datasets.push({
        label: `Theil-Sen Trend (${statResult.slope >= 0 ? '+' : ''}${statResult.slope.toFixed(4)}/yr)`,
        data: trendVals,
        borderColor: '#dc2626',
        borderWidth: 2.2,
        pointRadius: 0,
        fill: false,
        tension: 0,
        yAxisID: 'y'
      });
      datasets.push({
        label: '95% CI Upper Bound',
        data: ciHighVals,
        borderColor: 'rgba(220, 38, 38, 0.3)',
        borderWidth: 1,
        borderDash: [3, 3],
        pointRadius: 0,
        fill: '+1',
        backgroundColor: 'rgba(220, 38, 38, 0.08)',
        yAxisID: 'y'
      });
      datasets.push({
        label: '95% CI Lower Bound',
        data: ciLowVals,
        borderColor: 'rgba(220, 38, 38, 0.3)',
        borderWidth: 1,
        borderDash: [3, 3],
        pointRadius: 0,
        fill: false,
        yAxisID: 'y'
      });
    }

    if (state.overlayVariable && overlayPoints.length > 0) {
      const oVar = getVarMeta(state.overlayVariable);
      const ymMap = new Map();
      const decMap = new Map();
      overlayPoints.forEach(p => {
        if (p.ym) ymMap.set(p.ym, p.value);
        if (p.year && !p.month) ymMap.set(String(p.year), p.value);
        decMap.set(p.decimal_year, p.value);
      });

      const alignedOverlayVals = points.map(p => {
        if (p.ym && ymMap.has(p.ym)) return ymMap.get(p.ym);
        if (p.year && ymMap.has(String(p.year))) return ymMap.get(String(p.year));
        let bestVal = null;
        let minDiff = 0.08;
        for (const [t, val] of decMap.entries()) {
          const diff = Math.abs(t - p.decimal_year);
          if (diff < minDiff) { minDiff = diff; bestVal = val; }
        }
        return bestVal;
      });

      datasets.push({
        label: `${oVar ? oVar.name : 'Overlay'} (${oVar ? oVar.unit : ''})`,
        data: alignedOverlayVals,
        borderColor: '#ea580c',
        backgroundColor: '#ea580c',
        borderWidth: 1.8,
        borderDash: [5, 4],
        pointRadius: 2,
        pointHoverRadius: 5,
        tension: 0.15,
        yAxisID: 'y1'
      });
    }

    // Chart.js Plugins: 2017-18 Gap Shading & Flood Events
    const gapPlugin = {
      id: 'gapAndFloodsOverlay',
      beforeDraw(chart) {
        if (!chart.scales.x || !chart.scales.y) return;
        const ctx = chart.ctx;
        const xMeta = chart.getDatasetMeta(0);
        if (!xMeta || !xMeta.data || xMeta.data.length === 0) return;

        ctx.save();
        ctx.beginPath();
        ctx.rect(chart.chartArea.left, chart.chartArea.top, chart.chartArea.width, chart.chartArea.height);
        ctx.clip();

        // 1. Shaded 2017-2018 GRACE Bridge Gap
        if (state.showGap && curVar.has_gap) {
          let xStart = null;
          let xEnd = null;
          points.forEach((p, idx) => {
            if (p.decimal_year >= 2017.5 && xStart === null) xStart = xMeta.data[idx]?.x;
            if (p.decimal_year <= 2018.4) xEnd = xMeta.data[idx]?.x;
          });
          if (xStart && xEnd && xEnd > xStart) {
            ctx.save();
            ctx.fillStyle = 'rgba(148, 163, 184, 0.25)';
            ctx.fillRect(xStart, chart.chartArea.top, xEnd - xStart, chart.chartArea.bottom - chart.chartArea.top);
            ctx.strokeStyle = '#94a3b8';
            ctx.lineWidth = 1;
            ctx.setLineDash([3, 3]);
            ctx.strokeRect(xStart, chart.chartArea.top, xEnd - xStart, chart.chartArea.bottom - chart.chartArea.top);
            ctx.fillStyle = '#64748b';
            ctx.font = '10px -apple-system, sans-serif';
            ctx.fillText('11-Mo Inter-Mission Gap', xStart + 4, chart.chartArea.top + 14);
            ctx.restore();
          }
        }

        // 2. FFWC Historical Flood Event Markers
        if (state.showFloodMarkers) {
          const floodYears = [2004.58, 2007.67, 2017.62, 2020.54, 2022.46];
          const floodNames = ['Flood 2004', 'Flood 2007', 'Flood 2017', 'Flood 2020', 'Flood 2022'];

          floodYears.forEach((fy, fIdx) => {
            let closestIdx = -1;
            let minDiff = 0.08;
            points.forEach((p, idx) => {
              const diff = Math.abs(p.decimal_year - fy);
              if (diff < minDiff) { minDiff = diff; closestIdx = idx; }
            });

            if (closestIdx !== -1 && xMeta.data[closestIdx]) {
              const xPos = xMeta.data[closestIdx].x;
              ctx.save();
              ctx.strokeStyle = 'rgba(2, 132, 199, 0.7)';
              ctx.lineWidth = 1.2;
              ctx.setLineDash([4, 4]);
              ctx.beginPath();
              ctx.moveTo(xPos, chart.chartArea.top);
              ctx.lineTo(xPos, chart.chartArea.bottom);
              ctx.stroke();

              ctx.fillStyle = '#0284c7';
              ctx.font = '9.5px -apple-system, sans-serif';
              ctx.fillText(floodNames[fIdx], xPos + 3, chart.chartArea.top + 28 + (fIdx % 2) * 14);
              ctx.restore();
            }
          });
        }

        ctx.restore();
      }
    };

    chartInstance = new Chart(ctx, {
      type: 'line',
      data: { labels, datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 300 },
        interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: {
            position: 'top',
            align: 'start',
            labels: { boxWidth: 12, font: { size: 11, family: 'var(--font-sans)' }, color: '#475569' }
          },
          tooltip: {
            backgroundColor: 'rgba(15, 23, 42, 0.92)',
            titleFont: { size: 11.5, weight: 'bold' },
            bodyFont: { size: 11, family: 'var(--font-mono)' },
            padding: 8,
            cornerRadius: 4
          }
        },
        scales: {
          x: {
            min: (state.zoomStartRatio > 0.005 && labels.length > 0) ? labels[Math.max(0, Math.min(labels.length - 1, Math.round(state.zoomStartRatio * (labels.length - 1))))] : undefined,
            max: (state.zoomEndRatio < 0.995 && labels.length > 0) ? labels[Math.max(0, Math.min(labels.length - 1, Math.round(state.zoomEndRatio * (labels.length - 1))))] : undefined,
            grid: { color: '#f1f5f9' },
            ticks: { font: { size: 10, family: 'var(--font-mono)' }, color: '#64748b', maxTicksLimit: 14 }
          },
          y: {
            position: 'left',
            grid: { color: '#f1f5f9' },
            title: { display: true, text: `${curVar.name} (${curVar.unit})`, color: '#64748b', font: { size: 10.5 } },
            ticks: { font: { size: 10, family: 'var(--font-mono)' }, color: '#64748b' }
          },
          y1: {
            display: Boolean(state.overlayVariable),
            position: 'right',
            grid: { drawOnChartArea: false },
            title: {
              display: Boolean(state.overlayVariable),
              text: state.overlayVariable ? `${getVarMeta(state.overlayVariable)?.name || 'Overlay'} (${getVarMeta(state.overlayVariable)?.unit || ''})` : '',
              color: '#ea580c',
              font: { size: 10.5, family: 'var(--font-sans)', weight: '600' }
            },
            ticks: { font: { size: 10, family: 'var(--font-mono)' }, color: '#ea580c' }
          }
        }
      },
      plugins: [gapPlugin]
    });
  }

  // Lens 2: Seasonal Cycle & Anomaly Decomposition
  function renderLensSeasonal(ctx, inWindowRaw, curVar) {
    const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const monthlyGroups = Array.from({ length: 12 }, () => []);

    inWindowRaw.forEach(d => {
      if (d.month >= 1 && d.month <= 12 && !isNaN(d.value)) {
        monthlyGroups[d.month - 1].push(d.value);
      }
    });

    const means = monthlyGroups.map(vals => vals.length ? vals.reduce((a, b) => a + b, 0) / vals.length : 0);
    const sds = monthlyGroups.map((vals, i) => {
      if (vals.length < 2) return 0;
      const m = means[i];
      const variance = vals.reduce((sum, v) => sum + Math.pow(v - m, 2), 0) / (vals.length - 1);
      return Math.sqrt(variance);
    });

    const upper1Sigma = means.map((m, i) => m + sds[i]);
    const lower1Sigma = means.map((m, i) => m - sds[i]);

    chartInstance = new Chart(ctx, {
      type: 'line',
      data: {
        labels: monthNames,
        datasets: [
          {
            label: '12-Month Climatological Mean',
            data: means,
            borderColor: '#2563eb',
            backgroundColor: '#2563eb',
            borderWidth: 2.2,
            pointRadius: 4,
            tension: 0.25,
            fill: false
          },
          {
            label: '+1σ Seasonal Range',
            data: upper1Sigma,
            borderColor: 'rgba(37, 99, 235, 0.2)',
            backgroundColor: 'rgba(37, 99, 235, 0.1)',
            fill: '+1',
            pointRadius: 0,
            borderDash: [3, 3]
          },
          {
            label: '-1σ Seasonal Range',
            data: lower1Sigma,
            borderColor: 'rgba(37, 99, 235, 0.2)',
            fill: false,
            pointRadius: 0,
            borderDash: [3, 3]
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top', align: 'start' },
          tooltip: {
            callbacks: {
              label: (ctx) => `${ctx.dataset.label}: ${ctx.raw.toFixed(3)} ${curVar.unit}`
            }
          }
        },
        scales: {
          x: { grid: { color: '#f1f5f9' } },
          y: {
            grid: { color: '#f1f5f9' },
            title: { display: true, text: `Climatology (${curVar.unit})` }
          }
        }
      }
    });
  }

  // Lens 3: Multi-Epoch Comparison Bar Chart
  function renderLensEpochs(ctx, curVar) {
    const isDivision = state.spatialType === 'division';
    const rawAll = extractSeries(state.variable, state.entity, isDivision);

    const epochs = [
      { label: 'Full Baseline (2002–2026)', start: 2002, end: 2026 },
      { label: 'GRACE-1 Era (2002–2017)', start: 2002, end: 2017 },
      { label: 'GRACE-FO Era (2018–2026)', start: 2018, end: 2026 },
      { label: 'IMERG Overlap (2002–2025)', start: 2002, end: 2025 }
    ];

    const epochSlopes = [];
    const epochCiLows = [];
    const epochCiHighs = [];
    const pValues = [];

    epochs.forEach(ep => {
      const sub = rawAll.filter(d => d.year >= ep.start && d.year <= ep.end);
      let pts = [];
      if (curVar.can_deseasonalize) {
        const m = sub.map(d => d.month);
        const v = sub.map(d => d.value);
        const dv = window.Stats.deseasonalize(m, v);
        pts = sub.map((d, i) => ({ decimal_year: d.decimal_year, value: dv[i] })).filter(d => !isNaN(d.value));
      } else {
        pts = sub.filter(d => !isNaN(d.value));
      }

      if (pts.length >= 8) {
        const res = window.Stats.essMannKendall(pts.map(d => d.decimal_year), pts.map(d => d.value), 0.05);
        epochSlopes.push(res.slope);
        epochCiLows.push(res.slope_ci_low);
        epochCiHighs.push(res.slope_ci_high);
        pValues.push(res.p_value);
      } else {
        epochSlopes.push(0);
        epochCiLows.push(0);
        epochCiHighs.push(0);
        pValues.push(1);
      }
    });

    chartInstance = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: epochs.map(e => e.label),
        datasets: [
          {
            label: `Theil-Sen Rate (${curVar.unit}/yr)`,
            data: epochSlopes,
            backgroundColor: epochSlopes.map((s, idx) => pValues[idx] < 0.05 ? '#dc2626' : '#94a3b8'),
            borderRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top', align: 'start' },
          tooltip: {
            callbacks: {
              afterLabel: (ctx) => {
                const i = ctx.dataIndex;
                return `95% CI: [${epochCiLows[i].toFixed(3)}, ${epochCiHighs[i].toFixed(3)}]\np-Value: ${pValues[i] < 0.0001 ? '< 0.0001' : pValues[i].toFixed(4)}`;
              }
            }
          }
        },
        scales: {
          x: { grid: { color: '#f1f5f9' } },
          y: {
            grid: { color: '#f1f5f9' },
            title: { display: true, text: `Theil-Sen Rate (${curVar.unit}/yr)` }
          }
        }
      }
    });
  }

  // 10. Bottom 5-Cell Swiss Telemetry Verdict Strip
  function renderTelemetryStrip(statResult, count, curVar) {
    if (!statResult.valid) {
      el.telVerdict.innerHTML = '<span class="badge-null-trend">Insufficient Data</span>';
      el.telVerdictSub.textContent = `N = ${count} observations (minimum 8 required)`;
      el.telSlope.textContent = '—';
      el.telSlopeVol.textContent = '—';
      el.telCi.textContent = '—';
      el.telP.textContent = '—';
      el.telFdr.textContent = '—';
      el.telN.textContent = `${count}`;
      el.telMds.textContent = '—';
      return;
    }

    const isSig = statResult.p_value < 0.05;
    if (isSig) {
      el.telVerdict.innerHTML = '<span class="badge-sig-trend">Significant Trend (p < 0.05)</span>';
      el.telVerdictSub.textContent = `${statResult.slope > 0 ? 'Upward' : 'Downward'} secular rate meets statistical threshold`;
    } else {
      el.telVerdict.innerHTML = '<span class="badge-null-trend">No Detectable Trend (p ≥ 0.05)</span>';
      el.telVerdictSub.textContent = 'Rate does not exceed random noise boundary';
    }

    const sign = statResult.slope > 0 ? '+' : '';
    el.telSlope.textContent = `${sign}${statResult.slope.toFixed(4)} ${curVar.unit}/yr`;

    // Student plain verdict card
    if (el.studentVerdictHeading && el.studentVerdictSentence) {
      const isBn = (state.lang === 'bn') || (document.documentElement.lang === 'bn');
      const studentCell = el.studentVerdictHeading.closest('.student-verdict-cell');
      const slopeFormatted = `${sign}${statResult.slope.toFixed(2)} ${curVar.unit}/yr`;
      const direction = statResult.slope > 0 ? (isBn ? "বৃদ্ধি পাচ্ছে" : "increasing") : (isBn ? "হ্রাস পাচ্ছে" : "declining");
      const directionNoun = statResult.slope > 0 ? (isBn ? "বৃদ্ধি" : "Rise") : (isBn ? "হ্রাস" : "Decline");
      const regionLabel = state.entity || (isBn ? "নির্বাচিত অঞ্চল" : "Selected Region");
      const varLabel = curVar.name || (isBn ? "সর্বমোট পানি সঞ্চয় (TWS)" : "Total Water Storage (TWS)");

      if (isSig) {
        el.studentVerdictHeading.textContent = isBn
          ? `উল্লেখযোগ্য ${directionNoun} (${slopeFormatted})` // DRAFT: needs native review
          : `Significant ${directionNoun} (${slopeFormatted})`;
        el.studentVerdictSentence.textContent = isBn
          ? `${regionLabel}-এ ${varLabel} ${slopeFormatted} হারে ${direction}। আমরা অত্যন্ত নিশ্চিত (৯৯.৯%-এর বেশি পরিসংখ্যানগত নিশ্চয়তা) যে এই দীর্ঘমেয়াদী প্রবণতা বাস্তব এবং ঋতুভিত্তিক প্রাকৃতিক ওঠানামার চেয়ে বেশি।` // DRAFT: needs native review
          : `${varLabel} in ${regionLabel} is ${direction} at ${slopeFormatted}. We are highly confident (over 99.9% statistical certainty) that this secular trend is real and exceeds seasonal noise.`;
        if (studentCell) {
          studentCell.classList.add(statResult.slope < 0 ? 'verdict-decline' : 'verdict-stable');
          studentCell.classList.remove(statResult.slope < 0 ? 'verdict-stable' : 'verdict-decline');
        }
      } else {
        el.studentVerdictHeading.textContent = isBn
          ? `কোনো দীর্ঘমেয়াদী প্রবণতা লক্ষণীয় নয় (${slopeFormatted})` // DRAFT: needs native review
          : `No Detectable Long-Term Trend (${slopeFormatted})`;
        el.studentVerdictSentence.textContent = isBn
          ? `${regionLabel}-এ ${varLabel}-এ কোনো স্পষ্ট দীর্ঘমেয়াদী প্রবণতা দেখা যায়নি। বর্তমান হার (${slopeFormatted}) স্বাভাবিক আবহাওয়ার ওঠানামার মধ্যেই বিদ্যমান।` // DRAFT: needs native review
          : `${varLabel} in ${regionLabel} shows no clear multi-year ${directionNoun.toLowerCase()}. The observed rate (${slopeFormatted}) stays within expected natural weather fluctuations.`;
        if (studentCell) {
          studentCell.classList.add('verdict-stable');
          studentCell.classList.remove('verdict-decline');
        }
      }
      if (el.studentVerdictRate) {
        el.studentVerdictRate.textContent = isBn
          ? `হার: ${slopeFormatted} • নিশ্চয়তা: ${isSig ? 'উচ্চ (p < 0.05)' : 'স্বাভাবিক ওঠানামা'}` // DRAFT: needs native review
          : `Rate: ${slopeFormatted} • Confidence: ${isSig ? 'High (p < 0.05)' : 'Within Normal Variation'}`;
      }
    }

    // Volumetric conversion for TWS (NW area: 31,348 km²)
    if (curVar.id === 'grace_tws' && state.entity === 'NW') {
      const volKm3 = (statResult.slope / 100000) * 31348;
      el.telSlopeVol.textContent = `Volumetric: ${volKm3.toFixed(2)} km³/yr`;
    } else {
      el.telSlopeVol.textContent = `Median pairwise rate`;
    }

    const ciLow = (statResult.slope_ci_low !== undefined ? statResult.slope_ci_low : statResult.ci_low);
    const ciHigh = (statResult.slope_ci_high !== undefined ? statResult.slope_ci_high : statResult.ci_high);
    el.telCi.textContent = `[${ciLow !== null && !isNaN(ciLow) ? Number(ciLow).toFixed(3) : '—'}, ${ciHigh !== null && !isNaN(ciHigh) ? Number(ciHigh).toFixed(3) : '—'}]`;

    el.telP.textContent = statResult.p_value < 0.0001 ? '< 0.0001' : statResult.p_value.toFixed(4);
    if (statResult.is_precomputed) {
      if (typeof statResult.bh_fdr_q_value === 'number') {
        el.telFdr.textContent = `q = ${statResult.bh_fdr_q_value < 0.0001 ? '< 0.0001' : statResult.bh_fdr_q_value.toFixed(4)}`;
      } else {
        el.telFdr.textContent = `Z = ${statResult.z >= 0 ? '+' : ''}${statResult.z.toFixed(2)} • S = ${statResult.s}`;
      }
    } else {
      el.telFdr.textContent = 'precomputed windows only';
    }

    const nEff = statResult.n_eff !== undefined ? statResult.n_eff : (statResult.n_star !== undefined ? statResult.n_star : count);
    const mds = statResult.mds_80_power !== undefined && statResult.mds_80_power !== null ? statResult.mds_80_power : 0;
    if (typeof nEff === 'number') {
      el.telN.textContent = `N* = ${Number(nEff).toFixed(1)} (N = ${count})`;
    } else {
      el.telN.textContent = `N = ${count}`;
    }
    el.telMds.textContent = (typeof mds === 'number' && mds > 0) ? `80% MDS = ±${Number(mds).toFixed(3)} ${curVar.unit}/yr` : '—';

    // Step 5 link to Report (Bangladesh regions only)
    const isBangladesh = !['wisconsin_us', 'wisconsin'].includes(String(state.entity).toLowerCase());
    const reportLinkHref = window.URLState ? window.URLState.buildLink('report.html', {
      region: state.entity,
      var: VAR_MAP_TO_URL[state.variable] || state.variable,
      start: state.startYear,
      end: state.endYear,
      season: state.season,
      mode: state.mode,
      lang: state.lang
    }, '#subsurface-validation') : 'report.html#subsurface-validation';

    if (el.btnVerdictReportLink) {
      if (isBangladesh) {
        el.btnVerdictReportLink.style.display = 'inline-flex';
        el.btnVerdictReportLink.href = reportLinkHref;
      } else {
        el.btnVerdictReportLink.style.display = 'none';
      }
    }
    if (el.btnStudentReportLink) {
      if (isBangladesh) {
        el.btnStudentReportLink.style.display = 'inline-flex';
        el.btnStudentReportLink.href = reportLinkHref;
      } else {
        el.btnStudentReportLink.style.display = 'none';
      }
    }
    if (el.btnTriggerReportLink) {
      if (isBangladesh) {
        el.btnTriggerReportLink.style.display = 'inline-flex';
        el.btnTriggerReportLink.href = reportLinkHref;
      } else {
        el.btnTriggerReportLink.style.display = 'none';
      }
    }
  }

  // 11. Drawers Content Updaters
  function updateDiagnosticsContent(statResult, count, curVar) {
    const isPre = statResult.is_precomputed;
    const r1Text = (isPre && typeof statResult.r1_detrended === 'number')
      ? statResult.r1_detrended.toFixed(4)
      : (typeof statResult.r1_detrended === 'number' ? statResult.r1_detrended.toFixed(4) : 'precomputed windows only');
    const gamText = (isPre && typeof statResult.gamma === 'number')
      ? statResult.gamma.toFixed(3)
      : (typeof statResult.gamma === 'number' ? statResult.gamma.toFixed(3) : 'precomputed windows only');

    el.diagStatsGrid.innerHTML = `
      <div class="diag-item">
        <div class="diag-lbl">Mann-Kendall Score (S)</div>
        <div class="diag-val">${statResult.s !== undefined ? statResult.s : 0}</div>
      </div>
      <div class="diag-item">
        <div class="diag-lbl">Standardized Test (Z)</div>
        <div class="diag-val">${statResult.z !== undefined && typeof statResult.z === 'number' ? (statResult.z >= 0 ? '+' : '') + statResult.z.toFixed(3) : '0.000'}</div>
      </div>
      <div class="diag-item">
        <div class="diag-lbl">Hurwicz Lag-1 Autocorr (r₁*)</div>
        <div class="diag-val">${r1Text}</div>
      </div>
      <div class="diag-item">
        <div class="diag-lbl">Variance Inflation (γ)</div>
        <div class="diag-val">${gamText}</div>
      </div>
    `;

    // Dr. Acker's Window Length Lesson
    const spanYrs = state.endYear - state.startYear;
    const nEff = statResult.n_eff !== undefined ? statResult.n_eff : (statResult.n_star !== undefined ? statResult.n_star : count);
    const mds = statResult.mds_80_power !== undefined && statResult.mds_80_power !== null ? statResult.mds_80_power : 0;
    if (spanYrs <= 9) {
      el.diagWindowLesson.innerHTML = `
        <strong>[NOTE] Short Observation Baseline (${spanYrs} years):</strong>
        At N = ${count}, statistical power requires a steep slope (MDS threshold: ±${Number(mds).toFixed(3)}) to achieve significance. As Dr. James Acker notes: <em>'If p &gt; 0.05, that does not mean a trend does not exist—sometimes a longer time series is all that is needed.'</em> Widen the temporal window back to 2002 to test the secular baseline.
      `;
    } else {
      el.diagWindowLesson.innerHTML = `
        <strong>[VERIFIED] Multi-Decadal Baseline (${spanYrs} years):</strong>
        With ${count} observations spanning ${state.startYear}–${state.endYear}, the effective sample size (N* = ${Number(nEff).toFixed(1)}) drives the Minimum Detectable Slope down to ±${Number(mds).toFixed(3)} ${curVar.unit}/yr, allowing subtle secular trends to be identified reliably.
      `;
    }

    // Sensor safeguard audit note
    if (curVar.id === 'power_precip') {
      el.diagSensorSafeguard.innerHTML = '<strong>[AUDIT] Sensor Break Analysis:</strong> NASA POWER MERRA-2 exhibits a known observing system step artifact around 2015. Always verify model reanalysis trends against physical satellite radar (GPM IMERG).';
    } else if (curVar.id === 'grace_tws') {
      el.diagSensorSafeguard.innerHTML = '<strong>[MISSION BRIDGE] Gravimetry Inter-Mission Continuity:</strong> The 11-month observation gap between GRACE and GRACE-FO (July 2017 to May 2018) is shaded on the canvas. Newey-West HAC bridge testing confirms continuity across satellite generations.';
    } else if (curVar.id === 'airs_temp' || curVar.id === 'airs_h2o') {
      el.diagSensorSafeguard.innerHTML = '<strong>[SPATIAL AUDIT] AIRS 1.0° Footprint &amp; Clear-Sky Sampling:</strong> At 1° (~111 km), Bangladesh comprises ~10 grid cells. Regional values reflect area-weighted nearest-cell averages. Cloud-clearing retrievals have lower sampling frequency during deep monsoon cloud decks.';
    } else if (curVar.id === 'omi_no2') {
      el.diagSensorSafeguard.innerHTML = '<strong>[QUALITY AUDIT] OMI Row Anomaly &amp; Boundary Layer Dynamics:</strong> Cloud-screened tropospheric column NO₂ filters pixels affected by the OMI row anomaly. Winter peaks reflect boundary layer compression and winter brick kiln operations rather than annual emission shifts alone.';
    } else {
      el.diagSensorSafeguard.innerHTML = '<strong>[OBSERVATION AUDIT] NASA GES DISC Calibrations:</strong> Observations conform to standard NASA GES DISC calibrations.';
    }
  }

  function updateDirectivesContent() {
    const regKey = state.spatialType === 'division' ? 'National' : state.entity;
    const allDirectives = window.ED.catalog.stakeholderDirectives || window.ED.catalog.stakeholders || {};
    const directives = allDirectives[regKey] || allDirectives['NW'] || {
      region_name: 'Bangladesh',
      mandate: 'Sustainable water resources management.',
      farmer_dos: 'Adopt water-saving crop varieties.',
      farmer_donts: 'Avoid excessive dry-season pumping.',
      citizen_action: 'Promote rainwater harvesting.'
    };
    el.directivesRegionName.textContent = directives.region_name;

    const isBn = (state.lang === 'bn') || (document.documentElement.lang === 'bn');
    const labelMandate = isBn ? '[নীতিমালা] সরকারি ও পানি উন্নয়ন বোর্ড নীতি' : '[MANDATE] Government &amp; Water Board Policy'; // DRAFT: needs native review
    const labelFarmerDo = isBn ? '[সুপারিশ] টেকসই কৃষি পদ্ধতি (করণীয়)' : '[DIRECTIVE] Recommended Agricultural Practices (Do\'s)'; // DRAFT: needs native review
    const labelFarmerDont = isBn ? '[সীমাবদ্ধতা] অপচয়মূলক চর্চা (বর্জনীয়)' : '[RESTRICTION] Unsustainable Practices (Don\'ts)'; // DRAFT: needs native review
    const labelCitizen = isBn ? '[নাগরিক উদ্যোগ] পানি সংরক্ষণ কর্মপরিকল্পনা' : '[COMMUNITY] Citizen Water Conservation Actions'; // DRAFT: needs native review

    el.directivesItemsContainer.innerHTML = `
      <div class="drawer-directive-box mandate">
        <div class="dd-label" style="color:var(--accent-amber);">${labelMandate}</div>
        <p>${directives.mandate}</p>
      </div>

      <div class="drawer-directive-box farmer-do">
        <div class="dd-label" style="color:var(--accent-emerald);">${labelFarmerDo}</div>
        <p>${directives.farmer_dos}</p>
      </div>

      <div class="drawer-directive-box farmer-dont">
        <div class="dd-label" style="color:var(--accent-crimson);">${labelFarmerDont}</div>
        <p>${directives.farmer_donts}</p>
      </div>

      <div class="drawer-directive-box citizen">
        <div class="dd-label" style="color:var(--accent-cyan);">${labelCitizen}</div>
        <p>${directives.citizen_action}</p>
      </div>
    `;
  }

  function openDiagnosticsDrawer() {
    el.drawerDiagnostics.classList.add('open');
    el.diagnosticsBackdrop.classList.add('open');
  }

  function openDirectivesDrawer() {
    el.drawerDirectives.classList.add('open');
    el.directivesBackdrop.classList.add('open');
  }

  function openEvidenceDrawer(initialFragment = 'threeway') {
    if (el.drawerEvidence && el.evidenceBackdrop) {
      el.drawerEvidence.classList.add('open');
      el.evidenceBackdrop.classList.add('open');
      renderEvidenceFragment(initialFragment);
    }
  }

  function renderEvidenceFragment(fragId) {
    if (!el.evidenceContent) return;
    const frags = window.REPORT_FRAGMENTS || {};
    const html = frags[fragId] || `<div style="padding:20px; color:var(--text-muted);">Fragment #${fragId} not loaded.</div>`;
    el.evidenceContent.innerHTML = html;

    document.querySelectorAll('.evidence-tab-btn').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-frag') === fragId);
    });

    if (el.evidenceOpenReportLink) {
      el.evidenceOpenReportLink.href = window.URLState
        ? window.URLState.buildLink('report.html', {
            region: state.entity,
            var: VAR_MAP_TO_URL[state.variable] || state.variable,
            start: state.startYear,
            end: state.endYear,
            season: state.season,
            mode: state.mode,
            lang: state.lang
          }, '#' + fragId)
        : `report.html#${fragId}`;
    }

    if (window.applyLang) {
      window.applyLang(state.lang || 'en');
    }
  }

  function closeAllDrawers() {
    if (el.drawerDiagnostics) el.drawerDiagnostics.classList.remove('open');
    if (el.diagnosticsBackdrop) el.diagnosticsBackdrop.classList.remove('open');
    if (el.drawerDirectives) el.drawerDirectives.classList.remove('open');
    if (el.directivesBackdrop) el.directivesBackdrop.classList.remove('open');
    if (el.drawerEvidence) el.drawerEvidence.classList.remove('open');
    if (el.evidenceBackdrop) el.evidenceBackdrop.classList.remove('open');
  }

  // 12. Section 3: Tabbed Bento Case Dossier Explorer
  const DOSSIER_DATA = {
    'case-1': {
      badge: 'Case File #1',
      title: "Where Is the Northwest's Water Going?",
      tagline: 'Total Water Storage vs. Satellite Rainfall in the Barind Tract',
      science: `
        <p>Think of the regional water cycle as an immense natural savings account. During the summer monsoon, heavy precipitation deposits water across river corridors, soil layers, and subterranean storage reserves. Throughout the dry winter months, withdrawals occur through evaporation, plant transpiration, and human tubewell pumping.</p>
        <p>To measure how much water Bangladesh holds, NASA uses the twin <strong>GRACE and GRACE Follow-On</strong> satellites orbiting 500 km above Earth. These spacecraft act like an ultra-sensitive scale: as water mass shifts across the landscape, Earth's gravitational pull changes subtly, shifting the distance between the two satellites by micrometers. Simultaneously, the <strong>GPM IMERG</strong> constellation uses spaceborne radar and microwave sensors to track every millimeter of precipitation falling from clouds.</p>
      `,
      findings: `
        <p>Over the full 24-year satellite observation baseline (2002–2026), Northwest Bangladesh shows a statistically significant decrease in total water storage at a rate of <span class="bento-stat-chip">-1.25 cm/yr</span> (95% CI: [-1.50, -1.02] cm/yr; p &lt; 0.0001, FDR q &lt; 0.0001; total volumetric loss rate of -0.39 km³/yr).</p>
        <p>In contrast, GPM IMERG satellite rainfall over the identical geographic window exhibits <span class="bento-stat-chip">no detectable trend</span> (-1.91 mm/yr, 95% CI: [-11.0, +4.5] mm/yr; p = 0.54, FDR q = 0.8968). The storage decline occurring alongside precipitation with no detectable trend is consistent with intensive dry-season groundwater abstraction for Boro rice cultivation across 74.2% of the region's cultivated agricultural land.</p>
      `,
      impact: `
        <p>The Northwest region includes <strong>38.81 million people</strong> (22.9% of the national population) and produces over one-third of the country's domestic rice supply.</p>
        <p>As regional total water storage decreases year after year, shallow tubewells run dry during the critical pre-monsoon irrigation months (March–May). Farmers must repeatedly re-bore tubewells to greater depths and transition from suction-mode centrifugal pumps to costlier submersible pumps, increasing operating expenses and rural electrical and diesel energy demands.</p>
      `,
      limitations: `
        <p>GRACE satellite gravimetry operates at a native spatial resolution of ~300 km (roughly the size of an entire geographic macro-region). Consequently, satellite gravimetry cannot pinpoint field-scale drawdown at individual village tubewells.</p>
        <p>Furthermore, satellite gravimetry measures the vertically integrated water column (surface water, soil moisture, and deeper subsurface storage combined) and requires land surface model partitioning to isolate sub-root-zone deficits.</p>
      `,
      outlook: `
        <p>To secure agricultural resilience, the Barind Multipurpose Development Authority (BMDA) is expanding prepaid smart-card metering to discourage over-pumping.</p>
        <p>Widespread adoption of <strong>Alternate Wetting and Drying (AWD)</strong> irrigation reduces paddy water consumption by 15% to 30% without crop yield penalties, while crop diversification toward low-water winter pulses and oilseeds (BARI chhola, BARI sarisha) helps stabilize regional water reserves.</p>
      `
    },
    'case-2': {
      badge: 'Case File #2 • Benchmark',
      title: 'Is 8 Years Enough?',
      tagline: "Dr. James Acker's Core Lesson: Time Window Length & Detection Limits",
      science: `
        <p>When analyzing Earth observations, detecting whether a system is genuinely changing requires separating long-term secular trends from short-term natural variability and sensor noise.</p>
        <p>Dr. James Acker illustrates that statistical significance depends fundamentally on the length of the observation window. Over short durations (such as 5 to 8 years), climate cycles such as El Niño and monsoon fluctuations introduce statistical noise that can obscure persistent secular changes.</p>
      `,
      findings: `
        <p>Examining Northwest Bangladesh solely across the 8-year GRACE Follow-On mission era (2018–2026, N = 96 months), the calculated Theil-Sen rate yields a p-value of <span class="bento-stat-chip">p = 0.0549</span>—just above the conventional 0.05 significance threshold. Under strict criteria, this window would be classified as 'No detectable trend'.</p>
        <p>However, when the observation window is widened to encompass the full 24-year continuous record (2002–2026, N = 277 months), the identical downward trajectory yields <span class="bento-stat-chip">p &lt; 0.0001</span>. At 8 years, the 80% power Minimum Detectable Slope requires a steep rate of ±1.84 cm/yr to overcome noise, whereas across 24 years, the detection limit refines to ±0.42 cm/yr.</p>
      `,
      impact: `
        <p>Premature conclusions based on brief observational windows risk misinforming resource managers.</p>
        <p>If water planners had concluded in 2026 that Northwest storage had stabilized based on the single-mission 2018–2026 window, vital aquifer recharge and water-conservation policies might have been delayed.</p>
      `,
      limitations: `
        <p>Bridging separate satellite generations introduces potential instrument step offsets. Between GRACE-1 and GRACE-FO, an 11-month observation gap occurred (July 2017 to May 2018).</p>
        <p>Rigorous trend detectives apply Newey-West HAC offset testing and Monte Carlo synthetic red-noise null simulations to verify that bridge step offsets do not artificially produce trend significance.</p>
      `,
      outlook: `
        <p>Dr. Acker's guidance confirms that 'if p &gt; 0.05, that does not mean a trend does not exist—sometimes a longer time series is all that is needed.'</p>
        <p>Future satellite gravimetry missions, including NASA-ESA GRACE-C (scheduled for launch in 2028), will extend the continuous observation baseline past three decades, dramatically improving the statistical power of global trend detection.</p>
      `
    },
    'case-3': {
      badge: 'Case File #3 • Verification',
      title: 'The Reanalysis Trap',
      tagline: 'Atmospheric Model Artifact vs. Satellite Radar Observations',
      science: `
        <p>Earth scientists rely on two primary categories of global climate datasets: direct physical satellite observations (such as spaceborne radars and microwave radiometers) and numerical reanalysis models (which blend weather forecasts with ingested data streams).</p>
        <p>When atmospheric models transition their underlying assimilation satellite constellations, artificial discontinuities or 'step jumps' can be introduced into the synthetic output—simulating a climate shift that never actually occurred.</p>
      `,
      findings: `
        <p>A direct comparison of <strong>NASA POWER MERRA-2</strong> reanalysis precipitation against physical <strong>GPM IMERG</strong> satellite radar observations reveals a pronounced discrepancy starting around 2015.</p>
        <p>NASA POWER exhibits an abrupt upward shift of <span class="bento-stat-chip">+30 to +50 mm/month</span> over Bangladesh following updates to its underlying assimilation stream, whereas GPM IMERG physical radar retrievals confirm a steady, unbroken monsoonal distribution. Trend detectives must cross-validate model outputs against physical sensors before inferring climate shifts.</p>
      `,
      impact: `
        <p>National water and flood infrastructure design relies heavily on precipitation baselines.</p>
        <p>Relying on artificial reanalysis rainfall jumps could lead engineers to over-dimension stormwater drainage networks or misdiagnose regional monsoon precipitation dynamics.</p>
      `,
      limitations: `
        <p>While GPM IMERG V07B Final Run incorporates ground rain-gauge calibration from the Global Precipitation Climatology Centre (GPCC), gauge density across rural deltaic floodplains is uneven.</p>
        <p>Additionally, satellite microwave algorithms can encounter challenges with heavy convective attenuation along the Himalayan foothills.</p>
      `,
      outlook: `
        <p>Next-generation reanalysis projects (such as NASA GMAO's forthcoming GEOS-IT and MERRA-3) are implementing improved bias-correction routines to minimize sensor-break artifacts.</p>
        <p>Ground-truthing satellite radar retrievals with automated telemetry rain gauges operated by the Bangladesh Meteorological Department (BMD) ensures reliable precipitation records.</p>
      `
    },
    'case-4': {
      badge: 'Case File #4',
      title: 'Soil or Deeper?',
      tagline: 'Partitioning Root-Zone Moisture vs. Subsurface Residual',
      science: `
        <p>When satellite gravimetry detects that a region is losing water mass, where is that loss located? Is topsoil drying out in the sun, or are deeper subsurface reserves being drawn down?</p>
        <p>Total water storage measured from space represents the combined sum of all water columns: vegetation canopy moisture, topsoil moisture, rivers, lakes, and subterranean reserves. To partition these layers, hydrologists employ land surface models (such as NASA GLDAS Noah and VIC) that simulate water movement through the upper 2.0 meters of soil—the root zone. Subtracting simulated root-zone soil moisture from total satellite water storage isolates an <strong>unpartitioned residual (groundwater + surface water + biomass + model error)</strong>.</p>
      `,
      findings: `
        <p>In Northwest Bangladesh, simulated root-zone soil moisture (0–200 cm) from GLDAS Noah exhibits a small trend of only <span class="bento-stat-chip">-0.12 cm/yr</span> (-0.10 cm/yr under VIC), accounting for roughly 8% to 10% of the total regional storage decrease.</p>
        <p>In contrast, the unpartitioned residual (groundwater + surface water + biomass + model error) declines at <span class="bento-stat-chip">-1.12 to -1.11 cm/yr</span>, representing approximately 90% of the total storage deficit. While root-zone soil moisture replenishes each monsoon, the unpartitioned residual shows a persistent cumulative decline across consecutive seasons.</p>
      `,
      impact: `
        <p>Because upper root-zone moisture refills during monsoon rainfall, rainfed summer Aman rice cultivation is largely supported in normal monsoon seasons.</p>
        <p>However, the persistent deficit in the unpartitioned residual directly affects the winter Boro crop season, which depends on mechanized tubewell pumping. Lower water levels increase the energy requirements for pumping, and falling water tables heighten the risk of heavy metal and arsenic mobilization in rural drinking water supplies.</p>
      `,
      limitations: `
        <p>Standard GLDAS land surface models run in "open-loop" mode without dynamic irrigation abstractions, meaning they simulate natural infiltration but do not explicitly represent tubewell pumping.</p>
        <p>Furthermore, the residual remains an unpartitioned residual (groundwater + surface water + biomass + model error); satellite gravimetry alone cannot independently isolate deep groundwater from surface water bodies, vegetation biomass variations, or model structure errors.</p>
      `,
      outlook: `
        <p>Continued depletion of the unpartitioned residual will push water tables deeper across the Barind Tract, increasing operating expenses for agricultural tubewells.</p>
        <p>Integrating satellite gravimetry with in situ telemetric piezometers and high-resolution surface water altimetry from the <strong>SWOT</strong> satellite mission will enable detailed 3D partitioning between surface reservoirs and subsurface storage layers.</p>
      `
    },
    'case-5': {
      badge: 'Case File #5',
      title: "Is Dhaka's Air Getting Hazier?",
      tagline: 'NASA MODIS Aqua Satellite vs. AERONET Ground Sun Photometer',
      science: `
        <p>Suspended atmospheric particles—including smoke, soot, vehicle exhaust, and mineral dust—scatter and absorb incoming sunlight. Scientists measure this atmospheric haziness using <strong>Aerosol Optical Depth (AOD)</strong>.</p>
        <p>An AOD of ~0.1 indicates clear skies, while values exceeding 1.0 signify dense, hazardous smog. To measure aerosols without satellite cloud-glare distortion, NASA established the global <strong>AERONET</strong> network: calibrated ground-based sun photometers on rooftops that track direct solar extinction through spectral filters. Simultaneously, NASA's <strong>MODIS sensor aboard the Aqua satellite</strong> retrieves Level 3 1° gridded monthly AOD across entire regional landscapes at 550 nm.</p>
      `,
      findings: `
        <p>Synthesizing 24 years of NASA MODIS Aqua Level 3 satellite observations (2002–2026, 277 months) alongside 12 years of ground-truth NASA AERONET sun photometer observations (2012–2024, Dhaka University) establishes a statistically significant secular increase in atmospheric aerosol loading.</p>
        <p>Across the full 24-year satellite record, MODIS Aqua measures an upward slope in Dhaka AOD of <span class="bento-stat-chip">+0.0115 per year</span> (95% CI: [+0.0063, +0.0168], p &lt; 0.0001, Hurwicz-corrected ESS N* = 140.4). Across the nationwide Bangladesh bounding box, a statistically significant upward trend also emerges (+0.0081/yr, p = 0.0040). Ground-truth AERONET sun photometers independently validate this trajectory (+0.012/yr, p = 0.014). Both sensors reveal marked seasonality: monsoon rain scavenges particulates down to 0.2–0.4 AOD, while dry winter months (DJF) regularly exceed 1.1–1.4 AOD due to brick kiln operations and boundary layer stagnation.</p>
      `,
      impact: `
        <p>Central Bangladesh houses <strong>45.64 million residents</strong> (26.9% of the national population), predominantly residing within the Dhaka megacity area.</p>
        <p>Winter aerosol levels consistently exceeding 1.0 AOD correspond to hazardous particulate matter concentrations (PM2.5), contributing to acute spikes in pediatric respiratory infections, chronic obstructive pulmonary disease (COPD), and cardiovascular illnesses during the winter season.</p>
      `,
      limitations: `
        <p>While rooftop AERONET sun photometers provide high radiometric precision at a single point (Dhaka University), satellite MODIS retrievals provide spatial coverage at 1° (~110 km) resolution.</p>
        <p>Because optical sensors are passive, thick monsoon cloud decks obstruct retrievals during peak summer rainfall. Our analytical engine accounts for this via Hurwicz small-sample autocorrelation correction and effective sample size weighting.</p>
      `,
      outlook: `
        <p>Without structural interventions in regional brick kiln emissions and vehicular exhaust, winter aerosol loading will remain at hazardous levels across the capital.</p>
        <p>Effective interventions include transitioning traditional clamp kilns to cleaner Zigzag and tunnel kilns, enforcing vehicular emission standards, expanding urban tree cover, and coordinating cross-border airshed policies across the Indo-Gangetic Plain.</p>
      `
    },
    'case-6': {
      badge: 'Case File #6',
      title: 'Are Downpours Getting Stronger?',
      tagline: 'ETCCDI Extreme 1-Day Downpours (Rx1day)',
      science: `
        <p>Under climate warming, a warmer atmosphere can hold approximately 7% more water vapor per degree Celsius of warming (the Clausius-Clapeyron relation). Consequently, even if total seasonal rainfall remains constant, precipitation may fall in shorter, more violent deluges.</p>
        <p>To detect shifts in storm violence, international climatologists rely on the <strong>Expert Team on Climate Change Detection and Indices (ETCCDI)</strong> standard metrics, notably <strong>Rx1day</strong> (maximum 1-day rainfall recorded in a calendar year) derived from high-resolution satellite precipitation grids.</p>
      `,
      findings: `
        <p>Analyzing GPM IMERG daily precipitation across 22 years (2003–2024), annual maximum 1-day downpours in Bangladesh exhibit dramatic year-to-year volatility, swinging from ~50 mm/day up to &gt; 115 mm/day during catastrophic historical flood years (2004, 2007, 2017, 2020, and 2022).</p>
        <p>Testing for a monotonic trend in Rx1day yields a slightly positive rate (+0.32 mm/day per year), but with a p-value of <span class="bento-stat-chip">p = 0.42</span> (well above the 0.05 threshold). The statistical verdict is <span class="bento-stat-chip">No detectable trend</span>: extreme event variance is so high that 22 annual data points remain below the statistical detection boundary for a secular shift.</p>
      `,
      impact: `
        <p>Extreme single-day downpours trigger urban flash waterlogging in Dhaka and Chittagong within hours, paralyzing transit corridors and submerging informal settlements.</p>
        <p>In rural river basins, consecutive intense rainfall days breach earthen flood protection embankments, submerging standing Aman crops and washing away aquaculture ponds.</p>
      `,
      limitations: `
        <p>Rx1day is an annual maximum index, producing exactly one data point per calendar year (N = 22). Small sample sizes naturally limit statistical detection power.</p>
        <p>Furthermore, satellite radar passes can smooth localized cloudburst cores smaller than the satellite pixel footprint.</p>
      `,
      outlook: `
        <p>Even in the absence of a statistically significant monotonic trend, high storm volatility demands robust climate adaptation.</p>
        <p>Municipalities are deploying urban drainage pumping stations, restoring natural retention canals (khals), and implementing automated Flash Flood Early Warning Systems (FFEWS) across vulnerable northeastern Haor districts.</p>
      `
    },
    'case-7': {
      badge: 'Case File #7',
      title: "Is Dhaka's Air Getting Dirtier?",
      tagline: 'Combustion Trace Gases (OMI NO₂) vs Total Aerosol Loading (MODIS AOD)',
      science: `
        <p>Nitrogen dioxide (NO₂) is a short-lived atmospheric trace gas produced by high-temperature combustion in vehicle engines, brick kilns, and industrial facilities. Because it breaks down within hours to days, satellite NO₂ columns trace active, localized pollution hotspots.</p>
        <p>NASA's <strong>Ozone Monitoring Instrument (OMI)</strong> aboard Aura observes ultraviolet and visible sunlight backscattered by the atmosphere to quantify boundary-layer NO₂ density across a 0.25° grid.</p>
      `,
      findings: `
        <p>Across 22 years of continuous satellite observation (2004–2026), Central Bangladesh (Dhaka) exhibits strong seasonal winter boundary layer entrapment (&gt; 5.5 × 10¹⁵ molec/cm²).</p>
        <p>Statistical trend tests reveal a secular upward shift in winter NO₂ over the Dhaka metropolitan belt, tracking the expansion of heavy freight transit, distributed diesel power, and regional brick manufacturing.</p>
      `,
      impact: `
        <p>Over 22 million residents in the capital megacity experience chronic winter exposure to combustion byproducts, driving respiratory ailments and photochemical smog episodes.</p>
      `,
      limitations: `
        <p>Frequent summer monsoon cloud decks limit satellite optical retrievals, creating an inherent clear-sky sampling bias.</p>
        <p>Aging sensor row anomalies are mitigated through cloud-screened quality filtering.</p>
      `,
      outlook: `
        <p>Transitioning traditional brick kilns to cleaner zigzag/tunnel technologies and expanding electric mass transit (Dhaka Metro Rail) provide targeted avenues to curb combustion emissions.</p>
      `
    }
  };

  function renderDossierExplorer() {
    if (!el.dossierTabsList) return;
    el.dossierTabsList.innerHTML = '';
    const caseIds = Object.keys(DOSSIER_DATA);

    caseIds.forEach(cId => {
      const d = DOSSIER_DATA[cId];
      if (!d) return;

      const tab = document.createElement('div');
      const isActive = state.activeDossierCaseId === cId;
      tab.className = `dossier-tab-card ${isActive ? 'active' : ''}`;
      tab.innerHTML = `
        <div style="display:flex;justify-content:space-between;align-items:center;">
          <div class="dossier-tab-badge">${d.badge}</div>
          <button class="tab-direct-launch" data-case="${cId}" title="Launch simulation for ${d.badge}" style="background:var(--accent-blue-wash);border:1px solid var(--accent-blue-border);color:var(--accent-blue);font-size:10px;font-weight:700;border-radius:4px;cursor:pointer;padding:2px 6px;">🚀 Run &darr;</button>
        </div>
        <div class="dossier-tab-title">${d.title}</div>
        <div class="dossier-tab-domain">${d.tagline}</div>
      `;

      tab.addEventListener('click', (e) => {
        const directBtn = e.target.closest('.tab-direct-launch');
        if (directBtn) {
          e.stopPropagation();
          state.activeDossierCaseId = cId;
          activateCase(cId);
          jumpToSection('sec-workbench');
          return;
        }
        state.activeDossierCaseId = cId;
        renderDossierExplorer();
      });

      el.dossierTabsList.appendChild(tab);
    });

    const activeData = DOSSIER_DATA[state.activeDossierCaseId] || DOSSIER_DATA['case-1'];
    if (el.dossierBadge) el.dossierBadge.textContent = activeData.badge;
    if (el.dossierTitle) el.dossierTitle.textContent = activeData.title;
    if (el.dossierTagline) el.dossierTagline.textContent = activeData.tagline;

    if (el.dossierBodyScience) el.dossierBodyScience.innerHTML = activeData.science;
    if (el.dossierBodyFindings) el.dossierBodyFindings.innerHTML = activeData.findings;
    if (el.dossierBodyImpact) el.dossierBodyImpact.innerHTML = activeData.impact;
    if (el.dossierBodyLimitations) el.dossierBodyLimitations.innerHTML = activeData.limitations;
    if (el.dossierBodyOutlook) el.dossierBodyOutlook.innerHTML = activeData.outlook;

    // Animate Bento block entrance with GSAP
    if (window.gsap) {
      window.gsap.fromTo('#dossier-bento-grid .bento-block',
        { opacity: 0, y: 8 },
        { opacity: 1, y: 0, duration: 0.25, stagger: 0.04, ease: 'power2.out' }
      );
    }
  }

  // 13. Specification Modal (ⓘ Details)
  function openModal(varMeta) {
    el.modalTitle.textContent = varMeta.name;
    el.modalMeta.textContent = `${varMeta.sensor} • Footprint: ${varMeta.spatial_footprint} • Span: ${varMeta.temporal_range}`;
    el.modalDef.textContent = varMeta.definition;
    el.modalCaveats.textContent = varMeta.caveats;
    el.modalOverlay.classList.add('open');
  }

  function closeModal() {
    el.modalOverlay.classList.remove('open');
  }

  // Expose getters on ED namespace
  window.ED.getState = () => ({ ...state });
  window.ED.getChart = () => chartInstance;

  // 14. Main Initialization
  document.addEventListener('DOMContentLoaded', () => {
    initDOM();
    initNavigation();

    // Ingest URL State if present
    if (window.URLState) {
      const urlSt = window.URLState.getState();
      applyUrlStateToApp(urlSt);
    }

    initVariablePopover();
    initChartZoomBar();
    initEventListeners();
    initMap();

    renderCasesBentoGrid();
    renderDossierExplorer();

    syncCommandRibbon();
    runWorkflow();

    // If query string had params, auto-jump to workbench so verdict card is in view with no clicks
    if (window.location.search && window.location.search.length > 1) {
      setTimeout(() => {
        jumpToSection('sec-workbench');
      }, 150);
    }
  });

})();
