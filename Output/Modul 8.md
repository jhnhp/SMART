# Pemodelan Digital Soil Mapping

*Ceramah dan diskusi:*

## SCORPAN Sebagai Variabel Lingkungan

Modul 1 telah memperkenalkan SCORPAN sebagai kerangka pemetaan tanah digital. Kerangka ini berangkat dari model faktor pembentuk tanah Jenny, yang menyatakan tanah sebagai fungsi iklim, organisme, relief, bahan induk, dan waktu. McBratney et al. (2003) menambahkan dua faktor lagi, yaitu tanah itu sendiri dan posisi spasial, sehingga terbentuk model spasial yang menyatakan hubungan kuantitatif antara sifat atau kelas tanah di suatu lokasi dan kondisi lingkungannya (Wadoux, Minasny, & McBratney, 2020). Model tersebut dapat dituliskan sebagai berikut:

$$S = f(s, c, o, r, p, a, n) + e$$

dengan $S$ adalah sifat atau kelas tanah yang dipetakan, $s$ adalah informasi tanah yang telah diketahui, $c$ iklim, $o$ organisme, $r$ relief, $p$ bahan induk, $a$ umur, $n$ posisi spasial, $f$ fungsi yang menghubungkan $S$ dengan ketujuh faktor tersebut, dan $e$ bagian keragaman yang tidak dijelaskan oleh faktor-faktor itu. Fungsi $f$ tidak diturunkan dari teori, tetapi dipelajari dari data, yaitu dari pasangan nilai tanah hasil pengamatan dan nilai faktor lingkungan di lokasi yang sama. Karena itu, setiap faktor harus diwujudkan sebagai data spasial yang tersedia di seluruh wilayah yang akan dipetakan. Data inilah yang disebut kovariat atau variabel lingkungan.

Penginderaan jauh berperan besar dalam kerangka ini karena citra dan model elevasi tersedia menyeluruh, sedangkan tanah sendiri jarang teramati secara langsung. Mulder et al. (2011) menyebut penginderaan jauh dalam pemetaan tanah terutama sebagai sumber informasi lingkungan pengganti. Jumlah kovariat yang dipakai sangat beragam. SoilGrids 2.0 memetakan sifat tanah dunia pada resolusi 250 m dengan lebih dari 400 kovariat global yang menggambarkan vegetasi, morfologi medan, iklim, geologi, dan hidrologi, ditambah data tanah dari sekitar 240.000 lokasi (Poggio et al., 2021). Penelitian pada skala yang lebih kecil umumnya memakai sekitar 20 kovariat, dan hanya sedikit yang memakai kurang dari lima atau lebih dari 100 (Wadoux, Minasny, & McBratney, 2020). Kovariat yang paling sering dipakai adalah peta sifat atau kelas tanah yang sudah ada, rerata jangka panjang curah hujan dan suhu, citra penginderaan jauh dan indeks vegetasi, elevasi beserta atribut medan seperti kemiringan, kelengkungan, dan indeks kebasahan topografi (TWI), serta peta geologi. Contoh kovariat untuk setiap faktor beserta sumber datanya dirangkum pada Tabel 8.1.

Tabel 8.1 Faktor SCORPAN, Contoh Kovariat, dan Sumber Datanya

| **Faktor** | **Contoh kovariat** | **Sumber data** | **Catatan untuk perkebunan kelapa sawit** |
| :---------: | :-----------------: | :-----------------: | :-----------------: |
| s (tanah) | Peta tanah warisan, peta sifat tanah, data sensor proksimal | Survei terdahulu, ECa dan sinar gamma (Modul 7) | Peta tanah lama dapat dirinci dengan disagregasi; data PSS yang rapat menjadi kovariat lokal |
| c (iklim) | Curah hujan dan suhu rata-rata jangka panjang | Stasiun cuaca, produk iklim global | Jarang bervariasi di dalam satu kebun (Tabel 6.1) |
| o (organisme) | Indeks vegetasi, tutupan dan penggunaan lahan, komposit tanah terbuka | Citra optik multitemporal (Modul 4 dan 5) | Tajuk sawit lebih mencerminkan umur dan kondisi tanaman; pantulan tanah hanya terekam saat tanah terbuka |
| r (relief) | Elevasi, kemiringan, kelengkungan, TPI, TWI, MrVBF | Model elevasi digital dari radar satelit, LiDAR, atau peta topografi | Tetap tersedia di bawah tajuk; sering paling informatif untuk kelembapan dan drainase |
| p (bahan induk) | Satuan geologi, litologi, data radiometrik | Peta geologi, spektrometer sinar gamma | Skala peta geologi perlu diperiksa terhadap skala kebun |
| a (umur) | Umur relatif permukaan geomorfik, teras | Peta geomorfologi, interpretasi citra (Modul 6) | Umumnya hanya memberi urutan umur relatif |
| n (posisi) | Koordinat, peta jarak | Diturunkan dari lokasi pengamatan | Dapat menimbulkan artefak dan menyulitkan tafsiran model |

