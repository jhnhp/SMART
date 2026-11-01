# Matriks Rundown Pelatihan

**Pelatihan Pemanfaatan Remote Sensing dan Digital Soil Mapping untuk Pertanian Presisi pada Perkebunan Kelapa Sawit**
Pusat Studi Pengelolaan Sumber Daya Lahan (PS2DL), Universitas Gadjah Mada
Selasa–Kamis, 3–5 November 2026 · Kantor PS2DL UGM

Status: rancangan, untuk ditinjau.
Sumber jadwal: `Source/rundown_pelatihan_remote_sensing_dsm.json`. Isi praktik mengikuti rundown. Silabus hanya menjadi acuan modul teori.
Perangkat lunak praktik: QGIS dan Python (Google Colab).

Matriks ini memetakan setiap slot rundown ke jenis sesi, modul teori yang mendukungnya, dan penanggung jawabnya. Dokumen rancangan berikutnya (rancangan sesi praktik, spesifikasi teknis, dan instrumen evaluasi) menggunakan matriks ini sebagai dasar.

## 1. Jadwal per hari

Keterangan jenis sesi: **C** = ceramah dan diskusi, **P** = praktik terbimbing, **D** = demonstrasi.

### Hari ke-1 — Selasa, 3 November 2026 (pemandu praktik: Johan)

| Waktu | Menit | Sesi | Jenis | Modul teori pendukung | Narasumber/Pemandu |
|---|---:|---|:-:|---|---|
| 07.30–08.00 | 30 | Registrasi peserta | – | – | Panitia |
| 08.00–09.00 | 60 | Pengantar Remote Sensing dan Pemetaan Tanah pada Perkebunan | C | Modul 1 | Prof. Dr. rer.nat. Junun Sartohadi, M.Sc. |
| 09.00–09.15 | 15 | Coffee break | – | – | – |
| 09.15–10.15 | 60 | Interpretasi Pedologis dari Data Remote Sensing | C | Modul 6 | Dr. rer.nat Muhammad Anggri Setiawan, S.Si., M.Si. |
| 10.15–11.45 | 90 | Multi-source Data Fusion (1): karakteristik dan integrasi data optik, SAR, LiDAR, DEM, serta data lingkungan | P | Modul 2 | Johan |
| 11.45–13.00 | 75 | Istirahat | – | – | – |
| 13.00–14.00 | 60 | Multi-source Data Fusion (2) | P | Modul 2 | Johan |
| 14.00–14.15 | 15 | Coffee break | – | – | – |
| 14.15–16.00 | 105 | Remote Sensing untuk Delineasi SMU (1) | P | Modul 3, Modul 4, Modul 6 | Johan |

### Hari ke-2 — Rabu, 4 November 2026 (pemandu praktik: Nurarfiyah)

| Waktu | Menit | Sesi | Jenis | Modul teori pendukung | Narasumber/Pemandu |
|---|---:|---|:-:|---|---|
| 07.30–08.00 | 30 | Registrasi peserta | – | – | Panitia |
| 08.00–09.00 | 60 | Remote Sensing untuk Delineasi SMU (2) | P | Modul 3, Modul 4, Modul 6 | Nurarfiyah |
| 09.00–09.15 | 15 | Coffee break | – | – | – |
| 09.15–10.15 | 60 | Bare Soil Detection & Information Extraction | C | Modul 5 | Dr. Retnadi Heru Jatmiko, M.Sc. |
| 10.15–11.45 | 90 | Proximal Soil Sensing | C | Modul 7 | Pandu Yudha Adi Putra Wirabuana, S.Hut., M.Sc., Ph.D. |
| 11.45–13.00 | 75 | Istirahat | – | – | – |
| 13.00–14.00 | 60 | Proximal Soil Sensing: demonstrasi pengukuran | D | Modul 7 | Pak Pandu (alat buatan sendiri) |
| 14.00–14.15 | 15 | Coffee break | – | – | – |
| 14.15–16.00 | 105 | Bare Soil Detection & Information Extraction | P | Modul 5 | Nurarfiyah |

### Hari ke-3 — Kamis, 5 November 2026 (pemandu praktik: Ferry)

| Waktu | Menit | Sesi | Jenis | Modul teori pendukung | Narasumber/Pemandu |
|---|---:|---|:-:|---|---|
| 07.30–08.00 | 30 | Registrasi peserta | – | – | Panitia |
| 08.00–09.00 | 60 | Digital Soil Mapping | C | Modul 8 | Dr. Eng. Guruh Samodra, S.Si., M.Sc. |
| 09.00–09.15 | 15 | Coffee break | – | – | – |
| 09.15–10.15 | 60 | Machine Learning untuk Digital Soil Mapping | P | Modul 8 | Ferry |
| 10.15–11.45 | 90 | Penyiapan dan pemilihan kovariat dari data remote sensing berdasarkan konsep SCORPAN | P | Modul 8, Modul 2, Modul 4 | Ferry |
| 11.45–13.00 | 75 | Istirahat | – | – | – |
| 13.00–14.00 | 60 | Pembangunan model DSM (1) | P | Modul 8 | Ferry |
| 14.00–14.15 | 15 | Coffee break | – | – | – |
| 14.15–15.00 | 45 | Pembangunan model DSM (2) | P | Modul 8 | Ferry |
| 15.00–16.00 | 60 | Presentasi hasil, evaluasi, diskusi, kesan pesan, dan penutupan | P | – | Ferry bersama tim pemandu |

