#!/usr/bin/env bash
# ==============================================================================
# Skrip Otomasi Pembuatan Virtual Environment (venv) Pelatihan SMART
# PS2DL UGM & PT SMART Tbk
# ==============================================================================

set -e

ENV_NAME="env_smart"
echo "=== Menyiapkan Python Virtual Environment ($ENV_NAME) ==="

# 1. Periksa ketersediaan python3
if ! command -v python3 &> /dev/null; then
    echo "Galat: python3 tidak ditemukan di sistem. Harap instal Python 3.9+ terlebih dahulu."
    exit 1
fi

# 2. Buat venv jika belum ada
if [ ! -d "$ENV_NAME" ]; then
    echo "1. Membuat virtual environment baru di ./$ENV_NAME ..."
    python3 -m venv "$ENV_NAME"
else
    echo "1. Virtual environment ./$ENV_NAME sudah ada."
fi

# 3. Aktivasi venv
echo "2. Mengaktifkan environment..."
source "$ENV_NAME/bin/activate"

# 4. Perbarui pip dan pasang paket
echo "3. Memperbarui pip dan menginstal pustaka dependensi..."
pip install --upgrade pip
pip install -r requirements.txt

# 5. Daftarkan kernel ke Jupyter
echo "4. Mendaftarkan kernel Jupyter..."
python -m ipykernel install --user --name="$ENV_NAME" --display-name="Python (Pelatihan SMART)"

echo ""
echo "=== Penyiapan Berhasil Selesai! ==="
echo "Untuk mulai belajar:"
echo "  1. Aktifkan venv: source $ENV_NAME/bin/activate"
echo "  2. Jalankan JupyterLab: jupyter lab"
echo "  3. Pada JupyterLab, buka notebook di folder notebooks/ dan pilih kernel 'Python (Pelatihan SMART)'"
echo "=============================================================================="
