# Task 1 Calibration: Before-vs-After Significance Verdict Table

**Status:** PRELIMINARY — Comparison of Significance Calibration across all 4 Windows
- **Before Engine:** Hamed-Rao Modified Mann-Kendall with circular block-bootstrap CI (Uncalibrated; FPR 14–26%).
- **After Engine:** Calibrated Effective-Sample-Size (ESS) Mann-Kendall with duality-aligned Theil-Sen CI (FPR 5.0–5.8%, CI coverage 94.2–95.0%).

## Regional Annual Total Water Storage (TWS) Trends

| Window | Region | Slope (cm/yr) | Before p | Before FDR q | Before Verdict | After p | After FDR q | After Calibrated 95% CI | After Calibrated Verdict | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| `full_record` | **NW** | -1.25 | < 0.0001 | < 0.0001 | `Significant` | 0.0005 | 0.0015 | [-1.54, -0.96] | **`Significant`** | Retained (Significant) |
| `full_record` | **NE** | -0.56 | < 0.0001 | < 0.0001 | `Significant` | < 0.0001 | < 0.0001 | [-0.70, -0.42] | **`Significant`** | Retained (Significant) |
| `full_record` | **Central** | -0.47 | < 0.0001 | < 0.0001 | `Significant` | < 0.0001 | < 0.0001 | [-0.62, -0.34] | **`Significant`** | Retained (Significant) |
| `full_record` | **SW** | -0.05 | 0.3715 | 0.4217 | `No detectable trend` | 0.5235 | 0.9256 | [-0.17, +0.08] | `No detectable trend` | Retained (No detectable trend) |
| `full_record` | **SE** | -0.05 | 0.2581 | 0.3011 | `No detectable trend` | 0.4750 | 0.8867 | [-0.17, +0.06] | `No detectable trend` | Retained (No detectable trend) |
| `full_record` | **National** | -0.51 | < 0.0001 | < 0.0001 | `Significant` | < 0.0001 | < 0.0001 | [-0.66, -0.38] | **`Significant`** | Retained (Significant) |
| `grace_era` | **NW** | -1.56 | < 0.0001 | < 0.0001 | `Significant` | 0.0005 | 0.0020 | [-2.03, -1.11] | **`Significant`** | Retained (Significant) |
| `grace_era` | **NE** | -0.72 | < 0.0001 | < 0.0001 | `Significant` | < 0.0001 | < 0.0001 | [-0.99, -0.49] | **`Significant`** | Retained (Significant) |
| `grace_era` | **Central** | -0.63 | < 0.0001 | < 0.0001 | `Significant` | < 0.0001 | < 0.0001 | [-0.86, -0.42] | **`Significant`** | Retained (Significant) |
| `grace_era` | **SW** | -0.13 | 0.1250 | 0.1875 | `No detectable trend` | 0.1045 | 0.2508 | [-0.28, +0.03] | `No detectable trend` | Retained (No detectable trend) |
| `grace_era` | **SE** | -0.12 | 0.0897 | 0.1478 | `No detectable trend` | 0.1040 | 0.2508 | [-0.27, +0.02] | `No detectable trend` | Retained (No detectable trend) |
| `grace_era` | **National** | -0.68 | < 0.0001 | < 0.0001 | `Significant` | < 0.0001 | < 0.0001 | [-0.92, -0.45] | **`Significant`** | Retained (Significant) |
| `grace_fo_era` | **NW** | -1.67 | 0.0283 | 0.1249 | `Suggestive` | 0.0315 | 0.2406 | [-3.22, -0.11] | `Suggestive` | Retained (Suggestive) |
| `grace_fo_era` | **NE** | -0.79 | 0.0269 | 0.1249 | `Suggestive` | 0.1073 | 0.4410 | [-1.78, +0.19] | `No detectable trend` | CHANGED: Suggestive -> No detectable trend |
| `grace_fo_era` | **Central** | -0.81 | 0.0141 | 0.0790 | `Suggestive` | 0.1056 | 0.4410 | [-1.79, +0.20] | `No detectable trend` | CHANGED: Suggestive -> No detectable trend |
| `grace_fo_era` | **SW** | +0.53 | 0.1513 | 0.3345 | `No detectable trend` | 0.3460 | 0.7235 | [-0.47, +1.53] | `No detectable trend` | Retained (No detectable trend) |
| `grace_fo_era` | **SE** | +0.45 | 0.1270 | 0.2964 | `No detectable trend` | 0.2945 | 0.7235 | [-0.30, +1.22] | `No detectable trend` | Retained (No detectable trend) |
| `grace_fo_era` | **National** | -0.47 | 0.2125 | 0.3797 | `No detectable trend` | 0.3111 | 0.7235 | [-1.50, +0.53] | `No detectable trend` | Retained (No detectable trend) |
| `recent_2020` | **NW** | -2.93 | 0.0002 | 0.0038 | `Significant` | 0.0005 | 0.0070 | [-5.01, -0.81] | **`Significant`** | Retained (Significant) |
| `recent_2020` | **NE** | -1.06 | 0.0875 | 0.3063 | `No detectable trend` | 0.1682 | 0.7609 | [-2.64, +0.46] | `No detectable trend` | Retained (No detectable trend) |
| `recent_2020` | **Central** | -1.19 | 0.0309 | 0.1526 | `Suggestive` | 0.1296 | 0.6401 | [-2.69, +0.43] | `No detectable trend` | CHANGED: Suggestive -> No detectable trend |
| `recent_2020` | **SW** | +0.03 | 0.9347 | 0.9795 | `No detectable trend` | 0.9745 | 0.9854 | [-1.57, +1.60] | `No detectable trend` | Retained (No detectable trend) |
| `recent_2020` | **SE** | +0.39 | 0.3106 | 0.8198 | `No detectable trend` | 0.6830 | 0.9854 | [-0.84, +1.61] | `No detectable trend` | Retained (No detectable trend) |
| `recent_2020` | **National** | -1.02 | 0.1168 | 0.3773 | `No detectable trend` | 0.1721 | 0.7609 | [-2.53, +0.51] | `No detectable trend` | Retained (No detectable trend) |

