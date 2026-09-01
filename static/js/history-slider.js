/* Royal Smoke — history journey: loop arrows + tick highlight (no scroll highlight) */
(function () {
  'use strict';

  function prefersReducedMotion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function initHistoryJourney(root) {
    if (!root || root.dataset.historyReady === '1') return;
    root.dataset.historyReady = '1';

    var track = root.querySelector('[data-history-track]');
    var slides = Array.prototype.slice.call(root.querySelectorAll('[data-history-slide]'));
    var ticks = Array.prototype.slice.call(root.querySelectorAll('[data-history-tick]'));
    var btnPrev = root.querySelector('[data-history-prev]');
    var btnNext = root.querySelector('[data-history-next]');
    var total = slides.length;
    if (!track || !total) return;

    var index = 0;

    function updateActive(activeIndex) {
      ticks.forEach(function (tick, i) {
        var on = i === activeIndex;
        tick.classList.toggle('is-active', on);
        if (on) tick.setAttribute('aria-current', 'true');
        else tick.removeAttribute('aria-current');
      });
      slides.forEach(function (slide, i) {
        var on = i === activeIndex;
        slide.classList.toggle('is-active', on);
        if (on) slide.setAttribute('aria-current', 'true');
        else slide.removeAttribute('aria-current');
      });
    }

    function goToIndex(next, smooth) {
      if (total <= 0) return;
      var reduce = prefersReducedMotion();
      index = ((next % total) + total) % total;
      updateActive(index);

      var left = slides[index].offsetLeft;
      if (typeof track.scrollTo === 'function') {
        track.scrollTo({
          left: left,
          behavior: smooth && !reduce ? 'smooth' : 'auto',
        });
      } else {
        track.scrollLeft = left;
      }
    }

    function step(delta) {
      goToIndex(index + delta, true);
    }

    ticks.forEach(function (tick) {
      tick.addEventListener('click', function () {
        var i = parseInt(tick.getAttribute('data-index'), 10);
        if (!isNaN(i)) goToIndex(i, true);
      });
    });

    if (btnPrev) {
      btnPrev.addEventListener('click', function () {
        step(-1);
      });
    }
    if (btnNext) {
      btnNext.addEventListener('click', function () {
        step(1);
      });
    }

    track.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
        e.preventDefault();
        step(1);
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        e.preventDefault();
        step(-1);
      } else if (e.key === 'Home') {
        e.preventDefault();
        goToIndex(0, true);
      } else if (e.key === 'End') {
        e.preventDefault();
        goToIndex(total - 1, true);
      }
    });

    window.addEventListener(
      'resize',
      function () {
        goToIndex(index, false);
      },
      { passive: true }
    );

    updateActive(0);
  }

  function boot() {
    document.querySelectorAll('[data-history-journey]').forEach(initHistoryJourney);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
