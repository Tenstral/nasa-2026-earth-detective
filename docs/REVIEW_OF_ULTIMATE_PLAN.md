# Review of `ULTIMATE_WEBAPP_INSTRUCTION.md` vs. the "Earth System Trend Detective" brief

**Short verdict:** The plan has the right *direction* (turn a pre-computed report into an interactive 5-step tool). But it is really **two plans that contradict each other**. On top of that, it has a few **scientific-validity traps** that could cost you points with a NASA scientist judge, and **too much scope**. Combine the good pieces into one static-first app. Fix the validity issues, and cut the backend.

I checked several claims against the repo (see the note at the end). Most of the factual audit is accurate.

---

## 1. What the plan gets right (keep these)

1. **Mapping the UI one-to-one onto Dr. Acker's 5 steps** (variable → region → time period → inspect series → significance test). This is the single most important alignment decision. Judges will literally check for these 5 steps.
2. **Making the time window user-adjustable, plus the "Why window length matters" callout.** This directly teaches the video's key point: p > 0.05 does not mean "no trend", and a longer record may be all that's needed. Your NW GRACE-FO example (8-yr window p ≈ 0.055 → 24-yr window p < 0.0001, with the MDS explanation) is a great demo moment. It is probably your strongest "wow + correct" feature.
3. **Using p < 0.05 as the headline "Challenge Standard" verdict, with FDR as a secondary "audit" layer.** This respects the brief and still keeps your rigor.
4. **Adding Dr. Acker's Wisconsin MODIS-Aqua AOD case.** It proves the tool generalizes beyond Bangladesh and matches the video exactly.
5. **Plotting the trend line, the gap shading, and raw vs. deseasonalized views.** This covers "generate and *inspect*".
6. **Offline hardening** (vendoring Chart.js, system fonts), **a consistent set of numbers across documents**, and **cleaning up the repo root.**
7. **Guided "case files" plus a free-explorer mode.** This matches the video's point that variable selection is the hard part for users.
8. **Monthly data only.** The video explicitly says weekly/monthly resolution is better for trends than hourly or 3-hourly data.

---

## 2. The biggest structural problem: two contradictory architectures

- **Phases 1–7** describe a **static, offline, client-side** app: the data is embedded in the HTML and a JavaScript stats engine runs in the browser.
- **"Finalization" onwards** switches to **FastAPI + DuckDB/SQLite + live NASA API + Leaflet globe**. It even says "with your green light on a server-backed application".

A coding agent given this file will build both, or get confused. **Pick one. I recommend static-first:**

| Concern | Static client-side app | FastAPI + DB + live API |
|---|---|---|
| Works with venue Wi-Fi down | Yes, fully | Only for cached queries |
| Global judges can open a link | Yes (GitHub Pages, free, permanent) | Needs a paid or always-on server that can sleep or crash |
| Time to build reliably | Small | Large (server, DB, ingestion, caching, deployment) |
| "Under 5 ms" claims | True: a few hundred monthly points take microseconds in JS | Only on a cache hit |
| Failure points during a demo | ~0 | Server, DB, network, NASA rate limits |

The caching argument in "Finalization" solves a problem that **only exists because you added a live backend**. With embedded data, there's nothing to cache.

