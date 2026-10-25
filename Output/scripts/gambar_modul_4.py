"""Gambar dan analisis Modul 4 — Remote Sensing untuk Estimasi Soil Properties.

Jalankan: python3 Output/scripts/gambar_modul_4.py
Keluaran:
- Output/assets/modul-4/M4-G01_fitur-serapan-spektral-tanah.png
- Output/assets/modul-4/M4-G02_faktor-pengganggu-estimasi-tanah.png
- Output/assets/modul-4/M4-G03_peta-indeks-spektral-bompon.png
- Output/assets/modul-4/M4-G04_indeks-dan-fraksi-tanah-bompon.png
- Output/assets/modul-4/statistik_modul_4.json
"""
import json
import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle
from osgeo import gdal, ogr

import gaya
from gaya import WARNA, kanvas, kotak, panah, simpan

gdal.UseExceptions()
ogr.UseExceptions()

MODUL = "modul-4"
TERBUKA = os.path.join(gaya.AKAR, "Source", "Data Bompon", "terbuka")
KELUAR_JSON = os.path.join(gaya.ASET, MODUL, "statistik_modul_4.json")


def baca_sentinel2():
    ds = gdal.Open(os.path.join(TERBUKA, "sentinel2_l2a_20250721_10m.tif"))
    gt = ds.GetGeoTransform()
    ext = (gt[0], gt[0] + gt[1] * ds.RasterXSize, gt[3] + gt[5] * ds.RasterYSize, gt[3])
    b = {ds.GetRasterBand(i).GetDescription(): ds.GetRasterBand(i).ReadAsArray().astype(np.float32)
         for i in range(1, ds.RasterCount + 1)}
    # Mask batas Sub-DAS pada grid 10 m
    m_ds = gdal.GetDriverByName("MEM").Create("", ds.RasterXSize, ds.RasterYSize, 1, gdal.GDT_Byte)
    m_ds.SetGeoTransform(gt)
    src = ogr.Open(gaya.GPKG)
    gdal.RasterizeLayer(m_ds, [1], src.GetLayer("batas_subdas"), burn_values=[1])
    mask = m_ds.ReadAsArray().astype(bool)

    # Rasterisasi penggunaan lahan pada grid 10 m
    pl_ds = gdal.GetDriverByName("MEM").Create("", ds.RasterXSize, ds.RasterYSize, 1, gdal.GDT_Byte)
    pl_ds.SetGeoTransform(gt)
    lyr = src.GetLayer("penggunaan_lahan")
    kelas_pl = list(gaya.WARNA_PENGGUNAAN)
    for idx, nama in enumerate(kelas_pl, start=1):
        lyr.SetAttributeFilter(f"penggunaan_lahan = '{nama}'")
        gdal.RasterizeLayer(pl_ds, [1], lyr, burn_values=[idx])
    pl = pl_ds.ReadAsArray()
    return b, mask, pl, gt, ext


def hitung_indeks(b):
    eps = 1e-6
    bi = np.sqrt((b["B04"] ** 2 + b["B03"] ** 2 + b["B02"] ** 2) / 3.0)
    ci = b["B11"] / np.maximum(b["B12"], eps)
    ndwi = (b["B08"] - b["B11"]) / np.maximum(b["B08"] + b["B11"], eps)
    savi = 1.5 * (b["B08"] - b["B04"]) / np.maximum(b["B08"] + b["B04"] + 0.5, eps)
    ndvi = (b["B08"] - b["B04"]) / np.maximum(b["B08"] + b["B04"], eps)
    ri = (b["B04"] ** 2) / np.maximum(b["B02"] * (b["B03"] ** 3), eps)
    return {"BI": bi, "CI": ci, "NDWI": ndwi, "SAVI": savi, "NDVI": ndvi, "RI": ri}


