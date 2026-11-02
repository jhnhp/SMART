# RANCANGAN PRESENTASI (SLIDE DECK) PELATIHAN
## Bagian 1, 2, dan 3: Dasar-dasar Remote Sensing, Multi-source Data Fusion, dan Delineasi Soil Mapping Units (SMU)

**Pemateri:** Prof. Dr. rer. nat. Junun Sartohadi, M.Sc.  
**Institusi:** Pusat Studi Pengelolaan Sumber Daya Lahan (PS2DL), Universitas Gadjah Mada  
**Target Audiens:** Staf Teknis, Agronomis, Peneliti, dan Pengelola Perkebunan Kelapa Sawit (PT SMART Tbk)  
**Alokasi Waktu:** Sesi Ceramah Teori (60–90 Menit)  
**Dokumen Acuan:** `Modul Pelatihan SMART Pemanfaatan RS dan DSM.docx` (Bab 1, Bab 2, dan Bab 3)

---

### PANDUAN VISUAL & IDENTITAS SLIDE (DESIGN SYSTEM)
* **Warna Utama:** Biru Navy UGM (`#1F3A5F`), Hijau Daun Sawit (`#2A9D8F`), Kuning/Oranye Tanah (`#D9A35F` / `#E07B39`), Latar Putih Bersih (`#FFFFFF`).
* **Tipografi:** Sans-serif tegas (Calibri / Carlito / Arial), hierarki judul besar (32–36 pt), subjudul (20–24 pt), teks isi (14–16 pt).
* **Prinsip Tampilan:** *Data-dense yet clean*, 2 kolom visual-teks, diagram skematis ilmiah, hindari bullet point kosong tanpa bobot konseptual.

---

## DAFTAR SLIDE & STRUKTUR MATERI

```
BAGIAN 1: PENGANTAR REMOTE SENSING & DIGITAL SOIL MAPPING (Slide 1–8)
  - Slide 1: Judul & Pembuka Sesi
  - Slide 2: Latar Belakang & Urgensi Pemetaan Tanah Modern pada Kelapa Sawit
  - Slide 3: Konsep Dasar dan 4 Komponen Sistem Penginderaan Jauh
  - Slide 4: Interaksi Energi Elektromagnetik dengan Objek di Bumi
  - Slide 5: Sistem Sensor Pasif vs. Sensor Aktif
  - Slide 6: Spektrum Elektromagnetik dan Pola Respons Spektral Permukaan
  - Slide 7: Empat Dimensi Resolusi Citra Satelit
  - Slide 8: Dari Paradigma Konvensional (Jenny) Menuju SCORPAN (DSM)

BAGIAN 2: MULTI-SOURCE DATA FUSION (Slide 9–14)
  - Slide 9: Mengapa Multi-source Data Fusion?
  - Slide 10: Karakteristik 5 Pilar Sumber Data Geospasial
  - Slide 11: Konsep & Tiga Tingkatan Fusi Data (Piksel, Fitur, Keputusan)
  - Slide 12: Fusi Tingkat Fitur sebagai Tulang Punggung DSM
  - Slide 13: Prinsip Penyelarasan Data Geospatial Multi-sumber
  - Slide 14: Praktik Standarisasi Grid & Kontrol Mutu Data Lingkungan

BAGIAN 3: DELINEASI SOIL MAPPING UNITS (SMU) (Slide 15–22)
  - Slide 15: Konsep Pemetaan Tanah: Metode Analitik vs. Metode Sintetik
  - Slide 16: Memahami Soil Mapping Unit (SMU) vs. Satuan Taksonomi
  - Slide 17: Empat Kategori Satuan Peta Tanah (Konsosiasi, Asosiasi, Kompleks, Kelompok Tak Dibedakan)
  - Slide 18: Konsep Inklusi Tanah dan Batas Kemurnian Satuan Peta
  - Slide 19: Prinsip Delineasi Berbasis Bentanglahan & Konsep Catena
  - Slide 20: Skala Pemetaan, MLD (Minimum Legible Delineation), dan MLA
  - Slide 21: Jebakan Tumpang Susun Otomatis vs. Keunggulan Delineasi Visual-Pedologis
  - Slide 22: Rangkuman & Jembatan ke Estimasi Sifat Tanah dan Interpretasi Lanjutan
```

---

## RINCIAN KONTEN PER SLIDE

---

### SLIDE 1: JUDUL & PEMBUKA
* **Kategori:** Cover Presentation
* **Judul Utama:** Dasar-dasar Remote Sensing, Multi-source Data Fusion, dan Delineasi Soil Mapping Units (SMU)
* **Sub-judul:** Fondasi Geospasial dan Pedologis untuk Pertanian Presisi pada Perkebunan Kelapa Sawit
* **Identitas:** Prof. Dr. rer. nat. Junun Sartohadi, M.Sc. | Pusat Studi Pengelolaan Sumber Daya Lahan (PS2DL) UGM
* **Layout Visual:**
  * Kiri: Judul presentasi tebal, identitas pemateri, logo UGM & PS2DL.
  * Kanan: Tampilan visual montase foto udara resolusi tinggi perkebunan berdampingan dengan ilustrasi kurva spektral dan peta delineasi poligon tanah.
* **Poin Paparan:**
  * Membangun pemahaman komprehensif dari fisika penginderaan jauh hingga batas satuan peta tanah operasional.
  * Menghubungkan teori bentanglahan klasik dengan teknologi pemetaan digital modern.
* **Catatan Pemateri (Speaker Notes):**
  > "Selamat pagi Bapak dan Ibu sekalian. Dalam 90 menit ke depan, kita akan meletakkan fondasi ilmiah paling fundamental dalam pelatihan ini. Kita tidak bisa langsung melompat ke machine learning atau pemodelan statistik tanah tanpa memahami hakikat fisik dari sinyal yang ditangkap sensor di antariksa, bagaimana memadukan berbagai sumber sensor, serta bagaimana satuan tanah terbentuk secara alami di bentanglahan perkebunan kita."

---

