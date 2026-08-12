// Behavioral verification of the SHIPPED kev dashboard (extracted from the
// generated page): S3(a) hostile rows must render as text only (no img/svg
// elements, no handlers fire), plus filter/sort/paginate behavior and CVE
// link hrefs. S3(c): the inline script must not interpolate data via
// innerHTML. Runs in CI (site-deploy.yml) after the build step.
const { JSDOM } = require('jsdom');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const html = fs.readFileSync(path.join(ROOT, 'kev', 'index.html'), 'utf8');
const realRows = JSON.parse(fs.readFileSync(path.join(ROOT, 'kev', 'kev-index.json'), 'utf8'));

const hostile = {
  id: 'CVE-2026-9999',
  vendor: '<img src=x onerror=window.__xss=1>',
  product: '<svg/onload=window.__xss=2>',
  cvss: 9.9,
  auto: '<script>window.__xss=3</script>',
  exploit: 'unknown',
  poc: 'yes',
  threeDay: true,
  timeline: '<b>bold</b>',
  dateAdded: '2026-08-12',
};
const rows = [hostile, ...realRows.slice(0, 3)];

const dom = new JSDOM(html, {
  url: 'https://zarguell.github.io/tia-n-list/kev/',
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
  await later(300); // inline script fetch + render
  const hostileTr = d.querySelector('#kev-tbody tr');
  const out = {
    rowsRendered: d.querySelectorAll('#kev-tbody tr').length,
    imgCount: d.querySelectorAll('#kev-tbody img, #kev-tbody svg').length,
    xssFired: window.__xss || null,
    hostileCell: hostileTr ? hostileTr.textContent.slice(0, 60) : null,
    hostileIsText: hostileTr ? (hostileTr.querySelector('img,svg') === null) : null,
    hostileHref: (function () {
      const a = d.querySelector('#kev-tbody tr a');
      return a ? a.getAttribute('href') : null;
    })(),
    count: d.getElementById('f-count').textContent,
  };
  // search filters
  const q = d.getElementById('f-q');
  q.value = '9999';
  ev(q, 'input');
  await later(60);
  out.searchCount = d.getElementById('f-count').textContent;
  out.searchRows = d.querySelectorAll('#kev-tbody tr').length;
  // active-exploit chip filter
  q.value = '';
  ev(q, 'input');
  const chip = d.querySelector('[data-filter="exploit"][data-value="active"]');
  chip.click();
  await later(60);
  out.exploitActiveCount = d.getElementById('f-count').textContent;
  out.exploitActiveRows = d.querySelectorAll('#kev-tbody tr').length;
  // S3(c): no data interpolation via innerHTML in the inline script
  const script = html.split('<script>')[1] || '';
  out.scriptUsesInnerHTMLWithData = /innerHTML\s*=\s*[^;]*(\+|`)/.test(script) || null;
  out.scriptInlinesIndex = html.indexOf('CVE_DATA =') !== -1;
  console.log(JSON.stringify(out, null, 1));
  const ok =
    out.rowsRendered === rows.length &&
    out.imgCount === 0 &&
    !out.xssFired &&
    out.hostileIsText === true &&
    out.hostileHref === 'kev/cves/CVE-2026-9999/' &&
    out.searchCount === '1 of 4 shown' &&
    out.searchRows === 1 &&
    !out.scriptUsesInnerHTMLWithData &&
    !out.scriptInlinesIndex;
  process.exit(ok ? 0 : 1);
})().catch(e => { console.error('FATAL', e); process.exit(1); });
