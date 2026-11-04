#!/usr/bin/env node
/*
 * Menggabungkan modul praktik (Output/Pelatihan/modul/*.md) menjadi satu .docx.
 * Tata letak mengikuti Training Modul Precision Nutrient Management: sampul berpita, daftar isi berkotak nomor,
 * halaman Kurikulum Pembelajaran per bagian, tab judul di header, dan footer berwarna. Warnanya memakai biru dan emas UGM.
 *
 * Daftar isi, daftar tabel, dan daftar gambar adalah medan TOC bawaan Word, dan nomor caption adalah medan SEQ,
 * sehingga ikut berubah ketika dokumen diedit lalu medannya diperbarui. Word juga diminta memperbarui medan saat berkas
 * dibuka (updateFields). Agar isinya tetap tampil sebelum diperbarui, dokumen dibangun dua kali: bangunan pertama
 * dirender ke PDF untuk mengetahui halaman setiap judul, bangunan kedua menyimpan isi daftar sebagai nilai tersimpan.
 *
 * Jalankan: NODE_PATH=<folder>/node_modules node Output/scripts/pelatihan_buat_docx.js <folder_kerja_sementara>
 * Memerlukan: docx dan jszip (npm), LibreOffice, poppler-utils, ImageMagick.
 *
 * Di Windows, dua variabel lingkungan dapat menggantikan alat Linux tersebut:
 * - ALAT_PYTHON=<python yang memiliki Pillow dan PyMuPDF> menggantikan ImageMagick dan poppler-utils;
 * - PDF_WORD=1 membuat PDF uji dengan Microsoft Word melalui PowerShell, sehingga nomor halaman pada daftar
 *   mengikuti tata letak Word. Tanpa itu dipakai LibreOffice (`soffice`, atau jalur pada variabel SOFFICE).
 */
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const D = require('docx');
const JSZip = require('jszip');

const AKAR = path.resolve(__dirname, '..', '..');
const MODUL = path.join(AKAR, 'Output', 'Pelatihan', 'modul');
const ASET = path.join(AKAR, 'Output', 'assets', 'pelatihan');
const KELUAR = path.join(AKAR, 'Output', 'Pelatihan', 'Modul_Praktik_RS_DSM.docx');
const KERJA = process.argv[2];
fs.mkdirSync(path.join(KERJA, 'gambar'), { recursive: true });

const NAVY = '01416B', EMAS = 'FFD500', SOROT = 'FFF4C4', KOTAK = 'DCE8F2', ABU = '5F6B76', LEMBUT = 'F2F6FA', GARIS = 'C9D3DC';
const FONT = 'Calibri';
const LEBAR_HAL = 11906, TINGGI_HAL = 16838, TEPI = 1200;
const LEBAR_TEKS = LEBAR_HAL - 2 * TEPI;
const ORGANISASI = 'PS2DL Universitas Gadjah Mada';
const HAK_CIPTA = '© 2026 Pusat Studi Pengelolaan Sumber Daya Lahan, Universitas Gadjah Mada';

// ---------------------------------------------------------------- pembacaan markdown
function bacaBlok(teks) {
  const baris = teks.split('\n');
  const blok = [];
  let i = 0;
  while (i < baris.length) {
    const b = baris[i];
    if (!b.trim()) { i++; continue; }
    if (b.startsWith('```')) {
      const isi = [];
      i++;
      while (!baris[i].startsWith('```')) isi.push(baris[i++]);
      i++;
      blok.push({ jenis: 'kode', isi });
      continue;
    }
    if (b.startsWith('# ')) { blok.push({ jenis: 'h1', teks: b.slice(2) }); i++; continue; }
    if (b.startsWith('## ')) { blok.push({ jenis: 'h2', teks: b.slice(3) }); i++; continue; }
    let m = b.match(/^!\[.*\]\((.*)\)/);
    if (m) { blok.push({ jenis: 'gambar', jalur: m[1] }); i++; continue; }
    if (b.startsWith('|')) {
      const r = [];
      let rata = [];
      while (i < baris.length && baris[i].startsWith('|')) {
        const sel = baris[i].trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map(s => s.trim());
        if (sel.every(s => /^:?-+:?$/.test(s))) rata = sel.map(s => /^-+:$/.test(s));
        else r.push(sel);
        i++;
      }
      blok.push({ jenis: 'tabel', baris: r, rataKanan: rata });
      continue;
    }
    m = b.match(/^(\d+)\. (.*)/);
    if (m) { blok.push({ jenis: 'nomor', no: m[1], teks: m[2] }); i++; continue; }
    if (b.startsWith('- ')) { blok.push({ jenis: 'butir', teks: b.slice(2), tingkat: 0 }); i++; continue; }
    if (b.startsWith('   - ')) { blok.push({ jenis: 'butir', teks: b.slice(5), tingkat: 1 }); i++; continue; }
    if (/^Gambar P\d/.test(b)) { blok.push({ jenis: 'kapsi', teks: b }); i++; continue; }
    if (/^Tabel P\d+\.\d+ [A-Z*]/.test(b) && (baris[i + 2] || '').startsWith('|')) { blok.push({ jenis: 'kapsiTabel', teks: b }); i++; continue; }
    if (b.startsWith('Sumber:')) { blok.push({ jenis: 'sumber', teks: b }); i++; continue; }
    blok.push({ jenis: 'par', teks: b });
    i++;
  }
  return blok;
}