### SLIDE 2: URGENSI PADA PERKEBUNAN KELAPA SAWIT
* **Kategori:** Konteks Aplikasi & Latar Belakang
* **Judul:** Tantangan Pengelolaan Lahan Sawit & Kebutuhan Pertanian Presisi
* **Layout Visual:** 3 Kartu Masalah → 1 Solusi Terpadu didukung alur siklus presisi:
  * Kartu 1: Keterbatasan ekspansi lahan baru & dominasi tanaman tua/peremajaan.
  * Kartu 2: Keragaman spasial sifat tanah (drainase buruk, pirit, defisiensi hara spesifik).
  * Kartu 3: Tingginya biaya & lambatnya survei tanah konvensional ribuan hektar.
  * Visual Diagram:
    ![Gambar 1.6: Siklus Pertanian Presisi](../assets/modul-1/M1-G06_siklus-pertanian-presisi.png)
    *Gambar 1.6: Siklus Informasi Pertanian Presisi (Pengumpulan Data → Karakterisasi Variabilitas → Delineasi Zona Manajemen → Aplikasi Pupuk Spesifik Lokasi).*
* **Poin Paparan:**
  * Pertanian presisi (*site-specific crop management*) bertujuan memaksimalkan efisiensi hara, TBS, dan keberlanjutan ekosistem perkebunan.
  * Survei konvensional bor tanah memerlukan biaya luar biasa dan tenaga besar, sering kali menghasilkan batas kualitatif yang sulit diperbarui.
  * Integrasi Remote Sensing (RS) dan Digital Soil Mapping (DSM) hadir sebagai solusi kuantitatif, terukur, dan dapat diperbarui (*updatable*).
* **Catatan Pemateri:**
  > "Bapak dan Ibu yang mengelola estate sawit tentu merasakan: satu afdeling atau bahkan satu blok sawit tidak pernah homogen. Ada bagian rendahan yang sering tergenang, ada punggungan yang erosi dan kering. Memperlakukan seluruh blok dengan dosis pupuk yang sama rata adalah inefisiensi biaya. Di sinilah RS dan DSM bekerja menyediakan informasi spesifik lokasi."

---

### SLIDE 3: KONSEP DASAR SISTEM PENGINDERAAN JAUH
* **Kategori:** Teori Fisika Penginderaan Jauh
* **Judul:** Hakikat Penginderaan Jauh: Merekam Energi, Bukan Objek
* **Layout Visual:**
  * Diagram alur proses penginderaan jauh:
    ![Gambar 1.1: Alur Sistem Penginderaan Jauh](../assets/modul-1/M1-G01_alur-penginderaan-jauh.png)
    *Gambar 1.1: Komponen dan Alur Proses Sistem Penginderaan Jauh (Sumber Energi Alami/Buatan, Penetrasi Atmosfer, Interaksi Objek Permukaan, Sensor Satelit, dan Stasiun Bumi).*
  * Rincian 4 Komponen Kunci di sisi kanan.
* **Poin Paparan:**
  * **Definisi Ilmiah:** Ilmu, seni, dan teknologi memperoleh informasi objek tanpa kontak fisik langsung melalui perekaman energi elektromagnetik (Lillesand & Kiefer 1990; Sutanto 1994).
  * **4 Komponen Utama Sistem:**
    1. **Sumber Energi:** Alami (matahari, termal bumi) atau buatan (pulsa microwave/laser).
    2. **Atmosfer:** Medium perambat yang menyerap (*absorption*) dan menghamburkan (*scattering*) radiasi.
    3. **Objek Permukaan:** Mengubah sifat gelombang berdasarkan karakteristik fisik-kimia.
    4. **Sensor:** Alat perekam sinyal radiasi dan pengubah nilai digital (*Digital Number* / Reflektansi).
* **Catatan Pemateri:**
  > "Prinsip pertama yang wajib diingat: satelit di luar angkasa tidak pernah memotret 'kesuburan tanah' atau 'kadar lempung' secara kasat mata. Satelit hanya merekam foton energi yang dipantulkan atau dipancarkan. Tugas kitalah yang menerjemahkan variasi pantulan energi tersebut menjadi informasi tanah."

---

### SLIDE 4: HUKUM KEKEKALAN ENERGI DI PERMUKAAN BUMI
* **Kategori:** Interaksi Fisika Gelombang
* **Judul:** Interaksi Energi Elektromagnetik dengan Permukaan Lahan
* **Layout Visual:**
  * Diagram Interaksi Energi dan Keseimbangan Fluks:
    ![Gambar 1.7: Keseimbangan Energi Elektromagnetik di Permukaan Bumi](../assets/modul-1/M1-G07_keseimbangan-energi.png)
    *Gambar 1.7: Interaksi Radiasi Elektromagnetik dengan Daun/Kanopi, Permukaan Tanah, dan Air Permukaan ($E_I = E_R + E_A + E_T$).*
* **Poin Paparan:**
  * **Persamaan Keseimbangan Energi (Danoedoro 2012):**
    $$E_I(\lambda) = E_R(\lambda) + E_A(\lambda) + E_T(\lambda)$$
    * $E_I$: Energi datang (*Incident*)
    * $E_R$: Energi dipantulkan (*Reflected*)
    * $E_A$: Energi diserap (*Absorbed*)
    * $E_T$: Energi diteruskan (*Transmitted*)
  * **Reflektansi Spektral ($\rho_\lambda$):** Rasio $E_R(\lambda) / E_I(\lambda)$ pada panjang gelombang tertentu.
  * Pada sistem pasif optik, nilai reflektansi inilah yang menjadi tanda spektral (*spectral signature*) diagnostik pembeda objek.
* **Catatan Pemateri:**
  > "Jika energi mengenai permukaan tanah, sebagian dipantulkan, sebagian diserap menjadi panas, dan sebagian kecil diteruskan ke lapisan bawah. Komponen pantulan $E_R$ inilah yang ditangkap sensor optik satelit seperti Sentinel-2 atau Landsat."

---

### SLIDE 5: SENSOR PASIF VS SENSOR AKTIF
* **Kategori:** Klasifikasi Sensor
* **Judul:** Membedakan Sistem Perekaman: Sensor Pasif vs. Sensor Aktif
* **Layout Visual:** 2 Kolom Komparasi Berdampingan didukung ilustrasi sensor pasif vs aktif:
  ![Gambar 1.2: Sistem Sensor Pasif dan Sensor Aktif](../assets/modul-1/M1-G02_sensor-pasif-aktif.png)
  *Gambar 1.2: Perbedaan Fundamental Mekanisme Perekaman Sensor Pasif (Matahari) dan Sensor Aktif (Radar/LiDAR) (Diadaptasi dari Syah, 2010).*
  * Kolom Kiri: Sensor Pasif (Matahari sebagai sumber, optik/termal, terhalang awan).
  * Kolom Kanan: Sensor Aktif (Sensor memancarkan sinyal gelombang mikro/laser sendiri, menembus awan/malam).
