# RANCANGAN PRESENTASI (SLIDE DECK) PELATIHAN
## Bagian 4 dan 6: Remote Sensing untuk Estimasi Soil Properties & Interpretasi Pedologis dari Data Remote Sensing

**Pemateri:** Dr. rer. nat. Muhammad Anggri Setiawan, S.Si., M.Si.  
**Institusi:** Pusat Studi Pengelolaan Sumber Daya Lahan (PS2DL), Universitas Gadjah Mada  
**Target Audiens:** Staf Teknis, Agronomis, Peneliti, dan Pengelola Perkebunan Kelapa Sawit (PT SMART Tbk)  
**Alokasi Waktu:** Sesi Ceramah Teori (60–90 Menit)  
**Dokumen Acuan:** `Modul Pelatihan SMART Pemanfaatan RS dan DSM.docx` (Bab 4 dan Bab 6)

---

### PANDUAN VISUAL & IDENTITAS SLIDE (DESIGN SYSTEM)
* **Warna Utama:** Biru Navy UGM (`#1F3A5F`), Hijau Daun Sawit (`#2A9D8F`), Cokelat Tanah / Spektral (`#8C5A3C` / `#B5763F`), Oranye / Aksen Fitur (`#E07B39`).
* **Tipografi:** Sans-serif tegas (Calibri / Carlito / Arial), hierarki judul besar (32–36 pt), subjudul (20–24 pt), teks isi (14–16 pt).
* **Prinsip Tampilan:** Visualisasi kurva spektroskopi resolusi tinggi, penampang geomorfologi, diagram alir interpretasi bertingkat, komparasi visual berdampingan (*side-by-side comparison*).

---

## DAFTAR SLIDE & STRUKTUR MATERI

```
BAGIAN I: ESTIMASI SIFAT TANAH DARI PENGINDERAAN JAUH (Slide 1–11)
  - Slide 1: Judul & Pembuka Sesi
  - Slide 2: Dua Jalur Estimasi Sifat Tanah: Langsung vs. Tidak Langsung
  - Slide 3: Fisika Spektroskopi Tanah: Fitur Serapan Diagnostik Kunci
  - Slide 4: Kromofor Tanah Utama: Mineral Lempung, Oksida Besi, dan Bahan Organik
  - Slide 5: Pengaruh Dinamika Kelembapan dan Struktur Agregat Permukaan
  - Slide 6: Multispektral (Sentinel-2) vs. Hiperspektral (PRISMA/EnMAP)
  - Slide 7: Matriks Indikator Penginderaan Jauh untuk Berbagai Sifat Tanah
  - Slide 8: Ragam Transformasi Indeks Spektral Tanah (BI, SI, HI, RI, Clay Ratio, NSMI)
  - Slide 9: Enam Faktor Pengganggu Sinyal Tanah dan Strategi Pengendaliannya
  - Slide 10: Dilema Tebal Penetrasi Optik (0–2 mm) vs. Kedalaman Perakaran Sawit
  - Slide 11: Rangkuman Bagian 4 & Jembatan ke Interpretasi Pedologis

BAGIAN II: INTERPRETASI PEDOLOGIS DARI DATA REMOTE SENSING (Slide 12–22)
  - Slide 12: Pengantar Interpretasi Pedologis: Membaca Tanah di Balik Lanskap
  - Slide 13: Hipotesis Survei Tanah (Rossiter 2000 & Buringh 1955)
  - Slide 14: Delapan Unsur Interpretasi Citra untuk Analisis Pedologi
  - Slide 15: Pola Aliran dan Pola Erosi sebagai Cerminan Karakteristik Tanah
  - Slide 16: Analisis Tekstur Citra dan Varians Spasial Lokal
  - Slide 17: Menerjemahkan Faktor Pembentuk Tanah ke Kenampakan Citra
  - Slide 18: Penyusunan Kunci Interpretasi Bertingkat (Elimination Key)
  - Slide 19: Metodologi Penarikan Batas: Batas Tegas vs. Batas Bergradasi
  - Slide 20: Pertarungan Konsep: Interpretasi Pedologis vs. Klasifikasi Otomatis (Pixel/ML)
  - Slide 21: Studi Kasus Lapangan: Mengapa Algoritma Tertipu oleh Bayangan dan Blok Sawit?
  - Slide 22: Sintesis Akhir: Menempatkan Nalar Pedologi sebagai Pengendali Model Digital
```

---

## RINCIAN KONTEN PER SLIDE

---

### SLIDE 1: JUDUL & PEMBUKA
* **Kategori:** Cover Presentation
* **Judul Utama:** Remote Sensing untuk Estimasi Soil Properties & Interpretasi Pedologis
* **Sub-judul:** Menghubungkan Respon Spektral Sensor dengan Nalar Pembentukan Tanah di Lanskap Perkebunan
* **Identitas:** Dr. rer. nat. Muhammad Anggri Setiawan, S.Si., M.Si. | Pusat Studi Pengelolaan Sumber Daya Lahan (PS2DL) UGM
* **Layout Visual:**
  * Kiri: Judul presentasi tebal, identitas pemateri, logo UGM & PS2DL.
  * Kanan: Visualisasi berdampingan antara grafik kurva fitur serapan spektral mineral tanah (spektroskopi laboratorium) dan blok diagram interpretasi satuan tanah-lanskap berlereng.
* **Poin Paparan:**
  * Memahami mekanisme fisik bagaimana sifat tanah berinteraksi dengan gelombang elektromagnetik.
  * Membangun kemampuan berpikir pedologis (*pedological thinking*) dalam menafsirkan data penginderaan jauh multi-skala.
* **Catatan Pemateri (Speaker Notes):**
  > "Selamat pagi rekan-rekan agronomis dan pengelola perkebunan. Di sesi ini, kita akan membahas dua modul yang sangat erat hubungannya: Modul 4 tentang bagaimana gelombang cahaya bereaksi terhadap molekul tanah, dan Modul 6 tentang bagaimana pikiran seorang ahli tanah membaca lanskap kebun melalui citra satelit. Kita akan menggabungkan fisika spektral dengan geomorfologi pedologi."

---

