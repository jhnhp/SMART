"""Uji coba Praktik 2 (Delineasi SMU) di QGIS. Lihat uji_qgis_umum.py untuk cara menjalankan.

Klik digitasi disimulasikan pada kanvas QGIS dengan alat Add Polygon Feature. Koordinatnya berasal dari
penafsiran penulis atas bayangan medan, kontur, dan komposit SWIR, bukan dari peta bentuklahan riset.
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.join(os.environ['AKAR_PROYEK'], 'Output', 'scripts'))
from uji_qgis_umum import *  # noqa
from qgis.core import QgsField, QgsFields, QgsPointXY, QgsSnappingConfig, QgsTolerance, QgsVectorFileWriter, QgsWkbTypes, QgsCoordinateTransformContext
from qgis.PyQt.QtCore import QCoreApplication, QEvent, QVariant

KOLUVIAL = 'Kaki lereng dan dataran koluvial'
PUNGGUNG = 'Punggung dan interfluve'
LERENG = 'Lereng perbukitan'
POLIGON = [
    ('K', KOLUVIAL, [(396560, 9165900), (396640, 9165920), (396660, 9165800), (396720, 9165650), (396740, 9165500), (396720, 9165400), (396680, 9165380), (396650, 9165550), (396610, 9165700), (396560, 9165700)]),
    ('K', KOLUVIAL, [(396770, 9165950), (396840, 9166000), (396850, 9165850), (396800, 9165700), (396740, 9165620), (396720, 9165680), (396770, 9165800)]),
    ('K', KOLUVIAL, [(396620, 9165180), (396700, 9165180), (396710, 9165020), (396780, 9164990), (396770, 9164930), (396660, 9164920), (396620, 9165000)]),
    ('K', KOLUVIAL, [(396880, 9164970), (397000, 9164980), (397100, 9165100), (397120, 9165200), (397180, 9165150), (397150, 9165050), (397060, 9164900), (396960, 9164800), (396940, 9164700), (396880, 9164720)]),
    ('K', KOLUVIAL, [(396950, 9164650), (397010, 9164650), (397040, 9164450), (397060, 9164330), (397120, 9164280), (397120, 9164100), (397110, 9163950), (397080, 9163830), (397020, 9163880), (397000, 9164000), (397050, 9164150), (397060, 9164230), (396980, 9164260), (396890, 9164320), (396760, 9164340), (396760, 9164380), (396960, 9164380), (396960, 9164500)]),
    ('K', KOLUVIAL, [(397190, 9164300), (397260, 9164500), (397300, 9164620), (397430, 9164640), (397380, 9164460), (397320, 9164390), (397240, 9164250)]),
    ('P', PUNGGUNG, [(396430, 9166420), (396560, 9166400), (396540, 9166100), (396440, 9165850), (396400, 9165500), (396430, 9165000), (396420, 9164700), (396470, 9164400), (396480, 9164000), (396300, 9164000), (396300, 9166400)]),
    ('P', PUNGGUNG, [(397900, 9165250), (397900, 9163800), (397430, 9163800), (397500, 9164000), (397600, 9164200), (397590, 9164500), (397560, 9164800), (397600, 9165100), (397560, 9165250)]),
    ('P', PUNGGUNG, [(396560, 9166420), (396920, 9166300), (396900, 9166050), (396950, 9165800), (397050, 9165650), (397200, 9165450), (397560, 9165250), (397600, 9165400), (397200, 9165750), (397000, 9166000), (396950, 9166420)]),
    ('L', LERENG, [(396200, 9166500), (397900, 9166500), (397900, 9163100), (396200, 9163100)]),
]


def klik(u, x, y, tombol=None):
    vp = u.canvas.viewport()
    pt = u.canvas.getCoordinateTransform().transform(QgsPointXY(x, y))
    pos = QPoint(int(round(pt.x())), int(round(pt.y())))
    QTest.mouseMove(vp, pos)
    QApplication.processEvents()
    QTest.mouseClick(vp, tombol or Qt.LeftButton, Qt.NoModifier, pos)
    QApplication.processEvents()


def uji():
    u = Uji(2)
    u.siapkan_jendela()
    proj = QgsProject.instance()
    gp = u.d('bompon_vektor.gpkg')
    s2 = u.raster(u.d('sentinel2_l2a_20250721_10m.tif'), tampil=False)
    dem = u.raster(u.d('dem_10m.tif'))
    u.semu(dem, 'Spectral', balik=True)
    sungai = u.vektor(gp, 'sungai')
    u.garis(sungai, '#00e5ff', '0.5')
    batas = u.vektor(gp, 'batas_subdas')
    u.garis_tepi(batas, 'yellow', '0.7')
    u.zoom(batas, 1.1)
    iface.setActiveLayer(dem)

    # Tahap 1: turunan DEM
    r = u.dialog('gdal:slope', {'INPUT': dem, 'BAND': 1, 'SCALE': 1, 'AS_PERCENT': True, 'COMPUTE_EDGES': True, 'ZEVENBERGEN': False, 'OPTIONS': '', 'EXTRA': '', 'OUTPUT': u.h('lereng_persen.tif')}, 'dialog_lereng', ukuran=(820, 620))
    lereng = u.raster(r['OUTPUT'], 'lereng_persen')
    u.semu(lereng, 'RdYlGn', mn=0, mx=45, balik=True)
    st = lereng.dataProvider().bandStatistics(1)
    u.catat('lereng_statistik', dict(min=round(st.minimumValue, 1), mean=round(st.mean, 1), max=round(st.maximumValue, 1)))
    r = processing.run('gdal:hillshade', {'INPUT': dem, 'BAND': 1, 'Z_FACTOR': 1, 'SCALE': 1, 'AZIMUTH': 315, 'ALTITUDE': 45, 'COMPUTE_EDGES': True, 'ZEVENBERGEN': False, 'COMBINED': False, 'MULTIDIRECTIONAL': True, 'OPTIONS': '', 'EXTRA': '', 'OUTPUT': u.h('hillshade_multiarah.tif')})
    hs = u.raster(r['OUTPUT'], 'hillshade_multiarah')
    u.urut(batas, sungai, lereng, hs, dem, s2)
    u.hanya(batas, sungai, lereng)
    u.foto_jendela('peta_lereng_persen')
    tabel = [0, 8, 1, 8, 15, 2, 15, 25, 3, 25, 45, 4, 45, 100000, 5]
    r = u.dialog('native:reclassifybytable', {'INPUT_RASTER': lereng, 'RASTER_BAND': 1, 'TABLE': tabel, 'NO_DATA': -9999, 'RANGE_BOUNDARIES': 1, 'NODATA_FOR_MISSING': False, 'DATA_TYPE': 5, 'OUTPUT': u.h('kelas_lereng.tif')}, 'dialog_reklasifikasi', ukuran=(820, 560))
    kelas = u.raster(r['OUTPUT'], 'kelas_lereng')
    warna_lereng = {1: ('#1a9641', '1: 0–8%'), 2: ('#a6d96a', '2: 8–15%'), 3: ('#ffffbf', '3: 15–25%'), 4: ('#fdae61', '4: 25–45%'), 5: ('#d7191c', '5: >45%')}
    u.palet(kelas, warna_lereng)
    u.urut(batas, sungai, kelas, lereng, hs, dem, s2)
    u.hanya(batas, sungai, kelas)
    u.foto_jendela('peta_kelas_lereng')
    r = processing.run('gdal:contour', {'INPUT': dem, 'BAND': 1, 'INTERVAL': 10, 'FIELD_NAME': 'ELEV', 'CREATE_3D': False, 'IGNORE_NODATA': False, 'NODATA': None, 'OFFSET': 0, 'EXTRA': '', 'OUTPUT': u.h('kontur_10m.gpkg')})
    kontur = u.vektor(r['OUTPUT'], nama='kontur_10m')
    u.garis(kontur, '#ff9933', '0.15')

    # Tahap 2: indeks sifat tanah dari Sentinel-2
    n = s2.name()
    bi = u.kalkulator(f'sqrt(("{n}@3"^2 + "{n}@2"^2 + "{n}@1"^2) / 3)', u.h('indeks_bi.tif'), s2, foto='kalkulator_bi')
    ci = u.kalkulator(f'("{n}@3" - "{n}@2") / ("{n}@3" + "{n}@2")', u.h('indeks_ci.tif'), s2)
    cmr = u.kalkulator(f'"{n}@9" / "{n}@10"', u.h('indeks_cmr.tif'), s2)
    ndvi = u.kalkulator(f'("{n}@7" - "{n}@3") / ("{n}@7" + "{n}@3")', u.h('indeks_ndvi.tif'), s2)
    u.semu(bi, 'Greys', mn=0.02, mx=0.1, balik=False)
    u.semu(ci, 'RdYlBu', mn=-0.3, mx=0.2, balik=True)
    u.semu(cmr, 'YlOrBr', mn=1.4, mx=2.6)
    u.semu(ndvi, 'RdYlGn', mn=0.2, mx=0.9)
    u.urut(batas, sungai, bi, ci, cmr, ndvi, kontur, kelas, lereng, hs, dem, s2)
    u.hanya(batas, sungai, cmr)
    u.foto_jendela('indeks_cmr')
    u.hanya(batas, sungai, ndvi)
    u.foto_jendela('indeks_ndvi')
    stat = {}
    for l in (bi, ci, cmr, ndvi):
        st = l.dataProvider().bandStatistics(1)
        stat[l.name()] = dict(min=round(st.minimumValue, 3), mean=round(st.mean, 3), max=round(st.maximumValue, 3))
    u.catat('indeks_statistik', stat)

    # Tahap 3: digitasi satuan bentuklahan
    u.rgb(s2, 9, 7, 2)
    u.hanya(batas, sungai, s2)
    u.foto_jendela('acuan_komposit_swir')
    u.hanya(batas, sungai, kontur, hs)
    u.foto_jendela('acuan_bayangan_kontur')

    def foto_baru(d):
        d.resize(760, 680)
        from qgis.gui import QgsFileWidget
        from qgis.PyQt.QtWidgets import QComboBox, QToolButton
        d.findChild(QgsFileWidget, 'mFileName').setFilePath(u.h('bentuklahan_peserta.gpkg'))
        d.findChild(QLineEdit, 'mTableNameEdit').setText('bentuklahan_peserta')
        g = d.findChild(QComboBox, 'mGeometryTypeBox')
        g.setCurrentIndex(g.findText('Polygon', Qt.MatchContains))
        for nama_f in ('kode', 'bentuklahan'):
            d.findChild(QLineEdit, 'mFieldNameEdit').setText(nama_f)
            d.findChild(QToolButton, 'mAddAttributeButton').click()
        u.foto_widget(d, 'dialog_geopackage_baru')
        d.reject()
    u.modal(u.w.findChild(QAction, 'mActionNewGeoPackageLayer').trigger, foto_baru)
    jalur = u.h('bentuklahan_peserta.gpkg')
    f = QgsFields()
    f.append(QgsField('kode', QVariant.String, len=4))
    f.append(QgsField('bentuklahan', QVariant.String, len=60))
    op = QgsVectorFileWriter.SaveVectorOptions()
    op.driverName = 'GPKG'
    op.layerName = 'bentuklahan_peserta'
    tulis = QgsVectorFileWriter.create(jalur, f, QgsWkbTypes.MultiPolygon, proj.crs(), QgsCoordinateTransformContext(), op)
    del tulis
    bl = u.vektor(jalur, 'bentuklahan_peserta', 'bentuklahan_peserta')
    bl.setCrs(proj.crs())
    u.kategori(bl, 'bentuklahan', {KOLUVIAL: '#2c7fb8', PUNGGUNG: '#d95f0e', LERENG: '#78c679'}, transparan=140)
    u.urut(bl, batas, sungai, kontur, hs)
    u.hanya(bl, batas, sungai, kontur, hs)
    iface.setActiveLayer(bl)

    # snapping + avoid overlap, sesuai langkah modul
    u.w.findChild(QAction, 'mActionToggleSnappingToolBar').setChecked(True)
    cfg = proj.snappingConfig()
    cfg.setEnabled(True)
    cfg.setMode(QgsSnappingConfig.ActiveLayer)
    cfg.setTypeFlag(Qgis.SnappingType.Vertex | Qgis.SnappingType.Segment)
    cfg.setTolerance(8)
    cfg.setUnits(QgsTolerance.Pixels)
    proj.setSnappingConfig(cfg)
    proj.setTopologicalEditing(True)
    proj.setAvoidIntersectionsMode(Qgis.AvoidIntersectionsMode.AvoidIntersectionsCurrentLayer)

    bl.startEditing()
    u.w.findChild(QAction, 'mActionAddFeature').trigger()
    tunggu(500)
    u.canvas.setExtent(u.canvas.extent())
    for i, (kode, nama, koordinat) in enumerate(POLIGON):
        for x, y in koordinat:
            klik(u, x, y)
            tunggu(25)
        if i == 4:
            u.w.grab().save(u._nama('digitasi_sedang_berjalan'))
        klik(u, *koordinat[-1], Qt.RightButton)
        tunggu(700)
        # form atribut QGIS bersifat non-modal: isi lalu tekan OK seperti peserta
        form = [w for w in QApplication.topLevelWidgets() if w.isVisible() and w.metaObject().className() == 'QgsAttributeDialog']
        if not form:
            raise RuntimeError(f'Form atribut tidak muncul pada poligon {i + 1}')
        if i == 0:
            form[0].resize(620, 320)
            isian = [w for w in form[0].findChildren(QLineEdit) if w.isVisible() and w.isEnabled()]
            for w in isian:
                if 'Autogenerate' not in w.text():
                    w.setText(kode if not any(w2.text() == kode for w2 in isian) else nama)
            u.foto_widget(form[0], 'form_atribut')
        form[0].accept()
        form[0].close()
        form[0].deleteLater()
        QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
        tunggu(300)
        for ft in bl.getFeatures():
            if not ft['kode']:
                bl.changeAttributeValue(ft.id(), bl.fields().indexOf('kode'), kode)
                bl.changeAttributeValue(ft.id(), bl.fields().indexOf('bentuklahan'), nama)
        u.catat('digitasi_progres', dict(poligon_ke=i + 1, fitur=bl.featureCount()))
    bl.commitChanges()
    # sorotan form atribut hanya muncul selama form terbuka; pastikan tidak tertinggal di kanvas
    for item in u.canvas.scene().items():
        if type(item).__name__ != 'QgsMapCanvasMap' and item is not None and hasattr(item, 'hide') and 'Highlight' in type(item).__name__:
            item.hide()
    u.canvas.refresh()
    u.w.findChild(QAction, 'mActionPan').trigger()
    u.foto_jendela('hasil_digitasi_avoid_overlap')
    u.catat('digitasi', dict(fitur=bl.featureCount(), valid=all(ft.geometry().isGeosValid() for ft in bl.getFeatures())))

    # potong ke batas, hitung luas
    r = u.dialog('native:clip', {'INPUT': bl, 'OVERLAY': batas, 'OUTPUT': u.h('bentuklahan_terpotong.gpkg')}, 'dialog_clip_vektor', ukuran=(760, 460))
    bt = u.vektor(r['OUTPUT'], nama='bentuklahan_terpotong')
    r = u.dialog('native:fieldcalculator', {'INPUT': bt, 'FIELD_NAME': 'luas_ha', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 2, 'FORMULA': 'area($geometry) / 10000', 'OUTPUT': u.h('bentuklahan_luas.gpkg')}, 'dialog_kalkulator_field', ukuran=(860, 640))
    bt2 = u.vektor(r['OUTPUT'], nama='bentuklahan_luas')
    u.kategori(bt2, 'bentuklahan', {KOLUVIAL: '#2c7fb8', PUNGGUNG: '#d95f0e', LERENG: '#78c679'}, transparan=150)
    proj.removeMapLayer(bt)
    proj.removeMapLayer(bl)
    u.urut(bt2, batas, sungai, kontur, hs)
    u.hanya(bt2, batas, sungai, hs)
    u.foto_jendela('peta_bentuklahan_peserta')
    ringkas = {}
    for ft in bt2.getFeatures():
        ringkas[ft['bentuklahan']] = round(ringkas.get(ft['bentuklahan'], 0) + ft['luas_ha'], 2)
    u.catat('luas_bentuklahan_peserta_ha', ringkas)

    # Tahap 4: tumpang susun
    r = u.dialog('gdal:polygonize', {'INPUT': kelas, 'BAND': 1, 'FIELD': 'kelas', 'EIGHT_CONNECTEDNESS': False, 'EXTRA': '', 'OUTPUT': u.h('kelas_lereng_poligon.gpkg')}, 'dialog_poligonisasi', ukuran=(760, 520))
    kp = u.vektor(r['OUTPUT'], nama='kelas_lereng_poligon')
    u.catat('poligon_kelas_lereng', kp.featureCount())
    fx = u.dialog('native:fixgeometries', {'INPUT': kp, 'METHOD': 1, 'OUTPUT': 'memory:'}, 'dialog_fix_geometries', ukuran=(760, 460))['OUTPUT']
    fx.setName('kelas_lereng_diperbaiki')
    proj.addMapLayer(fx)
    u.lihat(fx, False)
    r = u.dialog('native:intersection', {'INPUT': bt2, 'OVERLAY': fx, 'INPUT_FIELDS': ['kode', 'bentuklahan'], 'OVERLAY_FIELDS': ['kelas'], 'OVERLAY_FIELDS_PREFIX': '', 'OUTPUT': 'memory:'}, 'dialog_intersection', ukuran=(760, 620))['OUTPUT']
    sp = processing.run('native:multiparttosingleparts', {'INPUT': r, 'OUTPUT': 'memory:'})['OUTPUT']
    r = processing.run('native:fieldcalculator', {'INPUT': sp, 'FIELD_NAME': 'luas_ha', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3, 'FORMULA': 'area($geometry) / 10000', 'OUTPUT': 'memory:'})['OUTPUT']
    r = processing.run('native:fieldcalculator', {'INPUT': r, 'FIELD_NAME': 'smu', 'FIELD_TYPE': 2, 'FIELD_LENGTH': 8, 'FIELD_PRECISION': 0, 'FORMULA': "\"kode\" || to_string(to_int(\"kelas\"))", 'OUTPUT': u.h('smu_mentah.gpkg')})
    sm = u.vektor(r['OUTPUT'], nama='smu_mentah')
    kecil = sum(1 for ft in sm.getFeatures() if ft['luas_ha'] < 0.4)
    u.catat('smu_mentah', dict(poligon=sm.featureCount(), lebih_kecil_MLA=kecil, persen=round(100 * kecil / sm.featureCount(), 1), jenis_smu=len({ft['smu'] for ft in sm.getFeatures()})))
    warna = {'K1': '#c6dbef', 'K2': '#6baed6', 'K3': '#2171b5', 'K4': '#08306b', 'K5': '#081d58', 'L1': '#e5f5e0', 'L2': '#a1d99b', 'L3': '#41ab5d', 'L4': '#006d2c', 'L5': '#00441b', 'P1': '#fee6ce', 'P2': '#fdae6b', 'P3': '#e6550d', 'P4': '#a63603', 'P5': '#7f2704'}
    u.kategori(sm, 'smu', warna)
    u.urut(sm, batas, bt2, kp, sungai, kontur, hs)
    u.hanya(sm, batas)
    u.foto_jendela('smu_mentah_sebelum_generalisasi')

    # Tahap 5: generalisasi ke MLA 0,4 ha (skala 1:10.000)
    sm.selectByExpression('"luas_ha" < 0.4')
    u.catat('terpilih_kecil', sm.selectedFeatureCount())
    u.foto_jendela('smu_kecil_terpilih')
    u.dialog('qgis:eliminateselectedpolygons', {'INPUT': sm, 'MODE': 2, 'OUTPUT': 'memory:'}, 'dialog_eliminate', jalankan=False, ukuran=(760, 460))
    sm.selectByExpression('"luas_ha" < 0.4')
    akhir = sm
    riwayat = []
    for putaran in range(1, 6):
        akhir.selectByExpression('"luas_ha" < 0.4')
        pilih = akhir.selectedFeatureCount()
        riwayat.append(dict(putaran=putaran, poligon=akhir.featureCount(), terpilih=pilih))
        if pilih == 0:
            break
        hasil = processing.run('qgis:eliminateselectedpolygons', {'INPUT': akhir, 'MODE': 2, 'OUTPUT': 'memory:'})['OUTPUT']
        hasil = processing.run('native:fieldcalculator', {'INPUT': hasil, 'FIELD_NAME': 'luas_ha', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 3, 'FORMULA': 'area($geometry) / 10000', 'OUTPUT': 'memory:'})['OUTPUT']
        hasil.setName('sementara')
        proj.addMapLayer(hasil, False)
        akhir = hasil
    u.catat('generalisasi_riwayat', riwayat)
    u.catat('poligon_sebelum_dissolve', akhir.featureCount())
    rf = u.dialog('native:retainfields', {'INPUT': akhir, 'FIELDS': ['smu', 'bentuklahan', 'kelas'], 'OUTPUT': 'memory:'}, 'dialog_retain_fields', ukuran=(760, 460))['OUTPUT']
    rf.setName('smu_ringkas')
    proj.addMapLayer(rf, False)
    r = u.dialog('native:dissolve', {'INPUT': rf, 'FIELD': ['smu', 'bentuklahan', 'kelas'], 'SEPARATE_DISJOINT': True, 'OUTPUT': 'memory:'}, 'dialog_dissolve', ukuran=(760, 560))['OUTPUT']
    r = processing.run('native:fieldcalculator', {'INPUT': r, 'FIELD_NAME': 'luas_ha', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 10, 'FIELD_PRECISION': 2, 'FORMULA': 'area($geometry) / 10000', 'OUTPUT': u.h('smu_akhir.gpkg')})
    smu = u.vektor(r['OUTPUT'], nama='smu_akhir')
    for nm in ('sementara', 'smu_ringkas', 'kelas_lereng_diperbaiki'):
        for l in proj.mapLayersByName(nm):
            proj.removeMapLayer(l)
    u.kategori(smu, 'smu', warna)
    u.urut(smu, batas, sm, bt2, kp, sungai, kontur, hs)
    u.hanya(smu, batas)
    u.foto_jendela('smu_akhir')
    u.catat('smu_akhir', dict(poligon=smu.featureCount(), terkecil=round(min(ft['luas_ha'] for ft in smu.getFeatures()), 3), jenis=len({ft['smu'] for ft in smu.getFeatures()})))
    r = u.dialog('qgis:statisticsbycategories', {'INPUT': smu, 'VALUES_FIELD_NAME': 'luas_ha', 'CATEGORIES_FIELD_NAME': ['smu', 'bentuklahan', 'kelas'], 'OUTPUT': u.h('legenda_smu.csv')}, 'dialog_statistik_kategori', ukuran=(760, 520))
    with open(u.h('legenda_smu.csv'), encoding='utf-8') as f2:
        u.catat('legenda_smu_csv', f2.read())

    # Tahap 6: perbandingan dengan peta riset
    rj = u.d('pembanding', 'peta_riset.gpkg')
    bref = u.vektor(rj, 'bentuklahan', 'bentuklahan_riset')
    lr = {'Interfluve': '#d95f0e', 'Lereng Atas Perbukitan': '#c2e699', 'Lereng Tengah Perbukitan': '#78c679', 'Lereng Bawah Perbukitan': '#238443', 'Lereng Kaki Koluvial': '#a6bddb', 'Dataran Koluvial': '#2c7fb8'}
    u.kategori(bref, 'bentuklahan', lr, transparan=170)
    ol = QgsVectorLayer(bt2.source(), 'batas_digitasi_peserta', 'ogr')
    proj.addMapLayer(ol)
    ol.setRenderer(QgsCategorizedSymbolRenderer('bentuklahan', [QgsRendererCategory(k, QgsFillSymbol.createSimple({'style': 'no', 'outline_color': '#111111', 'outline_width': '0.5'}), k) for k in (KOLUVIAL, PUNGGUNG, LERENG)]))
    ol.triggerRepaint()
    u.urut(ol, bref, batas, smu, sm, bt2, kp, sungai, kontur, hs)
    u.hanya(ol, bref, batas, hs)
    u.foto_jendela('banding_dengan_bentuklahan_riset')
    gab = processing.run('native:intersection', {'INPUT': bt2, 'OVERLAY': processing.run('native:fixgeometries', {'INPUT': bref, 'METHOD': 1, 'OUTPUT': 'memory:'})['OUTPUT'], 'INPUT_FIELDS': ['bentuklahan'], 'OVERLAY_FIELDS': ['bentuklahan'], 'OVERLAY_FIELDS_PREFIX': 'riset_', 'OUTPUT': 'memory:'})['OUTPUT']
    silang = {}
    for ft in gab.getFeatures():
        k = (ft['bentuklahan'], ft['riset_bentuklahan'])
        silang[k] = silang.get(k, 0) + ft.geometry().area() / 10000
    u.catat('silang_bentuklahan_ha', {' | '.join(k): round(v, 2) for k, v in silang.items()})
    luas_riset = {}
    for ft in bref.getFeatures():
        luas_riset[ft['bentuklahan']] = round(luas_riset.get(ft['bentuklahan'], 0) + ft.geometry().area() / 10000, 2)
    u.catat('luas_bentuklahan_riset_ha', luas_riset)
    # kelas lereng DEM 30 m terhadap kelas lereng LiDAR
    kref = u.vektor(rj, 'kelas_lereng', 'kelas_lereng_riset')
    u.lihat(kref, False)
    u.catat('luas_kelas_lereng_riset_ha', {ft['kelas_lereng']: round(ft['luas_ha'], 2) for ft in kref.getFeatures()})
    zh = processing.run('native:zonalhistogram', {'INPUT_RASTER': kelas, 'RASTER_BAND': 1, 'INPUT_VECTOR': batas, 'COLUMN_PREFIX': 'K_', 'OUTPUT': 'memory:'})['OUTPUT']
    ft = next(zh.getFeatures())
    u.catat('luas_kelas_lereng_dem30_ha', {n: round(ft[n] * 0.01, 2) for n in zh.fields().names() if n.startswith('K_')})
    u.hanya(smu, batas)
    u.urut(smu, batas)
    u.selesai()


jalankan(uji)
