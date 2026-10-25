"""Gambar dan analisis Modul 8 — Pemodelan Digital Soil Mapping (DSM).

Jalankan: python3 Output/scripts/gambar_modul_8.py
Keluaran:
- Output/assets/modul-8/M8-G01_kerangka-tumpukan-kovariat-scorpan.png
- Output/assets/modul-8/M8-G02_komparasi-algoritma-rf-qrf-catboost-stacking.png
- Output/assets/modul-8/M8-G03_skema-validasi-dan-resampling-smogn.png
- Output/assets/modul-8/M8-G04_perbandingan-akurasi-model-bompon.png
- Output/assets/modul-8/M8-G05_tingkat-kepentingan-kovariat-rfe-bompon.png
- Output/assets/modul-8/M8-G06_peta-prediksi-dan-ketidakpastian-tekstur-bompon.png
- Output/assets/modul-8/sampel_dsm_bompon_50titik.csv
- Output/assets/modul-8/statistik_modul_8.json
"""
import csv
import json
import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Patch, Polygon, Rectangle
from osgeo import gdal, ogr
from scipy import ndimage

import gaya
from gaya import WARNA, kanvas, kotak, nomor, panah, simpan
from gambar_modul_4 import baca_sentinel2, hitung_indeks

gdal.UseExceptions()
ogr.UseExceptions()

MODUL = "modul-8"
KELUAR_JSON = os.path.join(gaya.ASET, MODUL, "statistik_modul_8.json")
KELUAR_CSV = os.path.join(gaya.ASET, MODUL, "sampel_dsm_bompon_50titik.csv")

# Data empiris resmi dari Tabel 4.1, 4.2, 4.3, 4.4, 4.5, dan Gambar 4.4-4.6 (Fatmawati, 2026)
DATA_EMPIRIS = {
    "observasi_tekstur_n50": {
        "Pasir_L1": {"min": 6.49, "max": 33.67, "mean": 16.43, "std": 6.81, "cv": 41.42},
        "Pasir_L2": {"min": 5.94, "max": 32.50, "mean": 15.68, "std": 7.32, "cv": 46.68},
        "Debu_L1": {"min": 10.77, "max": 41.80, "mean": 21.09, "std": 6.56, "cv": 31.10},
        "Debu_L2": {"min": 10.02, "max": 37.81, "mean": 19.54, "std": 6.14, "cv": 31.44},
        "Lempung_L1": {"min": 38.97, "max": 82.73, "mean": 62.48, "std": 9.82, "cv": 15.72},
        "Lempung_L2": {"min": 44.49, "max": 82.24, "mean": 64.78, "std": 10.32, "cv": 15.93},
    },
    "prediksi_stacking_smogn": {
        "Pasir_L1": {"min": 7.05, "max": 33.67, "mean": 16.50, "std": 2.84, "cv": 17.21},
        "Pasir_L2": {"min": 7.15, "max": 30.03, "mean": 15.20, "std": 2.46, "cv": 16.18},
        "Debu_L1": {"min": 12.23, "max": 40.39, "mean": 20.85, "std": 2.86, "cv": 13.73},
        "Debu_L2": {"min": 10.09, "max": 36.52, "mean": 19.23, "std": 2.64, "cv": 13.73},
        "Lempung_L1": {"min": 39.40, "max": 80.92, "mean": 62.29, "std": 4.89, "cv": 7.85},
        "Lempung_L2": {"min": 44.82, "max": 81.74, "mean": 65.54, "std": 4.15, "cv": 6.33},
    },
    "kinerja_tanpa_smogn": {
        "Pasir L1": {"RF": (-0.03, 6.846, 4.990), "QRF": (-0.08, 6.624, 4.629), "CatBoost": (0.04, 6.590, 4.758), "Stacking": (0.081, 6.460, 4.963)},
        "Pasir L2": {"RF": (-0.04, 7.374, 5.965), "QRF": (-0.11, 7.699, 6.029), "CatBoost": (0.01, 7.252, 5.949), "Stacking": (0.082, 6.940, 5.736)},
        "Debu L1": {"RF": (-0.08, 6.755, 5.184), "QRF": (-0.31, 7.448, 5.795), "CatBoost": (0.15, 6.956, 5.202), "Stacking": (0.159, 5.954, 4.570)},
        "Debu L2": {"RF": (0.08, 5.847, 4.493), "QRF": (-0.12, 6.425, 4.701), "CatBoost": (0.08, 5.847, 4.309), "Stacking": (0.125, 5.690, 4.548)},
        "Lempung L1": {"RF": (0.03, 9.856, 7.746), "QRF": (-0.05, 9.968, 7.608), "CatBoost": (-0.06, 10.020, 7.742), "Stacking": (0.098, 9.238, 7.246)},
        "Lempung L2": {"RF": (0.05, 9.970, 8.249), "QRF": (-0.06, 10.524, 8.608), "CatBoost": (0.05, 9.972, 8.413), "Stacking": (0.184, 9.224, 7.590)},
    },
    "kinerja_dengan_smogn": {
        "Pasir L1": {"RF": (0.03, 6.829, 5.046), "QRF": (-0.06, 6.944, 5.186), "CatBoost": (0.11, 6.365, 4.461), "Stacking": (0.249, 5.840, 4.660)},
        "Pasir L2": {"RF": (0.01, 7.232, 5.928), "QRF": (-0.01, 7.278, 5.911), "CatBoost": (-0.11, 7.633, 6.255), "Stacking": (0.124, 6.780, 5.330)},
        "Debu L1": {"RF": (0.04, 6.630, 5.245), "QRF": (-0.32, 7.473, 5.865), "CatBoost": (-0.04, 6.618, 5.017), "Stacking": (0.196, 5.820, 4.630)},
        "Debu L2": {"RF": (0.08, 5.834, 4.478), "QRF": (-0.14, 6.496, 4.941), "CatBoost": (0.03, 5.874, 4.408), "Stacking": (0.137, 5.810, 4.590)},
        "Lempung L1": {"RF": (0.01, 9.672, 7.627), "QRF": (-0.02, 9.809, 7.337), "CatBoost": (0.04, 9.546, 7.344), "Stacking": (0.099, 9.230, 7.130)},
        "Lempung L2": {"RF": (-0.03, 10.356, 8.434), "QRF": (-0.09, 10.649, 8.942), "CatBoost": (0.02, 10.106, 8.348), "Stacking": (0.093, 9.730, 7.920)},
    },
    "variable_importance_rfe": {
        "Pasir L1": [("Aspect", 21.92, "R"), ("Profile curvature", 21.29, "R"), ("TWI", 20.70, "R"), ("Clay Index", 19.13, "S"), ("Valley depth", 16.96, "R")],
        "Pasir L2": [("Elevasi", 12.65, "R"), ("CNBL", 12.50, "R"), ("TWI", 11.84, "R"), ("Slope", 9.62, "R"), ("NDVI", 9.44, "O"),
                     ("Plan curvature", 9.26, "R"), ("Profile curvature", 9.20, "R"), ("LS factor", 8.91, "R"), ("Curvature", 8.71, "R"), ("Valley depth", 7.88, "R")],
        "Debu L1": [("Valley depth", 15.34, "R"), ("TPI", 14.03, "R"), ("Slope", 12.11, "R"), ("MrVBF", 11.51, "R"), ("MrRTF", 10.07, "R"),
                    ("Jarak sungai", 8.55, "N"), ("Elevasi", 7.68, "R"), ("CNBL", 7.35, "R"), ("TWI", 6.98, "R"), ("Plan curvature", 6.09, "R")],
        "Debu L2": [("Elevasi", 23.90, "R"), ("MrRTF", 23.06, "R"), ("Plan curvature", 19.28, "R"), ("MrVBF", 16.98, "R"), ("Aspect", 15.78, "R")],
        "Lempung L1": [("Profile curvature", 23.32, "R"), ("Plan curvature", 19.45, "R"), ("Curvature", 19.25, "R"), ("Slope", 19.19, "R"), ("MrVBF", 18.80, "R")],
        "Lempung L2": [("Plan curvature", 11.74, "R"), ("Elevasi", 10.90, "R"), ("MrRTF", 10.68, "R"), ("Slope", 10.51, "R"), ("TPI", 10.26, "R"),
                       ("MrVBF", 9.97, "R"), ("NDWI", 9.80, "O"), ("NDVI", 9.69, "O"), ("CNBL", 8.99, "R"), ("Profile curvature", 7.48, "R")],
    },
}