Sumber: Rangkuman penulis berdasarkan McBratney et al. (2003), Wadoux, Minasny, dan McBratney (2020), Poggio et al. (2021), dan Ågren et al. (2014)

Sebagian besar kovariat berupa lapisan raster yang menutupi seluruh wilayah, seperti diilustrasikan pada Gambar 8.1. Kovariat relief diturunkan dari model elevasi, kovariat organisme dari citra, dan kovariat bahan induk dari peta geologi. Nilai setiap lapisan kemudian diambil di titik-titik sampel tanah. Perhatikan bahwa pola kovariat organisme pada contoh tersebut mengikuti blok kebun, sedangkan pola kovariat relief mengikuti bentuk lahan.

![](assets/modul-8/M8-G01_kovariat-scorpan-sebagai-lapisan-raster.png)

Gambar 8.1 Ilustrasi kovariat SCORPAN sebagai lapisan raster pada sebuah kebun dan titik sampel tanah di atasnya

Sumber: Ilustrasi konseptual dengan data sintetis; jenis kovariat mengacu pada Wadoux, Minasny, dan McBratney (2020)

Faktor tanah, bahan induk, umur, dan posisi lebih sulit diwujudkan sebagai kovariat daripada relief dan organisme. Peta tanah warisan dapat dipakai langsung sebagai kovariat kategorik, atau dirinci lebih dulu dengan teknik disagregasi spasial, yaitu memisahkan satuan peta tanah menjadi bagian-bagian yang lebih rinci berdasarkan hubungan tanah–lanskap. Sulaeman dan Husnain (2021) menilai teknik ini bermanfaat di Indonesia untuk merinci peta, menyelaraskan batas antarpeta, dan memetakan wilayah baru dengan memakai hubungan tanah–lanskap dari wilayah lain. Informasi bahan induk juga berharga. Cahyana et al. (2023) melaporkan bahwa informasi bahan induk memperbaiki hasil pemetaan tanah digital di Bogor. Faktor posisi biasanya diwakili oleh koordinat atau peta jarak. Kovariat semacam ini dapat mengurangi autokorelasi residual, tetapi koordinat cenderung menimbulkan artefak pada peta yang dibuat dengan algoritme berbasis pohon. Peta jarak juga tidak bermakna pedologis, sehingga menyulitkan tafsiran model (Wadoux, Minasny, & McBratney, 2020).

Kovariat tidak perlu dikumpulkan sebanyak-banyaknya. Poggio et al. (2021) menyeleksi kovariatnya untuk mengurangi kemiripan antarkovariat, memperoleh model yang lebih sederhana dan efisien, menurunkan risiko *overfitting*, yaitu model yang terlalu menyesuaikan diri dengan data latih, serta menghindari penilaian tingkat kepentingan variabel yang bias. Untuk kebutuhan kebun, kriteria pemilihan kovariat dapat dirumuskan sebagai berikut:

1. **Relevansi pedologis**, yaitu kovariat mewakili faktor yang secara masuk akal mengendalikan sifat tanah sasaran. Kadar lempung, misalnya, lebih berkaitan dengan bahan induk dan posisi lereng daripada dengan indeks vegetasi tajuk sawit.

2. **Kesesuaian resolusi dan skala**, yaitu ukuran piksel kovariat sepadan dengan keragaman yang ingin dipetakan dan dengan skala peta (Modul 3). Nilai TWI peka terhadap resolusi DEM, sedangkan TPI bergantung pada skala analisisnya (Ågren et al., 2014).

3. **Ketersediaan yang menyeluruh dan seragam**, yaitu kovariat tersedia untuk seluruh wilayah prediksi dengan mutu yang sama, karena model hanya dapat memprediksi di tempat nilai kovariatnya diketahui.

4. **Kesesuaian waktu**, yaitu kovariat yang berubah menurut waktu, seperti citra, direkam pada periode yang sesuai dengan sifat tanah yang dipetakan dan dengan waktu pengambilan sampel.

5. **Tidak berlebihan**, yaitu kovariat yang sangat mirip satu sama lain cukup diwakili oleh salah satunya.

