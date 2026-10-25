"""Gambar dan analisis Modul 6 — Interpretasi Pedologis dari Data Remote Sensing.

Jalankan: python3 Output/scripts/gambar_modul_6.py
Keluaran:
- Output/assets/modul-6/M6-G01_sembilan-kunci-interpretasi-pedologis.png
- Output/assets/modul-6/M6-G02_komposit-warna-dan-tekstur-citra-bompon.png
- Output/assets/modul-6/M6-G03_sintesis-fisiografi-dan-longsor-bompon.png
- Output/assets/modul-6/M6-G04_kerangka-konvergensi-bukti-satuan-peta-tanah.png
- Output/assets/modul-6/statistik_modul_6.json
"""
import json
import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from osgeo import gdal, ogr

import gaya
from gaya import WARNA, kanvas, kotak, nomor, panah, simpan
from gambar_modul_4 import baca_sentinel2, hitung_indeks

gdal.UseExceptions()
ogr.UseExceptions()

MODUL = "modul-6"
KELUAR_JSON = os.path.join(gaya.ASET, MODUL, "statistik_modul_6.json")

URUT_BL = list(gaya.WARNA_BENTUKLAHAN)
SINGKAT_BL = {
    "Interfluve": "Interfluve",
    "Lereng Atas Perbukitan": "Lereng Atas",
    "Lereng Tengah Perbukitan": "Lereng Tengah",
    "Lereng Bawah Perbukitan": "Lereng Bawah",
    "Lereng Kaki Koluvial": "Lereng Kaki Kol.",
    "Dataran Koluvial": "Dataran Koluvial",
}
URUT_LONGSOR = ["Longsor aktif dalam", "Longsor aktif dangkal", "Longsor dorman"]
WARNA_LONGSOR = {
    "Longsor aktif dalam": "#C0392B",
    "Longsor aktif dangkal": "#E67E22",
    "Longsor dorman": "#F5B041",
}


def rasterisasi_kategori(layer, field, daftar_nama, cols, rows, gt):
    ds = ogr.Open(gaya.GPKG)
    lyr = ds.GetLayerByName(layer)
    mem_v = gdal.GetDriverByName("MEM").Create("", 0, 0, 0, gdal.GDT_Unknown)
    lyr_v = mem_v.CreateLayer("k", lyr.GetSpatialRef(), ogr.wkbPolygon)
    lyr_v.CreateField(ogr.FieldDefn("kode", ogr.OFTInteger))
    peta = {nama: i + 1 for i, nama in enumerate(daftar_nama)}
    for feat in lyr:
        val = feat.GetField(field)
        f2 = ogr.Feature(lyr_v.GetLayerDefn())
        f2.SetGeometry(feat.GetGeometryRef().Clone())
        f2.SetField("kode", peta.get(val, 0))
        lyr_v.CreateFeature(f2)
    r_ds = gdal.GetDriverByName("MEM").Create("", cols, rows, 1, gdal.GDT_Byte)
    r_ds.SetGeoTransform(gt)
    r_ds.SetProjection(lyr.GetSpatialRef().ExportToWkt())
    gdal.RasterizeLayer(r_ds, [1], lyr_v, options=["ATTRIBUTE=kode"])
    return r_ds.GetRasterBand(1).ReadAsArray()


def filter_std_3x3(arr, mask):
    a = np.where(mask, arr, np.nan)
    pad = np.pad(a, 1, mode="edge")
    win = np.lib.stride_tricks.sliding_window_view(pad, (3, 3))
    return np.nanstd(win, axis=(-2, -1))


def regangkan_rgb(r, g, b, mask, p_low=2, p_high=98):
    rgb = np.zeros(r.shape + (3,), dtype=np.float32)
    for idx, ch in enumerate((r, g, b)):
        lo, hi = np.percentile(ch[mask], [p_low, p_high])
        norm = np.clip((ch - lo) / max(hi - lo, 1e-6), 0, 1)
        rgb[..., idx] = np.where(mask, norm, 1.0)
    return rgb


