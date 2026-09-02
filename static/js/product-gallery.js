/* Royal Smoke — product gallery + quantity stepper */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function clamp(n, min, max) {
    return Math.max(min, Math.min(max, n));
  }

  function initGallery(root) {
    var gallery = root.querySelector('[data-pd-gallery]');
    if (!gallery) return;

    var slides = Array.prototype.slice.call(gallery.querySelectorAll('[data-pd-slide]'));
    var thumbs = Array.prototype.slice.call(gallery.querySelectorAll('[data-pd-thumb]'));
    var prevBtn = gallery.querySelector('[data-pd-prev]');
    var nextBtn = gallery.querySelector('[data-pd-next]');
    var index = 0;
    var total = slides.length;

    if (!total) return;

    function goTo(next) {
      var target = ((next % total) + total) % total;
      if (target === index && slides[index].classList.contains('is-active')) return;
      index = target;

      slides.forEach(function (slide, i) {
        var on = i === index;
        slide.classList.toggle('is-active', on);
        slide.setAttribute('aria-hidden', on ? 'false' : 'true');
      });

      thumbs.forEach(function (thumb, i) {
        var on = i === index;
        thumb.classList.toggle('is-active', on);
        thumb.setAttribute('aria-selected', on ? 'true' : 'false');
      });
    }

    if (prevBtn) {
      prevBtn.addEventListener('click', function () {
        goTo(index - 1);
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', function () {
        goTo(index + 1);
      });
    }

    thumbs.forEach(function (thumb) {
      thumb.addEventListener('click', function () {
        var i = parseInt(thumb.getAttribute('data-index'), 10);
        if (!isNaN(i)) goTo(i);
      });
    });

    var startX = 0;
    var deltaX = 0;
    var stage = gallery.querySelector('.rs-pd__stage');

    if (stage && 'ontouchstart' in window) {
      stage.addEventListener('touchstart', function (e) {
        if (!e.touches || !e.touches.length) return;
        startX = e.touches[0].clientX;
        deltaX = 0;
      }, { passive: true });

      stage.addEventListener('touchmove', function (e) {
        if (!e.touches || !e.touches.length) return;
        deltaX = e.touches[0].clientX - startX;
      }, { passive: true });

      stage.addEventListener('touchend', function () {
        if (Math.abs(deltaX) < 40) return;
        if (deltaX > 0) goTo(index - 1);
        else goTo(index + 1);
        deltaX = 0;
      });
    }

    goTo(0);
  }

  function initQty(root) {
    var wrap = root.querySelector('[data-pd-qty]');
    if (!wrap) return;

    var input = wrap.querySelector('.rs-pd__qty-input');
    var minus = wrap.querySelector('[data-pd-qty-minus]');
    var plus = wrap.querySelector('[data-pd-qty-plus]');
    if (!input) return;

    var min = parseInt(input.getAttribute('min'), 10) || 1;
    var max = parseInt(input.getAttribute('max'), 10) || 99;

    function setVal(v) {
      input.value = String(clamp(v, min, max));
    }

    if (minus) {
      minus.addEventListener('click', function () {
        setVal((parseInt(input.value, 10) || min) - 1);
      });
    }

    if (plus) {
      plus.addEventListener('click', function () {
        setVal((parseInt(input.value, 10) || min) + 1);
      });
    }

    input.addEventListener('change', function () {
      setVal(parseInt(input.value, 10) || min);
    });
  }

  function boot() {
    var root = document.querySelector('[data-pd]');
    if (!root) return;
    initGallery(root);
    initQty(root);
    if (reduceMotion) {
      root.classList.add('is-reduced-motion');
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