### SLIDE 2: DUA JALUR ESTIMASI SIFAT TANAH
* **Kategori:** Arsitektur Konsep
* **Judul:** Dua Jalur Pendugaan Sifat Tanah: Langsung vs. Tidak Langsung
* **Layout Visual:**
  * Diagram Alir Dua Jalur Estimasi:
    ![Gambar 4.1: Jalur Estimasi Sifat Tanah](../assets/modul-4/M4-G01_jalur-estimasi-sifat-tanah.png)
    *Gambar 4.1: Dua Jalur Pendugaan Sifat Tanah dari Penginderaan Jauh: Jalur Langsung (Tanah Terbuka) vs. Jalur Tidak Langsung (Kovariat Lingkungan) (Mulder et al., 2011).*
  * Cabang Kiri (Jalur Langsung): Permukaan Terbuka $\rightarrow$ Interaksi Spektral Kromofor $\rightarrow$ Sifat Aktif Spektral (Tekstur, Besi, Bahan Organik, Kelembapan).
  * Cabang Kanan (Jalur Tidak Langsung): Permukaan Tertutup Vegetasi $\rightarrow$ Deteksi Sinyal Vegetasi / Respon Kanopi Sawit $\rightarrow$ Parameter Topografi (DEM) $\rightarrow$ Sifat Non-Spektral (pH, KTK, Drainase, Hara).
* **Poin Paparan:**
  * **Jalur Langsung (*Direct Sensing*):**
    * Hanya berlaku pada piksel tanah terbuka (*bare soil*).
    * Sensor merekam pantulan langsung dari mineral lempung, oksida besi, dan bahan organik di permukaan.
  * **Jalur Tidak Langsung (*Indirect Sensing*):**
    * Mendominasi perkebunan kelapa sawit dewasa bertajuk rapat.
    * Sifat tanah diduga melalui proksi lingkungan: kesehatan kanopi sawit (NDVI/klorofil), posisi relief dari DEM (arah akumulasi air), dan sejarah bahan induk.
* **Catatan Pemateri:**
  > "Bapak dan Ibu harus jernih membedakan dua jalur ini. Jika tanah tertutup kanopi sawit 100%, Anda tidak bisa mengukur lempung tanah secara langsung dari citra optik. Kita harus beralih ke jalur tidak langsung: memanfaatkan anomali kehijauan daun sawit dan posisi topografinya sebagai proksi kondisi perakaran tanah."

---

### SLIDE 3: FISIKA SPEKTROSKOPI TANAH
* **Kategori:** Spektroskopi Dasar
* **Judul:** Fitur Serapan Diagnostik pada Spektrum Pantulan Tanah
* **Layout Visual:**
  * Kurva Spektral Kontinu dan Lembah Serapan Diagnostik:
    ![Gambar 4.2: Fitur Serapan Spektrum Tanah](../assets/modul-4/M4-G02_fitur-serapan-spektrum-tanah.png)
    *Gambar 4.2: Kurva Spektroskopi Pantulan Tanah dan Fitur Serapan Diagnostik Kunci (Al-OH $2.20\ \mu\text{m}$, O-H / Air Bebas $1.4\ \mu\text{m}$ dan $1.9\ \mu\text{m}$, serta Transisi Elektron Oksida Besi Fe).*
  * Lembah $0.4–1.0\ \mu\text{m}$ (Transisi elektron Fe)
  * Lembah $1.4\ \mu\text{m}$ (Getaran O-H air bebas & kisi kristal)
  * Lembah $1.9\ \mu\text{m}$ (Kombinasi getaran tekuk-rentang $H_2O$)
  * Lembah $2.20\ \mu\text{m}$ (Serapan diagnostik Al-OH mineral lempung kaolinit/illit)
  * Lembah $2.30–2.35\ \mu\text{m}$ (Serapan Mg-OH dan $CO_3^{2-}$ karbonat)
* **Poin Paparan:**
  * Setiap molekul dan mineral tanah memiliki frekuensi getaran resonansi ikatan kimia yang khas.
  * Ketika disinari cahaya matahari, panjang gelombang yang bersesuaian dengan energi getaran tersebut akan diserap (*absorbed*), menghasilkan lembah serapan spektral (*spectral absorption features*).
  * Kedalaman dan luas lembah serapan berkorelasi langsung dengan konsentrasi konstituen tanah tersebut di laboratorium.
* **Catatan Pemateri:**
  > "Mengapa tanah berwarna merah? Mengapa tanah berlempung tinggi memiliki tanda spektral khusus di SWIR? Ini bukan kebetulan visual. Ini adalah hukum spektroskopi molekuler. Di panjang gelombang 2,2 mikron, ikatan aluminium dan hidroksil (Al-OH) pada mineral lempung menyerap energi secara spesifik. Di sinilah letak 'sidik jari' tekstur tanah kita."

---

### SLIDE 4: KROMOFOR UTAMA TANAH
* **Kategori:** Komponen Tanah Aktif Spektral
* **Judul:** Tiga Kromofor Utama Pengendali Pantulan Spektral
* **Layout Visual:** 3 Panel Visual Zat Pewarna Tanah (Kromofor) dan Efek Kurvanya:
  * Panel 1: Mineral Lempung (Kaolinit, Smektit) $\rightarrow$ Lembah tajam di $2.20\ \mu\text{m}$ dan $1.4\ \mu\text{m}$.
  * Panel 2: Oksida Besi (Hematit $\alpha\text{-Fe}_2\text{O}_3$ & Goethit $\alpha\text{-FeOOH}$) $\rightarrow$ Serapan kuat wilayah biru-hijau, warna merah-kuning cerah.
  * Panel 3: Bahan Organik Tanah (SOM / C-Organik) $\rightarrow$ Penurunan albedo secara drastis, perataan kemiringan kurva.
* **Poin Paparan:**
  * **1. Mineral Lempung:** Fitur serapan sempit di wilayah SWIR ($2.1–2.4\ \mu\text{m}$). Semakin tinggi lempung, semakin dalam lembah serapan $2.2\ \mu\text{m}$.
  * **2. Oksida Besi:** Menentukan warna tanah (*soil hue/chroma*). Transisi elektron ion feri ($\text{Fe}^{3+}$) menyerap kuat cahaya biru ($< 0.55\ \mu\text{m}$), memantulkan cahaya merah. Membedakan tanah terlapuk lanjut (Oxisols/Ultisols).
  * **3. Bahan Organik Tanah (SOM):** Bertindak sebagai penyerap cahaya global. Kadar C-organik $> 2\%$ menggelapkan seluruh spektrum tampak dan NIR, menutupi fitur mineral di bawahnya.
