"""Gambar dan analisis Modul 7 — Proximal Soil Sensing (PSS).

Jalankan: python3 Output/scripts/gambar_modul_7.py
Keluaran:
- Output/assets/modul-7/M7-G01_taksonomi-instrumen-proximal-soil-sensing.png
- Output/assets/modul-7/M7-G02_komparasi-skala-rs-vs-pss.png
- Output/assets/modul-7/M7-G03_fitur-serapan-spektral-vnir-swir-tanah.png
- Output/assets/modul-7/M7-G04_prapemrosesan-kemometrik-dan-kalibrasi-plsr.png
- Output/assets/modul-7/spektrum_pss_simulasi.csv
- Output/assets/modul-7/statistik_modul_7.json
"""
import csv
import json
import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle
from scipy.signal import savgol_filter

import gaya
from gaya import WARNA, kanvas, kotak, nomor, panah, simpan

MODUL = "modul-7"
KELUAR_JSON = os.path.join(gaya.ASET, MODUL, "statistik_modul_7.json")
KELUAR_CSV = os.path.join(gaya.ASET, MODUL, "spektrum_pss_simulasi.csv")


def gauss(wl, mu, sigma, amp):
    return amp * np.exp(-0.5 * ((wl - mu) / sigma) ** 2)


def bangkitkan_spektrum_tanah(wl, lempung_persen, soc_persen, lengas_persen, fe_persen, jenis_fe="hematit", rng=None):
    """Model fisik Beer-Lambert semu spektrum Vis-NIR-SWIR (400-2500 nm)."""
    x = (wl - 400.0) / 2100.0
    # Absorbansi dasar matriks kuarsa-feldspar menurun dari tampak ke SWIR
    a_base = 0.42 + 0.58 * np.exp(-3.2 * x) + 0.04 * x ** 2
    # Efek bahan organik (SOC meningkatkan absorbansi tampak-NIR)
    a_soc = 0.055 * (soc_persen - 1.0) * np.exp(-1.6 * x)
    # Efek lengas umum pada baseline
    a_lengas_base = 0.006 * (lengas_persen - 6.0)

    # Pita serapan oksida besi Fe3+ (430, 480/530, 660, dan 885/925 nm)
    mu_fe = 885.0 if jenis_fe == "hematit" else 925.0
    mu_vis = 530.0 if jenis_fe == "hematit" else 480.0
    a_fe = (
        gauss(wl, 430.0, 45.0, 0.055 * fe_persen)
        + gauss(wl, mu_vis, 55.0, 0.048 * fe_persen)
        + gauss(wl, 660.0, 50.0, 0.020 * fe_persen)
        + gauss(wl, mu_fe, 85.0, 0.038 * fe_persen)
    )
    # Pita serapan O-H air bebas & air antarlapis (1414 nm dan 1915 nm)
    amp_w1 = 0.040 + 0.0085 * lengas_persen + 0.0014 * lempung_persen
    amp_w2 = 0.080 + 0.0150 * lengas_persen + 0.0024 * lempung_persen
    a_air = (
        gauss(wl, 1414.0, 30.0, amp_w1)
        + gauss(wl, 1465.0, 45.0, 0.32 * amp_w1)
        + gauss(wl, 1915.0, 36.0, amp_w2)
        + gauss(wl, 1975.0, 55.0, 0.35 * amp_w2)
    )
    # Pita serapan gugus Al-OH mineral lempung (1395, 2165, 2208, 2382 nm)
    amp_cl = 0.0026 * lempung_persen
    a_lempung = (
        gauss(wl, 1395.0, 14.0, 0.35 * amp_cl)
        + gauss(wl, 2165.0, 14.0, 0.48 * amp_cl)
        + gauss(wl, 2208.0, 17.0, amp_cl)
        + gauss(wl, 2382.0, 26.0, 0.38 * amp_cl)
    )
    # Pita serapan ikatan C-H / N-H bahan organik (1726 dan 2312 nm)
    amp_org = 0.0065 * soc_persen
    a_org = gauss(wl, 1726.0, 20.0, amp_org) + gauss(wl, 2312.0, 22.0, 1.3 * amp_org)

    A_tot = a_base + a_soc + a_lengas_base + a_fe + a_air + a_lempung + a_org
    refl = 10.0 ** (-A_tot)
    if rng is not None:
        refl += rng.normal(0.0, 0.0005, size=wl.shape)
    return np.clip(refl, 0.015, 0.65)


