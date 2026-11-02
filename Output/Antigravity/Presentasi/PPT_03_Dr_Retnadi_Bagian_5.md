# RANCANGAN PRESENTASI (SLIDE DECK) PELATIHAN
## Bagian 5: Bare Soil Detection & Information Extraction

**Pemateri:** Dr. Retnadi Heru Jatmiko, M.Sc.  
**Institusi:** Pusat Studi Pengelolaan Sumber Daya Lahan (PS2DL), Universitas Gadjah Mada  
**Target Audiens:** Staf Teknis, Agronomis, Peneliti, dan Pengelola Perkebunan Kelapa Sawit (PT SMART Tbk)  
**Alokasi Waktu:** Sesi Ceramah Teori (60 Menit)  
**Dokumen Acuan:** `Modul Pelatihan SMART Pemanfaatan RS dan DSM.docx` (Bab 5)

---

### PANDUAN VISUAL & IDENTITAS SLIDE (DESIGN SYSTEM)
* **Warna Utama:** Biru Navy UGM (`#1F3A5F`), Hijau Sawit (`#2A9D8F`), Oranye/Cokelat Tanah Terbuka (`#E07B39` / `#8C5A3C`), Kuning Emas (`#F2C14E`).
* **Tipografi:** Sans-serif modern (Calibri / Carlito / Arial), kontras tinggi untuk keterbacaan formula dan diagram alir.
* **Prinsip Tampilan:** Fokus pada perbandingan kurva pantulan spektral (*spectral unmixing*), grafik ruang spektral *Soil Line*, dan diagram alir pengolahan deret waktu (*multitemporal compositing*).

---

## DAFTAR SLIDE & STRUKTUR MATERI

```
BAGIAN 5: BARE SOIL DETECTION & INFORMATION EXTRACTION (Slide 1–15)
  - Slide 1: Judul & Pembuka Sesi
  - Slide 2: Mengapa Deteksi Tanah Terbuka Menjadi Prasyarat Mutlak DSM?
  - Slide 3: Perilaku Spektral Tiga Permukaan Kunci (Tanah Terbuka vs. Vegetasi Hijau vs. Serasah Kering)
  - Slide 4: Masalah Pencampuran Spektral (Spectral Mixing) dalam Satu Piksel
  - Slide 5: Konsep Soil Line (Garis Tanah) pada Ruang Spektral Merah–NIR
  - Slide 6: Ragam Indeks Deteksi Tanah Terbuka (NDVI, SAVI, BSI, NBR2, NDTI)
  - Slide 7: Peran Saluran SWIR2 dalam Memisahkan Tanah Murni dari Serasah Tanaman
  - Slide 8: Penentuan Ambang Batas (Thresholding): Ambang Global vs. Kalibrasi Lokal
  - Slide 9: Tantangan Ekstrem pada Perkebunan Kelapa Sawit: Kanopi Tertutup Sepanjang Tahun
  - Slide 10: Jendela Peluang Keterbukaan Tanah di Perkebunan Sawit (Replanting, Piringan, Gawangan)
  - Slide 11: Dinamika Spektral Blok Peremajaan Sawit dengan Kacangan Penutup Tanah (LCC)
  - Slide 12: Pendekatan Deret Waktu (Multitemporal): Dari Citra Tunggal ke Komposit Jangka Panjang
  - Slide 13: Alur Kerja Algoritma Komposit Tanah Terbuka (GEOBAT / Barest Pixel Composite)
  - Slide 14: Produk Akhir: Komposit Reflektansi Murni, Peta Frekuensi Keterbukaan, dan Ketidakpastian
  - Slide 15: Rangkuman & Kesiapan Menuju Sesi Praktik Studio
```

---

## RINCIAN KONTEN PER SLIDE

---

### SLIDE 1: JUDUL & PEMBUKA
* **Kategori:** Cover Presentation
* **Judul Utama:** Bare Soil Detection & Information Extraction
* **Sub-judul:** Teknik Ekstraksi Informasi Spektral Tanah Terbuka di Bawah Tantangan Kanopi Rapat Perkebunan Kelapa Sawit
* **Identitas:** Dr. Retnadi Heru Jatmiko, M.Sc. | Pusat Studi Pengelolaan Sumber Daya Lahan (PS2DL) UGM
* **Layout Visual:**
  * Kiri: Judul presentasi tebal, identitas pemateri, logo UGM & PS2DL.
  * Kanan: Visualisasi satelit perbandingan antara blok sawit tua yang hijau pekat dengan blok replanting yang terbuka berwarna tanah kemerahan, dilengkapi skema grafik spektrum tanah terbuka.