* **Poin Paparan:**
  * **Sensor Pasif:**
    * Mengandalkan radiasi matahari (optik $0.4–2.5\ \mu\text{m}$) atau emisi termal ($8–14\ \mu\text{m}$).
    * Contoh: Sentinel-2 MSI, Landsat-8/9 OLI, MODIS, PlanetScope.
    * Keunggulan: Informasi spektral sangat kaya untuk vegetasi dan tanah.
    * Keterbatasan: Buta saat malam hari dan mutlak terhalang awan tropis tebal.
  * **Sensor Aktif:**
    * Memancarkan pulsa sendiri dan merekam hamburan balik (*backscatter*).
    * Contoh: RADAR SAR (Sentinel-1 C-band, ALOS PALSAR L-band) & LiDAR.
    * Keunggulan: *All-weather capability* (menembus awan/hujan), dapat merekam malam hari, peka struktur dan dielektrik/kelembapan.
* **Catatan Pemateri:**
  > "Di wilayah perkebunan kelapa sawit di Sumatra, Kalimantan, atau Riau, tutupan awan adalah musuh utama sensor optik. Oleh karena itu, kita tidak bisa hanya bergantung pada citra optik; kita wajib memahami dan memadukannya dengan sensor aktif radar dan LiDAR."

---

### SLIDE 6: SPEKTRUM EM & TANDA SPEKTRAL OBJEK
* **Kategori:** Spektroskopi Lingkungan
* **Judul:** Spektrum Elektromagnetik & Pola Respons Spektral
* **Layout Visual:** Dua panel berdampingan:
  * Panel 1: Spektrum Elektromagnetik dan Jendela Transmisi Atmosfer:
    ![Gambar 1.3: Spektrum Elektromagnetik dan Jendela Transmisi Atmosfer](../assets/modul-1/M1-G03_spektrum-elektromagnetik.png)
    *Gambar 1.3: Spektrum Gelombang Elektromagnetik dan Jendela Transmisi Atmosfer.*
  * Panel 2: Kurva Respons Spektral 5 Objek Permukaan Bumi:
    ![Gambar 1.4: Pola Respons Spektral Objek Permukaan Bumi](../assets/modul-1/M1-G04_pola-respons-spektral.png)
    *Gambar 1.4: Kurva Pantulan Spektral Vegetasi Sehat, Tanah Kering, Tanah Lembap, Air Jernih, dan Air Keruh.*
* **Poin Paparan:**
  * **Jendela Atmosfer (*Atmospheric Windows*):** Wilayah panjang gelombang yang lolos serapan uap air ($H_2O$), $CO_2$, dan ozon ($O_3$)—tempat sensor satelit bekerja.
  * **Karakteristik Tanda Spektral Kunci:**
    1. **Vegetasi Hijau:** Serapan klorofil di kanal Merah ($0.66\ \mu\text{m}$), lonjakan tajam pada *Red Edge* ke NIR ($0.7–0.9\ \mu\text{m}$) akibat struktur mesofil daun, dan serapan air pada $1.4\ \mu\text{m}$ dan $1.9\ \mu\text{m}$.
    2. **Tanah Kering:** Pantulan meningkat bertahap dari Tampak ke SWIR tanpa lonjakan tajam.
    3. **Tanah Lembap:** Pola kurva sama dengan tanah kering tetapi seluruh tingkat pantulan tertekan ke bawah karena air menyerap radiasi secara kuat.
    4. **Air Jernih:** Menyerap hampir 100% energi pada panjang gelombang inframerah.
* **Catatan Pemateri:**
  > "Perhatikan Gambar 1.4: kurva tanah basah berada persis di bawah kurva tanah kering. Ketika tanah basah kuyup terkena air hujan, ia tampak jauh lebih gelap. Mengapa? Karena air mengisi pori-pori tanah dan menyerap foton cahaya. Perbedaan kontras ini menjadi dasar estimasi kelembapan tanah."

---

### SLIDE 7: EMPAT DIMENSI RESOLUSI CITRA SATELIT
* **Kategori:** Karakteristik Data Satelit
* **Judul:** Memilih Data Sesuai Kebutuhan: Empat Resolusi Citra
* **Layout Visual:** Matriks 4 Kuadran Dimensi Resolusi Citra:
  | Resolusi Spasial | Resolusi Spektral |
  | :---: | :---: |
  | ![Resolusi Spasial](../assets/modul-1/M1-T01a_resolusi-spasial.png) | ![Resolusi Spektral](../assets/modul-1/M1-T01b_resolusi-spektral.png) |
  | **Resolusi Radiometrik** | **Resolusi Temporal** |
  | ![Resolusi Radiometrik](../assets/modul-1/M1-T01c_resolusi-radiometrik.png) | ![Resolusi Temporal](../assets/modul-1/M1-T01d_resolusi-temporal.png) |
  *Gambar 1.5 (Tabel 1.1): Empat Dimensi Resolusi Citra Penginderaan Jauh (Spasial, Spektral, Radiometrik, Temporal).*
* **Poin Paparan:**
  * **1. Resolusi Spasial:** Ukuran piksel terkecil di permukaan bumi.
    * *Sentinel-2 (10–20 m)* vs *Landsat (30 m)* vs *Drone/Pleiades (< 1 m)*.
    * Relevansi: Menentukan skala terkecil unit yang dapat dibedakan (misal pohon sawit individual vs blok kebun).
  * **2. Resolusi Spektral:** Jumlah, lebar, dan posisi saluran/kanal radiasi.
    * Semakin banyak saluran sempit, semakin spesifik identifikasi mineral dan pigmen.
  * **3. Resolusi Radiometrik:** Kepekaan sensor mencatat variasi energi (kedalaman bit).
    * 8-bit (256 level) vs 12-bit (4.096 level pada Sentinel-2/Landsat-8). Membedakan gradasi halus bayangan.
  * **4. Resolusi Temporal:** Interval siklus perekaman ulang di lokasi yang sama.
    * Sentinel-2 (5 hari dengan konstelasi 2A/2B), Landsat (16 hari). Kritis untuk deret waktu dering iklim.
