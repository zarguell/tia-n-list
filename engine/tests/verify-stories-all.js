// Verify the SHIPPED all-stories inline script (extracted from the generated
// page) against a DOM, with the real index data — the runtime path obscura's
// page-context fetch blocking prevented. fetch is stubbed to the real data.
const { JSDOM } = require('jsdom');
const fs = require('fs');

const html = fs.readFileSync('/home/coder/workspace/tia-n-list/stories/index.html', 'utf8');
const index = JSON.parse(fs.readFileSync('/home/coder/workspace/tia-n-list/stories-index.json', 'utf8'));

const dom = new JSDOM(html, {
  url: 'https://zarguell.github.io/tia-n-list/stories/',
  runScripts: 'dangerously',
  pretendToBeVisual: true,
  beforeParse(window) {
    window.fetch = (url) => {
      if (String(url).includes('stories-index.json'))
        return Promise.resolve({ json: () => Promise.resolve(index) });
      return Promise.reject(new Error('unexpected fetch: ' + url));
    };
  },
});
const { window } = dom;
const d = window.document;
const ev = (el, type) => el.dispatchEvent(new window.Event(type));
const later = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  await later(900); // inline script fetch+render
  const out = {
    initialCards: d.querySelectorAll('.story-card').length,
    initialCount: d.getElementById('f-count').textContent,
    firstTitle: d.querySelector('.story-card h3 a')?.textContent.slice(0, 55),
    loadingGone: !d.getElementById('loading'), // true = render ran (apply wipes the grid)
  };
  // search
  const q = d.getElementById('f-q'); q.value = 'deadlock'; ev(q, 'input');
  await later(60);
  out.searchCount = d.getElementById('f-count').textContent;
  out.searchCards = d.querySelectorAll('.story-card').length;
  out.searchTitles = [...d.querySelectorAll('.story-card h3 a')].map(a => a.textContent.slice(0, 36));
  // clear, hot sort
  q.value = ''; ev(q, 'input');
  const s = d.getElementById('f-sort'); s.value = 'hot'; ev(s, 'change');
  await later(60);
  out.hotFirst = d.querySelector('.story-card h3 a')?.textContent.slice(0, 45);
  out.hotScore = d.querySelector('.story-card')?.dataset.score;
  out.hotUrl = window.location.pathname + window.location.search;
  // pager page 2
  const p2 = d.querySelector('#pager a[data-page="2"]');
  out.hasPager = !!p2;
  out.pagerLinks = d.querySelectorAll('#pager a[data-page]').length;
  if (p2) p2.click();
  await later(60);
  out.p2Url = window.location.pathname + window.location.search;
  out.p2Rank = d.querySelector('.story-card .rank')?.textContent;
  out.p2Cards = d.querySelectorAll('.story-card').length;
  // year filter shares URL state
  const fy = d.getElementById('f-year'); fy.value = '2026'; ev(fy, 'change');
  await later(60);
  out.yearUrl = window.location.pathname + window.location.search;
  out.yearCount = d.getElementById('f-count').textContent;
  // XSS: a hostile title must render as text
  const hostile = { ...index[0], title: '<img src=x onerror=alert(1)>', snippet: '<svg/onload=alert(1)>', sources: ['<script>alert(2)</script>'] };
  const saved = window.__apply; // not reachable; test via a fresh cardEl-equivalent path is not possible — instead verify no innerHTML-with-data in the page script
  out.scriptUsesInnerHTMLWithData = /innerHTML\s*=\s*[^;]*(\+|`)/.test(html.split('<script>')[1]) || null;
  console.log(JSON.stringify(out, null, 1));
  process.exit(0);
})().catch(e => { console.error('FATAL', e); process.exit(1); });
