import fs from 'node:fs';
import path from 'node:path';
import { marked } from 'marked';

const root = process.cwd();
const sourceDir = path.join(root, 'Output');
const siteDir = path.join(root, '_site');
const assetDir = path.join(siteDir, 'assets');
const websiteDir = path.join(root, 'website');

fs.mkdirSync(siteDir, { recursive: true });
fs.mkdirSync(assetDir, { recursive: true });
fs.cpSync(path.join(sourceDir, 'assets'), assetDir, { recursive: true });
fs.copyFileSync(path.join(websiteDir, 'styles.css'), path.join(siteDir, 'styles.css'));

const titles = [
  'Dasar-dasar Remote Sensing dan Digital Soil Mapping',
  'Multi-source Data Fusion',
  'Remote Sensing untuk Delineasi Soil Mapping Units (SMU)',
  'Remote Sensing untuk Estimasi Soil Properties',
  'Bare Soil Detection & Information Extraction',
  'Interpretasi Pedologis dari Data Remote Sensing',
  'Proximal Soil Sensing',
  'Pemodelan Digital Soil Mapping'
];

const renderer = new marked.Renderer();
renderer.image = ({ href, title, text }) => {
  const safeHref = String(href || '').replace(/^\.\//, '');
  const finalHref = safeHref.startsWith('assets/') ? safeHref : safeHref;
  const titleAttr = title ? ' title="' + escapeAttr(title) + '"' : '';
  return '<img src="' + escapeAttr(finalHref) + '" alt="' + escapeAttr(text || '') + '"' + titleAttr + ' loading="lazy">';
};
marked.setOptions({ gfm: true, breaks: false, renderer });

function escapeHtml(s) {
  return String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
}
function escapeAttr(s) { return escapeHtml(s).replace(/'/g, '&#39;'); }

for (let n = 1; n <= 8; n++) {
  const mdPath = path.join(sourceDir, `Modul ${n}.md`);
  const markdown = fs.readFileSync(mdPath, 'utf8');
  const content = marked.parse(markdown);
  const previous = n > 1 ? `<a href="modul-${n-1}.html">← Modul sebelumnya</a>` : '<a href="index.html">← Beranda</a>';
  const next = n < 8 ? `<a href="modul-${n+1}.html">Modul berikutnya →</a>` : '<a href="index.html">Kembali ke beranda ↑</a>';
  const html = `<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#f7f7f2">
<title>Modul ${n} — ${escapeHtml(titles[n-1])} | SMART Fieldbook</title>
<link rel="stylesheet" href="styles.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<style>
.module-page{max-width:1120px;margin:0 auto;padding:28px clamp(18px,4vw,56px) 80px}
.module-head{display:flex;align-items:center;justify-content:space-between;gap:16px;border-bottom:1px solid var(--line,#ddd);padding-bottom:18px;margin-bottom:28px}
.module-head a{color:inherit;text-decoration:none}.module-tag{font:500 12px monospace;letter-spacing:.12em;opacity:.7}
.module-content{max-width:850px;margin:auto;line-height:1.75}.module-content img{max-width:100%;height:auto;display:block;margin:24px auto;border-radius:8px}
.module-content table{display:block;max-width:100%;overflow-x:auto;border-collapse:collapse}
.module-content th,.module-content td{border:1px solid var(--line,#ddd);padding:9px 12px;vertical-align:top}
.module-content th{background:var(--surface,#f3f4f5)}.module-content pre{overflow:auto;padding:16px;border-radius:8px;background:var(--surface,#f3f4f5)}
.module-content blockquote{border-left:3px solid #4d8b75;padding-left:16px;opacity:.9}
.module-bottom{display:flex;justify-content:space-between;gap:12px;margin-top:48px;padding-top:20px;border-top:1px solid var(--line,#ddd)}
.module-bottom a{padding:12px 16px;border:1px solid var(--line,#ddd);border-radius:8px;text-decoration:none;color:inherit}
@media(max-width:600px){.module-head{align-items:flex-start;flex-direction:column}.module-bottom a{font-size:14px}}
@media print{.topbar,.module-bottom{display:none}.module-page{max-width:none;padding:0}.module-content{max-width:none}}
</style>
</head>
<body>
<header class="topbar">
<a class="wordmark" href="index.html"><span class="mark">S<span>·</span></span><span>SMART <small>FIELD BOOK / UGM</small></span></a>
<div class="top-actions"><button class="icon-btn" id="themeToggle" aria-label="Ubah tema" title="Ubah tema">◐</button><button class="icon-btn" id="textToggle" aria-label="Perbesar teks" title="Perbesar teks">Aa</button><button class="icon-btn" onclick="window.print()" aria-label="Cetak atau simpan PDF" title="Cetak atau simpan PDF">↗</button></div>
</header>
<div class="module-page">
<div class="module-head"><div><div class="module-tag">SMART FIELDBOOK · MODUL ${String(n).padStart(2,'0')} / 08</div><h1>${escapeHtml(titles[n-1])}</h1></div><a href="index.html">← Semua modul</a></div>
<main class="module-content" id="content">
${content}
</main>
<div class="module-bottom">${previous}${next}</div>
</div>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"><\/script>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"><\/script>
<script>
(()=>{if(window.renderMathInElement)renderMathInElement(document.getElementById('content'),{delimiters:[{left:'$$',right:'$$',display:true},{left:'\\\\[',right:'\\\\]',display:true},{left:'\\\\(',right:'\\\\)',display:false},{left:'$',right:'$',display:false}],throwOnError:false,ignoredTags:['script','style','textarea','pre','code']});const theme=document.getElementById('themeToggle');theme.onclick=()=>{const dark=document.documentElement.dataset.theme!=='dark';document.documentElement.dataset.theme=dark?'dark':'light';localStorage.setItem('smart-theme',dark?'dark':'light')};document.getElementById('textToggle').onclick=()=>document.body.classList.toggle('xlarge-text');if(localStorage.getItem('smart-theme')==='dark')document.documentElement.dataset.theme='dark';})();
<\/script>
</body></html>`;
  fs.writeFileSync(path.join(siteDir, `modul-${n}.html`), html, 'utf8');
}
fs.copyFileSync(path.join(websiteDir, 'index.html'), path.join(siteDir, 'index.html'));
fs.writeFileSync(path.join(siteDir, '.nojekyll'), '');
console.log('Generated 8 pre-rendered HTML modules; Markdown is not fetched by the browser.');
