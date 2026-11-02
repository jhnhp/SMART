"""Susun berkas Word (.docx) dari modul-modul Output/Modul N.md.

Jalankan: python3 Output/scripts/buat_docx.py 4 8   -> Output/Modul RS-DSM Bab 4-8.docx
          python3 Output/scripts/buat_docx.py 1 8   -> Output/Modul RS-DSM Bab 1-8.docx

- Rumus ditulis dalam notasi TeX ($...$ dan $$...$$) di berkas modul, sehingga pandoc
  mengubahnya menjadi equation Word (OMML), bukan teks biasa.
- Gaya dokumen (A4, huruf Calibri, tabel bergaris, keterangan gambar dan tabel, daftar
  pustaka dengan inden gantung, nomor halaman) diatur melalui dokumen acuan yang dibuat
  ulang setiap kali skrip dijalankan.
- Daftar pustaka hanya memuat entri yang dikutip dalam bab yang disertakan.
- Catatan editor (komentar HTML) tidak ikut ke .docx.
"""
import os
import re
import subprocess
import sys
import tempfile
import zipfile

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import periksa_modul  # noqa: E402  (pemilah sitasi yang sama dengan pemeriksa modul)

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT = os.path.join(AKAR, "Output", "Materi")
DAFTAR_PUSTAKA = os.path.join(OUTPUT, "Daftar Pustaka.md")
JUDUL = "Pemanfaatan Remote Sensing dan Digital Soil Mapping untuk Pertanian Presisi pada Perkebunan Kelapa Sawit"
NAVY = RGBColor(0x1F, 0x3A, 0x5F)
HURUF = "Calibri"


# ---------------------------------------------------------------- dokumen acuan
def atur_huruf(gaya, ukuran=None, tebal=None, miring=None, warna=None):
    gaya.font.name = HURUF
    rpr = gaya.element.get_or_add_rPr()
    fonts = rpr.find(qn("w:rFonts"))
    if fonts is None:
        fonts = OxmlElement("w:rFonts")
        rpr.insert(0, fonts)
    for atribut in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        fonts.set(qn(atribut), HURUF)
    for atribut in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
        if fonts.get(qn(atribut)) is not None:
            del fonts.attrib[qn(atribut)]
    if ukuran:
        gaya.font.size = Pt(ukuran)
    if tebal is not None:
        gaya.font.bold = tebal
    if miring is not None:
        gaya.font.italic = miring
    gaya.font.color.rgb = warna or RGBColor(0, 0, 0)


def atur_paragraf(gaya, rata=None, sebelum=None, sesudah=None, spasi=None, tetap_bersama=None, inden_gantung=None):
    pf = gaya.paragraph_format
    if rata is not None:
        pf.alignment = rata
    if sebelum is not None:
        pf.space_before = Pt(sebelum)
    if sesudah is not None:
        pf.space_after = Pt(sesudah)
    if spasi is not None:
        pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        pf.line_spacing = spasi
    if tetap_bersama is not None:
        pf.keep_with_next = tetap_bersama
    if inden_gantung is not None:
        pf.left_indent = Cm(inden_gantung)
        pf.first_line_indent = Cm(-inden_gantung)


def gaya_paragraf(doc, nama, dasar="Normal"):
    try:
        gaya = doc.styles[nama]
    except KeyError:
        gaya = doc.styles.add_style(nama, WD_STYLE_TYPE.PARAGRAPH)
    gaya.base_style = doc.styles[dasar]
    gaya.quick_style = True
    return gaya


