"""Uji coba Praktik 1 (penggabungan data dan pan-sharpening) di QGIS. Lihat uji_qgis_umum.py untuk cara menjalankan."""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.environ['AKAR_PROYEK'], 'Output', 'scripts'))
from uji_qgis_umum import *  # noqa
from qgis.core import QgsContrastEnhancement, QgsPointXY, QgsRectangle

EXT10 = '396060,397980,9162990,9166610 [EPSG:32749]'
EXT25 = '396260,397780,9163190,9166410 [EPSG:32749]'
POTONG = QgsRectangle(396660, 9164210, 397460, 9165010)


def warp(u, masuk, keluar, res, metode, ext, sumber=None, foto=None, nodata=None):
    p = {'INPUT': masuk, 'SOURCE_CRS': sumber, 'TARGET_CRS': 'EPSG:32749', 'RESAMPLING': metode, 'NODATA': nodata, 'TARGET_RESOLUTION': res, 'OPTIONS': '', 'DATA_TYPE': 6,
         'TARGET_EXTENT': ext, 'TARGET_EXTENT_CRS': 'EPSG:32749', 'MULTITHREADING': False, 'EXTRA': '', 'OUTPUT': u.h(keluar)}
    if foto:
        return u.dialog('gdal:warpreproject', p, foto, ukuran=(860, 720))['OUTPUT']
    return processing.run('gdal:warpreproject', p)['OUTPUT']


def statistik(jalur):
    r = processing.run('native:rasterlayerstatistics', {'INPUT': jalur, 'BAND': 1})
    return {k: round(r[k], 5) for k in ('MIN', 'MAX', 'MEAN', 'STD_DEV')}


def rgb_tetap(u, lyr, mn=0.005, mx=0.11):
    """Rentang tampilan yang sama untuk semua citra agar warnanya dapat dibandingkan."""
    u.rgb(lyr, 1, 2, 3)
    r = lyr.renderer()
    for setel, pita in ((r.setRedContrastEnhancement, 1), (r.setGreenContrastEnhancement, 2), (r.setBlueContrastEnhancement, 3)):
        ce = QgsContrastEnhancement(lyr.dataProvider().dataType(pita))
        ce.setContrastEnhancementAlgorithm(QgsContrastEnhancement.StretchToMinimumMaximum)
        ce.setMinimumValue(mn)
        ce.setMaximumValue(mx)
        setel(ce)
    lyr.triggerRepaint()


def potong(u, lyr, nama):
    u.canvas.setExtent(POTONG)
    u.foto_jendela(nama)


