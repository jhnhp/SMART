"""Pustaka bersama uji coba praktik di antarmuka QGIS yang sebenarnya.

Skrip uji dijalankan oleh QGIS Desktop, tanpa jendela yang mengganggu layar:

    QT_QPA_PLATFORM=offscreen qgis --nologo --noversioncheck --lang en \
        --profiles-path <folder_profil_bersih> --code Output/scripts/uji_praktik_N.py

Setiap langkah membuka dialog QGIS yang sama dengan yang dipakai peserta, memotretnya,
lalu menjalankan algoritmenya. Peta dan tangkapan layar berasal dari data sebenarnya.
"""
import json
import os
import re
import shutil
import sys
import traceback
import zipfile

import processing
from qgis.core import (Qgis, QgsApplication, QgsCategorizedSymbolRenderer, QgsColorRampShader, QgsContrastEnhancement,
                       QgsCoordinateReferenceSystem, QgsFillSymbol, QgsLayerTreeLayer, QgsMarkerSymbol, QgsLineSymbol, QgsMultiBandColorRenderer,
                       QgsPalettedRasterRenderer, QgsProject, QgsRasterLayer, QgsRasterMinMaxOrigin, QgsRasterShader,
                       QgsRendererCategory, QgsSettings, QgsSingleBandGrayRenderer, QgsSingleBandPseudoColorRenderer,
                       QgsStyle, QgsVectorLayer)
from qgis.gui import QgsFileWidget
from qgis.PyQt.QtCore import QEventLoop, QPoint, Qt, QTimer
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtTest import QTest
from qgis.PyQt.QtWidgets import QAbstractButton, QAction, QApplication, QDialogButtonBox, QDockWidget, QLineEdit, QPlainTextEdit, QTextEdit
from qgis.utils import iface

AKAR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')) if '__file__' in globals() else os.environ['AKAR_PROYEK']
PELATIHAN = os.path.join(AKAR, 'Output', 'Pelatihan')
CATATAN = {}


def tunggu(ms=300):
    loop = QEventLoop()
    QTimer.singleShot(ms, loop.quit)
    loop.exec()


