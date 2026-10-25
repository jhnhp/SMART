"""Gambar dan analisis Modul 5 — Bare Soil Detection & Information Extraction.

Jalankan: python3 Output/scripts/gambar_modul_5.py
Keluaran:
- Output/assets/modul-5/M5-G01_bauran-spektral-dan-siklus-sawit.png
- Output/assets/modul-5/M5-G02_metode-komposit-tanah-terbuka-multitemporal.png
- Output/assets/modul-5/M5-G03_peta-bsi-dan-deteksi-tanah-terbuka-bompon.png
- Output/assets/modul-5/M5-G04_ruang-fitur-ndvi-bsi-bompon.png
- Output/assets/modul-5/statistik_modul_5.json
"""
import json
import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Circle, Patch, Polygon, Rectangle
from osgeo import gdal, ogr

import gaya
from gaya import WARNA, kanvas, kotak, nomor, panah, simpan
from gambar_modul_4 import baca_sentinel2

gdal.UseExceptions()
ogr.UseExceptions()

MODUL = "modul-5"
KELUAR_JSON = os.path.join(gaya.ASET, MODUL, "statistik_modul_5.json")


def hitung_indeks_bsi(b):
    eps = 1e-6
    ndvi = (b["B08"] - b["B04"]) / np.maximum(b["B08"] + b["B04"], eps)
    bsi = ((b["B11"] + b["B04"]) - (b["B08"] + b["B02"])) / np.maximum((b["B11"] + b["B04"]) + (b["B08"] + b["B02"]), eps)
    mbi = ((b["B11"] - b["B12"] - b["B08"]) / np.maximum(b["B11"] + b["B12"] + b["B08"], eps)) + 0.5
    nbr2 = (b["B11"] - b["B12"]) / np.maximum(b["B11"] + b["B12"], eps)
    ndbai = (b["B11"] - b["B12"]) / np.maximum(b["B11"] + b["B12"], eps)  # Sentinel-2 SWIR proxy
    return {"NDVI": ndvi, "BSI": bsi, "MBI": mbi, "NBR2": nbr2}


def klasifikasi_keterbukaan(ind, pl):
    """Klasifikasi piksel:
    1 = Vegetasi rapat (NDVI >= 0.75)
    2 = Vegetasi sedang/campuran (0.55 <= NDVI < 0.75 atau BSI <= -0.12)
    3 = Tanah terbuka sebagian / bera pertanian (NDVI < 0.55 dan BSI > -0.12 dan bukan permukiman)
    4 = Permukiman / permukaan terbangun terbuka (NDVI < 0.55 dan BSI > -0.12 pada kelas Permukiman)
    """
    ndvi, bsi = ind["NDVI"], ind["BSI"]
    terbuka_spektral = (ndvi < 0.55) & (bsi > -0.12)
    kelas = np.full(ndvi.shape, 2, dtype=np.int32)
    kelas[ndvi >= 0.75] = 1
    kelas[terbuka_spektral & (pl != 4)] = 3
    kelas[terbuka_spektral & (pl == 4)] = 4
    return kelas


