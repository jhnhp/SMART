#!/usr/bin/env python3
"""Memecah docx modul teori per dosen, lalu membuat PDF semua modul .docx.

Sumber: Output/Materi/Modul Pelatihan SMART Pemanfaatan RS dan DSM.docx, yang sudah diedit tim di Word dan lebih baru
daripada berkas Modul N.md. Keluaran: Output/Materi/Modul_Teori_N_*.docx dan .pdf, ditambah PDF docx gabungan teori dan
docx modul praktik.

- Daftar isi, daftar gambar, dan daftar tabel tetap medan Word; isinya disaring dan nomor halamannya dihitung ulang.
- Penomoran bab mengikuti modul aslinya (Modul 6 tetap 6.1, Gambar 6.1, dan seterusnya).
- Daftar pustaka hanya memuat entri yang dikutip pada modul di dalam berkas itu.
- LibreOffice menghitung STYLEREF dan SEQ pada caption secara keliru, sehingga PDF dibuat dari salinan sementara yang
  nomor caption-nya dibekukan. Berkas .docx tetap memakai medan aslinya.

Jalankan: python3 Output/scripts/materi_pecah_per_dosen.py
Memerlukan: python-docx, Pillow, LibreOffice, poppler-utils.
"""
import copy
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import periksa_modul  # noqa: E402  (pemilah sitasi yang sama dengan pemeriksa modul)

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MATERI = os.path.join(AKAR, "Output", "Materi")
MASTER = os.path.join(MATERI, "Modul Pelatihan SMART Pemanfaatan RS dan DSM.docx")
PRAKTIK = os.path.join(AKAR, "Output", "Pelatihan", "Modul_Praktik_RS_DSM.docx")
DOSEN = [
    dict(berkas="Modul_Teori_1_Prof_Junun_Pengantar_RS_dan_Pemetaan_Tanah", modul=[1, 2, 3], label="MODUL 1, 2, DAN 3",
         tema="Pengantar Remote Sensing dan Pemetaan Tanah", pemateri="Prof. Dr. rer.nat. Junun Sartohadi, M.Sc."),
    dict(berkas="Modul_Teori_2_Dr_Anggri_Estimasi_Sifat_Tanah_dan_Interpretasi_Pedologis", modul=[4, 6], label="MODUL 4 DAN 6",
         tema="Estimasi Sifat Tanah dan Interpretasi Pedologis", pemateri="Dr. rer.nat Muhammad Anggri Setiawan, S.Si., M.Si."),
    dict(berkas="Modul_Teori_3_Dr_Retnadi_Bare_Soil_Detection", modul=[5], label="MODUL 5",
         tema="Bare Soil Detection dan Ekstraksi Informasi", pemateri="Dr. Retnadi Heru Jatmiko, M.Sc."),
    dict(berkas="Modul_Teori_4_Dr_Pandu_Proximal_Soil_Sensing", modul=[7], label="MODUL 7",
         tema="Proximal Soil Sensing", pemateri="Pandu Yudha Adi Putra Wirabuana, S.Hut., M.Sc., Ph.D."),
    dict(berkas="Modul_Teori_5_Dr_Guruh_Digital_Soil_Mapping", modul=[8], label="MODUL 8",
         tema="Pemodelan Digital Soil Mapping", pemateri="Dr. Eng. Guruh Samodra, S.Si., M.Sc."),
]
W_R, W_P = qn("w:r"), qn("w:p")


def teks(e):
    return "".join(t.text or "" for t in e.iter(qn("w:t")))


def gaya(p):
    ppr = p.find(qn("w:pPr"))
    s = ppr.find(qn("w:pStyle")) if ppr is not None else None
    return s.get(qn("w:val")) if s is not None else ""


def rapi(t):
    return re.sub(r"\s+", " ", t).strip().lower()