**If you really want a "live NASA data" story**, add it as an *optional* enhancement inside the static app: a "Try any location" button that calls NASA POWER directly from the browser (it's keyless and supports CORS). Show a clear "live, needs internet" label, and fall back gracefully if it fails. No server is needed.

**Drop entirely:**
- DuckDB/SQLite and the ingestion scripts
- the authenticated Earthdata connector (you can't ship credentials in a public demo)
- the **Open-Meteo fallback** (it's not NASA data, and the brief is about NASA data)
- the Kasatochi SO₂ case
- the Leaflet globe
- the "🟢 LIVE FASTAPI + DUCKDB BACKEND CONNECTED" pill (jargon that means nothing to students)

---

## 3. Scientific-validity problems (these matter most with a NASA judge)

1. **Wisconsin AOD must be real data.** The plan says "add a compact time series *representing* MODIS AOD". There is currently **no AOD data in the repo**. Do it the way Dr. Acker did: generate the Wisconsin area-averaged monthly AOD time series (MODIS Aqua, monthly Level-3 product, 550 nm combined Dark Target/Deep Blue) in **Giovanni**, export the CSV, and commit it with the exact product name, version, and download date. A synthetic or hand-made series would be a disqualifying-level credibility problem if anyone asks. Also check the latest month actually available, and mention any end-of-mission caveat for Aqua in the data card.

2. **Seasonal trends are being computed the wrong way (it's implied, not stated).** The plan feeds "monsoon" or "summer JJA" *monthly* values into the test. The scientifically correct approach for "is summer AOD increasing?" or "is monsoon storage changing?" is to **first average each season to one value per year** (e.g., the JJA mean for 2002, 2003, …), then run Mann-Kendall/Theil-Sen on that annual series (n ≈ 22–24). Feeding 3–4 consecutive months per year breaks the time spacing and the autocorrelation assumptions. This is exactly the "trend within a single season" case the video mentions. Get it right.

3. **Minimum record length.** "Minimum 5 years" is too short for annual or seasonal series: 5 points can almost never reach significance, and the normal approximation is poor. Enforce something like **≥ 8–10 points for annual/seasonal series** and **≥ 5 years for monthly series**. When the window is too short, the UI should say why, not just show "no detectable trend".

4. **The NW 2017–18 step offset: don't cherry-pick.** Checklist item 1 tells the agent to rewrite the README to "+9.15 cm, p = 0.028". But your own status doc shows the result **depends on the method**: significant without a buffer, **not significant (p = 0.171) with a ±6-month buffer**, and the README has a third value (+1.34 cm, p = 0.49). Reconcile all documents to report **all specifications together** with the honest label "method-dependent". Then explain *why* the README's number differs (different model or window), or delete it if it's outdated. Picking the significant one would contradict your project's whole philosophy.

5. **The student-mode p-value definition is wrong.** "p < 0.05 means < 5% chance of random noise" is the classic misinterpretation, and a statistician judge will catch it. Use something like: *"If there were really no trend, a pattern this strong would show up by chance less than 5% of the time."*

6. **The slider creates a hidden multiple-testing problem.** Users can slide the window until something turns significant (p-hacking). Turn this into a teaching feature: a small note saying "Trying many windows increases the chance of a false positive. The preset windows are corrected for this (FDR); custom windows are not." Only show the FDR q-value for the canonical presets, as the plan already suggests.

7. **Label the "95% CI fan" honestly.** Lines drawn with the lower and upper slope bounds through the median point show *slope uncertainty*. They are not a prediction band. Call it "range of plausible trend slopes", or students will think the data should fall inside it.

8. **Deseasonalizing within the selected window means the climatology changes as the user drags the slider.** That's acceptable, but state it in the scientist view.

9. **The reanalysis contradiction.** Case File #3 shows NASA POWER precipitation has a 2015 step artifact. Yet the live "any coordinate" feature would offer POWER precipitation for trend detection. If you keep live POWER, prefer **temperature (T2M) and solar radiation**, and add a warning on precipitation. Also note that a POWER point is a ~0.5° grid cell, not a "region".

10. **Wording that violates your own guardrails.** The plan's own demo text uses "rainfall stays flat", "storage plummeting", "Barind Enigma", "explains only a fraction", and "threatening Boro rice". Some of these are banned phrases, and others make causal claims. Use "no detectable rainfall trend" and "consistent with irrigation demand, not proof of it". Also, GLDAS 0–2 m is the **root zone, not "topsoil"** (Case File #2).

11. **Impact translation.** I checked the arithmetic: −1.25 cm/yr × NW area ≈ 0.39 km³/yr ≈ 390 billion L ≈ 156k Olympic pools. That's correct, so keep it, but show the CI range (−1.02 to −1.50 cm/yr), not just the central value.

12. **The JS port must be *proven* to match Python.** Don't just claim "matches to 4 decimals". Export ~20 golden test cases from the Python engine (different regions, windows, seasons, and edge cases such as ties, gaps, and negative r₁). Then add a test that runs the JS engine on them and compares the results. This is your "validity" evidence.

13. Minor: the gap dates are inconsistent ("June 2017 – May 2018" in one place, `2017-07 to 2018-05` in the schema). Use the data-driven dates: the last GRACE month is 2017-06 and the first GRACE-FO month is 2018-06.

---

## 4. Smaller corrections to the audit section

- **The failing test only fails without `pymannkendall` installed.** In this environment all **78 tests pass**. Guarding the import is still worth doing, but it's not a "critical bug".
- **Removing `PROJECT_ISSUES.md` "so judges don't read flaws"**: archive it, fine. But keep a visible **Limitations** section (footprint size, the step offset, model dependence). Judges score *validity*, and honest limitations count in your favor.
- **The forbidden-phrase list is fine internally**, but make sure UI copy for students stays readable. "No detectable trend" is fine; don't let the guardrail make the student mode sound robotic.

---

## 5. Scope: what to cut so you finish

| Keep (core) | Keep but shrink | Cut |
|---|---|---|
| 5-step workbench | Bilingual: translate only the verdict card, step labels, and case-file intros (not every narrative) | FastAPI / DuckDB / SQLite |
| JS stats engine + parity tests | 10 variables → start with ~6: TWS, IMERG, POWER precip (for the trap case), GLDAS soil moisture, subsurface residual, AOD; add extremes if time allows | Earthdata auth connector, Open-Meteo |
| 3–4 case files incl. Wisconsin | Scientist audit mode = one collapsible panel, not a separate app | Leaflet globe, Kasatochi |
| Window-length lesson | Live POWER = one optional button | 336-row filterable registry in the UI (link to the CSV instead) |
| Offline + GitHub Pages hosting | Flood markers (cite the source for each year) | "Live backend" status pill |

---

## 6. Recommended order of work

1. **Freeze the science:** make the master CSV/JSON the single source of truth, reconcile every document to it (with the honest step-offset wording), and add the cross-document consistency test.
2. **Get the real Wisconsin AOD CSV from Giovanni**, with provenance.
3. **Fix the seasonal aggregation** (one value per season per year) in both Python and the upcoming JS engine.
4. **Write the JS engine**, plus golden-fixture parity tests against Python.
5. **Build the 5-step workbench UI** on top of the embedded data, with case files and the window-length callout.
6. **Write student-mode copy** (correct p-value definition, impact translation with a range) and the minimal Bangla layer.
7. **Harden offline** (vendor Chart.js and fonts) and deploy to GitHub Pages, so there is one public URL for global judges.
8. *(Optional)* Live NASA POWER "try any location" button.
9. **Demo script and video:** a 30-second hook (Wisconsin case → Bangladesh NW → slide the window to show p crossing 0.05), then the scientist-mode reveal.

---

## 7. How this maps to typical Space Apps judging criteria

- **Relevance:** explicit 5 steps, the p < 0.05 rule, the video's own Wisconsin example, and the window-length lesson.
- **Validity:** real NASA data with provenance, a JS engine proven against Python, honest method-dependent results, and correct seasonal aggregation.
- **Impact:** Bangladesh water storage affecting ~108M people in the declining regions, with Bangla support and farmer/policymaker cards.
- **Creativity:** the "detective case files" framing, plus the reanalysis-trap case (teaching students to question their data source is a strong, unusual angle).
- **Presentation:** one stable public link that works offline, and a tight demo flow.

> [!NOTE]
> Verified in the repo: 78/78 tests pass (`pymannkendall` 1.4.3 is installed here). The README really does contain the stale +1.34 cm step offset. There is no AOD/Wisconsin data in the repo. `index.html` loads Chart.js and Google Fonts from CDNs. The NW figures (74.2% cropland, −1.25 cm/yr [−1.50, −1.02]) match `exposure_table.csv`.
