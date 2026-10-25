"""Gambar Modul 3 — Remote Sensing untuk Delineasi Soil Mapping Units (SMU).

Jalankan: python3 Output/scripts/gambar_modul_3.py
Keluaran: Output/assets/modul-3/M3-Gxx_*.png
Gambar data memakai bompon.gpkg, folder terbuka/ (Sentinel-2, Copernicus DEM), dan foto udara
data proyek; angka tumpang susun dihitung ulang melalui analisis_modul_3.py.
"""
import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Circle, Patch, PathPatch, Polygon, Rectangle
from matplotlib.path import Path
from osgeo import gdal

import gaya
import analisis_modul_3 as analisis
from gaya import WARNA, kanvas, kotak, panah, simpan

gdal.UseExceptions()
MODUL = "modul-3"
TERBUKA = os.path.join(gaya.AKAR, "Source", "Data Bompon", "terbuka")
FOTO_UDARA = os.path.join(gaya.AKAR, "Source", "Data Bompon", "mentah", "SHP Bompon", "das Bompon1.tif")


def gumpalan(cx, cy, r, seed, n=14, kasar=0.18):
    """Poligon tak beraturan (delineasi) sebagai matplotlib Path."""
    rng = np.random.default_rng(seed)
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    rr = r * (1 + kasar * rng.standard_normal(n))
    pts = np.c_[cx + rr * np.cos(t) * 1.25, cy + rr * np.sin(t)]
    halus = []
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        halus.extend([a, (a + b) / 2])
    return Path(np.vstack(halus + [halus[0]]), closed=True)


# ---------------------------------------------------------------- Gambar 3.1
def g01_jenis_satuan_peta():
    fig, ax = kanvas(10, 3.6, (0, 104), (0, 37))
    A, A2, B, C = "#B5763F", "#D9A35F", "#5E9E8A", "#7B5EA7"
    judul = ["(a) Konsosiasi", "(b) Asosiasi", "(c) Kompleks", "(d) Kelompok tak dibedakan"]
    ket = ["didominasi satu taksa (A)\ndan taksa serupa (A')",
           "A dan B berpola teratur;\ndapat dipisah pada skala lebih besar",
           "A dan B berpola rumit;\ntidak dapat dipisah pada skala praktis",
           "A dan C tidak selalu bersama,\ntetapi penggunaannya serupa"]
    rng = np.random.default_rng(3)
    for k in range(4):
        x0 = 2 + k * 26
        ax.text(x0 + 11, 34.8, judul[k], ha="center", fontsize=10, fontweight="bold", color=WARNA["navy"])
        ax.text(x0 + 11, 3.2, ket[k], ha="center", va="center", fontsize=8.2, linespacing=1.2)
        if k == 3:
            for j, (cx, cy, isi, lbl) in enumerate(((x0 + 6.5, 21, A, "A"), (x0 + 16, 15.5, C, "C"))):
                p = gumpalan(cx, cy, 5.0, 40 + j)
                ax.add_patch(PathPatch(p, fc=isi, ec=WARNA["navy"], lw=1.4, alpha=0.9))
                ax.text(cx, cy, lbl, ha="center", va="center", color="white", fontsize=11, fontweight="bold")
            ax.text(x0 + 11, 8.8, "legenda: \"A dan C\"", ha="center", fontsize=8, style="italic", color=WARNA["abu"])
            continue
        p = gumpalan(x0 + 11, 19, 8.2, 10 + k)
        latar = PathPatch(p, fc=A if k != 2 else "white", ec="none")
        ax.add_patch(latar)
        if k == 0:
            for _ in range(9):
                c = Circle((x0 + 11 + rng.uniform(-8, 8), 19 + rng.uniform(-6, 6)), rng.uniform(0.6, 1.4), fc=A2, ec="none")
                c.set_clip_path(latar)
                ax.add_patch(c)
            c = Circle((x0 + 15, 15), 1.0, fc=B, ec="none")
            c.set_clip_path(latar)
            ax.add_patch(c)
        elif k == 1:
            for j in range(4):
                xs = np.linspace(x0, x0 + 22, 50)
                ys = 13 + j * 3.2 + 0.9 * np.sin(xs * 0.7 + j)
                pita = Polygon(np.c_[np.r_[xs, xs[::-1]], np.r_[ys, ys[::-1] + 1.4]], fc=B, ec="none")
                pita.set_clip_path(latar)
                ax.add_patch(pita)
        else:
            for _ in range(70):
                c = Rectangle((x0 + rng.uniform(0, 21), 9 + rng.uniform(0, 20)), rng.uniform(1, 3), rng.uniform(1, 3),
                              angle=rng.uniform(0, 90), fc=A if rng.random() < 0.55 else B, ec="none")
                c.set_clip_path(latar)
                ax.add_patch(c)
        ax.add_patch(PathPatch(p, fc="none", ec=WARNA["navy"], lw=1.6))
    unsur = [Patch(fc=A, label="taksa A"), Patch(fc=A2, label="taksa serupa A'"), Patch(fc=B, label="taksa tak serupa B"),
             Patch(fc=C, label="taksa C")]
    fig.legend(handles=unsur, loc="lower center", ncol=4, fontsize=8.5, bbox_to_anchor=(0.5, -0.04))
    simpan(fig, MODUL, "M3-G01_jenis-satuan-peta-tanah.png")


