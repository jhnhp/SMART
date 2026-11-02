"""
Skrip Pengambilan Tangkapan Layar QGIS GUI untuk Target C-Organik (Praktik 5)
- Titik Sampel Graduated C-Organik
- Peta Prediksi Kontinu C-Organik 0-20 cm (%)
- Peta Ketidakpastian PI90 C-Organik
"""

import os
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
    QgsSimpleMarkerSymbolLayer,
    QgsGraduatedSymbolRenderer,
    QgsRendererRange,
    QgsSymbol
)
from qgis.gui import QgsMessageBar
from qgis.utils import iface

BASE_DIR = "/home/jhn/Documents/Sayangku/Modul Junun"
SCREENSHOT_DIR = os.path.join(BASE_DIR, "Output/Pelatihan/screenshots")

mw = iface.mainWindow()
mw.resize(1366, 850)
proj = QgsProject.instance()

def clean_banners():
    try:
        iface.messageBar().clearWidgets()
        for bar in mw.findChildren(QgsMessageBar):
            bar.clearWidgets()
            bar.hide()
    except Exception:
        pass

def zoom_to_bompon(canvas, v_layer):
    clean_banners()
    ext = v_layer.extent()
    ext.scale(1.10)
    canvas.setExtent(ext)
    canvas.refresh()

def step_p5_corg_pts():
    print("[1/3] Titik Sampel Graduated C-Organik...")
    proj.clear()
    proj.setCrs(QgsCoordinateReferenceSystem("EPSG:32749"))

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

    v_pts = QgsVectorLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-5/titik_sampel_lapangan.gpkg", "Kadar C-Organik Lab (%) Lapisan 0-20 cm", "ogr")
    
    # 5 Kelas C-Organik: Rendah (<0.6%), Sedang (0.6-0.9%), Agak Tinggi (0.9-1.2%), Tinggi (>1.2%)
    cfg = [
        (0.0, 0.6, QColor(254, 237, 222), 2.8, "< 0.6% (Sangat Rendah)"),
        (0.6, 0.85, QColor(253, 190, 133), 3.4, "0.6% - 0.85% (Rendah)"),
        (0.85, 1.1, QColor(253, 141, 60), 4.0, "0.85% - 1.1% (Sedang)"),
        (1.1, 1.3, QColor(230, 85, 13), 4.6, "1.1% - 1.3% (Tinggi)"),
        (1.3, 2.5, QColor(166, 54, 3), 5.4, "> 1.3% (Sangat Tinggi)")
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

    zoom_to_bompon(iface.mapCanvas(), v_batas)
    QTimer.singleShot(1500, snap_p5_corg_pts_out)

def snap_p5_corg_pts_out():
    clean_banners()
    out = os.path.join(SCREENSHOT_DIR, "praktik_05_qgis_titik_graduated_lempung.png")
    mw.grab().save(out, "PNG")
    print(f" -> Saved: {out}")
    step_p5_corg_pred()

def step_p5_corg_pred():
    print("[2/3] Peta Prediksi C-Organik...")
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
    sym_pt.setColor(QColor(40, 40, 40))
    sym_pt.setStrokeColor(QColor(255, 255, 255))
    sym_pt.setStrokeWidth(0.5)
    v_pts.renderer().symbol().changeSymbolLayer(0, sym_pt)
    proj.addMapLayer(v_pts)

    # Muat GeoTIFF Prediksi C-Organik
    r_pred = QgsRasterLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-5/prediksi_corganik_0_20cm.tif", "Prediksi Kadar C-Organik 0-20cm (%)")
    fcn_p = QgsColorRampShader()
    fcn_p.setColorRampType(QgsColorRampShader.Interpolated)
    # Skema warna tanah/organik (Kuning pucat ke Cokelat Tua / Hijau Zaitun)
    items_p = [
        QgsColorRampShader.ColorRampItem(0.5, QColor(255, 255, 212), "0.5% - Sangat Rendah"),
        QgsColorRampShader.ColorRampItem(0.75, QColor(254, 217, 142), "0.75% - Rendah"),
        QgsColorRampShader.ColorRampItem(1.0, QColor(254, 153, 41), "1.00% - Sedang"),
        QgsColorRampShader.ColorRampItem(1.25, QColor(204, 76, 2), "1.25% - Tinggi"),
        QgsColorRampShader.ColorRampItem(1.5, QColor(102, 37, 6), "> 1.50% - Sangat Tinggi (Humus)")
    ]
    fcn_p.setColorRampItemList(items_p)
    shader_p = QgsRasterShader()
    shader_p.setRasterShaderFunction(fcn_p)
    ps_rend_p = QgsSingleBandPseudoColorRenderer(r_pred.dataProvider(), 1, shader_p)
    r_pred.setRenderer(ps_rend_p)
    proj.addMapLayer(r_pred)

    zoom_to_bompon(iface.mapCanvas(), v_batas)
    QTimer.singleShot(1500, snap_p5_corg_pred_out)

def snap_p5_corg_pred_out():
    clean_banners()
    out = os.path.join(SCREENSHOT_DIR, "praktik_05_qgis_prediksi_lempung.png")
    mw.grab().save(out, "PNG")
    print(f" -> Saved: {out}")
    step_p5_corg_unc()

def step_p5_corg_unc():
    print("[3/3] Peta Ketidakpastian PI90 C-Organik...")
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

    r_unc = QgsRasterLayer(f"{BASE_DIR}/Output/Pelatihan/data/praktik-5/ketidakpastian_pi90_corganik.tif", "Ketidakpastian PI90 C-Organik (%)")
    fcn_u = QgsColorRampShader()
    fcn_u.setColorRampType(QgsColorRampShader.Interpolated)
    items_u = [
        QgsColorRampShader.ColorRampItem(0.1, QColor(254, 229, 217), "0.1% - Sangat Pasti"),
        QgsColorRampShader.ColorRampItem(0.3, QColor(252, 174, 145), "0.3%"),
        QgsColorRampShader.ColorRampItem(0.6, QColor(251, 106, 74), "0.6%"),
        QgsColorRampShader.ColorRampItem(1.0, QColor(165, 15, 21), "> 1.0% - Ketidakpastian Tinggi")
    ]
    fcn_u.setColorRampItemList(items_u)
    shader_u = QgsRasterShader()
    shader_u.setRasterShaderFunction(fcn_u)
    ps_rend_u = QgsSingleBandPseudoColorRenderer(r_unc.dataProvider(), 1, shader_u)
    r_unc.setRenderer(ps_rend_u)
    proj.addMapLayer(r_unc)

    zoom_to_bompon(iface.mapCanvas(), v_batas)
    QTimer.singleShot(1500, snap_p5_corg_unc_out)

def snap_p5_corg_unc_out():
    clean_banners()
    out = os.path.join(SCREENSHOT_DIR, "praktik_05_qgis_ketidakpastian_pi90.png")
    mw.grab().save(out, "PNG")
    print(f" -> Saved: {out}")
    print("=== TANGKAPAN LAYAR C-ORGANIK QGIS SELESAI 100%! ===")
    QTimer.singleShot(500, iface.actionExit().trigger)

QTimer.singleShot(2500, step_p5_corg_pts)
