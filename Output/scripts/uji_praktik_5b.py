"""Uji coba Praktik 5 bagian akhir: menampilkan hasil notebook di QGIS bersama peta SMU."""
import os
import shutil
import sys

sys.path.insert(0, os.path.join(os.environ['AKAR_PROYEK'], 'Output', 'scripts'))
from uji_qgis_umum import *  # noqa


def uji():
    u = Uji(5)
    u.no = len([f for f in os.listdir(u.foto) if f.endswith('.png')])
    smu_p2 = os.path.join(PELATIHAN, 'data', 'praktik-2', 'hasil', 'smu_akhir.gpkg')
    if os.path.exists(smu_p2):
        shutil.copy2(smu_p2, u.d('smu_akhir.gpkg'))
    u.siapkan_jendela()
    proj = QgsProject.instance()
    proj.setFileName(u.h('Praktik_5_selesai.qgz'))
    gp = u.d('bompon_vektor.gpkg')
    pred = u.raster(u.h('prediksi_C_Organik_1.tif'), 'prediksi_C_Organik_1')
    pi90 = u.raster(u.h('pi90_C_Organik_1.tif'), 'pi90_C_Organik_1', tampil=False)
    aoa = u.raster(u.h('aoa_C_Organik_1.tif'), 'aoa_C_Organik_1', tampil=False)
    smu = u.vektor(u.d('smu_akhir.gpkg'), nama='smu_akhir')
    tt = u.vektor(u.h('titik_sampel.gpkg'), nama='titik_sampel')
    u.titik(tt, '#111111', '1.8')
    batas = u.vektor(gp, 'batas_subdas')
    u.garis_tepi(batas, 'black', '0.7')
    u.semu(pred, 'YlOrBr')
    u.semu(pi90, 'Magma', balik=True)
    u.palet(aoa, {0: ('#d7191c', 'Di luar AOA'), 1: ('#a6d96a', 'Di dalam AOA')})
    # batas SMU sebagai garis
    from qgis.core import QgsSingleSymbolRenderer
    smu.setRenderer(QgsSingleSymbolRenderer(QgsFillSymbol.createSimple({'style': 'no', 'outline_color': '#333333', 'outline_width': '0.15'})))
    u.urut(tt, batas, smu, pred, pi90, aoa)
    u.zoom(batas, 1.1)
    u.hanya(pred, smu, tt, batas)
    u.foto_jendela('peta_prediksi_corganik_dengan_smu')
    u.hanya(pi90, smu, tt, batas)
    u.foto_jendela('peta_pi90_dengan_smu')
    u.hanya(aoa, smu, tt, batas)
    u.foto_jendela('peta_aoa')
    r = u.dialog('native:zonalstatisticsfb', {'INPUT': smu, 'INPUT_RASTER': pred, 'RASTER_BAND': 1, 'COLUMN_PREFIX': 'pred_', 'STATISTICS': [1, 2, 4, 5, 6], 'OUTPUT': u.h('smu_prediksi.gpkg')}, 'dialog_zonal_statistik', ukuran=(760, 560))
    r2 = processing.run('native:zonalstatisticsfb', {'INPUT': r['OUTPUT'], 'INPUT_RASTER': pi90, 'RASTER_BAND': 1, 'COLUMN_PREFIX': 'pi90_', 'STATISTICS': [2], 'OUTPUT': u.h('smu_prediksi_pi90.gpkg')})
    sp = u.vektor(r2['OUTPUT'], nama='smu_prediksi_pi90')
    u.lihat(sp, False)
    ringkas = {}
    for ft in sp.getFeatures():
        ringkas.setdefault(ft['bentuklahan'], []).append((ft['luas_ha'], ft['pred_mean'], ft['pi90_mean']))
    u.catat('rerata_per_bentuklahan_peserta', {k: dict(luas_ha=round(sum(a for a, _, _ in v), 1), prediksi=round(sum(a * b for a, b, _ in v) / sum(a for a, _, _ in v), 1), pi90=round(sum(a * c for a, _, c in v) / sum(a for a, _, _ in v), 1)) for k, v in ringkas.items()})
    os.remove(u.h('smu_prediksi.gpkg'))
    meja = iface.showAttributeTable(sp)
    meja.resize(1300, 560)
    u.foto_widget(meja, 'tabel_zonal_smu')
    meja.close()
    u.hanya(pred, smu, tt, batas)
    u.selesai()


jalankan(uji)
