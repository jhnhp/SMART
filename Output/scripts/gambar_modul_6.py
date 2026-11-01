"""Gambar Modul 6 — Interpretasi Pedologis dari Data Remote Sensing.

Jalankan: python3 Output/scripts/gambar_modul_6.py
Keluaran: Output/assets/modul-6/M6-Gxx_*.png
Semua gambar bersifat konseptual; Gambar 6.2 dan 6.5 dihitung dari data sintetis.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from matplotlib.patches import Circle, Patch
from matplotlib.ticker import FuncFormatter
from scipy import ndimage
from scipy.cluster.vq import kmeans2

import gaya
from gaya import WARNA, kanvas, kotak, panah, simpan

MODUL = "modul-6"
SUNGAI = WARNA["biru"]
KOMA2 = FuncFormatter(lambda v, _: f"{v:.2f}".replace(".", ","))


# ---------------------------------------------------------------- Gambar 6.1
def cabang(ax, x, y, sudut, panjang, tingkat, rng, lebar=1.6):
    """Jaringan dendritik: cabang bercabang acak ke arah hulu."""
    if tingkat == 0 or panjang < 0.02:
        return
    x2, y2 = x + panjang * np.cos(sudut), y + panjang * np.sin(sudut)
    ax.plot([x, x2], [y, y2], color=SUNGAI, lw=lebar, solid_capstyle="round")
    for arah in (-1, 1):
        cabang(ax, x2, y2, sudut + arah * rng.uniform(0.35, 0.75), panjang * rng.uniform(0.6, 0.78), tingkat - 1, rng,
               max(lebar * 0.72, 0.5))


def pola_dendritik(ax, rng):
    cabang(ax, 0.5, 0.05, np.pi / 2, 0.28, 6, rng)


def pola_paralel(ax, rng):
    for x0 in np.linspace(0.12, 0.88, 6):
        t = np.linspace(0, 1, 60)
        xs = x0 + 0.03 * np.sin(t * 5 + x0 * 7) + 0.18 * t
        ys = 0.95 - 0.9 * t
        ax.plot(xs, ys, color=SUNGAI, lw=1.2)
        for tt in rng.uniform(0.2, 0.8, 2):
            i = int(tt * 59)
            ax.plot([xs[i] - 0.06, xs[i]], [ys[i] + 0.08, ys[i]], color=SUNGAI, lw=0.7)


def pola_trellis(ax, rng):
    for x0 in (0.2, 0.42, 0.64, 0.86):
        ax.plot([x0, x0], [0.12, 0.95], color=SUNGAI, lw=1.4)
        for y in np.arange(0.2, 0.92, 0.09):
            arah = rng.choice([-1, 1])
            ax.plot([x0, x0 + arah * rng.uniform(0.04, 0.09)], [y, y + 0.01], color=SUNGAI, lw=0.8)
    ax.plot([0.2, 0.86], [0.12, 0.12], color=SUNGAI, lw=1.8)
    ax.plot([0.53, 0.53], [0.12, 0.03], color=SUNGAI, lw=1.8)


def pola_rektangular(ax, rng):
    titik = [(0.1, 0.9), (0.1, 0.62), (0.38, 0.62), (0.38, 0.4), (0.62, 0.4), (0.62, 0.16), (0.9, 0.16)]
    xs, ys = zip(*titik)
    ax.plot(xs, ys, color=SUNGAI, lw=1.7)
    for (a, b) in [((0.38, 0.62), (0.38, 0.9)), ((0.38, 0.75), (0.62, 0.75)), ((0.62, 0.4), (0.88, 0.4)),
                   ((0.88, 0.4), (0.88, 0.7)), ((0.62, 0.28), (0.4, 0.28)), ((0.4, 0.28), (0.4, 0.1)),
                   ((0.1, 0.62), (0.1, 0.35)), ((0.1, 0.35), (0.24, 0.35))]:
        ax.plot([a[0], b[0]], [a[1], b[1]], color=SUNGAI, lw=0.9)


def pola_radial(ax, rng):
    ax.add_patch(Circle((0.5, 0.5), 0.07, fc="#D9B48F", ec=WARNA["tanah"], lw=0.8))
    for s in np.linspace(0, 2 * np.pi, 11, endpoint=False):
        r = np.linspace(0.09, 0.46, 30)
        s2 = s + 0.12 * np.sin(r * 9)
        ax.plot(0.5 + r * np.cos(s2), 0.5 + r * np.sin(s2), color=SUNGAI, lw=1.1)


def pola_anular(ax, rng):
    ax.add_patch(Circle((0.5, 0.5), 0.08, fc="#D9B48F", ec=WARNA["tanah"], lw=0.8))
    for r, (a0, a1) in ((0.2, (0.3, 5.6)), (0.33, (1.2, 6.9)), (0.44, (2.1, 7.6))):
        s = np.linspace(a0, a1, 80)
        ax.plot(0.5 + r * np.cos(s), 0.5 + r * np.sin(s), color=SUNGAI, lw=1.2)
    for s in (0.3, 1.2, 2.1):
        ax.plot([0.5 + 0.2 * np.cos(s), 0.5 + 0.48 * np.cos(s)], [0.5 + 0.2 * np.sin(s), 0.5 + 0.48 * np.sin(s)],
                color=SUNGAI, lw=1.0)


def g01_pola_aliran():
    pola = [("Dendritik", "resistensi batuan seragam;\ntanpa kontrol struktur", pola_dendritik),
            ("Paralel", "lereng terjal; sedimen\nmudah tererosi", pola_paralel),
            ("Trellis", "lapisan sedimen miring atau\nterlipat, kuat–lemah berselang", pola_trellis),
            ("Rektangular", "dikendalikan kekar\natau sesar", pola_rektangular),
            ("Radial", "kerucut gunungapi\natau kubah", pola_radial),
            ("Anular", "kubah tererosi pada lapisan\nkuat–lemah berselang", pola_anular)]
    fig, axs = plt.subplots(2, 3, figsize=(9.4, 6.3))
    fig.subplots_adjust(left=0.02, right=0.98, top=0.95, bottom=0.04, wspace=0.08, hspace=0.42)
    rng = np.random.default_rng(8)
    for ax, (nama, ket, fungsi) in zip(axs.ravel(), pola):
        ax.add_patch(plt.Rectangle((0, 0), 1, 1, fc=WARNA["latar"], ec=WARNA["abu_muda"], lw=0.8))
        fungsi(ax, rng)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(nama, fontsize=10.5, pad=3)
        ax.text(0.5, -0.04, ket, transform=ax.transAxes, ha="center", va="top", fontsize=8.1, color=WARNA["abu"],
                linespacing=1.1)
    simpan(fig, MODUL, "M6-G01_pola-aliran-dan-pengontrolnya.png")


# ---------------------------------------------------------------- Gambar 6.2
def citra_tekstur(n=180, seed=11):
    """Citra sintetis tiga zona selebar n/3: permukaan seragam, tajuk teratur, dan tajuk tidak teratur.

    Tajuk dimodelkan sebagai kubah yang disinari dari kanan atas, dengan bayangan jatuh di kiri
    bawahnya. Rerata nilai piksel ketiga zona disamakan agar zona tidak dapat dibedakan dari rona.
    """
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:n, 0:n].astype(float)
    lebar = n // 3
    tinggi = np.zeros((n, n))

    def tajuk(cx, cy, r, t=1.0):
        d2 = ((xx - cx) ** 2 + (yy - cy) ** 2) / r ** 2
        np.maximum(tinggi, t * r * np.sqrt(np.clip(1 - d2, 0, None)), out=tinggi)

    jarak = 15
    for j, cy in enumerate(np.arange(jarak / 2, n, jarak * 0.87)):      # susunan segitiga
        for cx in np.arange(lebar + 6 + (jarak / 2 if j % 2 else 0), 2 * lebar - 6, jarak):
            tajuk(cx, cy, 6.0)
    pusat = []
    for _ in range(5000):
        if len(pusat) == 55:
            break
        r = rng.uniform(3, 9)
        cx, cy = rng.uniform(2 * lebar + r, n - 1), rng.uniform(1, n - 1)
        if all(np.hypot(cx - a, cy - b) > 0.8 * (r + c) for a, b, c in pusat):
            pusat.append((cx, cy, r))
            tajuk(cx, cy, r, rng.uniform(0.8, 1.2))

    gy, gx = np.gradient(tinggi)
    normal = np.dstack([-gx, -gy, np.ones_like(tinggi)])
    normal /= np.linalg.norm(normal, axis=2, keepdims=True)
    sinar = np.array([0.55, -0.55, 0.63])
    terang = np.clip(normal @ (sinar / np.linalg.norm(sinar)), 0, 1)
    ada_tajuk = tinggi > 0.3
    bayang = ndimage.shift(tinggi, (3, -3), order=0) > 0.3
    citra = np.where(ada_tajuk, 0.10 + 0.60 * terang, np.where(bayang, 0.05, 0.15))
    z2, z3 = citra[:, lebar:2 * lebar], citra[:, 2 * lebar:]
    z3 *= z2.mean() / z3.mean()
    citra += rng.normal(0, 0.012, citra.shape)
    citra[:, :lebar] = citra[:, lebar:].mean() + ndimage.gaussian_filter(rng.normal(0, 0.03, (n, lebar)), 1.2)
    return np.clip(citra, 0, 1), lebar


def sd_lokal(citra, k):
    """Simpangan baku sampel nilai piksel di dalam jendela k × k (pembagi n − 1)."""
    n = k * k
    rerata = ndimage.uniform_filter(citra, k, mode="reflect")
    rerata2 = ndimage.uniform_filter(citra ** 2, k, mode="reflect")
    return np.sqrt(np.clip(rerata2 - rerata ** 2, 0, None) * n / (n - 1))


def g02_tekstur_citra():
    citra, lebar = citra_tekstur()
    n = citra.shape[0]
    peta = {3: sd_lokal(citra, 3), 11: sd_lokal(citra, 11)}
    warna_sd = LinearSegmentedColormap.from_list("sd", [WARNA["latar"], "#9DC3E6", WARNA["biru"], WARNA["navy"]])
    batas = np.quantile(peta[3], 0.99)
    koma = lambda v, d=2: f"{v:.{d}f}".replace(".", ",")  # noqa: E731

    fig, axs = plt.subplots(1, 3, figsize=(10, 4.3))
    fig.subplots_adjust(left=0.01, right=0.9, top=0.88, bottom=0.2, wspace=0.06)
    axs[0].imshow(citra, cmap="gray", vmin=0, vmax=0.75, interpolation="nearest")
    for ax, k in zip(axs[1:], (3, 11)):
        im = ax.imshow(peta[k], cmap=warna_sd, vmin=0, vmax=batas, interpolation="nearest")
    judul = ["(a) Citra sintetis dengan\nrona rerata hampir sama", "(b) Simpangan baku lokal,\njendela 3 × 3", "(c) Simpangan baku lokal,\njendela 11 × 11"]
    zona = ["seragam", "tajuk teratur", "tajuk tidak\nteratur"]
    tepi = 6                       # piksel tepi zona tidak dihitung dalam rerata
    for i, ax in enumerate(axs):
        ax.set_title(judul[i], fontsize=9.2, pad=4)
        ax.set_xticks([]), ax.set_yticks([])
        for x in (lebar - 0.5, 2 * lebar - 0.5):
            ax.axvline(x, color=WARNA["oranye"], lw=0.9, ls="--")
        for z in range(3):
            tengah = (slice(None), slice(z * lebar + tepi, (z + 1) * lebar - tepi))
            if i == 0:
                teks = f"{zona[z]}\nrerata {koma(citra[tengah].mean())}"
            else:
                teks = f"rerata\n{koma(peta[(3, 11)[i - 1]][tengah].mean(), 3)}"
            ax.text((z + 0.5) * lebar, n + 3, teks, ha="center", va="top", fontsize=7.6, linespacing=1.15,
                    color=WARNA["teks"])
    for k, x0, y0 in ((3, 7, 150), (11, 22, 146)):
        axs[0].add_patch(plt.Rectangle((x0 - 0.5, y0 - 0.5), k, k, fill=False, ec=WARNA["oranye"], lw=1.1))
        axs[0].text(x0 + k / 2, y0 - 3, f"{k}×{k}", ha="center", va="bottom", fontsize=6.8, color=WARNA["oranye"],
                    fontweight="bold")
    cax = fig.add_axes([0.915, 0.29, 0.014, 0.5])
    cb = fig.colorbar(im, cax=cax)
    cb.set_label("simpangan baku lokal\n(nilai piksel)", fontsize=8.2)
    cb.ax.yaxis.set_major_formatter(KOMA2)
    cb.ax.tick_params(labelsize=7.6)
    fig.text(0.01, 0.015, "Data sintetis; rerata nilai piksel ketiga zona dibuat hampir sama. Garis putus-putus = batas zona; "
             "kotak pada (a) = ukuran jendela.", fontsize=7.4, style="italic", color=WARNA["abu"])
    simpan(fig, MODUL, "M6-G02_tekstur-citra-dan-simpangan-baku-lokal.png")


# ---------------------------------------------------------------- Gambar 6.3
def g03_kunci_bertingkat():
    fig, ax = kanvas(10, 5.9, (0, 104), (0, 60))
    abu = WARNA["abu"]

    def node(x, y, teks, isi=WARNA["putih"], warna=WARNA["navy"], w=17.5, h=7.0, ukuran=7.8, tebal=False):
        kotak(ax, x, y, w, h, teks, isi=isi, warna=warna, ukuran=ukuran, tebal=tebal, r=0.7, lw=1.0)

    def ke(x1, y1, x2, y2):
        panah(ax, x1, y1, x2, y2, warna=abu, lw=1.0, skala=9)

    judul = [(9.5, "Tingkat 1\nBentang lahan"), (33.0, "Tingkat 2\nBentuklahan dan posisi"),
             (57.0, "Tingkat 3\nPetunjuk pada citra"), (84.0, "Hipotesis satuan tanah\n(diuji di lapangan)")]
    for x, t in judul:
        ax.text(x, 57.5, t, ha="center", va="top", fontsize=8.6, fontweight="bold", color=WARNA["navy"], linespacing=1.1)
    node(1, 34, "Perbukitan", isi="#F3E3CF", warna=WARNA["tanah"], tebal=True, h=8)
    node(1, 10, "Dataran dan\nlembah", isi="#DCEAF7", warna=WARNA["biru"], tebal=True, h=8)
    tingkat2 = [(43.5, "Punggungan dan\nlereng atas"), (34.5, "Lereng tengah\ncuram"), (25.5, "Kaki lereng\nkoluvial"),
                (14.0, "Tanggul dan\nteras sungai"), (5.0, "Dataran banjir\ndan rawa belakang")]
    tingkat3 = ["rona cerah; aliran\nrapat dan dangkal", "bekas longsor;\nalur pengikisan", "lereng landai;\nbentuk kipas",
                "rona cerah; relief\nsedikit lebih tinggi", "rona gelap atau basah;\njauh dari tanggul"]
    hipotesis = ["tanah berkembang di\ntempat, relatif dangkal", "tanah tipis dan beragam;\nbahan terangkut", "tanah koluvial\nlebih dalam",
                 "tanah aluvial berlapis;\ndrainase lebih baik", "tanah aluvial halus;\ndrainase terhambat"]
    for i, (y, t2) in enumerate(tingkat2):
        node(24.5, y, t2)
        node(48.5, y, tingkat3[i], isi=WARNA["latar"], warna=abu)
        node(75.5, y, hipotesis[i], isi="#EAF3E2", warna=WARNA["teal"])
        asal = (18.5, 38) if i < 3 else (18.5, 14)
        ke(asal[0], asal[1], 24.5, y + 3.5)
        ke(42.0, y + 3.5, 48.5, y + 3.5)
        ke(66.0, y + 3.5, 75.5, y + 3.5)
    ax.text(52, 0.6, "Ilustrasi konseptual; isi kunci harus disusun dari data lapangan wilayah setempat",
            ha="center", fontsize=7.6, style="italic", color=abu)
    simpan(fig, MODUL, "M6-G03_contoh-kunci-interpretasi-bertingkat.png")


# ---------------------------------------------------------------- Gambar 6.4
def g04_konvergensi_batas():
    fig, axs = plt.subplots(1, 4, figsize=(10, 3.2))
    fig.subplots_adjust(left=0.01, right=0.99, top=0.82, bottom=0.12, wspace=0.08)
    t = np.linspace(0, 1, 100)
    garis = {
        "A": (0.30 + 0.06 * np.sin(t * 6), t),               # tepi dasar lembah
        "B": (0.62 + 0.05 * np.sin(t * 5 + 1), t),           # tekuk lereng
        "C": (t, 0.70 + 0.04 * np.sin(t * 7)),               # batas penggunaan lahan
        "D": (0.80 + 0.03 * np.cos(t * 9), 0.15 + 0.5 * t),   # perubahan rona setempat
    }
    analisis = [("(a) Relief dan bentuklahan", ["A", "B"]), ("(b) Pola aliran dan rona", ["A", "B", "D"]),
                ("(c) Vegetasi dan lahan", ["A", "C"])]
    for ax, (judul, kunci) in zip(axs[:3], analisis):
        for k in kunci:
            ax.plot(*garis[k], color=WARNA["navy"], lw=1.4)
        ax.set_title(judul, fontsize=9.2, pad=4)
    hitung = {k: sum(k in ks for _, ks in analisis) for k in garis}
    for k, (xs, ys) in garis.items():
        n = hitung[k]
        axs[3].plot(xs, ys, color={3: WARNA["merah"], 2: WARNA["oranye"], 1: WARNA["abu"]}[n], lw=1.0 + 1.3 * n,
                    ls="-" if n > 1 else "--")
    axs[3].set_title("(d) Gabungan: bobot batas", fontsize=9.2, pad=4)
    unsur = [plt.Line2D([], [], color=WARNA["merah"], lw=4.9, label="muncul pada 3 analisis"),
             plt.Line2D([], [], color=WARNA["oranye"], lw=3.6, label="muncul pada 2 analisis"),
             plt.Line2D([], [], color=WARNA["abu"], lw=2.3, ls="--", label="muncul pada 1 analisis")]
    fig.legend(handles=unsur, loc="lower center", ncol=3, fontsize=8.2, bbox_to_anchor=(0.5, -0.03))
    for ax in axs:
        ax.add_patch(plt.Rectangle((0, 0), 1, 1, fc=WARNA["latar"], ec=WARNA["abu_muda"], lw=0.8, zorder=0))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect("equal")
        ax.axis("off")
    simpan(fig, MODUL, "M6-G04_konvergensi-batas-analisis-unsur.png")


# ---------------------------------------------------------------- Gambar 6.5
def lanskap_kebun(n=200, seed=3):
    """Punggungan diagonal dengan lembah di kiri dan kanan; matahari dari timur (kanan)."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:n, 0:n] / (n - 1)
    jarak = xx - (0.40 + 0.20 * yy)
    z = 80 - 120 * np.abs(jarak) ** 1.2 + 8 * yy + ndimage.gaussian_filter(rng.normal(0, 1, (n, n)), 8) * 30
    gy, gx = np.gradient(z, 1 / (n - 1))
    lereng = np.hypot(gx, gy)
    sinar = np.clip(0.80 - 0.0035 * gx, 0.38, 1.18)
    kolom = np.minimum((xx * 4).astype(int), 3)
    baris = np.minimum((yy * 4).astype(int), 3)
    blok = baris * 4 + kolom
    jalan = (np.abs(xx * 4 - np.round(xx * 4)) < 0.022) | (np.abs(yy * 4 - np.round(yy * 4)) < 0.022)
    return z, lereng, sinar, blok, jalan, rng


