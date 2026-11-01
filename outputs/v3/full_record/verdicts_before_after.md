# Task 1 Calibration: Before-vs-After Significance Verdict Table

**Status:** PRELIMINARY — Comparison of Significance Calibration across all 4 Windows
- **Before Engine:** Hamed-Rao Modified Mann-Kendall with circular block-bootstrap CI (Uncalibrated; FPR 14–26%).
- **After Engine:** Calibrated Effective-Sample-Size (ESS) Mann-Kendall with duality-aligned Theil-Sen CI (FPR 5.0–5.8%, CI coverage 94.2–95.0%).

## Regional Annual Total Water Storage (TWS) Trends

| Window | Region | Slope (cm/yr) | Before p | Before FDR q | Before Verdict | After p | After FDR q | After Calibrated 95% CI | After Calibrated Verdict | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| `full_record` | **NW** | -1.25 | < 0.0001 | < 0.0001 | `Significant` | < 0.0001 | < 0.0001 | [-1.50, -1.02] | **`Significant`** | Unchanged (Significant) |
| `full_record` | **NE** | -0.56 | < 0.0001 | < 0.0001 | `Significant` | < 0.0001 | < 0.0001 | [-0.70, -0.42] | **`Significant`** | Unchanged (Significant) |
| `full_record` | **Central** | -0.47 | < 0.0001 | < 0.0001 | `Significant` | < 0.0001 | < 0.0001 | [-0.62, -0.34] | **`Significant`** | Unchanged (Significant) |
| `full_record` | **SW** | -0.05 | 0.3715 | 0.4217 | `No detectable trend` | 0.5459 | 0.6114 | [-0.20, +0.10] | `No detectable trend` | Unchanged (No detectable trend) |
| `full_record` | **SE** | -0.05 | 0.2581 | 0.3011 | `No detectable trend` | 0.3754 | 0.4380 | [-0.17, +0.06] | `No detectable trend` | Unchanged (No detectable trend) |
| `full_record` | **National** | -0.51 | < 0.0001 | < 0.0001 | `Significant` | < 0.0001 | < 0.0001 | [-0.66, -0.38] | **`Significant`** | Unchanged (Significant) |
| `grace_era` | **NW** | -1.56 | < 0.0001 | < 0.0001 | `Significant` | < 0.0001 | < 0.0001 | [-1.96, -1.17] | **`Significant`** | Unchanged (Significant) |
| `grace_era` | **NE** | -0.72 | < 0.0001 | < 0.0001 | `Significant` | < 0.0001 | < 0.0001 | [-0.99, -0.49] | **`Significant`** | Unchanged (Significant) |
| `grace_era` | **Central** | -0.63 | < 0.0001 | < 0.0001 | `Significant` | < 0.0001 | < 0.0001 | [-0.86, -0.42] | **`Significant`** | Unchanged (Significant) |
| `grace_era` | **SW** | -0.13 | 0.1250 | 0.1875 | `No detectable trend` | 0.2896 | 0.3988 | [-0.36, +0.10] | `No detectable trend` | Unchanged (No detectable trend) |
| `grace_era` | **SE** | -0.12 | 0.0897 | 0.1478 | `No detectable trend` | 0.2296 | 0.3269 | [-0.32, +0.07] | `No detectable trend` | Unchanged (No detectable trend) |
| `grace_era` | **National** | -0.68 | < 0.0001 | < 0.0001 | `Significant` | < 0.0001 | < 0.0001 | [-0.92, -0.45] | **`Significant`** | Unchanged (Significant) |
| `grace_fo_era` | **NW** | -1.67 | 0.0283 | 0.1249 | `Suggestive` | 0.0549 | 0.3841 | [-3.32, +0.06] | `No detectable trend` | CHANGED: Suggestive -> No detectable trend |
| `grace_fo_era` | **NE** | -0.79 | 0.0269 | 0.1249 | `Suggestive` | 0.1073 | 0.4752 | [-1.78, +0.19] | `No detectable trend` | CHANGED: Suggestive -> No detectable trend |
| `grace_fo_era` | **Central** | -0.81 | 0.0141 | 0.0790 | `Suggestive` | 0.1056 | 0.4752 | [-1.79, +0.20] | `No detectable trend` | CHANGED: Suggestive -> No detectable trend |
| `grace_fo_era` | **SW** | +0.53 | 0.1513 | 0.3345 | `No detectable trend` | 0.3419 | 0.6348 | [-0.63, +1.53] | `No detectable trend` | Unchanged (No detectable trend) |
| `grace_fo_era` | **SE** | +0.45 | 0.1270 | 0.2964 | `No detectable trend` | 0.1848 | 0.5009 | [-0.27, +1.18] | `No detectable trend` | Unchanged (No detectable trend) |
| `grace_fo_era` | **National** | -0.47 | 0.2125 | 0.3797 | `No detectable trend` | 0.3111 | 0.6158 | [-1.50, +0.53] | `No detectable trend` | Unchanged (No detectable trend) |
| `recent_2020` | **NW** | -2.93 | 0.0002 | 0.0038 | `Significant` | 0.0107 | 0.0819 | [-4.97, -0.78] | `Suggestive` | CHANGED: Significant -> Suggestive |
| `recent_2020` | **NE** | -1.06 | 0.0875 | 0.3063 | `No detectable trend` | 0.1682 | 0.7228 | [-2.64, +0.46] | `No detectable trend` | Unchanged (No detectable trend) |
| `recent_2020` | **Central** | -1.19 | 0.0309 | 0.1526 | `Suggestive` | 0.1296 | 0.6401 | [-2.69, +0.43] | `No detectable trend` | CHANGED: Suggestive -> No detectable trend |
| `recent_2020` | **SW** | +0.03 | 0.9347 | 0.9795 | `No detectable trend` | 0.9506 | 0.9865 | [-1.60, +1.49] | `No detectable trend` | Unchanged (No detectable trend) |
| `recent_2020` | **SE** | +0.39 | 0.3106 | 0.8198 | `No detectable trend` | 0.4069 | 0.9865 | [-0.80, +1.43] | `No detectable trend` | Unchanged (No detectable trend) |
| `recent_2020` | **National** | -1.02 | 0.1168 | 0.3773 | `No detectable trend` | 0.1721 | 0.7228 | [-2.53, +0.51] | `No detectable trend` | Unchanged (No detectable trend) |

