# RANCANGAN PRESENTASI (SLIDE DECK) PELATIHAN
## Bagian 8: Pemodelan Digital Soil Mapping (DSM)

**Pemateri:** Dr. Eng. Guruh Samodra, S.Si., M.Sc.  
**Institusi:** Pusat Studi Pengelolaan Sumber Daya Lahan (PS2DL), Universitas Gadjah Mada  
**Target Audiens:** Staf Teknis, Agronomis, Peneliti, dan Pengelola Perkebunan Kelapa Sawit (PT SMART Tbk)  
**Alokasi Waktu:** Sesi Ceramah Teori (60 Menit) + Pengantar Sesi Praktik Machine Learning Hari ke-3  
**Dokumen Acuan:** `Modul Pelatihan SMART Pemanfaatan RS dan DSM.docx` (Bab 8)

---

### PANDUAN VISUAL & IDENTITAS SLIDE (DESIGN SYSTEM)
* **Warna Utama:** Biru Navy UGM (`#1F3A5F`), Hijau Daun Sawit (`#2A9D8F`), Oranye/Merah Analitik (`#E07B39` / `#C0392B`), Abu-abu Komputasi (`#6B7280`).
* **Tipografi:** Sans-serif modern (Calibri / Carlito / Arial), hierarki judul besar (32–36 pt), subjudul (20–24 pt), teks isi (14–16 pt).
* **Prinsip Tampilan:** Diagram arsitektur machine learning, matriks formula statistik validasi, grafik semivariogram residual spasial, dan peta ketidakpastian / *Area of Applicability*.

---

## DAFTAR SLIDE & STRUKTUR MATERI

```
BAGIAN 8: PEMODELAN DIGITAL SOIL MAPPING (Slide 1–20)
  - Slide 1: Judul & Pembuka Sesi
  - Slide 2: Arsitektur Konseptual DSM: Menghubungkan Titik Sampel dengan Lanskap
  - Slide 3: Formula SCORPAN: Transformasi Faktor Genetik Menjadi Lapisan Kovariat Spasial
  - Slide 4: Matriks Kovariat SCORPAN untuk Perkebunan Kelapa Sawit
  - Slide 5: Seleksi Kovariat & Rekayasa Fitur: Menghindari Korelasi Semu (Spurious Correlation)
  - Slide 6: Taksonomi Algoritma DSM: Dari Regresi Linear Hingga Deep Learning
  - Slide 7: Algoritma Berbasis Pohon (Tree-based Ensembles): Mengapa Random Forest Mendominasi?
  - Slide 8: Pemodelan Hibrida Geostatistik: Konsep Regression Kriging (RK)
  - Slide 9: Bahaya Autokorelasi Spasial dalam Pembagian Data (Data Splitting)
  - Slide 10: Metodologi Validasi Spasial yang Sahih: Spatial Cross-Validation
  - Slide 11: Alur Kerja Lengkap Pembuatan Model DSM (End-to-End Workflow)
  - Slide 12: Standardisasi Interval Kedalaman Profil Tanah (Spesifikasi GlobalSoilMap)
  - Slide 13: Enam Metrik Statistik Validasi Model Tanah (ME, MAE, RMSE, MEC, R², CCC)
  - Slide 14: Memahami Hakikat Residual Model dan Struktur Spasialnya
  - Slide 15: Pemodelan Ketidakpastian Prediksi: Quantile Regression Forests (QRF)
  - Slide 16: Menguji Interval Prediksi: Prediction Interval Coverage Probability (PICP)
  - Slide 17: Batas Keberlakuan Model: Konsep Area of Applicability (AOA) Meyer & Pebesma
  - Slide 18: Dari Peta Kontinu ke Keputusan Agronomi: Penyusunan Zona Pengelolaan Lahan Sawit
  - Slide 19: Siklus Pemetaan Adaptif: Pengambilan Sampel Ulang Berbasis Ketidakpastian
  - Slide 20: Rangkuman & Arahan Memulai Praktik Machine Learning Hari ke-3
```

---

## RINCIAN KONTEN PER SLIDE

---

### SLIDE 1: JUDUL & PEMBUKA
* **Kategori:** Cover Presentation
* **Judul Utama:** Pemodelan Digital Soil Mapping (DSM)
* **Sub-judul:** Membangun Model Kuantitatif Berbasis SCORPAN dan Machine Learning untuk Prediksi Spasial Sifat Tanah Perkebunan
* **Identitas:** Dr. Eng. Guruh Samodra, S.Si., M.Sc. | Pusat Studi Pengelolaan Sumber Daya Lahan (PS2DL) UGM
* **Layout Visual:**
  * Kiri: Judul presentasi tebal, identitas pemateri, logo UGM & PS2DL.
  * Kanan: Visualisasi 3D tumpukan lapisan raster kovariat lingkungan (DEM, SAR, Optik) yang dihubungkan dengan diagram pohon keputusan *Random Forest* dan menghasilkan peta prediksi kontinyu tekstur tanah beserta peta ketidakpastiannya.
* **Poin Paparan:**
  * Menyatukan seluruh materi dari Modul 1 hingga Modul 7 ke dalam satu kerangka pemodelan komputasi spasial terpadu.
  * Memahami matematika prediksi tanah, algoritma *machine learning*, validasi spasial yang bebas bias, dan kuantifikasi ketidakpastian.
* **Catatan Pemateri (Speaker Notes):**
  > "Selamat pagi rekan-rekan peserta pelatihan. Hari ini kita tiba di puncak dari seluruh rangkaian pelatihan ini: Pemodelan Digital Soil Mapping. Kita telah mengumpulkan citra satelit optik, radar, DEM, peta bentanglahan dari Prof. Junun dan Dr. Anggri, teknik deteksi tanah terbuka dari Dr. Retnadi, serta data sensor lapangan dari Pak Pandu. Sekarang, tugas kita adalah merajut seluruh data raksasa tersebut ke dalam algoritma komputasi untuk menghasilkan peta sifat tanah digital yang presisi dan dapat dipertanggungjawabkan."

