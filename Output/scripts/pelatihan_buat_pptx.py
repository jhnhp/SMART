#!/usr/bin/env python3
"""Membuat PPTX dari naskah Output/Presentasi/PPT_*.md memakai template resmi UGM Opt-1 (Wide Size).

Slide sampul, pemisah, isi, dan penutup diambil dari keempat slide contoh di dalam template.
Sintaks naskah ada pada berkas .md: "## Judul", lalu "Tata letak: ...", butir "- ", gambar, tabel,
"Rumus:", "Sumber:", "Catatan:".

Jalankan: python3 Output/scripts/pelatihan_buat_pptx.py [nomor_deck ...]
"""
import copy
import glob
import os
import re
import shutil
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEMPLATE = os.path.join(AKAR, 'Source', '(NEW) Template Presentasi UGM Opt-1 (Wide Size)_2026.pptx')
FOLDER = os.path.join(AKAR, 'Output', 'Presentasi')
GAMBAR = os.path.join(FOLDER, 'gambar')
ASET = os.path.join(AKAR, 'Output', 'assets')
BIRU = RGBColor(0x01, 0x41, 0x6B)
ABU = RGBColor(0x55, 0x55, 0x55)
HITAM = RGBColor(0x22, 0x22, 0x22)
FONT_BOLD = 'Gama-Sans-Bold'
FONT = 'Gama-Sans-Regular'
# area isi pada layout "Title and Content": di bawah judul, di atas pita bawah template
KIRI, KANAN = 500000, 11700000
ATAS, BAWAH = 1190000, 6130000
TINGGI_SUMBER = 270000


def baca_naskah(jalur):
    dek = {'slide': []}
    sl = None
    tabel = None
    for baris in open(jalur, encoding='utf-8').read().split('\n'):
        b = baris.rstrip()
        if b.startswith('# '):
            dek['judul'] = b[2:]
        elif b.startswith('## '):
            sl = {'judul': b[3:], 'tata': 'teks', 'butir': [], 'gambar': [], 'tabel': None, 'rumus': None, 'sumber': None, 'catatan': None, 'keterangan': None}
            dek['slide'].append(sl)
            tabel = None
        elif sl is None:
            m = re.match(r'(Subjudul|Pemateri|Sesi|Acuan): (.*)', b)
            if m:
                dek[m.group(1).lower()] = m.group(2)
        elif b.startswith('Tata letak: '):
            sl['tata'] = b[12:].strip()
        elif b.startswith('Keterangan: '):
            sl['keterangan'] = b[12:]
        elif b.startswith('- '):
            sl['butir'].append(b[2:])
        elif b.startswith('!['):
            m = re.match(r'!\[(.*)\]\((.*)\)', b)
            sl['gambar'].append((m.group(1), os.path.join(FOLDER, m.group(2))))
        elif b.startswith('Rumus: '):
            sl['rumus'] = b[7:]
        elif b.startswith('Sumber: '):
            sl['sumber'] = b[8:]
        elif b.startswith('Catatan: '):
            sl['catatan'] = b[9:]
        elif b.startswith('|'):
            sel = [c.strip() for c in b.strip('|').split('|')]
            if set(''.join(sel)) <= set('-: '):
                continue
            if sl['tabel'] is None:
                sl['tabel'] = []
            sl['tabel'].append(sel)
    return dek


def siapkan_gambar(dek):
    """Menyalin gambar yang dipakai dari Output/assets ke satu folder Presentasi/gambar."""
    os.makedirs(GAMBAR, exist_ok=True)
    for sl in dek['slide']:
        for _, jalur in sl['gambar']:
            nama = os.path.basename(jalur)
            m = re.match(r'M(\d)-', nama)
            sumber = os.path.join(ASET, f'modul-{m.group(1)}', nama)
            if not os.path.exists(sumber):
                raise FileNotFoundError(sumber)
            shutil.copy2(sumber, jalur)