def garis_tabel(doc):
    """Gaya tabel "Table" bawaan pandoc: garis tipis di semua sisi dan baris judul berlatar."""
    gaya = doc.styles["Table"].element
    tblpr = gaya.find(qn("w:tblPr"))
    if tblpr is None:
        tblpr = OxmlElement("w:tblPr")
        gaya.append(tblpr)
    for lama in tblpr.findall(qn("w:tblBorders")) + tblpr.findall(qn("w:tblCellMar")):
        tblpr.remove(lama)
    batas = OxmlElement("w:tblBorders")
    for sisi in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{sisi}")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), "4")
        e.set(qn("w:space"), "0")
        e.set(qn("w:color"), "808080")
        batas.append(e)
    tblpr.append(batas)
    margin = OxmlElement("w:tblCellMar")
    for sisi, nilai in (("top", 40), ("left", 85), ("bottom", 40), ("right", 85)):
        e = OxmlElement(f"w:{sisi}")
        e.set(qn("w:w"), str(nilai))
        e.set(qn("w:type"), "dxa")
        margin.append(e)
    tblpr.append(margin)
    for lama in gaya.findall(qn("w:tblStylePr")):
        gaya.remove(lama)
    baris_judul = OxmlElement("w:tblStylePr")
    baris_judul.set(qn("w:type"), "firstRow")
    rpr = OxmlElement("w:rPr")
    rpr.append(OxmlElement("w:b"))
    baris_judul.append(rpr)
    tcpr = OxmlElement("w:tcPr")
    latar = OxmlElement("w:shd")
    latar.set(qn("w:val"), "clear")
    latar.set(qn("w:color"), "auto")
    latar.set(qn("w:fill"), "DCE6F0")
    tcpr.append(latar)
    baris_judul.append(tcpr)
    gaya.append(baris_judul)


def nomor_halaman(section):
    section.different_first_page_header_footer = True      # sampul tanpa nomor halaman
    p = section.footer.paragraphs[0] if section.footer.paragraphs else section.footer.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for bagian, isi in (("begin", None), (None, "PAGE"), ("separate", None), (None, "1"), ("end", None)):
        r = OxmlElement("w:r")
        rpr = OxmlElement("w:rPr")
        f = OxmlElement("w:rFonts")
        for atribut in ("w:ascii", "w:hAnsi", "w:cs"):
            f.set(qn(atribut), HURUF)
        rpr.append(f)
        sz = OxmlElement("w:sz")
        sz.set(qn("w:val"), "20")
        rpr.append(sz)
        r.append(rpr)
        if bagian:
            fc = OxmlElement("w:fldChar")
            fc.set(qn("w:fldCharType"), bagian)
            r.append(fc)
        elif isi == "PAGE":
            instr = OxmlElement("w:instrText")
            instr.set(qn("xml:space"), "preserve")
            instr.text = " PAGE "
            r.append(instr)
        else:
            t = OxmlElement("w:t")
            t.text = isi
            r.append(t)
        p._p.append(r)