---

### SLIDE 2: ARSITEKTUR KONSEPTUAL DSM
* **Kategori:** Fondasi Teori Pedometrik
* **Judul:** Arsitektur Konseptual DSM: Menjembatani Titik Sampel ke Seluruh Lanskap
* **Layout Visual:** Diagram Alir 3 Komponen Utama DSM (Lagacherie & McBratney 2006; Minasny & McBratney 2016):
  * Komponen Input 1: Observasi Tanah di Lapangan ($S$) $\rightarrow$ Sampel profil, analisis lab, sensor proksimal.
  * Komponen Input 2: Kovariat Lingkungan Menyeluruh ($E$) $\rightarrow$ Citra satelit, turunan medan DEM, iklim, geologi.
  * Komponen Pusat: Fungsi Prediksi Spasial Matematis ($f$) $\rightarrow$ Algoritma *Machine Learning* / Geostatistik.
  * Komponen Output: Peta Prediksi Spasial Kontinu + Peta Ketidakpastian (*Uncertainty Map*).
* **Poin Paparan:**
  * **Definisi DSM:** Pembuatan dan pengisian sistem informasi tanah spasial dengan model numerik yang menduga variasi sifat tanah berdasarkan observasi lapangan dan variabel lingkungan pengganti (Lagacherie & McBratney 2006).
  * **Perbedaan Revolusioner:** Survei konvensional menarik batas poligon secara subjektif; DSM menghasilkan grid nilai piksel kontinu dengan estimasi galat matematis yang transparan pada setiap lokasi.
* **Catatan Pemateri:**
  > "DSM bukan sulap dan bukan tebak-tebakan. DSM adalah fungsi transfer spasial. Kita memiliki data tanah di 100 titik sampel bor, tetapi kita ingin mengetahui sifat tanah di 1 juta titik piksel di seluruh kebun sawit kita. Bagaimana caranya? Kita hubungkan 100 titik tersebut dengan karakteristik lingkungannya melalui fungsi matematika $f$."

---

### SLIDE 3: FORMULA MATEMATIKA SCORPAN
* **Kategori:** Formula Inti Pedometrik
* **Judul:** Formula SCORPAN: Landasan Empiris Pemetaan Tanah Digital
* **Layout Visual:**
  * Diagram Tumpukan Kovariat SCORPAN sebagai Lapisan Raster:
    ![Gambar 8.1: Kovariat SCORPAN sebagai Lapisan Raster Spasial](../assets/modul-8/M8-G01_kovariat-scorpan-sebagai-lapisan-raster.png)
    *Gambar 8.1: Representasi Faktor Pembentuk Tanah SCORPAN sebagai Lapisan Raster Spasial Kontinu: Elevasi, Lereng, TWI, Indeks Vegetasi NDVI, Indeks Tanah BSI, dan Konduktivitas Listrik Semu.*
  * Atas: Formula Matematika SCORPAN (McBratney et al. 2003):
    $$S = f(s, c, o, r, p, a, n) + e$$
  * Bawah: Penjelasan 7 Huruf SCORPAN sebagai Lapisan Raster Spasial:
    * $s$ (*soil*): Sifat tanah terdahulu / peta warisan
    * $c$ (*climate*): Iklim (curah hujan, suhu)
    * $o$ (*organisms*): Vegetasi, kanopi sawit, penutup lahan
    * $r$ (*relief*): Topografi, kelerengan, kurvatur, TWI
    * $p$ (*parent material*): Litologi, bahan induk geologi
    * $a$ (*age*): Umur relatif permukaan geomorfik
    * $n$ (*spatial position*): Koordinat X, Y, jarak geografis
    * $e$ (*error*): Bagian keragaman yang tidak terjelaskan (residual)
* **Poin Paparan:**
  * Berbeda dengan persamaan Hans Jenny (1941) yang bersifat konseptual murni, fungsi $f$ dalam SCORPAN **tidak diturunkan dari teori abstrak, melainkan dipelajari dari data** (*data-driven empirical function*).
  * Syarat mutlak: Setiap faktor pembentuk tanah wajib diwujudkan dalam bentuk lapisan raster spasial kontinu yang menutupi seluruh area kebun.
* **Catatan Pemateri:**
  > "Tujuh huruf SCORPAN adalah peta jalan kita. Di komputer, setiap huruf ini adalah satu berkas file GeoTIFF. Huruf $r$ adalah TIF kelerengan dari DEMNAS, huruf $o$ adalah TIF komposit tanah terbuka dari Sentinel-2, huruf $p$ adalah TIF peta geologi. Semua layer ini kita tumpuk dan kita sejajarkan."

---

### SLIDE 4: MATRIKS KOVARIAT SCORPAN UNTUK KEBUN SAWIT
* **Kategori:** Taksonomi Data Lapangan
* **Judul:** Matriks Kovariat SCORPAN Khusus Perkebunan Kelapa Sawit
* **Layout Visual:** Tabel Komprehensif Berdasarkan Tabel 8.1 Modul (Faktor SCORPAN | Contoh Kovariat | Sumber Data | Catatan Kritis Sawit).
* **Poin Paparan:**
  1. **Faktor $r$ (Relief - Paling Informatif):**
     * Elevasi, Kelerengan (*Slope*), Kelengkungan Lereng (*Curvature*), Indeks Posisi Topografi (TPI), Indeks Kebasahan Topografi (TWI), *Multi-resolution Valley Bottom Flatness* (MrVBF).
     * *Catatan Sawit:* Relief tetap terbaca di bawah tajuk melalui DTM LiDAR / radar interferometri; pengendali utama pergerakan air dan akumulasi hara.
  2. **Faktor $o$ (Organisme):**
     * Indeks vegetasi (NDVI, SAVI), komposit tanah terbuka multitemporal (BSI).
     * *Catatan Sawit:* Mencerminkan umur tanam, kerapatan tajuk, dan biomassa tanaman penutup (*LCC*).
  3. **Faktor $p$ (Bahan Induk):**
     * Peta formasi geologi, data spektrometer gamma ($^{40}\text{K}, ^{232}\text{Th}$), peta material permukaan.
  4. **Faktor $c$ (Iklim):**
     * Curah hujan tahunan (CHIRPS) dan suhu. *Catatan Sawit:* Cenderung homogen di dalam 1 estate, sehingga variansnya sering nol.
  5. **Faktor $s$ & $n$ (Tanah & Posisi):**
     * Konduktivitas listrik semu ($EC_a$ PSS) dan koordinat spasial UTM.
