/* Royal Smoke — brands snap (Cohiba-inspired, no GSAP)
   All viewports: soft proximity snap + image 100%→50% then text reveal (one-way).
   Snap only near the header line and only on the nearest panel (rarer / softer pull).
   Reverse scroll never trapped: snap off while scrolling up / near section top.
*/
(function () {
  'use strict';

  var SHRINK_MS = 1000;
  /* Text starts mid-shrink — earlier than waiting for width end */
  var TEXT_AT_MS = 580;
  var EASE = 'cubic-bezier(0.23, 1, 0.32, 1)';
  /* Fraction of viewport: snap engages only when panel top is this close to header */
  var SNAP_BAND = 0.11;
  /* Extra px slack so tiny trackpad jitter doesn’t re-arm snap */
  var SNAP_BAND_PX_MIN = 56;
  /* Play when panel is further into view (first slide waits a bit more) */
  var PLAY_RATIO = 0.4;
  var PLAY_RATIO_FIRST = 0.55;

  function prefersReduced() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function finishPanel(panel, asset, content) {
    if (!panel || panel.dataset.done === '1') return;
    panel.dataset.done = '1';
    if (asset) {
      asset.classList.add('is-shrinking', 'is-done');
      asset.style.transition = '';
      asset.style.width = '';
    }
    if (content) content.classList.add('is-done');
  }

  function playPanel(panel) {
    if (!panel || panel.dataset.done === '1' || panel.dataset.playing === '1') return;

    var asset = panel.querySelector('[data-snap-asset]');
    var content = panel.querySelector('[data-snap-content]');
    if (!asset || !content) return;

    if (prefersReduced()) {
      finishPanel(panel, asset, content);
      return;
    }

    panel.dataset.playing = '1';

    asset.classList.remove('is-shrinking', 'is-done');
    asset.style.width = '100%';
    asset.style.transition = 'none';
    void asset.offsetWidth;

    asset.style.transition = 'width ' + SHRINK_MS + 'ms ' + EASE;
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        asset.classList.add('is-shrinking');
        asset.style.width = '';
      });
    });

    var textTimer = window.setTimeout(function () {
      content.classList.add('is-done');
    }, TEXT_AT_MS);

    var settled = false;
    function settle() {
      if (settled) return;
      settled = true;
      asset.removeEventListener('transitionend', onEnd);
      window.clearTimeout(fallback);
      window.clearTimeout(textTimer);
      asset.classList.add('is-done');
      asset.style.transition = '';
      asset.style.width = '';
      content.classList.add('is-done');
      panel.dataset.done = '1';
      panel.dataset.playing = '0';
    }

    function onEnd(e) {
      if (e.target !== asset) return;
      if (e.propertyName && e.propertyName !== 'width') return;
      settle();
    }

    asset.addEventListener('transitionend', onEnd);
    var fallback = window.setTimeout(settle, SHRINK_MS + 140);
  }

  function init(root) {
    if (!root || root.dataset.brandsReady === '1') return;
    root.dataset.brandsReady = '1';

    var panels = Array.prototype.slice.call(root.querySelectorAll('[data-brand-snap]'));
    if (!panels.length) return;

    var snapZone = root.querySelector('[data-brands-snaps]') || root;
    var html = document.documentElement;
    var ioPanels = null;
    var zoneVisible = false;
    var lastY = window.scrollY || 0;
    var scrollingUp = false;
    var snapLockedOff = false;

    function headerInset() {
      var raw = getComputedStyle(html).getPropertyValue('--rs-header-h').trim();
      var h = parseFloat(raw);
      if (!isFinite(h) || h <= 0) h = 60;
      return h;
    }

    function clearSnapTargets() {
      panels.forEach(function (p) {
        p.classList.remove('is-snap-target');
      });
    }

    /** Only the nearest panel gets snap-align, and only inside a tight band. */
    function syncNearestSnapTarget() {
      clearSnapTargets();
      if (prefersReduced() || !zoneVisible) return false;

      var inset = headerInset();
      var band = Math.max(SNAP_BAND_PX_MIN, window.innerHeight * SNAP_BAND);
      var nearest = null;
      var nearestDist = Infinity;

      panels.forEach(function (p) {
        var dist = Math.abs(p.getBoundingClientRect().top - inset);
        if (dist < nearestDist) {
          nearestDist = dist;
          nearest = p;
        }
      });

      if (!nearest || nearestDist > band) return false;
      nearest.classList.add('is-snap-target');
      return true;
    }

    function setSnapAllowed(allow) {
      if (prefersReduced() || !zoneVisible) {
        clearSnapTargets();
        html.classList.remove('rs-brands-snap-on', 'rs-brands-snap-off');
        return;
      }
      html.classList.add('rs-brands-snap-on');
      if (allow && !snapLockedOff) {
        html.classList.remove('rs-brands-snap-off');
      } else {
        clearSnapTargets();
        html.classList.add('rs-brands-snap-off');
      }
    }

    function nearTopExit() {
      var rect = snapZone.getBoundingClientRect();
      return rect.top > -Math.min(120, window.innerHeight * 0.18);
    }

    function nearBottomExit() {
      var rect = snapZone.getBoundingClientRect();
      return rect.bottom < window.innerHeight * 0.72;
    }

    function updateSnapFromScroll() {
      var y = window.scrollY || 0;
      var dy = y - lastY;
      if (Math.abs(dy) > 1) scrollingUp = dy < 0;
      lastY = y;

      if (!zoneVisible) {
        setSnapAllowed(false);
        return;
      }

      if (scrollingUp || nearTopExit() || nearBottomExit()) {
        snapLockedOff = true;
        setSnapAllowed(false);
        return;
      }

      if (!scrollingUp && snapZone.getBoundingClientRect().top < -80) {
        snapLockedOff = false;
      }

      var inBand = syncNearestSnapTarget();
      setSnapAllowed(inBand);
    }

    function disconnectObservers() {
      if (ioPanels) {
        ioPanels.disconnect();
        ioPanels = null;
      }
    }

    function onZoneIntersect(entries) {
      zoneVisible = entries.some(function (e) {
        return e.isIntersecting;
      });
      if (!zoneVisible) {
        snapLockedOff = false;
        clearSnapTargets();
        html.classList.remove('rs-brands-snap-on', 'rs-brands-snap-off');
        return;
      }
      updateSnapFromScroll();
    }

    var ioZone = new IntersectionObserver(onZoneIntersect, {
      root: null,
      threshold: 0,
      rootMargin: '0px 0px 0px 0px',
    });

    function wirePanels() {
      disconnectObservers();
      clearSnapTargets();
      html.classList.remove('rs-brands-snap-on', 'rs-brands-snap-off');
      zoneVisible = false;
      snapLockedOff = false;

      ioZone.disconnect();
      ioZone.observe(snapZone);

      ioPanels = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (!entry.isIntersecting) return;
            var first = entry.target.getAttribute('data-index') === '0';
            var need = first ? PLAY_RATIO_FIRST : PLAY_RATIO;
            if (entry.intersectionRatio < need) return;
            playPanel(entry.target);
          });
        },
        {
          root: null,
          threshold: [0.35, 0.4, 0.45, 0.5, 0.55, 0.65, 0.75],
          rootMargin: '0px 0px -10% 0px',
        }
      );
      panels.forEach(function (p) {
        ioPanels.observe(p);
      });
    }

    function applyMode() {
      panels.forEach(function (p) {
        if (p.dataset.done === '1') return;
        var asset = p.querySelector('[data-snap-asset]');
        var content = p.querySelector('[data-snap-content]');
        p.dataset.playing = '0';
        if (asset) {
          asset.classList.remove('is-shrinking', 'is-done');
          asset.style.transition = '';
          asset.style.width = '';
        }
        if (content) content.classList.remove('is-done');
      });

      if (prefersReduced()) {
        disconnectObservers();
        ioZone.disconnect();
        clearSnapTargets();
        html.classList.remove('rs-brands-snap-on', 'rs-brands-snap-off');
        panels.forEach(function (p) {
          finishPanel(
            p,
            p.querySelector('[data-snap-asset]'),
            p.querySelector('[data-snap-content]')
          );
        });
        return;
      }

      wirePanels();
    }

    applyMode();

    window.addEventListener('scroll', updateSnapFromScroll, { passive: true });
    window.addEventListener('wheel', function (e) {
      if (e.deltaY < 0) {
        scrollingUp = true;
        snapLockedOff = true;
        setSnapAllowed(false);
      }
    }, { passive: true });

    var touchY = null;
    window.addEventListener('touchstart', function (e) {
      if (e.touches && e.touches[0]) touchY = e.touches[0].clientY;
    }, { passive: true });
    window.addEventListener('touchmove', function (e) {
      if (touchY == null || !e.touches || !e.touches[0]) return;
      var dy = e.touches[0].clientY - touchY;
      if (dy > 8) {
        scrollingUp = true;
        snapLockedOff = true;
        setSnapAllowed(false);
      }
      touchY = e.touches[0].clientY;
    }, { passive: true });

    window.addEventListener(
      'pagehide',
      function () {
        clearSnapTargets();
        html.classList.remove('rs-brands-snap-on', 'rs-brands-snap-off');
      },
      { passive: true }
    );
  }

  function boot() {
    document.querySelectorAll('[data-brands-craft]').forEach(init);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
