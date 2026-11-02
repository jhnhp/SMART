"""Membuka setiap Praktik_N_selesai.qgz dan melaporkan layer yang gagal dimuat."""
import json
import os
from qgis.core import QgsProject
from qgis.PyQt.QtCore import QTimer

AKAR = os.environ['AKAR_PROYEK']


def go():
    lapor = {}
    for n in (1, 2, 4, 5):
        p = QgsProject.instance()
        jalur = os.path.join(AKAR, 'Output', 'Pelatihan', 'data', f'praktik-{n}', 'hasil-contoh', f'Praktik_{n}_selesai.qgz')
        ok = p.read(jalur)
        ls = list(p.mapLayers().values())
        lapor[n] = dict(terbuka=ok, layer=len(ls), rusak=[l.name() for l in ls if not l.isValid()])
    with open(os.environ['KELUAR_CEK'], 'w') as f:
        json.dump(lapor, f, indent=1)
    p.setDirty(False)
    os._exit(0)


QTimer.singleShot(4000, go)
