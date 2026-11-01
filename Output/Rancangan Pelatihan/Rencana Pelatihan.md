# Rencana Pelatihan

**Pelatihan Pemanfaatan Remote Sensing dan Digital Soil Mapping untuk Pertanian Presisi pada Perkebunan Kelapa Sawit**

Pusat Studi Pengelolaan Sumber Daya Lahan (PS2DL), Universitas Gadjah Mada

Selasa–Kamis, 3–5 November 2026 · Kantor PS2DL UGM

Status: rancangan.

## Gambaran umum

| Hal | Rencana |
|--------|------------------------------|
| Metode | Ceramah dan diskusi (±30%), praktik terbimbing (±60%), demonstrasi PSS, presentasi hasil |
| Wilayah latihan | Sub-DAS Bompon, Magelang (±295 ha). Pemandu menyertakan analogi ke kebun sawit karena wilayah ini bukan kebun sawit |
| Perangkat lunak | QGIS dan Python (Google Colab) |
| Pemandu praktik | Hari ke-1 Johan, hari ke-2 Nurarfiyah, hari ke-3 Ferry; demo PSS oleh Pak Pandu |
| Kegiatan lapangan | Tidak ada |
| Alur praktik | Semua praktik memakai data Bompon dan saling tersambung: data fusion → delineasi SMU dan bare soil → kovariat SCORPAN → model DSM → presentasi |

## Jadwal

Registrasi berlangsung setiap hari pukul 07.30–08.00. Coffee break pukul 09.00–09.15 dan 14.00–14.15. Istirahat pukul 11.45–13.00.

| Hari | Waktu | Kegiatan | Jenis | Pengisi |
|-------|--------|------------------------|-----|-------|
| Selasa, 3 Nov | 08.00–09.00 | Pengantar Remote Sensing dan Pemetaan Tanah pada Perkebunan (Modul 1) | Ceramah | Prof. Junun |
| | 09.15–10.15 | Interpretasi Pedologis dari Data Remote Sensing (Modul 6) | Ceramah | Dr. Anggri |
| | 10.15–11.45, 13.00–14.00 | Multi-source Data Fusion | **Praktik** | Johan |
| | 14.15–16.00 | Delineasi SMU (bagian 1) | **Praktik** | Johan |
| Rabu, 4 Nov | 08.00–09.00 | Delineasi SMU (bagian 2) | **Praktik** | Nurarfiyah |
| | 09.15–10.15 | Bare Soil Detection & Information Extraction (Modul 5) | Ceramah | Dr. Retnadi |
| | 10.15–11.45 | Proximal Soil Sensing (Modul 7) | Ceramah | Dr. Pandu |
| | 13.00–14.00 | Demonstrasi PSS | **Praktik** | Pak Pandu |
| | 14.15–16.00 | Bare Soil Detection | **Praktik** | Nurarfiyah |
| Kamis, 5 Nov | 08.00–09.00 | Digital Soil Mapping (Modul 8) | Ceramah | Dr. Guruh |
| | 09.15–10.15 | Machine Learning untuk DSM | **Praktik** | Ferry |
| | 10.15–11.45 | Penyiapan dan Pemilihan Kovariat SCORPAN | **Praktik** | Ferry |
| | 13.00–14.00, 14.15–15.00 | Pembangunan Model DSM | **Praktik** | Ferry |
| | 15.00–16.00 | Presentasi hasil, evaluasi, dan penutupan | **Praktik** | Ferry dan tim |

## Rincian sesi praktik

### Hari ke-1

#### 10.15–11.45 dan 13.00–14.00 · Praktik Multi-source Data Fusion
**Pemandu:** Johan · **Alat:** QGIS · **Konsep:** Modul 2

**Data:**

- Sentinel-2 dan Sentinel-1 (Copernicus);
- Copernicus DEM, DEMNAS (BIG), dan DTM LiDAR Bompon;
- penggunaan lahan dan peta material permukaan Bompon.

**Langkah:**

1. Pengantar singkat jenis data (optik, SAR, LiDAR, DEM, data lingkungan) dan tingkat fusi data.
2. Orientasi wilayah latihan Sub-DAS Bompon dan struktur folder data.
3. **Data optik:** membuka Sentinel-2, menampilkan komposit warna asli dan warna semu, membaca nilai pantulan, dan menyaring awan dengan lapisan SCL.
4. **Data SAR:** membuka Sentinel-1 polarisasi VV dan VH, lalu membandingkan kenampakannya dengan citra optik.
5. **Data elevasi:** membandingkan DEM permukaan (Copernicus DEM) dengan DTM LiDAR dan DEMNAS, lalu membuat *hillshade*.
6. **Data lingkungan:** membuka peta penggunaan lahan dan material permukaan.
7. **Integrasi:** menyeragamkan sistem koordinat, ukuran piksel, dan batas wilayah semua data, lalu menyusunnya menjadi satu tumpukan data.
8. Diskusi kelebihan dan keterbatasan setiap sumber data, termasuk analoginya untuk kebun sawit.