* **Poin Paparan:**
  * Menembus tantangan kanopi vegetasi untuk memperoleh sinyal spektral tanah murni.
  * Memahami matematika indeks spektral dan algoritma deret waktu (*time-series analysis*) untuk pemetaan tanah digital.
* **Catatan Pemateri (Speaker Notes):**
  > "Selamat pagi Bapak dan Ibu sekalian. Kita telah mempelajari dasar-dasar penginderaan jauh dan bagaimana sifat tanah berinteraksi dengan cahaya di sesi sebelumnya. Sekarang kita menghadapi kenyataan lapangan perkebunan kelapa sawit: sebagian besar tanah kita tertutup oleh tajuk sawit yang rimbun! Bagaimana cara satelit bisa mengekstrak sifat tanah jika tanahnya tidak terlihat? Di Modul 5 ini, kita akan membedah teknologi Bare Soil Detection."

---

### SLIDE 2: URGENSI DETEKSI TANAH TERBUKA UNTUK DSM
* **Kategori:** Latar Belakang & Landasan Konsep
* **Judul:** Mengapa Deteksi Tanah Terbuka Menjadi Prasyarat Mutlak?
* **Layout Visual:** Diagram Sebab-Akibat 3 Tingkat:
  * Fakta Fisik: Sensor optik satelit hanya merekam radiasi dari permukaan teratas ($0–2\ \text{mm}$).
  * Masalah: Adanya daun hijau atau serasah kering mendistorsi sinyal pantulan mineral tanah.
  * Solusi DSM: Penapisan piksel tanah terbuka (*bare soil masking*) untuk menghasilkan data kovariat tanah murni (*pure soil reflectance*) bebas vegetasi (Demattê et al. 2020; Diek et al. 2017).
* **Poin Paparan:**
  * **Definisi Tanah Terbuka (*Bare Soil*):** Permukaan abiotik alami (tanah, pasir, singkapan) yang vegetasi penutupnya tidak ada atau sangat minimal (Demattê et al. 2020).
  * Menghindari kesalahan estimasi sifat tanah: jika piksel bervegetasi diolah dengan rumus lempung atau bahan organik, hasilnya adalah artefak klorofil, bukan sifat tanah.
  * Ekstraksi tanah terbuka memungkinkan pemetaan sifat tanah lempung, pasir, debu, dan C-organik secara langsung pada skala regional (Diek et al. 2017).
* **Catatan Pemateri:**
  > "Ingat kembali materi Dr. Anggri: sensor satelit optik tidak punya sinar tembus rontgen. Satelit hanya merekam apa yang terpapar di udara. Jika yang terpapar adalah daun sawit, maka yang terukur adalah klorofil daun. Untuk mengukur lempung dan bahan organik tanah, kita wajib menyaring piksel-piksel yang benar-benar memperlihatkan tanah terbuka."

---

### SLIDE 3: PERILAKU SPEKTRAL TIGA PERMUKAAN KUNCI
* **Kategori:** Fisika Spektroskopi Komparatif
* **Judul:** Membedakan Sinyal Spektral: Tanah, Vegetasi Hijau, dan Serasah Kering
* **Layout Visual:**
  * Kurva Pantulan Spektral Tiga Permukaan Kunci:
    ![Gambar 5.1: Spektrum Pantulan Tanah, Vegetasi, dan Serasah](../assets/modul-5/M5-G01_spektrum-tanah-vegetasi-serasah.png)
    *Gambar 5.1(a): Perilaku Spektroskopi Tanah Terbuka vs. Vegetasi Hijau Sehat vs. Serasah Kering/Residu Tanaman pada Rentang $0.4–2.5\ \mu\text{m}$.*
  * Kurva Cokelat: Tanah terbuka (naik kontinu dari tampak ke SWIR1).
  * Kurva Hijau: Vegetasi hijau sehat (puncak hijau $0.55\ \mu\text{m}$, serapan merah $0.66\ \mu\text{m}$, lonjakan *red edge* ke NIR $> 0.7\ \mu\text{m}$).
  * Kurva Oranye Putus-putus: Serasah kering / sisa tanaman (*crop residues/dead biomass*).
