# RANCANGAN PRESENTASI (SLIDE DECK) PELATIHAN
## Bagian 7: Proximal Soil Sensing (PSS)

**Pemateri:** Pandu Yudha Adi Putra Wirabuana, S.Hut., M.Sc., Ph.D.  
**Institusi:** Pusat Studi Pengelolaan Sumber Daya Lahan (PS2DL), Universitas Gadjah Mada  
**Target Audiens:** Staf Teknis, Agronomis, Peneliti, dan Pengelola Perkebunan Kelapa Sawit (PT SMART Tbk)  
**Alokasi Waktu:** Sesi Ceramah Teori (60–90 Menit) + Pengantar Demonstrasi Alat  
**Dokumen Acuan:** `Modul Pelatihan SMART Pemanfaatan RS dan DSM.docx` (Bab 7)

---

### PANDUAN VISUAL & IDENTITAS SLIDE (DESIGN SYSTEM)
* **Warna Utama:** Biru Navy UGM (`#1F3A5F`), Hijau Daun Sawit (`#2A9D8F`), Ungu Spektral / Sensorik (`#7B5EA7`), Kuning/Oranye (`#F2C14E` / `#E07B39`).
* **Tipografi:** Sans-serif modern (Calibri / Carlito / Arial), hierarki judul besar (32–36 pt), subjudul (20–24 pt), teks isi (14–16 pt).
* **Prinsip Tampilan:** Foto instrumen sensor lapangan nyata, diagram alir gelombang spektrum, grafik praolah data (*signal processing*), dan jembatan ke demonstrasi alat spektrometer mandiri (*custom sensor*).

---

## DAFTAR SLIDE & STRUKTUR MATERI

```
BAGIAN 7: PROXIMAL SOIL SENSING (Slide 1–16)
  - Slide 1: Judul & Pembuka Sesi
  - Slide 2: Krisis Data Tanah Konvensional & Kelahiran Paradigma "Bottom-Up"
  - Slide 3: Definisi & Tiga Moda Operasi Proximal Soil Sensing (Benchtop, Handheld, On-the-Go)
  - Slide 4: Taksonomi Sensor PSS: Di Dalam dan Di Luar Spektrum Elektromagnetik
  - Slide 5: Spektroskopi Reflektansi Optik: Vis-NIR vs. MIR
  - Slide 6: Karakterisasi Unsur Kimia Tanah: pXRF dan LIBS
  - Slide 7: Sensor Geofisika & Elektromagnetik: EMI (ECa) dan Sinar Gamma
  - Slide 8: Sensor Non-Optik: Penetrometer Elektronik untuk Pemadatan Tanah
  - Slide 9: Menembus Kedalaman: Membandingkan Daya Tembus PSS vs. Satelit RS
  - Slide 10: Matriks Komparasi Menyeluruh: Remote Sensing vs. Proximal Soil Sensing
  - Slide 11: Anatomi Derau Spektral & Mengapa Spektrum Mentah Tidak Bisa Langsung Dipakai?
  - Slide 12: Empat Langkah Utama Praolah Spektrum (Savitzky-Golay, SNV, Derivatif, Continuum Removal)
  - Slide 13: Alur Pemodelan Kemometrika: Dari Kurva Spektral ke Nilai Sifat Tanah (PLSR, SVR, CNN)
  - Slide 14: Pemanfaatan PSS di Perkebunan Kelapa Sawit (Zonasi Pemadatan, Pirit, Gambut, Dosis Pupuk)
  - Slide 15: Sekilas Demo Alat: Pengenalan Sensor Spektroskopi Mandiri (Siang Nanti)
  - Slide 16: Rangkuman & Integrasi PSS sebagai Penyuplai Data Emas untuk Pemodelan DSM
```

---

## RINCIAN KONTEN PER SLIDE

---

### SLIDE 1: JUDUL & PEMBUKA
* **Kategori:** Cover Presentation
* **Judul Utama:** Proximal Soil Sensing (PSS)
* **Sub-judul:** Karakterisasi Sifat Tanah Cepat, Non-Destruktif, dan Rapat di Bawah Tajuk Perkebunan Kelapa Sawit
* **Identitas:** Pandu Yudha Adi Putra Wirabuana, S.Hut., M.Sc., Ph.D. | Pusat Studi Pengelolaan Sumber Daya Lahan (PS2DL) UGM
* **Layout Visual:**
  * Kiri: Judul presentasi tebal, identitas pemateri, logo UGM & PS2DL.
  * Kanan: Montase visual spektrometer lapangan portabel, probe penetrometer elektronik di kebun, dan kurva spektrum vis-NIR reflektansi tanah.