**Hasil:** satu set data Bompon yang sudah seragam dan siap dipakai di sesi berikutnya.

#### 14.15–16.00 · Praktik Delineasi SMU (bagian 1)
**Pemandu:** Johan · **Alat:** QGIS · **Data:** hasil data fusion · **Konsep:** Modul 3, Modul 4, Modul 6

1. Pengantar singkat konsep SMU, prinsip delineasi berbasis lanskap, serta skala dan luas minimum pemetaan.
2. Membuat peta kemiringan lereng dari DEM, lalu mengelompokkannya ke dalam kelas lereng.
3. Membuat *hillshade* untuk membantu melihat bentuk medan.
4. **Estimasi sifat tanah (Modul 4):** menghitung beberapa indeks sifat tanah dari Sentinel-2, misalnya indeks kecerahan, indeks warna, dan rasio mineral lempung.
5. Mengidentifikasi area yang karakteristik spektralnya berbeda, lalu mendiskusikan mengapa indeks ini hanya bermakna pada tanah yang terbuka.
6. Mendigitasi satuan bentuklahan di layar (*on-screen digitizing*) dengan bantuan *hillshade*, citra, dan unsur interpretasi.
7. Menyimpan semua hasil untuk dilanjutkan esok hari.

**Hasil:** poligon bentuklahan, peta kelas lereng, dan peta indeks sifat tanah.

### Hari ke-2

#### 08.00–09.00 · Praktik Delineasi SMU (bagian 2)
**Pemandu:** Nurarfiyah · **Alat:** QGIS · **Data:** hasil hari ke-1, penggunaan lahan, serta peta bentuklahan dan kelas lereng Bompon sebagai pembanding

1. Rekap hasil hari ke-1.
2. Menumpangsusunkan satuan bentuklahan, kelas lereng, dan penggunaan lahan.
3. Menyusun legenda SMU dari hasil tumpang susun.
4. Menggabungkan poligon yang terlalu kecil untuk skala peta sasaran.
5. Membandingkan hasil digitasi peserta dengan peta bentuklahan hasil riset.
6. Diskusi: letak perbedaan batas dan penyebabnya, serta mengapa SMU tetap perlu diuji di lapangan.

**Hasil:** peta SMU beserta legendanya.

#### 13.00–14.00 · Demonstrasi PSS
**Pengisi:** Pak Pandu, didampingi Nurarfiyah · **Bahan:** sensor hiperspektral buatan Pak Pandu dan sampel tanah

1. Pengenalan alat: bagian-bagian alat dan cara kerjanya.
2. Persiapan sampel tanah dan pengukuran referensi atau kalibrasi.
3. Demonstrasi pengukuran spektrum pantulan sampel tanah.
4. Peserta mencoba mengukur secara bergantian.
5. Membaca spektrum hasil ukur: membandingkan antarsampel dan mengenali fitur serapan.
6. Penjelasan alur dari spektrum ke sifat tanah melalui *machine learning*, sebagai jembatan ke praktik hari ke-3.

#### 14.15–16.00 · Praktik Bare Soil Detection
**Pemandu:** Nurarfiyah · **Alat:** QGIS (dan Colab untuk peragaan) · **Data:** deret waktu Sentinel-2 (Copernicus), penggunaan lahan Bompon

1. Rekap singkat materi pagi.
2. Memilih citra pada saat tegalan dan sawah sedang terbuka.
3. Menghitung NDVI, SAVI, BSI, dan NBR2.
4. Menentukan ambang, lalu membuat masker tanah terbuka.
5. Memeriksa salah deteksi pada jalan, permukiman, dan serasah.
6. Membandingkan lahan bervegetasi rapat (analogi blok sawit menghasilkan) dengan tegalan atau sawah bera (analogi blok peremajaan).
7. Menerapkan masker tanah terbuka pada peta indeks sifat tanah dari hari ke-1.
8. Peragaan oleh pemandu: menyusun komposit tanah terbuka dari deret waktu citra.
9. Diskusi keterbatasan metode.

**Hasil:** masker tanah terbuka dan peta indeks sifat tanah pada tanah terbuka.

### Hari ke-3