* **Catatan Pemateri:**
  > "Perhatikan Tabel 8.1. Mengapa di perkebunan sawit faktor Relief ($r$) hampir selalu menjadi prediktor nomor satu? Karena dalam satu kebun, iklimnya sama dan batuannya sering kali sama. Yang membuat tanah di Blok 1 berbeda dengan Blok 2 adalah apakah tanah itu berada di puncak bukit yang kering atau di cekungan lembah yang menerima limpasan air!"

---

### SLIDE 5: SELEKSI KOVARIAT & REKAYASA FITUR
* **Kategori:** *Feature Engineering*
* **Judul:** Seleksi Kovariat: Membuang Multikolinearitas & Korelasi Semu
* **Layout Visual:** Diagram Alir Seleksi Fitur (Dari 50 Kovariat Mentah $\rightarrow$ 10–15 Kovariat Terpilih):
  * Matriks Korelasi Pearson/Spearman ($r > 0.85$ dibuang).
  * Analisis *Variance Inflation Factor* (VIF $> 10$ dieliminasi).
  * *Recursive Feature Elimination* (RFE) & *Permutation Feature Importance*.
* **Poin Paparan:**
  * Memasukkan terlalu banyak kovariat ($> 50$ layer) memicu **bencana dimensi (*curse of dimensionality*)** dan *overfitting* (model menghafal data latih).
  * **Multikolinearitas:** Kovariat yang saling menduplikasi informasi (misal: kanal B2, B3, B4 yang sangat berkorelasi linier) memperlambat komputasi dan mengacaukan interpretasi bobot variabel.
  * **Filter Kelayakan Pedologis:** Jangan memilih kovariat hanya karena angka statistiknya tinggi secara kebetulan (*spurious correlation*); pastikan hubungan antara kovariat dan sifat tanah memiliki penjelasan pedologis yang logis.
* **Catatan Pemateri:**
  > "Banyak analis GIS pemula berpikir: 'Semakin banyak layer yang dimasukkan, semakin pintar modelnya.' Ini salah besar! Memasukkan 100 layer kovariat hanya akan membuat model machine learning Anda bingung dan overfitting. Kita harus menyaringnya menjadi 10 hingga 15 kovariat terbaik yang secara statistik independen dan secara pedologi masuk akal."

---

### SLIDE 6: TAKSONOMI ALGORITMA DIGITAL SOIL MAPPING
* **Kategori:** Perbandingan Algoritma Komputasi
* **Judul:** Taksonomi Algoritma DSM: Dari Geostatistik Hingga Machine Learning
* **Layout Visual:** Tabel Perbandingan Karakteristik 5 Kelompok Algoritma (Berdasarkan Tabel 8.2 Modul):
  * Kelompok: Regresi Linear | Geostatistik Murni | Hibrida Geostatistik | Berbasis Pohon (*Tree-based*) | Pembelajaran Mesin Lain.
* **Poin Paparan:**
  * **1. Regresi Linear Berganda (MLR / Lasso / Ridge):**
    * Cepat, sederhana, transparan. Keterbatasan: gagal menangkap hubungan non-linearitas alamiah tanah.
  * **2. Geostatistik Murni (Ordinary Kriging):**
    * Bertumpu pada autokorelasi spasial jarak (hukum Tobler). Keterbatasan: tidak memanfaatkan informasi citra satelit/DEM.
  * **3. Geostatistik Hibrida (Regression Kriging - RK):**
    * Standar emas pedometrik klasik: memadukan model tren lingkungan dengan kriging terhadap residual spasial.
  * **4. Berbasis Pohon (*Tree-based Ensembles* - RF, XGBoost, Cubist):**
    * Paling dominan di era modern: mampu memetakan interaksi non-linear yang sangat rumit tanpa asumsi distribusi normal.
  * **5. Artificial Neural Networks (ANN) & SVM:**
    * Sangat fleksibel, namun cenderung berperilaku sebagai *black-box* yang sulit diinterpretasikan.
* **Catatan Pemateri:**
  > "Tabel 8.2 merangkum kotak perkakas algoritma kita. Tidak ada satu algoritma yang menang dalam segala situasi (*No Free Lunch Theorem*). Namun, dalam literatur pemetaan tanah dunia selama 10 tahun terakhir, algoritma berbasis pohon seperti Random Forest dan Cubist secara konsisten memberikan akurasi tertinggi untuk sifat tanah."

---

### SLIDE 7: ALGORITMA BERBASIS POHON: RANDOM FOREST
* **Kategori:** Arsitektur Algoritma Unggulan
* **Judul:** Mengapa *Random Forest* Menjadi Standar Emas Pemetaan Tanah?
* **Layout Visual:** Diagram Arsitektur Kerja *Random Forest* (Gambar Konsep Ensemble Learning):
  * Data Latih $\rightarrow$ *Bootstrap Aggregating* (Bagging) $\rightarrow$ Pembangunan 500 Pohon Keputusan Independen (*Decision Trees*) dengan sub-fitur acak $\rightarrow$ Agregasi Prediksi Rata-rata (*Ensemble Average*).