# ---------------------------------------------------------------- Gambar 3.2
def g02_hierarki_taksonomi():
    fig, ax = kanvas(10, 4.9, (0, 104), (0, 50))
    tingkat = [
        ("Ordo", "ada/tidaknya horizon dan sifat\npenciri utama hasil proses pembentukan", "Ultisols", "ult", "benua/nasional"),
        ("Subordo", "sifat utama, mis. rejim kelembapan\natau drainase", "Udults", "ud + ult", ""),
        ("Great group", "jenis dan susunan horizon\npenciri lain", "Kandiudults", "kandi + ud + ult", "±1:250.000"),
        ("Subgrup", "konsep sentral (Typic) atau peralihan\nke taksa lain (intergrade)", "Typic Kandiudults", "", "±1:100.000"),
        ("Famili", "sifat penting bagi penggunaan: kelas\nbesar butir, mineralogi, suhu tanah", "Typic Kandiudults, fine-loamy,\nkaolinitic, thermic", "", "±1:50.000"),
        ("Seri", "satuan paling homogen;\ndiberi nama lokasi", "(nama seri setempat)", "", "±1:20.000"),
    ]
    warna = ["#7A4E2D", "#9B6235", "#B5763F", "#C98D4E", "#D9A35F", "#E6BE84"]
    ax.text(1, 48, "Kategori", fontsize=9.5, fontweight="bold", color=WARNA["navy"])
    ax.text(30, 48, "Dasar pembeda", fontsize=9.5, fontweight="bold", color=WARNA["navy"])
    ax.text(63, 48, "Contoh nama", fontsize=9.5, fontweight="bold", color=WARNA["navy"])
    ax.text(92, 48, "Padanan skala", fontsize=9.5, fontweight="bold", color=WARNA["navy"], ha="center")
    for i, (nama, dasar, contoh, unsur, skala) in enumerate(tingkat):
        y = 40 - i * 7.4
        kotak(ax, 1 + i * 1.6, y, 24 - i * 1.6, 6.2, nama, isi=warna[i], warna=warna[i], ukuran=9.5, tebal=True,
              warna_teks="white" if i < 4 else WARNA["teks"], r=0.6)
        ax.text(30, y + 3.1, dasar, fontsize=8.1, va="center", linespacing=1.15)
        ax.text(63, y + 3.1 + (0.9 if unsur else 0), contoh, fontsize=8.6, va="center", style="italic", linespacing=1.15)
        if unsur:
            ax.text(63, y + 1.2, f"unsur formatif: {unsur}", fontsize=7.6, va="center", color=WARNA["oranye"])
        if skala:
            ax.text(92, y + 3.1, skala, fontsize=8.4, va="center", ha="center", color=WARNA["abu"])
    panah(ax, 102, 41, 102, 4, warna=WARNA["abu"], lw=1.2)
    ax.text(103.2, 22.5, "makin rinci", rotation=-90, va="center", fontsize=8, color=WARNA["abu"])
    simpan(fig, MODUL, "M3-G02_hierarki-kategori-taksonomi-tanah.png")


