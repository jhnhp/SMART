"""Pemeriksaan teknis berkas modul (Output/Modul N.md) dan daftar pustaka gabungan.

Jalankan: python3 Output/scripts/periksa_modul.py [nomor_modul ...]
Tanpa argumen, semua berkas Output/Modul *.md diperiksa.

Yang diperiksa:
- struktur sama dengan Bab 1 dan 2: judul modul (H1) dan subbab (H2) persis sesuai kerangka di
  Source/Modul 1 & 2.md, label "*Ceramah dan diskusi:*" di bawah judul, tanpa heading tingkat 3,
  serta tanpa bagian Tujuan, Capaian, Rangkuman, Praktik, atau daftar pustaka per modul;
- urutan nomor gambar dan tabel, keberadaan berkas gambar, kecocokan ID berkas (M<n>-G<kk> untuk
  gambar, M<n>-T<kk><huruf> untuk ilustrasi di dalam tabel) dengan nomor caption, serta baris
  "Sumber:" setelah caption gambar dan setelah tabel;
- kecocokan sitasi dalam semua modul dengan Output/Daftar Pustaka.md (dua arah);
- istilah terlarang: studi kasus Bompon (ditunda selama fokus teori), ejaan "Bompong", branding
  PT SMART, dan salah ketik lama Bab 1–2.
Gambar atau tabel yang tidak dirujuk di teks hanya dilaporkan sebagai catatan, karena Bab 1 dan 2
asli juga memuat gambar yang tidak dirujuk.
"""
import glob
import os
import re
import sys
import unicodedata

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT = os.path.join(AKAR, "Output")
KERANGKA = os.path.join(AKAR, "Source", "Modul 1 & 2.md")
DAFTAR_PUSTAKA = os.path.join(OUTPUT, "Daftar Pustaka.md")
TERLARANG = ["Bompon", "Bompong", "PT SMART", "SMART Tbk", "cahya", "Menggunaka", "iformasi", "Misanya",
             "menghasikan", "Unigersity", "dibawah ini", "dimana"]
BAGIAN_TERLARANG = ["Tujuan", "Capaian", "Rangkuman", "Praktik", "Daftar Pustaka", "DAFTAR PUSTAKA"]
TAHUN = r"(?:\d{4}|t\.t\.)(?:-[a-z])?"
KAPITAL = "A-ZÀ-ÖØ-ÞĀ-Ž"  # huruf awal nama penulis, termasuk berdiakritik (mis. Ågren)


def kerangka():
    """Judul modul (H1) dan subbab (H2) dari kerangka di Source, berurutan per modul."""
    hasil = []
    for b in open(KERANGKA, encoding="utf-8"):
        b = b.rstrip()
        if b.startswith("# ") and b[2:].strip() != "DAFTAR PUSTAKA":
            hasil.append((b[2:].strip(), []))
        elif b.startswith("## ") and hasil:
            hasil[-1][1].append(b[3:].strip())
    return hasil


def tanpa_komentar(teks):
    return re.sub(r"<!--.*?-->", "", teks, flags=re.S)


def kunci_penulis(teks):
    teks = teks.strip().strip("(").strip()
    teks = re.split(r"\s+et al\.|\s+&\s+|\s+dan\s+|,", teks)[0].strip().rstrip(".")
    return teks.lower()


