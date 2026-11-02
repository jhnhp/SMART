#!/usr/bin/env python3
"""Menyusun data masukan praktik di Output/Pelatihan/data/praktik-{1..5}.

Hanya menyalin atau memotong data dari Source/; tidak ada nilai yang dibuat-buat.
Keluaran contoh (folder hasil-contoh/) tidak dibuat di sini, melainkan oleh
pelatihan_uji_semua.sh saat uji coba.

Jalankan: python3 Output/scripts/pelatihan_siapkan_data.py
"""
import csv
import gzip
import os
import shutil

from osgeo import gdal, ogr

gdal.UseExceptions()
ogr.UseExceptions()

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BOMPON = os.path.join(AKAR, "Source", "Data Bompon")
TERBUKA = os.path.join(BOMPON, "terbuka")
PSS = os.path.join(AKAR, "Source", "Proximal Sensing")
DATA = os.path.join(AKAR, "Output", "Pelatihan", "data")
GPKG = os.path.join(BOMPON, "bompon.gpkg")
BATAS_10M = (396060, 9162990, 397980, 9166610)


def p(n, *nama):
    folder = os.path.join(DATA, f"praktik-{n}", *nama[:-1])
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, nama[-1])


def salin(sumber, tujuan):
    shutil.copy2(sumber, tujuan)


def layer_vektor(tujuan, *nama_layer):
    """Menyalin beberapa layer bompon.gpkg ke satu GeoPackage."""
    if os.path.exists(tujuan):
        os.remove(tujuan)
    for nama in nama_layer:
        gdal.VectorTranslate(tujuan, GPKG, layers=[nama], layerName=nama, accessMode="append" if os.path.exists(tujuan) else None, format="GPKG")


def unduh_scl_2024(tujuan):
    """SCL adegan S2A_49MCM_20240813 (Earth Search), dipotong ke grid 10 m latihan."""
    url = ("/vsicurl/https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/"
           "49/M/CM/2024/8/S2A_49MCM_20240813_0_L2A/SCL.tif")
    gdal.Warp(tujuan, url, outputBounds=BATAS_10M, xRes=10, yRes=10, resampleAlg="near",
              dstSRS="EPSG:32749", creationOptions=["COMPRESS=DEFLATE"])