def buat_rumus(rumus, nama):
    fig = plt.figure(figsize=(6, 1), dpi=300)
    t = fig.text(0.5, 0.5, rumus, fontsize=22, ha='center', va='center', color='#01416B')
    fig.canvas.draw()
    k = t.get_window_extent().expanded(1.04, 1.25).transformed(fig.dpi_scale_trans.inverted())
    jalur = os.path.join(GAMBAR, nama)
    fig.savefig(jalur, bbox_inches=k, transparent=True)
    plt.close(fig)
    return jalur


def salin_slide(prs, sumber):
    """Menggandakan slide template beserta gambar dan hubungan berkasnya."""
    baru = prs.slides.add_slide(sumber.slide_layout)
    for s in list(baru.shapes):
        s._element.getparent().remove(s._element)
    latar = sumber._element.find(qn('p:cSld')).find(qn('p:bg'))
    if latar is not None:
        baru._element.find(qn('p:cSld')).insert(0, copy.deepcopy(latar))
    peta = {}
    for rid, rel in sumber.part.rels.items():
        if rel.reltype.endswith('/slideLayout') or rel.reltype.endswith('/notesSlide'):
            continue
        peta[rid] = baru.part.relate_to(rel._target, rel.reltype) if not rel.is_external else baru.part.relate_to(rel._target, rel.reltype, is_external=True)
    for el in sumber.shapes._spTree:
        if el.tag.endswith('}nvGrpSpPr') or el.tag.endswith('}grpSpPr'):
            continue
        klon = copy.deepcopy(el)
        for sub in klon.iter():
            for attr, nilai in list(sub.attrib.items()):
                if attr.startswith('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}') and nilai in peta:
                    sub.set(attr, peta[nilai])
        baru.shapes._spTree.append(klon)
    return baru


def isi_kotak(kotak, baris, ukuran=None, warna=None, tebal=None):
    """Mengganti teks kotak dengan mempertahankan format run pertama pada paragraf pertama."""
    tf = kotak.text_frame
    p0 = tf.paragraphs[0]
    r0 = copy.deepcopy(p0.runs[0]._r) if p0.runs else None
    pPr0 = copy.deepcopy(p0._p.pPr) if p0._p.pPr is not None else None
    for p in list(tf.paragraphs)[1:]:
        p._p.getparent().remove(p._p)
    for el in list(p0._p):
        p0._p.remove(el)
    for i, teks in enumerate(baris):
        p = p0 if i == 0 else tf.add_paragraph()
        if pPr0 is not None:
            if p._p.pPr is not None:
                p._p.remove(p._p.pPr)
            p._p.insert(0, copy.deepcopy(pPr0))
        r = copy.deepcopy(r0)
        r.find(qn('a:t')).text = teks
        p._p.append(r)
        run = p.runs[0]
        if ukuran:
            run.font.size = Pt(ukuran)
        if warna is not None:
            run.font.color.rgb = warna
        if tebal is not None:
            run.font.bold = tebal


def tulis_kaya(p, teks, ukuran, warna=HITAM, font=FONT):
    """Menulis **tebal** dan *miring* sebagai run terpisah."""
    for bagian in re.split(r'(\*\*[^*]+\*\*|\*[^*]+\*)', teks):
        if not bagian:
            continue
        r = p.add_run()
        if bagian.startswith('**'):
            r.text, r.font.bold = bagian[2:-2], True
            r.font.name = FONT_BOLD
            r.font.color.rgb = BIRU
        elif bagian.startswith('*'):
            r.text, r.font.italic = bagian[1:-1], True
            r.font.name = font
            r.font.color.rgb = warna
        else:
            r.text = bagian
            r.font.name = font
            r.font.color.rgb = warna
        r.font.size = Pt(ukuran)


def atur_judul(sl, teks):
    j = sl.shapes.title
    j.left, j.top, j.width, j.height = Emu(KIRI), Emu(230000), Emu(9700000), Emu(900000)
    tf = j.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    for r in list(p.runs):
        r._r.getparent().remove(r._r)
    r = p.add_run()
    r.text = teks
    r.font.size = Pt(26 if len(teks) <= 62 else 23)
    r.font.bold = True
    r.font.name = FONT_BOLD
    r.font.color.rgb = BIRU