def sitasi_teks(isi):
    hasil = set()
    beberapa = TAHUN + r"(?:\s*,\s*" + TAHUN + r")*"   # satu penulis dengan beberapa tahun, mis. (Buringh, 1954, 1955)
    for grup in re.findall(r"\(([^()]*?" + TAHUN + r"[^()]*?)\)", isi):
        for bagian in grup.split(";"):
            m = re.match(r"\s*(?:lihat juga\s+)?(.+?),\s*(" + beberapa + r")\s*$", bagian.strip())
            if m and not re.fullmatch(beberapa, m.group(1).strip()):
                for th in re.findall(TAHUN, m.group(2)):
                    hasil.add((kunci_penulis(m.group(1)), th))
    nama = r"(?:(?:van|de|von)\s+)?[" + KAPITAL + r"][\w\-’']+"
    blok = nama + r"(?:\s+[" + KAPITAL + r"][\w\-’']+)*"            # nama bermarga majemuk, mis. Viscarra Rossel
    # satu atau beberapa penulis: "A", "A et al.", "A dan B", "A, B, dan C", "A, B, et al.". Bentuk daftar
    # mensyaratkan koma sebelum "dan"/"et al." agar frasa seperti "tanah tropis Brasil, Galvão dan ..." tidak ikut.
    penulis_naratif = (blok + r"(?:(?:,\s+" + blok + r")+,\s+(?:(?:dan|&)\s+" + blok + r"|et al\.)"
                       + r"|\s+et al\.|\s+(?:dan|&)\s+" + blok + r")?")
    naratif = r"(" + penulis_naratif + r")\s+\((" + TAHUN + r")\)"
    naratif_ganda = r"(" + penulis_naratif + r")\s+\((" + TAHUN + r"(?:\s*,\s*" + TAHUN + r")+)\)"
    for penulis, th in re.findall(naratif, isi):
        hasil.add((kunci_penulis(penulis), th))
    for penulis, th in re.findall(naratif_ganda, isi):
        for t in re.findall(TAHUN, th):
            hasil.add((kunci_penulis(penulis), t))
    return hasil


def pustaka(isi):
    hasil = {}
    for blok in tanpa_komentar(isi).split("\n\n"):
        blok = blok.strip()
        m = re.match(r"(.+?)\s\((" + TAHUN + r")(?:,[^)]*)?\)\.", blok)
        if m:
            hasil[(kunci_penulis(m.group(1)), m.group(2))] = blok[:70]
    return hasil


def periksa_struktur(n, baris, masalah):
    daftar = kerangka()
    if n > len(daftar):
        masalah.append(f"Modul {n} tidak ada di kerangka")
        return
    judul, subbab = daftar[n - 1]
    isi_baris = [b for b in baris if b.strip()]
    if not isi_baris or isi_baris[0] != f"# {judul}":
        masalah.append(f"judul modul harus '# {judul}'")
    if len(isi_baris) < 2 or isi_baris[1] != "*Ceramah dan diskusi:*":
        masalah.append("baris kedua harus '*Ceramah dan diskusi:*'")
    h1 = [b for b in baris if re.match(r"# ", b)]
    if len(h1) != 1:
        masalah.append(f"heading tingkat 1 harus tepat satu, ditemukan {len(h1)}")
    h2 = [b[3:].strip() for b in baris if re.match(r"## ", b)]
    if h2 != subbab:
        masalah.append(f"subbab tidak sesuai kerangka:\n       ada    : {h2}\n       kerangka: {subbab}")
    for b in baris:
        if re.match(r"#{3,} ", b):
            masalah.append(f"heading tingkat 3 atau lebih tidak diizinkan: {b}")
        if re.match(r"#+ ", b) and any(k in b for k in BAGIAN_TERLARANG):
            masalah.append(f"bagian tidak diizinkan: {b}")


def periksa_gambar(n, baris, isi, masalah, catatan):
    nomor_gambar = []
    tabel_aktif = None
    for i, b in enumerate(baris):
        m_tabel = re.match(rf"Tabel {n}\.(\d+) \S", b)
        if m_tabel:
            tabel_aktif = int(m_tabel.group(1))
        for rel in re.findall(r"!\[\]\(([^)]+)\)", b):
            if not rel.startswith(f"assets/modul-{n}/"):
                masalah.append(f"gambar di luar folder assets/modul-{n}/: {rel}")
            if not os.path.exists(os.path.join(OUTPUT, rel)):
                masalah.append(f"berkas gambar tidak ada: {rel}")
            if b.startswith("|"):
                if tabel_aktif is None or not re.search(rf"M{n}-T{tabel_aktif:02d}[a-z]_", rel):
                    masalah.append(f"ID ilustrasi tabel {os.path.basename(rel)} tidak cocok dengan Tabel {n}.{tabel_aktif}")
                continue
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
            if len(re.findall(rf"Gambar {n}\.{k}(?!\d)", isi)) < 2:
                catatan.append(f"Gambar {n}.{k} tidak dirujuk di teks")
    if nomor_gambar != list(range(1, len(nomor_gambar) + 1)):
        masalah.append(f"urutan nomor gambar tidak runtut: {nomor_gambar}")
    return nomor_gambar