* **Poin Paparan:**
  * **Keunggulan Mutlak Random Forest dalam DSM:**
    1. **Tahan Terhadap Overfitting:** Rata-rata dari ratusan pohon mereduksi varians model secara drastis.
    2. **Mampu Menangkap Interaksi Kompleks:** Mampu memodelkan kondisi bersyarat (misal: "JIKA kelerengan $> 15\%$ DAN litologi adalah breksi, MAKA lempung $= 60\%$").
    3. **Tahan Multikolinearitas dan Outlier:** Tidak mensyaratkan data berdistribusi normal (non-parametrik).
    4. **Menyediakan Metrik Kepentingan Variabel (*Variable Importance*):** Mengidentifikasi kovariat mana yang paling berkontribusi terhadap penurunan galat prediksi.
  * **Keterbatasan Utama:** Bersifat non-ekstrapolatif; tidak dapat memprediksi nilai tanah di luar rentang nilai data latih minimum dan maksimumnya.
* **Catatan Pemateri:**
  > "Random Forest bekerja seperti dewan pakar. Alih-alih mempercayai satu pohon keputusan tunggal yang mungkin bias, Random Forest membangun 500 pohon keputusan yang masing-masing melihat kombinasi data berbeda, lalu mengambil suara mayoritas atau rata-ratanya. Itulah mengapa prediksinya sangat stabil dan tangguh di lapangan."

---

### SLIDE 8: PEMODELAN HIBRIDA: REGRESSION KRIGING (RK)
* **Kategori:** Integrasi Geostatistik & ML
* **Judul:** Pemodelan Hibrida: Menggabungkan Machine Learning dan Geostatistik
* **Layout Visual:**
  * Diagram Dekomposisi Regression Kriging (Tren + Residual Spasial):
    ![Gambar 8.4: Dekomposisi Tren dan Residual Spasial dalam Regression Kriging](../assets/modul-8/M8-G04_residual-dan-regression-kriging.png)
    *Gambar 8.4: Dekomposisi Pemodelan Regression Kriging (RK): Komponen Tren Deterministik Lingkungan (via Random Forest) Ditambah Komponen Residual Spasial Terkorelasikan (via Ordinary Kriging).*
  * Komponen 1: Prediksi Tren Deterministik Lingkungan ($\hat{m}(s)$ via ML/RF).
  * Komponen 2: Variasi Residual Terkorelasikan Spasial ($\hat{e}(s)$ via Ordinary Kriging).
  * Hasil Penjumlahan: Prediksi Final $\hat{z}(s) = \hat{m}(s) + \hat{e}(s)$.
* **Poin Paparan:**
  * **Konsep Dasar Regression Kriging:**
    $$\hat{Z}(s) = \hat{m}(s) + \hat{e}(s)$$
    * $\hat{m}(s)$: Nilai tren tanah yang diprediksi oleh kovariat lingkungan (SCORPAN) menggunakan Random Forest atau regresi.
    * $\hat{e}(s)$: Nilai sisa (*residual*) pada titik sampel yang diinterpolasi menggunakan *Ordinary Kriging* berdasarkan semivariogram residual.
  * **Kapan Menggunakan RK?**
    * Ketika residual model ML masih memiliki struktur autokorelasi spasial (titik sampel yang berdekatan memiliki galat yang mirip).
    * RK mengembalikan akurasi lokal pada titik-titik pengamatan dan menyempurnakan prediksi di sekitarnya.
* **Catatan Pemateri:**
  > "Perhatikan Gambar 8.4. Algoritma Random Forest hebat dalam membaca tren lanskap, tetapi ia tidak tahu bahwa titik A dan titik B yang bersebelahan punya kedekatan spasial. Dengan Regression Kriging, galat sisa dari Random Forest kita interpolasi ulang dengan kriging. Ini menggabungkan kecerdasan buatan dengan hukum geostatistik Tobler!"

---

### SLIDE 9: BAHAYA AUTOKORELASI SPASIAL DALAM PEMBAGIAN DATA
* **Kategori:** Metodologi Validasi Kritis
* **Judul:** Jebakan Autokorelasi Spasial: Ilusi Akurasi Semu (*Data Leakage*)
* **Layout Visual:**
  * Komparasi Skema Pembagian Data Acak vs Spasial:
    ![Gambar 8.2: Skema Pembagian Data Acak vs Pembagian Blok Spasial](../assets/modul-8/M8-G02_skema-pembagian-data.png)
    *Gambar 8.2: Jebakan Autokorelasi Spasial: Pembagian Acak Sederhana (Memicu Kebocoran Data dan Akurasi Palsu) vs. Pembagian Blok Spasial (Spatial Block Partitioning yang Bebas Bias).*
  * Kiri: Pembagian Acak Sederhana (*Random Split*) $\rightarrow$ Titik uji berada tepat di sebelah titik latih (Jarak $< 50\ \text{m}$) $\rightarrow$ Kebocoran informasi spasial $\rightarrow$ Nilai $R^2$ tinggi palsu ($0.90$).
  * Kanan: Pembagian Blok Spasial (*Spatial Block Split*) $\rightarrow$ Satu blok utuh diisolasi sebagai data uji $\rightarrow$ Nilai $R^2$ realistis ($0.55$).
* **Poin Paparan:**
  * **Hukum Pertama Geografi Tobler:** Objek yang dekat lebih mirip dibandingkan objek yang jauh.
  * Jika sampel dibagi secara acak biasa (*random k-fold cross-validation*), titik uji akan bertetangga dekat dengan titik latih. Model akan 'mencontek' nilai tetangga terdekat, bukan memprediksi berdasarkan kovariat!
  * **Dampak Bahaya:** Model terlihat luar biasa akurat di atas kertas ($R^2 > 0.85$), tetapi saat dibawa ke afdeling baru yang belum disampel, prediksinya hancur berantakan (*model failure*).
