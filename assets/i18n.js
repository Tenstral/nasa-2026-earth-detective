/**
 * NASA Space Apps Challenge 2026 - Trend Detective
 * assets/i18n.js
 * 
 * Bilingual Internationalization (EN / বাংলা) Engine
 * 
 * SCIENTIFIC GLOSSARY:
 * - Total Water Storage (TWS) -> সর্বমোট পানি সঞ্চয় (TWS)
 * - Trend -> প্রবণতা (Trend)
 * - p-value -> পি-মান (p-value)
 * - Confidence -> আস্থা / নিশ্চয়তা (Confidence)
 * - Rainfall -> বৃষ্টিপাত (Rainfall)
 * - Soil Moisture -> মাটির আর্দ্রতা (Soil Moisture)
 * - Groundwater -> ভূগর্ভস্থ পানি (Groundwater)
 * - Subsurface Residual -> ভূগর্ভস্থ ও পৃষ্ঠীয় পানি অবশিষ্ট (Residual)
 * - Detection Limit -> শনাক্তকরণ সীমা (Detection Limit)
 * - Minimum Detectable Slope (MDS) -> সর্বনিম্ন শনাক্তযোগ্য ঢাল (MDS)
 */

(function(root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    const exports = factory();
    root.I18N = exports;
    if (typeof window !== 'undefined') {
      window.t = exports.t;
      window.applyLang = exports.applyLang;
    }
  }
})(typeof globalThis !== 'undefined' ? globalThis : this, function() {
  'use strict';

  const GLOSSARY = {
    tws: { en: 'Total Water Storage (TWS)', bn: 'সর্বমোট পানি সঞ্চয় (TWS)' }, // DRAFT: needs native review
    trend: { en: 'Trend', bn: 'প্রবণতা (Trend)' }, // DRAFT: needs native review
    p_value: { en: 'p-value', bn: 'পি-মান (p-value)' }, // DRAFT: needs native review
    confidence: { en: 'Confidence', bn: 'পরিসংখ্যানগত নিশ্চয়তা (Confidence)' }, // DRAFT: needs native review
    rainfall: { en: 'Rainfall', bn: 'বৃষ্টিপাত (Rainfall)' }, // DRAFT: needs native review
    soil_moisture: { en: 'Soil Moisture', bn: 'মাটির আর্দ্রতা (Soil Moisture)' }, // DRAFT: needs native review
    groundwater: { en: 'Groundwater', bn: 'ভূগর্ভস্থ পানি (Groundwater)' }, // DRAFT: needs native review
    residual: { en: 'groundwater + surface water + model error residual', bn: 'ভূগর্ভস্থ + পৃষ্ঠীয় পানি + মডেল অবশিষ্ট (Residual)' } // DRAFT: needs native review
  };

  const DICTIONARY = {
    en: {
      // Top Navigation
      'nav.brand': 'NASA TREND DETECTIVE',
      'nav.title': 'Universal 5-Step Earth Observation Tool',
      'nav.workbench': '🔍 5-Step Detective Workbench',
      'nav.report': '🇧🇩 Flagship Report: Bangladesh Deep-Dive',
      'nav.demo': '📊 Interactive Pitch Deck',
      'nav.mode_student': 'Student',
      'nav.mode_scientist': 'Scientist',
      'nav.lang_toggle': 'বাংলা',

      // Workbench Steps
      'step.step1': 'Step 1: Select Earth Science Variable',
      'step.step2': 'Step 2: Inspect Temporal Signature',
      'step.step3': 'Step 3: Test Statistical Trend',
      'step.step4': 'Step 4: Cross-Sensor Comparison',
      'step.step5': 'Step 5: Impact & Adaptation Directives',

      // Map & Controls
      'map.choropleth': 'Choropleth',
      'map.grid': '1° Grid',
      'map.station': 'Station',
      'map.reset': '⟲ Reset',
      'map.legend_left': '−1.5 cm/yr',
      'map.legend_mid': '0.0',
      'map.legend_right': '+1.5 cm/yr',

      // Lenses & Chart
      'lens.trend': 'Trend & 95% CI Fan',
      'lens.seasonal': 'Seasonal Climatology Cycle',
      'lens.epochs': 'Multi-Epoch Comparison',
      'lens.compare': '+ Compare Series',
      'layer.deseason': 'Deseasonalized',
      'layer.trendline': 'Trend Line & CI',
      'layer.gap': '11-Mo Gap',
      'layer.floods': 'Historical Floods',
      'chart.zoom_tag': '[ZOOM VIEWPORT]',
      'chart.reset_zoom': 'Reset Zoom',

      // Telemetry Verdict Strip
      'tel.verdict_label': 'Statistical Verdict',
      'tel.verdict_sub': 'Standard threshold p < 0.05',
      'tel.slope_label': 'Theil-Sen Slope',
      'tel.slope_vol': 'Volumetric rate',
      'tel.ci_label': '95% Confidence Bounds',
      'tel.ci_sub': 'Duality rank inversion',
      'tel.p_label': 'p-Value & FDR',
      'tel.p_sub': 'Benjamini-Hochberg',
      'tel.n_label': 'Sample & Power Limit',
      'tel.n_sub': '80% detection threshold',

      // Student Verdict Card
      'student.verdict_title': 'Trend Detective Plain Verdict',
      'student.evaluating_title': 'Evaluating Trend...',
      'student.evaluating_desc': 'Analyzing satellite observations across selected years...',
      'student.insufficient_title': 'Insufficient Observations',
      'student.insufficient_desc': 'At least 8 data points are required to detect a trend. Currently selected time range contains too few observations.',
      'student.sig_decline_title': 'Significant Water Storage Decline',
      'student.sig_rise_title': 'Significant Water Storage Rise',
      'student.no_trend_title': 'No Detectable Long-Term Trend',
      'student.confidence_high': 'High Statistical Confidence (p < 0.05)',
      'student.confidence_normal': 'Within Expected Natural Fluctuations',
      'student.open_report': 'Open Full Hydrogeological Proof & Audit in Report →',

      // Drawer Triggers
      'btn.open_diagnostics': 'Statistical Rigor Diagnostics & Detection Power Drawer',
      'btn.open_directives': 'Regional Stakeholder Action Directives Drawer',
      'btn.open_evidence': '🔍 View Methodological Proof',
      'btn.open_report_link': 'Open Full Hydrogeological Proof & Audit in Report →',

      // Evidence Drawer
      'evidence.title': 'Methodological Proof',
      'evidence.subtitle': 'Methods and validation from Case #01',
      'evidence.tab_threeway': '3-Way Transition',
      'evidence.tab_gldas': 'GLDAS Partition',
      'evidence.tab_pairwise': 'Pairwise Differences',
      'evidence.tab_directives': 'Stakeholder Directives',
      'evidence.tab_limitations': 'Limitations',
      'evidence.open_report': 'Open in full report →',

      // Diagnostics Drawer
      'diag.title': 'Statistical Diagnostics',
      'diag.subtitle': 'Effective-sample-size Mann-Kendall stats, Minimum Detectable Slope, and sensor provenance.',
      'diag.sec_stats': 'Mann-Kendall Stats',
      'diag.sec_window': 'Window Length',
      'diag.sec_sensor': 'Sensor Safeguards',

      // Directives Drawer
      'directives.title': 'Stakeholder Directives',
      'directives.subtitle': 'Policy, farm, and local steps from 24-year satellite trends for',
      'directives.bangladesh_regions_only': 'Directives are available for Bangladesh hydrological regions.',

      // Report Specific Notice & Headings
      'report.notice_methods_english': 'Full methodological narrative and diagnostic tables are maintained in English for peer-review precision.',
      'report.header_badge': 'TECHNICAL AUDIT DOSSIER #01',
      'report.header_title': 'Secular Water Depletion Audit in Northwest Bangladesh',
      'report.header_subtitle': 'Multi-Satellite Gravimetry (GRACE / GRACE-FO), Reanalysis Homogeneity, and Multimodel Physical Partitioning (2002–2026)',
      'report.nav_sec1': '1. Spatial Overview',
      'report.nav_sec2': '2. Regional Trends',
      'report.nav_sec3': '3. Subsurface & Validation',
      'report.nav_sec4': '4. Seasonal & Exposure',
      'report.nav_sec5': '5. Stakeholder Directives',
      'report.nav_sec6': '6. Limitations & Appendix',
      'report.sec1_title': '1. Spatial Overview: Water Storage & Precipitation Scrubber',
      'report.sec2_title': '2. Regional Water Storage Trends & Time Series Analysis',
      'report.sec3_title': '3. Subsurface Storage Partitioning & Sensor Transition Integrity',
      'report.sec4_title': '4. Seasonal Storage Dynamics & Agricultural Exposure',
      'report.sec5_title': '5. Regional Stakeholder Action Directives',
      'report.sec6_title': '6. Scientific Limitations & Master Data Appendix',

      // Demo & General UI
      'demo.header_title': 'NASA Space Apps 2026 // Trend Detective',
      'demo.header_target': 'Pitch Target: 240 Seconds | Hub: tenstral-nasa26.pages.dev',
      'btn.prev': '◀ Previous',
      'btn.next': 'Next ▶',
      'btn.finish': 'Finish ↺',
      'demo.script_label': 'VOICEOVER SCRIPT'
    },

    bn: {
      // Top Navigation
      'nav.brand': 'নাসা ট্রেন্ড গোয়েন্দা', // DRAFT: needs native review
      'nav.title': 'সার্বজনীন ৫-ধাপের ভূ-পর্যবেক্ষণ প্রযুক্তি', // DRAFT: needs native review
      'nav.workbench': '🔍 ৫-ধাপের গোয়েন্দা ওয়ার্কবেঞ্চ', // DRAFT: needs native review
      'nav.report': '🇧🇩 মূল অনুসন্ধান প্রতিবেদন: বাংলাদেশ', // DRAFT: needs native review
      'nav.demo': '📊 ইন্টারেক্টিভ উপস্থাপনা', // DRAFT: needs native review
      'nav.mode_student': 'শিক্ষার্থী', // DRAFT: needs native review
      'nav.mode_scientist': 'বিজ্ঞানী', // DRAFT: needs native review
      'nav.lang_toggle': 'English', // DRAFT: needs native review

      // Workbench Steps
      'step.step1': 'ধাপ ১: ভূ-বিজ্ঞান চলক নির্বাচন', // DRAFT: needs native review
      'step.step2': 'ধাপ ২: সময়কাল ও ঋতুভিত্তিক প্যাটার্ন', // DRAFT: needs native review
      'step.step3': 'ধাপ ৩: দীর্ঘমেয়াদী পরিসংখ্যানগত পরীক্ষা', // DRAFT: needs native review
      'step.step4': 'ধাপ ৪: বহু-উপগ্রহ সেন্সর তুলনা', // DRAFT: needs native review
      'step.step5': 'ধাপ ৫: মানবিক প্রভাব ও নীতিগত নির্দেশনা', // DRAFT: needs native review

      // Map & Controls
      'map.choropleth': 'মানচিত্রের রঙ (Choropleth)', // DRAFT: needs native review
      'map.grid': '১° গ্রিড', // DRAFT: needs native review
      'map.station': 'স্টেশন', // DRAFT: needs native review
      'map.reset': '⟲ রিসেট', // DRAFT: needs native review
      'map.legend_left': '−১.৫ সেমি/বছর', // DRAFT: needs native review
      'map.legend_mid': '০.০', // DRAFT: needs native review
      'map.legend_right': '+১.৫ সেমি/বছর', // DRAFT: needs native review

      // Lenses & Chart
      'lens.trend': 'প্রবণতা ও ৯৫% আত্মবিশ্বাস ফ্যান', // DRAFT: needs native review
      'lens.seasonal': 'ঋতুভিত্তিক জলবায়ু চক্র', // DRAFT: needs native review
      'lens.epochs': 'বহু-যুগীয় তুলনা (Epochs)', // DRAFT: needs native review
      'lens.compare': '+ চলক তুলনা করুন', // DRAFT: needs native review
      'layer.deseason': 'ঋতু প্রভাবমুক্ত', // DRAFT: needs native review
      'layer.trendline': 'প্রবণতা রেখা ও সিআই', // DRAFT: needs native review
      'layer.gap': '১১-মাসের ব্যবধান', // DRAFT: needs native review
      'layer.floods': 'ঐতিহাসিক বন্যা', // DRAFT: needs native review
      'chart.zoom_tag': '[জুম ভিউপোর্ট]', // DRAFT: needs native review
      'chart.reset_zoom': 'জুম রিসেট', // DRAFT: needs native review

      // Telemetry Verdict Strip
      'tel.verdict_label': 'পরিসংখ্যানগত সিদ্ধান্ত', // DRAFT: needs native review
      'tel.verdict_sub': 'মানক সীমা p < 0.05', // DRAFT: needs native review
      'tel.slope_label': 'থেইল-সেন ঢাল (Theil-Sen Slope)', // DRAFT: needs native review
      'tel.slope_vol': 'আয়তনিক পরিবর্তনের হার', // DRAFT: needs native review
      'tel.ci_label': '৯৫% আত্মবিশ্বাস সীমা (CI)', // DRAFT: needs native review
      'tel.ci_sub': 'দ্বৈত র‍্যাঙ্ক ইনভার্শন', // DRAFT: needs native review
      'tel.p_label': 'পি-মান ও এফডিআর (p-Value & FDR)', // DRAFT: needs native review
      'tel.p_sub': 'বেনজামিনি-হচবার্গ সমন্বয়', // DRAFT: needs native review
      'tel.n_label': 'নমুনার আকার ও ক্ষমতা সীমা', // DRAFT: needs native review
      'tel.n_sub': '৮০% শনাক্তকরণ সীমা (MDS)', // DRAFT: needs native review

      // Student Verdict Card
      'student.verdict_title': 'ট্রেন্ড গোয়েন্দা সহজ সিদ্ধান্ত', // DRAFT: needs native review
      'student.evaluating_title': 'প্রবণতা মূল্যায়ন করা হচ্ছে...', // DRAFT: needs native review
      'student.evaluating_desc': 'নির্বাচিত বছরের উপগ্রহ পর্যবেক্ষণ বিশ্লেষণ চলছে...', // DRAFT: needs native review
      'student.insufficient_title': 'অপর্যাপ্ত পর্যবেক্ষণ সংখ্যা', // DRAFT: needs native review
      'student.insufficient_desc': 'প্রবণতা নির্ণয়ের জন্য কমপক্ষে ৮টি ডেটা পয়েন্ট প্রয়োজন। বর্তমানে নির্বাচিত সময় পরিসরে পর্যাপ্ত পয়েন্ট নেই।', // DRAFT: needs native review
      'student.sig_decline_title': 'উল্লেখযোগ্য পানি সঞ্চয় হ্রাস (Significant Decline)', // DRAFT: needs native review
      'student.sig_rise_title': 'উল্লেখযোগ্য পানি সঞ্চয় বৃদ্ধি (Significant Rise)', // DRAFT: needs native review
      'student.no_trend_title': 'কোনো দীর্ঘমেয়াদী প্রবণতা লক্ষণীয় নয় (No Detectable Trend)', // DRAFT: needs native review
      'student.confidence_high': 'উচ্চ পরিসংখ্যানগত নিশ্চয়তা (p < 0.05)', // DRAFT: needs native review
      'student.confidence_normal': 'স্বাভাবিক প্রাকৃতিক ওঠানামার মধ্যেই সীমাবদ্ধ', // DRAFT: needs native review
      'student.open_report': 'প্রতিবেদনে সম্পূর্ণ হাইড্রোলজিক্যাল প্রমাণ ও অডিট দেখুন →', // DRAFT: needs native review

      // Drawer Triggers
      'btn.open_diagnostics': 'পরিসংখ্যানগত নির্ভুলতা ও শনাক্তকরণ ক্ষমতা ড্রয়ার', // DRAFT: needs native review
      'btn.open_directives': 'আঞ্চলিক অংশীজন কর্মপরিকল্পনা ড্রয়ার', // DRAFT: needs native review
      'btn.open_evidence': '🔍 পদ্ধতিগত প্রমাণ ও অডিট দেখুন', // DRAFT: needs native review
      'btn.open_report_link': 'প্রতিবেদনে সম্পূর্ণ হাইড্রোলজিক্যাল প্রমাণ ও অডিট দেখুন →', // DRAFT: needs native review

      // Evidence Drawer
      'evidence.title': 'পদ্ধতিগত প্রমাণ ও বিশদ অডিট', // DRAFT: needs native review
      'evidence.subtitle': 'ডজিয়ার #০১ থেকে যাচাইকৃত বিশ্লেষণাত্মক প্রমাণাদি', // DRAFT: needs native review
      'evidence.tab_threeway': '৩-মুখী ট্রানজিশন', // DRAFT: needs native review
      'evidence.tab_gldas': 'GLDAS মাটির আর্দ্রতা বিভাজন', // DRAFT: needs native review
      'evidence.tab_pairwise': 'অঞ্চলভিত্তিক পার্থক্য', // DRAFT: needs native review
      'evidence.tab_directives': 'অংশীজন নির্দেশিকা', // DRAFT: needs native review
      'evidence.tab_limitations': 'বৈজ্ঞানিক সীমাবদ্ধতা', // DRAFT: needs native review
      'evidence.open_report': 'সম্পূর্ণ প্রতিবেদনে খুলুন →', // DRAFT: needs native review

      // Diagnostics Drawer
      'diag.title': 'পরিসংখ্যানগত নির্ভুলতা ও শনাক্তকরণ ক্ষমতা', // DRAFT: needs native review
      'diag.subtitle': 'ক্যালিব্রেটেড কার্যকরী নমুনার মান-কেন্ডাল পরিসংখ্যান, সনাক্তকরণ সক্ষমতা ও নাসা সেন্সর প্রমাণ নিরীক্ষা।', // DRAFT: needs native review
      'diag.sec_stats': 'মান-কেন্ডাল টেস্ট পরিসংখ্যান', // DRAFT: needs native review
      'diag.sec_window': 'ডঃ জেমস একারের সময়কাল ও পর্যবেক্ষণ পাঠ', // DRAFT: needs native review
      'diag.sec_sensor': 'সেন্সর ট্রানজিশন ও ব্রেক সুরক্ষা ব্যবস্থা', // DRAFT: needs native review

      // Directives Drawer
      'directives.title': 'আঞ্চলিক অংশীজন কর্মপরিকল্পনা নির্দেশিকা', // DRAFT: needs native review
      'directives.subtitle': '২৪ বছরের স্যাটেলাইট প্রবণতা থেকে প্রণীত বাস্তবমুখী নীতি ও অভিযোজন পরিকল্পনা:', // DRAFT: needs native review
      'directives.bangladesh_regions_only': 'কর্মপরিকল্পনা শুধুমাত্র বাংলাদেশের জলবায়ু অঞ্চলের জন্য প্রযোজ্য।', // DRAFT: needs native review

      // Report Specific Notice & Headings
      'report.notice_methods_english': 'সম্পূর্ণ বৈজ্ঞানিক গবেষণাপদ্ধতি ও বিশদ সারণী ইংরেজি ভাষায় সংরক্ষিত।', // DRAFT: needs native review
      'report.header_badge': 'কারিগরি অডিট ডজিয়ার #০১', // DRAFT: needs native review
      'report.header_title': 'উত্তর-পশ্চিম বাংলাদেশে পানি সঞ্চয় হ্রাসের দীর্ঘমেয়াদী অডিট', // DRAFT: needs native review
      'report.header_subtitle': 'মাল্টি-স্যাটেলাইট গ্র্যাভিমেট্রি (GRACE / GRACE-FO), পুনঃবিশ্লেষণ সামঞ্জস্য ও বহুমডেল বিভাজন (2002–2026)', // DRAFT: needs native review
      'report.nav_sec1': '১. স্থানিক সমীক্ষা', // DRAFT: needs native review
      'report.nav_sec2': '২. আঞ্চলিক প্রবণতা', // DRAFT: needs native review
      'report.nav_sec3': '৩. ভূগর্ভস্থ ও যাচাইকরণ', // DRAFT: needs native review
      'report.nav_sec4': '৪. ঋতু ও ঝুঁকি', // DRAFT: needs native review
      'report.nav_sec5': '৫. অংশীজন কর্মপরিকল্পনা', // DRAFT: needs native review
      'report.nav_sec6': '৬. সীমাবদ্ধতা ও পরিশিষ্ট', // DRAFT: needs native review
      'report.sec1_title': '১. স্থানিক সমীক্ষা: পানি সঞ্চয় ও বৃষ্টিপাত স্ক্রাবার', // DRAFT: needs native review
      'report.sec2_title': '২. আঞ্চলিক পানি সঞ্চয় প্রবণতা ও টাইম সিরিজ বিশ্লেষণ', // DRAFT: needs native review
      'report.sec3_title': '৩. ভূগর্ভস্থ পানি বিভাজন ও সেন্সর রূপান্তর নির্ভরযোগ্যতা', // DRAFT: needs native review
      'report.sec4_title': '৪. ঋতুভিত্তিক পরিবর্তনশীলতা ও কৃষি ক্ষেত্রে প্রভাব', // DRAFT: needs native review
      'report.sec5_title': '৫. আঞ্চলিক অংশীজন কর্মপরিকল্পনা নির্দেশিকা', // DRAFT: needs native review
      'report.sec6_title': '৬. বৈজ্ঞানিক সীমাবদ্ধতা ও তথ্য পরিশিষ্ট', // DRAFT: needs native review

      // Demo & General UI
      'demo.header_title': 'নাসা স্পেস অ্যাপস ২০২৬ // ট্রেন্ড গোয়েন্দা', // DRAFT: needs native review
      'demo.header_target': 'উপস্থাপনার লক্ষ্য: ২৪০ সেকেন্ড | হাব: tenstral-nasa26.pages.dev', // DRAFT: needs native review
      'btn.prev': '◀ পূর্ববর্তী', // DRAFT: needs native review
      'btn.next': 'পরবর্তী ▶', // DRAFT: needs native review
      'btn.finish': 'সমাপ্ত ↺', // DRAFT: needs native review
      'demo.script_label': 'ভয়েসওভার স্ক্রিপ্ট' // DRAFT: needs native review
    }
  };

  /**
   * Retrieves translation for key. Falls back to English, then defaultVal, then key.
   */
  function t(key, defaultVal) {
    if (!key) return '';
    let currentLang = 'en';
    if (typeof window !== 'undefined' && window.URLState) {
      currentLang = window.URLState.getState().lang || 'en';
    } else if (typeof document !== 'undefined' && document.documentElement && document.documentElement.lang) {
      currentLang = document.documentElement.lang;
    }

    if (currentLang === 'bn') {
      if (DICTIONARY.bn && DICTIONARY.bn[key] !== undefined) {
        return DICTIONARY.bn[key];
      }
    }
    if (DICTIONARY.en && DICTIONARY.en[key] !== undefined) {
      return DICTIONARY.en[key];
    }
    return defaultVal !== undefined ? defaultVal : key;
  }

  /**
   * Applies language to the document and updates all data-i18n elements
   */
  function applyLang(lang) {
    const l = (lang === 'bn') ? 'bn' : 'en';

    if (typeof document !== 'undefined' && document.documentElement) {
      document.documentElement.lang = l;
      document.documentElement.setAttribute('lang', l);

      // Update Top Nav button text
      const langLabel = document.getElementById('nav-lang-label');
      if (langLabel) {
        langLabel.textContent = (l === 'bn') ? 'English' : 'বাংলা';
      }

      // 1. Text elements with data-i18n
      const textNodes = document.querySelectorAll('[data-i18n]');
      textNodes.forEach(node => {
        const key = node.getAttribute('data-i18n');
        if (!key) return;
        if (!node._i18nFallback) {
          node._i18nFallback = node.textContent;
        }
        if (l === 'bn') {
          const trans = t(key);
          if (trans && trans !== key) {
            node.textContent = trans;
          } else {
            node.textContent = node._i18nFallback;
          }
        } else {
          node.textContent = node._i18nFallback;
        }
      });

      // 2. Attribute elements with data-i18n-attr="attr:key,..."
      const attrNodes = document.querySelectorAll('[data-i18n-attr]');
      attrNodes.forEach(node => {
        const spec = node.getAttribute('data-i18n-attr');
        if (!spec) return;
        if (!node._i18nAttrFallbacks) node._i18nAttrFallbacks = {};

        spec.split(',').forEach(pair => {
          const [attr, key] = pair.split(':').map(s => s.trim());
          if (!attr || !key) return;
          if (!node._i18nAttrFallbacks[attr]) {
            node._i18nAttrFallbacks[attr] = node.getAttribute(attr) || '';
          }
          if (l === 'bn') {
            const trans = t(key);
            if (trans && trans !== key) {
              node.setAttribute(attr, trans);
            } else {
              node.setAttribute(attr, node._i18nAttrFallbacks[attr]);
            }
          } else {
            node.setAttribute(attr, node._i18nAttrFallbacks[attr]);
          }
        });
      });
    }

    if (typeof window !== 'undefined') {
      try {
        window.dispatchEvent(new CustomEvent('i18n:langchange', { detail: { lang: l } }));
      } catch (e) {}
    }
    return l;
  }

  // Auto-init on DOMContentLoaded if in browser
  if (typeof window !== 'undefined' && typeof document !== 'undefined') {
    const handleBootstrap = () => {
      const state = (window.URLState && window.URLState.getState) ? window.URLState.getState() : { lang: 'en' };
      applyLang(state.lang || 'en');
    };
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', handleBootstrap);
    } else {
      setTimeout(handleBootstrap, 0);
    }
    window.addEventListener('urlstatechange', (e) => {
      const lang = (e && e.detail && e.detail.lang) || (window.URLState && window.URLState.getState().lang) || 'en';
      applyLang(lang);
    });
  }

  return {
    GLOSSARY,
    DICTIONARY,
    t,
    applyLang
  };
});