Kriteria pertama paling sering terlewat. Model pembelajaran mesin dapat tampak akurat meskipun memakai kovariat semu yang tidak berhubungan dengan pembentukan tanah, sebagaimana dibahas dalam Modul 6 (Wadoux, Samuel-Rosa, et al., 2020). Pemilihan kovariat karena itu sebaiknya dimulai dari pengetahuan pedologis, lalu diperkuat dengan seleksi statistik. Seleksi statistik dapat memangkas kovariat secara drastis. Dalam perbandingan Nussbaum et al. (2018), lasso dan dua metode lain hanya mempertahankan 3–6% dari 300–500 kovariat yang tersedia, dan perbedaan ketelitian antarmetode umumnya kecil.

Kondisi perkebunan kelapa sawit menuntut perhatian khusus pada kovariat organisme dan relief. Tajuk sawit yang telah menutup menghalangi pantulan tanah (Modul 5), sehingga indeks vegetasi di blok yang tanamannya sudah menghasilkan lebih mencerminkan umur dan kondisi tanaman daripada tanah. Informasi spektral tanah hanya dapat diperoleh dari periode tanah terbuka, misalnya saat peremajaan, melalui komposit citra tanah terbuka. Kovariat relief sebaliknya tetap tersedia di bawah tajuk. Martinez et al. (2021) memodelkan medan sebuah perkebunan kelapa sawit seluas 5.220 ha di Llanos, Kolombia, dari DEM SRTM beresolusi 30 m. Lereng di perkebunan itu hanya 0–3%, tanahnya tergolong satu kelas, dan pengelolaannya seragam. Meskipun demikian, luas tangkapan termodifikasi (*Modified Catchment Area*, MCA), yaitu ukuran kecenderungan suatu sel untuk kehilangan atau menerima air, berkorelasi paling kuat dengan hasil panen di antara atribut medan yang diuji. Arah korelasinya berbeda antarzona pengelolaan, yaitu positif di satu zona dan negatif di tiga zona lain. Artinya, hasil panen dapat dibatasi oleh kekurangan maupun kelebihan air, dan atribut medan dapat menangkap keduanya. Di bawah tajuk, data sensor proksimal yang rapat, seperti ECa, juga dapat menjadi kovariat atau variabel bantu (Modul 7).

## Algoritma Digital Soil Mapping

Fungsi $f$ dalam persamaan SCORPAN dapat diduga dengan berbagai algoritme. Secara garis besar, algoritme DSM dapat dikelompokkan sebagai berikut:

1. **Model regresi linear**, seperti regresi linear berganda dan lasso, yang menyatakan sifat tanah sebagai kombinasi linear kovariat.

2. **Model geostatistik**, seperti *ordinary kriging*, yang memprediksi dari nilai pengamatan di sekitarnya, serta *kriging* dengan *external drift* dan *regression kriging*, yang memadukan tren dari kovariat dengan *kriging* residualnya.

3. **Pembelajaran mesin berbasis pohon**, seperti *random forest*, *cubist*, dan *boosted regression tree*, yang menggabungkan banyak pohon keputusan sehingga mampu menangkap hubungan tidak linear dan interaksi antarkovariat.

4. **Pembelajaran mesin lainnya**, seperti *support vector machine*, jaringan saraf tiruan, dan *k-nearest neighbours*.

5. **Pendekatan berbasis pengetahuan dan disagregasi**, seperti SoLIM yang memadukan pengetahuan pakar dengan kondisi lingkungan (Zhu et al., 2001) dan disagregasi spasial peta tanah warisan (Sulaeman & Husnain, 2021).

Kelompok-kelompok tersebut berbeda dalam kebutuhan data, kemampuan menangkap hubungan yang rumit, dan kemudahan tafsirannya. Perbandingannya dirangkum pada Tabel 8.2.

Tabel 8.2 Perbandingan Kelompok Algoritma Digital Soil Mapping

| **Kelompok** | **Contoh** | **Kekuatan** | **Keterbatasan** |
| :---------: | :-----------------: | :-----------------: | :-----------------: |
| Regresi linear | Regresi linear berganda, lasso | Sederhana, cepat, dan mudah ditafsirkan | Kurang mampu menangkap hubungan tidak linear; lasso cenderung kurang pas (*underfitting*) |
| Geostatistik | *Ordinary kriging*, *external drift kriging*, *regression kriging* | Memanfaatkan autokorelasi spasial dan menghasilkan varians prediksi | Memerlukan sampel yang cukup rapat; *ordinary kriging* tidak memanfaatkan kovariat |
| Berbasis pohon | *Random forest*, *cubist*, *boosted regression tree* | Menangkap hubungan tidak linear dan interaksi; tahan terhadap kovariat yang saling berkorelasi | Cenderung *overfitting*; prediksi di luar rentang data latih tidak andal; sulit ditafsirkan |
| Pembelajaran mesin lain | *Support vector machine*, jaringan saraf tiruan, *k-nearest neighbours* | Luwes untuk pola yang rumit | Memerlukan pilihan parameter dan data latih yang tepat |
| Berbasis pengetahuan dan disagregasi | SoLIM, disagregasi spasial | Memanfaatkan pengetahuan pakar dan peta tanah warisan | Bergantung pada mutu pengetahuan dan peta yang tersedia |