* **Catatan Pemateri:**
  > "Dalam memilih data untuk perkebunan, selalu ada kompromi (*trade-off*). Citra drone resolusi spasial 5 cm sangat tajam, tetapi cakupan luasannya terbatas dan biaya operasionalnya tinggi. Citra Sentinel-2 beresolusi 10 meter, gratis setiap 5 hari, sangat ideal untuk monitoring skala lanskap estate."

---

### SLIDE 8: DARI JENNY (CLORPT) MENUJU SCORPAN
* **Kategori:** Transisi Teori Pedologi ke Digital
* **Judul:** Paradigma Pemetaan Tanah: Dari Faktor Pembentuk ke SCORPAN
* **Layout Visual:**
  * Diagram Paradigma SCORPAN:
    ![Gambar 1.5: Konsep SCORPAN dalam Digital Soil Mapping](../assets/modul-1/M1-G05_konsep-scorpan.png)
    *Gambar 1.5: Transisi Paradigma Pemetaan Tanah dari Hans Jenny (1941) ke Formula Empiris SCORPAN (McBratney et al., 2003).*
  * Bawah: Tabel ringkas komparasi Konvensional vs. DSM (Tabel 1.2 Modul).
* **Poin Paparan:**
  * **Formula Hans Jenny (1941):** Tanah adalah fungsi dari *Climate* ($cl$), *Organisms* ($o$), *Relief* ($r$), *Parent material* ($p$), dan *Time* ($t$). Konsep ini bersifat kualitatif dan penarikan batas mengandalkan intuisi *tacit knowledge* surveyor (Hudson 1992).
  * **Revolusi DSM - Model SCORPAN (McBratney et al. 2003):**
    $$S = f(s, c, o, r, p, a, n) + \varepsilon$$
    * $s$ = sifat tanah yang diketahui terdahulu, $c$ = iklim, $o$ = organisme/vegetasi, $r$ = topografi/relief, $p$ = bahan induk, $a$ = umur permukaan, $n$ = posisi spasial, $\varepsilon$ = galat residual.
  * DSM mengubah pengetahuan tanah tersirat menjadi model empiris-kuantitatif yang dapat diuji ketelitiannya dan diulang (*reproducible*).
* **Catatan Pemateri:**
  > "Hans Jenny memberi kita cara berpikir tentang bagaimana tanah terbentuk. McBratney dan rekan-rekan mengubah cara berpikir tersebut menjadi persamaan matematika spasial. Tujuh huruf SCORPAN adalah kunci utama seluruh modul pelatihan ini!"

---

### SLIDE 9: MENGAPA MULTI-SOURCE DATA FUSION?
* **Kategori:** Pengantar Bagian 2 - Data Fusion
* **Judul:** Kompleksitas Bentanglahan & Kebutuhan Fusi Multi-sumber
* **Layout Visual:**
  * Diagram masalah 'Single Sensor Blind Spot':
    * Sensor Optik terhalang awan dan kanopi rapat.
    * Sensor Radar terganggu *speckle* dan distorsi lereng.
    * DEM radar mencampur elevasi tajuk dengan elevasi tanah.
  * Kesimpulan visual: Penggabungan data multisensor untuk merepresentasikan seluruh faktor SCORPAN secara komplementer.
* **Poin Paparan:**
  * Tidak ada satupun sensor tunggal yang mampu merekam seluruh faktor pembentuk tanah sekaligus.
  * Fusi data (*data fusion*) menggabungkan kekuatan sinergis dari sensor yang berbeda karakteristik resolusi, spektral, dan fisik perekamannya (Zhang 2010).
  * Menghasilkan dataset komprehensif untuk mendeskripsikan kondisi lahan perkebunan tropis yang kompleks.
* **Catatan Pemateri:**
  > "Kita masuk ke Bagian 2. Sering muncul pertanyaan: 'Pak, apakah cukup memakai citra Sentinel-2 saja untuk memetakan tanah sawit?' Jawabannya: tidak pernah cukup. Sawit yang rimbun menutupi tanah dari citra optik. Kita butuh radar untuk kelembapan, butuh DEM untuk arah aliran air, dan butuh peta geologi untuk bahan induk."

---

### SLIDE 10: LIMA PILAR SUMBER DATA GEOSPASIAL
* **Kategori:** Taksonomi Data Geospasial
* **Judul:** Karakteristik Sumber Data untuk Multi-source Data Fusion
* **Layout Visual:** Tabel Komparasi Elegan 5 Pilar Data (didasarkan pada Tabel 2.1 Modul).
* **Poin Paparan:**
  1. **Citra Optik (Sentinel-2, Landsat):** Merekam spektrum pantulan $0.4–2.5\ \mu\text{m}$. Menghasilkan indeks vegetasi (NDVI), indeks tanah (BSI). Keterbatasan: terhalang awan/kanopi.
  2. **Radar SAR (Sentinel-1 C-band, PALSAR L-band):** Mengukur hamburan balik gelombang mikro. Peka kekasaran, struktur tanaman, dan kelembapan. Bebas awan. Keterbatasan: derau *speckle* dan distorsi geometris lereng (*layover/foreshortening*).
  3. **LiDAR:** Pulsa laser aktif dengan kemampuan *multiple returns*. Mampu menembus sela kanopi untuk merekam tanah asli (menghasilkan DTM murni dan Tinggi Kanopi / CHM).
  4. **DEM / Elevasi (DEMNAS, SRTM):** Grid ketinggian. Menurunkan parameter medan: kelerengan, kelengkungan, akumulasi aliran, dan *Topographic Wetness Index* (TWI).
  5. **Data Lingkungan:** Data iklim/curah hujan (CHIRPS/stasiun kebun), peta geologi/bahan induk, dan peta tanah eksisting.
* **Catatan Pemateri:**
  > "Perhatikan perbedaan antara DSM (Digital Surface Model) dan DTM (Digital Terrain Model). Radar SRTM sering kali merekam puncak tajuk sawit sebagai elevasi, padahal yang kita cari untuk hidrologi tanah adalah tanah di bawah pohon (DTM). Di sinilah peran LiDAR atau koreksi DEM menjadi sangat penting."

---

