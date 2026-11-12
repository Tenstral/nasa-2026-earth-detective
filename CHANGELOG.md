# Changelog: Slide-Over Drawers Enrichment & Statistical Hardening
**Branch:** `drawers-enrichment`  
**Base Commit:** `51c504e` (`DOOM`)  
**Deliverable:** Slide-Over Drawers Enrichment & Statistical Hardening for NASA Space Apps 2026

---

## Summary of Changes

This release completely enriches, calibrates, and verifies the three slide-over drawers in `index.html`:
1. **Drawer A ("Methodological Proof & In-Depth Audit", `#evidenceDrawer`):** Replaced missing `REPORT_FRAGMENTS` with an automated build pipeline extracting pre-rendered empirical tables, transition comparisons, multi-model storage partitions, pairwise differences, and limitations directly from `report.html`.
2. **Drawer B ("Statistical Rigor & Detection Power", `#drawer-diagnostics`):** Expanded the diagnostic grid to 10 comprehensive metrics, enabled numeric live calibrated ESS-MK statistics for custom temporal windows, computed 80% Minimum Detectable Slope (MDS) power limits across all call sites, added Dr. James Acker's window length power verdict (identifying underpowered short windows), and added a 13-variable NASA sensor provenance audit.
3. **Drawer C ("Regional Stakeholder Action Directives", `#drawer-directives`):** Surfaced all 6 catalog fields with satellite evidence leading, implemented robust division-to-region mapping with division header labeling, added live scientific basis footers, tagged all agronomic and policy claims with verified citations (`assets/js/citations.js`), and ensured strict storage stability terminology for the southern regions.

---

## Files Created

- `tools/build_fragments.py`: Automated build script that extracts `#threeway`, `#gldas`, `#pairwise-differences`, `#stakeholder-actions`, and `#limitations` from `report.html`, strips executable scripts/event handlers, normalizes relative asset paths, and outputs `assets/js/report_fragments.js`.
- `assets/js/report_fragments.js`: Generated data store defining `window.REPORT_FRAGMENTS` containing complete HTML tables and relative figure links for each evidence tab (>67 KB).
- `assets/js/citations.js`: Central registry defining `window.CITATIONS` (19 verified peer-reviewed, policy, and agronomic references) and `window.getCitationBadge(id)`.
- `tests/drawers.test.mjs`: Comprehensive Node acceptance test suite validating 14 test cases across all 5 regions, 3 variables, custom windows, power detection limits, division mapping, and golden number cross-checks.
- `TODO_UNVERIFIED.md`: Traceability and verification audit register verifying all surfaced numbers against committed data files.
- `CHANGELOG.md`: Detailed documentation of all changes made across the repository.

---

## Files Modified

- `report.html`:
  - Populated empty table bodies (`#threeWayTableBody`, `#gldasTableBody`, `#pairwiseTableBody`) with exact empirical numbers from `outputs/v3/`.
  - Added relative image links (`fig1_grace_gracefo_record.png`, `fig3_transition_gap.png`, `fig_pairwise_slope_differences.png`).
  - Added multi-model GLDAS partition tables, transition offset models, real-residual placebo results, and synthesis matrices.
  - Linked citations using verified badge annotations.
- `index.html`:
  - Loaded `assets/js/report_fragments.js` and `assets/js/citations.js` prior to `assets/js/app.js`.
  - Added student mode summary container (`#diag-student-summary`) and detection power verdict box (`#diag-power-verdict-box`) in `#drawer-diagnostics`.
  - Updated subtitle in both English and Bangla.
- `assets/i18n.js`:
  - Synchronized English and Bangla translation keys for `diag.subtitle`.
- `assets/css/app.css`:
  - Added semantic CSS variable aliases (`--ink-primary`, `--ink-secondary`, `--ink-muted`, `--border-subtle`).
  - Added styling for `.citation-badge.verified`, `.citation-badge.unverified`, `.diag-power-verdict`, and `.directive-basis`.
  - Added declarative display rules ensuring open drawers display cleanly in both student and scientist modes.
- `assets/js/stats.js`:
  - In `Stats.analyze()`, replaced `'precomputed windows only'` placeholder strings with live numeric `theil_sen_slope`, duality-aligned CI, p-value, `gamma`, `r1_detrended`, and `n_star` using `essMannKendall()`.
  - Handled sample size $n < 10$ gracefully by returning `null` numeric fields with `p_formatted: 'n too small'`.
- `assets/js/app.js`:
  - Added `ensureMDS()` helper ensuring `mds_80_power` is computed and `n_eff = n_star` aliasing across all three call sites.
  - Added `SENSOR_AUDIT_REGISTER` dictionary covering all 13 NASA Earth Observation variables.
  - Refactored `updateDiagnosticsContent()` to render the expanded 10-metric grid, student plain-language summary, underpowered detection power callouts, and sensor provenance.
  - Refactored `updateDirectivesContent()` to render all 6 catalog fields, map divisions to parent regions with contextual headers, show explicit empty states for unknown regions, link verified citation badges, and attach live scientific basis footers.
- `tests/js/analyze.test.mjs`:
  - Updated custom window test cases to verify numeric ESS-MK return fields and $n < 10$ behavior.

---

## Test Verification

- **Node Drawers Acceptance Tests (`tests/drawers.test.mjs`):** 14/14 passed (100%).
- **Node Core Test Suite (`tests/js/*.test.mjs`):** 31/31 passed across 6 test suites (100%).
- **Python Verification & Pipeline Tests (`tests/`):** 107/107 passed (100%).
- **Zero Forbidden Phrases Test:** Passed with 0 violations.
- **Offline & File Protocol Compatibility:** Verified 100% offline-ready, zero external CDN dependencies, static vanilla JS compatible with `file://` and Cloudflare Pages.
