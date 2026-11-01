"""Gambar Modul 3 — Remote Sensing untuk Delineasi Soil Mapping Units (SMU).

Jalankan: python3 Output/scripts/gambar_modul_3.py
Keluaran: Output/assets/modul-3/M3-Gxx_*.png
Semua gambar bersifat konseptual; Gambar 3.5 memakai data sintetis.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Patch, PathPatch, Polygon, Rectangle
from matplotlib.path import Path
from osgeo import gdal
from scipy import ndimage

import gaya
from gaya import WARNA, kanvas, kotak, nomor, panah, simpan

gdal.UseExceptions()
MODUL = "modul-3"


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
SATUAN_LERENG = [
    ("Interfluve", "proses pedologis oleh gerakan air\nvertikal di bawah permukaan"),
    ("Lereng rembesan", "eluviasi mekanis dan kimiawi oleh\naliran air lateral bawah permukaan"),
    ("Lereng rayapan cembung", "rayapan tanah"),
    ("Muka jatuhan", "jatuhan; bahan induk tersingkap"),
    ("Lereng tengah transportasional", "pengangkutan material ke bawah lereng\n(aliran, nendatan, longsoran, rayapan)"),
    ("Lereng kaki koluvial", "pengendapan kembali material\nkoluvial dari lereng di atasnya"),
    ("Kaki lereng aluvial", "pengendapan material aluvial\nyang dibawa sungai dari hulu"),
    ("Dinding saluran", "korasi (pengikisan) oleh aliran sungai"),
    ("Dasar saluran", "pengangkutan material searah\naliran sungai"),
]


def profil_sembilan_satuan():
    """Profil lereng skematis: daftar (x, y) per satuan."""
    seg = []
    x = np.linspace(0, 9, 20); seg.append((x, np.full_like(x, 60.0)))
    x = np.linspace(9, 22, 30); seg.append((x, 60 - (x - 9) * 2.5 / 13))
    x = np.linspace(22, 31, 30); seg.append((x, 57.5 - (x - 22) ** 2 * 8.5 / 81))
    x = np.linspace(31, 34, 10); seg.append((x, 49 - (x - 31) * 12 / 3))
    x = np.linspace(34, 56, 30); seg.append((x, 37 - (x - 34) * 20 / 22))
    x = np.linspace(56, 71, 30); seg.append((x, 8.5 + (71 - x) ** 2 * 8.5 / 225))
    x = np.linspace(71, 86, 20); seg.append((x, 8.5 - (x - 71) * 1.0 / 15))
    x = np.linspace(86, 88.5, 10); seg.append((x, 7.5 - (x - 86) * 5 / 2.5))
    x = np.linspace(88.5, 100, 20); seg.append((x, np.full_like(x, 2.5)))
    return seg


def g03_model_sembilan_satuan():
    fig, ax = kanvas(10, 7.0, (0, 100), (-52, 70))
    seg = profil_sembilan_satuan()
    xs = np.concatenate([s[0] for s in seg])
    ys = np.concatenate([s[1] for s in seg])
    ax.fill_between(xs, -4, ys, color="#E6D3B8", zorder=1)
    ax.fill_between(xs, -4, ys - 3.0, color="#CDB89A", zorder=1.2)
    ax.add_patch(Rectangle((88.5, -1.0), 11.5, 3.5, fc=WARNA["biru"], alpha=0.55, ec="none", zorder=2))
    warna = ["#7A4E2D", "#9B6235", "#B5763F", "#6B7280", "#D9A35F", "#9CC5A1", "#5E9E8A", "#3B82C4", "#1F3A5F"]
    for i, ((x, y), w) in enumerate(zip(seg, warna)):
        ax.plot(x, y, color=w, lw=4.5, solid_capstyle="butt", zorder=3)
        xm = x[len(x) // 2]
        ym = y[len(y) // 2]
        dx = {3: -3.6, 7: -2.8, 8: 1.5}.get(i, 0.0)
        nomor(ax, xm + dx, ym + 5.0, i + 1, warna=w, r=1.9, ukuran=9)
    ax.text(94.2, -2.4, "sungai", fontsize=7.5, ha="center", color="white", fontweight="bold", zorder=4)
    for i, (nama, proses) in enumerate(SATUAN_LERENG):
        kol, bar = divmod(i, 5)
        x0 = 1 + kol * 50
        y0 = -9.0 - bar * 8.6
        nomor(ax, x0 + 1.6, y0, i + 1, warna=warna[i], r=1.6, ukuran=8)
        ax.text(x0 + 4.2, y0 + 0.4, nama, fontsize=8.6, fontweight="bold", va="center", color=WARNA["teks"])
        ax.text(x0 + 4.2, y0 - 1.6, proses, fontsize=7.8, va="top", color=WARNA["abu"], linespacing=1.1)
    simpan(fig, MODUL, "M3-G03_model-sembilan-satuan-permukaan-lahan.png")


# ---------------------------------------------------------------- Gambar 3.4
def g04_mla_berbagai_skala():
    fig, ax = plt.subplots(figsize=(8.8, 4.9))
    ax.add_patch(Rectangle((0, 0), 1000, 1000, fc="#F4F1E8", ec=WARNA["navy"], lw=1.4))
    for v in range(100, 1000, 100):
        ax.plot([v, v], [0, 1000], color="white", lw=0.8)
        ax.plot([0, 1000], [v, v], color="white", lw=0.8)
    skala = [(10000, WARNA["teal"]), (25000, WARNA["oranye"]), (50000, WARNA["merah"]), (100000, WARNA["ungu"])]
    letak = {100000: (20, 20), 50000: (672, 20), 25000: (672, 356), 10000: (850, 356)}
    for sn, w in skala:
        mla = (sn / 1000) ** 2 / 250
        sisi = np.sqrt(mla * 1e4)
        ax.add_patch(Rectangle(letak[sn], sisi, sisi, fc=w, alpha=0.55, ec=w, lw=1.2))
    y = 950
    for sn, w in skala:
        mla = (sn / 1000) ** 2 / 250
        sisi = np.sqrt(mla * 1e4)
        jumlah = 100 / mla
        teks = (f"1:{sn:,}".replace(",", ".") + f"  —  MLA {str(round(mla, 3)).replace('.', ',')} ha "
                f"(sisi ±{sisi:.0f} m); {str(round(jumlah, 1)).replace('.0', '').replace('.', ',')} MLA per 100 ha")
        ax.add_patch(Rectangle((1060, y - 32), 40, 40, fc=w, alpha=0.55, ec=w))
        ax.text(1120, y - 12, teks, va="center", fontsize=8.8, color=WARNA["teks"])
        y -= 90
    ax.text(500, -60, "Kotak acuan 1 × 1 km (100 ha); garis bantu setiap 100 m", ha="center", fontsize=8.5, color=WARNA["abu"])
    ax.set_xlim(-20, 2300)
    ax.set_ylim(-100, 1020)
    ax.set_aspect("equal")
    ax.axis("off")
    simpan(fig, MODUL, "M3-G04_mla-pada-berbagai-skala.png")


# ---------------------------------------------------------------- Gambar 3.5
def medan_sintetis(n=240, seed=7):
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:n, 0:n] / n
    z = 60 * np.sin(2.2 * np.pi * xx + 0.6) * np.cos(1.4 * np.pi * yy) + 40 * yy
    z += ndimage.gaussian_filter(rng.normal(0, 1, (n, n)), 12) * 220
    mikro = ndimage.gaussian_filter(rng.normal(0, 1, (n, n)), 1.2) * 2.2   # relief mikro, mis. teras
    return z, z + mikro


def kelaskan(a, q):
    return np.digitize(a, np.quantile(a, q)) + 1


def hitung_patch(kode):
    struktur = np.ones((3, 3), bool)
    ukuran = []
    for k in np.unique(kode):
        lab, n = ndimage.label(kode == k, structure=struktur)
        ukuran.extend(np.bincount(lab.ravel())[1:].tolist())
    return np.array(ukuran)


def saring_ulang(kode, ambang):
    cur = kode.astype(np.int32)
    drv = gdal.GetDriverByName("MEM")
    for _ in range(50):
        src = drv.Create("", cur.shape[1], cur.shape[0], 1, gdal.GDT_Int32)
        src.GetRasterBand(1).WriteArray(cur)
        dst = drv.Create("", cur.shape[1], cur.shape[0], 1, gdal.GDT_Int32)
        gdal.SieveFilter(src.GetRasterBand(1), None, dst.GetRasterBand(1), ambang, 8)
        nxt = dst.GetRasterBand(1).ReadAsArray()
        if (nxt == cur).all():
            break
        cur = nxt
    return cur


def g05_ilustrasi_tumpang_susun():
    z_halus, z_rinci = medan_sintetis()
    bentuk = kelaskan(ndimage.gaussian_filter(z_halus, 6), [0.25, 0.5, 0.75])
    gy, gx = np.gradient(z_rinci)
    lereng = kelaskan(np.hypot(gx, gy), [0.3, 0.6, 0.85])
    kode = bentuk * 10 + lereng
    ambang = 150
    u0 = hitung_patch(kode)
    umum = saring_ulang(kode, ambang)
    u1 = hitung_patch(umum)
    rng = np.random.default_rng(3)
    palet = plt.get_cmap("tab20")(np.linspace(0, 1, 20))[:, :3]
    unik = np.unique(kode)
    peta = {k: palet[i % 20] * 0.85 + 0.15 * rng.random(3) for i, k in enumerate(rng.permutation(unik))}

    def rgb(a):
        out = np.ones(a.shape + (3,))
        for k, w in peta.items():
            out[a == k] = np.clip(w, 0, 1)
        return out

    fig, axs = plt.subplots(2, 2, figsize=(7.0, 7.9))
    fig.subplots_adjust(left=0.01, right=0.99, top=0.94, bottom=0.035, wspace=0.05, hspace=0.14)
    axs = axs.ravel()
    coklat = plt.get_cmap("YlOrBr")
    judul = [
        "(a) Satuan bentuklahan\n(4 kelas, batas halus)",
        "(b) Kelas lereng dari DEM\nresolusi tinggi (4 kelas)",
        f"(c) Tumpang susun (a) dan (b)\n{len(u0):,} poligon; {np.mean(u0 < ambang) * 100:.0f}% < MLA".replace(",", "."),
        f"(d) Generalisasi otomatis\n{len(u1)} poligon; semua ≥ MLA",
    ]
    axs[0].imshow(bentuk, cmap=coklat, vmin=0, vmax=5, interpolation="nearest")
    axs[1].imshow(lereng, cmap="RdYlGn_r", vmin=0.5, vmax=4.5, interpolation="nearest")
    axs[2].imshow(rgb(kode), interpolation="nearest")
    axs[3].imshow(rgb(umum), interpolation="nearest")
    for a, t in zip(axs, judul):
        a.set_xticks([]), a.set_yticks([])
        a.set_title(t, fontsize=10.5)
    fig.text(0.5, 0.008, "Data sintetis untuk ilustrasi; MLA ditetapkan 150 piksel", ha="center", fontsize=9,
             style="italic", color=WARNA["abu"])
    simpan(fig, MODUL, "M3-G05_ilustrasi-tumpang-susun-dan-generalisasi.png")


if __name__ == "__main__":
    gaya.atur()
    g01_jenis_satuan_peta()
    g02_hierarki_taksonomi()
    g03_model_sembilan_satuan()
    g04_mla_berbagai_skala()
    g05_ilustrasi_tumpang_susun()
