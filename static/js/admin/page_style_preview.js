(function () {
  function readColor(name) {
    var native = document.querySelector('[name="' + name + '"][data-cms-color-native], [name="' + name + '"]');
    if (!native) return '';
    var val = String(native.value || '').trim().toLowerCase();
    return /^#[0-9a-f]{6}$/.test(val) ? val : '';
  }

  function buildUrl(base, defaults) {
    var bg = readColor('background_color') || (defaults && defaults.bg) || '';
    var text = readColor('text_color') || (defaults && defaults.text) || '';
    var accent = readColor('accent_color') || (defaults && defaults.accent) || '';
    var params = new URLSearchParams();
    params.set('rs_style_preview', '1');
    if (bg) params.set('preview_bg', bg);
    if (text) params.set('preview_text', text);
    if (accent) params.set('preview_accent', accent);
    var sep = base.indexOf('?') >= 0 ? '&' : '?';
    return base + sep + params.toString();
  }

  document.addEventListener('DOMContentLoaded', function () {
    var btn = document.querySelector('[data-page-style-preview]');
    if (!btn) return;
    var base = btn.getAttribute('data-preview-base') || '/';
    var defaults = {
      bg: btn.getAttribute('data-default-bg') || '',
      text: btn.getAttribute('data-default-text') || '',
      accent: btn.getAttribute('data-default-accent') || '',
    };
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      window.open(buildUrl(base, defaults), '_blank', 'noopener');
    });
  });
})();
