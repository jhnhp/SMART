# Data Spasial Sub-DAS Bompon

Data studi kasus serial modul pelatihan *Remote Sensing* dan *Digital Soil Mapping*. Folder ini memisahkan **data mentah** (apa adanya, untuk penelusuran asal-usul) dari **data bersih** (siap dipakai di modul dan praktik).

```
Data Bompon/
├── README.md                       ← dokumen ini
├── bompon.gpkg                     ← data bersih: 14 layer, EPSG:32749 (WGS 84 / UTM 49S)
├── tabel/
│   ├── titik_sampel_rencana.csv    ← 50 titik rencana + atribut satuan lahan
│   ├── titik_sampel_lapangan.csv   ← posisi GPS aktual pengambilan sampel (Feb 2025)
│   └── titik_survei.csv            ← titik survei pendahuluan (Feb 2025)
├── skrip/
│   └── rapikan_data_bompon.py      ← membuat ulang bompon.gpkg dan tabel/ dari mentah/
└── mentah/                         ← data asli (struktur folder asli dipertahankan)
```

Membuat ulang data bersih: `python3 "Source/Data Bompon/skrip/rapikan_data_bompon.py"` (memerlukan GDAL/OGR Python dan `7z`).

## Gambaran wilayah

Hasil perhitungan dari `batas_subdas`: luas **294,71 ha**, kira-kira 110,0596–110,0734° BT dan 7,5404–7,5694° LS. Sambodo (2021) menyebut Sub-DAS Bompon berada di bagian selatan Kabupaten Magelang pada lereng selatan Gunung Sumbing, dengan luas ±294,69 ha, dan merupakan bagian dari DAS Bogowonto.

**Wilayah administratif (perlu konfirmasi).** Tumpang susun `batas_subdas` dengan batas desa RBI 1:25.000 (`rbi_desa_magelang`) menghasilkan:
- Desa Wonogiri, Kecamatan Kajoran: 166,32 ha;
- Desa Margoyoso, Kecamatan Salaman: 93,41 ha;
- Desa Kuwaderan, Kecamatan Kajoran: 34,98 ha (data proyek menulis "Kwaderan").

Sambodo (2021) menyebut "Kalisari village" di Kecamatan Salaman. Data proyek mencatat Kalisari sebagai **dusun**, sehingga kemungkinan besar Kalisari adalah dusun di Desa Margoyoso.

## Isi `bompon.gpkg`

| Layer | Geometri | Fitur | Atribut utama | Sumber mentah | Catatan |
|---|---|---|---|---|---|
| `batas_subdas` | poligon | 1 | `nama`, `luas_ha` | `SHP Bompon/Batas_Bompon.shp` | Atribut lama `R`, `R_class` tidak dibawa karena maknanya tidak terdokumentasi |
| `batas_dusun` | poligon | 9 | `dusun`, `luas_ha` | `SHP Bompon/Batas_Dusun_Bompon.shp` | Kolom `luas` asli bernilai 295 untuk semua dusun (salah); luas dihitung ulang |
| `bentuklahan` | poligon | 69 | `bentuklahan`, `luas_ha` | `Survei/ArcGIS/Survei.mpk` → `shp_ta/Landform.shp` | 6 satuan: Interfluve, Lereng Atas/Tengah/Bawah Perbukitan, Lereng Kaki Koluvial, Dataran Koluvial |
| `kelas_lereng` | multipoligon | 5 | `kelas_lereng`, `luas_ha` | `Survei.mpk` → `data_ta.gdb/slope_lidar25` | 164.116 poligon hasil konversi raster digabung per kelas; tetap sangat terfragmentasi |
| `penggunaan_lahan` | poligon | 75 | `penggunaan_lahan`, `luas_ha` | `Survei.mpk` → `shp_ta/Digit_PL.shp` | 4 kelas: Agroforestri, Tegalan, Sawah, Permukiman |
| `longsor` | poligon | 21 | `kelas`, `luas_ha` | `Longsor/Shp Longsor Bompon.zip` | Longsor dorman, aktif dalam, aktif dangkal |
| `sungai` | garis | 7 | `jenis`, `panjang_m` | `SHP Bompon/Sungai_2020.shp` | Sungai perenial dan intermiten |
| `jalan` | garis | 34 | `kelas`, `panjang_m` | `SHP Bompon/Jalan_2020.shp` | Roda 4, roda 2, jalan kaki |
| `rute_survei` | garis | 26 | `sumber_berkas` | `Survei.mpk` → `data_ta.gdb/Rute` | Identik dengan `Survei/Data Survei/Shp_rute/rute_atas_tengah.shp` |
| `fasilitas_pengamatan` | titik | 9 | `jenis` | `St_Hujan`, `SPAS`, `Plot Erosi`, `embung_point` | Stasiun hujan (3), SPAS (3), plot erosi (2), embung (1) |
| `rbi_desa_magelang` | poligon | 253 | `desa`, `kecamatan`, `luas_ha` | `Survei.mpk` → `rbi_magelang/ADMINISTRASIDESA_AR_25K.shp` | Batas desa RBI 1:25.000 (BIG); hanya mencakup 14 kecamatan di Kabupaten Magelang. Dipakai untuk peta lokasi |
| `titik_sampel_rencana` | titik | 50 | `kode`, `tim`, `satuan_lahan`, `penggunaan_lahan`, `bentuklahan`, `kelas_lereng` | `Survei.mpk` → `data_ta.gdb/baru_sampel` | Rancangan sampel berstrata per satuan lahan (penggunaan lahan × bentuklahan × lereng) |
| `titik_sampel_lapangan` | titik | 50 | `kode`, `waktu`, `jarak_ke_rencana_m`, `status` | CSV/KMZ di `Sampling/` | Posisi GPS aktual 22–25 Feb 2025; lihat bagian duplikat di bawah |
| `titik_survei` | titik | 154 | `nama`, `waktu`, `kegiatan` | CSV/KMZ di `Survei/Data Survei/` | Survei pendahuluan Februari 2025; duplikat persis lintas format dibuang |

