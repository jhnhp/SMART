"""
Skrip Otomasi Pengambilan Screenshot Tambahan QGIS GUI untuk 5 Sesi Praktik Pelatihan SMART
Dijalankan via: qgis --code /home/jhn/Documents/Sayangku/Modul Junun/Output/scripts/ambil_screenshot_qgis_tambahan.py
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
    QgsRectangle,
    QgsColorRampShader,
    QgsRasterShader,
    QgsSingleBandPseudoColorRenderer,
    QgsMultiBandColorRenderer,
    QgsSimpleLineSymbolLayer,
    QgsSimpleFillSymbolLayer,
    QgsSimpleMarkerSymbolLayer,
    QgsSingleSymbolRenderer,
    QgsGraduatedSymbolRenderer,
    QgsRendererRange,
    QgsSymbol
)
from qgis.utils import iface

BASE_DIR = "/home/jhn/Documents/Sayangku/Modul Junun"
SCREENSHOT_DIR = os.path.join(BASE_DIR, "Output/Pelatihan/screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

mw = iface.mainWindow()
mw.resize(1366, 850)

proj = QgsProject.instance()

def set_extent_bompon(canvas):
    rect = QgsRectangle(407000, 9161000, 409300, 9165200)
    canvas.setExtent(rect)
    canvas.refresh()

# --- TAHAP 1: DEM Elevation Map ---
def step_dem_elevation():
    print("[1/5] Menyiapkan Tampilan DEM Elevation Map...")
    proj.clear()
    proj.setCrs(QgsCoordinateReferenceSystem("EPSG:32749"))

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
        QgsColorRampShader.ColorRampItem(300, QColor(43, 131, 186, 180), "300 mdpl (Lembah Hilir)"),
        QgsColorRampShader.ColorRampItem(380, QColor(171, 221, 164, 180), "380 mdpl"),
        QgsColorRampShader.ColorRampItem(460, QColor(254, 224, 139, 180), "460 mdpl"),
        QgsColorRampShader.ColorRampItem(540, QColor(253, 174, 97, 180), "540 mdpl"),
        QgsColorRampShader.ColorRampItem(620, QColor(215, 25, 28, 180), "620 mdpl (Puncak Hulu)")
    ]
    fcn.setColorRampItemList(items)
    shader = QgsRasterShader()
    shader.setRasterShaderFunction(fcn)
    ps_renderer = QgsSingleBandPseudoColorRenderer(r_dem.dataProvider(), 1, shader)
    r_dem.setRenderer(ps_renderer)
    proj.addMapLayer(r_dem)

    set_extent_bompon(iface.mapCanvas())
    QTimer.singleShot(1500, snap_dem_elevation)

def snap_dem_elevation():
    out = os.path.join(SCREENSHOT_DIR, "praktik_01_qgis_dem_elevation.png")
    mw.grab().save(out, "PNG")
    print(f" -> Saved: {out}")
    step_cir_composite()

# --- TAHAP 2: Color Infrared (CIR 8-4-3) ---
def step_cir_composite():
    print("[2/5] Menyiapkan Tampilan Color Infrared (CIR RGB 8-4-3)...")
    proj.clear()

    v_batas = QgsVectorLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-2/batas_subdas.gpkg", "Batas Sub-DAS Bompon", "ogr")
    sym = QgsSimpleLineSymbolLayer()
    sym.setColor(QColor(255, 255, 0)) # Kuning tegas di atas CIR
    sym.setWidth(0.8)
    v_batas.renderer().symbol().changeSymbolLayer(0, sym)
    proj.addMapLayer(v_batas)

    r_s2 = QgsRasterLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-2/sentinel2_l2a_20250721_10m.tif", "Sentinel-2 Color Infrared (CIR 8-4-3)")
    # Band 7 = B08 (NIR), Band 3 = B04 (Red), Band 2 = B03 (Green)
    renderer_cir = QgsMultiBandColorRenderer(r_s2.dataProvider(), 7, 3, 2)
    r_s2.setRenderer(renderer_cir)
    proj.addMapLayer(r_s2)

    set_extent_bompon(iface.mapCanvas())
    QTimer.singleShot(1500, snap_cir_composite)

def snap_cir_composite():
    out = os.path.join(SCREENSHOT_DIR, "praktik_02_qgis_cir_composite.png")
    mw.grab().save(out, "PNG")
    print(f" -> Saved: {out}")
    step_bsi_map()

# --- TAHAP 3: Peta BSI (Bare Soil Index) ---
def step_bsi_map():
    print("[3/5] Menyiapkan Tampilan Peta Bare Soil Index (BSI)...")
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

    set_extent_bompon(iface.mapCanvas())
    QTimer.singleShot(1500, snap_bsi_map)

def snap_bsi_map():
    out = os.path.join(SCREENSHOT_DIR, "praktik_04_qgis_bsi_map.png")
    mw.grab().save(out, "PNG")
    print(f" -> Saved: {out}")
    step_titik_graduated()

# --- TAHAP 4: Titik Sampel Graduated Lempung ---
def step_titik_graduated():
    print("[4/5] Menyiapkan Tampilan 50 Titik Sampel Graduated Kadar Lempung...")
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
    
    # Buat graduated renderer berdasarkan kolom Lempung_1
    field_name = "Lempung_1"
    ranges = []
    
    # 5 Kelas Kadar Lempung
    cfg = [
        (30.0, 50.0, QColor(255, 255, 178), 2.5, "35% - 50% (Lempung Rendah)"),
        (50.0, 60.0, QColor(254, 204, 92), 3.2, "50% - 60%"),
        (60.0, 68.0, QColor(253, 141, 60), 3.8, "60% - 68%"),
        (68.0, 74.0, QColor(240, 59, 32), 4.4, "68% - 74%"),
        (74.0, 85.0, QColor(189, 0, 38), 5.2, "> 74% (Lempung Sangat Tinggi)")
    ]
    for lower, upper, col, size, label in cfg:
        sym = QgsSymbol.defaultSymbol(v_pts.geometryType())
        sym.setColor(col)
        sym.setSize(size)
        sym.symbolLayer(0).setStrokeColor(QColor(0, 0, 0))
        sym.symbolLayer(0).setStrokeWidth(0.4)
        rng = QgsRendererRange(lower, upper, sym, label)
        ranges.append(rng)
        
    grad_renderer = QgsGraduatedSymbolRenderer(field_name, ranges)
    v_pts.setRenderer(grad_renderer)
    proj.addMapLayer(v_pts)

    set_extent_bompon(iface.mapCanvas())
    QTimer.singleShot(1500, snap_titik_graduated)

def snap_titik_graduated():
    out = os.path.join(SCREENSHOT_DIR, "praktik_05_qgis_titik_graduated_lempung.png")
    mw.grab().save(out, "PNG")
    print(f" -> Saved: {out}")
    print("=== SEMUA SCREENSHOT TAMBAHAN SELESAI DIAMBIL 100%! ===")
    QTimer.singleShot(500, iface.actionExit().trigger)

# Mulai pipeline
QTimer.singleShot(2500, step_dem_elevation)