* **Catatan Pemateri:**
  > "Ini adalah kesalahan paling umum dalam penelitian machine learning geospasial! Jika Anda membagi data latih dan uji secara acak biasa, Anda sedang membohongi diri sendiri. Titik uji Anda berjarak 20 meter dari titik latih, tentu saja modelnya bisa menebak dengan mudah. Untuk menguji apakah model kita benar-benar pintar, kita harus mengujinya di blok kebun yang terpisah jauh secara spasial!"

---

### SLIDE 10: METODOLOGI SPATIAL CROSS-VALIDATION
* **Kategori:** Validasi Spasial Bebas Bias
* **Judul:** Solusi Ilmiah: *Spatial Cross-Validation* dan *Block Partitioning*
* **Layout Visual:**
  * Partisi Blok Geografis Bebas Bias Spasial:
    ![Gambar 8.2: Skema Partisi Blok Spasial Bebas Bias](../assets/modul-8/M8-G02_skema-pembagian-data.png)
    *Gambar 8.2 (Panel Kanan): Skema Partisi Blok Geografis ($k$-Fold Spatial Cross-Validation) untuk Menilai Kemampuan Generalisasi Ekstrapolasi Model Antar-Afdeling.*
  * Diagram Partisi Blok Geografis ($5\text{-Fold Spatial Block}$): Area perkebunan dibagi menjadi 5 klaster spasial besar; pada setiap iterasi, 4 blok menjadi data latih dan 1 blok utuh menjadi data uji independen.
* **Poin Paparan:**
  * **Spatial Block Cross-Validation:**
    * Memisahkan data latih dan data uji berdasarkan batas blok geografis atau jarak pemisah (*buffer distance*) yang melebihi rentang autokorelasi spasial (*range* semivariogram).
  * **Mengukur Kemampuan Generalisasi Sejati (*True Spatial Transferability*):**
    * Menguji apakah model yang dilatih di Afdeling 1 mampu memprediksi tanah di Afdeling 4 dengan akurat tanpa memerlukan sampel bor baru.
  * Menjadi jaminan integritas bahwa model siap dipakai dalam skala operasional estate.
* **Catatan Pemateri:**
  > "Dengan Spatial Cross-Validation, kita melatih model di Kebun A, lalu kita uji kemampuannya menebak tanah di Kebun B yang belum pernah dilihat oleh algoritma. Angka akurasi yang keluar dari metode ini mungkin terlihat lebih rendah, tetapi itulah akurasi nyata yang jujur di lapangan!"

---

### SLIDE 11: ALUR KERJA LENGKAP PEMODELAN DSM
* **Kategori:** *End-to-End Pipeline*
* **Judul:** Alur Kerja Baku Pemodelan DSM: Dari Data Mentah Hingga Peta Prediksi
* **Layout Visual:**
  * Diagram Alir Lengkap Pemodelan DSM:
    ![Gambar 8.3: Alur Kerja Baku Pemodelan DSM](../assets/modul-8/M8-G03_alur-pemodelan-dsm.png)
    *Gambar 8.3: Diagram Alir Lengkap Pemodelan Digital Soil Mapping: Dari Standardisasi Profil Tanah dan Ekstraksi Kovariat hingga Penalaan Model, Prediksi Grid, dan Kuantifikasi Ketidakpastian.*
  * Rincian 7 Tahap Pemodelan:
    * Tahap 1: Standardisasi Data Titik Tanah & Kedalaman Baku.
    * Tahap 2: Ekstraksi Nilai Kovariat Multisumber pada Lokasi Titik (*Spatial Overlay*).
    * Tahap 3: Penyusunan Matriks Pemodelan ($X$ Kovariat, $Y$ Sifat Tanah).
    * Tahap 4: Penalaan Hiperparameter (*Hyperparameter Tuning*) via Spatial CV.
    * Tahap 5: Pelatihan Model Akhir (*Model Fitting*).
    * Tahap 6: Prediksi Spasial Menyeluruh ke Seluruh Grid Piksel (*Spatial Application*).
    * Tahap 7: Kuantifikasi Ketidakpastian Prediksi & Pembuatan Peta Luaran.
* **Poin Paparan:**
  * Alur kerja ini menghubungkan seluruh data yang telah dipelajari dari Modul 1 hingga 7.
  * Tahap ekstraksi (*overlay*) mengubah tumpukan berkas TIF menjadi tabel data tabular yang siap diproses oleh pustaka Python (`scikit-learn`, `xgboost`, `spatial-cross-validation`).
* **Catatan Pemateri:**
  > "Bapak dan Ibu, Gambar 8.3 adalah peta arsitektur yang akan kita eksekusi pada praktik Python di Google Colab hari ini. Dari tumpukan layer TIF dan koordinat GPS bor tanah, kita ekstraksi menjadi tabel data, kita latih model Random Forest-nya, lalu kita instruksikan model tersebut merender peta prediksi seluruh blok."

---

### SLIDE 12: STANDARDISASI INTERVAL KEDALAMAN TANAH
* **Kategori:** Harmonization Standar Internasional
* **Judul:** Menstandarkan Lapisan Profil: Spesifikasi Kedalaman GlobalSoilMap
* **Layout Visual:**
  * Diagram Harmonisasi Kedalaman Equal-Area Spline & GlobalSoilMap:
    ![Gambar 8.6: Harmonisasi Kedalaman Tanah dengan Equal-Area Spline dan 6 Interval GlobalSoilMap](../assets/modul-8/M8-G06_interval-kedalaman-globalsoilmap.png)
    *Gambar 8.6: Harmonisasi Lapisan Profil Tanah: Dari Horizon Lapangan Tak Beraturan melalui Fungsi Kontinu Equal-Area Quadratic Spline Menuju 6 Interval Kedalaman Baku GlobalSoilMap ($0–5$, $5–15$, $15–30$, $30–60$, $60–100$, $100–200\ \text{cm}$).*
  * Rincian 6 Interval Baku GlobalSoilMap (Poggio et al. 2021 / SoilGrids 2.0):
    * Lapisan 1: $0–5\ \text{cm}$
    * Lapisan 2: $5–15\ \text{cm}$
    * Lapisan 3: $15–30\ \text{cm}$
    * Lapisan 4: $30–60\ \text{cm}$
    * Lapisan 5: $60–100\ \text{cm}$
    * Lapisan 6: $100–200\ \text{cm}$