* **Poin Paparan:**
  * Memahami konsep sensor kontak dekat (*proximal*) sebagai pelengkap esensial citra satelit.
  * Mengenal prinsip fisika ragam sensor (spektroskopi, pXRF, EMI, gamma) dan alur praolah sinyal kemometrika.
* **Catatan Pemateri (Speaker Notes):**
  > "Selamat pagi rekan-rekan agronomis dan tim riset perkebunan kelapa sawit. Di sesi-sesi sebelumnya, kita melihat tanah dari ketinggian ratusan kilometer di antariksa. Sekarang, di Modul 7 ini, kita turun langsung ke tanah, menyentuh tanahnya dari jarak nol hingga dua meter menggunakan Proximal Soil Sensing. Kita akan melihat bagaimana teknologi sensor ini menjadi terobosan spektakuler dalam memotong biaya dan waktu uji laboratorium."

---

### SLIDE 2: KRISIS DATA TANAH KONVENSIONAL & PARADIGMA BOTTOM-UP
* **Kategori:** Latar Belakang & Filosofi PSS
* **Judul:** Mengapa Kita Membutuhkan Proximal Soil Sensing?
* **Layout Visual:** Komparasi 2 Paradigma Pengelolaan Hara:
  * Kiri (Pendekatan Klasik *Top-Down*): Sampel bor tanah jarang $\rightarrow$ Kirim ke lab kimia (mahal & berminggu-minggu) $\rightarrow$ Rekomendasi dosis pupuk seragam per afdeling.
  * Kanan (Pendekatan Presisi *Bottom-Up* Viscarra Rossel & Bouma 2016): Sensor proksimal di lapangan $\rightarrow$ Pengukuran instan dalam hitungan detik $\rightarrow$ Data tanah sangat rapat (1 sampel/ha) $\rightarrow$ Pemupukan presisi spesifik pokok.
* **Poin Paparan:**
  * **Hambatan Utama Pertanian Presisi:** Peta kesuburan tanah yang andal memerlukan minimal 1 sampel tanah per hektare (Molin & Tavares 2019). Pada kebun sawit seluas $20.000\ \text{ha}$, ini berarti $20.000$ sampel lab—biaya miliaran rupiah dan waktu berbulan-bulan!
  * **Dampak Negatif:** Manajemen terpaksa mengambil jalan pintas dengan meratakan dosis pupuk, memicu pemborosan pupuk kimia dan pencemaran air.
  * **Solusi Sensor Proksimal:** Pengukuran cepat (*rapid*), akurat, murah (*cost-effective*), dan non-destruktif langsung di kebun.
* **Catatan Pemateri:**
  > "Bapak dan Ibu yang bekerja di perkebunan pasti paham betul: menunggu hasil lab tanah dari kantor pusat itu lamanya minta ampun. Begitu hasilnya keluar 2 bulan kemudian, pupuk sudah terlanjur ditabur dengan dosis rata. Kita butuh alat yang bisa memberi tahu kadar karbon, lempung, dan status hara tanah di lapangan saat itu juga. Di sinilah PSS menjadi penolong utama kita."

---

### SLIDE 3: DEFINISI & TIGA MODA OPERASI PSS
* **Kategori:** Definisi & Operasionalisasi
* **Judul:** Apa Itu Proximal Soil Sensing dan Bagaimana Cara Kerjanya?
* **Layout Visual:** Ilustrasi 3 Moda Kerja Sensor di Kebun:
  * Moda 1: *Benchtop* (Laboratorium mini di kantor afdeling, sampel dikering-anginkan).
  * Moda 2: *Handheld* (Instrumen genggam dioperasikan asisten kebun/surveyor di lapangan).
  * Moda 3: *On-the-Go / Mobile* (Sensor terpasang di traktor atau UTV, merekam otomatis sambil berjalan).
* **Poin Paparan:**
  * **Definisi Ilmiah (Viscarra Rossel et al. 2011):** Penggunaan sensor berbasis lapangan yang bekerja bersentuhan langsung dengan tanah atau pada jarak sangat dekat ($< 2\ \text{meter}$ dari permukaan).
  * **Tiga Moda Operasi PSS (England & Viscarra Rossel 2018):**
    1. **Alat Meja (*Benchtop*):** Akurasi tertinggi karena kondisi sampel terkendali (kering dan lolos ayakan $2\ \text{mm}$).
    2. **Alat Genggam (*Handheld / In-situ*):** Pengukuran langsung pada singkapan tanah, dinding profil, atau piringan sawit tanpa merusak tanah.
    3. **Alat Bergerak (*On-the-go Mobile Sensing*):** Sensor ditarik traktor melintasi gawangan, menghasilkan ribuan titik data kontinu dalam satu hari kerja.
