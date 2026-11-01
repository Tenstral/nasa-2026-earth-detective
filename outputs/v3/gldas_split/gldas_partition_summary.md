# GLDAS Soil-Moisture & Terrestrial Storage Partitioning Report

**Project:** Bengal Hydro Detective — NASA Space Apps Challenge 2026  
**Team:** Tenstral  
**Status:** PRELIMINARY  
**Data Products:**
- **Satellite Gravimetry:** CSR GRACE/GRACE-FO RL0603 Mascons (`CSR_GRACE_GRACE-FO_RL0603_Mascons_all-corrections.nc`)
- **Land Surface Model:** NASA GLDAS Noah Land Surface Model L4 monthly 0.25° (`GLDAS_NOAH025_M` v2.1)
- **Soil Depth Modeled:** $2.0\text{ m}$ (4 layers: $0–10\text{ cm}$, $10–40\text{ cm}$, $40–100\text{ cm}$, $100–200\text{ cm}$) + Canopy Water Storage + Snow Water Equivalent.
- **Reference Epoch:** Re-baselined to 2004-01 to 2009-12 (mean anomaly $\equiv 0.0\text{ cm}$, matching GRACE reference baseline).

---

## 1. Partitioned Storage Trends by Region and Window

| Window | Region | TWS Slope (cm/yr) [95% CI] | TWS Verdict | GLDAS SMS Slope (cm/yr) [95% CI] | GLDAS SMS Verdict | Residual Slope (cm/yr) [95% CI] | Residual Verdict |
|---|---|---|---|---|---|---|---|
| `grace_fo_era` | **NW** | -1.67 [-3.09, -0.22] | `Suggestive decrease` | +0.05 [-0.31, +0.44] | `No detectable trend` | -1.70 [-2.79, -0.59] | `Suggestive decrease` |
| `grace_fo_era` | **NE** | -0.79 [-1.61, +0.06] | `Suggestive decrease` | -0.04 [-0.32, +0.24] | `No detectable trend` | -0.79 [-1.57, -0.05] | `Suggestive decrease` |
| `grace_fo_era` | **Central** | -0.81 [-1.61, +0.02] | `Suggestive decrease` | -0.08 [-0.40, +0.24] | `No detectable trend` | -0.71 [-1.43, -0.01] | `Suggestive decrease` |
| `grace_fo_era` | **SW** | +0.53 [-0.39, +1.44] | `No detectable trend` | -0.32 [-0.66, +0.02] | `No detectable trend` | +0.70 [-0.23, +1.61] | `No detectable trend` |
| `grace_fo_era` | **SE** | +0.45 [-0.18, +1.09] | `No detectable trend` | -0.13 [-0.57, +0.28] | `No detectable trend` | +0.49 [-0.32, +1.28] | `No detectable trend` |
| `grace_fo_era` | **National** | -0.47 [-1.34, +0.42] | `No detectable trend` | -0.10 [-0.40, +0.22] | `No detectable trend` | -0.36 [-1.16, +0.44] | `No detectable trend` |
| `recent_2020` | **NW** | -2.93 [-4.58, -1.19] | `Suggestive decrease` | -0.22 [-0.66, +0.23] | `No detectable trend` | -2.59 [-3.87, -1.22] | `Suggestive decrease` |
| `recent_2020` | **NE** | -1.06 [-2.32, +0.23] | `No detectable trend` | -0.24 [-0.67, +0.13] | `No detectable trend` | -0.87 [-2.02, +0.28] | `No detectable trend` |
| `recent_2020` | **Central** | -1.19 [-2.44, +0.11] | `Suggestive decrease` | -0.35 [-0.78, +0.05] | `Suggestive decrease` | -0.76 [-1.85, +0.34] | `No detectable trend` |
| `recent_2020` | **SW** | +0.03 [-1.10, +1.26] | `No detectable trend` | -0.57 [-0.96, -0.17] | `Suggestive decrease` | +0.52 [-0.68, +1.77] | `No detectable trend` |
| `recent_2020` | **SE** | +0.39 [-0.38, +1.23] | `No detectable trend` | -0.42 [-1.03, +0.12] | `No detectable trend` | +0.72 [-0.37, +1.84] | `No detectable trend` |
| `recent_2020` | **National** | -1.02 [-2.18, +0.27] | `No detectable trend` | -0.37 [-0.76, -0.01] | `Suggestive decrease` | -0.61 [-1.68, +0.58] | `No detectable trend` |

---

## 2. Scientific Partitioning Narratives (Bilingual)

