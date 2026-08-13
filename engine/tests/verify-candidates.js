// Behavioral verification of the SHIPPED KEV-tracking dashboard (extracted
// from the generated page): hostile rows must render as text only (no img/svg
// elements, no handlers fire), view toggle (All vs pure candidates), status
// filter + search, default sort (first exploit report, newest first), and
// base-relative links (candidates -> candidates/<id>/, on-KEV -> kev/cves/<id>/).
// S3(c): the inline script must not interpolate data via innerHTML.
// Runs in CI (site-deploy.yml) after the build step, same recipe as
// verify-kev.js.
const { JSDOM } = require('jsdom');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const html = fs.readFileSync(path.join(ROOT, 'kev', 'candidates', 'index.html'), 'utf8');
const realRows = JSON.parse(
  fs.readFileSync(path.join(ROOT, 'kev', 'candidates', 'kev-candidates-index.json'), 'utf8'));

const hostile = {
  id: 'CVE-2026-9999',
  name: '<img src=x onerror=window.__xss=1>',
  firstReported: '<b>bold</b>',
  firstExploit: '2999-01-01',
  disclose: '<svg/onload=window.__xss=2>',
  onKev: false,
  kevAdded: '',
  exploitToKev: null,
  status: '<script>window.__xss=3</script>',
  stories: 7,
  score: 9.9,
  analysis: false,
};
const hostileKev = {
  id: 'CVE-2026-8888',
  name: 'On KEV entry <img src=x onerror=window.__xss=4>',
  firstReported: '2026-06-01',
  firstExploit: '2026-07-01',
  disclose: '2026-06-01',
  onKev: true,
  kevAdded: '2026-08-01',
  exploitToKev: -3,
  status: 'exploited',
  stories: 2,
  score: 5.0,
  analysis: true,
};
const rows = [hostile, hostileKev, ...realRows.slice(0, 3)];

const dom = new JSDOM(html, {
  url: 'https://zarguell.github.io/tia-n-list/kev/candidates/',
  runScripts: 'dangerously',
  pretendToBeVisual: true,
  beforeParse(window) {
    window.__fetchUrls = [];
    window.fetch = url => {
      window.__fetchUrls.push(url);
      return Promise.resolve({ json: () => Promise.resolve(rows) });
    };
  },
});
const { window } = dom;
const d = window.document;
const ev = (el, type) => el.dispatchEvent(new window.Event(type));
const later = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  await later(300);
  const firstTr = d.querySelector('#cand-tbody tr');
  const byId = id => {
    const trs = d.querySelectorAll('#cand-tbody tr');
    for (const tr of trs) {
      if (tr.children[0].textContent === id) return tr;
    }
    return null;
  };
  const candRowCount = rows.filter(r => !r.onKev).length;
  const out = {
    rowsRendered: d.querySelectorAll('#cand-tbody tr').length,
    imgCount: d.querySelectorAll('#cand-tbody img, #cand-tbody svg').length,
    xssFired: window.__xss || null,
    hostileIsText: firstTr ? (firstTr.querySelector('img,svg') === null) : null,
    hostileHref: (function () { const a = d.querySelector('#cand-tbody tr a'); return a ? a.getAttribute('href') : null; })(),
    count: d.getElementById('f-count').textContent,
    viewCount: d.getElementById('view-count').textContent,
  };
  // default view is Pure candidates: on-KEV rows are hidden initially
  out.defaultIsCandidates = out.rowsRendered === candRowCount &&
    out.viewCount === candRowCount + ' not on KEV';
  // switch to All: on-KEV rows appear, links/columns check out
  d.querySelector('[data-view="all"]').click();
  await later(60);
  const kevTr = byId('CVE-2026-8888');
  out.allRows = d.querySelectorAll('#cand-tbody tr').length;
  out.allViewCount = d.getElementById('view-count').textContent;
  out.kevHref = kevTr ? kevTr.children[0].querySelector('a').getAttribute('href') : null;
  out.kevNameText = kevTr ? kevTr.children[1].textContent.trim() : null;
  out.kevDeltaText = kevTr ? kevTr.children[5].textContent : null;
  out.kevStatusText = kevTr ? kevTr.children[6].textContent.trim() : null;
  // status filter (All view): exploited only
  const chip = d.querySelector('[data-filter="status"][data-value="exploited"]');
  chip.click();
  await later(60);
  const exploitedRows = rows.filter(r => r.status === 'exploited');
  out.exploitCount = d.getElementById('f-count').textContent;
  out.exploitRows = d.querySelectorAll('#cand-tbody tr').length;
  // search (reset view + filter first)
  d.querySelector('[data-view="candidates"]').click();
  d.querySelector('[data-filter="status"][data-value="all"]').click();
  await later(60);
  const q = d.getElementById('f-q');
  q.value = '9999';
  ev(q, 'input');
  await later(60);
  out.searchCount = d.getElementById('f-count').textContent;
  out.searchRows = d.querySelectorAll('#cand-tbody tr').length;
  // S3(c): no data interpolation via innerHTML in the inline script
  const script = html.split('<script>')[1] || '';
  out.scriptUsesInnerHTMLWithData = /innerHTML\s*=\s*[^;]*(\+|`)/.test(script) || null;
  // the fetch target must be base-relative to the actual file (2026-08-13:
  // 'kev-candidates-index.json' resolved to the repo root -> live 404)
  out.fetchUrl = (window.__fetchUrls || [])[0] || null;
  console.log(JSON.stringify(out, null, 1));
  const ok =
    out.rowsRendered === candRowCount &&
    out.imgCount === 0 &&
    !out.xssFired &&
    out.hostileIsText === true &&
    out.hostileHref === 'kev/candidates/CVE-2026-9999/' &&
    out.count === candRowCount + ' of ' + candRowCount + ' shown' &&
    out.defaultIsCandidates === true &&
    out.allRows === rows.length &&
    out.allViewCount === 'All ' + rows.length &&
    out.kevHref === 'kev/cves/CVE-2026-8888/' &&
    out.kevNameText === 'On KEV entry <img src=x onerror=window.__xss=4>' &&
    out.kevDeltaText === '-3d' &&
    out.kevStatusText === 'On KEVExploited' &&
    out.exploitCount === exploitedRows.length + ' of ' + rows.length + ' shown' &&
    out.exploitRows === exploitedRows.length &&
    out.searchCount === '1 of ' + candRowCount + ' shown' &&
    out.searchRows === 1 &&
    out.fetchUrl === 'kev/candidates/kev-candidates-index.json' &&
    !out.scriptUsesInnerHTMLWithData;
  process.exit(ok ? 0 : 1);
})().catch(e => { console.error('FATAL', e); process.exit(1); });
