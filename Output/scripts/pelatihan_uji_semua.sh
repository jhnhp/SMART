#!/bin/bash
# Mengulang seluruh uji coba praktik: data, QGIS, notebook. Keluaran lama ditimpa.
# Selama uji, keluaran ditulis ke hasil/ seperti yang dilakukan peserta, lalu diganti nama menjadi hasil-contoh/.
#
# Jalankan dari salinan proyek di folder bernama netral agar screenshot tidak memuat nama folder pribadi.
# Pemakaian: bash Output/scripts/pelatihan_uji_semua.sh <python_dengan_pustaka_notebook> <folder_profil_qgis>
set -e
PY=$1; PROFIL=$2
export AKAR_PROYEK="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$AKAR_PROYEK/Output/scripts"
DATA=../Pelatihan/data
export LOG_UJI=$PROFIL/galat_uji.txt; rm -f "$LOG_UJI"
qg() { QT_QPA_PLATFORM=offscreen timeout 600 qgis --nologo --noversioncheck --profiles-path "$PROFIL" --lang en --code "uji_praktik_$1.py" >"$PROFIL/log_$1.txt" 2>&1; }
# tangkapan layar portal (W*) pada praktik-0 diambil manual dari browser dan tidak dihapus
rm -rf ../Pelatihan/screenshots/praktik-{1,2,3,4,5} $DATA/praktik-{0,1,2,3,4,5}/hasil-contoh $DATA/praktik-{0,1,2,3,4,5}/hasil
python3 pelatihan_siapkan_data.py
qg 1; qg 2; qg 4; qg 5a
"$PY" pelatihan_buat_notebook.py
"$PY" pelatihan_buat_notebook_0_1.py
for n in "praktik-0/Praktik_0_Akuisisi_Data" "praktik-1/Praktik_1_Evaluasi_Pansharpening" "praktik-3/Praktik_3_Spektrum_ke_Sifat_Tanah" "praktik-5/Praktik_5_Machine_Learning_DSM"; do
  (cd "$DATA/$(dirname "$n")" && "$PY" -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=1200 "$(basename "$n").ipynb")
done
qg 5b
for n in 0 1 2 3 4 5; do mv "$DATA/praktik-$n/hasil" "$DATA/praktik-$n/hasil-contoh"; done
find "$DATA" -name "*.aux.xml" -delete
if [ -f "$LOG_UJI" ]; then echo "ADA GALAT:"; cat "$LOG_UJI"; exit 1; fi
echo "Uji coba selesai tanpa galat."
