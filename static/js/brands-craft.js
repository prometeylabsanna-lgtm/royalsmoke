/* Royal Smoke — brands snap (Cohiba-inspired, no GSAP)
   Desktop ≥768: soft proximity snap + image 100%→50% then text reveal (one-way).
   Reverse scroll never trapped: snap off while scrolling up / near section top.
   Mobile: simple reveal once.
*/
(function () {
  'use strict';

  var MQ = '(min-width: 768px)';
  var SHRINK_MS = 780;
  var TEXT_DELAY_MS = 160;
  var EASE = 'cubic-bezier(0.22, 1, 0.36, 1)';

  function prefersReduced() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function isDesktop() {
    return window.matchMedia(MQ).matches;
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

  function playDesktop(panel) {
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

    var settled = false;
    function settle() {
      if (settled) return;
      settled = true;
      asset.removeEventListener('transitionend', onEnd);
      window.clearTimeout(fallback);
      asset.classList.add('is-done');
      asset.style.transition = '';
      asset.style.width = '';
      window.setTimeout(function () {
        content.classList.add('is-done');
        panel.dataset.done = '1';
        panel.dataset.playing = '0';
      }, TEXT_DELAY_MS);
    }

    function onEnd(e) {
      if (e.target !== asset) return;
      if (e.propertyName && e.propertyName !== 'width') return;
      settle();
    }

    asset.addEventListener('transitionend', onEnd);
    var fallback = window.setTimeout(settle, SHRINK_MS + 140);
  }

  function playMobile(panel) {
    if (!panel || panel.dataset.done === '1') return;
    var asset = panel.querySelector('[data-snap-asset]');
    var content = panel.querySelector('[data-snap-content]');
    finishPanel(panel, asset, content);
  }

  function play(panel) {
    if (isDesktop()) playDesktop(panel);
    else playMobile(panel);
  }

  function init(root) {
    if (!root || root.dataset.brandsReady === '1') return;
    root.dataset.brandsReady = '1';

    var panels = Array.prototype.slice.call(root.querySelectorAll('[data-brand-snap]'));
    if (!panels.length) return;

    var snapZone = root.querySelector('[data-brands-snaps]') || root;
    var html = document.documentElement;
    var ioPanels = null;
    var mq = window.matchMedia(MQ);
    var zoneVisible = false;
    var lastY = window.scrollY || 0;
    var scrollingUp = false;
    var snapLockedOff = false;

    function setSnapAllowed(allow) {
      if (!isDesktop() || prefersReduced() || !zoneVisible) {
        html.classList.remove('rs-brands-snap-on', 'rs-brands-snap-off');
        return;
      }
      html.classList.add('rs-brands-snap-on');
      if (allow && !snapLockedOff) {
        html.classList.remove('rs-brands-snap-off');
      } else {
        html.classList.add('rs-brands-snap-off');
      }
    }

    function nearTopExit() {
      var rect = snapZone.getBoundingClientRect();
      // Top of brands zone near/above viewport — free scroll to hero
      return rect.top > -Math.min(120, window.innerHeight * 0.18);
    }

    function updateSnapFromScroll() {
      var y = window.scrollY || 0;
      var dy = y - lastY;
      if (Math.abs(dy) > 1) scrollingUp = dy < 0;
      lastY = y;

      if (!zoneVisible || !isDesktop()) {
        setSnapAllowed(false);
        return;
      }

      // Reverse scroll or leaving toward hero: disable snap so it never traps
      if (scrollingUp || nearTopExit()) {
        snapLockedOff = true;
        setSnapAllowed(false);
        return;
      }

      // Scrolling down deeper into brands: soft proximity ok again
      if (!scrollingUp && snapZone.getBoundingClientRect().top < -40) {
        snapLockedOff = false;
      }
      setSnapAllowed(true);
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

    function wireDesktop() {
      disconnectObservers();
      html.classList.remove('rs-brands-snap-on', 'rs-brands-snap-off');
      zoneVisible = false;
      snapLockedOff = false;

      ioZone.disconnect();
      ioZone.observe(snapZone);

      ioPanels = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (!entry.isIntersecting) return;
            if (entry.intersectionRatio < 0.28) return;
            play(entry.target);
          });
        },
        { root: null, threshold: [0.28, 0.45, 0.65] }
      );
      panels.forEach(function (p) {
        ioPanels.observe(p);
      });
    }

    function wireMobile() {
      disconnectObservers();
      html.classList.remove('rs-brands-snap-on', 'rs-brands-snap-off');
      ioZone.disconnect();

      ioPanels = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (!entry.isIntersecting) return;
            play(entry.target);
          });
        },
        { root: null, threshold: 0.2, rootMargin: '0px 0px -8% 0px' }
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

      if (isDesktop()) wireDesktop();
      else wireMobile();
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

    function onMqChange() {
      applyMode();
    }
    if (mq.addEventListener) mq.addEventListener('change', onMqChange);
    else if (mq.addListener) mq.addListener(onMqChange);

    window.addEventListener(
      'pagehide',
      function () {
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