def analisis_modul_5(b, ind, mask, pl):
    kelas = klasifikasi_keterbukaan(ind, pl)
    kelas_pl = list(gaya.WARNA_PENGGUNAAN)
    total_px = int(mask.sum())
    r_corr = float(np.corrcoef(ind["NDVI"][mask], ind["BSI"][mask])[0, 1])

    nama_k = {
        1: "Vegetasi rapat (NDVI >= 0,75)",
        2: "Vegetasi campuran (0,55 <= NDVI < 0,75)",
        3: "Tanah terbuka/bera pertanian (NDVI < 0,55 & BSI > -0,12)",
        4: "Permukaan terbangun/permukiman terbuka",
    }
    proporsi_kelas = {}
    for k, lbl in nama_k.items():
        n_px = int((mask & (kelas == k)).sum())
        proporsi_kelas[lbl] = {
            "piksel": n_px,
            "luas_ha": round(n_px * 0.01, 2),
            "persen": round(n_px / total_px * 100, 2),
        }

    per_pl = {}
    for i, nama in enumerate(kelas_pl, start=1):
        sel = mask & (pl == i)
        n_pl = int(sel.sum())
        n_terbuka = int((sel & (ind["NDVI"] < 0.55) & (ind["BSI"] > -0.12)).sum())
        n_ketat = int((sel & (ind["NDVI"] < 0.40) & (ind["BSI"] > 0.0)).sum())
        per_pl[nama] = {
            "luas_ha": round(n_pl * 0.01, 2),
            "median_ndvi": round(float(np.median(ind["NDVI"][sel])), 3),
            "median_bsi": round(float(np.median(ind["BSI"][sel])), 3),
            "q25_bsi": round(float(np.percentile(ind["BSI"][sel], 25)), 3),
            "q75_bsi": round(float(np.percentile(ind["BSI"][sel], 75)), 3),
            "median_mbi": round(float(np.median(ind["MBI"][sel])), 3),
            "median_nbr2": round(float(np.median(ind["NBR2"][sel])), 3),
            "piksel_terbuka_sebagian": n_terbuka,
            "persen_terbuka_sebagian": round(n_terbuka / n_pl * 100, 2),
            "piksel_terbuka_murni_ndvi04_bsi0": n_ketat,
            "persen_terbuka_murni": round(n_ketat / n_pl * 100, 2),
        }

    kanal_urut = ["B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8A", "B11", "B12"]
    spektrum_kelompok = {}
    for k, lbl in ((1, "Vegetasi rapat"), (2, "Vegetasi campuran"), (3, "Tanah terbuka/bera pertanian")):
        sel = mask & (kelas == k)
        spektrum_kelompok[lbl] = {kn: round(float(np.median(b[kn][sel])), 4) for kn in kanal_urut}
    sel_kering = mask & (ind["NDVI"] < 0.40) & (ind["BSI"] > 0.0)
    spektrum_kelompok["Permukaan terbuka kering (BSI > 0)"] = {
        kn: round(float(np.median(b[kn][sel_kering])), 4) for kn in kanal_urut
    }

    stat = {
        "total_piksel_10m": total_px,
        "luas_grid_10m_ha": round(total_px * 0.01, 2),
        "korelasi_ndvi_bsi": round(r_corr, 3),
        "keseluruhan": {
            k: {
                "min": round(float(ind[k][mask].min()), 3),
                "p05": round(float(np.percentile(ind[k][mask], 5)), 3),
                "median": round(float(np.median(ind[k][mask])), 3),
                "mean": round(float(np.mean(ind[k][mask])), 3),
                "p95": round(float(np.percentile(ind[k][mask], 95)), 3),
                "max": round(float(ind[k][mask].max()), 3),
            }
            for k in ("BSI", "MBI", "NBR2", "NDVI")
        },
        "proporsi_keterbukaan": proporsi_kelas,
        "per_penggunaan_lahan": per_pl,
        "spektrum_median": spektrum_kelompok,
    }
    os.makedirs(os.path.dirname(KELUAR_JSON), exist_ok=True)
    with open(KELUAR_JSON, "w", encoding="utf-8") as fh:
        json.dump(stat, fh, indent=2, ensure_ascii=False)
    return stat, kelas