* **Catatan Pemateri:**
  > "Jika tanah Anda sangat kaya bahan organik atau gambut, kurva pantulan akan turun drastis ke bawah menjadi sangat gelap. Sebaliknya, pada tanah mineral Ultisol yang teroksidasi kuat di perkebunan kita, oksida besi dan mineral lempung mendominasi pantulan, memberikan warna kemerahan dan serapan khas di SWIR."

---

### SLIDE 5: PENGARUH KELEMBAPAN & STRUKTUR AGREGAT
* **Kategori:** Variabilitas Dinamis Lapangan
* **Judul:** Pengaruh Dinamika Kelembapan dan Kekasaran Permukaan
* **Layout Visual:**
  * Kiri: Grafik perbandingan kurva tanah yang sama pada 4 tingkat kadar air (Kering mutlak, Kapasitas lapang, Jenuh, Tergenang).
  * Kanan: Diagram ilustrasi pemerangkapan cahaya (*light trapping*) pada partikel halus vs. agregat kasar berongga.
* **Poin Paparan:**
  * **Pengaruh Air Tanah:**
    * Molekul air bebas memiliki koefisien serapan tinggi di seluruh rentang optik.
    * Tanah basah memiliki reflektansi jauh lebih rendah dibandingkan tanah kering yang sama, dengan pendalaman ekstrem pada lembah $1.4\ \mu\text{m}$ dan $1.9\ \mu\text{m}$.
  * **Pengaruh Ukuran Butir dan Agregat Permukaan:**
    * Tanah gembur berbutir halus memantulkan cahaya lebih banyak (hamburan balik tinggi).
    * Permukaan tanah beragregat kasar, berbatu, atau berkerak memerangkap cahaya dalam mikrorongga bayangan, menurunkan nilai pantulan spektral yang terekam sensor.
* **Catatan Pemateri:**
  > "Kondisi lapangan sangat dinamis. Tanah lempung yang sama jika direkam pada pagi hari setelah hujan lebat akan memberikan nilai digital yang sama sekali berbeda dibanding saat terekam di puncak musim kemarau. Itulah mengapa koreksi kelembapan dan pemilihan waktu citra mutlak diperlukan."

---

### SLIDE 6: MULTISPEKTRAL VS HIPERSPEKTRAL
* **Kategori:** Kemampuan Sensor
* **Judul:** Sensor Multispektral (Sentinel-2) vs. Hiperspektral (PRISMA/EnMAP)
* **Layout Visual:**
  * Komparasi Kanal Sensor pada Kurva Spektroskopi Tanah:
    ![Gambar 4.2: Spektrum Hiperspektral vs Kanal Lebar Multispektral](../assets/modul-4/M4-G02_fitur-serapan-spektrum-tanah.png)
    *Gambar 4.2(b): Komparasi Kanal Lebar Sentinel-2 MSI (B11 dan B12) terhadap Kurva Spektroskopi Kontinu Hiperspektral pada Wilayah Serapan Lempung SWIR.*
  * Atas: Sensor Hiperspektral (ratusan pita kontinu sempit $\sim 10\ \text{nm}$, mampu menangkap kedalaman lembah serapan Al-OH secara presisi).
  * Bawah: Sensor Multispektral Sentinel-2 (Kanal lebar B11 dan B12 di wilayah SWIR yang hanya menangkap nilai rata-rata agregat).
* **Poin Paparan:**
  * **Multispektral (Sentinel-2 / Landsat-8/9):**
    * Memiliki 10–13 saluran lebar ($20–100\ \text{nm}$).
    * Tidak mampu memisahkan lembah serapan sempit mineral lempung individual, tetapi sangat efektif menghitung rasio indeks permukaan (*Clay Ratio* B11/B12).
    * Resolusi spasial tinggi (10–20 m), gratis, cakupan global rutin 5 harian.
  * **Hiperspektral (PRISMA, EnMAP, EMIT, AVIRIS):**
    * Memiliki 200+ saluran sempit kontinu ($5–10\ \text{nm}$).
    * Mampu melakukan dekonvolusi serapan kimiawi murni dan mengidentifikasi tipe lempung spesifik (kaolinit vs montmorilonit).
    * Keterbatasan: Cakupan sapuan sempit ($30\ \text{km}$), waktu kunjungan ulang rendah, volume data sangat besar.
* **Catatan Pemateri:**
  > "Sentinel-2 adalah 'kuda beban' kita sehari-hari di perkebunan karena ketersediaannya gratis dan rutin. Namun, Sentinel-2 memiliki keterbatasan spektral: ia merata-ratakan wilayah serapan SWIR ke dalam dua saluran (Band 11 dan 12). Jika kita membutuhkan identifikasi mineral lempung spesifik, data hiperspektral seperti EnMAP atau PRISMA adalah rujukan utamanya."

---

### SLIDE 7: MATRIKS INDIKATOR PENGINDERAAN JAUH
* **Kategori:** Tabel Operasional
* **Judul:** Indikator Penginderaan Jauh untuk Karakterisasi Sifat Tanah
* **Layout Visual:** Tabel Komprehensif Berdasarkan Tabel 4.1 Modul (Sifat Tanah | Dasar Keterkaitan | Indikator Spektral/Sensor | Jalur).
* **Poin Paparan:**
  1. **Tekstur (Kadar Lempung):** Serapan gugus Al-OH $2.2\ \mu\text{m}$, rasio SWIR1/SWIR2, dinamika penurunan kelembapan pasca-hujan pada SAR (Jalur Langsung & Tidak Langsung).
  2. **Kelembapan Permukaan:** Pantulan SWIR menurun tajam, hamburan balik SAR meningkat seiring kenaikan konstanta dielektrik tanah basah (Jalur Langsung).
  3. **Bahan Organik (C-Organik):** Penurunan pantulan tampak, indeks kecerahan (BI), indeks warna (Jalur Langsung).
  4. **Oksida Besi (Fe):** Transisi elektron di kanal tampak dan NIR, indeks kemerahan (RI), indeks pewarnaan (CI) (Jalur Langsung).
  5. **Drainase & Muka Air Tanah:** Indeks kebasahan topografi (TWI) dari DEM, persistensi basah multitemporal SAR (Jalur Tidak Langsung).
  6. **pH, KTK, Hara (N, P, K):** Tidak memiliki fitur serapan primer; diduga melalui kovariat vegetasi, bentuklahan, dan korelasi sekunder dengan lempung/SOM (Jalur Tidak Langsung).
