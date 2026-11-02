# Multi-source Data Fusion

*Ceramah dan diskusi:*

## Data untuk Multi-Source Data Fusion

Setiap sumber data memiliki karakteristik dan informasi yang berbeda. Pemahaman terhadap karakteristik tersebut menjadi dasar dalam menentukan jenis data yang dapat diintegrasikan sesuai dengan tujuan analisis. Berikut beberapa jenis sumber data yang umum digunakan dalam *Multi-Source Data Fusion* (Tabel 2.1).

Tabel 2.1 Sumber Data untuk Multi-Source Data Fusion

| **Sumber Data** | **Karakteristik** | **Contoh** | **Produk Turunan** |
| :----------: | :--------------------: | :----------: | :----------: |
| *Optical remote sensing* | Menggunakan pantulan cahaya matahari (sensor pasif); menampilkan visual objek (seperti foto udara) | Sentinel-2, Landsat 8, SPOT, Worldview | NDVI, EVI, BSI |
| SAR *(Synthetic Aperture Radar)* | Menggunakan gelombang mikro (sensor aktif); sensitif terhadap kekasaran permukaan, bentuk fisik objek, dan kelembapan air | Sentinel-1, ALOS PALSAR, TerraSAR-X | Backscatter HH, VV, HV, VH, rasio polarisasi |
| LiDAR (*Light Detection and Ranging*) | Menggunakan pulsa laser (sensor aktif); kemampuan menembus celah vegetasi rapat untuk merekam tanah asli | Airborne LiDAR | CHM, DTM, DSM |
| DEM *(Digital Elevation Model)* | Hasil pengolahan data SAR, LiDAR, atau foto udara; menampilkan nilai elevasi permukaan bumi | DEMNAS, SRTM | Slope, TWI, flow accumulation |

Sumber: Rangkuman penulis

## Konsep Multi-source Data Fusion

*Data fusion* merupakan pendekatan multidisiplin yang menggabungkan informasi dari data *multi-source* untuk meningkatkan nilai informasi, kinerja interpretasi, serta kualitas representasi visual data. Teknik ini dapat dimanfaatkan dalam deteksi, pengenalan, identifikasi, dan klasifikasi objek, pemantauan objek, deteksi perubahan, serta pendukung pengambilan keputusan (Zhang, 2010). Integrasi data penginderaan jauh dari berbagai sumber dengan teknologi deep learning semakin berkembang dalam mendukung pertanian presisi (Ma et al., 2026).

Fusi data penginderaan jauh merupakan teknik yang banyak digunakan untuk mengintegrasikan informasi dari berbagai sensor yang memiliki karakteristik resolusi spasial dan spektral berbeda. Proses integrasi ini bertujuan menghasilkan dataset yang lebih informatif dan detail melalui pemanfaatan informasi yang saling melengkapi dari setiap sumber data. Secara umum, fusi data penginderaan jauh dibedakan menjadi tiga tingkatan berdasarkan tahap integrasi informasi yang dilakukan, yaitu fusi tingkat piksel atau data (*the pixel/data level*), fusi tingkat fitur (*the feature level*), dan fusi tingkat keputusan (*the decision level*) (Pohl & van Genderen, 1998), yang diilustrasikan pada Gambar 2.1.

![](assets/modul-2/M2-G01_tingkat-fusi-data.png)

Gambar 2.1 Ilustrasi Tingkat Fusi

Sumber: Digambar ulang dengan modifikasi berdasarkan konsep Pohl dan van Genderen (1998)

Setiap tingkat fusi memiliki tujuan dan pendekatan yang berbeda, bergantung pada jenis informasi yang digabungkan. Perbedaan tersebut dapat dilihat melalui karakteristik dan contoh penerapannya dalam pengolahan data penginderaan jauh berikut.

1. **Fusi tingkat piksel atau data (*the pixel/data level*)**

    Fusi tingkat piksel pada citra optik bertujuan untuk meningkatkan resolusi spasial dan detail tekstural (pan-sharpening). Pada citra multitemporal bertujuan untuk mengidentifikasi perubahan antar-waktu. Misalnya, menggabungkan citra pankromatik resolusi tinggi dengan citra multispektral resolusi lebih rendah untuk menghasilkan citra berwarna dengan resolusi spasial lebih tinggi.

2. **Fusi tingkat fitur (*the feature level*)**

    Fusi tingkat fitur bertujuan untuk menggabungkan fitur atau parameter yang diekstrak dari beberapa sumber data. Misalnya, menggabungkan NDVI dari Sentinel-2 dengan backscatter HH dan HV dari ALOS PALSAR untuk klasifikasi tutupan lahan.

3. **Fusi tingkat keputusan (*the decision level*)**

    Fusi tingkat keputusan menggabungkan hasil klasifikasi atau prediksi dari beberapa algoritma untuk menghasilkan keputusan akhir. Misalnya, menggabungkan hasil klasifikasi tutupan lahan dari Sentinel-2 dan ALOS PALSAR menggunakan *majority voting*.
