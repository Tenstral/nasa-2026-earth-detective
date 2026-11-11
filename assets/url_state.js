/**
 * NASA Space Apps Challenge 2026 - Trend Detective
 * assets/url_state.js
 * ==================================================
 * Shared URL State Contract (Single Source of Truth)
 * Supported across index.html, report.html, demo.html.
 *
 * Parameters:
 *   region  : NW, NE, Central, SW, SE, National, Rajshahi, Rangpur, Sylhet,
 *             Dhaka, Mymensingh, Khulna, Barishal, Chattogram, Wisconsin_US
 *   var     : tws, imerg, power, noah_sms, vic_sms, residual, ratio, drawdown, rx1day, aod
 *   window  : full_record, grace_era, grace_fo_era, recent_2020
 *   start   : year integer (e.g. 2002) - overrides window if both given
 *   end     : year integer (e.g. 2026)
 *   season  : annual, monsoon, dry
 *   mode    : student, scientist
 *   lang    : en, bn
 */

(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    const exports = factory();
    root.URLState = exports;
    root.ED = root.ED || {};
    root.ED.urlState = exports;
  }
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  // Canonical allowed sets
  const ALLOWED_REGIONS = [
    'NW', 'NE', 'Central', 'SW', 'SE', 'National',
    'Rajshahi', 'Rangpur', 'Sylhet', 'Dhaka', 'Mymensingh',
    'Khulna', 'Barishal', 'Chattogram', 'Wisconsin_US'
  ];

  const ALLOWED_VARS = [
    'tws', 'imerg', 'power', 'noah_sms', 'vic_sms',
    'residual', 'ratio', 'drawdown', 'rx1day', 'aod'
  ];

  // Aliases for backwards compatibility / legacy parameter conversion
  const VAR_ALIASES = {
    'grace_tws': 'tws',
    'grace_tws_cm': 'tws',
    'imerg_precip': 'imerg',
    'imerg_precip_mm': 'imerg',
    'precip': 'imerg',
    'power_precip': 'power',
    'power_precip_mm': 'power',
    'noah_sms_anom': 'noah_sms',
    'noah_sms_anom_cm': 'noah_sms',
    'vic_sms_anom': 'vic_sms',
    'vic_sms_anom_cm': 'vic_sms',
    'subsurface_residual': 'residual',
    'residual_mid': 'residual',
    'extreme_rx1day': 'rx1day',
    'rx1day_mm': 'rx1day',
    'modis_aod': 'aod',
    'aeronet_aod': 'aod'
  };

  const ALLOWED_WINDOWS = [
    'full_record',
    'grace_era',
    'grace_fo_era',
    'recent_2020'
  ];

  const WINDOW_YEARS = {
    'full_record': { start: 2002, end: 2026 },
    'grace_era': { start: 2002, end: 2017 },
    'grace_fo_era': { start: 2018, end: 2026 },
    'recent_2020': { start: 2020, end: 2026 }
  };

  const ALLOWED_SEASONS = ['annual', 'monsoon', 'dry'];
  const ALLOWED_MODES = ['student', 'scientist'];
  const ALLOWED_LANGS = ['en', 'bn'];

  const DEFAULTS = {
    region: 'NW',
    var: 'tws',
    window: 'full_record',
    start: null,
    end: null,
    season: 'annual',
    mode: 'scientist',
    lang: 'en'
  };

  /**
   * Helper to parse query string from search or full URL
   */
  function parseParams(searchStr) {
    const params = {};
    if (!searchStr) return params;

    let s = searchStr;
    const qIndex = s.indexOf('?');
    if (qIndex !== -1) {
      s = s.substring(qIndex + 1);
    }
    const hIndex = s.indexOf('#');
    if (hIndex !== -1) {
      s = s.substring(0, hIndex);
    }

    const pairs = s.split('&');
    for (let i = 0; i < pairs.length; i++) {
      if (!pairs[i]) continue;
      const eq = pairs[i].indexOf('=');
      if (eq === -1) {
        const key = decodeURIComponent(pairs[i]).trim();
        params[key] = '';
      } else {
        const key = decodeURIComponent(pairs[i].substring(0, eq)).trim();
        const val = decodeURIComponent(pairs[i].substring(eq + 1)).trim();
        params[key] = val;
      }
    }
    return params;
  }

  /**
   * Validates and canonicalizes state fields, falling back to defaults on unknown values
   */
  function sanitizeState(raw) {
    const state = { ...DEFAULTS };
    if (!raw || typeof raw !== 'object') return state;

    // 1. region
    if (raw.region) {
      const match = ALLOWED_REGIONS.find(r => r.toLowerCase() === String(raw.region).toLowerCase());
      if (match) state.region = match;
    }

    // 2. var (with legacy alias mapping)
    const rawVar = raw.var || raw.variable;
    if (rawVar) {
      const vStr = String(rawVar).toLowerCase();
      if (ALLOWED_VARS.includes(vStr)) {
        state.var = vStr;
      } else if (VAR_ALIASES[vStr]) {
        state.var = VAR_ALIASES[vStr];
      }
    }

    // 3. window
    if (raw.window) {
      const wStr = String(raw.window).toLowerCase();
      if (ALLOWED_WINDOWS.includes(wStr)) {
        state.window = wStr;
      }
    }

    // 4. start & end (custom window)
    if (raw.start !== undefined && raw.start !== null && raw.start !== '') {
      const s = parseInt(raw.start, 10);
      if (!isNaN(s) && s >= 1990 && s <= 2040) {
        state.start = s;
      }
    }
    if (raw.end !== undefined && raw.end !== null && raw.end !== '') {
      const e = parseInt(raw.end, 10);
      if (!isNaN(e) && e >= 1990 && e <= 2040) {
        state.end = e;
      }
    }

    // Ensure start <= end if both are valid
    if (state.start !== null && state.end !== null && state.start > state.end) {
      const tmp = state.start;
      state.start = state.end;
      state.end = tmp;
    }

    // 5. season
    if (raw.season) {
      const sStr = String(raw.season).toLowerCase();
      if (ALLOWED_SEASONS.includes(sStr)) {
        state.season = sStr;
      }
    }

    // 6. mode
    if (raw.mode) {
      const mStr = String(raw.mode).toLowerCase();
      if (ALLOWED_MODES.includes(mStr)) {
        state.mode = mStr;
      }
    }

    // 7. lang
    if (raw.lang) {
      const lStr = String(raw.lang).toLowerCase();
      if (ALLOWED_LANGS.includes(lStr)) {
        state.lang = lStr;
      }
    }

    return state;
  }

  /**
   * Reads URL state from window.location.search or provided search string
   */
  function getState(searchStr) {
    let s = searchStr;
    if (typeof s === 'undefined' && typeof window !== 'undefined' && window.location) {
      s = window.location.search;
    }
    const parsed = parseParams(s || '');
    return sanitizeState(parsed);
  }

  /**
   * Serializes a state object into a URL query string
   */
  function serializeQuery(state) {
    const parts = [];

    if (state.region) parts.push(`region=${encodeURIComponent(state.region)}`);
    if (state.var) parts.push(`var=${encodeURIComponent(state.var)}`);

    if (state.start !== null && state.end !== null) {
      parts.push(`start=${encodeURIComponent(state.start)}`);
      parts.push(`end=${encodeURIComponent(state.end)}`);
    } else if (state.window) {
      parts.push(`window=${encodeURIComponent(state.window)}`);
    }

    if (state.season) parts.push(`season=${encodeURIComponent(state.season)}`);
    if (state.mode) parts.push(`mode=${encodeURIComponent(state.mode)}`);
    if (state.lang) parts.push(`lang=${encodeURIComponent(state.lang)}`);

    return parts.length > 0 ? `?${parts.join('&')}` : '';
  }

  /**
   * Updates the current URL via history.replaceState without reloading
   */
  function setState(partial) {
    const current = getState();
    const updated = sanitizeState({ ...current, ...partial });

    if (typeof window !== 'undefined' && window.history && window.history.replaceState) {
      const query = serializeQuery(updated);
      const hash = window.location.hash || '';
      const newUrl = `${window.location.pathname}${query}${hash}`;
      window.history.replaceState(null, '', newUrl);

      // Declaratively apply mode if updated
      applyMode(updated.mode);

      // Dispatch custom event for reactive listeners
      try {
        window.dispatchEvent(new CustomEvent('urlstatechange', { detail: updated }));
      } catch (e) {
        // Fallback for environments where CustomEvent might be constrained
      }
    }
    return updated;
  }

  /**
   * Builds a URL link to a target page with state merged and optional hash anchor
   */
  function buildLink(page, partial, hash) {
    let targetPage = page || 'index.html';
    let targetHash = hash || '';

    // If page already contains a hash, extract it
    const pageHashIdx = targetPage.indexOf('#');
    if (pageHashIdx !== -1) {
      if (!targetHash) {
        targetHash = targetPage.substring(pageHashIdx);
      }
      targetPage = targetPage.substring(0, pageHashIdx);
    }

    // If partial has a hash property
    if (partial && partial.hash && !targetHash) {
      targetHash = partial.hash;
    }
    if (targetHash && !targetHash.startsWith('#')) {
      targetHash = `#${targetHash}`;
    }

    const current = getState();
    const merged = sanitizeState({ ...current, ...(partial || {}) });
    const query = serializeQuery(merged);

    return `${targetPage}${query}${targetHash}`;
  }

  /**
   * Declaratively applies mode ('student' | 'scientist') to the root document element
   */
  function applyMode(mode) {
    const m = mode === 'student' ? 'student' : 'scientist';
    if (typeof document !== 'undefined' && document.documentElement) {
      document.documentElement.dataset.mode = m;
      document.documentElement.setAttribute('data-mode', m);
    }
    const modeLabel = typeof document !== 'undefined' ? document.getElementById('nav-mode-label') : null;
    if (modeLabel) {
      modeLabel.textContent = m === 'student' ? 'Student' : 'Scientist';
    }
    return m;
  }

  /**
   * Initializes or updates the shared top navigation bar:
   *  - Sets relative links with current mode & lang
   *  - Highlights the active page link
   *  - Hooks up student/scientist and en/bn toggles
   */
  function initTopNav(explicitActivePage) {
    if (typeof document === 'undefined') return;

    let activePage = explicitActivePage;
    if (!activePage && typeof window !== 'undefined' && window.location) {
      const parts = window.location.pathname.split('/');
      activePage = parts[parts.length - 1] || 'index.html';
    }
    if (!activePage || activePage === '') activePage = 'index.html';

    const state = getState();
    applyMode(state.mode);

    // 1. Update navigation links
    const navLinks = document.querySelectorAll('.top-nav-link, .top-nav a[data-page]');
    navLinks.forEach(link => {
      const rawHref = link.getAttribute('href') || '';
      const targetPage = link.getAttribute('data-page') || rawHref.split('?')[0].split('#')[0] || 'index.html';
      const linkHash = link.getAttribute('data-hash') || (rawHref.includes('#') ? '#' + rawHref.split('#')[1] : '');

      // Carrying mode & lang
      link.href = buildLink(targetPage, { mode: state.mode, lang: state.lang }, linkHash);

      if (targetPage === activePage) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });

    // 2. Mode toggle button
    const modeBtn = document.getElementById('nav-mode-toggle');
    const modeLabel = document.getElementById('nav-mode-label');
    if (modeBtn) {
      if (modeLabel) {
        modeLabel.textContent = state.mode === 'student' ? 'Student' : 'Scientist';
      }
      modeBtn.onclick = function(e) {
        e.preventDefault();
        const nextMode = state.mode === 'student' ? 'scientist' : 'student';
        setState({ mode: nextMode });
      };
    }

    // 3. Lang toggle button
    const langBtn = document.getElementById('nav-lang-toggle');
    const langLabel = document.getElementById('nav-lang-label');
    if (langBtn) {
      if (langLabel) {
        langLabel.textContent = state.lang === 'bn' ? 'English' : 'বাংলা';
      }
      langBtn.onclick = function(e) {
        e.preventDefault();
        const nextLang = state.lang === 'bn' ? 'en' : 'bn';
        setState({ lang: nextLang });
      };
    }
  }

  // Automatic bootstrap on DOMContentLoaded if in browser
  if (typeof window !== 'undefined' && typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => initTopNav());
    } else {
      setTimeout(() => initTopNav(), 0);
    }
    window.addEventListener('urlstatechange', () => initTopNav());
  }

  return {
    DEFAULTS,
    ALLOWED_REGIONS,
    ALLOWED_VARS,
    ALLOWED_WINDOWS,
    WINDOW_YEARS,
    ALLOWED_SEASONS,
    ALLOWED_MODES,
    ALLOWED_LANGS,
    getState,
    setState,
    buildLink,
    applyMode,
    sanitizeState,
    serializeQuery,
    initTopNav
  };
}));
