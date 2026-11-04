#!/usr/bin/env python3
"""Menyusun data masukan praktik di Output/Pelatihan/data/praktik-{1..5}.

Hanya menyalin atau memotong data dari Source/; tidak ada nilai yang dibuat-buat.
Keluaran contoh (folder hasil-contoh/) tidak dibuat di sini, melainkan oleh
pelatihan_uji_semua.sh saat uji coba.

Jalankan: python3 Output/scripts/pelatihan_siapkan_data.py
"""
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


def jalur_demnas():
    """DEMNAS lembar 1408-23 (0,27 detik busur, sekitar 8 m), di Source/ atau Source/DEMNAS/."""
    for jalur in (os.path.join(AKAR, "Source", "DEMNAS_1408-23_v1.0.tif"), os.path.join(AKAR, "Source", "DEMNAS", "DEMNAS_1408-23_v1.0.tif")):
        if os.path.exists(jalur):
            return jalur
    raise FileNotFoundError("DEMNAS_1408-23_v1.0.tif tidak ditemukan di Source/ maupun Source/DEMNAS/")


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


def spektra(tujuan_spektra):
    """Pustaka spektral sampel tanah Site Gunung Madu Plantation, disalin apa adanya dalam bentuk terkompresi."""
    with open(os.path.join(PSS, "data spectro geo.csv"), "rb") as masuk, gzip.open(tujuan_spektra, "wb") as keluar:
        shutil.copyfileobj(masuk, keluar)


def spektrum_sampel_baru(tujuan, n_lapisan_4=8, seed=3):
    """Berkas contoh (dummy) untuk bagian 13 notebook Praktik 3, berformat seperti hasil pengukuran sampel baru:
    kolom `sampel` dan w350-w2500 tanpa kolom laboratorium. Isinya spektrum asli dari pustaka yang sama, bukan nilai
    rekaan: dua sampel lapisan 1 yang memang tidak memiliki hasil laboratorium, ditambah beberapa sampel lapisan 4
    yang dipilih acak sebagai contoh tanah yang tidak dipakai melatih model lapisan 1."""
    import csv
    import random
    with open(os.path.join(PSS, "data spectro geo.csv"), encoding="utf-8-sig") as f:
        baris = list(csv.reader(f))
    kepala = baris[0]
    i_sampel, i_lempung = kepala.index("sampel"), kepala.index("clay")
    i_spektrum = [i for i, k in enumerate(kepala) if k.startswith("w") and k[1:].isdigit()]
    tanpa_lab = [r for r in baris[1:] if r[i_sampel].endswith(" L1") and not r[i_lempung].strip()]
    lapisan_4 = [r for r in baris[1:] if r[i_sampel].endswith(" L4") and r[i_lempung].strip()]
    pilih = sorted(random.Random(seed).sample(lapisan_4, n_lapisan_4), key=lambda r: int(r[i_sampel].split()[0][1:]))
    with open(tujuan, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["sampel"] + [kepala[i] for i in i_spektrum])
        for r in tanpa_lab + pilih:
            w.writerow([r[i_sampel]] + [r[i] for i in i_spektrum])


def praktik_1_lidar_demnas():
    """DEMNAS dan DTM LiDAR disalin utuh agar peserta memotongnya sendiri; foto udara 5–8 cm dirata-ratakan ke 1 m."""
    from osgeo import gdal
    import glob
    import tempfile
    gdal.UseExceptions()
    salin(jalur_demnas(), p(1, "DEMNAS_1408-23_v1.0.tif"))
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


def praktik_5_demnas():
    """DEMNAS untuk kovariat medan Praktik 5: diproyeksikan ke UTM 49S pada piksel 8 m dan dipotong ke grid 10 m
    ditambah penyangga 500 m, agar TPI, TRI, dan TWI di tepi Sub-DAS tidak terpotong. Berkas asal tidak memiliki
    CRS, sehingga EPSG:4326 ditetapkan seperti pada Praktik 1."""
    from osgeo import gdal
    gdal.UseExceptions()
    b = 500
    gdal.Warp(p(5, "demnas_8m.tif"), jalur_demnas(), srcSRS="EPSG:4326", dstSRS="EPSG:32749",
              outputBounds=(BATAS_10M[0] - b, BATAS_10M[1] - b, BATAS_10M[2] + b, BATAS_10M[3] + b),
              xRes=8, yRes=8, targetAlignedPixels=True, resampleAlg="bilinear", outputType=gdal.GDT_Float32,
              dstNodata=-9999, creationOptions=["COMPRESS=DEFLATE"])


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
    spektrum_sampel_baru(p(3, "spektrum_sampel_baru.csv"))

    # Praktik 4: dua tanggal citra dengan SCL masing-masing
    for nama in ("sentinel2_l2a_20250721_10m.tif", "sentinel2_l2a_20250721_scl_10m.tif", "sentinel2_l2a_20240813_10m.tif"):
        salin(os.path.join(TERBUKA, nama), p(4, nama))
    unduh_scl_2024(p(4, "sentinel2_l2a_20240813_scl_10m.tif"))
    layer_vektor(p(4, "bompon_vektor.gpkg"), "batas_subdas", "penggunaan_lahan", "jalan")

    # Praktik 5: data dasar kovariat. Atribut medan memakai DEMNAS 8 m. Titik latih/uji tutupan material dan
    # peta acuan 10 m dibuat terpisah oleh pelatihan_titik_tutupan_material.py (memerlukan rasterio, geopandas,
    # scikit-learn).
    praktik_5_demnas()
    layer_vektor(p(5, "bompon_vektor.gpkg"), "batas_subdas", "bentuklahan", "penggunaan_lahan", "sungai")

    print("Selesai.")
    for n in range(1, 6):
        print(n, sorted(os.listdir(os.path.join(DATA, f"praktik-{n}"))))


if __name__ == "__main__":
    main()