# ---------------------------------------------------------------- Gambar 3.3
def g03_toposekuen_bompon():
    fig, ax = kanvas(10, 4.6, (0, 100), (-10, 44))
    x = np.linspace(0, 100, 600)
    z = np.interp(x, [0, 10, 14, 30, 55, 70, 82, 96, 97.5, 100], [32, 32, 31, 25, 12.5, 7, 4.2, 3.0, 1.0, 1.2])
    z = np.convolve(np.pad(z, 15, mode="edge"), np.ones(31) / 31, mode="valid")
    satuan = [("Interfluve", 0, 12), ("Lereng Atas Perbukitan", 12, 30), ("Lereng Tengah Perbukitan", 30, 55),
              ("Lereng Bawah Perbukitan", 55, 70), ("Lereng Kaki Koluvial", 70, 82), ("Dataran Koluvial", 82, 96)]
    ax.fill_between(x, -6, z - 3.5, color="#C9B8A0", zorder=1)
    ax.text(40, 4.5, "bahan induk: breksi teralterasi", fontsize=8, color="#6B5B45", style="italic")
    kol = (x > 66) & (x < 97)
    ax.fill_between(x[kol], np.maximum(z[kol] - 3.5, -1.5) - np.interp(x[kol], [66, 82, 97], [0, 2.8, 3.2]), z[kol] - 0.2,
                    color="#9CC5A1", alpha=0.9, zorder=2)
    ax.text(84, -3.6, "endapan koluvial", fontsize=8, color="#2F6B50", ha="center", style="italic")
    ax.fill_between(x, z - 3.5, z, color="#D9B48F", zorder=1.5)
    for nama, a, b in satuan:
        sel = (x >= a) & (x <= b)
        ax.plot(x[sel], z[sel], color=gaya.WARNA_BENTUKLAHAN[nama], lw=5, solid_capstyle="butt", zorder=3)
        xm = (a + b) / 2
        zm = np.interp(xm, x, z)
        ax.plot([a, a], [np.interp(a, x, z) - 3.5, 41], color=WARNA["abu_muda"], lw=0.8, ls=":", zorder=0)
        ax.text(xm, 41.5, nama.replace(" Perbukitan", "\nPerbukitan").replace(" Koluvial", "\nKoluvial"),
                ha="center", va="bottom", fontsize=7.8, color=WARNA["teks"], linespacing=1.05)
    ax.add_patch(Rectangle((96.5, -0.5), 2, 2.2, fc=WARNA["biru"], ec="none", zorder=4))
    ax.text(97.5, -2.6, "sungai", fontsize=7.5, ha="center", color=WARNA["biru"])
    proses = [(0, 30, "erosi dominan", WARNA["merah"]), (30, 70, "transportasi", WARNA["oranye"]), (70, 96, "deposisi", WARNA["teal"])]
    for a, b, lbl, w in proses:
        ax.annotate("", xy=(b - 1, 37.2), xytext=(a + 1, 37.2), arrowprops=dict(arrowstyle="-|>", color=w, lw=1.6))
        ax.text((a + b) / 2, 37.9, lbl, ha="center", fontsize=8.5, color=w, fontweight="bold")
    pl = [(6, 32.5, "agroforestri"), (42, 21.5, "agroforestri, permukiman"), (89, 6.5, "sawah")]
    for xx, zz, t in pl:
        ax.text(xx, zz + 1.3, t, fontsize=7.8, ha="center", color=WARNA["hijau"], style="italic")
    ax.text(0, -8.5, "Penggunaan lahan dominan diringkas dari tumpang susun data proyek; penampang tidak berskala.",
            fontsize=7.8, color=WARNA["abu"], style="italic")
    simpan(fig, MODUL, "M3-G03_toposekuen-subdas-bompon.png")


