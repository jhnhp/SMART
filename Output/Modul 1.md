# Pengantar Remote Sensing dan Digital Soil Mapping

*Ceramah dan diskusi:*

## Pengenalan Remote Sensing

Remote sensing atau penginderaan jauh merupakan ilmu, seni, dan teknologi untuk memperoleh informasi mengenai suatu objek, fenomena, atau kondisi di permukaan bumi dengan menggunakan alat tanpa melakukan kontak langsung dengan objek yang diamati (Lillesand & Kiefer, 1990). Informasi tersebut diperoleh menggunakan alat pengindera atau sensor yang ditempatkan pada suatu wahana, seperti balon udara, pesawat terbang, pesawat ulang-alik, maupun satelit (Sutanto, 1994). Sutanto (1994) menjelaskan bahwa penginderaan jauh merupakan suatu teknik untuk memperoleh dan menganalisis informasi mengenai permukaan bumi berdasarkan energi elektromagnetik yang dipantulkan atau dipancarkan oleh suatu objek.

Penginderaan jauh merupakan teknologi yang memanfaatkan radiasi elektromagnetik atau spektrum energi lainnya untuk memperoleh informasi mengenai objek di permukaan bumi. Proses penginderaan jauh melibatkan empat komponen utama, yaitu sumber energi, objek, atmosfer, dan sensor dengan rincian sebagai berikut:

1. **Sumber energi**, radiasi elektromagnetik dalam penginderaan jauh berasal dari sumber alami seperti matahari atau sumber energi buatan dari sensor, yang membedakan sistem pasif dan aktif.

2. **Objek**, objek penginderaan jauh meliputi berbagai kenampakan di permukaan bumi, seperti tanah, air, vegetasi, dan objek hasil aktivitas manusia.

3. **Interaksi atmosfer**, atmosfer menjadi media perambatan energi elektromagnetik yang dapat menyebabkan penyerapan dan hamburan sehingga memengaruhi energi yang diterima sensor.

4. **Sensor**, sensor merupakan perangkat yang merekam energi elektromagnetik dari objek di permukaan bumi dan mengubahnya menjadi data yang dapat diolah menjadi informasi.

Berdasarkan komponen utama tersebut remote sensing melibatkan energi elektromagnetik yang berinteraksi dengan objek di permukaan bumi akan mengalami proses pemantulan, penyerapan, atau transmisi, kemudian energi yang diterima oleh sensor direkam sebagai data. Data tersebut selanjutnya diolah dan diinterpretasikan untuk menghasilkan informasi mengenai karakteristik objek atau fenomena di permukaan bumi. Sistem remote sensing tersebut ditunjukkan pada Gambar 1.1.

![](assets/modul-1/M1-G01_alur-penginderaan-jauh.png)

Gambar 1.1 Diagram alur proses penginderaan jauh

Sumber: Diagram konseptual

Sumber energi dalam penginderaan jauh terdiri dari energi aktif dan energi pasif. Sensor yang memanfaatkan energi radiasi matahari disebut sensor pasif, sedangkan sensor yang memancarkan sendiri sinyal buatan dari wahana, seperti satelit, disebut sensor aktif. Contoh sensor pasif yang digunakan dalam penginderaan jauh antara lain Sentinel-2 MSI, Landsat OLI, dan MODIS, sementara itu, sensor aktif dalam penginderaan jauh antara lain RADAR (Sentinel-1 SAR), ALOS PALSAR, dan LiDAR.

Energi yang umum digunakan dalam sensor aktif maupun pasif berupa gelombang elektromagnetik, seperti gelombang radio, inframerah, dan cahaya tampak. Ketika energi elektromagnetik mengenai suatu objek di permukaan bumi, energi tersebut dapat mengalami tiga bentuk interaksi, yaitu dipantulkan, diserap, atau diteruskan (ditransmisikan) (Danoedoro, 2012). Dengan menerapkan hukum kekekalan energi, hubungan timbal balik antara tiga jenis interaksi tenaga tersebut dapat dinyatakan sebagai berikut:

$$E_I(\lambda) = E_R(\lambda) + E_A(\lambda) + E_T(\lambda)$$

dengan:

$E_I$ = tenaga yang mengenai benda

$E_R$ = tenaga yang dipantulkan

$E_A$ = tenaga yang diserap

$E_T$ = tenaga yang ditransmisikan

![](assets/modul-1/M1-G02_sensor-pasif-aktif.png)

Gambar 1.2 Energi yang dipantulkan dan dipancarkan oleh sensor penginderaan jauh

Sumber: Digambar ulang dengan modifikasi dari Syah (2010)

Susunan seluruh gelombang elektromagnetik berdasarkan panjang gelombangnya disebut spektrum elektromagnetik (Gambar 1.3). Gambar spektrum elektromagnetik di bawah ini disusun berdasarkan panjang gelombang mencakup kisaran energi yang sangat rendah, dengan panjang gelombang tinggi dan frekuensi rendah. Setiap objek memiliki struktur partikel yang berbeda, baik pada skala mikro maupun makro, sehingga menghasilkan pola respons elektromagnetik yang berbeda. Perbedaan respons tersebut menjadi dasar dalam membedakan objek melalui penginderaan jauh. Setiap objek memberikan respons yang berbeda terhadap gelombang elektromagnetik pada panjang gelombang tertentu.