* **Catatan Pemateri:**
  > "Teknik spektroskopi dan induksi elektromagnetik sebenarnya bukan barang baru. Yang baru adalah evolusi teknologinya: alat yang dulunya sebesar kulkas di laboratorium riset, sekarang sudah bisa diringkas menjadi alat genggam seukuran bor baterai yang bisa dibawa mandor ke tengah blok kebun."

---

### SLIDE 4: TAKSONOMI RAGAM SENSOR PSS
* **Kategori:** Klasifikasi Instrumen
* **Judul:** Ragam Sensor PSS: Di Dalam dan Di Luar Spektrum Elektromagnetik
* **Layout Visual:**
  * Diagram Taksonomi Sensor PSS pada Spektrum Gelombang:
    ![Gambar 7.1: Ragam Sensor PSS pada Spektrum Elektromagnetik](../assets/modul-7/M7-G01_sensor-pss-pada-spektrum-elektromagnetik.png)
    *Gambar 7.1: Taksonomi Ragam Sensor Proximal Soil Sensing (PSS) pada Spektrum Elektromagnetik (Sinar Gamma, Sinar-X pXRF, Vis-NIR, MIR, dan Gelombang Mikro/EMI) serta Sensor Non-Spektrum Mekanis.*
  * Cabang 1: Sensor Berbasis Spektrum Elektromagnetik (Sinar Gamma, pXRF, LIBS, Spektroskopi MIR, Spektroskopi Vis-NIR, Gelombang Mikro / EMI).
  * Cabang 2: Sensor Non-Spektrum (Mekanis / Penetrometer, Elektrokimia / Ion Selektif).
* **Poin Paparan:**
  * Sensor PSS memanfaatkan beragam fenomena fisika untuk menginterogasi sifat tanah:
    * **Radiasi Nuklir Alami:** Sinar Gamma ($^{40}\text{K}, ^{238}\text{U}, ^{232}\text{Th}$).
    * **Fluoresensi Atomik:** Sinar-X (pXRF) untuk analisis unsur total.
    * **Emisi Plasma Termal:** Laser (LIBS) untuk unsur ringan mikro.
    * **Getaran Molekuler:** Inframerah Vis-NIR ($0.4–2.5\ \mu\text{m}$) dan MIR ($2.5–25\ \mu\text{m}$).
    * **Induksi Medan Elektromagnetik:** EMI untuk konduktivitas listrik semu ($EC_a$).
    * **Gaya Mekanik:** Tahanan ujung konus penetrometer untuk memetakan kepadatan tanah.
* **Catatan Pemateri:**
  > "Lihat Gambar 7.1: dunia sensor tanah proksimal itu sangat luas. Dari spektrum energi sinar gamma yang sangat tinggi hingga frekuensi radio gelombang mikro, semuanya bisa kita manfaatkan untuk 'menginterogasi' tanah tanpa harus membawa sekarung tanah ke laboratorium kimia basah."

---

### SLIDE 5: SPEKTROSKOPI REFLEKTANSI OPTIK (VIS-NIR VS MIR)
* **Kategori:** Spektroskopi Molekuler
* **Judul:** Spektroskopi Pantulan Tanah: Memilih Antara Vis-NIR dan MIR
* **Layout Visual:** Tabel Komparasi Berdampingan + Spektrum Karakteristik:
  * Kolom Kiri: Vis-NIR ($400–2.500\ \text{nm}$).
  * Kolom Kanan: MIR ($2.500–25.000\ \text{nm}$ / $4.000–400\ \text{cm}^{-1}$).
* **Poin Paparan:**
  * **Spektroskopi Vis-NIR:**
    * Mengukur nada atas (*overtones*) dan getaran kombinasi ikatan $C\text{-}H$, $O\text{-}H$, $N\text{-}H$.
    * **Sifat Tanah:** Karbon organik tanah (SOC), lempung, nitrogen total, oksida besi, dan kelembapan.
    * **Kelebihan:** Instrumen portabel, optik serat fleksibel, biaya lebih murah, sangat ideal untuk operasional lapangan.
    * **Keterbatasan:** Puncak serapan relatif tumpang tindih dan sangat dipengaruhi oleh air bebas di lapangan.
  * **Spektroskopi MIR:**
    * Mengukur getaran dasar (*fundamental vibrations*) molekul mineral dan bahan organik.
    * **Kelebihan:** Puncak serapan sangat tajam dan spesifik; model kalibrasi sangat kokoh dan akurat.
    * **Keterbatasan:** Sampel wajib dikeringkan dan digiling sangat halus; sangat terganggu oleh air; alat lapangan masih langka dan mahal.
* **Catatan Pemateri:**
  > "Untuk operasional sehari-hari di kebun sawit kita, Vis-NIR adalah pilihan paling praktis. Mengapa? Karena sensor Vis-NIR bisa ditempelkan langsung ke permukaan tanah tanpa harus menggiling sampel menjadi tepung seperti pada MIR. Nanti siang, alat buatan sendiri yang akan kita demonstrasikan bekerja pada rentang Vis-NIR ini."

