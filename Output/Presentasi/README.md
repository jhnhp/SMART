# PANDUAN STRUKTUR RANCANGAN SLIDE PRESENTASI (SLIDE DECKS)
## Pelatihan Pemanfaatan Remote Sensing dan Digital Soil Mapping untuk Pertanian Presisi pada Perkebunan Kelapa Sawit
**Pusat Studi Pengelolaan Sumber Daya Lahan (PS2DL), Universitas Gadjah Mada & PT SMART Tbk**

Dokumen Acuan Sumber: `Modul Pelatihan SMART Pemanfaatan RS dan DSM.docx` (Modul 1 s.d. Modul 8)

---

## 1. DAFTAR PEMATERI DAN SLIDE DECK

| No | Berkas Presentasi PPTX | Naskah Markdown | Modul Terkait | Topik Utama | Pemateri / Narasumber | Jumlah Slide |
|:---:|:---|:---|:---:|:---|:---|:---:|
| 1 | [`PPT_01_Prof_Junun_Bagian_1-3.pptx`](PPT_01_Prof_Junun_Bagian_1-3.pptx) | [`PPT_01_...md`](PPT_01_Prof_Junun_Bagian_1-3.md) | Modul 1, 2, 3 | Dasar-dasar Remote Sensing, Multi-source Data Fusion, dan Delineasi Soil Mapping Units (SMU) | **Prof. Dr. rer. nat. Junun Sartohadi, M.Sc.** | 22 Slide |
| 2 | [`PPT_02_Dr_Anggri_Bagian_4_dan_6.pptx`](PPT_02_Dr_Anggri_Bagian_4_dan_6.pptx) | [`PPT_02_...md`](PPT_02_Dr_Anggri_Bagian_4_dan_6.md) | Modul 4 & 6 | Remote Sensing untuk Estimasi Soil Properties & Interpretasi Pedologis dari Data Remote Sensing | **Dr. rer. nat. Muhammad Anggri Setiawan, S.Si., M.Si.** | 22 Slide |
| 3 | [`PPT_03_Dr_Retnadi_Bagian_5.pptx`](PPT_03_Dr_Retnadi_Bagian_5.pptx) | [`PPT_03_...md`](PPT_03_Dr_Retnadi_Bagian_5.md) | Modul 5 | Bare Soil Detection & Information Extraction | **Dr. Retnadi Heru Jatmiko, M.Sc.** | 15 Slide |
| 4 | [`PPT_04_Pak_Pandu_Bagian_7.pptx`](PPT_04_Pak_Pandu_Bagian_7.pptx) | [`PPT_04_...md`](PPT_04_Pak_Pandu_Bagian_7.md) | Modul 7 | Proximal Soil Sensing (PSS) & Karakterisasi Sifat Tanah Cepat | **Pandu Yudha Adi Putra Wirabuana, S.Hut., M.Sc., Ph.D.** | 16 Slide |
| 5 | [`PPT_05_Dr_Guruh_Bagian_8.pptx`](PPT_05_Dr_Guruh_Bagian_8.pptx) | [`PPT_05_...md`](PPT_05_Dr_Guruh_Bagian_8.md) | Modul 8 | Pemodelan Digital Soil Mapping (DSM), Machine Learning, & Evaluasi Ketidakpastian | **Dr. Eng. Guruh Samodra, S.Si., M.Sc.** | 20 Slide |
| **Total** | **5 File PPTX Siap Pakai** | **5 Naskah MD** | | **Kurikulum Lengkap 8 Modul Pelatihan** | **5 Narasumber Ahli UGM** | **95 Slide** |

---

## 2. ANATOMI SETIAP RANCANGAN SLIDE

Setiap slide di dalam berkas Markdown dirancang dengan standar profesional universitas dan industri agronomi:
1. **Nomor & Judul Slide:** Judul tegas, lugas, dan mencerminkan esensi gagasan.
2. **Kategori Materi:** Memudahkan pelacakan tahapan (Teori Dasar, Metodologi, Pembuktian Matematis, Kasus Lapangan, Evaluasi).
3. **Layout & Panduan Visual (*Visual Blueprint*):** Panduan eksplisit tata letak grafis 2-kolom, matriks, atau panel perbandingan, merujuk langsung ke nomor Gambar dan Tabel di dalam dokumen master Word/PDF.
4. **Poin Paparan (*Key Content*):** Butir-butir materi ilmiah padat, mencantumkan definisi, rumus matematika, batasan data, dan parameter spesifik perkebunan kelapa sawit.
5. **Catatan Pemateri (*Speaker Notes / Narasi Lisan*):** Narasi lisan langsung yang siap dibacakan atau diimprovisasi oleh pemateri, dilengkapi analogi kontekstual, penekanan poin krusial, dan jembatan antarslide.