def simpan_statistik(indeks, mask, pl, gt):
    kelas_pl = list(gaya.WARNA_PENGGUNAAN)
    stat = {"keseluruhan_subdas": {}, "per_penggunaan_lahan": {}, "sampel_50_titik": {}}
    for k, arr in indeks.items():
        val = arr[mask]
        stat["keseluruhan_subdas"][k] = {
            "min": round(float(np.min(val)), 3),
            "p05": round(float(np.percentile(val, 5)), 3),
            "median": round(float(np.median(val)), 3),
            "mean": round(float(np.mean(val)), 3),
            "p95": round(float(np.percentile(val, 95)), 3),
            "max": round(float(np.max(val)), 3),
            "std": round(float(np.std(val)), 3),
        }
    for idx, nama in enumerate(kelas_pl, start=1):
        sel = mask & (pl == idx)
        stat["per_penggunaan_lahan"][nama] = {
            k: {
                "median": round(float(np.median(arr[sel])), 3),
                "mean": round(float(np.mean(arr[sel])), 3),
                "std": round(float(np.std(arr[sel])), 3),
                "q25": round(float(np.percentile(arr[sel], 25)), 3),
                "q75": round(float(np.percentile(arr[sel], 75)), 3),
            }
            for k, arr in indeks.items()
        }
    # Ekstrak pada 50 titik sampel rencana
    titik = gaya.baca_layer("titik_sampel_rencana")
    sampel_val = {k: [] for k in indeks}
    for atr, g in titik:
        col = int((g.GetX() - gt[0]) / gt[1])
        row = int((g.GetY() - gt[3]) / gt[5])
        for k, arr in indeks.items():
            sampel_val[k].append(float(arr[row, col]))
    for k, v in sampel_val.items():
        v = np.array(v)
        stat["sampel_50_titik"][k] = {
            "min": round(float(v.min()), 3),
            "median": round(float(np.median(v)), 3),
            "mean": round(float(v.mean()), 3),
            "max": round(float(v.max()), 3),
            "std": round(float(v.std()), 3),
        }
    os.makedirs(os.path.dirname(KELUAR_JSON), exist_ok=True)
    with open(KELUAR_JSON, "w", encoding="utf-8") as fh:
        json.dump(stat, fh, indent=2, ensure_ascii=False)
    return stat


