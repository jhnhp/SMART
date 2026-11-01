"""Gambar Modul 8 — Pemodelan Digital Soil Mapping.

Jalankan: python3 Output/scripts/gambar_modul_8.py
Keluaran: Output/assets/modul-8/M8-Gxx_*.png
Gambar 8.3 adalah diagram konseptual; Gambar 8.1, 8.2, 8.4, dan 8.5 dihitung dari data sintetis.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle
from matplotlib.ticker import FuncFormatter, MultipleLocator
from scipy import ndimage
from scipy.cluster.vq import kmeans2
from scipy.spatial import cKDTree

import gaya
from gaya import WARNA, kanvas, kotak, panah, simpan

MODUL = "modul-8"
KOMA = lambda d: FuncFormatter(lambda v, _: f"{v:.{d}f}".replace(".", ",").replace("-", "−"))  # noqa: E731
# Palet kategorik tervalidasi (lima slot pertama palet acuan dataviz)
KATEGORI = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
PENANDA = ["o", "s", "^", "D", "v"]


def ramp(nama, terang, gelap):
    return LinearSegmentedColormap.from_list(nama, [terang, gelap])


def koma(v, d=1):
    return f"{v:.{d}f}".replace(".", ",")


# ---------------------------------------------------------------- lanskap sintetis
def lanskap(n=140, sel=30.0, seed=4):
    """Elevasi sintetis dua bukit dengan lembah di antaranya; sel 30 m."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:n, 0:n] / (n - 1)
    z = (55 + 14 * (1 - yy)
         + 28 * np.exp(-((xx - 0.25) ** 2 + (yy - 0.30) ** 2) / 0.035)
         + 22 * np.exp(-((xx - 0.78) ** 2 + (yy - 0.72) ** 2) / 0.045)
         - 9 * np.exp(-((xx - 0.52 - 0.15 * (yy - 0.5)) ** 2) / 0.006)
         + ndimage.gaussian_filter(rng.normal(0, 1, (n, n)), 6) * 9)
    gy, gx = np.gradient(z, sel)
    lereng = np.hypot(gx, gy)
    return z, lereng, xx, yy, rng


def akumulasi_mfd(z, p=1.1):
    """Luas tangkapan (jumlah sel) dengan aliran banyak arah: setiap sel membagi alirannya ke semua tetangga
    yang lebih rendah sebanding dengan (penurunan)^p, diproses dari sel tertinggi ke terendah."""
    n, m = z.shape
    akum = np.ones(n * m)
    zf = z.ravel()
    tetangga = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for idx in np.argsort(zf)[::-1]:
        i, j = divmod(idx, m)
        tujuan, bobot = [], []
        for di, dj in tetangga:
            ii, jj = i + di, j + dj
            if 0 <= ii < n and 0 <= jj < m:
                turun = (zf[idx] - z[ii, jj]) / np.hypot(di, dj)
                if turun > 0:
                    tujuan.append(ii * m + jj)
                    bobot.append(turun ** p)
        if tujuan:
            b = np.array(bobot)
            akum[tujuan] += akum[idx] * b / b.sum()
    return akum.reshape(n, m)


def twi(z, lereng, sel=30.0):
    a = akumulasi_mfd(z) * sel         # luas tangkapan spesifik (m²/m)
    return np.log(a / np.maximum(lereng, 0.002))


def blok_kebun(xx, yy, rng, kolom=6, baris=6):
    """Indeks tajuk per blok kebun (umur tanam berbeda) dengan jalan di antara blok."""
    bx = np.minimum((xx * kolom).astype(int), kolom - 1)
    by = np.minimum((yy * baris).astype(int), baris - 1)
    blok = by * kolom + bx
    nilai = rng.uniform(0.62, 0.86, kolom * baris)
    nilai[[8, 27]] = rng.uniform(0.30, 0.38, 2)          # blok tanaman muda
    nilai[21] = 0.18                                     # blok peremajaan (tanah terbuka)
    indeks = nilai[blok] + rng.normal(0, 0.015, xx.shape)
    jalan = (np.abs(xx * kolom - np.round(xx * kolom)) < 0.03) | (np.abs(yy * baris - np.round(yy * baris)) < 0.03)
    indeks[jalan] = 0.12
    return indeks, jalan


