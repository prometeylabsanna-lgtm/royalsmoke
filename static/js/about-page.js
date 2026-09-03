(function () {
  'use strict';

  var reduceMotion =
    window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function easeOutCubic(t) {
    return 1 - Math.pow(1 - t, 3);
  }

  function animateCounter(el, target, duration) {
    if (reduceMotion || !duration) {
      el.textContent = String(target);
      return;
    }

    var start = null;

    function frame(ts) {
      if (start === null) start = ts;
      var p = Math.min(1, (ts - start) / duration);
      el.textContent = String(Math.round(easeOutCubic(p) * target));
      if (p < 1) {
        window.requestAnimationFrame(frame);
      }
    }

    window.requestAnimationFrame(frame);
  }

  function initCounters() {
    var nodes = document.querySelectorAll('[data-rs-counter]');
    if (!nodes.length) return;

    if (!('IntersectionObserver' in window)) {
      nodes.forEach(function (el) {
        var target = parseInt(el.getAttribute('data-rs-counter'), 10) || 0;
        el.textContent = String(target);
      });
      return;
    }

    var seen = new WeakSet();
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting || seen.has(entry.target)) return;
          seen.add(entry.target);
          var target =
            parseInt(entry.target.getAttribute('data-rs-counter'), 10) || 0;
          animateCounter(entry.target, target, 1400);
          io.unobserve(entry.target);
        });
      },
      { threshold: 0.35, rootMargin: '0px 0px -8% 0px' }
    );

    nodes.forEach(function (el) {
      io.observe(el);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCounters);
  } else {
    initCounters();
  }
})();