class Uji:
    def __init__(self, n):
        self.n = n
        self.data = os.path.join(PELATIHAN, 'data', f'praktik-{n}')
        self.hasil = os.path.join(self.data, 'hasil')
        self.foto = os.path.join(PELATIHAN, 'screenshots', f'praktik-{n}')
        os.makedirs(self.hasil, exist_ok=True)
        os.makedirs(self.foto, exist_ok=True)
        self.no = 0
        self.w = iface.mainWindow()
        self.canvas = iface.mapCanvas()
        jalur_catatan = os.path.join(self.hasil, 'catatan_uji.json')
        self.catatan = json.load(open(jalur_catatan)) if os.path.exists(jalur_catatan) else {}

    def siapkan_jendela(self):
        self.w.resize(1480, 880)
        for d in self.w.findChildren(QDockWidget):
            if d.objectName() in ('Browser', 'Browser2', 'browserDock', 'QgsBrowserDockWidget') or d.windowTitle().startswith('Browser'):
                d.hide()
        iface.newProject(False)
        p = QgsProject.instance()
        p.setCrs(QgsCoordinateReferenceSystem('EPSG:32749'))
        p.setFileName(self.h(f'Praktik_{self.n}_selesai.qgz'))
        tunggu(800)

    # ---- jalur berkas
    def d(self, *nama):
        return os.path.join(self.data, *nama)

    def h(self, *nama):
        return os.path.join(self.hasil, *nama)

    # ---- pemotretan
    def _nama(self, nama):
        self.no += 1
        return os.path.join(self.foto, f'{self.no:02d}_{nama}.png')

    def render(self):
        for node in QgsProject.instance().layerTreeRoot().findLayers():
            node.setExpanded(False)
        self.canvas.refreshAllLayers()
        tunggu(300)
        for _ in range(100):
            QApplication.processEvents()
            if not self.canvas.isDrawing():
                break
            tunggu(100)
        tunggu(300)

    def foto_jendela(self, nama):
        self.render()
        # pesan pemasangan font dari profil baru tidak relevan bagi peserta
        for w in iface.messageBar().items():
            if 'font' in (w.text() or '').lower() or 'font' in (w.title() or '').lower():
                iface.messageBar().popWidget(w)
        tunggu(100)
        self.w.grab().save(self._nama(nama))

    def foto_widget(self, widget, nama):
        tunggu(500)
        widget.grab().save(self._nama(nama))

    def dialog(self, alg, param, nama, jalankan=True, ukuran=None):
        """Membuka dialog algoritme seperti yang dilihat peserta, memotret, lalu menjalankannya."""
        dlg = processing.createAlgorithmDialog(alg, param)
        if ukuran:
            dlg.resize(*ukuran)
        dlg.show()
        self.foto_widget(dlg, nama)
        dlg.close()
        dlg.deleteLater()
        return processing.run(alg, param) if jalankan else None

    def modal(self, pemicu, saat_terbuka, jeda=1800):
        """Menjalankan aksi yang membuka dialog modal; saat_terbuka(dialog) wajib menutupnya."""
        hasil = {}

        def cb():
            try:
                d = QApplication.activeModalWidget()
                hasil['ok'] = saat_terbuka(d)
            except Exception:
                self.catat('galat_modal', traceback.format_exc())
                d = QApplication.activeModalWidget()
                if d:
                    d.reject()
        QTimer.singleShot(jeda, cb)
        pemicu()
        tunggu(300)
        return hasil.get('ok')

    def properti(self, layer, halaman, nama, ukuran=(980, 700)):
        """Layer Properties raster tidak memblokir (show, bukan exec), vektor memblokir."""
        iface.setActiveLayer(layer)
        if layer.type() == 1:
            iface.showLayerProperties(layer, halaman)
            tunggu(1500)
            d = QApplication.activeModalWidget()
            d.resize(*ukuran)
            self.foto_widget(d, nama)
            d.reject()
            tunggu(500)
            return

        def buka(d):
            d.resize(*ukuran)
            self.foto_widget(d, nama)
            d.reject()
        self.modal(lambda: iface.showLayerProperties(layer, halaman), buka)

    def kalkulator(self, ekspresi, keluaran, acuan, foto=None, nama_layer=None):
        """Raster Calculator dari menu Raster, dialog yang sama dengan peserta."""
        iface.setActiveLayer(acuan)

        def isi(d):
            d.resize(980, 720)
            d.findChild(QTextEdit, 'mExpressionTextEdit').setPlainText(ekspresi)
            d.findChild(QgsFileWidget, 'mOutputLayer').setFilePath(keluaran)
            tunggu(300)
            if foto:
                self.foto_widget(d, foto)
            ok = d.findChild(QDialogButtonBox).button(QDialogButtonBox.Ok)
            if not ok.isEnabled():
                raise RuntimeError('Ekspresi ditolak: ' + ekspresi)
            d.accept()
        aksi = self.w.findChild(QAction, 'mActionShowRasterCalculator')
        self.modal(aksi.trigger, isi)
        tunggu(800)
        dasar = os.path.splitext(os.path.basename(keluaran))[0]
        ls = QgsProject.instance().mapLayersByName(dasar)
        if not ls:
            raise RuntimeError('Hasil kalkulator tidak dimuat: ' + keluaran)
        ls[0].setName(nama_layer or dasar)
        return ls[0]

    # ---- pemuatan
    def raster(self, jalur, nama=None, tampil=True):
        lyr = QgsRasterLayer(jalur, nama or os.path.splitext(os.path.basename(jalur))[0])
        if not lyr.isValid():
            raise RuntimeError('Raster tidak valid: ' + jalur)
        QgsProject.instance().addMapLayer(lyr)
        self.lihat(lyr, tampil)
        return lyr

    def vektor(self, gpkg, layer=None, nama=None):
        uri = f'{gpkg}|layername={layer}' if layer else gpkg
        lyr = QgsVectorLayer(uri, nama or layer or os.path.splitext(os.path.basename(gpkg))[0], 'ogr')
        if not lyr.isValid():
            raise RuntimeError('Vektor tidak valid: ' + uri)
        QgsProject.instance().addMapLayer(lyr)
        return lyr

    def lihat(self, lyr, tampil=True):
        node = QgsProject.instance().layerTreeRoot().findLayer(lyr.id())
        if node:
            node.setItemVisibilityChecked(tampil)

    def hanya(self, *layers):
        for l in QgsProject.instance().mapLayers().values():
            self.lihat(l, l in layers)

    def urut(self, *layers):
        """Mengurutkan panel Layers dari atas ke bawah."""
        root = QgsProject.instance().layerTreeRoot()
        for i, l in enumerate(layers):
            node = root.findLayer(l.id())
            klon = node.clone()
            root.insertChildNode(i, klon)
            node.parent().removeChildNode(node)

    def zoom(self, lyr, skala=1.05):
        e = lyr.extent()
        e.scale(skala)
        self.canvas.setExtent(e)
        self.render()

    # ---- simbologi
    def rgb(self, lyr, r, g, b):
        ren = QgsMultiBandColorRenderer(lyr.dataProvider(), r, g, b)
        lyr.setRenderer(ren)
        lyr.setContrastEnhancement(QgsContrastEnhancement.StretchToMinimumMaximum, QgsRasterMinMaxOrigin.CumulativeCut)
        lyr.triggerRepaint()
        iface.layerTreeView().refreshLayerSymbology(lyr.id())

    def abu(self, lyr, band=1, mn=None, mx=None):
        ren = QgsSingleBandGrayRenderer(lyr.dataProvider(), band)
        lyr.setRenderer(ren)
        if mn is None:
            lyr.setContrastEnhancement(QgsContrastEnhancement.StretchToMinimumMaximum, QgsRasterMinMaxOrigin.CumulativeCut)
        else:
            ce = QgsContrastEnhancement(lyr.dataProvider().dataType(band))
            ce.setContrastEnhancementAlgorithm(QgsContrastEnhancement.StretchToMinimumMaximum)
            ce.setMinimumValue(mn)
            ce.setMaximumValue(mx)
            ren.setContrastEnhancement(ce)
        lyr.triggerRepaint()
        iface.layerTreeView().refreshLayerSymbology(lyr.id())

    def semu(self, lyr, ramp='Spectral', mn=None, mx=None, balik=False, band=1, label=None):
        st = lyr.dataProvider().bandStatistics(band)
        mn = st.minimumValue if mn is None else mn
        mx = st.maximumValue if mx is None else mx
        r = QgsStyle.defaultStyle().colorRamp(ramp)
        if balik:
            r.invert()
        n = 7
        item = []
        for i in range(n):
            f = i / (n - 1)
            v = mn + f * (mx - mn)
            item.append(QgsColorRampShader.ColorRampItem(v, r.color(f), f'{v:.2f}'))
        sh = QgsColorRampShader(mn, mx)
        sh.setSourceColorRamp(r)
        sh.setColorRampType(QgsColorRampShader.Interpolated)
        sh.setColorRampItemList(item)
        rs = QgsRasterShader()
        rs.setRasterShaderFunction(sh)
        ren = QgsSingleBandPseudoColorRenderer(lyr.dataProvider(), band, rs)
        ren.setClassificationMin(mn)
        ren.setClassificationMax(mx)
        lyr.setRenderer(ren)
        lyr.triggerRepaint()
        iface.layerTreeView().refreshLayerSymbology(lyr.id())

    def palet(self, lyr, kelas, band=1):
        """kelas = {nilai: (warna, label)}"""
        k = [QgsPalettedRasterRenderer.Class(v, QColor(w), l) for v, (w, l) in kelas.items()]
        lyr.setRenderer(QgsPalettedRasterRenderer(lyr.dataProvider(), band, k))
        lyr.triggerRepaint()
        iface.layerTreeView().refreshLayerSymbology(lyr.id())

    def garis_tepi(self, lyr, warna='black', lebar='0.6'):
        lyr.renderer().setSymbol(QgsFillSymbol.createSimple({'style': 'no', 'outline_color': warna, 'outline_width': lebar}))
        lyr.triggerRepaint()
        iface.layerTreeView().refreshLayerSymbology(lyr.id())

    def garis(self, lyr, warna='#1f78b4', lebar='0.5'):
        lyr.renderer().setSymbol(QgsLineSymbol.createSimple({'line_color': warna, 'line_width': lebar}))
        lyr.triggerRepaint()
        iface.layerTreeView().refreshLayerSymbology(lyr.id())

    def titik(self, lyr, warna='#e31a1c', ukuran='2.2'):
        lyr.renderer().setSymbol(QgsMarkerSymbol.createSimple({'name': 'circle', 'color': warna, 'outline_color': 'white', 'outline_width': '0.2', 'size': ukuran}))
        lyr.triggerRepaint()
        iface.layerTreeView().refreshLayerSymbology(lyr.id())

    def kategori(self, lyr, kolom, warna, transparan=255, tepi='#333333'):
        cat = []
        for nilai, w in warna.items():
            c = QColor(w)
            c.setAlpha(transparan)
            s = QgsFillSymbol.createSimple({'color': f'{c.red()},{c.green()},{c.blue()},{c.alpha()}', 'outline_color': tepi, 'outline_width': '0.15'})
            cat.append(QgsRendererCategory(nilai, s, str(nilai)))
        lyr.setRenderer(QgsCategorizedSymbolRenderer(kolom, cat))
        lyr.triggerRepaint()
        iface.layerTreeView().refreshLayerSymbology(lyr.id())

    # ---- pencatatan angka untuk modul
    def catat(self, kunci, nilai):
        self.catatan[kunci] = nilai
        with open(self.h('catatan_uji.json'), 'w') as f:
            json.dump(self.catatan, f, indent=1, ensure_ascii=False, default=str)

    def selesai(self):
        QgsProject.instance().write()
        tunggu(300)
        # pengaturan GPS proyek menyimpan alamat absolut layer aktif; dikosongkan agar proyek tidak memuat alamat komputer uji
        jalur = QgsProject.instance().fileName()
        with zipfile.ZipFile(jalur) as z:
            isi = {n: z.read(n) for n in z.namelist()}
        for n in isi:
            if n.endswith('.qgs'):
                isi[n] = re.sub(rb'destinationLayerSource="[^"]*"', b'destinationLayerSource=""', isi[n])
        with zipfile.ZipFile(jalur, 'w', zipfile.ZIP_DEFLATED) as z:
            for n, v in isi.items():
                z.writestr(n, v)
        for f in os.listdir(self.hasil):
            if f.endswith('.aux.xml'):
                os.remove(os.path.join(self.hasil, f))
        self.catat('status', 'selesai')


def jalankan(fungsi):
    def bungkus():
        try:
            fungsi()
        except Exception:
            with open(os.environ.get('LOG_UJI', '/tmp/uji_qgis_galat.txt'), 'a') as f:
                f.write(traceback.format_exc())
            print(traceback.format_exc(), flush=True)
        # keluar paksa supaya tidak ada dialog simpan proyek
        QgsProject.instance().setDirty(False)
        os._exit(0)
    QTimer.singleShot(5000, bungkus)
