/* Royal Smoke service worker — catalog offline + push */
/* eslint-disable no-restricted-globals */
const RS_SHELL = 'rs-pwa-shell-v1';
const RS_DATA = 'rs-pwa-data-v1';
const RS_PAGES = 'rs-pwa-pages-v1';
const RS_STATIC = 'rs-pwa-static-v1';
const ADMIN_PREFIX = '/{{ admin_url }}';

const SHELL_URLS = [
  '/pwa/offline/',
  '/pwa/offline-catalog.json',
  '/static/css/tokens.css',
  '/static/css/pwa-offline.css',
  '/static/js/pwa-offline-catalog.js',
  '/static/img/pwa-192.png',
  '/static/img/pwa-512.png',
];

const NETWORK_ONLY_PREFIXES = [
  '/api/',
  '/orders/',
  '/cart/',
  '/accounts/',
  ADMIN_PREFIX,
  '/i18n/',
  '/pwa/push/',
  '/pwa/vapid-public-key/',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(RS_SHELL).then((cache) => cache.addAll(SHELL_URLS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  const keep = new Set([RS_SHELL, RS_DATA, RS_PAGES, RS_STATIC]);
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => !keep.has(k)).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

function isCatalogPath(pathname) {
  return (
    pathname === '/catalog' ||
    pathname === '/catalog/' ||
    pathname.indexOf('/catalog/') !== -1 ||
    /\/(en|zh-hans)\/catalog(\/|$)/.test(pathname)
  );
}

function shouldNetworkOnly(url) {
  if (url.pathname === '/sw.js' || url.pathname === '/manifest.webmanifest') return true;
  return NETWORK_ONLY_PREFIXES.some((p) => url.pathname.indexOf(p) === 0);
}

function staleBannerHtml(lang) {
  const messages = {
    uk: 'Офлайн-копія каталогу. Ціни та наявність можуть бути застарілими.',
    en: 'Offline catalog copy. Prices and stock may be outdated.',
    'zh-hans': '离线目录副本。价格与库存可能已过期。',
  };
  const text = messages[lang] || messages.uk;
  return (
    '<div class="rs-pwa-stale" role="status" data-rs-pwa-stale>' +
    '<span>' + text + '</span></div>'
  );
}

function detectLang(pathname) {
  if (pathname.indexOf('/en/') === 0 || pathname === '/en') return 'en';
  if (pathname.indexOf('/zh-hans/') === 0 || pathname === '/zh-hans') return 'zh-hans';
  return 'uk';
}

async function injectStale(response, lang) {
  const ctype = response.headers.get('content-type') || '';
  if (ctype.indexOf('text/html') === -1) return response;
  const text = await response.text();
  const banner = staleBannerHtml(lang);
  let html = text;
  if (html.indexOf('data-rs-pwa-stale') === -1) {
    html = html.replace(/<body([^>]*)>/i, '<body$1>' + banner);
  }
  const headers = new Headers(response.headers);
  headers.set('Content-Type', 'text/html; charset=utf-8');
  return new Response(html, { status: response.status, statusText: response.statusText, headers });
}

async function networkFirstPage(request, lang) {
  const cache = await caches.open(RS_PAGES);
  try {
    const fresh = await fetch(request);
    if (fresh && fresh.ok) {
      cache.put(request, fresh.clone());
    }
    return fresh;
  } catch (err) {
    const cached = await cache.match(request);
    if (cached) return injectStale(cached, lang);
    if (isCatalogPath(new URL(request.url).pathname)) {
      const offline = await caches.match('/pwa/offline/');
      if (offline) return injectStale(offline, lang);
    }
    throw err;
  }
}

async function cacheFirstStatic(request) {
  const cached = await caches.match(request);
  if (cached) return cached;
  const fresh = await fetch(request);
  if (fresh && fresh.ok) {
    const cache = await caches.open(RS_STATIC);
    cache.put(request, fresh.clone());
  }
  return fresh;
}

async function networkFirstData(request) {
  const cache = await caches.open(RS_DATA);
  try {
    const fresh = await fetch(request);
    if (fresh && fresh.ok) cache.put(request, fresh.clone());
    return fresh;
  } catch (err) {
    const cached = await cache.match(request);
    if (cached) return cached;
    throw err;
  }
}

self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (request.method !== 'GET') return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;
  if (shouldNetworkOnly(url)) return;

  if (url.pathname === '/pwa/offline-catalog.json') {
    event.respondWith(networkFirstData(request));
    return;
  }

  if (url.pathname.indexOf('/static/') === 0 || url.pathname.indexOf('/media/') === 0) {
    event.respondWith(cacheFirstStatic(request));
    return;
  }

  if (request.mode === 'navigate' || (request.headers.get('accept') || '').indexOf('text/html') !== -1) {
    const lang = detectLang(url.pathname);
    event.respondWith(networkFirstPage(request, lang));
  }
});

self.addEventListener('push', (event) => {
  let data = {};
  try {
    data = event.data ? event.data.json() : {};
  } catch (e) {
    data = { body: event.data ? event.data.text() : '' };
  }
  const title = data.title || 'Royal Smoke';
  const options = {
    body: data.body || '',
    icon: data.icon || '/static/img/pwa-192.png',
    badge: data.badge || '/static/img/pwa-192.png',
    tag: data.tag || 'rs-push',
    data: { url: data.url || '/' },
    renotify: true,
  };
  event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  const target = (event.notification.data && event.notification.data.url) || '/';
  event.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then((clients) => {
      for (let i = 0; i < clients.length; i += 1) {
        const client = clients[i];
        if ('focus' in client) {
          client.navigate(target);
          return client.focus();
        }
      }
      if (self.clients.openWindow) return self.clients.openWindow(target);
      return undefined;
    })
  );
});