* **Poin Paparan:**
  * **1. Tanah Terbuka:** Reflektansi meningkat bertahap dari kanal biru hingga SWIR1. Penyerapan di wilayah tampak dipicu oksida besi dan bahan organik; pantulan tinggi di NIR dan SWIR1 dipicu kuarsa.
  * **2. Vegetasi Hijau:** Kontras ekstrem antara serapan klorofil di kanal merah dengan pantulan tinggi di inframerah dekat (NIR).
  * **3. Serasah Kering (*Plant Residue*):**
    * Tidak memiliki klorofil aktif (tidak ada lonjakan tajam *red edge*).
    * Namun, memiliki serapan diagnostik selulosa dan lignin di panjang gelombang $2.1\ \mu\text{m}$ dan $2.3\ \mu\text{m}$ pada kanal SWIR2!
* **Catatan Pemateri:**
  > "Lihat Gambar 5.1(a) di layar. Membedakan tanah terbuka dengan vegetasi hijau itu sangat mudah: cukup gunakan indeks NDVI. Namun, tantangan terbesar kita di kebun sawit adalah membedakan tanah terbuka dengan SERASAH KERING atau pelepah mati. Serasah kering kurvanya sepintas mirip tanah, tetapi ia memiliki 'lembah' serapan lignin dan selulosa di SWIR2. Inilah celah fisika yang kita manfaatkan!"

---

### SLIDE 4: MASALAH PENCAMPURAN SPEKTRAL (*SPECTRAL MIXING*)
* **Kategori:** Analisis Sub-Piksel
* **Judul:** Masalah Pencampuran Spektral dalam Satu Piksel Lapangan
* **Layout Visual:**
  * Analisis Spektrum Campuran Sub-Piksel:
    ![Gambar 5.1: Dinamika Spektrum Campuran NDVI dan NBR2](../assets/modul-5/M5-G01_spektrum-tanah-vegetasi-serasah.png)
    *Gambar 5.1(b): Pengaruh Fraksi Tutupan Serasah dan Vegetasi terhadap Respon Indeks NDVI dan NBR2 pada Spektrum Campuran.*
  * Kiri: Ilustrasi piksel Sentinel-2 ($10 \times 10\ \text{m}$) di perkebunan yang mencakup $40\%$ tajuk pelepah sawit, $30\%$ rumput penutup, $20\%$ serasah kering, dan $10\%$ tanah terbuka.
  * Kanan: Grafik Dinamika Indeks NDVI vs NBR2 pada Spektrum Campuran.
* **Poin Paparan:**
  * Sinyal yang terekam oleh satu piksel satelit adalah nilai rata-rata tertimbang (*linear spectral mixing*) dari seluruh objek di dalam luasan $100\ \text{m}^2$.
  * Ketika tutupan vegetasi hijau menurun, nilai NDVI turun, tetapi nilai BSI dan NBR2 bergerak secara non-linear bergantung pada proporsi serasah kering (Gambar 5.1b).
  * **Peringatan Teknis:** Piksel dengan nilai NDVI rendah ($< 0.25$) belum tentu tanah terbuka murni; piksel tersebut bisa berupa tumpukan serasah kering atau tanaman mati tebas!
* **Catatan Pemateri:**
  > "Satu piksel Sentinel-2 berukuran 10 kali 10 meter. Di lapangan kebun sawit, luasan 100 meter persegi itu bisa berisi pohon sawit, gawangan, piringan, dan tumpukan pelepah mati sekaligus. Sinyal yang kita terima adalah sinyal 'gado-gado' (campuran). Tugas kita adalah mencari piksel yang paling murni tanahnya."

---

### SLIDE 5: KONSEP SOIL LINE PADA RUANG SPEKTRAL MERAH–NIR
* **Kategori:** Teori Transformasi Spektral
* **Judul:** Garis Tanah (*Soil Line*): Dasar Geometris Pemisahan Vegetasi
* **Layout Visual:**
  * Scatter Plot Ruang Spektral Merah vs. NIR:
    ![Gambar 5.2: Garis Tanah pada Ruang Spektral Merah-NIR](../assets/modul-5/M5-G02_garis-tanah-ruang-merah-nir.png)
    *Gambar 5.2: Konsep Garis Tanah (Soil Line) pada Ruang Spektral Merah vs. NIR (Berdasarkan Richardson & Wiegand, 1977; Baret et al., 1993).*
  * Sumbu X: Reflektansi Kanal Merah ($R$).
  * Sumbu Y: Reflektansi Kanal Inframerah Dekat (NIR).
  * Garis Miring Dasar: *Soil Line* ($NIR = a \cdot R + b$).
  * Awan Titik di Atas Garis: Vegetasi hijau (bergerak menjauh ke arah sumbu NIR).
  * Titik-titik Berimpit pada Garis: Berbagai variasi tanah (dari tanah basah gelap di dekat sumbu 0 hingga tanah kering terang di ujung atas).