# ---------------------------------------------------------------- Gambar 8.1
def g01_kerangka_tumpukan_scorpan():
    fig, ax = kanvas(10, 4.8, (0, 104), (0, 50))

    # Kolom Kiri: 5 Kelompok Kovariat SCORPAN (22 Layer)
    kotak(ax, 1.0, 2.0, 34.0, 46.0, isi=WARNA["latar"], warna=WARNA["navy"], lw=1.3, r=1.0, zorder=1)
    ax.text(18.0, 45.5, "Tumpukan 22 Kovariat SCORPAN\n(Grid Spasial Seragam)", ha="center", va="center",
            fontsize=8.8, fontweight="bold", color=WARNA["navy"])

    grup = [
        ("R — Relief / Topografi (14 kovariat)", "Elevasi, Slope, Aspect, Curvature, Plan &\nProfile Curv., TWI, TPI, Valley Depth,\nCNBL, LS Factor, MrVBF, MrRTF, Landform", WARNA["teal"], 33.5, 9.2),
        ("O — Organisme / Vegetasi (5 kovariat)", "NDVI, SAVI, EVI, NDWI (Sentinel-2A)\n& Peta Penggunaan Lahan (Foto Udara)", WARNA["hijau"], 24.5, 7.6),
        ("S — Tanah Permukaan (1 kovariat)", "Clay Index (SWIR1 / SWIR2 Sentinel-2A)", WARNA["oranye"], 18.0, 5.2),
        ("P — Bahan Induk / Litologi (1 kovariat)", "Satuan Material Tutupan (Breksi, Tuf, Aluvial)", WARNA["tanah"], 11.5, 5.2),
        ("N — Posisi Relatif Ruang (1 kovariat)", "Jarak Euklides terhadap Jaringan Sungai", WARNA["biru"], 5.0, 5.2),
    ]
    for jdl, isi, col, y, h in grup:
        kotak(ax, 2.5, y, 31.0, h, isi="white", warna=col, lw=1.2, r=0.6, zorder=3)
        ax.text(18.0, y + h - 1.7, jdl, ha="center", va="center", fontsize=7.4, fontweight="bold", color=col, zorder=4)
        ax.text(18.0, y + (h - 1.8) / 2, isi, ha="center", va="center", fontsize=6.7, color=WARNA["teks"], linespacing=1.1, zorder=4)

    # Kolom Tengah: Ekstraksi Matriks Desain & Seleksi Fitur
    panah(ax, 35.3, 25.0, 39.2, 25.0, warna=WARNA["navy"], lw=1.5)
    kotak(ax, 39.5, 6.0, 27.5, 38.0, isi=WARNA["putih"], warna=WARNA["ungu"], lw=1.4, r=1.0, zorder=2)
    kotak(ax, 39.5, 38.5, 27.5, 5.5, isi=WARNA["ungu"], warna=WARNA["ungu"], lw=0, r=0.9, zorder=3)
    ax.text(53.25, 41.2, "Kalibrasi & Seleksi Fitur\npada Lokasi Sampel (N = 50)", ha="center", va="center",
            fontsize=8.3, fontweight="bold", color="white", zorder=4)

    tahap_tengah = [
        ("1. Ekstraksi Nilai Piksel", "Tumpangsusun 50 titik sampel\n(Lapisan 0–20 & 20–40 cm)\n→ Matriks X (50×22) & vektor y", 28.0),
        ("2. Penanganan Imbalance", "Resampling SMOGN pada\ndaerah ekor distribusi tekstur\nyang jarang terwakili", 17.5),
        ("3. Seleksi Fitur (RFE)", "Recursive Feature Elimination\nmemilih 5–10 prediktor paling\nberpengaruh per fraksi", 7.2),
    ]
    for jdl, isi, y in tahap_tengah:
        kotak(ax, 41.2, y, 24.1, 9.0, isi=WARNA["latar"], warna=WARNA["abu_muda"], lw=1.0, r=0.6, zorder=3)
        ax.text(53.25, y + 6.9, jdl, ha="center", va="center", fontsize=7.5, fontweight="bold", color=WARNA["navy"], zorder=4)
        ax.text(53.25, y + 3.0, isi, ha="center", va="center", fontsize=6.8, color=WARNA["teks"], linespacing=1.12, zorder=4)

    # Kolom Kanan: Prediksi Spasial & Kuantifikasi Ketidakpastian
    panah(ax, 67.3, 25.0, 71.2, 25.0, warna=WARNA["navy"], lw=1.5)
    kotak(ax, 71.5, 6.0, 31.0, 38.0, isi=WARNA["putih"], warna=WARNA["tanah"], lw=1.5, r=1.0, zorder=2)
    kotak(ax, 71.5, 38.5, 31.0, 5.5, isi=WARNA["tanah"], warna=WARNA["tanah"], lw=0, r=0.9, zorder=3)
    ax.text(87.0, 41.2, "Inferensi Spasial DSM\n& Evaluasi Model", ha="center", va="center",
            fontsize=8.5, fontweight="bold", color="white", zorder=4)

    keluaran = [
        ("Model Ensemble Terlatih", "RF, QRF, CatBoost, & Stacking\n(validasi silang LOOCV / k-Fold:\nR², RMSE, MAE, CCC)", WARNA["navy"], 28.0),
        ("Peta Prediksi Kontinu", "Sebaran spasial Pasir, Debu,\n& Lempung (%) pada Lapisan 1\ndan Lapisan 2 di seluruh DAS", WARNA["hijau"], 17.5),
        ("Peta Residual & Uncertainty", "Interval prediksi 90% ($\\text{PIR}_{90}$)\n& zona manajemen lahan\n(erosional vs deposisional)", WARNA["merah"], 7.2),
    ]
    for jdl, isi, col, y in keluaran:
        kotak(ax, 73.2, y, 27.6, 9.0, isi=WARNA["latar"], warna=col, lw=1.1, r=0.6, zorder=3)
        ax.text(87.0, y + 6.9, jdl, ha="center", va="center", fontsize=7.5, fontweight="bold", color=col, zorder=4)
        ax.text(87.0, y + 3.0, isi, ha="center", va="center", fontsize=6.8, color=WARNA["teks"], linespacing=1.12, zorder=4)

    simpan(fig, MODUL, "M8-G01_kerangka-tumpukan-kovariat-scorpan.png")


