"""Gambar Modul 5 — Bare Soil Detection & Information Extraction.

Jalankan: python3 Output/scripts/gambar_modul_5.py
Keluaran: Output/assets/modul-5/M5-Gxx_*.png
Semua gambar bersifat konseptual. Spektrum pada Gambar 5.1 adalah ilustrasi skematis, sedangkan nilai indeks
pada Gambar 5.1(b) dan deret waktu pada Gambar 5.3 dihitung dari data sintetis.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.ticker import FuncFormatter, MultipleLocator
from scipy.interpolate import PchipInterpolator

import gaya
from gaya import WARNA, kanvas, kotak, panah, simpan

MODUL = "modul-5"
KOMA1 = FuncFormatter(lambda v, _: f"{v:.1f}".replace(".", ","))
KOMA2 = FuncFormatter(lambda v, _: f"{v:.2f}".replace(".", ","))
PERSEN = FuncFormatter(lambda v, _: f"{v:.0f}%")

# Kanal Sentinel-2 MSI yang dipakai indeks (batas bawah–atas, µm; Drusch et al., 2012)
KANAL = {"B2": (0.4575, 0.5225), "B3": (0.5425, 0.5775), "B4": (0.650, 0.680), "B8": (0.7845, 0.8995),
         "B11": (1.565, 1.655), "B12": (2.100, 2.280)}

# Spektrum skematis (titik kendali panjang gelombang µm, pantulan 0–1)
SPEKTRUM = {
    "Tanah terbuka kering": (WARNA["oranye"], "-",
        [(0.40, 0.09), (0.49, 0.12), (0.56, 0.16), (0.665, 0.20), (0.75, 0.24), (0.84, 0.27), (1.00, 0.31), (1.20, 0.34),
         (1.34, 0.355), (1.40, 0.33), (1.45, 0.335), (1.61, 0.36), (1.80, 0.365), (1.90, 0.335), (1.97, 0.34),
         (2.10, 0.345), (2.20, 0.32), (2.30, 0.325), (2.45, 0.31)]),
    "Tanah terbuka lembap": (WARNA["tanah"], "-",
        [(0.40, 0.05), (0.49, 0.07), (0.56, 0.09), (0.665, 0.12), (0.75, 0.14), (0.84, 0.16), (1.00, 0.18), (1.20, 0.195),
         (1.34, 0.20), (1.40, 0.15), (1.45, 0.155), (1.61, 0.20), (1.80, 0.205), (1.90, 0.12), (1.97, 0.125),
         (2.10, 0.175), (2.20, 0.165), (2.30, 0.165), (2.45, 0.15)]),
    "Vegetasi hijau": (WARNA["hijau"], "-",
        [(0.40, 0.03), (0.49, 0.04), (0.55, 0.085), (0.60, 0.06), (0.665, 0.04), (0.69, 0.05), (0.72, 0.22), (0.76, 0.42),
         (0.84, 0.45), (1.00, 0.46), (1.20, 0.42), (1.34, 0.38), (1.40, 0.22), (1.45, 0.17), (1.61, 0.22), (1.70, 0.22),
         (1.80, 0.19), (1.90, 0.07), (1.97, 0.06), (2.10, 0.10), (2.20, 0.11), (2.30, 0.10), (2.45, 0.07)]),
    "Serasah dan sisa tanaman kering": ("#C99A2E", "--",
        [(0.40, 0.07), (0.49, 0.10), (0.56, 0.14), (0.665, 0.18), (0.75, 0.24), (0.84, 0.30), (1.00, 0.34), (1.20, 0.37),
         (1.34, 0.37), (1.40, 0.33), (1.45, 0.34), (1.61, 0.38), (1.72, 0.37), (1.80, 0.36), (1.90, 0.30), (1.97, 0.31),
         (2.03, 0.31), (2.10, 0.25), (2.17, 0.30), (2.22, 0.29), (2.30, 0.27), (2.45, 0.24)]),
}


def kurva(titik, x):
    xs, ys = zip(*titik)
    return PchipInterpolator(xs, ys)(x)


def pantulan_kanal(titik):
    """Rata-rata pantulan skematis di dalam rentang setiap kanal Sentinel-2."""
    hasil = {}
    for nama, (a, b) in KANAL.items():
        xx = np.linspace(a, b, 60)
        hasil[nama] = float(np.mean(kurva(titik, xx)))
    return hasil


def ndvi(k):
    return (k["B8"] - k["B4"]) / (k["B8"] + k["B4"])


def nbr2(k):
    return (k["B11"] - k["B12"]) / (k["B11"] + k["B12"])


# ---------------------------------------------------------------- Gambar 5.1
def g01_spektrum_dan_campuran():
    x = np.linspace(0.40, 2.45, 1200)
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(10, 4.4), gridspec_kw=dict(width_ratios=[1.45, 1.0], wspace=0.28))

    for a, b in ((1.35, 1.45), (1.80, 1.95)):
        ax.axvspan(a, b, color=WARNA["abu_muda"], zorder=0)
    for nama, (a, b) in KANAL.items():
        ax.add_patch(Rectangle((a, 0.555), b - a, 0.022, fc=WARNA["navy"], ec="none", clip_on=False))
        ax.text((a + b) / 2, 0.583, nama, ha="center", va="bottom", fontsize=7, color=WARNA["navy"], clip_on=False)
    for nama, (warna, gaya_garis, titik) in SPEKTRUM.items():
        ax.plot(x, kurva(titik, x), color=warna, ls=gaya_garis, lw=2.0, label=nama, zorder=3)
    ax.annotate("serapan klorofil", xy=(0.672, 0.045), xytext=(0.76, 0.062), fontsize=7.4, color=WARNA["hijau"],
                arrowprops=dict(arrowstyle="-|>", color=WARNA["hijau"], lw=0.8))
    ax.annotate("serapan selulosa–lignin\n(±2,1 µm)", xy=(2.10, 0.252), xytext=(1.72, 0.47), fontsize=7.4,
                color="#9A7A1A", arrowprops=dict(arrowstyle="-|>", color="#9A7A1A", lw=0.8))
    ax.set_xlim(0.40, 2.45)
    ax.set_ylim(0, 0.55)
    ax.xaxis.set_major_locator(MultipleLocator(0.5))
    ax.xaxis.set_major_formatter(KOMA1)
    ax.set_yticks([])
    ax.set_xlabel("Panjang gelombang (µm)")
    ax.set_ylabel("Pantulan relatif")
    ax.legend(loc="lower left", bbox_to_anchor=(0.315, 0.0), fontsize=7.6)
    ax.text(0.99, 0.015, "Ilustrasi skematis", transform=ax.transAxes, ha="right", va="bottom", fontsize=7.6,
            style="italic", color=WARNA["abu"])
    ax.text(-0.02, 1.07, "(a)", transform=ax.transAxes, fontsize=10, fontweight="bold", color=WARNA["navy"])

    # (b) nilai indeks pada campuran tanah kering dengan vegetasi hijau atau serasah (pencampuran linear)
    tanah = pantulan_kanal(SPEKTRUM["Tanah terbuka kering"][2])
    hijau = pantulan_kanal(SPEKTRUM["Vegetasi hijau"][2])
    serasah = pantulan_kanal(SPEKTRUM["Serasah dan sisa tanaman kering"][2])
    f = np.linspace(0, 1, 101)

    def campur(lain, fr):
        return {k: (1 - fr) * tanah[k] + fr * lain[k] for k in tanah}

    seri = [(hijau, ndvi, WARNA["hijau"], "-", "NDVI, tanah + vegetasi hijau"),
            (serasah, ndvi, "#9A7A1A", "-", "NDVI, tanah + serasah"),
            (serasah, nbr2, "#9A7A1A", "--", "NBR2, tanah + serasah")]
    for lain, fungsi, warna, gaya_garis, label in seri:
        bx.plot(f * 100, [fungsi(campur(lain, v)) for v in f], color=warna, ls=gaya_garis, lw=1.9, label=label)
    bx.axhline(0.25, color=WARNA["abu"], lw=0.9, ls=":")
    bx.text(99, 0.262, "NDVI = 0,25", ha="right", fontsize=7.2, color=WARNA["abu"])
    bx.axhline(0.10, color=WARNA["abu"], lw=0.9, ls=":")
    bx.text(99, 0.112, "NBR2 = 0,10", ha="right", fontsize=7.2, color=WARNA["abu"])
    bx.axvspan(0, 20, color=WARNA["teal"], alpha=0.10, lw=0)
    bx.text(10, 0.80, "tutupan\n≤ 20%", ha="center", fontsize=7.4, color=WARNA["teal"])
    bx.set_xlim(0, 100)
    bx.set_ylim(0, 0.9)
    bx.xaxis.set_major_formatter(PERSEN)
    bx.yaxis.set_major_formatter(KOMA1)
    bx.set_xlabel("Fraksi penutup di dalam piksel")
    bx.set_ylabel("Nilai indeks")
    bx.legend(loc="upper left", bbox_to_anchor=(0.16, 1.0), fontsize=7.4)
    bx.text(0.99, 0.015, "Data sintetis", transform=bx.transAxes, ha="right", va="bottom", fontsize=7.6,
            style="italic", color=WARNA["abu"])
    bx.text(-0.02, 1.07, "(b)", transform=bx.transAxes, fontsize=10, fontweight="bold", color=WARNA["navy"])
    simpan(fig, MODUL, "M5-G01_spektrum-tanah-vegetasi-serasah.png")


# ---------------------------------------------------------------- Gambar 5.2
def g02_garis_tanah():
    fig, ax = plt.subplots(figsize=(6.6, 5.4))
    r = np.linspace(0.0, 0.42, 50)
    ax.plot(r, 0.02 + 1.12 * r, color=WARNA["tanah"], lw=2.2, zorder=3)
    ax.text(0.385, 0.475, "garis tanah", rotation=40, fontsize=8.6, color=WARNA["tanah"], ha="center")
    for rr, label in ((0.06, "tanah basah\natau gelap"), (0.33, "tanah kering\natau cerah")):
        ax.scatter([rr], [0.02 + 1.12 * rr], s=70, color=WARNA["tanah"], zorder=4)
        ax.text(rr + 0.012, 0.02 + 1.12 * rr - 0.045, label, fontsize=8, color=WARNA["tanah"], va="top")
    rng = np.random.default_rng(4)
    rv = rng.normal(0.045, 0.012, 60)
    nv = rng.normal(0.44, 0.04, 60)
    ax.scatter(rv, nv, s=14, color=WARNA["hijau"], alpha=0.75, zorder=3)
    ax.text(0.075, 0.50, "vegetasi hijau\nrapat", fontsize=8.4, color=WARNA["hijau"])
    rs = rng.normal(0.21, 0.022, 40)
    ns = 0.06 + 1.18 * rs + rng.normal(0, 0.012, 40)
    ax.scatter(rs, ns, s=12, marker="s", color="#E3B84A", ec="#9A7A1A", lw=0.4, zorder=3)
    ax.text(0.245, 0.215, "serasah dan sisa\ntanaman kering", fontsize=8, color="#9A7A1A")
    panah(ax, 0.20, 0.25, 0.07, 0.40, warna=WARNA["hijau"], lw=1.1, putus=True, skala=10)
    ax.text(0.155, 0.355, "makin banyak\nvegetasi hijau", fontsize=7.4, color=WARNA["hijau"])
    for v in (0.25, 0.5, 0.75):
        kemiringan = (1 + v) / (1 - v)
        rr = np.linspace(0, 0.6 / kemiringan, 20)
        ax.plot(rr, kemiringan * rr, color=WARNA["abu"], lw=0.8, ls=":", zorder=2)
        ax.text(0.6 / kemiringan + 0.004, 0.6, f"NDVI = {str(v).replace('.', ',')}", fontsize=7.4, color=WARNA["abu"],
                rotation=np.degrees(np.arctan(kemiringan * 0.88)) - 4, va="top")
    ax.set_xlim(0, 0.45)
    ax.set_ylim(0, 0.62)
    ax.xaxis.set_major_formatter(KOMA2)
    ax.yaxis.set_major_formatter(KOMA2)
    ax.set_xlabel("Pantulan kanal merah")
    ax.set_ylabel("Pantulan kanal inframerah dekat")
    ax.text(0.99, 0.015, "Diagram konseptual; titik bersifat ilustratif", transform=ax.transAxes, ha="right",
            va="bottom", fontsize=7.6, style="italic", color=WARNA["abu"])
    simpan(fig, MODUL, "M5-G02_garis-tanah-ruang-merah-nir.png")


# ---------------------------------------------------------------- Gambar 5.3
def g03_deret_waktu_peremajaan():
    rng = np.random.default_rng(12)
    t = np.arange(-6, 37, 0.5)
    # fraksi penutup sintetis: tajuk tua (sebelum 0), tumbang dan persiapan lahan (0–3 bulan),
    # kacangan penutup tanah menutup dalam ±5–6 bulan setelah ditanam, tajuk muda menutup ±2–3 tahun
    tajuk = np.where(t < 0, 0.85, np.clip((t - 3) / 33, 0, 1) ** 1.6 * 0.8)
    kacangan = np.where(t < 3, 0.0, np.clip((t - 3) / 5.5, 0, 1) * 0.9)
    kacangan = kacangan * (1 - 0.6 * np.clip((t - 24) / 12, 0, 1))
    hijau = np.clip(np.maximum(tajuk, 0) + kacangan * (1 - tajuk), 0, 0.95)
    serasah = np.where((t >= 0) & (t < 3), 0.35, np.where(t >= 3, 0.35 * np.exp(-(t - 3) / 6), 0.0)) * (1 - hijau)
    tanah = np.clip(1 - hijau - serasah, 0, 1)
    tk = pantulan_kanal(SPEKTRUM["Tanah terbuka kering"][2])
    hj = pantulan_kanal(SPEKTRUM["Vegetasi hijau"][2])
    sr = pantulan_kanal(SPEKTRUM["Serasah dan sisa tanaman kering"][2])

    def bsi(k):
        return ((k["B11"] + k["B4"]) - (k["B8"] + k["B2"])) / ((k["B11"] + k["B4"]) + (k["B8"] + k["B2"]))

    nd, bs = [], []
    for a, b, c in zip(tanah, hijau, serasah):
        k = {n: a * tk[n] + b * hj[n] + c * sr[n] for n in tk}
        nd.append(ndvi(k))
        bs.append(bsi(k))
    nd = np.array(nd) + rng.normal(0, 0.015, len(t))
    bs = np.array(bs) + rng.normal(0, 0.008, len(t))
    awan = rng.random(len(t)) < 0.40

    fig, ax = plt.subplots(figsize=(10, 4.4))
    fase = [(-6, 0, "tegakan tua\n(tajuk menutup)", "#E6F0DC"), (0, 3, "tumbang,\ncincang,\nrumpuk", "#F3E3CF"),
            (3, 9, "kacangan\npenutup tanah\ntumbuh", "#EAF3E2"), (9, 36, "tanaman muda; tajuk berkembang hingga menutup", "#F5F7FA")]
    for a, b, label, isi in fase:
        ax.axvspan(a, b, color=isi, zorder=0)
        ax.text((a + b) / 2, 1.03, label, ha="center", va="bottom", fontsize=7.4, color=WARNA["teks"], linespacing=1.0)
    ax.axvspan(0.5, 6.0, ymin=0.06, ymax=0.09, color=WARNA["oranye"], lw=0)
    ax.text(3.25, -0.355, "jendela tanah terbuka", ha="center", va="bottom", fontsize=7.6, color=WARNA["oranye"],
            fontweight="bold")
    ax.plot(t[~awan], nd[~awan], "o-", color=WARNA["hijau"], ms=3.2, lw=1.2, label="NDVI (perekaman cerah)")
    ax.plot(t[~awan], bs[~awan], "s-", color=WARNA["oranye"], ms=3.0, lw=1.2, label="BSI (perekaman cerah)")
    ax.scatter(t[awan], np.full(awan.sum(), -0.465), marker="x", s=13, color=WARNA["abu"], label="tertutup awan, dibuang")
    ax.axhline(0, color=WARNA["abu"], lw=0.6)
    ax.set_xlim(-6, 36)
    ax.set_ylim(-0.5, 1.0)
    ax.xaxis.set_major_locator(MultipleLocator(6))
    ax.yaxis.set_major_formatter(KOMA1)
    ax.set_xlabel("Bulan sejak penumbangan")
    ax.set_ylabel("Nilai indeks")
    ax.legend(loc="center right", bbox_to_anchor=(1.0, 0.40), fontsize=7.8)
    ax.text(0.99, 0.965, "Ilustrasi konseptual dengan data sintetis", transform=ax.transAxes, ha="right", va="top",
            fontsize=7.6, style="italic", color=WARNA["abu"])
    simpan(fig, MODUL, "M5-G03_deret-waktu-indeks-blok-peremajaan.png")


# ---------------------------------------------------------------- Gambar 5.4
def g04_alur_deteksi():
    fig, ax = kanvas(10, 4.3, (0, 104), (2, 45))
    w, h = 18.0, 10.0

    def node(x, y, teks, isi=WARNA["putih"], warna=WARNA["navy"], tebal=False, lebar=w, tinggi=h):
        kotak(ax, x, y, lebar, tinggi, teks, isi=isi, warna=warna, ukuran=8.1, tebal=tebal, r=0.8, lw=1.1)

    def ke(x1, y1, x2, y2):
        panah(ax, x1, y1, x2, y2, warna=WARNA["abu"], lw=1.1, skala=10)

    node(1, 33, "Deret waktu citra\npantulan permukaan\n(mis. Sentinel-2 L2A)", isi=WARNA["latar"], warna=WARNA["abu"])
    node(22.5, 33, "Penyaringan awan\ndan bayangan\n(lapisan mutu)")
    node(44, 33, "Indeks per\nperekaman:\nNDVI, NBR2, BSI")
    node(65.5, 33, "Penandaan piksel\ntanah terbuka\ndengan nilai ambang", isi=WARNA["teal"], warna=WARNA["teal"])
    ax.texts[-1].set_color("white")
    node(85, 33, "Agregasi\nmultitemporal:\nmedian, piksel\nterbersih", lebar=18.0)
    ke(19.0, 38, 22.5, 38), ke(40.5, 38, 44, 38), ke(62.0, 38, 65.5, 38), ke(83.5, 38, 85, 38)

    node(85, 4, "Produk: komposit\npantulan tanah\nterbuka dan\nfrekuensi terbuka", isi="#DCEAF7")
    node(46, 4, "Pemeriksaan mutu:\npola spektrum, garis\ntanah, citra resolusi\ntinggi, cek lapangan")
    node(46, 19.5, "Penyesuaian ambang\nsesuai kondisi\nsetempat", isi=WARNA["latar"], warna=WARNA["abu"], tinggi=9.0)
    node(1, 4, "Estimasi sifat tanah\n(Modul 4) dan\nkovariat DSM\n(Modul 8)", isi="#DCEAF7")
    ke(94, 33, 94, 14.1)
    ke(85, 9, 64.1, 9)
    ke(46, 9, 19.1, 9)
    ax.text(32.5, 10.0, "lolos", ha="center", va="bottom", fontsize=7.6, color=WARNA["abu"], style="italic")
    ke(55, 14, 55, 19.4)
    ax.text(55.8, 16.2, "tidak lolos", ha="left", va="center", fontsize=7.6, color=WARNA["abu"], style="italic")
    panah(ax, 64.1, 24.0, 74.5, 32.9, warna=WARNA["abu"], lw=1.0, putus=True, skala=9)
    ax.text(70.6, 26.0, "umpan balik", fontsize=7.4, color=WARNA["abu"], rotation=40)
    simpan(fig, MODUL, "M5-G04_alur-deteksi-tanah-terbuka.png")


if __name__ == "__main__":
    gaya.atur()
    g01_spektrum_dan_campuran()
    g02_garis_tanah()
    g03_deret_waktu_peremajaan()
    g04_alur_deteksi()
