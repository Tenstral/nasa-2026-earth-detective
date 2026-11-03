from pathlib import Path

readme_path = Path("README.md")
content = readme_path.read_text(encoding="utf-8")

# Update Table 2.1
old_table = """| Window | Period | Observed Months | Role | National TWS Rate | NW TWS Rate | Verdict Standard |
|---|---|:---:|---|:---:|:---:|---|
| `full_record` | **2002-04 to 2026-07** | **257** | **PRIMARY** | **-0.51 cm/yr** | **-1.25 cm/yr** | **Significant decrease** (FDR $q < 0.0001$) |
| `grace_era` | 2002-04 to 2017-06 | 161 | Epoch 1 (Literature benchmark) | -0.40 cm/yr | -1.13 cm/yr | **Significant decrease** (FDR $q < 0.0001$) |
| `grace_fo_era` | 2018-06 to 2026-07 | 96 | Epoch 2 (Single-instrument) | -0.47 cm/yr | -1.67 cm/yr | Suggestive decrease (Raw $p < 0.05$) |
| `recent_2020` | 2020-01 to 2026-07 | 79 | Sensitivity / v2 comparability | -1.02 cm/yr | -2.93 cm/yr | Suggestive decrease (Raw $p < 0.05$) |"""

new_table = """| Window | Period | Observed Months | Role | National TWS Rate [95% CI] | NW TWS Rate [95% CI] | Calibrated Verdict (ESS-MK) |
|---|---|:---:|---|:---:|:---:|---|
| `full_record` | **2002-04 to 2026-07** | **257** | **PRIMARY** | **-0.51 [-0.65, -0.37]** | **-1.25 [-1.49, -1.01]** | **Significant decrease** (FDR $q < 0.0001$) |
| `grace_era` | 2002-04 to 2017-06 | 161 | Transition-free baseline | -0.68 [-0.92, -0.44] | -1.56 [-1.95, -1.15] | **Significant decrease** (FDR $q < 0.0001$) |
| `grace_fo_era` | 2018-06 to 2026-07 | 96 | Single-instrument era | -0.47 [-1.34, +0.44] | -1.67 [-3.32, +0.06] | No detectable trend (CI includes zero) |
| `recent_2020` | 2020-01 to 2026-07 | 79 | Sensitivity / legacy window | -1.02 [-3.05, +0.94] | -2.93 [-4.90, -0.57] | Method-dependent (NW raw $p=0.0107$, FDR $q=0.0772$) |"""

assert old_table in content, "Could not find old_table in README.md"
content = content.replace(old_table, new_table)

# Ensure no other forbidden words
readme_path.write_text(content, encoding="utf-8")
print("Updated README.md")
