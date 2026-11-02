/* Interaksi situs: tema, ukuran huruf, menu, daftar isi halaman, pencarian, perbesar gambar, dan salin kode. */
(function () {
  'use strict';
  var akar = document.documentElement;
  var $ = function (s, k) { return (k || document).querySelector(s); };
  var $$ = function (s, k) { return Array.prototype.slice.call((k || document).querySelectorAll(s)); };
  var simpan = function (k, v) { try { localStorage.setItem(k, v); } catch (e) { /* mode privat */ } };
  var baca = function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } };

  // Tema dan ukuran huruf
  var tombolTema = $('#tema');
  if (tombolTema) tombolTema.addEventListener('click', function () {
    var baru = akar.dataset.tema === 'gelap' ? 'terang' : 'gelap';
    akar.dataset.tema = baru;
    simpan('tema', baru);
    tombolTema.setAttribute('aria-pressed', String(baru === 'gelap'));
  });
  var tombolHuruf = $('#huruf');
  if (tombolHuruf) tombolHuruf.addEventListener('click', function () {
    var urut = ['normal', 'besar', 'kecil'];
    var baru = urut[(urut.indexOf(akar.dataset.huruf || 'normal') + 1) % 3];
    akar.dataset.huruf = baru;
    simpan('huruf', baru);
    tombolHuruf.title = 'Ukuran huruf: ' + baru;
  });

  // Menu pada layar kecil
  var samping = $('.samping'), selubung = $('.selubung'), tombolMenu = $('#menu');
  function menu(buka) {
    if (!samping) return;
    samping.classList.toggle('buka', buka);
    if (selubung) selubung.classList.toggle('buka', buka);
    if (tombolMenu) tombolMenu.setAttribute('aria-expanded', String(buka));
    if (buka) { var a = $('[aria-current="page"]', samping) || $('a', samping); if (a) a.focus(); }
  }
  if (tombolMenu) tombolMenu.addEventListener('click', function () { menu(true); });
  if (selubung) selubung.addEventListener('click', function () { menu(false); });
  var tutupMenu = $('.samping-tutup');
  if (tutupMenu) tutupMenu.addEventListener('click', function () { menu(false); tombolMenu.focus(); });
  if (samping) {
    var kini = $('[aria-current="page"]', samping);
    if (kini) kini.scrollIntoView({ block: 'center' });
  }

  // Kemajuan membaca dan tombol ke atas
  var kemajuan = $('.kemajuan'), keAtas = $('.ke-atas');
  function gulir() {
    var total = document.body.scrollHeight - innerHeight;
    if (kemajuan) kemajuan.style.width = (total > 0 ? Math.min(100, scrollY / total * 100) : 0) + '%';
    if (keAtas) keAtas.classList.toggle('tampil', scrollY > 700);
  }
  addEventListener('scroll', gulir, { passive: true });
  gulir();
  if (keAtas) keAtas.addEventListener('click', function () { scrollTo({ top: 0 }); });

  // Daftar isi halaman mengikuti posisi baca
  var tautanIsi = $$('.kanan a');
  if (tautanIsi.length && 'IntersectionObserver' in window) {
    var peta = {};
    tautanIsi.forEach(function (a) { peta[decodeURIComponent(a.hash.slice(1))] = a; });
    var aktif = null;
    var tandai = function (a) {
      if (aktif === a) return;
      if (aktif) { aktif.classList.remove('aktif'); aktif.removeAttribute('aria-current'); }
      aktif = a;
      if (a) { a.classList.add('aktif'); a.setAttribute('aria-current', 'location'); }
      if (a) { var kanan = $('.kanan'), b = a.getBoundingClientRect(), k = kanan.getBoundingClientRect(); if (b.top < k.top || b.bottom > k.bottom) kanan.scrollTop += b.top - k.top - 80; }
    };
    var judul = $$('.prosa h2[id]').filter(function (h) { return peta[h.id]; });
    var cek = function () {
      var batas = 120, hasil = null;
      judul.forEach(function (h) { if (h.getBoundingClientRect().top <= batas) hasil = h; });
      tandai(hasil ? peta[hasil.id] : tautanIsi[0]);
    };
    addEventListener('scroll', cek, { passive: true });
    cek();
  }

  // Salin kode
  $$('.prosa pre').forEach(function (pre) {
    var b = document.createElement('button');
    b.className = 'salin';
    b.type = 'button';
    b.textContent = 'Salin';
    b.addEventListener('click', function () {
      var kode = $('code', pre) || pre;
      var selesai = function () { b.textContent = 'Tersalin'; setTimeout(function () { b.textContent = 'Salin'; }, 1500); };
      if (navigator.clipboard) navigator.clipboard.writeText(kode.textContent).then(selesai);
    });
    pre.appendChild(b);
  });

  // Perbesar gambar
  var pembesar = $('.pembesar');
  if (pembesar) {
    var gbr = $('img', pembesar), ket = $('p', pembesar), asal = null;
    var tutup = function () { pembesar.classList.remove('buka'); gbr.removeAttribute('src'); if (asal) asal.focus(); };
    $$('.prosa figure.gambar img, .prosa td img').forEach(function (i) {
      i.tabIndex = 0;
      i.setAttribute('role', 'button');
      i.setAttribute('aria-label', 'Perbesar gambar: ' + (i.alt || ''));
      var buka = function () {
        asal = i;
        gbr.src = i.currentSrc || i.src;
        gbr.alt = i.alt;
        var fc = i.closest('figure') && $('figcaption', i.closest('figure'));
        ket.textContent = fc ? fc.textContent : '';
        pembesar.classList.add('buka');
        $('button', pembesar).focus();
      };
      i.addEventListener('click', buka);
      i.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); buka(); } });
    });
    pembesar.addEventListener('click', tutup);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && pembesar.classList.contains('buka')) tutup(); });
  }

  // Pencarian
  var lapis = $('.cari-lapis'), masukan = $('#cari-masukan'), wadah = $('.cari-hasil');
  var indeks = null, pilihan = -1, dasar = document.body.dataset.akar || '';
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function bukaCari() {
    if (!lapis) return;
    lapis.classList.add('buka');
    masukan.focus();
    masukan.select();
    if (!indeks) fetch(dasar + 'aset/indeks-cari.json').then(function (r) { return r.json(); }).then(function (d) { indeks = d; tampil(); }).catch(function () { wadah.innerHTML = '<div class="cari-kosong">Indeks pencarian belum dapat dimuat.</div>'; });
    else tampil();
  }
  function tutupCari() { if (lapis) lapis.classList.remove('buka'); }
  function sorot(t, kata) {
    var h = esc(t);
    kata.forEach(function (k) { h = h.replace(new RegExp('(' + k.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'ig'), '<mark>$1</mark>'); });
    return h;
  }
  function cuplik(x, kata) {
    var r = x.toLowerCase(), p = -1;
    kata.some(function (k) { p = r.indexOf(k); return p >= 0; });
    if (p < 0) return x.slice(0, 150);
    var a = Math.max(0, p - 60);
    return (a ? '… ' : '') + x.slice(a, a + 180) + (a + 180 < x.length ? ' …' : '');
  }
  function tampil() {
    var q = (masukan.value || '').trim().toLowerCase();
    pilihan = -1;
    if (!q) { wadah.innerHTML = '<div class="cari-kosong">Ketik istilah, misalnya SCORPAN, pan-sharpening, atau NDVI.</div>'; return; }
    if (!indeks) { wadah.innerHTML = '<div class="cari-kosong">Memuat indeks…</div>'; return; }
    var kata = q.split(/\s+/).filter(Boolean);
    var hasil = [];
    indeks.forEach(function (d) {
      var j = d.j.toLowerCase(), x = d.x.toLowerCase(), skor = 0;
      var semua = kata.every(function (k) {
        var dj = j.indexOf(k) >= 0, dx = x.indexOf(k) >= 0;
        if (dj) skor += 12;
        if (dx) skor += Math.min(6, x.split(k).length - 1);
        return dj || dx;
      });
      if (semua) hasil.push({ d: d, s: skor });
    });
    hasil.sort(function (a, b) { return b.s - a.s; });
    if (!hasil.length) { wadah.innerHTML = '<div class="cari-kosong">Tidak ada hasil untuk “' + esc(q) + '”.</div>'; return; }
    wadah.innerHTML = hasil.slice(0, 30).map(function (h) {
      return '<a href="' + dasar + h.d.u + '"><small>' + esc(h.d.h) + '</small><b>' + sorot(h.d.j, kata) + '</b><span>' + sorot(cuplik(h.d.x, kata), kata) + '</span></a>';
    }).join('');
  }
  if (lapis) {
    var bukaTombol = $('.cari-tombol');
    if (bukaTombol) bukaTombol.addEventListener('click', bukaCari);
    lapis.addEventListener('click', function (e) { if (e.target === lapis) tutupCari(); });
    masukan.addEventListener('input', tampil);
    masukan.addEventListener('keydown', function (e) {
      var a = $$('a', wadah);
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault();
        if (!a.length) return;
        pilihan = (pilihan + (e.key === 'ArrowDown' ? 1 : -1) + a.length) % a.length;
        a.forEach(function (x, i) { x.classList.toggle('pilih', i === pilihan); });
        a[pilihan].scrollIntoView({ block: 'nearest' });
      } else if (e.key === 'Enter' && a.length) {
        location.href = a[Math.max(pilihan, 0)].href;
      }
    });
    wadah.addEventListener('click', function (e) { if (e.target.closest('a')) tutupCari(); });
  }

  // Pintasan papan tik
  document.addEventListener('keydown', function (e) {
    var ketik = /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName);
    if ((e.key === 'k' && (e.ctrlKey || e.metaKey)) || (e.key === '/' && !ketik)) { e.preventDefault(); bukaCari(); return; }
    if (e.key === 'Escape') { tutupCari(); menu(false); }
  });

  // Bacaan terakhir
  var halaman = document.body.dataset.halaman;
  if (halaman) simpan('terakhir', JSON.stringify({ u: halaman, j: document.body.dataset.judul }));
  var lanjutkan = $('.lanjutkan');
  if (lanjutkan) {
    try {
      var t = JSON.parse(baca('terakhir') || 'null');
      if (t) { var a = $('a', lanjutkan); a.href = t.u; a.textContent = t.j; lanjutkan.classList.add('tampil'); }
    } catch (e) { /* abaikan */ }
  }
})();