# ---------------------------------------------------------------- Gambar 4.1
def g01_fitur_serapan_tanah():
    w = np.linspace(0.4, 2.5, 700)
    # Kurva dasar reflektansi tanah (%)
    dasar = 12 + 28 * (1 - np.exp(-(w - 0.38) / 0.65))
    air = 10 * np.exp(-((w - 1.42) / 0.055) ** 2) + 15 * np.exp(-((w - 1.92) / 0.065) ** 2)
    lempung_oh = 9.5 * np.exp(-((w - 2.205) / 0.042) ** 2) + 2.5 * np.exp(-((w - 1.41) / 0.03) ** 2)
    besi = 6.5 * np.exp(-((w - 0.48) / 0.08) ** 2) + 5.5 * np.exp(-((w - 0.88) / 0.09) ** 2)

    k_pasir_kering = dasar + 4.5 - 0.45 * air - 0.2 * lempung_oh
    k_lempung_fe = dasar - 3.5 - 0.75 * air - 1.15 * lempung_oh - besi
    k_organik_tinggi = (dasar * 0.50) - 4 * np.exp(-((w - 0.65) / 0.25) ** 2) - 0.7 * air - 0.6 * lempung_oh
    k_lempung_lembap = (k_lempung_fe * 0.56) - 0.65 * air

    fig, ax = plt.subplots(figsize=(10, 4.9))
    # Pita serapan utama
    pita = [
        (0.43, 0.55, "Fe³⁺\n(goetit/hematit)", "#FDEBD0"),
        (0.82, 0.96, "Fe³⁺\n(transisi kristal)", "#FDEBD0"),
        (1.37, 1.47, "H₂O & OH\n(1,4 µm)", "#DCEAF7"),
        (1.86, 1.99, "H₂O\n(1,9 µm)", "#DCEAF7"),
        (2.16, 2.26, "Al–OH lempung\n(2,2 µm)", "#E8DAEF"),
    ]
    for a, b_w, lbl, col in pita:
        ax.axvspan(a, b_w, color=col, alpha=0.85, zorder=0)
        ax.text((a + b_w) / 2, 47.5, lbl, ha="center", va="top", fontsize=7.6, color=WARNA["teks"], linespacing=1.1)

    ax.plot(w, k_pasir_kering, color=WARNA["kuning"], lw=2.2, label="Tanah berpasir kering (SOM rendah)")
    ax.plot(w, k_lempung_fe, color=WARNA["oranye"], lw=2.2, label="Tanah berlempung kaya oksida besi & kaolinit")
    ax.plot(w, k_organik_tinggi, color=WARNA["tanah"], lw=2.2, label="Tanah kaya bahan organik (C-organik tinggi)")
    ax.plot(w, k_lempung_lembap, color=WARNA["navy"], lw=2.0, ls="--", label="Tanah berlempung lembap (kadar lengas tinggi)")

    # Bar perbandingan kanal Sentinel-2 vs Hiperspektral di bagian atas
    s2_bands = [("B2", 0.458, 0.523), ("B3", 0.543, 0.578), ("B4", 0.650, 0.680), ("B5", 0.698, 0.713),
                ("B6", 0.733, 0.748), ("B7", 0.773, 0.793), ("B8", 0.785, 0.900), ("B8A", 0.855, 0.875),
                ("B11", 1.565, 1.655), ("B12", 2.100, 2.280)]
    for nama, a, b_w in s2_bands:
        ax.add_patch(Rectangle((a, 51.5), b_w - a, 2.2, fc=WARNA["teal"], ec="white", lw=0.4, clip_on=False))
        if nama in ("B2", "B3", "B4", "B8", "B11", "B12"):
            ax.text((a + b_w) / 2, 54.1, nama, ha="center", va="bottom", fontsize=7.5, fontweight="bold",
                    color=WARNA["navy"], clip_on=False)
    for hw in np.arange(0.42, 2.46, 0.014):
        if not (1.36 < hw < 1.46 or 1.82 < hw < 1.96):
            ax.add_patch(Rectangle((hw, 49.2), 0.010, 1.4, fc=WARNA["ungu"], ec="none", alpha=0.8, clip_on=False))
    ax.text(0.40, 52.6, "Sentinel-2 MSI (lebar):", ha="right", va="center", fontsize=7.8, color=WARNA["teal"],
            fontweight="bold", clip_on=False)
    ax.text(0.40, 49.9, "Hiperspektral (sempit):", ha="right", va="center", fontsize=7.8, color=WARNA["ungu"],
            fontweight="bold", clip_on=False)

    ax.annotate("Penurunan pantulan tampak–NIR\nakibat bahan organik (SOM)", xy=(0.68, 13.8), xytext=(0.95, 6.8),
                arrowprops=dict(arrowstyle="-|>", color=WARNA["tanah"], lw=1.1), fontsize=8, color=WARNA["tanah"])
    ax.annotate("Serapan spesifik Al–OH (2,20 µm)\ntertangkap di dalam kanal B12", xy=(2.205, 21.3), xytext=(1.48, 25.0),
                arrowprops=dict(arrowstyle="-|>", color=WARNA["ungu"], lw=1.1), fontsize=8, color=WARNA["ungu"])

    ax.set_xlim(0.4, 2.5)
    ax.set_ylim(0, 48.5)
    ax.set_xlabel("Panjang gelombang (µm)", fontsize=9.5)
    ax.set_ylabel("Reflektansi permukaan (%)", fontsize=9.5)
    ax.legend(loc="upper left", bbox_to_anchor=(0.01, 0.90), fontsize=8.4, framealpha=0.9, frameon=True, facecolor="white")
    ax.text(0.99, 0.02, "Ilustrasi skematis berdasarkan Ben-Dor et al. (2009) dan Mulder et al. (2011)",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=7.8, style="italic", color=WARNA["abu"])
    fig.subplots_adjust(top=0.84, left=0.14, right=0.98, bottom=0.12)
    simpan(fig, MODUL, "M4-G01_fitur-serapan-spektral-tanah.png")


