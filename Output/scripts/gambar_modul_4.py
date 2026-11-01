"""Gambar Modul 4 — Remote Sensing untuk Estimasi Soil Properties.

Jalankan: python3 Output/scripts/gambar_modul_4.py
Keluaran: Output/assets/modul-4/M4-Gxx_*.png
Semua gambar bersifat konseptual; kurva pada Gambar 4.2 adalah ilustrasi skematis, bukan data terukur.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle
from matplotlib.ticker import FuncFormatter, MultipleLocator
from scipy.interpolate import PchipInterpolator

import gaya
from gaya import WARNA, kanvas, kotak, nomor, panah, simpan

MODUL = "modul-4"
KOMA = FuncFormatter(lambda v, _: f"{v:.1f}".replace(".", ","))

# Kanal Sentinel-2 MSI (batas bawah–atas, µm) dari panjang gelombang pusat dan lebar kanal (Drusch et al., 2012)
KANAL_S2 = [("B2", 0.4575, 0.5225), ("B3", 0.5425, 0.5775), ("B4", 0.650, 0.680), ("B5", 0.6975, 0.7125),
            ("B6", 0.7325, 0.7475), ("B7", 0.773, 0.793), ("B8", 0.7845, 0.8995), ("B11", 1.565, 1.655),
            ("B12", 2.100, 2.280)]
SERAPAN_ATMOSFER = [(1.35, 1.45), (1.80, 1.95)]


# ---------------------------------------------------------------- Gambar 4.1
def g01_jalur_estimasi():
    fig, ax = kanvas(10, 5.6, (0, 104), (0, 58))
    w, h = 17.5, 9.0

    def node(x, y, teks, isi=WARNA["putih"], warna=WARNA["navy"], tebal=False, tinggi=h, lebar=w, ukuran=8.2):
        kotak(ax, x, y, lebar, tinggi, teks, isi=isi, warna=warna, ukuran=ukuran, tebal=tebal, r=0.8, lw=1.1)

    def ke(x1, y1, x2, y2, warna=WARNA["abu"]):
        panah(ax, x1, y1, x2, y2, warna=warna, lw=1.1, skala=10)

    # data penginderaan jauh
    ax.text(10.5, 56.0, "Data penginderaan jauh", ha="center", va="center", fontsize=9.5, fontweight="bold",
            color=WARNA["navy"])
    data = ["Citra optik\n(pantulan)", "Citra SAR\n(hamburan balik)", "DEM dan\nturunannya", "Citra multitemporal\n(respons vegetasi)"]
    for i, teks in enumerate(data):
        node(1.5, 43.0 - i * 12.0, teks, isi=WARNA["latar"], warna=WARNA["abu"], tinggi=8.0, lebar=18.0)
    ax.plot([21.0, 21.0], [11.0, 47.0], color=WARNA["abu"], lw=1.1)
    for y in (47.0, 35.0, 23.0, 11.0):
        ax.plot([19.5, 21.0], [y, y], color=WARNA["abu"], lw=1.1)

    # dua jalur
    lajur = [(31.0, "(a) Jalur langsung", WARNA["teal"], "hasil mewakili lapisan permukaan",
              ["Permukaan tanah\nterbuka", "Indikator spektral:\npantulan kanal, indeks,\nkedalaman serapan",
               "Sifat aktif secara spektral:\nbahan organik, lempung,\noksida besi, kelembapan"]),
             (4.0, "(b) Jalur tidak langsung", WARNA["oranye"], "dapat mencakup lapisan lebih dalam",
              ["Permukaan bervegetasi\natau sifat tanpa\nfitur spektral", "Indikator pengganti:\nrespons vegetasi, posisi\ntopografi, dinamika air",
               "Hubungan tanah–\nlingkungan\n(kovariat SCORPAN)"])]
    for y0, label, warna, catatan, isi_kotak in lajur:
        ax.add_patch(Rectangle((23.0, y0 - 1.0), 59.5, 23.0, fc=WARNA["latar"], ec="none", zorder=0))
        ax.text(24.5, y0 + 19.6, label, fontsize=10, fontweight="bold", color=warna, va="center")
        for k, teks in enumerate(isi_kotak):
            x = 24.5 + k * 19.5
            if k == 2:
                node(x, y0 + 4.0, teks, isi=warna, warna=warna, tebal=False, tinggi=10.5)
                ax.texts[-1].set_color("white")
            else:
                node(x, y0 + 4.75, teks)
            if k:
                ke(x - 2.0, y0 + 9.25, x, y0 + 9.25)
        ke(21.0, y0 + 9.25, 24.5, y0 + 9.25)
        ax.text(72.75, y0 + 1.9, catatan, ha="center", va="center", fontsize=7.6, color=warna, style="italic")

    # kalibrasi dan keluaran
    node(85.5, 24.5, "Kalibrasi dan\nvalidasi dengan\ndata tanah lapangan\ndan laboratorium", isi="#DCEAF7",
         tinggi=12.0, lebar=17.5)
    node(85.5, 4.0, "Peta estimasi\nsifat tanah", isi="#DCEAF7", tebal=True, tinggi=9.0, lebar=17.5)
    ke(81.5, 40.25, 92.0, 36.6, warna=WARNA["teal"])
    ke(81.5, 13.25, 92.0, 24.4, warna=WARNA["oranye"])
    ke(94.25, 24.4, 94.25, 13.1, warna=WARNA["navy"])
    simpan(fig, MODUL, "M4-G01_jalur-estimasi-sifat-tanah.png")


# ---------------------------------------------------------------- Gambar 4.2
def kurva_halus(titik, x):
    xs, ys = zip(*titik)
    y = PchipInterpolator(xs, ys)(x)
    k = np.ones(5) / 5
    return np.convolve(np.pad(y, 2, mode="edge"), k, mode="valid")


def g02_fitur_serapan():
    x = np.linspace(0.40, 2.50, 1400)
    seri = [
        ("Tanah berlempung, bahan organik dan besi rendah", WARNA["teal"],
         [(0.40, 0.22), (0.50, 0.32), (0.60, 0.42), (0.70, 0.50), (0.80, 0.56), (1.00, 0.63), (1.20, 0.68), (1.33, 0.70),
          (1.38, 0.62), (1.41, 0.585), (1.45, 0.63), (1.55, 0.69), (1.70, 0.71), (1.84, 0.70), (1.90, 0.58), (1.93, 0.555),
          (1.97, 0.60), (2.05, 0.66), (2.14, 0.665), (2.20, 0.575), (2.26, 0.645), (2.33, 0.63), (2.42, 0.59), (2.50, 0.55)]),
        ("Tanah kaya oksida besi", WARNA["merah"],
         [(0.40, 0.08), (0.45, 0.09), (0.50, 0.115), (0.55, 0.175), (0.60, 0.265), (0.65, 0.315), (0.70, 0.345),
          (0.75, 0.360), (0.80, 0.352), (0.88, 0.328), (0.96, 0.338), (1.04, 0.370), (1.12, 0.405), (1.25, 0.445),
          (1.33, 0.455), (1.38, 0.41), (1.41, 0.39), (1.45, 0.42), (1.55, 0.465), (1.70, 0.485), (1.84, 0.48), (1.90, 0.405),
          (1.93, 0.385), (1.97, 0.42), (2.05, 0.455), (2.14, 0.46), (2.20, 0.41), (2.26, 0.45), (2.35, 0.435), (2.50, 0.395)]),
        ("Tanah kaya bahan organik", WARNA["tanah"],
         [(0.40, 0.040), (0.50, 0.050), (0.60, 0.064), (0.70, 0.084), (0.80, 0.104), (1.00, 0.138), (1.20, 0.166),
          (1.33, 0.178), (1.38, 0.162), (1.41, 0.156), (1.45, 0.165), (1.60, 0.188), (1.84, 0.198), (1.90, 0.172),
          (1.93, 0.166), (1.97, 0.176), (2.10, 0.190), (2.20, 0.180), (2.30, 0.182), (2.50, 0.170)]),
    ]
    fig, (ax, bx) = plt.subplots(2, 1, figsize=(10, 6.6), sharex=True, gridspec_kw=dict(height_ratios=[3.3, 1.0], hspace=0.08))

    # (a) spektrum skematis
    xa = ax.get_xaxis_transform()    # x dalam µm, y dalam fraksi sumbu
    for a, b in SERAPAN_ATMOSFER:
        ax.axvspan(a, b, color=WARNA["abu_muda"], zorder=0)
        bx.axvspan(a, b, color=WARNA["abu_muda"], zorder=0)
    for xm in (1.40, 1.875):
        ax.text(xm, 0.015, "serapan\nuap air\natmosfer", transform=xa, ha="center", va="bottom", fontsize=7.3,
                color=WARNA["abu"])
    for (a, b) in ((0.48, 0.57), (0.85, 1.02)):
        ax.axvspan(a, b, ymin=0.855, ymax=0.88, color=WARNA["merah"], alpha=0.40, lw=0)
    fitur = [(0.525, "Fe³⁺\n(oksida besi)", WARNA["merah"]), (0.935, "Fe³⁺\n(oksida besi)", WARNA["merah"]),
             (1.40, "OH dan\nH₂O", WARNA["biru"]), (1.90, "H₂O", WARNA["biru"]), (2.20, "OH kisi\nmineral lempung", WARNA["teal"])]
    for xf, label, warna in fitur:
        if xf > 1.0:
            ax.axvline(xf, ymin=0.14, ymax=0.855, color=warna, lw=0.9, ls=":", zorder=1)
            ax.axvspan(xf - 0.012, xf + 0.012, ymin=0.855, ymax=0.88, color=warna, alpha=0.55, lw=0)
        ax.text(xf, 0.895, label, transform=xa, ha="center", va="bottom", fontsize=7.6, color=warna, linespacing=1.05)
    for label, warna, titik in seri:
        ax.plot(x, kurva_halus(titik, x), color=warna, lw=2.0, label=label, zorder=3)
    ax.annotate("bahan organik menurunkan pantulan,\nterutama pada 0,55–0,70 µm", xy=(0.63, 0.072), xytext=(0.80, 0.235),
                fontsize=7.6, color=WARNA["tanah"], arrowprops=dict(arrowstyle="-|>", color=WARNA["tanah"], lw=0.8))
    for a, b, label in ((0.40, 0.70, "Tampak"), (0.70, 1.30, "Inframerah dekat"), (1.30, 2.50, "Inframerah gelombang pendek (SWIR)")):
        ax.plot([a + 0.01, b - 0.01], [1.015, 1.015], transform=xa, color=WARNA["abu"], lw=0.8, clip_on=False)
        ax.text((a + b) / 2, 1.025, label, transform=xa, ha="center", va="bottom", fontsize=8.2, color=WARNA["abu"],
                clip_on=False)
    ax.set_ylim(0, 1.22)
    ax.set_yticks([])
    ax.set_ylabel("Pantulan relatif")
    ax.legend(loc="upper left", bbox_to_anchor=(0.005, 0.835), fontsize=8.6)
    ax.text(0.995, 0.015, "Ilustrasi skematis — bukan data terukur", transform=ax.transAxes, ha="right", va="bottom",
            fontsize=7.8, style="italic", color=WARNA["abu"])
    ax.text(-0.035, 1.0, "(a)", transform=ax.transAxes, fontsize=10, fontweight="bold", color=WARNA["navy"], va="bottom")

    # (b) posisi kanal
    for nama, a, b in KANAL_S2:
        isi = "#4F6D8F" if nama in ("B5", "B6", "B7") else WARNA["navy"]
        bx.add_patch(Rectangle((a, 1.55), b - a, 0.6, fc=isi, ec="white", lw=0.4))
    for nama, xl in (("B2", 0.49), ("B3", 0.56), ("B4", 0.665), ("B5–B7", 0.745), ("B8", 0.842), ("B11", 1.61), ("B12", 2.19)):
        bx.text(xl, 2.25, nama, ha="center", va="bottom", fontsize=7.4, color=WARNA["navy"])
    for w0 in np.arange(0.40, 2.50, 0.0105):
        bx.add_patch(Rectangle((w0, 0.35), 0.0085, 0.6, fc=WARNA["ungu"], ec="none"))
    bx.text(0.405, 2.95, "Sentinel-2 MSI: kanal lebar (B12 selebar ±180 nm)", fontsize=8.2, va="bottom", color=WARNA["navy"])
    bx.text(0.405, 1.05, "Hiperspektral (mis. PRISMA): ±240 kanal bersambung, lebar ≤ 15 nm", fontsize=8.2, va="bottom",
            color=WARNA["ungu"])
    bx.set_ylim(0, 3.6)
    bx.set_yticks([])
    bx.spines["left"].set_visible(False)
    bx.set_xlim(0.40, 2.50)
    bx.xaxis.set_major_locator(MultipleLocator(0.5))
    bx.xaxis.set_minor_locator(MultipleLocator(0.1))
    bx.xaxis.set_major_formatter(KOMA)
    bx.set_xlabel("Panjang gelombang (µm)")
    bx.text(-0.035, 1.0, "(b)", transform=bx.transAxes, fontsize=10, fontweight="bold", color=WARNA["navy"], va="bottom")
    simpan(fig, MODUL, "M4-G02_fitur-serapan-spektrum-tanah.png")


# ---------------------------------------------------------------- Gambar 4.3
def matahari(ax, x, y, r=2.6):
    for a in np.linspace(0, 2 * np.pi, 12, endpoint=False):
        ax.plot([x + 1.25 * r * np.cos(a), x + 1.7 * r * np.cos(a)],
                [y + 1.25 * r * np.sin(a), y + 1.7 * r * np.sin(a)], color=WARNA["kuning"], lw=1.5, zorder=3)
    ax.add_patch(Circle((x, y), r, fc=WARNA["kuning"], ec="#E0A82E", lw=1, zorder=4))


def satelit(ax, x, y, s=0.8):
    ax.add_patch(Rectangle((x - 1.6 * s, y - 1.2 * s), 3.2 * s, 2.4 * s, fc="#C9CED6", ec=WARNA["navy"], lw=1, zorder=5))
    for arah in (-1, 1):
        x0 = x + 1.6 * s if arah > 0 else x - 1.6 * s - 4.6 * s
        ax.add_patch(Rectangle((x0, y - 0.9 * s), 4.6 * s, 1.8 * s, fc="#2F5D8C", ec=WARNA["navy"], lw=0.8, zorder=5))


def pohon(ax, x, y, s=1.0):
    ax.add_patch(Rectangle((x - 0.25 * s, y), 0.5 * s, 2.6 * s, fc="#6B4A2B", ec="none", zorder=4))
    for dx, dy, r in [(0, 3.9, 1.8), (-1.2, 3.1, 1.3), (1.2, 3.1, 1.3)]:
        ax.add_patch(Circle((x + dx * s, y + dy * s), r * s, fc=WARNA["hijau"], ec="#3A7A20", lw=0.6, zorder=4))


def g03_faktor_sinyal_tanah():
    fig, ax = kanvas(10, 5.6, (0, 127), (-10.5, 64))
    ax.add_patch(Rectangle((0, 16), 100, 48, fc="#F7FAFD", ec="none", zorder=0))
    ax.add_patch(Rectangle((0, 38), 100, 10, fc="#EEF5FB", ec="none", zorder=0))
    rng = np.random.default_rng(5)
    ax.scatter(rng.uniform(1, 99, 150), rng.uniform(38.5, 47.5, 150), s=3, color="#A9C1DA", zorder=1)
    ax.text(58.0, 43.0, "Atmosfer: hamburan dan serapan\noleh aerosol dan uap air", ha="left", va="center", fontsize=8,
            color=WARNA["abu"], style="italic", zorder=2, bbox=dict(boxstyle="round,pad=0.25", fc="#EEF5FB", ec="none"))
    nomor(ax, 55.4, 43.0, 1)

    # medan: bukit di kiri, dataran di kanan
    bukit = np.array([(0, 16), (0, 19), (7, 24), (14, 30), (20, 31.5), (26, 29), (32, 22.5), (38, 17.5), (42, 16)])
    terang = np.array([(0, 16), (0, 19), (7, 24), (14, 30), (20, 31.5), (20, 16)])
    gelap = np.array([(20, 31.5), (26, 29), (32, 22.5), (38, 17.5), (42, 16), (20, 16)])
    ax.add_patch(Polygon(terang, fc="#F0E1C8", ec="none", zorder=2.1))
    ax.add_patch(Polygon(gelap, fc="#B9A182", ec="none", zorder=2.1))
    ax.plot(bukit[:, 0], bukit[:, 1], color=WARNA["tanah"], lw=1.2, zorder=3)
    ax.text(8.5, 19.6, "lereng\nterkena sinar", ha="center", fontsize=7.6, color=WARNA["teks"], zorder=4)
    ax.text(30.5, 18.0, "lereng\nterbayangi", ha="center", fontsize=7.6, color="white", zorder=4)
    nomor(ax, 33.5, 26.5, 2)

    # tanah di bawah permukaan dan jenis permukaan pada dataran
    ax.add_patch(Rectangle((0, 2), 100, 14, fc="#CDB89A", ec="none", zorder=1.5))
    seg = [(42, 52, "#E3C79F"), (52, 61, "#9C7650"), (61, 69, "#CDB27A"), (69, 77, "#B79E7C")]
    for x0, x1, isi in seg:
        ax.add_patch(Rectangle((x0, 14.6), x1 - x0, 1.4, fc=isi, ec="none", zorder=2.5))
    for k in range(6):
        ax.plot([52.6 + k * 1.4, 53.6 + k * 1.4], [15.3, 15.9], color="#6E5236", lw=0.9, zorder=3)
    for k in range(14):
        xx = 61.4 + k * 0.53
        ax.plot([xx, xx + 0.9], [16.0, 16.9 + 0.3 * (k % 3)], color="#A9863F", lw=1.0, zorder=3)
    for xp in (71.4, 75.0):
        pohon(ax, xp, 16.0, 1.1)
    ax.plot([42, 100], [16, 16], color=WARNA["tanah"], lw=1.2, zorder=3)
    for xm, label in ((47.0, "tanah\nterbuka\nkering"), (56.5, "tanah\nlembap,\nberkerak"), (65.0, "serasah,\nsisa\ntanaman"),
                      (73.0, "tajuk\nvegetasi")):
        ax.text(xm, 10.6, label, ha="center", va="center", fontsize=7.3, color=WARNA["teks"], zorder=4, linespacing=1.05)
    nomor(ax, 56.5, 20.0, 4)
    nomor(ax, 66.0, 21.8, 3)

    # satu piksel campuran
    ax.plot([52, 52, 77, 77], [25.4, 26.6, 26.6, 25.4], color=WARNA["navy"], lw=1.1, zorder=4)
    ax.text(64.5, 27.4, "satu piksel: campuran beberapa permukaan", ha="center", va="bottom", fontsize=7.6,
            color=WARNA["navy"], zorder=5, bbox=dict(boxstyle="round,pad=0.15", fc="#F7FAFD", ec="none"))
    nomor(ax, 79.6, 26.0, 5)

    # sumber energi, sensor, dan lintasan energi
    matahari(ax, 6.5, 57.0)
    satelit(ax, 46.5, 58.5)
    ax.text(46.5, 61.6, "Sensor optik", ha="center", fontsize=8.5)
    satelit(ax, 89.0, 58.5)
    ax.text(89.0, 61.6, "Sensor SAR", ha="center", fontsize=8.5)
    for xt, yt in ((10.0, 25.6), (47.0, 16.4)):
        panah(ax, 9.0, 53.0, xt, yt, warna=WARNA["oranye"], lw=1.4)
    for xs, ys, lebar in ((10.0, 25.6, 2.0), (30.0, 25.0, 0.6), (47.0, 16.4, 2.0), (65.0, 17.6, 1.0)):
        panah(ax, xs, ys, 46.0, 55.6, warna=WARNA["teal"], lw=lebar)
    ax.text(48.2, 31.0, "pantulan", fontsize=7.6, color=WARNA["teal"], ha="left")
    for k in range(3):
        panah(ax, 87.6 + k * 1.4, 55.5, 85.0 + k * 3.0, 16.4, warna=WARNA["ungu"], lw=0.9, putus=True, skala=8)
    ax.text(93.0, 30.0, "gelombang\nmikro", fontsize=7.6, color=WARNA["ungu"], ha="left")

    # panel kedalaman yang terwakili
    ax.add_patch(Rectangle((101.5, 2.0), 25.5, 62.0, fc=WARNA["latar"], ec="none", zorder=0))
    ax.text(114.25, 59.5, "Kedalaman yang\nterwakili", ha="center", va="center", fontsize=8.8, fontweight="bold",
            color=WARNA["navy"])
    nomor(ax, 114.25, 53.6, 6)
    atas, skala = 47.0, 1.3          # 0 cm pada y = 47; 1 cm = 1,3 satuan gambar
    ax.add_patch(Rectangle((106.0, atas - 30 * skala), 5.0, 30 * skala, fc="#CDB89A", ec=WARNA["tanah"], lw=0.8))
    for z in (0, 5, 15, 30):
        y = atas - z * skala
        ax.plot([105.2, 111.0], [y, y], color=WARNA["tanah"], lw=0.8, ls="--" if z else "-")
        ax.text(104.8, y, f"{z} cm" if z == 30 else f"{z}", ha="right", va="center", fontsize=7.2, color=WARNA["teks"])
    ax.add_patch(Rectangle((111.8, atas - 0.6), 1.0, 0.6, fc=WARNA["teal"], ec="none"))
    ax.add_patch(Rectangle((113.4, atas - 5 * skala), 1.0, 5 * skala, fc=WARNA["ungu"], alpha=0.75, ec="none"))
    ax.add_patch(Rectangle((115.0, atas - 30 * skala), 1.0, 30 * skala, fc=WARNA["navy"], ec="none"))
    ax.text(116.8, atas - 0.3, "optik: permukaan\npaling atas", fontsize=6.8, color="#0F5E55", va="center",
            linespacing=1.05)
    ax.text(116.8, atas - 5.6, "gelombang\nmikro pita L:\nbeberapa cm\nteratas", fontsize=7.0, color="#4B3575",
            va="center", linespacing=1.05)
    ax.text(116.8, atas - 21.0, "interval\nkedalaman\nDSM, mis.\nGlobalSoilMap\n0–5, 5–15,\n15–30 cm", fontsize=7.0,
            color=WARNA["navy"], va="center", linespacing=1.05)

    # keterangan nomor
    ket = ["Atmosfer", "Iluminasi dan topografi", "Penutup permukaan", "Kondisi permukaan tanah",
           "Resolusi sensor dan piksel campuran", "Kedalaman yang terwakili"]
    for i, teks in enumerate(ket):
        kol, bar = divmod(i, 2)
        x0, y0 = 3.0 + kol * 42.0, -2.6 - bar * 4.8
        nomor(ax, x0, y0, i + 1, r=1.5, ukuran=8)
        ax.text(x0 + 2.8, y0, teks, va="center", fontsize=8.5)
    simpan(fig, MODUL, "M4-G03_faktor-sinyal-tanah.png")


if __name__ == "__main__":
    gaya.atur()
    g01_jalur_estimasi()
    g02_fitur_serapan()
    g03_faktor_sinyal_tanah()
