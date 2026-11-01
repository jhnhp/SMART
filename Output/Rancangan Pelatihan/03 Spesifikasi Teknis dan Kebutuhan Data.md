# Spesifikasi Teknis dan Kebutuhan Data

**Pelatihan Pemanfaatan Remote Sensing dan Digital Soil Mapping untuk Pertanian Presisi pada Perkebunan Kelapa Sawit**
PS2DL UGM · 3–5 November 2026

Status: rancangan, untuk ditinjau.
Dasar: `02 Rancangan Sesi Praktik.md`.

Dokumen ini memuat empat hal:
1. perangkat lunak dan lingkungan kerja;
2. spesifikasi laptop peserta;
3. instruksi persiapan yang dikirim ke peserta sebelum pelatihan;
4. daftar kebutuhan data per blok sebagai acuan penyiapan data.

Butir bertanda **[perlu konfirmasi]** belum ditetapkan.

## 1. Perangkat lunak

### 1.1 QGIS

| Hal | Ketentuan |
|---|---|
| Versi | **QGIS 3.44 LTR (*Long Term Release*)**. Saat diperiksa di qgis.org pada 28 Oktober 2026, versi LTR yang tersedia adalah 3.44.15 "Solothurn", sedangkan versi terbaru adalah 4.2.3. Versi LTR dipilih karena paling stabil. Semua peserta dan pemandu memakai seri 3.44 yang sama |
| Pemasang | Windows: *standalone installer* dari qgis.org. macOS dan Linux: paket resmi dari qgis.org |
| Plugin wajib | **Tidak ada.** Semua langkah praktik memakai alat bawaan QGIS (lihat Tabel 1.1) agar instalasi peserta tetap sederhana |
| Plugin opsional | Peta dasar daring (mis. QuickMapServices) hanya untuk orientasi, tidak wajib |

Tabel 1.1 Alat bawaan QGIS yang dipakai per blok