## 2. Rekap durasi efektif

Durasi efektif tidak mencakup registrasi, coffee break, dan istirahat.

| Hari | Ceramah | Praktik terbimbing | Demonstrasi | Presentasi & penutupan | Total |
|---|---:|---:|---:|---:|---:|
| 1 | 120 | 255 | – | – | 375 |
| 2 | 150 | 165 | 60 | – | 375 |
| 3 | 60 | 255 | – | 60 | 375 |
| **Jumlah** | **330 (29%)** | **675 (60%)** | **60 (5%)** | **60 (5%)** | **1.125 (18,75 jam)** |

## 3. Blok praktik

Beberapa slot rundown merupakan lanjutan dari blok yang sama, sehingga slot-slot itu digabung menjadi satu blok. Setiap blok nanti mendapat satu kartu di `02 Rancangan Sesi Praktik.md`.

| No. | Blok praktik | Slot rundown | Menit | Alat | Pemandu |
|---:|---|---|---:|---|---|
| 1 | Multi-source Data Fusion | H1 10.15–11.45, 13.00–14.00 | 150 | QGIS/Colab* | Johan |
| 2 | Delineasi SMU (termasuk estimasi sifat tanah dari Modul 4) | H1 14.15–16.00, H2 08.00–09.00 | 165 | QGIS* | Johan → Nurarfiyah |
| 3 | Demonstrasi Proximal Soil Sensing | H2 13.00–14.00 | 60 | Sensor hiperspektral buatan Pak Pandu | Pak Pandu |
| 4 | Bare Soil Detection & Information Extraction | H2 14.15–16.00 | 105 | QGIS/Colab* | Nurarfiyah |
| 5 | Machine Learning untuk DSM | H3 09.15–10.15 | 60 | Colab* | Ferry |
| 6 | Penyiapan dan pemilihan kovariat SCORPAN | H3 10.15–11.45 | 90 | QGIS/Colab* | Ferry |
| 7 | Pembangunan model DSM | H3 13.00–14.00, 14.15–15.00 | 105 | Colab* | Ferry |
| 8 | Presentasi hasil dan penutupan | H3 15.00–16.00 | 60 | – | Ferry bersama tim |

\* Usulan awal. Pembagian alat QGIS dan Colab per blok ditetapkan di dokumen rancangan sesi.

## 4. Pemetaan modul teori ke sesi

| Modul | Judul | Disampaikan sebagai ceramah | Dipakai dalam praktik |
|---|---|---|---|
| 1 | Pengantar Remote Sensing dan Digital Soil Mapping | H1 08.00 (Prof. Junun) | – (konteks umum) |
| 2 | Multi-source Data Fusion | **tidak ada slot ceramah** | Blok 1, Blok 6 |
| 3 | Remote Sensing untuk Delineasi SMU | **tidak ada slot ceramah** | Blok 2 |
| 4 | Remote Sensing untuk Estimasi Soil Properties | **tidak ada slot ceramah** | Blok 2 (dilebur), Blok 6 |
| 5 | Bare Soil Detection & Information Extraction | H2 09.15 (Dr. Retnadi) | Blok 4 |
| 6 | Interpretasi Pedologis dari Data Remote Sensing | H1 09.15 (Dr. Anggri) | Blok 2 |
| 7 | Proximal Soil Sensing | H2 10.15 (Dr. Pandu) | Blok 3 |
| 8 | Pemodelan Digital Soil Mapping | H3 08.00 (Dr. Guruh) | Blok 5, 6, 7 |

## 5. Catatan untuk ditinjau

1. **Modul 2, 3, dan 4 tidak punya slot ceramah.** Ketiganya hanya muncul sebagai praktik. Usulan: setiap blok tersebut dibuka dengan pengantar konsep singkat oleh pemandu (±10–15 menit) yang merujuk ke modul. Peserta tetap menerima modul lengkap sebagai bacaan.
2. **Serah terima Delineasi SMU.** Blok 2 dimulai oleh Johan pada hari ke-1 dan dilanjutkan Nurarfiyah pada hari ke-2 pagi. Kartu sesi perlu menetapkan titik henti hari ke-1 dan keluaran yang dibawa ke hari ke-2.
3. **Modul 8 hanya mendapat satu jam ceramah**, padahal modul ini memuat enam subbab (SCORPAN, algoritma, data splitting, pembuatan model dan validasi, residual dan uncertainty). Blok 5–7 perlu menyelipkan penjelasan konsep di dalam praktik.
4. **Demo PSS memakai sensor hiperspektral buatan Pak Pandu.** Alat ini merekam spektrum pantulan, dan sifat tanah diperoleh dari spektrum melalui pembelajaran mesin. Demo ini sejalan dengan subbab "Interpretasi Pantulan Spektral Proximal Soil Sensing" di Modul 7 dan menjadi jembatan ke praktik ML hari ke-3.
5. **Presentasi hari ke-3** mengandaikan peserta punya hasil yang bisa dipresentasikan. Hasil itu bergantung pada alur keluaran Blok 1→2→6→7 dan akan dirancang di dokumen berikutnya.
