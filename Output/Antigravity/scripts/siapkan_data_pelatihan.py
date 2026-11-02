#!/usr/bin/env python3
"""
siapkan_data_pelatihan.py
Menyiapkan, menyelaraskan, dan mendistribusikan data ke masing-masing folder praktik (1 s.d. 5)
di dalam direktori Output/Pelatihan/data/.
"""

import os
import shutil
import csv
from osgeo import gdal, ogr

gdal.UseExceptions()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'Pelatihan', 'data')
SOURCE_BOMPON = os.path.join(BASE_DIR, '..', 'Source', 'Data Bompon')
SOURCE_PSS = os.path.join(BASE_DIR, '..', 'Source', 'Proximal Sensing')

BATAS_10M = (396060, 9162990, 397980, 9166610)


def export_gpkg_layer(src_gpkg, layer_name, dst_gpkg):
    """Mengekspor satu layer dari GeoPackage master ke GeoPackage baru."""
    src_ds = ogr.Open(src_gpkg)
    layer = src_ds.GetLayerByName(layer_name)
    if layer is None:
        print(f"Layer {layer_name} tidak ditemukan di {src_gpkg}")
        return
    
    drv = ogr.GetDriverByName("GPKG")
    if os.path.exists(dst_gpkg):
        os.remove(dst_gpkg)
    dst_ds = drv.CreateDataSource(dst_gpkg)
    dst_ds.CopyLayer(layer, layer_name, ["OVERWRITE=YES"])
    dst_ds = None
    src_ds = None


def setup_praktik_1():
    """Praktik 1: Multi-source Data Fusion"""
    p1_dir = os.path.join(DATA_DIR, 'praktik-1')
    os.makedirs(p1_dir, exist_ok=True)
    print("\n[PRAKTIK 1] Menyiapkan data Multi-source Data Fusion...")
    
    # 1. Optik Sentinel-2 L2A (10 m)
    s2_src = os.path.join(SOURCE_BOMPON, 'terbuka', 'sentinel2_l2a_20250721_10m.tif')
    shutil.copy2(s2_src, os.path.join(p1_dir, 'sentinel2_l2a_20250721_10m.tif'))
    
    # 2. Radar SAR Sentinel-1 RTC (10 m)
    s1_src = os.path.join(SOURCE_BOMPON, 'terbuka', 'sentinel1_rtc_20240830_10m.tif')
    shutil.copy2(s1_src, os.path.join(p1_dir, 'sentinel1_rtc_20240830_10m.tif'))
    
    # 3. Copernicus DEM GLO-30 (30 m)
    dem_src = os.path.join(SOURCE_BOMPON, 'terbuka', 'copdem_glo30_30m.tif')
    shutil.copy2(dem_src, os.path.join(p1_dir, 'copdem_glo30_30m.tif'))
    
    # 4. Batas Sub-DAS (Vektor)
    bompon_gpkg = os.path.join(SOURCE_BOMPON, 'bompon.gpkg')
    export_gpkg_layer(bompon_gpkg, 'batas_subdas', os.path.join(p1_dir, 'batas_subdas.gpkg'))
    print("  -> Praktik 1 data siap.")


def setup_praktik_2():
    """Praktik 2: Delineasi Soil Mapping Units (SMU)"""
    p2_dir = os.path.join(DATA_DIR, 'praktik-2')
    os.makedirs(p2_dir, exist_ok=True)
    print("\n[PRAKTIK 2] Menyiapkan data Delineasi SMU...")
    
    # 1. Resample Copernicus DEM ke grid 10 m terselaras
    dem_30m = os.path.join(SOURCE_BOMPON, 'terbuka', 'copdem_glo30_30m.tif')
    dem_10m = os.path.join(p2_dir, 'copdem_10m.tif')
    gdal.Warp(dem_10m, dem_30m, format='GTiff', dstSRS='EPSG:32749',
              outputBounds=BATAS_10M, xRes=10, yRes=10, resampleAlg='bilinear',
              outputType=gdal.GDT_Float32, creationOptions=['COMPRESS=DEFLATE'])
    
    # 2. Sentinel-2 L2A untuk True Color & CIR (8-4-3)
    s2_src = os.path.join(SOURCE_BOMPON, 'terbuka', 'sentinel2_l2a_20250721_10m.tif')
    shutil.copy2(s2_src, os.path.join(p2_dir, 'sentinel2_l2a_20250721_10m.tif'))
    
    # 3. Layer vektor batas & rujukan
    bompon_gpkg = os.path.join(SOURCE_BOMPON, 'bompon.gpkg')
    export_gpkg_layer(bompon_gpkg, 'batas_subdas', os.path.join(p2_dir, 'batas_subdas.gpkg'))
    export_gpkg_layer(bompon_gpkg, 'bentuklahan', os.path.join(p2_dir, 'bentuklahan_rujukan.gpkg'))
    export_gpkg_layer(bompon_gpkg, 'kelas_lereng', os.path.join(p2_dir, 'kelas_lereng_rujukan.gpkg'))
    print("  -> Praktik 2 data siap.")