# ---------------------------------------------------------------- Gambar 3.4
def regang(a, m):
    lo, hi = np.percentile(a[m], [2, 98])
    return np.clip((a - lo) / (hi - lo), 0, 1)


def g04_data_penginderaan_jauh():
    s2 = gdal.Open(os.path.join(TERBUKA, "sentinel2_l2a_20250721_10m.tif"))
    kanal = {s2.GetRasterBand(i).GetDescription(): s2.GetRasterBand(i).ReadAsArray() for i in range(1, s2.RasterCount + 1)}
    gt = s2.GetGeoTransform()
    ext = (gt[0], gt[0] + gt[1] * s2.RasterXSize, gt[3] + gt[5] * s2.RasterYSize, gt[3])
    m = analisis.topeng_batas(s2.RasterXSize, s2.RasterYSize, gt)
    asli = np.dstack([regang(kanal[k], m) for k in ("B04", "B03", "B02")]) ** 0.8
    semu = np.dstack([regang(kanal[k], m) for k in ("B08", "B04", "B03")])
    dem = gdal.Open(os.path.join(TERBUKA, "copdem_glo30_30m.tif"))
    bayang = gdal.DEMProcessing("", dem, "hillshade", format="MEM", azimuth=315, altitude=45, computeEdges=True).ReadAsArray()
    gd = dem.GetGeoTransform()
    ext_d = (gd[0], gd[0] + gd[1] * dem.RasterXSize, gd[3] + gd[5] * dem.RasterYSize, gd[3])
    batas = gaya.baca_layer("batas_subdas")[0][1]
    fig, axs = plt.subplots(1, 3, figsize=(10, 6.4))
    fig.subplots_adjust(left=0.01, right=0.99, top=0.92, bottom=0.04, wspace=0.04)
    judul = ["(a) Sentinel-2 komposit warna asli\n(B4-B3-B2), 10 m", "(b) Sentinel-2 komposit inframerah\nsemu (B8-B4-B3), 10 m",
             "(c) Bayangan medan Copernicus DEM 30 m\ndan batas bentuklahan"]
    axs[0].imshow(asli, extent=ext, interpolation="nearest")
    axs[1].imshow(semu, extent=ext, interpolation="nearest")
    axs[2].imshow(bayang, extent=ext_d, cmap="gray", interpolation="bilinear")
    for atr, g in gaya.baca_layer("bentuklahan"):
        gaya.gambar_poligon(axs[2], g, fc="none", ec=gaya.WARNA_BENTUKLAHAN[atr["bentuklahan"]], lw=0.9)
    for ax, t in zip(axs, judul):
        gaya.gambar_poligon(ax, batas, fc="none", ec="#FFD54A", lw=1.4)
        ax.set_xlim(ext[0], ext[1])
        ax.set_ylim(ext[2], ext[3])
        ax.set_xticks([]), ax.set_yticks([])
        ax.set_title(t, fontsize=9.5)
    gaya.skala_batang(axs[0], ext[0] + 60, ext[2] + 70, 500, "500 m", tinggi=25)
    for s in axs[0].texts[-2:]:
        s.set_color("white")
    simpan(fig, MODUL, "M3-G04_data-penginderaan-jauh-subdas-bompon.png")