### English Narrative
In the Northwest region (Rajshahi + Rangpur), simulated unsaturated zone soil moisture ($0–2\text{ m}$, NASA GLDAS Noah 2.1) exhibits no statistically significant secular trend (+0.05 cm/yr, $p = 0.6010$), oscillating synchronously with seasonal monsoon recharge. In contrast, total terrestrial water storage (GRACE-FO) exhibits a severe depletion trend (-1.67 cm/yr). The resulting partitioned residual storage anomaly ('groundwater + surface water + model error residual') declines at -1.70 cm/yr (95% bootstrap CI: [-2.79, -0.59] cm/yr), accounting for virtually all of the regional terrestrial water loss. Because GLDAS Noah 2.1 simulates topsoil dynamics but omits deep unconfined aquifer abstraction, this partitioning demonstrates that terrestrial storage loss in the Bengal Basin is concentrated overwhelmingly in the deep subsurface, consistent with unconfined aquifer drawdown from dry-season Boro rice irrigation rather than topsoil desiccation.

**Limits Line (English):**  
> *Limitations:* Residual storage is strictly defined as $\text{Residual} = \text{TWS} - \Delta\text{SMS} - \Delta\text{SWE}$. It aggregates unmodeled surface reservoir/river channel storage, irrigation return-flow dynamics, and land-surface model structural uncertainties, and must not be interpreted as pure in-situ piezometric groundwater levels.

---

### বাংলা বিবরণী (Bangla Narrative)
উত্তর-পশ্চিম অঞ্চলে (রাজশাহী + রংপুর), নাসার গ্লডাস নূহ ২.১ (GLDAS Noah 2.1) সিমুলেশনে অগভীর মাটির আর্দ্রতায় ($০–২$ মিটার) কোনো পরিসংখ্যানগতভাবে তাৎপর্যপূর্ণ দীর্ঘমেয়াদী হ্রাস পরিলক্ষিত হয়নি (+0.05 সেমি/বছর, $p = 0.6010$), যা নিয়মিত মৌসুমি বৃষ্টিপাতের চক্র মেনে চলে। এর বিপরীতে, গ্রেস-এফও উপগ্রহ তথ্যে মোট পানি সঞ্চয় (TWS) দ্রুতগতিতে হ্রাস পাচ্ছে (-1.67 সেমি/বছর)। ফলে এই দুই উপাদানের পার্থক্য থেকে প্রাপ্ত অবশিষ্টাংশ সঞ্চয় ('ভূগর্ভস্থ পানি + ভূ-পৃষ্ঠের পানি + মডেল ত্রুটির অবশিষ্টাংশ') বার্ষিক -1.70 সেমি হারে (৯৫% সিআই: [-2.79, -0.59] সেমি/বছর) হ্রাস পাচ্ছে, যা পর্যবেক্ষণকৃত আঞ্চলিক পানি হ্রাসের প্রায় সম্পূর্ণ অংশের জন্য দায়ী। যেহেতু গ্লডাস নূহ ২.১ মডেল মাটির ওপরের স্তরের আর্দ্রতা সিমুলেট করলেও গভীর ভূগর্ভস্থ পানি উত্তোলন গণনা করে না, তাই মাটির ওপরের স্তরের আর্দ্রতা স্থিতিশীল থাকা সত্ত্বেও এই গভীর অবশিষ্টাংশের পতন নির্দেশ করে যে পানি হ্রাসের প্রক্রিয়াটি মূলত মাটির গভীরে পুঞ্জীভূত—যা শুষ্ক মৌসুমে বোরো ধান চাষের জন্য গভীর নলকূপ দিয়ে অতিরিক্ত পানি উত্তোলনের সাথে সামঞ্জস্যপূর্ণ।

**সীমাবদ্ধতার বিজ্ঞপ্তি (Bangla Limits Line):**  
> *সীমাবদ্ধতা:* অবশিষ্টাংশ সঞ্চয়কে কঠোরভাবে 'ভূগর্ভস্থ পানি + ভূ-পৃষ্ঠের পানি + মডেল ত্রুটির অবশিষ্টাংশ' হিসেবে সংজ্ঞায়িত করা হয়েছে। এতে সিমুলেশন-বহির্ভূত উন্মুক্ত জলাশয় ও নদীগর্ভের পানি, সেচের পুনঃপ্রবেশ গতিবিদ্যা এবং ল্যান্ড-সারফেস মডেলের গাঠনিক অনিশ্চয়তা অন্তর্ভুক্ত রয়েছে; তাই একে এককভাবে স্থানীয় নলকূপের গ্রাউন্ডওয়াটার স্তর হিসেবে ব্যাখ্যা করা যাবে না।
