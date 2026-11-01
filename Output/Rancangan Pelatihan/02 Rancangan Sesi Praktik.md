# Rancangan Sesi Praktik

**Pelatihan Pemanfaatan Remote Sensing dan Digital Soil Mapping untuk Pertanian Presisi pada Perkebunan Kelapa Sawit**
PS2DL UGM · 3–5 November 2026

Status: rancangan, untuk ditinjau.
Dasar: `01 Matriks Rundown.md`. Isi setiap blok diturunkan dari judul dan cakupan sesi pada rundown. Modul teori dipakai sebagai rujukan konsep.
Perangkat lunak: QGIS dan Python (Google Colab).

Dokumen ini merancang **apa yang dikerjakan** di setiap blok praktik. Berkas data belum disiapkan, sehingga kebutuhan data ditulis secara deskriptif. Rinciannya akan dituangkan di `03 Spesifikasi Teknis dan Kebutuhan Data.md`. Butir bertanda **[perlu konfirmasi]** belum boleh diisi dengan asumsi.

## 1. Alur benang merah

Semua blok praktik mengerjakan **satu wilayah latihan yang sama**. Dengan begitu, keluaran satu blok menjadi masukan blok berikutnya, dan pada hari ke-3 peserta memegang satu alur kerja DSM yang utuh dari data mentah sampai peta prediksi.

```
[B1] Data Fusion (H1)
  data seragam: optik, SAR, DEM, data lingkungan
   │
   ├──► [B2] Delineasi SMU (H1–H2)
   │      SMU, kelas lereng, indeks sifat tanah (Modul 4) ──┐
   │                                                        │
   └──► [B4] Bare Soil (H2)                                 │
          masker & komposit tanah terbuka ──────────────────┤
                                                            │
[B3] Demo PSS hiperspektral (H2)                            │
  spektrum pantulan sampel                                  │
   ┆                                                        │
   ┆ opsional: pustaka spektral                             │
   ▼                                                        ▼
[B5] ML untuk DSM (H3) ───── bekal alur kerja ─────► [B6] Kovariat SCORPAN (H3)
                                                       tabel dataset + stack kovariat
                                                            │
                                                            ▼
                                                     [B7] Model DSM (H3)
                                                       peta prediksi, ketidakpastian, metrik
                                                            │
                                                            ▼
                                                     [B8] Presentasi (H3)
```

Garis putus-putus menunjukkan kaitan konseptual. Spektrum dari alat PSS diubah menjadi sifat tanah dengan pembelajaran mesin, sama seperti logika yang dipakai pada hari ke-3. Jika tersedia pustaka spektral berpasangan nilai laboratorium, data itu dapat menjadi contoh latihan Blok 5 **[perlu konfirmasi]**.

### Wilayah latihan: Sub-DAS Bompon

Wilayah latihan adalah **Sub-DAS Bompon**, Kabupaten Magelang (±295 ha, EPSG:32749 / UTM 49S). Data dasarnya ada di `Source/Data Bompon/`. Wilayah ini dipilih karena datanya paling lengkap untuk alur DSM: titik sampel tanah berlapis bentuklahan × penggunaan lahan × lereng, peta bentuklahan hasil riset, serta tesis SCORPAN yang memakai data yang sama (Fatmawati, 2026). Nurarfiyah, pemandu hari ke-2, adalah penulis tesis tersebut.