# ---------------------------------------------------------------- Gambar 4.2
def g02_faktor_pengganggu():
    fig, ax = kanvas(10, 4.4, (0, 104), (-2, 44))
    panel = [
        ("(a) Kedalaman penetrasi dangkal", "Optik hanya merekam < 1 mm;\nSAR gelombang C/L hanya ±2–20 cm,\nsedangkan solum mencapai > 40 cm"),
        ("(b) Tutupan tajuk dan serasah", "Piksel mencampur pantulan tajuk,\nserasah kering (NPV), dan tanah;\nsinyal tanah tertutup di kebun rapat"),
        ("(c) Kelembapan permukaan sesaat", "Hujan lokal menurunkan pantulan\nseluruh kanal sehingga tanah basah\ntampak menyerupai tanah kaya SOM"),
        ("(d) Kekasaran dan bayangan mikro", "Bongkah pengolahan tanah atau\nlereng curam menimbulkan bayangan\nmikro yang menurunkan pantulan"),
    ]
    for k, (judul, ket) in enumerate(panel):
        x0 = 1 + k * 26
        kotak(ax, x0, 8, 24, 30, isi=WARNA["latar"], warna=WARNA["abu_muda"], lw=1.0, r=1.0, zorder=1)
        ax.text(x0 + 12, 40.5, judul, ha="center", va="center", fontsize=9.2, fontweight="bold", color=WARNA["navy"])
        ax.text(x0 + 12, 3.0, ket, ha="center", va="center", fontsize=7.9, color=WARNA["teks"], linespacing=1.2)

    # (a) Penampang kedalaman
    x0 = 3
    ax.add_patch(Rectangle((x0, 26), 20, 4, fc="#8C5A3C", ec="white", lw=0.8, zorder=3))
    ax.add_patch(Rectangle((x0, 18), 20, 8, fc="#B5763F", ec="white", lw=0.8, zorder=3))
    ax.add_patch(Rectangle((x0, 10), 20, 8, fc="#D9A35F", ec="white", lw=0.8, zorder=3))
    ax.text(x0 + 10, 28, "Kulit permukaan (< 1 mm)", ha="center", va="center", fontsize=7.3, color="white", fontweight="bold", zorder=4)
    ax.text(x0 + 10, 22, "Lapisan 1 (0–20 cm)", ha="center", va="center", fontsize=7.5, color="white", zorder=4)
    ax.text(x0 + 10, 14, "Lapisan 2 (20–40 cm)", ha="center", va="center", fontsize=7.5, color=WARNA["teks"], zorder=4)
    panah(ax, x0 + 5, 36.5, x0 + 5, 30.2, warna=WARNA["teal"], lw=1.6)
    ax.text(x0 + 5, 36.8, "Optik", ha="center", va="bottom", fontsize=7.5, color=WARNA["teal"], fontweight="bold")
    panah(ax, x0 + 15, 36.5, x0 + 15, 25.0, warna=WARNA["ungu"], lw=1.6)
    ax.text(x0 + 15, 36.8, "SAR", ha="center", va="bottom", fontsize=7.5, color=WARNA["ungu"], fontweight="bold")

    # (b) Mixed pixel
    x0 = 29
    ax.add_patch(Rectangle((x0 + 2, 11), 16, 16, fc=WARNA["tanah_muda"], ec=WARNA["navy"], lw=1.4, zorder=3))
    ax.add_patch(Rectangle((x0 + 2, 17), 11, 10, fc=WARNA["hijau"], alpha=0.85, ec="none", zorder=4))
    ax.add_patch(Rectangle((x0 + 10, 11), 8, 9, fc="#C9A25F", alpha=0.9, ec="none", zorder=4))
    ax.text(x0 + 7.5, 22, "Tajuk\nvegetasi\n(60%)", ha="center", va="center", fontsize=7.5, color="white", fontweight="bold", zorder=5)
    ax.text(x0 + 14, 15.5, "Serasah\n(25%)", ha="center", va="center", fontsize=7.3, color=WARNA["teks"], zorder=5)
    ax.text(x0 + 6, 14, "Tanah\n(15%)", ha="center", va="center", fontsize=7.3, color=WARNA["teks"], fontweight="bold", zorder=5)
    ax.text(x0 + 10, 32.5, "Satu piksel 10 × 10 m", ha="center", fontsize=8, color=WARNA["navy"], fontweight="bold")
    ax.text(x0 + 10, 29.2, "$R_{piksel} = f_v R_v + f_s R_s + f_t R_t$", ha="center", fontsize=7.8, color=WARNA["abu"])

    # (c) Kelembapan
    x0 = 55
    ax.add_patch(Rectangle((x0 + 1, 12), 9, 8, fc="#D9A35F", ec=WARNA["tanah"], lw=1, zorder=3))
    ax.add_patch(Rectangle((x0 + 10, 12), 9, 8, fc="#5C3A21", ec=WARNA["tanah"], lw=1, zorder=3))
    ax.text(x0 + 5.5, 16, "Kering\n(cerah)", ha="center", va="center", fontsize=7.5, color=WARNA["teks"], fontweight="bold", zorder=4)
    ax.text(x0 + 14.5, 16, "Basah\n(gelap)", ha="center", va="center", fontsize=7.5, color="white", fontweight="bold", zorder=4)
    panah(ax, x0 + 5.5, 20.5, x0 + 5.5, 33, warna=WARNA["oranye"], lw=2.2)
    panah(ax, x0 + 14.5, 20.5, x0 + 14.5, 27, warna=WARNA["biru"], lw=1.3)
    ax.text(x0 + 10, 34.5, "Tanah yang sama,\nreflektansi berbeda", ha="center", fontsize=7.8, color=WARNA["navy"])

    # (d) Kekasaran permukaan
    x0 = 81
    ax.add_patch(Rectangle((x0 + 1, 24), 18, 2.5, fc=WARNA["tanah_muda"], ec=WARNA["tanah"], lw=1, zorder=3))
    panah(ax, x0 + 4, 33, x0 + 8, 26.8, warna=WARNA["oranye"], lw=1.3)
    panah(ax, x0 + 8, 26.8, x0 + 14, 33.5, warna=WARNA["teal"], lw=1.6)
    ax.text(x0 + 17, 29, "halus", fontsize=7.5, color=WARNA["teal"], ha="center")
    # permukaan kasar bergelombang
    xs = np.linspace(x0 + 1, x0 + 19, 13)
    ys = [12, 16, 12, 15.5, 12, 16, 12, 15.5, 12, 16, 12, 15, 12]
    poly = np.vstack([np.c_[xs, ys], [[x0 + 19, 10], [x0 + 1, 10]]])
    ax.add_patch(Polygon(poly, fc=WARNA["tanah"], ec="#4A2E1B", lw=0.9, zorder=3))
    panah(ax, x0 + 4, 21, x0 + 7.5, 14.5, warna=WARNA["oranye"], lw=1.3)
    ax.text(x0 + 13.5, 18.5, "bayangan mikro\n(hamburan terjebak)", fontsize=7.3, color=WARNA["merah"], ha="center")

    simpan(fig, MODUL, "M4-G02_faktor-pengganggu-estimasi-tanah.png")