* **Poin Paparan:**
  * Sampel tanah lapangan sering diambil pada kedalaman yang tidak seragam (misal ada yang $0–20\ \text{cm}$, ada yang $10–30\ \text{cm}$).
  * **Penyetaraan Kedalaman (*Depth Harmonization*):**
    * Menggunakan fungsi spline kuadratik (*equal-area quadratic splines*) untuk merekonstruksi kurva sifat tanah kontinu terhadap kedalaman sebelum dimodelkan (Malone et al. 2017).
    * Diperlukan model 3D DSM terpisah untuk setiap interval kedalaman agar rekomendasi agronomi sesuai dengan stratifikasi perakaran sawit.
* **Catatan Pemateri:**
  > "Jangan pernah mencampur sampel kedalaman 0–10 cm dengan sampel 20–40 cm ke dalam satu kolom model yang sama. Sifat tanah berubah drastis menurut kedalaman. Kita mengadopsi standar internasional GlobalSoilMap yang membagi profil menjadi lapisan baku, sehingga kita bisa menghasilkan peta lempung lapisan atas dan peta lempung lapisan perakaran dalam secara terpisah."

---

### SLIDE 13: ENAM METRIK STATISTIK VALIDASI MODEL
* **Kategori:** Evaluasi Kinerja Kuantitatif
* **Judul:** Mengukur Kualitas Prediksi: Enam Metrik Validasi Kunci
* **Layout Visual:** Tabel Rumus & Kriteria Evaluasi (Berdasarkan Tabel 8.3 Modul):
* **Poin Paparan:**
  1. **Mean Error (ME / Bias):** $\frac{1}{n}\sum (\hat{y}_i - y_i) \rightarrow$ Ideal $= 0$. Mengukur kecenderungan model menaksir terlalu tinggi (positif) atau terlalu rendah (negatif).
  2. **Mean Absolute Error (MAE):** $\frac{1}{n}\sum |\hat{y}_i - y_i| \rightarrow$ Besar galat rata-rata dalam satuan asli (misal: $\pm 3.2\%$ lempung).
  3. **Root Mean Square Error (RMSE):** $\sqrt{\frac{1}{n}\sum (\hat{y}_i - y_i)^2} \rightarrow$ Lebih peka terhadap kesalahan prediksi yang bernilai ekstrem.
  4. **Model Efficiency Coefficient (MEC / Nash-Sutcliffe):**
     $$\text{MEC} = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2} \rightarrow \text{Ideal } = 1.0$$
     * Jika $\text{MEC} \le 0$, model Anda **lebih buruk** daripada hanya menebak nilai rata-rata sampel!
  5. **Koefisien Determinasi ($R^2$):** Proporsi keragaman data yang berhasil dijelaskan.
  6. **Lin's Concordance Correlation Coefficient (CCC):** Mengukur presisi sekaligus akurasi relatif terhadap garis 1:1 sempurna.
* **Catatan Pemateri:**
  > "Tolong jangan hanya melaporkan nilai R-square! Nilai R-square bisa menipu jika ada bias konstan. Metrik paling jujur dalam pedometrik adalah MEC (Model Efficiency Coefficient) dan RMSE. Jika nilai MEC model Anda negatif, itu artinya peta yang dihasilkan model machine learning Anda lebih sesat daripada sekadar mengambil nilai rata-rata dari seluruh kebun!"

---

### SLIDE 14: MEMAHAMI RESIDUAL DAN STRUKTUR SPASIALNYA
* **Kategori:** Analisis Galat Spasial
* **Judul:** Anatomi Galat: Analisis Semivariogram Residual Model
* **Layout Visual:**
  * Diagram Semivariogram Residual dan Struktur Spasial:
    ![Gambar 8.4: Analisis Semivariogram Residual](../assets/modul-8/M8-G04_residual-dan-regression-kriging.png)
    *Gambar 8.4 (Panel Semivariogram): Pemodelan Struktur Spasial Residual: Pure Nugget Effect (Galat Acak Murni) vs. Struktur Berpola (Sill & Range) yang Memerlukan Regression Kriging.*
  * Kiri: Plot Sebaran Titik Residual ($e_i = y_i - \hat{y}_i$) di Peta Kebun.
  * Kanan: Kurva Semivariogram Eksperimental Residual $\gamma(h)$ lengkap dengan parameter *Nugget*, *Sill*, dan *Range*.
* **Poin Paparan:**
  * Galat (*residual*) model bukanlah sampah, melainkan sumber informasi berharga.
  * **Uji Autokorelasi Spasial Residual:**
    * Jika semivariogram residual berbentuk garis datar murni (*pure nugget effect*), berarti model ML telah mengekstraksi seluruh pola spasial yang ada; sisa galat murni derau acak tak berpola.
    * Jika semivariogram residual menunjukkan kenaikan teratur menuju *sill*, berarti masih ada pola spasial lokal yang tertinggal $\rightarrow$ Wajib dilanjutkan dengan **Regression Kriging**!
* **Catatan Pemateri:**
  > "Setelah model selesai memprediksi, jangan langsung puas. Hitung nilai residualnya dan buat semivariogramnya. Jika residualnya masih memiliki struktur spasial, artinya ada faktor pembentuk tanah lokal yang belum tertangkap oleh citra satelit Anda. Di situlah kita mengaktifkan kriging residual."

---

