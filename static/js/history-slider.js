/* Royal Smoke — history journey: loop arrows + tick highlight + scroll sync */
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
    var ignoreScroll = false;
    var scrollTimer = null;

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

    function nearestIndex() {
      var best = 0;
      var bestDist = Infinity;
      var left = track.scrollLeft;
      slides.forEach(function (slide, i) {
        var d = Math.abs(slide.offsetLeft - left);
        if (d < bestDist) {
          bestDist = d;
          best = i;
        }
      });
      return best;
    }

    function goToIndex(next, smooth) {
      if (total <= 0) return;
      var reduce = prefersReducedMotion();
      index = ((next % total) + total) % total;
      updateActive(index);

      ignoreScroll = true;
      if (scrollTimer) window.clearTimeout(scrollTimer);

      var left = slides[index].offsetLeft;
      if (typeof track.scrollTo === 'function') {
        track.scrollTo({
          left: left,
          behavior: smooth && !reduce ? 'smooth' : 'auto',
        });
      } else {
        track.scrollLeft = left;
      }

      scrollTimer = window.setTimeout(function () {
        ignoreScroll = false;
        scrollTimer = null;
      }, smooth && !reduce ? 450 : 80);
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

    track.addEventListener('scroll', function () {
      if (ignoreScroll) return;
      var nearest = nearestIndex();
      if (nearest !== index) {
        index = nearest;
        updateActive(index);
      }
    }, { passive: true });

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