---

### SLIDE 6: KARAKTERISASI UNSUR: pXRF DAN LIBS
* **Kategori:** Analisis Unsur Kimia
* **Judul:** Deteksi Unsur Kimia Cepat: Portable XRF dan LIBS
* **Layout Visual:**
  * Kiri: Diagram prinsip kerja pXRF (Penyinaran sinar-X primer $\rightarrow$ Pelepasan elektron kulit dalam $\rightarrow$ Emisi fluoresensi karakteristik unsur).
  * Kanan: Ringkasan Sifat Unsur yang Terdeteksi & Batasan Pengukuran.
* **Poin Paparan:**
  * **Portable X-ray Fluorescence (pXRF):**
    * Menganalisis konsentrasi **unsur total** secara instan (1–2 menit per titik).
    * Mengukur unsur-unsur penting: Besi ($\text{Fe}$), Silikon ($\text{Si}$), Aluminium ($\text{Al}$), Kalium ($\text{K}$), Kalsium ($\text{Ca}$), Fosfor ($\text{P}$), Titanium ($\text{Ti}$), dan Zirkonium ($\text{Zr}$).
    * Indikator pelapukan: Rasio $\text{Fe/Al}$ dan $\text{Ti/Zr}$ untuk membedakan lapisan bahan induk.
    * *Catatan Kritis:* pXRF mengukur kadar hara total, bukan hara tersedia bagi tanaman; tidak dapat mendeteksi unsur bernomor atom ringan ($Z < 12$, seperti C dan N).
  * **Laser-Induced Breakdown Spectroscopy (LIBS):**
    * Menggunakan pulsa laser intensitas tinggi untuk menguapkan titik mikro sampel menjadi plasma; mampu mendeteksi unsur-unsur ringan termasuk Karbon ($\text{C}$).
* **Catatan Pemateri:**
  > "Alat pXRF bentuknya seperti pistol fiksi ilmiah. Anda cukup menembakkan sensor ini ke batu atau tanah selama 60 detik, dan di layar akan langsung muncul: 'Kadar Besi 12%, Silikon 25%, Kalium 1,2%'. Ini luar biasa untuk memetakan cadangan hara total dan mendeteksi lapisan pirit ($\text{FeS}_2$) di lahan pasang surut!"

---

### SLIDE 7: SENSOR GEOFISIKA & ELEKTROMAGNETIK (EMI & GAMMA)
* **Kategori:** Geofisika Permukaan Dangkal
* **Judul:** Geofisika Lapangan: Induksi Elektromagnetik (EMI) dan Sinar Gamma
* **Layout Visual:** Ilustrasi Penerapan di Blok Kelapa Sawit:
  * Atas: Sensor EMI (*Electromagnetic Induction*) mengukur Konduktivitas Listrik Semu ($EC_a$) hingga kedalaman 1–2 meter.
  * Bawah: Spektrometer Sinar Gamma pasif merekam radiasi alami radioisotop Potassium ($^{40}\text{K}$), Uranium ($^{238}\text{U}$), dan Thorium ($^{232}\text{Th}$).
* **Poin Paparan:**
  * **Electromagnetic Induction (EMI):**
    * Mengukur konduktivitas listrik semu (*apparent electrical conductivity - $EC_a$*).
    * $EC_a$ berkorelasi erat dengan: **Kadar Lempung, Kelembapan Tanah, Salinitas/Intrusi Air Laut, dan Kedalaman Lapangan Kedap Air/Padas**.
    * Sangat penting untuk zonasi tanah salin di kebun pesisir dan memetakan ketebalan kubah gambut.
  * **Spektrometer Sinar Gamma Lapangan:**
    * Merekam peluruhan radioaktif alami lapisan $0–30\ \text{cm}$ tanah.
    * Rasio isotop menjadi 'sidik jari' asal usul batuan induk dan intensitas pelindian (*leaching*) tanah tropis.
* **Catatan Pemateri:**
  > "Jika Anda mengelola perkebunan sawit di tepi pantai Sumatra atau di lahan gambut, sensor EMI adalah instrumen wajib. Dengan menarik sensor EMI di belakang sepeda motor atau UTV di sepanjang jalan rintis, Anda bisa langsung memetakan kantong-kantong tanah bergaram tinggi atau batas ketebalan lapisan tanah mineral di bawah gambut."

---

