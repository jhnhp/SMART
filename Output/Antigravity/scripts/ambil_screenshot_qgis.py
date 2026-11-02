"""
Skrip Otomasi Pengambilan Screenshot QGIS GUI untuk 5 Sesi Praktik Pelatihan SMART
Dijalankan via: qgis --code /home/jhn/Documents/Sayangku/Modul Junun/Output/scripts/ambil_screenshot_qgis.py
"""

import os
import sys
import time
from PyQt5.QtCore import QTimer, QSize, Qt
from PyQt5.QtGui import QColor
from qgis.core import (
    QgsProject,
    QgsRasterLayer,
    QgsVectorLayer,
    QgsCoordinateReferenceSystem,
    QgsRectangle,
    QgsColorRampShader,
    QgsRasterShader,
    QgsSingleBandPseudoColorRenderer,
    QgsMultiBandColorRenderer,
    QgsSingleBandGrayRenderer,
    QgsSimpleLineSymbolLayer,
    QgsSimpleFillSymbolLayer,
    QgsSimpleMarkerSymbolLayer,
    QgsSingleSymbolRenderer,
    QgsCategorizedSymbolRenderer,
    QgsRendererCategory,
    QgsSymbol
)
from qgis.utils import iface

BASE_DIR = "/home/jhn/Documents/Sayangku/Modul Junun"
SCREENSHOT_DIR = os.path.join(BASE_DIR, "Output/Pelatihan/screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

mw = iface.mainWindow()
mw.resize(1366, 820)

proj = QgsProject.instance()

def set_extent_bompon(canvas):
    # Extent Sub-DAS Bompon EPSG:32749
    rect = QgsRectangle(407000, 9161000, 409300, 9165200)
    canvas.setExtent(rect)
    canvas.refresh()

def step_praktik_1():
    print("[1/5] Menyiapkan Tampilan Praktik 1: Multi-source Data Fusion...")
    proj.clear()
    proj.setCrs(QgsCoordinateReferenceSystem("EPSG:32749"))
    
    # 1. Batas Sub-DAS
    v_batas = QgsVectorLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-1/batas_subdas.gpkg", "Batas Sub-DAS Bompon", "ogr")
    sym = QgsSimpleLineSymbolLayer()
    sym.setColor(QColor(220, 20, 60))
    sym.setWidth(0.8)
    v_batas.renderer().symbol().changeSymbolLayer(0, sym)
    proj.addMapLayer(v_batas)

    # 2. Sentinel-2 L2A True Color (RGB 4,3,2 -> Band 3,2,1)
    r_s2 = QgsRasterLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-1/sentinel2_l2a_20250721_10m.tif", "Sentinel-2 L2A (True Color RGB 4-3-2)")
    renderer_s2 = QgsMultiBandColorRenderer(r_s2.dataProvider(), 3, 2, 1)
    r_s2.setRenderer(renderer_s2)
    proj.addMapLayer(r_s2)

    # 3. Sentinel-1 SAR RTC (VH)
    r_sar = QgsRasterLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-1/sentinel1_rtc_20240830_10m.tif", "Sentinel-1 RTC SAR (C-band VH)")
    proj.addMapLayer(r_sar)
    proj.layerTreeRoot().findLayer(r_sar.id()).setItemVisibilityChecked(False)

    # 4. Copernicus DEM 30m
    r_dem = QgsRasterLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-1/copdem_glo30_30m.tif", "Copernicus DEM GLO-30")
    proj.addMapLayer(r_dem)
    proj.layerTreeRoot().findLayer(r_dem.id()).setItemVisibilityChecked(False)

    iface.mapCanvas().setDestinationCrs(QgsCoordinateReferenceSystem("EPSG:32749"))
    set_extent_bompon(iface.mapCanvas())
    
    QTimer.singleShot(1500, snap_p1_overview)

def snap_p1_overview():
    out = os.path.join(SCREENSHOT_DIR, "praktik_01_qgis_multisensor_overview.png")
    mw.grab().save(out, "PNG")
    print(f" -> Saved: {out}")
    
    # Beralih ke tampilan SAR
    root = proj.layerTreeRoot()
    for child in root.children():
        if "Sentinel-1" in child.name():
            child.setItemVisibilityChecked(True)
        elif "Sentinel-2" in child.name():
            child.setItemVisibilityChecked(False)
    iface.mapCanvas().refresh()
    QTimer.singleShot(1200, snap_p1_sar)

def snap_p1_sar():
    out = os.path.join(SCREENSHOT_DIR, "praktik_01_qgis_sar_radar.png")
    mw.grab().save(out, "PNG")
    print(f" -> Saved: {out}")
    step_praktik_2()

def step_praktik_2():
    print("[2/5] Menyiapkan Tampilan Praktik 2: Delineasi SMU...")
    proj.clear()
    
    # 1. Batas Sub-DAS
    v_batas = QgsVectorLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-2/batas_subdas.gpkg", "Batas Sub-DAS Bompon", "ogr")
    sym_b = QgsSimpleLineSymbolLayer()
    sym_b.setColor(QColor(0, 0, 0))
    sym_b.setWidth(0.9)
    v_batas.renderer().symbol().changeSymbolLayer(0, sym_b)
    proj.addMapLayer(v_batas)

    # 2. Hillshade
    r_hs = QgsRasterLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-2/hillshade_10m.tif", "Hillshade Copernicus DEM 10m")
    proj.addMapLayer(r_hs)

    # 3. Slope
    r_slope = QgsRasterLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-2/slope_10m.tif", "Peta Kelerengan (Derajat)")
    fcn = QgsColorRampShader()
    fcn.setColorRampType(QgsColorRampShader.Interpolated)
    items = [
        QgsColorRampShader.ColorRampItem(0, QColor(43, 131, 186, 180), "0° - Datar"),
        QgsColorRampShader.ColorRampItem(8, QColor(171, 221, 164, 180), "8° - Landai"),
        QgsColorRampShader.ColorRampItem(15, QColor(254, 224, 139, 180), "15° - Agak Curam"),
        QgsColorRampShader.ColorRampItem(25, QColor(253, 174, 97, 180), "25° - Curam"),
        QgsColorRampShader.ColorRampItem(40, QColor(215, 25, 28, 180), "> 40° - Sangat Curam")
    ]
    fcn.setColorRampItemList(items)
    shader = QgsRasterShader()
    shader.setRasterShaderFunction(fcn)
    ps_renderer = QgsSingleBandPseudoColorRenderer(r_slope.dataProvider(), 1, shader)
    r_slope.setRenderer(ps_renderer)
    proj.addMapLayer(r_slope)

    # 4. Bentuklahan Rujukan
    v_landform = QgsVectorLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-2/bentuklahan_rujukan.gpkg", "Satuan Bentuklahan Rujukan (SMU)", "ogr")
    sym_lf = QgsSimpleFillSymbolLayer()
    sym_lf.setStrokeColor(QColor(70, 130, 180))
    sym_lf.setStrokeWidth(0.6)
    sym_lf.setFillColor(QColor(70, 130, 180, 40))
    v_landform.renderer().symbol().changeSymbolLayer(0, sym_lf)
    proj.addMapLayer(v_landform)
    proj.layerTreeRoot().findLayer(v_landform.id()).setItemVisibilityChecked(False)

    set_extent_bompon(iface.mapCanvas())
    QTimer.singleShot(1500, snap_p2_slope)

def snap_p2_slope():
    out = os.path.join(SCREENSHOT_DIR, "praktik_02_qgis_slope_hillshade.png")
    mw.grab().save(out, "PNG")
    print(f" -> Saved: {out}")
    
    root = proj.layerTreeRoot()
    for child in root.children():
        if "Bentuklahan" in child.name():
            child.setItemVisibilityChecked(True)
        elif "Kelerengan" in child.name():
            child.setItemVisibilityChecked(False)
    iface.mapCanvas().refresh()
    QTimer.singleShot(1200, snap_p2_smu)

def snap_p2_smu():
    out = os.path.join(SCREENSHOT_DIR, "praktik_02_qgis_smu_landform.png")
    mw.grab().save(out, "PNG")
    print(f" -> Saved: {out}")
    step_praktik_3()

def step_praktik_3():
    print("[3/5] Menyiapkan Tampilan Praktik 3: Sebaran Titik Sampel Lapangan PSS...")
    proj.clear()

    # 1. Batas Sub-DAS
    v_batas = QgsVectorLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-5/batas_subdas.gpkg", "Batas Sub-DAS Bompon", "ogr")
    sym_b = QgsSimpleLineSymbolLayer()
    sym_b.setColor(QColor(0, 0, 0))
    sym_b.setWidth(0.8)
    v_batas.renderer().symbol().changeSymbolLayer(0, sym_b)
    proj.addMapLayer(v_batas)

    # 2. Sentinel-2 True Color
    r_s2 = QgsRasterLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-1/sentinel2_l2a_20250721_10m.tif", "Sentinel-2 L2A (True Color)")
    renderer_s2 = QgsMultiBandColorRenderer(r_s2.dataProvider(), 3, 2, 1)
    r_s2.setRenderer(renderer_s2)
    proj.addMapLayer(r_s2)

    # 3. 50 Titik Sampel
    v_pts = QgsVectorLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-5/titik_sampel_lapangan.gpkg", "50 Titik Sampel Tanah Lapangan", "ogr")
    sym_pt = QgsSimpleMarkerSymbolLayer()
    sym_pt.setShape(QgsSimpleMarkerSymbolLayer.Circle)
    sym_pt.setSize(3.8)
    sym_pt.setColor(QColor(255, 215, 0))
    sym_pt.setStrokeColor(QColor(0, 0, 0))
    sym_pt.setStrokeWidth(0.4)
    v_pts.renderer().symbol().changeSymbolLayer(0, sym_pt)
    proj.addMapLayer(v_pts)

    set_extent_bompon(iface.mapCanvas())
    QTimer.singleShot(1500, snap_p3_pts)

def snap_p3_pts():
    out = os.path.join(SCREENSHOT_DIR, "praktik_03_qgis_titik_sampel_pss.png")
    mw.grab().save(out, "PNG")
    print(f" -> Saved: {out}")
    step_praktik_4()

def step_praktik_4():
    print("[4/5] Menyiapkan Tampilan Praktik 4: Deteksi Tanah Terbuka (Bare Soil)...")
    proj.clear()

    # 1. Batas Sub-DAS
    v_batas = QgsVectorLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-4/batas_subdas.gpkg", "Batas Sub-DAS Bompon", "ogr")
    sym_b = QgsSimpleLineSymbolLayer()
    sym_b.setColor(QColor(0, 0, 0))
    sym_b.setWidth(0.8)
    v_batas.renderer().symbol().changeSymbolLayer(0, sym_b)
    proj.addMapLayer(v_batas)

    # 2. Sentinel-2 Kemarau 2024
    r_s2_24 = QgsRasterLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-4/sentinel2_l2a_20240813_10m.tif", "Sentinel-2 Puncak Kemarau (13-08-2024)")
    rend_s2_24 = QgsMultiBandColorRenderer(r_s2_24.dataProvider(), 3, 2, 1)
    r_s2_24.setRenderer(rend_s2_24)
    proj.addMapLayer(r_s2_24)

    # 3. Masker Tanah Terbuka
    r_mask = QgsRasterLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-4/masker_tanah_terbuka_20240813.tif", "Masker Tanah Terbuka (Merah)")
    fcn_m = QgsColorRampShader()
    fcn_m.setColorRampType(QgsColorRampShader.Exact)
    items_m = [
        QgsColorRampShader.ColorRampItem(0, QColor(0, 0, 0, 0), "Bukan Tanah (Transparan)"),
        QgsColorRampShader.ColorRampItem(1, QColor(255, 0, 0, 230), "Tanah Terbuka (Bare Soil)")
    ]
    fcn_m.setColorRampItemList(items_m)
    shader_m = QgsRasterShader()
    shader_m.setRasterShaderFunction(fcn_m)
    ps_rend_m = QgsSingleBandPseudoColorRenderer(r_mask.dataProvider(), 1, shader_m)
    r_mask.setRenderer(ps_rend_m)
    proj.addMapLayer(r_mask)

    set_extent_bompon(iface.mapCanvas())
    QTimer.singleShot(1500, snap_p4_mask)

def snap_p4_mask():
    out = os.path.join(SCREENSHOT_DIR, "praktik_04_qgis_masker_tanah_terbuka.png")
    mw.grab().save(out, "PNG")
    print(f" -> Saved: {out}")
    step_praktik_5()

def step_praktik_5():
    print("[5/5] Menyiapkan Tampilan Praktik 5: Peta Prediksi DSM & Ketidakpastian PI90...")
    proj.clear()

    # 1. Batas Sub-DAS
    v_batas = QgsVectorLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-5/batas_subdas.gpkg", "Batas Sub-DAS Bompon", "ogr")
    sym_b = QgsSimpleLineSymbolLayer()
    sym_b.setColor(QColor(0, 0, 0))
    sym_b.setWidth(0.9)
    v_batas.renderer().symbol().changeSymbolLayer(0, sym_b)
    proj.addMapLayer(v_batas)

    # 2. Titik Sampel
    v_pts = QgsVectorLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-5/titik_sampel_lapangan.gpkg", "50 Titik Sampel Lapangan", "ogr")
    sym_pt = QgsSimpleMarkerSymbolLayer()
    sym_pt.setShape(QgsSimpleMarkerSymbolLayer.Circle)
    sym_pt.setSize(3.2)
    sym_pt.setColor(QColor(50, 50, 50))
    sym_pt.setStrokeColor(QColor(255, 255, 255))
    sym_pt.setStrokeWidth(0.5)
    v_pts.renderer().symbol().changeSymbolLayer(0, sym_pt)
    proj.addMapLayer(v_pts)

    # 3. Peta Prediksi Lempung
    r_pred = QgsRasterLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-5/prediksi_lempung_0_20cm.tif", "Prediksi Kadar Lempung 0-20cm (%)")
    fcn_p = QgsColorRampShader()
    fcn_p.setColorRampType(QgsColorRampShader.Interpolated)
    items_p = [
        QgsColorRampShader.ColorRampItem(45, QColor(255, 255, 212), "45% - Rendah"),
        QgsColorRampShader.ColorRampItem(55, QColor(254, 217, 142), "55%"),
        QgsColorRampShader.ColorRampItem(65, QColor(254, 153, 41), "65%"),
        QgsColorRampShader.ColorRampItem(75, QColor(204, 76, 2), "75% - Tinggi")
    ]
    fcn_p.setColorRampItemList(items_p)
    shader_p = QgsRasterShader()
    shader_p.setRasterShaderFunction(fcn_p)
    ps_rend_p = QgsSingleBandPseudoColorRenderer(r_pred.dataProvider(), 1, shader_p)
    r_pred.setRenderer(ps_rend_p)
    proj.addMapLayer(r_pred)

    # 4. Peta Ketidakpastian PI90
    r_unc = QgsRasterLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-5/ketidakpastian_pi90_lempung.tif", "Ketidakpastian Prediksi (PI90 Width %)")
    fcn_u = QgsColorRampShader()
    fcn_u.setColorRampType(QgsColorRampShader.Interpolated)
    items_u = [
        QgsColorRampShader.ColorRampItem(0, QColor(254, 229, 217), "0% - Sangat Pasti"),
        QgsColorRampShader.ColorRampItem(10, QColor(252, 174, 145), "10%"),
        QgsColorRampShader.ColorRampItem(20, QColor(251, 106, 74), "20%"),
        QgsColorRampShader.ColorRampItem(35, QColor(165, 15, 21), "35% - Ketidakpastian Tinggi")
    ]
    fcn_u.setColorRampItemList(items_u)
    shader_u = QgsRasterShader()
    shader_u.setRasterShaderFunction(fcn_u)
    ps_rend_u = QgsSingleBandPseudoColorRenderer(r_unc.dataProvider(), 1, shader_u)
    r_unc.setRenderer(ps_rend_u)
    proj.addMapLayer(r_unc)
    proj.layerTreeRoot().findLayer(r_unc.id()).setItemVisibilityChecked(False)

    set_extent_bompon(iface.mapCanvas())
    QTimer.singleShot(1500, snap_p5_pred)

def snap_p5_pred():
    out = os.path.join(SCREENSHOT_DIR, "praktik_05_qgis_prediksi_lempung.png")
    mw.grab().save(out, "PNG")
    print(f" -> Saved: {out}")
    
    root = proj.layerTreeRoot()
    for child in root.children():
        if "Ketidakpastian" in child.name():
            child.setItemVisibilityChecked(True)
        elif "Prediksi" in child.name():
            child.setItemVisibilityChecked(False)
    iface.mapCanvas().refresh()
    QTimer.singleShot(1200, snap_p5_unc)

def snap_p5_unc():
    out = os.path.join(SCREENSHOT_DIR, "praktik_05_qgis_ketidakpastian_pi90.png")
    mw.grab().save(out, "PNG")
    print(f" -> Saved: {out}")
    print("=== SELURUH SCREENSHOT QGIS BERHASIL DIAMBIL LENGKAP! ===")
    QTimer.singleShot(500, iface.actionExit().trigger)

# Mulai urutan eksekusi setelah QGIS siap
QTimer.singleShot(2500, step_praktik_1)