## Regional Annual Precipitation Trends (Preliminary POWER Series)

| Window | Region | Slope (mm/yr) | Before p | Before FDR q | Before Verdict | After p | After FDR q | After Calibrated 95% CI | After Calibrated Verdict | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| `full_record` | **NW** | +29.1 | < 0.0001 | < 0.0001 | `Significant` | < 0.0001 | < 0.0001 | [+16.51, +42.82] | **`Significant`** | Unchanged (Significant) |
| `full_record` | **NE** | +54.4 | < 0.0001 | < 0.0001 | `Significant` | < 0.0001 | < 0.0001 | [+29.97, +83.45] | **`Significant`** | Unchanged (Significant) |
| `full_record` | **Central** | +47.7 | < 0.0001 | < 0.0001 | `Significant` | < 0.0001 | < 0.0001 | [+29.41, +67.91] | **`Significant`** | Unchanged (Significant) |
| `full_record` | **SW** | +73.2 | < 0.0001 | < 0.0001 | `Significant` | < 0.0001 | < 0.0001 | [+39.13, +111.00] | **`Significant`** | Unchanged (Significant) |
| `full_record` | **SE** | +85.9 | < 0.0001 | < 0.0001 | `Significant` | < 0.0001 | < 0.0001 | [+48.44, +130.10] | **`Significant`** | Unchanged (Significant) |
| `full_record` | **National** | +60.3 | < 0.0001 | < 0.0001 | `Significant` | < 0.0001 | < 0.0001 | [+36.66, +86.34] | **`Significant`** | Unchanged (Significant) |
| `grace_era` | **NW** | +10.2 | 0.1064 | 0.1625 | `No detectable trend` | 0.1363 | 0.2437 | [-3.60, +33.40] | `No detectable trend` | Unchanged (No detectable trend) |
| `grace_era` | **NE** | +25.1 | 0.0963 | 0.1556 | `No detectable trend` | 0.1534 | 0.2545 | [-9.14, +70.95] | `No detectable trend` | Unchanged (No detectable trend) |
| `grace_era` | **Central** | +30.1 | 0.0205 | 0.0391 | `Significant` | 0.0453 | 0.0866 | [+0.35, +67.90] | `Suggestive` | CHANGED: Significant -> Suggestive |
| `grace_era` | **SW** | +74.1 | 0.0010 | 0.0019 | `Significant` | 0.0004 | 0.0014 | [+28.31, +132.05] | **`Significant`** | Unchanged (Significant) |
| `grace_era` | **SE** | +127.5 | < 0.0001 | < 0.0001 | `Significant` | < 0.0001 | < 0.0001 | [+61.38, +206.49] | **`Significant`** | Unchanged (Significant) |
| `grace_era` | **National** | +54.9 | 0.0006 | 0.0012 | `Significant` | 0.0010 | 0.0028 | [+20.54, +98.38] | **`Significant`** | Unchanged (Significant) |
| `grace_fo_era` | **NW** | +12.1 | 0.5123 | 0.6724 | `No detectable trend` | 0.5123 | 0.7227 | [-33.67, +68.60] | `No detectable trend` | Unchanged (No detectable trend) |
| `grace_fo_era` | **NE** | +1.1 | 0.9631 | 0.9797 | `No detectable trend` | 0.9697 | 0.9871 | [-96.68, +116.70] | `No detectable trend` | Unchanged (No detectable trend) |
| `grace_fo_era` | **Central** | -8.2 | 0.7879 | 0.8812 | `No detectable trend` | 0.8192 | 0.9023 | [-79.43, +71.70] | `No detectable trend` | Unchanged (No detectable trend) |
| `grace_fo_era` | **SW** | -116.1 | 0.1039 | 0.2728 | `No detectable trend` | 0.1320 | 0.4752 | [-311.55, +35.85] | `No detectable trend` | Unchanged (No detectable trend) |
| `grace_fo_era` | **SE** | -109.8 | 0.1814 | 0.3515 | `No detectable trend` | 0.1269 | 0.4752 | [-258.75, +21.90] | `No detectable trend` | Unchanged (No detectable trend) |
| `grace_fo_era` | **National** | -39.6 | 0.2428 | 0.4163 | `No detectable trend` | 0.3019 | 0.6158 | [-137.54, +45.21] | `No detectable trend` | Unchanged (No detectable trend) |
| `recent_2020` | **NW** | +1.2 | 0.9678 | 0.9795 | `No detectable trend` | 0.9746 | 0.9865 | [-75.24, +91.66] | `No detectable trend` | Unchanged (No detectable trend) |
| `recent_2020` | **NE** | -1.2 | 0.9269 | 0.9795 | `No detectable trend` | 0.9393 | 0.9865 | [-122.27, +134.72] | `No detectable trend` | Unchanged (No detectable trend) |
| `recent_2020` | **Central** | +11.8 | 0.7930 | 0.9795 | `No detectable trend` | 0.8330 | 0.9865 | [-89.39, +139.03] | `No detectable trend` | Unchanged (No detectable trend) |
| `recent_2020` | **SW** | -39.4 | 0.6069 | 0.9795 | `No detectable trend` | 0.6340 | 0.9865 | [-232.62, +142.24] | `No detectable trend` | Unchanged (No detectable trend) |
| `recent_2020` | **SE** | -5.2 | 0.9468 | 0.9795 | `No detectable trend` | 0.9502 | 0.9865 | [-203.83, +164.58] | `No detectable trend` | Unchanged (No detectable trend) |
| `recent_2020` | **National** | -21.4 | 0.5215 | 0.9795 | `No detectable trend` | 0.6582 | 0.9865 | [-150.21, +109.23] | `No detectable trend` | Unchanged (No detectable trend) |