### SLIDE 8: SENSOR MEKANIS: PENETROMETER PEMADATAN TANAH
* **Kategori:** Sifat Fisik & Struktur Tanah
* **Judul:** Memetakan Pemadatan Tanah: Penetrometer Elektronik Terintegrasi GPS
* **Layout Visual:**
  * Kiri: Foto penetrometer konus elektronik genggam dengan sensor gaya dan pencatat kedalaman otomatis.
  * Kanan: Kurva Profil Tahanan Penetrasi (*Cone Index - MPa*) vs Kedalaman ($0–80\ \text{cm}$) pada gawangan sawit, piringan, dan pasar rintis.
* **Poin Paparan:**
  * **Masalah Lapangan Sawit:** Lalu lintas traktor pengangkut TBS seberat belasan ton memicu pemadatan tanah ekstrem (*soil compaction*) di pasar rintis.
  * Pemadatan tanah menghancurkan pori aerasi tanah, menghambat infiltrasi air hujan (memicu genangan), dan membatasi penetrasi akar sawit.
  * **Penetrometer Konus Elektronik:**
    * Mengukur gaya tahanan tanah per satuan luas (MegaPascal / MPa).
    * Ambang kritis: Tahanan $> 2.0\ \text{MPa}$ merupakan batas terhentinya perkembangan akar sawit.
    * Mengidentifikasi kedalaman lapisan padas (*hardpan layer*) secara presisi untuk rekomendasi pembajakan dalam (*subsoiling*).
* **Catatan Pemateri:**
  > "Produksi TBS sawit sering drop bukan karena kurang pupuk, tapi karena tanahnya padat membatu tergilas roda traktor! Akibatnya akar sawit tercekik tidak bisa bernapas. Penetrometer elektronik ini memungkinkan kita menusuk tanah dan langsung mengetahui: 'Oh, di kedalaman 25 cm ada lapisan keras kedap akar'. Kita bisa merekomendasikan alat subsoiler tepat di blok yang membutuhkan."

---

### SLIDE 9: MENEMBUS KEDALAMAN: PSS VS SATELIT
* **Kategori:** Komparasi Kedalaman Efektif
* **Judul:** Menembus Lapisan Tanah: Daya Tembus PSS vs. Penginderaan Jauh Satelit
* **Layout Visual:**
  * Diagram Penampang Kedalaman Informasi Sensor Tanah:
    ![Gambar 7.2: Kedalaman Informasi Berbagai Teknik Penginderaan Tanah](../assets/modul-7/M7-G02_kedalaman-informasi-berbagai-teknik.png)
    *Gambar 7.2: Kedalaman Informasi Berbagai Teknik Penginderaan Tanah: Satelit RS ($0–2\ \text{mm}$) vs. Spektrometer Vis-NIR ($0–2\ \text{mm}$) vs. Sinar Gamma ($0–30\ \text{cm}$) vs. Penetrometer ($0–80\ \text{cm}$) vs. Induksi Elektromagnetik EMI ($0.5–2.0\ \text{m}$).*
  * Rincian kedalaman efektif:
    * Kedalaman $0–2\ \text{mm}$: Satelit Optik & Sensor Vis-NIR.
    * Kedalaman $< 1\ \text{mm}$: pXRF.
    * Kedalaman $0–30\ \text{cm}$: Spektrometer Sinar Gamma.
    * Kedalaman $0–80\ \text{cm}$: Penetrometer Elektronik.
    * Kedalaman $0.5–2.0\ \text{meter}$: Induksi Elektromagnetik (EMI / $EC_a$).
* **Poin Paparan:**
  * Kelemahan terbesar satelit optik adalah keterbatasan penetrasi pada 'kulit luar' tanah ($0–2\ \text{mm}$).
  * Rangkaian sensor PSS memiliki kedalaman integrasi yang bervariasi secara signifikan.
  * Sensor EMI dan Penetrometer mampu membaca kondisi fisik dan kimia tanah hingga kedalaman $1–2\ \text{meter}$—tepat di jantung zona perakaran aktif dan pergerakan air tanah kelapa sawit.
* **Catatan Pemateri:**
  > "Perhatikan Gambar 7.2 di layar. Ini alasan mengapa PSS tidak bisa digantikan oleh satelit luar angkasa. Satelit hanya menyentuh lapisan 2 milimeter paling atas. Tetapi sensor EMI bisa 'melihat' sampai kedalaman 2 meter ke dalam tanah, membaca kelembapan dan salinitas di zona akar sawit kita. Ini adalah keunggulan absolut PSS."

---

### SLIDE 10: MATRIKS KOMPARASI RS VS PSS
* **Kategori:** Tabel Evaluasi Komprehensif
* **Judul:** Perbandingan Karakteristik: Remote Sensing vs. Proximal Soil Sensing
* **Layout Visual:** Tabel Komparasi Berwarna (Berdasarkan Tabel 7.2 Modul):
  * 7 Parameter: Jarak Sensor | Cakupan Spasial | Lapisan Terwakili | Gangguan Atmosfer & Kanopi | Resolusi Spektral | Sifat Terukur | Peran dalam DSM.
