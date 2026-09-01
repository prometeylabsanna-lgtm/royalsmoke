/* Royal Smoke — home catalog horizontal slider */
(function () {
  'use strict';

  function prefersReducedMotion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function initCatalogSlider(root) {
    if (!root || root.dataset.catalogReady === '1') return;
    root.dataset.catalogReady = '1';

    var track = root.querySelector('[data-catalog-track]');
    var btnPrev = root.querySelector('[data-catalog-prev]');
    var btnNext = root.querySelector('[data-catalog-next]');
    if (!track) return;

    function slideStep() {
      var slide = track.querySelector('[data-catalog-slide]');
      if (!slide) return Math.max(track.clientWidth * 0.75, 160);
      var styles = window.getComputedStyle(track);
      var gap = parseFloat(styles.columnGap || styles.gap) || 0;
      return slide.getBoundingClientRect().width + gap;
    }

    function maxScroll() {
      return Math.max(0, track.scrollWidth - track.clientWidth);
    }

    function updateNav() {
      var left = track.scrollLeft;
      var max = maxScroll();
      var eps = 2;
      if (btnPrev) btnPrev.disabled = left <= eps;
      if (btnNext) btnNext.disabled = left >= max - eps;
    }

    function scrollByDir(dir) {
      var reduce = prefersReducedMotion();
      var left = track.scrollLeft + dir * slideStep();
      if (typeof track.scrollTo === 'function') {
        track.scrollTo({
          left: left,
          behavior: reduce ? 'auto' : 'smooth',
        });
      } else {
        track.scrollLeft = left;
      }
    }

    if (btnPrev) {
      btnPrev.addEventListener('click', function () {
        scrollByDir(-1);
      });
    }
    if (btnNext) {
      btnNext.addEventListener('click', function () {
        scrollByDir(1);
      });
    }

    track.addEventListener(
      'scroll',
      function () {
        updateNav();
      },
      { passive: true }
    );

    track.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') {
        e.preventDefault();
        scrollByDir(1);
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault();
        scrollByDir(-1);
      } else if (e.key === 'Home') {
        e.preventDefault();
        if (typeof track.scrollTo === 'function') {
          track.scrollTo({ left: 0, behavior: prefersReducedMotion() ? 'auto' : 'smooth' });
        } else {
          track.scrollLeft = 0;
        }
      } else if (e.key === 'End') {
        e.preventDefault();
        if (typeof track.scrollTo === 'function') {
          track.scrollTo({ left: maxScroll(), behavior: prefersReducedMotion() ? 'auto' : 'smooth' });
        } else {
          track.scrollLeft = maxScroll();
        }
      }
    });

    window.addEventListener(
      'resize',
      function () {
        updateNav();
      },
      { passive: true }
    );

    updateNav();
  }

  function boot() {
    document.querySelectorAll('[data-catalog-slider]').forEach(initCatalogSlider);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
