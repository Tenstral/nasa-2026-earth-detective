# Critical review of Bengal Hydro Detective (judge's view)

This review is based on the README, `PROJECT_STATUS.md`, and the Nov 10 summary. I did not run the code or open the dashboard in a browser.

## Biggest risk: it reads as a report, not a tool

The challenge says: "create a **tool** that can **select variables**… visualize… determine if significant." The audience is high school and college students and the public.

- **One fixed study.** The project is a pipeline for one region and one question: GRACE water storage, rainfall and soil moisture in Bangladesh. I found no sign that a user can pick any variable or region and get a trend result. The pipeline is hard-wired and run by scripts (`run_all.py`, `v3/*.py`). A judge may see it as "excellent analysis, but not the tool requested."
- **No variable-discovery step.** The challenge stresses the difficulty of choosing variables. I saw no guided questions, variable search, or "what should I investigate?" flow.
- **Wrong audience level.** The README uses terms like ESS-MK, Hurwicz bias correction, BH-FDR, Newey-West HAC, circular block bootstrap and placebo tests. The brief wants simple definitions for students. `PROJECT_STATUS.md` is aimed at teammates, not at the public.
- **Scope creep.** The brief says linear trends are "a great start" and complex analysis is out of scope. Spending effort on 336 tests, Monte Carlo calibration and pairwise placebo tests spends the team's limited time on methodology rather than usability.
- **Demos.** The brief suggests demonstration examples. `index.html` and `demo.html` may cover this, but the Bangladesh story is the only one.

## Internal inconsistencies (they hurt credibility)

Judges in a regional round often skim, but one stale number can undercut a "rigorous" pitch.

- **Exposed population.** The README gives NE 26.68M and Central 43.01M. The Nov 10 summary says these were corrected to NE 24.05M and Central 45.64M. The total is still 108.5M, but the README is stale.
- **GRACE-to-GRACE-FO offset.**
  - The README says there is no significant step: NW +1.34 cm, p=0.49.
  - `PROJECT_STATUS.md` says there is a step: NW +9.15 cm, p=0.028.
  - These contradict each other on a central methodological claim.
- **Test counts.** The README says "14 tests". The summary says "76 passed of 78", which means 2 are failing.
- **Branch and status.** The README tells people to `git checkout v3-expansion`. Other notes say the useful commit `9edb82a` still has to be merged into `main`.
- **Small drift.** Seasonal response is 32.6% in the README and 32.5% in the summary.

## Scientific and communication weaknesses

- **Coarse resolution.** GRACE is about 300 km, and the project admits regions are not independent. Division-level maps look more precise than the data allow, and the project says so itself.
- **Mixed message on significance.** Some GRACE-FO-era and 2020s results are "method-dependent" or "no detectable trend". The headline of an ongoing NW decline is not equally strong in every window. The project is honest about this, but it is hard to present in 5 minutes.
- **Attribution without in-situ data.** There are no well or pumping records, so irrigation as the cause is only "consistent with." Attribution to irrigation may feel unproven to a judge.
- **Over-hedged wording.** Forbidden-phrase rules, "PRELIMINARY" banners and heavy caveats make the story harder to follow, and the tone is defensive.
- **Repo hygiene.**
  - Committed `__pycache__` folders.
  - Two `LATEST_SUMMARY` files.
  - A `scratch/` folder.
  - Many root-level scripts alongside v2 and v3, so it is unclear which pipeline is current.
  - A `.docx` mentor brief.
- **Dependencies and reproducibility.**
  - NASA Earthdata login is needed to rerun it.
  - `index.html` loads Chart.js and fonts from a CDN, so it breaks offline. That is a risk at a venue with unreliable Wi-Fi.
- **Human-impact claim.** "108.5M people exposed" counts everyone in regions with a significant trend. It is a regional population total, not people actually affected. A skeptical judge could call it inflated.

## Winning chance in the Dhaka regional round

I can't know the competition or judging rubric, so this is a judgment, not data.

| Factor | Assessment |
|---|---|
| Scientific depth | Likely well above most teams |
| Local relevance | Strong. Bangladesh groundwater and Boro irrigation, in a Dhaka judging room |
| Data use | Strong. GRACE, GPM, GLDAS, MODIS and SEDAC |
| Fit to "tool" brief | Weak to moderate |
| Accessibility for students and public | Weak to moderate |
| Demo risk | Moderate (CDN, complexity, 5-minute limit) |

- **Regional win:** roughly 35–50% if you present it well. The depth and local relevance are strong. Most Space Apps entries in this category are simple notebooks or dashboards. The main threat is a competing team with a polished, interactive, student-friendly "pick a variable and region" tool.
- **Global Nominee:** lower, around 10–15%. Judges at that stage weigh creativity and fit to the brief more heavily than methodological depth.

## Highest-value fixes before presenting

1. **Reconcile the numbers.** Make the README, `PROJECT_STATUS.md` and dashboard agree on the offset, population and test counts, and fix the 2 failing tests.
2. **Add a "Detective mode" to the dashboard.** Pick a variable and a region, then show the time series, slope, CI and a plain-English verdict. Even 3–4 preset variables would answer the "tool" requirement.
3. **Write a one-page plain-language guide.** Define the variables and explain "significant" for students.
4. **Run the pitch around the story.** Tell the rain-is-flat but storage-is-falling story first, then the method. Treat the method as proof, not the headline.
5. **Make the dashboard work offline.** Bundle Chart.js and the fonts, and keep a backup recording.
6. **Clean the repo.** Remove `__pycache__` and `scratch`, and make clear which pipeline is current.
