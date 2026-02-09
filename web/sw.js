// Service Worker for Slow Shakespeare PWA
// Caches app files for offline use

const CACHE_NAME = 'slow-shakespeare-v1';
const ASSETS = [
  '/app.html',
  '/style.css',
  '/data.js',
  '/manifest.json',
  '/icon-192.png',
  '/icon-512.png'
];

// Install: cache core assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(ASSETS))
      .catch(err => console.error('SW install failed:', err))
  );
  self.skipWaiting();
});

// Activate: clean old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
      ))
      .catch(err => console.error('SW activate failed:', err))
  );
  self.clients.claim();
});

// Fetch: serve from cache, fall back to network
self.addEventListener('fetch', event => {
  // Skip non-GET and external requests
  if (event.request.method !== 'GET') return;
  if (!event.request.url.startsWith(self.location.origin)) return;

  event.respondWith(
    caches.match(event.request)
      .then(cached => {
        if (cached) return cached;
        return fetch(event.request).then(response => {
          // Don't cache non-ok responses
          if (!response || response.status !== 200) return response;
          // Clone and cache
          const clone = response.clone();
          caches.open(CACHE_NAME)
            .then(cache => cache.put(event.request, clone))
            .catch(err => console.error('SW cache put failed:', err));
          return response;
        });
      })
      .catch(err => {
        console.error('SW fetch failed:', err);
        // Return offline fallback if available
        return caches.match('/app.html');
      })
  );
});