* **Poin Paparan:**
  * **Persamaan Garis Tanah (*Soil Line*):**
    $$\text{NIR} = a \cdot R + b$$
    * Hubungan linier alami antara pantulan merah dan NIR untuk tanah tanpa vegetasi.
    * Parameter $a$ (kemiringan) dan $b$ (intersep) merupakan karakteristik khas jenis tanah setempat.
  * **Makna Fisis:** Semua tanah terbuka (apapun kelembapannya) akan jatuh tepat di atas atau sangat dekat dengan garis ini. Semakin banyak vegetasi hijau yang tumbuh, titik piksel akan bergeser menjauh tegak lurus ke arah atas (*perpendicular distance*).
* **Catatan Pemateri:**
  > "Konsep *Soil Line* adalah salah satu pilar terindah dalam remote sensing. Jika kita memplot kanal Merah dan NIR dari tanah kosong, semua titik tanah—mulai dari tanah gambut basah yang hitam hingga tanah pasiran kering yang putih—akan berbaris rapi membentuk satu garis lurus. Jarak tegak lurus dari garis inilah yang kita ukur sebagai keberadaan tanaman."

---

### SLIDE 6: RAGAM INDEKS DETEKSI TANAH TERBUKA
* **Kategori:** Algoritma & Transformasi Matematika
* **Judul:** Indeks Spektral Utama untuk Deteksi Tanah Terbuka
* **Layout Visual:** Tabel Ringkas Berdasarkan Tabel 5.1 Modul (Indeks | Formula Sentinel-2 | Fungsi & Pemanfaatan).
* **Poin Paparan:**
  1. **Normalized Difference Vegetation Index (NDVI):**
     $$\text{NDVI} = \frac{\text{B8} - \text{B4}}{\text{B8} + \text{B4}} \quad (\text{Ambang: } < 0.25 \text{ atau } -0.1 \le \text{NDVI} \le 0.25)$$
     * Menyaring vegetasi hijau fotosintesis aktif.
  2. **Soil Adjusted Vegetation Index (SAVI):**
     $$\text{SAVI} = \frac{1.5 \times (\text{B8} - \text{B4})}{\text{B8} + \text{B4} + 0.5}$$
     * Meredam pengaruh latar belakang tanah pada wilayah dengan kanopi jarang/awal tanam.
  3. **Bare Soil Index (BSI - Rikimaru et al. 2002):**
     $$\text{BSI} = \frac{(\text{B11} + \text{B4}) - (\text{B8} + \text{B2})}{(\text{B11} + \text{B4}) + (\text{B8} + \text{B2})}$$
     * Nilai meningkat tajam seiring bertambahnya luas tanah terbuka tanpa penutup.
  4. **Normalized Burn Ratio 2 (NBR2):**
     $$\text{NBR2} = \frac{\text{B11} - \text{B12}}{\text{B11} + \text{B12}}$$
     * Kunci pemisah antara tanah terbuka sejati dan serasah kering!
* **Catatan Pemateri:**
  > "Tolong perhatikan indeks BSI (Bare Soil Index). Rumusnya mengombinasikan SWIR1 dan Merah di pembilang, lalu dikurangkan dengan NIR dan Biru. Mengapa? Karena tanah terbuka memantulkan kuat SWIR1 dan Merah, tetapi memantulkan sangat sedikit Biru dan tidak memiliki lonjakan NIR seperti daun sawit."

---

### SLIDE 7: PERAN STRATEGIS SALURAN SWIR2
* **Kategori:** Spektroskopi Residu & Serasah
* **Judul:** Memecahkan Kebuntuan: Memisahkan Tanah dari Serasah dengan SWIR2
* **Layout Visual:** Diagram Komparasi Spektral Wilayah SWIR ($1.6\ \mu\text{m}$ vs. $2.2\ \mu\text{m}$):
  * Kanal B11 Sentinel-2 ($1.61\ \mu\text{m}$ / SWIR1) vs. Kanal B12 ($2.19\ \mu\text{m}$ / SWIR2).
  * Kurva Serasah: Lignin dan selulosa menyerap radiasi di $2.1\ \mu\text{m}$ dan $2.3\ \mu\text{m}$, menekan nilai kanal B12 ke bawah secara tajam $\rightarrow$ Nilai NBR2 melonjak tinggi.
  * Kurva Tanah Terbuka: Rasio B11 dan B12 relatif seimbang atau landai $\rightarrow$ Nilai NBR2 rendah atau mendekati nol.