def continuum_removal(wl, refl):
    """Hitung kurva continuum removal (CR) dengan selubung cembung atas (upper convex hull)."""
    pts = np.column_stack([wl, refl])
    hull_idx = [0]
    for i in range(1, len(wl)):
        while len(hull_idx) >= 2:
            i1, i2 = hull_idx[-2], hull_idx[-1]
            slope_prev = (refl[i2] - refl[i1]) / (wl[i2] - wl[i1])
            slope_curr = (refl[i] - refl[i1]) / (wl[i] - wl[i1])
            if slope_curr >= slope_prev:
                hull_idx.pop()
            else:
                break
        hull_idx.append(i)
    cont = np.interp(wl, wl[hull_idx], refl[hull_idx])
    return refl / np.maximum(cont, 1e-6), cont


def plsr_sederhana(X, y, n_comp=4):
    """Implementasi NIPALS / SIMPLS Partial Least Squares Regression (PLSR) 1-target."""
    X_mean = X.mean(axis=0)
    y_mean = y.mean()
    Xk = X - X_mean
    yk = y - y_mean
    n, p = X.shape
    W = np.zeros((p, n_comp))
    P = np.zeros((p, n_comp))
    Q = np.zeros(n_comp)
    T = np.zeros((n, n_comp))
    for a in range(n_comp):
        w = Xk.T @ yk
        w = w / np.linalg.norm(w)
        t = Xk @ w
        tt = float(t.T @ t)
        p_vec = (Xk.T @ t) / tt
        q_val = float(yk.T @ t) / tt
        Xk = Xk - np.outer(t, p_vec)
        yk = yk - t * q_val
        W[:, a] = w
        P[:, a] = p_vec
        Q[a] = q_val
        T[:, a] = t
    R_mat = W @ np.linalg.inv(P.T @ W)
    beta = R_mat @ Q
    intercept = y_mean - float(X_mean @ beta)
    return beta, intercept


