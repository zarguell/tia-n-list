// Behavioral verification of the SHIPPED megapatch release page table.
//
// Regression (2026-11-13): commit fbbb7d66eb0 added `var PAGE = '{{ month.url }}'`
// to carry the page path into CVE links. It collided with the existing
// `var PAGE = 50` (rows per page) in the same IIFE, so `page * PAGE` was NaN and
// `list.slice(NaN, ...)` returned []: every release page rendered its 11-column
// header with ZERO rows while the counter said "208 of 208". No CI step covered
// the megapatch table, so it shipped.
//
// Contract:
//   1. the table body renders the fetched rows (capped at PAGE=50);
//   2. the counter reads "<shown> of <total>";
//   3. pagination appears when total > 50 and page 2 shows the next slice;
//   4. CVE links carry the release page path (the fix fbbb7d66eb0 intended),
//      not a bare '?cve=' that resolves to the site root via <base>;
//   5. filter chips narrow the table and reset to page 1;
//   6. row text is inserted as text (no img/svg, no handlers).
//
// Runs in CI (site-deploy.yml) after the build step, same recipe as
// verify-kev.js / verify-candidates.js.
const { JSDOM } = require('jsdom');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const MP = path.join(ROOT, 'megapatch');

// pick a release page that has a data file next to it
const candidates = [];
for (const track of fs.readdirSync(MP)) {
  const tdir = path.join(MP, track);
  if (!fs.statSync(tdir).isDirectory()) continue;
  for (const slug of fs.readdirSync(tdir)) {
    const json = path.join(tdir, slug + '.json');
    const page = path.join(tdir, slug, 'index.html');
    if (fs.existsSync(json) && fs.existsSync(page)) {
      candidates.push({ track, slug, json, page });
    }
  }
}
if (!candidates.length) {
  console.error('FAIL: no megapatch release page with a data file found');
  process.exit(1);
}
const rel = candidates[0];
const html = fs.readFileSync(rel.page, 'utf8');
const rows = JSON.parse(fs.readFileSync(rel.json, 'utf8'));
const PAGE = 50;

// hostile values must stay text
const hostile = {
  cve: 'CVE-2026-9999',
  title: '<img src=x onerror=window.__xss=1>',
  family: '<svg/onload=window.__xss=2>',
  severity: 'critical',
  score: 9.9, cvss: 9.9, epss_pct: 0.5,
  kev: true, automatable: 'yes', technical_impact: 'total',
  bod_public: '3_days', media: 2, three_day: true,
};
const data = [...rows, hostile];

const pageUrl = `https://zarguell.github.io/tia-n-list/megapatch/${rel.track}/${rel.slug}/`;
const dom = new JSDOM(html, {
  url: pageUrl,
  runScripts: 'dangerously',
  pretendToBeVisual: true,
  beforeParse(window) {
    window.__fetchUrls = [];
    window.fetch = (url) => {
      window.__fetchUrls.push(url);
      return Promise.resolve({ json: () => Promise.resolve(data) });
    };
  },
});
const { window } = dom;
const d = window.document;
const later = (ms) => new Promise((r) => setTimeout(r, ms));
const ev = (el, type) => el.dispatchEvent(new window.Event(type));

(async () => {
  await later(300);
  const total = data.length;
  const tbody = d.getElementById('mp-tbody');
  const out = {
    release: `${rel.track}/${rel.slug}`,
    total,
    fetchUrl: (window.__fetchUrls || [])[0] || null,
    expectedFetchUrl: `megapatch/${rel.track}/${rel.slug}.json`,
    rowsRendered: tbody.querySelectorAll('tr').length,
    expectedFirstPage: Math.min(total, PAGE),
    count: d.getElementById('mp-count').textContent,
    firstHref: (tbody.querySelector('tr a') || {}).getAttribute
      ? tbody.querySelector('tr a').getAttribute('href') : null,
    expectedHrefPrefix: `megapatch/${rel.track}/${rel.slug}/?cve=CVE-`,
    pagerButtons: d.querySelectorAll('#mp-pager button').length,
    expectedPager: Math.ceil(total / PAGE),
    imgCount: tbody.querySelectorAll('img, svg').length,
    xssFired: window.__xss || null,
  };

  // page 2 = the next slice, and the pager marks itself active
  if (out.pagerButtons > 1) {
    d.querySelectorAll('#mp-pager button')[1].click();
    await later(80);
    out.page2Rows = tbody.querySelectorAll('tr').length;
    out.expectedPage2 = Math.min(PAGE, total - PAGE);
    out.page2Active = d.querySelector('#mp-pager button.active').textContent;
  }

  // filter chip: only KEV rows, counter narrows, pager resets to page 1
  const kevChip = d.querySelector('[data-mp-filter="kev"]');
  kevChip.click();
  await later(80);
  out.kevRows = tbody.querySelectorAll('tr').length;
  out.expectedKevRows = Math.min(data.filter((r) => r.kev).length, PAGE);
  out.kevCount = d.getElementById('mp-count').textContent;
  out.kevTotal = data.filter((r) => r.kev).length;
  out.chipActive = kevChip.classList.contains('active');

  // hostile rows are text only
  const hostileRow = [...tbody.querySelectorAll('tr')].find(
    (tr) => (tr.children[1] || {}).textContent === 'CVE-2026-9999');
  out.hostileIsText = hostileRow
    ? hostileRow.querySelector('img, svg') === null : null;

  console.log(JSON.stringify(out, null, 1));

  const ok =
    out.fetchUrl === out.expectedFetchUrl &&
    out.rowsRendered > 0 &&
    out.rowsRendered === out.expectedFirstPage &&
    out.count === `${total} of ${total}` &&
    String(out.firstHref || '').startsWith(out.expectedHrefPrefix) &&
    out.pagerButtons === out.expectedPager &&
    out.imgCount === 0 &&
    out.xssFired === null &&
    (out.pagerButtons === 1 ||
      (out.page2Rows === out.expectedPage2 && out.page2Active === '2')) &&
    out.kevRows === out.expectedKevRows &&
    out.kevCount === `${out.kevTotal} of ${total}` &&
    out.chipActive === true &&
    (out.hostileIsText === null || out.hostileIsText === true);

  console.log(ok ? 'PASS megapatch release table' : 'FAIL megapatch release table');
  process.exit(ok ? 0 : 1);
})();
