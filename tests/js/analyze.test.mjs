/**
 * tests/js/analyze.test.mjs
 * =========================
 * Node.js test suite for window.Stats.analyze()
 */

import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import Stats from '../../assets/js/stats.js';

describe('Client-side analyze() tests', () => {

  test('analyze() returns precomputed diagnostics when matching full_record NW tws', () => {
    // Generate synthetic monthly NW tws data (2002–2026)
    const points = [];
    for (let yr = 2002; yr <= 2026; yr++) {
      for (let mo = 1; mo <= 12; mo++) {
        const decYr = yr + (mo - 0.5) / 12;
        // declining slope of approx -1.25 cm/yr plus sinusoidal season
        const val = -1.25 * (decYr - 2002) + 15 * Math.sin(2 * Math.PI * (mo / 12));
        points.push({ ym: `${yr}-${mo < 10 ? '0' + mo : mo}`, year: yr, month: mo, decimal_year: decYr, value: val });
      }
    }

    const mockDashboardData = {
      results: [
        {
          window: 'full_record',
          entity: 'NW',
          variable: 'tws',
          season: 'annual',
          slope: -1.255,
          slope_ci_low: -1.498,
          slope_ci_high: -1.020,
          p_value: '< 0.0001',
          bh_fdr_q_value: '< 0.0001',
          verdict: 'Significant',
          primary_method: 'Calibrated ESS-MK',
          gamma: 3.612,
          r1_detrended: 0.5663,
          n_star: 71.2,
          n_obs: 257
        }
      ]
    };

    const res = Stats.analyze({
      var: 'tws',
      region: 'NW',
      start: 2002,
      end: 2026,
      season: 'annual',
      points: points,
      data: mockDashboardData
    });

    assert.equal(res.is_precomputed, true);
    assert.equal(res.window, 'full_record');
    assert.equal(res.verdict, 'Significant');
    assert.equal(res.theil_sen_slope, -1.255);
    assert.equal(res.p_formatted, '< 0.0001');
    assert.equal(res.bh_fdr_q_value, '< 0.0001');
    assert.equal(res.gamma, 3.612);
    assert.equal(res.r1_detrended, 0.5663);
    assert.equal(res.n_star, 71.2);
    assert.ok(Math.abs(res.slope - (-1.25)) < 0.05);
  });

  test('analyze() for custom window computes simple live tests and labels advanced diagnostics "precomputed windows only"', () => {
    // Custom window: 2005 to 2020
    const points = [];
    for (let yr = 2005; yr <= 2020; yr++) {
      for (let mo = 1; mo <= 12; mo++) {
        const decYr = yr + (mo - 0.5) / 12;
        const val = -0.8 * (decYr - 2005) + 10 * Math.sin(2 * Math.PI * (mo / 12));
        points.push({ ym: `${yr}-${mo < 10 ? '0' + mo : mo}`, year: yr, month: mo, decimal_year: decYr, value: val });
      }
    }

    const res = Stats.analyze({
      var: 'tws',
      region: 'NW',
      start: 2005,
      end: 2020,
      season: 'annual',
      points: points
    });

    assert.equal(res.is_precomputed, false);
    assert.equal(res.window, 'custom');
    assert.ok(res.n > 100);
    assert.ok(!isNaN(res.slope));
    assert.ok(!isNaN(res.theil_sen_slope));
    assert.ok(!isNaN(res.p_value));
    assert.equal(res.bh_fdr_q_value, 'precomputed windows only');
    assert.equal(res.gamma, 'precomputed windows only');
    assert.equal(res.r1_detrended, 'precomputed windows only');
    assert.equal(res.n_star, 'precomputed windows only');
  });

});