* **Poin Paparan:**
  * **Cakupan Spasial:** RS unggul mutlak dalam cakupan luas menyeluruh setiap piksel ($100\%$ area); PSS menghasilkan data berbentuk titik rapat atau lintasan transek.
  * **Gangguan Kanopi Sawit:** RS sangat terhalang kanopi sawit; PSS beroperasi di bawah kanopi tanpa hambatan atmosfer sama sekali.
  * **Resolusi Spektral:** RS multispektral memiliki kanal lebar ($20–100\ \text{nm}$); PSS spektroskopi memiliki resolusi sangat tinggi bersambung ($1–10\ \text{nm}$).
  * **Sinergi Ideal dalam DSM:** RS menyediakan **kovariat spasial menyeluruh**; PSS menyediakan **data kalibrasi/validasi tanah yang rapat, akurat, dan murah**.
* **Catatan Pemateri:**
  > "Kita tidak perlu mempertentangkan mana yang lebih baik antara satelit RS atau sensor PSS. Keduanya adalah pasangan ideal. Satelit memberikan peta menyeluruh satu lanskap kebun, sedangkan sensor PSS memberikan titik-titik sampel tanah yang sangat rapat dan presisi di bawah pohon untuk mengkalibrasi satelit tersebut."

---

### SLIDE 11: ANATOMI DERAU SPEKTRAL PADA DATA MENTAH
* **Kategori:** Praolah Sinyal & Kemometrika
* **Judul:** Mengapa Spektrum Mentah (*Raw Spectra*) Tidak Bisa Langsung Dimodelkan?
* **Layout Visual:**
  * Kiri: Grafik Spektrum Mentah Tanah (*Raw Reflectance Spectra*) yang penuh derau bintik dan pergeseran garis dasar (*baseline shifts*).
  * Kanan: Tiga Sumber Distorsi Fisik:
    1. Derau instrumen elektronik (*High-frequency random noise*).
    2. Efek hamburan cahaya akibat perbedaan ukuran butir tanah (*Albedo shift*).
    3. Fluktuasi kelembapan tanah sesaat (*Moisture baseline distortion*).
* **Poin Paparan:**
  * Spektrum pantulan tanah mentah dari alat Vis-NIR tidak pernah bersih.
  * Partikel tanah yang kasar memantulkan cahaya secara acak (*multiple scattering*), menggeser seluruh kurva spektrum ke atas atau ke bawah secara artifisial.
  * Jika spektrum mentah ini langsung dimasukkan ke model prediksi, algoritma akan terkecoh oleh derau dan pergeseran albedo, bukan membaca ikatan kimia mineral tanah.
* **Catatan Pemateri:**
  > "Jika Anda menembakkan spektrometer ke tanah, kurva yang keluar di layar jangan langsung dimasukkan ke regresi! Kurva mentah itu kotor: ada derau sensor, ada efek butiran tanah yang kasar, dan ada gangguan kelembapan. Kita wajib melakukan praolah sinyal (*preprocessing*) agar sidik jari kimia tanahnya muncul dengan murni."

---

### SLIDE 12: EMPAT LANGKAH UTAMA PRAOLAH SPEKTRUM
* **Kategori:** Algoritma Pra-pemrosesan Sinyal
* **Judul:** Standardisasi Spektrum: Empat Algoritma Praolah Kunci
* **Layout Visual:**
  * Empat Tahap Baku Praolah Sinyal Spektroskopi Tanah:
    ![Gambar 7.3: Praolah Spektrum Tanah Sintetis](../assets/modul-7/M7-G03_praolah-spektrum-sintetis.png)
    *Gambar 7.3: Empat Tahap Baku Praolah Sinyal Spektroskopi Tanah: (a) Savitzky-Golay Smoothing, (b) Standard Normal Variate (SNV), (c) Turunan Pertama & Kedua, dan (d) Continuum Removal.*
  * Panel (a) *Savitzky-Golay Smoothing* (Menghilangkan derau frekuensi tinggi tanpa mengikis puncak serapan).
  * Panel (b) *Standard Normal Variate (SNV)* (Mengoreksi pergeseran garis dasar dan efek hamburan partikel).
  * Panel (c) *First & Second Derivative* (Menghilangkan offset dan mempertajam pemisahan lembah serapan sempit).
  * Panel (d) *Continuum Removal* (Mengisolasi kedalaman relatif lembah serapan spesifik terhadap garis kontinum atas).
