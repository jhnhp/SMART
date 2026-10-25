"""Analisis data Sub-DAS Bompon untuk Modul 3 (delineasi SMU).

Jalankan: python3 Output/scripts/analisis_modul_3.py
Keluaran: Output/assets/modul-3/statistik_modul_3.json (angka yang dikutip di teks modul)

Analisis:
1. Tabulasi silang luas bentuklahan × penggunaan lahan.
2. Tumpang susun otomatis bentuklahan × kelas lereng × penggunaan lahan pada grid 2 m:
   jumlah kombinasi, jumlah poligon (patch terhubung-8), dan porsi yang lebih kecil dari
   MLA skala 1:10.000 (0,4 ha; Rossiter, 2000).
3. Generalisasi otomatis bertahap dengan penyaringan (sieve) GDAL pada ambang MLA: lapisan
   lereng disaring lebih dulu, ditumpangsusunkan kembali, lalu poligon sisa disaring.
   Penyaringan diulang sampai tidak ada perubahan.
4. Keterwakilan strata oleh 50 titik sampel rencana.
5. Perbandingan sebaran kelas lereng dari DTM LiDAR (data proyek) dan Copernicus DEM 30 m.
"""
import json
import os

import numpy as np
from osgeo import gdal, ogr
from scipy import ndimage

import gaya
from gambar_modul_2 import rasterisasi

gdal.UseExceptions()
ogr.UseExceptions()

BENTUKLAHAN = list(gaya.WARNA_BENTUKLAHAN)
LERENG = list(gaya.WARNA_LERENG)
PENGGUNAAN = list(gaya.WARNA_PENGGUNAAN)
RES = 2.0                      # m
MLA_HA = 0.4                   # MLA skala 1:10.000 dengan MLD 0,4 cm² (Rossiter, 2000)
MLA_PX = int(MLA_HA * 10000 / RES ** 2)
TERBUKA = os.path.join(gaya.AKAR, "Source", "Data Bompon", "terbuka")
KELUAR = os.path.join(gaya.ASET, "modul-3", "statistik_modul_3.json")


def topeng_batas(nx, ny, gt):
    ds = gdal.GetDriverByName("MEM").Create("", nx, ny, 1, gdal.GDT_Byte)
    ds.SetGeoTransform(gt)
    src = ogr.Open(gaya.GPKG)
    gdal.RasterizeLayer(ds, [1], src.GetLayer("batas_subdas"), burn_values=[1])
    return ds.ReadAsArray().astype(bool)


def grid_lapisan():
    lf, ext = rasterisasi("bentuklahan", "bentuklahan", BENTUKLAHAN, RES)
    sl, _ = rasterisasi("kelas_lereng", "kelas_lereng", LERENG, RES)
    pl, _ = rasterisasi("penggunaan_lahan", "penggunaan_lahan", PENGGUNAAN, RES)
    gt = (ext[0], RES, 0, ext[3], 0, -RES)
    m = topeng_batas(lf.shape[1], lf.shape[0], gt)
    return lf.astype(np.int32), sl.astype(np.int32), pl.astype(np.int32), m, gt, ext


def grid_kombinasi():
    lf, sl, pl, m, gt, ext = grid_lapisan()
    sah = m & (lf > 0) & (sl > 0) & (pl > 0)
    kode = np.where(sah, lf * 100 + sl * 10 + pl, 0).astype(np.int32)
    return kode, gt, ext


def isi_kosong(a, m):
    """Isi piksel kosong di dalam batas dengan kelas tetangga terdekat (celah rasterisasi)."""
    idx = ndimage.distance_transform_edt(a == 0, return_distances=False, return_indices=True)
    return np.where(m, a[tuple(idx)], 0).astype(np.int32)


def saring_ulang(a, m, gt):
    """Sieve diulang sampai stabil; mengembalikan hasil dan jumlah putaran."""
    cur = a
    for putaran in range(1, 51):
        nxt = np.where(m, saring(cur, gt), 0)
        if (nxt == cur).all():
            return cur, putaran
        cur = nxt
    return cur, putaran