* **Catatan Pemateri:**
  > "Tabel ini adalah ringkasan operasional yang wajib dipahami tim GIS estate. Perhatikan baris pH dan hara NPK: hara tanah tidak memiliki sinyal optik primer di citra satelit! Menduga pH dan KTK dari citra satelit murni dilakukan melalui jalur tidak langsung menggunakan model korelasi lingkungan."

---

### SLIDE 8: RAGAM TRANSFORMASI INDEKS SPEKTRAL TANAH
* **Kategori:** Formula & Algoritma Indeks
* **Judul:** Transformasi Indeks Spektral Tanah pada Sentinel-2
* **Layout Visual:** Grid Formula Matematika & Makna Agronomis (Berdasarkan Tabel 4.2 Modul):
* **Poin Paparan:**
  * **Indeks Kecerahan (*Brightness Index - BI*):**
    $$\text{BI} = \sqrt{\frac{R^2 + G^2 + B^2}{3}} = \sqrt{\frac{\text{B4}^2 + \text{B3}^2 + \text{B2}^2}{3}}$$
    * Sensitif terhadap albedo permukaan, kadar bahan organik, dan status kelembapan tanah.
  * **Indeks Kemerahan (*Redness Index - RI*):**
    $$\text{RI} = \frac{R^2}{B \times G^3} = \frac{\text{B4}^2}{\text{B2} \times \text{B3}^3}$$
    * Diagnostik kandungan mineral hematit dan intensitas pelapukan tanah tropis.
  * **Rasio Mineral Lempung (*Clay Ratio*):**
    $$\text{Clay Ratio} = \frac{\text{SWIR1}}{\text{SWIR2}} = \frac{\text{B11}}{\text{B12}}$$
    * Memanfaatkan kontras serapan hidroksil lempung pada kanal $2.19\ \mu\text{m}$ (B12).
  * **Indeks Kelembapan Tanah Ternormalisasi (*NSMI*):**
    $$\text{NSMI} = \frac{\text{B11} - \text{B12}}{\text{B11} + \text{B12}}$$
    * Indikator cepat estimasi kelembapan permukaan tanah terbuka.
* **Catatan Pemateri:**
  > "Mengapa kita melakukan transformasi indeks dan rasio pita? Karena rasio antar-saluran dapat mereduksi gangguan bayangan topografi dan variasi sudut datang matahari. Rasio Band 11 terhadap Band 12 pada Sentinel-2 adalah indikator paling populer untuk mendeteksi konsentrasi lempung tanah terbuka."

---

### SLIDE 9: FAKTOR PENGGANGGU DAN MITIGASINYA
* **Kategori:** Kalibrasi & Koreksi Data
* **Judul:** Enam Faktor Pengganggu Sinyal Tanah dan Pengendaliannya
* **Layout Visual:**
  * Diagram Enam Faktor Pengganggu Sinyal Tanah:
    ![Gambar 4.3: Faktor-Faktor yang Memengaruhi Sinyal Tanah](../assets/modul-4/M4-G03_faktor-sinyal-tanah.png)
    *Gambar 4.3: Enam Faktor Lingkungan yang Memengaruhi Sinyal Penginderaan Jauh Tanah: Atmosfer, Iluminasi/Topografi, Tutupan Permukaan, Kondisi Fisik Tanah, Resolusi Piksel Campuran, dan Kedalaman Sinyal.*
  * Matriks 2 Kolom (Faktor Pengganggu $\rightarrow$ Upaya Pengendalian Teknis):
* **Poin Paparan:**
  1. **Atmosfer (Uap Air, Aerosol):** Gunakan data Level-2A (Bottom-of-Atmosphere / BOA) yang telah dikoreksi Sen2Cor; hindari kanal di luar jendela atmosfer.
  2. **Iluminasi & Topografi:** Lereng yang menghadap matahari berpantulan jauh lebih tinggi dibanding lereng terbayang; gunakan koreksi topografi (*cosine/C-correction*) dengan bantuan DEM teliti.
  3. **Penutup Vegetasi & Serasah:** Menutupi sinyal tanah asli; lakukan penapisan tanah terbuka (*bare soil filtering*) menggunakan ambang NDVI dan NBR2 (Modul 5).
  4. **Kelembapan & Kekasaran Tanah:** Menekan pantulan spektral; standardisasi pemilihan citra pada periode kering seragam.
  5. **Karakteristik Sensor:** Sesuaikan resolusi spasial dan spektral dengan tujuan pemetaan.
  6. **Kedalaman Sinyal:** Sinyal sensor hanya mewakili $0–2\ \text{mm}$ permukaan atas; kalibrasikan secara hati-hati terhadap data laboratorium lapisan profil perakaran.
* **Catatan Pemateri:**
  > "Jangan pernah mengolah citra Level-1C (Top of Atmosphere) mentah untuk estimasi tanah. Uap air di udara tropis akan disangka lempung oleh model Anda! Kita wajib menggunakan produk Level-2A reflektansi permukaan dan melakukan koreksi topografi pada blok-blok kebun yang berbukit."

---

### SLIDE 10: DILEMA PENETRASI OPTIK VS PERAKARAN SAWIT
* **Kategori:** Realitas Biofisik
* **Judul:** Tantangan Kedalaman: Sinyal Permukaan (0–2 mm) vs. Zona Perakaran (0–100 cm)
* **Layout Visual:**
  * Penampang Kedalaman Informasi Sensor vs Profil Tanah:
    ![Gambar 4.3: Kedalaman Informasi yang Terwakili](../assets/modul-4/M4-G03_faktor-sinyal-tanah.png)
    *Gambar 4.3 (Panel Inzet Kanan): Kontras Kedalaman Informasi: Sensor Optik Satelit ($0–2\ \text{mm}$) vs Radar L-band (beberapa cm) vs Lapisan Perakaran Aktif Sawit ($20–80\ \text{cm}$) dan Interval Baku GlobalSoilMap.*
  * Rincian stratifikasi lapisan:
    * Lapisan Paling Atas ($0–2\ \text{mm}$): Sinyal optik satelit (hanya 'kulit' permukaan).
    * Lapisan $0–20\ \text{cm}$: Lapisan olah / penaburan pupuk / seresah piringan.
    * Lapisan $20–60\ \text{cm}$: Zona perakaran aktif kelapa sawit (*active feeding roots*).
    * Lapisan $> 60\ \text{cm}$: Kedalaman air tanah, konkresi pirit, lapisan padas.