def setup_praktik_3():
    """Praktik 3: Demonstrasi Proximal Soil Sensing (PSS)"""
    p3_dir = os.path.join(DATA_DIR, 'praktik-3')
    os.makedirs(p3_dir, exist_ok=True)
    print("\n[PRAKTIK 3] Menyiapkan data Demonstrasi PSS...")
    
    # 1. Salin berkas Excel master
    excel_src = os.path.join(SOURCE_PSS, 'Dataset_ML_Tanah_Gabungan_new.xlsx')
    shutil.copy2(excel_src, os.path.join(p3_dir, 'Dataset_ML_Tanah_Gabungan_new.xlsx'))
    
    # 2. Ekspor ke CSV agar ringan dan cepat dibaca oleh notebook Python
    import openpyxl
    wb = openpyxl.load_workbook(excel_src, read_only=True)
    sheet = wb['Sheet1']
    csv_out = os.path.join(p3_dir, 'spektra_visnir_857sampel.csv')
    with open(csv_out, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for row in sheet.iter_rows(values_only=True):
            writer.writerow(row)
    wb.close()
    print(f"  -> Konversi CSV berhasil: {csv_out} ({os.path.getsize(csv_out):,} bytes)")
    print("  -> Praktik 3 data siap.")


def setup_praktik_4():
    """Praktik 4: Bare Soil Detection & Extraction"""
    p4_dir = os.path.join(DATA_DIR, 'praktik-4')
    os.makedirs(p4_dir, exist_ok=True)
    print("\n[PRAKTIK 4] Menyiapkan data Bare Soil Detection...")
    
    # 1. Sentinel-2 Juli 2025 (Kondisi Kanopi Rapat)
    s2_2025 = os.path.join(SOURCE_BOMPON, 'terbuka', 'sentinel2_l2a_20250721_10m.tif')
    shutil.copy2(s2_2025, os.path.join(p4_dir, 'sentinel2_l2a_20250721_10m.tif'))
    
    # 2. Sentinel-2 Agustus 2024 (Kondisi Puncak Kemarau / Bera)
    s2_2024 = os.path.join(SOURCE_BOMPON, 'terbuka', 'sentinel2_l2a_20240813_10m.tif')
    shutil.copy2(s2_2024, os.path.join(p4_dir, 'sentinel2_l2a_20240813_10m.tif'))
    
    # 3. Scene Classification Layer (SCL)
    scl_src = os.path.join(SOURCE_BOMPON, 'terbuka', 'sentinel2_l2a_20250721_scl_10m.tif')
    shutil.copy2(scl_src, os.path.join(p4_dir, 'sentinel2_l2a_20250721_scl_10m.tif'))
    
    # 4. Batas & Tutupan Lahan
    bompon_gpkg = os.path.join(SOURCE_BOMPON, 'bompon.gpkg')
    export_gpkg_layer(bompon_gpkg, 'batas_subdas', os.path.join(p4_dir, 'batas_subdas.gpkg'))
    export_gpkg_layer(bompon_gpkg, 'penggunaan_lahan', os.path.join(p4_dir, 'penggunaan_lahan.gpkg'))
    print("  -> Praktik 4 data siap.")


def setup_praktik_5():
    """Praktik 5: Machine Learning untuk Digital Soil Mapping (DSM)"""
    p5_dir = os.path.join(DATA_DIR, 'praktik-5')
    os.makedirs(p5_dir, exist_ok=True)
    kovariat_dir = os.path.join(p5_dir, 'kovariat')
    os.makedirs(kovariat_dir, exist_ok=True)
    print("\n[PRAKTIK 5] Menyiapkan data Machine Learning DSM...")
    
    # 1. Tabel Hasil Uji Lab 50 Titik Sampel
    sampel_src = os.path.join(SOURCE_BOMPON, 'sampel.csv')
    shutil.copy2(sampel_src, os.path.join(p5_dir, 'sampel_tanah_50titik.csv'))
    
    # 2. Vektor Titik Sampel Lapangan
    bompon_gpkg = os.path.join(SOURCE_BOMPON, 'bompon.gpkg')
    export_gpkg_layer(bompon_gpkg, 'titik_sampel_lapangan', os.path.join(p5_dir, 'titik_sampel_lapangan.gpkg'))
    export_gpkg_layer(bompon_gpkg, 'batas_subdas', os.path.join(p5_dir, 'batas_subdas.gpkg'))
    
    # 3. Tumpukan Kovariat SCORPAN Grid 10 m
    # 3a. DEM 10 m
    dem_30m = os.path.join(SOURCE_BOMPON, 'terbuka', 'copdem_glo30_30m.tif')
    dem_10m = os.path.join(kovariat_dir, 'dem_10m.tif')
    gdal.Warp(dem_10m, dem_30m, format='GTiff', dstSRS='EPSG:32749',
              outputBounds=BATAS_10M, xRes=10, yRes=10, resampleAlg='bilinear',
              outputType=gdal.GDT_Float32, creationOptions=['COMPRESS=DEFLATE'])
    
    # 3b. Slope & Aspect & Hillshade
    slope_file = os.path.join(kovariat_dir, 'slope_10m.tif')
    gdal.DEMProcessing(slope_file, dem_10m, 'slope', computeEdges=True)
    
    aspect_file = os.path.join(kovariat_dir, 'aspect_10m.tif')
    gdal.DEMProcessing(aspect_file, dem_10m, 'aspect', computeEdges=True)
    
    hillshade_file = os.path.join(kovariat_dir, 'hillshade_10m.tif')
    gdal.DEMProcessing(hillshade_file, dem_10m, 'hillshade', computeEdges=True)
    
    tpi_file = os.path.join(kovariat_dir, 'tpi_10m.tif')
    gdal.DEMProcessing(tpi_file, dem_10m, 'TPI', computeEdges=True)
    
    # 3c. Sentinel-2 L2A & Sentinel-1 SAR
    s2_src = os.path.join(SOURCE_BOMPON, 'terbuka', 'sentinel2_l2a_20250721_10m.tif')
    shutil.copy2(s2_src, os.path.join(kovariat_dir, 'sentinel2_l2a_10m.tif'))
    
    s1_src = os.path.join(SOURCE_BOMPON, 'terbuka', 'sentinel1_rtc_20240830_10m.tif')
    shutil.copy2(s1_src, os.path.join(kovariat_dir, 'sentinel1_sar_10m.tif'))
    
    # 3d. Raster Penggunaan Lahan (faktor O)
    pl_raster = os.path.join(kovariat_dir, 'penggunaan_lahan_10m.tif')
    sql_pl = (
        "SELECT CASE penggunaan_lahan "
        "WHEN 'Agroforestri' THEN 1 "
        "WHEN 'Permukiman' THEN 2 "
        "WHEN 'Sawah' THEN 3 "
        "WHEN 'Tegalan' THEN 4 "
        "ELSE 0 END AS kelas_id, geom FROM penggunaan_lahan"
    )
    gdal.Rasterize(pl_raster, bompon_gpkg, SQLStatement=sql_pl,
                   attribute='kelas_id', outputBounds=BATAS_10M, xRes=10, yRes=10,
                   outputSRS='EPSG:32749', outputType=gdal.GDT_Byte,
                   initValues=[0], creationOptions=['COMPRESS=DEFLATE'])
    
    print("  -> Seluruh lapisan kovariat SCORPAN siap di folder kovariat/.")
    print("  -> Praktik 5 data siap.")


def write_readme_data():
    """Menulis README.md untuk direktori data pelatihan."""
    readme_path = os.path.join(DATA_DIR, 'README.md')
    content = """# KATALOG DATA PRAKTIK PELATIHAN
## Remote Sensing, Proximal Soil Sensing, dan Digital Soil Mapping
**Pusat Studi Pengelolaan Sumber Daya Lahan (PS2DL) UGM & PT SMART Tbk**

Direktori ini memuat paket data geospasial dan spektroskopi yang telah diselaraskan ke sistem koordinat seragam **`EPSG:32749` (WGS 84 / UTM Zone 49S)** dan batas grid 10 m Sub-DAS Bompon (396060–397980 E, 9162990–9166610 N).

---

### STRUKTUR DIREKTORI DATA PER PRAKTIK

```
Output/Pelatihan/data/
├── praktik-1/          # Multi-source Data Fusion
│   ├── sentinel2_l2a_20250721_10m.tif    (Optik L2A 10 kanal, 10 m)
│   ├── sentinel1_rtc_20240830_10m.tif    (Radar SAR RTC VV & VH, 10 m)
│   ├── copdem_glo30_30m.tif              (Copernicus DEM asli, 30 m)
│   └── batas_subdas.gpkg                 (Poligon batas Sub-DAS Bompon)
│
├── praktik-2/          # Delineasi Soil Mapping Units (SMU)
│   ├── copdem_10m.tif                    (DEM terselaras 10 m)
│   ├── sentinel2_l2a_20250721_10m.tif    (Optik komposit RGB & CIR)
│   ├── batas_subdas.gpkg                 (Batas wilayah studi)
│   ├── bentuklahan_rujukan.gpkg          (Peta rujukan fisiografi pakar)
│   └── kelas_lereng_rujukan.gpkg         (Peta rujukan kelas lereng)
│
├── praktik-3/          # Demonstrasi Proximal Soil Sensing (PSS)
│   ├── Dataset_ML_Tanah_Gabungan_new.xlsx (857 spektra Vis-NIR 350-2500 nm)
│   └── spektra_visnir_857sampel.csv      (Versi CSV bersih untuk notebook Python)
│
├── praktik-4/          # Bare Soil Detection & Extraction
│   ├── sentinel2_l2a_20250721_10m.tif    (Kondisi kanopi rapat)
│   ├── sentinel2_l2a_20240813_10m.tif    (Puncak kemarau/sawah-tegalan bera)
│   ├── sentinel2_l2a_20250721_scl_10m.tif(Scene Classification Layer)
│   ├── batas_subdas.gpkg                 (Batas wilayah studi)
│   └── penggunaan_lahan.gpkg             (Vektor tutupan lahan)
│
└── praktik-5/          # Machine Learning untuk Digital Soil Mapping (DSM)
    ├── sampel_tanah_50titik.csv          (Data lab 50 titik: Clay %, Sand %, pH, KPK, C-Org)
    ├── titik_sampel_lapangan.gpkg        (Vektor spasial 50 titik GPS lapangan)
    ├── batas_subdas.gpkg                 (Batas wilayah studi)
    └── kovariat/                         (Tumpukan raster kovariat SCORPAN 10 m)
        ├── dem_10m.tif                   (Elevasi)
        ├── slope_10m.tif                 (Kelerengan derajat)
        ├── aspect_10m.tif                (Orientasi lereng)
        ├── hillshade_10m.tif             (Bayangan relief bukit)
        ├── tpi_10m.tif                   (Topographic Position Index)
        ├── sentinel2_l2a_10m.tif         (Optik kanal B02-B12)
        ├── sentinel1_sar_10m.tif         (SAR VV & VH)
        └── penggunaan_lahan_10m.tif      (Raster tutupan lahan)
```
"""
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  -> Katalog data tersimpan di: {readme_path}")


def main():
    print("==================================================================")
    print("PENYIAPAN DAN PENYELARASAN DATA LENGKAP PRAKTIK 1 S.D. 5")
    print("==================================================================")
    setup_praktik_1()
    setup_praktik_2()
    setup_praktik_3()
    setup_praktik_4()
    setup_praktik_5()
    write_readme_data()
    print("\n==================================================================")
    print("SELURUH DATA PRAKTIK 1 S.D. 5 BERHASIL DISIAPKAN 100% LENGKAP!")
    print("==================================================================")


if __name__ == '__main__':
    main()
