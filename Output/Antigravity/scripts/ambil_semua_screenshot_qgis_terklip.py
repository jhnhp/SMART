"""
Skrip Otomasi Pengambilan Seluruh Screenshot QGIS GUI untuk 5 Sesi Praktik Pelatihan SMART
- Seluruh layer terpotong rapi (clipped) mengikuti batas poligon Sub-DAS Bompon.
- Seluruh message bar/banner python error ditutup dan dibersihkan sebelum capture.
Dijalankan via: qgis --code /home/jhn/Documents/Sayangku/Modul Junun/Output/scripts/ambil_semua_screenshot_qgis_terklip.py
"""

import os
import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget
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
    QgsSimpleLineSymbolLayer,
    QgsSimpleFillSymbolLayer,
    QgsSimpleMarkerSymbolLayer,
    QgsGraduatedSymbolRenderer,
    QgsRendererRange,
    QgsSymbol
)
from qgis.gui import QgsMessageBar
from qgis.utils import iface

BASE_DIR = "/home/jhn/Documents/Sayangku/Modul Junun"
SCREENSHOT_DIR = os.path.join(BASE_DIR, "Output/Pelatihan/screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

mw = iface.mainWindow()
mw.resize(1366, 850)

proj = QgsProject.instance()

def clean_banners():
    try:
        iface.messageBar().clearWidgets()
        for bar in mw.findChildren(QgsMessageBar):
            bar.clearWidgets()
            bar.hide()
    except Exception as e:
        pass

def zoom_to_bompon(canvas, v_layer):
    clean_banners()
    ext = v_layer.extent()
    ext.scale(1.10)
    canvas.setExtent(ext)
    canvas.refresh()

def safe_grab(out_path):
    clean_banners()
    mw.grab().save(out_path, "PNG")
    print(f" -> Saved: {out_path}")

# =====================================================================
# PRAKTIK 1: MULTI-SOURCE DATA FUSION
# =====================================================================
def step_p1_multisensor():
    print("[1/12] Praktik 1: Multi-source Overview (Clipped & Clean)...")
    proj.clear()
    proj.setCrs(QgsCoordinateReferenceSystem("EPSG:32749"))

    v_batas = QgsVectorLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-1/batas_subdas.gpkg", "Batas Sub-DAS Bompon", "ogr")
    sym = QgsSimpleLineSymbolLayer()
    sym.setColor(QColor(220, 20, 60))
    sym.setWidth(0.8)
    v_batas.renderer().symbol().changeSymbolLayer(0, sym)
    proj.addMapLayer(v_batas)

    r_s2 = QgsRasterLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-1/sentinel2_l2a_20250721_10m.tif", "Sentinel-2 L2A (True Color RGB 4-3-2)")
    renderer_s2 = QgsMultiBandColorRenderer(r_s2.dataProvider(), 3, 2, 1)
    r_s2.setRenderer(renderer_s2)
    proj.addMapLayer(r_s2)

    r_sar = QgsRasterLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-1/sentinel1_rtc_20240830_10m.tif", "Sentinel-1 RTC SAR (C-band VH)")
    proj.addMapLayer(r_sar)
    proj.layerTreeRoot().findLayer(r_sar.id()).setItemVisibilityChecked(False)

    zoom_to_bompon(iface.mapCanvas(), v_batas)
    QTimer.singleShot(1500, snap_p1_overview)

def snap_p1_overview():
    safe_grab(os.path.join(SCREENSHOT_DIR, "praktik_01_qgis_multisensor_overview.png"))
    step_p1_sar()

def step_p1_sar():
    print("[2/12] Praktik 1: Sentinel-1 SAR Radar (Clipped & Clean)...")
    clean_banners()
    root = proj.layerTreeRoot()
    for child in root.children():
        if "Sentinel-1" in child.name():
            child.setItemVisibilityChecked(True)
        elif "Sentinel-2" in child.name():
            child.setItemVisibilityChecked(False)
    iface.mapCanvas().refresh()
    QTimer.singleShot(1200, snap_p1_sar_out)

def snap_p1_sar_out():
    safe_grab(os.path.join(SCREENSHOT_DIR, "praktik_01_qgis_sar_radar.png"))
    step_p1_dem()

def step_p1_dem():
    print("[3/12] Praktik 1: DEM Elevation (Clipped & Clean)...")
    proj.clear()

    v_batas = QgsVectorLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-1/batas_subdas.gpkg", "Batas Sub-DAS Bompon", "ogr")
    sym = QgsSimpleLineSymbolLayer()
    sym.setColor(QColor(0, 0, 0))
    sym.setWidth(0.8)
    v_batas.renderer().symbol().changeSymbolLayer(0, sym)
    proj.addMapLayer(v_batas)

    r_hs = QgsRasterLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-2/hillshade_10m.tif", "Hillshade DEM 10m")
    proj.addMapLayer(r_hs)

    r_dem = QgsRasterLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-2/copdem_10m.tif", "Model Elevasi DEM 10m (mdpl)")
    fcn = QgsColorRampShader()
    fcn.setColorRampType(QgsColorRampShader.Interpolated)
    items = [
        QgsColorRampShader.ColorRampItem(300, QColor(43, 131, 186, 200), "300 mdpl (Lembah Hilir)"),
        QgsColorRampShader.ColorRampItem(380, QColor(171, 221, 164, 200), "380 mdpl"),
        QgsColorRampShader.ColorRampItem(460, QColor(254, 224, 139, 200), "460 mdpl"),
        QgsColorRampShader.ColorRampItem(540, QColor(253, 174, 97, 200), "540 mdpl"),
        QgsColorRampShader.ColorRampItem(620, QColor(215, 25, 28, 200), "620 mdpl (Puncak Hulu)")
    ]
    fcn.setColorRampItemList(items)
    shader = QgsRasterShader()
    shader.setRasterShaderFunction(fcn)
    ps_renderer = QgsSingleBandPseudoColorRenderer(r_dem.dataProvider(), 1, shader)
    r_dem.setRenderer(ps_renderer)
    proj.addMapLayer(r_dem)

    zoom_to_bompon(iface.mapCanvas(), v_batas)
    QTimer.singleShot(1500, snap_p1_dem_out)

def snap_p1_dem_out():
    safe_grab(os.path.join(SCREENSHOT_DIR, "praktik_01_qgis_dem_elevation.png"))
    step_p2_slope()

# =====================================================================
# PRAKTIK 2: DELINEASI SMU
# =====================================================================
def step_p2_slope():
    print("[4/12] Praktik 2: Slope & Hillshade (Clipped & Clean)...")
    proj.clear()

    v_batas = QgsVectorLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-2/batas_subdas.gpkg", "Batas Sub-DAS Bompon", "ogr")
    sym_b = QgsSimpleLineSymbolLayer()
    sym_b.setColor(QColor(0, 0, 0))
    sym_b.setWidth(0.9)
    v_batas.renderer().symbol().changeSymbolLayer(0, sym_b)
    proj.addMapLayer(v_batas)

    r_hs = QgsRasterLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-2/hillshade_10m.tif", "Hillshade Copernicus DEM 10m")
    proj.addMapLayer(r_hs)

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

    zoom_to_bompon(iface.mapCanvas(), v_batas)
    QTimer.singleShot(1500, snap_p2_slope_out)

def snap_p2_slope_out():
    safe_grab(os.path.join(SCREENSHOT_DIR, "praktik_02_qgis_slope_hillshade.png"))
    step_p2_cir()

def step_p2_cir():
    print("[5/12] Praktik 2: Color Infrared CIR (Clipped & Clean)...")
    proj.clear()

    v_batas = QgsVectorLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-2/batas_subdas.gpkg", "Batas Sub-DAS Bompon", "ogr")
    sym = QgsSimpleLineSymbolLayer()
    sym.setColor(QColor(255, 255, 0))
    sym.setWidth(0.8)
    v_batas.renderer().symbol().changeSymbolLayer(0, sym)
    proj.addMapLayer(v_batas)

    r_s2 = QgsRasterLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-2/sentinel2_l2a_20250721_10m.tif", "Sentinel-2 Color Infrared (CIR 8-4-3)")
    renderer_cir = QgsMultiBandColorRenderer(r_s2.dataProvider(), 7, 3, 2)
    r_s2.setRenderer(renderer_cir)
    proj.addMapLayer(r_s2)

    zoom_to_bompon(iface.mapCanvas(), v_batas)
    QTimer.singleShot(1500, snap_p2_cir_out)

def snap_p2_cir_out():
    safe_grab(os.path.join(SCREENSHOT_DIR, "praktik_02_qgis_cir_composite.png"))
    step_p2_smu()

def step_p2_smu():
    print("[6/12] Praktik 2: SMU Landform (Clipped & Clean)...")
    proj.clear()

    v_batas = QgsVectorLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-2/batas_subdas.gpkg", "Batas Sub-DAS Bompon", "ogr")
    sym_b = QgsSimpleLineSymbolLayer()
    sym_b.setColor(QColor(0, 0, 0))
    sym_b.setWidth(0.9)
    v_batas.renderer().symbol().changeSymbolLayer(0, sym_b)
    proj.addMapLayer(v_batas)

    r_hs = QgsRasterLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-2/hillshade_10m.tif", "Hillshade Copernicus DEM 10m")
    proj.addMapLayer(r_hs)

    v_landform = QgsVectorLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-2/bentuklahan_rujukan.gpkg", "Satuan Bentuklahan Rujukan (SMU)", "ogr")
    sym_lf = QgsSimpleFillSymbolLayer()
    sym_lf.setStrokeColor(QColor(70, 130, 180))
    sym_lf.setStrokeWidth(0.6)
    sym_lf.setFillColor(QColor(70, 130, 180, 50))
    v_landform.renderer().symbol().changeSymbolLayer(0, sym_lf)
    proj.addMapLayer(v_landform)

    zoom_to_bompon(iface.mapCanvas(), v_batas)
    QTimer.singleShot(1500, snap_p2_smu_out)

def snap_p2_smu_out():
    safe_grab(os.path.join(SCREENSHOT_DIR, "praktik_02_qgis_smu_landform.png"))
    step_p3_pts()

# =====================================================================
# PRAKTIK 3: TITIK SAMPEL PSS
# =====================================================================
def step_p3_pts():
    print("[7/12] Praktik 3: Titik Sampel Lapangan PSS (Clean)...")
    proj.clear()

    v_batas = QgsVectorLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-5/batas_subdas.gpkg", "Batas Sub-DAS Bompon", "ogr")
    sym_b = QgsSimpleLineSymbolLayer()
    sym_b.setColor(QColor(0, 0, 0))
    sym_b.setWidth(0.8)
    v_batas.renderer().symbol().changeSymbolLayer(0, sym_b)
    proj.addMapLayer(v_batas)

    r_s2 = QgsRasterLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-1/sentinel2_l2a_20250721_10m.tif", "Sentinel-2 L2A (True Color)")
    renderer_s2 = QgsMultiBandColorRenderer(r_s2.dataProvider(), 3, 2, 1)
    r_s2.setRenderer(renderer_s2)
    proj.addMapLayer(r_s2)

    v_pts = QgsVectorLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-5/titik_sampel_lapangan.gpkg", "50 Titik Sampel Lapangan PSS", "ogr")
    sym_pt = QgsSimpleMarkerSymbolLayer()
    sym_pt.setShape(QgsSimpleMarkerSymbolLayer.Circle)
    sym_pt.setSize(3.8)
    sym_pt.setColor(QColor(255, 215, 0))
    sym_pt.setStrokeColor(QColor(0, 0, 0))
    sym_pt.setStrokeWidth(0.5)
    v_pts.renderer().symbol().changeSymbolLayer(0, sym_pt)
    proj.addMapLayer(v_pts)

    zoom_to_bompon(iface.mapCanvas(), v_batas)
    QTimer.singleShot(1500, snap_p3_pts_out)

def snap_p3_pts_out():
    safe_grab(os.path.join(SCREENSHOT_DIR, "praktik_03_qgis_titik_sampel_pss.png"))
    step_p4_bsi()

# =====================================================================
# PRAKTIK 4: BARE SOIL DETECTION & EXTRACTION
# =====================================================================
def step_p4_bsi():
    print("[8/12] Praktik 4: Bare Soil Index Map (Clipped & Clean)...")
    proj.clear()

    v_batas = QgsVectorLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-4/batas_subdas.gpkg", "Batas Sub-DAS Bompon", "ogr")
    sym = QgsSimpleLineSymbolLayer()
    sym.setColor(QColor(0, 0, 0))
    sym.setWidth(0.8)
    v_batas.renderer().symbol().changeSymbolLayer(0, sym)
    proj.addMapLayer(v_batas)

    r_bsi = QgsRasterLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-4/bsi_20240813.tif", "Bare Soil Index Kemarau 2024 (BSI)")
    fcn_b = QgsColorRampShader()
    fcn_b.setColorRampType(QgsColorRampShader.Interpolated)
    items_b = [
        QgsColorRampShader.ColorRampItem(-0.5, QColor(0, 104, 55, 200), "-0.5 (Kanopi Vegetasi Rapat)"),
        QgsColorRampShader.ColorRampItem(-0.2, QColor(102, 189, 99, 200), "-0.2 (Vegetasi Sedang)"),
        QgsColorRampShader.ColorRampItem(0.0, QColor(254, 224, 139, 200), "0.0 (Batas Transisi)"),
        QgsColorRampShader.ColorRampItem(0.15, QColor(244, 109, 67, 220), "0.15 (Tanah Agak Terbuka)"),
        QgsColorRampShader.ColorRampItem(0.35, QColor(165, 0, 38, 240), "0.35 (Tanah Terbuka Murni)")
    ]
    fcn_b.setColorRampItemList(items_b)
    shader_b = QgsRasterShader()
    shader_b.setRasterShaderFunction(fcn_b)
    ps_rend_b = QgsSingleBandPseudoColorRenderer(r_bsi.dataProvider(), 1, shader_b)
    r_bsi.setRenderer(ps_rend_b)
    proj.addMapLayer(r_bsi)

    zoom_to_bompon(iface.mapCanvas(), v_batas)
    QTimer.singleShot(1500, snap_p4_bsi_out)

def snap_p4_bsi_out():
    safe_grab(os.path.join(SCREENSHOT_DIR, "praktik_04_qgis_bsi_map.png"))
    step_p4_mask()

def step_p4_mask():
    print("[9/12] Praktik 4: Masker Tanah Terbuka (Clipped & Clean)...")
    proj.clear()

    v_batas = QgsVectorLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-4/batas_subdas.gpkg", "Batas Sub-DAS Bompon", "ogr")
    sym_b = QgsSimpleLineSymbolLayer()
    sym_b.setColor(QColor(0, 0, 0))
    sym_b.setWidth(0.8)
    v_batas.renderer().symbol().changeSymbolLayer(0, sym_b)
    proj.addMapLayer(v_batas)

    r_s2_24 = QgsRasterLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-4/sentinel2_l2a_20240813_10m.tif", "Sentinel-2 Puncak Kemarau (13-08-2024)")
    rend_s2_24 = QgsMultiBandColorRenderer(r_s2_24.dataProvider(), 3, 2, 1)
    r_s2_24.setRenderer(rend_s2_24)
    proj.addMapLayer(r_s2_24)

    r_mask = QgsRasterLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-4/masker_tanah_terbuka_20240813.tif", "Masker Tanah Terbuka (Merah)")
    fcn_m = QgsColorRampShader()
    fcn_m.setColorRampType(QgsColorRampShader.Exact)
    items_m = [
        QgsColorRampShader.ColorRampItem(0, QColor(0, 0, 0, 0), "Bukan Tanah (Transparan)"),
        QgsColorRampShader.ColorRampItem(1, QColor(255, 0, 0, 240), "Tanah Terbuka (Bare Soil)")
    ]
    fcn_m.setColorRampItemList(items_m)
    shader_m = QgsRasterShader()
    shader_m.setRasterShaderFunction(fcn_m)
    ps_rend_m = QgsSingleBandPseudoColorRenderer(r_mask.dataProvider(), 1, shader_m)
    r_mask.setRenderer(ps_rend_m)
    proj.addMapLayer(r_mask)

    zoom_to_bompon(iface.mapCanvas(), v_batas)
    QTimer.singleShot(1500, snap_p4_mask_out)

def snap_p4_mask_out():
    safe_grab(os.path.join(SCREENSHOT_DIR, "praktik_04_qgis_masker_tanah_terbuka.png"))
    step_p5_pts()

# =====================================================================
# PRAKTIK 5: MACHINE LEARNING DSM
# =====================================================================
def step_p5_pts():
    print("[10/12] Praktik 5: Titik Graduated Lempung (Clean)...")
    proj.clear()

    v_batas = QgsVectorLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-5/batas_subdas.gpkg", "Batas Sub-DAS Bompon", "ogr")
    sym_b = QgsSimpleLineSymbolLayer()
    sym_b.setColor(QColor(0, 0, 0))
    sym_b.setWidth(0.8)
    v_batas.renderer().symbol().changeSymbolLayer(0, sym_b)
    proj.addMapLayer(v_batas)

    r_s2 = QgsRasterLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-1/sentinel2_l2a_20250721_10m.tif", "Sentinel-2 L2A (True Color)")
    renderer_s2 = QgsMultiBandColorRenderer(r_s2.dataProvider(), 3, 2, 1)
    r_s2.setRenderer(renderer_s2)
    proj.addMapLayer(r_s2)

    v_pts = QgsVectorLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-5/titik_sampel_lapangan.gpkg", "Kadar Lempung Lab (%) Lapisan 0-20 cm", "ogr")
    
    cfg = [
        (30.0, 50.0, QColor(255, 255, 178), 2.5, "35% - 50% (Lempung Rendah)"),
        (50.0, 60.0, QColor(254, 204, 92), 3.2, "50% - 60%"),
        (60.0, 68.0, QColor(253, 141, 60), 3.8, "60% - 68%"),
        (68.0, 74.0, QColor(240, 59, 32), 4.4, "68% - 74%"),
        (74.0, 85.0, QColor(189, 0, 38), 5.2, "> 74% (Lempung Sangat Tinggi)")
    ]
    ranges = []
    for lower, upper, col, size, label in cfg:
        sym = QgsSymbol.defaultSymbol(v_pts.geometryType())
        sym.setColor(col)
        sym.setSize(size)
        sym.symbolLayer(0).setStrokeColor(QColor(0, 0, 0))
        sym.symbolLayer(0).setStrokeWidth(0.4)
        rng = QgsRendererRange(lower, upper, sym, label)
        ranges.append(rng)
        
    grad_renderer = QgsGraduatedSymbolRenderer("Lempung_1", ranges)
    v_pts.setRenderer(grad_renderer)
    proj.addMapLayer(v_pts)

    zoom_to_bompon(iface.mapCanvas(), v_batas)
    QTimer.singleShot(1500, snap_p5_pts_out)

def snap_p5_pts_out():
    safe_grab(os.path.join(SCREENSHOT_DIR, "praktik_05_qgis_titik_graduated_lempung.png"))
    step_p5_pred()

def step_p5_pred():
    print("[11/12] Praktik 5: Peta Prediksi Lempung (Clipped & Clean)...")
    proj.clear()

    v_batas = QgsVectorLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-5/batas_subdas.gpkg", "Batas Sub-DAS Bompon", "ogr")
    sym_b = QgsSimpleLineSymbolLayer()
    sym_b.setColor(QColor(0, 0, 0))
    sym_b.setWidth(0.9)
    v_batas.renderer().symbol().changeSymbolLayer(0, sym_b)
    proj.addMapLayer(v_batas)

    v_pts = QgsVectorLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-5/titik_sampel_lapangan.gpkg", "50 Titik Sampel Lapangan", "ogr")
    sym_pt = QgsSimpleMarkerSymbolLayer()
    sym_pt.setShape(QgsSimpleMarkerSymbolLayer.Circle)
    sym_pt.setSize(3.2)
    sym_pt.setColor(QColor(50, 50, 50))
    sym_pt.setStrokeColor(QColor(255, 255, 255))
    sym_pt.setStrokeWidth(0.5)
    v_pts.renderer().symbol().changeSymbolLayer(0, sym_pt)
    proj.addMapLayer(v_pts)

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

    zoom_to_bompon(iface.mapCanvas(), v_batas)
    QTimer.singleShot(1500, snap_p5_pred_out)

def snap_p5_pred_out():
    safe_grab(os.path.join(SCREENSHOT_DIR, "praktik_05_qgis_prediksi_lempung.png"))
    step_p5_unc()

def step_p5_unc():
    print("[12/12] Praktik 5: Peta Ketidakpastian PI90 (Clipped & Clean)...")
    proj.clear()

    v_batas = QgsVectorLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-5/batas_subdas.gpkg", "Batas Sub-DAS Bompon", "ogr")
    sym_b = QgsSimpleLineSymbolLayer()
    sym_b.setColor(QColor(0, 0, 0))
    sym_b.setWidth(0.9)
    v_batas.renderer().symbol().changeSymbolLayer(0, sym_b)
    proj.addMapLayer(v_batas)

    v_pts = QgsVectorLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-5/titik_sampel_lapangan.gpkg", "50 Titik Sampel Lapangan", "ogr")
    sym_pt = QgsSimpleMarkerSymbolLayer()
    sym_pt.setShape(QgsSimpleMarkerSymbolLayer.Circle)
    sym_pt.setSize(3.2)
    sym_pt.setColor(QColor(50, 50, 50))
    sym_pt.setStrokeColor(QColor(255, 255, 255))
    sym_pt.setStrokeWidth(0.5)
    v_pts.renderer().symbol().changeSymbolLayer(0, sym_pt)
    proj.addMapLayer(v_pts)

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

    zoom_to_bompon(iface.mapCanvas(), v_batas)
    QTimer.singleShot(1500, snap_p5_unc_out)

def snap_p5_unc_out():
    safe_grab(os.path.join(SCREENSHOT_DIR, "praktik_05_qgis_ketidakpastian_pi90.png"))
    print("=== SELURUH SCREENSHOT BERHASIL DIAMBIL BERSIH 100%! ===")
    QTimer.singleShot(500, iface.actionExit().trigger)

# Mulai pipeline setelah GUI siap
QTimer.singleShot(2500, step_p1_multisensor)