* **Poin Paparan:**
  * Sensor optik satelit **tidak memiliki daya tembus kedalaman**; sinyal yang direkam murni berasal dari fraksi milimeter teratas tanah terbuka.
  * Akar sawit menyerap hara dan air pada kedalaman $20–80\ \text{cm}$.
  * Estimasi sifat lapisan bawah (*subsoil*) tidak dapat dilakukan secara langsung, melainkan harus dimodelkan melalui fungsi transfer pedologis (*pedotransfer functions*) atau model korelasi SCORPAN multi-kedalaman (Modul 8).
* **Catatan Pemateri:**
  > "Ini adalah peringatan penting bagi kita semua: satelit optik tidak bisa melihat apa yang ada di kedalaman 50 cm di bawah tanah! Yang dilihat satelit hanya 'kulit ari' tanah setebal 2 milimeter. Untuk memetakan profil tanah sawit yang dalam, kita membutuhkan jembatan penalaran pedologis dan pemodelan kovariat lingkungan."

---

### SLIDE 11: RANGKUMAN BAGIAN 4 & JEMBATAN KE BAGIAN 6
* **Kategori:** Transisi Materi
* **Judul:** Rangkuman Estimasi Spektral & Membuka Nalar Pedologi
* **Layout Visual:** Diagram Transisi: Fisika Spektral Tanah (Mikro/Piksel) $\rightarrow$ Jembatan Pemikiran $\rightarrow$ Interpretasi Pedologis Lanskap (Makro/Bentanglahan).
* **Poin Paparan:**
  * Estimasi langsung terbatas pada tanah terbuka dan sifat aktif spektral; estimasi tidak langsung memerlukan kovariat lingkungan.
  * Namun, apakah memetakan tanah cukup hanya dengan menghitung nilai piksel indeks spektral? **TIDAK.**
  * Komputer hanya melihat angka numerik reflektansi, tetapi seorang pedologis melihat sejarah bentanglahan, arah erosi, akumulasi air, dan proses pembentukan tanah di baliknya.
  * Kita melangkah ke Bagian 6: **Interpretasi Pedologis dari Data Remote Sensing**.
* **Catatan Pemateri:**
  > "Setelah kita memahami rumus dan indeks spektral di Bagian 4, sekarang kita akan masuk ke 'jiwa' dari pemetaan tanah di Bagian 6. Bagaimana kita membaca sebuah citra satelit bukan sekadar sebagai kumpulan angka piksel, melainkan sebagai sebuah bentanglahan hidup yang memiliki sejarah pembentukan tanah? Mari kita masuk ke Interpretasi Pedologis."

---

### SLIDE 12: MEMBACA TANAH DI BALIK LANSKAP
* **Kategori:** Pengantar Bagian 6 - Interpretasi Pedologis
* **Judul:** Hakikat Interpretasi Pedologis: Melihat yang Tak Tampak
* **Layout Visual:**
  * Kiri: Foto permukaan kebun sawit rimbun (tanah tidak terlihat sama sekali).
  * Kanan: Diagram blok interpretasi pedologis yang memperlihatkan profil tanah di bawah tegakan sawit berdasarkan posisi lereng dan pola drainase.
* **Poin Paparan:**
  * **Masalah Fundamental:** Tanah pada citra satelit hampir selalu tertutup oleh tajuk vegetasi (pohon sawit, semak, LCC) atau lapisan serasah (Buringh 1955).
  * **Definisi Interpretasi Pedologis:** Proses deduktif-ilmiah menerjemahkan kenampakan lanskap luar yang tampak pada citra menjadi informasi sebaran, batas, dan sifat tanah di bawahnya.
  * Berbeda dengan pemetaan tutupan lahan biasa, interpretasi pedologis menuntut integrasi antara geomorfologi, hidrologi, dan genesis tanah.
* **Catatan Pemateri:**
  > "Profesor Buringh sejak tahun 1955 sudah menegaskan: menafsirkan tanah dari foto udara sangat berbeda dengan menafsirkan jalan atau pohon. Pohon sawit tampak nyata di foto. Tanah tidak tampak! Namun, pohon sawit yang menguning di cekungan rendahan memberi tahu kita bahwa di bawahnya ada masalah drainase atau pirit dangkal. Kita membaca tanah dari petunjuk lingkungannya."

---

### SLIDE 13: HIPOTESIS SURVEI TANAH (ROSSITER 2000)
* **Kategori:** Landasan Teori Ilmiah
* **Judul:** *The Soil Survey Hypothesis*: Dasar Logika Delineasi Tanah
* **Layout Visual:** Box Quote Ilmiah David Rossiter (2000) diapit oleh 4 Pilar Kenampakan Eksternal:
  * Pilar 1: Bentuklahan & Geomorfologi (*Landform*)
  * Pilar 2: Tipe Vegetasi Alami & Respons Tanaman (*Vegetation/Crop Status*)
  * Pilar 3: Penggunaan Lahan & Pola Pertanian (*Land Use*)
  * Pilar 4: Litologi & Sejarah Permukaan (*Surface Geology*)
* **Poin Paparan:**
  * **Hipotesis Survei Tanah (Rossiter 2000):**
    > *"Pola sebaran tanah di alam tidak acak, melainkan dapat diprediksi dan berkorelasi kuat dengan kenampakan bentanglahan luar yang lebih mudah diamati dan dipetakan melalui penginderaan jauh."*
  * Korelasi bentanglahan-tanah (*landscape-soil correlation*) memungkinkan penarikan batas satuan tanah secara efisien tanpa harus menggali lubang tanah di setiap meter persegi.
* **Catatan Pemateri:**
  > "Tanah di alam tidak jatuh dari langit secara acak. Tanah adalah hasil interaksi bentanglahan selama ribuan tahun. Karena kita bisa melihat bentuklahan dan pola aliran air di citra satelit, kita bisa menduga di mana batas perubahan sifat tanah terjadi. Inilah inti dari hipotesis survei tanah."

---