## Keputusan pembersihan

**Versi yang dipilih ketika ada lebih dari satu.**
- Penggunaan lahan memakai `Digit_PL` karena hanya versi ini yang menutup seluruh Sub-DAS (294,71 ha) dengan kelas yang konsisten dengan rancangan sampel. Versi lain tidak dipakai. `PL_Bompon` (Hutan/Kebun/Permukiman/Sawah Irigasi) memakai sistem kelas berbeda. `PL_Bompon2020` hanya berisi tegalan, dan `PL_Kebun2020` hanya satu poligon seluas seluruh wilayah.
- Kelas lereng memakai `slope_lidar25` (0–8, 8–15, 15–25, 25–45, >45 %) karena kelas ini dipakai untuk menyusun satuan lahan dan peta survei (`Survei/Peta Survei/Peta_SurveI_Slope.pdf`). `SHP Bompon/Kemiringan_Lereng.shp` memakai klasifikasi lain (7–15, 15–30, 30–70, 70–140, >140) tanpa satuan tertulis, dan Sambodo (2021) memakai klasifikasi ketiga. Fatmawati (2026) mengonfirmasi bahwa kelas ini diturunkan dari DTM LiDAR, tetapi DTM-nya tidak ada di folder ini.
- Sungai memakai `Sungai_2020`. `Sungai_Intermitten` + `Sungai_Perennial` adalah digitasi lain yang sedikit berbeda posisinya.
- Jalan memakai `Jalan_2020`. `Jalan_Bompon` memiliki 7 segmen tanpa kelas dan melampaui batas Sub-DAS.

**Titik sampel.** `titik_sampel_rencana` adalah lokasi rencana. `titik_sampel_lapangan` adalah posisi GPS yang benar-benar dicatat; jaraknya ke rencana berkisar 1–490 m.
- Rekaman ganda berjarak < 25 m dianggap satu kunjungan yang tercatat dua kali, lalu digabung (C34, C35, C36 tercatat di `Peta 1 Tim C` dan `Peta 2 tim C`).
- **Perlu konfirmasi:** B30 tercatat dua kali di lokasi berbeda (6 m dan 92 m dari rencana). C38 tercatat sebagai "C38" dan "C38 ril" yang terpaut ±490 m.
- B32 dan C47 tidak memiliki rekaman GPS.
- Salah ketik "Datang" pada A12 dikoreksi menjadi "Datar".
- Elevasi GPS bernilai 0 diperlakukan sebagai kosong. Elevasi GPS genggam tidak cocok untuk analisis topografi.

**Berkas yang dihapus dari `mentah/`.** Hanya berkas yang terbukti tidak berisi data:
- 19 berkas kunci ArcGIS `*.sr.lock` berukuran 0 byte;
- folder `SHP Bompon/Bompon/`, yang isinya identik byte-per-byte dengan `SHP Bompon/Bompon.zip`.

Folder `Data Bompon/Data Bompon/` (bersarang ganda) diganti nama menjadi `mentah/`.

## Data mentah yang tidak dimasukkan ke data bersih

