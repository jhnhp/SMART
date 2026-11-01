"""Gambar Modul 7 — Proximal Soil Sensing.

Jalankan: python3 Output/scripts/gambar_modul_7.py
Keluaran: Output/assets/modul-7/M7-Gxx_*.png
Gambar 7.1, 7.2, dan 7.4 adalah diagram konseptual; Gambar 7.3 dihitung dari spektrum sintetis.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.ticker import FuncFormatter, MultipleLocator
from scipy.signal import savgol_filter
from scipy.spatial import ConvexHull

import gaya
from gaya import WARNA, kanvas, kotak, panah, simpan

MODUL = "modul-7"
KOMA1 = FuncFormatter(lambda v, _: f"{v:.1f}".replace(".", ","))


# ---------------------------------------------------------------- Gambar 7.1
def g01_sensor_spektrum():
    fig, ax = kanvas(10, 4.6, (0, 104), (0, 50))
    wilayah = [("Sinar gamma", "#5B3C88"), ("Sinar-X", "#7B5EA7"), ("Ultraungu\ndan tampak", "#3B82C4"),
               ("Inframerah\ndekat", "#C0392B"), ("Inframerah\ntengah", "#E07B39"), ("Gelombang\nmikro", "#8C5A3C"),
               ("Frekuensi\nrendah (kHz)", "#6B7280")]
    x0, lebar = 2, 14
    for i, (nama, warna) in enumerate(wilayah):
        ax.add_patch(Rectangle((x0 + i * lebar, 36), lebar - 0.4, 7.5, fc=warna, ec="none", alpha=0.85))
        ax.text(x0 + i * lebar + (lebar - 0.4) / 2, 39.75, nama, ha="center", va="center", fontsize=8.2, color="white",
                fontweight="bold", linespacing=1.05)
    panah(ax, 100, 46.5, 2, 46.5, warna=WARNA["abu"], lw=1.0, skala=9)
    ax.text(51, 48.2, "energi makin tinggi, panjang gelombang makin pendek", ha="center", fontsize=7.8, color=WARNA["abu"])
    sensor = [(0, "Spektrometer\nsinar gamma", "K, U, Th: bahan induk,\ntekstur, lempung"),
              (1, "XRF portabel\n(pXRF)", "kadar total unsur\n(nomor atom ≥ 12)"),
              (2, "LIBS", "unsur, termasuk\nnomor atom < 12"),
              (3, "Spektroskopi\nvis-NIR", "bahan organik, lempung,\noksida besi, air"),
              (4, "Spektroskopi\nMIR", "mineral dan senyawa\norganik (lebih tajam)"),
              (6, "Induksi\nelektromagnetik", "ECa: salinitas, tekstur,\nkelembapan, KTK")]
    for i, nama, ket in sensor:
        cx = x0 + i * lebar + (lebar - 0.4) / 2
        kotak(ax, cx - 6.4, 21, 12.8, 9, nama, isi=WARNA["putih"], warna=WARNA["navy"], ukuran=7.6, r=0.6, lw=0.9)
        ax.text(cx, 18.6, ket, ha="center", va="top", fontsize=7.0, color=WARNA["teks"], linespacing=1.1)
        panah(ax, cx, 35.8, cx, 30.2, warna=WARNA["abu"], lw=0.9, skala=8)
    ax.add_patch(Rectangle((2, 1), 97.6, 7.0, fc=WARNA["latar"], ec=WARNA["abu_muda"], lw=0.8))
    ax.text(4, 4.5, "Di luar spektrum elektromagnetik:", fontsize=8, fontweight="bold", color=WARNA["navy"], va="center")
    ax.text(31, 4.5, "resistivitas dengan elektrode galvanik (ECa)  •  elektrode ion selektif (pH, K, nitrat)  "
            "•  penetrometer", fontsize=7.8, va="center", color=WARNA["teks"])
    simpan(fig, MODUL, "M7-G01_sensor-pss-pada-spektrum-elektromagnetik.png")


# ---------------------------------------------------------------- Gambar 7.2
def g02_kedalaman_informasi():
    """Kedalaman yang diwakili tiap teknik, digambar sebagai profil tanah (kedalaman ke bawah)."""
    rj, pss = WARNA["biru"], WARNA["tanah"]
    lebar = 0.46
    fig, ax = plt.subplots(figsize=(10, 6.0))
    fig.subplots_adjust(left=0.07, right=0.99, top=0.83, bottom=0.08)
    ax.axhspan(0, 118, color="#F7F1EA", zorder=-2)
    ax.axhline(0, color=WARNA["tanah"], lw=1.4, zorder=1)

    def batang(x, atas, bawah, warna, w=lebar):
        ax.add_patch(Rectangle((x - w / 2, atas), w, bawah - atas, fc=warna, ec="none", alpha=0.9, zorder=3))

    def ket(x, y, teks):
        ax.text(x, y, teks, ha="center", va="top", fontsize=7.6, color=WARNA["teks"], linespacing=1.15, zorder=4)

    batang(0, 0, 0.9, rj)                                        # citra optik: hanya permukaan
    ket(0, 3, "hanya permukaan;\nradiasi menembus\n10–50 µm")
    for i, a in enumerate(np.linspace(0.9, 0.05, 30)):            # pita L: beberapa cm teratas, batas tidak tegas
        ax.add_patch(Rectangle((1 - lebar / 2, i * 0.2), lebar, 0.2, fc=rj, ec="none", alpha=a, zorder=3))
    ket(1, 8.5, "beberapa cm\nteratas")
    batang(2.4, 0, 20, pss)
    ket(2.4, 23, "sering hanya\n0–20 cm")
    batang(3.4, 8.5, 11.5, pss)                                   # ISE: sampel diambil pada ±10 cm
    ax.plot([3.4, 3.4], [0, 8.5], color=pss, lw=1.0, ls=":", zorder=3)
    ket(3.4, 14.5, "sampel diambil\npada sekitar\n10 cm")
    batang(4.4, 0, 50, pss)
    ket(4.4, 53, "sekitar 95%\nradiasi berasal\ndari 0–50 cm")
    batang(5.2, 0, 30, pss, w=0.3)
    batang(5.6, 0, 90, pss, w=0.3)
    ket(5.2, 33, "dangkal\n0–30 cm")
    ket(5.6, 93, "dalam\n0–90 cm")
    ket(5.4, 104, "pembacaan dalam\njuga memuat\nlapisan dangkal")
    batang(6.6, 0, 100, pss)
    for y in np.arange(2, 100, 2):                                # inti 1 m diukur tiap 2 cm
        ax.plot([6.6 - lebar / 2, 6.6 + lebar / 2], [y, y], color="white", lw=0.45, zorder=3.5)
    ket(6.6, 103, "inti 1 m,\ndiukur tiap 2 cm")

    ax.axhline(30, color=WARNA["abu"], lw=0.9, ls="--", zorder=2)
    ax.text(-0.42, 28.8, "30 cm: kedalaman minimum yang\ndianjurkan untuk akuntansi\nkarbon tanah", fontsize=7.4,
            color=WARNA["abu"], style="italic", va="bottom", linespacing=1.1)

    nama = ["Citra optik\n(satelit)", "Gelombang\nmikro pita L\n(satelit)", "Spektrometer\nvis-NIR\nbergerak",
            "Elektrode ion\nselektif (pH,\nsampel bergerak)", "Spektrometer\nsinar gamma", "ECa\n(dangkal dan\ndalam)",
            "Pemindai inti\ntanah vis-NIR"]
    ax.set_xticks([0, 1, 2.4, 3.4, 4.4, 5.4, 6.6])
    ax.set_xticklabels(nama, fontsize=8.2, linespacing=1.1)
    ax.xaxis.tick_top()
    ax.tick_params(axis="x", length=0, pad=6)
    for teks, x0, x1, warna in (("Penginderaan jauh", -0.35, 1.35, rj), ("Proximal soil sensing", 2.05, 6.95, pss)):
        ax.plot([x0, x1], [1.15, 1.15], transform=ax.get_xaxis_transform(), color=warna, lw=2.2, clip_on=False)
        ax.text((x0 + x1) / 2, 1.165, teks, transform=ax.get_xaxis_transform(), ha="center", va="bottom", fontsize=9.6,
                fontweight="bold", color=warna, style="italic" if "soil" in teks else "normal")
    ax.set_xlim(-0.5, 7.0)
    ax.set_ylim(118, -2)
    ax.yaxis.set_major_locator(MultipleLocator(20))
    ax.set_ylabel("Kedalaman tanah (cm)")
    for s in ("top", "right", "bottom"):
        ax.spines[s].set_visible(False)
    ax.text(0.0, -0.035, "Diagram konseptual; kedalaman merupakan contoh dari pustaka dan bergantung pada alat serta "
            "konfigurasinya.", transform=ax.transAxes, fontsize=7.4, style="italic", color=WARNA["abu"], va="top")
    simpan(fig, MODUL, "M7-G02_kedalaman-informasi-berbagai-teknik.png")


# ---------------------------------------------------------------- Gambar 7.3
def spektrum_sintetis(x, rng):
    """Spektrum pantulan sintetis: garis dasar, serapan Fe, air/OH, lempung, dan pengaruh hamburan."""
    hasil = []
    for k in range(6):
        bo = rng.uniform(0.6, 1.4)          # bahan organik (menggelapkan tampak)
        fe = rng.uniform(0.2, 1.0)
        lempung = rng.uniform(0.3, 1.0)
        air = rng.uniform(0.3, 1.0)
        dasar = 0.18 + 0.28 * (1 - np.exp(-(x - 0.35) / 0.45)) - 0.04 * bo * np.exp(-(x - 0.4) / 0.25)
        serap = (0.05 * fe * np.exp(-0.5 * ((x - 0.90) / 0.07) ** 2)
                 + 0.06 * air * np.exp(-0.5 * ((x - 1.41) / 0.025) ** 2)
                 + 0.10 * air * np.exp(-0.5 * ((x - 1.91) / 0.035) ** 2)
                 + 0.06 * lempung * np.exp(-0.5 * ((x - 2.205) / 0.018) ** 2))
        r = dasar - serap
        r = r * rng.uniform(0.75, 1.25) + rng.uniform(-0.03, 0.03)     # hamburan (perkalian) dan pergeseran
        hasil.append(np.clip(r + rng.normal(0, 0.001, x.size), 0.02, 0.9))
    return np.array(hasil)


def kontinum(x, r):
    titik = np.c_[x, r]
    hull = ConvexHull(np.vstack([titik, [x[-1], 0], [x[0], 0]]))
    atas = sorted(i for i in hull.vertices if i < x.size)
    return np.interp(x, x[atas], r[atas])


def g03_praolah_spektrum():
    rng = np.random.default_rng(21)
    x = np.linspace(0.40, 2.45, 1026)
    R = spektrum_sintetis(x, rng)
    A = np.log10(1 / R)
    snv = (A - A.mean(axis=1, keepdims=True)) / A.std(axis=1, keepdims=True)
    d1 = savgol_filter(A, 31, 2, deriv=1, axis=1)
    halus = savgol_filter(R, 21, 2, axis=1)
    cr = np.array([r / kontinum(x, r) for r in halus])
    warna = plt.get_cmap("viridis")(np.linspace(0.05, 0.85, R.shape[0]))
    fig, axs = plt.subplots(2, 2, figsize=(10, 6.0), sharex=True)
    fig.subplots_adjust(left=0.07, right=0.99, top=0.93, bottom=0.09, hspace=0.32, wspace=0.18)
    data = [(R, "(a) Pantulan asli", "Pantulan"), (snv, "(b) Absorbans log(1/R) setelah SNV", "Nilai SNV"),
            (d1, "(c) Turunan pertama Savitzky–Golay", "Turunan pertama"), (cr, "(d) Penghilangan kontinum", "R / kontinum")]
    for ax, (d, judul, ylabel) in zip(axs.ravel(), data):
        for i in range(d.shape[0]):
            ax.plot(x, d[i], color=warna[i], lw=1.1)
        ax.set_title(judul, fontsize=9.6, loc="left")
        ax.set_ylabel(ylabel, fontsize=8.6)
        ax.tick_params(labelsize=8)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}".replace(".", ",")))
        for xf in (0.90, 1.41, 1.91, 2.205):
            ax.axvline(xf, color=WARNA["abu"], lw=0.6, ls=":", zorder=0)
    for ax in axs[1]:
        ax.set_xlabel("Panjang gelombang (µm)", fontsize=8.8)
        ax.xaxis.set_major_locator(MultipleLocator(0.5))
        ax.xaxis.set_major_formatter(KOMA1)
    axs[0, 0].text(0.99, 0.04, "Data sintetis", transform=axs[0, 0].transAxes, ha="right", fontsize=7.6, style="italic",
                   color=WARNA["abu"])
    for xf, lbl in ((0.90, "Fe"), (1.41, "OH, H₂O"), (1.91, "H₂O"), (2.205, "lempung")):
        axs[0, 1].text(xf, 0.93, lbl, transform=axs[0, 1].get_xaxis_transform(), ha="center", va="bottom", fontsize=7.4,
                       color=WARNA["abu"], bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none"))
    simpan(fig, MODUL, "M7-G03_praolah-spektrum-sintetis.png")


# ---------------------------------------------------------------- Gambar 7.4
def g04_alur_pemodelan():
    fig, ax = kanvas(10, 6.2, (0, 104), (0, 64))
    abu = WARNA["abu"]

    def node(x, y, teks, w=22, h=6.0, isi=WARNA["putih"], warna=WARNA["navy"], tebal=False):
        kotak(ax, x, y, w, h, teks, isi=isi, warna=warna, ukuran=7.8, tebal=tebal, r=0.7, lw=1.0)

    def ke(x1, y1, x2, y2, putus=False):
        panah(ax, x1, y1, x2, y2, warna=abu, lw=1.0, skala=9, putus=putus)

    for x, w, judul in ((1, 31, "1. Pengukuran"), (34, 39, "2. Pemodelan"), (75, 28, "3. Prediksi")):
        ax.add_patch(Rectangle((x, 1), w, 61, fc=WARNA["latar"], ec="none", zorder=0))
        ax.text(x + w / 2, 59.6, judul, ha="center", fontsize=10, fontweight="bold", color=WARNA["navy"])
    node(5, 47, "Spektrum semua\nsampel wilayah kajian\n(protokol baku)", w=23, h=8, isi="#DCEAF7")
    node(5, 34, "Pemeriksaan\npencilan spektrum", w=23)
    node(3, 20, "Set latih\n(mis. Kennard–Stone)", w=13)
    node(17, 20, "Set validasi\n(acak)", w=12)
    node(5, 6, "Analisis laboratorium\nset latih dan validasi", w=23, isi="#F3E3CF", warna=WARNA["tanah"])
    ke(16.5, 47, 16.5, 40.1), ke(16.5, 34, 9.5, 26.1), ke(16.5, 34, 23, 26.1)
    ke(9.5, 20, 12, 12.1), ke(23, 20, 21, 12.1)
    langkah = ["Praolah spektrum\n(absorbans, penghalusan,\nturunan, koreksi air)", "Analisis pencilan\ndan data berpengaruh",
               "Pemodelan spektroskopi\n(PLSR, pembelajaran mesin)", "Optimasi dengan\nvalidasi silang dan diagnosis",
               "Penilaian akurasi pada\nset validasi (RMSE, R², RPD)"]
    for i, t in enumerate(langkah):
        y = 47 - i * 10.5
        node(39, y, t, w=29, h=7.5, isi="#EAF3E2" if i == 2 else WARNA["putih"], warna=WARNA["teal"] if i == 2 else WARNA["navy"])
        if i:
            ke(53.5, y + 10.5, 53.5, y + 7.6)
    ke(28.1, 9, 39, 50.5)
    node(78, 47, "Spektrum lapangan\natau sampel baru", w=22, h=8, isi="#DCEAF7")
    node(78, 33, "Praolah yang sama\ndengan set latih", w=22, h=7.5)
    node(78, 17, "Estimasi sifat tanah\ndan ketidakpastiannya", w=22, h=8, isi="#DCEAF7", tebal=True)
    ke(89, 47, 89, 40.6), ke(89, 33, 89, 25.1)
    ke(68.1, 6.2 + 3.7, 78, 21, putus=True)
    ax.text(76.5, 10.5, "model\nteroptimasi", fontsize=7.4, color=abu, ha="left", style="italic")
    simpan(fig, MODUL, "M7-G04_alur-pemodelan-spektroskopi.png")


if __name__ == "__main__":
    gaya.atur()
    g01_sensor_spektrum()
    g02_kedalaman_informasi()
    g03_praolah_spektrum()
    g04_alur_pemodelan()