def simulasi_dan_plsr():
    """Bangkitkan 50 spektrum sampel tanah (terkalibrasi pada rentang tekstur Bompon) dan jalankan 10-fold CV PLSR."""
    rng = np.random.default_rng(2026)
    wl = np.arange(400.0, 2501.0, 10.0)  # 211 kanal (interval 10 nm)
    n = 50
    # Distribusi lempung mengikuti Tabel 4.1 Lapisan 1 Sub-DAS Bompon (min 31.32, max 68.18, mean ~50.35, sd ~7.73)
    lempung = np.clip(rng.normal(50.35, 7.73, size=n), 31.32, 68.18)
    pasir = np.clip(rng.normal(20.44, 6.96, size=n) - 0.35 * (lempung - 50.35), 4.94, 41.35)
    debu = np.clip(100.0 - lempung - pasir, 14.77, 45.77)
    # Normalisasi agar pas 100%
    tot = lempung + pasir + debu
    lempung, pasir, debu = lempung / tot * 100.0, pasir / tot * 100.0, debu / tot * 100.0
    soc = np.clip(rng.normal(1.85, 0.48, size=n) + 0.015 * (lempung - 50.0), 0.85, 3.20)
    lengas = np.clip(rng.normal(9.5, 2.4, size=n), 5.0, 16.0)
    fe = np.clip(rng.normal(2.2, 0.55, size=n), 1.1, 3.6)

    R = np.zeros((n, len(wl)))
    x_norm = (wl - 400.0) / 2100.0
    for i in range(n):
        j_fe = "hematit" if i % 2 == 0 else "goetit"
        spek_murni = bangkitkan_spektrum_tanah(wl, lempung[i], soc[i], lengas[i], fe[i], jenis_fe=j_fe, rng=None)
        A_murni = -np.log10(spek_murni)
        # Hamburan fisik ukuran agregat: pergeseran aditif baseline & kemiringan spektral pada absorbansi
        b0 = rng.uniform(-0.11, 0.11)
        b_tilt = rng.uniform(-0.08, 0.08) * (x_norm - 0.5)
        A_ukur = A_murni + b0 + b_tilt + rng.normal(0.0, 0.0004, size=wl.shape)
        R[i] = np.clip(10.0 ** (-A_ukur), 0.015, 0.68)

    # Simpan ke CSV untuk bahan praktik
    os.makedirs(os.path.dirname(KELUAR_CSV), exist_ok=True)
    with open(KELUAR_CSV, "w", newline="", encoding="utf-8") as fh:
        w_csv = csv.writer(fh)
        header = ["id_sampel", "pasir_persen", "debu_persen", "lempung_persen", "soc_persen", "lengas_persen"] + [f"R_{int(w)}nm" for w in wl]
        w_csv.writerow(header)
        for i in range(n):
            row = [f"S{i+1:02d}", round(pasir[i], 2), round(debu[i], 2), round(lempung[i], 2), round(soc[i], 2), round(lengas[i], 2)]
            row.extend([round(val, 5) for val in R[i]])
            w_csv.writerow(row)

    # Prapemrosesan:
    # 1. Absorbansi A = log10(1/R)
    A = np.log10(1.0 / R)
    # 2. SNV (Standard Normal Variate) per baris
    A_snv = (A - A.mean(axis=1, keepdims=True)) / A.std(axis=1, keepdims=True)
    # 3. Savitzky-Golay turunan pertama (window=9, poly=2) pada A_snv
    A_sg1 = savgol_filter(A_snv, window_length=9, polyorder=2, deriv=1, delta=10.0, axis=1)

    # Evaluasi 10-fold CV PLSR (n_comp=4) pada: (a) R mentah, (b) A_snv, (c) A_sg1
    folds = np.array_split(np.arange(n), 10)
    hasil_cv = {}
    pred_terbaik = np.zeros(n)
    for nama_p, X_mat in (("Reflektansi mentah (R)", R), ("Absorbansi + SNV", A_snv), ("SNV + Savitzky-Golay d1", A_sg1)):
        y_pred = np.zeros(n)
        for idx_val in folds:
            idx_tr = np.setdiff1d(np.arange(n), idx_val)
            beta, b0 = plsr_sederhana(X_mat[idx_tr], lempung[idx_tr], n_comp=4)
            y_pred[idx_val] = X_mat[idx_val] @ beta + b0
        rmse = float(np.sqrt(np.mean((lempung - y_pred) ** 2)))
        mae = float(np.mean(np.abs(lempung - y_pred)))
        r2 = float(1.0 - np.sum((lempung - y_pred) ** 2) / np.sum((lempung - lempung.mean()) ** 2))
        rpd = float(np.std(lempung, ddof=1) / rmse)
        rpiq = float((np.percentile(lempung, 75) - np.percentile(lempung, 25)) / rmse)
        hasil_cv[nama_p] = {
            "R2_cv": round(r2, 3),
            "RMSE_cv": round(rmse, 2),
            "MAE_cv": round(mae, 2),
            "RPD": round(rpd, 2),
            "RPIQ": round(rpiq, 2),
        }
        if nama_p == "SNV + Savitzky-Golay d1":
            pred_terbaik = y_pred

    stat = {
        "jumlah_sampel": n,
        "jumlah_kanal": len(wl),
        "rentang_nm": [400, 2500],
        "interval_nm": 10,
        "statistik_lempung": {
            "min": round(float(lempung.min()), 2),
            "mean": round(float(lempung.mean()), 2),
            "median": round(float(np.median(lempung)), 2),
            "sd": round(float(np.std(lempung, ddof=1)), 2),
            "max": round(float(lempung.max()), 2),
        },
        "evaluasi_plsr_lempung_10fold": hasil_cv,
    }
    with open(KELUAR_JSON, "w", encoding="utf-8") as fh:
        json.dump(stat, fh, indent=2, ensure_ascii=False)
    return wl, R, A_snv, A_sg1, lempung, pred_terbaik, stat