Sumber: Rangkuman penulis berdasarkan Nussbaum et al. (2018), Wadoux, Minasny, dan McBratney (2020), Maxwell et al. (2018), Meyer dan Pebesma (2021), Zhu et al. (2001), dan Sulaeman dan Husnain (2021)

Tidak ada algoritme yang selalu unggul. Nussbaum et al. (2018) membandingkan enam pendekatan untuk 48 kombinasi sifat tanah dan kedalaman di tiga wilayah di Swiss. Perbedaan ketelitiannya umumnya kecil. *Random forest* paling sering menjadi yang terbaik di antara metode tunggal, yaitu pada 28 dari 48 kasus, tetapi cenderung *overfitting*, dan pada separuh kasus tersebut kalah oleh rata-rata tertimbang beberapa model. Pada skala global, Hengl et al. (2017) mengaitkan peningkatan ketelitian SoilGrids250m dengan tiga hal, yaitu penggunaan pembelajaran mesin sebagai pengganti regresi linear, kovariat yang lebih rinci, dan tambahan data profil tanah. Faktor kedua dan ketiga menunjukkan bahwa mutu kovariat dan data tanah sama pentingnya dengan pilihan algoritme. Dalam pustaka DSM, *random forest* adalah algoritme pembelajaran mesin yang paling populer untuk memetakan sifat tanah, dan sekitar 80% penelitian pemetaan kelas tanah memakai sedikitnya satu algoritme berbasis pohon (Wadoux, Minasny, & McBratney, 2020).

Pilihan algoritme untuk perkebunan kelapa sawit sebaiknya didasarkan pada kondisi data dan kebutuhan pengguna, bukan pada popularitas algoritme. Nussbaum et al. (2018) merumuskan beberapa syarat metode DSM. Metode tersebut sebaiknya mampu membangun model secara efisien meskipun jumlah kovariat melebihi jumlah pengamatan, tahan terhadap banyak kovariat yang saling berkorelasi dan berderau, menghasilkan prediksi yang teliti tanpa *overfitting*, memodelkan hubungan yang tidak linear, memperhitungkan autokorelasi spasial, memungkinkan pemeriksaan kewajaran pedologis, dan mengukur ketidakpastian prediksi. Tidak ada satu algoritme yang memenuhi semuanya dengan sama baiknya, sehingga pilihan bergantung pada syarat mana yang paling penting. Jika sampel tanah sedikit, risiko *overfitting* pada model yang sangat luwes meningkat, sehingga model yang lebih sederhana dan mudah diperiksa layak dipertimbangkan. Jika sampelnya rapat dan residualnya masih berautokorelasi spasial, *kriging* residual dapat menambah ketelitian. Jika rekomendasi pemupukan memerlukan rentang nilai, algoritme yang menghasilkan interval prediksi, seperti *quantile regression forest*, lebih sesuai. Pilihan akhir sebaiknya ditentukan dengan membandingkan beberapa algoritme pada skema validasi yang sama.

## Data Splitting

Model DSM harus dinilai dengan data yang tidak dipakai untuk membangunnya. Model yang dinilai dengan data latihnya sendiri hampir selalu tampak lebih baik daripada kenyataannya, terutama model yang luwes dan cenderung *overfitting* seperti *random forest* (Nussbaum et al., 2018). Karena itu, data tanah dibagi menjadi data untuk melatih model dan data untuk menilainya. Dalam pustaka DSM, sekitar 30% penelitian menilai model dengan validasi silang dan 30% lainnya dengan pembagian data tunggal, sedangkan hanya dua penelitian yang mengumpulkan sampel probabilitas tambahan khusus untuk validasi (Wadoux, Minasny, & McBratney, 2020). Skema pembagian data yang umum dipakai adalah sebagai berikut:

1. **Pembagian tunggal (*holdout*)**, yaitu data dibagi sekali menjadi data latih dan data uji, misalnya dua pertiga untuk pelatihan dan sepertiga untuk validasi seperti yang dianjurkan untuk kalibrasi spektroskopi (England & Viscarra Rossel, 2018).

2. **Validasi silang lipat-k (*k-fold cross-validation*)**, yaitu data dibagi menjadi k kelompok, lalu model dibangun k kali dengan satu kelompok sebagai data uji pada setiap putaran. SoilGrids, misalnya, memakai validasi silang 10 lipatan (Hengl et al., 2017; Poggio et al., 2021).

