"""Uji coba Praktik 4 (Bare Soil Detection) di QGIS. Lihat uji_qgis_umum.py untuk cara menjalankan."""
import os
import sys

sys.path.insert(0, os.path.join(os.environ['AKAR_PROYEK'], 'Output', 'scripts'))
from uji_qgis_umum import *  # noqa
import numpy as np


def baca(lyr, band=1):
    pr = lyr.dataProvider()
    b = pr.block(band, lyr.extent(), lyr.width(), lyr.height())
    return np.array([[b.value(r, c) for c in range(lyr.width())] for r in range(lyr.height())])


def uji():
    u = Uji(4)
    u.siapkan_jendela()
    proj = QgsProject.instance()
    gp = u.d('bompon_vektor.gpkg')
    s25 = u.raster(u.d('sentinel2_l2a_20250721_10m.tif'), tampil=False)
    scl25 = u.raster(u.d('sentinel2_l2a_20250721_scl_10m.tif'), tampil=False)
    s24 = u.raster(u.d('sentinel2_l2a_20240813_10m.tif'))
    scl24 = u.raster(u.d('sentinel2_l2a_20240813_scl_10m.tif'), tampil=False)
    pl = u.vektor(gp, 'penggunaan_lahan')
    warna_pl = {'Agroforestri': '#1b7837', 'Tegalan': '#e6c229', 'Sawah': '#67a9cf', 'Permukiman': '#d73027'}
    u.kategori(pl, 'penggunaan_lahan', warna_pl, transparan=170)
    u.lihat(pl, False)
    jalan = u.vektor(gp, 'jalan')
    u.garis(jalan, '#ffffff', '0.3')
    u.lihat(jalan, False)
    batas = u.vektor(gp, 'batas_subdas')
    u.garis_tepi(batas, 'yellow', '0.7')
    u.rgb(s24, 5, 4, 2)
    u.rgb(s25, 9, 7, 2)
    u.zoom(batas, 1.1)
    u.urut(batas, jalan, pl, s24, s25, scl24, scl25)
    u.foto_jendela('komposit_swir_20240813')
    u.hanya(s25, batas)
    u.foto_jendela('komposit_swir_20250721')
    u.properti(s24, 'mOptsPage_Information', 'informasi_kanal_2024')

    # Tahap 2: masker awan dari SCL
    n24, n25 = s24.name(), s25.name()
    b24 = u.kalkulator(f'("{scl24.name()}@1" = 4) OR ("{scl24.name()}@1" = 5)', u.h('bersih_20240813.tif'), scl24, foto='kalkulator_masker_scl')
    b25 = u.kalkulator(f'("{scl25.name()}@1" = 4) OR ("{scl25.name()}@1" = 5)', u.h('bersih_20250721.tif'), scl25)

    # Tahap 3: indeks
    ndvi24 = u.kalkulator(f'("{n24}@4" - "{n24}@3") / ("{n24}@4" + "{n24}@3")', u.h('ndvi_20240813.tif'), s24, foto='kalkulator_ndvi')
    savi24 = u.kalkulator(f'1.5 * ("{n24}@4" - "{n24}@3") / ("{n24}@4" + "{n24}@3" + 0.5)', u.h('savi_20240813.tif'), s24)
    bsi24 = u.kalkulator(f'(("{n24}@5" + "{n24}@3") - ("{n24}@4" + "{n24}@1")) / (("{n24}@5" + "{n24}@3") + ("{n24}@4" + "{n24}@1"))', u.h('bsi_20240813.tif'), s24, foto='kalkulator_bsi')
    nbr24 = u.kalkulator(f'("{n24}@5" - "{n24}@6") / ("{n24}@5" + "{n24}@6")', u.h('nbr2_20240813.tif'), s24)
    ndvi25 = u.kalkulator(f'("{n25}@7" - "{n25}@3") / ("{n25}@7" + "{n25}@3")', u.h('ndvi_20250721.tif'), s25)
    bsi25 = u.kalkulator(f'(("{n25}@9" + "{n25}@3") - ("{n25}@7" + "{n25}@1")) / (("{n25}@9" + "{n25}@3") + ("{n25}@7" + "{n25}@1"))', u.h('bsi_20250721.tif'), s25)
    nbr25 = u.kalkulator(f'("{n25}@9" - "{n25}@10") / ("{n25}@9" + "{n25}@10")', u.h('nbr2_20250721.tif'), s25)
    u.semu(ndvi24, 'RdYlGn', mn=0.1, mx=0.9)
    u.semu(savi24, 'RdYlGn', mn=0.05, mx=0.6)
    u.semu(bsi24, 'RdYlBu', mn=-0.4, mx=0.2, balik=True)
    u.semu(nbr24, 'PuOr', mn=0.05, mx=0.45)
    u.semu(ndvi25, 'RdYlGn', mn=0.1, mx=0.9)
    u.semu(bsi25, 'RdYlBu', mn=-0.4, mx=0.2, balik=True)
    u.semu(nbr25, 'PuOr', mn=0.05, mx=0.45)
    u.urut(batas, ndvi24, bsi24, nbr24, savi24, ndvi25, bsi25, nbr25, b24, b25, jalan, pl, s24, s25, scl24, scl25)
    u.hanya(batas, ndvi24)
    u.foto_jendela('ndvi_20240813')
    u.hanya(batas, bsi24)
    u.foto_jendela('bsi_20240813')
    u.hanya(batas, nbr24)
    u.foto_jendela('nbr2_20240813')

    # Tahap 4: membandingkan aturan
    def aturan(nama, eks, acuan, foto=None):
        return u.kalkulator(eks, u.h(nama + '.tif'), acuan, foto=foto)
    nn, nb, nr, nc = ndvi24.name(), bsi24.name(), nbr24.name(), b24.name()
    a = aturan('aturan_a_ndvi025', f'("{nn}@1" < 0.25) AND ("{nc}@1" = 1)', ndvi24)
    b = aturan('aturan_b_ndvi035_bsi0', f'("{nn}@1" < 0.35) AND ("{nb}@1" > 0) AND ("{nc}@1" = 1)', ndvi24, foto='kalkulator_aturan_b')
    c = aturan('aturan_c_ndvi025_nbr2', f'("{nn}@1" < 0.25) AND ("{nr}@1" > -0.30) AND ("{nr}@1" < 0.10) AND ("{nc}@1" = 1)', ndvi24)
    nn5, nb5, nc5 = ndvi25.name(), bsi25.name(), b25.name()
    b5 = aturan('aturan_b_20250721', f'("{nn5}@1" < 0.35) AND ("{nb5}@1" > 0) AND ("{nc5}@1" = 1)', ndvi25)
    tabel = {}
    for l in (a, b, c, b5):
        z = processing.run('native:zonalhistogram', {'INPUT_RASTER': l, 'RASTER_BAND': 1, 'INPUT_VECTOR': batas, 'COLUMN_PREFIX': 'H_', 'OUTPUT': 'memory:'})['OUTPUT']
        ft = next(z.getFeatures())
        tabel[l.name()] = {f: ft[f] for f in z.fields().names() if f.startswith('H_')}
    u.catat('piksel_per_aturan_dalam_subdas', tabel)
    u.palet(b, {0: ('#00000000', 'Bukan'), 1: ('#00ffff', 'Kandidat tanah terbuka')})
    u.palet(a, {0: ('#00000000', 'Bukan'), 1: ('#ff00ff', 'NDVI < 0,25')})
    u.palet(b5, {0: ('#00000000', 'Bukan'), 1: ('#ff0000', 'Kandidat tanah terbuka')})
    u.urut(batas, b, a, s24, jalan, pl, ndvi24)
    u.hanya(batas, b, s24)
    u.foto_jendela('masker_aturan_b_di_atas_citra')
    from qgis.core import QgsRectangle
    u.canvas.setExtent(QgsRectangle(396650, 9164150, 397450, 9165250))
    u.render()
    u.foto_jendela('masker_aturan_b_diperbesar')
    u.palet(b, {0: ('#00000000', 'Bukan'), 1: ('#000000', 'Kandidat tanah terbuka')})
    u.hanya(batas, b, jalan, pl)
    u.foto_jendela('masker_aturan_b_di_atas_penggunaan_lahan')
    u.zoom(batas, 1.1)
    u.foto_jendela('masker_aturan_b_seluruh_subdas')

    # Tahap 5: per penggunaan lahan
    r = u.dialog('native:zonalhistogram', {'INPUT_RASTER': b, 'RASTER_BAND': 1, 'INPUT_VECTOR': pl, 'COLUMN_PREFIX': 'H_', 'OUTPUT': u.h('histogram_per_penggunaan_lahan.gpkg')}, 'dialog_zonal_histogram', ukuran=(760, 520))
    zh = u.vektor(r['OUTPUT'], nama='histogram_per_penggunaan_lahan')
    r2 = u.dialog('qgis:statisticsbycategories', {'INPUT': zh, 'VALUES_FIELD_NAME': 'H_1', 'CATEGORIES_FIELD_NAME': ['penggunaan_lahan'], 'OUTPUT': u.h('rekap_per_penggunaan_lahan.csv')}, 'dialog_statistik_penggunaan', ukuran=(760, 500))
    rekap = {}
    for ft in zh.getFeatures():
        k = ft['penggunaan_lahan']
        rekap.setdefault(k, [0, 0])
        rekap[k][0] += ft['H_1']
        rekap[k][1] += ft['H_0'] + ft['H_1']
    u.catat('aturan_b_per_penggunaan_lahan', {k: dict(terbuka=v[0], semua=v[1], persen=round(100 * v[0] / v[1], 2)) for k, v in rekap.items()})
    z5 = processing.run('native:zonalhistogram', {'INPUT_RASTER': b5, 'RASTER_BAND': 1, 'INPUT_VECTOR': pl, 'COLUMN_PREFIX': 'H_', 'OUTPUT': 'memory:'})['OUTPUT']
    rekap5 = {}
    for ft in z5.getFeatures():
        rekap5[ft['penggunaan_lahan']] = rekap5.get(ft['penggunaan_lahan'], 0) + ft['H_1']
    u.catat('aturan_b_2025_per_penggunaan_lahan', rekap5)

    # Tahap 6: buang permukiman
    r = u.dialog('native:extractbyexpression', {'INPUT': pl, 'EXPRESSION': '"penggunaan_lahan" <> \'Permukiman\'', 'OUTPUT': u.h('lahan_non_permukiman.gpkg')}, 'dialog_extract_non_permukiman', ukuran=(760, 460))
    np_l = u.vektor(r['OUTPUT'], nama='lahan_non_permukiman')
    r = processing.run('native:zonalhistogram', {'INPUT_RASTER': b, 'RASTER_BAND': 1, 'INPUT_VECTOR': np_l, 'COLUMN_PREFIX': 'H_', 'OUTPUT': 'memory:'})['OUTPUT']
    tot = sum(ft['H_1'] for ft in r.getFeatures())
    u.catat('aturan_b_tanpa_permukiman_piksel', tot)
    r = u.dialog('gdal:cliprasterbymasklayer', {'INPUT': b, 'MASK': np_l, 'SOURCE_CRS': None, 'TARGET_CRS': None, 'TARGET_EXTENT': None, 'NODATA': 0, 'ALPHA_BAND': False, 'CROP_TO_CUTLINE': False,
                                                'KEEP_RESOLUTION': True, 'SET_RESOLUTION': False, 'X_RESOLUTION': None, 'Y_RESOLUTION': None, 'MULTITHREADING': False, 'OPTIONS': '', 'DATA_TYPE': 1, 'EXTRA': '', 'OUTPUT': u.h('masker_tanah_terbuka_20240813.tif')}, 'dialog_clip_masker', ukuran=(860, 760))
    mt = u.raster(r['OUTPUT'], 'masker_tanah_terbuka_20240813')
    u.palet(mt, {1: ('#00ffff', 'Tanah terbuka (bukan permukiman)')})
    u.urut(batas, mt, pl, s24)
    u.hanya(batas, mt, s24)
    u.canvas.setExtent(QgsRectangle(396650, 9164150, 397450, 9165250))
    u.render()
    u.foto_jendela('masker_final')
    u.zoom(batas, 1.1)

    # Tahap 7: ekstraksi informasi
    bi = u.kalkulator(f'sqrt(("{n24}@3"^2 + "{n24}@2"^2 + "{n24}@1"^2) / 3)', u.h('bi_20240813.tif'), s24)
    cmr = u.kalkulator(f'"{n24}@5" / "{n24}@6"', u.h('cmr_20240813.tif'), s24)
    bim = u.kalkulator(f'"{bi.name()}@1" / ("{mt.name()}@1" = 1)', u.h('bi_tanah_terbuka.tif'), bi, foto='kalkulator_ekstraksi')
    cmrm = u.kalkulator(f'"{cmr.name()}@1" / ("{mt.name()}@1" = 1)', u.h('cmr_tanah_terbuka.tif'), cmr)
    st = {}
    for l in (bi, cmr, bim, cmrm):
        z = processing.run('native:rasterlayerstatistics', {'INPUT': l, 'BAND': 1})
        st[l.name()] = dict(min=round(z['MIN'], 3), rerata=round(z['MEAN'], 3), maks=round(z['MAX'], 3), simpangan=round(z['STD_DEV'], 3), jumlah_valid=z.get('SUM') and round(z['SUM'] / z['MEAN']))
    u.catat('statistik_ekstraksi', st)
    u.semu(cmrm, 'YlOrBr', mn=1.0, mx=2.0)
    u.urut(batas, cmrm, bim, mt, s24)
    u.hanya(batas, cmrm, s24)
    u.canvas.setExtent(QgsRectangle(396650, 9164150, 397450, 9165250))
    u.render()
    u.foto_jendela('cmr_hanya_pada_tanah_terbuka')
    u.zoom(batas, 1.1)

    # Rerata pantulan piksel tanah terbuka dan vegetasi, pemeriksaan spektrum menurut Dematte et al. (2020)
    A = np.stack([baca(s24, i) for i in range(1, 7)])
    M = baca(mt)
    B = baca(b)
    N = baca(ndvi24)
    bk = M == 1
    veg = (N > 0.8) & (B == 0)
    u.catat('spektrum_rerata', dict(kanal=['B02', 'B03', 'B04', 'B08', 'B11', 'B12'], tanah_terbuka=[round(float(A[i][bk].mean()), 4) for i in range(6)], vegetasi=[round(float(A[i][veg].mean()), 4) for i in range(6)], n_terbuka=int(bk.sum()), n_vegetasi=int(veg.sum())))

    # Tahap 8: komposit dua tanggal
    r = u.dialog('native:cellstatistics', {'INPUT': [ndvi24, ndvi25], 'STATISTIC': 6, 'IGNORE_NODATA': True, 'REFERENCE_LAYER': ndvi24, 'OUTPUT_NODATA_VALUE': -9999, 'OUTPUT': u.h('ndvi_minimum.tif')}, 'dialog_cell_statistics', ukuran=(760, 560))
    nm = u.raster(r['OUTPUT'], 'ndvi_minimum')
    fr = u.kalkulator(f'"{b.name()}@1" + "{b5.name()}@1"', u.h('frekuensi_terbuka.tif'), b)
    u.palet(fr, {1: ('#fdae61', 'Terbuka satu kali'), 2: ('#d7191c', 'Terbuka dua kali')})
    u.urut(batas, fr, s24)
    u.hanya(batas, fr, s24)
    u.foto_jendela('frekuensi_keterbukaan')
    z = processing.run('native:zonalhistogram', {'INPUT_RASTER': fr, 'RASTER_BAND': 1, 'INPUT_VECTOR': batas, 'COLUMN_PREFIX': 'H_', 'OUTPUT': 'memory:'})['OUTPUT']
    ft = next(z.getFeatures())
    u.catat('frekuensi', {f: ft[f] for f in z.fields().names() if f.startswith('H_')})
    # komposit CMR dari tanggal dengan NDVI terendah
    k = u.kalkulator(f'("{nn}@1" <= "{nn5}@1") * "{cmr.name()}@1" + ("{nn}@1" > "{nn5}@1") * ("{n25}@9" / "{n25}@10")', u.h('komposit_cmr_terbersih.tif'), ndvi24, foto='kalkulator_komposit')
    u.semu(k, 'YlOrBr', mn=1.4, mx=2.6)
    u.urut(batas, k, nm, fr, s24)
    u.hanya(batas, k)
    u.foto_jendela('komposit_cmr_terbersih')
    u.hanya(batas, mt, s24)
    u.urut(batas, mt, s24)
    u.selesai()


jalankan(uji)