def analisis_modul_6(b, ind, mask, pl, gt):
    rows, cols = mask.shape
    bl = rasterisasi_kategori("bentuklahan", "bentuklahan", URUT_BL, cols, rows, gt)
    sl = rasterisasi_kategori("kelas_lereng", "kelas_lereng", list(gaya.WARNA_LERENG), cols, rows, gt)
    ls = rasterisasi_kategori("longsor", "kelas", URUT_LONGSOR, cols, rows, gt)
    std_nir = filter_std_3x3(b["B08"], mask)
    bright = (b["B02"] + b["B03"] + b["B04"]) / 3.0

    # Statistik per bentuklahan
    stat_bl = {}
    for i, nama in enumerate(URUT_BL, start=1):
        sel = mask & (bl == i)
        n_px = int(sel.sum())
        n_ls_aktif = int((sel & ((ls == 1) | (ls == 2))).sum())
        n_ls_dorman = int((sel & (ls == 3)).sum())
        pl_counts = {
            k_pl: round(int((sel & (pl == j)).sum()) / max(n_px, 1) * 100, 1)
            for j, k_pl in enumerate(gaya.WARNA_PENGGUNAAN, start=1)
        }
        pl_dom = max(pl_counts, key=pl_counts.get)
        stat_bl[nama] = {
            "luas_ha": round(n_px * 0.01, 2),
            "persen_das": round(n_px / int(mask.sum()) * 100, 2),
            "median_ndvi": round(float(np.median(ind["NDVI"][sel])), 3),
            "median_ndmi": round(float(np.median(ind["NDMI"][sel])), 3),
            "median_bsi": round(float(np.median(ind["BSI"][sel])), 3),
            "median_kecerahan_vis_persen": round(float(np.median(bright[sel]) * 100), 2),
            "median_tekstur_nir_persen": round(float(np.median(std_nir[sel]) * 100), 2),
            "persen_longsor_aktif": round(n_ls_aktif / max(n_px, 1) * 100, 1),
            "persen_longsor_dorman": round(n_ls_dorman / max(n_px, 1) * 100, 1),
            "persen_bebas_longsor": round(100.0 - (n_ls_aktif + n_ls_dorman) / max(n_px, 1) * 100, 1),
            "penggunaan_dominan": f"{pl_dom} ({pl_counts[pl_dom]}%)",
            "proporsi_penggunaan": pl_counts,
        }

    # Statistik per penggunaan lahan (untuk kunci interpretasi rona & tekstur)
    stat_pl = {}
    for j, k_pl in enumerate(gaya.WARNA_PENGGUNAAN, start=1):
        sel = mask & (pl == j)
        n_px = int(sel.sum())
        stat_pl[k_pl] = {
            "luas_ha": round(n_px * 0.01, 2),
            "median_ndvi": round(float(np.median(ind["NDVI"][sel])), 3),
            "median_ndmi": round(float(np.median(ind["NDMI"][sel])), 3),
            "median_kecerahan_vis_persen": round(float(np.median(bright[sel]) * 100), 2),
            "median_tekstur_nir_persen": round(float(np.median(std_nir[sel]) * 100), 2),
        }

    # Statistik longsor keseluruhan
    stat_ls = {}
    for i, nama in enumerate(URUT_LONGSOR, start=1):
        sel = mask & (ls == i)
        n_px = int(sel.sum())
        stat_ls[nama] = {
            "luas_ha": round(n_px * 0.01, 2),
            "persen_das": round(n_px / int(mask.sum()) * 100, 2),
            "median_ndvi": round(float(np.median(ind["NDVI"][sel])), 3),
            "median_tekstur_nir_persen": round(float(np.median(std_nir[sel]) * 100), 2),
        }

    # Jaringan sungai
    sungai_stat = {}
    for a, _ in gaya.baca_layer("sungai"):
        jns = a["jenis"]
        sungai_stat[jns] = round(sungai_stat.get(jns, 0.0) + a["panjang_m"], 1)
    total_sungai_km = sum(sungai_stat.values()) / 1000.0
    luas_das_km2 = int(mask.sum()) * 0.01 / 100.0
    sungai_stat["total_panjang_m"] = round(sum(sungai_stat.values()), 1)
    sungai_stat["kerapatan_drainase_km_per_km2"] = round(total_sungai_km / luas_das_km2, 2)

    stat = {
        "per_bentuklahan": stat_bl,
        "per_penggunaan_lahan": stat_pl,
        "per_zona_longsor": stat_ls,
        "jaringan_drainase": sungai_stat,
    }
    os.makedirs(os.path.dirname(KELUAR_JSON), exist_ok=True)
    with open(KELUAR_JSON, "w", encoding="utf-8") as fh:
        json.dump(stat, fh, indent=2, ensure_ascii=False)
    return stat, bl, sl, ls, std_nir