### SLIDE 14: DELAPAN UNSUR INTERPRETASI CITRA UNTUK PEDOLOGI
* **Kategori:** Metodologi Interpretasi Citra
* **Judul:** Delapan Unsur Interpretasi Citra dalam Konteks Pedologi
* **Layout Visual:** Matriks 8 Kartu Elemen Interpretasi (Lillesand et al. 2015; NRCan 2025):
* **Poin Paparan:**
  1. **Rona & Warna (*Tone/Color*):** Mencerminkan kelembapan tanah, kandungan bahan organik, dan status klorofil tanaman penutup.
  2. **Bentuk (*Shape*):** Mengidentifikasi satuan geomorfik (kipas aluvial, tanggul alam/levee, bukit sisa, teras sungai).
  3. **Ukuran (*Size*):** Dimensi fisik bentuklahan untuk mencocokkan dengan skala survei dan ambang batas MLA.
  4. **Pola (*Pattern*):** Pola spasial teratur atau berulang (pola drainase, pola singkapan, terasering).
  5. **Tekstur (*Texture*):** Tingkat kehalusan/kekasaran visual citra; tekstur kasar tajuk sawit tua vs tekstur halus semak/tanaman muda.
  6. **Bayangan (*Shadow*):** Menegaskan relief mikro dan makro lereng; waspada distorsi bayangan matahari.
  7. **Situs (*Site*):** Posisi topografi relatif (puncak igir, lereng terjal, kaki bukit, dasar rawa).
  8. **Asosiasi (*Association*):** Hubungan keterkaitan logis (rawa selalu berasosiasi dengan tanah histosol/gambut atau gleysol; tanggul alam berasosiasi dengan tanah fluvent bertekstur pasiran).
* **Catatan Pemateri:**
  > "Delapan unsur interpretasi ini bukan sekadar hafalan geografi dasar. Bagi seorang pedologis, unsur 'Asosiasi' dan 'Situs' adalah yang paling kuat. Jika Anda melihat posisi lahan berada di dataran banjir sungai dengan pola meander, secara pedologis asosiasinya pasti tanah aluvial muda (Entisol/Inceptisol), bukan tanah tua Ultisol yang masam."

---

### SLIDE 15: POLA ALIRAN DAN EROSI SEBAGAI CERMINAN TANAH
* **Kategori:** Analisis Morfometri & Drainase
* **Judul:** Pola Aliran Sungai dan Pola Erosi Mencerminkan Sifat Tanah
* **Layout Visual:**
  * Diagram 4 Pola Aliran Permukaan Utama:
    ![Gambar 6.1: Pola Aliran Permukaan dan Pengontrolnya](../assets/modul-6/M6-G01_pola-aliran-dan-pengontrolnya.png)
    *Gambar 6.1: Empat Pola Aliran Permukaan Utama dan Pengontrol Struktur/Litologi Bawah Permukaannya: (a) Dendritik, (b) Paralel, (c) Rektangular, dan (d) Trellis.*
  * Rincian karakter:
    * (a) Dendritik (Material homogen, batuan sedimen mendatar/vulkanik, permeabilitas seragam).
    * (b) Paralel (Kelerengan curam seragam atau kontrol struktur patahan/kekar).
    * (c) Rektangular (Dikendalikan oleh rekahan/kekar batuan dasar saling tegak lurus).
    * (d) Trellis (Perlapisan batuan keras dan lunak berselingan, punggungan antiklin/sinklin).
* **Poin Paparan:**
  * Jaringan drainase permukaan adalah ekspresi langsung dari permeabilitas, ketahanan erosi, dan struktur batuan di bawah tanah.
  * **Kerapatan Aliran (*Drainage Density*):**
    * Kerapatan aliran tinggi: Permeabilitas tanah rendah (lempung berat, limpasan permukaan tinggi, mudah tererosi).
    * Kerapatan aliran rendah: Permeabilitas tanah tinggi (tanah pasiran porous atau batuan berpori, air meresap cepat).
  * Pola erosi parit (*gully erosion*) yang tampak pada foto udara menandakan solum tanah tebal yang rentan dispersi pada lereng rentan.
* **Catatan Pemateri:**
  > "Perhatikan pola alur air di afdeling kebun Anda dari foto udara. Jika cabang-cabang sungai kecil sangat rapat seperti jaring laba-laba, itu indikator mutlak bahwa tanah tersebut berlempung berat dengan infiltrasi rendah sehingga air lari di permukaan. Jika air tidak tampak mengalir di permukaan, tanahnya sangat porous atau berpasir."

---

### SLIDE 16: TEKSTUR CITRA DAN VARIABILITAS LOKAL
* **Kategori:** Analisis Statistik Spasial
* **Judul:** Analisis Tekstur Citra dan Simpangan Baku Lokal
* **Layout Visual:**
  * Komparasi Visual Tekstur Citra dan Skala Jendela:
    ![Gambar 6.2: Tekstur Citra dan Simpangan Baku Lokal](../assets/modul-6/M6-G02_tekstur-citra-dan-simpangan-baku-lokal.png)
    *Gambar 6.2: Kuantifikasi Tekstur Citra Menggunakan Filter Simpangan Baku Lokal: (a) Citra Asli Perkebunan, (b) Jendela $3\times 3$ Piksel (Mikro-tekstur Tajuk Sawit Individual), dan (c) Jendela $15\times 15$ Piksel (Makro-bentanglahan).*
  * Panel (a) Citra asli perkebunan dengan variasi kanopi.
  * Panel (b) Peta simpangan baku lokal jendela kecil ($3 \times 3$ piksel) $\rightarrow$ Menonjolkan tepi blok dan pohon individual.
  * Panel (c) Peta simpangan baku lokal jendela besar ($15 \times 15$ piksel) $\rightarrow$ Menggeneralisasi variasi makro bentanglahan.
* **Poin Paparan:**
  * Tekstur pada citra optik mencerminkan frekuensi perubahan rona/warna dalam area tertentu.
  * Tekstur dapat dikuantifikasi secara matematis menggunakan filter simpangan baku lokal (*local standard deviation*) atau matriks GLCM (*Gray-Level Co-occurrence Matrix*).
  * Pada perkebunan kelapa sawit:
    * Tekstur halus: Sawah, permukaan air, tanah terbuka rata, tanaman penutup tanah homogen.
    * Tekstur kasar/bintik-bintik: Blok kelapa sawit dewasa (tajuk berulang dan bayangan sela pelepah).
* **Catatan Pemateri:**
  > "Tekstur membantu kita memisahkan batas tanaman homogen dengan semak liar atau vegetasi riparian alami di sepanjang sempadan sungai kebun sawit. Filter simpangan baku lokal adalah alat bantu kuantitatif untuk mempertajam batas tekstur tersebut."

---

