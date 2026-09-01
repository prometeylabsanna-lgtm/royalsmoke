(function () {
  'use strict';

  function initCalc(root) {
    if (!root || root.dataset.calcReady === '1') return;
    root.dataset.calcReady = '1';

    var form = root.querySelector('#home-calc-form');
    var summary = root.querySelector('[data-calc-summary]');
    if (!form || !summary) return;

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

    function updateSummary() {
      var parts = [
        selectedLabel('strength'),
        selectedLabel('format'),
        selectedLabel('country'),
        selectedLabel('budget'),
      ].filter(Boolean);
      summary.textContent = parts.join(' · ');
      syncChipState();
    }

    form.addEventListener('change', function (e) {
      if (e.target && e.target.matches('[data-calc-chip]')) {
        updateSummary();
      }
    });

    updateSummary();
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