# ---------------------------------------------------------------- Gambar 6.1
def g01_sembilan_kunci_interpretasi():
    fig, ax = kanvas(10, 5.8, (0, 102), (0, 60))
    kunci = [
        ("Rona dan Warna\n(Tone / Color)", "Tingkat kecerahan & rona spektral",
         "Tanah gelap-lembap (SOM/lengas tinggi)\nvs tanah cerah-kering atau tererosi", WARNA["biru"]),
        ("Tekstur Citra\n(Texture)", "Kehalusan/kekasaran variasi rona",
         "Kanopi agroforestri/hutan (kasar)\nvs petak sawah/tanah olah (halus)", WARNA["teal"]),
        ("Pola Spasial\n(Pattern)", "Susunan keruangan objek/aliran",
         "Pola aliran dendritik vs paralel;\nkisi barisan sawit teratur vs kebun acak", WARNA["hijau"]),
        ("Bentuk Objek\n(Shape)", "Konfigurasi batas/geometri poligon",
         "Dataran koluvial memanjang di lembah,\ngawir mahkota longsor melengkung", WARNA["oranye"]),
        ("Ukuran\n(Size)", "Dimensi luas, lebar, dan skala petak",
         "Petak sawah rakyat sempit (<0,1 ha)\nvs blok kebun komersial (25–30 ha)", WARNA["ungu"]),
        ("Bayangan\n(Shadow)", "Efek penyinaran & sudut datang surya",
         "Menegaskan igir interfluve, gawir\nlongsor, torehan lembah, & tinggi tajuk", WARNA["abu"]),
        ("Situs Topografi\n(Site)", "Kedudukan vertikal pada katena lereng",
         "Lereng atas tererosi (solum terpenggal)\nvs dataran koluvial basah (akumulasi)", WARNA["tanah"]),
        ("Asosiasi\n(Association)", "Keterkaitan fungsional antar-objek",
         "Teras sawah berasosiasi dengan bahan\nkoluvial-aluvial & rembesan kaki lereng", WARNA["merah"]),
        ("Konvergensi Bukti\n(Convergence)", "Sintesis silang seluruh petunjuk",
         "Merumuskan batas Satuan Peta Tanah\n(SMU) dan hipotesis sifat pedologis", WARNA["navy"]),
    ]

    w, h = 31.2, 16.2
    x_pos = [1.5, 35.4, 69.3]
    y_pos = [41.0, 21.5, 2.0]

    for idx, (judul, definisi, makna, warna) in enumerate(kunci):
        r, c = divmod(idx, 3)
        x, y = x_pos[c], y_pos[r]
        kotak(ax, x, y, w, h, isi=WARNA["putih"], warna=warna, lw=1.5, r=1.0, zorder=2)
        kotak(ax, x + 0.8, y + h - 5.2, w - 1.6, 4.4, isi=warna, warna=warna, lw=0, r=0.6, zorder=4)
        nomor(ax, x + 3.0, y + h - 3.0, idx + 1, warna=WARNA["navy"], r=1.45, ukuran=8.2)
        ax.text(x + 17.2, y + h - 3.0, judul.replace("\n", " "), ha="center", va="center",
                fontsize=7.5, fontweight="bold", color="white", zorder=6)
        ax.text(x + w / 2, y + 8.1, definisi, ha="center", va="center",
                fontsize=7.4, style="italic", color=WARNA["abu"], zorder=4)
        ax.text(x + w / 2, y + 3.5, makna, ha="center", va="center",
                fontsize=7.5, fontweight="bold", color=WARNA["teks"], linespacing=1.18, zorder=4)

    simpan(fig, MODUL, "M6-G01_sembilan-kunci-interpretasi-pedologis.png")