def g05_perbandingan_metode():
    z, lereng, sinar, blok, jalan, rng = lanskap_kebun()
    n = z.shape[0]
    jenis = np.zeros(16, int)          # 0 tajuk tua (seragam)
    jenis[[2, 13]] = 1                 # tajuk muda
    jenis[7] = 2                       # blok peremajaan (tanah terbuka)
    warna_dasar = np.array([[0.18, 0.40, 0.16], [0.45, 0.62, 0.30], [0.74, 0.57, 0.40]])
    citra = warna_dasar[jenis[blok]] * sinar[..., None]
    citra[jalan] = [0.84, 0.82, 0.78]
    citra = np.clip(citra + rng.normal(0, 0.025, citra.shape), 0, 1)

    data = citra.reshape(-1, 3)
    pusat, label = kmeans2(data, 4, seed=5, minit="++")
    urut = np.argsort(np.argsort(pusat.sum(axis=1)))     # 0 tergelap ... 3 tercerah
    kelas_piksel = urut[label].reshape(n, n)
    warna_kelas = ["#173D22", "#3F8A2A", "#A8C686", "#D9B48F"]
    peta_piksel = ListedColormap(warna_kelas)

    objek = np.where(jalan, -1, blok)
    rata = np.full((n, n), 3.0)
    for b in range(16):
        m = objek == b
        rata[m] = np.bincount(kelas_piksel[m], minlength=4).argmax()

    zf = ndimage.gaussian_filter(z, 3)
    satuan = np.full((n, n), 2)
    satuan[zf < np.quantile(zf, 0.30)] = 1
    satuan[zf < np.quantile(zf, 0.12)] = 0
    satuan[zf > np.quantile(zf, 0.86)] = 3
    satuan = ndimage.median_filter(satuan, 7)
    warna_satuan = ["#5E9E8A", "#9CC5A1", "#D9A35F", "#9B6235"]
    peta_satuan = ListedColormap(warna_satuan)

    fig, axs = plt.subplots(1, 4, figsize=(10.2, 3.5))
    fig.subplots_adjust(left=0.01, right=0.99, top=0.84, bottom=0.22, wspace=0.06)
    axs[0].imshow(citra, interpolation="nearest")
    axs[0].contour(zf, levels=8, colors="white", linewidths=0.5, alpha=0.45)
    axs[1].imshow(kelas_piksel, cmap=peta_piksel, vmin=-0.5, vmax=3.5, interpolation="nearest")
    axs[2].imshow(rata, cmap=peta_piksel, vmin=-0.5, vmax=3.5, interpolation="nearest")
    axs[2].contour(objek, levels=np.arange(-0.5, 16), colors="white", linewidths=0.5)
    axs[3].imshow(satuan, cmap=peta_satuan, vmin=-0.5, vmax=3.5, interpolation="nearest")
    axs[3].contour(objek, levels=np.arange(-0.5, 16), colors="white", linewidths=0.4, alpha=0.7)
    judul = ["(a) Citra sintetis kebun di atas\npunggungan (sinar dari timur)", "(b) Klasifikasi per piksel\n(4 kelas spektral)",
             "(c) Klasifikasi berbasis objek\n(segmen = blok kebun)", "(d) Interpretasi pedologis\n(satuan tanah–lanskap)"]
    for a, j in zip(axs, judul):
        a.set_xticks([]), a.set_yticks([])
        a.set_title(j, fontsize=8.8, pad=4)
    leg1 = [Patch(fc=c, label=l) for c, l in zip(warna_kelas, ["tajuk, lereng terbayangi", "tajuk, lereng terkena sinar",
                                                               "tajuk muda", "tanah terbuka dan jalan"])]
    leg2 = [Patch(fc=c, label=l) for c, l in zip(warna_satuan, ["dasar lembah", "kaki lereng", "lereng", "punggungan"])]
    fig.legend(handles=leg1, loc="lower left", ncol=2, fontsize=7.4, bbox_to_anchor=(0.25, 0.0))
    fig.legend(handles=leg2, loc="lower right", ncol=2, fontsize=7.4, bbox_to_anchor=(1.0, 0.0))
    fig.text(0.01, 0.02, "Data sintetis; garis putih pada (a) = kontur,\npada (c) dan (d) = batas blok kebun", fontsize=7.2,
             style="italic", color=WARNA["abu"])
    simpan(fig, MODUL, "M6-G05_perbandingan-klasifikasi-dan-interpretasi.png")


if __name__ == "__main__":
    gaya.atur()
    g01_pola_aliran()
    g02_tekstur_citra()
    g03_kunci_bertingkat()
    g04_konvergensi_batas()
    g05_perbandingan_metode()
