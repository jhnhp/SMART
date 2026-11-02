"""
Skrip Pembuat dan Penyimpan Berkas Proyek QGIS (.qgz) Mandiri untuk Sesi Praktik Pelatihan SMART (Praktik 1 s.d. 5)

Setiap proyek QGIS disimpan langsung di folder data masing-masing:
- Output/Pelatihan/data/praktik-1/Praktik_01_Multi_Source_Data_Fusion.qgz
- Output/Pelatihan/data/praktik-2/Praktik_02_Delineasi_SMU.qgz
- Output/Pelatihan/data/praktik-3/Praktik_03_Demonstrasi_PSS.qgz
- Output/Pelatihan/data/praktik-4/Praktik_04_Bare_Soil_Detection.qgz
- Output/Pelatihan/data/praktik-5/Praktik_05_Machine_Learning_DSM_C_Organik.qgz

Dijalankan via: qgis --code /home/jhn/Documents/Sayangku/Modul Junun/Output/scripts/simpan_proyek_qgis_per_praktik.py
"""

import os
import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor
from qgis.core import (
    QgsProject,
    QgsRasterLayer,
    QgsVectorLayer,
    QgsCoordinateReferenceSystem,
    QgsColorRampShader,
    QgsRasterShader,
    QgsSingleBandPseudoColorRenderer,
    QgsMultiBandColorRenderer,
    QgsSimpleLineSymbolLayer,
    QgsSimpleFillSymbolLayer,
    QgsSimpleMarkerSymbolLayer,
    QgsGraduatedSymbolRenderer,
    QgsRendererRange,
    QgsSymbol,
    QgsLayerTreeGroup
)
from qgis.gui import QgsMessageBar
from qgis.utils import iface

BASE_DIR = "/home/jhn/Documents/Sayangku/Modul Junun"
DATA_DIR = os.path.join(BASE_DIR, "Output/Pelatihan/data")

proj = QgsProject.instance()

def clean_banners():
    try:
        iface.messageBar().clearWidgets()
        for bar in iface.mainWindow().findChildren(QgsMessageBar):
            bar.clearWidgets()
            bar.hide()
    except Exception:
        pass

def zoom_to_layer(layer):
    if layer and layer.isValid():
        ext = layer.extent()
        ext.scale(1.10)
        iface.mapCanvas().setExtent(ext)
        iface.mapCanvas().refresh()

# =====================================================================
# PRAKTIK 1: MULTI-SOURCE DATA FUSION
# =====================================================================
def buat_proyek_praktik_1():
    print("\n--- [1/5] Membuat Proyek Praktik 1: Multi-Source Data Fusion ---")
    p1_dir = os.path.join(DATA_DIR, "praktik-1")
    qgz_path = os.path.join(p1_dir, "Praktik_01_Multi_Source_Data_Fusion.qgz")

    proj.clear()
    proj.setTitle("Praktik 01: Multi-Source Data Fusion & Eksplorasi Data Spasial Bompon")
    proj.setCrs(QgsCoordinateReferenceSystem("EPSG:32749"))

    # Batas Sub-DAS
    v_batas = QgsVectorLayer(os.path.join(p1_dir, "batas_subdas.gpkg"), "Batas Sub-DAS Bompon", "ogr")
    sym = QgsSimpleLineSymbolLayer()
    sym.setColor(QColor(220, 20, 60))
    sym.setWidth(0.8)
    v_batas.renderer().symbol().changeSymbolLayer(0, sym)
    proj.addMapLayer(v_batas)

    # Sentinel-2 True Color
    r_s2 = QgsRasterLayer(os.path.join(p1_dir, "sentinel2_l2a_20250721_10m.tif"), "Sentinel-2 L2A (True Color RGB 4-3-2)")
    renderer_s2 = QgsMultiBandColorRenderer(r_s2.dataProvider(), 3, 2, 1)
    r_s2.setRenderer(renderer_s2)
    proj.addMapLayer(r_s2)

    # Sentinel-1 SAR VH
    r_sar = QgsRasterLayer(os.path.join(p1_dir, "sentinel1_rtc_20240830_10m.tif"), "Sentinel-1 RTC SAR (C-band VH)")
    proj.addMapLayer(r_sar)
    proj.layerTreeRoot().findLayer(r_sar.id()).setItemVisibilityChecked(False)

    # Copernicus DEM GLO-30
    r_dem = QgsRasterLayer(os.path.join(p1_dir, "copdem_glo30_30m.tif"), "Copernicus DEM GLO-30 (30m)")
    proj.addMapLayer(r_dem)
    proj.layerTreeRoot().findLayer(r_dem.id()).setItemVisibilityChecked(False)

    zoom_to_layer(v_batas)
    proj.setFileName(qgz_path)
    proj.write(qgz_path)
    print(f"Berhasil disimpan: {qgz_path}")

