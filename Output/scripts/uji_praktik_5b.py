"""Uji coba Praktik 5 bagian akhir: menampilkan peta tutupan material hasil notebook di QGIS bersama peta SMU."""
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.join(os.environ['AKAR_PROYEK'], 'Output', 'scripts'))
from uji_qgis_umum import *  # noqa


def uji():
    u = Uji(5)
    # lanjutkan nomor tangkapan layar QGIS dari bagian 5a; tangkapan layar notebook (J*) tidak dihitung
    u.no = len([f for f in os.listdir(u.foto) if re.match(r'\d\d_', f)])
    smu_p2 = os.path.join(PELATIHAN, 'data', 'praktik-2', 'hasil', 'smu_akhir.gpkg')
    if os.path.exists(smu_p2):
        shutil.copy2(smu_p2, u.d('smu_akhir.gpkg'))
    u.siapkan_jendela()
    proj = QgsProject.instance()
    proj.setFileName(u.h('Praktik_5_selesai.qgz'))
    gp = u.d('bompon_vektor.gpkg')
    pred = u.raster(u.h('prediksi_material.tif'), 'prediksi_material')
    acuan = u.raster(u.d('material_acuan_10m.tif'), 'material_acuan_10m', tampil=False)
    pel = u.raster(u.h('peluang_maks_material.tif'), 'peluang_maks_material', tampil=False)
    ses = u.raster(u.h('kesesuaian_material.tif'), 'kesesuaian_material', tampil=False)
    aoa = u.raster(u.h('aoa_material.tif'), 'aoa_material', tampil=False)
    smu = u.vektor(u.d('smu_akhir.gpkg'), nama='smu_akhir')
    tt = u.vektor(u.d('titik_tutupan_material.gpkg'), 'titik_tutupan_material', nama='titik_tutupan_material')
    u.titik(tt, '#111111', '1.4')
    batas = u.vektor(gp, 'batas_subdas')
    u.garis_tepi(batas, 'black', '0.7')
    u.palet(pred, PALET_MATERIAL)
    u.palet(acuan, PALET_MATERIAL)
    u.semu(pel, 'Viridis', mn=0, mx=1)
    u.palet(ses, {1: ('#a6d96a', 'Sama dengan peta acuan'), 2: ('#fdae61', 'Berbeda dari peta acuan')})
    u.palet(aoa, {0: ('#d7191c', 'Di luar AOA'), 1: ('#a6d96a', 'Di dalam AOA')})
    # batas SMU sebagai garis
    from qgis.core import QgsSingleSymbolRenderer
    smu.setRenderer(QgsSingleSymbolRenderer(QgsFillSymbol.createSimple({'style': 'no', 'outline_color': '#333333', 'outline_width': '0.15'})))
    u.urut(tt, batas, smu, pred, acuan, pel, ses, aoa)
    u.zoom(batas, 1.1)
    u.hanya(pred, smu, tt, batas)
    u.foto_jendela('peta_prediksi_material_dengan_smu')
    u.hanya(pel, smu, tt, batas)
    u.foto_jendela('peta_peluang_maks')
    u.hanya(ses, tt, batas)
    u.foto_jendela('peta_kesesuaian')
    u.hanya(aoa, smu, tt, batas)
    u.foto_jendela('peta_aoa')

    # komposisi material per poligon SMU: jumlah piksel setiap kelas di dalam setiap poligon
    r = u.dialog('native:zonalhistogram', {'INPUT_RASTER': pred, 'RASTER_BAND': 1, 'INPUT_VECTOR': smu, 'COLUMN_PREFIX': 'kelas_', 'OUTPUT': u.h('smu_komposisi_material.gpkg')}, 'dialog_zonal_histogram', ukuran=(760, 560))
    sk = u.vektor(r['OUTPUT'], nama='smu_komposisi_material')
    u.lihat(sk, False)
    kolom = [f.name() for f in sk.fields() if re.fullmatch(r'kelas_\d+', f.name())]
    ringkas = {}
    for ft in sk.getFeatures():
        b = ringkas.setdefault(ft['bentuklahan'], {k: 0 for k in kolom})
        for k in kolom:
            b[k] += ft[k] or 0
    # persen luas setiap kelas di setiap bentuklahan peta SMU
    u.catat('komposisi_material_per_bentuklahan_smu', {bl: {k: round(100 * v / max(1, sum(n.values())), 1) for k, v in n.items()} for bl, n in ringkas.items()})
    u.catat('luas_ha_per_bentuklahan_smu', {bl: round(sum(n.values()) * 100 / 1e4, 1) for bl, n in ringkas.items()})
    meja = iface.showAttributeTable(sk)
    meja.setMinimumSize(1300, 560)  # di Windows resize saja tidak cukup
    meja.resize(1300, 560)
    u.foto_widget(meja, 'tabel_komposisi_smu')
    meja.close()
    u.hanya(pred, smu, tt, batas)
    u.selesai()


jalankan(uji)