# ---------------------------------------------------------------- Gambar 5.1
def g01_bauran_dan_siklus_sawit():
    fig, ax = kanvas(10, 4.6, (0, 104), (0, 48))

    # Panel (a): Segitiga Bauran Spektral PV - NPV - Bare Soil
    ax.text(24, 45.5, "(a) Segitiga bauran spektral (spectral mixing)", ha="center", fontsize=10,
            fontweight="bold", color=WARNA["navy"])
    kotak(ax, 1, 2, 46, 41, isi=WARNA["latar"], warna=WARNA["abu_muda"], lw=1.0, r=1.0, zorder=1)
    p_pv = np.array([24.0, 36.5])
    p_bs = np.array([9.0, 11.5])
    p_npv = np.array([39.0, 11.5])
    tri = Polygon([p_pv, p_bs, p_npv], fc="white", ec=WARNA["navy"], lw=1.5, zorder=2)
    ax.add_patch(tri)
    # Zona bare soil di sudut kiri bawah
    zona_bs = Polygon([p_bs, p_bs + 0.48 * (p_pv - p_bs), p_bs + 0.48 * (p_npv - p_bs)],
                      fc=WARNA["tanah_muda"], alpha=0.75, ec=WARNA["tanah"], lw=1.2, ls="--", zorder=3)
    ax.add_patch(zona_bs)
    ax.text(15.6, 14.8, "Zona target\ntanah terbuka\n(>70% tanah)", ha="center", va="center",
            fontsize=6.8, color=WARNA["tanah"], fontweight="bold", zorder=4)
    ax.text(24.2, 23.0, "Piksel campuran\n(mixed pixels)", ha="center", va="center",
            fontsize=8.0, color=WARNA["abu"], style="italic", zorder=4)

    for pt, warna, lbl, sub in (
        (p_pv, WARNA["hijau"], "Vegetasi Hijau (PV)", "NDVI tinggi, BSI rendah"),
        (p_bs, WARNA["tanah"], "Tanah Terbuka (BS)", "NDVI rendah, BSI tinggi"),
        (p_npv, WARNA["oranye"], "Serasah/Residu (NPV)", "NDVI rendah, serapan 2,1 µm"),
    ):
        ax.add_patch(Circle(pt, 1.3, fc=warna, ec="white", lw=1.0, zorder=5))
        dy = 3.2 if pt[1] > 20 else -3.6
        ax.text(pt[0], pt[1] + dy, f"{lbl}\n({sub})", ha="center", va="center",
                fontsize=7.8, fontweight="bold", color=warna, linespacing=1.15, zorder=5)

    # Panel (b): Perbandingan Blok Sawit Produktif vs Blok Peremajaan
    ax.text(77, 45.5, "(b) Keterbukaan tanah pada blok perkebunan kelapa sawit", ha="center", fontsize=10,
            fontweight="bold", color=WARNA["navy"])
    kotak(ax, 50, 2, 53, 41, isi=WARNA["latar"], warna=WARNA["abu_muda"], lw=1.0, r=1.0, zorder=1)

    # Sub-kotak kiri: Blok Produktif (TM)
    kotak(ax, 52, 9, 23.5, 29, isi="#C7E2B8", warna=WARNA["hijau"], lw=1.2, r=0.8, zorder=2)
    ax.text(63.75, 39.8, "Blok Sawit Produktif (TM)", ha="center", fontsize=8.8, fontweight="bold", color=WARNA["hijau"])
    for r_y in (14, 23, 32):
        for c_x in (56.5, 63.75, 71.0):
            ax.add_patch(Circle((c_x, r_y), 3.6, fc=WARNA["hijau"], ec="#2D5F28", lw=0.8, alpha=0.92, zorder=4))
            ax.add_patch(Circle((c_x, r_y), 1.1, fc=WARNA["tanah_muda"], ec="none", alpha=0.5, zorder=3))
    ax.add_patch(Rectangle((52.5, 17.8), 22.5, 1.4, fc="#D9B48F", ec="none", zorder=3))
    ax.text(63.75, 5.2, "Tajuk menutup rapat (>80%);\ntanah hanya terbuka sempit di\npiringan dan jalan panen (BSI < 0)",
            ha="center", va="center", fontsize=7.6, linespacing=1.15)

    # Sub-kotak kanan: Blok Peremajaan (Replanting / TBM)
    kotak(ax, 77.5, 9, 23.5, 29, isi=WARNA["tanah_muda"], warna=WARNA["tanah"], lw=1.2, r=0.8, zorder=2)
    ax.text(89.25, 39.8, "Blok Peremajaan (Replanting)", ha="center", fontsize=8.8, fontweight="bold", color=WARNA["tanah"])
    for r_y in (14, 23, 32):
        ax.add_patch(Rectangle((79.0, r_y - 3.8), 20.5, 1.2, fc="#A38350", ec="none", zorder=3))  # jalur rumpukan batang/NPV
        for c_x in (82.0, 89.25, 96.5):
            ax.add_patch(Circle((c_x, r_y), 1.1, fc="#68B045", ec="#2D5F28", lw=0.6, zorder=4))
    ax.text(89.25, 5.2, "Permukaan tanah terbuka luas\n(BSI > 0, NDVI rendah); jendela\nutama ekstraksi sifat tanah",
            ha="center", va="center", fontsize=7.6, linespacing=1.15)

    simpan(fig, MODUL, "M5-G01_bauran-spektral-dan-siklus-sawit.png")


