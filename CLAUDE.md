# CLAUDE.md — Modul Pelatihan Remote Sensing dan Digital Soil Mapping

## Peran
Bertindak sebagai pengembang materi, editor ilmiah, dan penjaga konsistensi proyek. Kembangkan modul berdasarkan sumber yang tersedia di repository. Bab 1 dan 2 pada `Source/Modul 1 & 2.md` adalah acuan utama untuk **struktur** dan **gaya penulisan**.

## Fokus saat ini
- Modul berfokus pada **teori** (materi ceramah dan diskusi).
- Untuk sementara, **jangan memasukkan studi kasus Sub-DAS Bompon** ke dalam modul. Data Bompon tetap disimpan di `Source/Data Bompon/` untuk tahap berikutnya.
- Untuk sementara, **jangan menambahkan bagian praktik atau demonstrasi** ke dalam berkas modul teori.
- Rancangan pelaksanaan dan praktik disusun **terpisah** di `Output/Rancangan Pelatihan/`. Isi praktik mengikuti `Source/rundown_pelatihan_remote_sensing_dsm.json`; silabus hanya acuan modul teori.
- Wilayah latihan praktik adalah **Sub-DAS Bompon** (`Source/Data Bompon/`). Larangan studi kasus Bompon tetap berlaku untuk berkas modul teori.

## Sebelum bekerja
- Audit struktur repository dan temukan sumber yang relevan: kerangka modul, silabus, referensi, dan aset visual.
- Baca Bab 1 dan 2 secara menyeluruh sebelum menulis. Pelajari gaya narasi aktualnya, bukan hanya struktur judul.
- Jangan langsung menulis atau menimpa berkas sebelum memahami kondisi proyek.
- Jika ada konflik atau kekosongan sumber, laporkan; jangan diam-diam menebak atau mengisi dengan asumsi.

## Struktur modul (100% mengikuti Bab 1 dan 2)
Setiap modul disusun persis seperti Bab 1 dan 2 di `Source/Modul 1 & 2.md`:
1. **Judul modul** sebagai heading tingkat 1 (`# Judul`), sesuai judul pada kerangka di `Source/Modul 1 & 2.md`.
2. **Label metode** `*Ceramah dan diskusi:*` tepat di bawah judul.
3. **Subbab** sebagai heading tingkat 2 (`## Judul Subbab`), sesuai judul subbab pada kerangka. Tidak ada heading tingkat 3. Jangan menambah, menghapus, atau mengganti nama subbab tanpa persetujuan.
4. **Isi subbab** berupa narasi ilmiah. Butir silabus yang relevan diakomodasi di dalam subbab yang ada.
5. **Gambar**: `![](assets/...)`, lalu caption `Gambar X.Y Judul` di bawahnya, lalu baris `Sumber: ...`.
6. **Tabel**: caption `Tabel X.Y Judul` di atas tabel, lalu baris `Sumber: ...` di bawah tabel.
7. **Daftar pustaka** disatukan dalam satu `# DAFTAR PUSTAKA` di akhir dokumen, seperti pada sumber. Selama modul masih berupa berkas terpisah, daftar gabungan ini disimpan di `Output/Daftar Pustaka.md`; berkas modul tidak memuat daftar pustaka sendiri.

Modul **tidak** memuat bagian Tujuan, Capaian Pembelajaran, Rangkuman, kuis, refleksi, maupun praktik.

## Gaya penulisan
- Tiru gaya penulisan, kedalaman pembahasan, alur argumentasi, integrasi referensi, contoh, caption, dan transisi antargagasan dari Bab 1 dan 2.
- Gunakan bahasa Indonesia formal-profesional dengan kedalaman setara buku teks/short course universitas dan pelatihan teknis profesional.
- Utamakan narasi ilmiah yang mengalir, koheren, dan saling terhubung. Hindari subbab yang didominasi bullet point.
- Kembangkan konsep secara bertahap: pengertian, alasan penting, hubungan dengan konsep lain, penerapan, dan keterbatasan.
- Daftar bernomor hanya untuk komponen atau jenis, dengan pola `1. **Istilah**, penjelasan...`, didahului kalimat pengantar bertitik dua dan diikuti paragraf sintesis.
- Berikan padanan atau penjelasan bahasa Indonesia ketika istilah teknis Inggris pertama kali muncul (istilah asing dicetak miring), lalu gunakan istilah secara konsisten.
- Jangan menyalin kalimat referensi secara mekanis atau memaksakan kaitan dengan kelapa sawit jika tidak relevan.

