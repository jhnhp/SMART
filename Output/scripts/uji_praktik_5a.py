"""Uji coba Praktik 5 bagian QGIS: penyiapan kovariat SCORPAN dan titik sampel."""
import os
import shutil
import sys

sys.path.insert(0, os.path.join(os.environ['AKAR_PROYEK'], 'Output', 'scripts'))
from uji_qgis_umum import *  # noqa


def uji():
    u = Uji(5)
    kov = u.d('kovariat')
    if os.path.isdir(kov):
        shutil.rmtree(kov)
    os.makedirs(kov)
    h1 = os.path.join(PELATIHAN, 'data', 'praktik-1', 'hasil')
    h4 = os.path.join(PELATIHAN, 'data', 'praktik-4', 'hasil')
    # elevasi tetap dari Copernicus DEM 10 m pada folder Praktik 2, karena Praktik 1 kini memakai DEMNAS dan LiDAR
    shutil.copy2(os.path.join(PELATIHAN, 'data', 'praktik-2', 'dem_10m.tif'), os.path.join(kov, 'elevasi.tif'))
    for n, t in (('s1_vv_db.tif', 'sar_vv.tif'), ('s1_vh_db.tif', 'sar_vh.tif')):
        shutil.copy2(os.path.join(h1, n), os.path.join(kov, t))
    for n, t in (('ndvi_20250721.tif', 'ndvi_2025.tif'), ('ndvi_20240813.tif', 'ndvi_2024.tif'), ('bsi_20240813.tif', 'bsi_2024.tif'), ('cmr_20240813.tif', 'cmr_2024.tif'), ('bi_20240813.tif', 'bi_2024.tif')):
        shutil.copy2(os.path.join(h4, n), os.path.join(kov, t))
    u.siapkan_jendela()
    proj = QgsProject.instance()
    gp = u.d('bompon_vektor.gpkg')
    dem = u.raster(os.path.join(kov, 'elevasi.tif'), 'elevasi')
    dem30 = u.raster(u.d('copdem_glo30_30m.tif'), tampil=False)
    u.semu(dem, 'Spectral', balik=True)
    sungai = u.vektor(gp, 'sungai')
    u.garis(sungai, '#00e5ff', '0.5')
    batas = u.vektor(gp, 'batas_subdas')
    u.garis_tepi(batas, 'black', '0.7')
    u.zoom(batas, 1.1)
    grid = '396060,397980,9162990,9166610 [EPSG:32749]'

    def ke_10m(masukan, keluaran):
        return processing.run('gdal:warpreproject', {'INPUT': masukan, 'SOURCE_CRS': None, 'TARGET_CRS': 'EPSG:32749', 'RESAMPLING': 1, 'NODATA': None, 'TARGET_RESOLUTION': 10, 'OPTIONS': '', 'DATA_TYPE': 6, 'TARGET_EXTENT': grid, 'TARGET_EXTENT_CRS': 'EPSG:32749', 'MULTITHREADING': False, 'EXTRA': '', 'OUTPUT': keluaran})['OUTPUT']

    # relief
    processing.run('gdal:slope', {'INPUT': dem, 'BAND': 1, 'SCALE': 1, 'AS_PERCENT': True, 'COMPUTE_EDGES': True, 'ZEVENBERGEN': False, 'OPTIONS': '', 'EXTRA': '', 'OUTPUT': os.path.join(kov, 'lereng.tif')})
    r = processing.run('gdal:aspect', {'INPUT': dem, 'BAND': 1, 'TRIG_ANGLE': False, 'ZERO_FLAT': True, 'COMPUTE_EDGES': True, 'ZEVENBERGEN': False, 'OPTIONS': '', 'EXTRA': '', 'OUTPUT': u.h('aspek_derajat.tif')})
    asp = u.raster(r['OUTPUT'], 'aspek_derajat', tampil=False)
    u.kalkulator(f'cos("aspek_derajat@1" * 3.14159265 / 180)', os.path.join(kov, 'arah_utara.tif'), asp, foto='kalkulator_arah_utara')
    r = u.dialog('gdal:tpitopographicpositionindex', {'INPUT': dem30, 'BAND': 1, 'COMPUTE_EDGES': True, 'OPTIONS': '', 'OUTPUT': u.h('tpi_30m.tif')}, 'dialog_tpi', ukuran=(760, 500))
    ke_10m(r['OUTPUT'], os.path.join(kov, 'tpi.tif'))
    r = processing.run('gdal:triterrainruggednessindex', {'INPUT': dem30, 'BAND': 1, 'COMPUTE_EDGES': True, 'OPTIONS': '', 'OUTPUT': u.h('tri_30m.tif')})
    ke_10m(r['OUTPUT'], os.path.join(kov, 'tri.tif'))
    # TWI dari GRASS bila tersedia
    try:
        r = u.dialog('grass:r.topidx', {'input': dem30, 'output': u.h('twi_30m.tif'), 'GRASS_REGION_PARAMETER': None, 'GRASS_REGION_CELLSIZE_PARAMETER': 0, 'GRASS_RASTER_FORMAT_OPT': '', 'GRASS_RASTER_FORMAT_META': ''}, 'dialog_twi_grass', ukuran=(760, 560))
        ke_10m(r['output'], os.path.join(kov, 'twi.tif'))
        twi_lyr = QgsRasterLayer(os.path.join(kov, 'twi.tif'), 'twi')
        s = twi_lyr.dataProvider().bandStatistics(1)
        u.catat('twi', dict(min=round(s.minimumValue, 2), rerata=round(s.mean, 2), maks=round(s.maximumValue, 2)))
    except Exception as e:
        u.catat('twi_gagal', str(e))

    # jarak ke sungai
    r = u.dialog('gdal:rasterize', {'INPUT': sungai, 'FIELD': None, 'BURN': 1, 'USE_Z': False, 'UNITS': 1, 'WIDTH': 10, 'HEIGHT': 10, 'EXTENT': grid, 'NODATA': 0, 'OPTIONS': '', 'DATA_TYPE': 0, 'INIT': None, 'INVERT': False, 'EXTRA': '', 'OUTPUT': u.h('sungai_raster.tif')}, 'dialog_rasterize_sungai', ukuran=(800, 720))
    r = u.dialog('gdal:proximity', {'INPUT': r['OUTPUT'], 'BAND': 1, 'VALUES': '1', 'UNITS': 0, 'MAX_DISTANCE': 0, 'REPLACE': 0, 'NODATA': -9999, 'OPTIONS': '', 'EXTRA': '', 'DATA_TYPE': 5, 'OUTPUT': os.path.join(kov, 'jarak_sungai.tif')}, 'dialog_jarak_sungai', ukuran=(800, 640))

    # kovariat kategorik: bentuklahan dan penggunaan lahan
    bl = u.vektor(gp, 'bentuklahan')
    pl = u.vektor(gp, 'penggunaan_lahan')
    u.lihat(bl, False)
    u.lihat(pl, False)
    eks_bl = ("CASE WHEN \"bentuklahan\"='Interfluve' THEN 1 WHEN \"bentuklahan\"='Lereng Atas Perbukitan' THEN 2 WHEN \"bentuklahan\"='Lereng Tengah Perbukitan' THEN 3 "
              "WHEN \"bentuklahan\"='Lereng Bawah Perbukitan' THEN 4 WHEN \"bentuklahan\"='Lereng Kaki Koluvial' THEN 5 WHEN \"bentuklahan\"='Dataran Koluvial' THEN 6 END")
    r = u.dialog('native:fieldcalculator', {'INPUT': bl, 'FIELD_NAME': 'kode', 'FIELD_TYPE': 1, 'FIELD_LENGTH': 2, 'FIELD_PRECISION': 0, 'FORMULA': eks_bl, 'OUTPUT': u.h('bentuklahan_kode.gpkg')}, 'dialog_kode_bentuklahan', ukuran=(860, 660))
    bk = r['OUTPUT']
    eks_pl = "CASE WHEN \"penggunaan_lahan\"='Agroforestri' THEN 1 WHEN \"penggunaan_lahan\"='Tegalan' THEN 2 WHEN \"penggunaan_lahan\"='Sawah' THEN 3 WHEN \"penggunaan_lahan\"='Permukiman' THEN 4 END"
    pk = processing.run('native:fieldcalculator', {'INPUT': pl, 'FIELD_NAME': 'kode', 'FIELD_TYPE': 1, 'FIELD_LENGTH': 2, 'FIELD_PRECISION': 0, 'FORMULA': eks_pl, 'OUTPUT': u.h('penggunaan_lahan_kode.gpkg')})['OUTPUT']
    for masukan, tujuan in ((bk, 'kat_bentuklahan.tif'), (pk, 'kat_penggunaan_lahan.tif')):
        processing.run('gdal:rasterize', {'INPUT': masukan, 'FIELD': 'kode', 'BURN': 0, 'USE_Z': False, 'UNITS': 1, 'WIDTH': 10, 'HEIGHT': 10, 'EXTENT': grid, 'NODATA': 0, 'OPTIONS': '', 'DATA_TYPE': 1, 'INIT': None, 'INVERT': False, 'EXTRA': '', 'OUTPUT': os.path.join(kov, tujuan)})

    # periksa grid semua kovariat
    laporan = {}
    for f in sorted(os.listdir(kov)):
        if f.endswith('.tif'):
            l = QgsRasterLayer(os.path.join(kov, f), f[:-4])
            s = l.dataProvider().bandStatistics(1)
            laporan[f[:-4]] = dict(kolom=l.width(), baris=l.height(), piksel=l.rasterUnitsPerPixelX(), min=round(s.minimumValue, 3), rerata=round(s.mean, 3), maks=round(s.maximumValue, 3))
    u.catat('kovariat', laporan)

    # titik sampel dari CSV
    r = u.dialog('native:createpointslayerfromtable', {'INPUT': u.d('sampel_tanah_bompon.csv'), 'XFIELD': 'x', 'YFIELD': 'y', 'ZFIELD': None, 'MFIELD': None, 'TARGET_CRS': 'EPSG:32749', 'OUTPUT': u.h('titik_sampel.gpkg')}, 'dialog_titik_dari_tabel', ukuran=(760, 560))
    tt = u.vektor(r['OUTPUT'], nama='titik_sampel')
    u.titik(tt, '#e31a1c', '2.6')
    lrg = u.raster(os.path.join(kov, 'lereng.tif'), 'lereng')
    u.semu(lrg, 'RdYlGn', mn=0, mx=45, balik=True)
    u.urut(tt, batas, sungai, lrg, dem)
    u.hanya(tt, batas, sungai, lrg)
    u.foto_jendela('titik_sampel_di_atas_lereng')
    r = u.dialog('native:rastersampling', {'INPUT': tt, 'RASTERCOPY': lrg, 'COLUMN_PREFIX': 'lereng_', 'OUTPUT': u.h('titik_sampel_lereng.gpkg')}, 'dialog_sample_raster', ukuran=(760, 520))
    tl = u.vektor(r['OUTPUT'], nama='titik_sampel_lereng')
    iface.setActiveLayer(tl)
    meja = iface.showAttributeTable(tl)
    meja.resize(1300, 560)
    u.foto_widget(meja, 'tabel_atribut_titik')
    meja.close()
    u.catat('jumlah_titik_di_dalam_batas', sum(1 for ft in tt.getFeatures() if next(batas.getFeatures()).geometry().contains(ft.geometry())))
    u.selesai()


jalankan(uji)