* **Poin Paparan:**
  * **1. Savitzky-Golay Filter:** Menghaluskan kurva menggunakan fitting polinomial lokal; derau hilang, bentuk puncak asli tetap terjaga.
  * **2. SNV (*Standard Normal Variate*):** Memusatkan dan membagi spektrum dengan simpangan bakunya; meratakan kurva dari pengaruh perbedaan kekasaran sampel.
  * **3. Turunan Pertama (*First Derivative*):** Mengubah puncak serapan menjadi titik perpotongan nol (*zero-crossing*), meniadakan pergeseran baseline konstan.
  * **4. *Continuum Removal*:** Menormalisasi kurva ke skala 0 hingga 1; sangat efektif mengukur volume absolut mineral lempung di $2.20\ \mu\text{m}$.
* **Catatan Pemateri:**
  > "Perhatikan Gambar 7.3. Dengan Continuum Removal, kurva tanah yang tadinya melengkung naik turun disetarakan garis atasnya menjadi datar di angka 1.0. Sekarang, kedalaman lembah serapan di 2,2 mikron murni menunjukkan kuantitas lempung tanah tanpa terganggu oleh apakah tanah itu warnanya gelap atau terang!"

---

### SLIDE 13: ALUR PEMODELAN KEMOMETRIKA
* **Kategori:** Pemodelan Prediktif Spektral
* **Judul:** Alur Pemodelan Spektroskopi Tanah: Dari Sinyal ke Sifat Tanah
* **Layout Visual:**
  * Diagram Alir Baku Pemodelan Spektroskopi:
    ![Gambar 7.4: Alur Pemodelan Spektroskopi Tanah](../assets/modul-7/M7-G04_alur-pemodelan-spektroskopi.png)
    *Gambar 7.4: Alur Pemodelan Kemometrika Tanah: Dari Sampel Kalibrasi dan Spektrum Pantulan Mentah hingga Kalibrasi Algoritma PLSR/Random Forest dan Validasi Model Lapangan.*
  * Sampel Kalibrasi Lapangan $\rightarrow$ Uji Lab Standar ($Y$) $\leftrightarrow$ Rekaman Spektrum Vis-NIR ($X$) $\rightarrow$ Praolah Spektra $\rightarrow$ Kalibrasi Algoritma Kemometrika (PLSR / SVR / Random Forest / 1D-CNN) $\rightarrow$ Validasi Silang Independen $\rightarrow$ Model Siap Pakai di Lapangan.
* **Poin Paparan:**
  * **Algoritma Kemometrika Standar:**
    * **Partial Least Squares Regression (PLSR):** Standar industri; mereduksi ratusan panjang gelombang berkorelasi tinggi menjadi variabel laten (*latent variables*) prediktif.
    * **Support Vector Regression (SVR) & Random Forest:** Mengakomodasi hubungan non-linear spektral yang kompleks.
    * **1D-Convolutional Neural Networks (CNN):** Pendekatan *deep learning* mutakhir yang mampu mengekstrak fitur secara otomatis dari bentuk kurva.
  * **Metrik Evaluasi Model:**
    * $R^2 > 0.80$, RMSE rendah, dan **RPD (*Residual Predictive Deviation*) $> 2.0$** menunjukkan model kalibrasi sangat handal untuk prediksi rutin operasional.
* **Catatan Pemateri:**
  > "Gambar 7.4 adalah 'resep dapur' spektroskopi tanah. Kita hanya butuh 100 sampel tanah awal yang diuji lab kimia secara akurat untuk melatih model PLSR atau Random Forest kita. Begitu modelnya valid dengan nilai RPD di atas 2,0, maka ribuan titik tanah berikutnya di kebun cukup kita 'tembak' dengan sensor tanpa perlu biaya lab lagi!"

---

### SLIDE 14: IMPLEMENTASI PSS PADA PERKEBUNAN KELAPA SAWIT
* **Kategori:** Aplikasi Lapangan di Perkebunan
* **Judul:** Aplikasi Praktis PSS untuk Peningkatan Produktivitas Kelapa Sawit
* **Layout Visual:** 4 Kartu Studi Kasus Aplikasi Lapangan di Perkebunan Sawit:
  * Kartu 1: Pemetaan Kepadatan Tanah Jalur Panen (Penetrometer $\rightarrow$ Rekomendasi Subsoiling).
  * Kartu 2: Deteksi Dini Lapisan Pirit Dangkal di Lahan Pasang Surut (pXRF $\rightarrow$ Pengendalian Tata Air).
  * Kartu 3: Pemantauan Ketebalan Gambut & Salinitas Pesisir (Sensor EMI / $EC_a$).
  * Kartu 4: Prediksi C-Organik dan Lempung di Bawah Kanopi Rimbun (Spektrometer Vis-NIR Lapangan).