* **Poin Paparan:**
  * NDVI dan BSI sering terkecoh oleh tumpukan pelepah sawit kering (*pruned fronds*) di gawangan mati karena keduanya tidak berdaun hijau.
  * **Indeks NBR2 dan NDTI (*Normalized Difference Tillage Index*):**
    * Memanfaatkan sensitivitas serapan ikatan hidroksil selulosa tanaman mati pada rentang $2.1–2.3\ \mu\text{m}$.
    * Kombinasi ambang: Piksel tanah terbuka murni wajib memenuhi kriteria ganda: **NDVI Rendah + BSI Tinggi + NBR2 Rendah**.
* **Catatan Pemateri:**
  > "Ini adalah wawasan teknis paling berharga di modul ini: jangan hanya mengandalkan NDVI dan BSI! Jika Anda hanya memakai NDVI $< 0.2$, tumpukan pelepah sawit kering yang menggunung di gawangan mati akan dikira tanah terbuka oleh komputer. Anda wajib memasukkan indeks NBR2 (B11 dan B12) untuk menyortir serasah tersebut."

---

### SLIDE 8: AMBANG BATAS GLOBAL VS KALIBRASI LOKAL
* **Kategori:** Kalibrasi Ambang Batas
* **Judul:** Menentukan Ambang Batas (*Thresholding*): Bahaya Nilai Baku Global
* **Layout Visual:** Diagram Distribusi Nilai Piksel & Kurva Frekuensi Indeks:
  * Batas Ambang Statis Global (misal: NDVI $< 0.25$) $\rightarrow$ Kesalahan klasifikasi pada tanah basah atau tanah berpasir putih.
  * Pendekatan Ambang Adaptif Lokal Berbasis Persentil (Danylo et al. 2021).
* **Poin Paparan:**
  * Ambang batas baku literatur global (misal NDVI $< 0.25$, BSI $> 0$) **tidak dapat ditelan mentah-mentah** di perkebunan sawit Indonesia.
  * **Faktor yang Menggeser Nilai Ambang:**
    1. Warna alami tanah (tanah gambut gelap vs tanah podsolik pasiran terang).
    2. Kadar kelembapan tanah sesaat saat satelit melintas.
  * **Solusi: Kalibrasi Ambang Berbasis Data Lokal:**
    * Menggunakan nilai persentil (misal persentil ke-95 BSI dari blok sawit baru dibuka) sebagai batas ambang dinamis perkebunan (Danylo et al. 2021).
    * Memadukan dengan data penutup lahan untuk menyingkirkan permukaan buatan (atap bangunan pabrik PKS, jalan aspal, dan perumahan divisi).
* **Catatan Pemateri:**
  > "Banyak analis bertanya: 'Pak Retnadi, berapa angka cut-off BSI yang pasti untuk tanah terbuka?' Jawaban ilmiahnya: tidak ada angka tunggal yang mutlak untuk seluruh Indonesia! Tanah gambut di Riau memiliki albedo yang sangat berbeda dibanding tanah Ultisol berbatu di Kalimantan Barat. Kita harus melakukan kalibrasi ambang lokal berbasis data kebun setempat."

---

### SLIDE 9: TANTANGAN PERKEBUNAN KELAPA SAWIT
* **Kategori:** Kondisi Biofisik Spesifik Sawit
* **Judul:** Paradoks Perkebunan Sawit: Kanopi Menghalangi Tanah Sepanjang Tahun
* **Layout Visual:** Ilustrasi Arsitektur Kanopi Kelapa Sawit Dewasa:
  * Fase Tanaman Menghasilkan (TM, umur $> 4$ tahun): Indeks Luas Daun (*Leaf Area Index - LAI*) mencapai 4–6, tajuk pelepah bersentuhan menutup sinar matahari hingga $> 90\%$.
  * Di bawah kanopi: Tanah terlindung rapat dari pandangan sensor optik satelit nadir.