3. **Validasi silang tinggalkan-satu (*leave-one-out*)**, yaitu bentuk ekstrem validasi silang dengan hanya satu pengamatan sebagai data uji pada setiap putaran.

4. **Validasi silang spasial**, yaitu data dibagi menjadi blok-blok yang terpisah secara geografis, atau pengamatan di sekitar data uji dikeluarkan dari data latih (Roberts et al., 2017; Wadoux, Minasny, & McBratney, 2020).

5. **Validasi dengan sampel probabilitas independen**, yaitu sampel baru yang dipilih secara acak, misalnya acak berstrata, khusus untuk menilai peta (Brus et al., 2011).

Keempat skema pertama membagi sampel yang sudah ada, sedangkan skema kelima menambah data baru. Perbedaan skema-skema tersebut diilustrasikan pada Gambar 8.2.

![](assets/modul-8/M8-G02_skema-pembagian-data.png)

Gambar 8.2 Ilustrasi skema pembagian data pada sampel tanah yang mengelompok

Sumber: Ilustrasi konseptual dengan data sintetis; skema mengacu pada Brus et al. (2011), Roberts et al. (2017), dan Wadoux, Minasny, dan McBratney (2020)

Pilihan skema memengaruhi hasil penilaian. Wadoux, Minasny, dan McBratney (2020) mengingatkan bahwa pengamatan tanah yang berdekatan cenderung mirip, padahal pembelajaran mesin mengasumsikan pengamatan yang saling bebas. Jika sampel mengelompok, data uji dalam validasi silang acak hampir selalu memiliki tetangga dekat di dalam data latih. Statistik validasi yang diperoleh lebih mencerminkan kemampuan model mengulang data latihnya daripada kemampuannya memetakan wilayah yang tidak disampel, sehingga hasilnya terlalu optimistis. Ploton et al. (2020) menunjukkan akibatnya dengan jelas. Pada pemetaan biomassa hutan di Afrika Tengah dari data inventarisasi 11,8 juta pohon, validasi acak menunjukkan bahwa model *random forest* menjelaskan lebih dari separuh keragaman biomassa, sedangkan validasi spasial menunjukkan kemampuan prediksi yang hampir nol. Validasi silang spasial mengatasi masalah ini, tetapi dapat bergeser ke arah sebaliknya. Blok yang terlalu besar memaksa model mengekstrapolasi, sehingga hasilnya terlalu pesimistis (Roberts et al., 2017; Wadoux, Minasny, & McBratney, 2020).

Jalan keluar yang paling kokoh adalah sampel validasi independen yang dipilih dengan desain probabilitas. Brus et al. (2011) menganjurkan pengumpulan data tambahan semacam ini karena ukuran mutu peta beserta galat bakunya dapat diduga tanpa asumsi apa pun tentang autokorelasi spasial galat prediksi. Di antara lima desain sampling acak yang mereka evaluasi, sampling acak berstrata umumnya merupakan pilihan yang baik karena mudah diterapkan dan memberikan dugaan yang relatif teliti.

Di perkebunan, sampel tanah dapat mengelompok, misalnya menurut blok atau di sepanjang jalan kebun, atau berasal dari beberapa survei dengan desain yang berbeda. Struktur ini perlu diperhitungkan saat membagi data. Roberts et al. (2017) menyarankan agar data dibagi menurut struktur yang menimbulkan ketergantungan, seperti ruang, waktu, atau kelompok hierarkis. Dalam konteks kebun, pengamatan dari blok yang sama dapat diperlakukan sebagai satu kelompok, sehingga seluruh pengamatan satu blok selalu berada bersama di data latih atau di data uji. Agar data latih mewakili keragaman kovariat, titik sampel dapat dipilih dengan algoritme Kennard–Stone (England & Viscarra Rossel, 2018) atau dengan rancangan *conditioned Latin hypercube* (cLHS), yang bertujuan mencakup ruang yang dibentuk oleh kovariat (Wadoux, Minasny, & McBratney, 2020). Rancangan semacam ini paling baik diterapkan sejak perencanaan pengambilan sampel, bukan setelah data terkumpul.

## Pembuatan Model dan Validasi

Pembuatan model DSM mengikuti urutan yang relatif baku (Gambar 8.3). Data tanah diperiksa mutunya, lalu disetarakan kedalamannya. SoilGrids 2.0, misalnya, memakai enam interval kedalaman baku menurut spesifikasi GlobalSoilMap, yaitu 0–5, 5–15, 15–30, 30–60, 60–100, dan 100–200 cm (Poggio et al., 2021). Nilai kovariat di setiap lokasi pengamatan kemudian diambil dengan penumpangan (*overlay*), sehingga terbentuk tabel pemodelan yang memuat nilai sifat tanah dan nilai semua kovariat di setiap titik. Tabel inilah yang dipakai untuk memilih kovariat, membagi data, menala parameter, dan membangun model. Model akhir lalu diterapkan pada setiap piksel untuk menghasilkan peta prediksi beserta peta ketidakpastiannya.