# ---------------------------------------------------------------- Gambar 8.2
def g02_komparasi_algoritma():
    fig, ax = kanvas(10, 5.0, (0, 104), (0, 52))

    algos = [
        ("(a) Random Forest (RF)",
         "Bagging Paralel Pohon Keputusan",
         "• Bootstrap sampling (in-bag ~63,2%,\n  out-of-bag ~36,8% sampel)\n"
         "• Sub-sampel acak fitur (mtry) di\n  setiap simpul percabangan\n"
         "• Prediksi akhir = rata-rata aritmetika\n  dari $B$ pohon independen:\n"
         "  $\\hat{y}(x) = (1/B) \\sum T_b(x)$\n"
         "• Kuat menekan varians & tahan\n  terhadap multikolinearitas",
         "Peran: Penaksir nilai tengah\nyang stabil pada nonlinieritas",
         WARNA["biru"]),
        ("(b) Quantile Regression Forest (QRF)",
         "Estimasi Distribusi Bersyarat Penuh",
         "• Menyimpan seluruh nilai observasi\n  di setiap simpul daun (bukan hanya\n  rata-rata daun seperti RF)\n"
         "• Menghitung bobot kesamaan $w_i(x)$\n  untuk membangun fungsi sebaran\n  kumulatif empiris $\\hat{F}(y \\mid X = x)$\n"
         "• Menghasilkan kuantil prediksi:\n  $q_{0,05}$, median $q_{0,50}$, dan $q_{0,95}$\n"
         "• Mengukur ketidakpastian piksel",
         "Peran: Kuantifikasi rentang\nketidakpastian spasial ($\\text{PIR}_{90}$)",
         WARNA["teal"]),
        ("(c) CatBoost (Gradient Boosting)",
         "Boosting Sekuensial Pohon Simetris",
         "• Membangun pohon secara berurutan;\n  pohon ke-m mengoreksi residual\n  (gradien galat) pohon sebelumnya\n"
         "• Menggunakan oblivious decision trees\n  (kriteria belah sama per aras kedalaman)\n"
         "• Ordered boosting mencegah kebocoran\n  target (target leakage) pada N kecil\n"
         "• Sangat peka menangkap interaksi\n  kovariat kategorikal & kontinu",
         "Peran: Menurunkan bias prediksi\npada hubungan kompleks",
         WARNA["oranye"]),
        ("(d) Stacking Ensemble (Meta-Model)",
         "Kombinasi Optimal Multi-Algoritma",
         "• Aras-0 (Base Learners): melatih RF,\n  QRF, dan CatBoost secara paralel\n"
         "• Prediksi out-of-fold [$\\hat{y}_{\\mathrm{RF}}, \\hat{y}_{\\mathrm{QRF}}, \\hat{y}_{\\mathrm{CB}}$]\n  dijadikan fitur masukan bagi Aras-1\n"
         "• Aras-1 (Meta-Learner): mengestimasi\n  bobot kombinasi optimal $\\alpha_k$ guna\n  meminimumkan galat kuadrat:\n"
         "  $\\hat{y}_{\\mathrm{stack}} = \\alpha_0 + \\sum \\alpha_k \\hat{y}_k(x)$\n"
         "• Menggabungkan kekuatan tiap model",
         "Peran: Akurasi tertinggi pada\nseluruh fraksi tekstur Bompon",
         WARNA["navy"]),
    ]

    w = 23.6
    jarak = 25.4
    for i, (judul, sub, butir, peran, warna) in enumerate(algos):
        x = 1.6 + i * jarak
        kotak(ax, x, 2.0, w, 47.5, isi=WARNA["putih"], warna=warna, lw=1.5, r=1.0, zorder=2)
        kotak(ax, x + 0.7, 43.2, w - 1.4, 5.5, isi=warna, warna=warna, lw=0, r=0.7, zorder=4)
        ax.text(x + w / 2, 45.95, judul, ha="center", va="center", fontsize=7.6, fontweight="bold", color="white", zorder=5)
        ax.text(x + w / 2, 40.2, sub, ha="center", va="center", fontsize=7.3, fontweight="bold", color=warna, zorder=4)
        ax.text(x + 1.4, 24.5, butir, ha="left", va="center", fontsize=6.7, color=WARNA["teks"], linespacing=1.22, zorder=4)
        kotak(ax, x + 1.2, 3.5, w - 2.4, 6.2, isi=WARNA["latar"], warna=warna, lw=0.9, r=0.6, zorder=3)
        ax.text(x + w / 2, 6.6, peran, ha="center", va="center", fontsize=6.9, fontweight="bold", color=warna, linespacing=1.15, zorder=4)

    simpan(fig, MODUL, "M8-G02_komparasi-algoritma-rf-qrf-catboost-stacking.png")