# ---------------------------------------------------------------- Gambar 7.1
def g01_taksonomi_instrumen_pss():
    fig, ax = kanvas(10, 5.2, (0, 104), (0, 54))

    # Header utama
    kotak(ax, 22, 46.5, 60, 5.8, "Klasifikasi Teknologi Proximal Soil Sensing (PSS)\n(Jarak sensor < 2 m atau kontak langsung dengan tanah)",
          isi=WARNA["navy"], warna=WARNA["navy"], warna_teks="white", ukuran=9.2, tebal=True, r=0.9)

    kelompok = [
        ("1. Spektroskopi Reflektansi\nOptik (Vis–NIR–SWIR & MIR)",
         "350–2.500 nm (Vis–NIR–SWIR)\n2.500–25.000 nm (Mid-IR)",
         "Vibrasi molekul O–H, C–H,\nN–H, Al–OH, Fe–OH & transisi Fe³⁺",
         "SOC, tekstur (lempung/pasir),\nlengas, KTK, pH, mineral lempung",
         "Non-invasif / kontak probe\n(Lab, titik lapangan, on-the-go)",
         WARNA["biru"]),
        ("2. Spektroskopi Unsur Atomik\n(pXRF & LIBS)",
         "Sinar-X (0,01–10 nm)\n& plasma optik laser (LIBS)",
         "Fluoresensi sinar-X kulit dalam\n& emisi atom tereksitasi",
         "Total unsur hara & logam:\nFe, Al, Si, K, Ca, Ti, Zr, P, Pb",
         "Kontak langsung in-situ /\npemindaian inti bor (core)",
         WARNA["oranye"]),
        ("3. Geofisika Elektromagnetik\n& Radar (EMI, ERT, GPR)",
         "Frekuensi rendah (kHz)\nhingga gelombang mikro (MHz–GHz)",
         "Konduktivitas listrik semu (ECa)\n& konstanta dielektrik tanah",
         "Salinitas, kadar air volumetrik,\nkedalaman lempung/muka air/gambut",
         "Non-invasif mobile (ditarik\nATV/traktor di gawangan kebun)",
         WARNA["teal"]),
        ("4. Radiometri Sinar Gama &\nSensor Elektrokimia/Mekanis",
         "Sinar-γ (⁴⁰K, ²³⁸U, ²³²Th)\n& elektroda selektif ion / penetrometer",
         "Peluruhan isotop alami bahan\ninduk & potensial membran/tahanan",
         "Mineralogi pelapukan, tekstur,\npH langsung, NO₃⁻, pemadatan tanah",
         "Pasif non-invasif (γ-ray) &\ninvasif kontak langsung (ISE/konus)",
         WARNA["tanah"]),
    ]

    w = 23.6
    jarak = 25.4
    for i, (judul, spek, fisik, target, moda, warna) in enumerate(kelompok):
        x = 1.6 + i * jarak
        panah(ax, 52, 46.5, x + w / 2, 40.5, warna=WARNA["abu"], lw=1.2)
        kotak(ax, x, 2.5, w, 37.5, isi=WARNA["putih"], warna=warna, lw=1.5, r=1.0, zorder=2)
        kotak(ax, x + 0.7, 34.0, w - 1.4, 5.3, isi=warna, warna=warna, lw=0, r=0.7, zorder=4)
        ax.text(x + w / 2, 36.65, judul, ha="center", va="center", fontsize=7.6, fontweight="bold", color="white", linespacing=1.15, zorder=5)

        sub_blok = [
            ("Rentang Spektral:", spek, 28.5),
            ("Mekanisme Fisik:", fisik, 20.8),
            ("Sifat Tanah Target:", target, 13.0),
            ("Moda Akuisisi:", moda, 5.5),
        ]
        for lbl_s, isi_s, y_pos in sub_blok:
            ax.text(x + w / 2, y_pos + 2.6, lbl_s, ha="center", va="center", fontsize=7.1, fontweight="bold", color=warna, zorder=4)
            ax.text(x + w / 2, y_pos - 0.3, isi_s, ha="center", va="center", fontsize=6.9, color=WARNA["teks"], linespacing=1.12, zorder=4)

    simpan(fig, MODUL, "M7-G01_taksonomi-instrumen-proximal-soil-sensing.png")