### SLIDE 15: KUANTIFIKASI KETIDAKPASTIAN PREDIKSI (QRF)
* **Kategori:** Pemodelan Probabilistik
* **Judul:** Pemodelan Ketidakpastian: *Quantile Regression Forests* (QRF)
* **Layout Visual:**
  * Kiri: Konsep Distribusi Probabilitas Prediksi Per-Piksel (Bukan sekadar angka tunggal, melainkan kurva lonceng persentil ke-5, 50, dan 95).
  * Kanan: Peta Interval Prediksi 90% (Lebar interval $=$ Batas Atas 95% $-$ Batas Bawah 5%).
* **Poin Paparan:**
  * Setiap prediksi spasial tanah **selalu mengandung ketidakpastian** akibat variabilitas mikro, galat posisi GPS, dan resolusi citra.
  * Algoritma **Quantile Regression Forests (QRF)** tidak hanya menduga nilai rata-rata (*mean*), tetapi menghitung seluruh distribusi probabilitas kumulatif pada setiap piksel.
  * **Interval Prediksi 90% (*90% Prediction Interval*):**
    * Rentang nilai di mana tanah aktual memiliki peluang $90\%$ berada di dalamnya.
    * Interval sempit: Prediksi sangat yakin (*high confidence*).
    * Interval sangat lebar: Prediksi tidak pasti (*high uncertainty*).
* **Catatan Pemateri:**
  > "Seorang ilmuwan yang jujur tidak pernah mengatakan: 'Kadar lempung di titik ini pasti 42,5%'. Ilmuwan yang jujur mengatakan: 'Model menduga kadar lempung 42,5%, dengan keyakinan 90% berada di rentang 39% hingga 46%'. QRF memberi kita peta batas bawah dan batas atas keyakinan tersebut."

---

### SLIDE 16: VALIDASI INTERVAL PREDIKSI DENGAN PICP
* **Kategori:** Kalibrasi Ketidakpastian
* **Judul:** Menguji Kejujuran Ketidakpastian: Metrik PICP
* **Layout Visual:**
  * Grafik Evaluasi Interval Prediksi PICP:
    ![Gambar 8.5: Evaluasi Interval Prediksi PICP](../assets/modul-8/M8-G05_interval-prediksi-dan-aoa.png)
    *Gambar 8.5(a): Evaluasi Kejujuran Ketidakpastian Menggunakan Metrik PICP: Sebaran Nilai Observasi Uji Lapangan terhadap Rentang Interval Prediksi 90% dari Quantile Regression Forests (QRF).*
  * Batang Vertikal Abu-abu: Interval prediksi per titik sampel uji.
  * Titik Hitam: Nilai tanah observasi laboratorium nyata.
  * Titik Merah di Luar Batang: Nilai observasi yang meleset dari interval prediksi.
* **Poin Paparan:**
  * **Prediction Interval Coverage Probability (PICP):**
    $$\text{PICP} = \frac{1}{n}\sum_{i=1}^n \mathbf{1}\left(L_i \le y_i \le U_i\right) \times 100\%$$
    * Proporsi sampel validasi nyata yang jatuh di dalam rentang interval prediksi $[L_i, U_i]$.
  * **Kriteria Evaluasi Kejujuran Model:**
    * Jika kita merancang interval prediksi nominal $90\%$, maka nilai PICP idealnya harus tepat berada di sekitar **$90\%$**.
    * Jika $\text{PICP} \ll 90\%$ (misal hanya $60\%$): Model terlalu percaya diri (*overconfident* / meremehkan ketidakpastian).
    * Jika $\text{PICP} \gg 90\%$ (misal $99\%$): Interval terlalu lebar dan tidak berguna secara praktis (*underconfident*).
* **Catatan Pemateri:**
  > "Lihat Gambar 8.5(a). Dari 100 titik uji independen kita, berapa banyak yang jatuh di dalam rentang kurung prediksi kita? Jika tepat 90 titik yang masuk, maka model estimasi ketidakpastian kita sempurna dan jujur secara statistik!"

---

### SLIDE 17: BATAS KEBERLAKUAN MODEL: AREA OF APPLICABILITY (AOA)
* **Kategori:** Kendali Mutu Spasial Mutakhir
* **Judul:** Batas Wilayah Keberlakuan: Konsep *Area of Applicability* (AOA)
* **Layout Visual:**
  * Peta Wilayah Keberlakuan Model (AOA):
    ![Gambar 8.5: Peta Wilayah Keberlakuan Model (AOA)](../assets/modul-8/M8-G05_interval-prediksi-dan-aoa.png)
    *Gambar 8.5(b): Peta Area of Applicability (AOA) Berdasarkan Indeks Ketidakmiripan (DI) Meyer & Pebesma (2021): Memisahkan Area Validasi Andal vs Area Ekstrapolasi Berisiko.*
  * Area Hijau: *Inside AOA* (Kombinasi kovariat serupa dengan data latih; prediksi valid dan dapat dipercaya).
  * Area Merah Berarsir: *Outside AOA* (Wilayah ekstrapolasi berbahaya; kombinasi lingkungan belum pernah disampel).
* **Poin Paparan:**
  * Algoritma *machine learning* sering menghasilkan nilai prediksi pada area yang kovariat lingkungannya sangat berbeda dari data latih (*extrapolation*).
  * **Dissimilarity Index (DI) & AOA (Meyer & Pebesma 2021):**
    * Mengukur jarak multi-dimensi ternormalisasi antara setiap piksel kebun dengan sebaran titik sampel di ruang kovariat berbobot.
    * Mengidentifikasi ambang batas di mana model tidak lagi memiliki dasar data untuk memprediksi.
  * **Pemberitahuan Tegas untuk Manajemen:** Area di luar AOA **dilarang digunakan** untuk keputusan agronomi sebelum dilakukan penambahan titik sampel tanah baru!
