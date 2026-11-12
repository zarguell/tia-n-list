// "My stack": pick the vendor/product pairs you run and keep only those KEV
// entries. Client-side only — the selection lives in localStorage under
// ts-kev-stack and never leaves the browser. Included inline by both
// kev_index.html and kev_deadlines.html so there is one implementation.
window.KevStack = (function () {
  var KEY = 'ts-kev-stack';
  var active = new Set();       // selected "<vendor>|<product>" keys
  var items = [];               // [{key, vendor, product}] sorted, deduped

  function itemKey(vendor, product) {
    return (vendor || '') + '|' + (product || '');
  }
  function label(item) {
    return item.product ? item.vendor + ' — ' + item.product : item.vendor;
  }
  function load() {
    try {
      var raw = JSON.parse(window.localStorage.getItem(KEY) || '[]');
      active = new Set(Array.isArray(raw) ? raw.filter(function (x) {
        return typeof x === 'string' && x.indexOf('|') !== -1;
      }) : []);
    } catch (e) {
      active = new Set();      // storage blocked (private mode, quota) -> empty
    }
    return active;
  }
  function save() {
    try { window.localStorage.setItem(KEY, JSON.stringify(Array.from(active))); } catch (e) {}
  }
  function build(rows) {
    var seen = Object.create(null);
    items = [];
    (rows || []).forEach(function (r) {
      var key = itemKey(r.vendor, r.product);
      if (seen[key] || (!r.vendor && !r.product)) return;
      seen[key] = 1;
      items.push({ key: key, vendor: r.vendor || '', product: r.product || '' });
    });
    items.sort(function (a, b) {
      return label(a).toLowerCase() < label(b).toLowerCase() ? -1 : 1;
    });
    return items;
  }
  // no selection = everything (an empty stack must not blank the catalog)
  function matches(r) {
    return active.size === 0 || active.has(itemKey(r.vendor, r.product));
  }
  function count() { return active.size; }

  function mount(host, rows, onChange) {
    if (!host) return null;
    build(rows);
    load();

    var details = document.createElement('details');
    details.className = 'stack';

    var summary = document.createElement('summary');
    summary.className = 'stack-summary';
    var sumLabel = document.createElement('span');
    sumLabel.textContent = 'My stack';
    var sumCount = document.createElement('span');
    sumCount.className = 'stack-count';
    summary.appendChild(sumLabel);
    summary.appendChild(sumCount);

    var panel = document.createElement('div');
    panel.className = 'stack-panel';

    var hint = document.createElement('p');
    hint.className = 'stack-hint';
    hint.textContent = 'Tick what you run — the catalog then shows only those entries. Saved in this browser only.';
    panel.appendChild(hint);

    var tools = document.createElement('div');
    tools.className = 'stack-tools';
    var search = document.createElement('input');
    search.type = 'search';
    search.className = 'stack-search';
    search.placeholder = 'Filter vendors and products';
    search.setAttribute('aria-label', 'Filter the stack list');
    var clear = document.createElement('button');
    clear.type = 'button';
    clear.className = 'chip stack-clear';
    clear.textContent = 'Clear';
    tools.appendChild(search);
    tools.appendChild(clear);
    panel.appendChild(tools);

    var list = document.createElement('div');
    list.className = 'stack-list';
    panel.appendChild(list);

    var boxes = [];
    items.forEach(function (item) {
      var lab = document.createElement('label');
      lab.className = 'stack-item';
      var cb = document.createElement('input');
      cb.type = 'checkbox';
      cb.value = item.key;
      cb.checked = active.has(item.key);
      var span = document.createElement('span');
      span.textContent = label(item);
      lab.appendChild(cb);
      lab.appendChild(span);
      lab.dataset.label = label(item).toLowerCase();
      list.appendChild(lab);
      boxes.push(cb);
      cb.addEventListener('change', function () {
        if (cb.checked) active.add(cb.value); else active.delete(cb.value);
        save();
        refresh();
        if (onChange) onChange();
      });
    });

    function refresh() {
      sumCount.textContent = active.size ? ' · ' + active.size + ' selected' : '';
      details.classList.toggle('is-active', active.size > 0);
      clear.disabled = active.size === 0;
    }

    clear.addEventListener('click', function () {
      active = new Set();
      boxes.forEach(function (cb) { cb.checked = false; });
      save();
      refresh();
      if (onChange) onChange();
    });
    search.addEventListener('input', function () {
      var term = search.value.trim().toLowerCase();
      Array.prototype.forEach.call(list.children, function (lab) {
        lab.hidden = term !== '' && lab.dataset.label.indexOf(term) === -1;
      });
    });

    details.appendChild(summary);
    details.appendChild(panel);
    host.appendChild(details);
    refresh();
    return details;
  }

  return {
    mount: mount,
    matches: matches,
    count: count,
    itemKey: itemKey,
    load: load,
    _items: function () { return items; },
  };
})();