# ---------------------------------------------------------------- Gambar 4.3
def g03_peta_indeks(indeks, mask, ext):
    batas = gaya.baca_layer("batas_subdas")[0][1]
    titik = gaya.baca_layer("titik_sampel_rencana")
    tx = [g.GetX() for _, g in titik]
    ty = [g.GetY() for _, g in titik]

    konfig = [
        ("BI", "(a) Brightness Index (BI)\nKecerahan permukaan", "YlOrBr", 0.03, 0.14),
        ("CI", "(b) Clay Minerals Ratio (B11/B12)\nNisbah SWIR1 terhadap SWIR2", "PuOr", 1.45, 2.25),
        ("NDWI", "(c) Normalized Difference Water Index\nNDWI = (B8 − B11)/(B8 + B11)", "RdYlBu", 0.10, 0.48),
        ("SAVI", "(d) Soil-Adjusted Vegetation Index\nSAVI (L = 0,5)", "YlGn", 0.25, 0.65),
    ]
    fig, axs = plt.subplots(1, 4, figsize=(10, 6.2))
    fig.subplots_adjust(left=0.01, right=0.99, top=0.88, bottom=0.14, wspace=0.05)
    for ax, (k, judul, cmap, vmin, vmax) in zip(axs, konfig):
        arr = np.ma.masked_where(~mask, indeks[k])
        im = ax.imshow(arr, extent=ext, cmap=cmap, vmin=vmin, vmax=vmax, interpolation="nearest")
        gaya.gambar_poligon(ax, batas, fc="none", ec=WARNA["navy"], lw=1.2)
        ax.scatter(tx, ty, s=7, c="white", edgecolors=WARNA["navy"], lw=0.5, zorder=5)
        ax.set_xlim(ext[0] + 140, ext[1] - 140)
        ax.set_ylim(ext[2] + 140, ext[3] - 140)
        ax.set_xticks([]), ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)
        ax.set_title(judul, fontsize=8.8)
        cb = fig.colorbar(im, ax=ax, orientation="horizontal", fraction=0.045, pad=0.03)
        cb.ax.tick_params(labelsize=7.5)
    gaya.skala_batang(axs[0], ext[0] + 200, ext[2] + 220, 500, "500 m", tinggi=24)
    gaya.panah_utara(axs[0], 0.88, 0.88, 0.05)
    simpan(fig, MODUL, "M4-G03_peta-indeks-spektral-bompon.png")


