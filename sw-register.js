/* Registers the offline worker and hands new builds over safely.
   A new worker waits until the page asks for it; the page then reloads once onto the new build. */
(function () {
  if (!('serviceWorker' in navigator) || location.protocol === 'file:') return;
  var reg = null, reloading = false, asked = false;

  function activate() {
    var w = reg && reg.waiting;
    if (!w) return false;
    asked = true;
    w.postMessage('skip-waiting');
    setTimeout(function () { if (!reloading) { reloading = true; location.reload(); } }, 3000);   /* in case controllerchange never fires */
    return true;
  }

  /* the app calls this where it used to call location.reload(): with a worker in charge a plain reload would just show the old cached copy */
  window.momoReload = function () {
    if (!navigator.serviceWorker.controller || !reg) { location.reload(); return; }
    if (activate()) return;
    /* the new worker is still downloading: give it up to 20 s, then fall back to a plain reload */
    reg.update().catch(function () {});
    var t0 = Date.now(), iv = setInterval(function () {
      if (activate()) clearInterval(iv);
      else if (Date.now() - t0 > 20000) { clearInterval(iv); location.reload(); }
    }, 500);
  };

  navigator.serviceWorker.addEventListener('controllerchange', function () {
    if (reloading || !asked) return;       /* the first install also changes the controller: no reload then */
    reloading = true; location.reload();
  });

  navigator.serviceWorker.register('sw.js').then(function (r) {
    reg = r;
    function seen() {
      /* a new build is installed and waiting: let the app's own update logic (pill / quiet reload) take over */
      if (reg.waiting && navigator.serviceWorker.controller) window.momoSwReady = true;
    }
    r.addEventListener('updatefound', function () {
      var nw = r.installing;
      if (nw) nw.addEventListener('statechange', function () { if (nw.state === 'installed') seen(); });
    });
    seen();
    document.addEventListener('visibilitychange', function () { if (!document.hidden) r.update().catch(function () {}); });
    setInterval(function () { r.update().catch(function () {}); }, 5 * 60 * 1000);
  }).catch(function () {});
})();