* **Catatan Pemateri:**
  > "Ini adalah konsep paling mutakhir dari Meyer dan Pebesma (2021). Bayangkan Anda melatih model tanah hanya di kebun dataran rendah, lalu model itu Anda terapkan untuk memprediksi puncak gunung berbatu. Komputer tetap akan mengeluarkan angka, tapi angkanya adalah omong kosong! Peta AOA menandai area merah tersebut: 'Dilarang percaya pada prediksi di area ini karena data latih kita belum pernah mencakupnya'."

---

### SLIDE 18: DARI PETA KONTINU KE ZONA PENGELOLAAN SAWIT
* **Kategori:** Aplikasi Agronomi Presisi
* **Judul:** Dari Peta Digital ke Aksi Lapangan: Penyusunan Zona Pengelolaan
* **Layout Visual:** Alur Konversi Peta Prediksi Menjadi Peta Rekomendasi Agronomi:
  * Peta Grid Kontinu Lempung ($25–65\%$) $\rightarrow$ *Spatial Clustering* ($k\text{-means} / \text{fuzzy c-means}$) $\rightarrow$ Batas Blok Manajemen Homogen $\rightarrow$ Peta Dosis Rekomendasi Pemupukan Spesifik Lokasi (*Variable Rate Application - VRA*).
* **Poin Paparan:**
  * Peta raster kontinu dengan resolusi 10 meter tidak dapat langsung dieksekusi oleh mandor pemupukan di lapangan (terlalu rumit).
  * **Delineasi Zona Pengelolaan (*Management Zones*):**
    * Mengelompokkan variabilitas sifat tanah kontinu menjadi 3–4 zona pengelolaan yang seragam secara fungsional.
    * Contoh: Zona Rendahan Rawan Genangan (butuh drainase), Zona Punggungan Defisiensi Kalium (butuh penambahan MOP), Zona Normal.
  * Memandu mesin penabur pupuk otomatis (*fertilizer spreader*) atau tim pemupuk manual dengan dosis presisi per afdeling.
* **Catatan Pemateri:**
  > "Tujuan akhir pelatihan ini bukan sekadar menghasilkan peta cantik di laptop. Tujuannya adalah efisiensi operasional kebun PT SMART. Dari peta kontinu DSM, kita mengelompokkannya menjadi Zona Manajemen Pupuk. Blok yang lempungnya tinggi mendapat dosis tertentu, blok yang berpasir mendapat dosis terpisah. Inilah inti dari Precision Agriculture!"

---

### SLIDE 19: SIKLUS PEMETAAN TANAH ADAPTIF
* **Kategori:** Siklus Keberlanjutan Data
* **Judul:** Siklus Pemetaan Adaptif (*Adaptive Soil Sampling Strategy*)
* **Layout Visual:** Diagram Siklus Tertutup (*Closed-Loop Feedback System*):
  * Survei Awal / PSS $\rightarrow$ Bangun Model DSM $\rightarrow$ Peta Prediksi & Peta Ketidakpastian $\rightarrow$ Peta AOA $\rightarrow$ Penempatan Sampel Tambahan Terfokus pada Wilayah Ketidakpastian Tinggi $\rightarrow$ Kalibrasi Ulang Model $\rightarrow$ Akurasi Model Meningkat Drastis.
* **Poin Paparan:**
  * Pemetaan tanah digital bukanlah proses satu kali selesai, melainkan **siklus belajar yang terus menyempurna**.
  * **Strategi Sampling Adaptif (*Adaptive Sampling*):**
    * Alih-alih mengebor secara acak, anggaran survei tahun depan diarahkan khusus ke wilayah yang memiliki nilai ketidakpastian tinggi (*high uncertainty*) atau di luar wilayah AOA.
    * Dengan menambah sedikit sampel di lokasi yang tepat, ketelitian peta tanah seluruh kebun melonjak signifikan dengan biaya termurah.
* **Catatan Pemateri:**
  > "Jika tahun depan manajemen memberi anggaran untuk 50 sampel bor tanah tambahan, di mana Anda harus mengebor? Jangan mengebor di tempat yang sudah dipahami model! Lihat peta ketidakpastian kita. Bor-lah di lokasi yang warnanya merah, di mana model kita paling ragu-ragu. Begitu data baru masuk, model diperbarui, dan kebun kita menjadi semakin presisi setiap tahunnya."

---

### SLIDE 20: RANGKUMAN & PERSIAPAN PRAKTIK MACHINE LEARNING
* **Kategori:** Penutup Sesi & Transisi Studio
* **Judul:** Rangkuman Kunci & Memulai Praktik Machine Learning Hari ke-3
* **Layout Visual:** Poin Evaluasi Kunci & Tangkapan Layar Lingkungan Google Colab Python.
* **Poin Paparan:**
  * **Intisari Pembelajaran DSM:**
    1. SCORPAN adalah kerangka kerja pengikatan data spasial lingkungan ke sifat tanah.
    2. *Random Forest* dan *Regression Kriging* memberikan kombinasi terbaik untuk memodelkan hubungan spasial non-linear.
    3. *Spatial Cross-Validation* adalah syarat mutlak untuk evaluasi model yang jujur dan bebas bias autokorelasi.
    4. Setiap peta prediksi wajib disertai peta ketidakpastian (QRF) dan batas keberlakuan (AOA).
  * **Agenda Praktik Studio Hari Ini (Dipandu Ferry):**
    * Penyiapan kovariat SCORPAN di QGIS dan Python.
    * Pelatihan model Random Forest untuk prediksi tekstur tanah.
    * Validasi akurasi, visualisasi semivariogram residual, dan ekspor peta GeoTIFF.
* **Catatan Pemateri:**
  > "Bapak dan Ibu sekalian, teori telah selesai secara tuntas dari Modul 1 sampai Modul 8. Sekarang adalah waktunya kita membuktikan seluruh teori ini dengan baris-baris kode nyata di komputer Anda. Bersama Mas Ferry, kita akan menjalankan Google Colab untuk melatih model Random Forest dan menghasilkan peta DSM pertama Anda hari ini. Selamat berpraktik, terima kasih, dan salam pedometrik!"
