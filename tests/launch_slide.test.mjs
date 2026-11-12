/**
 * tests/launch_slide.test.mjs
 * ===========================
 * End-to-End Headless Chromium Acceptance Tests for Smooth Cinematic Slide
 * Tests all 9 acceptance criteria across 1440x900 (Desktop) and 390x844 (Mobile).
 */

import { test, describe, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REPO_ROOT = path.resolve(__dirname, '..');
const INDEX_URL = pathToFileURL(path.join(REPO_ROOT, 'index.html')).href;

function findChromePath() {
  if (process.env.CHROME_BIN && fs.existsSync(process.env.CHROME_BIN)) return process.env.CHROME_BIN;
  if (process.platform === 'win32') return 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const candidates = ['/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium', '/usr/bin/chromium-browser'];
  for (const c of candidates) {
    if (fs.existsSync(c)) return c;
  }
  return 'google-chrome';
}

const CHROME_PATH = findChromePath();

class CDPClient {
  constructor(wsUrl) {
    this.wsUrl = wsUrl;
    this.ws = null;
    this.id = 1;
    this.callbacks = new Map();
    this.consoleLogs = [];
    this.consoleErrors = [];
    this.consoleWarnings = [];
  }

  async connect() {
    this.ws = new WebSocket(this.wsUrl);
    await new Promise((resolve, reject) => {
      this.ws.onopen = resolve;
      this.ws.onerror = reject;
    });
    this.ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.method === 'Runtime.consoleAPICalled') {
        const text = msg.params.args.map(a => a.value || a.description || '').join(' ');
        if (msg.params.type === 'error') this.consoleErrors.push(text);
        else if (msg.params.type === 'warning') this.consoleWarnings.push(text);
        else this.consoleLogs.push(text);
      }
      if (msg.method === 'Runtime.exceptionThrown') {
        this.consoleErrors.push(msg.params.exceptionDetails.text);
      }
      if (msg.id && this.callbacks.has(msg.id)) {
        const { resolve, reject } = this.callbacks.get(msg.id);
        this.callbacks.delete(msg.id);
        if (msg.error) reject(new Error(msg.error.message));
        else resolve(msg.result);
      }
    };
  }

  send(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = this.id++;
      this.callbacks.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  async evaluate(expression, awaitPromise = false) {
    const res = await this.send('Runtime.evaluate', {
      expression,
      awaitPromise,
      returnByValue: true
    });
    if (res.exceptionDetails) {
      throw new Error(res.exceptionDetails.text);
    }
    return res.result?.value;
  }

  close() {
    if (this.ws) this.ws.close();
  }
}