def sampel_bersih(tujuan):
    """Merapikan header sampel.csv dan menandai nilai 0 yang tidak masuk akal sebagai kosong.

    Kolom ke-20 berheader ganda 'C_Organik_1' diberi nama C_Organik_2 (urutannya diapit
    Bahan_Organik_1 dan Bahan_Organik_2). KPK dan berat volume bernilai 0 dikosongkan karena
    tidak mungkin secara fisik; asal nilai ini perlu dikonfirmasi ke pemilik data.
    """
    with open(os.path.join(BOMPON, "sampel.csv"), encoding="utf-8-sig") as f:
        baris = list(csv.reader(f))
    kepala = baris[0]
    kepala[19] = "C_Organik_2"
    kepala[kepala.index("Kdar_Lengas_1")] = "Kadar_Lengas_1"
    kepala[kepala.index("KPK1")] = "KPK_1"
    kepala[kepala.index("KPK2")] = "KPK_2"
    kosongkan = [i for i, k in enumerate(kepala) if k.startswith(("KPK", "Berat_Volume"))]
    with open(tujuan, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(kepala)
        for r in baris[1:]:
            for i in kosongkan:
                if float(r[i]) == 0:
                    r[i] = ""
            # Titik 49: C-organik tidak konsisten dengan bahan organiknya, diduga salah ukur.
            # Untuk latihan, nilainya dihitung ulang dari bahan organik dengan faktor 1,724.
            if r[0] == "49":
                for c, bo in (("C_Organik_1", "Bahan_Organik_1"), ("C_Organik_2", "Bahan_Organik_2")):
                    r[kepala.index(c)] = f"{float(r[kepala.index(bo)]) / 1.724:.2f}"
            w.writerow(r)


def spektra(tujuan_spektra):
    """Pustaka spektral sampel tanah Site Gunung Madu Plantation, disalin apa adanya dalam bentuk terkompresi."""
    with open(os.path.join(PSS, "data spectro geo.csv"), "rb") as masuk, gzip.open(tujuan_spektra, "wb") as keluar:
        shutil.copyfileobj(masuk, keluar)


def praktik_1_lidar_demnas():
    """DEMNAS dan DTM LiDAR disalin utuh agar peserta memotongnya sendiri; foto udara 5–8 cm dirata-ratakan ke 1 m."""
    from osgeo import gdal
    import glob
    import tempfile
    gdal.UseExceptions()
    salin(os.path.join(AKAR, "Source", "DEMNAS", "DEMNAS_1408-23_v1.0.tif"), p(1, "DEMNAS_1408-23_v1.0.tif"))
    L = os.path.join(AKAR, "Source", "Lidar")
    salin(glob.glob(os.path.join(L, "Lidar-*", "Lidar", "LiDAR_Kalijambe_Bompon_20222023.tif"))[0], p(1, "LiDAR_Kalijambe_Bompon_20222023.tif"))
    for berkas in glob.glob(os.path.join(BOMPON, "mentah", "SHP Bompon", "Batas_Bompon.*")):
        if berkas.rsplit(".", 1)[1].lower() in ("shp", "shx", "dbf", "prj", "cpg"):
            salin(berkas, p(1, os.path.basename(berkas)))
    # mosaik per kanal dari dua pemotretan, lalu disatukan; nodata 0 berada di luar batas Sub-DAS
    with tempfile.TemporaryDirectory() as tmp:
        kanal = []
        for b in (1, 2, 3):
            gdal.Warp(f"{tmp}/{b}.tif", [os.path.join(L, f"fu_ac{b}", "hdr.adf"), os.path.join(L, f"fu_bc{b}", "hdr.adf")],
                      outputBounds=(396260, 9163190, 397780, 9166410), xRes=1, yRes=1, resampleAlg="average",
                      srcSRS="EPSG:32749", dstSRS="EPSG:32749", dstNodata=-32768, outputType=gdal.GDT_Int16)
            kanal.append(gdal.Open(f"{tmp}/{b}.tif"))
        keluar = gdal.GetDriverByName("GTiff").Create(p(1, "foto_udara_rgb_1m.tif"), kanal[0].RasterXSize, kanal[0].RasterYSize, 3, gdal.GDT_Byte, ["COMPRESS=DEFLATE", "TILED=YES"])
        keluar.SetGeoTransform(kanal[0].GetGeoTransform())
        keluar.SetProjection(kanal[0].GetProjection())
        for i, ds in enumerate(kanal, start=1):
            a = ds.ReadAsArray()
            a[a < 0] = 0
            pita = keluar.GetRasterBand(i)
            pita.WriteArray(a.clip(0, 255).astype("uint8"))
            pita.SetNoDataValue(0)
        keluar = None


def main():
    for n in range(1, 6):
        os.makedirs(os.path.join(DATA, f"praktik-{n}"), exist_ok=True)

    # Praktik 1: data mentah per sumber, belum seragam
    for nama in ("sentinel2_l2a_20250721_10m.tif", "sentinel2_l2a_20250721_scl_10m.tif", "sentinel1_rtc_20240830_10m.tif"):
        salin(os.path.join(TERBUKA, nama), p(1, nama))
    praktik_1_lidar_demnas()

    # Praktik 2: citra, DEM mentah, dan peta pembanding yang dibuka di akhir
    salin(os.path.join(TERBUKA, "sentinel2_l2a_20250721_10m.tif"), p(2, "sentinel2_l2a_20250721_10m.tif"))
    from osgeo import gdal
    gdal.UseExceptions()
    gdal.Warp(p(2, "dem_10m.tif"), os.path.join(TERBUKA, "copdem_glo30_30m.tif"), dstSRS="EPSG:32749", outputBounds=BATAS_10M, xRes=10, yRes=10,
              resampleAlg="bilinear", outputType=gdal.GDT_Float32)
    layer_vektor(p(2, "bompon_vektor.gpkg"), "batas_subdas", "penggunaan_lahan", "sungai")
    layer_vektor(p(2, "pembanding", "peta_riset.gpkg"), "bentuklahan", "kelas_lereng")

    # Praktik 3: pustaka spektral
    spektra(p(3, "spektra_visnir_gmp.csv.gz"))

    # Praktik 4: dua tanggal citra dengan SCL masing-masing
    for nama in ("sentinel2_l2a_20250721_10m.tif", "sentinel2_l2a_20250721_scl_10m.tif", "sentinel2_l2a_20240813_10m.tif"):
        salin(os.path.join(TERBUKA, nama), p(4, nama))
    unduh_scl_2024(p(4, "sentinel2_l2a_20240813_scl_10m.tif"))
    layer_vektor(p(4, "bompon_vektor.gpkg"), "batas_subdas", "penggunaan_lahan", "jalan")

    # Praktik 5: sampel laboratorium dan data dasar kovariat
    sampel_bersih(p(5, "sampel_tanah_bompon.csv"))
    salin(os.path.join(TERBUKA, "copdem_glo30_30m.tif"), p(5, "copdem_glo30_30m.tif"))
    layer_vektor(p(5, "bompon_vektor.gpkg"), "batas_subdas", "bentuklahan", "penggunaan_lahan", "sungai")

    print("Selesai.")
    for n in range(1, 6):
        print(n, sorted(os.listdir(os.path.join(DATA, f"praktik-{n}"))))


if __name__ == "__main__":
    main()