## Contoh dan data
- Gunakan contoh dari literatur dengan sitasi yang jelas.
- Contoh yang tidak berasal dari data atau literatur harus dinyatakan sebagai ilustrasi konseptual.
- Jangan mengarang koordinat, data sampel, nilai sifat tanah, hasil analisis, akurasi model, atau temuan.

## Referensi dan akurasi
- Utamakan sumber primer, publikasi ilmiah, dan dokumentasi teknis resmi.
- Pastikan referensi mendukung klaim yang dirujuk. Jangan mengarang sitasi, DOI, angka, atau hasil penelitian.
- Catat referensi yang belum dapat diverifikasi dan bedakan fakta dari interpretasi konseptual.
- Sitasi dalam teks memakai format penulis–tahun, misalnya (Lillesand & Kiefer, 1990); daftar pustaka memakai gaya APA.

## Identitas proyek
- Institusi: Universitas Gadjah Mada (UGM) dan Pusat Studi Pengelolaan Sumber Daya Lahan (PS2DL).
- Jangan menggunakan branding PT SMART pada materi baru.
- Jangan membuat logo UGM/PS2DL palsu.
- Pertahankan istilah, judul modul, penomoran gambar/tabel, ID visual, caption, dan nama berkas sesuai konvensi proyek.

## Visual dan produksi
- Semua gambar dibuat dengan Python (matplotlib) melalui skrip di `Output/scripts/`. Gambar dari referensi digambar ulang dengan atribusi "Digambar ulang dengan modifikasi dari ..."; gambar berisi data empiris tidak digambar ulang tanpa data aslinya.
- Tempatkan visual dekat dengan pembahasan yang dijelaskannya.
- Setiap visual memiliki ID unik (nama berkas `MN-Gkk_nama.png` di `Output/assets/modul-N/`; ilustrasi di dalam sel tabel memakai `MN-Tkk[a-z]_nama.png`), nomor, caption, dan sumber atau keterangan sebagai diagram konseptual.
- Jangan membuat visual yang seolah-olah menunjukkan data empiris jika data tidak tersedia.
- Keluaran sementara berupa satu berkas per modul (`Output/Modul N.md`). Setelah semua modul selesai, gabungkan menjadi satu berkas .docx yang rapi.
- Jangan mengubah `Source/Modul 1 & 2.md`; revisi Bab 1 dan 2 ditulis ke `Output/`.

## Workflow wajib
1. Audit repository dan sumber.
2. Baca Bab 1 dan 2, lalu simpulkan pola editorial aktual.
3. Periksa kerangka modul, silabus, dan batas cakupan modul target.
4. Buat outline (judul subbab sesuai kerangka) dan batas cakupan sebelum menulis.
5. Kembangkan materi per subbab.
6. Periksa akurasi, referensi, istilah, dan kesinambungan antarmodul.
7. Periksa visual, caption, ID, serta struktur berkas.
8. Jalankan pemeriksaan teknis yang relevan (`Output/scripts/periksa_modul.py`).
9. Laporkan file yang dibuat/diubah, pemeriksaan, masalah tersisa, dan asumsi.

Jangan menulis semua modul sekaligus tanpa pemeriksaan. Untuk perubahan besar yang memengaruhi struktur proyek, ajukan rencana terlebih dahulu dan tunggu persetujuan.

## Kriteria mutu
Materi siap ditinjau jika strukturnya identik dengan Bab 1 dan 2, gayanya konsisten, alurnya mengalir dan cukup mendalam, isinya sesuai kerangka dan silabus, akurat dan dapat ditelusuri, bebas dari data/sumber rekaan, konsisten dalam visual, serta terintegrasi dengan repository.
