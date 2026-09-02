(function () {
  'use strict';

  var FIELDS = ['strength', 'format', 'country', 'budget'];
  var TOTAL = FIELDS.length;

  function initCalc(root) {
    if (!root || root.dataset.calcReady === '1') return;
    root.dataset.calcReady = '1';

    var form = root.querySelector('#home-calc-form');
    if (!form) return;

    var panels = Array.prototype.slice.call(root.querySelectorAll('[data-calc-panel]'));
    var progressItems = Array.prototype.slice.call(root.querySelectorAll('[data-calc-progress]'));
    var nextBtn = root.querySelector('[data-calc-next]');
    var prevBtn = root.querySelector('[data-calc-prev]');
    var submitBtn = root.querySelector('[data-calc-submit]');
    var step = 0;

    function selectedLabel(name) {
      var input = form.querySelector('input[name="' + name + '"]:checked');
      if (!input) return '';
      var chip = input.closest('.rs-home-calc__chip');
      var span = chip && chip.querySelector('span');
      return span ? span.textContent.trim() : '';
    }

    function syncChipState() {
      form.querySelectorAll('.rs-home-calc__chip').forEach(function (chip) {
        var input = chip.querySelector('input');
        chip.classList.toggle('is-active', !!(input && input.checked));
      });
    }

    function updatePicks() {
      FIELDS.forEach(function (name, idx) {
        var el = root.querySelector('[data-calc-pick="' + name + '"]');
        if (!el) return;
        var label = idx <= step ? selectedLabel(name) : '';
        el.textContent = label || '—';
        el.classList.toggle('is-empty', !label);
      });
      syncChipState();
    }

    function setStep(next, opts) {
      var options = opts || {};
      step = Math.max(0, Math.min(TOTAL - 1, next));
      root.dataset.calcStep = String(step);

      panels.forEach(function (panel) {
        var idx = Number(panel.getAttribute('data-calc-panel'));
        var active = idx === step;
        panel.classList.toggle('is-active', active);
        if (active) {
          panel.removeAttribute('hidden');
        } else {
          panel.setAttribute('hidden', '');
        }
      });

      progressItems.forEach(function (item) {
        var idx = Number(item.getAttribute('data-calc-progress'));
        item.classList.toggle('is-active', idx === step);
        item.classList.toggle('is-done', idx < step);
      });

      if (prevBtn) prevBtn.hidden = step === 0;
      if (nextBtn) nextBtn.hidden = step === TOTAL - 1;
      if (submitBtn) submitBtn.hidden = step !== TOTAL - 1;

      updatePicks();

      if (options.focus === false) return;

      var activePanel = panels[step];
      if (activePanel) {
        var focusTarget = activePanel.querySelector('.rs-home-calc__question') || activePanel;
        if (focusTarget && typeof focusTarget.focus === 'function') {
          focusTarget.setAttribute('tabindex', '-1');
          focusTarget.focus({ preventScroll: true });
        }
      }
    }

    function canGoTo(target) {
      if (target <= step) return true;
      for (var i = 0; i < target; i += 1) {
        if (!selectedLabel(FIELDS[i])) return false;
      }
      return true;
    }

    form.addEventListener('change', function (e) {
      if (e.target && e.target.matches('[data-calc-chip]')) {
        updatePicks();
      }
    });

    if (nextBtn) {
      nextBtn.addEventListener('click', function () {
        if (!selectedLabel(FIELDS[step])) return;
        setStep(step + 1);
      });
    }

    if (prevBtn) {
      prevBtn.addEventListener('click', function () {
        setStep(step - 1);
      });
    }

    root.querySelectorAll('[data-calc-goto]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var target = Number(btn.getAttribute('data-calc-goto'));
        if (Number.isNaN(target) || !canGoTo(target)) return;
        setStep(target);
      });
    });

    form.addEventListener('keydown', function (e) {
      if (e.key !== 'Enter') return;
      if (e.target && e.target.matches('input[type="radio"]')) {
        e.preventDefault();
        if (step < TOTAL - 1) {
          if (nextBtn) nextBtn.click();
        } else if (submitBtn) {
          submitBtn.click();
        }
      }
    });

    setStep(0, { focus: false });
  }

  function boot() {
    document.querySelectorAll('[data-home-calc]').forEach(initCalc);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