![](assets/modul-8/M8-G03_alur-pemodelan-dsm.png)

Gambar 8.3 Alur pembuatan model *digital soil mapping* dari data tanah dan kovariat hingga peta prediksi dan ketidakpastiannya

Sumber: Diagram konseptual disusun berdasarkan Poggio et al. (2021) dan Wadoux, Minasny, dan McBratney (2020)

Seleksi kovariat dan penalaan parameter sering dikerjakan bersamaan. Poggio et al. (2021) menyeleksi kovariat dalam dua langkah, yaitu membuang kovariat yang saling berkorelasi kuat, lalu menjalankan eliminasi fitur rekursif (*recursive feature elimination*). Parameter *random forest*, yaitu jumlah pohon (*ntree*) dan jumlah kovariat yang dicoba pada setiap percabangan (*mtry*), kemudian ditala dengan validasi silang 10 lipatan. Hasil penalaan tersebut memberi pelajaran praktis. Menambah jumlah pohon di atas 200 hanya menaikkan ketelitian kurang dari 0,1%, padahal memerlukan memori dan waktu hitung yang jauh lebih besar. Penalaan dan penilaian akhir sebaiknya tidak memakai data uji yang sama, karena hasilnya akan terlalu optimistis. Untuk data yang berautokorelasi spasial, penalaan dapat dikerjakan dengan validasi silang spasial bersarang, yaitu blok spasial dibagi sekali lagi khusus untuk mencari parameter terbaik (Wadoux, Minasny, & McBratney, 2020).

Ketelitian model dinilai dengan membandingkan nilai prediksi dan nilai pengamatan pada data validasi. Ukuran yang paling sering dipakai dirangkum pada Tabel 8.3. Setiap ukuran menjawab pertanyaan yang berbeda. Galat rata-rata (*mean error*, ME) menunjukkan bias, yaitu kecenderungan model menaksir terlalu tinggi atau terlalu rendah. MAE dan RMSE menunjukkan besarnya galat dalam satuan sifat tanah, dan RMSE lebih peka terhadap galat yang besar. Koefisien efisiensi model (*model efficiency coefficient*, MEC) menunjukkan bagian keragaman yang dijelaskan model terhadap garis 1:1.

Tabel 8.3 Ukuran Ketelitian untuk Validasi Peta Sifat Tanah

| **Ukuran** | **Rumus** | **Nilai ideal** | **Makna** |
| :---------: | :-----------------: | :-----------------: | :-----------------: |
| Galat rata-rata (ME) | $\frac{1}{n} \sum_{i=1}^{n} \left(\hat{y}_{i} - y_{i}\right)$ | 0 | Bias; nilai positif berarti model rata-rata menaksir terlalu tinggi |
| Galat absolut rata-rata (MAE) | $\frac{1}{n} \sum_{i=1}^{n} \lvert \hat{y}_{i} - y_{i} \rvert$ | 0 | Besar galat rata-rata dalam satuan sifat tanah |
| Akar galat kuadrat rata-rata (RMSE) | $\sqrt{\frac{1}{n} \sum_{i=1}^{n} \left(\hat{y}_{i} - y_{i}\right)^{2}}$ | 0 | Besar galat; lebih peka terhadap galat yang besar |
| Koefisien efisiensi model (MEC) | $1 - \frac{\sum_{i=1}^{n} \left(y_{i} - \hat{y}_{i}\right)^{2}}{\sum_{i=1}^{n} \left(y_{i} - \bar{y}\right)^{2}}$ | 1 | Bagian keragaman yang dijelaskan terhadap garis 1:1; negatif jika prediksi lebih buruk daripada nilai rerata |
| Koefisien determinasi (R²) | Kuadrat koefisien korelasi Pearson antara $y$ dan $\hat{y}$ | 1 | Kekuatan hubungan linear; tidak peka terhadap bias |
| PICP | Proporsi pengamatan yang berada di dalam interval prediksi | Sama dengan tingkat interval, misalnya 0,90 | Ketepatan dugaan ketidakpastian |

Sumber: Rangkuman penulis berdasarkan Nussbaum et al. (2018), Poggio et al. (2021), dan Wadoux, Minasny, dan McBratney (2020); $y_{i}$ = nilai pengamatan, $\hat{y}_{i}$ = nilai prediksi, $\bar{y}$ = rerata pengamatan, $n$ = jumlah data validasi

