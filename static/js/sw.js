// sw.js - very small service worker for offline caching
const CACHE_NAME = "taskmaster-cache-v1";
const OFFLINE_URL = "/";

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll([
        "/",
        "/static/css/main.css",
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"
      ]);
    })
  );
});

self.addEventListener("fetch", function(event) {
  event.respondWith(fetch(event.request).catch(function() {
    return caches.match(event.request).then(function(response) {
      return response || caches.match(OFFLINE_URL);
    });
  }));
});