# ---------------------------------------------------------------- struktur dokumen
def peta(body):
    """Letak daftar di depan dokumen, awal setiap bab, dan awal daftar pustaka."""
    anak = list(body)
    h1 = [e for e in anak if e.tag == W_P and gaya(e) == "Heading1"]
    if rapi(teks(h1[-1])) != "daftar pustaka" or len(h1) != 9:
        raise SystemExit("Struktur docx berubah: diharapkan 8 bab dan DAFTAR PUSTAKA")
    daftar = {}
    for kunci, judul in (("isi", "DAFTAR ISI"), ("gambar", "DAFTAR GAMBAR"), ("tabel", "DAFTAR TABEL")):
        i = next(i for i, e in enumerate(anak) if e.tag == W_P and teks(e).strip() == judul)
        entri, j = [], i + 1
        while teks(anak[j]).strip():
            entri.append(anak[j])
            j += 1
        daftar[kunci] = dict(judul=anak[i], entri=entri, akhir=anak[j])
    return dict(anak=anak, h1=h1, daftar=daftar)


def blok_bab(anak, h1):
    """Elemen per bab: dari Heading 1 sampai sebelum Heading 1 berikutnya."""
    hasil = {}
    urut = [anak.index(h) for h in h1]
    for no, (a, b) in enumerate(zip(urut, urut[1:]), start=1):
        hasil[no] = anak[a:b]
    return hasil


def judul_entri(p):
    """Teks entri daftar tanpa nomor halaman, dan elemen teks nomor halamannya."""
    link = p.find(qn("w:hyperlink"))
    bagian, halaman, dalam = [], None, False
    for r in link.iter(W_R):
        if r.find(qn("w:fldChar")) is not None:
            jenis = r.find(qn("w:fldChar")).get(qn("w:fldCharType"))
            dalam = jenis in ("begin", "separate")
            continue
        if dalam:
            t = r.find(qn("w:t"))
            if t is not None:
                halaman = t
            continue
        for c in r:
            if c.tag == qn("w:t"):
                bagian.append(c.text or "")
            elif c.tag == qn("w:tab"):
                bagian.append("\t")
    return "".join(bagian).strip(), halaman


def bab_entri(judul):
    m = re.match(r"(?:Gambar |Tabel )?(\d+)\.", judul)
    return int(m.group(1)) if m else None


def saring_daftar(info, modul):
    """Hanya entri bab terpilih yang tersisa. Awal medan TOC dipindah ke entri pertama yang tersisa."""
    for d in info.values():
        pertama = d["entri"][0]
        awal = []
        for c in list(pertama):
            if c.tag == qn("w:hyperlink"):
                break
            if c.tag == W_R:
                awal.append(c)
        sisa = []
        for p in d["entri"]:
            j, _ = judul_entri(p)
            b = bab_entri(j)
            if b is None or b in modul:
                sisa.append(p)
        if sisa[0] is not pertama:
            for r in awal:
                pertama.remove(r)
            ppr = sisa[0].find(qn("w:pPr"))
            letak = list(sisa[0]).index(ppr) + 1 if ppr is not None else 0
            for k, r in enumerate(awal):
                sisa[0].insert(letak + k, r)
        for p in d["entri"]:
            if p not in sisa:
                p.getparent().remove(p)
        d["entri"] = sisa


def numbering_bab(doc, modul, bab):
    """Bab pertama mulai dari nomor aslinya; bab yang melompat memakai salinan daftar bernomor sendiri."""
    numbering = doc.part.numbering_part.element
    num4 = next(n for n in numbering.findall(qn("w:num")) if n.get(qn("w:numId")) == "4")
    abs_id = num4.find(qn("w:abstractNumId")).get(qn("w:val"))
    abstrak = next(a for a in numbering.findall(qn("w:abstractNum")) if a.get(qn("w:abstractNumId")) == abs_id)

    def atur_mulai(a, nilai):
        lvl = next(x for x in a.findall(qn("w:lvl")) if x.get(qn("w:ilvl")) == "0")
        lvl.find(qn("w:start")).set(qn("w:val"), str(nilai))

    salinan_dasar = copy.deepcopy(abstrak)
    atur_mulai(abstrak, modul[0])
    for sebelumnya, no in zip(modul, modul[1:]):
        if no == sebelumnya + 1:
            continue
        baru = copy.deepcopy(salinan_dasar)
        id_baru = str(max(int(a.get(qn("w:abstractNumId"))) for a in numbering.findall(qn("w:abstractNum"))) + 1)
        baru.set(qn("w:abstractNumId"), id_baru)
        nsid = baru.find(qn("w:nsid"))
        if nsid is not None:
            nsid.set(qn("w:val"), f"{int(id_baru) + 0x5A000000:08X}")
        atur_mulai(baru, no)
        numbering.findall(qn("w:abstractNum"))[-1].addnext(baru)
        num_baru = OxmlElement("w:num")
        id_num = str(max(int(n.get(qn("w:numId"))) for n in numbering.findall(qn("w:num"))) + 1)
        num_baru.set(qn("w:numId"), id_num)
        ref = OxmlElement("w:abstractNumId")
        ref.set(qn("w:val"), id_baru)
        num_baru.append(ref)
        numbering.findall(qn("w:num"))[-1].addnext(num_baru)
        for e in bab[no]:
            if e.tag == W_P and gaya(e) in ("Heading1", "Heading2"):
                numpr = e.find(qn("w:pPr")).get_or_add_numPr()
                numpr.get_or_add_ilvl().val = 0 if gaya(e) == "Heading1" else 1
                numpr.get_or_add_numId().val = int(id_num)