Perbedaan antara R² dan MEC perlu diperhatikan saat membaca laporan penelitian. Sebagian penelitian melaporkan R² yang identik dengan MEC, sedangkan yang lain melaporkan kuadrat koefisien korelasi Pearson. Kedua nilai itu berbeda, kecuali untuk model linear yang diduga dengan metode kuadrat terkecil biasa (Nussbaum et al., 2018). Sebagai ilustrasi, model yang prediksinya selalu 20% lebih tinggi daripada nilai sebenarnya dapat memiliki R² korelasi yang tinggi, tetapi MEC-nya rendah karena bias tersebut. Untuk peta kelas tanah, ukuran yang sesuai adalah kemurnian keseluruhan (*overall purity*), kemurnian setiap satuan peta (*user's accuracy*), dan keterwakilan setiap kelas tanah (*producer's accuracy*) (Brus et al., 2011).

Statistik validasi sebaiknya dilengkapi dengan pemeriksaan kewajaran model. *Random forest* menyediakan ukuran tingkat kepentingan variabel dari data *out-of-bag*, yaitu data yang tidak terpilih saat setiap pohon dibangun (Breiman, 2001). Penilaian tingkat kepentingan ini dapat bias, sehingga Poggio et al. (2021) menyeleksi kovariat terlebih dahulu, antara lain untuk menghindari bias tersebut. Tafsiran model juga berguna untuk memeriksa apakah model memprediksi karena alasan yang benar. Tafsiran model untuk memetakan nitrogen tanah lapisan atas, misalnya, dapat mengungkap bahwa model tersebut sebenarnya memprediksi kadar lempung sebagai perantaranya. Peta hasil prediksi juga perlu diperiksa secara visual, karena dua peta dengan statistik validasi yang mirip dapat memiliki pola spasial yang berbeda (Wadoux, Minasny, & McBratney, 2020).

## Residual dan Uncertainty

Residual adalah selisih antara nilai pengamatan dan nilai prediksi, yaitu bagian $e$ dalam persamaan SCORPAN. Residual memuat informasi yang sering terabaikan. Jika semua kovariat yang relevan telah dimasukkan, residual seharusnya tidak lagi berautokorelasi spasial. Residual yang masih berautokorelasi menandakan bahwa ada prediktor penting yang belum masuk ke dalam model (Wadoux, Minasny, & McBratney, 2020). Memetakan residual karena itu berguna untuk menemukan proses yang terlewat. Residual yang makin besar dengan makin jauhnya jarak dari sungai, misalnya, mengisyaratkan perlunya kovariat yang mewakili pengaruh sungai.

Autokorelasi residual juga dapat dimanfaatkan secara langsung. Residual di titik-titik pengamatan diinterpolasi dengan *kriging*, lalu hasilnya ditambahkan pada prediksi model tren. Prinsip ini mendasari *regression kriging* dan *kriging* dengan *external drift*, seperti yang dipakai Nussbaum et al. (2018), dan dapat pula diterapkan pada residual model pembelajaran mesin (Wadoux, Minasny, & McBratney, 2020). Manfaatnya bergantung pada kerapatan sampel. Pada SoilGrids250m, residual hampir tidak menunjukkan struktur spasial pada jarak di bawah 300 km, sehingga *kriging* residual tidak diperlukan untuk peta global. Namun, di tempat yang titik pengamatannya rapat, *kriging* residual masih dapat bermanfaat (Hengl et al., 2017). Kondisi kedua ini lebih dekat dengan perkebunan yang memiliki data tanah rapat, misalnya dari pengukuran sensor proksimal. Gambar 8.4 mengilustrasikan prinsip tersebut pada sebuah transek sintetis.

![](assets/modul-8/M8-G04_residual-dan-regression-kriging.png)

Gambar 8.4 Ilustrasi pemanfaatan residual dalam *regression kriging* pada transek sintetis

Sumber: Ilustrasi konseptual dengan data sintetis; prinsip mengacu pada Nussbaum et al. (2018) dan Hengl et al. (2017)

Setiap peta prediksi mengandung ketidakpastian. Menurut tinjauan Wadoux, Minasny, dan McBratney (2020), analisis ketidakpastian menentukan apakah peta cukup andal untuk dipakai dalam sistem produksi pertanian atau pengambilan keputusan. Mereka juga merujuk pustaka pembelajaran mesin yang membedakan dua sumber ketidakpastian. Ketidakpastian aleatorik berasal dari derau dan galat pengukuran data, sehingga sulit diduga dan lebih sulit lagi dikurangi. Ketidakpastian epistemik berasal dari keterbatasan model dan parameternya, dan dapat dikurangi, misalnya dengan menambah sampel di daerah yang jarang diamati. Galat analisis laboratorium dan galat estimasi sensor proksimal (Modul 7) termasuk sumber yang pertama, sedangkan sampel yang tidak mewakili seluruh keragaman kovariat termasuk sumber yang kedua.