# ---------------------------------------------------------------- Gambar 7.2
def g02_komparasi_rs_vs_pss():
    fig = plt.figure(figsize=(10, 4.5))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.12, 1.0], left=0.02, right=0.98, top=0.88, bottom=0.14, wspace=0.18)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])

    # Panel (a): Skema perbandingan RS vs PSS
    ax1.set_xlim(0, 56)
    ax1.set_ylim(0, 46)
    ax1.set_aspect("equal")
    ax1.axis("off")
    ax1.set_title("(a) Geometri akuisisi dan cakupan kedalaman\nRemote Sensing vs Proximal Soil Sensing", fontsize=9.2)

    # Kotak kiri: Remote Sensing
    kotak(ax1, 1.0, 2.0, 25.5, 40.5, isi=WARNA["latar"], warna=WARNA["biru"], lw=1.3, r=0.9, zorder=1)
    ax1.text(13.75, 40.0, "Remote Sensing (Satelit/Udara)", ha="center", fontsize=8.3, fontweight="bold", color=WARNA["biru"])
    kotak(ax1, 5.75, 34.0, 16.0, 3.6, "Satelit (700–800 km)", isi=WARNA["biru"], warna=WARNA["biru"], warna_teks="white", ukuran=7.3, tebal=True, zorder=3)
    ax1.text(13.75, 29.2, "Gangguan atmosfer, uap air,\n& hamburan aerosol", ha="center", fontsize=7.0, style="italic", color=WARNA["abu"])
    # Kanopi pohon menghalangi
    for cx in (6.5, 13.75, 21.0):
        ax1.add_patch(Circle((cx, 21.5), 3.4, fc=WARNA["hijau"], ec="#2D5F28", lw=0.8, alpha=0.88, zorder=3))
    ax1.text(13.75, 15.8, "Halangan tajuk vegetasi & serasah", ha="center", fontsize=7.0, color=WARNA["hijau"], fontweight="bold")
    # Profil tanah
    ax1.add_patch(Rectangle((2.5, 4.0), 22.5, 9.5, fc=WARNA["tanah_muda"], ec=WARNA["tanah"], lw=1.0, zorder=2))
    ax1.add_patch(Rectangle((2.5, 12.2), 22.5, 1.3, fc=WARNA["oranye"], ec="none", zorder=3))
    ax1.text(13.75, 8.5, "Hanya kulit permukaan (0–2 mm)\nPiksel campuran 10–30 m\n(10–13 kanal diskrit)", ha="center", va="center", fontsize=7.0, fontweight="bold", color=WARNA["teks"])

    # Kotak kanan: Proximal Soil Sensing
    kotak(ax1, 29.0, 2.0, 25.5, 40.5, isi=WARNA["latar"], warna=WARNA["tanah"], lw=1.3, r=0.9, zorder=1)
    ax1.text(41.75, 40.0, "Proximal Soil Sensing (PSS)", ha="center", fontsize=8.3, fontweight="bold", color=WARNA["tanah"])
    kotak(ax1, 30.5, 30.8, 22.5, 6.4, "Spektrometer Vis–NIR–SWIR\n/ Probe Kontak / Sensor EMI\n(Jarak < 2 m, sumber cahaya internal)", isi=WARNA["tanah"], warna=WARNA["tanah"], warna_teks="white", ukuran=6.6, tebal=True, zorder=3)
    ax1.text(41.75, 26.6, "Bebas gangguan atmosfer &\nditerapkan langsung pada tanah", ha="center", fontsize=7.0, color=WARNA["hijau"], fontweight="bold")
    # Profil tanah berlapis (0-20, 20-40, 40-100 cm)
    ax1.add_patch(Rectangle((30.5, 16.5), 22.5, 6.0, fc="#7A4E2D", ec=WARNA["navy"], lw=0.8, zorder=2))
    ax1.add_patch(Rectangle((30.5, 10.5), 22.5, 6.0, fc="#A66E43", ec=WARNA["navy"], lw=0.8, zorder=2))
    ax1.add_patch(Rectangle((30.5, 4.0), 22.5, 6.5, fc="#D4A373", ec=WARNA["navy"], lw=0.8, zorder=2))
    ax1.text(41.75, 19.5, "Horizon A (0–20 cm): Probe/Lab", ha="center", va="center", fontsize=6.7, color="white", fontweight="bold")
    ax1.text(41.75, 13.5, "Horizon B1 (20–40 cm): Core/Auger", ha="center", va="center", fontsize=6.7, color="white", fontweight="bold")
    ax1.text(41.75, 7.2, "Subsoil (40–100 cm): EMI / Penetrometer", ha="center", va="center", fontsize=6.4, color=WARNA["teks"], fontweight="bold")
    panah(ax1, 41.75, 30.8, 41.75, 22.8, warna=WARNA["oranye"], lw=1.6)

    # Panel (b): Kurva spektral kontinu PSS (2151 kanal) vs kanal diskrit Sentinel-2 MSI
    wl_pss = np.linspace(400, 2500, 1051)
    r_pss = bangkitkan_spektrum_tanah(wl_pss, lempung_persen=55.0, soc_persen=1.6, lengas_persen=8.5, fe_persen=2.6, jenis_fe="hematit")
    ax2.plot(wl_pss, r_pss * 100, color=WARNA["tanah"], lw=2.0, label="Spektrum kontinu PSS (resolusi 1–2 nm)")

    # Kanal Sentinel-2
    s2_wl = np.array([490, 560, 665, 705, 740, 783, 842, 865, 1610, 2190])
    s2_bw = np.array([65, 35, 30, 15, 15, 20, 115, 20, 90, 180])
    s2_r = np.interp(s2_wl, wl_pss, r_pss) * 100
    for w_c, bw in zip(s2_wl, s2_bw):
        ax2.axvspan(w_c - bw / 2, w_c + bw / 2, color=WARNA["biru"], alpha=0.14, zorder=1)
    ax2.plot(s2_wl, s2_r, "s--", color=WARNA["biru"], lw=1.2, markersize=5.5, label="Pencuplikan 10 kanal Sentinel-2 MSI")

    # Sorot fitur diagnostik sempit yang terlewat satelit
    ax2.annotate("Pita serapan Fe³⁺\n(~885 nm)", xy=(885, 14.8), xytext=(1060, 7.5),
                 arrowprops=dict(arrowstyle="->", color=WARNA["merah"], lw=1.0),
                 fontsize=7.3, fontweight="bold", color=WARNA["merah"], ha="center")
    ax2.annotate("Serapan O–H\n(1.414 & 1.915 nm)", xy=(1915, 12.0), xytext=(1600, 6.5),
                 arrowprops=dict(arrowstyle="->", color=WARNA["teal"], lw=1.0),
                 fontsize=7.3, fontweight="bold", color=WARNA["teal"], ha="center")
    ax2.annotate("Doublet Al–OH kaolinit\n(2.165 & 2.208 nm)\nterlewat oleh lebar B12", xy=(2208, 22.5), xytext=(1940, 36.5),
                 arrowprops=dict(arrowstyle="->", color=WARNA["navy"], lw=1.1),
                 fontsize=7.2, fontweight="bold", color=WARNA["navy"], ha="center")

    ax2.set_xlim(380, 2520)
    ax2.set_ylim(0, 45)
    ax2.set_xlabel("Panjang gelombang (nm)", fontsize=9)
    ax2.set_ylabel("Reflektansi tanah (%)", fontsize=9)
    ax2.set_title("(b) Resolusi spektral PSS kontinu vs pencuplikan\nkanal lebar satelit multispektral", fontsize=9.2)
    ax2.legend(loc="upper left", fontsize=7.6)
    ax2.grid(color=WARNA["abu_muda"], lw=0.5)

    simpan(fig, MODUL, "M7-G02_komparasi-skala-rs-vs-pss.png")