* **Poin Paparan:**
  * Kelapa sawit adalah tanaman tahunan monokotil raksasa (*perennial evergreen*) yang tidak mengalami musim gugur daun (*deciduous*).
  * Pada blok sawit produktif umur 7–20 tahun, tanah praktis **tidak pernah terlihat** oleh sensor optik satelit dari atas.
  * Apakah ini berarti penginderaan jauh gagal? **TIDAK.** Kuncinya adalah mencari **Jendela Peluang (*Window of Opportunity*)**.
* **Catatan Pemateri:**
  > "Mari kita hadapi kenyataan lapangan kita: kebun sawit bukan kebun jagung atau kedelai di Amerika yang setiap tahun tanahnya dibajak dan dibiarkan gundul selama 4 bulan. Sawit hijau sepanjang tahun! Tapi jangan putus asa. Perkebunan kelapa sawit memiliki siklus manajemen yang selalu membuka jendela peluang keterbukaan tanah."

---

### SLIDE 10: JENDELA PELUANG KETERBUKAAN TANAH SAWIT
* **Kategori:** Dinamika Manajemen Perkebunan
* **Judul:** Tiga Jendela Peluang Deteksi Tanah Terbuka di Kebun Sawit
* **Layout Visual:** 3 Kartu Peluang Manajemen Lapangan:
  * Kartu 1: Fase Replanting (Peremajaan Lahan Umur 0–2 Tahun).
  * Kartu 2: Manajemen Piringan Sawit (*Weeded Circles*) & Jalan Rintis.
  * Kartu 3: Fase Land Preparation & Terasering Kontur Awal.
* **Poin Paparan:**
  1. **Fase Peremajaan (*Replanting Period*):**
     * Tanaman tua ditumbangkan dan dicacah (*chipping*). Permukaan lahan terpapar terbuka luas selama beberapa bulan hingga tanaman penutup tanah legum menutup sempurna. Ini adalah peluang emas pemetaan tanah resolusi tinggi.
  2. **Blok Tanaman Belum Menghasilkan (TBM 1 & TBM 2):**
     * Tajuk sawit masih kecil (diameter $< 2–3\ \text{m}$), proporsi tanah di sekitarnya masih dominan terlihat pada citra resolusi tinggi.
  3. **Piringan Pohon dan Jalan Panen (*Harvesting Paths*):**
     * Pembersihan gulma herbisida secara rutin di sekeliling pokok sawit membuka tanah secara konsisten.
* **Catatan Pemateri:**
  > "Kapan waktu terbaik memetakan tanah di kebun sawit kita? Saat replanting! Ketika pohon tua ditumbangkan, tanah terbuka dari ujung ke ujung afdeling. Data satelit yang kita rekam pada jendela waktu beberapa bulan replanting tersebut akan menjadi peta tanah definitif yang berlaku untuk 25 tahun masa tanam siklus berikutnya!"

---

### SLIDE 11: DINAMIKA SPEKTRAL BLOK PEREMAJAAN
* **Kategori:** Suksesi Spektral Lapangan
* **Judul:** Dinamika Spektral Blok Replanting dengan Tanaman Penutup (LCC)
* **Layout Visual:**
  * Grafik Dinamika Temporal NDVI dan BSI pada Blok Replanting:
    ![Gambar 5.3: Deret Waktu Indeks Spektral pada Blok Peremajaan](../assets/modul-5/M5-G03_deret-waktu-indeks-blok-peremajaan.png)
    *Gambar 5.3: Dinamika Temporal Indeks NDVI dan BSI pada Blok Replanting Kelapa Sawit (0–24 Bulan) Menunjukkan Jendela Peluang Keterbukaan Tanah.*
  * Bulan 0: Penumbangan $\rightarrow$ BSI memuncak sangat tinggi, NDVI anjlok mendekati 0.
  * Bulan 3–6: Tanam bibit & pertumbuhan awal kacangan penutup tanah (*Mucuna bracteata*) $\rightarrow$ BSI mulai menurun perlahan.
  * Bulan 9–18: LCC menutup lebat $\rightarrow$ NDVI melonjak tinggi ($> 0.8$), BSI jatuh ke nilai negatif.
* **Poin Paparan:**
  * Penanaman tanaman penutup tanah (*Legume Cover Crop - LCC*) memperpendek jendela keterbukaan tanah murni menjadi hanya sekitar 3 hingga 6 bulan.
  * Setelah LCC menutup rapat, sinyal tanah kembali tertutup oleh biomassa kacangan hijau.
  * **Implikasi Analisis:** Penginderaan jauh membutuhkan kemampuan memantau deret waktu citra secara periodik tinggi untuk menangkap momen puncak tanah terbuka sebelum LCC menutup.