### SLIDE 11: TIGA TINGKATAN FUSI DATA
* **Kategori:** Arsitektur Fusi Data
* **Judul:** Konsep dan Tingkatan Fusi Data Geospasial
* **Layout Visual:** Diagram Alir 3 Tingkatan Fusi:
  ![Gambar 2.1: Tiga Tingkat Fusi Data Geospasial](../assets/modul-2/M2-G01_tingkat-fusi-data.png)
  *Gambar 2.1: Tiga Tingkatan Fusi Data Geospasial: Piksel, Fitur, dan Keputusan (Diadaptasi dari Pohl & van Genderen, 1998).*
  * Tingkat 1: Fusi Piksel (Citra A + Citra B → Citra Gabungan Baru)
  * Tingkat 2: Fusi Fitur (Ekstraksi Fitur A + Ekstraksi Fitur B → Matriks Fitur / Tumpukan Kovariat)
  * Tingkat 3: Fusi Keputusan (Prediksi Model A + Prediksi Model B → Klasifikasi Akhir via Voting/Ensemble)
* **Poin Paparan:**
  * **1. Fusi Tingkat Piksel (*Pixel Level*):**
    * Integrasi langsung nilai digital sebelum ekstraksi informasi. Contoh: *Pan-sharpening* (menggabungkan kanal pankromatik resolusi tinggi dengan multispektral) atau deteksi perubahan multitemporal.
  * **2. Fusi Tingkat Fitur (*Feature Level*):**
    * Parameter atau indeks diekstraksi terlebih dahulu dari masing-masing sensor (NDVI dari optik, VV/VH dari SAR, Kelerengan dari DEM), lalu digabungkan menjadi multi-layer stack. Ini adalah tingkatan fusi utama dalam DSM.
  * **3. Fusi Tingkat Keputusan (*Decision Level*):**
    * Penggabungan hasil klasifikasi/estimasi dari beberapa model independen menggunakan aturan konsensus (*majority voting*, *fuzzy logic*).
* **Catatan Pemateri:**
  > "Ketika kita menyusun 20 kovariat di QGIS atau Python untuk memprediksi tanah, tingkat fusi mana yang sedang kita lakukan? Kita sedang melakukan fusi tingkat fitur (*feature level*). Kita mengekstrak NDVI dari satelit optik, slope dari DEM, dan backscatter dari SAR, lalu menumpuknya menjadi prediktor."

---

### SLIDE 12: IMPLEMENTASI FUSI TINGKAT FITUR PADA DSM
* **Kategori:** Arsitektur Variabel Lingkungan
* **Judul:** Menghubungkan Fusi Tingkat Fitur dengan Faktor SCORPAN
* **Layout Visual:** Skema Tumpukan Layer Raster (Stacking) yang berimpit tepat di atas titik sampel tanah:
  ![Gambar Kovariat SCORPAN Multi-sumber](../assets/modul-8/M8-G01_kovariat-scorpan-sebagai-lapisan-raster.png)
  *Ilustrasi Fusi Tingkat Fitur: Tumpukan Kovariat SCORPAN Multisumber (DEM, Lereng, TWI, Indeks Spektral, Radar) yang Berimpit pada Titik Observasi Tanah.*
  * Layer 1: Indeks Vegetasi (NDVI, SAVI) $\rightarrow$ Mewakili Faktor Organisme ($o$).
  * Layer 2: Turunan Topografi (Slope, TWI, TPI) $\rightarrow$ Mewakili Faktor Relief ($r$).
  * Layer 3: Hamburan Balik SAR (VV, VH) $\rightarrow$ Indikator Struktur & Kelembapan.
  * Layer 4: Peta Geologi / Litologi $\rightarrow$ Mewakili Bahan Induk ($p$).
* **Poin Paparan:**
  * Setiap piksel di lanskap perkebunan memiliki 'vektor atribut multisumber' yang unik.
  * Titik sampel tanah di lapangan berfungsi mengikat nilai-nilai fitur lingkungan ini ke dalam model matematika kalibrasi.
  * Kualitas fusi fitur sangat menentukan keberhasilan prediksi algoritma *machine learning*.
* **Catatan Pemateri:**
  > "Fusi tingkat fitur memungkinkan kita melihat tanah dari berbagai kacamata sekaligus. Satu titik di kebun sawit tidak hanya memiliki koordinat X dan Y, tetapi memiliki elevasi, kemiringan lereng, indeks kebasahan, kelebatan kanopi di atasnya, dan jenis batuan di bawahnya."

---

### SLIDE 13: PRINSIP PENYELARASAN DATA GEOSPASIAL
* **Kategori:** Standarisasi Teknis & Pra-pemrosesan
* **Judul:** Prinsip Penyelarasan Multi-source Data Menjadi Tumpukan Selaras
* **Layout Visual:** Diagram Alir Alur Penyelarasan Data:
  * Raw Data $\rightarrow$ Proyeksi Koordinat $\rightarrow$ Resampling Grid $\rightarrow$ Koreksi Radiometrik $\rightarrow$ Buffer & Kliping $\rightarrow$ Stack Terkoregistrasi.
* **Poin Paparan:**
  * Syarat mutlak fusi data: setiap lapisan raster harus merujuk pada ruang, ukuran sel, dan posisi grid yang identik persis.
  * **6 Kaidah Penyelarasan Data:**
    1. **Sistem Proyeksi Seragam:** Menggunakan UTM (satuan meter), bukan derajat geografis, untuk akurasi perhitungan luas dan gradien kemiringan.
    2. **Grid Acuan Tetap (*Reference Grid*):** Menetapkan ukuran piksel (misal 10 m) dengan koordinat batas kelipatan bulat dari resolusi piksel.
    3. **Metode Resampling Sesuai Sifat Data:**
       * *Nearest Neighbour* mutlak untuk data kategorik (kelas tanah, geologi, bentuklahan) agar tidak merusak kode kelas.
       * *Bilinear / Cubic Convolution* untuk data permukaan kontinu (elevasi, pantulan optik).
    4. **Koreksi Radiometrik & Fisik:** Nilai digital dikonversi ke reflektansi permukaan (BOA).
    5. **Penyelarasan Waktu:** Memilih citra pada musim yang relevan dengan pengambilan sampel.
    6. **Penyangga (*Buffer Area*):** Menambahkan area penyangga di luar batas estate agar analisis medan tidak rusak oleh efek tepi (*edge effect*).
