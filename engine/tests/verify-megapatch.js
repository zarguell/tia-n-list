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
  // comma + quote + newline exercise RFC4180 quoting; the leading '=' would be
  // run as a spreadsheet formula without the injection guard
  title: '=HYPERLINK("http://x"), quoted "title"\nsecond line',
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
    // jsdom has no blob URL / download plumbing: capture what the export builds
    window.__csvBlob = null;
    window.__csvDownload = null;
    window.URL.createObjectURL = (blob) => { window.__csvBlob = blob; return 'blob:fake'; };
    window.URL.revokeObjectURL = () => {};
    window.HTMLAnchorElement.prototype.click = function () {
      window.__csvDownload = this.download;
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
    firstTarget: (tbody.querySelector('tr a') || {}).getAttribute
      ? tbody.querySelector('tr a').getAttribute('target') : null,
    firstRel: (tbody.querySelector('tr a') || {}).getAttribute
      ? tbody.querySelector('tr a').getAttribute('rel') : null,
    expectedAdvisory: data[0].advisory,
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

  // ---- CSV export: all fields, RFC4180 escaped, filter-scoped ------------
  // A real CSV parser (quotes, doubled quotes, commas inside cells) so the
  // assertions below validate the escaping rather than assume it.
  function parseCsvLine(line) {
    const out = []; let cur = ''; let q = false;
    for (let i = 0; i < line.length; i++) {
      const ch = line[i];
      if (q) {
        if (ch === '"') {
          if (line[i + 1] === '"') { cur += '"'; i++; } else { q = false; }
        } else { cur += ch; }
      } else if (ch === '"') { q = true; }
      else if (ch === ',') { out.push(cur); cur = ''; }
      else { cur += ch; }
    }
    out.push(cur);
    return out;
  }
  await (async () => {
    const btn = d.getElementById('mp-export');
    out.exportButton = !!btn;
    out.exportDisabledWhenEmpty = (() => {
      // filter that matches nothing (no KEV rows in this release) -> disabled
      d.querySelector('[data-mp-filter="forensic"]').click();
      return btn.disabled;
    })();
    d.querySelector('[data-mp-filter="all"]').click();
    await later(80);
    out.exportLabel = btn.querySelector('.mp-export-label').textContent;
    out.exportEnabled = !btn.disabled;

    d.getElementById('mp-export').click();
    await later(80);
    const readBlob = (blob) => new Promise((res, rej) => {
      const fr = new window.FileReader();
      fr.onload = () => res(fr.result);
      fr.onerror = rej;
      fr.readAsText(blob);
    });
    const csv = await readBlob(window.__csvBlob);
    out.__csvPreview = csv.slice(0, 150);
    const lines = csv.replace(/^\ufeff/, '').split('\r\n').filter(Boolean);
    const H = parseCsvLine(lines[0]);
    out.csvDownload = window.__csvDownload;
    out.csvHeader = lines[0];
    out.csvColumns = H.length;
    out.csvLineCount = lines.length - 1;

    // every row has the same shape as the header (no ragged rows from a
    // comma/quote/newline inside a cell)
    const parsed = lines.slice(1).map(parseCsvLine);
    out.csvRagged = parsed.filter((r) => r.length !== H.length).length;

    const row = parsed[0];
    const col = (name) => row[H.indexOf(name)];
    out.csvFirstCve = col('cve');
    out.csvVendor = col('vendor');
    out.csvRelease = col('release');
    out.csvVector = col('cvss_vector');
    out.csvImpact = col('impact');
    out.csvAdvisory = col('advisory');
    out.csvReleaseUrl = col('release_url');
    out.csvVendorDoc = col('vendor_doc');
    out.csvTriState = { kev: col('kev'), exploited: col('exploited'),
                        threeDay: col('three_day'), disclosed: col('disclosed') };

    // the hostile row: commas/quotes survive, formula prefix is neutralised
    const hostileRow = parsed.find((r) => r[H.indexOf('cve')] === 'CVE-2026-9999');
    out.csvHostileTitle = hostileRow ? hostileRow[H.indexOf('title')] : null;
    out.csvHostileKe = hostileRow ? hostileRow[H.indexOf('kev')] : null;
    out.csvHostileThreeDay = hostileRow ? hostileRow[H.indexOf('three_day')] : null;

    // filter scoping: KEV narrows the export exactly like the table
    d.querySelector('[data-mp-filter="kev"]').click();
    await later(80);
    d.getElementById('mp-export').click();
    await later(80);
    const kevCsv = await readBlob(window.__csvBlob);
    out.csvKevLines = kevCsv.replace(/^\ufeff/, '').split('\r\n').filter(Boolean).length - 1;
    out.csvKevFilename = window.__csvDownload;
  })();


  // hostile rows are text only
  const hostileRow = [...tbody.querySelectorAll('tr')].find(
    (tr) => (tr.children[1] || {}).textContent === 'CVE-2026-9999');
  out.hostileIsText = hostileRow
    ? hostileRow.querySelector('img, svg') === null : null;
  out.hostileHref = hostileRow && hostileRow.children[1].querySelector('a')
    ? hostileRow.children[1].querySelector('a').getAttribute('href') : null;

  // ---- ?cve= deep links (story pages -> release) still filter the table ----
  {
    const cve = data[0].cve;
    const dom2 = new JSDOM(html, {
      url: pageUrl + '?cve=' + encodeURIComponent(cve),
      runScripts: 'dangerously',
      pretendToBeVisual: true,
      beforeParse(w) {
        w.fetch = () => Promise.resolve({ json: () => Promise.resolve(data) });
      },
    });
    await later(300);
    const d2 = dom2.window.document;
    out.deepLinkQuery = d2.getElementById('mp-q').value;
    out.deepLinkRows = d2.querySelectorAll('#mp-tbody tr').length;
    out.deepLinkExpected = data.filter((r) => r.cve === cve).length;
    dom2.window.close();
  }

  console.log(JSON.stringify(out, null, 1));

  const ok =
    out.fetchUrl === out.expectedFetchUrl &&
    out.rowsRendered > 0 &&
    out.rowsRendered === out.expectedFirstPage &&
    out.count === `${total} of ${total}` &&
    out.firstHref === out.expectedAdvisory &&
    /^https:\/\//.test(String(out.firstHref)) &&
    !String(out.firstHref).includes('?cve=') &&
    out.firstTarget === '_blank' &&
    /noopener/.test(String(out.firstRel)) &&
    out.pagerButtons === out.expectedPager &&
    out.imgCount === 0 &&
    out.xssFired === null &&
    (out.pagerButtons === 1 ||
      (out.page2Rows === out.expectedPage2 && out.page2Active === '2')) &&
    out.kevRows === out.expectedKevRows &&
    out.kevCount === `${out.kevTotal} of ${total}` &&
    out.chipActive === true &&
    (out.hostileIsText === null || out.hostileIsText === true) &&
    (out.hostileHref === null ||
      out.hostileHref === 'https://nvd.nist.gov/vuln/detail/CVE-2026-9999') &&
    // CSV export: all fields, properly escaped, filter scoped
    out.exportButton === true &&
    out.exportLabel === 'Export CSV · ' + total &&
    out.exportDisabledWhenEmpty === true &&
    out.exportEnabled === true &&
    out.csvColumns === 33 &&
    out.csvLineCount === total &&
    out.csvRagged === 0 &&
    /^megapatch-[a-z0-9-]+\.csv$/.test(String(out.csvDownload)) &&
    out.csvVendor === 'Adobe' &&
    out.csvRelease === 'September 2026' &&
    /^CVSS:3\.1\/AV:/.test(String(out.csvVector)) &&
    typeof out.csvImpact === 'string' &&      // column present (MS-only value)
    /^https:\/\//.test(String(out.csvAdvisory)) &&
    String(out.csvReleaseUrl).startsWith('megapatch/') &&
    /^https:\/\//.test(String(out.csvVendorDoc)) &&
    out.csvTriState.kev === 'no' &&
    out.csvTriState.exploited === 'no' &&
    out.csvTriState.threeDay === '' &&
    out.csvTriState.disclosed === 'no' &&
    out.csvHostileTitle ===
      "'=HYPERLINK(\"http://x\"), quoted \"title\" second line" &&
    out.csvHostileKe === 'yes' &&
    out.csvHostileThreeDay === 'yes' &&
    out.csvKevLines === data.filter((r) => r.kev).length &&
    // the in-page filter is still reachable via ?cve= (story links use it)
    out.deepLinkQuery === data[0].cve &&
    out.deepLinkRows === out.deepLinkExpected;

  console.log(ok ? 'PASS megapatch release table' : 'FAIL megapatch release table');
  process.exit(ok ? 0 : 1);
})();
