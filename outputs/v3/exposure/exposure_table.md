# Socioeconomic Exposure: Bangladesh Water Storage and Rainfall Coupling

> **PRELIMINARY — NASA Space Apps Challenge 2026**
> **Team Tenstral | Project: Bengal Hydro Detective**
> Integrated exposure analysis connecting satellite gravimetry verdicts and primary precipitation trends to gridded human population and satellite cropland classification.

---

## 1. Regional Socioeconomic, Storage & Rainfall Exposure Table

| Region | Population (Millions) | National Pop Share | Cropland (%) | TWS Slope (cm/yr) [95% CI] | TWS Verdict (FDR q) | IMERG Rain Slope (mm/yr) [95% CI] | Rain Verdict (FDR q) | Hydrological Coupling |
|---|---|---|---|---|---|---|---|---|
| **NW** | 38.81 M | 22.9% | 74.2% | -1.25 [-1.50, -1.02] | **`Significant`** (q=< 0.0001) | -1.91 [-11.04, +4.48] | `No detectable trend` (q=0.8968) | `TWS decline, no detectable rainfall trend` |
| **NE** | 24.05 M | 14.2% | 58.6% | -0.56 [-0.70, -0.42] | **`Significant`** (q=< 0.0001) | -0.59 [-15.38, +16.13] | `No detectable trend` (q=0.9342) | `TWS decline, no detectable rainfall trend` |
| **Central** | 45.64 M | 26.9% | 56.4% | -0.47 [-0.62, -0.34] | **`Significant`** (q=< 0.0001) | +0.89 [-9.75, +12.72] | `No detectable trend` (q=0.9342) | `TWS decline, no detectable rainfall trend` |
| **SW** | 27.14 M | 16.0% | 48.7% | -0.05 [-0.20, +0.10] | **`No detectable trend`** (q=0.8968) | +2.25 [-7.31, +14.56] | `No detectable trend` (q=0.8968) | `No detectable trend (below detection limit)` |
| **SE** | 34.18 M | 20.1% | 32.1% | -0.05 [-0.17, +0.06] | **`No detectable trend`** (q=0.8968) | +1.76 [-9.35, +13.75] | `No detectable trend` (q=0.9342) | `No detectable trend (below detection limit)` |
| **National** | 169.83 M | 100.0% | 57.8% | -0.51 [-0.66, -0.38] | **`Significant`** (q=< 0.0001) | +2.04 [-7.70, +12.45] | `No detectable trend` (q=0.9342) | `TWS decline, no detectable rainfall trend` |

---

## 2. Standardized Descriptive Exposure Statements

- **NW:** *"Approximately 38.81 million people (GPWv4, 2020) and 74.2% of land classified as cropland (MODIS MCD12Q1, 2022) are in the NW region, where regional-mean total water storage declined significantly (-1.25 cm/yr, FDR q = < 0.0001) in the absence of a detected rainfall trend (-1.91 mm/yr, FDR q = 0.8968) over the full 2002–2026 record, classified as TWS decline, no detectable rainfall trend."*

- **NE:** *"Approximately 24.05 million people (GPWv4, 2020) and 58.6% of land classified as cropland (MODIS MCD12Q1, 2022) are in the NE region, where regional-mean total water storage declined significantly (-0.56 cm/yr, FDR q = < 0.0001) in the absence of a detected rainfall trend (-0.59 mm/yr, FDR q = 0.9342) over the full 2002–2026 record, classified as TWS decline, no detectable rainfall trend."*

- **Central:** *"Approximately 45.64 million people (GPWv4, 2020) and 56.4% of land classified as cropland (MODIS MCD12Q1, 2022) are in the Central region, where regional-mean total water storage declined significantly (-0.47 cm/yr, FDR q = < 0.0001) in the absence of a detected rainfall trend (+0.89 mm/yr, FDR q = 0.9342) over the full 2002–2026 record, classified as TWS decline, no detectable rainfall trend."*

- **SW:** *"Approximately 27.14 million people (GPWv4, 2020) and 48.7% of land classified as cropland (MODIS MCD12Q1, 2022) are in the SW region, where regional-mean total water storage showed no detectable trend (-0.05 cm/yr, FDR q = 0.8968) and primary precipitation showed no detectable trend (+2.25 mm/yr, FDR q = 0.8968) over the full 2002–2026 record, classified as No detectable trend (below detection limit)."*

- **SE:** *"Approximately 34.18 million people (GPWv4, 2020) and 32.1% of land classified as cropland (MODIS MCD12Q1, 2022) are in the SE region, where regional-mean total water storage showed no detectable trend (-0.05 cm/yr, FDR q = 0.8968) and primary precipitation showed no detectable trend (+1.76 mm/yr, FDR q = 0.9342) over the full 2002–2026 record, classified as No detectable trend (below detection limit)."*

- **National:** *"Approximately 169.83 million people (GPWv4, 2020) and 57.8% of land classified as cropland (MODIS MCD12Q1, 2022) are in the National region, where regional-mean total water storage declined significantly (-0.51 cm/yr, FDR q = < 0.0001) in the absence of a detected rainfall trend (+2.04 mm/yr, FDR q = 0.9342) over the full 2002–2026 record, classified as TWS decline, no detectable rainfall trend."*


---

## 3. Key Exposure Findings

1. **Massive Human and Agricultural Exposure in the Depletion Corridor:**
   - The primary depletion hotspot (the **Northwest region**, Rajshahi + Rangpur) supports **38.81 million people** (22.9% of Bangladesh) and possesses the nation's highest concentration of intensive cropland (**74.2%** of surface area).
   - Combined with the **Central region** (Dhaka: 45.64M people) and **Northeast** (Sylhet + Mymensingh: 24.05M people), a total of **108.5 million people (63.9% of the national population)** live in regions where regional-mean total water storage declined significantly over the full 2002–2026 record in the absence of a detected rainfall trend.
   - Crucially, across all three regions, primary precipitation (GPM IMERG) exhibits **no detectable trend** (-1.9 to +0.9 mm/yr, p >= 0.54), indicating that this exposure is consistent with intensive irrigation abstraction exceeding recharge rather than rainfall deficit.

2. **Southern Stability and Ecological Constraints:**
   - Southern divisions (Khulna, Barishal, Chattogram) show **no detectable multi-decadal storage trend** (-0.05 cm/yr) and **no detectable rainfall trend** (+1.8 to +2.3 mm/yr).
   - *(Untested hypothesis)*: It has been hypothesized that southern stability is influenced by coastal estuarine buffering and lower dry-season abstraction relative to the north, but this mechanism has not been verified with in-situ data in this study.