| Blok | Alat (menu *Processing* / bawaan) |
|---|---|
| B1 Data Fusion | Tampilan multikanal, *Warp (reproject)*, *Clip raster by mask layer*, *Align rasters*, *Build virtual raster* |
| B2 Delineasi SMU | *Slope*, *Hillshade*, *Reclassify by table*, *Raster calculator*, alat digitasi, *Union*/*Intersection*, *Eliminate selected polygons* |
| B4 Bare Soil | *Raster calculator*, simbologi dan histogram, *Zonal statistics* |
| B6 Kovariat | *TPI (Topographic Position Index)* dari GDAL, *Sample raster values* (untuk pengecekan) |
| B7 Model DSM | Menampilkan GeoTIFF hasil prediksi dan ketidakpastian |

Kovariat relief yang memerlukan alat tambahan, seperti TWI dan kelengkungan (SAGA/WhiteboxTools), **dihitung sebelumnya oleh pemandu** dan dibagikan sebagai raster jadi. Peserta cukup memahami makna dan cara membuatnya dari pengantar konsep. Dengan begitu, peserta tidak perlu memasang SAGA.

### 1.2 Python di Google Colab

| Hal | Ketentuan |
|---|---|
| Akses | Peramban (Chrome disarankan) dan **akun Google pribadi** setiap peserta |
| Data | Folder bersama di Google Drive yang disambungkan (*mount*) ke Colab |
| Pustaka | `numpy`, `pandas`, `matplotlib`, `scipy`, `scikit-learn`, `geopandas`, `rasterio`, `quantile-forest` |
| Pemasangan | Sel pertama setiap notebook menjalankan `pip install` untuk pustaka yang belum tersedia di Colab. Isi bawaan Colab bisa berubah sewaktu-waktu, jadi notebook **diuji ulang H-1** |
| Batas sumber daya | Colab gratis memiliki batas RAM dan waktu sesi. Raster wilayah latihan dijaga kecil (resolusi 10–30 m, cakupan beberapa km²) agar seluruh proses selesai dalam hitungan detik sampai menit |

Tabel 1.2 Penggunaan Colab per blok

| Blok | Isi notebook |
|---|---|
| B1 | Peragaan akses dan pengunduhan data (oleh pemandu saja) |
| B3/B5 | Membaca spektrum, praolah (SNV, turunan Savitzky–Golay dengan `scipy`) jika pustaka spektral tersedia |
| B4 | Peragaan komposit multitemporal (median piksel tanah terbuka) dengan `rasterio` + `numpy` |
| B5 | Pengenalan alur ML: `pandas`, `scikit-learn` (*random forest*), metrik |
| B6 | Ekstraksi nilai raster di titik (`rasterio`, `geopandas`), matriks korelasi, seleksi kovariat |
| B7 | Pembagian data dan validasi silang spasial, RF dan regresi linear, metrik Tabel 8.3, prediksi ke grid, QRF (`quantile-forest`), peragaan AOA dengan kode yang disiapkan pemandu |

### 1.3 Ketergantungan pada internet

Colab hanya bisa dipakai jika internet berjalan. Risiko ini diantisipasi sebagai berikut.
1. **Jaringan lokasi.** Kapasitas jaringan di Kantor PS2DL perlu diperiksa untuk ±5–20 laptop yang memakai Colab bersamaan. **[perlu konfirmasi]**
2. **Data diunggah ke Drive sebelum pelatihan.** Data juga disalin ke *flashdisk* untuk kebutuhan QGIS.
3. **Cadangan jika jaringan gagal.** Pemandu menjalankan notebook di proyektor dari laptop dengan koneksi seluler, dan hasil setiap titik periksa dibagikan sebagai berkas jadi lewat *flashdisk*.

## 2. Spesifikasi laptop peserta

Spesifikasi berikut adalah rekomendasi penyelenggara untuk praktik ini, bukan syarat minimum resmi QGIS.

| Komponen | Rekomendasi |
|---|---|
| Sistem operasi | Windows 10/11 64-bit, macOS, atau Linux 64-bit |
| RAM | ≥ 8 GB |
| Ruang disk kosong | ≥ 10 GB (QGIS beserta paket data dan hasil kerja) |
| Peramban | Chrome versi terbaru |
| Perlengkapan | **Mouse** (wajib untuk digitasi di Blok 2), pengisi daya, dan sebaiknya *port* USB untuk *flashdisk* |
| Hak akses | Hak administrator untuk memasang perangkat lunak, atau QGIS sudah dipasang oleh tim TI perusahaan sebelum pelatihan |

## 3. Instruksi persiapan untuk peserta

Instruksi ini dikirim melalui panitia paling lambat **H-4 (30 Oktober 2026)** **[perlu konfirmasi]**. Peserta diminta menyelesaikannya sebelum hari pertama.

1. **Pasang QGIS** versi LTR yang ditentukan dari qgis.org. Buka QGIS sekali untuk memastikan program berjalan.
2. **Siapkan akun Google**, lalu buka colab.research.google.com dan pastikan bisa masuk.
3. **Jalankan notebook uji** (`00_uji_lingkungan.ipynb`, tautan dari panitia). Notebook ini memasang pustaka, menyambungkan Google Drive, dan mencetak versi pustaka. Peserta mengirimkan tangkapan layar hasilnya ke panitia.
4. **Unduh paket data** dari tautan panitia, lalu ekstrak ke folder dengan nama pendek tanpa spasi, misalnya `C:\pelatihan_dsm\`.
5. **Pastikan perlengkapan:** mouse, pengisi daya, dan izin administrator.

Peserta yang mengalami kendala menghubungi pemandu sebelum H-1 **[perlu konfirmasi: kanal kontak]**. Pada hari pertama, 07.30–08.00 (registrasi) dapat dipakai untuk pengecekan cepat oleh tim pemandu.

## 4. Kebutuhan data per blok

Wilayah latihan adalah **Sub-DAS Bompon** (EPSG:32749 / UTM 49S). Data dasarnya ada di `Source/Data Bompon/` (`bompon.gpkg`, `tabel/`, `terbuka/`). Tabel berikut memisahkan data yang **sudah ada**, yang **diminta** dari Nurarfiyah, dan yang **belum** diunduh.

| Blok | Data | Bentuk | Sumber | Penyiap | Status |
|---|---|---|---|---|---|
| Semua | Batas Sub-DAS | Vektor | `bompon.gpkg` → `batas_subdas` | – | **Ada** |
| B1, B2 | Sentinel-2 L2A 21 Juli 2025 + SCL (10 kanal, 10 m) | Raster | `terbuka/` (Earth Search) | – | **Ada** |
| B4 | Deret waktu Sentinel-2 L2A, termasuk adegan saat tegalan dan sawah terbuka | Raster | Earth Search; perluasan `skrip/unduh_data_terbuka.py` | Johan | Belum |
| B1 | Sentinel-1 σ⁰ VV, VH (terkoreksi medan) | Raster | Kandidat: Microsoft Planetary Computer (`sentinel-1-rtc`), atau CDSE/GEE | Johan | Belum |
| B1, B2, B6 | Copernicus DEM GLO-30 (model **permukaan**, 30 m) | Raster | `terbuka/` | – | **Ada** |
| B1, B2, B6 | DEMNAS (±8 m) | Raster | BIG (memerlukan akun) | Johan | Belum |
| B1, B2, B6 | DTM LiDAR (dasar `kelas_lereng`) | Raster | Nurarfiyah | Nurarfiyah | **Diminta** |
| B2 | Penggunaan lahan (4 kelas) | Vektor | `bompon.gpkg` → `penggunaan_lahan` | – | **Ada** |
| B2 (pembanding) | Bentuklahan (6 satuan) dan kelas lereng | Vektor | `bompon.gpkg` → `bentuklahan`, `kelas_lereng` | – | **Ada** |
| B1, B6 | Peta material permukaan (kovariat *p* dalam tesis, dari Malik, 2017) | Vektor | Nurarfiyah | Nurarfiyah | **Diminta** |
| B1, B6 | Peta geologi lembar | Vektor | Badan Geologi | Johan | Opsional |
| B6 | Curah hujan rata-rata (mis. CHIRPS) | Raster | Produk iklim global | Johan | Opsional; hampir seragam di ±295 ha, jadi berguna sebagai contoh kovariat yang tidak informatif (Tabel 8.1) |
| B6 | TWI, kelengkungan (dihitung sebelumnya) | Raster | Diturunkan dari DTM LiDAR, atau DEMNAS jika LiDAR tidak ada | Ferry | Menunggu DEM |
| B5–B7 | 50 titik sampel (posisi GPS lapangan) | Vektor/CSV | `titik_sampel_lapangan`, `tabel/titik_sampel_lapangan.csv` | – | **Ada** |
| B5–B7 | **Tabel nilai laboratorium per titik** (0–20 dan 20–40 cm) | Tabel | Nurarfiyah | Nurarfiyah | **Diminta, penentu Blok 6–7** |
| B3, B5 | Spektrum alat PSS dan pustaka spektral | Tabel/berkas spektral | Pak Pandu | Pak Pandu | **Diminta** |
| Semua | Berkas hasil jadi setiap titik periksa (TP1–TP9) | Campuran | Dibuat saat uji coba alur | Pemandu tiap hari | Belum |
| B4–B7 | Notebook Colab (B4, B5, B6, B7) | `.ipynb` | Dibuat tim | Nurarfiyah (B4), Ferry (B5–B7) | Belum |
| – | Notebook uji lingkungan | `.ipynb` | `notebook/00_uji_lingkungan.ipynb` | Johan | **Ada** |

Catatan data Bompon yang perlu diselesaikan bersama Nurarfiyah (dari `Source/Data Bompon/README.md`):
- B30 tercatat di dua lokasi, sedangkan C38 tercatat sebagai "C38" dan "C38 ril" yang terpaut ±490 m. Posisi yang benar perlu dipastikan.
- B32 dan C47 tidak memiliki rekaman GPS.
- **Izin penggunaan.** Data ini adalah data riset, sehingga perlu dipastikan boleh dibagikan ke peserta pelatihan dari perusahaan, dan dengan ketentuan atribusi apa.

### 4.1 Struktur paket data yang diusulkan

```
pelatihan_dsm/
├── 00_batas/            batas wilayah latihan
├── 01_optik/            Sentinel-2 (adegan tunggal, SCL, deret waktu)
├── 02_sar/              Sentinel-1 σ⁰ VV, VH
├── 03_dem/              Copernicus DEM, DEMNAS, DTM LiDAR, turunan relief jadi (TWI, kelengkungan)
├── 04_lingkungan/       penggunaan lahan, material permukaan, geologi, curah hujan
├── 04b_pembanding/      bentuklahan, kelas_lereng (dibagikan di akhir Blok 2)
├── 05_titik_sampel/     titik sampel + nilai laboratorium
├── 06_spektral_pss/     spektrum dan pustaka spektral (jika tersedia)
├── notebook/            00_uji_lingkungan, B4, B5, B6, B7
└── cadangan/            TP1 … TP9 (hasil jadi setiap titik periksa)
```

Semua raster dan vektor memakai **EPSG:32749 (WGS 84 / UTM 49S)** dan grid acuan yang sama dengan `terbuka/`, yaitu penyangga 200 m dari batas Sub-DAS.

## 5. Usulan jadwal persiapan

| Tanggal | Kegiatan | Penanggung jawab |
|---|---|---|
| Kam, 29 Okt | Meminta tabel laboratorium, DTM LiDAR, dan peta material permukaan kepada Nurarfiyah; mengirim pertanyaan ke Pak Pandu | Johan |
| Jum, 30 Okt | Mengirim instruksi persiapan dan notebook uji ke peserta melalui panitia | Johan, panitia |
| 30 Okt–1 Nov | Menyiapkan data dan notebook per blok | Johan (H1), Nurarfiyah (H2), Ferry (H3) |
| Min, 1 Nov | **Uji coba alur penuh** B1→B7 oleh pemandu di laptop bersih; membuat berkas cadangan TP1–TP9 | Tim pemandu |
| Sen, 2 Nov | Paket data final diunggah ke Drive dan disalin ke *flashdisk*; uji ulang notebook di Colab; mengecek jaringan dan proyektor di lokasi | Tim pemandu, panitia |

Tanggal di atas adalah usulan dan perlu disesuaikan dengan ketersediaan tim. **[perlu konfirmasi]**