Cara mengukur ketidakpastian bergantung pada algoritmenya. Model geostatistik menghasilkan varians *kriging*. Untuk pembelajaran mesin, interval dapat diperoleh dengan *bootstrap*, yaitu melatih banyak model pada sampel ulang data, atau dengan *quantile regression forest* (QRF) (Wadoux, Minasny, & McBratney, 2020). QRF adalah perluasan *random forest* yang tidak hanya menaksir rerata bersyarat, tetapi seluruh sebaran bersyarat sifat tanah, sehingga kuantil apa pun dapat diduga (Meinshausen, 2006). SoilGrids 2.0 memakai QRF untuk menghasilkan median serta kuantil 0,05 dan 0,95 di setiap piksel, yaitu batas bawah dan atas interval prediksi 90% (Poggio et al., 2021). Lebar interval tersebut dapat dipetakan sebagai peta ketidakpastian:

$$\text{PI90} = q_{\text{0,95}} - q_{\text{0,05}}$$

dengan $q_{\text{0,95}}$ dan $q_{\text{0,05}}$ adalah kuantil 0,95 dan 0,05 sebaran prediksi. Poggio et al. (2021) juga memetakan rasio lebar interval tersebut terhadap median, sehingga ketidakpastian dapat dibandingkan antardaerah yang nilai prediksinya berbeda.

Interval prediksi juga perlu divalidasi. Ukurannya adalah peluang cakupan interval prediksi (*prediction interval coverage probability*, PICP), yaitu proporsi data validasi yang berada di dalam interval prediksi (Poggio et al., 2021). Untuk interval 90%, PICP idealnya mendekati 0,90. PICP yang jauh lebih kecil berarti intervalnya terlalu sempit, sehingga ketidakpastian diremehkan. Sebaliknya, PICP yang jauh lebih besar berarti intervalnya terlalu lebar. Gambar 8.5(a) mengilustrasikan perhitungan PICP dengan data sintetis.

<!-- Catatan editor: Poggio et al. (2021, bagian 2.5.2) menulis bahwa PICP yang jauh lebih besar dari 0,9 menandakan ketidakpastian diremehkan, dan PICP yang lebih kecil menandakan ketidakpastian dilebih-lebihkan. Tafsiran tersebut terbalik terhadap definisi PICP pada kalimat sebelumnya di naskah yang sama, sehingga modul memakai tafsiran yang sesuai definisinya. -->

Interval prediksi hanya bermakna di wilayah yang menyerupai data latih. Meyer dan Pebesma (2021) menunjukkan bahwa interval prediksi *random forest* tidak melebar ketika model memprediksi di luar rentang data latih, padahal prediksinya justru makin tidak andal, dan QRF pun tidak mengatasi masalah ini. Untuk itu mereka mengusulkan indeks ketidakmiripan (*dissimilarity index*, DI), yaitu jarak terdekat suatu lokasi ke data latih dalam ruang kovariat yang dibobot dengan tingkat kepentingan kovariat. Wilayah keberlakuan model (*area of applicability*, AOA) adalah wilayah yang nilai DI-nya tidak melampaui ambang yang diturunkan dari DI data latih melalui validasi silang. Di dalam AOA, ketelitian hasil validasi silang dapat dianggap berlaku. Di luar AOA, prediksi sebaiknya ditandai atau tidak dipakai, seperti pada Gambar 8.5(b).

![](assets/modul-8/M8-G05_interval-prediksi-dan-aoa.png)

Gambar 8.5 Ilustrasi validasi interval prediksi dengan PICP (a) dan wilayah keberlakuan model (b)

Sumber: Ilustrasi konseptual dengan data sintetis; PICP mengacu pada Poggio et al. (2021), sedangkan DI dan AOA mengacu pada Meyer dan Pebesma (2021)

Bagi perkebunan, peta ketidakpastian dan AOA memiliki kegunaan yang sangat praktis. Keduanya menunjukkan di mana peta dapat dipercaya untuk rekomendasi pemupukan dan di mana diperlukan sampel tambahan. Daerah dengan interval yang lebar atau yang berada di luar AOA, misalnya blok pada bentuk lahan yang tidak terwakili dalam data latih, menjadi sasaran utama pengambilan sampel berikutnya. Logika yang sama dipakai pada skala global. Peta ketidakpastian SoilGrids 2.0 menunjukkan perlunya lebih banyak pengamatan tanah, terutama di wilayah lintang tinggi (Poggio et al., 2021). Dengan cara ini, DSM tidak berhenti pada satu peta. Peta, ketidakpastian, sampel baru, dan model yang diperbarui membentuk siklus yang terus memperbaiki informasi tanah di kebun.