# ---------------------------------------------------------------- Gambar 5.2
def g02_komposit_multitemporal():
    fig, ax = kanvas(10, 4.1, (0, 104), (0, 42))
    tahap = [
        ("Deret waktu citra\noptik ($t_1, t_2, \\dots, t_n$)", "Rekaman multi-musim\natau multi-tahun\n(Sentinel-2 / Landsat)", WARNA["biru"]),
        ("Penapisan kualitas\npiksel (Masking)", "Hapus awan, bayangan\nawan, dan tubuh air\nmenggunakan SCL/QA", WARNA["abu"]),
        ("Penyaringan indeks\ntanah terbuka", "Pilih piksel yang lolos:\nNDVImin < NDVI < NDVImax\nBSI > ambang & NBR2 rendah", WARNA["oranye"]),
        ("Agregasi statistik\nlintas waktu", "Hitung nilai median\nreflektansi per kanal dari\nseluruh tanggal terbuka", WARNA["teal"]),
        ("Komposit tanah\nterbuka sintetis", "Peta reflektansi tanah\n(SYSI / GEOS3) siap untuk\nestimasi sifat tanah", WARNA["tanah"]),
    ]
    w, jarak = 17.6, 20.6
    for i, (judul, isi, warna) in enumerate(tahap):
        x = 1.2 + i * jarak
        kotak(ax, x, 14, w, 19, isi=WARNA["putih"], warna=warna, lw=1.5, r=1.0)
        nomor(ax, x + w / 2, 33, i + 1, warna=warna, r=1.8, ukuran=9.5)
        ax.text(x + w / 2, 27.2, judul, ha="center", va="center", fontsize=8.8, fontweight="bold", color=warna, linespacing=1.15)
        ax.text(x + w / 2, 18.8, isi, ha="center", va="center", fontsize=7.7, color=WARNA["teks"], linespacing=1.15)
        if i < 4:
            panah(ax, x + w + 0.3, 23.5, x + jarak - 0.3, 23.5, warna=WARNA["navy"], lw=1.4)

    # Ilustrasi piksel lintas waktu di bagian bawah
    kotak(ax, 1.2, 1.5, 101.6, 9.5, isi=WARNA["latar"], warna=WARNA["abu_muda"], lw=0.9, r=0.8)
    ax.text(2.8, 6.2, "Ilustrasi satu piksel\npertanian/peremajaan:", ha="left", va="center", fontsize=7.8, fontweight="bold", color=WARNA["navy"])
    contoh_t = [
        ("$t_1$ (Jan)", "Berawan", "#CBD5E1", WARNA["merah"], "Dibuang"),
        ("$t_2$ (Apr)", "Tajuk rapat", WARNA["hijau"], WARNA["merah"], "Dibuang"),
        ("$t_3$ (Jul)", "Bera basah", WARNA["tanah_muda"], WARNA["hijau"], "Dipilih"),
        ("$t_4$ (Agu)", "Tanah terbuka", "#C89D7C", WARNA["hijau"], "Dipilih"),
        ("$t_5$ (Nov)", "Vegetatif", WARNA["hijau"], WARNA["merah"], "Dibuang"),
    ]
    for j, (t_lbl, kond, fc, col_st, st) in enumerate(contoh_t):
        x0 = 24.5 + j * 13.2
        ax.add_patch(Rectangle((x0, 2.8), 11.4, 6.8, fc=fc, ec=WARNA["navy"], lw=0.8, zorder=3))
        ax.text(x0 + 5.7, 7.6, t_lbl, ha="center", va="center", fontsize=7.3, fontweight="bold",
                color="white" if fc == WARNA["hijau"] else WARNA["teks"], zorder=4)
        ax.text(x0 + 5.7, 4.8, f"{kond}\n({st})", ha="center", va="center", fontsize=6.5, linespacing=1.05,
                color="white" if fc == WARNA["hijau"] else col_st, fontweight="bold", zorder=4)
    panah(ax, 90.0, 6.2, 93.2, 6.2, warna=WARNA["navy"], lw=1.3)
    ax.add_patch(Rectangle((93.8, 2.8), 7.8, 6.8, fc=WARNA["tanah"], ec=WARNA["navy"], lw=1.0, zorder=3))
    ax.text(97.7, 6.2, "Median\n($t_3, t_4$)", ha="center", va="center", fontsize=7.4, fontweight="bold", color="white", zorder=4)

    simpan(fig, MODUL, "M5-G02_metode-komposit-tanah-terbuka-multitemporal.png")


