# SMART Fieldbook

Website pembaca untuk delapan modul pelatihan Remote Sensing dan Digital Soil Mapping.

## Prinsip sumber

- Isi modul **tidak ditulis ulang** di aplikasi web.
- Workflow deploy menyalin file `Output/Modul 1.md` sampai `Output/Modul 8.md` ke folder `modules/` tanpa mengubah isi file.
- `app.js` hanya merender Markdown asli menjadi HTML. Penyesuaian path gambar dilakukan saat rendering, bukan pada berkas sumber.
- Setiap perubahan pada file Markdown atau aset di `Output/` memicu deployment ulang.

## Deploy

Workflow `.github/workflows/deploy-pages.yml` menyusun folder statis dan menerbitkannya menggunakan GitHub Pages. Pastikan Pages di repository diizinkan menggunakan **GitHub Actions** sebagai deployment source. Jalankan workflow `Deploy SMART Fieldbook to GitHub Pages` dari tab Actions bila deployment pertama belum terpicu.