# ---------------------------------------------------------------- Gambar 8.1
def g01_kovariat():
    z, lereng, xx, yy, rng = lanskap()
    t = twi(z, lereng)
    ndvi, jalan = blok_kebun(xx, yy, rng)
    lembah = 0.52 + 0.15 * (yy - 0.5)
    geologi = np.where(xx < lembah, 0, 1)                         # dua satuan batuan di kedua bukit
    geologi[ndimage.gaussian_filter(z, 2) < np.quantile(z, 0.2)] = 2   # endapan aluvial di bagian terendah
    n = z.shape[0]
    titik = np.column_stack([rng.uniform(4, n - 5, 40), rng.uniform(4, n - 5, 40)])

    peta = [("(a) Elevasi (r)", z, ramp("el", "#F3E3CF", WARNA["tanah"]), "m", 0),
            ("(b) Kemiringan lereng (r)", lereng * 100, ramp("lr", "#FDEBD9", "#B4501A"), "%", 0),
            ("(c) Indeks kebasahan topografi (r)", t, ramp("tw", WARNA["biru_muda"], WARNA["navy"]), "TWI", 0),
            ("(d) Indeks vegetasi tajuk (o)", ndvi, ramp("nd", "#EEF6E8", "#2F6B1F"), "NDVI", 1)]
    fig, axs = plt.subplots(2, 3, figsize=(10, 7.0))
    fig.subplots_adjust(left=0.02, right=0.98, top=0.95, bottom=0.08, wspace=0.08, hspace=0.32)
    for ax, (judul, data, cmap, satuan, d) in zip(axs.ravel()[:4], peta):
        im = ax.imshow(data, cmap=cmap, interpolation="nearest")
        cb = fig.colorbar(im, ax=ax, orientation="horizontal", fraction=0.046, pad=0.03)
        cb.ax.tick_params(labelsize=7.2)
        cb.ax.xaxis.set_major_formatter(KOMA(d))
        cb.set_label(satuan, fontsize=7.6)
        ax.set_title(judul, fontsize=9.2, pad=4)
    ax = axs[1, 1]
    warna_geo = ["#E8D3B9", "#CFE5D6", "#DCD3EC"]
    ax.imshow(geologi, cmap=ListedColormap(warna_geo), interpolation="nearest")
    for k, nama in enumerate(["Satuan A", "Satuan B", "Aluvium"]):
        iy, ix = np.argwhere(geologi == k).mean(axis=0)
        ax.text(ix, iy, nama, ha="center", va="center", fontsize=8, color=WARNA["teks"],
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.7))
    ax.set_title("(e) Satuan geologi (p)", fontsize=9.2, pad=4)
    cb_kosong = fig.colorbar(plt.cm.ScalarMappable(cmap=ListedColormap(warna_geo)), ax=ax, orientation="horizontal",
                             fraction=0.046, pad=0.03)
    cb_kosong.ax.set_visible(False)                      # menjaga ukuran panel tetap sama
    ax = axs[1, 2]
    sinar = np.clip(0.75 + 0.35 * (np.gradient(z)[1] - np.gradient(z)[0]) / 2.0, 0, 1)
    ax.imshow(sinar, cmap="gray", vmin=0, vmax=1.1, interpolation="nearest")
    ax.imshow(np.ma.masked_where(~jalan, jalan), cmap=ListedColormap(["#FFFFFF"]), alpha=0.6, interpolation="nearest")
    ax.scatter(titik[:, 0], titik[:, 1], s=22, c=WARNA["oranye"], edgecolors="white", linewidths=0.8, zorder=3)
    ax.set_title("(f) Titik sampel tanah", fontsize=9.2, pad=4)
    cb_kosong = fig.colorbar(plt.cm.ScalarMappable(cmap="gray"), ax=ax, orientation="horizontal", fraction=0.046,
                             pad=0.03)
    cb_kosong.ax.set_visible(False)
    for a in axs.ravel():
        a.set_xticks([]), a.set_yticks([])
    fig.text(0.02, 0.012, "Data sintetis; huruf dalam kurung = faktor SCORPAN. Garis putih pada (d) dan (f) = jalan kebun; "
             "nilai semua lapisan diambil di setiap titik pada (f).", fontsize=7.4, style="italic", color=WARNA["abu"])
    simpan(fig, MODUL, "M8-G01_kovariat-scorpan-sebagai-lapisan-raster.png")


