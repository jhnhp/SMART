# Modul Pelatihan Pemanfaatan Remote Sensing dan Digital Soil Mapping

Repositori ini memuat materi dan dokumentasi lengkap modul pelatihan **Pemanfaatan Penginderaan Jauh (Remote Sensing) dan Pemetaan Tanah Digital (Digital Soil Mapping / DSM)** dengan studi kasus serial Sub-DAS Bompon, Kabupaten Magelang.

## Struktur Modul Pelatihan

1. **Modul 1: Dasar-dasar Remote Sensing untuk Pemetaan Sumberdaya Lahan**
   - Prinsip fisis radiasi elektromagnetik, jendela atmosfer, resolusi sensor, dan interaksi spektral vegetasi, tanah, serta air.
2. **Modul 2: Karakteristik Sensor Optis dan SAR untuk Pemetaan Tanah**
   - Karakteristik spektral sensor optis (Sentinel-2, Landsat-8/9, PlanetScope) dan gelombang mikro SAR (Sentinel-1).
3. **Modul 3: Pra-Pengolahan Citra Penginderaan Jauh**
   - Koreksi radiometrik, kalibrasi reflektansi permukaan (BOA/L2A), kalibrasi radiometrik & koreksi medan SAR, serta cloud masking.
4. **Modul 4: Ekstraksi Fitur Spektral dan Transformasi Indeks Lingkungan**
   - Indeks vegetasi (NDVI, EVI, SAVI), indeks kebasahan & air (NDWI, NDMI), indeks tanah & mineral (BSI, BI, CI), dan analisis multitemporal.
5. **Modul 5: Konsep Dasar dan Kerangka Kerja Digital Soil Mapping (DSM)**
   - Paradigma Dokuchaev, model kuantitatif SCORPAN, dan desain sampling spasial tanah (cLHS).
6. **Modul 6: Penyiapan Kovariat Lingkungan (SCORPAN)**
   - Derivasi atribut topografi primer & sekunder dari DEM (SRTM, NASADEM, DEMNAS), harmonisasi spasial, dan integrasi multi-sensor.
7. **Modul 7: Pemodelan Spasial Tanah Berbasis Machine Learning**
   - Algoritma Random Forest, XGBoost, Support Vector Machines (SVM), dan evaluasi fitur prediktor.
8. **Modul 8: Validasi Model, Evaluasi Ketidakpastian, dan Visualisasi Peta Digital**
   - Validasi silang spasial (Spatial Cross-Validation), metrik evaluasi (RMSE, MAE, R², Lin's CCC), pemetaan ketidakpastian (PI90), dan penyajian kartografis standar.

## Struktur Direktori

```
.
├── ANTIGRAVITY.md        # Panduan editorial dan standar kualitas proyek
├── README.md             # Dokumentasi umum repositori
├── Source/               # Dokumen rujukan, silabus, dan data spasial mentah
│   ├── Data Bompon/      # Data spasial & atribut Sub-DAS Bompon
│   └── ...               # Silabus dan dokumen acuan
└── Output/               # Seluruh berkas keluaran modul pelatihan
    ├── Modul 1.md ~ Modul 8.md
    ├── Modul Pelatihan Pemanfaatan RS dan DSM.docx
    ├── assets/           # 42 visual resolusi tinggi (M1-G01 s.d. M8-G06)
    └── scripts/          # Skrip Python pembuat visual dan pengolah dokumen
```

## Dokumen Final

Dokumen utuh yang telah digabungkan dan diformat lengkap mencakup sampul depan/belakang *full-bleed*, persamaan matematis native Word (OMML), tabel terstandardisasi, dan master daftar pustaka tersedia di:
- `Output/Modul Pelatihan Pemanfaatan RS dan DSM.docx`