Konsekuensinya bagi rancangan:
1. **Bukan perkebunan kelapa sawit.** Penggunaan lahannya agroforestri (±209 ha), permukiman (±35 ha), sawah (±34 ha), dan tegalan (±17 ha). Setiap blok perlu menyertakan **analogi ke kebun sawit** yang disampaikan pemandu. Misalnya, tegalan atau sawah saat bera dianalogikan dengan blok peremajaan, sedangkan agroforestri dianalogikan dengan blok bertajuk rapat.
2. **Tanah jarang terbuka.** Pada adegan Sentinel-2 21 Juli 2025, SCL mencatat ±98,6% vegetasi di dalam Sub-DAS. Blok 4 karena itu memakai **deret waktu Sentinel-2** untuk menangkap tegalan dan sawah saat terbuka. Indeks sifat tanah di Blok 2 juga hanya bermakna pada piksel tersebut, dan hal ini dijadikan bahan diskusi.
3. **Titik sampel tersedia, nilai laboratoriumnya belum.** Ada 50 titik, masing-masing dengan kedalaman 0–20 cm dan 20–40 cm. Parameternya pH, P, KPK, C-organik, tekstur, dan berat volume. Tabel nilai per titik diminta dari Nurarfiyah (`08 Pesan untuk Nurarfiyah.md`).
4. **Peta riset sebagai pembanding.** Layer `bentuklahan` dan `kelas_lereng` **tidak dibagikan di awal Blok 2**. Keduanya dipakai sebagai pembanding hasil digitasi peserta di akhir blok.
5. **Sifat sasaran pemodelan** diusulkan **fraksi lempung 0–20 cm**, sejalan dengan fokus tesis pada fraksi tekstur. **[perlu konfirmasi: Ferry dan Nurarfiyah]**

## 2. Prinsip umum semua blok

- **Pengantar konsep di awal blok.** Modul 2, 3, dan 4 tidak punya slot ceramah, sehingga blok yang memakainya dibuka dengan pengantar konsep 10–15 menit oleh pemandu yang merujuk ke tabel dan gambar modul.
- **Pola kerja.** Pemandu memperagakan satu langkah, peserta mengulanginya di laptop masing-masing, lalu hasilnya dicek bersama. Setiap blok punya **titik periksa**, yaitu hasil antara yang harus dimiliki semua peserta sebelum lanjut.
- **Data sudah disiapkan.** Data dibagikan sebelum sesi, tidak diunduh saat pelatihan, untuk menghindari kendala jaringan. Cara mengakses dan mengunduh hanya diperagakan.
- **Cadangan.** Setiap titik periksa disertai berkas hasil jadi, agar peserta yang tertinggal dapat langsung melanjutkan ke blok berikutnya.

---

## Blok 1 — Multi-source Data Fusion

| | |
|---|---|
| **Slot** | Hari ke-1, 10.15–11.45 (90') dan 13.00–14.00 (60'), total 150 menit |
| **Pemandu** | Johan |
| **Alat** | QGIS (utama); Colab untuk peragaan pengunduhan/akses data |
| **Modul teori** | Modul 2: Tabel 2.1 (sumber data), Gambar 2.1 dan tiga tingkat fusi |

**Tujuan sesi** (dari rundown: *karakteristik dan integrasi data optik, SAR, LiDAR, DEM, serta data lingkungan*)
1. Peserta mengenali karakteristik setiap jenis data: resolusi, satuan nilai, sistem koordinat, dan informasi yang dibawanya.
2. Peserta mampu menyeragamkan data multisumber ke satu sistem koordinat, satu grid, dan satu batas wilayah sehingga siap dipadukan.

**Alur**