# ---------------------------------------------------------------- Gambar 8.2
def sampel_mengelompok(rng):
    """Sampel warisan yang mengelompok di beberapa lokasi survei dan di sepanjang jalan."""
    pusat = np.array([[0.7, 0.6], [1.6, 2.3], [2.9, 0.9], [3.4, 2.4]])
    kelompok = np.vstack([c + rng.normal(0, 0.18, (14, 2)) for c in pusat])
    jalan = np.column_stack([rng.uniform(0.2, 3.8, 24), np.full(24, 1.5) + rng.normal(0, 0.05, 24)])
    xy = np.vstack([kelompok, jalan])
    return np.clip(xy, [0.08, 0.08], [3.92, 2.92])


def latar_kebun(ax):
    ax.add_patch(Rectangle((0, 0), 4, 3, fc=WARNA["latar"], ec=WARNA["abu_muda"], lw=0.8, zorder=0))
    for x in np.arange(0.5, 4, 0.5):
        ax.plot([x, x], [0, 3], color="white", lw=1.4, zorder=0.5)
    for y in np.arange(0.5, 3, 0.5):
        ax.plot([0, 4], [y, y], color="white", lw=1.4, zorder=0.5)
    ax.set_xlim(-0.05, 4.05)
    ax.set_ylim(-0.05, 3.05)
    ax.set_aspect("equal")
    ax.set_xticks([]), ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


def g02_pembagian_data():
    rng = np.random.default_rng(12)
    xy = sampel_mengelompok(rng)
    n = len(xy)
    fig, axs = plt.subplots(2, 2, figsize=(10, 7.9))
    fig.subplots_adjust(left=0.02, right=0.98, top=0.95, bottom=0.08, wspace=0.06, hspace=0.30)
    for ax in axs.ravel():
        latar_kebun(ax)

    ax = axs[0, 0]                                         # (a) pembagian tunggal
    uji = rng.permutation(n)[: n // 3]
    latih = np.setdiff1d(np.arange(n), uji)
    ax.scatter(*xy[latih].T, s=30, c=KATEGORI[0], marker="o", edgecolors="white", linewidths=0.8, label="data latih (2/3)")
    ax.scatter(*xy[uji].T, s=36, c=KATEGORI[1], marker="^", edgecolors="white", linewidths=0.8, label="data uji (1/3)")
    ax.set_title("(a) Pembagian tunggal acak", fontsize=9.6, loc="left")

    ax = axs[0, 1]                                         # (b) lipat-5 acak
    lipat = rng.permutation(np.arange(n) % 5)
    for k in range(5):
        ax.scatter(*xy[lipat == k].T, s=30, c=KATEGORI[k], marker=PENANDA[k], edgecolors="white", linewidths=0.8,
                   label=f"lipatan {k + 1}")
    ax.set_title("(b) Validasi silang acak 5 lipatan", fontsize=9.6, loc="left")

    ax = axs[1, 0]                                         # (c) blok spasial
    _, blok = kmeans2(xy, 5, seed=3, minit="++")
    urut = np.argsort(np.argsort([xy[blok == k, 0].mean() for k in range(5)]))
    for k in range(5):
        m = urut[blok] == k
        ax.scatter(*xy[m].T, s=30, c=KATEGORI[k], marker=PENANDA[k], edgecolors="white", linewidths=0.8,
                   label=f"blok {k + 1}")
    ax.set_title("(c) Validasi silang spasial 5 blok", fontsize=9.6, loc="left")

    ax = axs[1, 1]                                         # (d) sampel probabilitas independen
    strata = [(0, 0, 2, 1.5), (2, 0, 2, 1.5), (0, 1.5, 2, 1.5), (2, 1.5, 2, 1.5)]
    for x0, y0, w, h in strata:
        ax.add_patch(Rectangle((x0, y0), w, h, fill=False, ec=WARNA["abu"], lw=1.0, ls="--", zorder=1))
    baru = np.vstack([np.column_stack([rng.uniform(x0 + 0.1, x0 + w - 0.1, 3), rng.uniform(y0 + 0.1, y0 + h - 0.1, 3)])
                      for x0, y0, w, h in strata])
    ax.scatter(*xy.T, s=24, c=KATEGORI[0], marker="o", edgecolors="white", linewidths=0.8, alpha=0.9,
               label="data latih (semua sampel lama)")
    ax.scatter(*baru.T, s=46, c=KATEGORI[1], marker="^", edgecolors="white", linewidths=0.8,
               label="sampel validasi baru (acak berstrata)")
    ax.plot([], [], color=WARNA["abu"], ls="--", lw=1.0, label="batas strata")
    ax.set_title("(d) Sampel probabilitas independen", fontsize=9.6, loc="left")

    for ax in axs.ravel():
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.01), ncol=5 if ax in (axs[0, 1], axs[1, 0]) else 3,
                  fontsize=7.6, handletextpad=0.3, columnspacing=0.9, frameon=False)
    fig.text(0.02, 0.005, "Data sintetis; kotak putih = blok kebun 500 m × 500 m. Sampel lama mengelompok di empat lokasi "
             "survei dan di sepanjang jalan utama.", fontsize=7.4, style="italic", color=WARNA["abu"])
    simpan(fig, MODUL, "M8-G02_skema-pembagian-data.png")


