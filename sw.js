const CACHE = 'mindmap-shell-v3.1-ta-icons-2-ta-names-1-ta-update-v3';
const SHELL = ['./pwa-update.js', './icon.svg?v=ta-20261027', './', './index.html', './manifest.webmanifest', './icon.svg', './icon-192.png', './icon-512.png', './icon-maskable-192.png', './icon-maskable-512.png'];
self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(SHELL)));
});
self.addEventListener('activate', event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(key => key.startsWith('mindmap-shell-') && key !== CACHE).map(key => caches.delete(key)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  if (event.request.method !== 'GET' || url.origin !== self.location.origin || !url.pathname.startsWith(new URL(self.registration.scope).pathname)) return;
  event.respondWith(caches.open(CACHE).then(async cache => (await cache.match(event.request)) || fetch(event.request)));
});

/* TA PWA update worker v1. Append to sw.js (classic or module). */
(() => {
  let updating = false;
  self.addEventListener('message', event => {
    if (event.data?.type !== 'TA_UPDATE_APPLY') return;
    const reply = accepted => event.ports[0]?.postMessage({accepted});
    if (updating || !event.source?.url?.startsWith(self.registration.scope)) { reply(false); return; }
    updating = true;
    event.waitUntil((async () => {
      let windows = [];
      try {
        windows = (await self.clients.matchAll({type:'window',includeUncontrolled:true}))
          .filter(client => client.url.startsWith(self.registration.scope));
        if (!windows.length) { reply(false); return; }
        const ready = await Promise.all(windows.map(client => new Promise(resolve => {
          const channel = new MessageChannel();
          const timeout = setTimeout(() => { channel.port1.close(); resolve(false); },2000);
          channel.port1.onmessage = message => {
            clearTimeout(timeout); channel.port1.close(); resolve(message.data?.ready === true);
          };
          client.postMessage({type:'TA_UPDATE_PREPARE'},[channel.port2]);
        })));
        if (!ready.every(Boolean)) {
          windows.forEach(client => client.postMessage({type:'TA_UPDATE_CANCEL'}));
          reply(false); return;
        }
        reply(true);
        await self.skipWaiting();
      } catch {
        windows.forEach(client => client.postMessage({type:'TA_UPDATE_CANCEL'}));
        reply(false);
      } finally { updating = false; }
    })());
  });
})();