# ---------------------------------------------------------------- Gambar 6.2
def g02_komposit_dan_tekstur(b, std_nir, mask, ext):
    batas = gaya.baca_layer("batas_subdas")[0][1]
    sungai = gaya.baca_layer("sungai")
    dem_ds = gdal.Open(os.path.join(gaya.AKAR, "Source", "Data Bompon", "terbuka", "copdem_glo30_30m.tif"))
    dem = dem_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
    gt_d = dem_ds.GetGeoTransform()
    ext_d = [gt_d[0], gt_d[0] + dem_ds.RasterXSize * gt_d[1], gt_d[3] + dem_ds.RasterYSize * gt_d[5], gt_d[3]]
    m_ds = gdal.GetDriverByName("MEM").Create("", dem_ds.RasterXSize, dem_ds.RasterYSize, 1, gdal.GDT_Byte)
    m_ds.SetGeoTransform(gt_d)
    src_v = ogr.Open(gaya.GPKG)
    gdal.RasterizeLayer(m_ds, [1], src_v.GetLayer("batas_subdas"), burn_values=[1])
    dem_m = m_ds.ReadAsArray().astype(bool)
    gy, gx = np.gradient(dem, 30.0, 30.0)
    az, alt = np.deg2rad(315.0), np.deg2rad(45.0)
    slp = np.arctan(np.hypot(gx, gy))
    asp = np.arctan2(-gx, gy)
    hs = np.sin(alt) * np.cos(slp) + np.cos(alt) * np.sin(slp) * np.cos(az - asp)
    hs_m = np.ma.masked_where(~dem_m, hs)

    fig, axs = plt.subplots(1, 4, figsize=(10, 6.1))
    fig.subplots_adjust(left=0.01, right=0.99, top=0.88, bottom=0.15, wspace=0.05)

    # (a) False Color NIR-R-G (B08-B04-B03)
    rgb_fcc = regangkan_rgb(b["B08"], b["B04"], b["B03"], mask)
    axs[0].imshow(rgb_fcc, extent=ext, interpolation="nearest")
    axs[0].set_title("(a) Komposit warna semu\nNIR–Merah–Hijau (B8–B4–B3)", fontsize=8.8)
    axs[0].text(0.5, -0.05, "Merah tua = tajuk agroforestri;\nmerah muda/kehijauan = sawah",
                transform=axs[0].transAxes, ha="center", va="top", fontsize=7.4, color=WARNA["teks"])

    # (b) Komposit SWIR1-NIR-Red (B11-B08-B04)
    rgb_swir = regangkan_rgb(b["B11"], b["B08"], b["B04"], mask)
    axs[1].imshow(rgb_swir, extent=ext, interpolation="nearest")
    axs[1].set_title("(b) Komposit tanah–vegetasi\nSWIR1–NIR–Merah (B11–B8–B4)", fontsize=8.8)
    axs[1].text(0.5, -0.05, "Hijau cerah = kanopi rapat;\njingga/merah muda = bera/permukiman",
                transform=axs[1].transAxes, ha="center", va="top", fontsize=7.4, color=WARNA["teks"])

    # (c) Tekstur lokal NIR (SD 3x3)
    tex_m = np.ma.masked_where(~mask, std_nir * 100)
    im2 = axs[2].imshow(tex_m, extent=ext, cmap="magma_r", vmin=0.4, vmax=4.8, interpolation="nearest")
    axs[2].set_title("(c) Tekstur citra (SD 3×3 B8)\nKekasaran tajuk & batas petak", fontsize=8.8)
    cb2 = fig.colorbar(im2, ax=axs[2], orientation="horizontal", fraction=0.045, pad=0.03)
    cb2.set_label("SD reflektansi NIR (%)", fontsize=7.5)
    cb2.ax.tick_params(labelsize=7.2)

    # (d) Hillshade + Pola Aliran Sungai
    axs[3].imshow(hs_m, extent=ext_d, cmap="Greys_r", vmin=0.2, vmax=0.95, interpolation="bilinear")
    for a_s, g_s in sungai:
        peren = a_s["jenis"] == "Sungai perenial"
        gaya.gambar_garis(axs[3], g_s, color="#0284C7" if peren else "#38BDF8",
                          lw=1.3 if peren else 0.8, ls="-" if peren else "--")
    axs[3].set_title("(d) Situs relief (Hillshade DEM)\n& pola aliran sungai", fontsize=8.8)
    axs[3].text(0.5, -0.05, "Biru utuh = sungai perenial;\nbiru putus = alur intermiten",
                transform=axs[3].transAxes, ha="center", va="top", fontsize=7.4, color=WARNA["teks"])

    for ax in axs:
        gaya.gambar_poligon(ax, batas, fc="none", ec=WARNA["navy"], lw=1.2)
        ax.set_xlim(ext[0] + 140, ext[1] - 140)
        ax.set_ylim(ext[2] + 140, ext[3] - 140)
        ax.set_xticks([]), ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)

    gaya.skala_batang(axs[0], ext[0] + 200, ext[2] + 220, 500, "500 m", tinggi=24)
    gaya.panah_utara(axs[0], 0.88, 0.88, 0.05)
    simpan(fig, MODUL, "M6-G02_komposit-warna-dan-tekstur-citra-bompon.png")