## Regional Annual Precipitation Trends (Preliminary POWER Series)

| Window | Region | Slope (mm/yr) | Before p | Before FDR q | Before Verdict | After p | After FDR q | After Calibrated 95% CI | After Calibrated Verdict | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| `full_record` | **NW** | -1.9 | < 0.0001 | < 0.0001 | `Significant` | 0.5427 | 0.9256 | [-11.04, +4.48] | `No detectable trend` | CHANGED: Significant -> No detectable trend |
| `full_record` | **NE** | -0.6 | < 0.0001 | < 0.0001 | `Significant` | 0.9068 | 0.9688 | [-15.38, +16.13] | `No detectable trend` | CHANGED: Significant -> No detectable trend |
| `full_record` | **Central** | +0.9 | < 0.0001 | < 0.0001 | `Significant` | 0.8298 | 0.9688 | [-9.75, +12.72] | `No detectable trend` | CHANGED: Significant -> No detectable trend |
| `full_record` | **SW** | +2.2 | < 0.0001 | < 0.0001 | `Significant` | 0.5165 | 0.9256 | [-7.31, +14.56] | `No detectable trend` | CHANGED: Significant -> No detectable trend |
| `full_record` | **SE** | +1.8 | < 0.0001 | < 0.0001 | `Significant` | 0.7121 | 0.9486 | [-9.35, +13.75] | `No detectable trend` | CHANGED: Significant -> No detectable trend |
| `full_record` | **National** | +2.0 | < 0.0001 | < 0.0001 | `Significant` | 0.6395 | 0.9486 | [-7.70, +12.45] | `No detectable trend` | CHANGED: Significant -> No detectable trend |
| `grace_era` | **NW** | -6.4 | 0.1064 | 0.1625 | `No detectable trend` | 0.3609 | 0.6737 | [-26.68, +7.62] | `No detectable trend` | Retained (No detectable trend) |
| `grace_era` | **NE** | +2.9 | 0.0963 | 0.1556 | `No detectable trend` | 0.8253 | 0.9552 | [-30.83, +40.10] | `No detectable trend` | Retained (No detectable trend) |
| `grace_era` | **Central** | -1.1 | 0.0205 | 0.0391 | `Significant` | 0.8802 | 0.9603 | [-29.14, +23.74] | `No detectable trend` | CHANGED: Significant -> No detectable trend |
| `grace_era` | **SW** | +6.1 | 0.0010 | 0.0019 | `Significant` | 0.5078 | 0.7876 | [-14.30, +26.97] | `No detectable trend` | CHANGED: Significant -> No detectable trend |
| `grace_era` | **SE** | +11.3 | < 0.0001 | < 0.0001 | `Significant` | 0.2911 | 0.5917 | [-9.15, +45.48] | `No detectable trend` | CHANGED: Significant -> No detectable trend |
| `grace_era` | **National** | +3.1 | 0.0006 | 0.0012 | `Significant` | 0.7689 | 0.9516 | [-18.81, +25.82] | `No detectable trend` | CHANGED: Significant -> No detectable trend |
| `grace_fo_era` | **NW** | -2.2 | 0.5123 | 0.6724 | `No detectable trend` | 0.8932 | 0.9774 | [-48.65, +64.06] | `No detectable trend` | Retained (No detectable trend) |
| `grace_fo_era` | **NE** | +26.4 | 0.9631 | 0.9797 | `No detectable trend` | 0.4925 | 0.8576 | [-47.37, +122.85] | `No detectable trend` | Retained (No detectable trend) |
| `grace_fo_era` | **Central** | +15.6 | 0.7879 | 0.8812 | `No detectable trend` | 0.6120 | 0.9399 | [-40.61, +87.38] | `No detectable trend` | Retained (No detectable trend) |
| `grace_fo_era` | **SW** | +8.2 | 0.1039 | 0.2728 | `No detectable trend` | 0.8111 | 0.9774 | [-78.90, +102.87] | `No detectable trend` | Retained (No detectable trend) |
| `grace_fo_era` | **SE** | +5.1 | 0.1814 | 0.3515 | `No detectable trend` | 0.8790 | 0.9774 | [-59.24, +80.72] | `No detectable trend` | Retained (No detectable trend) |
| `grace_fo_era` | **National** | +3.1 | 0.2428 | 0.4163 | `No detectable trend` | 0.9109 | 0.9774 | [-50.37, +69.85] | `No detectable trend` | Retained (No detectable trend) |
| `recent_2020` | **NW** | -26.6 | 0.9678 | 0.9795 | `No detectable trend` | 0.4014 | 0.9854 | [-119.36, +43.63] | `No detectable trend` | Retained (No detectable trend) |
| `recent_2020` | **NE** | -1.3 | 0.9269 | 0.9795 | `No detectable trend` | 0.9628 | 0.9854 | [-84.11, +105.69] | `No detectable trend` | Retained (No detectable trend) |
| `recent_2020` | **Central** | -7.7 | 0.7930 | 0.9795 | `No detectable trend` | 0.8143 | 0.9854 | [-95.32, +72.65] | `No detectable trend` | Retained (No detectable trend) |
| `recent_2020` | **SW** | -8.7 | 0.6069 | 0.9795 | `No detectable trend` | 0.8227 | 0.9854 | [-112.46, +95.41] | `No detectable trend` | Retained (No detectable trend) |
| `recent_2020` | **SE** | +24.1 | 0.9468 | 0.9795 | `No detectable trend` | 0.6846 | 0.9854 | [-84.00, +144.84] | `No detectable trend` | Retained (No detectable trend) |
| `recent_2020` | **National** | -28.6 | 0.5215 | 0.9795 | `No detectable trend` | 0.4613 | 0.9854 | [-115.32, +52.29] | `No detectable trend` | Retained (No detectable trend) |