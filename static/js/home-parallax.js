/* Royal Smoke — home parallax: media only, never layout sections */
(function () {
  'use strict';

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var media = [];
  var ticking = false;
  var listening = false;

  function collect() {
    media = Array.prototype.slice
      .call(document.querySelectorAll('[data-parallax-media]'))
      .filter(function (el) {
        /* Never transform reveal hosts — fights opacity/transform reveal */
        return !el.hasAttribute('data-rs-reveal');
      })
      .map(function (el) {
        var depth = parseFloat(el.getAttribute('data-depth') || '0.08');
        if (isNaN(depth)) depth = 0.08;
        return { el: el, depth: Math.min(depth, 0.14) };
      });
  }

  function apply() {
    var vh = window.innerHeight || 1;
    for (var i = 0; i < media.length; i++) {
      var item = media[i];
      var rect = item.el.getBoundingClientRect();
      if (rect.bottom < -80 || rect.top > vh + 80) continue;
      var center = rect.top + rect.height * 0.5;
      var offset = (center - vh * 0.5) * item.depth * -0.45;
      if (offset > 18) offset = 18;
      if (offset < -18) offset = -18;
      item.el.style.transform = 'translate3d(0,' + offset.toFixed(2) + 'px,0)';
    }
    ticking = false;
  }

  function onScroll() {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(apply);
    }
  }

  function boot() {
    /* Clear leftover section transforms from older parallax builds */
    Array.prototype.forEach.call(
      document.querySelectorAll('[data-parallax-layer], [data-parallax-fixed], .rs-section, .rs-history-journey'),
      function (el) {
        if (el.hasAttribute('data-parallax-media')) return;
        el.style.transform = '';
      }
    );

    collect();
    if (!media.length) return;
    if (!listening) {
      listening = true;
      window.addEventListener('scroll', onScroll, { passive: true });
      window.addEventListener('resize', function () {
        collect();
        apply();
      }, { passive: true });
    }
    apply();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