# ---------------------------------------------------------------- Gambar 6.3
def g03_sintesis_fisiografi_dan_longsor(bl, sl, ls, mask, ext, stat):
    batas = gaya.baca_layer("batas_subdas")[0][1]
    titik = [g.GetPoint() for _, g in gaya.baca_layer("titik_sampel_lapangan")]
    xs = [p[0] for p in titik]
    ys = [p[1] for p in titik]

    fig = plt.figure(figsize=(10, 6.2))
    gs = fig.add_gridspec(1, 4, width_ratios=[1.0, 1.0, 1.0, 1.28], left=0.01, right=0.98, top=0.88, bottom=0.23, wspace=0.08)
    ax0 = fig.add_subplot(gs[0, 0])
    ax1 = fig.add_subplot(gs[0, 1])
    ax2 = fig.add_subplot(gs[0, 2])
    ax3 = fig.add_subplot(gs[0, 3])

    # (a) Bentuklahan
    cmap_bl = ListedColormap(["#FFFFFF"] + [gaya.WARNA_BENTUKLAHAN[k] for k in URUT_BL])
    ax0.imshow(np.where(mask, bl, 0), extent=ext, cmap=cmap_bl, vmin=0, vmax=6, interpolation="nearest")
    ax0.set_title("(a) Satuan bentuklahan\n(katena geomorfologi)", fontsize=8.8)
    leg_bl = [Patch(fc=gaya.WARNA_BENTUKLAHAN[k], label=SINGKAT_BL[k]) for k in URUT_BL]
    ax0.legend(handles=leg_bl, loc="upper center", bbox_to_anchor=(0.5, -0.01), ncol=2, fontsize=6.7, frameon=False, columnspacing=0.6)

    # (b) Kelas Lereng
    urut_sl = list(gaya.WARNA_LERENG)
    cmap_sl = ListedColormap(["#FFFFFF"] + [gaya.WARNA_LERENG[k] for k in urut_sl])
    ax1.imshow(np.where(mask, sl, 0), extent=ext, cmap=cmap_sl, vmin=0, vmax=5, interpolation="nearest")
    ax1.set_title("(b) Kelas kemiringan lereng\n(pengendali erosi–deposisi)", fontsize=8.8)
    leg_sl = [Patch(fc=gaya.WARNA_LERENG[k], label=k) for k in urut_sl]
    ax1.legend(handles=leg_sl, loc="upper center", bbox_to_anchor=(0.5, -0.01), ncol=1, fontsize=6.7, frameon=False)

    # (c) Zona Longsor + 50 titik sampel
    cmap_ls = ListedColormap(["#FFFFFF", "#E5E7EB"] + [WARNA_LONGSOR[k] for k in URUT_LONGSOR])
    arr_ls = np.where(~mask, 0, np.where(ls > 0, ls + 1, 1))
    ax2.imshow(arr_ls, extent=ext, cmap=cmap_ls, vmin=0, vmax=4, interpolation="nearest")
    ax2.scatter(xs, ys, s=11, c="white", edgecolors=WARNA["navy"], linewidths=0.7, zorder=5)
    ax2.set_title("(c) Zona gerakan massa &\n50 titik pengamatan", fontsize=8.8)
    leg_ls = [
        Patch(fc="#C0392B", label="Longsor aktif dalam (1,0%)"),
        Patch(fc="#E67E22", label="Longsor aktif dangkal (0,9%)"),
        Patch(fc="#F5B041", label="Longsor dorman (26,3%)"),
        Patch(fc="#E5E7EB", label="Stabil / bebas longsor (71,8%)"),
    ]
    ax2.legend(handles=leg_ls, loc="upper center", bbox_to_anchor=(0.5, -0.01), fontsize=6.7, frameon=False)

    for ax in (ax0, ax1, ax2):
        gaya.gambar_poligon(ax, batas, fc="none", ec=WARNA["navy"], lw=1.1)
        ax.set_xlim(ext[0] + 140, ext[1] - 140)
        ax.set_ylim(ext[2] + 140, ext[3] - 140)
        ax.set_xticks([]), ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)

    gaya.skala_batang(ax0, ext[0] + 200, ext[2] + 220, 500, "500 m", tinggi=24)
    gaya.panah_utara(ax0, 0.88, 0.88, 0.05)

    # (d) Diagram batang horizontal proporsi penggunaan lahan per bentuklahan
    pos = ax3.get_position()
    ax3.set_position([pos.x0 + 0.09, pos.y0 + 0.03, pos.width - 0.09, pos.height - 0.05])
    y_idx = np.arange(len(URUT_BL))
    lbl_y = [SINGKAT_BL[k] for k in URUT_BL]
    kiri = np.zeros(len(URUT_BL))
    for k_pl, w_pl in gaya.WARNA_PENGGUNAAN.items():
        vals = np.array([stat["per_bentuklahan"][k]["proporsi_penggunaan"][k_pl] for k in URUT_BL])
        ax3.barh(y_idx, vals, left=kiri, color=w_pl, height=0.62, label=k_pl)
        kiri += vals
    ax3.set_yticks(y_idx, lbl_y, fontsize=7.6)
    ax3.invert_yaxis()
    ax3.set_xlim(0, 100)
    ax3.set_xlabel("Proporsi luas penggunaan (%)", fontsize=8.0)
    ax3.set_title("(d) Asosiasi bentuklahan dengan\npenggunaan lahan", fontsize=8.8)
    ax3.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=2, fontsize=7.1, frameon=False)
    ax3.grid(axis="x", color=WARNA["abu_muda"], lw=0.5)

    simpan(fig, MODUL, "M6-G03_sintesis-fisiografi-dan-longsor-bompon.png")


