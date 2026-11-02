# PANDUAN PENGGUNAAN JUPYTER NOTEBOOK & VIRTUAL ENVIRONMENT (VENV)
## Pelatihan Pemanfaatan Remote Sensing, PSS, dan DSM untuk Pertanian Presisi
**Pusat Studi Pengelolaan Sumber Daya Lahan (PS2DL) UGM & PT SMART Tbk**

---

Direktori ini memuat dua Jupyter Notebook interaktif:
1. `Praktik_03_Demonstrasi_PSS_Kemometrika.ipynb`: Analisis kemometrika spektroskopi Vis-NIR (350–2500 nm) dan kalibrasi PLSR C-Organik.
2. `Praktik_05_Machine_Learning_Digital_Soil_Mapping.ipynb`: Pemodelan spasial SCORPAN, Random Forest, dan ketidakpastian QRF (PI90) C-Organik 0–20 cm.

---

## PENYIAPAN PYTHON VIRTUAL ENVIRONMENT (`venv`)

Untuk mencegah benturan versi paket Python (*dependency conflict*) dan memastikan kelancaran eksekusi algoritma kemometrika serta machine learning spasial, **seluruh peserta diarahkan menjalankan notebook dalam virtual environment terisolasi (`env_smart`)**.

### Cara 1: Setup Cepat Satu Klik (Otomatis)
Buka terminal / command prompt, lalu jalankan skrip pembangun otomatis dari folder `Output/Pelatihan/`:
* **Linux / macOS:**
  ```bash
  cd Output/Pelatihan
  ./setup_env.sh
  ```
* **Windows (Command Prompt / PowerShell):**
  ```cmd
  cd Output\Pelatihan
  setup_env.bat
  ```

---

### Cara 2: Setup Manual Langkah demi Langkah

#### 1. Buat Virtual Environment
Buka terminal di folder `Output/Pelatihan/`:
* *Linux / macOS:*
  ```bash
  python3 -m venv env_smart
  ```
* *Windows:*
  ```cmd
  python -m venv env_smart
  ```

#### 2. Aktivasi Virtual Environment
* *Linux / macOS:*
  ```bash
  source env_smart/bin/activate
  ```
* *Windows (Command Prompt):*
  ```cmd
  env_smart\Scripts\activate.bat
  ```
* *Windows (PowerShell):*
  ```powershell
  .\env_smart\Scripts\Activate.ps1
  ```
*(Indikator berhasil: muncul prefiks `(env_smart)` di awal baris terminal).*

#### 3. Instal Paket Dependensi
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Daftarkan Kernel ke Jupyter
```bash
python -m ipykernel install --user --name=env_smart --display-name="Python (Pelatihan SMART)"
```

#### 5. Buka JupyterLab
```bash
jupyter lab
```

---

## PEMILIHAN KERNEL DI JUPYTERLAB
Saat Anda membuka notebook `.ipynb` di antarmuka Jupyter:
1. Perhatikan indikator kernel di pojok kanan atas jendela kerja.
2. Pastikan tertulis **`Python (Pelatihan SMART)`**.
3. Jika masih tertulis `Python 3` atau yang lain, klik pada nama kernel tersebut, lalu pilih **`Python (Pelatihan SMART)`** dari daftar dropdown kernel.
4. Anda siap menjalankan sel demi sel dari atas ke bawah!