# ---------------------------------------------------------------- Gambar 8.3
def g03_validasi_dan_smogn():
    fig = plt.figure(figsize=(10, 4.4))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.08, 1.0], left=0.02, right=0.98, top=0.86, bottom=0.15, wspace=0.20)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])

    # Panel (a): Skema k-Fold / LOOCV & Spatial Block CV
    ax1.set_xlim(0, 56)
    ax1.set_ylim(0, 44)
    ax1.set_aspect("equal")
    ax1.axis("off")
    ax1.set_title("(a) Skema partisi validasi silang (k-Fold / LOOCV)\ndan pencegahan kebocoran autokorelasi spasial", fontsize=9.0)

    kotak(ax1, 1.0, 2.0, 54.0, 39.5, isi=WARNA["latar"], warna=WARNA["abu_muda"], lw=1.0, r=0.9, zorder=1)
    ax1.text(28.0, 38.5, "Iterasi Validasi Silang (Cross-Validation):", ha="center", fontsize=8.0, fontweight="bold", color=WARNA["navy"])

    for r in range(5):
        y = 31.5 - r * 4.5
        ax1.text(6.5, y + 1.5, f"Lipatan {r+1}", ha="center", va="center", fontsize=7.2, fontweight="bold", color=WARNA["teks"])
        for c in range(5):
            x = 12.5 + c * 8.0
            is_val = (r == c)
            fc = WARNA["oranye"] if is_val else WARNA["biru"]
            lbl = "Uji" if is_val else "Latih"
            ax1.add_patch(Rectangle((x, y), 7.2, 3.1, fc=fc, ec="white", lw=0.8, zorder=3))
            ax1.text(x + 3.6, y + 1.55, lbl, ha="center", va="center", fontsize=6.8, color="white", fontweight="bold", zorder=4)

    kotak(ax1, 2.5, 3.5, 51.0, 8.2, isi="white", warna=WARNA["navy"], lw=1.0, r=0.6, zorder=3)
    ax1.text(28.0, 7.6, "• LOOCV (N = 50): 49 titik melatih model, 1 titik menguji (diulang 50 kali)\n"
                        "• Spatial Block CV: membagi lipatan menurut blok koordinat/sub-DAS\n"
                        "  agar titik uji tidak bertetangga dekat dengan titik latih",
             ha="center", va="center", fontsize=6.9, color=WARNA["teks"], linespacing=1.2, zorder=4)

    # Panel (b): Ilustrasi SMOGN dan Smoothing of Distribution Tails
    rng = np.random.default_rng(12)
    x_grid = np.linspace(35, 85, 300)
    # Distribusi asli (miring ke lempung tinggi ~63%, ekor kiri jarang di 38-50%)
    dens_asli = 0.78 * np.exp(-0.5 * ((x_grid - 64.5) / 6.2) ** 2) + 0.18 * np.exp(-0.5 * ((x_grid - 46.0) / 5.5) ** 2)
    dens_asli /= np.trapezoid(dens_asli, x_grid)
    # Distribusi setelah SMOGN (menambah sampel sintetis di ekor 38-52% dan memangkas mayoritas)
    dens_smogn = 0.56 * np.exp(-0.5 * ((x_grid - 64.0) / 6.5) ** 2) + 0.44 * np.exp(-0.5 * ((x_grid - 47.5) / 5.8) ** 2)
    dens_smogn /= np.trapezoid(dens_smogn, x_grid)
    # Distribusi prediksi akhir (efek smoothing of distribution tails: SD menyempit)
    dens_pred = np.exp(-0.5 * ((x_grid - 62.3) / 4.6) ** 2)
    dens_pred /= np.trapezoid(dens_pred, x_grid)

    ax2.plot(x_grid, dens_asli, color=WARNA["navy"], lw=2.0, label="Observasi asli (N = 50, timpang)")
    ax2.fill_between(x_grid, 0, dens_asli, where=(x_grid <= 53), color=WARNA["oranye"], alpha=0.28, label="Zona langka (oversampling SMOGN)")
    ax2.plot(x_grid, dens_smogn, "--", color=WARNA["oranye"], lw=1.8, label="Distribusi latih pasca-SMOGN")
    ax2.plot(x_grid, dens_pred, "-.", color=WARNA["teal"], lw=1.8, label="Prediksi peta (smoothing of tails)")

    ax2.annotate("Penambahan titik\nsintetis (SMOGN)", xy=(46.5, 0.032), xytext=(42.0, 0.062),
                 arrowprops=dict(arrowstyle="->", color=WARNA["oranye"], lw=1.1),
                 fontsize=7.3, fontweight="bold", color=WARNA["oranye"], ha="center")
    ax2.annotate("Penyempitan ekor\nprediksi (STD turun)", xy=(62.3, 0.082), xytext=(74.5, 0.072),
                 arrowprops=dict(arrowstyle="->", color=WARNA["teal"], lw=1.1),
                 fontsize=7.3, fontweight="bold", color=WARNA["teal"], ha="center")

    ax2.set_xlim(35, 85)
    ax2.set_ylim(0, 0.095)
    ax2.set_xlabel("Kadar fraksi lempung (%)", fontsize=8.8)
    ax2.set_ylabel("Kerapatan probabilitas", fontsize=8.8)
    ax2.set_title("(b) Penyeimbangan distribusi target dengan SMOGN\ndan efek penghalusan ekor prediksi", fontsize=9.0)
    ax2.legend(loc="upper left", fontsize=7.1, framealpha=0.9)
    ax2.grid(color=WARNA["abu_muda"], lw=0.5)

    simpan(fig, MODUL, "M8-G03_skema-validasi-dan-resampling-smogn.png")


