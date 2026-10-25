"""Mengunduh potongan data terbuka untuk Sub-DAS Bompon dan menyelaraskannya ke grid acuan.

Jalankan: python3 "Source/Data Bompon/skrip/unduh_data_terbuka.py"

Keluaran (folder Source/Data Bompon/terbuka/):
- sentinel2_l2a_<tanggal>_10m.tif : reflektansi permukaan Sentinel-2 L2A (B02, B03, B04, B05, B06,
  B07, B08, B8A, B11, B12), float32, grid 10 m EPSG:32749
- sentinel2_l2a_<tanggal>_scl_10m.tif : Scene Classification Layer (tetangga terdekat)
- copdem_glo30_30m.tif : Copernicus DEM GLO-30 diproyeksikan ke EPSG:32749, grid 30 m
- metadata.json : sumber, tanggal akses, dan parameter pengolahan

Grid acuan sama dengan praktik Modul 2: batas penyangga 200 m dari batas Sub-DAS yang
dibulatkan ke kelipatan ukuran piksel. Hanya jendela wilayah kajian yang dibaca dari
berkas Cloud-Optimized GeoTIFF (COG), bukan seluruh petak.
"""
import datetime
import json
import os
import urllib.request

from osgeo import gdal

gdal.UseExceptions()
gdal.SetConfigOption("GDAL_DISABLE_READDIR_ON_OPEN", "EMPTY_DIR")
gdal.SetConfigOption("CPL_VSIL_CURL_ALLOWED_EXTENSIONS", ".tif")

DASAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KELUAR = os.path.join(DASAR, "terbuka")
STAC = "https://earth-search.aws.element84.com/v1/collections/sentinel-2-l2a/items/"
ADEGAN = "S2B_49MCM_20250721_0_L2A"
KANAL = [("B02", "blue"), ("B03", "green"), ("B04", "red"), ("B05", "rededge1"), ("B06", "rededge2"),
         ("B07", "rededge3"), ("B08", "nir"), ("B8A", "nir08"), ("B11", "swir16"), ("B12", "swir22")]
COPDEM = ("https://copernicus-dem-30m.s3.amazonaws.com/Copernicus_DSM_COG_10_S08_00_E110_00_DEM/"
          "Copernicus_DSM_COG_10_S08_00_E110_00_DEM.tif")
BATAS_10M = (396060, 9162990, 397980, 9166610)   # xmin, ymin, xmax, ymax
BATAS_30M = (396060, 9162990, 397980, 9166620)


def warp(sumber, tujuan, batas, resolusi, metode, tipe=gdal.GDT_Float32, nodata=None):
    return gdal.Warp(tujuan, sumber, format="MEM" if tujuan == "" else "GTiff", dstSRS="EPSG:32749",
                     outputBounds=batas, xRes=resolusi, yRes=resolusi, resampleAlg=metode,
                     outputType=tipe, dstNodata=nodata, creationOptions=None if tujuan == "" else ["COMPRESS=DEFLATE"])


def main():
    os.makedirs(KELUAR, exist_ok=True)
    item = json.load(urllib.request.urlopen(STAC + ADEGAN, timeout=60))
    aset = item["assets"]
    tanggal = item["properties"]["datetime"][:10].replace("-", "")
    # Pada katalog Earth Search, offset BOA (-1000 DN) sudah diterapkan ke berkas COG bila
    # earthsearch:boa_offset_applied = True; offset pada raster:bands tidak boleh diterapkan lagi.
    offset_sudah = bool(item["properties"].get("earthsearch:boa_offset_applied"))

    lapis = []
    for nama, kunci in KANAL:
        rb = aset[kunci]["raster:bands"][0]
        resolusi_asli = aset[kunci].get("gsd") or rb.get("spatial_resolution")
        metode = "near" if resolusi_asli == 10 else "bilinear"
        ds = warp("/vsicurl/" + aset[kunci]["href"], "", BATAS_10M, 10, metode)
        arr = ds.GetRasterBand(1).ReadAsArray().astype("float32")
        lapis.append((nama, arr * rb["scale"] + (0.0 if offset_sudah else rb["offset"]), ds))
        print("kanal", nama, "selesai")
    acuan = lapis[0][2]
    berkas = os.path.join(KELUAR, f"sentinel2_l2a_{tanggal}_10m.tif")
    out = gdal.GetDriverByName("GTiff").Create(berkas, acuan.RasterXSize, acuan.RasterYSize, len(lapis),
                                               gdal.GDT_Float32, ["COMPRESS=DEFLATE", "PREDICTOR=3"])
    out.SetGeoTransform(acuan.GetGeoTransform())
    out.SetProjection(acuan.GetProjection())
    for i, (nama, arr, _) in enumerate(lapis, start=1):
        b = out.GetRasterBand(i)
        b.WriteArray(arr)
        b.SetDescription(nama)
    out = None

    warp("/vsicurl/" + aset["scl"]["href"], os.path.join(KELUAR, f"sentinel2_l2a_{tanggal}_scl_10m.tif"),
         BATAS_10M, 10, "near", gdal.GDT_Byte)
    warp("/vsicurl/" + COPDEM, os.path.join(KELUAR, "copdem_glo30_30m.tif"), BATAS_30M, 30, "bilinear")

    meta = {
        "diakses": datetime.date.today().isoformat(),
        "sentinel2": {
            "adegan": ADEGAN,
            "tanggal_perekaman": item["properties"]["datetime"],
            "processing_baseline": item["properties"].get("s2:processing_baseline"),
            "tutupan_awan_petak_persen": item["properties"].get("eo:cloud_cover"),
            "katalog": STAC + ADEGAN,
            "konversi": ("reflektansi = DN * 0.0001 (offset BOA sudah diterapkan pada COG)" if offset_sudah
                         else "reflektansi = DN * 0.0001 - 0.1"),
            "earthsearch_boa_offset_applied": offset_sudah,
            "kanal": [k for k, _ in KANAL],
            "atribusi": "Contains modified Copernicus Sentinel data 2025",
        },
        "copernicus_dem": {
            "sumber": COPDEM,
            "doi": "https://doi.org/10.5270/ESA-c5d3d65",
            "catatan": "DSM (permukaan termasuk tajuk dan bangunan), resolusi asli 1 detik busur",
        },
        "grid": {"epsg": 32749, "batas_10m": BATAS_10M, "batas_30m": BATAS_30M},
    }
    with open(os.path.join(KELUAR, "metadata.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
    print("selesai:", os.listdir(KELUAR))


if __name__ == "__main__":
    main()
