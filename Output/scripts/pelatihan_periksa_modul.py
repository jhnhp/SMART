#!/usr/bin/env python3
"""Pemeriksaan teknis modul praktik di Output/Pelatihan/modul/.

Memeriksa: berkas gambar ada, nomor gambar dan tabel berurutan, setiap gambar dan tabel punya caption dan
Sumber, tidak ada heading tingkat 3, tidak ada sisa penanda, tidak ada kata terlarang, dan sitasi penulis-tahun
tercantum di Daftar Pustaka modul teori (kecuali yang dituliskan sebagai rujukan tambahan di modul itu sendiri).

Jalankan: python3 Output/scripts/pelatihan_periksa_modul.py
"""
import glob
import os
import re
import sys

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODUL = os.path.join(AKAR, 'Output', 'Pelatihan', 'modul')
PUSTAKA = os.path.join(AKAR, 'Output', 'Materi', 'Daftar Pustaka.md')
TERLARANG = ['PT SMART', 'SMART', 'Antigravity', 'Sayangku', 'Modul Junun', '{{']


def periksa(jalur, pustaka):
    masalah = []
    teks = open(jalur, encoding='utf-8').read()
    baris = teks.split('\n')
    n = re.search(r'Modul_Praktik_(\d)', jalur).group(1)
    tambahan = teks.split('## Rujukan Tambahan')[-1] if '## Rujukan Tambahan' in teks else ''
    if sum(1 for b in baris if b.startswith('# ')) != 1:
        masalah.append('heading tingkat 1 tidak tepat satu')
    if any(b.startswith('### ') for b in baris):
        masalah.append('ada heading tingkat 3')
    for kata in TERLARANG:
        if kata in teks:
            masalah.append(f'kata terlarang: {kata}')
    # gambar
    no_g = 0
    for i, b in enumerate(baris):
        m = re.match(r'!\[.*\]\((.*)\)', b)
        if not m:
            continue
        rel = m.group(1)
        if not os.path.exists(os.path.normpath(os.path.join(MODUL, rel))):
            masalah.append(f'gambar tidak ada: {rel}')
        cap = baris[i + 2] if i + 2 < len(baris) else ''
        sumber = baris[i + 4] if i + 4 < len(baris) else ''
        no_g += 1
        if not cap.startswith(f'Gambar P{n}.{no_g} '):
            masalah.append(f'caption gambar ke-{no_g} tidak sesuai: {cap[:40]}')
        if not sumber.startswith('Sumber:'):
            masalah.append(f'gambar ke-{no_g} tanpa Sumber')
    # tabel
    no_t = 0
    for i, b in enumerate(baris):
        if b.startswith('Tabel P'):
            no_t += 1
            if not b.startswith(f'Tabel P{n}.{no_t} '):
                masalah.append(f'nomor tabel tidak urut: {b[:30]}')
            if not baris[i + 2].startswith('|'):
                masalah.append(f'caption tanpa tabel: {b[:30]}')
            j = i + 2
            while j < len(baris) and baris[j].startswith('|'):
                j += 1
            if not baris[j + 1].startswith('Sumber:'):
                masalah.append(f'tabel tanpa Sumber: {b[:30]}')
    # sitasi: "(Nama, 2020)", "(Nama et al., 2020; Lain, 2021)", dan naratif "Nama (2020)" atau "Nama et al. (2020)"
    sitasi = set()
    for isi in re.findall(r'\(([^()]*\d{4}[^()]*)\)', teks):
        for bagian in isi.split(';'):
            m = re.match(r"\s*([A-Z][\w'’\-êé]+).*?,\s*(\d{4})\s*$", bagian)
            if m:
                sitasi.add(m.groups())
    sitasi |= set(re.findall(r"([A-Z][\w'’\-êé]+)(?: et al\.,?| dan [A-Z][\w\-]+| & [A-Z][\w\-]+)?(?:, [A-Z][\w\-]+, et al\.,?)? \((\d{4})\)", teks))
    for nama, tahun in sorted(sitasi):
        cocok = any(nama in p[:200] and f'({tahun}' in p for p in pustaka) or (nama in tambahan and tahun in tambahan)
        if not cocok:
            masalah.append(f'sitasi tidak ditemukan di pustaka: {nama} {tahun}')
    return no_g, no_t, masalah


def main():
    pustaka = [b for b in open(PUSTAKA, encoding='utf-8').read().split('\n') if b.strip()]
    gagal = 0
    for jalur in sorted(glob.glob(os.path.join(MODUL, 'Modul_Praktik_*.md'))):
        g, t, m = periksa(jalur, pustaka)
        print(f'{os.path.basename(jalur)}: {g} gambar, {t} tabel, {len(open(jalur, encoding="utf-8").read().split())} kata')
        for x in m:
            print('   -', x)
        gagal += len(m)
    print('Tidak ada masalah.' if not gagal else f'{gagal} masalah.')
    sys.exit(1 if gagal else 0)


if __name__ == '__main__':
    main()