def buat_acuan(path):
    bawaan = subprocess.run(["pandoc", "--print-default-data-file", "reference.docx"], check=True,
                            capture_output=True).stdout
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
        f.write(bawaan)
    doc = Document(f.name)
    os.unlink(f.name)

    s = doc.sections[0]
    s.page_width, s.page_height = Cm(21.0), Cm(29.7)
    s.top_margin = s.bottom_margin = Cm(2.5)
    s.left_margin = s.right_margin = Cm(2.5)
    s.header_distance = s.footer_distance = Cm(1.25)
    s.gutter = Cm(0)
    nomor_halaman(s)

    st = doc.styles
    atur_huruf(st["Normal"], 11)
    atur_paragraf(st["Normal"], sesudah=6, spasi=1.15)
    for nama in ("Body Text", "First Paragraph"):
        atur_huruf(st[nama], 11)
        atur_paragraf(st[nama], rata=WD_ALIGN_PARAGRAPH.JUSTIFY, sebelum=0, sesudah=8, spasi=1.15)
    atur_huruf(st["Compact"], 11)                              # daftar rapat; isi tabel memakai "Isi Tabel"
    atur_paragraf(st["Compact"], sebelum=0, sesudah=3, spasi=1.15)
    atur_huruf(st["Heading 1"], 16, tebal=True, warna=NAVY)
    atur_paragraf(st["Heading 1"], rata=WD_ALIGN_PARAGRAPH.LEFT, sebelum=0, sesudah=10, tetap_bersama=True)
    st["Heading 1"].paragraph_format.page_break_before = True
    atur_huruf(st["Heading 2"], 13, tebal=True, warna=NAVY)
    atur_paragraf(st["Heading 2"], sebelum=14, sesudah=6, tetap_bersama=True)
    atur_huruf(st["Title"], 22, tebal=True, warna=NAVY)
    atur_paragraf(st["Title"], rata=WD_ALIGN_PARAGRAPH.CENTER, sebelum=150, sesudah=18)
    atur_huruf(st["Subtitle"], 14, warna=NAVY)
    atur_paragraf(st["Subtitle"], rata=WD_ALIGN_PARAGRAPH.CENTER, sebelum=0, sesudah=60)
    for nama in ("Author", "Date"):
        atur_huruf(st[nama], 12)
        atur_paragraf(st[nama], rata=WD_ALIGN_PARAGRAPH.CENTER, sebelum=0, sesudah=4)

    tengah = WD_ALIGN_PARAGRAPH.CENTER
    g = gaya_paragraf(doc, "Gambar")
    atur_huruf(g, 11)
    atur_paragraf(g, rata=tengah, sebelum=6, sesudah=4, spasi=1.0, tetap_bersama=True)
    g = gaya_paragraf(doc, "Keterangan Gambar")
    atur_huruf(g, 10)
    atur_paragraf(g, rata=tengah, sebelum=0, sesudah=2, spasi=1.0, tetap_bersama=True)
    g = gaya_paragraf(doc, "Keterangan Tabel")
    atur_huruf(g, 10)
    atur_paragraf(g, rata=tengah, sebelum=10, sesudah=4, spasi=1.0, tetap_bersama=True)
    g = gaya_paragraf(doc, "Sumber")
    atur_huruf(g, 9, miring=True)
    atur_paragraf(g, rata=tengah, sebelum=2, sesudah=12, spasi=1.0)
    g = gaya_paragraf(doc, "Isi Tabel")
    atur_huruf(g, 9.5)
    atur_paragraf(g, sebelum=0, sesudah=0, spasi=1.0)
    g = gaya_paragraf(doc, "Daftar Pustaka")
    atur_huruf(g, 10.5)
    atur_paragraf(g, rata=WD_ALIGN_PARAGRAPH.LEFT, sebelum=0, sesudah=6, spasi=1.1, inden_gantung=1.27)
    st["Hyperlink"].font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    garis_tabel(doc)
    doc.save(path)


# ---------------------------------------------------------------- isi dokumen
def blok_gaya(teks, gaya):
    return f'::: {{custom-style="{gaya}"}}\n{teks}\n:::'


def olah_modul(teks):
    """Beri gaya khusus pada gambar, keterangan, dan baris Sumber; tabel dan rumus dibiarkan."""
    teks = periksa_modul.tanpa_komentar(teks)
    blok = [b.strip() for b in re.split(r"\n\s*\n", teks.strip()) if b.strip()]
    hasil = []
    for i, b in enumerate(blok):
        sebelum = blok[i - 1] if i else ""
        sesudah = blok[i + 1] if i + 1 < len(blok) else ""
        if re.fullmatch(r"!\[[^\]]*\]\([^)]+\)(\{[^}]*\})?", b):
            if not b.endswith("}"):
                b += "{width=16cm}"
            b = blok_gaya(b, "Gambar")
        # keterangan gambar tepat di bawah gambar; keterangan tabel tepat di atas tabel
        elif re.match(r"Gambar \d+\.\d+ ", b) and sebelum.startswith("!["):
            b = blok_gaya(b, "Keterangan Gambar")
        elif re.match(r"Tabel \d+\.\d+ ", b) and sesudah.startswith("|"):
            b = blok_gaya(b, "Keterangan Tabel")
        elif b.startswith("Sumber:"):
            b = blok_gaya(b, "Sumber")
        hasil.append(b)
    return "\n\n".join(hasil)