# ---------------------------------------------------------------- Gambar 3.5
def g05_unsur_interpretasi_foto_udara():
    lokasi = [
        ("(a) Sawah di dataran koluvial", 397400, 9164540, "pola petak teratur mengikuti kontur;\nrona cerah pada petak bera"),
        ("(b) Agroforestri di lereng perbukitan", 396860, 9163800, "tekstur kasar dari tajuk berlapis;\nrona gelap; tanah tidak tampak"),
        ("(c) Permukiman", 396760, 9164730, "pola mengelompok; bentuk atap\npersegi; asosiasi dengan jalan"),
        ("(d) Tegalan", 396420, 9165765, "pola baris bedengan; rona\nberagam sesuai fase tanaman"),
    ]
    fig, axs = plt.subplots(1, 4, figsize=(10, 3.6))
    fig.subplots_adjust(left=0.01, right=0.99, top=0.86, bottom=0.17, wspace=0.05)
    for ax, (judul, x, y, ket) in zip(axs, lokasi):
        ds = gdal.Translate("", FOTO_UDARA, format="MEM", projWin=[x - 100, y + 100, x + 100, y - 100], bandList=[1, 2, 3],
                            outputType=gdal.GDT_Byte, scaleParams=[[0, 255, 0, 255]], width=400, height=400)
        ax.imshow(ds.ReadAsArray().transpose(1, 2, 0), extent=(x - 100, x + 100, y - 100, y + 100))
        ax.set_xticks([]), ax.set_yticks([])
        ax.set_title(judul, fontsize=9, loc="left")
        ax.text(0.0, -0.05, ket, transform=ax.transAxes, fontsize=7.9, va="top", linespacing=1.15)
        ax.add_patch(Rectangle((x - 90, y - 92), 50, 5, fc="white", ec="#1F2933", lw=0.6))
        ax.text(x - 65, y - 84, "50 m", ha="center", fontsize=7.5, color="white", fontweight="bold")
    simpan(fig, MODUL, "M3-G05_unsur-interpretasi-foto-udara.png")


# ---------------------------------------------------------------- Gambar 3.6
def g06_tumpang_susun_dan_generalisasi(stat, kode, tersaring):
    lf, sl, pl, m, gt, ext = analisis.grid_lapisan()
    kode_unik = np.unique(kode[kode > 0])
    rng = np.random.default_rng(5)
    palet = plt.get_cmap("tab20")(np.linspace(0, 1, 20))
    warna = {k: palet[i % 20] * 0.85 + 0.15 * rng.random(4) for i, k in enumerate(rng.permutation(kode_unik))}

    def rgb(a):
        out = np.ones(a.shape + (3,))
        for k, w in warna.items():
            out[a == k] = w[:3]
        return np.clip(out, 0, 1)

    fig = plt.figure(figsize=(10, 6.2))
    gs = fig.add_gridspec(1, 4, width_ratios=[1, 1, 0.42, 1.25], left=0.01, right=0.98, top=0.88, bottom=0.10, wspace=0.04)
    batas = gaya.baca_layer("batas_subdas")[0][1]
    ts, ga = stat["tumpang_susun"], stat["generalisasi_otomatis"]["akhir"]
    pct_kecil = f"{ts['persen_poligon_kecil']:.1f}".replace(".", ",")
    for j, (arr, judul) in enumerate(((kode, f"(a) Tumpang susun otomatis\n{ts['jumlah_poligon']:,} poligon; ".replace(",", ".")
                                             + f"{pct_kecil}% < 0,4 ha"),
                                      (tersaring, f"(b) Generalisasi otomatis\n{ga['jumlah_poligon']} poligon; "
                                                  f"{ga['jumlah_kombinasi']} kombinasi"))):
        ax = fig.add_subplot(gs[0, j])
        ax.imshow(rgb(arr), extent=ext, interpolation="nearest")
        gaya.gambar_poligon(ax, batas, fc="none", ec=WARNA["navy"], lw=1.0)
        ax.set_xticks([]), ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)
        ax.set_title(judul, fontsize=9.5)
    ax = fig.add_subplot(gs[0, 3])
    sebelum = ga_l = stat["generalisasi_otomatis"]["lereng"]
    kelas = list(gaya.WARNA_LERENG)
    y = np.arange(len(kelas))
    a = [sebelum["luas_kelas_ha_sebelum"].get(k, 0) for k in kelas]
    b = [ga_l["luas_kelas_ha_sesudah"].get(k, 0) for k in kelas]
    ax.barh(y + 0.2, a, height=0.38, color=[gaya.WARNA_LERENG[k] for k in kelas], ec="#555555", lw=0.5, label="sebelum")
    ax.barh(y - 0.2, b, height=0.38, color="white", ec="#555555", lw=0.8, hatch="////", label="sesudah generalisasi")
    for yy, v1, v2 in zip(y, a, b):
        ax.text(v1 + 2, yy + 0.2, f"{v1:.1f}".replace(".", ","), va="center", fontsize=7.8)
        ax.text(v2 + 2, yy - 0.2, f"{v2:.1f}".replace(".", ","), va="center", fontsize=7.8)
    ax.set_yticks(y)
    ax.set_yticklabels([k.replace("-", "–") for k in kelas], fontsize=8.5)
    ax.invert_yaxis()
    ax.set_xlabel("Luas (ha)", fontsize=8.5)
    ax.tick_params(axis="x", labelsize=8)
    ax.set_xlim(0, 150)
    ax.legend(fontsize=8, loc="lower right")
    ax.set_title(f"(c) Luas kelas lereng sebelum dan sesudah\ngeneralisasi ({ga_l['persen_piksel_berubah_kelas']:.1f}% piksel berubah kelas)".replace(".", ","),
                 fontsize=9.5)
    simpan(fig, MODUL, "M3-G06_tumpang-susun-dan-generalisasi-otomatis.png")


