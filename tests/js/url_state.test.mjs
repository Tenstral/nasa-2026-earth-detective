/**
 * tests/js/url_state.test.mjs
 * ============================
 * Node.js test suite for assets/url_state.js.
 */

import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import URLState from '../../assets/url_state.js';

describe('Shared URL State Module (url_state.js)', () => {

  test('Exact query matching: ?region=NW&var=tws&window=full_record&mode=scientist&lang=bn', () => {
    const q = '?region=NW&var=tws&window=full_record&mode=scientist&lang=bn';
    const state = URLState.getState(q);

    assert.equal(state.region, 'NW');
    assert.equal(state.var, 'tws');
    assert.equal(state.window, 'full_record');
    assert.equal(state.mode, 'scientist');
    assert.equal(state.lang, 'bn');
    assert.equal(state.season, 'annual'); // default
    assert.equal(state.start, null);
    assert.equal(state.end, null);
  });

  test('Garbage values fall back to defaults without throwing', () => {
    const q = '?region=Atlantis&var=kryptonite&window=century&mode=godmode&lang=elvish&season=eclipse';
    const state = URLState.getState(q);

    assert.equal(state.region, URLState.DEFAULTS.region); // NW
    assert.equal(state.var, URLState.DEFAULTS.var);       // tws
    assert.equal(state.window, URLState.DEFAULTS.window); // full_record
    assert.equal(state.mode, URLState.DEFAULTS.mode);     // scientist
    assert.equal(state.lang, URLState.DEFAULTS.lang);     // en
    assert.equal(state.season, URLState.DEFAULTS.season); // annual
  });

  test('Legacy aliases map correctly to canonical var IDs', () => {
    const legacy1 = URLState.getState('?variable=grace_tws_cm');
    assert.equal(legacy1.var, 'tws');

    const legacy2 = URLState.getState('?var=imerg_precip_mm');
    assert.equal(legacy2.var, 'imerg');

    const legacy3 = URLState.getState('?var=subsurface_residual');
    assert.equal(legacy3.var, 'residual');

    const legacy4 = URLState.getState('?var=extreme_rx1day');
    assert.equal(legacy4.var, 'rx1day');
  });

  test('Custom window with start and end overrides window', () => {
    const q = '?region=Central&var=tws&start=2005&end=2021&window=full_record';
    const state = URLState.getState(q);

    assert.equal(state.region, 'Central');
    assert.equal(state.start, 2005);
    assert.equal(state.end, 2021);

    const link = URLState.buildLink('index.html', state);
    assert.ok(link.includes('start=2005'));
    assert.ok(link.includes('end=2021'));
    // When start and end are present, serializeQuery uses them
    assert.ok(!link.includes('window=full_record'));
  });

  test('buildLink merges partial state and handles section hashes', () => {
    const base = '?region=NW&var=tws&window=full_record&mode=scientist&lang=en';
    const link = URLState.buildLink('report.html', { region: 'NE' }, '#subsurface-validation');

    assert.ok(link.startsWith('report.html?'));
    assert.ok(link.includes('region=NE'));
    assert.ok(link.endsWith('#subsurface-validation'));
  });

  test('Divisions and universality regions are recognized', () => {
    const divState = URLState.getState('?region=Rajshahi');
    assert.equal(divState.region, 'Rajshahi');

    const wisconsinState = URLState.getState('?region=Wisconsin_US');
    assert.equal(wisconsinState.region, 'Wisconsin_US');
  });

  test('buildLink preserves mode and lang across pages', () => {
    const state = { region: 'NW', var: 'tws', window: 'full_record', mode: 'student', lang: 'bn' };
    const link1 = URLState.buildLink('index.html', state);
    const link2 = URLState.buildLink('report.html', state);
    const link3 = URLState.buildLink('demo.html', state);

    assert.ok(link1.includes('mode=student') && link1.includes('lang=bn'));
    assert.ok(link2.includes('mode=student') && link2.includes('lang=bn'));
    assert.ok(link3.includes('mode=student') && link3.includes('lang=bn'));
    assert.ok(link1.startsWith('index.html?'));
    assert.ok(link2.startsWith('report.html?'));
    assert.ok(link3.startsWith('demo.html?'));
  });

});