# ---------------------------------------------------------------- Gambar 5.3
def g03_peta_bsi_bompon(ind, kelas, mask, ext):
    batas = gaya.baca_layer("batas_subdas")[0][1]
    fig, axs = plt.subplots(1, 4, figsize=(10, 6.2))
    fig.subplots_adjust(left=0.01, right=0.99, top=0.88, bottom=0.15, wspace=0.05)

    # (a) BSI
    arr_bsi = np.ma.masked_where(~mask, ind["BSI"])
    im0 = axs[0].imshow(arr_bsi, extent=ext, cmap="RdYlGn_r", vmin=-0.42, vmax=0.05, interpolation="nearest")
    axs[0].set_title("(a) Bare Soil Index (BSI)\nSentinel-2, 21 Juli 2025", fontsize=8.8)
    cb0 = fig.colorbar(im0, ax=axs[0], orientation="horizontal", fraction=0.045, pad=0.03)
    cb0.ax.tick_params(labelsize=7.5)

    # (b) MBI
    arr_mbi = np.ma.masked_where(~mask, ind["MBI"])
    im1 = axs[1].imshow(arr_mbi, extent=ext, cmap="PuOr_r", vmin=0.02, vmax=0.36, interpolation="nearest")
    axs[1].set_title("(b) Modified Bare Soil Index\n(MBI)", fontsize=8.8)
    cb1 = fig.colorbar(im1, ax=axs[1], orientation="horizontal", fraction=0.045, pad=0.03)
    cb1.ax.tick_params(labelsize=7.5)

    # (c) NBR2
    arr_nbr2 = np.ma.masked_where(~mask, ind["NBR2"])
    im2 = axs[2].imshow(arr_nbr2, extent=ext, cmap="YlGnBu", vmin=0.18, vmax=0.42, interpolation="nearest")
    axs[2].set_title("(c) Normalized Burn Ratio 2\nNBR2 = (B11 − B12)/(B11 + B12)", fontsize=8.8)
    cb2 = fig.colorbar(im2, ax=axs[2], orientation="horizontal", fraction=0.045, pad=0.03)
    cb2.ax.tick_params(labelsize=7.5)

    # (d) Peta Kelas Keterbukaan Permukaan
    warna_k = ["#FFFFFF", "#2D6A4F", "#95D5B2", "#D97724", "#7B5EA7"]
    cmap_k = ListedColormap(warna_k)
    arr_k = np.where(mask, kelas, 0)
    axs[3].imshow(arr_k, extent=ext, cmap=cmap_k, vmin=0, vmax=4, interpolation="nearest")
    axs[3].set_title("(d) Kelas keterbukaan lahan\n(ambang NDVI dan BSI)", fontsize=8.8)
    unsur = [
        Patch(fc="#2D6A4F", label="Vegetasi rapat (82,4%)"),
        Patch(fc="#95D5B2", label="Vegetasi campuran (13,6%)"),
        Patch(fc="#D97724", label="Tanah terbuka/bera (1,8%)"),
        Patch(fc="#7B5EA7", label="Terbangun terbuka (2,2%)"),
    ]
    axs[3].legend(handles=unsur, loc="upper center", bbox_to_anchor=(0.5, -0.01), fontsize=7.2, frameon=False)

    for ax in axs:
        gaya.gambar_poligon(ax, batas, fc="none", ec=WARNA["navy"], lw=1.2)
        ax.set_xlim(ext[0] + 140, ext[1] - 140)
        ax.set_ylim(ext[2] + 140, ext[3] - 140)
        ax.set_xticks([]), ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)

    gaya.skala_batang(axs[0], ext[0] + 200, ext[2] + 220, 500, "500 m", tinggi=24)
    gaya.panah_utara(axs[0], 0.88, 0.88, 0.05)
    simpan(fig, MODUL, "M5-G03_peta-bsi-dan-deteksi-tanah-terbuka-bompon.png")