# ---------------------------------------------------------------- Gambar 4.4
def g04_indeks_dan_fraksi(indeks, mask, pl):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.6), gridspec_kw={"width_ratios": [1.05, 1.15]})
    fig.subplots_adjust(left=0.07, right=0.98, top=0.86, bottom=0.18, wspace=0.26)

    # Panel (a): Boxplot SAVI dan Clay Ratio per penggunaan lahan
    kelas_pl = list(gaya.WARNA_PENGGUNAAN)
    data_savi = [indeks["SAVI"][mask & (pl == i + 1)] for i in range(len(kelas_pl))]
    data_ndwi = [indeks["NDWI"][mask & (pl == i + 1)] for i in range(len(kelas_pl))]
    pos = np.arange(len(kelas_pl))
    bp1 = ax1.boxplot(data_savi, positions=pos - 0.17, widths=0.28, patch_artist=True, showfliers=False,
                      medianprops=dict(color=WARNA["navy"], lw=1.4))
    bp2 = ax1.boxplot(data_ndwi, positions=pos + 0.17, widths=0.28, patch_artist=True, showfliers=False,
                      medianprops=dict(color=WARNA["navy"], lw=1.4))
    for patch in bp1["boxes"]:
        patch.set_facecolor(WARNA["hijau"])
        patch.set_alpha(0.75)
    for patch in bp2["boxes"]:
        patch.set_facecolor(WARNA["biru"])
        patch.set_alpha(0.75)
    ax1.set_xticks(pos)
    ax1.set_xticklabels(kelas_pl, fontsize=8.5)
    ax1.set_ylabel("Nilai indeks spektral", fontsize=9)
    ax1.set_title("(a) Sebaran SAVI dan NDWI per penggunaan lahan\n(citra Sentinel-2 Sub-DAS Bompon, 21 Juli 2025)", fontsize=9.2)
    from matplotlib.patches import Patch
    ax1.legend(handles=[Patch(fc=WARNA["hijau"], alpha=0.75, label="SAVI (kerapatan vegetasi)"),
                        Patch(fc=WARNA["biru"], alpha=0.75, label="NDWI (kebasahan tajuk/permukaan)")],
               loc="lower left", fontsize=8)
    ax1.grid(axis="y", color=WARNA["abu_muda"], lw=0.5)

    # Panel (b): Fraksi tekstur laboratorium per bentuklahan (Fatmawati, 2026 Lampiran 4, Lapisan 1: 0-20 cm)
    lf_nama = ["Interfluve", "Lereng Atas\nPerbukitan", "Lereng Tengah\nPerbukitan",
               "Lereng Bawah\nPerbukitan", "Lereng Kaki\nKoluvial", "Dataran\nKoluvial"]
    pasir_l1 = np.array([15.72, 16.12, 16.37, 16.34, 18.00, 18.61])
    debu_l1 = np.array([21.27, 20.64, 20.39, 20.50, 21.96, 23.00])
    lempung_l1 = np.array([62.86, 63.09, 62.92, 62.63, 59.20, 57.91])
    lempung_l2 = np.array([66.86, 67.41, 65.75, 64.68, 61.02, 64.04])

    x = np.arange(len(lf_nama))
    w = 0.24
    ax2.bar(x - w, lempung_l1, width=w, color=WARNA["tanah"], label="Lempung 0–20 cm")
    ax2.bar(x, lempung_l2, width=w, color=WARNA["oranye"], label="Lempung 20–40 cm")
    ax2.bar(x + w, debu_l1, width=w, color=WARNA["teal"], label="Debu 0–20 cm")
    ax2.plot(x + w, pasir_l1, "o--", color=WARNA["navy"], lw=1.4, markersize=5, label="Pasir 0–20 cm")

    ax2.set_xticks(x)
    ax2.set_xticklabels(lf_nama, fontsize=7.6)
    ax2.set_ylim(0, 82)
    ax2.set_ylabel("Rata-rata fraksi tekstur (%)", fontsize=9)
    ax2.set_title("(b) Rata-rata fraksi tekstur tanah per bentuklahan\n(data observasi laboratorium; Fatmawati, 2026)", fontsize=9.2)
    ax2.legend(loc="upper right", ncol=2, fontsize=7.8)
    ax2.grid(axis="y", color=WARNA["abu_muda"], lw=0.5)

    simpan(fig, MODUL, "M4-G04_indeks-dan-fraksi-tanah-bompon.png")


if __name__ == "__main__":
    gaya.atur()
    b, mask, pl, gt, ext = baca_sentinel2()
    indeks = hitung_indeks(b)
    stat = simpan_statistik(indeks, mask, pl, gt)
    print(json.dumps(stat, indent=2, ensure_ascii=False))
    g01_fitur_serapan_tanah()
    g02_faktor_pengganggu()
    g03_peta_indeks(indeks, mask, ext)
    g04_indeks_dan_fraksi(indeks, mask, pl)