* **Catatan Pemateri:**
  > "Banyak analis geospasial melakukan kesalahan fatal di sini: menggabungkan raster UTM dengan raster derajat geografis, atau me-resample peta jenis tanah menggunakan metode Bilinear sehingga muncul jenis tanah baru yang tidak pernah ada! Kaidah ini wajib dipatuhi di studio nanti."

---

### SLIDE 14: KONTROL MUTU & MITIGASI ARTEFAK DATA
* **Kategori:** *Quality Assurance* Data Lingkungan
* **Judul:** Kontrol Mutu Data Lingkungan Sebelum Analisis
* **Layout Visual:** 2 Panel Kasus Kesalahan Data (Sebelum vs Sesudah Diperbaiki):
  * Kiri: Pola garis garis lurus/artefak striping pada DTM kelerengan.
  * Kanan: Masalah *NoData* di perbatasan dan pergeseran koordinat setengah piksel (*pixel misalignment*).
* **Poin Paparan:**
  * Data turunan seperti kelerengan (*slope*) sangat sensitif terhadap kualitas DEM asal; cacat data elevasi menghasilkan artefak kelerengan buatan yang merusak model tanah.
  * Pemilihan resolusi grid harus realistis terhadap skala survei; memperkecil piksel (*upsampling*) data kasar 90 m menjadi 5 m tidak menambah informasi, melainkan menciptakan ilusi ketelitian palsu.
  * Verifikasi konsistensi atribut sebelum fusi fitur dijalankan.
* **Catatan Pemateri:**
  > "Prinsip komputasi berlaku mutlak: *Garbage In, Garbage Out*. Jika data turunan kelerengan kita penuh garis artefak pemotongan citra, model pedometrik kita akan menganggap garis lurus tersebut sebagai batas tanah alami. Selalu periksa data raster Anda secara visual dan statistik sebelum dimodelkan."

---

### SLIDE 15: METODE PEMETAAN TANAH: ANALITIK VS SINTETIK
* **Kategori:** Pengantar Bagian 3 - Delineasi SMU
* **Judul:** Pendekatan Pemetaan Tanah: Metode Analitik vs. Metode Sintetik
* **Layout Visual:** Tabel Komparasi Berwarna (Tabel 3.1 Modul).
  * Kolom 1: Aspek Pembeda.
  * Kolom 2: Metode Analitik (Konvensional Lapangan).
  * Kolom 3: Metode Sintetik (Pemodelan Bentanglahan Geospasial).
* **Poin Paparan:**
  * **Metode Analitik (Konvensional):**
    * Bertolak dari pengamatan profil tanah detail di lapangan, lalu mengelompokkan pedon-pedon serupa menjadi satuan tanah.
    * Kelebihan: Karakteristik tanah terukur langsung dan sangat detail.
    * Keterbatasan: Biaya sangat tinggi, lambat, batas poligon ditarik interpolasi kasar antar lubang bor.
  * **Metode Sintetik (Lanskap Terintegrasi):**
    * Bertolak dari pembagian bentanglahan (*landform*) dan satuan lingkungan menggunakan penginderaan jauh, kemudian mendeliniasi satuan bentang lahan homogen sebagai wadah persebaran tanah.
    * Kelebihan: Batas batas unit selaras dengan morfologi nyata di lapangan, efisien secara spasial dan biaya.
* **Catatan Pemateri:**
  > "Kita melangkah ke Bagian 3: Delineasi Soil Mapping Unit. Apakah kita harus mengebor setiap 50 meter di kebun sawit seluas puluhan ribu hektar? Itu metode analitik murni yang sangat mahal. Pendekatan modern mengombinasikan metode sintetik: kita petakan dulu satuan morfologi bentanglahan dari citra dan DEM, baru kita tempatkan titik observasi secara berstrata."

---

### SLIDE 16: HAKIKAT SOIL MAPPING UNIT (SMU)
* **Kategori:** Konsep Taksonomi vs Kartografi
* **Judul:** Memahami Batasan: Satuan Taksonomi vs. Satuan Peta Tanah
* **Layout Visual:**
  * Diagram Hierarki Taksonomi Tanah:
    ![Gambar 3.2: Hierarki Kategori Taksonomi Tanah](../assets/modul-3/M3-G02_hierarki-kategori-taksonomi-tanah.png)
    *Gambar 3.2: Hierarki Enam Kategori Taksonomi Tanah USDA (Ordo hingga Seri) sebagai Satuan Klasifikasi Abstrak.*
  * Komparasi konseptual: Satuan Taksonomi (abstrak di buku) vs Satuan Peta Tanah (poligon fisik nyata di lapangan).
* **Poin Paparan:**
  * **Satuan Taksonomi (*Taxonomic Unit*):** Kelas klasifikasi abstrak (misal: *Typic Kandiudults*) yang didefinisikan secara ketat oleh batasan sifat morfologi dan laboratorium.
  * **Satuan Peta Tanah (*Soil Mapping Unit - SMU*):** Poligon di atas peta yang mendeliniasi area tertentu di permukaan bumi yang didominasi oleh satu atau beberapa komponen taksonomi.
  * Di alam nyata, batas tanah tidak pernah berupa garis tegas homogen sempurna; setiap poligon SMU selalu memuat variabilitas tanah yang tidak dapat dipisahkan pada skala pemetaan tersebut.
* **Catatan Pemateri:**
  > "Tolong bedakan antara Taksonomi Tanah dan Satuan Peta Tanah. Taksonomi tanah ada di buku teks sistem klasifikasi; sedangkan SMU ada di atas peta dan di hamparan kebun sawit. SMU adalah wadah spasial operasional kita untuk mengelola pupuk dan drainase."

---

### SLIDE 17: EMPAT KATEGORI SATUAN PETA TANAH (USDA)
* **Kategori:** Standar Satuan Peta
* **Judul:** Komposisi Satuan Peta Tanah: Dari Konsosiasi Hingga Kompleks
* **Layout Visual:**
  * Ilustrasi 4 Kategori Satuan Peta Tanah:
    ![Gambar 3.1: Empat Kategori Satuan Peta Tanah](../assets/modul-3/M3-G01_jenis-satuan-peta-tanah.png)
    *Gambar 3.1: Empat Kategori Satuan Peta Tanah: Konsosiasi, Asosiasi, Kompleks, dan Kelompok Tak Dibedakan (Berdasarkan Standar USDA Soil Survey Manual).*
  * Rincian proporsi komponen:
    * (a) Konsosiasi (Didominasi 1 taksa utama $\ge 50\%$)
    * (b) Asosiasi (2+ taksa berpola geografis teratur yang dapat dipisah di skala detail)
    * (c) Kompleks (2+ taksa berpola sangat rumit yang tidak dapat dipisah di skala praktis)
    * (d) Kelompok Tak Dibedakan (Undifferentiated Group - taksa berbeda tetapi respons pengelolaannya sama)
