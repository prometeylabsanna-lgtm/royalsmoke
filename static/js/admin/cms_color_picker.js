(function () {
  function sync(root) {
    var native = root.querySelector('[data-cms-color-native]');
    var hex = root.querySelector('[data-cms-color-hex]');
    var circle = root.querySelector('[data-cms-color-circle]');
    var resetBtn = root.querySelector('[data-cms-color-default]');
    var fallback = root.getAttribute('data-default-color') || '#100d0c';
    if (!native || !hex || !circle) return;

    function normalize(val) {
      var v = String(val || '').trim();
      if (!v) return '';
      if (v.charAt(0) !== '#') v = '#' + v;
      if (/^#[0-9a-fA-F]{3}$/.test(v)) {
        v = '#' + v[1] + v[1] + v[2] + v[2] + v[3] + v[3];
      }
      if (!/^#[0-9a-fA-F]{6}$/.test(v)) return '';
      return v.toLowerCase();
    }

    function paint(val) {
      var n = normalize(val) || normalize(fallback) || native.value;
      circle.style.background = n;
      hex.value = n;
      native.value = n;
    }

    native.addEventListener('input', function () {
      paint(native.value);
    });
    hex.addEventListener('change', function () {
      var n = normalize(hex.value);
      paint(n || native.value);
    });
    if (resetBtn) {
      resetBtn.addEventListener('click', function (e) {
        e.preventDefault();
        paint(fallback);
      });
    }
    paint(native.value || fallback);
  }

  function init(scope) {
    (scope || document).querySelectorAll('[data-cms-colorpick]').forEach(sync);
  }

  document.addEventListener('DOMContentLoaded', function () {
    init(document);
  });
})();