# ---------------------------------------------------------------- Gambar 6.4
def g04_kerangka_konvergensi_bukti():
    fig, ax = kanvas(10, 4.3, (0, 104), (0, 44))

    # Kolom 1: Bukti Spektral & Spasial Citra
    kotak(ax, 1.5, 4, 28, 36, isi=WARNA["latar"], warna=WARNA["biru"], lw=1.4, r=1.0)
    ax.text(15.5, 37.2, "1. Bukti Citra Optik & SAR", ha="center", va="center", fontsize=9.2, fontweight="bold", color=WARNA["biru"])
    butir_1 = [
        ("Rona & Indeks Spektral", "NDVI, NDMI, BSI, rasio lempung/besi"),
        ("Tekstur & Ukuran Petak", "Kekasaran tajuk (SD 3×3) & batas petak"),
        ("Pola Penggunaan Lahan", "Sawah berteras, agroforestri, blok sawit"),
    ]
    for i, (j, s) in enumerate(butir_1):
        y = 27.5 - i * 10.0
        kotak(ax, 3.2, y, 24.6, 7.6, isi="white", warna=WARNA["abu_muda"], lw=1.0, r=0.7)
        ax.text(15.5, y + 5.1, j, ha="center", va="center", fontsize=8.0, fontweight="bold", color=WARNA["navy"])
        ax.text(15.5, y + 2.2, s, ha="center", va="center", fontsize=7.2, color=WARNA["teks"])

    # Kolom 2: Bukti Medan & Geologi
    kotak(ax, 35.0, 4, 28, 36, isi=WARNA["latar"], warna=WARNA["teal"], lw=1.4, r=1.0)
    ax.text(49.0, 37.2, "2. Bukti Medan & Geomorfologi", ha="center", va="center", fontsize=9.2, fontweight="bold", color=WARNA["teal"])
    butir_2 = [
        ("Situs Katena Bentuklahan", "Interfluve, lereng perbukitan, koluvial"),
        ("Pola Aliran & Kebasahan", "Alur perenial/intermiten & indeks TWI"),
        ("Dinamika Gerakan Massa", "Gawir pengikisan vs kaki akumulasi"),
    ]
    for i, (j, s) in enumerate(butir_2):
        y = 27.5 - i * 10.0
        kotak(ax, 36.7, y, 24.6, 7.6, isi="white", warna=WARNA["abu_muda"], lw=1.0, r=0.7)
        ax.text(49.0, y + 5.1, j, ha="center", va="center", fontsize=8.0, fontweight="bold", color=WARNA["navy"])
        ax.text(49.0, y + 2.2, s, ha="center", va="center", fontsize=7.2, color=WARNA["teks"])

    # Kolom 3: Konvergensi Bukti -> Informasi Pedologis & Manajemen
    kotak(ax, 68.5, 4, 34, 36, isi=WARNA["putih"], warna=WARNA["tanah"], lw=1.6, r=1.0)
    kotak(ax, 68.5, 34.5, 34, 5.5, isi=WARNA["tanah"], warna=WARNA["tanah"], lw=0, r=0.9)
    ax.text(85.5, 37.2, "3. Sintesis Informasi Pedologis", ha="center", va="center", fontsize=9.2, fontweight="bold", color="white")

    butir_3 = [
        ("Delineasi Satuan Peta Tanah", "Batas poligon fisiografis-pedologis\n(Soil Map Unit / SMU) pra-survei", WARNA["navy"]),
        ("Hipotesis Proses Pedogenesis", "Pengikisan horizon di lereng curam vs\npenimbunan koluvial-aluvial di lembah", WARNA["hijau"]),
        ("Prediksi Sifat & Kendala Lahan", "Tekstur, kedalaman solum, kelas\ndrainase, & kerawanan longsor/genangan", WARNA["oranye"]),
    ]
    for i, (j, s, col) in enumerate(butir_3):
        y = 24.5 - i * 9.5
        kotak(ax, 70.5, y, 30.0, 8.2, isi=WARNA["latar"], warna=col, lw=1.1, r=0.7)
        ax.text(85.5, y + 5.8, j, ha="center", va="center", fontsize=8.0, fontweight="bold", color=col)
        ax.text(85.5, y + 2.5, s, ha="center", va="center", fontsize=7.1, color=WARNA["teks"], linespacing=1.15)

    panah(ax, 29.8, 22.0, 34.7, 22.0, warna=WARNA["navy"], lw=1.5)
    panah(ax, 63.3, 22.0, 68.2, 22.0, warna=WARNA["tanah"], lw=1.6)

    simpan(fig, MODUL, "M6-G04_kerangka-konvergensi-bukti-satuan-peta-tanah.png")


if __name__ == "__main__":
    gaya.atur()
    b, mask, pl, gt, ext = baca_sentinel2()
    ind = hitung_indeks(b)
    ind["NDMI"] = (b["B08"] - b["B11"]) / np.maximum(b["B08"] + b["B11"], 1e-6)
    ind["BSI"] = ((b["B11"] + b["B04"]) - (b["B08"] + b["B02"])) / np.maximum((b["B11"] + b["B04"]) + (b["B08"] + b["B02"]), 1e-6)
    stat, bl, sl, ls, std_nir = analisis_modul_6(b, ind, mask, pl, gt)
    print(json.dumps(stat, indent=2, ensure_ascii=False))
    g01_sembilan_kunci_interpretasi()
    g02_komposit_dan_tekstur(b, std_nir, mask, ext)
    g03_sintesis_fisiografi_dan_longsor(bl, sl, ls, mask, ext, stat)
    g04_kerangka_konvergensi_bukti()
