"""Gambar Modul 1 — Dasar-dasar Remote Sensing dan Digital Soil Mapping.

Jalankan: python3 Output/scripts/gambar_modul_1.py
Keluaran: Output/assets/modul-1/M1-Gxx_*.png
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, ConnectionPatch, Polygon, Rectangle

import gaya
from gaya import WARNA, kanvas, kotak, nomor, panah, simpan

MODUL = "modul-1"


# ---------------------------------------------------------------- utilitas lokal
def gelombang(ax, p1, p2, warna, amp=0.6, siklus=5, lw=1.4, kepala=True, zorder=3):
    """Garis bergelombang dari p1 ke p2 dengan kepala panah di p2."""
    p1, p2 = np.array(p1, float), np.array(p2, float)
    d = p2 - p1
    panjang = np.hypot(*d)
    u = d / panjang
    n = np.array([-u[1], u[0]])
    t = np.linspace(0, 1, 200)
    redam = np.clip((1 - t) / 0.12, 0, 1)  # gelombang mereda menjelang ujung
    pts = p1 + np.outer(t, d) + np.outer(amp * np.sin(2 * np.pi * siklus * t) * redam, n)
    ax.plot(pts[:, 0], pts[:, 1], color=warna, lw=lw, zorder=zorder, solid_capstyle="round")
    if kepala:
        panah(ax, *(p2 - u * 1.2), *p2, warna=warna, lw=lw, skala=11, zorder=zorder)


def matahari(ax, x, y, r=3.2):
    for a in np.linspace(0, 2 * np.pi, 12, endpoint=False):
        ax.plot([x + 1.25 * r * np.cos(a), x + 1.7 * r * np.cos(a)],
                [y + 1.25 * r * np.sin(a), y + 1.7 * r * np.sin(a)], color=WARNA["kuning"], lw=1.6, zorder=3)
    ax.add_patch(Circle((x, y), r, fc=WARNA["kuning"], ec="#E0A82E", lw=1, zorder=4))


def satelit(ax, x, y, s=1.0):
    ax.add_patch(Rectangle((x - 1.6 * s, y - 1.2 * s), 3.2 * s, 2.4 * s, fc="#C9CED6", ec=WARNA["navy"], lw=1, zorder=5))
    for arah in (-1, 1):
        x0 = x + arah * 1.6 * s if arah > 0 else x - 1.6 * s - 4.6 * s
        ax.add_patch(Rectangle((x0, y - 0.9 * s), 4.6 * s, 1.8 * s, fc="#2F5D8C", ec=WARNA["navy"], lw=0.8, zorder=5))
        for k in range(1, 4):
            ax.plot([x0 + k * 1.15 * s] * 2, [y - 0.9 * s, y + 0.9 * s], color="#9DB7D3", lw=0.5, zorder=6)
    ax.add_patch(Polygon([[x - 0.9 * s, y - 1.2 * s], [x + 0.9 * s, y - 1.2 * s], [x, y - 2.3 * s]],
                         fc=WARNA["navy"], ec="none", zorder=5))


def sensor(ax, x, y, w=4.0, h=2.2):
    """Sensor generik berbentuk trapesium menghadap ke bawah."""
    ax.add_patch(Polygon([[x - w / 2, y + h / 2], [x + w / 2, y + h / 2], [x + w / 3, y - h / 2], [x - w / 3, y - h / 2]],
                         fc="#C9CED6", ec=WARNA["navy"], lw=1.1, zorder=5))


def pohon(ax, x, y, s=1.0):
    ax.add_patch(Rectangle((x - 0.25 * s, y), 0.5 * s, 2.0 * s, fc="#6B4A2B", ec="none", zorder=4))
    for dx, dy, r in [(0, 3.0, 1.5), (-1.0, 2.4, 1.1), (1.0, 2.4, 1.1)]:
        ax.add_patch(Circle((x + dx * s, y + dy * s), r * s, fc=WARNA["hijau"], ec="#3A7A20", lw=0.6, zorder=4))


def panjang_gel_ke_rgb(nm):
    """Pendekatan warna untuk panjang gelombang tampak (380–750 nm)."""
    if nm < 440:
        r, g, b = -(nm - 440) / (440 - 380), 0.0, 1.0
    elif nm < 490:
        r, g, b = 0.0, (nm - 440) / (490 - 440), 1.0
    elif nm < 510:
        r, g, b = 0.0, 1.0, -(nm - 510) / (510 - 490)
    elif nm < 580:
        r, g, b = (nm - 510) / (580 - 510), 1.0, 0.0
    elif nm < 645:
        r, g, b = 1.0, -(nm - 645) / (645 - 580), 0.0
    else:
        r, g, b = 1.0, 0.0, 0.0
    if nm < 420:
        f = 0.3 + 0.7 * (nm - 380) / (420 - 380)
    elif nm > 700:
        f = 0.3 + 0.7 * (750 - nm) / (750 - 700)
    else:
        f = 1.0
    return (r * f, g * f, b * f)


# ---------------------------------------------------------------- Gambar 1.1
def g01_alur_penginderaan_jauh():
    fig, ax = kanvas(10, 5.0, (0, 100), (-6, 47))
    ax.add_patch(Rectangle((0, 12), 74, 35, fc="#EEF5FB", ec="none", zorder=0))
    rng = np.random.default_rng(7)
    ax.scatter(rng.uniform(1, 73, 160), rng.uniform(17, 28, 160), s=3, color="#A9C1DA", zorder=1)
    ax.text(72.5, 22.5, "Atmosfer\n(hamburan dan serapan)", ha="right", va="center", fontsize=8.5,
            color=WARNA["abu"], style="italic", zorder=2,
            bbox=dict(boxstyle="round,pad=0.25", fc="#EEF5FB", ec="none"))
    nomor(ax, 59.0, 22.5, 2)

    # permukaan bumi
    segmen = [(10, 26, WARNA["hijau_muda"], "Vegetasi"), (26, 42, WARNA["tanah_muda"], "Tanah"), (42, 58, "#BFD9EE", "Air")]
    for x0, x1, isi, label in segmen:
        ax.add_patch(Rectangle((x0, 0), x1 - x0, 12, fc=isi, ec="white", lw=1.5, zorder=2))
        ax.text((x0 + x1) / 2, -2.4, label, ha="center", va="center", fontsize=9, fontweight="bold")
    for xp in (13, 17, 21):
        pohon(ax, xp, 6.5, 1.0)
    for k in range(5):
        ax.plot([27.5 + 3 * k, 29.5 + 3 * k], [4, 9], color=WARNA["tanah"], lw=1.4, zorder=3)
    for k, yy in enumerate((3.5, 6.5, 9.5)):
        xs = np.linspace(43, 57, 80)
        ax.plot(xs, yy + 0.4 * np.sin(xs * 1.4 + k), color=WARNA["biru"], lw=1, zorder=3)
    ax.add_patch(Rectangle((0, 0), 10, 12, fc="#E9E3D6", ec="white", lw=1.5, zorder=2))
    ax.add_patch(Rectangle((58, 0), 16, 12, fc="#E9E3D6", ec="white", lw=1.5, zorder=2))
    ax.text(34, -5.0, "Objek di permukaan bumi", ha="center", va="center", fontsize=9, color=WARNA["navy"])
    nomor(ax, 21.5, -5.0, 3)

    # sumber energi dan sensor
    matahari(ax, 8, 39)
    ax.text(14.2, 42.5, "Sumber energi\n(radiasi matahari)", ha="left", va="center", fontsize=9)
    nomor(ax, 14.2, 37.6, 1)
    satelit(ax, 60, 40, 0.9)
    ax.text(60, 45.2, "Sensor pada wahana (satelit)", ha="center", va="center", fontsize=9)
    nomor(ax, 47.5, 45.2, 4)

    # lintasan energi
    for xt in (18, 34, 50):
        panah(ax, 10.5, 35.5, xt, 12.3, warna=WARNA["oranye"], lw=1.5)
    panah(ax, 14.6, 26.0, 9.5, 29.5, warna=WARNA["oranye"], lw=1.0, putus=True, skala=9)
    ax.text(5.0, 25.5, "hamburan", fontsize=7.5, color=WARNA["oranye"], ha="center")
    for xs, lebar in ((18, 2.4), (34, 1.6), (50, 0.8)):
        panah(ax, xs, 12.3, 59.0, 36.8, warna=WARNA["teal"], lw=lebar)
    ax.text(20.5, 15.4, "pantulan", fontsize=7.5, color=WARNA["teal"], rotation=37)
    panah(ax, 36.0, 11.5, 37.4, 5.0, warna=WARNA["tanah"], lw=1.1, skala=9)
    ax.text(38.3, 7.0, "serapan", fontsize=7.5, color=WARNA["tanah"])
    panah(ax, 52.0, 11.5, 53.2, 2.0, warna=WARNA["biru"], lw=1.1, putus=True, skala=9)
    ax.text(54.0, 4.0, "transmisi", fontsize=7.5, color=WARNA["biru"])

    # data dan informasi
    kotak(ax, 77, 25, 22, 20, isi=WARNA["latar"], warna=WARNA["abu"], lw=0.8)
    ax.text(88, 42.6, "Data", ha="center", fontsize=9.5, fontweight="bold", color=WARNA["navy"])
    nomor(ax, 80.2, 42.6, 5)
    nilai = np.array([[0.2, 0.3, 0.5, 0.7, 0.8], [0.3, 0.4, 0.6, 0.8, 0.9], [0.5, 0.5, 0.4, 0.6, 0.7], [0.7, 0.6, 0.3, 0.2, 0.3]])
    cmap = plt.get_cmap("Blues")
    for i in range(4):
        for j in range(5):
            ax.add_patch(Rectangle((80.5 + j * 3.0, 37.5 - i * 2.6), 2.9, 2.5, fc=cmap(0.25 + 0.7 * nilai[i, j]), ec="white", lw=0.6, zorder=4))
    ax.text(88, 26.6, "nilai digital/reflektansi\nper piksel", ha="center", va="bottom", fontsize=7.8, color=WARNA["abu"])
    kotak(ax, 77, 1, 22, 20, isi=WARNA["latar"], warna=WARNA["abu"], lw=0.8)
    ax.text(88, 18.6, "Informasi", ha="center", fontsize=9.5, fontweight="bold", color=WARNA["navy"])
    nomor(ax, 80.2, 18.6, 6)
    ax.add_patch(Polygon([[80.5, 6], [86, 5.5], [88, 10], [85, 15.5], [80.5, 15]], fc=WARNA["hijau"], ec="white", lw=0.8, zorder=4))
    ax.add_patch(Polygon([[86, 5.5], [95.5, 6], [95.5, 11], [88, 10]], fc=WARNA["tanah_muda"], ec="white", lw=0.8, zorder=4))
    ax.add_patch(Polygon([[88, 10], [95.5, 11], [95.5, 15.5], [85, 15.5]], fc="#9CC5E8", ec="white", lw=0.8, zorder=4))
    ax.text(88, 1.9, "interpretasi menjadi\npeta tematik", ha="center", va="bottom", fontsize=7.8, color=WARNA["abu"])
    panah(ax, 64.5, 39.0, 76.6, 36.0, warna=WARNA["navy"], lw=1.2, putus=True)
    ax.text(70.5, 39.6, "transmisi data", fontsize=7.5, color=WARNA["navy"], ha="center", rotation=-13)
    panah(ax, 88, 24.8, 88, 21.2, warna=WARNA["navy"], lw=1.4)
    simpan(fig, MODUL, "M1-G01_alur-penginderaan-jauh.png")


# ---------------------------------------------------------------- Gambar 1.2
def g02_sensor_pasif_aktif():
    fig, ax = kanvas(10, 3.6, (0, 96), (-4, 31))
    judul = ["(a) Sistem pasif: pantulan", "(b) Sistem pasif: pancaran (emisi)", "(c) Sistem aktif"]
    for k, x0 in enumerate((0, 33, 66)):
        ax.add_patch(Rectangle((x0 + 1, 0), 28, 3, fc=WARNA["tanah_muda"], ec="none", zorder=1))
        for i in range(7):
            ax.plot([x0 + 2 + 4 * i, x0 + 4 + 4 * i], [0.4, 2.6], color=WARNA["tanah"], lw=0.8, zorder=2)
        ax.text(x0 + 15, -2.2, "Permukaan bumi", ha="center", fontsize=8.5, color=WARNA["abu"])
        ax.text(x0 + 15, 29.5, judul[k], ha="center", fontsize=10, fontweight="bold", color=WARNA["navy"])
    # (a)
    matahari(ax, 6.5, 22, r=2.4)
    sensor(ax, 23, 22)
    gelombang(ax, (8.5, 19.5), (14.5, 3.4), WARNA["oranye"])
    gelombang(ax, (15.5, 3.4), (22.2, 20.6), WARNA["teal"])
    ax.text(5.0, 11.0, "radiasi\nmatahari", fontsize=8, color=WARNA["oranye"], ha="center")
    ax.text(25.5, 11.0, "energi\ndipantulkan", fontsize=8, color=WARNA["teal"], ha="center")
    ax.text(23, 25.2, "sensor", fontsize=8, ha="center")
    # (b)
    sensor(ax, 48, 22)
    gelombang(ax, (48, 3.4), (48, 20.6), WARNA["merah"], siklus=6)
    ax.text(53.5, 11.0, "energi termal\ndipancarkan\nobjek", fontsize=8, color=WARNA["merah"], ha="left")
    ax.text(48, 25.2, "sensor", fontsize=8, ha="center")
    # (c)
    sensor(ax, 81, 22)
    gelombang(ax, (79.6, 20.6), (79.6, 3.4), WARNA["ungu"], siklus=7)
    gelombang(ax, (82.4, 3.4), (82.4, 20.6), WARNA["ungu"], siklus=7, lw=1.0)
    ax.text(76.5, 11.0, "pulsa\ndipancarkan", fontsize=8, color=WARNA["ungu"], ha="right")
    ax.text(85.5, 11.0, "hamburan\nbalik diterima", fontsize=8, color=WARNA["ungu"], ha="left")
    ax.text(81, 25.2, "sensor (radar/LiDAR)", fontsize=8, ha="center")
    simpan(fig, MODUL, "M1-G02_sensor-pasif-aktif.png")


# ---------------------------------------------------------------- Gambar 1.3
def g03_spektrum_elektromagnetik():
    fig = plt.figure(figsize=(10, 4.3))
    ax = fig.add_axes([0.04, 0.50, 0.92, 0.13])
    wil = [
        ("Sinar\ngamma", -13.0, -11.0, "#4B3F72"),
        ("Sinar-X", -11.0, -8.0, "#6C5A9C"),
        ("Ultraviolet", -8.0, np.log10(4e-7), "#9C8CC9"),
        ("", np.log10(4e-7), np.log10(7e-7), None),
        ("Inframerah", np.log10(7e-7), -3.0, "#C46A4A"),
        ("Gelombang\nmikro", -3.0, 0.0, "#2A9D8F"),
        ("Gelombang radio", 0.0, 3.0, "#3B82C4"),
    ]
    for label, a, b, warna in wil:
        if warna is None:
            for nm in np.linspace(400, 700, 60):
                x = np.log10(nm * 1e-9)
                ax.add_patch(Rectangle((x, 0), np.log10((nm + 5.2) * 1e-9) - x, 1, fc=panjang_gel_ke_rgb(nm), ec="none"))
            continue
        ax.add_patch(Rectangle((a, 0), b - a, 1, fc=warna, ec="white", lw=1))
        ax.text((a + b) / 2, 1.35, label, ha="center", va="bottom", fontsize=9, color=WARNA["teks"])
    ax.set_xlim(-13, 3)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xticks([-12, -9, -6, -3, 0, 3])
    ax.set_xticklabels(["1 pm", "1 nm", "1 µm", "1 mm", "1 m", "1 km"], fontsize=9)
    ax.tick_params(axis="x", length=3)
    ax.set_xlabel("Panjang gelombang (skala logaritmik)", fontsize=9, labelpad=2)

    # rentang yang umum dipakai penginderaan jauh
    atas = fig.add_axes([0.04, 0.80, 0.92, 0.16], sharex=ax)
    atas.axis("off")
    atas.set_ylim(0, 1)
    rentang = [
        (np.log10(0.4e-6), np.log10(2.5e-6), "optik pantulan 0,4–2,5 µm", WARNA["teal"], "right"),
        (np.log10(8e-6), np.log10(14e-6), "inframerah termal 8–14 µm", WARNA["merah"], "atas"),
        (-3.0, 0.0, "gelombang mikro/radar ±1 mm–1 m", WARNA["navy"], "center"),
    ]
    for a, b, label, warna, posisi in rentang:
        atas.plot([a, a, b, b], [0.30, 0.15, 0.15, 0.30], color=warna, lw=1.4)
        if posisi == "center":
            atas.text((a + b) / 2, 0.42, label, ha="center", va="bottom", fontsize=8.5, color=warna)
        elif posisi == "atas":
            atas.plot([(a + b) / 2] * 2, [0.30, 0.66], color=warna, lw=0.8)
            atas.text((a + b) / 2, 0.70, label, ha="center", va="bottom", fontsize=8.5, color=warna)
        else:
            x = a - 0.12 if posisi == "right" else b + 0.12
            atas.text(x, 0.42, label, ha=posisi, va="bottom", fontsize=8.5, color=warna)
    atas.text(-13, 0.62, "Rentang yang umum\ndipakai penginderaan jauh:", fontsize=8.5, fontweight="bold",
              color=WARNA["navy"], va="center")

    # perbesaran cahaya tampak
    zoom = fig.add_axes([0.30, 0.10, 0.40, 0.11])
    for nm in np.arange(400, 700, 1):
        zoom.add_patch(Rectangle((nm, 0), 1.05, 1, fc=panjang_gel_ke_rgb(nm), ec="none"))
    zoom.set_xlim(400, 700)
    zoom.set_ylim(0, 1)
    zoom.set_yticks([])
    zoom.set_xticks([400, 450, 500, 550, 600, 650, 700])
    zoom.tick_params(labelsize=8, length=2)
    zoom.set_xlabel("Perbesaran cahaya tampak (nm)", fontsize=8.5, labelpad=1)
    for s in zoom.spines.values():
        s.set_visible(False)
    for x_spek, x_zoom in ((np.log10(4e-7), 400), (np.log10(7e-7), 700)):
        fig.add_artist(ConnectionPatch((x_spek, 0), (x_zoom, 1), "data", "data", axesA=ax, axesB=zoom,
                                       color=WARNA["abu"], lw=0.8, linestyle="--"))
    fig.text(0.96, 0.30, "Panjang gelombang makin besar →\nfrekuensi dan energi foton makin kecil",
             ha="right", va="center", fontsize=8.5, color=WARNA["abu"], style="italic")
    simpan(fig, MODUL, "M1-G03_spektrum-elektromagnetik.png")


# ---------------------------------------------------------------- Gambar 1.4
def kurva(titik, x):
    xs, ys = zip(*titik)
    y = np.interp(x, xs, ys)
    k = np.ones(9) / 9
    return np.convolve(np.pad(y, 4, mode="edge"), k, mode="valid")


def g04_respons_spektral():
    x = np.linspace(0.4, 2.5, 600)
    seri = [
        ("Vegetasi hijau", WARNA["hijau"], "-", [(0.40, 4), (0.45, 5), (0.50, 6), (0.55, 11), (0.60, 7), (0.65, 4.5), (0.68, 4), (0.70, 8),
                                            (0.72, 25), (0.75, 44), (0.80, 48), (0.90, 50), (1.00, 51), (1.10, 50), (1.20, 46), (1.30, 44),
                                            (1.40, 30), (1.45, 22), (1.50, 26), (1.60, 33), (1.65, 34), (1.70, 33), (1.80, 28), (1.90, 12),
                                            (1.95, 8), (2.00, 10), (2.10, 15), (2.20, 18), (2.30, 16), (2.40, 12), (2.50, 10)]),
        ("Tanah kering", WARNA["oranye"], "-", [(0.40, 10), (0.50, 16), (0.60, 23), (0.70, 28), (0.80, 32), (1.00, 38), (1.20, 42), (1.35, 43),
                                             (1.40, 40), (1.45, 40), (1.50, 43), (1.70, 48), (1.85, 49), (1.90, 44), (1.95, 43), (2.00, 46),
                                             (2.20, 47), (2.35, 44), (2.50, 42)]),
        ("Tanah basah", WARNA["tanah"], "-", [(0.40, 5), (0.50, 8), (0.60, 11), (0.70, 14), (0.80, 16), (1.00, 19), (1.20, 22), (1.35, 22),
                                           (1.40, 15), (1.45, 13), (1.50, 17), (1.70, 24), (1.85, 24), (1.90, 12), (1.95, 10), (2.00, 13),
                                           (2.20, 17), (2.35, 15), (2.50, 12)]),
        ("Air jernih", WARNA["biru"], "-", [(0.40, 7), (0.45, 7), (0.50, 6), (0.55, 4.5), (0.60, 3), (0.65, 2), (0.70, 1), (0.75, 0.5),
                                          (0.80, 0.3), (1.00, 0.2), (2.50, 0.1)]),
        ("Air keruh", WARNA["ungu"], "--", [(0.40, 8), (0.50, 10), (0.55, 11), (0.60, 10.5), (0.65, 9), (0.70, 7), (0.75, 4), (0.80, 3),
                                          (0.90, 1.5), (1.00, 0.8), (1.20, 0.4), (2.50, 0.2)]),
    ]
    fig, ax = plt.subplots(figsize=(10, 4.6))
    for a, b in ((1.35, 1.45), (1.80, 1.95)):
        ax.axvspan(a, b, color=WARNA["abu_muda"], zorder=0)
    ax.text(1.40, 57, "serapan\nuap air\natmosfer", ha="center", va="top", fontsize=7.5, color=WARNA["abu"])
    ax.text(1.875, 57, "serapan\nuap air\natmosfer", ha="center", va="top", fontsize=7.5, color=WARNA["abu"])
    kanal = [("B2", 0.458, 0.523), ("B3", 0.543, 0.578), ("B4", 0.650, 0.680), ("B8", 0.785, 0.900), ("B11", 1.565, 1.655), ("B12", 2.100, 2.280)]
    for nama, a, b in kanal:
        ax.add_patch(Rectangle((a, 61), b - a, 2.6, fc=WARNA["navy"], ec="none", clip_on=False))
        ax.text((a + b) / 2, 64.4, nama, ha="center", va="bottom", fontsize=7.5, color=WARNA["navy"], clip_on=False)
    ax.text(2.5, 68.5, "Posisi sebagian kanal Sentinel-2 MSI", ha="right", fontsize=8, color=WARNA["navy"], clip_on=False)
    for label, warna, gaya_garis, titik in seri:
        ax.plot(x, kurva(titik, x), color=warna, lw=2.0, ls=gaya_garis, label=label, zorder=3)
    for a, b, label in ((0.4, 0.7, "Tampak"), (0.7, 1.3, "Inframerah dekat"), (1.3, 2.5, "Inframerah gelombang pendek")):
        ax.text((a + b) / 2, -10.0, label, ha="center", va="top", fontsize=8.5, color=WARNA["abu"], clip_on=False)
        ax.plot([a + 0.01, b - 0.01], [-8.6, -8.6], color=WARNA["abu"], lw=0.8, clip_on=False)
    ax.set_xlim(0.4, 2.5)
    ax.set_ylim(0, 60)
    ax.set_xlabel("Panjang gelombang (µm)", labelpad=46)
    ax.set_ylabel("Pantulan (%)")
    ax.legend(loc="center left", bbox_to_anchor=(1.01, 0.5), fontsize=9.5)
    ax.text(0.99, 0.02, "Ilustrasi skematis — bukan data terukur", transform=ax.transAxes, ha="right",
            va="bottom", fontsize=8, style="italic", color=WARNA["abu"])
    simpan(fig, MODUL, "M1-G04_pola-respons-spektral.png")


# ---------------------------------------------------------------- Gambar 1.5
def bentang_sintetis(n=120, seed=4):
    """Bentang lahan sintetis (RGB 0–1) untuk ilustrasi resolusi spasial."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:n, 0:n]
    img = np.zeros((n, n, 3))
    img[:] = (0.55, 0.72, 0.38)                                   # vegetasi campuran
    petak = [(5, 50, 8, 40, (0.80, 0.66, 0.45)), (55, 85, 10, 35, (0.62, 0.80, 0.42)),
             (60, 112, 70, 112, (0.78, 0.62, 0.42)), (8, 35, 70, 100, (0.70, 0.84, 0.50))]
    for x0, x1, y0, y1, w in petak:
        img[y0:y1, x0:x1] = w
    sungai = 60 + 14 * np.sin(yy / 17.0)
    img[np.abs(xx - sungai) < 2.2] = (0.30, 0.50, 0.75)
    img[(np.abs(yy - 0.45 * xx - 40) < 1.2)] = (0.85, 0.85, 0.85)  # jalan
    for _ in range(14):                                            # atap rumah
        cx, cy = rng.integers(88, 115), rng.integers(10, 40)
        img[cy:cy + 3, cx:cx + 3] = (0.75, 0.30, 0.25)
    img += rng.normal(0, 0.025, img.shape)
    return np.clip(img, 0, 1)