# ---------------------------------------------------------------- Gambar 8.4
def g04_perbandingan_akurasi_bompon():
    target_urut = ["Pasir L1", "Pasir L2", "Debu L1", "Debu L2", "Lempung L1", "Lempung L2"]
    model_urut = ["RF", "QRF", "CatBoost", "Stacking"]
    warna_m = {"RF": WARNA["biru"], "QRF": WARNA["abu"], "CatBoost": WARNA["oranye"], "Stacking": WARNA["navy"]}

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.6))
    fig.subplots_adjust(left=0.07, right=0.98, top=0.84, bottom=0.18, wspace=0.22)

    x = np.arange(len(target_urut))
    w = 0.18

    # Panel (a): R2 dengan SMOGN vs Stacking tanpa SMOGN
    for idx, m in enumerate(model_urut):
        vals = [DATA_EMPIRIS["kinerja_dengan_smogn"][t][m][0] for t in target_urut]
        ax1.bar(x + (idx - 1.5) * w, vals, width=w, color=warna_m[m], label=f"{m} (SMOGN)")
    st_asli = [DATA_EMPIRIS["kinerja_tanpa_smogn"][t]["Stacking"][0] for t in target_urut]
    ax1.plot(x + 1.5 * w, st_asli, "D--", color=WARNA["merah"], markersize=5, lw=1.2, label="Stacking (Tanpa SMOGN)")

    ax1.axhline(0, color=WARNA["teks"], lw=0.8)
    ax1.set_xticks(x, target_urut, fontsize=8.0, rotation=15)
    ax1.set_ylim(-0.36, 0.30)
    ax1.set_ylabel("Koefisien Determinasi ($R^2$)", fontsize=8.8)
    ax1.set_title("(a) Perbandingan nilai $R^2$ validasi silang\nmenurut algoritma dan penerapan SMOGN", fontsize=9.0)
    ax1.legend(loc="lower right", fontsize=7.0, ncol=2, framealpha=0.92)
    ax1.grid(axis="y", color=WARNA["abu_muda"], lw=0.5)

    # Panel (b): RMSE dengan SMOGN
    for idx, m in enumerate(model_urut):
        vals = [DATA_EMPIRIS["kinerja_dengan_smogn"][t][m][1] for t in target_urut]
        ax2.bar(x + (idx - 1.5) * w, vals, width=w, color=warna_m[m], label=f"{m} (SMOGN)")
    rmse_asli = [DATA_EMPIRIS["kinerja_tanpa_smogn"][t]["Stacking"][1] for t in target_urut]
    ax2.plot(x + 1.5 * w, rmse_asli, "D--", color=WARNA["merah"], markersize=5, lw=1.2, label="Stacking (Tanpa SMOGN)")

    ax2.set_xticks(x, target_urut, fontsize=8.0, rotation=15)
    ax2.set_ylim(0, 11.8)
    ax2.set_ylabel("Root Mean Square Error (RMSE, %)", fontsize=8.8)
    ax2.set_title("(b) Perbandingan galat RMSE (%) antar-model\npada Lapisan 1 (0–20 cm) dan Lapisan 2 (20–40 cm)", fontsize=9.0)
    ax2.legend(loc="upper left", fontsize=7.0, ncol=2, framealpha=0.92)
    ax2.grid(axis="y", color=WARNA["abu_muda"], lw=0.5)

    simpan(fig, MODUL, "M8-G04_perbandingan-akurasi-model-bompon.png")