* **Catatan Pemateri:**
  > "Perhatikan grafik Gambar 5.3: kita berkejaran dengan waktu! Setelah pohon ditumbangkan, tim agronomi akan segera menanam Mucuna bracteata untuk melindungi tanah dari erosi. Dalam waktu 6 bulan, tanah sudah hijau tertutup karpet kacangan. Jika kita hanya memakai satu citra satelit per tahun, kita pasti kehilangan momen emas keterbukaan tanah ini."

---

### SLIDE 12: DARI CITRA TUNGGAL KE DERET WAKTU (MULTITEMPORAL)
* **Kategori:** Metodologi Komposit Lanjut
* **Judul:** Solusi Multitemporal: Mengumpulkan Momen Terbuka Sepanjang Waktu
* **Layout Visual:** Diagram Konseptual Sintesis Citra Multitemporal:
  * Tumpukan 50 Scene Citra Sentinel-2 (Tahun 2020 s.d. 2025) di atas wilayah perkebunan yang sama.
  * Seleksi Per-Piksel: Piksel di Blok A terbuka pada Juli 2021; Piksel di Blok B terbuka pada Agustus 2023; Piksel di Blok C terbuka pada September 2024.
  * Penggabungan: Komposit Sintetis Tanah Terbuka (*Virtual Bare Soil Composite*).
* **Poin Paparan:**
  * Satu tanggal citra tunggal (*single-date image*) hanya mampu menangkap tanah terbuka pada sebagian kecil blok kebun ($< 5–10\%$).
  * **Prinsip Komposit Deret Waktu (*Time-Series Compositing*):**
    * Menggunakan arsip citra satelit selama 3 hingga 10 tahun (katalog bebas Sentinel-2 dan Landsat).
    * Setiap piksel dievaluasi riwayat spektralnya sepanjang waktu. Momen ketika piksel tersebut mencapai titik paling terbuka (*barest state*) disimpan dan digabungkan menjadi satu mozaik utuh tanpa awan dan tanpa vegetasi!
* **Catatan Pemateri:**
  > "Inilah keajaiban komputasi modern dan Big Data geospasial: jika Blok A direplanting tahun 2021 dan Blok B direplanting tahun 2024, kita tidak perlu memetakan tanah secara terpisah. Dengan algoritma multitemporal, komputer akan mencari hari di mana Blok A gundul dan hari di mana Blok B gundul, lalu menempelkannya menjadi satu peta tanah terbuka kebun yang utuh!"

---

### SLIDE 13: ALUR KERJA ALGORITMA KOMPOSIT TANAH TERBUKA
* **Kategori:** Diagram Alir Rekayasa Data
* **Judul:** Alur Kerja Baku Pembuatan Komposit Tanah Terbuka (GEOBAT / Barest Pixel)
* **Layout Visual:**
  * Diagram Alir Pembuatan Komposit Tanah Terbuka:
    ![Gambar 5.4: Alur Kerja Pembuatan Komposit Tanah Terbuka](../assets/modul-5/M5-G04_alur-deteksi-tanah-terbuka.png)
    *Gambar 5.4: Diagram Alir Baku Pembuatan Komposit Sintetis Tanah Terbuka Multitemporal (Metode GEOBAT / Barest Pixel Composite).*
  * Rincian 5 Tahap Pengolahan:
    * Tahap 1: Seleksi Koleksi Deret Waktu Satelit (Sentinel-2 L2A / Landsat-8/9 Surface Reflectance).
    * Tahap 2: Masking Kualitas Otomatis (Penapisan awan, bayangan awan via SCL, badan air via MNDWI, area terbangun).
    * Tahap 3: Perhitungan Indeks Spektral Per-Piksel (NDVI, SAVI, BSI, NBR2) untuk setiap tanggal.
    * Tahap 4: Penapisan Kondisi Terbuka Gabungan (Syarat: $\text{NDVI} < 0.25\ \cap\ \text{NBR2} < 0.15\ \cap\ \text{BSI} > 0$).
    * Tahap 5: Agregasi Statistik Per-Piksel (Menghitung Median Nilai Reflektansi Spektral saat status terbuka tercapai).