def daftar_pustaka(dikutip):
    """Entri daftar pustaka yang dikutip, dalam urutan aslinya."""
    entri = []
    for blok in periksa_modul.tanpa_komentar(open(DAFTAR_PUSTAKA, encoding="utf-8").read()).split("\n\n"):
        blok = blok.strip()
        m = re.match(r"(.+?)\s\((" + periksa_modul.TAHUN + r")(?:,[^)]*)?\)\.", blok)
        if m and (periksa_modul.kunci_penulis(m.group(1)), m.group(2)) in dikutip:
            entri.append(blok)
    return entri


def susun_markdown(awal, akhir):
    bab = list(range(awal, akhir + 1))
    isi_modul = [open(os.path.join(OUTPUT, f"Modul {n}.md"), encoding="utf-8").read() for n in bab]
    dikutip = set()
    for isi in isi_modul:
        dikutip |= periksa_modul.sitasi_teks(periksa_modul.tanpa_komentar(isi))
    entri = daftar_pustaka(dikutip)
    rentang = f"Bab {awal}–{akhir}" if awal != akhir else f"Bab {awal}"
    meta = ("---\n"
            f'title: "{JUDUL}"\n'
            f'subtitle: "Modul Pelatihan · {rentang}"\n'
            "author:\n"
            '  - "Universitas Gadjah Mada"\n'
            '  - "Pusat Studi Pengelolaan Sumber Daya Lahan (PS2DL)"\n'
            'date: "Draf untuk ditinjau · Oktober 2026"\n'
            "lang: id-ID\n"
            "---\n")
    bagian = [meta] + [olah_modul(isi) for isi in isi_modul]
    bagian.append("# DAFTAR PUSTAKA\n\n" + blok_gaya("\n\n".join(entri), "Daftar Pustaka"))
    return "\n\n".join(bagian) + "\n", len(entri)


def rapikan_docx(path):
    """Lengkapi deklarasi yang diminta skema OOXML: tipe isi PNG dan atribut gutter pada margin halaman."""
    sementara = path + ".tmp"
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(sementara, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "[Content_Types].xml":
                t = data.decode("utf-8")
                if 'Extension="png"' not in t:
                    t = t.replace('<Default Extension="xml"', '<Default Extension="png" ContentType="image/png" />'
                                  '<Default Extension="xml"', 1)
                data = t.encode("utf-8")
            elif item.filename == "word/document.xml":
                t = re.sub(r"<w:pgMar (?![^>]*w:gutter)", '<w:pgMar w:gutter="0" ', data.decode("utf-8"))
                # \text{} menghasilkan m:nor dan m:sty sekaligus, padahal skema OMML hanya mengizinkan salah satunya
                t = re.sub(r"<m:nor\s*/>\s*<m:sty [^>]*/>", "<m:nor />", t)
                # sel tabel memakai gaya "Isi Tabel" (huruf lebih kecil), bukan "Compact" milik daftar rapat
                t = re.sub(r"<w:tbl>.*?</w:tbl>", lambda m: m.group(0).replace('w:val="Compact"', 'w:val="IsiTabel"'),
                           t, flags=re.S)
                data = t.encode("utf-8")
            zout.writestr(item, data)
    os.replace(sementara, path)


def main():
    awal, akhir = (int(a) for a in sys.argv[1:3]) if len(sys.argv) >= 3 else (1, 8)
    keluaran = os.path.join(OUTPUT, f"Modul RS-DSM Bab {awal}-{akhir}.docx")
    with tempfile.TemporaryDirectory() as tmp:
        acuan = os.path.join(tmp, "acuan.docx")
        buat_acuan(acuan)
        teks, n_pustaka = susun_markdown(awal, akhir)
        md = os.path.join(tmp, "gabungan.md")
        open(md, "w", encoding="utf-8").write(teks)
        subprocess.run(["pandoc", md, "-f", "markdown", "-t", "docx", f"--reference-doc={acuan}",
                        f"--resource-path={OUTPUT}", "-o", keluaran], check=True)
    rapikan_docx(keluaran)
    print(f"tersimpan: {os.path.relpath(keluaran, AKAR)} ({n_pustaka} entri daftar pustaka)")


if __name__ == "__main__":
    main()