![](assets/modul-1/M1-G03_spektrum-elektromagnetik.png)

Gambar 1.3 Spektrum gelombang elektromagnetik yang umum digunakan

Sumber: Digambar ulang dengan modifikasi dari Jensen (2004)

Pola pantulan spektral setiap objek pada Gambar 1.4 menunjukkan karakteristik yang berbeda pada berbagai panjang gelombang, yang dapat dijelaskan sebagai berikut:

1. **Vegetasi (garis hijau)** memiliki pantulan rendah pada wilayah cahaya tampak, terutama pada kanal merah, kemudian mengalami peningkatan tajam pada inframerah dekat (NIR) sekitar 0,7 µm. Pantulan kembali menurun pada 1,4 dan 1,9 µm karena penyerapan oleh kandungan air dalam vegetasi.

2. **Tanah kering (garis oranye)** menunjukkan pantulan yang relatif tinggi dan meningkat secara bertahap dari wilayah tampak menuju inframerah dekat dan inframerah tengah. Pantulannya lebih tinggi dibandingkan tanah basah karena kandungan air yang lebih rendah.

3. **Tanah basah (garis cokelat)** memiliki pantulan lebih rendah dibandingkan tanah kering. Kandungan air menyebabkan penyerapan energi elektromagnetik sehingga nilai reflektansinya menurun.

4. **Air jernih (garis biru)** memiliki pantulan sangat rendah, terutama pada wilayah inframerah dekat dan inframerah tengah karena energi elektromagnetik pada wilayah tersebut banyak diserap oleh air.

5. **Air keruh (garis ungu)** menunjukkan pantulan sedikit lebih tinggi dibandingkan air jernih pada beberapa panjang gelombang karena adanya material tersuspensi di dalam air.

![](assets/modul-1/M1-G04_pola-respons-spektral.png)

Gambar 1.4 Pola respons spektral beberapa objek

Sumber: Ilustrasi skematis, digambar ulang dengan modifikasi dari Jensen (2004); posisi kanal Sentinel-2 mengacu pada Drusch et al. (2012)

Kemampuan sensor penginderaan jauh dalam merekam dan membedakan informasi objek secara detail, terdiri atas resolusi spasial, spektral, radiometrik, dan temporal. Rincian jenis resolusi penginderaan jauh disajikan pada Tabel 1.1.

Tabel 1.1 Resolusi Citra Satelit

| **Resolusi** | **Keterangan** | **Ilustrasi** |
| :-------: | :-------------: | :------------------: |
| Spasial | Ukuran objek terkecil yang masih dapat dideteksi oleh sistem pencitraan | ![](assets/modul-1/M1-T01a_resolusi-spasial.png){width=6.5cm} |
| Spektral | Kemampuan sistem optik-elektronik untuk membedakan informasi objek berdasarkan pantulan atau pancaran spektralnya. | ![](assets/modul-1/M1-T01b_resolusi-spektral.png){width=6.5cm} |
| Radiometrik | Kemampuan sensor dalam mencatat respons spektral objek | ![](assets/modul-1/M1-T01c_resolusi-radiometrik.png){width=6.5cm} |
| Temporal | Kemampuan suatu sistem satelit untuk merekam kembali wilayah yang sama dalam selang waktu tertentu | ![](assets/modul-1/M1-T01d_resolusi-temporal.png){width=6.5cm} |

Sumber: Ilustrasi digambar ulang dengan modifikasi dari Jensen (2004)

## Pemetaan Tanah Konvensional dan Pemetaan Tanah Digital

Pemahaman mengenai pola sifat tanah sangat penting dalam pertanian untuk meningkatkan produktivitas dan mendukung pengelolaan lahan yang berkelanjutan (Hosseinpour-Zarnaq et al., 2025). Variasi dan distribusi tanah pada suatu lanskap terbentuk melalui interaksi berbagai faktor pembentuk tanah, yaitu iklim, organisme, bahan induk, topografi, dan waktu. Pola dan distribusi sifat tanah dapat dipahami secara spasial melalui peta tanah. Pemetaan tanah merupakan kegiatan untuk memperoleh informasi mengenai jenis, sifat, dan distribusi tanah pada suatu wilayah. Pemetaan tanah dapat dilakukan melalui pendekatan konvensional maupun digital, yang memiliki perbedaan pada metode pengumpulan data, analisis, dan penyajian informasi spasial.