def uji():
    u = Uji(1)
    u.siapkan_jendela()
    s2 = u.raster(u.d('sentinel2_l2a_20250721_10m.tif'))
    s1 = u.raster(u.d('sentinel1_rtc_20240830_10m.tif'), tampil=False)
    demnas = u.raster(u.d('DEMNAS_1408-23_v1.0.tif'), tampil=False)
    demnas.setCrs(QgsCoordinateReferenceSystem('EPSG:4326'))
    lidar = u.raster(u.d('LiDAR_Kalijambe_Bompon_20222023.tif'), tampil=False)
    fu = u.raster(u.d('foto_udara_rgb_1m.tif'), tampil=False)
    batas = iface.addVectorLayer(u.d('Batas_Bompon.shp'), 'Batas_Bompon', 'ogr')
    u.garis_tepi(batas, 'yellow', '0.7')
    u.rgb(s2, 3, 2, 1)
    u.render()
    u.zoom(batas, 1.1)
    tunggu(500)
    u.zoom(batas, 1.1)
    u.foto_jendela('data_dimuat')

    info = {}
    for l in (s2, s1, demnas, lidar, fu):
        info[l.name()] = dict(kolom=l.width(), baris=l.height(), kanal=l.bandCount(), piksel=round(l.rasterUnitsPerPixelX(), 6), crs=l.crs().authid())
    u.catat('info_raster', info)
    u.properti(demnas, 'mOptsPage_Information', 'informasi_demnas')
    u.rgb(fu, 1, 2, 3)
    u.hanya(fu, batas)
    u.urut(batas, fu)
    u.zoom(batas, 1.1)
    u.foto_jendela('foto_udara_sambungan')

    # Tahap 3: grid 10 m
    d10 = warp(u, demnas, 'demnas_10m.tif', 10, 1, EXT10, sumber='EPSG:4326', foto='warp_demnas_10m')
    l10 = warp(u, lidar, 'lidar_10m.tif', 10, 5, EXT10, foto='warp_lidar_10m')
    d10 = u.raster(d10, 'demnas_10m')
    l10 = u.raster(l10, 'lidar_10m')
    nama_s1 = s1.name()
    vv = u.kalkulator(f'10 * log10("{nama_s1}@1")', u.h('s1_vv_db.tif'), s1, foto='kalkulator_vv_db')
    vh = u.kalkulator(f'10 * log10("{nama_s1}@2")', u.h('s1_vh_db.tif'), s1)
    u.abu(vv, 1, -20, 2)
    u.hanya(vv, batas)
    u.urut(batas, vv)
    u.zoom(batas, 1.1)
    u.foto_jendela('sar_vv_db')
    u.catat('statistik', {n: statistik(p) for n, p in (('demnas_10m', d10.source()), ('lidar_10m', l10.source()), ('vv', vv.source()), ('vh', vh.source()))})

    # Tahap 4: tumpukan
    masukan = [s2.source(), vv.source(), vh.source(), d10.source(), l10.source()]
    r = u.dialog('gdal:buildvirtualraster', {'INPUT': masukan, 'RESOLUTION': 0, 'SEPARATE': True, 'PROJ_DIFFERENCE': False, 'ADD_ALPHA': False, 'ASSIGN_CRS': None,
                                             'RESAMPLING': 0, 'SRC_NODATA': '', 'EXTRA': '', 'OUTPUT': u.h('stack_bompon_10m.vrt')}, 'build_virtual_raster', ukuran=(860, 640))
    with open(r['OUTPUT'], encoding='utf-8') as f:
        isi = f.read()
    isi = re.sub(r'<SourceFilename relativeToVRT="0">[^<]*/([^/<]+)</SourceFilename>', r'<SourceFilename relativeToVRT="1">../\1</SourceFilename>', isi)
    with open(r['OUTPUT'], 'w', encoding='utf-8') as f:
        f.write(isi)
    st = u.raster(r['OUTPUT'], 'stack_bompon_10m')
    r = u.dialog('gdal:cliprasterbymasklayer', {'INPUT': st, 'MASK': batas, 'SOURCE_CRS': None, 'TARGET_CRS': None, 'TARGET_EXTENT': None, 'NODATA': -9999, 'ALPHA_BAND': False,
                                                'CROP_TO_CUTLINE': True, 'KEEP_RESOLUTION': True, 'SET_RESOLUTION': False, 'X_RESOLUTION': None, 'Y_RESOLUTION': None,
                                                'MULTITHREADING': False, 'OPTIONS': '', 'DATA_TYPE': 6, 'EXTRA': '', 'OUTPUT': u.h('stack_bompon_terpotong.tif')}, 'clip_stack', ukuran=(860, 720))
    kl = u.raster(r['OUTPUT'], 'stack_bompon_terpotong')
    u.catat('stack', dict(kanal_vrt=st.bandCount(), kolom_vrt=st.width(), baris_vrt=st.height(), kanal=kl.bandCount(), kolom=kl.width(), baris=kl.height()))
    u.rgb(kl, 7, 12, 14)
    u.hanya(kl, batas)
    u.urut(batas, kl)
    u.zoom(batas, 1.1)
    u.foto_jendela('komposit_lintas_sensor')
    x, y = 396990.0, 9165005.0
    iface.setActiveLayer(kl)
    u.w.findChild(QAction, 'mActionIdentify').trigger()
    pt = u.canvas.getCoordinateTransform().transform(QgsPointXY(x, y))
    vp = u.canvas.viewport()
    QTest.mouseMove(vp, QPoint(int(pt.x()), int(pt.y())))
    tunggu(200)
    QTest.mouseClick(vp, Qt.LeftButton, Qt.NoModifier, QPoint(int(pt.x()), int(pt.y())))
    tunggu(1500)
    u.foto_jendela('identify_stack')
    u.catat('nilai_piksel_uji', dict(x=x, y=y, kanal={b: round(kl.dataProvider().sample(QgsPointXY(x, y), b)[0], 4) for b in range(1, kl.bandCount() + 1)}))
    for d in u.w.findChildren(QDockWidget):
        if 'Identify' in d.windowTitle():
            d.hide()

    # Tahap 5: membandingkan DEM
    sel = u.kalkulator('"demnas_10m@1" - "lidar_10m@1"', u.h('selisih_demnas_lidar.tif'), d10, foto='kalkulator_selisih_dem')
    sel = processing.run('gdal:cliprasterbymasklayer', {'INPUT': sel, 'MASK': batas, 'NODATA': -9999, 'CROP_TO_CUTLINE': True, 'KEEP_RESOLUTION': True, 'DATA_TYPE': 6, 'OUTPUT': u.h('selisih_demnas_lidar_terpotong.tif')})['OUTPUT']
    sel = u.raster(sel, 'selisih_demnas_lidar_terpotong')
    u.semu(sel, 'RdBu', mn=-40, mx=40, balik=True)
    u.hanya(sel, batas)
    u.urut(batas, sel)
    u.foto_jendela('peta_selisih_dem')
    u.catat('selisih_dem', statistik(sel.source()))
    hl = processing.run('gdal:hillshade', {'INPUT': lidar, 'BAND': 1, 'Z_FACTOR': 1, 'SCALE': 1, 'AZIMUTH': 315, 'ALTITUDE': 45, 'COMPUTE_EDGES': True, 'ZEVENBERGEN': False, 'COMBINED': False, 'MULTIDIRECTIONAL': False, 'OPTIONS': '', 'EXTRA': '', 'OUTPUT': u.h('hillshade_lidar_1m.tif')})['OUTPUT']
    hd = processing.run('gdal:hillshade', {'INPUT': d10, 'BAND': 1, 'Z_FACTOR': 1, 'SCALE': 1, 'AZIMUTH': 315, 'ALTITUDE': 45, 'COMPUTE_EDGES': True, 'ZEVENBERGEN': False, 'COMBINED': False, 'MULTIDIRECTIONAL': False, 'OPTIONS': '', 'EXTRA': '', 'OUTPUT': u.h('hillshade_demnas_10m.tif')})['OUTPUT']
    hd = u.raster(hd, 'hillshade_demnas_10m')
    hl = u.raster(hl, 'hillshade_lidar_1m')
    u.urut(batas, hd, hl)
    u.hanya(hd, batas)
    u.zoom(batas, 1.1)
    u.foto_jendela('hillshade_demnas')
    u.hanya(hl, batas)
    u.foto_jendela('hillshade_lidar')

    # Tahap 6: pan dari foto udara
    n = fu.name()
    abu = u.kalkulator(f'("{n}@1" + "{n}@2" + "{n}@3") / 3', u.h('fu_abu_1m.tif'), fu, foto='kalkulator_pan_abu')
    pan = warp(u, abu, 'pan_fu_2m5.tif', 2.5, 5, EXT25, foto='warp_pan_2m5', nodata=-9999)
    pan = u.raster(pan, 'pan_fu_2m5')
    rgb = u.dialog('gdal:translate', {'INPUT': s2, 'TARGET_CRS': None, 'NODATA': None, 'COPY_SUBDATASETS': False, 'OPTIONS': '', 'EXTRA': '-b 3 -b 2 -b 1 -projwin 396260 9166410 397780 9163190', 'DATA_TYPE': 0, 'OUTPUT': u.h('s2_rgb_10m.tif')}, 'translate_s2_rgb', ukuran=(860, 640))['OUTPUT']
    rgb = u.raster(rgb, 's2_rgb_10m')
    inten = u.kalkulator('("s2_rgb_10m@1" + "s2_rgb_10m@2" + "s2_rgb_10m@3") / 3', u.h('s2_intensitas_10m.tif'), rgb)
    # statistik pan dihitung pada piksel 10 m di dalam batas, agar sebanding dengan intensitas
    pan10 = warp(u, pan, 'pan_fu_10m.tif', 10, 5, '396260,397780,9163190,9166410 [EPSG:32749]', nodata=-9999)
    inten_klip = processing.run('gdal:cliprasterbymasklayer', {'INPUT': inten, 'MASK': batas, 'NODATA': -9999, 'CROP_TO_CUTLINE': False, 'KEEP_RESOLUTION': True, 'DATA_TYPE': 6, 'OUTPUT': u.h('s2_intensitas_terpotong.tif')})['OUTPUT']
    sp, si = statistik(pan10), statistik(inten_klip)
    u.catat('statistik_pan', dict(pan_10m=sp, intensitas=si))
    ek = f'("pan_fu_2m5@1" - {sp["MEAN"]}) * {si["STD_DEV"]} / {sp["STD_DEV"]} + {si["MEAN"]}'
    u.catat('rumus_setara', ek)
    panst = u.kalkulator(ek, u.h('pan_fu_setara.tif'), pan, foto='kalkulator_pan_setara')

    # Tahap 7: pan-sharpening foto udara
    r = u.dialog('gdal:pansharp', {'SPECTRAL': rgb, 'PANCHROMATIC': panst, 'RESAMPLING': 2, 'OPTIONS': '', 'EXTRA': '', 'OUTPUT': u.h('s2_rgb_tajam_fu_2m5.tif')}, 'dialog_pansharpening', ukuran=(860, 560))
    ps = u.raster(r['OUTPUT'], 's2_rgb_tajam_fu_2m5')
    u.catat('pansharp_fu', dict(kolom=ps.width(), baris=ps.height(), kanal=ps.bandCount(), piksel=ps.rasterUnitsPerPixelX(), kanal1=statistik(ps.source())))
    for l in (rgb, ps):
        rgb_tetap(u, l)
    u.urut(batas, ps, rgb)
    u.hanya(rgb, batas)
    potong(u, rgb, 'potongan_s2_asli')
    u.hanya(ps, batas)
    potong(u, ps, 'potongan_s2_tajam_fu')

    # Tahap 8: pan-sharpening bayangan medan LiDAR
    hl25 = warp(u, hl, 'hillshade_lidar_2m5.tif', 2.5, 5, EXT25, nodata=-9999)
    hs = statistik(hl25)
    hst = u.kalkulator(f'("hillshade_lidar_2m5@1" - {hs["MEAN"]}) * {si["STD_DEV"]} / {hs["STD_DEV"]} + {si["MEAN"]}', u.h('pan_hs_setara.tif'), u.raster(hl25, 'hillshade_lidar_2m5', tampil=False))
    u.catat('statistik_hillshade', hs)
    r = processing.run('gdal:pansharp', {'SPECTRAL': rgb, 'PANCHROMATIC': hst, 'RESAMPLING': 2, 'OPTIONS': '', 'EXTRA': '', 'OUTPUT': u.h('s2_rgb_tajam_lidar_2m5.tif')})
    pl = u.raster(r['OUTPUT'], 's2_rgb_tajam_lidar_2m5')
    rgb_tetap(u, pl)
    u.urut(batas, pl, ps, rgb)
    u.hanya(pl, batas)
    potong(u, pl, 'potongan_s2_tajam_lidar')
    u.zoom(batas, 1.1)
    u.hanya(ps, batas)
    u.foto_jendela('s2_tajam_fu_seluruh')
    u.selesai()


jalankan(uji)
