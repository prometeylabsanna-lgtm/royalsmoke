/* Royal Smoke — hero slider with next-thumb expand animation */
(function () {
  'use strict';

  var DURATION = 980;
  var FADE_MS = 360;
  var HANDOFF_MS = 280;
  var AUTO_MS = 4000;
  var EASE = 'cubic-bezier(0.22, 1, 0.36, 1)';
  var SWIPE_THRESHOLD = 40;

  function initHeroSlider(root) {
    if (!root) return;

    var stage = root.querySelector('[data-hero-stage]');
    var slides = Array.prototype.slice.call(root.querySelectorAll('[data-hero-slide]'));
    var dots = Array.prototype.slice.call(root.querySelectorAll('[data-hero-dot]'));
    var counter = root.querySelector('[data-hero-counter]');
    var nextBtn = root.querySelector('[data-hero-next]');
    var thumb = root.querySelector('[data-hero-thumb]');
    var ctaPrimary = root.querySelector('[data-hero-cta-primary]');
    var ctaSecondary = root.querySelector('[data-hero-cta-secondary]');
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var total = slides.length;
    if (!total) return;

    var index = 0;
    var busy = false;
    var touchX = 0;
    var expandEl = null;
    var expandImg = null;
    var expandVeil = null;
    var autoTimer = null;
    var autoPaused = false;
    var isIOS = /iP(hone|od|ad)/.test(navigator.userAgent);
    var parallaxFactor = reduce ? 0 : (isIOS ? 0.07 : 0.16);

    function pad(n) {
      return (n < 10 ? '0' : '') + n;
    }

    function nextIndex(i) {
      return (i + 1) % total;
    }

    function stopAuto() {
      if (autoTimer) {
        window.clearTimeout(autoTimer);
        autoTimer = null;
      }
    }

    function startAuto() {
      stopAuto();
      if (reduce || autoPaused || document.hidden || total < 2) return;
      autoTimer = window.setTimeout(function () {
        autoTimer = null;
        if (busy || autoPaused || document.hidden) return;
        expandThenAdvance();
      }, AUTO_MS);
    }

    function slideImage(i) {
      var img = slides[i].querySelector('img');
      if (img) return img.getAttribute('src');
      return null;
    }

    function slideImgEl(i) {
      return slides[i].querySelector('img');
    }

    function currentParallaxY() {
      var y = window.scrollY || 0;
      var heroBottom = root.offsetTop + root.offsetHeight;
      if (y >= heroBottom) return 0;
      return y * parallaxFactor;
    }

    function parallaxLayers() {
      return Array.prototype.slice.call(root.querySelectorAll('[data-hero-parallax]'));
    }

    function clearParallax() {
      parallaxLayers().forEach(function (el) {
        el.style.transform = 'none';
      });
      if (expandImg) expandImg.style.transform = 'none';
    }

    function applyParallax() {
      if (reduce || busy) return;
      var shift = currentParallaxY();
      var value = shift ? 'translate3d(0,' + shift.toFixed(2) + 'px,0)' : 'none';
      parallaxLayers().forEach(function (el) {
        el.style.transform = value;
      });
    }

    function updateThumb() {
      if (!thumb) return;
      var ni = nextIndex(index);
      var src = slideImage(ni);
      var existing = thumb.querySelector('img');
      var ph = thumb.querySelector('.rs-hero__placeholder');
      if (!src) return;
      if (existing) {
        if (existing.getAttribute('src') !== src) existing.setAttribute('src', src);
        existing.alt = 'Наступний кадр';
      } else if (ph) {
        var img = document.createElement('img');
        img.src = src;
        img.alt = 'Наступний кадр';
        ph.replaceWith(img);
      }
    }

    function syncCta(i) {
      var slide = slides[i];
      if (!slide) return;
      var pUrl = slide.getAttribute('data-cta-primary-url');
      var pLabel = slide.getAttribute('data-cta-primary-label');
      var sUrl = slide.getAttribute('data-cta-secondary-url');
      var sLabel = slide.getAttribute('data-cta-secondary-label');

      if (ctaPrimary) {
        if (pUrl && ctaPrimary.getAttribute('href') !== pUrl) {
          ctaPrimary.setAttribute('href', pUrl);
        }
        if (pLabel && ctaPrimary.textContent !== pLabel) {
          ctaPrimary.textContent = pLabel;
        }
      }
      if (ctaSecondary) {
        if (sUrl && ctaSecondary.getAttribute('href') !== sUrl) {
          ctaSecondary.setAttribute('href', sUrl);
        }
        if (sLabel && ctaSecondary.textContent !== sLabel) {
          ctaSecondary.textContent = sLabel;
        }
      }
    }

    function setActive(i, skipThumb) {
      index = i;
      slides.forEach(function (s, n) {
        var on = n === index;
        s.classList.toggle('is-active', on);
        s.setAttribute('aria-hidden', on ? 'false' : 'true');
      });
      dots.forEach(function (d, n) {
        var on = n === index;
        d.classList.toggle('is-active', on);
        d.setAttribute('aria-current', on ? 'true' : 'false');
      });
      if (counter) {
        counter.textContent = pad(index + 1) + ' / ' + pad(total);
      }
      syncCta(index);
      if (!skipThumb) updateThumb();
    }

    function ensureExpandLayer() {
      if (expandEl) return;
      expandEl = document.createElement('div');
      expandEl.className = 'rs-hero__expand';
      expandEl.setAttribute('data-hero-expand', '');
      expandEl.setAttribute('aria-hidden', 'true');

      expandImg = document.createElement('img');
      expandImg.className = 'rs-hero__expand-img';
      expandImg.alt = '';
      expandImg.decoding = 'async';

      expandVeil = document.createElement('div');
      expandVeil.className = 'rs-hero__expand-veil';

      expandEl.appendChild(expandImg);
      expandEl.appendChild(expandVeil);
      root.appendChild(expandEl);
    }

    function hideExpandLayer() {
      if (!expandEl) return;
      expandEl.classList.remove('is-on');
      expandEl.style.cssText = '';
      if (expandImg) expandImg.style.cssText = '';
      if (expandVeil) expandVeil.style.cssText = '';
    }

    function setThumbRestHidden(hidden) {
      if (!thumb) return;
      if (hidden) {
        thumb.style.visibility = 'hidden';
        thumb.style.pointerEvents = 'none';
      } else {
        thumb.style.visibility = '';
        thumb.style.pointerEvents = '';
      }
    }

    function showThumbForIndex(i) {
      if (!thumb) return;
      var src = slideImage(i);
      var existing = thumb.querySelector('img');
      if (!src || !existing) return;
      if (existing.getAttribute('src') !== src) existing.setAttribute('src', src);
      existing.alt = 'Наступний кадр';
    }

    function resetThumbMotion() {
      if (!thumb) return;
      thumb.style.transition = '';
      thumb.style.transform = '';
      thumb.style.opacity = '';
      thumb.style.visibility = '';
      thumb.style.pointerEvents = '';
    }

    /* New preview rides in from beyond the right edge of the viewport */
    function enterThumbFromRight(previewIndex) {
      if (!thumb) return;
      showThumbForIndex(previewIndex);
      thumb.style.transition = 'none';
      thumb.style.visibility = 'visible';
      thumb.style.opacity = '1';
      thumb.style.pointerEvents = 'none';
      thumb.style.transform = 'translate3d(0, 0, 0)';
      void thumb.offsetWidth;

      var rect = thumb.getBoundingClientRect();
      var dx = Math.max(
        Math.ceil(window.innerWidth - rect.left + 40),
        Math.ceil(rect.width + 80)
      );
      thumb.style.transform = 'translate3d(' + dx + 'px, 0, 0)';
      void thumb.offsetWidth;

      thumb.style.transition =
        'transform ' + DURATION + 'ms ' + EASE;
      thumb.style.transform = 'translate3d(0, 0, 0)';
    }

    function crossfadeTo(target) {
      if (busy) return;
      target = ((target % total) + total) % total;
      if (target === index) return;
      busy = true;
      stopAuto();

      slides.forEach(function (s) {
        s.style.transition = '';
      });
      setActive(target, false);

      window.setTimeout(function () {
        busy = false;
        startAuto();
      }, reduce ? 0 : 520);
    }

    function expandThenAdvance() {
      if (busy || !stage) return;
      var next = nextIndex(index);
      busy = true;
      stopAuto();

      if (reduce || !thumb) {
        setActive(next, false);
        busy = false;
        startAuto();
        return;
      }

      var src = slideImage(next);
      if (!src) {
        setActive(next, false);
        busy = false;
        startAuto();
        return;
      }

      ensureExpandLayer();

      var stageRect = stage.getBoundingClientRect();
      var thumbRect = thumb.getBoundingClientRect();
      var radius = window.getComputedStyle(thumb).borderRadius || '50%';
      if (!radius || radius === '0px') radius = '50%';
      var nextSlideImg = slideImgEl(next);
      var nextPos = nextSlideImg
        ? window.getComputedStyle(nextSlideImg).objectPosition
        : 'center 58%';

      /* Integer start — avoids subpixel drift into the full frame */
      var x0 = Math.round(thumbRect.left - stageRect.left);
      var y0 = Math.round(thumbRect.top - stageRect.top);
      var w0 = Math.round(thumbRect.width);
      var h0 = Math.round(thumbRect.height);

      /* Freeze parallax for the whole expand → handoff window */
      clearParallax();

      /* Clone of the thumb — crop already matches the destination slide */
      expandImg.src = src;
      expandImg.style.cssText = '';
      expandImg.style.transition = 'none';
      expandImg.style.opacity = '1';
      expandImg.style.inset = '0';
      expandImg.style.width = '100%';
      expandImg.style.height = '100%';
      expandImg.style.objectFit = 'cover';
      expandImg.style.objectPosition = nextPos;
      expandImg.style.transform = 'none';
      expandImg.style.margin = '0';

      expandVeil.style.transition = 'none';
      expandVeil.style.opacity = '1';
      expandVeil.style.display = 'block';

      expandEl.style.transition = 'none';
      expandEl.style.opacity = '1';
      expandEl.style.left = x0 + 'px';
      expandEl.style.top = y0 + 'px';
      expandEl.style.right = 'auto';
      expandEl.style.bottom = 'auto';
      expandEl.style.width = w0 + 'px';
      expandEl.style.height = h0 + 'px';
      expandEl.style.borderRadius = radius;
      expandEl.classList.add('is-on');

      /* Hide the resting thumb — expand is now that thumb growing */
      thumb.style.transition = 'none';
      thumb.style.visibility = 'hidden';
      thumb.style.pointerEvents = 'none';

      void expandEl.offsetWidth;

      expandEl.style.transition =
        'left ' + DURATION + 'ms ' + EASE + ',' +
        'top ' + DURATION + 'ms ' + EASE + ',' +
        'width ' + DURATION + 'ms ' + EASE + ',' +
        'height ' + DURATION + 'ms ' + EASE + ',' +
        'border-radius ' + DURATION + 'ms ' + EASE;

      /* End on CSS box of the stage — not fractional getBoundingClientRect px */
      expandEl.style.left = '0';
      expandEl.style.top = '0';
      expandEl.style.width = '100%';
      expandEl.style.height = '100%';
      expandEl.style.borderRadius = '0';

      /* Next preview rides in from the right while the circle expands */
      window.setTimeout(function () {
        enterThumbFromRight(nextIndex(next));
      }, 90);

      window.setTimeout(function () {
        slides.forEach(function (s) {
          s.style.transition = 'none';
        });

        /* Pixel-lock expand to stage before revealing the real slide */
        expandEl.style.transition = 'none';
        expandEl.style.left = '0';
        expandEl.style.top = '0';
        expandEl.style.right = '0';
        expandEl.style.bottom = '0';
        expandEl.style.width = 'auto';
        expandEl.style.height = 'auto';
        expandEl.style.borderRadius = '0';

        expandImg.style.transition = 'none';
        expandImg.style.objectPosition = nextPos;
        expandImg.style.transform = 'none';

        if (nextSlideImg) {
          nextSlideImg.style.transition = 'none';
          nextSlideImg.style.transform = 'none';
          nextSlideImg.style.objectPosition = nextPos;
        }

        setActive(next, true);
        void stage.offsetWidth;

        window.requestAnimationFrame(function () {
          window.requestAnimationFrame(function () {
            expandEl.style.transition = 'opacity ' + HANDOFF_MS + 'ms linear';
            expandEl.style.opacity = '0';

            window.setTimeout(function () {
              hideExpandLayer();

              slides.forEach(function (s) {
                s.style.transition = '';
              });
              if (nextSlideImg) {
                nextSlideImg.style.transition = '';
                nextSlideImg.style.objectPosition = '';
              }

              showThumbForIndex(nextIndex(index));
              resetThumbMotion();
              busy = false;
              applyParallax();
              startAuto();
            }, HANDOFF_MS);
          });
        });
      }, DURATION);
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', function (e) {
        e.preventDefault();
        expandThenAdvance();
      });
    }

    if (thumb) {
      thumb.addEventListener('click', function (e) {
        e.preventDefault();
        expandThenAdvance();
      });
    }

    dots.forEach(function (dot, i) {
      dot.addEventListener('click', function () {
        crossfadeTo(i);
      });
    });

    root.addEventListener('touchstart', function (e) {
      touchX = e.changedTouches[0].screenX;
    }, { passive: true });

    root.addEventListener('touchend', function (e) {
      var dx = e.changedTouches[0].screenX - touchX;
      if (Math.abs(dx) < SWIPE_THRESHOLD) return;
      if (dx < 0) expandThenAdvance();
      else crossfadeTo(index - 1);
    }, { passive: true });

    if (!reduce && stage) {
      var ticking = false;
      function onScroll() {
        if (ticking || busy) return;
        ticking = true;
        window.requestAnimationFrame(function () {
          applyParallax();
          ticking = false;
        });
      }
      window.addEventListener('scroll', onScroll, { passive: true });
    }

    document.addEventListener('visibilitychange', function () {
      if (document.hidden) {
        stopAuto();
      } else if (!autoPaused) {
        startAuto();
      }
    });

    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        var entry = entries[0];
        if (!entry) return;
        if (entry.isIntersecting && entry.intersectionRatio > 0.35) {
          autoPaused = false;
          if (!document.hidden) startAuto();
        } else {
          autoPaused = true;
          stopAuto();
        }
      }, { threshold: [0, 0.35, 0.6] });
      io.observe(root);
    }

    setActive(0, false);
    startAuto();
  }

  document.addEventListener('DOMContentLoaded', function () {
    var heroes = document.querySelectorAll('[data-hero]');
    Array.prototype.forEach.call(heroes, initHeroSlider);
  });
})();