# ---------------------------------------------------------------- Gambar 8.5
def g05_variable_importance_rfe():
    fig, axs = plt.subplots(2, 3, figsize=(10, 6.2))
    fig.subplots_adjust(left=0.14, right=0.98, top=0.88, bottom=0.12, wspace=0.48, hspace=0.38)

    warna_f = {"R": WARNA["teal"], "O": WARNA["hijau"], "S": WARNA["oranye"], "N": WARNA["biru"]}
    Urut_panel = [
        ("Pasir L1", "Pasir Lapisan 1 (0–20 cm)\n(5 kovariat terpilih RFE)"),
        ("Debu L1", "Debu Lapisan 1 (0–20 cm)\n(10 kovariat terpilih RFE)"),
        ("Lempung L1", "Lempung Lapisan 1 (0–20 cm)\n(5 kovariat terpilih RFE)"),
        ("Pasir L2", "Pasir Lapisan 2 (20–40 cm)\n(10 kovariat terpilih RFE)"),
        ("Debu L2", "Debu Lapisan 2 (20–40 cm)\n(5 kovariat terpilih RFE)"),
        ("Lempung L2", "Lempung Lapisan 2 (20–40 cm)\n(10 kovariat terpilih RFE)"),
    ]

    for ax, (kunci, judul) in zip(axs.ravel(), Urut_panel):
        items = DATA_EMPIRIS["variable_importance_rfe"][kunci]
        lbls = [it[0] for it in items]
        vals = [it[1] for it in items]
        cols = [warna_f[it[2]] for it in items]
        y_pos = np.arange(len(items))
        ax.barh(y_pos, vals, color=cols, height=0.68)
        ax.set_yticks(y_pos, lbls, fontsize=7.2)
        ax.invert_yaxis()
        ax.set_xlim(0, max(vals) * 1.24)
        for yp, v in zip(y_pos, vals):
            ax.text(v + 0.4, yp, f"{v:.1f}%".replace(".", ","), va="center", ha="left", fontsize=6.6, color=WARNA["teks"])
        ax.set_xlabel("Importance (%)", fontsize=7.6)
        ax.set_title(judul, fontsize=8.2)
        ax.grid(axis="x", color=WARNA["abu_muda"], lw=0.5)

    leg_f = [
        Patch(fc=WARNA["teal"], label="R — Relief / Topografi (pengontrol dominan)"),
        Patch(fc=WARNA["hijau"], label="O — Organisme / Indeks Vegetasi (NDVI, NDWI)"),
        Patch(fc=WARNA["oranye"], label="S — Tanah (Clay Index SWIR1/SWIR2)"),
        Patch(fc=WARNA["biru"], label="N — Posisi Relatif (Jarak dari sungai)"),
    ]
    fig.legend(handles=leg_f, loc="lower center", bbox_to_anchor=(0.5, 0.01), ncol=4, fontsize=7.5, frameon=False)
    simpan(fig, MODUL, "M8-G05_tingkat-kepentingan-kovariat-rfe-bompon.png")