function sebaris(teks, opsi = {}) {
  const ukuran = opsi.ukuran || 22;
  const warna = opsi.warna;
  const run = [];
  const pola = /(\*\*\*[^*]+\*\*\*|\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|<https?:[^>]+>|\[perlu konfirmasi[^\]]*\])/g;
  for (const potong of teks.split(pola)) {
    if (!potong) continue;
    const dasar = opsi.ikutGaya ? {} : { font: FONT, size: ukuran, color: warna, bold: opsi.tebal, italics: opsi.miring };
    if (potong.startsWith('***')) run.push(new D.TextRun({ ...dasar, text: potong.slice(3, -3), bold: true, italics: true }));
    else if (potong.startsWith('**')) {
      const dalam = potong.slice(2, -2);
      if (dalam.startsWith('[perlu')) run.push(new D.TextRun({ ...dasar, text: dalam, bold: true, highlight: 'yellow' }));
      else run.push(...sebaris(dalam, { ...opsi, tebal: true, warna: opsi.warna || NAVY }));
    }
    else if (potong.startsWith('*')) run.push(new D.TextRun({ ...dasar, text: potong.slice(1, -1), italics: true }));
    else if (potong.startsWith('`')) run.push(new D.TextRun(opsi.ikutGaya ? { text: potong.slice(1, -1), font: 'Consolas' } : { ...dasar, text: potong.slice(1, -1), font: 'Consolas', size: ukuran - 3, color: warna === 'FFFFFF' ? warna : '23476B' }));
    else if (potong.startsWith('<http')) run.push(new D.TextRun({ ...dasar, text: potong.slice(1, -1), color: NAVY, underline: {} }));
    else if (potong.startsWith('[perlu')) run.push(new D.TextRun({ ...dasar, text: potong, highlight: 'yellow' }));
    else run.push(new D.TextRun({ ...dasar, text: potong }));
  }
  return run;
}

// ---------------------------------------------------------------- alat luar
const ALAT_PYTHON = process.env.ALAT_PYTHON;
const PDF_WORD = process.env.PDF_WORD === '1';

function python(kode, ...arg) {
  return execFileSync(ALAT_PYTHON, ['-I', '-c', kode, ...arg], { maxBuffer: 256 * 1024 * 1024 }).toString();
}

// setara convert -background white -flatten -resize 1400x> -quality 86
const PY_GAMBAR = `
import sys
from PIL import Image
im = Image.open(sys.argv[1])
if im.mode in ('RGBA', 'LA', 'P', 'PA'):
    im = im.convert('RGBA')
    latar = Image.new('RGB', im.size, 'white')
    latar.paste(im, mask=im.split()[3])
    im = latar
else:
    im = im.convert('RGB')
if im.width > 1400:
    im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
im.save(sys.argv[2], quality=86)
`;

function ukuranGambar(jalur) {
  if (ALAT_PYTHON) return python('import sys\nfrom PIL import Image\nprint(*Image.open(sys.argv[1]).size)', jalur).trim().split(' ').map(Number);
  return execFileSync('identify', ['-format', '%w %h', jalur]).toString().split(' ').map(Number);
}

function keePdf(docx, folder) {
  if (PDF_WORD) {
    const pdf = path.join(folder, path.basename(docx).replace(/\.docx$/i, '.pdf'));
    const skrip = `$w = New-Object -ComObject Word.Application; $w.Visible = $false; $w.DisplayAlerts = 0; ` +
      `try { $d = $w.Documents.Open('${docx}', $false, $true); $d.ExportAsFixedFormat('${pdf}', 17); $d.Close(0) } finally { $w.Quit() }`;
    execFileSync('powershell', ['-NoProfile', '-NonInteractive', '-Command', skrip], { stdio: 'ignore', timeout: 600000 });
    return;
  }
  execFileSync(process.env.SOFFICE || 'soffice', ['--headless', '--convert-to', 'pdf', '--outdir', folder, docx], { stdio: 'ignore' });
}

function teksPerHalaman(pdf) {
  if (ALAT_PYTHON) return JSON.parse(python('import sys, json, fitz\nprint(json.dumps([p.get_text(sort=True) for p in fitz.open(sys.argv[1])]))', pdf));
  const jumlah = Number(execFileSync('pdfinfo', [pdf]).toString().match(/Pages:\s+(\d+)/)[1]);
  const hasil = [];
  for (let i = 1; i <= jumlah; i++) hasil.push(execFileSync('pdftotext', ['-f', String(i), '-l', String(i), pdf, '-']).toString());
  return hasil;
}

// ---------------------------------------------------------------- gambar
function siapkanGambar(jalur) {
  const asal = path.resolve(MODUL, jalur);
  const nama = jalur.replace(/[^\w.-]+/g, '_').replace(/\.png$/, '.jpg');
  const tujuan = path.join(KERJA, 'gambar', nama);
  if (!fs.existsSync(tujuan)) {
    if (ALAT_PYTHON) python(PY_GAMBAR, asal, tujuan);
    else execFileSync('convert', [asal, '-background', 'white', '-flatten', '-resize', '1400x>', '-quality', '86', tujuan]);
  }
  const [l, t] = ukuranGambar(tujuan);
  const asli = ukuranGambar(asal)[0];
  // jendela penuh selebar teks; dialog kecil ditampilkan lebih kecil agar tidak memakan halaman
  // dua gambar dengan satu langkah singkat harus muat dalam satu halaman
  let lebar = Number(asli) >= 1200 ? 570 : Math.min(570, Number(asli) * 0.54);
  let tinggi = lebar * t / l;
  if (tinggi > 355) { lebar *= 355 / tinggi; tinggi = 355; }
  return { data: fs.readFileSync(tujuan), lebar: Math.round(lebar), tinggi: Math.round(tinggi), bingkai: jalur.includes('screenshots') };
}

function gambarPng(nama, warna) {
  const tujuan = path.join(KERJA, nama);
  if (!fs.existsSync(tujuan)) {
    if (ALAT_PYTHON) python('import sys\nfrom PIL import Image\nImage.new("RGB", (8, 8), "#" + sys.argv[2]).save(sys.argv[1])', tujuan, warna);
    else execFileSync('convert', ['-size', '8x8', `xc:#${warna}`, tujuan]);
  }
  return fs.readFileSync(tujuan);
}