# ---------------------------------------------------------------- Gambar 7.3
def g03_fitur_serapan_spektral():
    wl = np.linspace(400, 2500, 1051)
    profil = [
        ("Tanah mineral lempung tinggi (Kaolinitik, kering)",
         bangkitkan_spektrum_tanah(wl, 64.0, 1.1, 6.0, 1.8, "hematit"), "#C0392B", "-"),
        ("Tanah kaya oksida besi (Goetit/kuning-cokelat)",
         bangkitkan_spektrum_tanah(wl, 48.0, 1.4, 8.0, 3.5, "goetit"), "#D97724", "-"),
        ("Tanah lempung sedang lembap (Inceptisols Bompon)",
         bangkitkan_spektrum_tanah(wl, 50.4, 1.9, 13.5, 2.2, "hematit"), "#2A9D8F", "-"),
        ("Tanah kaya bahan organik (SOC > 4%, gelap)",
         bangkitkan_spektrum_tanah(wl, 42.0, 4.6, 11.0, 1.5, "goetit"), "#1F3A5F", "--"),
    ]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))
    fig.subplots_adjust(left=0.07, right=0.98, top=0.86, bottom=0.16, wspace=0.22)

    for lbl, r, col, ls in profil:
        ax1.plot(wl, r * 100, ls=ls, color=col, lw=1.8, label=lbl)
        cr, _ = continuum_removal(wl, r)
        ax2.plot(wl, cr, ls=ls, color=col, lw=1.6, label=lbl)

    # Penanda zona serapan pada kedua panel
    pita = [
        (480, 540, "Fe³⁺", "#FDEBD0", 0.56),
        (860, 940, "Fe³⁺\n(kristal)", "#FDEBD0", 0.66),
        (1390, 1450, "O–H &\nAl–OH", "#D6EAF8", 0.39),
        (1890, 1960, "H₂O\n(air)", "#D6EAF8", 0.25),
        (2160, 2235, "Al–OH\n(lempung)", "#E8DAEF", 0.58),
        (2295, 2365, "C–H /\nMg–OH", "#D5F5E3", 0.72),
    ]
    for a1, a2, teks, fc, y_t in pita:
        ax1.axvspan(a1, a2, color=fc, alpha=0.65, zorder=0)
        ax2.axvspan(a1, a2, color=fc, alpha=0.65, zorder=0)
        ax2.text((a1 + a2) / 2, y_t, teks, ha="center", va="bottom", fontsize=6.3, color=WARNA["teks"], fontweight="bold")

    ax1.set_xlim(400, 2500)
    ax1.set_ylim(0, 49)
    ax1.set_xlabel("Panjang gelombang (nm)", fontsize=9)
    ax1.set_ylabel("Reflektansi (R, %)", fontsize=9)
    ax1.set_title("(a) Spektrum reflektansi Vis–NIR–SWIR empat\nkarakteristik tanah utama", fontsize=9.2)
    ax1.legend(loc="upper left", fontsize=7.0, framealpha=0.9)
    ax1.grid(color=WARNA["abu_muda"], lw=0.5)

    ax2.set_xlim(400, 2500)
    ax2.set_ylim(0.23, 1.03)
    ax2.set_xlabel("Panjang gelombang (nm)", fontsize=9)
    ax2.set_ylabel("Rasio Continuum Removal (CR)", fontsize=9)
    ax2.set_title("(b) Spektrum Continuum Removal (CR) yang\nmenajamkan kedalaman pita serapan", fontsize=9.2)
    ax2.grid(color=WARNA["abu_muda"], lw=0.5)

    simpan(fig, MODUL, "M7-G03_fitur-serapan-spektral-vnir-swir-tanah.png")


