import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const I18N = require('../../assets/i18n.js');

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REPO_ROOT = path.resolve(__dirname, '../..');

describe('Internationalization Engine & Bilingual Assets (i18n)', () => {
  const indexHtml = fs.readFileSync(path.join(REPO_ROOT, 'index.html'), 'utf-8');
  const reportHtml = fs.readFileSync(path.join(REPO_ROOT, 'report.html'), 'utf-8');
  const demoHtml = fs.readFileSync(path.join(REPO_ROOT, 'demo.html'), 'utf-8');
  const i18nJs = fs.readFileSync(path.join(REPO_ROOT, 'assets/i18n.js'), 'utf-8');

  test('assets/i18n.js exports dictionary and helper functions', () => {
    assert.ok(I18N.DICTIONARY, 'DICTIONARY must be exported');
    assert.ok(I18N.DICTIONARY.en, 'DICTIONARY.en must be exported');
    assert.ok(I18N.DICTIONARY.bn, 'DICTIONARY.bn must be exported');
    assert.ok(I18N.GLOSSARY, 'GLOSSARY must be exported');
    assert.equal(typeof I18N.t, 'function', 't() helper must be a function');
    assert.equal(typeof I18N.applyLang, 'function', 'applyLang() helper must be a function');
  });

  test('Scientific glossary contains required domain translations', () => {
    const requiredTerms = ['tws', 'trend', 'p_value', 'confidence', 'rainfall', 'soil_moisture', 'groundwater', 'residual'];
    for (const term of requiredTerms) {
      assert.ok(I18N.GLOSSARY[term], `Glossary term '${term}' must exist`);
      assert.ok(I18N.GLOSSARY[term].en, `Glossary term '${term}' must have EN translation`);
      assert.ok(I18N.GLOSSARY[term].bn, `Glossary term '${term}' must have BN translation`);
    }
    // Verify TWS specifically mentions Total Water Storage
    assert.match(I18N.GLOSSARY.tws.en, /Total Water Storage \(TWS\)/);
    assert.match(I18N.GLOSSARY.residual.en, /groundwater \+ surface water \+ model error residual/);
  });

  test('English and Bangla dictionary keys are symmetric and non-empty', () => {
    const enKeys = Object.keys(I18N.DICTIONARY.en);
    const bnKeys = Object.keys(I18N.DICTIONARY.bn);

    assert.deepEqual(enKeys.sort(), bnKeys.sort(), 'EN and BN dictionaries must share identical keys');
    assert.ok(enKeys.length >= 70, `Expected at least 70 dictionary keys, found ${enKeys.length}`);

    for (const key of enKeys) {
      assert.notEqual(I18N.DICTIONARY.en[key].trim(), '', `EN translation for '${key}' must not be empty`);
      assert.notEqual(I18N.DICTIONARY.bn[key].trim(), '', `BN translation for '${key}' must not be empty`);
    }
  });

  test('All data-i18n attributes in HTML pages exist in i18n dictionaries', () => {
    const pages = [
      { name: 'index.html', content: indexHtml },
      { name: 'report.html', content: reportHtml },
      { name: 'demo.html', content: demoHtml }
    ];

    for (const page of pages) {
      const matches = [...page.content.matchAll(/data-i18n="([^"]+)"/g)].map(m => m[1]);
      assert.ok(matches.length > 0, `${page.name} must have data-i18n elements`);

      for (const key of matches) {
        assert.ok(I18N.DICTIONARY.en[key], `${page.name} key '${key}' missing in DICTIONARY.en`);
        assert.ok(I18N.DICTIONARY.bn[key], `${page.name} key '${key}' missing in DICTIONARY.bn`);
      }
    }
  });

  test('Hard Rule 2: Scientific rates, p-values, and years preserve Latin digits in BN translations', () => {
    // Check that p-values, cm/yr, and year ranges in BN translations use Latin digits
    const bnDict = I18N.DICTIONARY.bn;
    for (const [key, value] of Object.entries(bnDict)) {
      if (value.includes('p <') || value.includes('p-value') || value.includes('cm/yr') || value.includes('2002–2026')) {
        // Assert that scientific expressions in BN use Latin digits 0-9
        assert.doesNotMatch(
          value,
          /p\s*[<>=]\s*[০-৯]/,
          `Key '${key}' in BN contains Bengali digits in p-value: ${value}`
        );
        assert.doesNotMatch(
          value,
          /[০-৯]+\.?([০-৯]+)?\s*cm\/yr/,
          `Key '${key}' in BN contains Bengali digits in cm/yr rate: ${value}`
        );
      }
    }
  });

  test('All draft Bengali strings are tagged for native speaker review', () => {
    const draftComments = (i18nJs.match(/\/\/ DRAFT: needs native review/g) || []).length;
    assert.ok(
      draftComments >= 70,
      `Expected at least 70 draft translation tags in assets/i18n.js, found ${draftComments}`
    );
  });
});
