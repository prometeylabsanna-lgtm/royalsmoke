/* Royal Smoke — cart rapid-click guard + multi-tab badge sync */
(function () {
  'use strict';

  var DEBOUNCE_MS = 300;
  var STORAGE_KEY = 'rs_cart_sync';
  var refreshing = false;

  function qs(sel, root) {
    return (root || document).querySelector(sel);
  }

  function isCartForm(form) {
    if (!form || form.tagName !== 'FORM') return false;
    if (form.hasAttribute('data-rs-cart-guard')) return true;
    var action = form.getAttribute('hx-post') || form.getAttribute('action') || '';
    return /\/cart\//.test(action);
  }

  function formFromEventTarget(elt) {
    if (!elt) return null;
    if (elt.tagName === 'FORM') return elt;
    if (elt.form) return elt.form;
    var formId = elt.getAttribute && elt.getAttribute('form');
    if (formId) return document.getElementById(formId);
    return elt.closest ? elt.closest('form') : null;
  }

  function setDisabled(form, on) {
    if (!form) return;
    var nodes = form.querySelectorAll('button, input[type="submit"]');
    Array.prototype.forEach.call(nodes, function (el) {
      el.disabled = !!on;
    });
    if (form.id) {
      Array.prototype.forEach.call(
        document.querySelectorAll('button[form="' + form.id + '"], input[form="' + form.id + '"]'),
        function (el) {
          el.disabled = !!on;
        }
      );
    }
  }

  function withinDebounce(form) {
    var now = Date.now();
    var prev = parseInt(form.getAttribute('data-rs-cart-ts') || '0', 10);
    if (prev && now - prev < DEBOUNCE_MS) return true;
    form.setAttribute('data-rs-cart-ts', String(now));
    return false;
  }

  function notifyOtherTabs() {
    try {
      localStorage.setItem(STORAGE_KEY, String(Date.now()));
    } catch (e) { /* private mode */ }
  }

  function badgeUrl() {
    return document.body.getAttribute('data-rs-cart-badge-url') || '';
  }

  function refreshBadge() {
    var url = badgeUrl();
    var badge = qs('#cart-badge');
    if (!url || !badge || refreshing) return;
    refreshing = true;
    fetch(url, {
      credentials: 'same-origin',
      headers: { 'HX-Request': 'true', 'X-Requested-With': 'XMLHttpRequest' },
    })
      .then(function (r) { return r.ok ? r.text() : ''; })
      .then(function (html) {
        if (!html) return;
        var tmp = document.createElement('div');
        tmp.innerHTML = html.trim();
        var next = tmp.firstElementChild;
        if (next && badge.parentNode) {
          badge.parentNode.replaceChild(next, badge);
        }
      })
      .catch(function () { /* ignore */ })
      .then(function () { refreshing = false; });
  }

  document.body.addEventListener('htmx:beforeRequest', function (evt) {
    var form = formFromEventTarget(evt.detail && evt.detail.elt);
    if (!isCartForm(form)) return;
    if (withinDebounce(form)) {
      evt.preventDefault();
      return;
    }
    setDisabled(form, true);
  });

  document.body.addEventListener('htmx:afterRequest', function (evt) {
    var form = formFromEventTarget(evt.detail && evt.detail.elt);
    if (!isCartForm(form)) return;
    setDisabled(form, false);
    notifyOtherTabs();
  });

  document.body.addEventListener('htmx:sendError', function (evt) {
    var form = formFromEventTarget(evt.detail && evt.detail.elt);
    if (isCartForm(form)) setDisabled(form, false);
  });

  document.body.addEventListener('htmx:responseError', function (evt) {
    var form = formFromEventTarget(evt.detail && evt.detail.elt);
    if (isCartForm(form)) setDisabled(form, false);
  });

  document.addEventListener('submit', function (evt) {
    var form = evt.target;
    if (!isCartForm(form)) return;
    if (form.hasAttribute('hx-post') || form.hasAttribute('hx-get')) return;
    if (withinDebounce(form)) {
      evt.preventDefault();
      return;
    }
    setDisabled(form, true);
  }, true);

  window.addEventListener('storage', function (evt) {
    if (evt.key === STORAGE_KEY) refreshBadge();
  });

  window.addEventListener('pageshow', function (evt) {
    if (evt.persisted) refreshBadge();
  });
})();