# =====================================================================
# PRAKTIK 2: DELINEASI SMU
# =====================================================================
def buat_proyek_praktik_2():
    print("\n--- [2/5] Membuat Proyek Praktik 2: Delineasi Satuan Pemetaan Tanah (SMU) ---")
    p2_dir = os.path.join(DATA_DIR, "praktik-2")
    qgz_path = os.path.join(p2_dir, "Praktik_02_Delineasi_SMU.qgz")

    proj.clear()
    proj.setTitle("Praktik 02: Delineasi Satuan Pemetaan Tanah (SMU) & Analisis Kelerengan")
    proj.setCrs(QgsCoordinateReferenceSystem("EPSG:32749"))

    # Batas Sub-DAS
    v_batas = QgsVectorLayer(os.path.join(p2_dir, "batas_subdas.gpkg"), "Batas Sub-DAS Bompon", "ogr")
    sym_b = QgsSimpleLineSymbolLayer()
    sym_b.setColor(QColor(0, 0, 0))
    sym_b.setWidth(0.9)
    v_batas.renderer().symbol().changeSymbolLayer(0, sym_b)
    proj.addMapLayer(v_batas)

    # Satuan Bentuklahan
    v_landform = QgsVectorLayer(os.path.join(p2_dir, "bentuklahan_rujukan.gpkg"), "Satuan Bentuklahan Rujukan (SMU)", "ogr")
    sym_lf = QgsSimpleFillSymbolLayer()
    sym_lf.setStrokeColor(QColor(70, 130, 180))
    sym_lf.setStrokeWidth(0.6)
    sym_lf.setFillColor(QColor(70, 130, 180, 50))
    v_landform.renderer().symbol().changeSymbolLayer(0, sym_lf)
    proj.addMapLayer(v_landform)

    # Kelas Lereng Rujukan
    v_lereng = QgsVectorLayer(os.path.join(p2_dir, "kelas_lereng_rujukan.gpkg"), "Kelas Lereng Rujukan", "ogr")
    proj.addMapLayer(v_lereng)
    proj.layerTreeRoot().findLayer(v_lereng.id()).setItemVisibilityChecked(False)

    # Slope
    r_slope = QgsRasterLayer(os.path.join(p2_dir, "slope_10m.tif"), "Peta Kelerengan (Derajat)")
    fcn_s = QgsColorRampShader()
    fcn_s.setColorRampType(QgsColorRampShader.Interpolated)
    items_s = [
        QgsColorRampShader.ColorRampItem(0, QColor(43, 131, 186, 180), "0° - Datar"),
        QgsColorRampShader.ColorRampItem(8, QColor(171, 221, 164, 180), "8° - Landai"),
        QgsColorRampShader.ColorRampItem(15, QColor(254, 224, 139, 180), "15° - Agak Curam"),
        QgsColorRampShader.ColorRampItem(25, QColor(253, 174, 97, 180), "25° - Curam"),
        QgsColorRampShader.ColorRampItem(40, QColor(215, 25, 28, 180), "> 40° - Sangat Curam")
    ]
    fcn_s.setColorRampItemList(items_s)
    shader_s = QgsRasterShader()
    shader_s.setRasterShaderFunction(fcn_s)
    ps_s = QgsSingleBandPseudoColorRenderer(r_slope.dataProvider(), 1, shader_s)
    r_slope.setRenderer(ps_s)
    proj.addMapLayer(r_slope)

    # Hillshade
    r_hs = QgsRasterLayer(os.path.join(p2_dir, "hillshade_10m.tif"), "Hillshade DEM 10m")
    proj.addMapLayer(r_hs)

    # Copernicus DEM 10m
    r_dem = QgsRasterLayer(os.path.join(p2_dir, "copdem_10m.tif"), "Model Elevasi DEM 10m (mdpl)")
    fcn_d = QgsColorRampShader()
    fcn_d.setColorRampType(QgsColorRampShader.Interpolated)
    items_d = [
        QgsColorRampShader.ColorRampItem(300, QColor(43, 131, 186, 200), "300 mdpl (Lembah Hilir)"),
        QgsColorRampShader.ColorRampItem(380, QColor(171, 221, 164, 200), "380 mdpl"),
        QgsColorRampShader.ColorRampItem(460, QColor(254, 224, 139, 200), "460 mdpl"),
        QgsColorRampShader.ColorRampItem(540, QColor(253, 174, 97, 200), "540 mdpl"),
        QgsColorRampShader.ColorRampItem(620, QColor(215, 25, 28, 200), "620 mdpl (Puncak Hulu)")
    ]
    fcn_d.setColorRampItemList(items_d)
    shader_d = QgsRasterShader()
    shader_d.setRasterShaderFunction(fcn_d)
    ps_d = QgsSingleBandPseudoColorRenderer(r_dem.dataProvider(), 1, shader_d)
    r_dem.setRenderer(ps_d)
    proj.addMapLayer(r_dem)
    proj.layerTreeRoot().findLayer(r_dem.id()).setItemVisibilityChecked(False)

    # Sentinel-2 CIR
    r_cir = QgsRasterLayer(os.path.join(p2_dir, "sentinel2_l2a_20250721_10m.tif"), "Sentinel-2 Color Infrared (CIR 8-4-3)")
    renderer_cir = QgsMultiBandColorRenderer(r_cir.dataProvider(), 4, 3, 2)
    r_cir.setRenderer(renderer_cir)
    proj.addMapLayer(r_cir)
    proj.layerTreeRoot().findLayer(r_cir.id()).setItemVisibilityChecked(False)

    zoom_to_layer(v_batas)
    proj.setFileName(qgz_path)
    proj.write(qgz_path)
    print(f"Berhasil disimpan: {qgz_path}")