function mengambang(data, x, y, l, t, jenis = 'png') {
  return new D.ImageRun({
    type: jenis, data, transformation: { width: l, height: t },
    floating: {
      horizontalPosition: { relative: D.HorizontalPositionRelativeFrom.PAGE, offset: Math.round(x * 9525) },
      verticalPosition: { relative: D.VerticalPositionRelativeFrom.PAGE, offset: Math.round(y * 9525) },
      allowOverlap: true, behindDocument: true, wrap: { type: D.TextWrappingType.NONE },
    },
  });
}

// ---------------------------------------------------------------- blok dokumen
const tanpaGaris = { style: D.BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const semuaTanpaGaris = { top: tanpaGaris, bottom: tanpaGaris, left: tanpaGaris, right: tanpaGaris };

function paragraf(teks, opsi = {}) {
  return new D.Paragraph({
    children: sebaris(teks, opsi),
    alignment: opsi.rata || D.AlignmentType.JUSTIFIED,
    spacing: { after: opsi.setelah ?? 120, before: opsi.sebelum ?? 0, line: 276 },
    indent: opsi.indent, keepNext: opsi.keepNext, keepLines: opsi.keepLines, border: opsi.border, shading: opsi.shading,
  });
}

function judulBesar(teks, marka) {
  const anak = [new D.TextRun({ text: teks })];
  return [new D.Paragraph({ heading: D.HeadingLevel.HEADING_1, children: marka ? [new D.Bookmark({ id: marka, children: anak })] : anak, border: { bottom: { style: D.BorderStyle.SINGLE, size: 18, color: EMAS, space: 6 } } })];
}

function judulTahap(teks, marka) {
  const anak = [new D.TextRun({ text: teks })];
  // hanya judul bermarka yang masuk daftar isi; judul lain memakai gaya serupa yang berada di luar jangkauan medan TOC
  return marka ? new D.Paragraph({ heading: D.HeadingLevel.HEADING_2, children: [new D.Bookmark({ id: marka, children: anak })] }) : new D.Paragraph({ style: 'Subjudul', children: anak });
}

function caption(b, opsi) {
  const m = b.teks.match(/^(Gambar|Tabel) (P\d+\.)(\d+) (.*)$/);
  if (!m) throw new Error('Caption tidak terbaca: ' + b.teks);
  const nomorCaption = new D.SimpleField(`SEQ ${m[1]}${b.ulang ? ' \\r 1' : ''} \\* ARABIC`, m[3]);
  return new D.Paragraph({
    style: 'Caption', alignment: opsi.rata, spacing: opsi.spacing,
    children: [new D.Bookmark({ id: b.marka, children: [new D.TextRun({ text: `${m[1]} ${m[2]}` }), nomorCaption, new D.TextRun({ text: ' ' }), ...sebaris(m[4], { ikutGaya: true })] })],
  });
}

function tabelMd(barisTabel, rataKanan = []) {
  const polos = barisTabel.map(r => r.map(s => s.replace(/\*/g, '')));
  const nk = polos[0].length;
  const kata = [...Array(nk).keys()].map(j => Math.max(...polos.map(r => Math.max(...(r[j] || '').replace(/`/g, '').split(/\s+/).map(k => k.length)))));
  const panjang = [...Array(nk).keys()].map(j => Math.max(...polos.map(r => (r[j] || '').replace(/`/g, '').length)));
  const bobot = [...Array(nk).keys()].map(j => Math.max(kata[j] * 1.5, Math.min(panjang[j], 70) * 0.8, 6));
  const jumlah = bobot.reduce((a, b) => a + b, 0);
  const lebar = bobot.map(b => Math.round(LEBAR_TEKS * b / jumlah));
  // kolom harus muat kata terpanjangnya, kecuali kata yang memang terlalu panjang seperti nama adegan
  const perlu = kata.map(k => Math.min(k, 34) * 94 + 180);
  for (let j = 0; j < nk; j++) {
    const kurang = perlu[j] - lebar[j];
    if (kurang <= 0) continue;
    const longgar = lebar.map((l, i) => (i === j ? 0 : Math.max(0, l - perlu[i])));
    const total = longgar.reduce((a, b) => a + b, 0);
    if (total <= 0) continue;
    const ambil = Math.min(kurang, total);
    lebar[j] += ambil;
    longgar.forEach((v, i) => { lebar[i] -= Math.round(ambil * v / total); });
  }
  lebar[nk - 1] += LEBAR_TEKS - lebar.reduce((a, b) => a + b, 0);
  const pendek = barisTabel.length <= 16;
  const garis = { style: D.BorderStyle.SINGLE, size: 4, color: GARIS };
  const baris = barisTabel.map((r, i) => new D.TableRow({
    tableHeader: i === 0, cantSplit: true,
    children: r.map((s, j) => new D.TableCell({
      width: { size: lebar[j], type: D.WidthType.DXA },
      shading: i === 0 ? { type: D.ShadingType.CLEAR, fill: NAVY, color: 'auto' } : (i % 2 === 0 ? { type: D.ShadingType.CLEAR, fill: LEMBUT, color: 'auto' } : undefined),
      margins: { top: 50, bottom: 50, left: 90, right: 90 }, verticalAlign: D.VerticalAlign.CENTER,
      borders: { top: garis, bottom: garis, left: tanpaGaris, right: tanpaGaris },
      children: [new D.Paragraph({
        children: i === 0 ? sebaris(s.replace(/\*\*/g, ''), { ukuran: 19, tebal: true, warna: 'FFFFFF' }) : sebaris(s, { ukuran: 19 }),
        alignment: rataKanan[j] ? D.AlignmentType.RIGHT : D.AlignmentType.LEFT, spacing: { after: 0, line: 245 }, keepNext: pendek,
      })],
    })),
  }));
  return new D.Table({ rows: baris, width: { size: LEBAR_TEKS, type: D.WidthType.DXA }, columnWidths: lebar, layout: D.TableLayoutType.FIXED });
}

function blokKeDokumen(blok) {
  const anak = [];
  for (const [urut, b] of blok.entries()) {
    const sesudah = (blok[urut + 1] || {}).jenis;
    const sebelum = (blok[urut - 1] || {}).jenis;
    // kalimat pengantar tidak boleh terpisah dari gambar, kode, atau daftar yang diantarnya
    const ikatLanjut = ['gambar', 'kode'].includes(sesudah) || (/:$/.test(b.teks || '') && ['nomor', 'butir', 'kode', 'kapsiTabel'].includes(sesudah));
    if (b.jenis === 'h2') anak.push(judulTahap(b.teks, b.marka));
    else if (b.jenis === 'par') {
      const sorot = /^\*\*(Titik periksa|Perhatian|Perhatikan|Peringatan)/.test(b.teks);
      if (sorot) anak.push(paragraf(b.teks, { sebelum: 120, setelah: 180, keepLines: true, shading: { type: D.ShadingType.CLEAR, fill: LEMBUT, color: 'auto' }, border: { left: { style: D.BorderStyle.SINGLE, size: 24, color: NAVY, space: 8 } } }));
      else anak.push(paragraf(b.teks, { keepNext: ikatLanjut }));
    }
    else if (b.jenis === 'nomor') anak.push(new D.Paragraph({
      children: [new D.TextRun({ text: `${b.no}.`, font: FONT, size: 22 }), new D.TextRun({ children: [new D.Tab()], font: FONT, size: 22 }), ...sebaris(b.teks)],
      tabStops: [{ type: D.TabStopType.LEFT, position: 400 }], indent: { left: 400, hanging: 320 }, alignment: D.AlignmentType.JUSTIFIED, spacing: { after: 90, line: 276 }, keepNext: ikatLanjut,
    }));
    else if (b.jenis === 'butir') anak.push(new D.Paragraph({
      children: sebaris(b.teks), numbering: { reference: 'butir', level: b.tingkat ? 1 : 0 }, alignment: D.AlignmentType.JUSTIFIED, spacing: { after: 60, line: 276 },
    }));
    else if (b.jenis === 'kode') for (const [i, l] of b.isi.entries()) anak.push(new D.Paragraph({
      children: [new D.TextRun({ text: l || ' ', font: 'Consolas', size: 18, color: '23476B' })], alignment: D.AlignmentType.LEFT,
      shading: { type: D.ShadingType.CLEAR, fill: LEMBUT, color: 'auto' }, indent: { left: 200 }, keepLines: true, keepNext: i < b.isi.length - 1,
      spacing: { after: i === b.isi.length - 1 ? 160 : 0, before: i === 0 ? 60 : 0 },
    }));
    else if (b.jenis === 'gambar') {
      const g = siapkanGambar(b.jalur);
      anak.push(new D.Paragraph({ children: [new D.ImageRun({ type: 'jpg', data: g.data, transformation: { width: g.lebar, height: g.tinggi }, ...(g.bingkai ? { outline: { type: 'solidFill', solidFillType: 'rgb', value: GARIS, width: 9525 } } : {}) })], alignment: D.AlignmentType.CENTER, spacing: { before: 140, after: 70 }, keepNext: true }));
    }
    else if (b.jenis === 'kapsi') anak.push(caption(b, { rata: D.AlignmentType.CENTER, spacing: { after: 20 } }));
    else if (b.jenis === 'kapsiTabel') anak.push(caption(b, { rata: D.AlignmentType.LEFT, spacing: { before: 120, after: 60 } }));
    else if (b.jenis === 'sumber') anak.push(paragraf(b.teks, { ukuran: 16, warna: ABU, rata: sebelum === 'tabel' ? D.AlignmentType.LEFT : D.AlignmentType.CENTER, setelah: 200, sebelum: sebelum === 'tabel' ? 70 : 40 }));
    else if (b.jenis === 'tabel') anak.push(tabelMd(b.baris, b.rataKanan));
  }
  return anak;
}

// ---------------------------------------------------------------- header dan footer
const logo = fs.readFileSync(path.join(ASET, 'logo_ugm_warna.png'));
function barisLogo() {
  return new D.Paragraph({ children: [new D.ImageRun({ type: 'png', data: logo, transformation: { width: 126, height: 36 } })], alignment: D.AlignmentType.RIGHT, spacing: { after: 60 } });
}
const headerDepan = () => new D.Header({ children: [barisLogo()] });

function headerTab(judul) {
  const teks = judul.toUpperCase();
  const lTab = Math.min(LEBAR_TEKS + TEPI - 1800, 480 + teks.length * 118);
  const lGaris = LEBAR_TEKS + TEPI - lTab;
  return new D.Header({
    children: [barisLogo(), new D.Table({
      indent: { size: -120, type: D.WidthType.DXA },
      width: { size: lTab + lGaris, type: D.WidthType.DXA }, columnWidths: [lTab, lGaris], layout: D.TableLayoutType.FIXED,
      rows: [new D.TableRow({ children: [
        new D.TableCell({ width: { size: lTab, type: D.WidthType.DXA }, borders: semuaTanpaGaris, shading: { type: D.ShadingType.CLEAR, fill: NAVY, color: 'auto' }, margins: { top: 70, bottom: 70, left: 140, right: 100 }, verticalAlign: D.VerticalAlign.CENTER,
          children: [new D.Paragraph({ children: [new D.TextRun({ text: teks, font: FONT, size: 19, bold: true, italics: true, color: 'FFFFFF', characterSpacing: 8 })], spacing: { after: 0 } })] }),
        new D.TableCell({ width: { size: lGaris, type: D.WidthType.DXA }, borders: { top: tanpaGaris, left: tanpaGaris, right: tanpaGaris, bottom: { style: D.BorderStyle.SINGLE, size: 12, color: EMAS } }, children: [new D.Paragraph({ children: [], spacing: { after: 0 } })] }),
      ] })],
    }), new D.Paragraph({ children: [], spacing: { after: 80 } })],
  });
}

const nomorHalaman = warna => new D.TextRun({ children: [D.PageNumber.CURRENT], font: FONT, size: 20, color: warna });

function footerDepan() {
  return new D.Footer({ children: [
    new D.Paragraph({ children: [new D.TextRun({ text: HAK_CIPTA, font: FONT, size: 14, color: ABU })], alignment: D.AlignmentType.RIGHT, spacing: { after: 80 } }),
    new D.Table({
      indent: { size: -TEPI, type: D.WidthType.DXA }, width: { size: LEBAR_HAL, type: D.WidthType.DXA }, columnWidths: [LEBAR_HAL], layout: D.TableLayoutType.FIXED,
      rows: [new D.TableRow({ height: { value: 620, rule: D.HeightRule.EXACT }, children: [new D.TableCell({
        width: { size: LEBAR_HAL, type: D.WidthType.DXA }, borders: { ...semuaTanpaGaris, top: { style: D.BorderStyle.SINGLE, size: 18, color: EMAS } }, shading: { type: D.ShadingType.CLEAR, fill: NAVY, color: 'auto' }, verticalAlign: D.VerticalAlign.CENTER, margins: { right: TEPI - 300 },
        children: [new D.Paragraph({ children: [nomorHalaman('FFFFFF')], alignment: D.AlignmentType.RIGHT, spacing: { after: 0 } })],
      })] })],
    }),
  ] });
}

function footerIsi() {
  const lKanan = 1500, lKiri = LEBAR_TEKS + TEPI - lKanan;
  return new D.Footer({ children: [
    new D.Table({
      width: { size: lKiri + lKanan, type: D.WidthType.DXA }, columnWidths: [lKiri, lKanan], layout: D.TableLayoutType.FIXED,
      rows: [new D.TableRow({ children: [
        new D.TableCell({ width: { size: lKiri, type: D.WidthType.DXA }, borders: semuaTanpaGaris, verticalAlign: D.VerticalAlign.CENTER, children: [new D.Paragraph({ children: [new D.TextRun({ text: ORGANISASI, font: FONT, size: 18, bold: true, color: NAVY })], spacing: { after: 0 } })] }),
        new D.TableCell({ width: { size: lKanan, type: D.WidthType.DXA }, borders: semuaTanpaGaris, shading: { type: D.ShadingType.CLEAR, fill: NAVY, color: 'auto' }, verticalAlign: D.VerticalAlign.CENTER, children: [new D.Paragraph({ children: [nomorHalaman('FFFFFF')], alignment: D.AlignmentType.CENTER, spacing: { after: 0 } })] }),
      ] })],
    }),
    new D.Paragraph({ children: [new D.TextRun({ text: HAK_CIPTA, font: FONT, size: 14, color: ABU })], alignment: D.AlignmentType.RIGHT, spacing: { before: 80, after: 60 } }),
  ] });
}

const halaman = (ekstra = {}) => ({ page: { size: { width: LEBAR_HAL, height: TINGGI_HAL }, margin: { top: 1500, bottom: 1250, left: TEPI, right: TEPI, header: 300, footer: 0, ...ekstra.margin }, pageNumbers: { formatType: D.NumberFormat.DECIMAL_ZERO, ...ekstra.pageNumbers } } });

// ---------------------------------------------------------------- isi
// akhir baris CRLF (salinan kerja Windows) disamakan dengan LF
function bacaModul(nama) { return bacaBlok(fs.readFileSync(path.join(MODUL, nama), 'utf8').replace(/\r\n?/g, '\n')); }

function potongBagian(blok, judul) {
  const a = blok.findIndex(b => b.jenis === 'h2' && b.teks === judul);
  if (a < 0) return [];
  let z = a + 1;
  while (z < blok.length && blok[z].jenis !== 'h2' && blok[z].jenis !== 'h1') z++;
  return blok.splice(a, z - a).slice(1);
}

function sampul() {
  const band = gambarPng('band.png', NAVY), emas = gambarPng('emas.png', EMAS);
  const banner = fs.readFileSync(path.join(ASET, 'sampul_alur_bompon.png'));
  const lBanner = 744, tBanner = Math.round(744 * 5.68 / 12);
  const kolom = (a, b) => new D.TableCell({ width: { size: 4300, type: D.WidthType.DXA }, borders: semuaTanpaGaris, children: [
    new D.Paragraph({ children: [new D.TextRun({ text: a, font: FONT, size: 24, color: '222222' })], spacing: { after: 40 } }),
    new D.Paragraph({ children: [new D.TextRun({ text: b, font: FONT, size: 24, bold: true, color: NAVY })], spacing: { after: 0 } }),
  ] });
  return {
    properties: { ...halaman({ margin: { top: 2500, bottom: 500, header: 0, footer: 0 } }) },
    children: [
      new D.Paragraph({ children: [
        mengambang(band, 744, 190, 50, 933), mengambang(emas, 736, 190, 8, 933), mengambang(logo, 622, 38, 150, 43),
        mengambang(gambarPng('garis.png', NAVY), 0, 470, 736, 2), mengambang(banner, 0, 488, lBanner - 8, tBanner),
        new D.TextRun({ text: 'Modul', font: FONT, size: 104, bold: true, color: NAVY }),
      ], spacing: { after: 0, line: 240 } }),
      new D.Paragraph({ children: [new D.TextRun({ text: 'Pembelajaran', font: FONT, size: 104, bold: true, color: NAVY })], spacing: { after: 160, line: 240 } }),
      new D.Paragraph({ children: [new D.TextRun({ text: 'Praktik Remote Sensing dan Digital Soil Mapping untuk Pertanian Presisi pada Perkebunan Kelapa Sawit', font: FONT, size: 30, bold: true, color: '222222' })], spacing: { after: 20 }, indent: { right: 900 } }),
      new D.Paragraph({ children: [new D.TextRun({ text: 'Wilayah latihan: Sub-DAS Bompon dan Site Gunung Madu Plantation', font: FONT, size: 26, color: '222222' })], spacing: { after: 0 } }),
      new D.Paragraph({ children: [new D.TextRun({ text: 'Sub-DAS Bompon, dari kiri: komposit inframerah dekat, komposit SWIR, batas SMU di atas bayangan medan, dan prediksi tutupan material dari model latihan. Contains modified Copernicus Sentinel data 2024–2025.', font: FONT, size: 15, color: ABU })], spacing: { before: 6420, after: 240 }, indent: { right: 900 } }),
      new D.Table({ width: { size: 8600, type: D.WidthType.DXA }, columnWidths: [4300, 4300], layout: D.TableLayoutType.FIXED, rows: [new D.TableRow({ children: [kolom('Disusun oleh:', 'Pusat Studi Pengelolaan Sumber Daya Lahan, Universitas Gadjah Mada'), kolom('Pelatihan:', '3–5 November 2026')] })] }),
    ],
  };
}

const penanda = kunci => new D.Paragraph({ children: [new D.TextRun({ text: `@@${kunci}@@` })] });
const xmlAman = t => t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

function runDaftar(teks) {
  return teks.replace(/`/g, '').split(/(\*[^*]+\*)/).filter(Boolean).map(p => {
    const miring = p.startsWith('*');
    return `<w:r>${miring ? '<w:rPr><w:i/></w:rPr>' : ''}<w:t xml:space="preserve">${xmlAman(miring ? p.slice(1, -1) : p)}</w:t></w:r>`;
  }).join('');
}

// satu medan TOC yang membentang beberapa paragraf, persis seperti yang ditulis Word sendiri
function medanDaftar(instruksi, entri, gayaEntri, nomor) {
  const baris = entri.map((e, i) => {
    const awal = i === 0 ? `<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> ${xmlAman(instruksi)} </w:instrText></w:r><w:r><w:fldChar w:fldCharType="separate"/></w:r>` : '';
    const halaman = `<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> PAGEREF ${e.marka} \\h </w:instrText></w:r><w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>${String(nomor[e.marka] ?? 0).padStart(2, '0')}</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r>`;
    return `<w:p><w:pPr><w:pStyle w:val="${gayaEntri(e)}"/></w:pPr>${awal}<w:hyperlink w:anchor="${e.marka}" w:history="1">${runDaftar(e.teks)}<w:r><w:tab/></w:r>${halaman}</w:hyperlink></w:p>`;
  });
  return baris.join('') + '<w:p><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>';
}

const gayaTambahan = [
  ['TOC1', 'toc 1', `<w:shd w:val="clear" w:color="auto" w:fill="${SOROT}"/><w:tabs><w:tab w:val="right" w:leader="dot" w:pos="${LEBAR_TEKS}"/></w:tabs><w:spacing w:before="70" w:after="40"/>`, `<w:b/><w:color w:val="${NAVY}"/><w:sz w:val="21"/>`],
  ['TOC2', 'toc 2', `<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="${LEBAR_TEKS}"/></w:tabs><w:spacing w:after="30"/><w:ind w:left="200"/>`, '<w:sz w:val="20"/>'],
  ['TableofFigures', 'table of figures', `<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="${LEBAR_TEKS}"/></w:tabs><w:spacing w:after="40"/><w:ind w:left="1050" w:right="500" w:hanging="1050"/>`, '<w:sz w:val="20"/>'],
].map(([id, nama, pPr, rPr]) => `<w:style w:type="paragraph" w:styleId="${id}"><w:name w:val="${nama}"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="39"/><w:unhideWhenUsed/><w:pPr>${pPr}</w:pPr><w:rPr>${rPr}</w:rPr></w:style>`).join('');

async function pasangDaftar(buffer, hasil, nomor) {
  const zip = await JSZip.loadAsync(buffer);
  let isi = await zip.file('word/document.xml').async('string');
  const pasang = (kunci, xml) => {
    const pola = new RegExp(`<w:p>(?:(?!</w:p>).)*?@@${kunci}@@(?:(?!</w:p>).)*?</w:p>`, 's');
    if (!pola.test(isi)) throw new Error('Penanda tidak ditemukan: ' + kunci);
    isi = isi.replace(pola, () => xml);
  };
  pasang('ISI', medanDaftar('TOC \\o "1-2" \\h \\z \\u', hasil.entri, e => (e.tingkat === 0 ? 'TOC1' : 'TOC2'), nomor));
  pasang('TABEL', medanDaftar('TOC \\h \\z \\c "Tabel"', hasil.daftarTabel, () => 'TableofFigures', nomor));
  pasang('GAMBAR', medanDaftar('TOC \\h \\z \\c "Gambar"', hasil.daftarGambar, () => 'TableofFigures', nomor));
  zip.file('word/document.xml', isi);
  const gaya = await zip.file('word/styles.xml').async('string');
  // gaya TOC bawaan pustaka diganti, agar tidak ada dua gaya dengan id yang sama
  const bersih = gaya.replace(/<w:style [^>]*w:styleId="TOC[12]"[^>]*>.*?<\/w:style>/gs, '');
  zip.file('word/styles.xml', bersih.replace('</w:styles>', gayaTambahan + '</w:styles>'));
  return zip.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE' });
}

function bangun(nomor) {
  const pengantar = bacaModul('Pengantar_dan_Penutup.md');
  const iPenutup = pengantar.findIndex(b => b.jenis === 'h1' && b.teks === 'Penutup');
  const blokPengantar = pengantar.slice(1, iPenutup), blokPenutup = pengantar.slice(iPenutup + 1);
  const pustaka = bacaModul('Daftar_Pustaka_Praktik.md').slice(1);
  const modul = ['Modul_Praktik_0_Persiapan.md', 'Modul_Praktik_1_Multi_Source_Data_Fusion.md', 'Modul_Praktik_2_Delineasi_SMU.md', 'Modul_Praktik_3_Proximal_Soil_Sensing.md', 'Modul_Praktik_4_Bare_Soil_Detection.md', 'Modul_Praktik_5_Machine_Learning_DSM.md'].map(bacaModul);

  const entri = [{ teks: 'Kata Pengantar', tingkat: 0, marka: 'hal_pengantar' }, { teks: 'Daftar Isi', tingkat: 0, marka: 'hal_isi' }, { teks: 'Daftar Tabel', tingkat: 0, marka: 'hal_tabel' }, { teks: 'Daftar Gambar', tingkat: 0, marka: 'hal_gambar' }];
  const daftarTabel = [], daftarGambar = [];
  let no = 0, noTabel = 0, noGambar = 0;
  const bagian = modul.map((blok, m) => {
    const judul = blok.find(b => b.jenis === 'h1').teks;
    const marka = `hal_modul_${m}`;
    entri.push({ teks: judul, tingkat: 0, marka });
    potongBagian(blok, 'Rujukan Tambahan');
    const kurikulum = potongBagian(blok, 'Kurikulum Pembelajaran');
    for (const b of blok) if (b.jenis === 'h2' && /^((Tahap|Bagian) \d|Memasang )/.test(b.teks)) {
      b.marka = `hal_${no++}`;
      entri.push({ teks: b.teks, tingkat: 1, marka: b.marka });
    }
    // SEQ dimulai lagi dari 1 pada setiap praktik, karena nomornya P1.1, P1.2, dan seterusnya
    let pertamaTabel = true, pertamaGambar = true;
    for (const b of blok) {
      if (b.jenis === 'kapsiTabel') { b.marka = `hal_tb_${noTabel++}`; b.ulang = pertamaTabel; pertamaTabel = false; daftarTabel.push({ teks: b.teks, marka: b.marka }); }
      if (b.jenis === 'kapsi') { b.marka = `hal_gb_${noGambar++}`; b.ulang = pertamaGambar; pertamaGambar = false; daftarGambar.push({ teks: b.teks, marka: b.marka }); }
    }
    const label = blok.filter(b => b.jenis === 'par').slice(0, 2);
    return { judul, marka, blok, kurikulum, label, m };
  });
  entri.push({ teks: 'Penutup', tingkat: 0, marka: 'hal_penutup' }, { teks: 'Daftar Pustaka', tingkat: 0, marka: 'hal_pustaka' });

  const sections = [sampul()];
  sections.push({
    properties: { ...halaman({ pageNumbers: { start: 1, formatType: D.NumberFormat.DECIMAL_ZERO } }), type: D.SectionType.NEXT_PAGE },
    headers: { default: headerDepan() }, footers: { default: footerDepan() },
    children: [...judulBesar('Kata Pengantar', 'hal_pengantar'), ...blokKeDokumen(blokPengantar.filter(b => !/^(Yogyakarta|Pusat Studi)/.test(b.teks || ''))),
      ...blokPengantar.filter(b => /^(Yogyakarta|Pusat Studi)/.test(b.teks || '')).map(b => paragraf(b.teks, { rata: D.AlignmentType.RIGHT, sebelum: 240 })),
      new D.Paragraph({ children: [new D.PageBreak()] }), ...judulBesar('Daftar Isi', 'hal_isi'), penanda('ISI'),
      new D.Paragraph({ children: [new D.PageBreak()] }), ...judulBesar('Daftar Tabel', 'hal_tabel'), penanda('TABEL'),
      new D.Paragraph({ children: [new D.PageBreak()] }), ...judulBesar('Daftar Gambar', 'hal_gambar'), penanda('GAMBAR'), new D.Paragraph({ children: [] })],
  });
  for (const b of bagian) {
    if (b.m === 0) {
      const isi = b.blok.filter(x => x.jenis !== 'h1');
      sections.push({ properties: { ...halaman({ margin: { top: 1750, bottom: 1100 } }), type: D.SectionType.NEXT_PAGE }, headers: { default: headerTab(b.judul) }, footers: { default: footerIsi() }, children: [...judulBesar(b.judul, b.marka), ...blokKeDokumen(isi)] });
      continue;
    }
    const label = b.blok.filter(x => x.jenis === 'par').slice(0, 2);
    const isi = b.blok.filter(x => x.jenis !== 'h1' && !label.includes(x));
    sections.push({
      properties: { ...halaman(), type: D.SectionType.NEXT_PAGE }, headers: { default: headerDepan() }, footers: { default: footerDepan() },
      children: [
        new D.Paragraph({ style: 'JudulKurikulum', children: [new D.TextRun({ text: 'Kurikulum Pembelajaran' })] }),
        new D.Paragraph({ style: 'JudulPraktik', children: [new D.Bookmark({ id: b.marka, children: [new D.TextRun({ text: b.judul })] })], border: { bottom: { style: D.BorderStyle.SINGLE, size: 18, color: EMAS, space: 6 } } }),
        paragraf(label[1] ? label[1].teks : '', { ukuran: 19, warna: ABU, rata: D.AlignmentType.LEFT, setelah: 140 }),
        ...blokKeDokumen(b.kurikulum),
      ],
    });
    sections.push({ properties: { ...halaman({ margin: { top: 1750, bottom: 1100 } }), type: D.SectionType.NEXT_PAGE }, headers: { default: headerTab(b.judul) }, footers: { default: footerIsi() }, children: blokKeDokumen(isi) });
  }
  sections.push({
    properties: { ...halaman(), type: D.SectionType.NEXT_PAGE }, headers: { default: headerDepan() }, footers: { default: footerDepan() },
    children: [...judulBesar('Penutup', 'hal_penutup'), ...blokKeDokumen(blokPenutup), new D.Paragraph({ children: [new D.PageBreak()] }), ...judulBesar('Daftar Pustaka', 'hal_pustaka'),
      ...pustaka.map(x => new D.Paragraph({ children: sebaris(x.teks, { ukuran: 20 }), indent: { left: 400, hanging: 400 }, spacing: { after: 70, line: 250 }, alignment: D.AlignmentType.LEFT }))],
  });

  const doc = new D.Document({
    title: 'Modul Praktik Remote Sensing dan Digital Soil Mapping', creator: 'PS2DL Universitas Gadjah Mada', description: 'Modul praktik pelatihan 3–5 November 2026',
    features: { updateFields: true },
    styles: {
      default: {
        document: { run: { font: FONT, size: 22 } },
        heading1: { run: { font: FONT, size: 60, bold: true, color: NAVY }, paragraph: { spacing: { before: 200, after: 80 }, keepNext: true, outlineLevel: 0 } },
        heading2: { run: { font: FONT, size: 32, bold: true, italics: true, underline: { type: D.UnderlineType.SINGLE }, color: NAVY }, paragraph: { spacing: { before: 260, after: 120 }, keepNext: true, outlineLevel: 1 } },
      },
      paragraphStyles: [
        { id: 'JudulKurikulum', name: 'Judul Kurikulum', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: 60, bold: true, color: NAVY }, paragraph: { spacing: { before: 200, after: 0 }, keepNext: true } },
        // tingkat kerangka 1: judul praktik masuk daftar isi seperti Heading 1
        { id: 'JudulPraktik', name: 'Judul Praktik', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: 24, bold: true, color: '222222' }, paragraph: { spacing: { after: 120 }, keepNext: true, outlineLevel: 0 } },
        // tingkat kerangka 3: tampil di panel navigasi Word, tetapi di luar jangkauan daftar isi
        { id: 'Subjudul', name: 'Subjudul', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: 32, bold: true, italics: true, underline: { type: D.UnderlineType.SINGLE }, color: NAVY }, paragraph: { spacing: { before: 260, after: 120 }, keepNext: true, outlineLevel: 2 } },
        { id: 'Caption', name: 'caption', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: 19, bold: true, color: NAVY }, paragraph: { spacing: { after: 20 }, keepNext: true } },
      ],
    },
    numbering: { config: [{ reference: 'butir', levels: [
      { level: 0, format: D.LevelFormat.BULLET, text: '•', alignment: D.AlignmentType.LEFT, style: { paragraph: { indent: { left: 400, hanging: 240 } } } },
      { level: 1, format: D.LevelFormat.BULLET, text: '•', alignment: D.AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 240 } } } },
    ] }] },
    sections,
  });
  return { doc, entri, daftarTabel, daftarGambar };
}

function halamanJudul(pdf, hasil) {
  const rapi = t => t.replace(/ﬁ/g, 'fi').replace(/ﬂ/g, 'fl').replace(/\s+/g, ' ').trim().toLowerCase();
  const teksHal = teksPerHalaman(pdf).map(rapi);
  const jumlah = teksHal.length;
  // halaman fisik 1 sampul; nomor tercetak = indeks 0-based pada teksHal
  const awal = judul => { const i = teksHal.findIndex(t => t.startsWith(judul)); if (i < 0) throw new Error('Halaman tidak ditemukan: ' + judul); return i; };
  const nomor = { hal_pengantar: awal('kata pengantar'), hal_isi: awal('daftar isi'), hal_tabel: awal('daftar tabel'), hal_gambar: awal('daftar gambar') };
  const mulai = teksHal.findIndex((t, i) => i > nomor.hal_gambar && t.includes('persiapan praktik') && t.includes('lima praktik'));
  if (mulai < 0) throw new Error('Halaman awal Persiapan tidak ditemukan pada PDF');
  const telusuri = daftar => {
    let p = mulai;
    for (const e of daftar) {
      if (!e.marka || nomor[e.marka] !== undefined) continue;
      const polos = e.teks.replace(/[*`]/g, '');
      const dari = p;
      const cari = rapi(polos);
      while (p < jumlah && !teksHal[p].includes(cari)) p++;
      if (p >= jumlah) {
        const tanpaNomor = rapi(polos.replace(/^(Gambar|Tabel) P\d+\.\d+ /, ''));
        p = dari;
        while (p < jumlah && !teksHal[p].includes(tanpaNomor)) p++;
      }
      if (p >= jumlah) throw new Error('Judul tidak ditemukan pada PDF: ' + e.teks);
      nomor[e.marka] = p;
    }
  };
  telusuri(hasil.entri);
  telusuri(hasil.daftarTabel);
  telusuri(hasil.daftarGambar);
  return { nomor, jumlah };
}

async function main() {
  const uji = path.join(KERJA, 'uji.docx');
  let hasil = bangun({});
  fs.writeFileSync(uji, await pasangDaftar(await D.Packer.toBuffer(hasil.doc), hasil, {}));
  keePdf(uji, KERJA);
  const { nomor, jumlah } = halamanJudul(path.join(KERJA, 'uji.pdf'), hasil);
  hasil = bangun(nomor);
  fs.writeFileSync(KELUAR, await pasangDaftar(await D.Packer.toBuffer(hasil.doc), hasil, nomor));
  console.log('Ditulis', path.basename(KELUAR), jumlah, 'halaman,', hasil.entri.length, 'entri daftar isi,', hasil.daftarTabel.length, 'tabel,', hasil.daftarGambar.length, 'gambar');
}

main().catch(e => { console.error(e); process.exit(1); });
