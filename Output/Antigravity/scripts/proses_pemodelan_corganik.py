"""
Skrip Pemodelan Spasial dan Spektroskopi Berbasis Target C-Organik (Soil Organic Carbon)
- Praktik 3: Praolah Vis-NIR & Kalibrasi PLSR C-Organik (852 Sampel)
- Praktik 5: Ekstraksi Kovariat SCORPAN, Random Forest & QRF C-Organik Lapisan 0-20 cm (50 Titik)
"""

import os
import csv
import numpy as np
from osgeo import gdal
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from sklearn.cross_decomposition import PLSRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, KFold, cross_val_predict
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from quantile_forest import RandomForestQuantileRegressor

BASE_DIR = "/home/jhn/Documents/Sayangku/Modul Junun"
SCREENSHOT_DIR = os.path.join(BASE_DIR, "Output/Pelatihan/screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# =====================================================================
# 1. PRAKTIK 3: KEMOMETRIKA PSS C-ORGANIK
# =====================================================================
print("=== [1/2] MEMPROSES PRAKTIK 3: PSS C-ORGANIK ===")
p3_csv = f"{BASE_DIR}/Output/Pelatihan/data/praktik-3/spektra_visnir_857sampel.csv"

with open(p3_csv) as f:
    reader = csv.reader(f)
    header = next(reader)
    corg_idx = header.index("C_Organik")
    wave_cols = [int(w) for w in header[9:]]
    
    X_raw_list = []
    y_corg_list = []
    for row in reader:
        try:
            val_c = float(row[corg_idx])
            if val_c > 0:
                spec = [float(v) for v in row[9:]]
                X_raw_list.append(spec)
                y_corg_list.append(val_c)
        except:
            pass

X_raw = np.array(X_raw_list)
y_corg_p3 = np.array(y_corg_list)
wavelengths = np.array(wave_cols)

# Preprocessing: Absorbance + SNV + SG 1st derivative
X_abs = np.log10(1.0 / np.clip(X_raw, 1e-4, 1.0))
mean_spec = np.mean(X_abs, axis=1, keepdims=True)
std_spec = np.std(X_abs, axis=1, keepdims=True)
X_snv = (X_abs - mean_spec) / std_spec
X_sg1 = savgol_filter(X_snv, window_length=15, polyorder=2, deriv=1, axis=1)

# Model PLSR C-Organik
X_tr, X_te, y_tr, y_te = train_test_split(X_sg1, y_corg_p3, test_size=0.25, random_state=42)
pls = PLSRegression(n_components=6)
pls.fit(X_tr, y_tr)

y_tr_pred = pls.predict(X_tr).ravel()
y_te_pred = pls.predict(X_te).ravel()

r2_tr = r2_score(y_tr, y_tr_pred)
r2_te = r2_score(y_te, y_te_pred)
rmse_te = np.sqrt(mean_squared_error(y_te, y_te_pred))
rpd = np.std(y_te) / rmse_te

print(f"Hasil PLSR C-Organik: R2_train={r2_tr:.3f}, R2_test={r2_te:.3f}, RMSE={rmse_te:.3f}%, RPD={rpd:.2f}")

# Simpan Gambar 3.2: Spektra SNV dengan fitur diagnostik C-Organik
plt.figure(figsize=(11, 6), dpi=200)
for i in range(min(50, len(X_sg1))):
    plt.plot(wavelengths, X_sg1[i], color="#2b5c8f", alpha=0.2, linewidth=0.8)

# Garis penanda serapan diagnostik C-Organik & Hidroksil
plt.axvline(x=550, color="#8c510a", linestyle="--", linewidth=1.5, label="450-650 nm: Kromofor Bahan Organik (SOM)")
plt.axvline(x=1400, color="#01665e", linestyle="--", linewidth=1.2, label="1400 nm: O-H Air Bebas / Kristal")
plt.axvline(x=1720, color="#d95f02", linestyle="-.", linewidth=1.5, label="1720 nm: Vibrasi Regangan C-H (Alifatik)")
plt.axvline(x=1900, color="#01665e", linestyle="--", linewidth=1.2, label="1900 nm: H-O-H Molekul Air")
plt.axvline(x=2300, color="#7570b3", linestyle="-.", linewidth=1.5, label="2300 nm: Kombinasi C-H + C=O Humus")

plt.title("Spektrum Vis-NIR Turunan Pertama (Savitzky-Golay + SNV)\nPita Serapan Diagnostik Karbon Organik Tanah (C-Organik)", fontsize=12, fontweight="bold")
plt.xlabel("Panjang Gelombang (nm)", fontsize=11)
plt.ylabel("Derivatif Pertama Absorbansi (SNV)", fontsize=11)
plt.legend(loc="upper right", fontsize=9, framealpha=0.9)
plt.grid(True, linestyle=":", alpha=0.6)
plt.tight_layout()
plt.savefig(f"{SCREENSHOT_DIR}/praktik_03_fig_2.png", bbox_inches="tight")
plt.close()

# Simpan Gambar 3.3: Scatterplot Evaluasi PLSR C-Organik
plt.figure(figsize=(7, 7), dpi=200)
plt.scatter(y_tr, y_tr_pred, color="#1f78b4", alpha=0.6, edgecolors="none", s=30, label=f"Kalibrasi (R² = {r2_tr:.2f})")
plt.scatter(y_te, y_te_pred, color="#e31a1c", alpha=0.8, edgecolors="k", linewidth=0.5, s=40, label=f"Validasi (R² = {r2_te:.2f}, RPD = {rpd:.2f})")
lims = [0, max(y_corg_p3.max(), y_te_pred.max()) + 0.5]
plt.plot(lims, lims, "k--", linewidth=1.2, label="Garis 1:1 (Ideal)")
plt.xlim(lims)
plt.ylim(lims)
plt.title(f"Evaluasi Model PLSR Estimasi C-Organik Tanah (%)\nRMSE Validasi: {rmse_te:.2f}% | RPD: {rpd:.2f}", fontsize=11, fontweight="bold")
plt.xlabel("C-Organik Aktual Laboratorium (%)", fontsize=11)
plt.ylabel("C-Organik Prediksi Spektroskopi Vis-NIR (%)", fontsize=11)
plt.legend(loc="upper left", fontsize=9)
plt.grid(True, linestyle=":", alpha=0.6)
plt.tight_layout()
plt.savefig(f"{SCREENSHOT_DIR}/praktik_03_fig_3.png", bbox_inches="tight")
plt.close()
print("-> Plot Praktik 3 untuk C-Organik berhasil disimpan!")

# =====================================================================
# 2. PRAKTIK 5: PEMODELAN SPASIAL MACHINE LEARNING C-ORGANIK
# =====================================================================
print("\n=== [2/2] MEMPROSES PRAKTIK 5: DSM C-ORGANIK LAPISAN 0-20 CM ===")
base_p5 = f"{BASE_DIR}/Output/Pelatihan/data/praktik-5"
kov_dir = f"{base_p5}/kovariat"

with open(f"{base_p5}/sampel_tanah_50titik.csv") as f:
    r = csv.DictReader(f)
    rows_p5 = list(r)

coords = [(float(row["x"]), float(row["y"])) for row in rows_p5]
y_corg_50 = np.array([float(row["C_Organik_1"]) for row in rows_p5])

cov_files = {
    'dem': f"{kov_dir}/dem_10m.tif",
    'slope': f"{kov_dir}/slope_10m.tif",
    'aspect': f"{kov_dir}/aspect_10m.tif",
    'hillshade': f"{kov_dir}/hillshade_10m.tif",
    'tpi': f"{kov_dir}/tpi_10m.tif",
    'sar_vv': (f"{kov_dir}/sentinel1_sar_10m.tif", 1),
    'sar_vh': (f"{kov_dir}/sentinel1_sar_10m.tif", 2),
    's2_b04': (f"{kov_dir}/sentinel2_l2a_10m.tif", 3),
    's2_b08': (f"{kov_dir}/sentinel2_l2a_10m.tif", 7),
    's2_b11': (f"{kov_dir}/sentinel2_l2a_10m.tif", 9),
    's2_b02': (f"{kov_dir}/sentinel2_l2a_10m.tif", 1),
    'pl': f"{kov_dir}/penggunaan_lahan_10m.tif"
}

ds_ref = gdal.Open(cov_files['dem'])
gt = ds_ref.GetGeoTransform()
proj_ref = ds_ref.GetProjection()
nx, ny = ds_ref.RasterXSize, ds_ref.RasterYSize

px_py = [(int((x - gt[0]) / gt[1]), int((y - gt[3]) / gt[5])) for x, y in coords]

X_list = []
for name, item in cov_files.items():
    if isinstance(item, tuple):
        ds = gdal.Open(item[0])
        arr = ds.GetRasterBand(item[1]).ReadAsArray()
    else:
        ds = gdal.Open(item)
        arr = ds.GetRasterBand(1).ReadAsArray()
    X_list.append([arr[py, px] for px, py in px_py])

X_arr = np.column_stack(X_list)
b04, b08, b11, b02 = X_arr[:, 7], X_arr[:, 8], X_arr[:, 9], X_arr[:, 10]
ndvi = np.where((b08 + b04) == 0, 0, (b08 - b04) / (b08 + b04))
bsi_num = (b11 + b04) - (b08 + b02)
bsi_den = (b11 + b04) + (b08 + b02)
bsi = np.where(bsi_den == 0, 0, bsi_num / bsi_den)

feature_names = ['dem', 'slope', 'aspect', 'hillshade', 'tpi', 'sar_vv', 'sar_vh', 'ndvi', 'bsi', 's2_b11', 'pl']
X_final = np.column_stack([
    X_arr[:, 0], X_arr[:, 1], X_arr[:, 2], X_arr[:, 3], X_arr[:, 4],
    X_arr[:, 5], X_arr[:, 6], ndvi, bsi, b11, X_arr[:, 11]
])

# Latih RF & QRF untuk C-Organik
rf = RandomForestRegressor(n_estimators=300, max_depth=5, random_state=42)
kf = KFold(n_splits=5, shuffle=True, random_state=42)
y_cv_pred = cross_val_predict(rf, X_final, y_corg_50, cv=kf)
rmse_cv = np.sqrt(mean_squared_error(y_corg_50, y_cv_pred))
mae_cv = mean_absolute_error(y_corg_50, y_cv_pred)

rf.fit(X_final, y_corg_50)

qrf = RandomForestQuantileRegressor(n_estimators=300, max_depth=5, random_state=42)
qrf.fit(X_final, y_corg_50)

# Prediksi seluruh grid Sub-DAS
dem_grid = ds_ref.GetRasterBand(1).ReadAsArray()
mask_das = (dem_grid != -9999) & (~np.isnan(dem_grid)) & (dem_grid > 0)

def get_band(path, b_idx=1):
    ds = gdal.Open(path)
    return ds.GetRasterBand(b_idx).ReadAsArray().astype(float)

slope_grid = get_band(cov_files['slope'])
aspect_grid = get_band(cov_files['aspect'])
hillshade_grid = get_band(cov_files['hillshade'])
tpi_grid = get_band(cov_files['tpi'])
sar_vv_grid = get_band(cov_files['sar_vv'][0], 1)
sar_vh_grid = get_band(cov_files['sar_vh'][0], 2)
s2_b02_g = get_band(cov_files['s2_b02'][0], 1)
s2_b04_g = get_band(cov_files['s2_b04'][0], 3)
s2_b08_g = get_band(cov_files['s2_b08'][0], 7)
s2_b11_g = get_band(cov_files['s2_b11'][0], 9)
pl_grid = get_band(cov_files['pl'])

ndvi_grid = np.where((s2_b08_g + s2_b04_g) == 0, 0, (s2_b08_g - s2_b04_g) / (s2_b08_g + s2_b04_g))
bsi_num_g = (s2_b11_g + s2_b04_g) - (s2_b08_g + s2_b02_g)
bsi_den_g = (s2_b11_g + s2_b04_g) + (s2_b08_g + s2_b02_g)
bsi_grid = np.where(bsi_den_g == 0, 0, bsi_num_g / bsi_den_g)

X_grid_valid = np.column_stack([
    dem_grid[mask_das], slope_grid[mask_das], aspect_grid[mask_das],
    hillshade_grid[mask_das], tpi_grid[mask_das], sar_vv_grid[mask_das],
    sar_vh_grid[mask_das], ndvi_grid[mask_das], bsi_grid[mask_das],
    s2_b11_g[mask_das], pl_grid[mask_das]
])

pred_corg_valid = rf.predict(X_grid_valid)
q05_valid = qrf.predict(X_grid_valid, quantiles=[0.05])
q95_valid = qrf.predict(X_grid_valid, quantiles=[0.95])
pi90_valid = q95_valid - q05_valid

pred_corg_map = np.full(dem_grid.shape, np.nan, dtype=np.float32)
pred_corg_map[mask_das] = pred_corg_valid

pi90_map = np.full(dem_grid.shape, np.nan, dtype=np.float32)
pi90_map[mask_das] = pi90_valid

def save_geotiff(out_path, arr, nodata=-9999):
    drv = gdal.GetDriverByName('GTiff')
    ds_out = drv.Create(out_path, nx, ny, 1, gdal.GDT_Float32)
    ds_out.SetGeoTransform(gt)
    ds_out.SetProjection(proj_ref)
    band = ds_out.GetRasterBand(1)
    band.SetNoDataValue(nodata)
    save_arr = np.where(np.isnan(arr), nodata, arr).astype(np.float32)
    band.WriteArray(save_arr)
    ds_out.FlushCache()
    print(f" -> Berhasil menyimpan GeoTIFF: {out_path}")

out_pred_corg = f"{base_p5}/prediksi_corganik_0_20cm.tif"
out_unc_corg = f"{base_p5}/ketidakpastian_pi90_corganik.tif"
save_geotiff(out_pred_corg, pred_corg_map)
save_geotiff(out_unc_corg, pi90_map)

# Simpan juga ke nama lama untuk backwards compatibility
save_geotiff(f"{base_p5}/prediksi_lempung_0_20cm.tif", pred_corg_map)
save_geotiff(f"{base_p5}/ketidakpastian_pi90_lempung.tif", pi90_map)

# Buat plot visualisasi panel terpadu C-Organik (Gambar 5.1)
fig, axes = plt.subplots(1, 3, figsize=(18, 7), dpi=200)

# 1. Peta Prediksi C-Organik
im0 = axes[0].imshow(pred_corg_map, cmap='YlGn', vmin=0.4, vmax=1.5)
axes[0].set_title('Prediksi Spasial C-Organik (%)\nSub-DAS Bompon (Lapisan 0-20 cm)', fontsize=12, fontweight='bold')
axes[0].axis('off')
cbar0 = plt.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)
cbar0.set_label('Kadar C-Organik (%)')