def tambah_butir(kotak, butir, ukuran):
    tf = kotak.text_frame
    tf.clear()
    tf.word_wrap = True
    for i, t in enumerate(butir):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(9)
        pPr = p._p.get_or_add_pPr()
        pPr.set('marL', '228600')
        pPr.set('indent', '-228600')
        for tag in ('a:buNone', 'a:buChar', 'a:buAutoNum'):
            for e in pPr.findall(qn(tag)):
                pPr.remove(e)
        warna = pPr.makeelement(qn('a:buClr'), {})
        warna.append(warna.makeelement(qn('a:srgbClr'), {'val': 'F2B705'}))
        pPr.append(warna)
        pPr.append(pPr.makeelement(qn('a:buFont'), {'typeface': 'Arial'}))
        pPr.append(pPr.makeelement(qn('a:buChar'), {'char': '•'}))
        tulis_kaya(p, t, ukuran)


def ukuran_teks(butir, lebar_emu, tinggi_emu, maks=22, mins=14):
    """Memilih ukuran huruf terbesar yang muat dengan perkiraan lebar karakter."""
    for u in range(maks, mins - 1, -1):
        cpl = lebar_emu / (u * 12700 * 0.56)
        baris = sum(max(1, -(-len(re.sub(r'\*', '', t)) // int(cpl))) for t in butir)
        tinggi = baris * u * 12700 * 1.24 + len(butir) * 9 * 12700
        if tinggi <= tinggi_emu:
            return u
    return mins


def pasang_gambar(sl, jalur, x, y, w, h):
    lebar, tinggi = Image.open(jalur).size
    sk = min(w / lebar, h / tinggi)
    gw, gh = int(lebar * sk), int(tinggi * sk)
    return sl.shapes.add_picture(jalur, Emu(int(x + (w - gw) / 2)), Emu(int(y + (h - gh) / 2)), Emu(gw), Emu(gh))


def teks_kecil(sl, x, y, w, h, teks, ukuran=11, warna=ABU, miring=False, rata=PP_ALIGN.LEFT, jangkar=MSO_ANCHOR.TOP):
    k = sl.shapes.add_textbox(Emu(x), Emu(y), Emu(w), Emu(h))
    tf = k.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = jangkar
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = rata
    tulis_kaya(p, teks, ukuran, warna)
    if miring:
        for r in p.runs:
            r.font.italic = True
    return k


def garis_sel(sel, warna='C9D3DC'):
    """Hanya garis bawah tipis; garis lain dimatikan agar tampilan sama di PowerPoint dan LibreOffice."""
    tcPr = sel._tc.get_or_add_tcPr()
    for i, tag in enumerate(('a:lnL', 'a:lnR', 'a:lnT', 'a:lnB')):
        ln = tcPr.makeelement(qn(tag), {'w': '9525' if tag == 'a:lnB' else '0', 'cap': 'flat', 'cmpd': 'sng', 'algn': 'ctr'})
        if tag == 'a:lnB':
            isi = ln.makeelement(qn('a:solidFill'), {})
            isi.append(isi.makeelement(qn('a:srgbClr'), {'val': warna}))
            ln.append(isi)
        else:
            ln.append(ln.makeelement(qn('a:noFill'), {}))
        tcPr.insert(i, ln)


def pasang_tabel(sl, tabel, x, y, w, h):
    nb, nk = len(tabel), len(tabel[0])
    polos = [[re.sub(r'\*', '', c) for c in b] for b in tabel]
    panjang = [max(len(polos[i][j]) for i in range(nb)) for j in range(nk)]
    kata = [max(len(k) for i in range(nb) for k in polos[i][j].split() or ['']) for j in range(nk)]
    bobot = [max(kata[j] * 1.75, panjang[j] * 0.62, 6) for j in range(nk)]
    lebar = [w * b / sum(bobot) for b in bobot]
    # ukuran huruf terbesar yang muat
    for ukuran in range(20, 10, -1):
        t_baris = []
        for i in range(nb):
            m = max(-(-len(polos[i][j]) // max(int((lebar[j] - 150000) / (ukuran * 12700 * 0.56)), 1)) for j in range(nk))
            t_baris.append(max(m, 1) * ukuran * 12700 * 1.26 + 100000)
        if sum(t_baris) <= h:
            break
    faktor = min(1.22, h / sum(t_baris))
    gr = sl.shapes.add_table(nb, nk, Emu(x), Emu(y), Emu(w), Emu(int(sum(t_baris) * faktor)))
    t = gr.table
    tblPr = t._tbl.tblPr
    for e in tblPr.findall(qn('a:tableStyleId')):
        tblPr.remove(e)
    tblPr.set('bandRow', '0')
    tblPr.set('firstRow', '0')
    for j in range(nk):
        t.columns[j].width = Emu(int(lebar[j]))
    for i in range(nb):
        t.rows[i].height = Emu(int(t_baris[i] * faktor))
        for j in range(nk):
            c = t.cell(i, j)
            c.margin_left = c.margin_right = Emu(75000)
            c.margin_top = c.margin_bottom = Emu(40000)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = c.text_frame.paragraphs[0]
            if i == 0:
                r = p.add_run()
                r.text = polos[i][j]
                r.font.bold = True
                r.font.size = Pt(ukuran)
                r.font.name = FONT_BOLD
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                c.fill.solid()
                c.fill.fore_color.rgb = BIRU
            else:
                tulis_kaya(p, tabel[i][j], ukuran)
                c.fill.solid()
                c.fill.fore_color.rgb = RGBColor(0xF3, 0xF6, 0xF9) if i % 2 == 0 else RGBColor(0xFF, 0xFF, 0xFF)
            garis_sel(c)
    return gr


def perbaiki_ugm(sl):
    """Kotak 'ugm.ac.id' dilebarkan agar tidak membungkus ketika font pengganti lebih lebar."""
    for s in sl.shapes:
        if s.has_text_frame and s.text_frame.text.strip() == 'ugm.ac.id':
            s.text_frame.word_wrap = False
            s.width = Emu(min(s.width + 420000, 12192000 - s.left))
            if s.left + s.width > 12100000:
                s.left = Emu(12100000 - s.width)


def isi_slide(prs, tpl, sl_data, nomor, id_rumus):
    tata = sl_data['tata']
    if tata == 'pemisah':
        s = salin_slide(prs, tpl['pemisah'])
        kotak = [x for x in s.shapes if x.has_text_frame]
        utama = [x for x in kotak if 'Halaman' in x.text_frame.text][0]
        ket = [x for x in kotak if 'area penjelasan' in x.text_frame.text][0]
        isi_kotak(utama, [sl_data['judul']], ukuran=34)
        utama.left, utama.top, utama.width, utama.height = Emu(2892475), Emu(2250000), Emu(8300000), Emu(1450000)
        utama.text_frame.word_wrap = True
        utama.text_frame.vertical_anchor = MSO_ANCHOR.BOTTOM
        isi_kotak(ket, [sl_data['keterangan'] or ''], ukuran=18)
        ket.left, ket.top, ket.width, ket.height = Emu(2892475), Emu(3850000), Emu(8000000), Emu(700000)
        perbaiki_ugm(s)
        return s
    s = prs.slides.add_slide(tpl['isi'].slide_layout)
    atur_judul(s, sl_data['judul'])
    tubuh = s.placeholders[1]
    bawah_isi = BAWAH - (TINGGI_SUMBER if sl_data['sumber'] else 0)
    panjang_sumber = len(sl_data['sumber'] or '')
    if panjang_sumber > 125:
        bawah_isi -= 170000
    if tata in ('teks', 'gambar-kanan'):
        y = ATAS
        if tata == 'gambar-kanan':
            lb_g, tg_g = Image.open(sl_data['gambar'][0][1]).size
            rasio = lb_g / tg_g
            lebar_teks = 3950000 if rasio >= 1.6 else (4500000 if rasio >= 1.1 else 5300000)
            x_g = KIRI + lebar_teks + 150000
            w_g = KANAN - x_g
            h_cap = 420000
            pasang_gambar(s, sl_data['gambar'][0][1], x_g, ATAS, w_g, bawah_isi - ATAS - h_cap)
            teks_kecil(s, x_g, bawah_isi - h_cap + 30000, w_g, h_cap, sl_data['gambar'][0][0], ukuran=12, warna=BIRU, rata=PP_ALIGN.CENTER)
        else:
            lebar_teks = KANAN - KIRI
        y_rumus = None
        if sl_data['rumus']:
            id_rumus[0] += 1
            r = buat_rumus(sl_data['rumus'], f"rumus_{id_rumus[1]}_{id_rumus[0]}.png")
            lb, tg = Image.open(r).size
            h_r = 620000 if tata == 'teks' else 520000
            w_r = int(lb / tg * h_r)
            if w_r > lebar_teks:
                w_r, h_r = lebar_teks, int(tg / lb * lebar_teks)
            if tata == 'teks' and sl_data['butir'] and sl_data['judul'].startswith('Fungsi'):
                s.shapes.add_picture(r, Emu(int(KIRI + (lebar_teks - w_r) / 2)), Emu(ATAS), Emu(w_r), Emu(h_r))
                y = ATAS + h_r + 150000
            else:
                y_rumus = (r, w_r, h_r)
        h_teks = bawah_isi - y - (y_rumus[2] + 120000 if y_rumus else 0)
        tubuh.left, tubuh.top, tubuh.width, tubuh.height = Emu(KIRI), Emu(y), Emu(lebar_teks), Emu(h_teks)
        u = ukuran_teks(sl_data['butir'], lebar_teks - 400000, h_teks - 150000, maks=24 if tata == 'teks' else 20)
        tambah_butir(tubuh, sl_data['butir'], u)
        if y_rumus:
            r, w_r, h_r = y_rumus
            s.shapes.add_picture(r, Emu(int(KIRI + (lebar_teks - w_r) / 2)), Emu(bawah_isi - h_r - 40000), Emu(w_r), Emu(h_r))
    else:
        tubuh._element.getparent().remove(tubuh._element)
        if tata == 'tabel':
            pasang_tabel(s, sl_data['tabel'], KIRI, ATAS + 30000, KANAN - KIRI, bawah_isi - ATAS - 60000)
        elif tata == 'gambar-penuh':
            h_cap = 330000
            pasang_gambar(s, sl_data['gambar'][0][1], KIRI, ATAS, KANAN - KIRI, bawah_isi - ATAS - h_cap)
            teks_kecil(s, KIRI, bawah_isi - h_cap + 40000, KANAN - KIRI, h_cap, sl_data['gambar'][0][0], ukuran=13, warna=BIRU, rata=PP_ALIGN.CENTER)
        elif tata == 'kisi':
            w_sel = (KANAN - KIRI - 300000) // 2
            h_sel = (bawah_isi - ATAS - 120000) // 2
            for i, (cap, jl) in enumerate(sl_data['gambar']):
                x = KIRI + (i % 2) * (w_sel + 300000)
                y = ATAS + (i // 2) * (h_sel + 120000)
                pasang_gambar(s, jl, x, y, w_sel, h_sel - 330000)
                teks_kecil(s, x, y + h_sel - 310000, w_sel, 300000, cap, ukuran=14, warna=BIRU, rata=PP_ALIGN.CENTER)
    if sl_data['sumber']:
        tinggi = TINGGI_SUMBER + (170000 if panjang_sumber > 125 else 0)
        teks_kecil(s, KIRI, BAWAH - tinggi + 50000, KANAN - KIRI, tinggi, 'Sumber: ' + sl_data['sumber'], ukuran=10.5, jangkar=MSO_ANCHOR.BOTTOM)
    teks_kecil(s, 11150000, 6535000, 700000, 230000, str(nomor), ukuran=12, warna=BIRU, rata=PP_ALIGN.RIGHT)
    return s


def buat_deck(jalur):
    dek = baca_naskah(jalur)
    siapkan_gambar(dek)
    prs = Presentation(TEMPLATE)
    contoh = list(prs.slides)
    tpl = {'sampul': contoh[0], 'pemisah': contoh[1], 'isi': contoh[2], 'penutup': contoh[3]}
    # lapisan bawaan: kotak ugm.ac.id jangan membungkus
    perbaiki_ugm(tpl['isi'].slide_layout)
    # sampul
    s = salin_slide(prs, tpl['sampul'])
    perbaiki_ugm(s)
    kotak = [x for x in s.shapes if x.has_text_frame]
    jd = [x for x in kotak if 'Judul Presentasi' in x.text_frame.text][0]
    sub = [x for x in kotak if 'sub-judul' in x.text_frame.text][0]
    n = len(dek['judul'])
    isi_kotak(jd, [dek['judul']], ukuran=34 if n <= 45 else 30)
    jd.left, jd.top, jd.width, jd.height = Emu(504768), Emu(1500000), Emu(5950000), Emu(2420000)
    jd.text_frame.word_wrap = True
    jd.text_frame.vertical_anchor = MSO_ANCHOR.BOTTOM
    isi_kotak(sub, [dek['subjudul'], dek['pemateri'], dek['sesi']], ukuran=14)
    sub.left, sub.top, sub.width, sub.height = Emu(508635), Emu(4180000), Emu(6000000), Emu(1250000)
    sub.text_frame.word_wrap = True
    if sub.text_frame.paragraphs[1].runs:
        sub.text_frame.paragraphs[1].runs[0].font.bold = True
    for i, data in enumerate(dek['slide'], start=2):
        s = isi_slide(prs, tpl, data, i, [0, os.path.basename(jalur)[4:5] + f'_{i}'])
        if data['catatan']:
            s.notes_slide.notes_text_frame.text = data['catatan']
    # penutup
    s = salin_slide(prs, tpl['penutup'])
    perbaiki_ugm(s)
    utama = [x for x in s.shapes if x.has_text_frame and 'kutipan' in x.text_frame.text][0]
    isi_kotak(utama, ['Terima kasih'], ukuran=40)
    # hapus empat slide contoh template
    daftar = prs.slides._sldIdLst
    for sid in list(daftar)[:4]:
        prs.part.drop_rel(sid.rId)
        daftar.remove(sid)
    # metadata template diganti dengan identitas sesi ini
    prs.core_properties.title = dek['judul']
    prs.core_properties.author = dek['pemateri']
    prs.core_properties.last_modified_by = dek['pemateri']
    prs.core_properties.subject = 'Pelatihan Pemanfaatan Remote Sensing dan Digital Soil Mapping untuk Pertanian Presisi pada Perkebunan Kelapa Sawit'
    keluar = jalur[:-3] + '.pptx'
    prs.save(keluar)
    print(os.path.basename(keluar), len(prs.slides), 'slide')


def rapikan_gambar():
    """Membuang gambar di folder gambar/ yang tidak dipakai naskah mana pun."""
    dipakai = set()
    for jalur in glob.glob(os.path.join(FOLDER, 'PPT_*.md')):
        no = os.path.basename(jalur)[4]
        for i, sl in enumerate(baca_naskah(jalur)['slide'], start=2):
            dipakai |= {os.path.basename(g) for _, g in sl['gambar']}
            if sl['rumus']:
                dipakai.add(f'rumus_{no}_{i}_1.png')
    for nama in os.listdir(GAMBAR):
        if nama not in dipakai:
            os.remove(os.path.join(GAMBAR, nama))


if __name__ == '__main__':
    pilih = sys.argv[1:]
    for jalur in sorted(glob.glob(os.path.join(FOLDER, 'PPT_*.md'))):
        if not pilih or os.path.basename(jalur)[4] in pilih:
            buat_deck(jalur)
    if not pilih:
        rapikan_gambar()
