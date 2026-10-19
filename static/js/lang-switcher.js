/* Випадний перемикач мов: закриття по кліку/тапу поза меню, Escape і при відкритті іншого. */
(function () {
  'use strict';

  var SELECTOR = '[data-lang-menu]';

  function openMenus() {
    return Array.prototype.slice.call(document.querySelectorAll(SELECTOR + '[open]'));
  }

  function closeAll(except) {
    openMenus().forEach(function (menu) {
      if (menu !== except) menu.removeAttribute('open');
    });
  }

  // pointerdown, а не click: iOS Safari не шле click по неінтерактивних елементах.
  document.addEventListener('pointerdown', function (event) {
    var target = event.target;
    var inside = target && target.closest ? target.closest(SELECTOR) : null;
    closeAll(inside);
  });

  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Escape') return;
    var menus = openMenus();
    if (!menus.length) return;
    var summary = menus[0].querySelector('summary');
    closeAll(null);
    if (summary) summary.focus();
  });

  document.addEventListener('toggle', function (event) {
    var menu = event.target;
    if (menu && menu.matches && menu.matches(SELECTOR) && menu.open) closeAll(menu);
  }, true);
})();
