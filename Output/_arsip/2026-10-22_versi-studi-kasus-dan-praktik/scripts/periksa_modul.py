"""Pemeriksaan teknis berkas modul (Output/Modul N.md).

Jalankan: python3 Output/scripts/periksa_modul.py [nomor_modul ...]
Tanpa argumen, semua berkas Output/Modul *.md diperiksa.

Yang diperiksa:
- urutan nomor gambar dan tabel, keberadaan berkas gambar, kecocokan ID berkas
  (M<n>-G<kk>) dengan nomor caption, serta baris "Sumber:" setelah caption/tabel;
- setiap gambar dan tabel dirujuk di teks sebelum atau sesudah kemunculannya;
- kecocokan sitasi dalam teks dengan Daftar Pustaka (dua arah);
- ejaan "Bompon", tidak ada branding PT SMART, dan salah ketik lama Modul 1–2.
"""
import glob
import os
import re
import sys

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT = os.path.join(AKAR, "Output")
TERLARANG = ["Bompong", "PT SMART", "SMART Tbk", "cahya", "Menggunaka", "iformasi", "Misanya", "menghasikan",
             "Unigersity", "dibawah ini", "dimana"]


def kunci_penulis(teks):
    teks = teks.strip().strip("(").strip()
    teks = re.split(r"\s+et al\.|\s+&\s+|\s+dan\s+|,", teks)[0].strip().rstrip(".")
    return teks.lower()


def sitasi_teks(isi):
    hasil = set()
    tahun = r"(?:\d{4}|t\.t\.)(?:-[a-z])?"
    for grup in re.findall(r"\(([^()]*?" + tahun + r"[^()]*?)\)", isi):
        for bagian in grup.split(";"):
            m = re.match(r"\s*(?:lihat juga\s+)?(.+?),\s*(" + tahun + r"(?:,\s*t\.t\.-[a-z])*)\s*$", bagian.strip())
            if m:
                for th in re.split(r",\s*", m.group(2)):
                    th = th if not th.startswith("t.t.-") or th == m.group(2) else th
                    hasil.add((kunci_penulis(m.group(1)), th))
    nama = r"(?:(?:van|de|von)\s+)?[A-Z][\w\-’']+"
    naratif = (r"(" + nama + r"(?:\s+[A-Z][\w\-’']+)*(?:\s+et al\.)?(?:\s+(?:dan|&)\s+" + nama + r")?)\s+\((" + tahun + r")\)")
    for nama, th in re.findall(naratif, isi):
        hasil.add((kunci_penulis(nama), th))
    return hasil


def pustaka(blok):
    hasil = {}
    for baris in blok.split("\n\n"):
        baris = baris.strip()
        m = re.match(r"(.+?)\s\(((?:\d{4}|t\.t\.)(?:-[a-z])?)\)\.", baris)
        if m:
            hasil[(kunci_penulis(m.group(1)), m.group(2))] = baris[:70]
    return hasil


def periksa(path):
    n = int(re.search(r"Modul (\d+)\.md$", path).group(1))
    isi = open(path, encoding="utf-8").read()
    baris = isi.split("\n")
    masalah = []

    # gambar
    nomor_gambar = []
    for i, b in enumerate(baris):
        m = re.match(r"!\[\]\((assets/[^)]+)\)", b)
        if not m:
            continue
        rel = m.group(1)
        if not os.path.exists(os.path.join(OUTPUT, rel)):
            masalah.append(f"berkas gambar tidak ada: {rel}")
        lanjut = [x for x in baris[i + 1:i + 6] if x.strip()]
        cap = re.match(rf"Gambar {n}\.(\d+) \S", lanjut[0]) if lanjut else None
        if not cap:
            masalah.append(f"caption tidak ditemukan setelah {rel}")
            continue
        k = int(cap.group(1))
        nomor_gambar.append(k)
        if not re.search(rf"M{n}-G{k:02d}_", rel):
            masalah.append(f"ID berkas {os.path.basename(rel)} tidak cocok dengan Gambar {n}.{k}")
        if len(lanjut) < 2 or not lanjut[1].startswith("Sumber:"):
            masalah.append(f"Gambar {n}.{k} tidak diikuti baris Sumber")
        rujukan = len(re.findall(rf"Gambar {n}\.{k}(?!\d)", isi)) - 1
        if rujukan < 1:
            masalah.append(f"Gambar {n}.{k} tidak dirujuk di teks")
    if nomor_gambar != list(range(1, len(nomor_gambar) + 1)):
        masalah.append(f"urutan nomor gambar tidak runtut: {nomor_gambar}")

    # tabel
    nomor_tabel = []
    for i, b in enumerate(baris):
        m = re.match(rf"Tabel {n}\.(\d+) \S", b)
        if not m:
            continue
        k = int(m.group(1))
        nomor_tabel.append(k)
        j = i + 1
        while j < len(baris) and not baris[j].startswith("|"):
            j += 1
        while j < len(baris) and baris[j].startswith("|"):
            j += 1
        sesudah = [x for x in baris[j:j + 3] if x.strip()]
        if not sesudah or not sesudah[0].startswith("Sumber:"):
            masalah.append(f"Tabel {n}.{k} tidak diikuti baris Sumber")
        if len(re.findall(rf"Tabel {n}\.{k}(?!\d)", isi)) < 2:
            masalah.append(f"Tabel {n}.{k} tidak dirujuk di teks")
    if nomor_tabel != list(range(1, len(nomor_tabel) + 1)):
        masalah.append(f"urutan nomor tabel tidak runtut: {nomor_tabel}")

    # sitasi
    if "## Daftar Pustaka" not in isi:
        masalah.append("bagian Daftar Pustaka tidak ada")
        teks, dp = isi, {}
    else:
        teks, blok = isi.split("## Daftar Pustaka", 1)
        dp = pustaka(blok)
    dikutip = sitasi_teks(teks)
    for k in sorted(dikutip - set(dp)):
        masalah.append(f"dikutip tetapi tidak ada di Daftar Pustaka: {k}")
    for k in sorted(set(dp) - dikutip):
        masalah.append(f"ada di Daftar Pustaka tetapi tidak dikutip: {k}")

    # istilah terlarang dan struktur wajib
    for kata in TERLARANG:
        if kata in isi:
            masalah.append(f"memuat '{kata}'")
    for bagian in ("## Tujuan dan Capaian Pembelajaran", "*Ceramah dan diskusi:*", "## Rangkuman"):
        if bagian not in isi:
            masalah.append(f"bagian wajib tidak ada: {bagian}")
    kata = len(re.sub(r"!\[\]\([^)]*\)", "", teks).split())
    print(f"Modul {n}: {kata} kata, {len(nomor_gambar)} gambar, {len(nomor_tabel)} tabel, "
          f"{len(dikutip)} sitasi unik, {len(dp)} entri pustaka")
    for m in masalah:
        print("   -", m)
    if not masalah:
        print("   tidak ada masalah")
    return not masalah


if __name__ == "__main__":
    pilihan = sys.argv[1:]
    berkas = sorted(glob.glob(os.path.join(OUTPUT, "Modul *.md")),
                    key=lambda p: int(re.search(r"Modul (\d+)", p).group(1)))
    if pilihan:
        berkas = [b for b in berkas if re.search(r"Modul (\d+)", b).group(1) in pilihan]
    ok = all([periksa(b) for b in berkas])
    sys.exit(0 if ok else 1)
