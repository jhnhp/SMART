(() => {
'use strict';

const modules = [
  {n:1,title:'Pengantar Remote Sensing dan Digital Soil Mapping',short:'Konsep dasar',file:'Modul 1.md',desc:'Memahami prinsip penginderaan jauh dan pemetaan tanah digital.'},
  {n:2,title:'Multi-source Data Fusion',short:'Integrasi sumber data',file:'Modul 2.md',desc:'Mengenali karakteristik sumber data dan level fusi data.'},
  {n:3,title:'Remote Sensing untuk Delineasi Soil Mapping Units (SMU)',short:'Delineasi SMU',file:'Modul 3.md',desc:'Membaca lanskap dan memahami satuan pemetaan tanah.'},
  {n:4,title:'Remote Sensing untuk Estimasi Soil Properties',short:'Estimasi sifat tanah',file:'Modul 4.md',desc:'Memahami indikator dan faktor estimasi sifat tanah.'},
  {n:5,title:'Bare Soil Detection & Information Extraction',short:'Ekstraksi informasi',file:'Modul 5.md',desc:'Memahami deteksi tanah terbuka dan informasi spektral.'},
  {n:6,title:'Interpretasi Pedologis dari Data Remote Sensing',short:'Interpretasi pedologis',file:'Modul 6.md',desc:'Menghubungkan pola citra dengan proses dan kondisi tanah.'},
  {n:7,title:'Proximal Soil Sensing',short:'Sensor proksimal',file:'Modul 7.md',desc:'Mengenal pengukuran spektral dari jarak dekat.'},
  {n:8,title:'Pemodelan Digital Soil Mapping',short:'Pemodelan DSM',file:'Modul 8.md',desc:'Mengintegrasikan data, pemodelan, validasi, dan ketidakpastian.'}
];
const $ = id => document.getElementById(id);
const nav = $('moduleNav'), cards = $('moduleCards'), prose = $('prose'), chapterList = $('chapterList');
let current = 1, cache = new Map(), searchTerm = '', toastTimer, requestId = 0;

const esc = value => String(value).replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
function say(message) {
  const toast = $('toast');
  if (!toast) return;
  toast.textContent = message; toast.classList.add('show');
  clearTimeout(toastTimer); toastTimer = setTimeout(() => toast.classList.remove('show'), 2600);
}
function makeNav() {
  nav.innerHTML = ''; cards.innerHTML = '';
  modules.forEach(m => {
    const a = document.createElement('a');
    a.className = 'module-nav-item'; a.href = '#modul-' + m.n; a.dataset.module = m.n;
    a.innerHTML = '<span class="nav-number">' + String(m.n).padStart(2,'0') + '</span><span class="nav-text">' + esc(m.title) + '</span>';
    a.addEventListener('click', e => { e.preventDefault(); loadModule(m.n, true); $('sidebar').classList.remove('open'); });
    nav.appendChild(a);

    const b = document.createElement('button');
    b.type = 'button'; b.className = 'module-card'; b.dataset.module = m.n;
    b.innerHTML = '<span class="card-number"><span>MODUL / ' + String(m.n).padStart(2,'0') + '</span><span class="card-arrow">↗</span></span><span class="card-title">' + esc(m.title) + '</span><span class="card-sub">' + esc(m.desc) + '</span>';
    b.addEventListener('click', () => loadModule(m.n, true));
    cards.appendChild(b);
  });
}
function activate(n) {
  current = n;
  document.querySelectorAll('[data-module]').forEach(el => {
    el.classList.toggle(el.classList.contains('module-card') ? 'selected' : 'active', Number(el.dataset.module) === n);
    if (el.classList.contains('module-nav-item')) el.setAttribute('aria-current', Number(el.dataset.module) === n ? 'page' : 'false');
  });
  const m = modules[n-1];
  $('readerKicker').textContent = 'MODUL ' + String(n).padStart(2,'0') + ' / 08';
  $('readerTitle').textContent = m.title;
  $('pageCounter').textContent = String(n).padStart(2,'0') + ' / 08';
  $('prevModule').disabled = n === 1; $('nextModule').disabled = false;
  $('prevModule').style.visibility = n === 1 ? 'hidden' : 'visible';
  $('nextModule').textContent = n === 8 ? 'Kembali ke Modul 1 ↑' : 'Modul berikutnya →';
  if (location.hash !== '#modul-' + n) history.replaceState(null, '', '#modul-' + n);
}
function fixPaths(md) {
  return md.replace(/(!\[[^\]]*\]\()((?:\.\/)?assets\/)/g, '$1../Output/assets/')
           .replace(/(!\[[^\]]*\]\()((?:\.\.\/)+assets\/)/g, '$1../Output/assets/')
           .replace(/(\]\()((?:\.\/)?assets\/)/g, '$1../Output/assets/');
}
function renderMath(root) {
  if (window.renderMathInElement) window.renderMathInElement(root, {
    delimiters: [{left:'$$',right:'$$',display:true},{left:'\\[',right:'\\]',display:true},{left:'\\(',right:'\\)',display:false},{left:'$',right:'$',display:false}],
    throwOnError:false, ignoredTags:['script','noscript','style','textarea','pre','code']
  });
}
function buildChapters() {
  chapterList.innerHTML = '';
  const headings = [...prose.querySelectorAll('h1,h2,h3')];
  if (!headings.length) { chapterList.textContent = 'Daftar isi tidak tersedia untuk modul ini.'; return; }
  headings.forEach((heading, i) => {
    if (!heading.id) heading.id = 'm' + current + '-heading-' + i;
    const a = document.createElement('a'); a.href = '#' + heading.id;
    a.className = 'chapter-link level-' + heading.tagName.slice(1); a.textContent = heading.textContent;
    a.addEventListener('click', e => {
      e.preventDefault(); heading.scrollIntoView({behavior:'smooth',block:'start'});
      chapterList.querySelectorAll('a').forEach(x => x.classList.remove('active')); a.classList.add('active');
    });
    chapterList.appendChild(a);
  });
}
async function fetchMarkdown(n) {
  if (cache.has(n)) return cache.get(n);
  const response = await fetch('../Output/' + encodeURIComponent(modules[n-1].file), {cache:'no-cache'});
  if (!response.ok) throw new Error('File sumber tidak ditemukan (HTTP ' + response.status + ').');
  const md = await response.text(); cache.set(n, md); return md;
}
async function loadModule(n, scroll = false) {
  if (n < 1 || n > modules.length) return;
  const thisRequest = ++requestId;
  activate(n);
  prose.innerHTML = '<div class="loading"><span class="spinner"></span><p>Membuka materi Modul ' + String(n).padStart(2,'0') + '…</p></div>';
  chapterList.innerHTML = '<div class="loading">Menyiapkan daftar isi…</div>';
  try {
    const md = await fetchMarkdown(n);
    if (thisRequest !== requestId) return;
    if (!window.marked) throw new Error('Pustaka Markdown gagal dimuat. Periksa koneksi internet lalu muat ulang halaman.');
    marked.setOptions({gfm:true,breaks:false});
    prose.innerHTML = marked.parse(fixPaths(md));
    prose.querySelectorAll('a').forEach(a => {
      const href = a.getAttribute('href') || '';
      if (/^https?:\/\//i.test(href)) { a.target = '_blank'; a.rel = 'noopener noreferrer'; }
      else if (href.endsWith('.md')) a.href = 'https://github.com/jhnhp/SMART/blob/main/Output/' + encodeURIComponent(href.split('/').pop());
    });
    prose.querySelectorAll('img').forEach(img => {
      img.loading = 'lazy';
      img.addEventListener('error', () => { img.alt = (img.alt ? img.alt + ' — ' : '') + 'Gambar tidak dapat dimuat: ' + img.getAttribute('src'); });
    });
    renderMath(prose); buildChapters();
    $('readerTime').textContent = md.trim().split(/\s+/).length.toLocaleString('id-ID') + ' KATA · MATERI SUMBER';
    if (scroll) $('readerSection').scrollIntoView({behavior:'smooth',block:'start'});
    if (searchTerm) searchInCurrent();
  } catch (error) {
    if (thisRequest !== requestId) return;
    prose.innerHTML = '<div class="load-error"><h3>Materi belum dapat dibuka</h3><p>' + esc(error.message) + '</p><p>Silakan coba lagi. Jika masalah berlanjut, sumber materi dapat dibuka langsung di repository.</p><a href="https://github.com/jhnhp/SMART/tree/main/Output" target="_blank" rel="noopener noreferrer">Buka folder sumber ↗</a><br><button type="button" id="retryLoad" class="quiet-btn">Coba muat lagi</button></div>';
    $('retryLoad').addEventListener('click', () => { cache.delete(n); loadModule(n, false); });
    chapterList.innerHTML = ''; $('readerTime').textContent = 'GAGAL MEMUAT';
    say('Modul ' + n + ' gagal dimuat. Detail error ditampilkan di area materi.');
  }
}
function searchInCurrent() {
  prose.querySelectorAll('.search-hit').forEach(el => el.classList.remove('search-hit'));
  if (!searchTerm) return;
  const walker = document.createTreeWalker(prose, NodeFilter.SHOW_TEXT);
  let node;
  while ((node = walker.nextNode())) {
    if (node.parentElement.closest('script,style,code,pre')) continue;
    if (node.nodeValue.toLocaleLowerCase('id').includes(searchTerm)) {
      node.parentElement.classList.add('search-hit');
      node.parentElement.scrollIntoView({behavior:'smooth',block:'center'}); return;
    }
  }
}
$('search').addEventListener('keydown', async e => {
  if (e.key !== 'Enter') return;
  searchTerm = e.target.value.trim().toLocaleLowerCase('id');
  if (!searchTerm) return;
  say('Mencari di seluruh delapan modul…');
  try {
    const all = await Promise.all(modules.map(async m => ({n:m.n, md:await fetchMarkdown(m.n)})));
    const found = all.find(item => item.md.toLocaleLowerCase('id').includes(searchTerm));
    if (found) { await loadModule(found.n, true); searchInCurrent(); say('Ditemukan di Modul ' + found.n); }
    else say('Istilah tidak ditemukan. Coba kata kunci lain.');
  } catch (error) { say('Pencarian gagal: ' + error.message); }
});
$('search').addEventListener('input', e => {
  if (!e.target.value) { searchTerm = ''; prose.querySelectorAll('.search-hit').forEach(el => el.classList.remove('search-hit')); }
});
$('themeToggle').addEventListener('click', () => {
  const dark = document.documentElement.dataset.theme !== 'dark';
  document.documentElement.dataset.theme = dark ? 'dark' : 'light';
  try { localStorage.setItem('smart-theme', dark ? 'dark' : 'light'); } catch (_) {}
});
$('textToggle').addEventListener('click', () => {
  const large = document.body.classList.toggle('xlarge-text');
  document.body.classList.remove('large-text'); say(large ? 'Teks diperbesar' : 'Ukuran teks normal');
});
$('printBtn').addEventListener('click', () => window.print());
$('focusBtn').addEventListener('click', () => {
  document.body.classList.toggle('focus-mode');
  $('focusBtn').textContent = document.body.classList.contains('focus-mode') ? 'Keluar mode baca ↙' : 'Mode baca ↗';
});
function closeModuleDrawer() {
  $('sidebar').classList.remove('open');
  document.body.classList.remove('nav-drawer-open');
  $('menuToggle').setAttribute('aria-expanded','false');
}
$('menuToggle').setAttribute('aria-controls','sidebar');
$('menuToggle').setAttribute('aria-expanded','false');
$('menuToggle').addEventListener('click', () => {
  if (window.matchMedia('(max-width: 1100px)').matches) {
    const open = $('sidebar').classList.toggle('open');
    document.body.classList.toggle('nav-drawer-open', open);
    $('menuToggle').setAttribute('aria-expanded', String(open));
  } else {
    const collapsed = document.body.classList.toggle('nav-sidebar-collapsed');
    $('menuToggle').setAttribute('aria-expanded', String(!collapsed));
    $('menuToggle').setAttribute('title', collapsed ? 'Tampilkan daftar modul' : 'Sembunyikan daftar modul');
  }
});
document.addEventListener('click', e => {
  if (document.body.classList.contains('nav-drawer-open') &&
      !e.target.closest('#sidebar') && !e.target.closest('#menuToggle')) closeModuleDrawer();
});
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModuleDrawer(); });
window.addEventListener('resize', () => {
  if (!window.matchMedia('(max-width: 1100px)').matches) closeModuleDrawer();
});
$('prevModule').addEventListener('click', () => loadModule(current-1, true));
$('nextModule').addEventListener('click', () => loadModule(current === 8 ? 1 : current+1, true));
window.addEventListener('scroll', () => {
  const d = document.documentElement, max = d.scrollHeight - innerHeight;
  $('progressBar').style.width = (max > 0 ? scrollY/max*100 : 0) + '%';
}, {passive:true});
try { if (localStorage.getItem('smart-theme') === 'dark') document.documentElement.dataset.theme = 'dark'; } catch (_) {}
makeNav();
const hashMatch = location.hash.match(/^#modul-(\d)$/);
loadModule(hashMatch ? Number(hashMatch[1]) : 1, false);
})();