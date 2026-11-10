/**
 * tests/js/stats.test.mjs
 * =======================
 * Node.js test suite verifying mathematical parity between
 * assets/js/stats.js and Python v3/trend_engine.py using
 * golden test cases in tests/fixtures/stats_golden.json.
 */

import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REPO_ROOT = path.resolve(__dirname, '../..');

// Load UMD module
import StatsModule from '../../assets/js/stats.js';
const Stats = StatsModule;

describe('Calibrated ESS-MK Engine Parity vs Python Golden Fixtures', () => {
  const fixturesPath = path.join(REPO_ROOT, 'tests/fixtures/stats_golden.json');
  const fixtures = JSON.parse(fs.readFileSync(fixturesPath, 'utf8'));

  for (const tc of fixtures) {
    test(`Golden Case: ${tc.case_id} (${tc.description})`, () => {
      let yInput = tc.y_deseasonalized || tc.y;
      if (!yInput && tc.y_raw && tc.months) {
        yInput = Stats.deseasonalize(tc.months, tc.y_raw);
      }

      const res = Stats.essMannKendall(tc.t, yInput, 0.05);
      const exp = tc.expected;

      // Check n
      assert.equal(res.n, exp.n_star ? Math.round(exp.n_star * exp.gamma) : tc.t.length);

      // Check slope
      const slopeDiff = Math.abs(res.slope - exp.slope);
      const relDiff = exp.slope !== 0 ? slopeDiff / Math.abs(exp.slope) : slopeDiff;
      assert.ok(
        relDiff < 1e-5 || slopeDiff < 1e-6,
        `Slope mismatch in ${tc.case_id}: JS=${res.slope}, Py=${exp.slope}`
      );

      // Check 95% CI bounds
      const ciLowDiff = Math.abs(res.ci_low - exp.ci_low);
      const ciHighDiff = Math.abs(res.ci_high - exp.ci_high);
      assert.ok(
        ciLowDiff < 1e-4,
        `CI low mismatch in ${tc.case_id}: JS=${res.ci_low}, Py=${exp.ci_low}`
      );
      assert.ok(
        ciHighDiff < 1e-4,
        `CI high mismatch in ${tc.case_id}: JS=${res.ci_high}, Py=${exp.ci_high}`
      );

      // Check p-value and significance verdict agreement (alpha = 0.05)
      const jsSig = res.p_value < 0.05;
      const pySig = exp.p_value < 0.05;
      assert.equal(
        jsSig,
        pySig,
        `Significance verdict divergence in ${tc.case_id}: JS(p=${res.p_value}) vs Py(p=${exp.p_value})`
      );

      // Check p-value numeric tolerance
      const pDiff = Math.abs(res.p_value - exp.p_value);
      assert.ok(
        pDiff < 1e-3,
        `p-value numerical drift in ${tc.case_id}: JS=${res.p_value}, Py=${exp.p_value}`
      );

      // Check Kendall S statistic
      assert.equal(res.s, exp.s, `Kendall S mismatch in ${tc.case_id}`);

      // Check gamma
      assert.ok(
        Math.abs(res.gamma - exp.gamma) < 0.01,
        `Gamma mismatch in ${tc.case_id}: JS=${res.gamma}, Py=${exp.gamma}`
      );
    });
  }
});

describe('Seasonal Aggregation Logic', () => {
  test('Monsoon aggregation requires at least 3 months and averages properly', () => {
    const dummy = [
      { ym: '2020-06', year: 2020, month: 6, value: 100 },
      { ym: '2020-07', year: 2020, month: 7, value: 200 },
      { ym: '2020-08', year: 2020, month: 8, value: 300 },
      { ym: '2020-09', year: 2020, month: 9, value: 400 },
      // 2021 has only 2 months (insufficient)
      { ym: '2021-06', year: 2021, month: 6, value: 150 },
      { ym: '2021-07', year: 2021, month: 7, value: 250 },
    ];

    const aggMean = Stats.seasonalAggregate(dummy, 'monsoon', 'mean');
    assert.equal(aggMean.length, 1);
    assert.equal(aggMean[0].year, 2020);
    assert.equal(aggMean[0].value, 250); // (100+200+300+400)/4
  });

  test('Winter offset assigns December to following calendar year', () => {
    const dummy = [
      { ym: '2019-12', year: 2019, month: 12, value: 50 },
      { ym: '2020-01', year: 2020, month: 1, value: 60 },
      { ym: '2020-02', year: 2020, month: 2, value: 70 },
    ];

    const agg = Stats.seasonalAggregate(dummy, 'winter', 'mean');
    assert.equal(agg.length, 1);
    assert.equal(agg[0].year, 2020); // Dec 2019 + Jan/Feb 2020 -> Winter 2020
    assert.equal(agg[0].value, 60);
  });
});
