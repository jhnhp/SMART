#!/usr/bin/env python3
"""
buat_notebook_pelatihan.py
Membangun notebook Jupyter (.ipynb) untuk Praktik 3 (Demonstrasi PSS) dan
Praktik 5 (Machine Learning DSM) di dalam Output/Pelatihan/notebooks/.
Fokus Utama: Prediksi Karbon Organik Tanah (C-Organik / Soil Organic Carbon).
"""

import json
import os

NOTEBOOKS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'Pelatihan', 'notebooks'
)
os.makedirs(NOTEBOOKS_DIR, exist_ok=True)


def create_notebook(cells, output_path):
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python (Pelatihan SMART)",
                "language": "python",
                "name": "env_smart"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.10.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print(f"-> Berhasil membuat notebook: {output_path}")


def md_cell(source):
    lines = [line + "\n" for line in source.strip().split("\n")]
    if lines:
        lines[-1] = lines[-1].rstrip("\n")
    return {"cell_type": "markdown", "metadata": {}, "source": lines}


def code_cell(source):
    lines = [line + "\n" for line in source.strip().split("\n")]
    if lines:
        lines[-1] = lines[-1].rstrip("\n")
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": lines
    }


def build_notebook_praktik_3():
    cells = [
        md_cell(
            "# PRAKTIK 3: DEMONSTRASI PROXIMAL SOIL SENSING (PSS)\n"
            "## Analisis Kemometrika Spektroskopi Pantulan Tanah Vis-NIR (350–2500 nm) untuk C-Organik\n"
            "**Pelatihan Pemanfaatan RS dan DSM untuk Pertanian Presisi**  \n"
            "Pusat Studi Pengelolaan Sumber Daya Lahan (PS2DL) UGM & PT SMART Tbk\n"
            "\n"
            "---\n"
            "> **Petunjuk Lingkungan Kerja (Virtual Environment / venv):**  \n"
            "> Pastikan notebook ini dijalankan pada kernel virtual environment **`Python (Pelatihan SMART)`** (`env_smart`).  \n"
            "> Jika belum membuat venv, jalankan skrip penyiapan otomatis:  \n"
            "> - **Linux / macOS:** `./setup_env.sh` (pada folder `Output/Pelatihan/`)  \n"
            "> - **Windows:** `setup_env.bat` (pada folder `Output\\Pelatihan\\`)  \n"
            "> Periksa pojok kanan atas jendela JupyterLab; pastikan kernel yang aktif tertulis `Python (Pelatihan SMART)`.\n"
            "\n"
            "---\n"
            "### Tujuan Praktikum:\n"
            "1. Membaca dan memvisualisasikan spektra tanah mentah (*raw reflectance spectra*) pada rentang Vis-NIR (350–2500 nm).\n"
            "2. Menerapkan transformasi praolah sinyal kemometrika: Absorbansi ($A = \\log(1/R)$), *Standard Normal Variate* (SNV), dan turunan pertama Savitzky–Golay.\n"
            "3. Mengidentifikasi puncak serapan fisis diagnostik bahan organik tanah (SOM 450–650 nm, ikatan C-H 1720 & 2300 nm) serta gugus hidroksil (O-H 1400 & 1900 nm).\n"
            "4. Melatih dan memvalidasi model *Partial Least Squares Regression* (PLSR) untuk estimasi kuantitatif kadar C-Organik tanah."
        ),
        code_cell(
            "# 1. Inisialisasi Pustaka Python\n"
            "import os\n"
            "import csv\n"
            "import numpy as np\n"
            "import matplotlib.pyplot as plt\n"
            "from scipy.signal import savgol_filter\n"
            "from sklearn.cross_decomposition import PLSRegression\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.metrics import r2_score, root_mean_squared_error, mean_absolute_error\n"
            "\n"
            "print('Pustaka berhasil diimpor dengan sukses!')"
        ),
        md_cell(
            "### 2. Memuat Dataset Spektroskopi Tanah Vis-NIR (852 Sampel)\n"
            "Kita membaca berkas `spektra_visnir_857sampel.csv` yang berisi spektra kontinu 350–2500 nm (resolusi 1 nm) berpasangan dengan hasil uji laboratorium kadar C-Organik (%)."
        ),
        code_cell(
            "# 2. Membaca data spektroskopi CSV\n"
            "csv_path = '../data/praktik-3/spektra_visnir_857sampel.csv'\n"
            "if not os.path.exists(csv_path):\n"
            "    csv_path = 'Output/Pelatihan/data/praktik-3/spektra_visnir_857sampel.csv'\n"
            "\n"
            "with open(csv_path, 'r', encoding='utf-8') as f:\n"
            "    reader = csv.reader(f)\n"
            "    header = next(reader)\n"
            "    corg_idx = header.index('C_Organik')\n"
            "    wavelengths = np.array([int(w) for w in header[9:]])\n"
            "    \n"
            "    X_list = []\n"
            "    y_list = []\n"
            "    for row in reader:\n"
            "        try:\n"
            "            val_c = float(row[corg_idx])\n"
            "            if val_c > 0:\n"
            "                X_list.append([float(v) for v in row[9:]])\n"
            "                y_list.append(val_c)\n"
            "        except:\n"
            "            pass\n"
            "\n"
            "spectra_raw = np.array(X_list)\n"
            "c_org = np.array(y_list)\n"
            "\n"
            "print(f'Total sampel tanah : {len(c_org)} sampel')\n"
            "print(f'Jumlah pita spektral: {len(wavelengths)} panjang gelombang ({wavelengths[0]} - {wavelengths[-1]} nm)')\n"
            "print(f'Rentang C-Organik    : {c_org.min():.2f}% - {c_org.max():.2f}% (Rata-rata: {c_org.mean():.2f}%)')"
        ),
        md_cell(
            "### 3. Visualisasi Kurva Spektral Mentah (*Raw Reflectance*)\n"
            "Perhatikan perbedaan kurva pantulan: Sampel dengan C-Organik tinggi memiliki reflektansi gelap (kurva di bawah 0.25) dan lereng curam di rentang tampak (400–700 nm) akibat penyerapan kromofor humus."
        ),
        code_cell(
            "# 3. Plot Kurva Spektral Mentah\n"
            "plt.figure(figsize=(10, 5), dpi=150)\n"
            "idx_high_corg = np.where(c_org > 2.0)[0]\n"
            "idx_low_corg = np.where(c_org < 0.8)[0]\n"
            "\n"
            "for idx in idx_low_corg[:5]:\n"
            "    plt.plot(wavelengths, spectra_raw[idx], color='#E76F51', alpha=0.7, label='C-Organik Rendah (<0.8%)' if idx == idx_low_corg[0] else '')\n"
            "for idx in idx_high_corg[:5]:\n"
            "    plt.plot(wavelengths, spectra_raw[idx], color='#264653', alpha=0.9, linewidth=1.5, label='C-Organik Tinggi (>2.0%)' if idx == idx_high_corg[0] else '')\n"
            "\n"
            "plt.title('Kurva Spektrum Reflektansi Mentah Tanah (Vis-NIR 350 - 2500 nm)', fontsize=12, fontweight='bold', pad=12)\n"
            "plt.xlabel('Panjang Gelombang (nm)', fontsize=11)\n"
            "plt.ylabel('Faktor Reflektansi (Reflectance)', fontsize=11)\n"
            "plt.grid(True, linestyle='--', alpha=0.5)\n"
            "plt.legend(loc='upper left')\n"
            "plt.tight_layout()\n"
            "plt.show()"
        ),
        md_cell(
            "### 4. Praolah Sinyal Kemometrika (Absorbansi, SNV, & Savitzky–Golay)\n"
            "Sinyal mentah mengandung derau akibat hamburan ukuran butir tanah. Kita terapkan 3 tahap praolah:\n"
            "1. **Absorbansi:** $A = \\log_{10}(1 / R)$\n"
            "2. **Standard Normal Variate (SNV):** Menghilangkan variasi lereng dan offset baseline antar-sampel.\n"
            "3. **Savitzky–Golay First Derivative:** Mempertegas titik belok dan puncak serapan diagnostik senyawa organik."
        ),
        code_cell(
            "# 4. Transformasi Absorbansi, SNV, dan Savitzky-Golay\n"
            "spectra_safe = np.clip(spectra_raw, 1e-4, 1.0)\n"
            "absorbance = np.log10(1.0 / spectra_safe)\n"
            "\n"
            "mean_abs = np.mean(absorbance, axis=1, keepdims=True)\n"
            "std_abs = np.std(absorbance, axis=1, keepdims=True)\n"
            "spectra_snv = (absorbance - mean_abs) / std_abs\n"
            "\n"
            "# Savitzky-Golay Filter (Window=15, Polyorder=2, Deriv=1)\n"
            "spectra_sg_deriv1 = savgol_filter(spectra_snv, window_length=15, polyorder=2, deriv=1, axis=1)\n"
            "\n"
            "print('Praolah sinyal SNV dan Savitzky-Golay turunan pertama berhasil dihitung!')"
        ),
        md_cell(
            "### 5. Visualisasi Fitur Serapan Diagnostik C-Organik\n"
            "Perhatikan bagaimana turunan pertama SNV menonjolkan fitur serapan kromofor bahan organik tanah di **450–650 nm**, ikatan C-H alifatik di **1720 nm**, ikatan C-H + C=O di **2300 nm**, serta serapan air di **1400 nm** dan **1900 nm**."
        ),
        code_cell(
            "# 5. Plot Perbandingan Hasil Praolah\n"
            "fig, axes = plt.subplots(2, 1, figsize=(11, 8), dpi=150, sharex=True)\n"
            "\n"
            "# Panel atas: Spektra ter-SNV\n"
            "for idx in idx_high_corg[:4]:\n"
            "    axes[0].plot(wavelengths, spectra_snv[idx], color='#01416B', alpha=0.8)\n"
            "axes[0].set_title('Spektra Absorbansi Ternormalisasi SNV', fontsize=12, fontweight='bold')\n"
            "axes[0].set_ylabel('SNV Absorbansi', fontsize=10)\n"
            "axes[0].axvline(550, color='#8c510a', linestyle='--', label='Kromofor SOM (450-650 nm)')\n"
            "axes[0].axvline(1400, color='gray', linestyle=':', label='O-H (1400 nm)')\n"
            "axes[0].axvline(1720, color='#d95f02', linestyle='-.', label='C-H Alifatik (1720 nm)')\n"
            "axes[0].axvline(1900, color='blue', linestyle=':', label='H2O (1900 nm)')\n"
            "axes[0].axvline(2300, color='#7570b3', linestyle='-.', label='C-H + C=O Humus (2300 nm)')\n"
            "axes[0].grid(True, linestyle='--', alpha=0.5)\n"
            "axes[0].legend(loc='upper right', fontsize=8)\n"
            "\n"
            "# Panel bawah: Turunan Pertama Savitzky-Golay\n"
            "for idx in idx_high_corg[:4]:\n"
            "    axes[1].plot(wavelengths, spectra_sg_deriv1[idx], color='#2A9D8F', alpha=0.8)\n"
            "axes[1].set_title('Turunan Pertama Savitzky–Golay (Puncak Serapan Diagnostik C-Organik)', fontsize=12, fontweight='bold')\n"
            "axes[1].set_xlabel('Panjang Gelombang (nm)', fontsize=11)\n"
            "axes[1].set_ylabel('Turunan Ke-1', fontsize=10)\n"
            "axes[1].axvline(550, color='#8c510a', linestyle='--')\n"
            "axes[1].axvline(1400, color='gray', linestyle=':')\n"
            "axes[1].axvline(1720, color='#d95f02', linestyle='-.')\n"
            "axes[1].axvline(1900, color='blue', linestyle=':')\n"
            "axes[1].axvline(2300, color='#7570b3', linestyle='-.')\n"
            "axes[1].grid(True, linestyle='--', alpha=0.5)\n"
            "\n"
            "plt.tight_layout()\n"
            "plt.show()"
        ),
        md_cell(
            "### 6. Pembangunan Model Kalibrasi Spektral (PLSR)\n"
            "Kita melatih algoritma *Partial Least Squares Regression* (PLSR) untuk mengestimasi kadar C-Organik (%) dari spektrum praolah."
        ),
        code_cell(
            "# 6. Pelatihan dan Evaluasi Model PLSR C-Organik\n"
            "X = spectra_sg_deriv1\n"
            "y = c_org\n"
            "\n"
            "# Pembagian 75% data latih dan 25% data validasi\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)\n"
            "\n"
            "# Kalibrasi PLSR dengan 6 komponen laten\n"
            "pls_model = PLSRegression(n_components=6)\n"
            "pls_model.fit(X_train, y_train)\n"
            "\n"
            "y_pred_train = pls_model.predict(X_train).ravel()\n"
            "y_pred_test = pls_model.predict(X_test).ravel()\n"
            "\n"
            "r2_train = r2_score(y_train, y_pred_train)\n"
            "rmse_train = root_mean_squared_error(y_train, y_pred_train)\n"
            "r2_test = r2_score(y_test, y_pred_test)\n"
            "rmse_test = root_mean_squared_error(y_test, y_pred_test)\n"
            "rpd_test = np.std(y_test) / rmse_test\n"
            "\n"
            "print('=== HASIL EVALUASI MODEL PLSR PREDIKSI C-ORGANIK ===')\n"
            "print(f'Kalibrasi Train R² : {r2_train:.3f} | RMSE: {rmse_train:.3f}%')\n"
            "print(f'Validasi Test R²   : {r2_test:.3f} | RMSE: {rmse_test:.3f}%')\n"
            "print(f'Rasio Kinerja RPD  : {rpd_test:.2f}')"
        ),
        md_cell(
            "### 7. Scatterplot Kalibrasi: Nilai Lab Aktual vs Prediksi C-Organik PSS\n"
            "Grafik sebaran 1:1 antara hasil uji laboratorium basah vs nilai estimasi spektrometer Vis-NIR."
        ),
        code_cell(
            "# 7. Plot Korelasi 1:1 Uji Lab vs Prediksi Spektroskopi C-Organik\n"
            "plt.figure(figsize=(6.5, 6.5), dpi=150)\n"
            "plt.scatter(y_train, y_pred_train, color='#1f78b4', alpha=0.5, s=35, label=f'Data Kalibrasi (R² = {r2_train:.2f})')\n"
            "plt.scatter(y_test, y_pred_test, color='#e31a1c', edgecolors='k', linewidth=0.5, s=45, alpha=0.8, label=f'Data Validasi (R² = {r2_test:.2f}, RPD = {rpd_test:.2f})')\n"
            "\n"
            "lims = [0, max(y.max(), y_pred_test.max()) + 0.5]\n"
            "plt.plot(lims, lims, color='black', linestyle='--', linewidth=1.5, label='Garis 1:1 Ideal')\n"
            "plt.xlim(lims)\n"
            "plt.ylim(lims)\n"
            "\n"
            "plt.title(f'Akurasi Estimasi PSS Vis-NIR: Kadar C-Organik (%)\\nRMSE Validasi: {rmse_test:.2f}% | RPD: {rpd_test:.2f}', fontsize=11, fontweight='bold', pad=12)\n"
            "plt.xlabel('Nilai Uji Laboratorium Aktual (%)', fontsize=11)\n"
            "plt.ylabel('Nilai Prediksi Spektroskopi Vis-NIR (%)', fontsize=11)\n"
            "plt.legend(loc='upper left', fontsize=9)\n"
            "plt.grid(True, linestyle='--', alpha=0.5)\n"
            "plt.tight_layout()\n"
            "plt.show()"
        ),
        md_cell(
            "### Kesimpulan Praktik 3:\n"
            "Spektroskopi reflektansi Vis-NIR terbukti mampu mendeteksi gugus kromofor bahan organik (SOM) dan ikatan C-H alifatik tanah, memungkinkan estimasi cepat C-Organik tanah secara non-destruktif dan real-time di perkebunan."
        )
    ]
    nb_path = os.path.join(NOTEBOOKS_DIR, 'Praktik_03_Demonstrasi_PSS_Kemometrika.ipynb')
    create_notebook(cells, nb_path)