| Menit | Kegiatan |
|---|---|
| **Sesi 1a (90')** | |
| 0–15 | Pengantar konsep: jenis data dan tingkat fusi (Modul 2) |
| 15–25 | Orientasi wilayah latihan dan struktur folder data |
| 25–55 | Data optik: membuka Sentinel-2, komposit warna asli dan semu, membaca nilai pantulan, masker awan (SCL) |
| 55–80 | Data SAR: membuka Sentinel-1, polarisasi VV dan VH, satuan dB, kenampakan *speckle*; perbandingan visual dengan optik |
| 80–90 | **Titik periksa 1:** citra optik dan SAR tampil benar di QGIS |
| **Sesi 1b (60')** | |
| 0–20 | DEM (dan LiDAR jika ada): perbedaan DSM dan DTM, *hillshade*, membandingkan dua resolusi DEM |
| 20–30 | Data lingkungan: peta geologi, data iklim, dan penggunaan lahan sebagai data vektor/raster pendukung |
| 30–50 | Integrasi: *reproject*, *resample* ke grid acuan, *clip* ke batas wilayah, lalu menyusun *virtual raster*/stack |
| 50–60 | **Titik periksa 2:** semua lapisan berada pada CRS, grid, dan batas yang sama; diskusi kelebihan dan keterbatasan tiap sumber |

**Keluaran peserta:** satu folder data wilayah latihan yang sudah seragam (CRS, resolusi, batas). Folder ini menjadi masukan Blok 2, 4, dan 6.
**Kebutuhan data:** Sentinel-2 L2A (beserta SCL), Sentinel-1 GRD hasil praolah, DEM (DEMNAS dan/atau Copernicus GLO-30), LiDAR (opsional), batas wilayah latihan, serta peta geologi dan iklim jika tersedia.
**Catatan:** Praolah Sentinel-1 (kalibrasi, koreksi medan) tidak dikerjakan peserta karena memakan waktu. Pemandu cukup menjelaskan langkahnya.

---

## Blok 2 — Remote Sensing untuk Delineasi SMU (termasuk estimasi sifat tanah)

| | |
|---|---|
| **Slot** | Hari ke-1, 14.15–16.00 (105'), dan hari ke-2, 08.00–09.00 (60'), total 165 menit |
| **Pemandu** | Johan (bagian 1) → Nurarfiyah (bagian 2) |
| **Alat** | QGIS |
| **Modul teori** | Modul 3: Tabel 3.1, Tabel 3.2, prinsip delineasi, MLA dan Gambar 3.4–3.5. Modul 4: Tabel 4.1–4.2. Modul 6: interpretasi pola citra (ceramah Dr. Anggri pagi harinya) |

**Tujuan sesi** (dari rundown: *Remote Sensing untuk Delineasi SMU*; Modul 4 dilebur di sini)
1. Peserta mampu menurunkan data pendukung delineasi dari data Blok 1, yaitu kelas lereng, *hillshade*, dan transformasi indeks sifat tanah.
2. Peserta mampu mendelineasi satuan bentuklahan secara *on-screen digitizing* dengan memakai unsur interpretasi.
3. Peserta mampu menyusun SMU dari tumpang susun satuan lahan dan menyesuaikannya dengan skala peta.

**Alur bagian 1 (hari ke-1, 105', Johan)**

| Menit | Kegiatan |
|---|---|
| 0–15 | Pengantar konsep: SMU, prinsip delineasi berbasis lanskap, skala dan MLA (Modul 3) |
| 15–35 | Turunan DEM: kemiringan lereng, lalu klasifikasi kelas lereng dan *hillshade* |
| 35–60 | Estimasi sifat tanah (Modul 4): menghitung beberapa indeks Tabel 4.2 (mis. BI, CI, RI, CMR) dengan *Raster Calculator*, lalu mengidentifikasi area yang berbeda karakteristik spektralnya; diskusi mengapa hasilnya hanya bermakna pada piksel tanah terbuka |
| 60–95 | Delineasi satuan bentuklahan secara *on-screen digitizing* dengan bantuan *hillshade*, citra, dan unsur interpretasi (Tabel 3.2) |
| 95–105 | **Titik periksa 3 (titik henti hari ke-1):** poligon bentuklahan, raster kelas lereng, dan raster indeks disimpan dalam satu GeoPackage |

**Alur bagian 2 (hari ke-2, 60', Nurarfiyah)**

| Menit | Kegiatan |
|---|---|
| 0–10 | Rekap hasil hari ke-1; peserta yang belum selesai memuat berkas cadangan |
| 10–30 | Tumpang susun bentuklahan × kelas lereng (× penggunaan lahan), lalu menyusun legenda SMU |
| 30–45 | Generalisasi: menggabungkan poligon yang lebih kecil dari MLA pada skala sasaran (Gambar 3.5) |
| 45–60 | **Titik periksa 4:** peta SMU dengan legenda. Hasil digitasi peserta ditumpangsusunkan dengan peta bentuklahan riset (layer `bentuklahan`), lalu didiskusikan: di mana batasnya berbeda, mengapa, dan mengapa SMU tetap merupakan hipotesis yang harus diuji di lapangan |

**Keluaran peserta:** peta SMU (GeoPackage + legenda), raster kelas lereng, dan raster indeks sifat tanah. Raster lereng dan indeks menjadi kandidat kovariat di Blok 6.
**Kebutuhan data:** keluaran Blok 1, layer `penggunaan_lahan`, layer pembanding `bentuklahan` dan `kelas_lereng` (dibuka di akhir blok), serta skala peta sasaran. **[perlu konfirmasi: skala sasaran]**
**Catatan:** Indeks Tabel 4.2 yang memerlukan data hiperspektral (NSMI, *band depth*) hanya dibahas, tidak dihitung.

---

## Blok 3 — Proximal Soil Sensing: demonstrasi pengukuran

| | |
|---|---|
| **Slot** | Hari ke-2, 13.00–14.00, 60 menit |
| **Pemandu** | Pak Pandu (alat buatan sendiri); Nurarfiyah mendampingi |
| **Alat** | Sensor hiperspektral buatan Pak Pandu. Alat ini merekam spektrum pantulan sampel tanah, bukan nilai sifat tanah secara langsung |
| **Modul teori** | Modul 7: subbab Interpretasi Pantulan Spektral Proximal Soil Sensing (fitur serapan, praolah pada Gambar 7.3, kalibrasi dan pustaka spektral pada Gambar 7.4); Modul 4: kromofor dan fitur serapan tanah |

**Tujuan sesi** (dari rundown: *demonstrasi pengukuran*)
1. Peserta melihat langsung prosedur pengukuran spektrum pantulan tanah dengan sensor hiperspektral.
2. Peserta mampu membaca spektrum hasil ukur, yaitu bentuk kurva dan fitur serapan, serta memahami bahwa sifat tanah diperoleh dari spektrum melalui model kalibrasi atau pembelajaran mesin, bukan dibaca langsung dari alat.

**Alur**

| Menit | Kegiatan |
|---|---|
| 0–10 | Pengenalan alat: komponen, sumber cahaya, rentang panjang gelombang, dan pengukuran referensi atau kalibrasi **[perlu konfirmasi: spesifikasi]** |
| 10–25 | Demonstrasi pengukuran: persiapan sampel, pengukuran referensi, pengukuran sampel, dan ulangan |
| 25–40 | Peserta mencoba mengukur secara bergantian **[perlu konfirmasi: jumlah unit alat dan sampel]** |
| 40–52 | Membaca spektrum: membandingkan spektrum antarsampel, mengenali fitur serapan sesuai rentang alat (oksida besi, air dan OH, mineral lempung), serta melihat efek praolah seperti SNV dan turunan (Gambar 7.3) |
| 52–60 | Jembatan ke hari ke-3: spektrum diolah dengan pustaka spektral dan pembelajaran mesin menjadi sifat tanah (Gambar 7.4); hasilnya dapat menjadi data sasaran tambahan atau kovariat faktor *s* (Tabel 8.1) |

**Keluaran peserta:** spektrum pantulan hasil ukur (berkas, jika dapat dibagikan) dan pemahaman alur dari spektrum ke sifat tanah.
**Kaitan ke Blok 5 (opsional):** Jika Pak Pandu memiliki pustaka spektral berpasangan nilai laboratorium yang boleh dipakai, data itu dapat menjadi tabel contoh latihan ML di Blok 5 (spektrum → sifat tanah). Dengan begitu, demo hari ke-2 tersambung langsung ke hari ke-3. **[perlu konfirmasi]**
**Yang perlu ditanyakan ke Pak Pandu:**
- nama alat, rentang panjang gelombang, dan resolusi spektral;
- prosedur referensi atau kalibrasi;
- format berkas keluaran;
- jumlah unit;
- kebutuhan sampel (jumlah, kering atau lembap, perlu diayak atau tidak);
- kebutuhan listrik atau ruang;
- ketersediaan pustaka spektral dengan nilai laboratorium untuk latihan;
- bahan presentasi pendukung.

---

## Blok 4 — Bare Soil Detection & Information Extraction

| | |
|---|---|
| **Slot** | Hari ke-2, 14.15–16.00, 105 menit |
| **Pemandu** | Nurarfiyah |
| **Alat** | QGIS (utama); Colab untuk peragaan komposit multitemporal |
| **Modul teori** | Modul 5: Gambar 5.1–5.2, Tabel 5.1, metode deteksi 1–5, Gambar 5.4 (ceramah Dr. Retnadi pagi harinya) |

**Tujuan sesi** (dari rundown: *Bare Soil Detection & Information Extraction*)
1. Peserta mampu menghitung indeks deteksi tanah terbuka dan menyusun masker tanah terbuka dengan ambang.
2. Peserta mampu mengekstraksi informasi tanah, yaitu pantulan dan indeks sifat tanah, hanya dari piksel tanah terbuka.

**Alur**

| Menit | Kegiatan |
|---|---|
| 0–10 | Rekap singkat ceramah pagi: mengapa tanah di perkebunan sawit jarang terbuka |
| 10–35 | Menghitung NDVI, SAVI, BSI, dan NBR2 (Tabel 5.1) dari Sentinel-2 dengan masker awan |
| 35–55 | Menerapkan ambang dan aturan gabungan untuk masker tanah terbuka pada citra saat tegalan dan sawah terbuka; membandingkan agroforestri (analogi blok bertajuk rapat) dengan tegalan dan sawah bera (analogi blok peremajaan) |
| 55–70 | **Titik periksa 5:** masker tanah terbuka; memeriksa salah deteksi pada jalan, permukiman, dan serasah |
| 70–90 | Ekstraksi informasi: menerapkan masker pada raster indeks sifat tanah dari Blok 2, lalu membandingkan pola sebelum dan sesudah masker |
| 90–105 | Peragaan oleh pemandu: komposit multitemporal (median piksel terbuka) di Colab; diskusi keterbatasan ambang (Modul 5) |

**Keluaran peserta:** raster indeks, masker tanah terbuka, raster indeks sifat tanah yang sudah dimasker, dan (dari peragaan) komposit tanah terbuka. Komposit ini menjadi kandidat kovariat faktor *o* di Blok 6.
**Kebutuhan data:** satu adegan Sentinel-2 L2A saat tegalan dan sawah terbuka (dipilih dari deret waktu), deret waktu Sentinel-2 untuk peragaan komposit, dan layer `penggunaan_lahan`.
**Catatan:** Ambang Tabel 5.1 tidak berlaku umum (Modul 5). Peserta diminta menilai ambang dengan melihat citra, bukan menerimanya begitu saja.

---

## Blok 5 — Machine Learning untuk Digital Soil Mapping

| | |
|---|---|
| **Slot** | Hari ke-3, 09.15–10.15, 60 menit |
| **Pemandu** | Ferry |
| **Alat** | Colab |
| **Modul teori** | Modul 8: Algoritma DSM (Tabel 8.2), Data Splitting (ceramah Dr. Guruh sebelumnya) |

**Tujuan sesi** (dari rundown: *Machine Learning untuk DSM*)
1. Peserta memahami alur pembelajaran mesin untuk DSM: data sasaran, kovariat, latih, uji, dan prediksi.
2. Peserta mampu menjalankan notebook Colab, membaca data tabel dan raster, serta melatih model sederhana.

**Alur**

| Menit | Kegiatan |
|---|---|
| 0–10 | Orientasi Colab: masuk akun, menyambungkan data (Google Drive), menjalankan sel |
| 10–20 | Pengantar konsep: regresi vs klasifikasi, *random forest*, *overfitting* (Modul 8) |
| 20–45 | Latihan pada tabel contoh: membaca data (pandas), membagi latih/uji, melatih *random forest* (scikit-learn), menghitung metrik |
| 45–60 | **Titik periksa 6:** notebook berjalan sampai metrik keluar; diskusi tentang makna *feature importance* dan bahayanya |

**Keluaran peserta:** notebook Colab yang berjalan dan pemahaman alur dasar sebagai bekal Blok 6–7.
**Kebutuhan data:** satu tabel contoh kecil berisi data prediktor dan nilai sasaran. Ada dua pilihan sumber:
1. **Pustaka spektral alat Pak Pandu**, berupa spektrum dan nilai laboratorium, yang menyambungkan demo Blok 3 dengan pembelajaran mesin. **[perlu konfirmasi]**
2. **Titik wilayah latihan**, berupa kovariat dan nilai sasaran, yang tersambung langsung dengan Blok 6.

---

## Blok 6 — Penyiapan dan pemilihan kovariat berdasarkan konsep SCORPAN

| | |
|---|---|
| **Slot** | Hari ke-3, 10.15–11.45, 90 menit |
| **Pemandu** | Ferry |
| **Alat** | QGIS (pemeriksaan lapisan) dan Colab (ekstraksi dan seleksi) |
| **Modul teori** | Modul 8: Tabel 8.1, kriteria pemilihan kovariat 1–5, Gambar 8.1. Modul 2 dan Modul 4 sebagai sumber kovariat |

**Tujuan sesi** (dari rundown: *penyiapan dan pemilihan kovariat dari data remote sensing berdasarkan SCORPAN*)
1. Peserta mampu memetakan keluaran Blok 1, 2, dan 4 ke faktor SCORPAN.
2. Peserta mampu menyusun dataset pemodelan dengan mengekstraksi nilai kovariat di titik sampel.
3. Peserta mampu memilih kovariat berdasarkan relevansi pedologis dan redundansi.

**Alur**

| Menit | Kegiatan |
|---|---|
| 0–15 | Pengantar: Tabel 8.1, lalu peserta mengisi lembar "kovariat saya per faktor SCORPAN" dari keluaran hari ke-1 dan ke-2 |
| 15–35 | Melengkapi kovariat relief dari DEM (mis. TWI, TPI, kelengkungan) dan menyeragamkan grid semua kovariat |
| 35–55 | Ekstraksi nilai kovariat di titik sampel tanah, lalu menggabungkannya dengan nilai sasaran menjadi tabel dataset |
| 55–80 | Seleksi: matriks korelasi antarkovariat, membuang yang redundan, dan menilai relevansi pedologis terhadap sifat sasaran |
| 80–90 | **Titik periksa 7:** tabel dataset dan daftar kovariat terpilih beserta alasannya |

**Keluaran peserta:** tabel dataset (titik × kovariat terpilih + nilai sasaran) dan stack raster kovariat terpilih.
**Kebutuhan data:** keluaran Blok 1, 2, dan 4; layer `titik_sampel_lapangan` beserta **tabel nilai laboratorium per titik** dari Nurarfiyah; dan peta material permukaan (kovariat *p*) jika diizinkan. **[perlu konfirmasi: sifat tanah sasaran]**

---

## Blok 7 — Pembangunan model DSM

| | |
|---|---|
| **Slot** | Hari ke-3, 13.00–14.00 (60') dan 14.15–15.00 (45'), total 105 menit |
| **Pemandu** | Ferry |
| **Alat** | Colab (pemodelan); QGIS (menampilkan peta) |
| **Modul teori** | Modul 8: Data Splitting, Pembuatan Model dan Validasi (Gambar 8.3, Tabel 8.3), Residual dan Uncertainty (Gambar 8.4–8.5) |

**Tujuan sesi** (dari rundown: *Pembangunan model DSM*)
1. Peserta mampu membangun dan memvalidasi model prediksi sifat tanah dari dataset Blok 6.
2. Peserta mampu menghasilkan peta prediksi beserta peta ketidakpastiannya dan menafsirkannya secara kritis.

**Alur**

| Menit | Kegiatan |
|---|---|
| **Sesi 7a (60')** | |
| 0–10 | Pengantar: alur Gambar 8.3 dan pilihan skema pembagian data |
| 10–30 | Membagi data dan membandingkan validasi acak dengan validasi silang spasial |
| 30–50 | Melatih *random forest* dan model pembanding sederhana (regresi linear), lalu menghitung ME, RMSE, dan MEC/R² (Tabel 8.3) |
| 50–60 | **Titik periksa 8:** tabel metrik kedua model; diskusi mengapa hasil validasi acak cenderung lebih optimistis |
| **Sesi 7b (45')** | |
| 0–20 | Prediksi ke seluruh grid, ekspor GeoTIFF, lalu menampilkannya di QGIS bersama peta SMU dari Blok 2 |
| 20–35 | Ketidakpastian: interval prediksi dengan *quantile regression forest* dan peta lebar interval; konsep wilayah keberlakuan model (AOA) cukup diperagakan |
| 35–45 | **Titik periksa 9:** peta prediksi dan peta ketidakpastian; peserta menyiapkan bahan presentasi |

**Keluaran peserta:** peta prediksi sifat tanah, peta ketidakpastian, dan tabel metrik validasi. Ketiganya menjadi bahan presentasi.
**Kebutuhan data:** keluaran Blok 6.
**Catatan:** Nilai metrik yang diperoleh bergantung pada data latihan. Rancangan ini tidak menetapkan target akurasi.

---

## Blok 8 — Presentasi hasil, evaluasi, dan penutupan

| | |
|---|---|
| **Slot** | Hari ke-3, 15.00–16.00, 60 menit |
| **Pemandu** | Ferry bersama tim pemandu |
| **Alat** | Proyektor; berkas peta dari Blok 2 dan Blok 7 |

**Tujuan sesi**
1. Peserta mampu menyajikan alur kerja dan hasilnya, serta menilai keterbatasannya.
2. Penyelenggara memperoleh data evaluasi pelatihan.

**Alur**

| Menit | Kegiatan |
|---|---|
| 0–30 | Presentasi peserta atau kelompok, masing-masing 5–7 menit: data yang dipakai, peta SMU, kovariat terpilih beserta alasannya, peta prediksi dan ketidakpastian, keterbatasan **[perlu konfirmasi: individu atau kelompok, sesuai jumlah peserta]** |
| 30–40 | Tanggapan pemandu dan narasumber |
| 40–50 | Post-test dan formulir evaluasi (lihat `04 Instrumen Evaluasi.md`) |
| 50–60 | Kesan dan pesan, lalu penutupan **[perlu konfirmasi: siapa yang menutup secara resmi]** |

**Keluaran peserta:** presentasi hasil, post-test, dan formulir evaluasi yang sudah diisi.

---

## 3. Daftar konfirmasi

| No. | Hal | Ditanyakan ke | Memengaruhi |
|---:|---|---|---|
| 1 | Tabel laboratorium per titik, DTM LiDAR, dan peta material permukaan Bompon, serta izin membagikannya ke peserta | Nurarfiyah | Blok 1, 2, 6, 7 |
| 2 | Sifat tanah sasaran pemodelan (usulan: fraksi lempung 0–20 cm) | Ferry / Nurarfiyah | Blok 6–7 |
| 3 | Spesifikasi sensor hiperspektral (rentang dan resolusi spektral), format berkas, jumlah unit, kebutuhan sampel, dan pustaka spektral untuk latihan | Pak Pandu | Blok 3, Blok 5 |
| 4 | Skala peta sasaran untuk delineasi SMU | Tim / Prof. Junun | Blok 2 |
| 5 | DTM LiDAR Bompon (yang dipakai untuk `kelas_lereng`) | Nurarfiyah | Blok 1, 2, 6 |
| 6 | Presentasi individu atau kelompok; pihak yang menutup acara | Tim | Blok 8 |