def saring_pustaka(body, bab_terpilih):
    """Mengosongkan entri yang tidak dikutip. Mengembalikan jumlah entri dan sitasi yang tidak punya entri."""
    isi = "\n\n".join("\n".join(teks(e) for e in blok if e.tag == W_P) for blok in bab_terpilih)
    dikutip = periksa_modul.sitasi_teks(isi)
    entri = [e for e in body if e.tag == W_P and gaya(e) == "DaftarPustaka"]
    ada, simpan = set(), 0
    for e in entri:
        m = re.match(r"(.+?)\s\((" + periksa_modul.TAHUN + r")(?:,[^)]*)?\)\.", teks(e))
        kunci = (periksa_modul.kunci_penulis(m.group(1)), m.group(2)) if m else None
        if kunci and kunci in dikutip:
            ada.add(kunci)
            simpan += 1
        else:
            body.remove(e)
    return simpan, sorted(f"{a} ({b})" for a, b in dikutip - ada)


def seksi_utama(doc, body, sect_pertama):
    """sectPr pertama dokumen asli memuat rujukan header dan footer, jadi harus tetap berada di seksi pertama."""
    semua = [s for s in body.iter(qn("w:sectPr"))]
    pertama = semua[0]
    if pertama is not sect_pertama:
        for c in list(pertama):
            if c.tag in (qn("w:headerReference"), qn("w:footerReference")):
                pertama.remove(c)
        for k, c in enumerate(c for c in sect_pertama if c.tag in (qn("w:headerReference"), qn("w:footerReference"))):
            pertama.insert(k, copy.deepcopy(c))


def nomor_halaman(doc):
    """Daftar isi merujuk nomor halaman, jadi halaman perlu bernomor; sampul tanpa nomor."""
    s = doc.sections[0]
    s.different_first_page_header_footer = True
    p = s.footer.paragraphs[0] if s.footer.paragraphs else s.footer.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    medan = OxmlElement("w:fldSimple")
    medan.set(qn("w:instr"), " PAGE ")
    r = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    f = OxmlElement("w:rFonts")
    for a in ("w:ascii", "w:hAnsi", "w:cs"):
        f.set(qn(a), "Times New Roman")
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), "20")
    rpr.append(f)
    rpr.append(sz)
    r.append(rpr)
    t = OxmlElement("w:t")
    t.text = "1"
    r.append(t)
    medan.append(r)
    p._p.append(medan)


def buang_gambar_tak_terpakai(doc):
    xml = doc.element.xml
    for rid, rel in list(doc.part.rels.items()):
        if rel.reltype == RT.IMAGE and f'"{rid}"' not in xml:
            del doc.part.rels[rid]


def minta_perbarui_medan(doc):
    st = doc.settings.element
    if st.find(qn("w:updateFields")) is None:
        e = OxmlElement("w:updateFields")
        e.set(qn("w:val"), "true")
        st.append(e)


