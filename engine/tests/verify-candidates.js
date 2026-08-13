// Behavioral verification of the SHIPPED KEV-candidates dashboard (extracted
// from the generated page): hostile rows must render as text only (no img/svg
// elements, no handlers fire), status-filter/search behavior, default sort
// (first exploit report, newest first), CVE link hrefs (base-relative), and
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
  firstReported: '<img src=x onerror=window.__xss=1>',
  firstExploit: '2999-01-01',
  disclose: '<svg/onload=window.__xss=2>',
  status: '<script>window.__xss=3</script>',
  stories: 7,
  score: 9.9,
  analysis: false,
};
const rows = [hostile, ...realRows.slice(0, 3)];

const dom = new JSDOM(html, {
  url: 'https://zarguell.github.io/tia-n-list/kev/candidates/',
  runScripts: 'dangerously',
  pretendToBeVisual: true,
  beforeParse(window) {
    window.fetch = () => Promise.resolve({ json: () => Promise.resolve(rows) });
  },
});
const { window } = dom;
const d = window.document;
const ev = (el, type) => el.dispatchEvent(new window.Event(type));
const later = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  await later(300);
  const hostileTr = d.querySelector('#cand-tbody tr');
  const exploitedRows = rows.filter(r => r.status === 'exploited');
  const topId = rows.slice().sort((a, b) => String(b.firstExploit || '').localeCompare(String(a.firstExploit || '')))[0].id;
  const out = {
    rowsRendered: d.querySelectorAll('#cand-tbody tr').length,
    imgCount: d.querySelectorAll('#cand-tbody img, #cand-tbody svg').length,
    xssFired: window.__xss || null,
    hostileIsText: hostileTr ? (hostileTr.querySelector('img,svg') === null) : null,
    hostileHref: (function () {
      const a = d.querySelector('#cand-tbody tr a');
      return a ? a.getAttribute('href') : null;
    })(),
    topHref: (function () {
      const a = d.querySelector('#cand-tbody tr a');
      return a ? a.getAttribute('href') : null;
    })(),
    count: d.getElementById('f-count').textContent,
    statusCell: hostileTr ? hostileTr.children[4].textContent : null,
  };
  // default sort: first exploit report newest first
  out.topIsNewestExploit = out.topHref === 'candidates/' + topId + '/';
  // status filter
  const chip = d.querySelector('[data-filter="status"][data-value="exploited"]');
  chip.click();
  await later(60);
  out.exploitCount = d.getElementById('f-count').textContent;
  out.exploitRows = d.querySelectorAll('#cand-tbody tr').length;
  // search (after resetting the status filter)
  const all = d.querySelector('[data-filter="status"][data-value="all"]');
  all.click();
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
  console.log(JSON.stringify(out, null, 1));
  const ok =
    out.rowsRendered === rows.length &&
    out.imgCount === 0 &&
    !out.xssFired &&
    out.hostileIsText === true &&
    out.statusCell === '' &&
    out.hostileHref === 'candidates/CVE-2026-9999/' &&
    out.topIsNewestExploit === true &&
    out.exploitCount === exploitedRows.length + ' of ' + rows.length + ' shown' &&
    out.exploitRows === exploitedRows.length &&
    out.searchCount === '1 of 4 shown' &&
    out.searchRows === 1 &&
    !out.scriptUsesInnerHTMLWithData;
  process.exit(ok ? 0 : 1);
})().catch(e => { console.error('FATAL', e); process.exit(1); });