* **Poin Paparan:**
  * **1. Konsosiasi (*Consociation*):** Didominasi oleh satu taksa tanah utama ($\ge 50\%$) bersama tanah-tanah serupa ($\ge 75\%$). Satuan paling murni.
  * **2. Asosiasi (*Association*):** Terdiri atas dua atau lebih taksa tanah berbeda yang tersebar mengikuti pola bentanglahan yang teratur dan berulang (misal: satu taksa di lereng atas, satu taksa di kaki lereng).
  * **3. Kompleks (*Complex*):** Dua atau lebih taksa tanah berbeda bercampur baur secara acak dan sangat rapat, sehingga tidak mungkin dipisahkan secara kartografis pada skala kerja.
  * **4. Kelompok Tak Dibedakan (*Undifferentiated Group*):** Dua atau lebih taksa yang secara geografis tidak selalu bersama, tetapi digabung dalam satu satuan peta karena potensi dan kendala pengelolaannya serupa (misal lereng sangat terjal berbatu).
* **Catatan Pemateri:**
  > "Di perkebunan sawit bergelombang, sebagian besar satuan peta kita adalah Asosiasi atau Kompleks. Jika pola tanah di punggungan dan lembah berselang-seling setiap 20 meter, kita tidak bisa mendelineasinya sebagai konsosiasi terpisah di peta skala 1:25.000; kita harus menamakannya sebagai Kompleks atau Asosiasi."

---

### SLIDE 18: KONSEP INKLUSI DAN KEMURNIAN SATUAN PETA
* **Kategori:** Standar Kartografi & Kontrol Kualitas
* **Judul:** Memahami Inklusi Tanah: Realitas Variabilitas Alami
* **Layout Visual:** Diagram Lingkaran Distribusi Persentase Kemurnian Poligon Konsosiasi:
  * $50–75\%$: Komponen Utama Bernama.
  * Hingga $25\%$: Inklusi Serupa (*Similar Inclusions*).
  * Maksimal $15\%$: Inklusi Tidak Serupa Non-Pembatas (*Dissimilar Non-limiting*).
  * Maksimal $10\%$: Inklusi Tidak Serupa Pembatas (*Dissimilar Limiting*).
* **Poin Paparan:**
  * **Definisi Inklusi:** Komponen tanah minor di dalam poligon yang tidak disebutkan dalam nama satuan peta karena ukurannya terlalu kecil untuk dipisahkan.
  * **Inklusi Serupa (*Similar*):** Sifatnya mirip dengan tanah dominan, sehingga respons agronomi dan rekomendasi pupuk/drainasenya sama.
  * **Inklusi Kontras/Tidak Serupa (*Dissimilar*):** Memiliki sifat yang sangat berbeda.
    * *Limiting (Pembatas):* Inklusi yang menurunkan kelayakan lahan secara drastis (misal: kantong gambut tipis atau singkapan batuan di tengah tanah mineral subur). Tidak boleh melebihi $10–15\%$ dari luas poligon!
* **Catatan Pemateri:**
  > "Tidak ada satuan peta tanah yang 100% murni. Jika Anda membuat peta tanah dan mengklaim seluruh poligon seratus persen adalah Typic Kandiudults, itu mustahil secara pedologi. Yang terpenting adalah mengendalikan inklusi pembatas agar tidak menyesatkan rekomendasi manajemen tanaman."

---

### SLIDE 19: DELINEASI BERBASIS BENTANGLAHAN & KONSEP CATENA
* **Kategori:** Teori Geomorfologi & Pedologi Lapangan
* **Judul:** Pendekatan Bentanglahan: Konsep Catena dalam Delineasi Batas
* **Layout Visual:**
  * Penampang Toposekuen Catena & Sembilan Satuan Lahan:
    ![Gambar 3.3: Model Sembilan Satuan Permukaan Lahan](../assets/modul-3/M3-G03_model-sembilan-satuan-permukaan-lahan.png)
    *Gambar 3.3: Konsep Catena dan Model Sembilan Satuan Permukaan Lahan (Dalrymple et al., 1968): Hubungan Posisi Lereng, Proses Pedogeomorfik, dan Sebaran Sifat Tanah.*
  * Rangkaian geomorfik: Puncak (*Interfluve*) $\rightarrow$ Lereng Atas $\rightarrow$ Lereng Tengah $\rightarrow$ Kaki Lereng $\rightarrow$ Lembah Aluvial (*Toeslope*).
* **Poin Paparan:**
  * **Konsep Catena (Milne 1935):** Rangkaian tanah yang berulang di sepanjang lereng topografi yang berkembang dari bahan induk dan iklim yang sama, di mana perbedaan sifat tanah dikendalikan oleh hidrologi, erosi, dan transportasi material.
  * **Hubungan Geomorfologi dan Tanah:**
    * Puncak/Punggungan: Erosi aktif, solum tanah cenderung lebih dangkal, drainase bebas, pelindian (*leaching*) intensif.
    * Lereng Tengah: Zona transfer/transportasi material.
    * Kaki Lereng & Lembah: Zona akumulasi/deposisi koluvial dan aluvial, solum tanah tebal, kaya lempung, muka air tanah dangkal hingga risiko genangan (*waterlogging*).
  * Delineasi batas SMU berbasis garis tekuk lereng (*slope breaks*) dan batas morfologi pada model elevasi digital (DEM).
* **Catatan Pemateri:**
  > "Air mengalir ke bawah membawa partikel halus dan hara terlarut. Itulah mengapa tanah di lembah selalu berbeda secara pedologis dibanding tanah di puncak bukit, meskipun batuan dasarnya sama. Dengan membaca bentuk lereng dari DEM dan bayangan medan (*hillshade*), kita sudah bisa menduga batas satuan tanah secara akurat."

---