# ---------------------------------------------------------------- Gambar 7.4
def g04_kemometrik_dan_plsr(wl, R, A_snv, A_sg1, lempung, pred_terbaik, stat):
    fig, axs = plt.subplots(2, 2, figsize=(10, 6.4))
    fig.subplots_adjust(left=0.08, right=0.97, top=0.92, bottom=0.09, wspace=0.25, hspace=0.36)

    cmap = plt.cm.YlOrBr
    norm = plt.Normalize(vmin=30, vmax=70)

    # (a) Spektrum mentah R
    ax = axs[0, 0]
    for i in range(len(lempung)):
        ax.plot(wl, R[i] * 100, color=cmap(norm(lempung[i])), lw=0.9, alpha=0.8)
    ax.set_title("(a) Spektrum reflektansi mentah (R)\n(dipengaruhi pergeseran baseline kekasaran)", fontsize=8.8)
    ax.set_xlabel("Panjang gelombang (nm)", fontsize=8.3)
    ax.set_ylabel("Reflektansi (%)", fontsize=8.3)
    ax.set_xlim(400, 2500)
    ax.grid(color=WARNA["abu_muda"], lw=0.5)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    cb = fig.colorbar(sm, ax=ax, pad=0.02)
    cb.set_label("Lempung (%)", fontsize=7.8)
    cb.ax.tick_params(labelsize=7.2)

    # (b) Absorbansi + SNV
    ax = axs[0, 1]
    for i in range(len(lempung)):
        ax.plot(wl, A_snv[i], color=cmap(norm(lempung[i])), lw=0.9, alpha=0.8)
    ax.set_title("(b) Absorbansi log(1/R) terstandarisasi SNV\n(koreksi efek hamburan ukuran partikel)", fontsize=8.8)
    ax.set_xlabel("Panjang gelombang (nm)", fontsize=8.3)
    ax.set_ylabel("Absorbansi SNV (satuan SD)", fontsize=8.3)
    ax.set_xlim(400, 2500)
    ax.grid(color=WARNA["abu_muda"], lw=0.5)

    # (c) Savitzky-Golay turunan ke-1 pada jendela SWIR 2000-2420 nm
    ax = axs[1, 0]
    sel_w = (wl >= 2000) & (wl <= 2420)
    for i in range(len(lempung)):
        ax.plot(wl[sel_w], A_sg1[i, sel_w] * 1e3, color=cmap(norm(lempung[i])), lw=1.0, alpha=0.85)
    ax.axvline(2208, color=WARNA["merah"], ls="--", lw=1.1)
    ax.text(2215, ax.get_ylim()[1] * 0.72 if ax.get_ylim()[1] > 0 else 4.2,
            "Titik belok Al–OH\n(2.208 nm)", fontsize=7.5, fontweight="bold", color=WARNA["merah"])
    ax.set_title("(c) Turunan pertama Savitzky–Golay (dA/dλ)\npada jendela serapan lempung SWIR", fontsize=8.8)
    ax.set_xlabel("Panjang gelombang (nm)", fontsize=8.3)
    ax.set_ylabel("d(SNV)/dλ (×10⁻³ nm⁻¹)", fontsize=8.3)
    ax.set_xlim(2000, 2420)
    ax.grid(color=WARNA["abu_muda"], lw=0.5)

    # (d) Kalibrasi & Validasi Silang PLSR Lempung
    ax = axs[1, 1]
    ev = stat["evaluasi_plsr_lempung_10fold"]["SNV + Savitzky-Golay d1"]
    ev_raw = stat["evaluasi_plsr_lempung_10fold"]["Reflektansi mentah (R)"]
    ax.scatter(lempung, pred_terbaik, c=lempung, cmap=cmap, norm=norm, s=34, edgecolors=WARNA["navy"], linewidths=0.7, zorder=4)
    ax.plot([30, 70], [30, 70], "--", color=WARNA["merah"], lw=1.3, label="Garis 1:1")
    teks_stat = (
        f"PLSR (4 komponen laten, 10-fold CV):\n"
        f"• SNV + SG d1: $R^2$ = {ev['R2_cv']:.2f}, RMSE = {ev['RMSE_cv']:.2f}%, RPD = {ev['RPD']:.2f}\n"
        f"• Spektrum mentah: $R^2$ = {ev_raw['R2_cv']:.2f}, RMSE = {ev_raw['RMSE_cv']:.2f}%"
    ).replace(".", ",")
    ax.text(0.04, 0.94, teks_stat, transform=ax.transAxes, va="top", ha="left", fontsize=7.4,
            bbox=dict(boxstyle="round,pad=0.35", fc=WARNA["latar"], ec=WARNA["abu_muda"]))
    ax.set_xlim(30, 70)
    ax.set_ylim(30, 70)
    ax.set_xlabel("Kadar lempung terukur laboratorium (%)", fontsize=8.3)
    ax.set_ylabel("Kadar lempung prediksi PLSR (%)", fontsize=8.3)
    ax.set_title("(d) Evaluasi prediksi kadar lempung dengan\nPartial Least Squares Regression (PLSR)", fontsize=8.8)
    ax.legend(loc="lower right", fontsize=7.8)
    ax.grid(color=WARNA["abu_muda"], lw=0.5)

    simpan(fig, MODUL, "M7-G04_prapemrosesan-kemometrik-dan-kalibrasi-plsr.png")


if __name__ == "__main__":
    gaya.atur()
    wl, R, A_snv, A_sg1, lempung, pred_terbaik, stat = simulasi_dan_plsr()
    print(json.dumps(stat, indent=2, ensure_ascii=False))
    g01_taksonomi_instrumen_pss()
    g02_komparasi_rs_vs_pss()
    g03_fitur_serapan_spektral()
    g04_kemometrik_dan_plsr(wl, R, A_snv, A_sg1, lempung, pred_terbaik, stat)
