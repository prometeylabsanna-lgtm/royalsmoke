/* Royal Smoke — main UI interactions */
(function () {
  'use strict';

  var COOKIE = 'age_ok';
  var COOKIE_DAYS = 30;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function setCookie(name, value, days) {
    var maxAge = days * 24 * 60 * 60;
    document.cookie =
      name + '=' + encodeURIComponent(value) +
      '; path=/; max-age=' + maxAge +
      '; SameSite=Lax';
  }

  function qs(sel, root) {
    return (root || document).querySelector(sel);
  }

  function qsa(sel, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  }

  /* ——— Age gate ——— */
  function initAgeGate() {
    var gate = qs('[data-age-gate]');
    if (!gate) return;

    var yesBtn = qs('[data-age-yes]', gate);
    var noBtn = qs('[data-age-no]', gate);
    var resetBtn = qs('[data-age-reset]', gate);

    function closeGate() {
      gate.classList.add('is-gate-out');
      window.setTimeout(function () {
        if (gate.parentNode) gate.parentNode.removeChild(gate);
        document.body.style.overflow = '';
      }, reduceMotion ? 0 : 320);
    }

    if (yesBtn) {
      yesBtn.addEventListener('click', function () {
        setCookie(COOKIE, '1', COOKIE_DAYS);
        closeGate();
      });
    }

    if (noBtn) {
      noBtn.addEventListener('click', function () {
        setCookie(COOKIE, '0', COOKIE_DAYS);
        gate.classList.add('is-denied');
        gate.setAttribute('aria-labelledby', 'age-gate-denied-title');
      });
    }

    if (resetBtn) {
      resetBtn.addEventListener('click', function () {
        setCookie(COOKIE, '', -1);
        gate.classList.remove('is-denied');
        gate.setAttribute('aria-labelledby', 'age-gate-title');
      });
    }

    if (gate.getAttribute('data-denied') === '1') {
      gate.classList.add('is-denied');
      gate.setAttribute('aria-labelledby', 'age-gate-denied-title');
    }
  }

  /* ——— iOS scroll lock ——— */
  var lockY = 0;
  var lockCount = 0;

  function lockScroll() {
    if (lockCount === 0) {
      lockY = window.scrollY || window.pageYOffset || 0;
      document.body.classList.add('is-locked');
      document.body.style.top = '-' + lockY + 'px';
    }
    lockCount += 1;
  }

  function unlockScroll() {
    if (lockCount === 0) return;
    lockCount -= 1;
    if (lockCount > 0) return;
    document.body.classList.remove('is-locked');
    document.body.style.top = '';
    window.scrollTo(0, lockY);
  }

  /* ——— Drawer ——— */
  function initDrawer() {
    var drawer = qs('[data-drawer]');
    var backdrop = qs('[data-drawer-backdrop]');
    var openBtns = qsa('[data-drawer-open]');
    var closeBtns = qsa('[data-drawer-close]');
    if (!drawer) return;

    var openBtn = qs('[data-drawer-open]');
    var focusableSel = 'a[href], button:not([disabled]), input, select, textarea, [tabindex]:not([tabindex="-1"])';
    var touchStartX = 0;

    function setExpanded(open) {
      openBtns.forEach(function (btn) {
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    }

    function openDrawer() {
      drawer.classList.add('is-open');
      drawer.setAttribute('aria-hidden', 'false');
      drawer.removeAttribute('inert');
      if (backdrop) backdrop.classList.add('is-open');
      setExpanded(true);
      lockScroll();
      var first = qs(focusableSel, drawer);
      if (first) first.focus();
    }

    function closeDrawer() {
      drawer.classList.remove('is-open');
      drawer.setAttribute('aria-hidden', 'true');
      drawer.setAttribute('inert', '');
      if (backdrop) backdrop.classList.remove('is-open');
      setExpanded(false);
      unlockScroll();
      if (openBtn) openBtn.focus();
    }

    openBtns.forEach(function (btn) {
      btn.addEventListener('click', openDrawer);
    });
    closeBtns.forEach(function (btn) {
      btn.addEventListener('click', closeDrawer);
    });
    if (backdrop) backdrop.addEventListener('click', closeDrawer);

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawer.classList.contains('is-open')) {
        closeDrawer();
      }
      if (e.key !== 'Tab' || !drawer.classList.contains('is-open')) return;
      var nodes = qsa(focusableSel, drawer);
      if (!nodes.length) return;
      var first = nodes[0];
      var last = nodes[nodes.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    });

    drawer.addEventListener('touchstart', function (e) {
      if (!e.changedTouches || !e.changedTouches.length) return;
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    drawer.addEventListener('touchend', function (e) {
      if (!e.changedTouches || !e.changedTouches.length) return;
      var dx = e.changedTouches[0].screenX - touchStartX;
      if (dx > 60) closeDrawer();
    }, { passive: true });
  }

  /* ——— Sticky header ——— */
  function initHeader() {
    var header = qs('[data-header]');
    if (!header) return;
    var ticking = false;

    function apply() {
      var y = window.scrollY || window.pageYOffset || 0;
      var start = 12;
      var range = 160;
      var t = (y - start) / range;
      if (t < 0) t = 0;
      if (t > 1) t = 1;
      /* smoothstep — softer than linear */
      t = t * t * (3 - 2 * t);
      header.style.setProperty('--rs-header-solid', t.toFixed(4));
      if (t >= 0.92) header.classList.add('is-solid');
      else header.classList.remove('is-solid');
      ticking = false;
    }

    function onScroll() {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(apply);
    }

    apply();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ——— Search popover ——— */
  function initSearch() {
    var root = qs('[data-search]');
    if (!root) return;

    var panel = qs('[data-search-panel]', root);
    var openBtn = qs('[data-search-open]', root);
    var input = qs('[data-search-input]', root);
    var results = qs('[data-search-results]', root);
    if (!panel || !openBtn) return;

    function isOpen() {
      return panel.classList.contains('is-open');
    }

    function openSearch() {
      panel.hidden = false;
      panel.classList.add('is-open');
      openBtn.setAttribute('aria-expanded', 'true');
      window.setTimeout(function () {
        if (input) input.focus();
      }, 30);
    }

    function closeSearch() {
      panel.classList.remove('is-open');
      panel.hidden = true;
      openBtn.setAttribute('aria-expanded', 'false');
      if (results) results.innerHTML = '';
      if (input) input.value = '';
    }

    openBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      if (isOpen()) closeSearch();
      else openSearch();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && isOpen()) {
        closeSearch();
        openBtn.focus();
      }
    });

    document.addEventListener('click', function (e) {
      if (!isOpen()) return;
      if (root.contains(e.target)) return;
      closeSearch();
    });

    panel.addEventListener('click', function (e) {
      e.stopPropagation();
    });

    document.body.addEventListener('htmx:beforeRequest', function (e) {
      var elt = e.detail && e.detail.elt;
      if (!elt || elt !== input) return;
      if ((elt.value || '').trim().length < 2) {
        e.preventDefault();
        if (results) results.innerHTML = '';
      }
    });
  }

  /* ——— Reveal ——— */
  var revealObserver = null;

  function initReveal() {
    var nodes = qsa('[data-rs-reveal]').filter(function (n) {
      /* Never hide chrome/layout shells */
      if (n.classList.contains('rs-footer') || n.classList.contains('rs-header')) return false;
      return !n.classList.contains('is-in');
    });
    if (!nodes.length) return;

    if (revealObserver) {
      revealObserver.disconnect();
      revealObserver = null;
    }

    if (reduceMotion || !('IntersectionObserver' in window)) {
      nodes.forEach(function (n) { n.classList.add('is-in'); });
      return;
    }

    revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        revealObserver.unobserve(el);
        el.classList.add('is-in');
      });
    }, {
      rootMargin: '0px 0px -48px 0px',
      threshold: 0.15
    });

    nodes.forEach(function (n, i) {
      var delay = n.getAttribute('data-reveal-delay');
      if (delay == null || delay === '') {
        delay = String((i % 5) * 120);
        n.setAttribute('data-reveal-delay', delay);
      }
      n.style.setProperty('--rs-reveal-delay', delay + 'ms');
      /* Already on screen at boot — show immediately */
      var rect = n.getBoundingClientRect();
      if (rect.top < window.innerHeight * 1.15 && rect.bottom > -40) {
        n.classList.add('is-in');
        return;
      }
      revealObserver.observe(n);
    });
  }

  /* ——— Floating actions + back-to-top ——— */
  function initFloat() {
    var floatEl = qs('[data-float]');
    var topBtn = qs('[data-back-top]');
    var lastY = window.scrollY || 0;
    var ticking = false;

    function jumpTop() {
      var se = document.scrollingElement || document.documentElement;
      if (se) se.scrollTop = 0;
      if (document.documentElement) document.documentElement.scrollTop = 0;
      if (document.body) document.body.scrollTop = 0;
      window.scrollTo(0, 0);
    }

    function syncTopBtn(y) {
      if (!topBtn) return;
      var threshold = Math.max(window.innerHeight || 0, 1);
      var show = y >= threshold;
      if (show) {
        topBtn.hidden = false;
        topBtn.removeAttribute('aria-hidden');
      } else {
        topBtn.hidden = true;
        topBtn.setAttribute('aria-hidden', 'true');
      }
    }

    function update() {
      var y = window.scrollY || window.pageYOffset || 0;
      if (floatEl) {
        if (y > lastY + 8 && y > 120) {
          floatEl.classList.add('is-hidden');
        } else if (y < lastY - 8) {
          floatEl.classList.remove('is-hidden');
        }
      }
      syncTopBtn(y);
      lastY = y;
      ticking = false;
    }

    if (topBtn) {
      topBtn.addEventListener('click', function (e) {
        e.preventDefault();
        jumpTop();
        lastY = 0;
        syncTopBtn(window.scrollY || window.pageYOffset || 0);
      });
    }

    window.addEventListener('scroll', function () {
      if (!ticking) {
        ticking = true;
        window.requestAnimationFrame(update);
      }
    }, { passive: true });

    syncTopBtn(window.scrollY || window.pageYOffset || 0);
  }

  /* ——— Callback modal ——— */
  function initCallback() {
    var triggers = qsa('[data-callback-open]');
    var panel = qs('[data-callback-panel]');
    if (!panel || !triggers.length) return;
    var closeBtns = qsa('[data-callback-close]', panel);
    var dialog = qs('.rs-callback__dialog', panel);

    function openPanel() {
      panel.hidden = false;
      panel.setAttribute('aria-hidden', 'false');
      lockScroll();
      var first = qs('input, button', panel);
      if (first) first.focus();
    }

    function closePanel() {
      panel.hidden = true;
      panel.setAttribute('aria-hidden', 'true');
      unlockScroll();
    }

    triggers.forEach(function (t) {
      t.addEventListener('click', openPanel);
    });
    closeBtns.forEach(function (b) {
      b.addEventListener('click', closePanel);
    });

    panel.addEventListener('click', function (e) {
      if (e.target === panel) closePanel();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !panel.hidden) closePanel();
    });

    if (dialog) {
      dialog.addEventListener('click', function (e) {
        e.stopPropagation();
      });
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    initAgeGate();
    initDrawer();
    initHeader();
    initSearch();
    initReveal();
    initFloat();
    initCallback();
  });

  /* Nova Poshta autocomplete selection (CSP-safe; no inline handlers) */
  document.body.addEventListener('click', function (e) {
    var cityBtn = e.target && e.target.closest
      ? e.target.closest('[data-np-city-ref]')
      : null;
    if (cityBtn) {
      var cityRef = document.getElementById('id_np_city_ref');
      var cityInput = document.getElementById('id_delivery_city');
      var whRef = document.getElementById('id_np_warehouse_ref');
      var whInput = document.getElementById('id_delivery_address');
      var citiesBox = document.getElementById('np-cities-results');
      var whBox = document.getElementById('np-warehouses-results');
      if (cityRef) cityRef.value = cityBtn.getAttribute('data-np-city-ref') || '';
      if (cityInput) cityInput.value = cityBtn.getAttribute('data-np-city-name') || '';
      if (whRef) whRef.value = '';
      if (whInput) whInput.value = '';
      if (citiesBox) citiesBox.innerHTML = '';
      if (whBox) whBox.innerHTML = '';
      return;
    }

    var whBtn = e.target && e.target.closest
      ? e.target.closest('[data-np-wh-ref]')
      : null;
    if (whBtn) {
      var warehouseRef = document.getElementById('id_np_warehouse_ref');
      var addressInput = document.getElementById('id_delivery_address');
      var warehousesBox = document.getElementById('np-warehouses-results');
      var deliverySelect = document.getElementById('id_delivery_service');
      if (warehouseRef) {
        warehouseRef.value = whBtn.getAttribute('data-np-wh-ref') || '';
      }
      if (addressInput) {
        addressInput.value = whBtn.getAttribute('data-np-wh-name') || '';
      }
      if (warehousesBox) warehousesBox.innerHTML = '';
      if (deliverySelect) {
        deliverySelect.dispatchEvent(new Event('change', { bubbles: true }));
      }
    }
  });

  document.body.addEventListener('htmx:afterSwap', function (e) {
    initReveal();
    if (window.RsValidate && typeof window.RsValidate.init === 'function') {
      window.RsValidate.init(e && e.detail && e.detail.target ? e.detail.target : document);
    }
  });
})();
