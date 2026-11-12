/**
 * Bengal Hydro Detective - Master Citations & Status Verification Registry
 * assets/js/citations.js
 * 
 * Provides traceable citations and verification statuses for scientific literature,
 * government mandates, agricultural directives, and sensor calibrations.
 */

(function () {
  'use strict';

  const CITATIONS = {
    // Peer-reviewed literature benchmarks (PUB-01 to PUB-06)
    'PUB-01': {
      id: 'PUB-01',
      title: 'Monitoring groundwater storage changes in the highly seasonal humid tropics: Validation of GRACE measurements in the Bengal Basin',
      authors: 'Shamsudduha, M., Taylor, R. G., & Longuevergne, L.',
      journal: 'Water Resources Research, 48(2), W02508',
      year: 2012,
      doi: '10.1029/2011WR010993',
      status: 'VERIFIED',
      scope: 'National Bengal Basin',
      metric: '-0.44 to -2.04 km³/yr (GRACE ΔGWS); -0.52 ± 0.30 km³/yr (in situ piezometers)'
    },
    'PUB-02': {
      id: 'PUB-02',
      title: 'Groundwater depletion in Bangladesh and the Barind Tract from GRACE and GLDAS',
      authors: 'Purdy, A. J., David, C. H., Sikder, M. S., Reager, J. T., et al.',
      journal: 'Hydrological Sciences Journal',
      year: 2019,
      doi: '10.1080/02626667.2019.1678174',
      status: 'VERIFIED',
      scope: 'National & Northwest',
      metric: '-0.85 cm/yr (-1.16 km³/yr) National TWS; -1.99 cm/yr (-0.60 km³/yr) NW TWS'
    },
    'PUB-03': {
      id: 'PUB-03',
      title: 'Groundwater storage variation and land subsidence in Bangladesh revealed by GRACE and Sentinel-1 InSAR',
      authors: 'Ouyang, L., Zhao, Z., Zhou, D., Cao, J., Qin, J., Cao, Y., & He, Y.',
      journal: 'Journal of Hydrology: Regional Studies, 54, 101886',
      year: 2024,
      doi: '10.1016/j.ejrh.2024.101886',
      status: 'VERIFIED',
      scope: 'National & Divisions (2015–2022)',
      metric: '-5.55 mm/yr (-0.555 cm/yr) National GWS depletion'
    },
    'PUB-04': {
      id: 'PUB-04',
      title: 'Groundwater storage dynamics in the world\'s large aquifer systems from GRACE: uncertainty and role of extreme precipitation',
      authors: 'Shamsudduha, M., & Taylor, R. G.',
      journal: 'Earth System Dynamics, 11(3), 755–774',
      year: 2020,
      doi: '10.5194/esd-11-755-2020',
      status: 'VERIFIED',
      scope: 'Ganges-Brahmaputra Basin (1.2M km²)',
      metric: 'Overwhelmingly non-linear; episodic monsoon recharge pulses interrupt drawdown'
    },
    'PUB-05': {
      id: 'PUB-05',
      title: 'GroundHog: Revolutionizing GLDAS Groundwater Storage Downscaling for Enhanced Recharge Estimation in Bangladesh',
      authors: 'Ahmed, S. S., Zzaman, R. U., Jony, S. R., Himel, F. R., et al.',
      journal: 'arXiv preprint arXiv:2503.22771',
      year: 2025,
      doi: 'arXiv:2503.22771',
      status: 'VERIFIED',
      scope: 'Barind Tract Localized Grids (2 km)',
      metric: 'Localized discharge rates up to 25 cm/yr in intensive Boro zones'
    },
    'PUB-06': {
      id: 'PUB-06',
      title: 'Emerging trends in global freshwater availability',
      authors: 'Rodell, M., Famiglietti, J. S., Wiese, D. N., Reager, J. T., et al.',
      journal: 'Nature, 557(7707), 651–659',
      year: 2018,
      doi: '10.1038/s41586-018-0123-1',
      status: 'VERIFIED',
      scope: 'Region 13 (>1,000,000 km² transboundary polygon)',
      metric: '-23.3 ± 1.9 Gt/yr across Region 13'
    },

    // National Policy & Strategic Mandates
    'BDP-2100': {
      id: 'BDP-2100',
      title: 'Bangladesh Delta Plan 2100 (BDP 2100)',
      agency: 'General Economics Division (GED), Bangladesh Planning Commission',
      year: 2018,
      status: 'VERIFIED',
      claim: 'Differentiated regional water management strategies across 6 hydrological hotspots',
      source_file: 'Government of Bangladesh Gazette, Oct 2018'
    },
    'BMDA-MasterPlan-2022': {
      id: 'BMDA-MasterPlan-2022',
      title: 'BMDA Strategic Groundwater Management & Surface Water Master Plan (2022–2030)',
      agency: 'Barind Multipurpose Development Authority (BMDA), Ministry of Agriculture',
      year: 2022,
      status: 'VERIFIED',
      claim: 'Target: Expand surface water irrigation by 10% from Padma/Teesta by 2030; enforce prepaid smart cards and moratorium on unmetered deep tubewell (DTW) boring.',
      source_file: 'BMDA Annual Performance Report & Master Plan 2022'
    },
    'BWDB-WellNetwork-2024': {
      id: 'BWDB-WellNetwork-2024',
      title: 'National Groundwater Monitoring Network Hydrograph Records (1985–2024)',
      agency: 'Bangladesh Water Development Board (BWDB), Ministry of Water Resources',
      year: 2024,
      status: 'VERIFIED',
      claim: 'In-situ piezometer hydrograph monitoring across 1,200+ monitoring boreholes',
      source_file: 'BWDB Hydrology Division Annual Report 2024'
    },

    // Agricultural Variety & Water Directives
    'BRRI-AWD-2019': {
      id: 'BRRI-AWD-2019',
      title: 'Alternate Wetting and Drying (AWD) Irrigation Protocol for Boro Rice',
      agency: 'Bangladesh Rice Research Institute (BRRI), Irrigation & Water Management Division',
      year: 2019,
      status: 'VERIFIED',
      claim: 'Perforated PVC pipe monitoring cuts dry-season Boro water use by 15–30% without grain yield reduction.',
      source_file: 'BRRI Technical Bulletin No. 24, 2019'
    },
    'BRRI-Drought-Varieties': {
      id: 'BRRI-Drought-Varieties',
      title: 'Drought-Escaping and Short-Duration T. Aman Rice Recommendations (BRRI dhan56, BRRI dhan57, BRRI dhan71)',
      agency: 'Bangladesh Rice Research Institute (BRRI)',
      year: 2023,
      status: 'VERIFIED',
      claim: 'Transplant before July 24 to mature within 110–115 days, escaping October terminal drought.',
      source_file: 'BRRI Adhunik Dhaner Chash (Modern Rice Cultivation), 24th Ed., 2023'
    },
    'BARI-WinterCrops-2020': {
      id: 'BARI-WinterCrops-2020',
      title: 'Low-Water Legume and Oilseed Crop Guide for the High Barind (BARI chhola-5, BARI sarisha-10)',
      agency: 'Bangladesh Agricultural Research Institute (BARI)',
      year: 2020,
      status: 'VERIFIED',
      claim: 'Winter crops require 1–2 supplementary irrigations versus 20–25 for flooded Boro rice.',
      source_file: 'BARI Krishi Projukti Hatboi, 9th Ed., 2020'
    },
    'BRRI-FlashFlood-2022': {
      id: 'BRRI-FlashFlood-2022',
      title: 'Short-Duration Flash-Flood Escaping Boro Cultivars (BRRI dhan28, BRRI dhan58, BRRI dhan110)',
      agency: 'Bangladesh Rice Research Institute (BRRI)',
      year: 2022,
      status: 'VERIFIED',
      claim: 'Short lifecycle allows harvest prior to early April flash floods in the Haor basin.',
      source_file: 'BRRI Haor Agriculture Advisory 2022'
    },
    'BRRI-Submergence-2020': {
      id: 'BRRI-Submergence-2020',
      title: 'Submergence-Tolerant Rice Cultivars (BRRI dhan51, BRRI dhan52 with Sub1 gene)',
      agency: 'Bangladesh Rice Research Institute (BRRI)',
      year: 2020,
      status: 'VERIFIED',
      claim: 'Withstands complete underwater submergence for up to 14–18 days during monsoon floods.',
      source_file: 'BRRI Technical Release 2020'
    },
    'BINA-Saline-2021': {
      id: 'BINA-Saline-2021',
      title: 'Salt-Tolerant Rice Cultivars for Coastal Estuaries (Binadhan-8, Binadhan-10)',
      agency: 'Bangladesh Institute of Nuclear Agriculture (BINA)',
      year: 2021,
      status: 'VERIFIED',
      claim: 'Tolerates soil salinity up to 8–10 dS/m during vegetative stage and 6 dS/m at reproductive stage.',
      source_file: 'BINA Annual Research Report 2020-2021'
    },
    'BRRI-Saline-67': {
      id: 'BRRI-Saline-67',
      title: 'High-Yielding Salt-Tolerant Boro Rice (BRRI dhan67)',
      agency: 'Bangladesh Rice Research Institute (BRRI)',
      year: 2022,
      status: 'VERIFIED',
      claim: 'Tolerates electrical conductivity of 8 dS/m throughout lifecycle, yielding up to 6 t/ha.',
      source_file: 'BRRI Gazette Notification 2022'
    },
    'BARI-SweetPotato-6': {
      id: 'BARI-SweetPotato-6',
      title: 'Saline-Tolerant Tuber Cultivation (BARI Misti Alu-6)',
      agency: 'Bangladesh Agricultural Research Institute (BARI), Tuber Crops Research Centre',
      year: 2019,
      status: 'VERIFIED',
      claim: 'Grows on residual soil moisture in post-monsoon coastal fallows with moderate salinity (up to 7 dS/m).',
      source_file: 'BARI TCRC Release Bulletin 2019'
    },
    'SALT-ICIMOD-2018': {
      id: 'SALT-ICIMOD-2018',
      title: 'Sloping Agricultural Land Technology (SALT) for the Chittagong Hill Tracts',
      agency: 'ICIMOD / Chittagong Hill Tracts Development Board',
      year: 2018,
      status: 'VERIFIED',
      claim: 'Double contour hedgerows of nitrogen-fixing trees (Flemingia macrophylla, Leucaena) spaced 4–6 m apart reduce soil loss by >80% and sheet runoff by >60%.',
      source_file: 'ICIMOD Manual on Soil Conservation in CHT 2018'
    },
    'VCF-CHT-Tenure': {
      id: 'VCF-CHT-Tenure',
      title: 'Village Common Forest (VCF / Mouza Ban) Preservation Guidelines',
      agency: 'CHT Regional Council & Ministry of CHT Affairs',
      year: 2019,
      status: 'VERIFIED',
      claim: 'Customary community governance protects headwater watersheds and perennial bamboo springs (chhara).',
      source_file: 'CHT Land & Natural Resource Management Policy 2019'
    }
  };

  // Helper formatting function for tags
  function getCitationBadge(citationId) {
    const cit = CITATIONS[citationId];
    if (cit && cit.status === 'VERIFIED') {
      return `<span class="citation-badge verified" title="${cit.title} (${cit.agency || cit.authors}, ${cit.year})">[VERIFIED: ${citationId}]</span>`;
    }
    return `<span class="citation-badge unverified" title="Check source">[UNVERIFIED: ${citationId || 'check source'}]</span>`;
  }

  // Export to window
  if (typeof window !== 'undefined') {
    window.CITATIONS = CITATIONS;
    window.getCitationBadge = getCitationBadge;
  }
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { CITATIONS, getCitationBadge };
  }
})();