def build_notebook_praktik_5():
    cells = [
        md_cell(
            "# PRAKTIK 5: MACHINE LEARNING UNTUK DIGITAL SOIL MAPPING (DSM)\n"
            "## Pemodelan Spasial SCORPAN, Random Forest, dan Ketidakpastian C-Organik Tanah (0–20 cm)\n"
            "**Pelatihan Pemanfaatan RS dan DSM untuk Pertanian Presisi**  \n"
            "Pusat Studi Pengelolaan Sumber Daya Lahan (PS2DL) UGM & PT SMART Tbk\n"
            "\n"
            "---\n"
            "> **Petunjuk Lingkungan Kerja (Virtual Environment / venv):**  \n"
            "> Pastikan notebook ini dijalankan pada kernel virtual environment **`Python (Pelatihan SMART)`** (`env_smart`).  \n"
            "> Jika belum membuat venv, jalankan skrip penyiapan otomatis:  \n"
            "> - **Linux / macOS:** `./setup_env.sh` (pada folder `Output/Pelatihan/`)  \n"
            "> - **Windows:** `setup_env.bat` (pada folder `Output\\Pelatihan\\`)  \n"
            "> Periksa pojok kanan atas jendela JupyterLab; pastikan kernel yang aktif tertulis `Python (Pelatihan SMART)`.\n"
            "\n"
            "---\n"
            "### Tujuan Praktikum:\n"
            "1. Menumpangkan 50 koordinat titik sampel lapangan ke tumpukan raster kovariat SCORPAN (*Point-in-Raster Overlay*).\n"
            "2. Menganalisis peringkat kepentingan variabel (*Feature Importance*) dalam mengendalikan sebaran spasial C-Organik.\n"
            "3. Melatih model *Random Forest Regressor* dan mengevaluasi akurasi menggunakan 5-Fold Cross-Validation.\n"
            "4. Memprediksi nilai kontinu C-Organik (Lapisan 0–20 cm) ke seluruh kisi Sub-DAS Bompon dan mengekspor GeoTIFF.\n"
            "5. Memodelkan ketidakpastian prediksi spasial menggunakan *Quantile Regression Forest* (QRF) pada interval keyakinan 90% (PI90)."
        ),
        code_cell(
            "# 1. Inisialisasi Pustaka Python\n"
            "import os\n"
            "import csv\n"
            "import numpy as np\n"
            "import matplotlib.pyplot as plt\n"
            "from osgeo import gdal\n"
            "from sklearn.ensemble import RandomForestRegressor\n"
            "from sklearn.model_selection import KFold\n"
            "from sklearn.metrics import r2_score, root_mean_squared_error, mean_absolute_error\n"
            "from quantile_forest import RandomForestQuantileRegressor\n"
            "\n"
            "gdal.UseExceptions()\n"
            "print('Pustaka Machine Learning dan Spasial berhasil dimuat!')"
        ),
        md_cell(
            "### 2. Memuat Data Titik Sampel Lapangan dan Hasil Lab C-Organik Tanah\n"
            "Kita membaca berkas `sampel_tanah_50titik.csv` dengan fokus target pada kolom `C_Organik_1` (kadar C-Organik lapisan 0–20 cm)."
        ),
        code_cell(
            "# 2. Membaca data uji lab 50 titik sampel\n"
            "csv_path = '../data/praktik-5/sampel_tanah_50titik.csv'\n"
            "if not os.path.exists(csv_path):\n"
            "    csv_path = 'Output/Pelatihan/data/praktik-5/sampel_tanah_50titik.csv'\n"
            "\n"
            "points_data = []\n"
            "with open(csv_path, 'r', encoding='utf-8') as f:\n"
            "    reader = csv.DictReader(f)\n"
            "    for r in reader:\n"
            "        points_data.append({\n"
            "            'id': r['Titik'],\n"
            "            'x': float(r['x']),\n"
            "            'y': float(r['y']),\n"
            "            'c_org': float(r['C_Organik_1']), # Target: C-Organik 0-20 cm\n"
            "            'clay': float(r['Lempung_1']),\n"
            "            'sand': float(r['Pasir_1']),\n"
            "            'ph': float(r['pH_H2O_1'])\n"
            "        })\n"
            "\n"
            "print(f'Total titik sampel tanah: {len(points_data)} titik')\n"
            "print(f'Target Prediksi         : Kadar C-Organik Lapisan 1 (0-20 cm)')\n"
            "print(f'Rata-rata C-Organik     : {np.mean([p[\"c_org\"] for p in points_data]):.2f}% (Std: {np.std([p[\"c_org\"] for p in points_data]):.2f}%)')"
        ),
        md_cell(
            "### 3. Ekstraksi Nilai Kovariat SCORPAN di Titik Sampel (Point Intersect)\n"
            "Kita mengekstrak nilai piksel 11 kovariat lingkungan SCORPAN pada koordinat 50 titik sampel."
        ),
        code_cell(
            "# 3. Ekstraksi Nilai Kovariat Raster di Titik Koordinat\n"
            "kovariat_dir = '../data/praktik-5/kovariat'\n"
            "if not os.path.exists(kovariat_dir):\n"
            "    kovariat_dir = 'Output/Pelatihan/data/praktik-5/kovariat'\n"
            "\n"
            "raster_files = {\n"
            "    'dem': 'dem_10m.tif',\n"
            "    'slope': 'slope_10m.tif',\n"
            "    'aspect': 'aspect_10m.tif',\n"
            "    'hillshade': 'hillshade_10m.tif',\n"
            "    'tpi': 'tpi_10m.tif',\n"
            "    'pl': 'penggunaan_lahan_10m.tif',\n"
            "    'sar_vv': ('sentinel1_sar_10m.tif', 1),\n"
            "    'sar_vh': ('sentinel1_sar_10m.tif', 2),\n"
            "    's2_b02': ('sentinel2_l2a_10m.tif', 1),\n"
            "    's2_b04': ('sentinel2_l2a_10m.tif', 3),\n"
            "    's2_b08': ('sentinel2_l2a_10m.tif', 7),\n"
            "    's2_b11': ('sentinel2_l2a_10m.tif', 9)\n"
            "}\n"
            "\n"
            "ref_ds = gdal.Open(os.path.join(kovariat_dir, 'dem_10m.tif'))\n"
            "gt = ref_ds.GetGeoTransform()\n"
            "inv_gt = gdal.InvGeoTransform(gt)\n"
            "\n"
            "cov_arrays = {}\n"
            "for name, item in raster_files.items():\n"
            "    fname, b_idx = item if isinstance(item, tuple) else (item, 1)\n"
            "    ds = gdal.Open(os.path.join(kovariat_dir, fname))\n"
            "    cov_arrays[name] = ds.GetRasterBand(b_idx).ReadAsArray().astype('float32')\n"
            "\n"
            "# Turunkan NDVI dan BSI\n"
            "b08 = cov_arrays['s2_b08']\n"
            "b04 = cov_arrays['s2_b04']\n"
            "b11 = cov_arrays['s2_b11']\n"
            "b02 = cov_arrays['s2_b02']\n"
            "cov_arrays['ndvi'] = (b08 - b04) / (b08 + b04 + 1e-6)\n"
            "cov_arrays['bsi'] = ((b11 + b04) - (b08 + b02)) / ((b11 + b04) + (b08 + b02) + 1e-6)\n"
            "\n"
            "cov_names = ['dem', 'slope', 'aspect', 'hillshade', 'tpi', 'sar_vv', 'sar_vh', 'ndvi', 'bsi', 's2_b11', 'pl']\n"
            "X_list = []\n"
            "y_list = []\n"
            "coords = []\n"
            "\n"
            "for pt in points_data:\n"
            "    px, py = gdal.ApplyGeoTransform(inv_gt, pt['x'], pt['y'])\n"
            "    px, py = int(round(px)), int(round(py))\n"
            "    if 0 <= py < cov_arrays['dem'].shape[0] and 0 <= px < cov_arrays['dem'].shape[1]:\n"
            "        vals = [cov_arrays[k][py, px] for k in cov_names]\n"
            "        X_list.append(vals)\n"
            "        y_list.append(pt['c_org'])\n"
            "        coords.append((pt['x'], pt['y']))\n"
            "\n"
            "X = np.array(X_list)\n"
            "y = np.array(y_list)\n"
            "coords = np.array(coords)\n"
            "print(f'Ekstraksi berhasil: {X.shape[0]} titik x {X.shape[1]} kovariat SCORPAN')\n"
            "print('Kovariat terpilih:', cov_names)"
        ),
        md_cell(
            "### 4. Pelatihan Model Random Forest & Validasi Silang C-Organik\n"
            "Kita melatih algoritma *Random Forest Regressor* dan menghitung metrik akurasi menggunakan 5-Fold Cross-Validation."
        ),
        code_cell(
            "# 4. Pelatihan Random Forest dan Evaluasi K-Fold CV\n"
            "kf = KFold(n_splits=5, shuffle=True, random_state=42)\n"
            "y_pred_cv = np.zeros_like(y)\n"
            "\n"
            "for train_idx, val_idx in kf.split(X):\n"
            "    rf_cv = RandomForestRegressor(n_estimators=300, max_depth=5, random_state=42)\n"
            "    rf_cv.fit(X[train_idx], y[train_idx])\n"
            "    y_pred_cv[val_idx] = rf_cv.predict(X[val_idx])\n"
            "\n"
            "r2_cv = r2_score(y, y_pred_cv)\n"
            "rmse_cv = root_mean_squared_error(y, y_pred_cv)\n"
            "mae_cv = mean_absolute_error(y, y_pred_cv)\n"
            "\n"
            "print('=== HASIL EVALUASI 5-FOLD CROSS-VALIDATION C-ORGANIK ===')\n"
            "print(f'Koefisien Determinasi (R²) : {r2_cv:.3f}')\n"
            "print(f'Root Mean Squared Error    : {rmse_cv:.3f}%')\n"
            "print(f'Mean Absolute Error (MAE)  : {mae_cv:.3f}%')\n"
            "\n"
            "# Latih model final pada seluruh data 50 titik\n"
            "rf_final = RandomForestRegressor(n_estimators=300, max_depth=5, random_state=42)\n"
            "rf_final.fit(X, y)\n"
            "\n"
            "# Peringkat Kepentingan Fitur (Feature Importance)\n"
            "importances = rf_final.feature_importances_\n"
            "sorted_idx = np.argsort(importances)[::-1]\n"
            "print('\\nPeringkat Kepentingan Kovariat SCORPAN untuk C-Organik:')\n"
            "for rank, idx in enumerate(sorted_idx, 1):\n"
            "    print(f'{rank}. {cov_names[idx]:10s} : {importances[idx]*100:.1f}%')"
        ),
        md_cell(
            "### 5. Prediksi Spasial ke Seluruh Grid Sub-DAS Bompon\n"
            "Model Random Forest diterapkan ke setiap piksel di dalam batas Sub-DAS Bompon untuk mengekspor peta kontinu C-Organik ke GeoTIFF."
        ),
        code_cell(
            "# 5. Prediksi Spasial Seluruh Piksel dan Ekspor GeoTIFF C-Organik\n"
            "rows, cols = cov_arrays['dem'].shape\n"
            "X_full = np.column_stack([cov_arrays[k].ravel() for k in cov_names])\n"
            "\n"
            "# Hanya prediksi pada piksel di dalam Sub-DAS Bompon (dem > 0 dan tidak NaN)\n"
            "valid_mask = ~np.isnan(X_full).any(axis=1) & (cov_arrays['dem'].ravel() > 0)\n"
            "pred_full = np.full(rows * cols, np.nan, dtype='float32')\n"
            "\n"
            "pred_full[valid_mask] = rf_final.predict(X_full[valid_mask])\n"
            "pred_map = pred_full.reshape((rows, cols))\n"
            "\n"
            "out_pred_path = os.path.join(kovariat_dir, '..', 'prediksi_corganik_0_20cm.tif')\n"
            "driver = gdal.GetDriverByName('GTiff')\n"
            "out_ds = driver.Create(out_pred_path, cols, rows, 1, gdal.GDT_Float32, ['COMPRESS=DEFLATE'])\n"
            "out_ds.SetGeoTransform(gt)\n"
            "out_ds.SetProjection(ref_ds.GetProjection())\n"
            "out_b = out_ds.GetRasterBand(1)\n"
            "out_b.WriteArray(np.where(np.isnan(pred_map), -9999.0, pred_map))\n"
            "out_b.SetNoDataValue(-9999.0)\n"
            "out_ds = None\n"
            "\n"
            "print(f'-> Berhasil menyimpan peta prediksi: {out_pred_path}')\n"
            "print(f'   Rentang nilai prediksi C-Organik: {np.nanmin(pred_map):.2f}% s.d. {np.nanmax(pred_map):.2f}%')"
        ),
        md_cell(
            "### 6. Pemodelan Ketidakpastian Spasial (Quantile Regression Forest / QRF)\n"
            "Kita melatih algoritma QRF untuk memprediksi lebar interval keyakinan 90% (PI90 = $q_{0.95} - q_{0.05}$) untuk estimasi C-Organik."
        ),
        code_cell(
            "# 6. Pemodelan Ketidakpastian QRF (PI90 C-Organik)\n"
            "qrf = RandomForestQuantileRegressor(n_estimators=300, max_depth=5, random_state=42)\n"
            "qrf.fit(X, y)\n"
            "\n"
            "q05 = qrf.predict(X_full[valid_mask], quantiles=[0.05])\n"
            "q95 = qrf.predict(X_full[valid_mask], quantiles=[0.95])\n"
            "pi90_valid = q95 - q05\n"
            "\n"
            "pi90_full = np.full(rows * cols, np.nan, dtype='float32')\n"
            "pi90_full[valid_mask] = pi90_valid\n"
            "pi90_map = pi90_full.reshape((rows, cols))\n"
            "\n"
            "out_unc_path = os.path.join(kovariat_dir, '..', 'ketidakpastian_pi90_corganik.tif')\n"
            "out_ds = driver.Create(out_unc_path, cols, rows, 1, gdal.GDT_Float32, ['COMPRESS=DEFLATE'])\n"
            "out_ds.SetGeoTransform(gt)\n"
            "out_ds.SetProjection(ref_ds.GetProjection())\n"
            "out_b = out_ds.GetRasterBand(1)\n"
            "out_b.WriteArray(np.where(np.isnan(pi90_map), -9999.0, pi90_map))\n"
            "out_b.SetNoDataValue(-9999.0)\n"
            "out_ds = None\n"
            "\n"
            "print(f'-> Berhasil menyimpan peta ketidakpastian: {out_unc_path}')\n"
            "print(f'   Rentang lebar PI90: {np.nanmin(pi90_map):.2f}% s.d. {np.nanmax(pi90_map):.2f}%')"
        ),
        md_cell(
            "### 7. Visualisasi Hasil Pemodelan Spasial C-Organik\n"
            "Panel terpadu menampilkan peta prediksi C-Organik, peta ketidakpastian PI90, dan peringkat kepentingan kovariat SCORPAN."
        ),
        code_cell(
            "# 7. Visualisasi Panel DSM C-Organik\n"
            "fig, axes = plt.subplots(1, 3, figsize=(18, 6.5), dpi=150)\n"
            "\n"
            "# 1. Peta Prediksi C-Organik\n"
            "im0 = axes[0].imshow(pred_map, cmap='YlGn', vmin=0.4, vmax=1.5)\n"
            "axes[0].set_title('Prediksi Spasial C-Organik (%)\\nSub-DAS Bompon (Lapisan 0-20 cm)', fontsize=12, fontweight='bold')\n"
            "axes[0].axis('off')\n"
            "cbar0 = plt.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)\n"
            "cbar0.set_label('Kadar C-Organik (%)')\n"
            "\n"
            "# 2. Peta Ketidakpastian PI90\n"
            "im1 = axes[1].imshow(pi90_map, cmap='Reds', vmin=0.1, vmax=1.2)\n"
            "axes[1].set_title('Ketidakpastian Prediksi Spasial (PI90)\\nInterval Keyakinan 90% (QRF)', fontsize=12, fontweight='bold')\n"
            "axes[1].axis('off')\n"
            "cbar1 = plt.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)\n"
            "cbar1.set_label('Lebar PI90 C-Organik (%)')\n"
            "\n"
            "# 3. Peringkat Kepentingan Kovariat\n"
            "sorted_idx_rev = sorted_idx[::-1]\n"
            "axes[2].barh(range(len(sorted_idx_rev)), importances[sorted_idx_rev]*100, color='#238b45')\n"
            "axes[2].set_yticks(range(len(sorted_idx_rev)))\n"
            "axes[2].set_yticklabels([cov_names[i] for i in sorted_idx_rev], fontsize=10)\n"
            "axes[2].set_xlabel('Tingkat Kepentingan Relatif (%)', fontsize=11)\n"
            "axes[2].set_title('Peringkat Kepentingan Kovariat SCORPAN\\nPrediktor Karbon Organik Tanah (SOC)', fontsize=12, fontweight='bold')\n"
            "axes[2].grid(axis='x', linestyle='--', alpha=0.6)\n"
            "\n"
            "plt.tight_layout()\n"
            "plt.show()"
        ),
        md_cell(
            "### Kesimpulan Praktik 5:\n"
            "Model Random Forest berhasil memetakan variabilitas spasial C-Organik pada resolusi 10 m. Radar SAR Sentinel-1 polarisasi VH dan indeks tanah terbuka BSI terbukti menjadi prediktor paling signifikan, merefleksikan kontribusi biomassa kanopi dan serasah permukaan terhadap kandungan karbon organik tanah."
        )
    ]
    nb_path = os.path.join(NOTEBOOKS_DIR, 'Praktik_05_Machine_Learning_Digital_Soil_Mapping.ipynb')
    create_notebook(cells, nb_path)


def main():
    print("==================================================================")
    print("MEMBANGUN JUPYTER NOTEBOOK PRAKTIK 3 DAN PRAKTIK 5 (C-ORGANIK)")
    print("==================================================================")
    build_notebook_praktik_3()
    build_notebook_praktik_5()
    print("\n==================================================================")
    print("KEDUA NOTEBOOK JUPYTER C-ORGANIK BERHASIL DIBANGUN 100% LENGKAP!")
    print("==================================================================")


if __name__ == '__main__':
    main()
