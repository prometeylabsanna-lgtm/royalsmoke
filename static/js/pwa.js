/* PWA client: service worker + Web Push subscribe/bind */
(function () {
  'use strict';

  var PUSH_PROMPT_KEY = 'rs_pwa_push_prompt';

  function csrfToken() {
    var input = document.querySelector('input[name="csrfmiddlewaretoken"]');
    if (input && input.value) return input.value;
    var match = document.cookie.match(/(?:^|;\s*)rs_csrftoken=([^;]+)/);
    return match ? decodeURIComponent(match[1]) : '';
  }

  function pageLang() {
    return (document.documentElement.lang || 'uk').toLowerCase();
  }

  function urlBase64ToUint8Array(base64String) {
    var padding = '='.repeat((4 - (base64String.length % 4)) % 4);
    var base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
    var raw = window.atob(base64);
    var out = new Uint8Array(raw.length);
    for (var i = 0; i < raw.length; i += 1) out[i] = raw.charCodeAt(i);
    return out;
  }

  function postJson(url, body, method) {
    return fetch(url, {
      method: method || 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken(),
      },
      body: JSON.stringify(body || {}),
    });
  }

  function registerSW() {
    if (!('serviceWorker' in navigator)) return Promise.resolve(null);
    return navigator.serviceWorker.register('/sw.js', { scope: '/' });
  }

  function saveSubscription(sub) {
    if (!sub) return Promise.resolve();
    var json = sub.toJSON();
    return postJson('/pwa/push/subscribe/', {
      endpoint: json.endpoint,
      keys: json.keys,
      language: pageLang(),
    });
  }

  function ensureSubscription(registration, publicKey, forceAsk) {
    if (!registration || !('PushManager' in window) || !publicKey) {
      return Promise.resolve(null);
    }
    return registration.pushManager.getSubscription().then(function (existing) {
      if (existing) return existing;
      if (Notification.permission === 'denied') return null;
      if (Notification.permission !== 'granted' && !forceAsk) return null;
      var ask = Notification.permission === 'granted'
        ? Promise.resolve('granted')
        : Notification.requestPermission();
      return ask.then(function (perm) {
        if (perm !== 'granted') return null;
        return registration.pushManager.subscribe({
          userVisibleOnly: true,
          applicationServerKey: urlBase64ToUint8Array(publicKey),
        });
      });
    }).then(function (sub) {
      return saveSubscription(sub).then(function () { return sub; });
    });
  }

  function pushCopy(lang) {
    var map = {
      uk: {
        text: 'Увімкнути сповіщення про оплату та статус замовлення?',
        yes: 'Увімкнути',
        no: 'Не зараз',
      },
      en: {
        text: 'Enable notifications for payment and order status?',
        yes: 'Enable',
        no: 'Not now',
      },
      'zh-hans': {
        text: '是否开启付款与订单状态通知？',
        yes: '开启',
        no: '稍后',
      },
    };
    return map[lang] || map.uk;
  }

  function showPushPrompt(registration, publicKey) {
    if (!publicKey || Notification.permission !== 'default') return;
    try {
      if (localStorage.getItem(PUSH_PROMPT_KEY) === '1') return;
    } catch (e) { /* ignore */ }

    var copy = pushCopy(pageLang());
    var bar = document.createElement('div');
    bar.className = 'rs-pwa-push-bar';
    bar.setAttribute('role', 'dialog');
    bar.innerHTML =
      '<p class="rs-pwa-push-bar__text"></p>' +
      '<div class="rs-pwa-push-bar__actions">' +
      '<button type="button" class="rs-btn rs-btn--gold" data-pwa-push-yes></button>' +
      '<button type="button" class="rs-btn rs-btn--ghost" data-pwa-push-no></button>' +
      '</div>';
    bar.querySelector('.rs-pwa-push-bar__text').textContent = copy.text;
    bar.querySelector('[data-pwa-push-yes]').textContent = copy.yes;
    bar.querySelector('[data-pwa-push-no]').textContent = copy.no;
    document.body.appendChild(bar);

    function dismiss() {
      try { localStorage.setItem(PUSH_PROMPT_KEY, '1'); } catch (e) { /* ignore */ }
      if (bar.parentNode) bar.parentNode.removeChild(bar);
    }

    bar.querySelector('[data-pwa-push-no]').addEventListener('click', dismiss);
    bar.querySelector('[data-pwa-push-yes]').addEventListener('click', function () {
      ensureSubscription(registration, publicKey, true).finally(dismiss);
    });
  }

  function initPush(registration) {
    return fetch('/pwa/vapid-public-key/', { credentials: 'same-origin' })
      .then(function (r) { return r.json(); })
      .then(function (info) {
        if (!info || !info.enabled || !info.publicKey) return;
        return ensureSubscription(registration, info.publicKey, false).then(function () {
          showPushPrompt(registration, info.publicKey);
        });
      })
      .catch(function () {});
  }

  function bindCheckoutEmail() {
    var form = document.getElementById('rs-checkout-form');
    var emailInput = document.getElementById('id_email');
    if (!form || !emailInput || !('serviceWorker' in navigator)) return;

    function bind() {
      var email = (emailInput.value || '').trim();
      if (!email || email.indexOf('@') === -1) return;
      navigator.serviceWorker.ready.then(function (reg) {
        return reg.pushManager.getSubscription();
      }).then(function (sub) {
        if (!sub) return;
        return postJson('/pwa/push/bind/', {
          endpoint: sub.endpoint,
          email: email,
        });
      }).catch(function () {});
    }

    form.addEventListener('submit', bind);
    emailInput.addEventListener('change', bind);
  }

  function warmCatalogCache() {
    fetch('/pwa/offline-catalog.json', { credentials: 'same-origin' })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        if (!data || !data.langs || !('caches' in window)) return;
        var urls = {};
        Object.keys(data.langs).forEach(function (lang) {
          var pack = data.langs[lang] || {};
          (pack.products || []).forEach(function (p) {
            if (p.image) urls[p.image] = true;
          });
          (pack.categories || []).forEach(function (c) {
            if (c.image) urls[c.image] = true;
          });
          (pack.brands || []).forEach(function (b) {
            if (b.logo) urls[b.logo] = true;
          });
        });
        var list = Object.keys(urls).slice(0, 400);
        return caches.open('rs-pwa-static-v1').then(function (cache) {
          var i = 0;
          function next() {
            if (i >= list.length) return Promise.resolve();
            var batch = list.slice(i, i + 6);
            i += 6;
            return Promise.all(batch.map(function (u) {
              return cache.add(u).catch(function () {});
            })).then(next);
          }
          return next();
        });
      })
      .catch(function () {});
    fetch('/pwa/offline/', { credentials: 'same-origin' }).catch(function () {});
  }

  function boot() {
    registerSW()
      .then(function (reg) {
        if (!reg) return null;
        return navigator.serviceWorker.ready.then(initPush);
      })
      .catch(function () {});
    bindCheckoutEmail();
    warmCatalogCache();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
