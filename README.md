# Modul Pelatihan SMART: Pemanfaatan Remote Sensing dan Digital Soil Mapping untuk Pertanian Presisi Kelapa Sawit

Repositori ini memuat materi kurikulum, modul ilmiah, rancangan pelatihan operasional, serta presentasi slide resmi Universitas Gadjah Mada (UGM) untuk program pelatihan kerja sama antara **Pusat Studi Pengelolaan Sumber Daya Lahan (PS2DL) UGM** dan **PT SMART Tbk**.

---

## 1. Ringkasan Dokumen Master & Presentasi

* **Dokumen Master Modul:** [`Output/Modul Pelatihan SMART Pemanfaatan RS dan DSM.docx`](Output/Modul%20Pelatihan%20SMART%20Pemanfaatan%20RS%20dan%20DSM.docx) (Gabungan lengkap Modul 1 s.d. 8, dilengkapi rumus matematis, tabel standar, dan master daftar pustaka).
* **Rancangan Pelatihan & Praktik:** [`Output/Rancangan Pelatihan/`](Output/Rancangan%20Pelatihan/) (Struktur rundown sesi teori dan panduan pelaksanaan praktik).
* **Paket Presentasi Resmi (PPTX):** [`Output/Presentasi/`](Output/Presentasi/) (5 berkas PPTX 16:9 Widescreen menggunakan template resmi UGM 2026, mencakup 95 slide dan 100% catatan pemateri / *speaker notes*).

---

## 2. Struktur Modul & Pemateri Pelatihan

| Bagian | Modul Terkait | Topik Utama | Pemateri / Narasumber | File Presentasi (.pptx) |
|:---:|:---:|:---|:---|:---|
| **1–3** | Modul 1, 2, 3 | Dasar-dasar Remote Sensing, Multi-source Data Fusion, dan Delineasi Soil Mapping Units (SMU) | **Prof. Dr. rer. nat. Junun Sartohadi, M.Sc.** | [`PPT_01_Prof_Junun_Bagian_1-3.pptx`](Output/Presentasi/PPT_01_Prof_Junun_Bagian_1-3.pptx) |
| **4 & 6** | Modul 4 & 6 | Remote Sensing untuk Estimasi Soil Properties & Interpretasi Pedologis Lanskap Kebun | **Dr. rer. nat. Muhammad Anggri Setiawan, S.Si., M.Si.** | [`PPT_02_Dr_Anggri_Bagian_4_dan_6.pptx`](Output/Presentasi/PPT_02_Dr_Anggri_Bagian_4_dan_6.pptx) |
| **5** | Modul 5 | Bare Soil Detection & Information Extraction di Bawah Kanopi Sawit | **Dr. Retnadi Heru Jatmiko, M.Sc.** | [`PPT_03_Dr_Retnadi_Bagian_5.pptx`](Output/Presentasi/PPT_03_Dr_Retnadi_Bagian_5.pptx) |
| **7** | Modul 7 | Proximal Soil Sensing (PSS) & Karakterisasi Sifat Tanah Cepat | **Pandu Yudha Adi Putra Wirabuana, S.Hut., M.Sc., Ph.D.** | [`PPT_04_Pak_Pandu_Bagian_7.pptx`](Output/Presentasi/PPT_04_Pak_Pandu_Bagian_7.pptx) |
| **8** | Modul 8 | Pemodelan Digital Soil Mapping (DSM), Machine Learning, & Evaluasi Ketidakpastian | **Dr. Eng. Guruh Samodra, S.Si., M.Sc.** | [`PPT_05_Dr_Guruh_Bagian_8.pptx`](Output/Presentasi/PPT_05_Dr_Guruh_Bagian_8.pptx) |

---

## 3. Struktur Direktori Proyek

```
.
├── CLAUDE.md             # Panduan editorial dan aturan penulisan modul
├── README.md             # Dokumentasi umum repositori
├── Source/               # Dokumen acuan, template resmi, dan data spasial
│   ├── (NEW) Template Presentasi UGM Opt-1 (Wide Size)_2026.pptx
│   ├── Data Bompon/      # Data spasial & atribut untuk sesi latihan praktik
│   ├── Referensi/        # Literatur pendukung dan silabus
│   └── rundown_pelatihan_remote_sensing_dsm.json
└── Output/               # Seluruh berkas keluaran modul pelatihan
    ├── Modul 1.md ~ Modul 8.md
    ├── Modul Pelatihan SMART Pemanfaatan RS dan DSM.docx
    ├── Daftar Pustaka.md
    ├── Presentasi/       # 5 Berkas PPTX resmi UGM & 5 naskah Markdown
    ├── Rancangan Pelatihan/ # Rancangan sesi ceramah dan modul praktik
    ├── assets/           # Visual resolusi tinggi (modul-1 s.d. modul-8)
    └── scripts/          # Skrip Python pembuat visual, docx, dan pptx
```

---

## 4. Skrip Otomasi dan Reproduksibilitas

* **Pembuat PPTX Presentasi Resmi UGM:**
  ```bash
  python3 Output/scripts/buat_pptx_ugm.py
  ```
* **Pembuat Dokumen Master Word (`.docx`):**
  ```bash
  python3 Output/scripts/buat_docx.py
  ```
* **Pemeriksa Konsistensi & Validasi Modul:**
  ```bash
  python3 Output/scripts/periksa_modul.py
  ```