def kasarkan(img, f):
    n = img.shape[0] // f * f
    b = img[:n, :n].reshape(n // f, f, n // f, f, 3).mean(axis=(1, 3))
    return np.kron(b, np.ones((f, f, 1)))


def judul_panel(fig, sel, teks):
    a = fig.add_subplot(sel)
    a.axis("off")
    a.set_title(teks, loc="left", pad=4)


def g05_empat_resolusi():
    fig = plt.figure(figsize=(10, 7.0))
    gs = fig.add_gridspec(2, 2, hspace=0.30, wspace=0.16, left=0.02, right=0.98, top=0.95, bottom=0.07)
    img = bentang_sintetis()

    # (a) spasial
    judul_panel(fig, gs[0, 0], "(a) Resolusi spasial")
    sub = gs[0, 0].subgridspec(1, 3, wspace=0.06)
    for k, (f, label) in enumerate(((1, "piksel 10 m"), (3, "piksel 30 m"), (6, "piksel 60 m"))):
        a = fig.add_subplot(sub[0, k])
        a.imshow(kasarkan(img, f), interpolation="nearest")
        a.set_xticks([]), a.set_yticks([])
        a.set_xlabel(label, fontsize=8.5)

    # (b) spektral
    judul_panel(fig, gs[0, 1], "(b) Resolusi spektral")
    a = fig.add_subplot(gs[0, 1].subgridspec(10, 1)[1:, 0])
    baris = [("Pankromatik: satu kanal lebar", [(0.45, 0.90)], WARNA["abu"]),
             ("Multispektral: beberapa kanal (contoh Sentinel-2)",
              [(0.458, 0.523), (0.543, 0.578), (0.650, 0.680), (0.698, 0.713), (0.733, 0.748), (0.773, 0.793),
               (0.785, 0.900), (0.855, 0.875), (1.565, 1.655), (2.100, 2.280)], WARNA["teal"]),
             ("Hiperspektral: ratusan kanal sempit bersambung", [(w, w + 0.009) for w in np.arange(0.40, 2.50, 0.010)], WARNA["ungu"])]
    for i, (nama, kanal, warna) in enumerate(baris):
        y = 2 - i
        for p, q in kanal:
            a.add_patch(Rectangle((p, y - 0.22), q - p, 0.44, fc=warna, ec="white", lw=0.3))
        a.text(0.41, y + 0.30, nama, ha="left", va="bottom", fontsize=8.5)
    a.set_xlim(0.4, 2.5)
    a.set_ylim(-0.4, 2.75)
    a.set_yticks([])
    a.spines["left"].set_visible(False)
    a.set_xlabel("Panjang gelombang (µm)", fontsize=8.5)
    a.tick_params(labelsize=8)

    # (c) radiometrik
    judul_panel(fig, gs[1, 0], "(c) Resolusi radiometrik")
    sub = gs[1, 0].subgridspec(1, 3, wspace=0.06)
    abu = img @ np.array([0.30, 0.59, 0.11])
    abu = (abu - abu.min()) / (abu.max() - abu.min())
    for k, bit in enumerate((1, 2, 8)):
        tingkat = 2 ** bit
        q = np.floor(abu * (tingkat - 1e-9)) / (tingkat - 1)
        a = fig.add_subplot(sub[0, k])
        a.imshow(q, cmap="gray", vmin=0, vmax=1, interpolation="nearest")
        a.set_xticks([]), a.set_yticks([])
        a.set_xlabel(f"{bit} bit = {tingkat} tingkat keabuan", fontsize=8.5)

    # (d) temporal
    judul_panel(fig, gs[1, 1], "(d) Resolusi temporal")
    a = fig.add_subplot(gs[1, 1].subgridspec(10, 1)[1:, 0])
    rng = np.random.default_rng(11)
    for i, (label, langkah) in enumerate((("Perekaman ulang tiap 5 hari (Sentinel-2, dua satelit)", 5),
                                          ("Perekaman ulang tiap 16 hari (Landsat 8)", 16))):
        y = 1 - i
        hari = np.arange(1, 91, langkah)
        awan = rng.random(len(hari)) < 0.45
        a.plot([0, 90], [y, y], color=WARNA["abu_muda"], lw=6, solid_capstyle="round", zorder=1)
        a.scatter(hari[~awan], [y] * (~awan).sum(), s=46, color=WARNA["teal"], zorder=3, label="perekaman cerah" if i == 0 else None)
        a.scatter(hari[awan], [y] * awan.sum(), s=46, facecolor="white", edgecolor=WARNA["abu"], zorder=3,
                  label="perekaman tertutup awan (ilustrasi)" if i == 0 else None)
        a.text(0, y + 0.22, label, ha="left", va="bottom", fontsize=8.5)
    a.set_xlim(-1, 91)
    a.set_ylim(-0.5, 2.1)
    a.set_yticks([])
    a.spines["left"].set_visible(False)
    a.set_xlabel("Hari ke-", fontsize=8.5)
    a.tick_params(labelsize=8)
    a.legend(loc="upper left", ncol=2, fontsize=8, bbox_to_anchor=(0.0, 1.04), handletextpad=0.3, columnspacing=1.2)
    simpan(fig, MODUL, "M1-G05_ilustrasi-empat-resolusi.png")


# ---------------------------------------------------------------- Gambar 1.6
def g06_scorpan():
    fig, ax = kanvas(9, 6.6, (0, 100), (0, 74))
    pusat = (50, 39)
    ax.add_patch(Circle(pusat, 10.5, fc=WARNA["navy"], ec="none", zorder=4))
    ax.text(*pusat, "S\nkelas atau sifat\ntanah di lokasi x, y\npada waktu t", ha="center", va="center",
            color="white", fontsize=9.5, zorder=5, linespacing=1.2)
    faktor = [
        ("s", "Soil", "tanah: peta tanah lama,\ndata profil, proximal sensing", WARNA["tanah"]),
        ("c", "Climate", "iklim: curah hujan,\nsuhu udara", WARNA["biru"]),
        ("o", "Organisms", "organisme: vegetasi,\npenggunaan lahan, NDVI", WARNA["hijau"]),
        ("r", "Relief", "relief: DEM, lereng,\nkelengkungan, TWI", WARNA["oranye"]),
        ("p", "Parent material", "bahan induk: peta\ngeologi dan litologi", WARNA["abu"]),
        ("a", "Age", "umur/waktu: umur\nbentuklahan dan endapan", WARNA["ungu"]),
        ("n", "Spatial position", "posisi: koordinat,\njarak ke sungai", WARNA["teal"]),
    ]
    for i, (huruf, nama, isi, warna) in enumerate(faktor):
        sudut = np.deg2rad(90 - i * 360 / 7)
        cx, cy = pusat[0] + 33 * np.cos(sudut), pusat[1] + 26 * np.sin(sudut)
        kotak(ax, cx - 12.5, cy - 5.6, 25, 11.2, isi=WARNA["putih"], warna=warna, lw=1.4, r=1.2)
        ax.add_patch(Circle((cx - 9.6, cy + 2.2), 2.3, fc=warna, ec="none", zorder=5))
        ax.text(cx - 9.6, cy + 2.2, huruf, ha="center", va="center", color="white", fontsize=11, fontweight="bold", zorder=6)
        ax.text(cx - 6.4, cy + 2.2, nama, ha="left", va="center", fontsize=9.5, fontweight="bold", color=warna, zorder=6)
        ax.text(cx, cy - 2.6, isi, ha="center", va="center", fontsize=8, zorder=6, linespacing=1.15)
        dx, dy = pusat[0] - cx, pusat[1] - cy
        jarak = np.hypot(dx, dy)
        mulai = (cx + dx / jarak * 8.5, cy + dy / jarak * 7.0)
        akhir = (pusat[0] - dx / jarak * 11.2, pusat[1] - dy / jarak * 11.2)
        panah(ax, *mulai, *akhir, warna=warna, lw=1.3)
    ax.text(50, 3.0, "S = f (s, c, o, r, p, a, n) + ε", ha="center", fontsize=12, fontweight="bold", color=WARNA["navy"])
    simpan(fig, MODUL, "M1-G06_konsep-scorpan.png")


# ---------------------------------------------------------------- Gambar 1.7
def g07_siklus_pertanian_presisi():
    fig, ax = kanvas(9, 6.0, (0, 100), (0, 66))
    pusat = (50, 33)
    ax.add_patch(Circle(pusat, 9.5, fc=WARNA["latar"], ec=WARNA["navy"], lw=1.2, zorder=2))
    ax.text(*pusat, "Pengelolaan\nspesifik\nlokasi", ha="center", va="center", fontsize=10, fontweight="bold", color=WARNA["navy"])
    tahap = [
        ("Akuisisi data", "citra, survei tanah,\nsensor lapangan", WARNA["biru"]),
        ("Analisis variabilitas", "pemetaan dengan\nRS dan DSM", WARNA["teal"]),
        ("Zona pengelolaan", "pengelompokan area\nyang relatif seragam", WARNA["hijau"]),
        ("Tindakan spesifik lokasi", "pemupukan, drainase,\nkonservasi tanah", WARNA["oranye"]),
        ("Pemantauan dan evaluasi", "kondisi tanaman\ndan hasil panen", WARNA["ungu"]),
    ]
    posisi = []
    for i in range(5):
        sudut = np.deg2rad(90 - i * 72)
        posisi.append((pusat[0] + 31 * np.cos(sudut), pusat[1] + 22.5 * np.sin(sudut)))
    for i, ((cx, cy), (judul, isi, warna)) in enumerate(zip(posisi, tahap)):
        kotak(ax, cx - 13, cy - 5.6, 26, 11.2, isi=WARNA["putih"], warna=warna, lw=1.5, r=1.2)
        nomor(ax, cx - 10.5, cy + 2.4, i + 1, warna=warna, r=1.6)
        ax.text(cx - 8.2, cy + 2.4, judul, ha="left", va="center", fontsize=9.5, fontweight="bold", color=warna)
        ax.text(cx, cy - 2.4, isi, ha="center", va="center", fontsize=8.3, linespacing=1.15)
    def tepi(arah):
        """Jarak dari pusat kotak (13 × 5,6) ke tepinya searah vektor arah, plus jeda."""
        return min(13.0 / max(abs(arah[0]), 1e-6), 5.6 / max(abs(arah[1]), 1e-6)) + 1.0

    for i in range(5):
        a, b = np.array(posisi[i]), np.array(posisi[(i + 1) % 5])
        arah = (b - a) / np.hypot(*(b - a))
        panah(ax, *(a + arah * tepi(arah)), *(b - arah * tepi(arah)), warna=WARNA["navy"], lw=1.4, lengkung=-0.12)
    simpan(fig, MODUL, "M1-G07_siklus-pertanian-presisi.png")


# ---------------------------------------------------------------- Gambar 1.8
def g08_alur_kerja_dsm():
    fig, ax = kanvas(10, 3.9, (0, 100), (0, 39))
    tahap = [
        ("Observasi\ntanah", "profil, sampel,\nanalisis lab, PSS", "Modul 3, 7"),
        ("Data\nlingkungan", "citra, DEM, SAR,\nLiDAR, iklim, geologi", "Modul 2, 4, 5, 6"),
        ("Prediksi\nspasial", "model statistik/\nmachine learning", "Modul 8"),
        ("Evaluasi", "validasi dan\nketidakpastian", "Modul 8"),
        ("Informasi\ntanah spasial", "peta kelas/sifat\ntanah + ketidakpastian", "Modul 8"),
        ("Interpretasi dan\nkeputusan", "penalaran pedologis,\npengelolaan lahan", "Modul 6"),
    ]
    warna = [WARNA["tanah"], WARNA["teal"], WARNA["navy"], WARNA["ungu"], WARNA["hijau"], WARNA["oranye"]]
    w, jarak = 14.2, 16.9
    for i, (judul, isi, modul) in enumerate(tahap):
        x = 1 + i * jarak
        kotak(ax, x, 17, w, 15, isi=WARNA["putih"], warna=warna[i], lw=1.5, r=1.0)
        nomor(ax, x + w / 2, 32, i + 1, warna=warna[i], r=1.8, ukuran=10)
        ax.text(x + w / 2, 26.6, judul, ha="center", va="center", fontsize=9.5, fontweight="bold", color=warna[i], linespacing=1.1)
        ax.text(x + w / 2, 20.6, isi, ha="center", va="center", fontsize=7.9, linespacing=1.15)
        kotak(ax, x + 1.5, 10.5, w - 3, 4.2, modul, isi=WARNA["latar"], warna=WARNA["abu"], ukuran=8, lw=0.6, r=0.8)
        if i < 5:
            panah(ax, x + w + 0.2, 24.5, x + jarak - 0.2, 24.5, warna=WARNA["navy"], lw=1.4)
    ax.annotate("", xy=(1 + w / 2, 10.3), xytext=(1 + 3 * jarak + w / 2, 10.3),
                arrowprops=dict(arrowstyle="-|>", color=WARNA["abu"], lw=1.1, ls="--",
                                connectionstyle="arc,angleA=-90,angleB=-90,armA=14,armB=14,rad=4"))
    ax.text(1 + 1.5 * jarak + w / 2, 6.9, "umpan balik: evaluasi dapat menunjukkan perlunya observasi tambahan",
            ha="center", va="top", fontsize=8, style="italic", color=WARNA["abu"])
    simpan(fig, MODUL, "M1-G08_alur-kerja-dsm.png")


# ---------------------------------------------------------------- Gambar 1.9
def g09_peta_lokasi_bompon():
    batas = gaya.baca_layer("batas_subdas")[0][1]
    minx, maxx, miny, maxy = batas.GetEnvelope()
    fig = plt.figure(figsize=(8.6, 8.8))
    ax = fig.add_axes([0.02, 0.04, 0.56, 0.92])
    ax.set_xlim(minx - 260, maxx + 260)
    ax.set_ylim(miny - 160, maxy + 160)
    ax.set_aspect("equal")

    desa = gaya.baca_layer("rbi_desa_magelang")
    for atr, g in desa:
        gaya.gambar_poligon(ax, g, fc="#F7F7F2", ec="#9AA1AA", lw=0.8, ls=(0, (5, 2, 1, 2)), zorder=1)
    geser_dusun = {"Salakan": (-70, -60)}
    for atr, g in gaya.baca_layer("batas_dusun"):
        gaya.gambar_poligon(ax, g, fc="#FBF6EC", ec="#B9A88E", lw=0.6, zorder=2)
        p = g.PointOnSurface()
        dx, dy = geser_dusun.get(atr["dusun"], (0, 0))
        ax.text(p.GetX() + dx, p.GetY() + dy, atr["dusun"], ha="center", va="center", fontsize=7.6, color="#5B4A36", zorder=7)
    for atr, g in gaya.baca_layer("jalan"):
        gaya.gambar_garis(ax, g, color="#C9A27E", lw=0.7 if atr["kelas"] != "Roda 4" else 1.1, zorder=3)
    for atr, g in gaya.baca_layer("sungai"):
        perenial = "perenial" in atr["jenis"]
        gaya.gambar_garis(ax, g, color=WARNA["biru"], lw=1.8 if perenial else 0.9, ls="-" if perenial else (0, (4, 1.5)), zorder=4)
    gaya.gambar_poligon(ax, batas, fc="none", ec=WARNA["navy"], lw=2.2, zorder=6)
    for atr, g in desa:
        if g.Intersects(batas):
            irisan = g.Intersection(batas)
            p = irisan.PointOnSurface()
            dx, dy = {"Margoyoso": (-330, 260), "Wonogiri": (0, 260)}.get(atr["desa"].title(), (60, -250))
            ax.text(p.GetX() + dx, p.GetY() + dy, f"Desa {atr['desa'].title()}",
                    ha="center", fontsize=8.5, style="italic", fontweight="bold", color=WARNA["abu"], zorder=7)
    gaya.grid_utm(ax, 500)
    gaya.panah_utara(ax, 0.92, 0.88)
    gaya.skala_batang(ax, maxx - 520, miny - 110, 500, "500 m", tinggi=22)

    # inset lokasi
    ins = fig.add_axes([0.62, 0.58, 0.36, 0.36])
    kec_warna = {"Kajoran": "#D6E4F0", "Salaman": "#E8DCC8"}
    for atr, g in desa:
        gaya.gambar_poligon(ins, g, fc=kec_warna.get(atr["kecamatan"], "#F1F1F1"), ec="white", lw=0.3)
    gaya.gambar_poligon(ins, batas, fc=WARNA["merah"], ec=WARNA["merah"], lw=1.2, zorder=5)
    for kec, (dx, dy) in (("Kajoran", (-3500, 2500)), ("Salaman", (2200, -3500))):
        xs = [g.Centroid().GetX() for a, g in desa if a["kecamatan"] == kec]
        ys = [g.Centroid().GetY() for a, g in desa if a["kecamatan"] == kec]
        ins.text(np.mean(xs) + dx * 0.1, np.mean(ys) + dy * 0.1, f"Kec. {kec}", fontsize=8, ha="center", fontweight="bold", color=WARNA["navy"])
    ins.set_aspect("equal")
    ins.autoscale_view()
    ins.set_xticks([]), ins.set_yticks([])
    for s in ins.spines.values():
        s.set_visible(True)
        s.set_color(WARNA["abu"])
    ins.set_title("Sebagian Kabupaten Magelang\n(batas desa RBI 1:25.000)", fontsize=8.5, fontweight="normal", color=WARNA["teks"])

    # legenda
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch

    unsur = [
        Line2D([], [], color=WARNA["navy"], lw=2.2, label="Batas Sub-DAS Bompon"),
        Patch(fc="#FBF6EC", ec="#B9A88E", label="Batas dusun"),
        Line2D([], [], color="#9AA1AA", lw=0.8, ls=(0, (5, 2, 1, 2)), label="Batas desa (RBI)"),
        Line2D([], [], color=WARNA["biru"], lw=1.8, label="Sungai perenial"),
        Line2D([], [], color=WARNA["biru"], lw=0.9, ls=(0, (4, 1.5)), label="Sungai intermiten"),
        Line2D([], [], color="#C9A27E", lw=1.1, label="Jalan"),
        Patch(fc=WARNA["merah"], ec=WARNA["merah"], label="Lokasi Sub-DAS (inset)"),
    ]
    fig.legend(handles=unsur, loc="upper left", bbox_to_anchor=(0.62, 0.50), fontsize=8.8, title="Keterangan",
               title_fontproperties={"weight": "bold", "size": 9.5}, alignment="left")
    fig.text(0.62, 0.13, "Sistem koordinat: WGS 84 / UTM zona 49S\n(EPSG:32749)\nLuas Sub-DAS: 294,71 ha",
             fontsize=8.3, color=WARNA["abu"], va="bottom")
    simpan(fig, MODUL, "M1-G09_peta-lokasi-subdas-bompon.png")


if __name__ == "__main__":
    gaya.atur()
    g01_alur_penginderaan_jauh()
    g02_sensor_pasif_aktif()
    g03_spektrum_elektromagnetik()
    g04_respons_spektral()
    g05_empat_resolusi()
    g06_scorpan()
    g07_siklus_pertanian_presisi()
    g08_alur_kerja_dsm()
    g09_peta_lokasi_bompon()
