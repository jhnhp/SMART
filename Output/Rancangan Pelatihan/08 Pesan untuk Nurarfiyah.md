# Pesan untuk Nurarfiyah

Status: draf pesan, silakan sesuaikan nadanya sebelum dikirim.
Tujuan pesan: melengkapi data Sub-DAS Bompon untuk praktik. Daftar kekurangannya diambil dari `Source/Data Bompon/README.md`.

---

Halo Nurarfiyah,

Untuk praktik pelatihan RS & DSM tanggal 3–5 November, kita sepakat memakai **Sub-DAS Bompon** sebagai wilayah latihan. Data yang sudah ada di folder proyek: batas Sub-DAS, bentuklahan, kelas lereng, penggunaan lahan, posisi 50 titik sampel, serta potongan Sentinel-2 dan Copernicus DEM. Supaya alur praktik dari delineasi SMU sampai model DSM bisa jalan dengan data asli, ada beberapa hal yang ingin kuminta:

1. **Tabel hasil laboratorium per titik** untuk kedua kedalaman (0–20 dan 20–40 cm): pH, P, KPK, C-organik, fraksi tekstur, dan berat volume, dengan kode titik yang sama seperti di data sampling (A1, B30, C38, dst.).
2. **DTM LiDAR** yang menjadi dasar kelas lereng `slope_lidar25`.
3. **Peta material permukaan** (dari Malik, 2017) yang kamu pakai sebagai kovariat bahan induk.
4. **Klarifikasi beberapa titik:**
   - B30 tercatat dua kali di lokasi berbeda (6 m dan 92 m dari rencana);
   - C38 tercatat sebagai "C38" dan "C38 ril" yang terpaut sekitar 490 m;
   - B32 dan C47 tidak punya rekaman GPS.

   Posisi mana yang benar untuk dipakai?
5. **Sifat sasaran pemodelan.** Usulan sementara: **fraksi lempung 0–20 cm**, sejalan dengan tesismu. Menurutmu ini cocok untuk latihan dengan 50 titik, atau ada sifat lain yang hasilnya lebih stabil?
6. **Izin dan atribusi.** Apakah data ini boleh dibagikan ke peserta pelatihan (mereka akan menyimpan salinannya)? Kalau ada syarat atribusi, misalnya menyebut tesismu, kelompok riset, atau pemilik data lain, tolong kabari supaya bisa kucantumkan di paket data.

Selain itu, kamu memandu **hari ke-2** (lanjutan Delineasi SMU 08.00–09.00 dan praktik Bare Soil 14.15–16.00), dan juga mendampingi demo PSS Pak Pandu. Rancangan sesinya ada di `02 Rancangan Sesi Praktik.md`. Satu hal yang perlu kamu tahu: peta bentuklahan riset sengaja **tidak dibagikan di awal**. Peta itu baru dibuka di akhir Delineasi SMU sebagai pembanding hasil digitasi peserta.

Kalau bisa, data nomor 1–3 kuterima paling lambat **Jumat, 30 Oktober**, supaya sempat diuji dalam uji coba alur penuh hari Minggu, 1 November.

Terima kasih!

Johan
