# KATALOG DATA PRAKTIK PELATIHAN
## Remote Sensing, Proximal Soil Sensing, dan Digital Soil Mapping
**Pusat Studi Pengelolaan Sumber Daya Lahan (PS2DL) UGM & PT SMART Tbk**

Direktori ini memuat paket data geospasial dan spektroskopi yang telah diselaraskan ke sistem koordinat seragam **`EPSG:32749` (WGS 84 / UTM Zone 49S)** dan batas grid 10 m Sub-DAS Bompon (396060–397980 E, 9162990–9166610 N).

---

### STRUKTUR DIREKTORI DATA PER PRAKTIK

```
Output/Pelatihan/data/
├── praktik-1/          # Multi-source Data Fusion
│   ├── Praktik_01_Multi_Source_Data_Fusion.qgz (Proyek QGIS siap pakai)
│   ├── sentinel2_l2a_20250721_10m.tif    (Optik L2A 10 kanal, 10 m)
│   ├── sentinel1_rtc_20240830_10m.tif    (Radar SAR RTC VV & VH, 10 m)
│   ├── copdem_glo30_30m.tif              (Copernicus DEM asli, 30 m)
│   └── batas_subdas.gpkg                 (Poligon batas Sub-DAS Bompon)
│
├── praktik-2/          # Delineasi Soil Mapping Units (SMU)
│   ├── Praktik_02_Delineasi_SMU.qgz      (Proyek QGIS siap pakai)
│   ├── copdem_10m.tif                    (DEM terselaras 10 m)
│   ├── slope_10m.tif                     (Kelerengan medan 10 m)
│   ├── hillshade_10m.tif                 (Hillshade topografi 10 m)
│   ├── sentinel2_l2a_20250721_10m.tif    (Optik komposit RGB & CIR)
│   ├── batas_subdas.gpkg                 (Batas wilayah studi)
│   ├── bentuklahan_rujukan.gpkg          (Peta rujukan fisiografi pakar)
│   └── kelas_lereng_rujukan.gpkg         (Peta rujukan kelas lereng)
│
├── praktik-3/          # Demonstrasi Proximal Soil Sensing (PSS)
│   ├── Praktik_03_Demonstrasi_PSS.qgz    (Proyek QGIS sebaran titik sampel & optik)
│   ├── titik_sampel_lapangan.gpkg        (Vektor spasial 50 titik sampel PSS)
│   ├── batas_subdas.gpkg                 (Poligon batas Sub-DAS Bompon)
│   ├── sentinel2_l2a_20250721_10m.tif    (Citra Sentinel-2 True Color)
│   ├── Dataset_ML_Tanah_Gabungan_new.xlsx (857 spektra Vis-NIR 350-2500 nm)
│   └── spektra_visnir_857sampel.csv      (Versi CSV bersih untuk notebook Python)
│
├── praktik-4/          # Bare Soil Detection & Extraction
│   ├── Praktik_04_Bare_Soil_Detection.qgz(Proyek QGIS siap pakai)
│   ├── sentinel2_l2a_20250721_10m.tif    (Kondisi kanopi rapat)
│   ├── sentinel2_l2a_20240813_10m.tif    (Puncak kemarau/sawah-tegalan bera)
│   ├── bsi_20240813.tif / bsi_20250721.tif (Bare Soil Index)
│   ├── masker_tanah_terbuka_20240813.tif (Masker biner tanah terbuka)
│   ├── barest_earth_bsi_composite.tif    (Komposit tanah terbuka multi-musim)
│   ├── batas_subdas.gpkg                 (Batas wilayah studi)
│   └── penggunaan_lahan.gpkg             (Vektor tutupan lahan)
│
└── praktik-5/          # Machine Learning untuk Digital Soil Mapping (DSM)
    ├── Praktik_05_Machine_Learning_DSM_C_Organik.qgz (Proyek QGIS pemodelan C-Organik)
    ├── sampel_tanah_50titik.csv          (Data lab 50 titik: C-Organik 0-20 cm, Clay, dll.)
    ├── titik_sampel_lapangan.gpkg        (Vektor spasial 50 titik GPS lapangan)
    ├── batas_subdas.gpkg                 (Batas wilayah studi)
    ├── prediksi_corganik_0_20cm.tif      (GeoTIFF kontinu estimasi C-Organik)
    ├── ketidakpastian_pi90_corganik.tif  (GeoTIFF lebar interval prediksi 90% PI90)
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