# ---------------------------------------------------------------- Gambar 5.4
def g04_ruang_fitur_dan_spektrum(b, ind, mask, pl, stat):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), gridspec_kw={"width_ratios": [1.08, 1.05]})
    fig.subplots_adjust(left=0.08, right=0.98, top=0.86, bottom=0.16, wspace=0.25)

    # Panel (a): Scatter NDVI vs BSI
    kelas_pl = list(gaya.WARNA_PENGGUNAAN)
    rng = np.random.default_rng(42)
    for i, nama in enumerate(kelas_pl, start=1):
        sel = mask & (pl == i)
        x_all = ind["NDVI"][sel]
        y_all = ind["BSI"][sel]
        idx = rng.choice(len(x_all), size=min(len(x_all), 900), replace=False)
        ax1.scatter(x_all[idx], y_all[idx], s=7, alpha=0.45, color=gaya.WARNA_PENGGUNAAN[nama], label=nama, edgecolors="none")

    ax1.axvline(0.55, color=WARNA["merah"], ls="--", lw=1.2)
    ax1.axhline(-0.12, color=WARNA["merah"], ls="--", lw=1.2)
    ax1.add_patch(Rectangle((0.02, -0.12), 0.53, 0.34, fc=WARNA["oranye"], alpha=0.12, ec="none", zorder=0))
    ax1.text(0.28, 0.14, "Jendela piksel tanah\nterbuka sebagian\n(NDVI < 0,55; BSI > −0,12)",
             ha="center", va="center", fontsize=7.8, color=WARNA["merah"], fontweight="bold")
    ax1.text(0.84, -0.37, f"r = {stat['korelasi_ndvi_bsi']:.2f}".replace(".", ","),
             ha="center", fontsize=8.5, fontweight="bold", color=WARNA["navy"])
    ax1.set_xlim(0.0, 0.98)
    ax1.set_ylim(-0.45, 0.23)
    ax1.set_xlabel("NDVI", fontsize=9)
    ax1.set_ylabel("Bare Soil Index (BSI)", fontsize=9)
    ax1.set_title("(a) Ruang fitur NDVI–BSI piksel Sub-DAS Bompon\nmenurut kelas penggunaan lahan", fontsize=9.2)
    ax1.legend(loc="lower left", fontsize=8, markerscale=1.8)
    ax1.grid(color=WARNA["abu_muda"], lw=0.5)

    # Panel (b): Kurva median reflektansi 4 kelompok keterbukaan
    kanal_urut = ["B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8A", "B11", "B12"]
    wl = np.array([0.490, 0.560, 0.665, 0.705, 0.740, 0.783, 0.842, 0.865, 1.610, 2.190])
    sp = stat["spektrum_median"]
    seri = [
        ("Vegetasi rapat (NDVI ≥ 0,75)", "Vegetasi rapat", "#2D6A4F", "-o"),
        ("Vegetasi campuran (0,55–0,75)", "Vegetasi campuran", WARNA["teal"], "-s"),
        ("Bera basah/terbuka sebagian", "Tanah terbuka/bera pertanian", WARNA["oranye"], "-^"),
        ("Permukaan terbuka kering (BSI > 0)", "Permukaan terbuka kering (BSI > 0)", WARNA["tanah"], "-D"),
    ]
    for label, kunci, warna, fmt in seri:
        ys = [sp[kunci][k] * 100 for k in kanal_urut]
        ax2.plot(wl, ys, fmt, color=warna, lw=1.8, markersize=4.2, label=label)

    for w_x, kn in zip([0.49, 0.56, 0.665, 0.842, 1.61, 2.19], ["B2", "B3", "B4", "B8", "B11", "B12"]):
        ax2.axvline(w_x, color=WARNA["abu_muda"], lw=0.6, ls=":", zorder=0)
        ax2.text(w_x, 0.7, kn, ha="center", va="bottom", fontsize=7.1, color=WARNA["abu"])

    ax2.set_xlim(0.42, 2.30)
    ax2.set_ylim(0, 38)
    ax2.set_xlabel("Panjang gelombang pusat kanal Sentinel-2 (µm)", fontsize=9)
    ax2.set_ylabel("Median reflektansi permukaan (%)", fontsize=9)
    ax2.set_title("(b) Perubahan pola spektral piksel dari vegetasi\nrapat menuju permukaan terbuka", fontsize=9.2)
    ax2.legend(loc="upper right", fontsize=7.3, framealpha=0.92)
    ax2.grid(axis="y", color=WARNA["abu_muda"], lw=0.5)

    simpan(fig, MODUL, "M5-G04_ruang-fitur-ndvi-bsi-bompon.png")


if __name__ == "__main__":
    gaya.atur()
    b, mask, pl, gt, ext = baca_sentinel2()
    ind = hitung_indeks_bsi(b)
    stat, kelas = analisis_modul_5(b, ind, mask, pl)
    print(json.dumps(stat, indent=2, ensure_ascii=False))
    g01_bauran_dan_siklus_sawit()
    g02_komposit_multitemporal()
    g03_peta_bsi_bompon(ind, kelas, mask, ext)
    g04_ruang_fitur_dan_spektrum(b, ind, mask, pl, stat)
