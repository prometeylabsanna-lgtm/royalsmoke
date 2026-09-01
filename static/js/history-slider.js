/* Royal Smoke — history journey: arrows + horizontal scroll + tick sync */
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
    var scrollingProgrammatic = false;
    var scrollEndTimer = null;
    var drag = { active: false, startX: 0, startLeft: 0, moved: false };

    function updateNav() {
      if (btnPrev) {
        btnPrev.disabled = index <= 0;
        btnPrev.setAttribute('aria-disabled', index <= 0 ? 'true' : 'false');
      }
      if (btnNext) {
        btnNext.disabled = index >= total - 1;
        btnNext.setAttribute('aria-disabled', index >= total - 1 ? 'true' : 'false');
      }
    }

    function updateTicks(activeIndex) {
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
      updateNav();
    }

    function nearestIndex() {
      var left = track.scrollLeft;
      var best = 0;
      var bestDist = Infinity;
      slides.forEach(function (slide, i) {
        var dist = Math.abs(slide.offsetLeft - left);
        if (dist < bestDist) {
          bestDist = dist;
          best = i;
        }
      });
      return best;
    }

    function scrollToIndex(next, smooth) {
      if (next < 0 || next >= total) return;
      var reduce = prefersReducedMotion();
      index = next;
      updateTicks(index);

      scrollingProgrammatic = true;
      var left = slides[next].offsetLeft;
      if (track.scrollWidth > track.clientWidth + 2) {
        if (smooth && !reduce && typeof track.scrollTo === 'function') {
          track.scrollTo({ left: left, behavior: 'smooth' });
        } else {
          track.scrollLeft = left;
        }
      }
      window.clearTimeout(scrollEndTimer);
      scrollEndTimer = window.setTimeout(function () {
        scrollingProgrammatic = false;
      }, reduce ? 50 : 420);
    }

    function onScroll() {
      if (scrollingProgrammatic || drag.active) return;
      var next = nearestIndex();
      if (next === index) return;
      index = next;
      updateTicks(index);
    }

    var scrollRaf = 0;
    track.addEventListener(
      'scroll',
      function () {
        if (scrollRaf) return;
        scrollRaf = window.requestAnimationFrame(function () {
          scrollRaf = 0;
          onScroll();
        });
      },
      { passive: true }
    );

    ticks.forEach(function (tick) {
      tick.addEventListener('click', function () {
        var i = parseInt(tick.getAttribute('data-index'), 10);
        if (!isNaN(i)) scrollToIndex(i, true);
      });
    });

    if (btnPrev) {
      btnPrev.addEventListener('click', function () {
        scrollToIndex(Math.max(0, index - 1), true);
      });
    }
    if (btnNext) {
      btnNext.addEventListener('click', function () {
        scrollToIndex(Math.min(total - 1, index + 1), true);
      });
    }

    track.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
        e.preventDefault();
        scrollToIndex(Math.min(total - 1, index + 1), true);
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        e.preventDefault();
        scrollToIndex(Math.max(0, index - 1), true);
      } else if (e.key === 'Home') {
        e.preventDefault();
        scrollToIndex(0, true);
      } else if (e.key === 'End') {
        e.preventDefault();
        scrollToIndex(total - 1, true);
      }
    });

    var wheelLockUntil = 0;

    track.addEventListener(
      'wheel',
      function (e) {
        var absX = Math.abs(e.deltaX);
        var absY = Math.abs(e.deltaY);
        var overflows = track.scrollWidth > track.clientWidth + 2;

        if (absX > absY) {
          if (!overflows) return;
          return;
        }

        if (overflows) {
          e.preventDefault();
          track.scrollLeft += e.deltaY;
          return;
        }

        var now = Date.now();
        if (now < wheelLockUntil) {
          e.preventDefault();
          return;
        }
        if (Math.abs(e.deltaY) < 12) return;
        e.preventDefault();
        wheelLockUntil = now + 380;
        if (e.deltaY > 0) scrollToIndex(Math.min(total - 1, index + 1), true);
        else scrollToIndex(Math.max(0, index - 1), true);
      },
      { passive: false }
    );

    track.addEventListener('pointerdown', function (e) {
      if (e.pointerType === 'touch') return;
      if (e.button !== 0) return;
      drag.active = true;
      drag.moved = false;
      drag.startX = e.clientX;
      drag.startLeft = track.scrollLeft;
      track.classList.add('is-dragging');
      try {
        track.setPointerCapture(e.pointerId);
      } catch (err) {}
    });

    track.addEventListener('pointermove', function (e) {
      if (!drag.active) return;
      var dx = e.clientX - drag.startX;
      if (Math.abs(dx) > 4) drag.moved = true;
      track.scrollLeft = drag.startLeft - dx;
    });

    function endDrag(e) {
      if (!drag.active) return;
      drag.active = false;
      track.classList.remove('is-dragging');
      try {
        track.releasePointerCapture(e.pointerId);
      } catch (err) {}
      var next = nearestIndex();
      if (next !== index) {
        index = next;
        updateTicks(index);
      }
      if (drag.moved) {
        scrollToIndex(next, true);
      }
    }

    track.addEventListener('pointerup', endDrag);
    track.addEventListener('pointercancel', endDrag);

    window.addEventListener(
      'resize',
      function () {
        scrollToIndex(index, false);
      },
      { passive: true }
    );

    updateTicks(0);
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
