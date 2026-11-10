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

    let meanT = 0;
    for (let i = 0; i < n; i++) meanT += validT[i];
    meanT /= n;

    let ssT = 0;
    let ssResid = 0;
    for (let i = 0; i < n; i++) {
      const dt = validT[i] - meanT;
      ssT += dt * dt;
      const resid = validY[i] - slope * validT[i];
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

  return {
    deseasonalize: deseasonalize,
    essMannKendall: essMannKendall,
    seasonalAggregate: seasonalAggregate,
    approxMDS: approxMDS,
    calcTrendLine: calcTrendLine,
    normalSurvival2Sided: normalSurvival2Sided
  };
}));