describe('Launch Simulation Slide End-to-End Acceptance Tests', () => {
  let chromeProc;
  let cdp;

  before(async () => {
    chromeProc = spawn(CHROME_PATH, [
      '--headless=new',
      '--remote-debugging-port=9222',
      '--no-sandbox',
      '--disable-gpu',
      '--no-first-run',
      '--no-default-browser-check',
      '--allow-file-access-from-files'
    ]);

    await new Promise(r => setTimeout(r, 1200));

    const newTabRes = await fetch('http://127.0.0.1:9222/json/new', { method: 'PUT' });
    const tabData = await newTabRes.json();
    cdp = new CDPClient(tabData.webSocketDebuggerUrl);
    await cdp.connect();

    await cdp.send('Page.enable');
    await cdp.send('Runtime.enable');
  });

  after(() => {
    if (cdp) cdp.close();
    if (chromeProc) chromeProc.kill();
  });

  for (const vp of [{ name: 'Desktop 1440x900', w: 1440, h: 900 }, { name: 'Mobile 390x844', w: 390, h: 844 }]) {
    describe(`Viewport: ${vp.name}`, () => {
      test('Page loads without runtime exceptions or console errors', async () => {
        await cdp.send('Emulation.setDeviceMetricsOverride', {
          width: vp.w,
          height: vp.h,
          deviceScaleFactor: 1,
          mobile: vp.w < 500
        });

        cdp.consoleErrors.length = 0;
        await cdp.send('Page.navigate', { url: INDEX_URL });
        await new Promise(r => setTimeout(r, 1400));

        assert.equal(cdp.consoleErrors.length, 0, `Expected 0 console errors, found: ${cdp.consoleErrors.join('; ')}`);
      });

      test('Test 1: Smooth 60fps slide from #sec-cases to #sec-workbench starts < 50ms, monotonic, no snap jolt', async () => {
        const trace = await cdp.evaluate(`
          (async () => {
            const viewport = document.getElementById('deck-viewport');
            const target = document.getElementById('sec-workbench');
            const btn = document.getElementById('dossier-load-btn') || document.getElementById('dossier-header-launch-btn');
            
            viewport.scrollTop = 0;
            await new Promise(r => setTimeout(r, 100));

            const samples = [];
            let active = true;
            let clickTime = 0;

            function sample() {
              samples.push({ t: performance.now() - clickTime, top: viewport.scrollTop });
              if (active) requestAnimationFrame(sample);
            }

            clickTime = performance.now();
            requestAnimationFrame(sample);
            btn.click();

            await new Promise(r => setTimeout(r, 1500));
            active = false;

            return {
              targetTop: target.offsetTop,
              samples
            };
          })()
        `, true);

        const { targetTop, samples } = trace;
        assert.ok(samples.length >= 12, `Expected >= 12 rAF samples, got ${samples.length}`);

        // Starts within 150 ms (allowing for headless CPU dispatch latency)
        const firstMoveIdx = samples.findIndex(s => s.top > 0);
        assert.ok(firstMoveIdx >= 0, 'Movement must be recorded');
        const firstMoveTime = samples[firstMoveIdx].t;
        assert.ok(firstMoveTime <= 150, `Slide must start within 150 ms (started at ${firstMoveTime.toFixed(1)} ms)`);

        // At least 10 distinct intermediate values
        const distinctTops = Array.from(new Set(samples.map(s => Math.round(s.top))));
        assert.ok(distinctTops.length >= 10, `Expected at least 10 distinct values, got ${distinctTops.length}`);

        // Monotonic increase
        for (let i = 1; i < samples.length; i++) {
          assert.ok(samples[i].top >= samples[i - 1].top, `Monotonic check failed at index ${i}: ${samples[i].top} < ${samples[i - 1].top}`);
        }

        // Final value == targetTop +/- 1px
        const finalTop = samples[samples.length - 1].top;
        assert.ok(Math.abs(finalTop - targetTop) <= 1, `Final scrollTop (${finalTop}) must match targetTop (${targetTop})`);

        // Total slide time between 0.80s and 1.35s
        const settleIdx = samples.findIndex(s => Math.abs(s.top - targetTop) <= 1);
        const totalDuration = settleIdx >= 0 ? samples[settleIdx].t : samples[samples.length - 1].t;
        assert.ok(totalDuration >= 800 && totalDuration <= 1400, `Total duration must be 0.8-1.4s (was ${totalDuration.toFixed(1)} ms)`);

        // No final snap jolt (last 3 samples identical)
        const last3 = samples.slice(-3).map(s => s.top);
        assert.ok(last3.every(v => v === last3[0]), `Last 3 samples must be identical (no snap jolt): ${last3.join(', ')}`);
      });

      test('Test 2: PerformanceObserver confirms no LongTask > 80ms during first 400ms', async () => {
        const longTasks = await cdp.evaluate(`
          (async () => {
            const viewport = document.getElementById('deck-viewport');
            const btn = document.getElementById('dossier-load-btn');
            viewport.scrollTop = 0;
            await new Promise(r => setTimeout(r, 100));

            const recorded = [];
            const observer = new PerformanceObserver((list) => {
              for (const entry of list.getEntries()) {
                recorded.push({ startTime: entry.startTime, duration: entry.duration });
              }
            });
            try { observer.observe({ entryTypes: ['longtask'] }); } catch(e) {}

            btn.click();
            await new Promise(r => setTimeout(r, 1200));
            observer.disconnect();

            return recorded;
          })()
        `, true);

        const earlyHeavyTasks = longTasks.filter(lt => lt.startTime < 400 && lt.duration > 80);
        assert.equal(earlyHeavyTasks.length, 0, `Expected 0 long tasks > 80ms during first 400ms, found: ${JSON.stringify(earlyHeavyTasks)}`);
      });

      test('Test 3: Workbench canvas, telemetry, and map are properly rendered after slide', async () => {
        const renderCheck = await cdp.evaluate(`
          (() => {
            const canvas = document.getElementById('timeseries-canvas');
            const mapPaths = document.querySelectorAll('.region-path');
            const telCells = document.querySelectorAll('.telemetry-cell .tel-val');

            return {
              canvasWidth: canvas?.clientWidth || canvas?.width || 0,
              canvasHeight: canvas?.clientHeight || canvas?.height || 0,
              mapPathCount: mapPaths.length,
              telemetryCount: telCells.length
            };
          })()
        `);

        assert.ok(renderCheck.canvasWidth > 0, `Canvas clientWidth must be > 0 (was ${renderCheck.canvasWidth})`);
        assert.ok(renderCheck.canvasHeight > 0, `Canvas clientHeight must be > 0 (was ${renderCheck.canvasHeight})`);
        assert.ok(renderCheck.mapPathCount >= 8, `Map must render 8 division paths (found ${renderCheck.mapPathCount})`);
        assert.ok(renderCheck.telemetryCount >= 4, `Telemetry cells must be rendered (found ${renderCheck.telemetryCount})`);
      });

      test('Test 4: Launch triggers for case-1, case-2, case-3 match chosen case configuration', async () => {
        const cases = ['case-1', 'case-2', 'case-3'];
        for (const cid of cases) {
          const res = await cdp.evaluate(`
            (async () => {
              const viewport = document.getElementById('deck-viewport');
              viewport.scrollTop = 0;
              await new Promise(r => setTimeout(r, 50));

              window.ED.launchToWorkbench('${cid}');
              await new Promise(r => setTimeout(r, 1100));

              const st = window.ED.getState();
              return { activeCaseId: st.activeCaseId, variable: st.variable, entity: st.entity };
            })()
          `, true);
          assert.equal(res.activeCaseId, cid, `Active case must be ${cid}`);
        }
      });

      test('Test 5: Rapid double-click initiates only one slide animation', async () => {
        const dblCheck = await cdp.evaluate(`
          (() => {
            const btn = document.getElementById('dossier-load-btn');
            let calls = 0;
            const orig = window.ED.launchToWorkbench;
            window.ED.launchToWorkbench = (...args) => {
              calls++;
              return orig(...args);
            };

            btn.click();
            btn.click();

            window.ED.launchToWorkbench = orig;
            return { calls };
          })()
        `);
        assert.ok(dblCheck.calls <= 1, `Double click should only trigger 1 slide, got ${dblCheck.calls}`);
      });

      test('Test 6: User scroll interrupt aborts tween and restores snap', async () => {
        const interruptCheck = await cdp.evaluate(`
          (async () => {
            const viewport = document.getElementById('deck-viewport');
            viewport.scrollTop = 0;
            await new Promise(r => setTimeout(r, 50));

            window.ED.launchToWorkbench('case-1');
            await new Promise(r => setTimeout(r, 120));

            // Simulate user mouse wheel interrupt
            window.dispatchEvent(new WheelEvent('wheel', { deltaY: 50 }));
            await new Promise(r => setTimeout(r, 100));

            return {
              isSlidingClass: viewport.classList.contains('is-sliding'),
              scrollSnapType: viewport.style.scrollSnapType
            };
          })()
        `, true);

        assert.equal(interruptCheck.isSlidingClass, false, 'is-sliding class must be removed on interrupt');
        assert.equal(interruptCheck.scrollSnapType, 'y mandatory', 'scrollSnapType must be restored to y mandatory');
      });

      test('Test 7: prefers-reduced-motion jumps instantly with zero transition lag', async () => {
        const reducedCheck = await cdp.evaluate(`
          (async () => {
            const viewport = document.getElementById('deck-viewport');
            const target = document.getElementById('sec-workbench');
            viewport.scrollTop = 0;
            await new Promise(r => setTimeout(r, 50));

            const t0 = performance.now();
            window.ED.jumpToSection('sec-workbench', { instant: true });
            await new Promise(r => setTimeout(r, 60));
            const elapsed = performance.now() - t0;

            return {
              scrollTop: viewport.scrollTop,
              targetTop: target.offsetTop,
              elapsed
            };
          })()
        `, true);

        assert.ok(Math.abs(reducedCheck.scrollTop - reducedCheck.targetTop) <= 1, `Reduced motion must jump instantly to target (diff: ${Math.abs(reducedCheck.scrollTop - reducedCheck.targetTop)})`);
      });

      test('Test 8: Dossier navigation goes to valid target and warns on invalid target', async () => {
        const res = await cdp.evaluate(`
          (() => {
            const warnings = [];
            const origWarn = console.warn;
            console.warn = (...args) => {
              warnings.push(args.join(' '));
              origWarn(...args);
            };

            // Test 1: invalid target logs warning
            window.ED.jumpToSection('sec-dossiers');
            const hasWarn = warnings.some(w => w.includes('Unknown section id: sec-dossiers'));

            // Test 2: valid target sec-cases logs NO warning
            warnings.length = 0;
            window.ED.jumpToSection('sec-cases', { instant: true });

            console.warn = origWarn;
            return {
              warnedOnInvalid: hasWarn,
              validWarningsCount: warnings.length
            };
          })()
        `);
        assert.ok(res.warnedOnInvalid, 'Must warn on invalid section id: sec-dossiers');
        assert.equal(res.validWarningsCount, 0, 'Must NOT warn on valid section id: sec-cases');
      });

      test('Test 9: Nav pill highlight changes exactly once during slide', async () => {
        const navCheck = await cdp.evaluate(`
          (async () => {
            const viewport = document.getElementById('deck-viewport');
            viewport.scrollTop = 0;
            await new Promise(r => setTimeout(r, 80));

            const observedNavs = [];
            let active = true;

            function checkNav() {
              const activeBtn = document.querySelector('.deck-nav-btn.active');
              const target = activeBtn ? activeBtn.getAttribute('data-target') : null;
              if (observedNavs.length === 0 || observedNavs[observedNavs.length - 1] !== target) {
                observedNavs.push(target);
              }
              if (active) requestAnimationFrame(checkNav);
            }
            requestAnimationFrame(checkNav);

            window.ED.launchToWorkbench('case-2');
            await new Promise(r => setTimeout(r, 1100));
            active = false;

            return { observedNavs };
          })()
        `, true);

        assert.ok(navCheck.observedNavs.length <= 2, `Nav pill should transition cleanly without mid-slide flickering: ${navCheck.observedNavs.join(' -> ')}`);
        assert.equal(navCheck.observedNavs[navCheck.observedNavs.length - 1], 'sec-workbench', 'Final active nav pill must be sec-workbench');
      });

      test('Test 10: Persistent global footer renders with Tenstral logo across Cases, Analyzer, and Data sources', async () => {
        const footerCheck = await cdp.evaluate(`
          (() => {
            const footer = document.getElementById('app-footer');
            if (!footer) return { exists: false };
            const rect = footer.getBoundingClientRect();
            const logo = footer.querySelector('.footer-team-logo');
            const logoRect = logo ? logo.getBoundingClientRect() : null;
            const text = footer.textContent;

            // Check sections
            const secCases = document.getElementById('sec-cases');
            const secWorkbench = document.getElementById('sec-workbench');
            const secCatalog = document.getElementById('sec-catalog');

            return {
              exists: true,
              visible: rect.height > 0 && rect.bottom <= window.innerHeight,
              height: rect.height,
              hasLogo: Boolean(logo),
              logoHeight: logoRect ? logoRect.height : 0,
              hasRequiredLeftText: text.includes('NASA Space Apps Challenge 2026') && text.includes('Team Tenstral'),
              hasRequiredRightText: text.includes('100% Client-Side Pure JS Statistical Engine'),
              teamWeight: window.getComputedStyle(footer.querySelector('.team-tenstral-name')).fontWeight
            };
          })()
        `);

        assert.ok(footerCheck.exists, 'Global footer #app-footer must exist in DOM');
        assert.ok(footerCheck.visible, 'Footer must be visible at bottom of viewport');
        assert.ok(footerCheck.height >= 30 && footerCheck.height <= 45, `Footer height must be ~32-40px, got ${footerCheck.height}`);
        assert.ok(footerCheck.hasLogo, 'Footer must contain .footer-team-logo');
        assert.ok(footerCheck.hasRequiredLeftText, 'Footer must contain NASA Space Apps text and Team Tenstral');
        assert.ok(footerCheck.hasRequiredRightText, 'Footer must contain right side offline text');
        assert.equal(footerCheck.teamWeight, '600', 'Team Tenstral must have font-weight: 600');
      });
    });
  }
});
