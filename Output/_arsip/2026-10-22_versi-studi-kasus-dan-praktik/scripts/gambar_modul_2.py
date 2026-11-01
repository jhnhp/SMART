"""Gambar Modul 2 — Multi-source Data Fusion.

Jalankan: python3 Output/scripts/gambar_modul_2.py
Keluaran: Output/assets/modul-2/M2-Gxx_*.png
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, Patch, Polygon, Rectangle

import gaya
from gaya import WARNA, kanvas, kotak, nomor, panah, simpan
from gambar_modul_1 import gelombang, matahari, satelit

MODUL = "modul-2"


def awan(ax, x, y, s=1.0):
    for dx, dy, r in [(0, 0, 2.2), (2.2, 0.6, 2.6), (4.6, 0, 2.0), (2.2, -0.9, 2.0)]:
        ax.add_patch(Circle((x + dx * s, y + dy * s), r * s, fc="white", ec="#B8C4D2", lw=0.8, zorder=4))


def pohon_tinggi(ax, x, y, s=1.0):
    ax.add_patch(Rectangle((x - 0.3 * s, y), 0.6 * s, 4.5 * s, fc="#6B4A2B", ec="none", zorder=3))
    ax.add_patch(Circle((x, y + 6.0 * s), 2.4 * s, fc=WARNA["hijau"], ec="#3A7A20", lw=0.6, zorder=3))


def pesawat(ax, x, y, s=1.0):
    ax.add_patch(Polygon([[x - 4 * s, y], [x + 4 * s, y + 0.4 * s], [x + 4.6 * s, y + 1.0 * s], [x - 4 * s, y + 0.9 * s]],
                         fc="#C9CED6", ec=WARNA["navy"], lw=0.9, zorder=5))
    ax.add_patch(Polygon([[x - 0.5 * s, y + 0.5 * s], [x + 1.6 * s, y + 0.5 * s], [x - 1.5 * s, y + 3.0 * s]],
                         fc="#9AA5B4", ec=WARNA["navy"], lw=0.8, zorder=5))
    ax.add_patch(Polygon([[x - 3.6 * s, y + 0.8 * s], [x - 2.6 * s, y + 0.8 * s], [x - 3.8 * s, y + 2.3 * s]],
                         fc="#9AA5B4", ec=WARNA["navy"], lw=0.8, zorder=5))


# ---------------------------------------------------------------- Gambar 2.1
def g01_prinsip_perekaman():
    fig, ax = kanvas(10, 4.3, (0, 102), (-11, 34))
    judul = ["(a) Optik (pasif)", "(b) SAR (aktif, gelombang mikro)", "(c) LiDAR (aktif, laser)"]
    keterangan = [
        "merekam pantulan energi matahari;\nterhalang awan; hanya permukaan teratas",
        "memancarkan pulsa dan merekam hamburan\nbalik; menembus awan; peka kekasaran\ndan kelembapan permukaan",
        "titik merah: pantulan pertama (tajuk);\ntitik biru tua: pantulan terakhir (tanah);\nmenghasilkan model permukaan dan model medan",
    ]
    for k, x0 in enumerate((0, 35, 70)):
        ax.text(x0 + 15.5, 32.5, judul[k], ha="center", fontsize=10, fontweight="bold", color=WARNA["navy"])
        ax.text(x0 + 15.5, -4.0, keterangan[k], ha="center", va="top", fontsize=8.3, color=WARNA["teks"], linespacing=1.2)
    # (a) optik
    ax.add_patch(Rectangle((1, 0), 30, 2.2, fc=WARNA["tanah_muda"], ec="none"))
    for xp in (6, 10, 14):
        pohon_tinggi(ax, xp, 2.2, 0.55)
    matahari(ax, 4, 26, r=2.2)
    satelit(ax, 25, 26, 0.75)
    awan(ax, 9.5, 19.5, 0.8)
    panah(ax, 6, 23.4, 12.2, 21.0, warna=WARNA["oranye"], lw=1.4)
    ax.text(14.6, 22.3, "×", fontsize=13, color=WARNA["merah"], ha="center", va="center", fontweight="bold")
    panah(ax, 5.8, 23.2, 20.5, 2.5, warna=WARNA["oranye"], lw=1.4)
    panah(ax, 20.5, 2.5, 24.6, 23.6, warna=WARNA["teal"], lw=1.8)
    ax.text(24.0, 11.0, "pantulan", fontsize=8, color=WARNA["teal"], rotation=78)
    # (b) SAR
    xs = np.linspace(36, 66, 200)
    bukit = 2.2 + 8.0 * np.exp(-((xs - 52) / 5.0) ** 2)
    ax.fill_between(xs, 0, bukit, color=WARNA["tanah_muda"], zorder=1)
    ax.add_patch(Polygon([[52.6, 9.8], [60.5, 2.2], [56.5, 2.2], [54.2, 5.0]], fc="#5F6B7A", alpha=0.35, ec="none", zorder=2))
    ax.text(60.5, 5.8, "bayangan\nradar", fontsize=7.5, color=WARNA["abu"], ha="left")
    satelit(ax, 38, 27, 0.75)
    awan(ax, 41.5, 19.0, 0.75)
    for x_akhir in (45.5, 49.0):
        ax.plot([39.5, x_akhir], [25.2, 2.2 + 8.0 * np.exp(-((x_akhir - 52) / 5.0) ** 2)], color=WARNA["ungu"], lw=1.3, zorder=3)
    gelombang(ax, (47.2, 6.6), (40.2, 24.4), WARNA["ungu"], amp=0.45, siklus=8, lw=1.0)
    ax.text(41.0, 9.5, "hamburan\nbalik", fontsize=7.5, color=WARNA["ungu"], ha="right")
    ax.plot([39.5, 39.5], [25.2, 16.0], color=WARNA["abu"], lw=0.6, ls=":")
    ax.text(38.3, 17.0, "θ", fontsize=9, color=WARNA["abu"], ha="center")
    ax.text(36.5, 13.6, "θ: sudut\npandang", fontsize=7, color=WARNA["abu"], ha="left")
    ax.text(57.5, 25.5, "pandangan\nmiring\n(side-looking)", fontsize=7.8, color=WARNA["abu"], ha="center")
    # (c) LiDAR
    ax.add_patch(Rectangle((71, 0), 30, 2.2, fc=WARNA["tanah_muda"], ec="none"))
    for xp in (78, 86, 94):
        pohon_tinggi(ax, xp, 2.2, 0.9)
    pesawat(ax, 86, 26, 1.0)
    for xt, yt in ((74.5, 2.2), (78.0, 10.3), (82.0, 2.2), (86.0, 10.3), (90.0, 2.2), (94.0, 10.3), (97.5, 2.2)):
        ax.plot([86, xt], [25.8, yt], color=WARNA["merah"], lw=0.7, alpha=0.8, zorder=2)
        ax.add_patch(Circle((xt, yt), 0.55, fc=WARNA["merah"] if yt > 3 else WARNA["navy"], ec="white", lw=0.5, zorder=6))
    simpan(fig, MODUL, "M2-G01_prinsip-perekaman-optik-sar-lidar.png")


# ---------------------------------------------------------------- Gambar 2.2
def g02_tingkat_fusi():
    fig, ax = kanvas(10, 6.2, (0, 104), (0, 64))
    abu, putih = WARNA["latar"], WARNA["putih"]
    w, h = 13, 5.2

    def node(x, y, teks, isi=putih, warna=WARNA["navy"], tebal=False):
        kotak(ax, x, y, w, h, teks, isi=isi, warna=warna, ukuran=8.3, tebal=tebal, r=0.8, lw=1.1)

    def ke(x1, y1, x2, y2):
        panah(ax, x1, y1, x2, y2, warna=WARNA["abu"], lw=1.1, skala=10)

    baris = [(44, "(a) Fusi tingkat piksel/data", WARNA["teal"]),
             (23, "(b) Fusi tingkat fitur", WARNA["oranye"]),
             (2, "(c) Fusi tingkat keputusan", WARNA["ungu"])]
    for y0, label, warna in baris:
        ax.add_patch(Rectangle((0, y0 - 1.0), 104, 19.5, fc=abu, ec="none", zorder=0))
        ax.text(1.5, y0 + 17.0, label, fontsize=10, fontweight="bold", color=warna, va="center")
        node(2, y0 + 8.6, "Data A\n(mis. citra optik)")
        node(2, y0 + 1.0, "Data B\n(mis. citra SAR)")

    # (a) piksel
    y0 = 44
    node(24, y0 + 4.8, "Fusi piksel", isi=WARNA["teal"], warna=WARNA["teal"], tebal=True)
    ax.texts[-1].set_color("white")
    node(44, y0 + 4.8, "Ekstraksi fitur")
    node(64, y0 + 4.8, "Klasifikasi/\nprediksi")
    node(86, y0 + 4.8, "Hasil akhir", isi="#DCEAF7")
    ke(15.2, y0 + 11.2, 24, y0 + 8.4), ke(15.2, y0 + 3.6, 24, y0 + 6.4)
    ke(37.2, y0 + 7.4, 44, y0 + 7.4), ke(57.2, y0 + 7.4, 64, y0 + 7.4), ke(77.2, y0 + 7.4, 86, y0 + 7.4)

    # (b) fitur
    y0 = 23
    node(24, y0 + 8.6, "Fitur A\n(mis. NDVI)")
    node(24, y0 + 1.0, "Fitur B\n(mis. backscatter)")
    node(44, y0 + 4.8, "Fusi fitur", isi=WARNA["oranye"], warna=WARNA["oranye"], tebal=True)
    ax.texts[-1].set_color("white")
    node(64, y0 + 4.8, "Klasifikasi/\nprediksi")
    node(86, y0 + 4.8, "Hasil akhir", isi="#DCEAF7")
    ke(15.2, y0 + 11.2, 24, y0 + 11.2), ke(15.2, y0 + 3.6, 24, y0 + 3.6)
    ke(37.2, y0 + 11.2, 44, y0 + 8.4), ke(37.2, y0 + 3.6, 44, y0 + 6.4)
    ke(57.2, y0 + 7.4, 64, y0 + 7.4), ke(77.2, y0 + 7.4, 86, y0 + 7.4)

    # (c) keputusan
    y0 = 2
    node(24, y0 + 8.6, "Fitur A")
    node(24, y0 + 1.0, "Fitur B")
    node(44, y0 + 8.6, "Keputusan A")
    node(44, y0 + 1.0, "Keputusan B")
    node(64, y0 + 4.8, "Fusi keputusan", isi=WARNA["ungu"], warna=WARNA["ungu"], tebal=True)
    ax.texts[-1].set_color("white")
    node(86, y0 + 4.8, "Hasil akhir", isi="#DCEAF7")
    ke(15.2, y0 + 11.2, 24, y0 + 11.2), ke(15.2, y0 + 3.6, 24, y0 + 3.6)
    ke(37.2, y0 + 11.2, 44, y0 + 11.2), ke(37.2, y0 + 3.6, 44, y0 + 3.6)
    ke(57.2, y0 + 11.2, 64, y0 + 8.4), ke(57.2, y0 + 3.6, 64, y0 + 6.4)
    ke(77.2, y0 + 7.4, 86, y0 + 7.4)
    simpan(fig, MODUL, "M2-G02_tingkat-fusi-data.png")


# ---------------------------------------------------------------- Gambar 2.3
def g03_penyelarasan_data():
    fig, ax = kanvas(10, 4.9, (0, 104), (0, 50))
    masukan = [
        ("Citra optik", "Sentinel-2, 10–20 m", WARNA["teal"]),
        ("Citra SAR", "Sentinel-1, ±10 m", WARNA["ungu"]),
        ("DEM", "DEMNAS, ±8 m", WARNA["oranye"]),
        ("Peta tematik (vektor)", "geologi, bentuklahan", WARNA["abu"]),
        ("Observasi lapangan", "titik GPS, sampel tanah", WARNA["tanah"]),
    ]
    ax.text(14, 47.5, "Data masukan beragam", ha="center", fontsize=10, fontweight="bold", color=WARNA["navy"])
    for i, (judul, isi, warna) in enumerate(masukan):
        y = 38.5 - i * 8.6
        kotak(ax, 1, y, 26, 7.0, isi=WARNA["putih"], warna=warna, lw=1.3, r=0.8)
        ax.add_patch(Rectangle((1.0, y), 1.6, 7.0, fc=warna, ec="none", zorder=4))
        ax.text(4.2, y + 4.6, judul, fontsize=9, fontweight="bold", color=warna, va="center")
        ax.text(4.2, y + 2.0, isi, fontsize=8.2, va="center")
        panah(ax, 27.4, y + 3.5, 36.5, 24.5, warna=WARNA["abu_muda"], lw=1.1, skala=8)

    langkah = ["Sistem koordinat seragam\n(mis. UTM 49S, EPSG:32749)", "Koreksi radiometrik\ndan geometrik",
               "Pemotongan ke batas\nwilayah kajian", "Resampling ke grid acuan\n(ukuran piksel sama)",
               "Penyelarasan waktu\nperekaman", "Kontrol mutu dan\npencatatan metadata"]
    ax.text(52, 47.5, "Penyelarasan", ha="center", fontsize=10, fontweight="bold", color=WARNA["navy"])
    kotak(ax, 37, 1, 30, 44.5, isi=WARNA["latar"], warna=WARNA["navy"], lw=1.2, r=1.0)
    for i, teks in enumerate(langkah):
        y = 40.0 - i * 7.3
        nomor(ax, 40.5, y, i + 1, r=1.5, ukuran=8.5)
        ax.text(43.2, y, teks, fontsize=8.4, va="center", linespacing=1.15)
    panah(ax, 67.6, 24, 74.5, 24, warna=WARNA["navy"], lw=1.6)

    ax.text(89, 47.5, "Tumpukan data selaras", ha="center", fontsize=10, fontweight="bold", color=WARNA["navy"])
    lapis = [("kanal optik dan indeks", WARNA["teal"]), ("backscatter VV/VH", WARNA["ungu"]),
             ("elevasi dan turunannya", WARNA["oranye"]), ("kelas tematik (rasterisasi)", WARNA["abu"])]
    for i, (label, warna) in enumerate(lapis):
        y = 36 - i * 8.2
        ax.add_patch(Polygon([[77, y], [95, y], [100, y + 4.2], [82, y + 4.2]], fc=warna, alpha=0.85, ec="white", lw=1.2, zorder=4 - i))
        for k in range(1, 6):
            ax.plot([77 + 3.6 * k, 82 + 3.6 * k], [y, y + 4.2], color="white", lw=0.4, alpha=0.6, zorder=4 - i)
        ax.text(88.5, y - 0.8, label, fontsize=8.2, ha="center", va="top")
    ax.text(88.5, 3.2, "setiap piksel memiliki nilai dari\nsemua lapisan pada lokasi yang sama", ha="center",
            fontsize=8, style="italic", color=WARNA["abu"])
    simpan(fig, MODUL, "M2-G03_prinsip-penyelarasan-data.png")


# ---------------------------------------------------------------- Gambar 2.4
def rasterisasi(layer, kolom, kelas, resolusi=2.0):
    from osgeo import gdal

    gdal.UseExceptions()
    batas = gaya.baca_layer("batas_subdas")[0][1]
    minx, maxx, miny, maxy = batas.GetEnvelope()
    nx, ny = int((maxx - minx) / resolusi) + 1, int((maxy - miny) / resolusi) + 1
    ds = gdal.GetDriverByName("MEM").Create("", nx, ny, 1, gdal.GDT_Byte)
    ds.SetGeoTransform((minx, resolusi, 0, maxy, 0, -resolusi))
    from osgeo import ogr, osr

    srs = osr.SpatialReference()
    srs.ImportFromEPSG(32749)
    ds.SetProjection(srs.ExportToWkt())
    src = ogr.Open(gaya.GPKG)
    lyr = src.GetLayer(layer)
    for i, k in enumerate(kelas, start=1):
        lyr.SetAttributeFilter(f"{kolom} = '{k}'")
        gdal.RasterizeLayer(ds, [1], lyr, burn_values=[i])
    arr = ds.GetRasterBand(1).ReadAsArray()
    return arr, (minx, minx + nx * resolusi, maxy - ny * resolusi, maxy)


def g04_lapisan_data_bompon():
    batas = gaya.baca_layer("batas_subdas")[0][1]
    minx, maxx, miny, maxy = batas.GetEnvelope()
    fig, axs = plt.subplots(1, 4, figsize=(10, 6.6))
    fig.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.27, wspace=0.05)
    judul = ["(a) Bentuklahan", "(b) Kelas lereng", "(c) Penggunaan lahan", "(d) Longsor dan titik sampel"]
    for ax, t in zip(axs, judul):
        ax.set_xlim(minx - 60, maxx + 60)
        ax.set_ylim(miny - 60, maxy + 60)
        ax.set_aspect("equal")
        ax.set_xticks([]), ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)
        ax.set_title(t, fontsize=10)

    legenda = []
    for atr, g in gaya.baca_layer("bentuklahan"):
        gaya.gambar_poligon(axs[0], g, fc=gaya.WARNA_BENTUKLAHAN[atr["bentuklahan"]], ec="white", lw=0.3)
    legenda.append([Patch(fc=c, label=k) for k, c in gaya.WARNA_BENTUKLAHAN.items()])

    kelas = list(gaya.WARNA_LERENG)
    arr, ext = rasterisasi("kelas_lereng", "kelas_lereng", kelas)
    from matplotlib.colors import ListedColormap

    cmap = ListedColormap(["#FFFFFF"] + [gaya.WARNA_LERENG[k] for k in kelas])
    axs[1].imshow(np.ma.masked_equal(arr, 0), cmap=cmap, vmin=0, vmax=len(kelas), extent=ext, interpolation="nearest")
    legenda.append([Patch(fc=gaya.WARNA_LERENG[k], ec="#BBBBBB", lw=0.4, label=k.replace("-", "–")) for k in kelas])

    for atr, g in gaya.baca_layer("penggunaan_lahan"):
        gaya.gambar_poligon(axs[2], g, fc=gaya.WARNA_PENGGUNAAN[atr["penggunaan_lahan"]], ec="white", lw=0.3)
    legenda.append([Patch(fc=c, label=k) for k, c in gaya.WARNA_PENGGUNAAN.items()])

    warna_longsor = {"Longsor dorman": "#EBCB8B", "Longsor aktif dalam": WARNA["merah"], "Longsor aktif dangkal": "#F08A7E"}
    gaya.gambar_poligon(axs[3], batas, fc="#F4F4EF", ec="none")
    for atr, g in gaya.baca_layer("longsor"):
        gaya.gambar_poligon(axs[3], g, fc=warna_longsor[atr["kelas"]], ec="#8C6D3F", lw=0.4)
    for atr, g in gaya.baca_layer("sungai"):
        gaya.gambar_garis(axs[3], g, color=WARNA["biru"], lw=1.2 if "perenial" in atr["jenis"] else 0.6)
    titik = gaya.baca_layer("titik_sampel_rencana")
    axs[3].scatter([g.GetX() for _, g in titik], [g.GetY() for _, g in titik], s=11, color=WARNA["navy"],
                   edgecolor="white", lw=0.4, zorder=6)
    legenda.append([Patch(fc=c, label=k) for k, c in warna_longsor.items()] +
                   [Line2D([], [], color=WARNA["biru"], lw=1.2, label="Sungai"),
                    Line2D([], [], marker="o", ls="", color=WARNA["navy"], markersize=4.5, label="Titik sampel rencana (50)")])

    for ax, unsur in zip(axs, legenda):
        gaya.gambar_poligon(ax, batas, fc="none", ec=WARNA["navy"], lw=1.2, zorder=7)
        ax.legend(handles=unsur, loc="upper center", bbox_to_anchor=(0.5, -0.01), fontsize=7.6, handlelength=1.2,
                  handleheight=0.9, labelspacing=0.35)
    gaya.skala_batang(axs[0], minx, miny - 40, 500, "500 m", tinggi=25)
    gaya.panah_utara(axs[0], 0.90, 0.88, 0.05)
    simpan(fig, MODUL, "M2-G04_lapisan-data-subdas-bompon.png")


if __name__ == "__main__":
    gaya.atur()
    g01_prinsip_perekaman()
    g02_tingkat_fusi()
    g03_penyelarasan_data()
    g04_lapisan_data_bompon()