def patch(kode):
    """Daftar ukuran patch (piksel) per kode, konektivitas-8."""
    struktur = np.ones((3, 3), bool)
    ukuran, per_kode = [], {}
    for k in np.unique(kode):
        if k == 0:
            continue
        lab, n = ndimage.label(kode == k, structure=struktur)
        s = np.bincount(lab.ravel())[1:]
        ukuran.extend(s.tolist())
        per_kode[int(k)] = s
    return np.array(ukuran), per_kode


def saring(kode, gt):
    drv = gdal.GetDriverByName("MEM")
    src = drv.Create("", kode.shape[1], kode.shape[0], 1, gdal.GDT_Int32)
    src.SetGeoTransform(gt)
    src.GetRasterBand(1).WriteArray(kode)
    src.GetRasterBand(1).SetNoDataValue(0)
    dst = drv.Create("", kode.shape[1], kode.shape[0], 1, gdal.GDT_Int32)
    dst.SetGeoTransform(gt)
    gdal.SieveFilter(src.GetRasterBand(1), src.GetRasterBand(1).GetMaskBand(), dst.GetRasterBand(1), MLA_PX, 8)
    hasil = dst.GetRasterBand(1).ReadAsArray()
    return np.where(kode > 0, hasil, 0)


def nama_kode(k):
    lf, sl, pl = k // 100, (k // 10) % 10, k % 10
    return f"{PENGGUNAAN[pl - 1]} {BENTUKLAHAN[lf - 1]} {LERENG[sl - 1].split(' (')[0]}"


def tabulasi_silang():
    hasil = {}
    for a, gl in gaya.baca_layer("bentuklahan"):
        for b, gp in gaya.baca_layer("penggunaan_lahan"):
            if gl.Intersects(gp):
                luas = gl.Intersection(gp).GetArea() / 1e4
                kunci = (a["bentuklahan"], b["penggunaan_lahan"])
                hasil[kunci] = hasil.get(kunci, 0) + luas
    tabel = {lf: {pl: round(hasil.get((lf, pl), 0.0), 2) for pl in PENGGUNAAN} for lf in BENTUKLAHAN}
    return tabel


def lereng_copdem():
    dem = gdal.Open(os.path.join(TERBUKA, "copdem_glo30_30m.tif"))
    sl = gdal.DEMProcessing("", dem, "slope", format="MEM", slopeFormat="percent", computeEdges=True).ReadAsArray()
    m = topeng_batas(dem.RasterXSize, dem.RasterYSize, dem.GetGeoTransform())
    batas = [0, 8, 15, 25, 45, 1e9]
    kelas = np.digitize(sl[m], batas[1:-1], right=False)
    persen = {LERENG[i]: round(float((kelas == i).mean() * 100), 1) for i in range(5)}
    return persen, round(float(np.median(sl[m])), 1)


