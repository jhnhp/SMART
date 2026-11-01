"""Gambar Modul 2 — Multi-source Data Fusion.

Jalankan: python3 Output/scripts/gambar_modul_2.py
Keluaran: Output/assets/modul-2/M2-Gxx_*.png
"""
from matplotlib.patches import Rectangle

import gaya
from gaya import WARNA, kanvas, kotak, panah, simpan

MODUL = "modul-2"


# ---------------------------------------------------------------- Gambar 2.1
def g01_tingkat_fusi():
    fig, ax = kanvas(10, 6.2, (0, 104), (0, 64))
    abu, putih = WARNA["latar"], WARNA["putih"]
    w, h = 13, 5.2

    def node(x, y, teks, isi=putih, warna=WARNA["navy"], tebal=False):
        kotak(ax, x, y, w, h, teks, isi=isi, warna=warna, ukuran=8.3, tebal=tebal, r=0.8, lw=1.1)

    def ke(x1, y1, x2, y2):
        panah(ax, x1, y1, x2, y2, warna=WARNA["abu"], lw=1.1, skala=10)

    baris = [(44, "(a) Fusi tingkat piksel/data", WARNA["teal"]),
             (23, "(b) Fusi tingkat fitur", WARNA["oranye"]),
             (2, "(c) Fusi tingkat keputusan", WARNA["ungu"])]
    for y0, label, warna in baris:
        ax.add_patch(Rectangle((0, y0 - 1.0), 104, 19.5, fc=abu, ec="none", zorder=0))
        ax.text(1.5, y0 + 17.0, label, fontsize=10, fontweight="bold", color=warna, va="center")
        node(2, y0 + 8.6, "Data A\n(mis. citra optik)")
        node(2, y0 + 1.0, "Data B\n(mis. citra SAR)")

    # (a) piksel
    y0 = 44
    node(24, y0 + 4.8, "Fusi piksel", isi=WARNA["teal"], warna=WARNA["teal"], tebal=True)
    ax.texts[-1].set_color("white")
    node(44, y0 + 4.8, "Ekstraksi fitur")
    node(64, y0 + 4.8, "Klasifikasi/\nprediksi")
    node(86, y0 + 4.8, "Hasil akhir", isi="#DCEAF7")
    ke(15.2, y0 + 11.2, 24, y0 + 8.4), ke(15.2, y0 + 3.6, 24, y0 + 6.4)
    ke(37.2, y0 + 7.4, 44, y0 + 7.4), ke(57.2, y0 + 7.4, 64, y0 + 7.4), ke(77.2, y0 + 7.4, 86, y0 + 7.4)

    # (b) fitur
    y0 = 23
    node(24, y0 + 8.6, "Fitur A\n(mis. NDVI)")
    node(24, y0 + 1.0, "Fitur B\n(mis. backscatter)")
    node(44, y0 + 4.8, "Fusi fitur", isi=WARNA["oranye"], warna=WARNA["oranye"], tebal=True)
    ax.texts[-1].set_color("white")
    node(64, y0 + 4.8, "Klasifikasi/\nprediksi")
    node(86, y0 + 4.8, "Hasil akhir", isi="#DCEAF7")
    ke(15.2, y0 + 11.2, 24, y0 + 11.2), ke(15.2, y0 + 3.6, 24, y0 + 3.6)
    ke(37.2, y0 + 11.2, 44, y0 + 8.4), ke(37.2, y0 + 3.6, 44, y0 + 6.4)
    ke(57.2, y0 + 7.4, 64, y0 + 7.4), ke(77.2, y0 + 7.4, 86, y0 + 7.4)

    # (c) keputusan
    y0 = 2
    node(24, y0 + 8.6, "Fitur A")
    node(24, y0 + 1.0, "Fitur B")
    node(44, y0 + 8.6, "Keputusan A")
    node(44, y0 + 1.0, "Keputusan B")
    node(64, y0 + 4.8, "Fusi keputusan", isi=WARNA["ungu"], warna=WARNA["ungu"], tebal=True)
    ax.texts[-1].set_color("white")
    node(86, y0 + 4.8, "Hasil akhir", isi="#DCEAF7")
    ke(15.2, y0 + 11.2, 24, y0 + 11.2), ke(15.2, y0 + 3.6, 24, y0 + 3.6)
    ke(37.2, y0 + 11.2, 44, y0 + 11.2), ke(37.2, y0 + 3.6, 44, y0 + 3.6)
    ke(57.2, y0 + 11.2, 64, y0 + 8.4), ke(57.2, y0 + 3.6, 64, y0 + 6.4)
    ke(77.2, y0 + 7.4, 86, y0 + 7.4)
    simpan(fig, MODUL, "M2-G01_tingkat-fusi-data.png")


if __name__ == "__main__":
    gaya.atur()
    g01_tingkat_fusi()
