const CACHE_NAME = 'findmyroomie-cache-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/login/',
  '/static/css/style.css',
  '/static/manifest.json',
  '/static/images/room1.png',
  '/static/images/room2.png',
  '/static/images/room3.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});
