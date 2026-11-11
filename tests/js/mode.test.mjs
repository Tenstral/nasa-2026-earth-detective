import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REPO_ROOT = path.resolve(__dirname, '../..');

describe('Mode Behavior (Student vs Scientist)', () => {
  const indexHtml = fs.readFileSync(path.join(REPO_ROOT, 'index.html'), 'utf-8');
  const reportHtml = fs.readFileSync(path.join(REPO_ROOT, 'report.html'), 'utf-8');
  const demoHtml = fs.readFileSync(path.join(REPO_ROOT, 'demo.html'), 'utf-8');
  const topNavCss = fs.readFileSync(path.join(REPO_ROOT, 'assets/css/top_nav.css'), 'utf-8');

  test('top_nav.css contains declarative mode visibility rules', () => {
    assert.match(topNavCss, /html\[data-mode="student"\]\s+\[data-mode="scientist"\]/);
    assert.match(topNavCss, /html\[data-mode="scientist"\]\s+\[data-mode="student"\]/);
    assert.match(topNavCss, /display:\s*none\s*!important;/);
  });

  test('index.html: Step 0 diagnostic elements carry data-mode="scientist"', () => {
    // 1. CI cell
    assert.match(indexHtml, /<div class="telemetry-cell"[^>]*data-mode="scientist"[^>]*>[\s\S]*?id="tel-ci"/);
    // 2. p & FDR cell
    assert.match(indexHtml, /<div class="telemetry-cell"[^>]*data-mode="scientist"[^>]*>[\s\S]*?id="tel-p"/);
    // 3. Sample & Power limit cell
    assert.match(indexHtml, /<div class="telemetry-cell"[^>]*data-mode="scientist"[^>]*>[\s\S]*?id="tel-n"/);
    // 4. Diagnostics drawer button
    assert.match(indexHtml, /<button class="drawer-btn"[^>]*id="btn-open-diagnostics"[^>]*data-mode="scientist"/);
    // 5. Diagnostics drawer itself
    assert.match(indexHtml, /<aside class="slide-drawer"[^>]*id="drawer-diagnostics"[^>]*data-mode="scientist"/);
    // 6. Student verdict cell exists with data-mode="student"
    assert.match(indexHtml, /<div class="telemetry-cell student-verdict-cell"[^>]*data-mode="student"/);
  });

  test('report.html: Step 0 diagnostic tables carry data-mode="scientist" and student summaries exist', () => {
    // MDS table
    assert.match(reportHtml, /<div class="table-container"[^>]*data-mode="scientist">[\s\S]*?id="mdsTableBody"/);
    // Pairwise table
    assert.match(reportHtml, /<div class="table-container"[^>]*data-mode="scientist">[\s\S]*?id="pairwiseTableBody"/);
    // GLDAS table
    assert.match(reportHtml, /<div class="table-container"[^>]*data-mode="scientist">[\s\S]*?id="gldasTableBody"/);
    // Three-way table
    assert.match(reportHtml, /<div class="table-container"[^>]*data-mode="scientist">[\s\S]*?id="threeWayTableBody"/);
    // Ratio and Drawdown tables
    assert.match(reportHtml, /<div class="table-container"[^>]*data-mode="scientist">[\s\S]*?id="ratioTrendTableBody"/);
    assert.match(reportHtml, /<div class="table-container"[^>]*data-mode="scientist">[\s\S]*?id="drawdownTableBody"/);
    // Full results table
    assert.match(reportHtml, /<details class="appendix-details"[^>]*id="registry"[^>]*data-mode="scientist"/);

    // Student summaries
    const studentSummaries = reportHtml.match(/<div class="student-plain-summary"[^>]*data-mode="student"/g);
    assert.ok(studentSummaries && studentSummaries.length >= 5, 'Must have at least 5 student plain summaries');
  });

  test('demo.html: Step 0 diagnostic boxes carry data-mode="scientist"', () => {
    // Slide 3 Calibrated ESS-MK box
    assert.match(demoHtml, /<div class="sketch-box"[^>]*data-mode="scientist">[\s\S]*?Calibrated ESS-MK/);
    assert.match(demoHtml, /<div class="sketch-box"[^>]*data-mode="student">[\s\S]*?Trend Verification/);

    // Slide 6 Placebo check box
    assert.match(demoHtml, /<div class="sketch-box"[^>]*data-mode="scientist">[\s\S]*?Placebo Check &amp; Overlap Precaution/);
    assert.match(demoHtml, /<div class="sketch-box"[^>]*data-mode="student">[\s\S]*?Regional Comparison Check/);

    // Slide 8 Power & MDS box
    assert.match(demoHtml, /<div class="sketch-box"[^>]*data-mode="scientist">[\s\S]*?Statistical Power &amp; Minimum Detectable Slopes/);
    assert.match(demoHtml, /<div class="sketch-box"[^>]*data-mode="student">[\s\S]*?Window Length &amp; Detection Lesson/);
  });
});
