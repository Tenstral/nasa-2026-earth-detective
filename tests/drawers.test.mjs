/**
 * tests/drawers.test.mjs
 * ======================
 * Comprehensive Acceptance Test Suite for the Three Slide-Over Drawers:
 *   A) Methodological Proof & In-Depth Audit (#evidenceDrawer)
 *   B) Statistical Rigor & Detection Power (#drawer-diagnostics)
 *   C) Regional Stakeholder Action Directives (#drawer-directives)
 */

import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REPO_ROOT = path.resolve(__dirname, '..');

// Helper to create a sandbox mimicking the browser environment
function createMockEnvironment() {
  const domElements = {};

  function makeElement(id) {
    return {
      id,
      innerHTML: '',
      textContent: '',
      style: {},
      classList: {
        classes: new Set(),
        add(c) { this.classes.add(c); },
        remove(c) { this.classes.delete(c); },
        contains(c) { return this.classes.has(c); }
      },
      querySelectorAll() { return []; },
      querySelector() { return null; }
    };
  }

  function getElementById(id) {
    if (!domElements[id]) {
      domElements[id] = makeElement(id);
    }
    return domElements[id];
  }

  const sandbox = {
    console,
    Math,
    Number,
    String,
    Boolean,
    Array,
    Object,
    RegExp,
    parseFloat,
    parseInt,
    isNaN,
    isFinite,
    document: {
      documentElement: { lang: 'en', getAttribute: () => 'scientist' },
      getElementById,
      querySelectorAll: () => [],
      querySelector: () => null
    }
  };
  sandbox.window = sandbox;

  // Load citations.js
  const citationsCode = fs.readFileSync(path.join(REPO_ROOT, 'assets/js/citations.js'), 'utf-8');
  vm.runInContext(citationsCode, vm.createContext(sandbox));

  // Load report_fragments.js
  const fragmentsCode = fs.readFileSync(path.join(REPO_ROOT, 'assets/js/report_fragments.js'), 'utf-8');
  vm.runInContext(fragmentsCode, sandbox);

  // Load catalog.js & map.js
  const catalogCode = fs.readFileSync(path.join(REPO_ROOT, 'data/catalog.js'), 'utf-8');
  vm.runInContext(catalogCode, sandbox);

  const mapCode = fs.readFileSync(path.join(REPO_ROOT, 'data/map.js'), 'utf-8');
  vm.runInContext(mapCode, sandbox);

  // Load DASHBOARD_DATA from index.html
  const indexHtml = fs.readFileSync(path.join(REPO_ROOT, 'index.html'), 'utf-8');
  const dashMatch = indexHtml.match(/const DASHBOARD_DATA = ([\s\S]*?);\s*<\/script>/);
  if (dashMatch) {
    sandbox.DASHBOARD_DATA = JSON.parse(dashMatch[1]);
  }

  // Load stats.js
  const statsCode = fs.readFileSync(path.join(REPO_ROOT, 'assets/js/stats.js'), 'utf-8');
  vm.runInContext(statsCode, sandbox);

  // Extract ensureMDS, SENSOR_AUDIT_REGISTER, updateDiagnosticsContent, updateDirectivesContent from app.js
  const appJsCode = fs.readFileSync(path.join(REPO_ROOT, 'assets/js/app.js'), 'utf-8');
  
  // Extract ensureMDS and SENSOR_AUDIT_REGISTER
  const emdsMatch = appJsCode.match(/function ensureMDS[\s\S]*?const SENSOR_AUDIT_REGISTER = \{[\s\S]*?\r?\n  \};\r?\n/);
  assert.ok(emdsMatch, 'Must find ensureMDS and SENSOR_AUDIT_REGISTER in app.js');
  vm.runInContext(emdsMatch[0], sandbox);

  // Extract updateDiagnosticsContent and updateDirectivesContent
  const diagMatch = appJsCode.match(/function updateDiagnosticsContent\([\s\S]*?\r?\n  function openDiagnosticsDrawer/);
  assert.ok(diagMatch, 'Must find drawer update functions in app.js');
  const drawerFuncsCode = diagMatch[0].replace(/function openDiagnosticsDrawer.*/, '');
  vm.runInContext(drawerFuncsCode, sandbox);

  return { sandbox, domElements, getElementById };
}

describe('Drawer A: Methodological Proof & In-Depth Audit (REPORT_FRAGMENTS)', () => {
  const { sandbox } = createMockEnvironment();

  test('REPORT_FRAGMENTS is defined on window with all 5 required tabs', () => {
    assert.ok(sandbox.window.REPORT_FRAGMENTS, 'window.REPORT_FRAGMENTS must exist');
    const requiredTabs = ['threeway', 'gldas', 'pairwise-differences', 'stakeholder-actions', 'limitations'];
    for (const tab of requiredTabs) {
      assert.ok(sandbox.window.REPORT_FRAGMENTS[tab], `Fragment '${tab}' must exist in REPORT_FRAGMENTS`);
    }
  });

  test('Each fragment has > 500 characters and contains at least one HTML table', () => {
    const tabs = ['threeway', 'gldas', 'pairwise-differences', 'stakeholder-actions', 'limitations'];
    for (const tab of tabs) {
      const html = sandbox.window.REPORT_FRAGMENTS[tab];
      assert.ok(html.length > 500, `Fragment '${tab}' length (${html.length}) must be > 500 characters`);
      assert.match(html, /<table[\s>]/, `Fragment '${tab}' must contain at least one <table>`);
      assert.doesNotMatch(html, /Fragment #[a-z0-9-]+ not loaded/i, `Fragment '${tab}' must not contain not loaded message`);
    }
  });

  test('Fragments use relative image paths and strip script tags', () => {
    const tabs = ['threeway', 'gldas', 'pairwise-differences', 'stakeholder-actions', 'limitations'];
    for (const tab of tabs) {
      const html = sandbox.window.REPORT_FRAGMENTS[tab];
      assert.doesNotMatch(html, /<script\b/i, `Fragment '${tab}' must not contain <script> tags`);
      assert.doesNotMatch(html, /on\w+="[^"]*"/i, `Fragment '${tab}' must not contain inline event handlers`);
      assert.doesNotMatch(html, /src=["']\/(?!\/)/, `Fragment '${tab}' must not contain root-relative image paths`);
    }
  });
});

describe('Numbers Cross-Check vs outputs/v3/full_record Golden Files', () => {
  test('Northwest TWS 24-year slope, CI, p-value match golden results exactly', () => {
    const csvContent = fs.readFileSync(path.join(REPO_ROOT, 'outputs/v3/full_record/results_all_windows.csv'), 'utf-8');
    const lines = csvContent.trim().split(/\r?\n/);
    const header = lines[0].split(',');
    
    // Find NW tws full_record row
    const nwRow = lines.slice(1).map(l => l.split(',')).find(r => 
      r[header.indexOf('window')] === 'full_record' &&
      r[header.indexOf('entity')] === 'NW' &&
      r[header.indexOf('variable')] === 'tws' &&
      r[header.indexOf('season')] === 'annual'
    );
    assert.ok(nwRow, 'NW tws full_record row must exist in results_all_windows.csv');
    
    const slope = parseFloat(nwRow[header.indexOf('slope')]);
    const ciLow = parseFloat(nwRow[header.indexOf('slope_ci_low')]);
    const ciHigh = parseFloat(nwRow[header.indexOf('slope_ci_high')]);
    const pVal = nwRow[header.indexOf('p_value')];
    
    // Check against expected values: -1.25 cm/yr, 95% CI [-1.50, -1.02], p < 0.0001
    assert.equal(slope.toFixed(2), '-1.25', 'NW TWS slope must be -1.25 cm/yr');
    assert.equal(ciLow.toFixed(2), '-1.50', 'NW TWS 95% CI lower bound must be -1.50');
    assert.equal(ciHigh.toFixed(2), '-1.02', 'NW TWS 95% CI upper bound must be -1.02');
    assert.ok(parseFloat(pVal) < 0.0001, 'NW TWS p-value must be < 0.0001');
  });

  test('Northwest IMERG precipitation slope and p-value match golden results', () => {
    const csvContent = fs.readFileSync(path.join(REPO_ROOT, 'outputs/v3/full_record/results_all_windows.csv'), 'utf-8');
    const lines = csvContent.trim().split(/\r?\n/);
    const header = lines[0].split(',');

    const nwImergRow = lines.slice(1).map(l => l.split(',')).find(r => 
      r[header.indexOf('window')] === 'full_record' &&
      r[header.indexOf('entity')] === 'NW' &&
      (r[header.indexOf('variable')] === 'imerg_precip' || r[header.indexOf('variable')] === 'precip') &&
      r[header.indexOf('season')] === 'annual'
    );
    assert.ok(nwImergRow, 'NW IMERG precipitation row must exist');

    const slope = parseFloat(nwImergRow[header.indexOf('slope')]);
    const pVal = parseFloat(nwImergRow[header.indexOf('p_value')]);

    assert.equal(slope.toFixed(2), '-1.91', 'NW IMERG slope must be -1.91 mm/yr');
    assert.equal(pVal.toFixed(2), '0.54', 'NW IMERG p-value must be 0.54');
  });

  test('Case-2 8-year GRACE-FO single mission era is borderline significant (p = 0.0549)', () => {
    const csvContent = fs.readFileSync(path.join(REPO_ROOT, 'outputs/v3/full_record/results_all_windows.csv'), 'utf-8');
    const lines = csvContent.trim().split(/\r?\n/);
    const header = lines[0].split(',');

    const case2Row = lines.slice(1).map(l => l.split(',')).find(r => 
      r[header.indexOf('window')] === 'grace_fo_era' &&
      r[header.indexOf('entity')] === 'NW' &&
      r[header.indexOf('variable')] === 'tws' &&
      r[header.indexOf('season')] === 'annual'
    );
    assert.ok(case2Row, 'Case-2 GRACE-FO NW row must exist');

    const pVal = parseFloat(case2Row[header.indexOf('p_value')]);
    assert.equal(pVal.toFixed(4), '0.0549', 'Case-2 p-value must be exactly 0.0549');
  });
});

describe('Drawer B: Statistical Rigor & Detection Power (#drawer-diagnostics)', () => {
  const { sandbox, domElements, getElementById } = createMockEnvironment();

  test('All 5 regions x 3 variables produce complete diagnostics with NO NaN, undefined, or ±0.000', () => {
    const regions = ['NW', 'NE', 'Central', 'SW', 'SE'];
    const variables = [
      { id: 'grace_tws', name: 'Total Water Storage (GRACE)', unit: 'cm' },
      { id: 'imerg_precip', name: 'Precipitation (GPM IMERG)', unit: 'mm' },
      { id: 'airs_temp', name: 'Surface Temperature (AIRS)', unit: '°C' }
    ];

    // Setup DOM elements expected by updateDiagnosticsContent
    sandbox.el = {
      diagStatsGrid: getElementById('diag-stats-grid'),
      diagWindowLesson: getElementById('diag-window-lesson'),
      diagSensorSafeguard: getElementById('diag-sensor-safeguard')
    };
    getElementById('diag-power-verdict-box');
    getElementById('diag-student-summary');

    for (const reg of regions) {
      for (const curVar of variables) {
        sandbox.state = {
          entity: reg,
          spatialType: 'region',
          variable: curVar.id,
          window: 'full_record',
          season: 'annual',
          startYear: 2002,
          endYear: 2026,
          lang: 'en'
        };

        // Query catalog precomputed result or mock
        const res = sandbox.DASHBOARD_DATA.results.find(r => 
          r.window === 'full_record' && 
          r.entity === reg && 
          (r.variable === curVar.id || (curVar.id === 'imerg_precip' && r.variable === 'precip') || (curVar.id === 'grace_tws' && r.variable === 'tws') || (curVar.id === 'airs_temp' && r.variable === 'temp')) &&
          r.season === 'annual'
        ) || {
          slope: -1.25,
          theil_sen_slope: -1.25,
          slope_ci_low: -1.50,
          slope_ci_high: -1.02,
          p_value: '< 0.0001',
          bh_fdr_q_value: '< 0.0001',
          s: -14200,
          z: -5.42,
          r1_detrended: 0.5663,
          gamma: 3.612,
          n_star: 71.2,
          mds_80_power: 0.320,
          primary_method: 'Calibrated ESS-MK',
          is_precomputed: true
        };

        const statResult = { ...res, is_precomputed: true };
        sandbox.ensureMDS(statResult, null, null, curVar);
        sandbox.updateDiagnosticsContent(statResult, 257, curVar);

        const renderedGrid = sandbox.el.diagStatsGrid.innerHTML;
        const renderedSafeguard = sandbox.el.diagSensorSafeguard.innerHTML;
        const renderedLesson = sandbox.el.diagWindowLesson.innerHTML;
        const renderedVerdict = getElementById('diag-power-verdict-box').innerHTML;

        const allRendered = `${renderedGrid} ${renderedSafeguard} ${renderedLesson} ${renderedVerdict}`;

        assert.doesNotMatch(allRendered, /\bNaN\b/, `${reg} ${curVar.id} diagnostics must not contain NaN`);
        assert.doesNotMatch(allRendered, /\bundefined\b/, `${reg} ${curVar.id} diagnostics must not contain undefined`);
        assert.doesNotMatch(allRendered, /precomputed windows only/i, `${reg} ${curVar.id} must not say 'precomputed windows only'`);
        assert.doesNotMatch(allRendered, /±0\.000\b/, `${reg} ${curVar.id} MDS must not be ±0.000`);
        assert.doesNotMatch(allRendered, /\+\/-0\.000\b/, `${reg} ${curVar.id} MDS must not be +/-0.000`);
      }
    }
  });

  test('Custom window (2010–2018) returns numeric stats and power analysis', () => {
    const curVar = { id: 'grace_tws', name: 'Total Water Storage (GRACE)', unit: 'cm' };
    sandbox.state = {
      entity: 'NW',
      spatialType: 'region',
      variable: 'grace_tws',
      window: 'custom',
      season: 'annual',
      startYear: 2010,
      endYear: 2018,
      lang: 'en'
    };

    // Synthesize 8 years of monthly points
    const points = [];
    const tYears = [];
    const yVals = [];
    for (let yr = 2010; yr <= 2018; yr++) {
      for (let mo = 1; mo <= 12; mo++) {
        const decYr = yr + (mo - 0.5) / 12;
        const val = -1.25 * (decYr - 2010) + 12 * Math.sin(2 * Math.PI * (mo / 12));
        tYears.push(decYr);
        yVals.push(val);
        points.push({
          year: yr,
          month: mo,
          ym: `${yr}-${mo < 10 ? '0' + mo : mo}`,
          decimal_year: decYr,
          value: val
        });
      }
    }

    const statResult = sandbox.Stats.analyze({
      var: 'grace_tws',
      region: 'NW',
      start: 2010,
      end: 2018,
      points: points,
      data: sandbox.DASHBOARD_DATA
    });

    sandbox.ensureMDS(statResult, tYears, yVals, curVar);
    sandbox.updateDiagnosticsContent(statResult, tYears.length, curVar);

    const renderedGrid = sandbox.el.diagStatsGrid.innerHTML;
    assert.doesNotMatch(renderedGrid, /\bNaN\b/, 'Custom window diagnostics must not contain NaN');
    assert.doesNotMatch(renderedGrid, /precomputed windows only/i, 'Custom window must not contain "precomputed windows only"');
    assert.ok(typeof statResult.gamma === 'number', 'Custom window gamma must be numeric');
    assert.ok(typeof statResult.r1_detrended === 'number', 'Custom window r1_detrended must be numeric');
    assert.ok(typeof statResult.n_star === 'number', 'Custom window n_star must be numeric');
    assert.ok(statResult.mds_80_power > 0, 'Custom window MDS must be positive');
  });

  test('Short observation window with borderline p-value triggers [UNDERPOWERED] verdict', () => {
    const curVar = { id: 'grace_tws', name: 'Total Water Storage (GRACE)', unit: 'cm' };
    sandbox.state = {
      entity: 'NW',
      spatialType: 'region',
      variable: 'grace_tws',
      window: 'grace_fo_era',
      season: 'annual',
      startYear: 2018,
      endYear: 2026,
      lang: 'en'
    };

    // Case-2: 8-yr GRACE-FO with slope = -0.92, p = 0.0549, MDS = 1.74 cm/yr
    const case2Stat = {
      theil_sen_slope: -0.92,
      slope: -0.92,
      slope_ci_low: -1.95,
      slope_ci_high: 0.12,
      p_value: 0.0549,
      p_formatted: '0.0549',
      bh_fdr_q_value: 0.0549,
      s: -310,
      z: -1.92,
      r1_detrended: 0.421,
      gamma: 2.14,
      n_star: 44.8,
      mds_80_power: 1.74,
      primary_method: 'Calibrated ESS-MK',
      is_precomputed: true
    };

    sandbox.updateDiagnosticsContent(case2Stat, 96, curVar);
    const powerVerdict = getElementById('diag-power-verdict-box').innerHTML;
    assert.match(powerVerdict, /\[UNDERPOWERED\]/i, 'Case-2 must trigger [UNDERPOWERED] verdict tag');
    assert.match(powerVerdict, /inconclusive\s*\(underpowered\)/i, 'Case-2 verdict must say inconclusive (underpowered)');
  });

  test('Per-variable sensor audit exists for every catalog variable', () => {
    const vars = sandbox.ED.catalog.variables;
    assert.ok(Array.isArray(vars) && vars.length >= 10, 'Catalog must contain variables');
    for (const v of vars) {
      sandbox.state = { entity: 'NW', spatialType: 'region', variable: v.id, startYear: 2002, endYear: 2026, lang: 'en' };
      const dummyStat = { slope: 0.1, p_value: 0.1, p_formatted: '0.1000', mds_80_power: 0.25 };
      sandbox.updateDiagnosticsContent(dummyStat, 100, v);
      const safeguardHtml = sandbox.el.diagSensorSafeguard.innerHTML;
      assert.ok(safeguardHtml.length > 50, `Variable ${v.id} must render detailed sensor safeguard audit`);
      assert.doesNotMatch(safeguardHtml, /undefined/i, `Safeguard for ${v.id} must not contain undefined`);
    }
  });
});

describe('Drawer C: Regional Stakeholder Action Directives (#drawer-directives)', () => {
  const { sandbox, getElementById } = createMockEnvironment();

  test('Directives render all 6 required fields in order for each region', () => {
    sandbox.el = {
      directivesRegionName: getElementById('directives-region-name'),
      directivesItemsContainer: getElementById('directives-items-container')
    };

    const regions = ['NW', 'NE', 'Central', 'SW', 'SE'];
    for (const reg of regions) {
      sandbox.state = {
        entity: reg,
        spatialType: 'region',
        variable: 'grace_tws',
        window: 'full_record',
        season: 'annual',
        startYear: 2002,
        endYear: 2026,
        lang: 'en'
      };

      sandbox.updateDirectivesContent();
      const html = sandbox.el.directivesItemsContainer.innerHTML;

      assert.match(html, /satellite-metric/, `${reg} must render satellite_metric block`);
      assert.match(html, /historical-context/, `${reg} must render historical_context block`);
      assert.match(html, /mandate/, `${reg} must render mandate block`);
      assert.match(html, /farmer-do/, `${reg} must render farmer_dos block`);
      assert.match(html, /farmer-dont/, `${reg} must render farmer_donts block`);
      assert.match(html, /citizen/, `${reg} must render citizen_action block`);
      assert.match(html, /directive-basis/, `${reg} must render directive-basis footer`);

      // Verify citation tags are included
      assert.match(html, /class="citation-badge verified"/, `${reg} must render verified citation badges`);
    }
  });

  test('Division selection correctly maps to parent region and displays division + region header', () => {
    sandbox.el = {
      directivesRegionName: getElementById('directives-region-name'),
      directivesItemsContainer: getElementById('directives-items-container')
    };

    const divisions = [
      { name: 'Rajshahi', expectedReg: 'Northwest' },
      { name: 'Rangpur', expectedReg: 'Northwest' },
      { name: 'Sylhet', expectedReg: 'Northeast' },
      { name: 'Dhaka', expectedReg: 'Central' },
      { name: 'Khulna', expectedReg: 'Southwest' },
      { name: 'Barishal', expectedReg: 'Southwest' },
      { name: 'Chattogram', expectedReg: 'Southeast' }
    ];

    for (const div of divisions) {
      sandbox.state = {
        entity: div.name,
        spatialType: 'division',
        variable: 'grace_tws',
        window: 'full_record',
        season: 'annual',
        startYear: 2002,
        endYear: 2026,
        lang: 'en'
      };

      sandbox.updateDirectivesContent();
      const headerText = sandbox.el.directivesRegionName.textContent;
      assert.match(headerText, new RegExp(div.name), `Header must contain division name ${div.name}`);
      assert.match(headerText, new RegExp(div.expectedReg), `Header must contain parent region ${div.expectedReg}`);
      
      const html = sandbox.el.directivesItemsContainer.innerHTML;
      assert.match(html, /directive-basis/, `Division ${div.name} must render directive basis footer`);
    }
  });

  test('Unknown entity shows explicit empty state rather than silent fallback', () => {
    sandbox.el = {
      directivesRegionName: getElementById('directives-region-name'),
      directivesItemsContainer: getElementById('directives-items-container')
    };

    sandbox.state = {
      entity: 'UnknownZone99',
      spatialType: 'region',
      variable: 'grace_tws',
      window: 'full_record',
      season: 'annual',
      startYear: 2002,
      endYear: 2026,
      lang: 'en'
    };

    sandbox.updateDirectivesContent();
    const html = sandbox.el.directivesItemsContainer.innerHTML;
    assert.match(html, /No directive found/i, 'Unknown entity must show explicit no directive message');
    assert.doesNotMatch(html, /Barind Tract/i, 'Unknown entity must NOT fall back to Barind / Northwest content');
  });

  test('Southwest and Southeast directives accurately state storage stability / no detectable trend', () => {
    const directivesCatalog = sandbox.ED.catalog.stakeholderDirectives;
    
    // SW check
    const swMetric = directivesCatalog.SW.satellite_metric;
    assert.match(swMetric, /no detectable trend/i, 'SW satellite metric must state no detectable trend');
    assert.doesNotMatch(swMetric, /\bdecline\b/i, 'SW must not claim secular decline');

    // SE check
    const seMetric = directivesCatalog.SE.satellite_metric;
    assert.match(seMetric, /no detectable trend/i, 'SE satellite metric must state no detectable trend');
    assert.doesNotMatch(seMetric, /\bdecline\b/i, 'SE must not claim secular decline');
  });
});