# =====================================================================
# PRAKTIK 3: DEMONSTRASI PSS
# =====================================================================
def buat_proyek_praktik_3():
    print("\n--- [3/5] Membuat Proyek Praktik 3: Demonstrasi PSS & Titik Spektral ---")
    p3_dir = os.path.join(DATA_DIR, "praktik-3")
    qgz_path = os.path.join(p3_dir, "Praktik_03_Demonstrasi_PSS.qgz")

    proj.clear()
    proj.setTitle("Praktik 03: Sebaran Titik Sampel Lapangan PSS & Ekstraksi Spektral")
    proj.setCrs(QgsCoordinateReferenceSystem("EPSG:32749"))

    # Titik Sampel Lapangan PSS
    v_pts = QgsVectorLayer(os.path.join(p3_dir, "titik_sampel_lapangan.gpkg"), "50 Titik Sampel Lapangan PSS", "ogr")
    sym_pt = QgsSimpleMarkerSymbolLayer()
    sym_pt.setShape(QgsSimpleMarkerSymbolLayer.Circle)
    sym_pt.setSize(4.0)
    sym_pt.setColor(QColor(255, 215, 0))
    sym_pt.setStrokeColor(QColor(0, 0, 0))
    sym_pt.setStrokeWidth(0.6)
    v_pts.renderer().symbol().changeSymbolLayer(0, sym_pt)
    proj.addMapLayer(v_pts)

    # Batas Sub-DAS
    v_batas = QgsVectorLayer(os.path.join(p3_dir, "batas_subdas.gpkg"), "Batas Sub-DAS Bompon", "ogr")
    sym_b = QgsSimpleLineSymbolLayer()
    sym_b.setColor(QColor(0, 0, 0))
    sym_b.setWidth(0.8)
    v_batas.renderer().symbol().changeSymbolLayer(0, sym_b)
    proj.addMapLayer(v_batas)

    # Sentinel-2 True Color
    r_s2 = QgsRasterLayer(os.path.join(p3_dir, "sentinel2_l2a_20250721_10m.tif"), "Sentinel-2 L2A (True Color RGB 4-3-2)")
    renderer_s2 = QgsMultiBandColorRenderer(r_s2.dataProvider(), 3, 2, 1)
    r_s2.setRenderer(renderer_s2)
    proj.addMapLayer(r_s2)

    zoom_to_layer(v_batas)
    proj.setFileName(qgz_path)
    proj.write(qgz_path)
    print(f"Berhasil disimpan: {qgz_path}")