# ---------------------------------------------------------------- Gambar 3.7
def g07_skala_dan_mla():
    batas = gaya.baca_layer("batas_subdas")[0][1]
    minx, maxx, miny, maxy = batas.GetEnvelope()
    fig, ax = plt.subplots(figsize=(8.6, 6.4))
    gaya.gambar_poligon(ax, batas, fc="#F4F1E8", ec=WARNA["navy"], lw=1.6)
    skala = [(10000, WARNA["teal"]), (25000, WARNA["oranye"]), (50000, WARNA["merah"]), (100000, WARNA["ungu"])]
    x0 = maxx + 250
    y = maxy - 120
    for sn, w in skala:
        mla = (sn / 1000) ** 2 / 250
        sisi = np.sqrt(mla * 1e4)
        ax.add_patch(Rectangle((x0, y - sisi), sisi, sisi, fc=w, alpha=0.35, ec=w, lw=1.4))
        lbl = f"1:{sn:,}".replace(",", ".")
        ax.text(x0 + sisi + 40, y - sisi / 2, f"{lbl}\nMLA {mla:g} ha".replace(".", ",", 1) if False else f"{lbl}\nMLA {str(mla).replace('.', ',')} ha\n(sisi ±{sisi:.0f} m)",
                va="center", fontsize=8.5, color=w)
        cx, cy = (minx + maxx) / 2 - 120, maxy - 700 - skala.index((sn, w)) * 650
        ax.add_patch(Rectangle((cx - sisi / 2, cy - sisi / 2), sisi, sisi, fc=w, alpha=0.55, ec=w, lw=1.0))
        y -= sisi + 260
    ax.text((minx + maxx) / 2, maxy + 70, "Sub-DAS Bompon (294,71 ha)", ha="center", fontsize=9.5, fontweight="bold", color=WARNA["navy"])
    ax.set_aspect("equal")
    ax.set_xlim(minx - 150, x0 + 1300)
    ax.set_ylim(miny - 240, maxy + 180)
    ax.axis("off")
    gaya.skala_batang(ax, (minx + maxx) / 2 - 250, miny - 190, 500, "500 m", tinggi=22)
    simpan(fig, MODUL, "M3-G07_skala-peta-dan-mla.png")


if __name__ == "__main__":
    gaya.atur()
    stat, kode, tersaring = analisis.main()
    g01_jenis_satuan_peta()
    g02_hierarki_taksonomi()
    g03_toposekuen_bompon()
    g04_data_penginderaan_jauh()
    g05_unsur_interpretasi_foto_udara()
    g06_tumpang_susun_dan_generalisasi(stat, kode, tersaring)
    g07_skala_dan_mla()