---

## 3. PEMBUATAN FILE PPTX DENGAN TEMPLATE RESMI UGM

Seluruh 5 berkas PowerPoint (`.pptx`) dibangun secara otomatis menggunakan skrip Python [`Output/scripts/buat_pptx_ugm.py`](../scripts/buat_pptx_ugm.py) dengan memanfaatkan template resmi universitas:
`Source/(NEW) Template Presentasi UGM Opt-1 (Wide Size)_2026.pptx` (Format 16:9 Widescreen).

### Fitur Otomasi PPTX:
1. **Master & Identitas UGM:**
   - Mempertahankan Slide Cover resmi UGM dengan judul kuning khas Gama-Sans (`#FDD402`), subjudul putih, identitas pemateri, logo UGM, dan footer resmi `ugm.ac.id`.
   - Menggunakan master slide *Title and Content* (Layout 1) yang secara otomatis menampilkan logo UGM di sudut kanan atas dan footer identitas.
2. **Tata Letak Adaptif (2-Kolom & 1-Kolom Lebar):**
   - **Slide dengan Gambar:** Kolom kiri untuk butir paparan berhirarki rapi; kolom kanan untuk gambar diagram resolusi tinggi yang diskalakan proporsional sesuai rasio aspek aslinya dilengkapi takarir (*caption*) miring di bawahnya.
   - **Slide Tanpa Gambar:** Jika butir paparan $\ge 5$, otomatis dibagi menjadi 2 kolom teks seimbang agar tidak padat vertikal; jika $< 5$, ditampilkan dalam satu kolom lebar (*data-dense clean*).
3. **Penyisipan Catatan Pemateri (*Speaker Notes*):**
   - Seluruh 95 narasi lisan disuntikkan langsung ke dalam fitur *Notes* bawaan PowerPoint (`slide.notes_slide`), sehingga pemateri dapat langsung membacanya saat menggunakan mode *Presenter View*.
4. **Perintah Menjalankan Skrip:**
   ```bash
   python3 Output/scripts/buat_pptx_ugm.py
   ```

---

## 4. INTEGRASI ASET GAMBAR DAN DIAGRAM

Seluruh naskah slide deck telah dilengkapi sintaks gambar Markdown (`![Caption](../assets/...)`) dengan total **47 referensi gambar** yang terhubung langsung ke aset resolusi tinggi di folder `Output/assets/`:

1. **`PPT_01` (Prof. Junun):** 18 gambar
   - Gambar 1.6: Siklus Pertanian Presisi (`modul-1/M1-G06_...`)
   - Gambar 1.1: Alur Sistem RS (`modul-1/M1-G01_...`)
   - Gambar 1.7: Keseimbangan Fluks Energi (`modul-1/M1-G07_...`)
   - Gambar 1.2: Sensor Pasif vs Aktif (`modul-1/M1-G02_...`)
   - Gambar 1.3 & 1.4: Spektrum EM & Respons Spektral 5 Objek (`modul-1/M1-G03_...`, `M1-G04_...`)
   - 4 Dimensi Resolusi Citra (`modul-1/M1-T01a` s.d. `M1-T01d`)
   - Gambar 1.5: Konsep SCORPAN (`modul-1/M1-G05_...`)
   - Gambar 2.1: Tiga Tingkat Fusi Data (`modul-2/M2-G01_...`)
   - Kovariat SCORPAN Multi-sumber (`modul-8/M8-G01_...`)
   - Gambar 3.2: Hierarki Taksonomi Tanah (`modul-3/M3-G02_...`)
   - Gambar 3.1: Empat Kategori Satuan Peta Tanah (`modul-3/M3-G01_...`)
   - Gambar 3.3: Model Sembilan Satuan Lahan / Catena (`modul-3/M3-G03_...`)
   - Gambar 3.4: Minimum Legible Area pada Berbagai Skala (`modul-3/M3-G04_...`)
   - Gambar 3.5: Komparasi Tumpang Susun Otomatis vs Delineasi Pedologis (`modul-3/M3-G05_...`)

