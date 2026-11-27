// Verify the SHIPPED 404 resolver (inline script in the built 404.html).
//
// A merged-away story's URL now lands on /404.html, which reads redirects.json
// and bounces to the canonical story. The navigation itself is jsdom's
// unimplemented path, so this suite drives the resolver's own pure function
// (window.__tiaRedirectTarget) against the real script and asserts the two
// properties that matter: base-prefix normalization, and same-origin-only
// targets (a corrupted map must never become an open redirect).
const { JSDOM, VirtualConsole } = require('jsdom');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const html = fs.readFileSync(path.join(ROOT, '404.html'), 'utf8');

// A map key that does NOT match the document URL, so the script under test
// never tries to navigate while we drive the pure function.
const map = { 'merged-one': 'canonical-one' };
const vc = new VirtualConsole();
vc.on('jsdomError', () => {}); // swallow "Not implemented: navigation"

const dom = new JSDOM(html, {
  url: 'https://zarguell.github.io/tia-n-list/stories/not-in-the-map/',
  runScripts: 'dangerously',
  virtualConsole: vc,
  beforeParse(window) {
    window.fetch = (url) =>
      String(url).includes('redirects.json')
        ? Promise.resolve({ ok: true, json: () => Promise.resolve(map) })
        : Promise.reject(new Error('unexpected fetch: ' + url));
  },
});

const { window } = dom;
const t = window.__tiaRedirectTarget;
const out = {
  exposed: typeof t === 'function',
  exact: t && t('stories/merged-one/', map),
  leadingSlash: t && t('/stories/merged-one/', map),
  noTrailingSlash: t && t('stories/merged-one', map),
  miss: t && t('stories/other/', map),
  absoluteTarget: t && t('stories/x/', { x: 'https://evil.test/' }),
  protocolRelative: t && t('stories/x/', { x: '//evil.test/' }),
  uppercaseId: t && t('stories/x/', { x: 'Bad/' }),
  traversal: t && t('stories/x/', { x: '../../etc/passwd' }),
  fetchesMap: /redirects\.json/.test(html),
};

const want = {
  exposed: true,
  exact: 'stories/canonical-one/',
  leadingSlash: 'stories/canonical-one/',
  noTrailingSlash: 'stories/canonical-one/',
  miss: null,
  absoluteTarget: null,
  protocolRelative: null,
  uppercaseId: null,
  traversal: null,
  fetchesMap: true,
};

let ok = true;
for (const k of Object.keys(want)) {
  const pass = out[k] === want[k];
  ok = ok && pass;
  console.log(`  [${pass ? 'PASS' : 'FAIL'}] ${k}: got ${JSON.stringify(out[k])} want ${JSON.stringify(want[k])}`);
}
console.log(ok ? 'ALL PASS' : 'FAILURES');
process.exit(ok ? 0 : 1);