* **Poin Paparan:**
  * PSS memecahkan masalah agronomi sawit spesifik lokasi yang tidak bisa dijawab oleh citra satelit antariksa.
  * Efisiensi biaya: Menghemat anggaran uji lab tanah tahunan perkebunan hingga $70–80\%$.
  * Presisi penempatan input: Memberikan rekomendasi dosis pembenah tanah (dolomit/kapur pada tanah pirit) dan pemupukan berdasarkan variabilitas aktual mikro-blok.
* **Catatan Pemateri:**
  > "Di kebun kelapa sawit kita, PSS bukan barang pajangan. Alat ini menyelamatkan tanaman dari bahaya pirit beracun, membebaskan perakaran dari tanah padat, dan memastikan dosis pemupukan kita presisi. Ini adalah wujud nyata modernisasi agronomi sawit."

---

### SLIDE 15: PENGANTAR DEMONSTRASI ALAT (SIANG NANTI)
* **Kategori:** *Teaser* Sesi Praktik / Demonstrasi
* **Judul:** Sekilas Demonstrasi: Pengujian Sensor Spektrometer Mandiri (*Custom Device*)
* **Layout Visual:**
  * Skema Arsitektur Sistem Instrumen Spektrometer Lapangan Mandiri:
    ![Gambar 7.5: Arsitektur Instrumen Spektrometer Lapangan Mandiri](../assets/modul-7/M7-G05_skema-spektrometer-mandiri.png)
    *Gambar 7.5: Arsitektur Sistem Spektrometer Portabel Mandiri (Custom Vis-NIR Device): Probe Kontak, Mikrokontroler, Antarmuka BLE/USB, dan GUI Python Prediksi Sifat Tanah Instan (< 10 Detik).*
  * Alur demo siang nanti di laboratorium/lapangan:
    1. Kalibrasi panel putih standar pantulan (*white reference*).
    2. Pengukuran sampel tanah uji secara langsung (*instant measurement*).
    3. Transfer data spektrum ke laptop secara nirkabel/kabel.
    4. Eksekusi kode Python praolah dan prediksi sifat tanah instan di layar.
* **Poin Paparan:**
  * Pembuktian bahwa teknologi spektroskopi tidak harus mahal dan tidak harus tergantung pada vendor luar negeri yang bernilai ratusan juta rupiah.
  * Peserta akan melihat langsung proses dari penembakan sensor hingga keluarnya angka estimasi kadar lempung dan bahan organik tanah dalam waktu kurang dari 10 detik!
* **Catatan Pemateri:**
  > "Siang nanti jam 13.00, kita tidak akan berteori lagi. Saya membawa instrumen spektrometer portabel yang kami rancang sendiri. Kita akan mendemonstrasikan bagaimana kita mengukur sampel tanah kebun dan melihat kurva pantulannya keluar seketika di laptop, lalu dihitung sifat tanahnya menggunakan model machine learning. Jangan lewatkan sesi ini!"

---

### SLIDE 16: RANGKUMAN & JEMBATAN KE PEMODELAN DSM
* **Kategori:** Kesimpulan & Jembatan ke Modul 8
* **Judul:** Rangkuman Kunci & Jembatan ke Pemodelan Digital Soil Mapping
* **Layout Visual:** Diagram Segitiga Sinergi Data:
  * Puncak: Remote Sensing Satelit (Kovariat Spasial Makro Seluruh Area).
  * Sudut Kiri: Proximal Soil Sensing (Data Tanah Mikro Rapat di Bawah Tajuk).
  * Sudut Kanan: Algoritma Pemodelan Digital Soil Mapping (Modul 8 - Dr. Guruh Samodra).
* **Poin Paparan:**
  * PSS menjawab kelemahan mendasar citra satelit optik di perkebunan kelapa sawit: PSS bekerja di bawah kanopi rapat dan menembus hingga zona perakaran aktif.
  * Praolah spektrum (Savitzky-Golay, SNV, Continuum Removal) adalah syarat mutlak untuk menghasilkan data spektroskopi yang sahih.
  * **Jembatan ke Modul 8:** Data tanah kerapatan tinggi yang dihasilkan oleh sensor PSS akan diserahkan kepada Dr. Eng. Guruh Samodra sebagai data masukan emas untuk membangun model prediksi spasial *Digital Soil Mapping* berbasis konsep SCORPAN.
* **Catatan Pemateri:**
  > "Bapak dan Ibu sekalian, kita telah menyelesaikan Modul 7. Kita sekarang memiliki senjata lengkap: kita punya citra satelit dari luar angkasa, dan kita punya data sensor proksimal dari bawah tajuk sawit. Bagaimana memadukan kedua data raksasa ini menjadi peta tanah presisi seluruh perkebunan? Jawabannya ada di Modul 8 bersama pakar pemodelan kita, Dr. Guruh Samodra. Sampai bertemu di sesi demonstrasi siang nanti. Terima kasih!"
