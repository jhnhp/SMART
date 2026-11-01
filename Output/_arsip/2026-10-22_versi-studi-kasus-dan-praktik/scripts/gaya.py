"""Gaya visual bersama untuk semua gambar modul.

Semua gambar dibuat dengan matplotlib agar seragam: font Carlito (metrik setara
Calibri), palet warna yang sama, dan ukuran keluaran yang pas untuk lebar
halaman A4 (±16 cm).
"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, PathPatch  # noqa: E402
from matplotlib.path import Path  # noqa: E402

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASET = os.path.join(AKAR, "Output", "assets")
GPKG = os.path.join(AKAR, "Source", "Data Bompon", "bompon.gpkg")

WARNA = {
    "navy": "#1F3A5F",
    "teks": "#1F2933",
    "teal": "#2A9D8F",
    "biru": "#3B82C4",
    "biru_muda": "#DCEAF7",
    "hijau": "#4C9A2A",
    "hijau_muda": "#DDEFD3",
    "tanah": "#8C5A3C",
    "tanah_muda": "#D9B48F",
    "oranye": "#E07B39",
    "kuning": "#F2C14E",
    "ungu": "#7B5EA7",
    "merah": "#C0392B",
    "abu": "#6B7280",
    "abu_muda": "#E5E7EB",
    "latar": "#F5F7FA",
    "putih": "#FFFFFF",
}

# Warna tetap untuk kelas data Bompon agar konsisten di semua modul
WARNA_BENTUKLAHAN = {
    "Interfluve": "#7A4E2D",
    "Lereng Atas Perbukitan": "#B5763F",
    "Lereng Tengah Perbukitan": "#D9A35F",
    "Lereng Bawah Perbukitan": "#EBCB8B",
    "Lereng Kaki Koluvial": "#9CC5A1",
    "Dataran Koluvial": "#5E9E8A",
}
WARNA_LERENG = {
    "Datar (0-8%)": "#E8F1D8",
    "Landai (8-15%)": "#BFDB8F",
    "Agak Curam (15-25%)": "#F2C14E",
    "Curam (25-45%)": "#E07B39",
    "Sangat Curam (>45%)": "#A8322D",
}
WARNA_PENGGUNAAN = {
    "Agroforestri": "#3F7D3A",
    "Tegalan": "#D9B26F",
    "Sawah": "#8FCB6B",
    "Permukiman": "#B0B0B0",
}


def atur():
    plt.rcParams.update({
        "font.family": "Carlito",
        "font.size": 10,
        "text.color": WARNA["teks"],
        "axes.edgecolor": WARNA["abu"],
        "axes.labelcolor": WARNA["teks"],
        "axes.titlesize": 11,
        "axes.titleweight": "bold",
        "axes.titlecolor": WARNA["navy"],
        "xtick.color": WARNA["abu"],
        "ytick.color": WARNA["abu"],
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
        "savefig.facecolor": "white",
    })


def simpan(fig, modul, nama):
    folder = os.path.join(ASET, modul)
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, nama)
    fig.savefig(path, dpi=200, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)
    print("tersimpan:", os.path.relpath(path, AKAR))


def kanvas(lebar, tinggi, xlim, ylim):
    """Sumbu kosong berkoordinat bebas untuk diagram."""
    fig, ax = plt.subplots(figsize=(lebar, tinggi))
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def kotak(ax, x, y, w, h, teks="", warna=None, isi=None, ukuran=10, tebal=False, warna_teks=None, r=0.6, lw=1.2, zorder=3):
    warna = warna or WARNA["navy"]
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=isi or WARNA["putih"], ec=warna, lw=lw, zorder=zorder))
    if teks:
        ax.text(x + w / 2, y + h / 2, teks, ha="center", va="center", fontsize=ukuran,
                fontweight="bold" if tebal else "normal", color=warna_teks or WARNA["teks"],
                zorder=zorder + 1, linespacing=1.25)


def panah(ax, x1, y1, x2, y2, warna=None, lw=1.4, gaya="-|>", skala=12, putus=False, lengkung=0.0, zorder=2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=gaya, mutation_scale=skala,
                                 color=warna or WARNA["navy"], lw=lw, linestyle="--" if putus else "-",
                                 connectionstyle=f"arc3,rad={lengkung}", zorder=zorder, shrinkA=0, shrinkB=0))


def nomor(ax, x, y, n, warna=None, r=1.3, ukuran=9):
    ax.add_patch(plt.Circle((x, y), r, fc=warna or WARNA["navy"], ec="none", zorder=6))
    ax.text(x, y, str(n), ha="center", va="center", color="white", fontsize=ukuran, fontweight="bold", zorder=7)


# ---------------------------------------------------------------- peta
def geom_ke_path(geom):
    """Ubah geometri OGR (Polygon/MultiPolygon) menjadi matplotlib Path."""
    from osgeo import ogr

    verts, codes = [], []

    def cincin(r):
        pts = r.GetPoints()
        if not pts:
            return
        verts.extend((p[0], p[1]) for p in pts)
        codes.extend([Path.MOVETO] + [Path.LINETO] * (len(pts) - 2) + [Path.CLOSEPOLY])

    def poligon(p):
        for i in range(p.GetGeometryCount()):
            cincin(p.GetGeometryRef(i))

    t = ogr.GT_Flatten(geom.GetGeometryType())
    if t == ogr.wkbPolygon:
        poligon(geom)
    elif t == ogr.wkbMultiPolygon:
        for i in range(geom.GetGeometryCount()):
            poligon(geom.GetGeometryRef(i))
    return Path(verts, codes) if verts else None


def baca_layer(nama, filter_sql=None):
    """Kembalikan daftar (atribut dict, geometri OGR klon) dari bompon.gpkg."""
    from osgeo import ogr

    ogr.UseExceptions()
    ds = ogr.Open(GPKG)
    lyr = ds.GetLayer(nama)
    if filter_sql:
        lyr.SetAttributeFilter(filter_sql)
    hasil = []
    for f in lyr:
        hasil.append((f.items(), f.GetGeometryRef().Clone()))
    return hasil


def gambar_poligon(ax, geom, **kw):
    path = geom_ke_path(geom)
    if path is not None:
        ax.add_patch(PathPatch(path, **kw))


def gambar_garis(ax, geom, **kw):
    from osgeo import ogr

    t = ogr.GT_Flatten(geom.GetGeometryType())
    bagian = [geom] if t == ogr.wkbLineString else [geom.GetGeometryRef(i) for i in range(geom.GetGeometryCount())]
    for g in bagian:
        pts = g.GetPoints()
        ax.plot([p[0] for p in pts], [p[1] for p in pts], **kw)


def panah_utara(ax, x, y, ukuran=0.06):
    """Panah utara di koordinat sumbu (0–1)."""
    ax.annotate("", xy=(x, y + ukuran), xytext=(x, y), xycoords="axes fraction",
                arrowprops=dict(arrowstyle="-|>", color=WARNA["navy"], lw=1.6, mutation_scale=14))
    ax.text(x, y + ukuran + 0.012, "U", transform=ax.transAxes, ha="center", va="bottom",
            fontsize=10, fontweight="bold", color=WARNA["navy"])


def skala_batang(ax, x0, y0, panjang_m, label, tinggi=None):
    """Skala batang dalam satuan peta (meter UTM)."""
    tinggi = tinggi or panjang_m * 0.04
    for i, warna in enumerate(["#1F2933", "white"]):
        ax.add_patch(plt.Rectangle((x0 + i * panjang_m / 2, y0), panjang_m / 2, tinggi, fc=warna, ec="#1F2933", lw=0.8, zorder=8))
    ax.text(x0, y0 + tinggi * 1.6, "0", ha="center", va="bottom", fontsize=8, zorder=8)
    ax.text(x0 + panjang_m, y0 + tinggi * 1.6, label, ha="center", va="bottom", fontsize=8, zorder=8)


def grid_utm(ax, langkah=500, ukuran=7):
    from matplotlib.ticker import FuncFormatter, MultipleLocator

    for sumbu in (ax.xaxis, ax.yaxis):
        sumbu.set_major_locator(MultipleLocator(langkah))
        sumbu.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}".replace(",", ".")))
    ax.tick_params(labelsize=ukuran, length=2)
    plt.setp(ax.get_yticklabels(), rotation=90, va="center")
    ax.grid(color=WARNA["abu_muda"], lw=0.5, zorder=0)
    for s in ax.spines.values():
        s.set_visible(True)
        s.set_color(WARNA["abu"])
        s.set_linewidth(0.8)