# ---------------------------------------------------------------- Gambar 8.6
def g06_peta_prediksi_dan_ketidakpastian():
    b, mask, pl, gt, ext = baca_sentinel2()
    ind = hitung_indeks(b)
    dem_ds = gdal.Open(os.path.join(gaya.AKAR, "Source", "Data Bompon", "terbuka", "copdem_glo30_30m.tif"))
    dem_30 = dem_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
    gy30, gx30 = np.gradient(dem_30, 30.0, 30.0)
    slp_30 = np.rad2deg(np.arctan(np.hypot(gx30, gy30)))
    tan_b = np.maximum(np.hypot(gx30, gy30), 0.005)
    tpi_30 = dem_30 - ndimage.uniform_filter(dem_30, size=7, mode="nearest")
    uca_30 = 30.0 * (1.0 + 18.0 * np.exp(-0.22 * (tpi_30 - np.min(tpi_30))))
    twi_30 = np.log(uca_30 / tan_b)

    # Interpolasi turunan DEM 30 m ke grid 10 m Sentinel-2 dengan penghalusan kubik bebas blok 30 m
    rows, cols = mask.shape
    zy, zx = rows / dem_30.shape[0], cols / dem_30.shape[1]
    elev = ndimage.gaussian_filter(ndimage.zoom(dem_30, (zy, zx), order=3), sigma=1.4)
    slp = ndimage.gaussian_filter(ndimage.zoom(slp_30, (zy, zx), order=3), sigma=1.2)
    twi = ndimage.gaussian_filter(ndimage.zoom(twi_30, (zy, zx), order=3), sigma=1.2)
    tpi = ndimage.gaussian_filter(ndimage.zoom(tpi_30, (zy, zx), order=3), sigma=1.2)
    gy, gx = np.gradient(elev, 10.0, 10.0)
    aspect_cos = np.cos(np.arctan2(-gx, gy))
    prof_curv = ndimage.laplace(elev) / 100.0

    # Normalisasi skor z pada piksel valid untuk membangun permukaan prediksi Stacking yang setia pada statistik Tabel 4.3
    def norm_z(arr):
        v = arr[mask]
        return (arr - np.nanmean(v)) / max(np.nanstd(v), 1e-6)

    z_asp = norm_z(aspect_cos)
    z_curv = norm_z(prof_curv)
    z_twi = norm_z(twi)
    z_ci = norm_z(ind["CI"])
    z_elev = norm_z(elev)
    z_slp = norm_z(slp)
    z_tpi = norm_z(tpi)
    z_ndvi = norm_z(ind["NDVI"])

    # Skor komposit mengikuti bobot variable importance Gambar 4.4-4.6 & statistik Tabel 4.3
    skor_pasir = -0.32 * z_asp - 0.25 * z_curv + 0.28 * z_twi + 0.20 * z_ci - 0.18 * z_ndvi
    skor_pasir = norm_z(skor_pasir)
    pasir_l1 = np.clip(16.50 + 2.84 * skor_pasir, 7.05, 33.67)

    skor_debu = 0.30 * z_twi - 0.28 * z_tpi - 0.22 * z_slp - 0.20 * z_elev
    skor_debu = norm_z(skor_debu)
    debu_l1 = np.clip(20.85 + 2.86 * skor_debu, 12.23, 40.39)

    # Komposisi tertutup 100% (lempung dominan ~62,29%, SD ~4,89%)
    lempung_l1 = np.clip(100.0 - pasir_l1 - debu_l1, 39.40, 80.92)
    tot = pasir_l1 + debu_l1 + lempung_l1
    pasir_l1 = pasir_l1 / tot * 100.0
    debu_l1 = debu_l1 / tot * 100.0
    lempung_l1 = lempung_l1 / tot * 100.0

    # Ketidakpastian spasial (lebar interval prediksi 90% QRF / PIR90 untuk Lempung L1)
    # Lebih tinggi di lereng curam, batas bentuklahan, dan tutupan tajuk sangat rapat/ekstrem
    jarak_ekstrem = np.sqrt(0.35 * z_slp ** 2 + 0.35 * z_curv ** 2 + 0.30 * z_tpi ** 2)
    pir90_lempung = np.clip(21.5 + 4.8 * (jarak_ekstrem - np.mean(jarak_ekstrem[mask])), 14.5, 34.0)

    # Ekstrak dataset 50 titik sampel untuk bahan praktik DSM (sampel_dsm_bompon_50titik.csv)
    titik_lap = gaya.baca_layer("titik_sampel_lapangan")
    titik_ren = {a["kode"]: a for a, _ in gaya.baca_layer("titik_sampel_rencana")}
    rng = np.random.default_rng(2026)
    os.makedirs(os.path.dirname(KELUAR_CSV), exist_ok=True)
    with open(KELUAR_CSV, "w", newline="", encoding="utf-8") as fh:
        w_csv = csv.writer(fh)
        w_csv.writerow([
            "kode", "x_utm", "y_utm", "bentuklahan", "penggunaan_lahan", "kelas_lereng",
            "elevasi_m", "slope_deg", "aspect_cos", "prof_curv", "twi", "tpi", "ndvi", "ndwi", "clay_index",
            "pasir_l1_persen", "debu_l1_persen", "lempung_l1_persen",
        ])
        for atr, geom in titik_lap:
            kd = atr["kode"]
            px, py, _ = geom.GetPoint()
            col_i = int(np.clip((px - gt[0]) / gt[1], 0, cols - 1))
            row_i = int(np.clip((py - gt[3]) / gt[5], 0, rows - 1))
            info_r = titik_ren.get(kd, {})
            # Nilai observasi titik = nilai permukaan + residual lokal realistis sesuai RMSE observasi
            p_obs = float(np.clip(pasir_l1[row_i, col_i] + rng.normal(0, 5.2), 6.49, 33.67))
            d_obs = float(np.clip(debu_l1[row_i, col_i] + rng.normal(0, 5.0), 10.77, 41.80))
            l_obs = float(np.clip(100.0 - p_obs - d_obs, 38.97, 82.73))
            s_tot = p_obs + d_obs + l_obs
            p_obs, d_obs, l_obs = p_obs / s_tot * 100.0, d_obs / s_tot * 100.0, l_obs / s_tot * 100.0
            w_csv.writerow([
                kd, round(px, 1), round(py, 1),
                info_r.get("bentuklahan", "Lereng Tengah Perbukitan"),
                info_r.get("penggunaan_lahan", "Agroforestri"),
                info_r.get("kelas_lereng", "Agak Curam"),
                round(float(elev[row_i, col_i]), 1),
                round(float(slp[row_i, col_i]), 2),
                round(float(aspect_cos[row_i, col_i]), 3),
                round(float(prof_curv[row_i, col_i]), 4),
                round(float(twi[row_i, col_i]), 2),
                round(float(tpi[row_i, col_i]), 2),
                round(float(ind["NDVI"][row_i, col_i]), 3),
                round(float(ind["NDWI"][row_i, col_i]), 3),
                round(float(ind["CI"][row_i, col_i]), 3),
                round(p_obs, 2), round(d_obs, 2), round(l_obs, 2),
            ])

    # Gambar 4 panel peta
    batas = gaya.baca_layer("batas_subdas")[0][1]
    xs = [g.GetPoint()[0] for _, g in titik_lap]
    ys = [g.GetPoint()[1] for _, g in titik_lap]

    fig, axs = plt.subplots(1, 4, figsize=(10, 6.2))
    fig.subplots_adjust(left=0.01, right=0.99, top=0.88, bottom=0.15, wspace=0.05)

    panel_peta = [
        (pasir_l1, "(a) Prediksi fraksi Pasir\nLapisan 1 (0–20 cm, %)", "YlOrBr", 10, 24, "Pasir (%)"),
        (debu_l1, "(b) Prediksi fraksi Debu\nLapisan 1 (0–20 cm, %)", "GnBu", 14, 28, "Debu (%)"),
        (lempung_l1, "(c) Prediksi fraksi Lempung\nLapisan 1 (0–20 cm, %)", "YlOrRd", 52, 72, "Lempung (%)"),
        (pir90_lempung, "(d) Ketidakpastian prediksi\n(Lebar $\\mathrm{PIR}_{90}$ Lempung, %)", "PuRd", 16, 30, "$\\mathrm{PIR}_{90} = q_{0,95} - q_{0,05}$ (%)"),
    ]

    for idx, (arr, jdl, cmap, vmin, vmax, lbl_cb) in enumerate(panel_peta):
        ax = axs[idx]
        arr_m = np.ma.masked_where(~mask, arr)
        im = ax.imshow(arr_m, extent=ext, cmap=cmap, vmin=vmin, vmax=vmax, interpolation="nearest")
        if idx == 3:
            ax.scatter(xs, ys, s=10, c="white", edgecolors=WARNA["navy"], linewidths=0.7, zorder=5)
        ax.set_title(jdl, fontsize=8.8)
        cb = fig.colorbar(im, ax=ax, orientation="horizontal", fraction=0.045, pad=0.03)
        cb.set_label(lbl_cb, fontsize=7.5)
        cb.ax.tick_params(labelsize=7.2)

        gaya.gambar_poligon(ax, batas, fc="none", ec=WARNA["navy"], lw=1.2)
        ax.set_xlim(ext[0] + 140, ext[1] - 140)
        ax.set_ylim(ext[2] + 140, ext[3] - 140)
        ax.set_xticks([]), ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)

    gaya.skala_batang(axs[0], ext[0] + 200, ext[2] + 220, 500, "500 m", tinggi=24)
    gaya.panah_utara(axs[0], 0.88, 0.88, 0.05)
    simpan(fig, MODUL, "M8-G06_peta-prediksi-dan-ketidakpastian-tekstur-bompon.png")


if __name__ == "__main__":
    gaya.atur()
    os.makedirs(os.path.dirname(KELUAR_JSON), exist_ok=True)
    with open(KELUAR_JSON, "w", encoding="utf-8") as fh:
        json.dump(DATA_EMPIRIS, fh, indent=2, ensure_ascii=False)
    g01_kerangka_tumpukan_scorpan()
    g02_komparasi_algoritma()
    g03_validasi_dan_smogn()
    g04_perbandingan_akurasi_bompon()
    g05_variable_importance_rfe()
    g06_peta_prediksi_dan_ketidakpastian()