# =====================================================================
# PRAKTIK 4: BARE SOIL DETECTION
# =====================================================================
def buat_proyek_praktik_4():
    print("\n--- [4/5] Membuat Proyek Praktik 4: Bare Soil Detection & Ekstraksi Tanah Terbuka ---")
    p4_dir = os.path.join(DATA_DIR, "praktik-4")
    qgz_path = os.path.join(p4_dir, "Praktik_04_Bare_Soil_Detection.qgz")

    proj.clear()
    proj.setTitle("Praktik 04: Bare Soil Detection & Ekstraksi Spektrum Tanah Terbuka Multitemporal")
    proj.setCrs(QgsCoordinateReferenceSystem("EPSG:32749"))

    # Batas Sub-DAS
    v_batas = QgsVectorLayer(os.path.join(p4_dir, "batas_subdas.gpkg"), "Batas Sub-DAS Bompon", "ogr")
    sym = QgsSimpleLineSymbolLayer()
    sym.setColor(QColor(0, 0, 0))
    sym.setWidth(0.8)
    v_batas.renderer().symbol().changeSymbolLayer(0, sym)
    proj.addMapLayer(v_batas)

    # Masker Tanah Terbuka 2024
    r_mask24 = QgsRasterLayer(os.path.join(p4_dir, "masker_tanah_terbuka_20240813.tif"), "Masker Tanah Terbuka Kemarau 2024 (Merah)")
    fcn_m24 = QgsColorRampShader()
    fcn_m24.setColorRampType(QgsColorRampShader.Exact)
    items_m24 = [
        QgsColorRampShader.ColorRampItem(0, QColor(0, 0, 0, 0), "Bukan Tanah"),
        QgsColorRampShader.ColorRampItem(1, QColor(255, 0, 0, 240), "Tanah Terbuka (Bare Soil)")
    ]
    fcn_m24.setColorRampItemList(items_m24)
    shader_m24 = QgsRasterShader()
    shader_m24.setRasterShaderFunction(fcn_m24)
    ps_m24 = QgsSingleBandPseudoColorRenderer(r_mask24.dataProvider(), 1, shader_m24)
    r_mask24.setRenderer(ps_m24)
    proj.addMapLayer(r_mask24)

    # Masker Tanah Terbuka 2025
    r_mask25 = QgsRasterLayer(os.path.join(p4_dir, "masker_tanah_terbuka_20250721.tif"), "Masker Tanah Terbuka Kemarau 2025 (Kuning)")
    fcn_m25 = QgsColorRampShader()
    fcn_m25.setColorRampType(QgsColorRampShader.Exact)
    items_m25 = [
        QgsColorRampShader.ColorRampItem(0, QColor(0, 0, 0, 0), "Bukan Tanah"),
        QgsColorRampShader.ColorRampItem(1, QColor(255, 255, 0, 240), "Tanah Terbuka (Bare Soil)")
    ]
    fcn_m25.setColorRampItemList(items_m25)
    shader_m25 = QgsRasterShader()
    shader_m25.setRasterShaderFunction(fcn_m25)
    ps_m25 = QgsSingleBandPseudoColorRenderer(r_mask25.dataProvider(), 1, shader_m25)
    r_mask25.setRenderer(ps_m25)
    proj.addMapLayer(r_mask25)
    proj.layerTreeRoot().findLayer(r_mask25.id()).setItemVisibilityChecked(False)

    # Barest Earth Composite
    r_barest = QgsRasterLayer(os.path.join(p4_dir, "barest_earth_bsi_composite.tif"), "Barest Earth BSI Composite (Max BSI)")
    proj.addMapLayer(r_barest)
    proj.layerTreeRoot().findLayer(r_barest.id()).setItemVisibilityChecked(False)

    # BSI 2024
    r_bsi24 = QgsRasterLayer(os.path.join(p4_dir, "bsi_20240813.tif"), "Bare Soil Index (BSI) Kemarau 2024")
    fcn_b = QgsColorRampShader()
    fcn_b.setColorRampType(QgsColorRampShader.Interpolated)
    items_b = [
        QgsColorRampShader.ColorRampItem(-0.5, QColor(0, 104, 55, 200), "-0.5 (Kanopi Rapat)"),
        QgsColorRampShader.ColorRampItem(-0.2, QColor(102, 189, 99, 200), "-0.2 (Vegetasi Sedang)"),
        QgsColorRampShader.ColorRampItem(0.0, QColor(254, 224, 139, 200), "0.0 (Batas Ambang)"),
        QgsColorRampShader.ColorRampItem(0.15, QColor(244, 109, 67, 220), "0.15 (Tanah Agak Terbuka)"),
        QgsColorRampShader.ColorRampItem(0.35, QColor(165, 0, 38, 240), "0.35 (Tanah Terbuka Murni)")
    ]
    fcn_b.setColorRampItemList(items_b)
    shader_b = QgsRasterShader()
    shader_b.setRasterShaderFunction(fcn_b)
    ps_b = QgsSingleBandPseudoColorRenderer(r_bsi24.dataProvider(), 1, shader_b)
    r_bsi24.setRenderer(ps_b)
    proj.addMapLayer(r_bsi24)

    # BSI 2025
    r_bsi25 = QgsRasterLayer(os.path.join(p4_dir, "bsi_20250721.tif"), "Bare Soil Index (BSI) Kemarau 2025")
    proj.addMapLayer(r_bsi25)
    proj.layerTreeRoot().findLayer(r_bsi25.id()).setItemVisibilityChecked(False)

    # NDVI 2024 & 2025
    r_ndvi24 = QgsRasterLayer(os.path.join(p4_dir, "ndvi_20240813.tif"), "NDVI Kemarau 2024")
    proj.addMapLayer(r_ndvi24)
    proj.layerTreeRoot().findLayer(r_ndvi24.id()).setItemVisibilityChecked(False)

    # Penggunaan Lahan
    v_lu = QgsVectorLayer(os.path.join(p4_dir, "penggunaan_lahan.gpkg"), "Penggunaan Lahan Rujukan", "ogr")
    proj.addMapLayer(v_lu)
    proj.layerTreeRoot().findLayer(v_lu.id()).setItemVisibilityChecked(False)

    # Sentinel-2 2024 True Color
    r_s2_24 = QgsRasterLayer(os.path.join(p4_dir, "sentinel2_l2a_20240813_10m.tif"), "Sentinel-2 L2A (13-08-2024 Kemarau)")
    renderer_s2_24 = QgsMultiBandColorRenderer(r_s2_24.dataProvider(), 3, 2, 1)
    r_s2_24.setRenderer(renderer_s2_24)
    proj.addMapLayer(r_s2_24)

    # Sentinel-2 2025 True Color
    r_s2_25 = QgsRasterLayer(os.path.join(p4_dir, "sentinel2_l2a_20250721_10m.tif"), "Sentinel-2 L2A (21-07-2025 Kemarau)")
    renderer_s2_25 = QgsMultiBandColorRenderer(r_s2_25.dataProvider(), 3, 2, 1)
    r_s2_25.setRenderer(renderer_s2_25)
    proj.addMapLayer(r_s2_25)
    proj.layerTreeRoot().findLayer(r_s2_25.id()).setItemVisibilityChecked(False)

    zoom_to_layer(v_batas)
    proj.setFileName(qgz_path)
    proj.write(qgz_path)
    print(f"Berhasil disimpan: {qgz_path}")