# ---------------------------------------------------------------- Gambar 8.3
def g03_alur():
    fig, ax = kanvas(10, 6.2, (0, 104), (0, 66))
    abu = WARNA["abu"]

    def node(x, y, teks, w=20, h=6.5, isi=WARNA["putih"], warna=WARNA["navy"], tebal=False):
        kotak(ax, x, y, w, h, teks, isi=isi, warna=warna, ukuran=7.8, tebal=tebal, r=0.7, lw=1.0)

    def ke(x1, y1, x2, y2, putus=False):
        panah(ax, x1, y1, x2, y2, warna=abu, lw=1.0, skala=9, putus=putus)

    def garis(xs, ys):
        ax.plot(xs, ys, color=abu, lw=1.0, ls="--", zorder=1)

    # masukan dan penyiapan
    node(2, 44, "Data tanah\n(sampel lapangan, data\nwarisan, sensor proksimal)", w=24, h=9, isi="#F3E3CF",
         warna=WARNA["tanah"], tebal=True)
    node(2, 22, "Kovariat SCORPAN\n(citra, DEM, iklim,\ngeologi, peta tanah)", w=24, h=9, isi="#DCEAF7",
         warna=WARNA["biru"], tebal=True)
    node(30, 45, "Pemeriksaan mutu dan\npenyetaraan kedalaman", w=22, h=7)
    node(30, 23, "Penyelarasan proyeksi\ndan resolusi", w=22, h=7)
    ke(26, 48.5, 30, 48.5), ke(26, 26.5, 30, 26.5)
    # rantai pemodelan
    rantai = [("Penumpangan (overlay):\ntabel pemodelan", "#EAF3E2", WARNA["teal"]), ("Seleksi kovariat", None, None),
              ("Pembagian data", None, None), ("Penalaan dan\npembangunan model", None, None),
              ("Validasi\n(ME, RMSE, MEC, PICP)", "#FFF6E5", WARNA["oranye"])]
    tinggi = [50, 39.5, 29, 18.5, 8]
    for (t, isi, warna), y in zip(rantai, tinggi):
        node(58, y, t, isi=isi or WARNA["putih"], warna=warna or WARNA["navy"], tebal=y == 50)
    for y1, y2 in zip(tinggi[:-1], tinggi[1:]):
        ke(68, y1, 68, y2 + 6.6)
    ke(52, 48.5, 58, 53.25), ke(52, 26.5, 58, 52.4)
    # umpan balik dari validasi ke seleksi kovariat
    garis([58, 56.8, 56.8], [11.25, 11.25, 42.75])
    ke(56.8, 42.75, 58, 42.75, putus=True)
    ax.text(55.7, 27, "perbaiki bila perlu", rotation=90, ha="center", va="center", fontsize=7.4, color=abu,
            style="italic")
    # keluaran
    hasil = ["Peta prediksi", "Peta ketidakpastian", "Peta residual dan AOA"]
    for i, t in enumerate(hasil):
        node(83, 26 - i * 9, t, w=19, h=6.5, isi="#DCEAF7", tebal=i == 0)
    ax.plot([80.5, 80.5], [11.25, 29.25], color=abu, lw=1.0, zorder=1)
    ax.plot([78, 80.5], [11.25, 11.25], color=abu, lw=1.0, zorder=1)
    for i in range(3):
        ke(80.5, 29.25 - i * 9, 83, 29.25 - i * 9)
    # siklus sampel tambahan
    garis([102, 103, 103, 14, 14], [20.25, 20.25, 61, 61, 57.5])
    ke(14, 57.5, 14, 53.1, putus=True)
    ax.text(58.5, 62.3, "sampel tambahan di daerah yang paling tidak pasti atau di luar AOA", ha="center", fontsize=7.6,
            color=abu, style="italic")
    simpan(fig, MODUL, "M8-G03_alur-pemodelan-dsm.png")