def periksa_tabel(n, baris, isi, masalah, catatan):
    nomor_tabel = []
    for i, b in enumerate(baris):
        m = re.match(rf"Tabel {n}\.(\d+) \S", b)
        if not m:
            continue
        k = int(m.group(1))
        nomor_tabel.append(k)
        sebelum = [x for x in baris[i + 1:i + 3] if x.strip()]
        if not sebelum or not sebelum[0].startswith("|"):
            masalah.append(f"caption Tabel {n}.{k} tidak langsung diikuti tabel")
        j = i + 1
        while j < len(baris) and not baris[j].startswith("|"):
            j += 1
        while j < len(baris) and baris[j].startswith("|"):
            j += 1
        sesudah = [x for x in baris[j:j + 3] if x.strip()]
        if not sesudah or not sesudah[0].startswith("Sumber:"):
            masalah.append(f"Tabel {n}.{k} tidak diikuti baris Sumber")
        if len(re.findall(rf"Tabel {n}\.{k}(?!\d)", isi)) < 2:
            catatan.append(f"Tabel {n}.{k} tidak dirujuk di teks")
    if nomor_tabel != list(range(1, len(nomor_tabel) + 1)):
        masalah.append(f"urutan nomor tabel tidak runtut: {nomor_tabel}")
    return nomor_tabel


def periksa(path):
    n = int(re.search(r"Modul (\d+)\.md$", path).group(1))
    isi = open(path, encoding="utf-8").read()
    teks = tanpa_komentar(isi)
    baris = teks.split("\n")
    masalah, catatan = [], []

    periksa_struktur(n, baris, masalah)
    nomor_gambar = periksa_gambar(n, baris, teks, masalah, catatan)
    nomor_tabel = periksa_tabel(n, baris, teks, masalah, catatan)
    for kata in TERLARANG:
        if re.search(rf"\b{re.escape(kata)}\b", isi):
            masalah.append(f"memuat '{kata}'")

    dikutip = sitasi_teks(teks)
    kata = len(re.sub(r"!\[\]\([^)]*\)(\{[^}]*\})?", "", teks).split())
    print(f"Modul {n}: {kata} kata, {len(nomor_gambar)} gambar, {len(nomor_tabel)} tabel, {len(dikutip)} sitasi unik")
    for m in masalah:
        print("   -", m)
    for c in catatan:
        print("   catatan:", c)
    if not masalah:
        print("   tidak ada masalah")
    return not masalah, dikutip


def periksa_pustaka(dikutip, semua_modul):
    if not os.path.exists(DAFTAR_PUSTAKA):
        print("Daftar Pustaka: berkas Output/Daftar Pustaka.md tidak ada")
        return False
    isi = open(DAFTAR_PUSTAKA, encoding="utf-8").read()
    dp = pustaka(isi)
    masalah = []
    if not isi.startswith("# DAFTAR PUSTAKA"):
        masalah.append("berkas harus diawali '# DAFTAR PUSTAKA'")
    # urutan alfabetis mengabaikan diakritik, seperti lazim dalam APA (Ågren diurutkan sebagai Agren)
    penulis = [unicodedata.normalize("NFKD", k[0]).encode("ascii", "ignore").decode() for k in dp]
    if penulis != sorted(penulis):
        masalah.append("entri tidak berurutan alfabetis")
    for k in sorted(dikutip - set(dp)):
        masalah.append(f"dikutip tetapi tidak ada di Daftar Pustaka: {k}")
    if semua_modul:
        for k in sorted(set(dp) - dikutip):
            masalah.append(f"ada di Daftar Pustaka tetapi tidak dikutip: {k}")
    print(f"Daftar Pustaka: {len(dp)} entri")
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
    hasil = [periksa(b) for b in berkas]
    dikutip = set().union(*(d for _, d in hasil)) if hasil else set()
    ok_pustaka = periksa_pustaka(dikutip, semua_modul=not pilihan)
    sys.exit(0 if all(o for o, _ in hasil) and ok_pustaka else 1)
