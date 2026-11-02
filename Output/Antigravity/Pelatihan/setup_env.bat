@echo off
REM ==============================================================================
REM Skrip Otomasi Pembuatan Virtual Environment (venv) Pelatihan SMART (Windows)
REM PS2DL UGM & PT SMART Tbk
REM ==============================================================================

set ENV_NAME=env_smart
echo === Menyiapkan Python Virtual Environment (%ENV_NAME%) ===

REM 1. Periksa ketersediaan python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Galat: python tidak ditemukan di PATH sistem. Harap instal Python 3.9+ terlebih dahulu.
    pause
    exit /b 1
)

REM 2. Buat venv jika belum ada
if not exist "%ENV_NAME%" (
    echo 1. Membuat virtual environment baru di .\%ENV_NAME% ...
    python -m venv %ENV_NAME%
) else (
    echo 1. Virtual environment .\%ENV_NAME% sudah ada.
)

REM 3. Aktivasi venv
echo 2. Mengaktifkan environment...
call %ENV_NAME%\Scripts\activate.bat

REM 4. Perbarui pip dan pasang paket
echo 3. Memperbarui pip dan menginstal pustaka dependensi...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM 5. Daftarkan kernel ke Jupyter
echo 4. Mendaftarkan kernel Jupyter...
python -m ipykernel install --user --name=%ENV_NAME% --display-name="Python (Pelatihan SMART)"

echo.
echo === Penyiapan Berhasil Selesai! ===
echo Untuk mulai belajar:
echo   1. Aktifkan venv: %ENV_NAME%\Scripts\activate.bat
echo   2. Jalankan JupyterLab: jupyter lab
echo   3. Pada JupyterLab, buka notebook di folder notebooks\ dan pilih kernel "Python (Pelatihan SMART)"
echo ==============================================================================
pause