# ---------------------------------------------------------------- Gambar 8.4
def kov_eksponensial(h, sill=4.0, jangkauan=250.0):
    return sill * np.exp(-h / jangkauan)


def g04_residual():
    rng = np.random.default_rng(7)
    x = np.linspace(0, 2000, 401)
    kovariat = 3 + 2.5 * np.sin(x / 330) + 1.2 * np.cos(x / 140)
    C = kov_eksponensial(np.abs(x[:, None] - x[None, :])) + 1e-9 * np.eye(x.size)
    komponen = np.linalg.cholesky(C) @ rng.normal(0, 1, x.size)
    benar = 18 + 2.2 * kovariat + komponen
    io = np.sort(rng.choice(x.size, 26, replace=False))
    obs = benar[io] + rng.normal(0, 0.5, io.size)
    A = np.column_stack([np.ones(io.size), kovariat[io]])
    koef = np.linalg.lstsq(A, obs, rcond=None)[0]
    tren = koef[0] + koef[1] * kovariat
    resid = obs - tren[io]
    Coo = kov_eksponensial(np.abs(x[io][:, None] - x[io][None, :])) + 0.25 * np.eye(io.size)
    Cpo = kov_eksponensial(np.abs(x[:, None] - x[io][None, :]))
    resid_krig = Cpo @ np.linalg.solve(Coo, resid)
    akhir = tren + resid_krig
    rmse = lambda p: np.sqrt(np.mean((p - benar) ** 2))  # noqa: E731

    fig, axs = plt.subplots(3, 1, figsize=(9.6, 7.8), sharex=True)
    fig.subplots_adjust(left=0.08, right=0.98, top=0.94, bottom=0.08, hspace=0.42)
    gaya_benar = dict(color=WARNA["abu"], lw=1.0, alpha=0.7)
    axs[0].plot(x, benar, label="nilai sebenarnya", **gaya_benar)
    axs[0].plot(x, tren, color=KATEGORI[0], lw=2, label="prediksi tren dari kovariat")
    axs[0].scatter(x[io], obs, s=26, c=WARNA["teks"], zorder=3, label="pengamatan")
    axs[0].set_title("(a) Pengamatan dan prediksi model tren", fontsize=9.6, loc="left")
    axs[1].axhline(0, color=WARNA["abu"], lw=0.8)
    axs[1].plot(x, resid_krig, color=KATEGORI[1], lw=2, label="residual hasil kriging")
    axs[1].scatter(x[io], resid, s=26, c=KATEGORI[1], edgecolors="white", linewidths=0.8, zorder=3,
                   label="residual di titik pengamatan")
    axs[1].set_title("(b) Residual berautokorelasi spasial dan hasil kriging-nya", fontsize=9.6, loc="left")
    axs[2].plot(x, benar, label="nilai sebenarnya", **gaya_benar)
    axs[2].plot(x, akhir, color=WARNA["navy"], lw=2, label="tren + kriging residual")
    axs[2].scatter(x[io], obs, s=26, c=WARNA["teks"], zorder=3, label="pengamatan")
    axs[2].set_title(f"(c) Prediksi regression kriging (RMSE {koma(rmse(akhir), 2)}; model tren saja "
                     f"{koma(rmse(tren), 2)})", fontsize=9.6, loc="left")
    for ax, yl in zip(axs, ["Sifat tanah", "Residual", "Sifat tanah"]):
        ax.set_ylabel(yl, fontsize=8.6)
        ax.tick_params(labelsize=8)
        ax.legend(fontsize=7.6, loc="lower right", bbox_to_anchor=(1.0, 1.0), ncol=3, frameon=False,
                  handletextpad=0.4, columnspacing=1.0, borderaxespad=0.2)
        ax.yaxis.set_major_locator(MultipleLocator(1 if yl == "Residual" else 5))
        ax.yaxis.set_major_formatter(KOMA(0))
    axs[2].set_xlabel("Jarak sepanjang transek (m)", fontsize=8.8)
    axs[2].xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}".replace(",", ".")))
    fig.text(0.08, 0.008, "Data sintetis; model tren berupa regresi linear terhadap satu kovariat, residual diinterpolasi "
             "dengan kriging sederhana bermodel eksponensial.", fontsize=7.4, style="italic", color=WARNA["abu"])
    simpan(fig, MODUL, "M8-G04_residual-dan-regression-kriging.png")