### SLIDE 17: FAKTOR PEMBENTUK TANAH PADA DATA CITRA
* **Kategori:** Tabel Sintesis Pedologi
* **Judul:** Menerjemahkan 5 Faktor Pembentuk Tanah ke Kenampakan Citra
* **Layout Visual:** Tabel Komprehensif Berdasarkan Tabel 6.1 Modul (Faktor | Kenampakan Citra | Petunjuk Pedologis | Catatan Praktis).
* **Poin Paparan:**
  1. **Relief:** Bentuk/kemiringan lereng, bayangan medan, model elevasi digital $\rightarrow$ Membedakan proses erosi (puncak), transportasi (lereng), dan deposisi koluvial (kaki lereng). **Faktor paling dominan pembeda tanah pada skala kebun!**
  2. **Bahan Induk:** Pola aliran, bentanglahan, rona singkapan batuan $\rightarrow$ Menentukan tekstur bawaan, cadangan mineral primer, dan tipe lempung.
  3. **Waktu (Umur Geomorfik):** Tingkat diseksi lereng, teras sungai bertingkat $\rightarrow$ Mengindikasikan stadium perkembangan profil (Entisol muda vs Ultisol/Oxisol tua).
  4. **Organisme:** Pola tutupan vegetasi, sejarah bukaan kebun $\rightarrow$ Mengindikasikan akumulasi bahan organik dan bioperturbasi.
  5. **Kondisi Air/Hidrologi:** Rona basah gelap, vegetasi rawa indikator, jalur depresi $\rightarrow$ Menentukan kelas drainase tanah dan kedalaman jeluk pirit/karat redoks.
* **Catatan Pemateri:**
  > "Dalam skala satu estate kelapa sawit ($10.000–20.000\ \text{ha}$), faktor iklim makro praktis seragam. Yang menyebabkan tanah di Blok A berbeda dengan Blok B adalah RELIEF dan BAHAN INDUK. Oleh karena itu, fokus utama interpretasi citra kita harus tertuju pada analisis morfologi medan dan litologi."

---

### SLIDE 18: KUNCI INTERPRETASI BERTINGKAT
* **Kategori:** Operasional Delineasi
* **Judul:** Penyusunan Kunci Interpretasi Bertingkat (*Hierarchical Elimination Key*)
* **Layout Visual:**
  * Diagram Pohon Keputusan Pedologis:
    ![Gambar 6.3: Contoh Kunci Interpretasi Bertingkat](../assets/modul-6/M6-G03_contoh-kunci-interpretasi-bertingkat.png)
    *Gambar 6.3: Pohon Keputusan Kunci Interpretasi Bertingkat (Hierarchical Elimination Key): Dari Bentuklahan Makro, Posisi Lereng, Litologi, hingga Kelas Drainase Tanah.*
  * Level 1: Bentuklahan Makro (Perbukitan Denudasional vs Dataran Aluvial / Rawa).
  * Level 2: Posisi Lereng (Punggungan / Lereng Atas / Lereng Bawah / Lembah).
  * Level 3: Bahan Induk / Litologi (Breksi Vulkanik vs Endapan Koluvial Aluvial).
  * Level 4: Status Drainase (Baik, Sedang, Terhambat/Gleisasi).
* **Poin Paparan:**
  * Kunci interpretasi bertingkat memandu penafsir bekerja secara sistematis dari fenomena makro ke detail mikro.
  * Mengeliminasi ambiguitas visual: rona gelap di dataran aluvial diartikan sebagai tanah tergenang (*poorly drained*), sedangkan rona gelap di punggungan bukit diartikan sebagai tanah kaya bahan organik atau bayangan awan.
  * Kunci interpretasi harus didokumentasikan tertulis agar proses delineasi dapat diuji dan direproduksi oleh analis lain.
* **Catatan Pemateri:**
  > "Jangan mendelineasi tanah secara acak melompat-lompat. Buat kunci eliminasi bertingkat seperti pada Gambar 6.3. Pertama, pisahkan dulu dataran dari perbukitan. Di perbukitan, bagi menjadi punggungan dan lereng. Di dataran, pisahkan yang tergenang dan yang kering. Bekerja terstruktur seperti ini menjamin peta tanah Anda logis."

---

### SLIDE 19: METODOLOGI PENARIKAN BATAS: TEGAS VS BERGRADASI
* **Kategori:** Kartografi Batas Tanah
* **Judul:** Menarik Garis Batas: Batas Tegas (*Abrupt*) vs. Batas Bergradasi (*Gradational*)
* **Layout Visual:**
  * Ilustrasi Prinsip Bukti Konvergen:
    ![Gambar 6.4: Konvergensi Batas Analisis Unsur](../assets/modul-6/M6-G04_konvergensi-batas-analisis-unsur.png)
    *Gambar 6.4: Prinsip Bukti Konvergen (Converging Evidence): Menarik Batas Satuan Peta Tanah Transisi Berdasarkan Tumpang Susun Garis Batas Rona, Vegetasi, dan Tekuk Lereng.*
  * Kiri: Ilustrasi Batas Tegas (Kontak sesar geologi tajam atau tekuk lereng terjal tanggul alam).
  * Kanan: Ilustrasi Batas Bergradasi & Pembobotan Batas Konvergen.
* **Poin Paparan:**
  * Di alam nyata, batas tanah terbagi menjadi dua tipe:
    1. **Batas Tegas (*Sharp Boundaries*):** Terjadi akibat diskontinuitas litologi tajam (misal kontak intrusi basal dengan batu pasir) atau tekuk lereng struktural patahan.
    2. **Batas Bergradasi (*Gradual / Diffuse Boundaries*):** Terjadi pada toposekuen lereng yang landai, di mana tanah perlahan berubah dari drainase baik ke drainase agak terhambat sepanjang ratusan meter.
  * **Prinsip *Converging Evidence* (Pembobotan Konvergen):**
    * Garis batas ditarik pada zona di mana batas perubahan lereng, batas rona citra, dan batas vegetasi saling berimpit atau berdekatan (Gambar 6.4).
* **Catatan Pemateri:**
  > "Seorang surveyor sering bingung: 'Pak, di lereng landai ini, di mana persisnya saya harus menggoreskan garis batas poligon?' Gunakan prinsip bukti konvergen. Periksa di mana garis tekuk lereng bertemu dengan perubahan rona kelembapan citra. Garis kompromi itulah batas satuan peta tanah terbaik."

---