### SLIDE 20: SKALA PEMETAAN, MLD, DAN MLA
* **Kategori:** Kaidah Kartografi Kuantitatif
* **Judul:** Berapa Luas Poligon Terkecil? Konsep MLD dan MLA
* **Layout Visual:**
  * Ilustrasi Hubungan Skala Peta dan Batas Luasan Minimum:
    ![Gambar 3.4: Minimum Legible Area (MLA) pada Berbagai Skala](../assets/modul-3/M3-G04_mla-pada-berbagai-skala.png)
    *Gambar 3.4: Hubungan Skala Peta, Minimum Legible Delineation (MLD), dan Minimum Legible Area (MLA).*
  * Formula Matematika Cornell University & Rossiter (2000).
* **Poin Paparan:**
  * **Minimum Legible Delineation (MLD):** Ukuran fisik terkecil poligon yang masih dapat digambar dan dibaca dengan jelas di atas peta cetak tanpa tertutup oleh tebal garis batas ($\approx 0.4\ \text{cm}^2$).
  * **Minimum Legible Area (MLA):** Luas area nyata terkecil di lapangan yang diwakili oleh MLD:
    $$\text{MLA (hektar)} = \left(\frac{\text{Skala (Scale Number)}}{1.000}\right)^2 \div 250$$
  * **Korelasi Skala Pemetaan dengan Batas Luas Minimum:**
    * Skala $1:10.000 \rightarrow \text{MLA} = 0.4\ \text{ha}$ (kotak sisi $63\ \text{m}$)
    * Skala $1:25.000 \rightarrow \text{MLA} = 2.5\ \text{ha}$ (kotak sisi $158\ \text{m}$)
    * Skala $1:50.000 \rightarrow \text{MLA} = 10.0\ \text{ha}$ (kotak sisi $316\ \text{m}$)
  * Poligon yang lebih kecil dari MLA dianggap sebagai 'sliver polygon' atau derau kartografis yang harus digabungkan (*generalized*).
* **Catatan Pemateri:**
  > "Jika kita menyusun peta survei operasional kebun skala 1:10.000, batas delineasi minimum kita adalah 0,4 hektar. Jangan mendeliniasi poligon seukuran 50 meter persegi di peta skala ini; secara kartografi itu tidak terbaca dan secara operasional mustahil diperlakukan sebagai blok manajemen terpisah."

---

### SLIDE 21: JEBAKAN TUMPANG SUSUN OTOMATIS VS DELINEASI PEDOLOGIS
* **Kategori:** Metodologi Analisis Spasial
* **Judul:** Mengapa Tumpang Susun Komputer Otomatis (*GIS Overlay*) Sering Gagal?
* **Layout Visual:**
  * Komparasi Bahaya Intersect Otomatis vs Delineasi Pedologis:
    ![Gambar 3.5: Perbandingan Tumpang Susun Otomatis dan Generalisasi](../assets/modul-3/M3-G05_ilustrasi-tumpang-susun-dan-generalisasi.png)
    *Gambar 3.5: Bahaya Intersect Otomatis (Fragmentasi Sliver Polygon) dan Distorsi Filter Sieve vs. Solusi Delineasi Terbimbing Pedologis.*
  * Kiri: Hasil *Intersect GIS* otomatis $\rightarrow$ Hancur menjadi puluhan ribu poligon renik (*slivers*).
  * Kanan: Hasil Generalisasi Sieve Filter otomatis $\rightarrow$ Menghilangkan kelas lereng kritis dan merusak kontinuitas bentanglahan alami.
* **Poin Paparan:**
  * **Kelemahan Tumpang Susun Otomatis Vektor/Raster:**
    * Penumpukan lapisan kelerengan detail dengan bentuklahan menghasilkan fragmentasi ekstrem: ribuan poligon kecil di bawah batas MLA ($> 95\%$ poligon renik).
    * Jika disaring otomatis dengan algoritma *sieve* komputer ke tetangga terbesar, batas alami bentanglahan terdistorsi berat dan kelas lereng terjal bisa musnah.
  * **Solusi: Delineasi Manual Terbimbing Lanskap (*On-Screen Expert Digitizing*):**
    * Penafsir pedologis menggunakan citra komposit Sentinel-2, foto udara, dan *hillshade* DEM sebagai panduan visual untuk menarik batas poligon alami yang mulus, logis secara geomorfologi, dan taat pada aturan MLA.
* **Catatan Pemateri:**
  > "Banyak operator GIS berpikir: 'Cukup ambil layer lereng, layer tanah, layer tutupan, lalu klik tombol INTERSECT di software.' Apa hasilnya? Peta Anda hancur menjadi ratusan ribu pecahan poligon kecil yang tidak bermakna! Komputer tidak memiliki penalaran pedologis. Kita memerlukan delineasi *on-screen* dengan panduan relief untuk menarik batas SMU yang masuk akal."

---

### SLIDE 22: RANGKUMAN & JEMBATAN KE MODUL SELANJUTNYA
* **Kategori:** Sintesis & Penutup Sesi
* **Judul:** Rangkuman Kunci & Jembatan ke Estimasi Sifat Tanah
* **Layout Visual:** Peta Alur Keterkaitan Materi (Roadmap Pelatihan).
  * Kotak 1 (Selesai): Fisika RS $\rightarrow$ Fusi Data Multisumber $\rightarrow$ Delineasi SMU Bentanglahan.
  * Kotak 2 (Sesi Berikutnya): Ekstraksi Spektral Sifat Tanah (Modul 4) & Interpretasi Pedologis (Modul 6).
* **Poin Paparan:**
  * Penginderaan jauh pasif dan aktif saling melengkapi untuk menembus keterbatasan lingkungan perkebunan tropis.
  * Fusi tingkat fitur memungkinkan pembentukan tumpukan kovariat SCORPAN yang selaras secara geometris dan fisik.
  * Satuan Peta Tanah (SMU) adalah unit bentanglahan operasional yang harus menghormati kaidah catena dan batas luasan kartografis (MLA).
  * SMU yang dideliniasi menjadi strata perancangan sampling tanah yang representatif dan efisien bagi pemodelan DSM.
* **Catatan Pemateri:**
  > "Bapak dan Ibu sekalian, kita telah menyelesaikan fondasi geospasial dan delineasi satuan peta tanah. Unit-unit poligon bentanglahan yang telah kita deliniasi ini akan menjadi kerangka kerja bagi Dr. Anggri di sesi berikutnya untuk menduga sifat-sifat fisik dan kimia tanah di dalamnya serta melakukan interpretasi pedologis mendalam. Terima kasih."