Pemetaan tanah konvensional mengandalkan survei lapangan yang meliputi pengamatan profil tanah, pengambilan sampel, analisis laboratorium, interpretasi lanskap, dan delineasi satuan tanah. Pengamatan lapangan memberikan informasi langsung mengenai karakteristik tanah yang kemudian diinterpretasikan dalam kaitannya dengan kondisi lingkungan dan lanskap. Pemetaan tanah dengan pendekatan survei konvensional membutuhkan waktu dan biaya yang relatif besar serta memiliki keterbatasan dalam pemantauan tanah pada skala luas (Lu et al., 2023). *Digital Soil Mapping* (DSM) atau pemetaan tanah digital dikembangkan untuk mengatasi keterbatasan tersebut melalui pemanfaatan data lingkungan, teknologi geospasial, dan pemodelan untuk menghasilkan informasi tanah secara spasial.

Pendekatan geografis dalam pemetaan tanah berkembang melalui berbagai metode geostatistik, seperti *trend surfaces*, *kriging*, dan *co-kriging*. Selanjutnya, konsep faktor pembentuk tanah yang dikemukakan oleh Jenny dikembangkan menjadi fungsi prediksi spasial tanah melalui hubungan kuantitatif empiris antara sifat tanah dan faktor lingkungan. Pendekatan tersebut dikenal sebagai konsep SCORPAN yang mencakup tujuh faktor, yaitu *soil, climate, organisms, relief, parent material, age,* dan *spatial position* (McBratney et al., 2003).

![](assets/modul-1/M1-G05_konsep-scorpan.png)

Gambar 1.5 Diagram konsep SCORPAN

Sumber: Diagram konseptual disusun berdasarkan McBratney et al. (2003)

## Peran Remote Sensing dan Digital Soil Mapping dalam Pertanian Presisi

Pertanian presisi, yang sering disebut juga sebagai pengelolaan tanaman spesifik lokasi, merupakan penerapan teknologi dan prinsip untuk mengelola variabilitas spasial dan temporal yang berkaitan dengan berbagai aspek produksi pertanian. Pertanian presisi didefinisikan sebagai suatu sistem yang mengintegrasikan informasi dengan produksi tanaman untuk meningkatkan efisiensi, produktivitas, dan profitabilitas produksi pertanian dalam jangka panjang dan secara spesifik lokasi, serta meminimalkan dampak yang tidak diinginkan terhadap ekosistem (Elsharkawy et al., 2022; Mukhamedova et al., 2022).

Penggunaan remote sensing memiliki potensi penting dalam mendukung penerapan pertanian presisi (Briliyanti et al., 2025). Pemanfaatan penginderaan jauh yang terintegrasi dengan GPS, Sistem Informasi Geografis (SIG), serta berbagai teknologi pendukung lainnya berperan dalam memperoleh dan mengolah informasi spasial untuk mendukung pengelolaan lahan secara spesifik lokasi (Mooy & Watuwaya, 2023). Integrasi berbagai teknologi tersebut memungkinkan pengembangan beragam aplikasi, termasuk pemetaan tanah dan pemantauan pertumbuhan tanaman (Martos et al., 2021; Segarra et al., 2020). Pada perkebunan sawit informasi tersebut dapat dimanfaatkan untuk meningkatkan ketepatan dalam perencanaan dan mendukung efisiensi penggunaan sumber daya pertanian, termasuk air dan pupuk.

Salah satu informasi penting dalam pengelolaan lahan secara spesifik lokasi adalah informasi mengenai sifat dan variabilitas tanah. Dalam konteks tersebut, Digital Soil Mapping (DSM) dapat digunakan untuk mengestimasi dan memetakan berbagai sifat tanah secara spasial berdasarkan data tanah dan informasi lingkungan. Informasi yang dihasilkan dapat berupa sifat fisik maupun kimia tanah, seperti tekstur, kelembapan, pH, bahan organik, dan indikator kesuburan tanah. Informasi tersebut selanjutnya dapat menjadi dasar dalam pengelolaan lahan spesifik lokasi dan melengkapi berbagai aplikasi pertanian presisi lainnya, seperti deteksi tekanan biotik berupa serangan hama dan penyakit serta tekanan abiotik seperti kekeringan dan banjir hingga estimasi hasil pertanian (Pascucci et al., 2020; Weiss et al., 2020).

![](assets/modul-1/M1-G06_siklus-pertanian-presisi.png)

Gambar 1.6 Siklus informasi dalam pertanian presisi

Sumber: Diagram konseptual disusun berdasarkan Elsharkawy et al. (2022) dan Weiss et al. (2020)

Penerapan pertanian presisi pada perkebunan kelapa sawit didasarkan pada pemanfaatan informasi mengenai berbagai faktor yang memengaruhi produksi, seperti kondisi iklim, kondisi dan kesuburan tanah, umur tanaman, serta faktor lainnya. Penerapan pertanian presisi pada perkebunan kelapa sawit untuk mendukung estimasi produksi juga memanfaatkan informasi indeks tanaman yang diperoleh dari citra satelit. Selain informasi indeks tanaman, berbagai faktor eksternal yang memengaruhi produksi, seperti curah hujan, kesuburan tanah, dan serangan hama dan penyakit, serta faktor internal seperti jumlah tanaman, varietas, dan umur tanaman dapat diintegrasikan dengan berbagai teknologi komputerisasi untuk mendukung pengelolaan perkebunan secara spesifik lokasi (Ginting & Wiratmoko, 2021).
