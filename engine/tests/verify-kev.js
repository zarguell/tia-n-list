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
  dateAdded: '2099-01-01',
};
const rows = [hostile, ...realRows.slice(0, 3)];

const dom = new JSDOM(html, {
  url: 'https://zarguell.github.io/tia-n-list/kev/',
  runScripts: 'dangerously',
  pretendToBeVisual: true,
  beforeParse(window) {
    window.fetch = () => Promise.resolve({ json: () => Promise.resolve(rows) });
    // start from "no stack saved" regardless of the harness
    try { window.localStorage.removeItem('ts-kev-stack'); } catch (e) {}
  },
});
const { window } = dom;
const d = window.document;
const ev = (el, type) => el.dispatchEvent(new window.Event(type));
const later = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  await later(300); // inline script fetch + render
  // Locate hostile row by its ID (not position — sorting may reorder)
  const allTrs = d.querySelectorAll('#kev-tbody tr');
  let hostileTr = null;
  for (let i = 0; i < allTrs.length; i++) {
    const link = allTrs[i].querySelector('a');
    if (link && link.textContent === 'CVE-2026-9999') { hostileTr = allTrs[i]; break; }
  }
  const out = {
    rowsRendered: allTrs.length,
    imgCount: d.querySelectorAll('#kev-tbody img, #kev-tbody svg').length,
    xssFired: window.__xss || null,
    hostileCell: hostileTr ? hostileTr.textContent.slice(0, 60) : null,
    hostileIsText: hostileTr ? (hostileTr.querySelector('img,svg') === null) : null,
    hostileHref: (function () {
      const a = hostileTr ? hostileTr.querySelector('a') : null;
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
  // ---- "My stack" picker (2026-11-13) -----------------------------------
  // Tick one vendor/product pair: the catalog must keep only those rows, the
  // selection must persist, and Clear must restore the full list.
  // reset the exploit chip left active by the previous block
  d.querySelector('[data-filter="auto"][data-value="all"]').click();  // All = reset (see dashboard)
  await later(60);
  out.stackMounted = !!d.querySelector('#stack-panel .stack');
  out.stackItems = d.querySelectorAll('#stack-panel .stack-item').length;
  out.stackMatchesPairs = (() => {
    const pairs = new Set(rows.filter((r) => r.vendor && r.product)
      .map((r) => r.vendor + '|' + r.product));
    return out.stackItems === pairs.size;
  })();
  // pick the first real (non-hostile) row's pair
  const realRow = rows.find((r) => r.id === realRows[0].id);
  const pairKey = realRow.vendor + '|' + realRow.product;
  const box = [...d.querySelectorAll('#stack-panel input[type=checkbox]')]
    .find((cb) => cb.value === pairKey);
  box.checked = true;
  box.dispatchEvent(new window.Event('change'));
  await later(80);
  out.stackCount = d.getElementById('f-count').textContent;
  out.stackRows = d.querySelectorAll('#kev-tbody tr').length;
  out.expectedStackRows = rows.filter(
    (r) => r.vendor === realRow.vendor && r.product === realRow.product).length;
  out.stackPersisted = JSON.parse(
    window.localStorage.getItem('ts-kev-stack') || '[]');
  out.stackSummary = d.querySelector('#stack-panel .stack-count').textContent;
  // search still narrows within the stack
  q.value = realRow.id;
  ev(q, 'input');
  await later(60);
  out.stackSearchRows = d.querySelectorAll('#kev-tbody tr').length;
  q.value = '';
  ev(q, 'input');
  // clear restores everything
  d.querySelector('#stack-panel .stack-clear').click();
  await later(80);
  out.stackAfterClear = d.getElementById('f-count').textContent;

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
    !out.scriptInlinesIndex &&
    // My stack
    out.stackMounted === true &&
    out.stackItems > 0 &&
    out.stackMatchesPairs === true &&
    out.stackRows === out.expectedStackRows &&
    out.stackRows < rows.length &&
    Array.isArray(out.stackPersisted) &&
    out.stackPersisted.length === 1 &&
    out.stackPersisted[0] === pairKey &&
    /1 selected/.test(out.stackSummary) &&
    out.stackSearchRows === 1 &&
    out.stackAfterClear === rows.length + ' of ' + rows.length + ' shown';
  process.exit(ok ? 0 : 1);
})().catch(e => { console.error('FATAL', e); process.exit(1); });
