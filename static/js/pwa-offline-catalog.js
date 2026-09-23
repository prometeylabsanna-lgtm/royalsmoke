/* Offline catalog renderer from /pwa/offline-catalog.json */
(function () {
  'use strict';

  var DATA_URL = '/pwa/offline-catalog.json';

  function qs(sel, root) {
    return (root || document).querySelector(sel);
  }

  function escapeHtml(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function detectLang(pathname) {
    if (pathname.indexOf('/en/') === 0 || pathname === '/en') return 'en';
    if (pathname.indexOf('/zh-hans/') === 0 || pathname === '/zh-hans') return 'zh-hans';
    return 'uk';
  }

  function stripLang(pathname) {
    return pathname.replace(/^\/(en|zh-hans)(?=\/|$)/, '') || '/';
  }

  function catalogBase(lang) {
    if (lang === 'uk') return '/catalog';
    return '/' + lang + '/catalog';
  }

  function parseRoute(pathname) {
    var lang = detectLang(pathname);
    var path = stripLang(pathname).replace(/\/+$/, '') || '/';
    if (path === '/catalog') {
      return { lang: lang, type: 'list', slug: '' };
    }
    var mProduct = path.match(/^\/catalog\/product\/([^/]+)$/);
    if (mProduct) return { lang: lang, type: 'product', slug: decodeURIComponent(mProduct[1]) };
    var mBrand = path.match(/^\/catalog\/brand\/([^/]+)$/);
    if (mBrand) return { lang: lang, type: 'brand', slug: decodeURIComponent(mBrand[1]) };
    var mCat = path.match(/^\/catalog\/([^/]+)$/);
    if (mCat) return { lang: lang, type: 'category', slug: decodeURIComponent(mCat[1]) };
    return { lang: lang, type: 'list', slug: '' };
  }

  function loadI18n() {
    try {
      return JSON.parse(qs('#rs-offline-i18n').textContent || '{}');
    } catch (e) {
      return {};
    }
  }

  function t(pack, key) {
    return (pack && pack[key]) || key;
  }

  function priceHtml(pack, product, currency) {
    var sym = (currency && currency.symbol) || '';
    var html = '<p class="rs-pwa-off__price">' + escapeHtml(sym) + ' ' + escapeHtml(product.price);
    if (product.old_price) {
      html += ' <s>' + escapeHtml(sym) + ' ' + escapeHtml(product.old_price) + '</s>';
    }
    html += '</p>';
    return html;
  }

  function productCard(pack, p, currency) {
    var img = p.image
      ? '<img src="' + escapeHtml(p.image) + '" alt="" loading="lazy" decoding="async">'
      : '<img alt="" width="1" height="1">';
    return (
      '<li><a class="rs-pwa-off__card" href="' + escapeHtml(p.url) + '">' +
      img +
      '<p class="rs-pwa-off__card-meta">' + escapeHtml(p.brand_name) + '</p>' +
      '<p class="rs-pwa-off__card-name">' + escapeHtml(p.name) + '</p>' +
      priceHtml(pack, p, currency) +
      '</a></li>'
    );
  }

  function renderList(main, pack, langData, route) {
    var products = langData.products || [];
    var categories = langData.categories || [];
    var brands = langData.brands || [];
    var title = t(pack, 'all');
    var filtered = products;

    if (route.type === 'category') {
      var cat = categories.filter(function (c) { return c.slug === route.slug; })[0];
      title = cat ? cat.name : route.slug;
      filtered = products.filter(function (p) { return p.category_slug === route.slug; });
    } else if (route.type === 'brand') {
      var brand = brands.filter(function (b) { return b.slug === route.slug; })[0];
      title = brand ? brand.name : route.slug;
      filtered = products.filter(function (p) { return p.brand_slug === route.slug; });
    }

    var chips = [
      '<a class="rs-pwa-off__chip' + (route.type === 'list' ? ' is-active' : '') +
      '" href="' + catalogBase(route.lang) + '/">' + escapeHtml(t(pack, 'all')) + '</a>'
    ];
    categories.forEach(function (c) {
      chips.push(
        '<a class="rs-pwa-off__chip' + (route.type === 'category' && route.slug === c.slug ? ' is-active' : '') +
        '" href="' + escapeHtml(c.url) + '">' + escapeHtml(c.name) + '</a>'
      );
    });
    brands.slice(0, 12).forEach(function (b) {
      chips.push(
        '<a class="rs-pwa-off__chip' + (route.type === 'brand' && route.slug === b.slug ? ' is-active' : '') +
        '" href="' + escapeHtml(b.url) + '">' + escapeHtml(b.name) + '</a>'
      );
    });

    var cards = filtered.map(function (p) {
      return productCard(pack, p, langData.currency);
    }).join('');

    main.innerHTML =
      '<h1 class="rs-pwa-off__title">' + escapeHtml(title) + '</h1>' +
      '<nav class="rs-pwa-off__nav" aria-label="' + escapeHtml(t(pack, 'categories')) + '">' +
      chips.join('') + '</nav>' +
      (cards
        ? '<ul class="rs-pwa-off__grid">' + cards + '</ul>'
        : '<p class="rs-pwa-off__empty">' + escapeHtml(t(pack, 'empty')) + '</p>');
  }

  function renderProduct(main, pack, langData, route) {
    var p = (langData.products || []).filter(function (x) { return x.slug === route.slug; })[0];
    if (!p) {
      main.innerHTML = '<p class="rs-pwa-off__empty">' + escapeHtml(t(pack, 'empty')) + '</p>';
      return;
    }
    var cur = langData.currency || {};
    var specs = [];
    if (p.country) specs.push([t(pack, 'country'), p.country]);
    if (p.strength) specs.push([t(pack, 'strength'), p.strength]);
    if (p.smoke_time) specs.push([t(pack, 'smoke'), p.smoke_time]);
    if (p.wrapper || p.binder || p.filler) {
      specs.push([t(pack, 'blend'), [p.wrapper, p.binder, p.filler].filter(Boolean).join(' / ')]);
    }
    var stockLabel = p.stock > 0
      ? t(pack, 'stock') + ': ' + p.stock
      : t(pack, 'out');

    main.innerHTML =
      '<a class="rs-pwa-off__link" href="' + catalogBase(route.lang) + '/">' +
      escapeHtml(t(pack, 'back')) + '</a>' +
      '<article class="rs-pwa-off__detail">' +
      '<div class="rs-pwa-off__detail-media">' +
      (p.image ? '<img src="' + escapeHtml(p.image) + '" alt="">' : '') +
      '</div><div>' +
      '<p class="rs-pwa-off__card-meta">' + escapeHtml(p.brand_name) +
      (p.category_name ? ' · ' + escapeHtml(p.category_name) : '') + '</p>' +
      '<h1>' + escapeHtml(p.name) + '</h1>' +
      priceHtml(pack, p, cur) +
      '<p class="rs-pwa-off__card-meta">' + escapeHtml(stockLabel) + '</p>' +
      (p.short_story ? '<p>' + escapeHtml(p.short_story) + '</p>' : '') +
      (p.description ? '<p>' + escapeHtml(p.description) + '</p>' : '') +
      (p.tasting_notes ? '<p><strong>' + escapeHtml(t(pack, 'notes')) + ':</strong> ' +
        escapeHtml(p.tasting_notes) + '</p>' : '') +
      (specs.length
        ? '<ul class="rs-pwa-off__specs">' + specs.map(function (row) {
          return '<li><span>' + escapeHtml(row[0]) + '</span><span>' +
            escapeHtml(row[1]) + '</span></li>';
        }).join('') + '</ul>'
        : '') +
      '</div></article>';
  }

  function applyPack(pack) {
    var stale = qs('[data-i18n="stale"]');
    if (stale && pack.stale) stale.textContent = pack.stale;
  }

  function render(data) {
    var route = parseRoute(window.location.pathname);
    var i18n = loadI18n();
    var pack = i18n[route.lang] || i18n.uk || {};
    applyPack(pack);
    document.documentElement.lang = route.lang;
    var langData = (data.langs && data.langs[route.lang]) || (data.langs && data.langs.uk) || {};
    var meta = qs('[data-offline-meta]');
    if (meta) {
      meta.textContent = t(pack, 'updated') + ': ' + (data.generated_at || '—');
    }
    var main = qs('#rs-offline-main');
    if (!main) return;
    if (!langData.products || !langData.products.length) {
      main.innerHTML = '<p class="rs-pwa-off__empty">' + escapeHtml(t(pack, 'empty')) + '</p>';
      return;
    }
    if (route.type === 'product') renderProduct(main, pack, langData, route);
    else renderList(main, pack, langData, route);
  }

  function boot() {
    if (!qs('[data-rs-offline-root]')) return;
    fetch(DATA_URL, { credentials: 'same-origin' })
      .then(function (r) { return r.json(); })
      .then(render)
      .catch(function () {
        var route = parseRoute(window.location.pathname);
        var pack = (loadI18n()[route.lang]) || {};
        var main = qs('#rs-offline-main');
        if (main) {
          main.innerHTML = '<p class="rs-pwa-off__empty">' + escapeHtml(t(pack, 'empty')) + '</p>';
        }
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
