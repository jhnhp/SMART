# Ringkasan untuk Tim Pemandu

**Pelatihan RS & DSM · PS2DL UGM · Selasa–Kamis, 3–5 November 2026**
Untuk: Johan, Nurarfiyah, Ferry, dan Pak Pandu.
Rincian lengkap ada di dokumen `01`–`06` dalam folder ini.

## Gambaran singkat

- Setiap hari efektif 08.00–16.00. Sekitar **60% waktu berupa praktik terbimbing**, ditambah 1 jam demo PSS.
- Isi praktik mengikuti rundown. Alatnya **QGIS 3.44 LTR** dan **Google Colab**.
- Wilayah latihan adalah **Sub-DAS Bompon**, Magelang (±295 ha). Wilayah ini bukan kebun sawit, jadi setiap blok menyertakan analogi ke kebun.
- Semua praktik memakai wilayah yang sama dan saling tersambung:
  ```
  Data Fusion ─► Delineasi SMU ─┐
              └► Bare Soil ─────┴─► Kovariat SCORPAN ─► Model DSM ─► Presentasi
  Demo PSS hiperspektral ┄┄► contoh latihan ML (opsional)
  ```
- Materi Modul 4 (estimasi sifat tanah) dilebur ke praktik Delineasi SMU.
- Tidak ada kegiatan lapangan.

## Pembagian tugas

| Pemandu | Sesi yang dipandu | Yang disiapkan sebelum 1 Nov |
|---|---|---|
| **Johan** | H1: Data Fusion (10.15–14.00), Delineasi SMU bagian 1 (14.15–16.00) | Paket data Bompon (deret waktu Sentinel-2, Sentinel-1, DEMNAS, dan data opsional seperti geologi atau iklim); notebook uji; berkas cadangan TP1–TP3; instruksi peserta |
| **Nurarfiyah** | H2: Delineasi SMU bagian 2 (08.00–09.00), Bare Soil (14.15–16.00); mendampingi demo PSS | **Tabel laboratorium per titik, DTM LiDAR, dan peta material permukaan Bompon**; notebook komposit B4; berkas cadangan TP4–TP5 |
| **Ferry** | H3: ML untuk DSM, Kovariat SCORPAN, Model DSM (09.15–15.00), memandu presentasi (15.00–16.00) | TWI dan kelengkungan; notebook B5–B7; berkas cadangan TP6–TP9 |
| **Pak Pandu** | H2: ceramah PSS (10.15–11.45) dan demo pengukuran (13.00–14.00) | Alat hiperspektral, sampel demo, dan pustaka spektral (jika ada) |

**Serah terima Delineasi SMU:** Johan menutup hari ke-1 di **TP3**, yaitu poligon bentuklahan, kelas lereng, dan raster indeks tersimpan dalam satu GeoPackage. Nurarfiyah melanjutkan dari situ pada hari ke-2.

## Jadwal persiapan

| Tanggal | Kegiatan |
|---|---|
| **Kam, 29 Okt** | Mengirim pesan ke Nurarfiyah (data Bompon) dan ke Pak Pandu (alat PSS) |
| **Jum, 30 Okt** | Mengirim instruksi persiapan dan notebook uji ke peserta melalui panitia |
| 30 Okt–1 Nov | Menyiapkan data dan notebook per hari |
| **Min, 1 Nov** | **Uji coba alur penuh B1→B7** di laptop bersih; membuat berkas cadangan TP1–TP9 |
| **Sen, 2 Nov** | Paket data final diunggah ke Drive dan disalin ke *flashdisk*; uji ulang Colab; mengecek jaringan dan proyektor di lokasi; memeriksa tangkapan layar uji dari peserta |

## Yang masih harus diputuskan

| No. | Hal | Siapa | Tenggat |
|---:|---|---|---|
| 1 | **Tabel laboratorium per titik Bompon, beserta izin membagikannya.** Blok 6–7 bergantung sepenuhnya pada ini | Nurarfiyah | 30 Okt |
| 2 | Sifat tanah sasaran model (usulan: fraksi lempung 0–20 cm) | Ferry / Nurarfiyah | 30 Okt |
| 3 | Spesifikasi alat PSS dan pustaka spektral | Pak Pandu | 30 Okt |
| 4 | Skala peta sasaran untuk SMU | Tim / Prof. Junun | 30 Okt |
| 5 | DTM LiDAR dan peta material permukaan Bompon | Nurarfiyah | 30 Okt |
| 6 | Kapasitas internet di Kantor PS2DL | Panitia | 30 Okt |
| 7 | Presentasi individu atau kelompok; pihak yang menutup acara; apakah sertifikat mensyaratkan nilai tertentu | Tim / panitia | 2 Nov |

## Evaluasi

- **Pre-test** dikerjakan saat registrasi hari ke-1. **Post-test** dikerjakan pada H3 15.40–15.50, dengan 16 soal yang sama.
- **Rubrik presentasi** (6 kriteria, skala 1–4) diisi pemandu dan narasumber.
- **Formulir evaluasi** dibuat di Google Form.
- Semua instrumen ada di `04 Instrumen Evaluasi.md`.