# =====================================================================
# PRAKTIK 5: MACHINE LEARNING DSM C-ORGANIK
# =====================================================================
def buat_proyek_praktik_5():
    print("\n--- [5/5] Membuat Proyek Praktik 5: Machine Learning DSM C-Organik ---")
    p5_dir = os.path.join(DATA_DIR, "praktik-5")
    qgz_path = os.path.join(p5_dir, "Praktik_05_Machine_Learning_DSM_C_Organik.qgz")

    proj.clear()
    proj.setTitle("Praktik 05: Machine Learning Digital Soil Mapping (DSM) C-Organik")
    proj.setCrs(QgsCoordinateReferenceSystem("EPSG:32749"))

    # Titik Graduated C-Organik
    v_pts = QgsVectorLayer(os.path.join(p5_dir, "titik_sampel_lapangan.gpkg"), "Kadar C-Organik Lapangan 0-20 cm (%)", "ogr")
    cfg = [
        (0.0, 0.6, QColor(254, 237, 222), 3.0, "< 0.6% (Sangat Rendah)"),
        (0.6, 0.85, QColor(253, 190, 133), 3.6, "0.6% - 0.85% (Rendah)"),
        (0.85, 1.1, QColor(253, 141, 60), 4.2, "0.85% - 1.1% (Sedang)"),
        (1.1, 1.3, QColor(230, 85, 13), 4.8, "1.1% - 1.3% (Tinggi)"),
        (1.3, 2.5, QColor(166, 54, 3), 5.6, "> 1.3% (Sangat Tinggi)")
    ]
    ranges = []
    for lower, upper, col, size, label in cfg:
        sym = QgsSymbol.defaultSymbol(v_pts.geometryType())
        sym.setColor(col)
        sym.setSize(size)
        sym.symbolLayer(0).setStrokeColor(QColor(0, 0, 0))
        sym.symbolLayer(0).setStrokeWidth(0.5)
        rng = QgsRendererRange(lower, upper, sym, label)
        ranges.append(rng)
        
    grad_renderer = QgsGraduatedSymbolRenderer("C_Organik_1", ranges)
    v_pts.setRenderer(grad_renderer)
    proj.addMapLayer(v_pts)

    # Batas Sub-DAS
    v_batas = QgsVectorLayer(os.path.join(p5_dir, "batas_subdas.gpkg"), "Batas Sub-DAS Bompon", "ogr")
    sym_b = QgsSimpleLineSymbolLayer()
    sym_b.setColor(QColor(0, 0, 0))
    sym_b.setWidth(0.9)
    v_batas.renderer().symbol().changeSymbolLayer(0, sym_b)
    proj.addMapLayer(v_batas)

    # Peta Prediksi C-Organik
    r_pred = QgsRasterLayer(os.path.join(p5_dir, "prediksi_corganik_0_20cm.tif"), "Prediksi Kadar C-Organik 0-20 cm (% SOC)")
    fcn_p = QgsColorRampShader()
    fcn_p.setColorRampType(QgsColorRampShader.Interpolated)
    items_p = [
        QgsColorRampShader.ColorRampItem(0.5, QColor(255, 255, 212), "0.50% - Sangat Rendah"),
        QgsColorRampShader.ColorRampItem(0.75, QColor(254, 217, 142), "0.75% - Rendah"),
        QgsColorRampShader.ColorRampItem(1.0, QColor(254, 153, 41), "1.00% - Sedang"),
        QgsColorRampShader.ColorRampItem(1.25, QColor(204, 76, 2), "1.25% - Tinggi"),
        QgsColorRampShader.ColorRampItem(1.5, QColor(102, 37, 6), "> 1.50% - Sangat Tinggi (Humus)")
    ]
    fcn_p.setColorRampItemList(items_p)
    shader_p = QgsRasterShader()
    shader_p.setRasterShaderFunction(fcn_p)
    ps_p = QgsSingleBandPseudoColorRenderer(r_pred.dataProvider(), 1, shader_p)
    r_pred.setRenderer(ps_p)
    proj.addMapLayer(r_pred)

    # Peta Ketidakpastian PI90 C-Organik
    r_pi90 = QgsRasterLayer(os.path.join(p5_dir, "ketidakpastian_pi90_corganik.tif"), "Ketidakpastian Lebar Interval Prediksi 90% (PI90 C-Organik)")
    fcn_u = QgsColorRampShader()
    fcn_u.setColorRampType(QgsColorRampShader.Interpolated)
    items_u = [
        QgsColorRampShader.ColorRampItem(0.5, QColor(252, 251, 253), "0.50% (Tinggi Keyakinan / Ketidakpastian Rendah)"),
        QgsColorRampShader.ColorRampItem(0.8, QColor(188, 189, 220), "0.80% (Keyakinan Sedang)"),
        QgsColorRampShader.ColorRampItem(1.1, QColor(128, 125, 186), "1.10% (Ketidakpastian Agak Tinggi)"),
        QgsColorRampShader.ColorRampItem(1.4, QColor(63, 0, 125), "1.40% (Ketidakpastian Sangat Tinggi)")
    ]
    fcn_u.setColorRampItemList(items_u)
    shader_u = QgsRasterShader()
    shader_u.setRasterShaderFunction(fcn_u)
    ps_u = QgsSingleBandPseudoColorRenderer(r_pi90.dataProvider(), 1, shader_u)
    r_pi90.setRenderer(ps_u)
    proj.addMapLayer(r_pi90)
    proj.layerTreeRoot().findLayer(r_pi90.id()).setItemVisibilityChecked(False)

    # Layer Kovariat Lingkungan
    kov_dir = os.path.join(p5_dir, "kovariat")
    kovariats = [
        ("sentinel1_sar_10m.tif", "Sentinel-1 RTC SAR (VH Polarisation)"),
        ("dem_10m.tif", "Copernicus DEM 10m (mdpl)"),
        ("slope_10m.tif", "Topographic Slope (Derajat)"),
        ("aspect_10m.tif", "Topographic Aspect (Derajat Azimuth)"),
        ("tpi_10m.tif", "Topographic Position Index (TPI)"),
        ("hillshade_10m.tif", "Hillshade 10m"),
        ("sentinel2_l2a_10m.tif", "Sentinel-2 Multispektral 10m"),
        ("penggunaan_lahan_10m.tif", "Penggunaan Lahan 10m")
    ]
    for k_file, k_name in kovariats:
        kp = os.path.join(kov_dir, k_file)
        if os.path.exists(kp):
            rk = QgsRasterLayer(kp, k_name)
            proj.addMapLayer(rk)
            proj.layerTreeRoot().findLayer(rk.id()).setItemVisibilityChecked(False)

    zoom_to_layer(v_batas)
    proj.setFileName(qgz_path)
    proj.write(qgz_path)
    print(f"Berhasil disimpan: {qgz_path}")

def main():
    clean_banners()
    try:
        buat_proyek_praktik_1()
        buat_proyek_praktik_2()
        buat_proyek_praktik_3()
        buat_proyek_praktik_4()
        buat_proyek_praktik_5()
        print("\n=== SEMUA 5 PROYEK QGIS BERHASIL DIBUAT DAN DISIMPAN! ===")
    except Exception as e:
        print(f"Error saat pembuatan proyek: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
    finally:
        QTimer.singleShot(1000, lambda: iface.actionExit().trigger())

main()