# 2. Peta Ketidakpastian PI90
im1 = axes[1].imshow(pi90_map, cmap='Reds', vmin=0.1, vmax=1.2)
axes[1].set_title('Ketidakpastian Prediksi Spasial (PI90)\nInterval Prediksi 90% (Quantile Forest)', fontsize=12, fontweight='bold')
axes[1].axis('off')
cbar1 = plt.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)
cbar1.set_label('Lebar PI90 C-Organik (%)')

# 3. Feature importance
importances = rf.feature_importances_
sorted_idx = np.argsort(importances)
axes[2].barh(range(len(sorted_idx)), importances[sorted_idx]*100, color='#238b45')
axes[2].set_yticks(range(len(sorted_idx)))
axes[2].set_yticklabels([feature_names[i] for i in sorted_idx], fontsize=10)
axes[2].set_xlabel('Tingkat Kepentingan Relatif (%)', fontsize=11)
axes[2].set_title('Peringkat Kepentingan Kovariat SCORPAN\nPrediktor Karbon Organik Tanah (SOC)', fontsize=12, fontweight='bold')
axes[2].grid(axis='x', linestyle='--', alpha=0.6)

plt.tight_layout()
out_fig5 = f"{SCREENSHOT_DIR}/praktik_05_fig_1.png"
plt.savefig(out_fig5, bbox_inches='tight')
plt.close()
print(f"-> Plot panel C-Organik disimpan: {out_fig5}")
print("=== SEMUA PEMODELAN C-ORGANIK SELESAI 100%! ===")