def sampul_berlabel(blob, d):
    """Label modul dan pemateri pada ruang kosong sampul; sisi kanannya segaris dengan judul."""
    img = Image.open(io.BytesIO(blob)).convert("RGB")
    gambar = ImageDraw.Draw(img)
    hijau = (11, 77, 46)
    huruf = lambda nama, n: ImageFont.truetype(subprocess.run(["fc-match", "-f", "%{file}", nama], capture_output=True, text=True).stdout, n)
    kanan, y = 1262, 628
    for tulisan, h in ((d["label"], huruf("Lato:bold", 38)), (d["tema"], huruf("Lato:semibold", 28)), (d["pemateri"], huruf("Lato", 25))):
        lebar = gambar.textlength(tulisan, font=h)
        gambar.text((kanan - lebar, y), tulisan, font=h, fill=hijau)
        y += int(h.size * 1.5)
    keluar = io.BytesIO()
    img.save(keluar, "PNG", optimize=True)
    return keluar.getvalue()


# ---------------------------------------------------------------- PDF dan nomor halaman
def bekukan_medan(body):
    """Mengganti medan STYLEREF dan SEQ dengan hasil tersimpannya, khusus salinan untuk PDF."""
    for p in body.iter(W_P):
        ins = [t.text or "" for t in p.iter(qn("w:instrText"))]
        if not any(re.match(r"\s*(STYLEREF|SEQ)\b", s) for s in ins):
            continue
        runs = list(p.iter(W_R))
        i = 0
        while i < len(runs):
            fc = runs[i].find(qn("w:fldChar"))
            if fc is None or fc.get(qn("w:fldCharType")) != "begin":
                i += 1
                continue
            j = i + 1
            instr = ""
            while runs[j].find(qn("w:fldChar")) is None or runs[j].find(qn("w:fldChar")).get(qn("w:fldCharType")) == "begin":
                it = runs[j].find(qn("w:instrText"))
                instr += it.text or "" if it is not None else ""
                j += 1
            k = j
            while runs[k].find(qn("w:fldChar")) is None or runs[k].find(qn("w:fldChar")).get(qn("w:fldCharType")) != "end":
                k += 1
            if re.match(r"\s*(STYLEREF|SEQ)\b", instr):
                for r in runs[i:j + 1] + [runs[k]]:
                    r.getparent().remove(r)
            i = k + 1


def ke_pdf(docx, folder, nama=None):
    filter_pdf = 'pdf:writer_pdf_Export:{"ExportBookmarks":{"type":"boolean","value":"true"},"UseTaggedPDF":{"type":"boolean","value":"true"}}'
    subprocess.run(["soffice", "--headless", "--convert-to", filter_pdf, "--outdir", folder, docx], check=True, capture_output=True)
    hasil = os.path.join(folder, os.path.splitext(os.path.basename(docx))[0] + ".pdf")
    if nama and hasil != nama:
        shutil.move(hasil, nama)
        return nama
    return hasil


def halaman_pdf(pdf):
    n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout).group(1))
    return [rapi(subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), pdf, "-"], capture_output=True, text=True).stdout) for i in range(1, n + 1)]


def isi_nomor_halaman(info, hal):
    """Mengisi nomor halaman pada ketiga daftar. Nomor tercetak sama dengan nomor halaman fisik, sampul halaman 1."""
    terakhir = max(i for i, t in enumerate(hal) if "daftar tabel" in t and "tabel" in t[:40] or t.startswith("daftar tabel"))
    mulai = next(i for i in range(terakhir, len(hal)) if "....." not in hal[i] and rapi(re.sub(r"^\d+\.\s*", "", judul_entri(info["isi"]["entri"][0])[0])) in hal[i])
    hasil = {}
    for kunci, d in info.items():
        p = mulai
        for e in d["entri"]:
            judul, tempat = judul_entri(e)
            polos = re.sub(r"^(?:\d+(?:\.\d+)*\.?\s*)", "", judul.replace("\t", " ")).strip()
            polos = re.sub(r"^(Gambar|Tabel) \d+\.\d+\s+", "", polos)
            # spasi diabaikan, karena baris dapat terpotong sesudah tanda hubung. Pencarian memakai nomornya dulu,
            # karena judul tabel bisa sama persis dengan kalimat di halaman sebelumnya.
            for cari in (rapi(judul).replace(" ", ""), rapi(polos).replace(" ", "")):
                q = p
                while q < len(hal) and cari not in hal[q].replace(" ", ""):
                    q += 1
                if q < len(hal):
                    break
            if q >= len(hal):
                raise SystemExit(f"Tidak ditemukan pada PDF: {judul}")
            p = q
            if tempat is not None:
                tempat.text = str(q + 1)
            hasil[judul] = q + 1
    return hasil