### SLIDE 20: INTERPRETASI PEDOLOGIS VS KLASIFIKASI OTOMATIS
* **Kategori:** Komparasi Metodologis Utama
* **Judul:** Benturan Paradigma: Interpretasi Pedologis vs. Klasifikasi Citra Otomatis
* **Layout Visual:** Tabel Komparasi Menyeluruh (Tabel 6.2 Modul):
  * Aspek: Satuan Analisis | Informasi Digunakan | Dasar Penalaran | Kekuatan | Keterbatasan Utama.
  * Kolom: Interpretasi Pedologis vs. Klasifikasi Berbasis Piksel vs. Klasifikasi Objek/Machine Learning.
* **Poin Paparan:**
  * **Klasifikasi Berbasis Piksel (Isodata, Maximum Likelihood):**
    * Murni mengelompokkan kemiripan spektral per sel. Sangat cepat, tetapi menghasilkan efek *salt-and-pepper* (bintik-bintik acak) dan tertipu oleh bayangan atau fase tanaman.
  * **Klasifikasi Berbasis Objek (OBIA) & Machine Learning:**
    * Mengelompokkan piksel menjadi segmen objek berdasarkan spektral dan bentuk. Lebih rapi, namun segmen sering kali hanya mengikuti petak blok jalan buatan manusia, bukan satuan tanah alami.
  * **Interpretasi Pedologis:**
    * Menggunakan nalar hubungan bentanglahan-tanah (*soil-landscape relationship*). Mampu melihat menembus kanopi vegetasi dan mengabaikan gangguan sesaat.
* **Catatan Pemateri:**
  > "Ini adalah tabel paling krusial di Modul 6. Mengapa kita tidak menyerahkan pemetaan tanah sepenuhnya kepada algoritma klasifikasi citra otomatis? Karena komputer tidak punya pengetahuan pedologi! Komputer hanya mengelompokkan warna piksel yang sama. Jika satu blok sawit terbayang awan, komputer akan mengklasifikasikannya sebagai jenis tanah yang berbeda. Ini fatal!"

---

### SLIDE 21: STUDI KASUS: JEBAKAN ILUMINASI DAN BLOK KEBUN
* **Kategori:** Studi Kasus Visual Lapangan
* **Judul:** Bukti Lapangan: Mengapa Algoritma Komputer Tertipu di Kebun Berbukit?
* **Layout Visual:**
  * Komparasi Hasil Klasifikasi Otomatis vs Delineasi Pedologis:
    ![Gambar 6.5: Perbandingan Klasifikasi Citra dan Interpretasi Pedologis](../assets/modul-6/M6-G05_perbandingan-klasifikasi-dan-interpretasi.png)
    *Gambar 6.5: Komparasi Bukti Lapangan Kebun Berbukit: (a) Klasifikasi Piksel (Tercemar Bayangan), (b) Klasifikasi Objek (Terkunci Blok Jalan), dan (c) Delineasi Pedologis Ahli yang Menghormati Kontur Alami.*
  * Panel (a) Klasifikasi Berbasis Piksel: Blok sawit di lereng terbayangi salah terklasifikasi; poligon hancur berbintik-bintik.
  * Panel (b) Klasifikasi Berbasis Objek (OBIA): Segmen rapi tetapi terkunci pada batas blok jalan buatan manusia; mewarisi kesalahan iluminasi bayangan lereng.
  * Panel (c) Interpretasi Pedologis Ahli: Batas satuan tanah memotong batas blok kebun secara logis, mengikuti punggungan bukit, lereng tengah, kaki lereng, dan dasar lembah.
* **Poin Paparan:**
  * Batas afdeling atau blok jalan kelapa sawit dibuat oleh manusia dengan garis lurus geometris, sedangkan batas satuan tanah di alam mengikuti kontur dan morfologi bentanglahan.
  * Klasifikasi otomatis berbasis citra optik selalu terdistorsi oleh perbedaan iluminasi lereng yang menghadap vs membelakangi matahari.
  * Penafsir pedologis memahami bahwa lereng yang terkena sinar matahari dan lereng yang terbayangi di punggungan yang sama memiliki bahan induk dan proses genesis tanah yang identik.
* **Catatan Pemateri:**
  > "Lihat Gambar 6.5 di layar. Panel kiri dan tengah adalah hasil algoritma komputer tanpa ahli pedologi: batasnya mengikuti jalan kebun dan terbelah oleh bayangan matahari. Sekarang lihat panel kanan: ahli pedologi menarik garis batas melengkung memotong jalan kebun karena bentuk bukitnya memang melengkung. Peta tanah yang benar untuk agronomi adalah panel kanan!"

---

### SLIDE 22: SINTESIS: NALAR PEDOLOGI SEBAGAI KEMUDI MODEL DIGITAL
* **Kategori:** Kesimpulan & Integrasi
* **Judul:** Menempatkan Nalar Pedologi sebagai Pengendali Model Digital
* **Layout Visual:** Diagram Siklus Sinergi: Nalar Pedologi (Geomorfologi & Kunci Interpretasi) $\leftrightarrow$ Data Remote Sensing Multispektral $\leftrightarrow$ Algoritma Pemodelan Digital Soil Mapping.
* **Poin Paparan:**
  * Estimasi spektral sifat tanah (Modul 4) memberikan data kuantitatif pada piksel tanah terbuka dan indeks kovariat permukaan.
  * Interpretasi pedologis (Modul 6) menyediakan kerangka konseptual bentanglahan yang mencegah model digital menghasilkan prediksi yang konyol secara logika alam.
  * **Pesan Kunci untuk Praktisi:**
    * *Machine learning* dan *remote sensing* adalah akselerator dan pengukur yang luar biasa cepat.
    * Namun, nalar pedologi adalah **kemudi (*steering wheel*)** yang menjamin peta tanah yang dihasilkan dapat dipertanggungjawabkan secara ilmiah dan operasional perkebunan.
* **Catatan Pemateri:**
  > "Bapak dan Ibu sekalian, kesimpulan dari Modul 4 dan 6: teknologi satelit mutakhir dan kecerdasan buatan hanyalah instrumen pengukur. Tanpa pemahaman pedologi di kepala kita, angka-angka itu tidak bermakna. Jadikan nalar pedologi sebagai nahkoda, dan jadikan remote sensing sebagai mata kita. Sesi berikutnya akan membahas bagaimana kita mengekstrak tanah terbuka di bawah tajuk sawit bersama Dr. Retnadi. Terima kasih."