#### 09.15–10.15 · Praktik Machine Learning untuk DSM
**Pemandu:** Ferry · **Alat:** Colab · **Data:** tabel titik sampel Bompon (opsional: pustaka spektral Pak Pandu)

1. Pengenalan Colab: masuk akun, menyambungkan Google Drive, dan menjalankan sel.
2. Konsep dasar *machine learning* untuk DSM: data sasaran, prediktor, data latih, dan data uji.
3. Membaca tabel data.
4. Membagi data menjadi data latih dan data uji.
5. Melatih model *random forest*.
6. Menghitung metrik ketelitian.
7. Diskusi tentang *overfitting* dan tingkat kepentingan variabel.

#### 10.15–11.45 · Praktik Penyiapan dan Pemilihan Kovariat SCORPAN
**Pemandu:** Ferry · **Alat:** QGIS dan Colab · **Data:** hasil praktik hari ke-1 dan ke-2, titik sampel dan nilai laboratorium Bompon

1. Mengelompokkan hasil praktik sebelumnya ke dalam faktor SCORPAN.
2. Melengkapi kovariat relief, misalnya TWI dan posisi topografi.
3. Menyeragamkan grid semua kovariat.
4. Mengambil nilai kovariat di setiap titik sampel.
5. Menggabungkan nilai kovariat dengan nilai laboratorium menjadi tabel dataset.
6. Memilih kovariat: membuang yang saling mirip dan menilai relevansinya terhadap sifat tanah sasaran.

**Hasil:** tabel dataset dan daftar kovariat terpilih beserta alasannya.

#### 13.00–14.00 dan 14.15–15.00 · Praktik Pembangunan Model DSM
**Pemandu:** Ferry · **Alat:** Colab dan QGIS · **Data:** dataset hasil sesi kovariat

1. Memilih skema pembagian data.
2. Membandingkan validasi acak dengan validasi spasial.
3. Melatih model *random forest* dan model pembanding sederhana.
4. Menghitung dan menafsirkan metrik validasi.
5. Membuat peta prediksi sifat tanah untuk seluruh wilayah.
6. Membuat peta ketidakpastian prediksi.
7. Menampilkan hasil di QGIS bersama peta SMU.
8. Menyiapkan bahan presentasi.

**Hasil:** peta prediksi, peta ketidakpastian, dan tabel hasil validasi.

#### 15.00–16.00 · Presentasi Hasil, Evaluasi, dan Penutupan
**Pengisi:** Ferry bersama tim pemandu dan narasumber

1. Peserta mempresentasikan alur kerja dan hasilnya: data yang dipakai, peta SMU, kovariat terpilih, peta prediksi, dan keterbatasannya.
2. Tanggapan dari pemandu dan narasumber.
3. Post-test dan pengisian formulir evaluasi.
4. Kesan dan pesan.
5. Penutupan.

## Kebutuhan data

| Data | Sumber | Status |
|------------------------|--------------|--------|
| Batas, penggunaan lahan, bentuklahan, kelas lereng, posisi 50 titik sampel Bompon | Data riset Bompon (sudah di repository) | Ada |
| Sentinel-2 (satu adegan) dan Copernicus DEM | Data terbuka (sudah di repository) | Ada |
| Deret waktu Sentinel-2, Sentinel-1 | Copernicus (data terbuka) | Perlu diunduh |
| DEMNAS | BIG | Perlu diunduh |
| Nilai laboratorium per titik, DTM LiDAR, peta material permukaan | Nurarfiyah | Perlu diminta |
| Alat, sampel, dan pustaka spektral PSS | Pak Pandu | Perlu dikonfirmasi |

## Evaluasi

- **Pre-test dan post-test** tentang materi teori. Pre-test dikerjakan saat registrasi hari ke-1, post-test pada sesi penutupan.
- **Penilaian presentasi** hasil praktik oleh pemandu dan narasumber.
- **Formulir evaluasi** peserta untuk sesi, bahan, dan penyelenggaraan.

## Yang masih perlu dipastikan

1. **Data dan izin.** Data laboratorium, DTM LiDAR, dan peta material permukaan Bompon perlu diminta, termasuk izin membagikannya ke peserta (Nurarfiyah).
2. **Sifat tanah yang dimodelkan.** Usulan: fraksi lempung (Ferry/Nurarfiyah).
3. **Demo PSS.** Rincian alat dan sampel (Pak Pandu).
4. **Skala peta untuk delineasi SMU.**
5. **Teknis acara:** jaringan internet di lokasi, presentasi individu atau kelompok, dan siapa yang menutup acara.
