/**
 * NASA Space Apps 2026 - Trend Detective
 * assets/js/stats.js
 * =====================================
 * Browser-grade calibrated statistical engine for time-series trend analysis:
 *   1. Calendar-month climatology deseasonalization
 *   2. Theil-Sen robust slope estimator (median pairwise rate)
 *   3. Effective-Sample-Size (ESS) Mann-Kendall test with Hurwicz bias-corrected
 *      detrended residual lag-1 autocorrelation (PRIMARY significance test)
 *   4. Exact duality-aligned 95% Theil-Sen confidence intervals with ESS rank bounds
 *   5. Scientifically valid seasonal aggregation (one observation per year)
 *   6. Analytic 80% power Minimum Detectable Slope (MDS) approximation
 *   7. Theil-Sen regression line evaluation
 *
 * Universal Module Definition (UMD) - runs in Node.js (node --test) and Browser.
 */

(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.Stats = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  /**
   * Complementary error function erfc(x) with double-precision Chebyshev rational fit.
   * Max error < 1.2e-7.
   */
  function erfc(x) {
    if (x < 0) return 2.0 - erfc(-x);
    if (x === 0) return 1.0;
    const z = Math.abs(x);
    const t = 1.0 / (1.0 + 0.5 * z);
    const ans = t * Math.exp(-z * z - 1.26551223 + t * (1.00002368 + t * (0.37409196 + t * (0.09678418 +
      t * (-0.18628806 + t * (0.27886807 + t * (-1.13520398 + t * (1.48851587 +
      t * (-0.82215223 + t * 0.17087277)))))))));
    return ans;
  }

  /**
   * Two-sided standard normal survival probability: p = 2 * (1 - Phi(|z|)).
   */
  function normalSurvival2Sided(z) {
    if (isNaN(z) || z === 0) return 1.0;
    const sf = 0.5 * erfc(Math.abs(z) / Math.SQRT2);
    return Math.min(1.0, Math.max(0.0, 2.0 * sf));
  }

  /**
   * Subtracts per-calendar-month mean across valid observations.
   * @param {Array<number>} months - 1-based calendar month (1..12) for each point
   * @param {Array<number>} values - observation values (may contain null / NaN)
   * @returns {Array<number>} deseasonalized anomalies
   */
  function deseasonalize(months, values) {
    const sums = new Array(13).fill(0);
    const counts = new Array(13).fill(0);

    for (let i = 0; i < values.length; i++) {
      const v = values[i];
      const m = months[i];
      if (v !== null && !isNaN(v) && m >= 1 && m <= 12) {
        sums[m] += v;
        counts[m] += 1;
      }
    }

    const means = new Array(13).fill(0);
    for (let m = 1; m <= 12; m++) {
      means[m] = counts[m] > 0 ? sums[m] / counts[m] : 0;
    }

    const out = new Array(values.length);
    for (let i = 0; i < values.length; i++) {
      const v = values[i];
      const m = months[i];
      if (v !== null && !isNaN(v) && m >= 1 && m <= 12) {
        out[i] = v - means[m];
      } else {
        out[i] = NaN;
      }
    }
    return out;
  }

  /**
   * Calibrated Effective-Sample-Size Mann-Kendall test with duality-aligned Theil-Sen 95% CIs.
   * Direct parity with Python v3/trend_engine.py:run_ess_mann_kendall.
   *
   * @param {Array<number>} tYears - decimal years (e.g., 2002.292)
   * @param {Array<number>} yValues - observation anomalies
   * @param {number} alpha - significance level (default 0.05)
   * @returns {object} { slope, ci_low, ci_high, p_value, z, s, gamma, r1_detrended, n_star, n }
   */
  function essMannKendall(tYears, yValues, alpha = 0.05) {
    // 1. Filter valid pairs
    const validT = [];
    const validY = [];
    for (let i = 0; i < yValues.length; i++) {
      const y = yValues[i];
      const t = tYears[i];
      if (y !== null && !isNaN(y) && t !== null && !isNaN(t)) {
        validT.push(t);
        validY.push(y);
      }
    }

    const n = validY.length;
    if (n < 10) {
      return {
        error: `Too few valid points for trend analysis: n=${n} (minimum 10 required)`,
        n: n,
        slope: NaN,
        ci_low: NaN,
        ci_high: NaN,
        p_value: NaN
      };
    }

    // 2. Pairwise slopes and Kendall S
    const slopes = [];
    let s = 0;

    for (let i = 0; i < n; i++) {
      const yi = validY[i];
      const ti = validT[i];
      for (let j = i + 1; j < n; j++) {
        const yj = validY[j];
        const tj = validT[j];
        const dy = yj - yi;
        const dt = tj - ti;

        slopes.push(dy / dt);

        if (dy > 0) s += 1;
        else if (dy < 0) s -= 1;
      }
    }

    slopes.sort((a, b) => a - b);
    const nPairs = slopes.length;
    const mid = Math.floor(nPairs / 2);
    const slopeMed = (nPairs % 2 === 1) ? slopes[mid] : (slopes[mid - 1] + slopes[mid]) / 2.0;

    // 3. Detrended residual lag-1 autocorrelation with Hurwicz small-sample bias correction
    const resid = new Array(n);
    for (let i = 0; i < n; i++) {
      resid[i] = validY[i] - slopeMed * validT[i];
    }

    const x = resid.slice(0, n - 1);
    const y = resid.slice(1, n);
    const m = n - 1;
    let sumX = 0, sumY = 0;
    for (let i = 0; i < m; i++) {
      sumX += x[i];
      sumY += y[i];
    }
    const meanX = sumX / m;
    const meanY = sumY / m;

    let sxx = 0, syy = 0, sxy = 0;
    for (let i = 0; i < m; i++) {
      const dx = x[i] - meanX;
      const dy = y[i] - meanY;
      sxx += dx * dx;
      syy += dy * dy;
      sxy += dx * dy;
    }

    const r1 = (sxx > 0 && syy > 0) ? (sxy / Math.sqrt(sxx * syy)) : 0.0;

    let gamma = 1.0;
    let r1Used = 0.0;
    if (!isNaN(r1) && r1 > 0.0) {
      const r1Bc = r1 + (1.0 + 4.0 * r1) / n;
      r1Used = Math.min(0.85, Math.max(0.0, r1Bc));
      gamma = (1.0 + r1Used) / (1.0 - r1Used);
    }

    // 4. Corrected MK variance
    const vS0 = (n * (n - 1) * (2 * n + 5)) / 18.0;
    const vSCorr = vS0 * gamma;

    // 5. Continuity-corrected Z and p-value
    let z = 0.0;
    if (s > 0) {
      z = (s - 1.0) / Math.sqrt(vSCorr);
    } else if (s < 0) {
      z = (s + 1.0) / Math.sqrt(vSCorr);
    }

    const pValue = normalSurvival2Sided(z);

    // 6. Duality-aligned Theil-Sen CI using corrected rank bounds
    const zCrit = 1.959963984540054; // stats.norm.ppf(0.975)
    const cAlpha = zCrit * Math.sqrt(vSCorr);
    let kLow = Math.floor((nPairs - cAlpha) / 2.0);
    let kHigh = Math.ceil((nPairs + cAlpha) / 2.0);
    kLow = Math.max(0, Math.min(nPairs - 1, kLow));
    kHigh = Math.max(0, Math.min(nPairs - 1, kHigh));

    const ciLow = slopes[kLow];
    const ciHigh = slopes[kHigh];

    return {
      slope: slopeMed,
      ci_low: ciLow,
      ci_high: ciHigh,
      p_value: pValue,
      z: z,
      s: s,
      gamma: Number(gamma.toFixed(3)),
      r1_detrended: Number(r1Used.toFixed(4)),
      n_star: Number((n / gamma).toFixed(1)),
      n: n
    };
  }

  /**
   * Scientifically valid seasonal aggregation:
   * Compresses monthly observations into ONE observation per calendar year.
   *
   * @param {Array<{ym: string, year: number, month: number, value: number}>} records
   * @param {string} seasonKey - 'annual' | 'monsoon' | 'winter' | 'pre_monsoon' | 'post_monsoon'
   * @param {string} kind - 'mean' (state variables) | 'sum' (rainfall totals)
   * @returns {Array<{year: number, decimal_year: number, value: number}>}
   */
  function seasonalAggregate(records, seasonKey, kind = 'mean') {
    // Define season months and completeness thresholds
    // Winter: Dec (year-1), Jan (year), Feb (year)
    const seasonDefs = {
      annual: { months: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], minMonths: 10, offsetDec: false },
      monsoon: { months: [6, 7, 8, 9], minMonths: 3, offsetDec: false }, // JJAS
      winter: { months: [12, 1, 2], minMonths: 3, offsetDec: true },      // DJF
      pre_monsoon: { months: [3, 4, 5], minMonths: 3, offsetDec: false }, // MAM
      post_monsoon: { months: [10, 11], minMonths: 2, offsetDec: false }   // ON
    };

    const def = seasonDefs[seasonKey] || seasonDefs.annual;

    // Group records by target season year
    const byYear = new Map();

    for (let i = 0; i < records.length; i++) {
      const r = records[i];
      if (r.value === null || isNaN(r.value)) continue;

      let targetYear = r.year;
      if (def.offsetDec && r.month === 12) {
        targetYear = r.year + 1; // Dec belongs to following year's winter
      }

      if (def.months.includes(r.month)) {
        if (!byYear.has(targetYear)) {
          byYear.set(targetYear, []);
        }
        byYear.get(targetYear).push(r);
      }
    }

    const out = [];
    const sortedYears = Array.from(byYear.keys()).sort((a, b) => a - b);

    for (const yr of sortedYears) {
      const items = byYear.get(yr);
      const uniqueMonths = new Set(items.map(x => x.month)).size;

      if (uniqueMonths >= def.minMonths) {
        let aggVal;
        if (kind === 'sum') {
          // If summing rainfall, require complete coverage so totals aren't under-reported
          if (uniqueMonths < def.months.length) continue;
          aggVal = items.reduce((acc, curr) => acc + curr.value, 0);
        } else {
          aggVal = items.reduce((acc, curr) => acc + curr.value, 0) / items.length;
        }

        out.push({
          year: yr,
          decimal_year: yr + 0.5,
          value: Number(aggVal.toFixed(4))
        });
      }
    }

    return out;
  }

  /**
   * Analytic approximation for Minimum Detectable Slope (MDS) at 80% power (alpha=0.05).
   * MDS approx (z_0.975 + z_0.80) * (sigma_resid / sqrt(SS_t)) * sqrt(gamma)
   */
  function approxMDS(tYears, yValues, slope, gamma = 1.0) {
    const validT = [];
    const validY = [];
    for (let i = 0; i < yValues.length; i++) {
      const y = yValues[i];
      const t = tYears[i];
      if (y !== null && !isNaN(y) && t !== null && !isNaN(t)) {
        validT.push(t);
        validY.push(y);
      }
    }
    const n = validY.length;
    if (n < 5) return null;

    // Calculate Theil-Sen intercept: median(y - slope * t)
    const rawIntercepts = [];
    for (let i = 0; i < n; i++) {
      rawIntercepts.push(validY[i] - slope * validT[i]);
    }
    rawIntercepts.sort((a, b) => a - b);
    const midIdx = Math.floor(n / 2);
    const intercept = (n % 2 !== 0)
      ? rawIntercepts[midIdx]
      : 0.5 * (rawIntercepts[midIdx - 1] + rawIntercepts[midIdx]);

    let meanT = 0;
    for (let i = 0; i < n; i++) meanT += validT[i];
    meanT /= n;

    let ssT = 0;
    let ssResid = 0;
    for (let i = 0; i < n; i++) {
      const dt = validT[i] - meanT;
      ssT += dt * dt;
      const resid = validY[i] - (intercept + slope * validT[i]);
      ssResid += resid * resid;
    }

    const sigmaE = Math.sqrt(ssResid / Math.max(1, n - 2));
    const zCrit = 1.959964;
    const zPower80 = 0.841621;
    const mds = (zCrit + zPower80) * (sigmaE / Math.sqrt(ssT)) * Math.sqrt(gamma);
    return Number(mds.toFixed(3));
  }

  /**
   * Computes points for the Theil-Sen regression line through (median(t), median(y)).
   */
  function calcTrendLine(tYears, yValues, slope) {
    const validT = [];
    const validY = [];
    for (let i = 0; i < yValues.length; i++) {
      const y = yValues[i];
      const t = tYears[i];
      if (y !== null && !isNaN(y) && t !== null && !isNaN(t)) {
        validT.push(t);
        validY.push(y);
      }
    }
    const n = validY.length;
    if (n === 0 || isNaN(slope)) return [];

    validT.sort((a, b) => a - b);
    validY.sort((a, b) => a - b);
    const mid = Math.floor(n / 2);
    const medT = (n % 2 === 1) ? validT[mid] : (validT[mid - 1] + validT[mid]) / 2.0;
    const medY = (n % 2 === 1) ? validY[mid] : (validY[mid - 1] + validY[mid]) / 2.0;

    return validT.map(t => ({
      t: t,
      y: medY + slope * (t - medT)
    }));
  }

  /**
   * Universal client-side analyze({var, region, start, end, season, data})
   * Reads DASHBOARD_DATA (or window.ED series) and computes:
   *   - n (sample count)
   *   - slope (linear OLS slope)
   *   - theil_sen_slope (median pairwise rate)
   *   - p_value (Mann-Kendall p-value)
   *   - slope_ci_low, slope_ci_high (95% CI)
   *   - If window matches a precomputed window (full_record, grace_era, grace_fo_era, recent_2020),
   *     reads advanced diagnostics (gamma, r1_detrended, n_star, bh_fdr_q_value, verdict)
   *     from precomputed results data.
   *   - For custom windows, sets advanced diagnostics to "precomputed windows only".
   */
  function analyze(params) {
    const opts = params || {};
    let varId = String(opts.var || opts.variable || 'tws').toLowerCase();
    const canonicalMap = {
      'tws': 'tws',
      'grace_tws': 'tws',
      'grace_tws_cm': 'tws',
      'imerg': 'imerg',
      'imerg_precip': 'imerg',
      'imerg_precip_mm': 'imerg',
      'precip': 'imerg',
      'power': 'power',
      'power_precip': 'power',
      'power_precip_mm': 'power',
      'noah_sms': 'noah_sms',
      'noah_sms_anom': 'noah_sms',
      'noah_sms_anom_cm': 'noah_sms',
      'vic_sms': 'vic_sms',
      'vic_sms_anom': 'vic_sms',
      'vic_sms_anom_cm': 'vic_sms',
      'residual': 'residual',
      'subsurface_residual': 'residual',
      'residual_mid': 'residual',
      'rx1day': 'rx1day',
      'extreme_rx1day': 'rx1day',
      'aod': 'aod',
      'modis_aod': 'aod',
      'aeronet_aod': 'aod'
    };
    varId = canonicalMap[varId] || varId;

    let region = String(opts.region || 'NW');
    let start = opts.start !== undefined && opts.start !== null ? parseInt(opts.start, 10) : 2002;
    let end = opts.end !== undefined && opts.end !== null ? parseInt(opts.end, 10) : 2026;
    if (isNaN(start)) start = 2002;
    if (isNaN(end)) end = 2026;
    if (start > end) { const tmp = start; start = end; end = tmp; }

    let season = String(opts.season || 'annual').toLowerCase();
    if (!['annual', 'monsoon', 'dry'].includes(season)) season = 'annual';

    const db = opts.data || (typeof window !== 'undefined' ? window.DASHBOARD_DATA : null);
    const ed = typeof window !== 'undefined' ? window.ED : null;

    // 1. Extract raw points
    let points = [];
    if (opts.points && Array.isArray(opts.points)) {
      points = opts.points;
    } else {
      let series = null;
      let valProp = 'tws';

      if (varId === 'tws') {
        series = (db && db.reg_monthly && db.reg_monthly[region]) ||
                 (db && db.div_monthly && db.div_monthly[region]) ||
                 (ed && ed.seriesRegions && ed.seriesRegions[region]) ||
                 (ed && ed.seriesDivisions && ed.seriesDivisions[region]);
        valProp = 'tws';
      } else if (varId === 'imerg') {
        series = (db && db.reg_monthly && db.reg_monthly[region]) ||
                 (db && db.div_monthly && db.div_monthly[region]) ||
                 (ed && ed.seriesRegions && ed.seriesRegions[region]) ||
                 (ed && ed.seriesDivisions && ed.seriesDivisions[region]);
        valProp = series && series.imerg ? 'imerg' : 'precip';
      } else if (varId === 'power') {
        series = (db && db.reg_monthly && db.reg_monthly[region]) ||
                 (ed && ed.seriesRegions && ed.seriesRegions[region]);
        valProp = 'power';
      } else if (varId === 'noah_sms') {
        series = (db && db.part_series && db.part_series[region]) ||
                 (ed && ed.seriesRegions && ed.seriesRegions[region]);
        valProp = 'noah_sms';
      } else if (varId === 'vic_sms') {
        series = (db && db.part_series && db.part_series[region]) ||
                 (ed && ed.seriesRegions && ed.seriesRegions[region]);
        valProp = 'vic_sms';
      } else if (varId === 'residual') {
        series = (db && db.part_series && db.part_series[region]) ||
                 (ed && ed.seriesRegions && ed.seriesRegions[region]);
        valProp = (series && series.residual_mid) ? 'residual_mid' : (series && series.noah_res ? 'noah_res' : 'subsurface');
      } else if (varId === 'rx1day') {
        const extList = (ed && ed.seriesExtremes && ed.seriesExtremes[region]) || [];
        points = extList.map(item => ({
          ym: `${item.year}-07`,
          year: item.year,
          month: 7,
          decimal_year: item.year + 0.5,
          value: item.rx1day_mm
        }));
      } else if (varId === 'aod') {
        const aodList = (ed && ed.seriesAOD && (ed.seriesAOD.bangladesh_modis || ed.seriesAOD.dhaka_modis)) || [];
        points = aodList.map(item => ({
          ym: item.ym,
          year: item.year,
          month: item.month,
          decimal_year: item.decimal_year,
          value: item.aod_550
        }));
      }

      if (series && series.ym && series[valProp]) {
        points = series.ym.map((ymStr, idx) => {
          const yr = parseInt(ymStr.slice(0, 4), 10);
          const mo = parseInt(ymStr.slice(5, 7), 10);
          const decYr = series.t ? series.t[idx] : (yr + (mo - 0.5) / 12);
          return {
            ym: ymStr,
            year: yr,
            month: mo,
            decimal_year: decYr,
            value: series[valProp][idx]
          };
        });
      }
    }

    // 2. Filter date window
    const inWindow = points.filter(d => d.year >= start && d.year <= end);

    // 3. Seasonal processing
    let processed = [];
    if (season !== 'annual') {
      const kind = (varId === 'imerg' || varId === 'power') ? 'sum' : 'mean';
      processed = seasonalAggregate(inWindow, season, kind);
    } else {
      const months = inWindow.map(d => d.month);
      const vals = inWindow.map(d => d.value);
      const des = deseasonalize(months, vals);
      processed = inWindow.map((d, i) => ({
        ym: d.ym,
        year: d.year,
        month: d.month,
        decimal_year: d.decimal_year,
        value: des[i]
      })).filter(d => d.value !== null && !isNaN(d.value));
    }

    // 4. Compute simple live statistics
    const validT = [];
    const validY = [];
    for (let i = 0; i < processed.length; i++) {
      const v = processed[i].value;
      const t = processed[i].decimal_year;
      if (v !== null && !isNaN(v) && t !== null && !isNaN(t)) {
        validT.push(t);
        validY.push(v);
      }
    }

    const n = validY.length;
    if (n < 10) {
      return {
        error: `n too small (n=${n}, minimum 10 required)`,
        n: n,
        slope: null,
        theil_sen_slope: null,
        slope_ci_low: null,
        slope_ci_high: null,
        p_value: null,
        p_formatted: 'n too small',
        z: null,
        s: null,
        is_precomputed: false,
        window: 'custom',
        verdict: 'n too small (< 10)',
        bh_fdr_q_value: null,
        gamma: null,
        r1_detrended: null,
        n_star: null,
        primary_method: 'Live Calibrated ESS-MK',
        diagnostics_note: 'Sample size n < 10 is too small for statistical trend estimation'
      };
    }

    // Linear OLS slope
    let sumT = 0, sumY = 0;
    for (let i = 0; i < n; i++) { sumT += validT[i]; sumY += validY[i]; }
    const meanT = sumT / n;
    const meanY = sumY / n;
    let cov = 0, varT = 0;
    for (let i = 0; i < n; i++) {
      const dt = validT[i] - meanT;
      cov += dt * (validY[i] - meanY);
      varT += dt * dt;
    }
    const olsSlope = varT > 0 ? cov / varT : 0;

    // Theil-Sen slope & Kendall S
    const slopes = [];
    let s = 0;
    for (let i = 0; i < n; i++) {
      for (let j = i + 1; j < n; j++) {
        const dy = validY[j] - validY[i];
        const dt = validT[j] - validT[i];
        slopes.push(dy / dt);
        if (dy > 0) s += 1;
        else if (dy < 0) s -= 1;
      }
    }
    slopes.sort((a, b) => a - b);
    const nPairs = slopes.length;
    const mid = Math.floor(nPairs / 2);
    const theilSenSlope = (nPairs % 2 === 1) ? slopes[mid] : (slopes[mid - 1] + slopes[mid]) / 2.0;

    // Simple Mann-Kendall variance and Z
    const vS0 = (n * (n - 1) * (2 * n + 5)) / 18.0;
    let z = 0;
    if (s > 0) z = (s - 1) / Math.sqrt(vS0);
    else if (s < 0) z = (s + 1) / Math.sqrt(vS0);
    const liveP = normalSurvival2Sided(z);

    // 95% CI rank bounds
    const zCrit = 1.959964;
    const cAlpha = zCrit * Math.sqrt(vS0);
    const kLow = Math.max(0, Math.floor((nPairs - cAlpha) / 2.0));
    const kHigh = Math.min(nPairs - 1, Math.ceil((nPairs + cAlpha) / 2.0));
    const ciLow = slopes[kLow];
    const ciHigh = slopes[kHigh];

    // 5. Precomputed matching
    let matchedWindow = null;
    if (start === 2002 && end === 2026) matchedWindow = 'full_record';
    else if (start === 2002 && end === 2017) matchedWindow = 'grace_era';
    else if (start === 2018 && end === 2026) matchedWindow = 'grace_fo_era';
    else if (start === 2020 && end === 2026) matchedWindow = 'recent_2020';

    let precomputedRow = null;
    if (matchedWindow) {
      const targetVar = (varId === 'imerg' ? 'precip' : varId);
      if (db && Array.isArray(db.results)) {
        precomputedRow = db.results.find(r =>
          r.window === matchedWindow &&
          String(r.entity).toLowerCase() === region.toLowerCase() &&
          r.variable === targetVar &&
          r.season === season
        );
      }
      if (!precomputedRow && ed && ed.presets) {
        const key = `${matchedWindow}_${region}_${targetVar}`;
        precomputedRow = ed.presets[key];
      }
    }

    if (precomputedRow) {
      const pValRaw = precomputedRow.p_value !== undefined ? precomputedRow.p_value : liveP;
      const pValNum = typeof pValRaw === 'number' ? pValRaw : (String(pValRaw).includes('<') ? 0.0 : parseFloat(pValRaw));
      return {
        n: precomputedRow.n_obs || n,
        slope: olsSlope,
        theil_sen_slope: precomputedRow.slope !== undefined ? Number(precomputedRow.slope) : theilSenSlope,
        slope_ci_low: precomputedRow.slope_ci_low !== undefined ? Number(precomputedRow.slope_ci_low) : ciLow,
        slope_ci_high: precomputedRow.slope_ci_high !== undefined ? Number(precomputedRow.slope_ci_high) : ciHigh,
        p_value: pValNum,
        p_formatted: typeof pValRaw === 'string' ? pValRaw : (pValNum < 0.0001 ? '< 0.0001' : pValNum.toFixed(4)),
        z: z,
        s: s,
        is_precomputed: true,
        window: matchedWindow,
        verdict: precomputedRow.verdict || (pValNum < 0.05 ? 'Significant' : 'No detectable trend'),
        bh_fdr_q_value: precomputedRow.bh_fdr_q_value !== undefined ? precomputedRow.bh_fdr_q_value : null,
        gamma: precomputedRow.gamma !== undefined ? precomputedRow.gamma : 1.0,
        r1_detrended: precomputedRow.r1_detrended !== undefined ? precomputedRow.r1_detrended : 0.0,
        n_star: precomputedRow.n_star !== undefined ? precomputedRow.n_star : n,
        primary_method: precomputedRow.primary_method || 'Calibrated ESS-MK',
        diagnostics_note: 'Precomputed calibrated diagnostics'
      };
    }

    // Custom window (Live Calibrated ESS-MK)
    if (n < 10) {
      return {
        n: n,
        slope: olsSlope,
        theil_sen_slope: theilSenSlope,
        slope_ci_low: null,
        slope_ci_high: null,
        p_value: null,
        p_formatted: 'n too small',
        z: null,
        s: s,
        is_precomputed: false,
        window: 'custom',
        verdict: 'n too small (< 10)',
        bh_fdr_q_value: null,
        gamma: null,
        r1_detrended: null,
        n_star: null,
        primary_method: 'Live Calibrated ESS-MK',
        diagnostics_note: 'Sample size n < 10 is too small for statistical trend estimation'
      };
    }

    const ess = essMannKendall(validT, validY);
    const pVal = ess.p_value;
    return {
      n: n,
      slope: olsSlope,
      theil_sen_slope: ess.slope,
      slope_ci_low: ess.ci_low,
      slope_ci_high: ess.ci_high,
      p_value: pVal,
      p_formatted: pVal < 0.0001 ? '< 0.0001' : pVal.toFixed(4),
      z: ess.z,
      s: ess.s,
      is_precomputed: false,
      window: 'custom',
      verdict: pVal < 0.05 ? 'Significant (p < 0.05)' : 'No detectable trend (p ≥ 0.05)',
      bh_fdr_q_value: null,
      gamma: ess.gamma,
      r1_detrended: ess.r1_detrended,
      n_star: ess.n_star,
      primary_method: 'Live Calibrated ESS-MK',
      diagnostics_note: 'Custom window computed via live ESS-Mann-Kendall'
    };
  }

  return {
    deseasonalize: deseasonalize,
    essMannKendall: essMannKendall,
    seasonalAggregate: seasonalAggregate,
    approxMDS: approxMDS,
    calcTrendLine: calcTrendLine,
    normalSurvival2Sided: normalSurvival2Sided,
    analyze: analyze
  };
}));