def susun_dua_kali(doc, keluar_docx, keluar_pdf, tulis_docx=True):
    """Bangunan pertama untuk mengukur halaman, bangunan kedua menyimpan nomornya."""
    with tempfile.TemporaryDirectory() as tmp:
        # nomor halaman mengikuti salinan beku, karena itulah yang dirender
        beku = os.path.join(tmp, "beku.docx")
        salin = os.path.join(tmp, "dok.docx")
        doc.save(salin)
        d2 = Document(salin)
        info2 = peta_daftar(d2.element.body)
        bekukan_medan(d2.element.body)
        d2.save(beku)
        hal = halaman_pdf(ke_pdf(beku, tmp))
        info = peta_daftar(doc.element.body)
        isi_nomor_halaman(info, hal)
        if tulis_docx:
            doc.save(keluar_docx)
        isi_nomor_halaman(info2, hal)
        d2.save(beku)
        ke_pdf(beku, tmp, keluar_pdf)
    return len(hal)


def peta_daftar(body):
    anak = list(body)
    daftar = {}
    for kunci, judul in (("isi", "DAFTAR ISI"), ("gambar", "DAFTAR GAMBAR"), ("tabel", "DAFTAR TABEL")):
        i = next(i for i, e in enumerate(anak) if e.tag == W_P and teks(e).strip() == judul)
        entri, j = [], i + 1
        while teks(anak[j]).strip():
            entri.append(anak[j])
            j += 1
        daftar[kunci] = dict(judul=anak[i], entri=entri, akhir=anak[j])
    return daftar


# ---------------------------------------------------------------- utama
def buat_berkas(d):
    doc = Document(MASTER)
    body = doc.element.body
    p = peta(body)
    bab = blok_bab(p["anak"], p["h1"])
    sect_pertama = next(body.iter(qn("w:sectPr")))
    sect_salinan = copy.deepcopy(sect_pertama)
    cover = re.search(r'r:embed="(rId\d+)"', p["anak"][0].xml).group(1)
    doc.part.related_parts[cover]._blob = sampul_berlabel(doc.part.related_parts[cover].blob, d)
    numbering_bab(doc, d["modul"], bab)
    saring_daftar(p["daftar"], d["modul"])
    for no, blok in bab.items():
        if no not in d["modul"]:
            for e in blok:
                body.remove(e)
    # bab terakhir yang dipilih bisa berakhir dengan pemisah seksi atau pemisah halaman; keduanya berguna sebelum pustaka
    jumlah, tanpa_entri = saring_pustaka(body, [bab[n] for n in d["modul"]])
    seksi_utama(doc, body, sect_salinan)
    nomor_halaman(doc)
    buang_gambar_tak_terpakai(doc)
    minta_perbarui_medan(doc)
    doc.core_properties.title = f"Modul Pelatihan RS dan DSM: {d['tema']}"
    keluar = os.path.join(MATERI, d["berkas"])
    n = susun_dua_kali(doc, keluar + ".docx", keluar + ".pdf")
    print(f"{d['berkas']}: {n} halaman, {jumlah} pustaka; sitasi tanpa entri: {tanpa_entri or 'tidak ada'}")
    return dict(berkas=d["berkas"], modul=d["modul"], halaman=n, pustaka=jumlah, tanpa_entri=tanpa_entri)


def main():
    hasil = [buat_berkas(d) for d in DOSEN]
    # docx gabungan teori tidak diubah; PDF-nya dibuat dari salinan dengan nomor halaman dan nomor caption yang benar
    doc = Document(MASTER)
    nomor_halaman(doc)
    n = susun_dua_kali(doc, None, os.path.splitext(MASTER)[0] + ".pdf", tulis_docx=False)
    print(f"Gabungan teori: PDF {n} halaman")
    with tempfile.TemporaryDirectory() as tmp:
        ke_pdf(PRAKTIK, tmp, os.path.splitext(PRAKTIK)[0] + ".pdf")
    print("Modul praktik: PDF dibuat")
    return hasil


if __name__ == "__main__":
    main()