| Berkas | Alasan |
|---|---|
| `SHP Bompon/das Bompon1.tif` | Ekspor tata letak peta foto udara (judul, legenda, dan garis ikut terbakar ke piksel), 0,8 m, tanpa `.prj` (koordinat UTM 49S dari `.tfw`). Tidak layak dipakai sebagai ortofoto analisis. |
| `SHP Bompon/FU Bompon.pdf`, `Survei/Peta Survei/*.pdf` | Peta jadi (PDF), bukan data. |
| `Longsor/Longsor Georeferencing.tif` | Gambar dari sebuah publikasi yang di-*georeference*; sumber publikasinya belum diketahui. |
| `SHP Bompon/Batas_Desa.shp` | Hanya 2 poligon dengan atribut luas yang tertukar; tidak cocok dengan daftar dusun. |
| `SHP Bompon/erosi.shp`, `Embung.shp`, `Jalur.shp`, `Jalur_Terbang.shp`, `grid_*.shp` | Layer kerja (rencana jalur terbang, grid lembar peta, poligon kecil). `grid_erosi.shp` kosong (0 fitur). |
| `SHP Bompon/Tansbulent.shp` | Satu titik tanpa keterangan. |
| `SHP Bompon/Kontur Bompon.xlsx` | Tabel atribut kontur tanpa geometri. |
| `SHP Bompon/Kaliwungu.rar`, `PL_Bompon2020.rar` | Format RAR5 yang tidak dapat dibuka dengan alat yang tersedia. `Kaliwungu.rar` berisi `DASSebelahBompon`; `PL_Bompon2020.rar` berisi versi `PL_Bompon2020` yang lebih besar (1,1 MB) daripada versi di folder. |
| `SHP Bompon/BL.mxd`, `Survei.mpk` (selain layer di atas) | Proyek ArcMap. `Survei.mpk` juga memuat layer RBI 1:25.000 Magelang (batas desa, batas administrasi, sungai) serta tabel `SPL.csv` dan `Sampel.csv`. |
| Foto di dalam berkas KMZ | Ratusan foto lapangan (JPG) tersimpan di dalam KMZ dan tidak diekstrak. |

## Data yang belum tersedia

1. **Tabel hasil analisis laboratorium per titik sampel.** Hasilnya telah dilaporkan secara ringkas oleh Fatmawati (2026), tetapi tabel per titik tidak ada di folder ini. Tanpa tabel tersebut, praktik estimasi sifat tanah (Modul 4) dan pemodelan DSM (Modul 8) belum dapat memakai nilai empiris per titik.
2. **DEM.** DTM LiDAR yang menjadi dasar `slope_lidar25` tidak ada. Untuk praktik, DEMNAS dapat diunduh dari Badan Informasi Geospasial.
3. **Ortofoto atau citra resolusi tinggi yang bersih**, tanpa unsur tata letak peta.
4. **Peta material permukaan (bahan induk)** yang dipakai Fatmawati (2026) sebagai kovariat P, bersumber dari Malik (2017).

## Asal-usul data

Tesis Fatmawati (2026), `Source/527460.pdf`, adalah sumber utama untuk menelusuri data `Survei.mpk` (`data_ta.gdb`, `shp_ta/`):

- **Rancangan sampel.** 50 titik ditentukan dengan *stratified random sampling* berdasarkan satuan pemetaan bentuklahan × penggunaan lahan × kemiringan lereng. Setiap titik diambil pada kedalaman 0–20 cm dan 20–40 cm (100 sampel). Parameter laboratorium meliputi pH, P, KPK, C-organik, tekstur (pemipetan), dan berat volume.
- **Kelas lereng** (`slope_lidar25` → `kelas_lereng`) diturunkan dari DTM LiDAR dengan kelas 0–8, 8–15, 15–25, 25–45, dan >45%.
- **Penggunaan lahan** (`Digit_PL` → `penggunaan_lahan`) berasal dari foto udara.
- **Bentuklahan** (`Landform` → `bentuklahan`) berasal dari survei kelompok riset Transbulent tahun 2015. Sambodo (2021) menyebut pemetaan tersebut berlangsung 2015–2016 dengan DEM TerraSAR-X 12 m dan foto udara.
- **Luas Sub-DAS.** Tesis menyebut luas Sub-DAS sekitar 292,69 ha. Sambodo (2021) menyebut 294,69 ha, dan perhitungan dari `batas_subdas` menghasilkan 294,71 ha.
- **Wilayah administratif.** Tesis menyebut Desa Wonogiri dan Kwaderan (Kecamatan Kajoran) serta Desa Margoyoso (Kecamatan Salaman), sesuai dengan hasil tumpang susun RBI di atas.

Hasil laboratorium dilaporkan dalam tesis berupa ringkasan statistik, sedangkan tabel data per titik tidak tersedia di folder ini. DTM LiDAR, foto udara asli, dan peta material permukaan juga tidak tersedia. Luas per bentuklahan pada `bentuklahan` sedikit berbeda dari tabel Sambodo (2021), sehingga versi datanya perlu dikonfirmasi.

## Rujukan

Fatmawati, N. D. (2026). *Evaluasi pendekatan SCORPAN dalam prediksi spasial fraksi tekstur tanah pada bahan induk hasil proses alterasi di Sub-DAS Bompon* [Tesis magister, Universitas Gadjah Mada]. Salinan: `Source/527460.pdf`.

Sambodo, A. P. (2021). *Application of landform arrangement and slope classes on detailed soil resources mapping in transitional volcanic landscape. Case study: Bompon Watershed, Magelang Regency, Central Java* [Tesis magister, Prince of Songkla University]. https://kb.psu.ac.th/psukb/bitstream/2016/17974/3/6130420006.pdf