# ---------------------------------------------------------------- Gambar 8.5
def indeks_ketidakmiripan(latih, prediksi, lipat):
    """DI menurut Meyer dan Pebesma (2021) dengan bobot kovariat yang sama.

    DI = jarak terdekat ke data latih dibagi rerata jarak antardata latih, pada kovariat yang telah dibakukan.
    Ambang AOA = nilai maksimum DI data latih (dihitung antarlipatan) setelah pencilan disingkirkan.
    """
    rerata, sd = latih.mean(axis=0), latih.std(axis=0)
    L, P = (latih - rerata) / sd, (prediksi - rerata) / sd
    d = np.sqrt(((L[:, None, :] - L[None, :, :]) ** 2).sum(-1))
    d_rerata = d[np.triu_indices(len(L), 1)].mean()
    di_prediksi = cKDTree(L).query(P)[0] / d_rerata
    di_latih = np.array([d[i, lipat != lipat[i]].min() for i in range(len(L))]) / d_rerata
    q1, q3 = np.percentile(di_latih, [25, 75])
    ambang = di_latih[di_latih <= q3 + 1.5 * (q3 - q1)].max()
    return di_prediksi, ambang


def g05_ketidakpastian():
    rng = np.random.default_rng(31)
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.9), gridspec_kw=dict(width_ratios=[1, 1.08]))
    fig.subplots_adjust(left=0.07, right=0.97, top=0.88, bottom=0.2, wspace=0.18)

    ax = axs[0]                                            # (a) PICP
    n = 60
    median = rng.uniform(1.0, 4.0, n)
    sd_benar = 0.18 + 0.12 * median
    obs = median + rng.normal(0, 1, n) * sd_benar
    sd_model = 0.78 * sd_benar                             # model terlalu yakin: interval terlalu sempit
    bawah, atas = median - 1.645 * sd_model, median + 1.645 * sd_model
    masuk = (obs >= bawah) & (obs <= atas)
    picp = masuk.mean()
    ax.vlines(median, bawah, atas, color=WARNA["abu"], lw=1.2, alpha=0.8, zorder=1)
    ax.scatter(median[masuk], obs[masuk], s=26, c=KATEGORI[0], marker="o", edgecolors="white", linewidths=0.8, zorder=3,
               label="di dalam interval 90%")
    ax.scatter(median[~masuk], obs[~masuk], s=34, c=KATEGORI[1], marker="^", edgecolors="white", linewidths=0.8, zorder=3,
               label="di luar interval 90%")
    ax.plot([0.5, 5.6], [0.5, 5.6], color=WARNA["abu"], ls="--", lw=0.9, zorder=0)
    ax.plot([], [], color=WARNA["abu"], lw=1.2, label="interval prediksi 90%")
    ax.set_xlim(0.6, 4.6)
    ax.set_ylim(0.2, 5.8)
    ax.set_xlabel("Prediksi (median)", fontsize=8.8)
    ax.set_ylabel("Pengamatan", fontsize=8.8)
    ax.set_title(f"(a) PICP = {koma(picp, 2)} untuk interval 90%", fontsize=9.6, loc="left")
    ax.legend(fontsize=7.6, loc="upper left", frameon=False)
    ax.text(0.98, 0.03, "interval terlalu sempit:\nketidakpastian diremehkan", transform=ax.transAxes, ha="right",
            va="bottom", fontsize=7.6, color=WARNA["teks"], bbox=dict(boxstyle="round,pad=0.25", fc="white",
                                                                     ec=WARNA["abu_muda"]))
    for f in (ax.xaxis, ax.yaxis):
        f.set_major_locator(MultipleLocator(1))
        f.set_major_formatter(KOMA(0))
    ax.tick_params(labelsize=8)

    ax = axs[1]                                            # (b) AOA
    z, lereng, xx, yy, rng2 = lanskap()
    t = twi(z, lereng)
    m = z.shape[0]
    kov = np.column_stack([z.ravel(), lereng.ravel() * 100, t.ravel()])
    rendah = np.argwhere((z < np.quantile(z, 0.55)) & (xx < 0.62))       # sampel hanya di bagian bawah barat
    pilih = rendah[rng.choice(len(rendah), 45, replace=False)]
    latih = kov[pilih[:, 0] * m + pilih[:, 1]]
    lipat = rng.permutation(np.arange(len(latih)) % 5)
    di, ambang = indeks_ketidakmiripan(latih, kov, lipat)
    di = di.reshape(m, m)
    im = ax.imshow(di, cmap=ramp("di", "#EAF1FB", WARNA["navy"]), interpolation="nearest", vmin=0,
                   vmax=np.quantile(di, 0.98))
    luar = np.ma.masked_where(di <= ambang, np.ones_like(di))
    ax.contourf(np.arange(m), np.arange(m), luar, levels=[0.5, 1.5], colors="none", hatches=["////"], zorder=2)
    ax.contour(di, levels=[ambang], colors=[WARNA["oranye"]], linewidths=1.6, zorder=3)
    ax.scatter(pilih[:, 1], pilih[:, 0], s=20, c=WARNA["oranye"], edgecolors="white", linewidths=0.7, zorder=4)
    ax.set_xticks([]), ax.set_yticks([])
    ax.set_title("(b) Indeks ketidakmiripan dan AOA", fontsize=9.6, loc="left")
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    cb.set_label("indeks ketidakmiripan (DI)", fontsize=8)
    cb.ax.tick_params(labelsize=7.4)
    cb.ax.yaxis.set_major_formatter(KOMA(1))
    tangan = [Line2D([], [], marker="o", ls="", markerfacecolor=WARNA["oranye"], markeredgecolor="white", markersize=6,
                     label="titik data latih"),
              Line2D([], [], color=WARNA["oranye"], lw=1.6, label=f"batas AOA (DI = {koma(ambang, 2)})"),
              Patch(fc="white", ec=WARNA["abu"], hatch="////", label="di luar AOA")]
    ax.legend(handles=tangan, fontsize=7.6, loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=3, frameon=False,
              handletextpad=0.4, columnspacing=1.0)
    fig.text(0.07, 0.015, "Data sintetis; DI dihitung dari elevasi, kemiringan lereng, dan TWI yang dibakukan dengan bobot "
             "sama.", fontsize=7.4, style="italic", color=WARNA["abu"])
    simpan(fig, MODUL, "M8-G05_interval-prediksi-dan-aoa.png")


if __name__ == "__main__":
    gaya.atur()
    g01_kovariat()
    g02_pembagian_data()
    g03_alur()
    g04_residual()
    g05_ketidakpastian()