def main():
    stat = {"mla_ha": MLA_HA, "resolusi_analisis_m": RES}
    kode, gt, _ = grid_kombinasi()
    luas_total = (kode > 0).sum() * RES ** 2 / 1e4
    ukuran, per_kode = patch(kode)
    kecil = ukuran < MLA_PX
    stat["tumpang_susun"] = {
        "luas_teranalisis_ha": round(float(luas_total), 2),
        "jumlah_kombinasi": len(per_kode),
        "jumlah_poligon": int(len(ukuran)),
        "poligon_lebih_kecil_dari_mla": int(kecil.sum()),
        "persen_poligon_kecil": round(float(kecil.mean() * 100), 2),
        "persen_luas_pada_poligon_kecil": round(float(ukuran[kecil].sum() / ukuran.sum() * 100), 2),
        "kombinasi_dengan_luas_total_kurang_dari_mla": int(sum(s.sum() < MLA_PX for s in per_kode.values())),
    }
    lf, sl, pl, m, gt, _ = grid_lapisan()
    per_lapisan = {}
    for nama, a in (("bentuklahan", lf), ("kelas_lereng", sl), ("penggunaan_lahan", pl)):
        u, _ = patch(np.where(m, a, 0))
        per_lapisan[nama] = {"jumlah_poligon": int(len(u)), "poligon_lebih_kecil_dari_mla": int((u < MLA_PX).sum())}
    stat["per_lapisan"] = per_lapisan

    sl_g, putaran_sl = saring_ulang(isi_kosong(sl, m), m, gt)
    u_sl, pk_sl = patch(sl_g)
    luas_kelas = lambda pk: {LERENG[k - 1]: round(float(s.sum() * RES ** 2 / 1e4), 1) for k, s in sorted(pk.items())}
    _, pk_sl0 = patch(np.where(m, sl, 0))
    tahap2 = np.where(m, isi_kosong(lf, m) * 100 + sl_g * 10 + isi_kosong(pl, m), 0).astype(np.int32)
    u2, pk2 = patch(tahap2)
    tersaring, putaran_akhir = saring_ulang(tahap2, m, gt)
    u3, pk3 = patch(tersaring)
    stat["generalisasi_otomatis"] = {
        "lereng": {
            "putaran_sieve": putaran_sl,
            "jumlah_poligon_setelah": int(len(u_sl)),
            "persen_piksel_berubah_kelas": round(float(((sl_g != sl) & m & (sl > 0)).sum() / (m & (sl > 0)).sum() * 100), 1),
            "luas_kelas_ha_sebelum": luas_kelas(pk_sl0),
            "luas_kelas_ha_sesudah": luas_kelas(pk_sl),
        },
        "tumpang_susun_ulang": {"jumlah_poligon": int(len(u2)), "poligon_lebih_kecil_dari_mla": int((u2 < MLA_PX).sum()),
                                "jumlah_kombinasi": len(pk2)},
        "akhir": {"putaran_sieve": putaran_akhir, "jumlah_poligon": int(len(u3)),
                  "poligon_lebih_kecil_dari_mla": int((u3 < MLA_PX).sum()), "jumlah_kombinasi": len(pk3),
                  "luas_rata_rata_poligon_ha": round(float(u3.mean() * RES ** 2 / 1e4), 2),
                  "kombinasi_terbesar": sorted(((nama_kode(k), round(float(s.sum() * RES ** 2 / 1e4), 2)) for k, s in pk3.items()),
                                               key=lambda x: -x[1])[:5]},
    }
    per_kode2 = pk3
    titik = gaya.baca_layer("titik_sampel_rencana")
    strata = {a["satuan_lahan"] for a, _ in titik}
    nama2 = {nama_kode(k) for k in per_kode2}
    nama_asli = {nama_kode(k) for k in per_kode}
    stat["sampel"] = {
        "jumlah_titik": len(titik),
        "jumlah_strata_tersampel": len(strata),
        "strata_tersampel_yang_ada_pada_tumpang_susun_asli": len(strata & nama_asli),
        "strata_tersampel_yang_bertahan_setelah_generalisasi_otomatis": len(strata & nama2),
        "kombinasi_setelah_generalisasi_tanpa_sampel": len(nama2 - strata),
    }
    stat["tabulasi_bentuklahan_penggunaan_ha"] = tabulasi_silang()
    lidar = {a["kelas_lereng"]: a["luas_ha"] for a, _ in gaya.baca_layer("kelas_lereng")}
    total = sum(lidar.values())
    persen_cop, median_cop = lereng_copdem()
    stat["kelas_lereng_persen"] = {
        "dtm_lidar_data_proyek": {k: round(v / total * 100, 1) for k, v in lidar.items()},
        "copernicus_dem_30m": persen_cop,
        "median_lereng_copdem_persen": median_cop,
    }
    os.makedirs(os.path.dirname(KELUAR), exist_ok=True)
    with open(KELUAR, "w", encoding="utf-8") as fh:
        json.dump(stat, fh, indent=2, ensure_ascii=False)
    print(json.dumps(stat, indent=2, ensure_ascii=False))
    return stat, kode, tersaring


if __name__ == "__main__":
    main()