2. **`PPT_02` (Dr. Anggri):** 10 gambar
   - Gambar 4.1: Jalur Estimasi Sifat Tanah Langsung vs Tidak Langsung (`modul-4/M4-G01_...`)
   - Gambar 4.2: Kurva Serapan Spektrum Tanah & Kanal Sentinel-2 MSI (`modul-4/M4-G02_...`)
   - Gambar 4.3: Enam Faktor Sinyal Tanah & Kedalaman Terwakili (`modul-4/M4-G03_...`)
   - Gambar 6.1: Pola Aliran Permukaan & Pengontrol Litologi (`modul-6/M6-G01_...`)
   - Gambar 6.2: Tekstur Citra & Simpangan Baku Lokal 3x3 dan 15x15 (`modul-6/M6-G02_...`)
   - Gambar 6.3: Pohon Keputusan Kunci Interpretasi Bertingkat (`modul-6/M6-G03_...`)
   - Gambar 6.4: Konvergensi Batas Analisis Unsur (`modul-6/M6-G04_...`)
   - Gambar 6.5: Komparasi Kasus Kebun Berbukit (Piksel vs OBIA vs Pedologis Ahli) (`modul-6/M6-G05_...`)

3. **`PPT_03` (Dr. Retnadi):** 5 gambar
   - Gambar 5.1: Spektrum Tanah, Vegetasi, Serasah & Dinamika Campuran Sub-piksel (`modul-5/M5-G01_...`)
   - Gambar 5.2: Garis Tanah (*Soil Line*) pada Ruang Spektral Merah-NIR (`modul-5/M5-G02_...`)
   - Gambar 5.3: Deret Waktu Indeks Spektral pada Blok Replanting Kelapa Sawit (`modul-5/M5-G03_...`)
   - Gambar 5.4: Alur Kerja Baku Pembuatan Komposit Tanah Terbuka GEOBAT (`modul-5/M5-G04_...`)

4. **`PPT_04` (Pak Pandu):** 5 gambar
   - Gambar 7.1: Taksonomi Ragam Sensor PSS pada Spektrum Elektromagnetik (`modul-7/M7-G01_...`)
   - Gambar 7.2: Kedalaman Informasi Berbagai Teknik Penginderaan Tanah (`modul-7/M7-G02_...`)
   - Gambar 7.3: Empat Langkah Praolah Sinyal Spektroskopi Tanah (`modul-7/M7-G03_...`)
   - Gambar 7.4: Alur Pemodelan Spektroskopi Tanah & Kemometrika (`modul-7/M7-G04_...`)
   - Gambar 7.5: Arsitektur Instrumen Spektrometer Lapangan Mandiri (`modul-7/M7-G05_...`)

5. **`PPT_05` (Dr. Guruh):** 9 gambar
   - Gambar 8.1: Kovariat SCORPAN sebagai Lapisan Raster Spasial (`modul-8/M8-G01_...`)
   - Gambar 8.2: Skema Pembagian Data Acak vs Spatial Block Cross-Validation (`modul-8/M8-G02_...`)
   - Gambar 8.3: Diagram Alir Lengkap Pemodelan Digital Soil Mapping (`modul-8/M8-G03_...`)
   - Gambar 8.4: Dekomposisi Tren & Semivariogram Residual Regression Kriging (`modul-8/M8-G04_...`)
   - Gambar 8.5: Evaluasi Interval Prediksi PICP & Peta Area of Applicability (`modul-8/M8-G05_...`)
   - Gambar 8.6: Harmonisasi Kedalaman Tanah dengan Equal-Area Spline & GlobalSoilMap (`modul-8/M8-G06_...`)

*Catatan Tambahan:* Tiga gambar baru (`M1-G07`, `M7-G05`, `M8-G06`) diproduksi menggunakan skrip Python [`Output/scripts/gambar_tambahan_presentasi.py`](../scripts/gambar_tambahan_presentasi.py) yang taat pada sistem desain dan palet warna bersama [`Output/scripts/gaya.py`](../scripts/gaya.py).
