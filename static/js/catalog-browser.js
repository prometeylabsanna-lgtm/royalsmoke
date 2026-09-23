/* Royal Smoke — catalog browser filters: multi-select + price range + HTMX */
(function () {
  'use strict';

  function parseList(raw) {
    if (!raw) return [];
    return String(raw)
      .split(',')
      .map(function (s) { return s.trim(); })
      .filter(Boolean);
  }

  function unique(list) {
    var out = [];
    list.forEach(function (v) {
      if (out.indexOf(v) === -1) out.push(v);
    });
    return out;
  }

  function toggleIn(list, value) {
    var i = list.indexOf(value);
    if (i >= 0) {
      list.splice(i, 1);
      return list;
    }
    list.push(value);
    return list;
  }

  function pctOf(value, min, max) {
    if (max <= min) return 0;
    return ((value - min) / (max - min)) * 100;
  }

  function init(root) {
    if (!root || root.dataset.cbReady === '1') return;
    root.dataset.cbReady = '1';

    var boundMin = Number(root.getAttribute('data-cb-bound-min')) || 0;
    var boundMax = Number(root.getAttribute('data-cb-bound-max')) || 1;
    var symbol = root.getAttribute('data-cb-currency') || '₴';
    var isBrand = root.getAttribute('data-cb-brand') === '1';
    var basePath = root.getAttribute('data-cb-base') || '/catalog/';
    var listPath = root.getAttribute('data-cb-list') || '/catalog/';
    var strengthMap = parseList(root.getAttribute('data-cb-strength-map'));
    var reqSeq = 0;

    var state = {
      categories: parseList(root.getAttribute('data-cb-categories')),
      strength: parseList(root.getAttribute('data-cb-strength')),
      country: parseList(root.getAttribute('data-cb-country')),
      priceMin: Number(root.getAttribute('data-cb-price-min')),
      priceMax: Number(root.getAttribute('data-cb-price-max')),
      sort: root.getAttribute('data-cb-sort') || '',
      strengthTouched: false,
    };

    if (!Number.isFinite(state.priceMin)) state.priceMin = boundMin;
    if (!Number.isFinite(state.priceMax)) state.priceMax = boundMax;
    if (state.categories.length === 0) state.categories = ['all'];
    if (state.strength.length) state.strengthTouched = true;

    var minInput = root.querySelector('[data-cb-range-min]');
    var maxInput = root.querySelector('[data-cb-range-max]');
    var fill = root.querySelector('[data-cb-range-fill]');
    var tipMin = root.querySelector('[data-cb-tip-min]');
    var tipMax = root.querySelector('[data-cb-tip-max]');
    var resetBtn = root.querySelector('[data-cb-reset]');
    var strengthInput = root.querySelector('[data-cb-strength-range]');
    var strengthFill = root.querySelector('[data-cb-strength-fill]');

    function strengthIndexFromState() {
      if (state.strength.length !== 1) return 0;
      var only = state.strength[0];
      if (only === 'medium_full') only = 'medium';
      var idx = strengthMap.indexOf(only);
      return idx >= 0 ? idx : 0;
    }

    function syncStrengthUi() {
      var idx = strengthIndexFromState();
      if (strengthInput) strengthInput.value = String(idx);
      if (strengthFill && strengthInput) {
        var max = Number(strengthInput.max) || 2;
        var pct = max > 0 ? (idx / max) * 100 : 0;
        strengthFill.style.width = pct + '%';
      }
    }

    function syncCategoryUi() {
      var allActive = state.categories.length === 0
        || (state.categories.length === 1 && state.categories[0] === 'all');
      root.querySelectorAll('[data-cb-cat]').forEach(function (btn) {
        var val = btn.getAttribute('data-cb-cat');
        var on = val === 'all' ? allActive : state.categories.indexOf(val) >= 0;
        btn.classList.toggle('is-active', on);
        btn.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
    }

    function syncChipUi(key) {
      root.querySelectorAll('[data-cb-chip="' + key + '"]').forEach(function (btn) {
        var val = btn.getAttribute('data-cb-value');
        var on = state[key].indexOf(val) >= 0;
        btn.classList.toggle('is-active', on);
        btn.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
    }

    function syncSortUi() {
      root.querySelectorAll('[data-cb-sort-btn]').forEach(function (btn) {
        var val = btn.getAttribute('data-cb-sort-btn');
        var on = state.sort === val;
        btn.classList.toggle('is-active', on);
        btn.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
    }

    function setTip(el, value, show) {
      if (!el) return;
      el.textContent = value + ' ' + symbol;
      el.classList.toggle('is-hidden', !show);
      el.setAttribute('aria-hidden', show ? 'false' : 'true');
      var left = pctOf(value, boundMin, boundMax);
      el.style.left = left + '%';
    }

    function syncRangeUi() {
      if (minInput) minInput.value = String(state.priceMin);
      if (maxInput) maxInput.value = String(state.priceMax);
      if (fill && boundMax > boundMin) {
        var left = pctOf(state.priceMin, boundMin, boundMax);
        var right = pctOf(state.priceMax, boundMin, boundMax);
        fill.style.left = left + '%';
        fill.style.width = Math.max(0, right - left) + '%';
      }
      setTip(tipMin, state.priceMin, state.priceMin > boundMin);
      setTip(tipMax, state.priceMax, state.priceMax < boundMax);
      if (minInput && maxInput) {
        var minPct = pctOf(state.priceMin, boundMin, boundMax);
        var maxPct = pctOf(state.priceMax, boundMin, boundMax);
        minInput.style.zIndex = minPct > maxPct - 8 ? '5' : '3';
        maxInput.style.zIndex = '4';
      }
    }

    function hasActiveFilters() {
      var cats = state.categories.filter(function (c) { return c !== 'all'; });
      return cats.length > 0
        || state.strength.length > 0
        || state.country.length > 0
        || state.priceMin > boundMin
        || state.priceMax < boundMax
        || !!state.sort;
    }

    function syncResetUi() {
      if (!resetBtn) return;
      var on = hasActiveFilters();
      resetBtn.classList.toggle('is-disabled', !on);
      resetBtn.disabled = !on;
      if (on) resetBtn.removeAttribute('aria-disabled');
      else resetBtn.setAttribute('aria-disabled', 'true');
    }

    function syncAll() {
      syncCategoryUi();
      syncStrengthUi();
      syncChipUi('country');
      syncSortUi();
      syncRangeUi();
      syncResetUi();
    }

    function resolvePath() {
      if (isBrand) return basePath;
      var cats = state.categories.filter(function (c) { return c !== 'all'; });
      if (cats.length === 1) return listPath.replace(/\/?$/, '/') + cats[0] + '/';
      return listPath;
    }

    function buildQuery() {
      var qs = new URLSearchParams();
      var cats = state.categories.filter(function (c) { return c !== 'all'; });
      if (!isBrand && cats.length > 1) {
        cats.forEach(function (c) { qs.append('category', c); });
      }
      state.strength.forEach(function (v) { qs.append('strength', v); });
      state.country.forEach(function (v) { qs.append('country', v); });
      if (state.priceMin > boundMin) qs.set('price_min', String(state.priceMin));
      if (state.priceMax < boundMax) qs.set('price_max', String(state.priceMax));
      if (state.sort) qs.set('sort', state.sort);
      return qs;
    }

    function hydrateFromUrl() {
      var u = new URL(window.location.href);
      state.strength = u.searchParams.getAll('strength');
      state.country = u.searchParams.getAll('country');
      state.sort = u.searchParams.get('sort') || '';
      var pmin = Number(u.searchParams.get('price_min'));
      var pmax = Number(u.searchParams.get('price_max'));
      state.priceMin = Number.isFinite(pmin) ? pmin : boundMin;
      state.priceMax = Number.isFinite(pmax) ? pmax : boundMax;
      state.priceMin = Math.max(boundMin, Math.min(state.priceMin, boundMax));
      state.priceMax = Math.max(boundMin, Math.min(state.priceMax, boundMax));
      state.strengthTouched = state.strength.length > 0;

      if (isBrand) {
        state.categories = parseList(root.getAttribute('data-cb-categories'));
        if (!state.categories.length) state.categories = ['all'];
        return;
      }

      var cats = u.searchParams.getAll('category');
      if (cats.length) {
        state.categories = unique(cats);
        return;
      }

      var base = listPath.replace(/\/?$/, '/');
      var path = u.pathname.replace(/\/?$/, '/');
      if (path.indexOf(base) === 0 && path.length > base.length) {
        var slug = path.slice(base.length).replace(/\/$/, '');
        state.categories = slug ? [slug] : ['all'];
      } else {
        state.categories = ['all'];
      }
    }

    function applyFilters(shouldPush) {
      var path = resolvePath();
      var qs = buildQuery();
      var url = qs.toString() ? path + '?' + qs.toString() : path;

      if (typeof htmx === 'undefined') {
        window.location.href = url;
        return;
      }

      var seq = ++reqSeq;
      var req = htmx.ajax('GET', url, {
        target: '#product-grid',
        swap: 'innerHTML',
      });

      function afterSwap() {
        if (seq !== reqSeq) return;
        if (shouldPush !== false) {
          try {
            history.pushState({ rsCb: 1 }, '', url);
          } catch (err) { /* ignore */ }
        }
        syncResetUi();
      }

      if (req && typeof req.then === 'function') {
        req.then(afterSwap);
      } else {
        afterSwap();
      }
    }

    function applyFromHistory() {
      hydrateFromUrl();
      syncAll();
      var url = window.location.pathname + window.location.search;
      if (typeof htmx === 'undefined') {
        window.location.reload();
        return;
      }
      var seq = ++reqSeq;
      var req = htmx.ajax('GET', url, {
        target: '#product-grid',
        swap: 'innerHTML',
      });
      function afterSwap() {
        if (seq !== reqSeq) return;
        syncResetUi();
      }
      if (req && typeof req.then === 'function') {
        req.then(afterSwap);
      } else {
        afterSwap();
      }
    }

    root.addEventListener('click', function (e) {
      var catBtn = e.target.closest('[data-cb-cat]');
      if (catBtn && root.contains(catBtn)) {
        var cat = catBtn.getAttribute('data-cb-cat');
        if (cat === 'all') {
          state.categories = ['all'];
        } else {
          state.categories = state.categories.filter(function (c) { return c !== 'all'; });
          state.categories = unique(toggleIn(state.categories.slice(), cat));
          if (state.categories.length === 0) state.categories = ['all'];
        }
        syncCategoryUi();
        syncResetUi();
        return;
      }

      var chip = e.target.closest('[data-cb-chip]');
      if (chip && root.contains(chip)) {
        var key = chip.getAttribute('data-cb-chip');
        var val = chip.getAttribute('data-cb-value');
        if (key === 'country' && val) {
          state.country = unique(toggleIn(state.country.slice(), val));
          syncChipUi('country');
          syncResetUi();
        }
        return;
      }

      var sortBtn = e.target.closest('[data-cb-sort-btn]');
      if (sortBtn && root.contains(sortBtn)) {
        var sortVal = sortBtn.getAttribute('data-cb-sort-btn') || '';
        state.sort = state.sort === sortVal ? '' : sortVal;
        syncSortUi();
        applyFilters(true);
        return;
      }

      if (e.target.closest('[data-cb-apply]')) {
        applyFilters(true);
        return;
      }

      if (e.target.closest('[data-cb-reset]') && !resetBtn.disabled) {
        state.categories = ['all'];
        state.strength = [];
        state.strengthTouched = false;
        state.country = [];
        state.priceMin = boundMin;
        state.priceMax = boundMax;
        state.sort = '';
        syncAll();
        applyFilters(true);
      }
    });

    function onRangeInput(which) {
      var minVal = Number(minInput && minInput.value);
      var maxVal = Number(maxInput && maxInput.value);
      if (!Number.isFinite(minVal)) minVal = boundMin;
      if (!Number.isFinite(maxVal)) maxVal = boundMax;

      if (which === 'min' && minVal > maxVal) minVal = maxVal;
      if (which === 'max' && maxVal < minVal) maxVal = minVal;

      state.priceMin = Math.max(boundMin, Math.min(minVal, boundMax));
      state.priceMax = Math.max(boundMin, Math.min(maxVal, boundMax));
      syncRangeUi();
      syncResetUi();
    }

    function onStrengthInput() {
      if (!strengthInput) return;
      var idx = Number(strengthInput.value);
      if (!Number.isFinite(idx)) idx = 0;
      idx = Math.max(0, Math.min(idx, strengthMap.length - 1));
      state.strengthTouched = true;
      state.strength = strengthMap[idx] ? [strengthMap[idx]] : [];
      syncStrengthUi();
      syncResetUi();
    }

    if (minInput) {
      minInput.addEventListener('input', function () { onRangeInput('min'); });
      minInput.addEventListener('change', function () { onRangeInput('min'); });
    }
    if (maxInput) {
      maxInput.addEventListener('input', function () { onRangeInput('max'); });
      maxInput.addEventListener('change', function () { onRangeInput('max'); });
    }
    if (strengthInput) {
      strengthInput.addEventListener('input', onStrengthInput);
      strengthInput.addEventListener('change', onStrengthInput);
    }

    window.addEventListener('popstate', function () {
      applyFromHistory();
    });

    syncAll();
  }

  function boot() {
    var root = document.querySelector('[data-cb-root]');
    if (root) init(root);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