* **Poin Paparan:**
  * Sistem mutakhir seperti **GEOBAT (*Geospatial Soil Sensing System*)** (Demattê et al. 2020) dan **Barest Pixel Composite** (Roberts et al. 2019) mengotomatiskan seluruh alur kerja ini pada platform komputasi awan (*Google Earth Engine*).
  * Menggunakan nilai **Median**, bukan rata-rata (*Mean*), untuk memastikan nilai reflektansi bebas dari pengaruh ekstrim anomali residu awan tipis atau kelembapan sesaat.
* **Catatan Pemateri:**
  > "Alur kerja pada Gambar 5.4 ini adalah SOP baku internasional yang dikembangkan tim Demattê (2020). Mengapa kita memakai median? Karena nilai median sangat tahan terhadap outlier (gangguan ekstrim). Jika ada satu tanggal di mana tanah masih sedikit basah kuyup, median akan mengabaikannya dan mengambil nilai pantulan tanah normal yang kering."

---

### SLIDE 14: PRODUK AKHIR EKSTRAKSI TANAH TERBUKA
* **Kategori:** Deliverable Teknis & Evaluasi
* **Judul:** Tiga Produk Luaran dari Ekstraksi Tanah Terbuka
* **Layout Visual:** Tiga Panel Produk Peta Hasil:
  * Panel 1: Komposit Reflektansi Spektral Murni (*Pure Bare Soil Reflectance* B2, B3, B4, B8, B11, B12).
  * Panel 2: Peta Frekuensi Keterbukaan (*Bare Soil Frequency Map* - persentase berapa kali piksel tersebut terbuka dalam 5 tahun).
  * Panel 3: Peta Ketidakpastian Spektral (*Uncertainty / Standard Deviation Map*).
* **Poin Paparan:**
  1. **Komposit Reflektansi Tanah Terbuka Murni:**
     * Menjadi masukan utama (*direct covariate*) bagi model prediksi sifat tanah (kadar lempung, pasir, C-organik) di Modul 4 dan Modul 8.
  2. **Peta Frekuensi Keterbukaan (*Bare Soil Frequency*):**
     * Mengidentifikasi blok-blok kebun yang mengalami erosi parah atau tutupan vegetasi kronis terdegradasi.
  3. **Peta Ketidakpastian:**
     * Menandai piksel-piksel yang frekuensi terbukanya sangat rendah ($< 3$ kali observasi) sebagai area dengan ketidakpastian estimasi tinggi.
* **Catatan Pemateri:**
  > "Hasil akhir dari modul ini bukan sekadar gambar berwarna cokelat. Kita menghasilkan tiga layer data berharga: citra reflektansi tanah bersih tanpa pohon sawit, peta frekuensi yang menunjukkan seberapa sering tanah itu terpapar, dan peta ketidakpastian. Layer reflektansi bersih inilah yang akan diserahkan ke Dr. Guruh untuk dimodelkan sifat tanahnya."

---

### SLIDE 15: RANGKUMAN & PERSIAPAN SESI PRAKTIK
* **Kategori:** Kesimpulan & Rencana Aksi
* **Judul:** Rangkuman Kunci & Kesiapan Menuju Studio Praktik
* **Layout Visual:** Poin Intisari & Cuplikan Latihan Praktik Studio (QGIS / Google Colab).
* **Poin Paparan:**
  * **Intisari Pembelajaran:**
    1. Deteksi tanah terbuka adalah filter krusial untuk mencegah sinyal vegetasi dan serasah merusak prediksi sifat tanah.
    2. Garis tanah (*Soil Line*) dan kanal SWIR2 (NBR2) adalah kunci pemisah tanah dari serasah kering.
    3. Di perkebunan kelapa sawit, komposit multitemporal deret waktu adalah satu-satunya cara mengatasi kendala tutupan kanopi rapat.
  * **Aplikasi Praktik Siang Nanti (Dipandu Nurarfiyah):**
    * Peserta akan menghitung indeks BSI, NDVI, dan NBR2 di QGIS.
    * Menerapkan multi-threshold filtering dan menyusun komposit tanah terbuka pada data latihan.
* **Catatan Pemateri:**
  > "Bapak dan Ibu, teori telah kita kuasai. Deteksi tanah terbuka bukan lagi misteri; ini adalah seni memadukan matematika indeks dengan logika kalender perkebunan. Siang nanti bersama Mbak Nurarfiyah, kita akan mempraktikkan langsung langkah demi langkah di komputer masing-masing. Terima kasih atas perhatiannya!"
