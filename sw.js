const CACHE_NAME = 'aatualatalo-cache-v2';

self.addEventListener('install', event => {
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.filter(name => name !== CACHE_NAME).map(name => caches.delete(name))
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  const request = event.request;
  const url = new URL(request.url);

  if (request.method !== 'GET') return;

  // Stale-While-Revalidate for local static assets and Cloudflare R2 images
  if (
    url.origin === location.origin && url.pathname.match(/\.(js|css|webp|jpg|jpeg|png|gif|svg|woff2?|eot|ttf|otf)$/i) ||
    url.hostname.includes('media.aatualatalo.com') ||
    url.hostname.includes('unpkg.com')
  ) {
    event.respondWith(
      caches.match(request).then(cachedResponse => {
        const networkFetch = fetch(request).then(response => {
          // Update cache if fetch succeeds
          if (response && response.status === 200) {
            const responseClone = response.clone();
            caches.open(CACHE_NAME).then(cache => {
              cache.put(request, responseClone);
            });
          }
          return response;
        }).catch(err => {
          // Ignore network failure and let the cached response serve if available
          console.log('[ServiceWorker] Fetch failed for', request.url, err);
        });

        return cachedResponse || networkFetch;
      })
    );
  }
});
