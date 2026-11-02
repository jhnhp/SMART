"""
Skrip Pemotongan (Clip by Mask Layer) Seluruh Raster Menggunakan Batas Poligon Sub-DAS Bompon
Memastikan semua data raster dan hasil pemodelan terpotong rapi mengikuti bentuk batas_subdas.gpkg
"""

import os
import glob
from osgeo import gdal, ogr

BASE_DIR = "/home/jhn/Documents/Sayangku/Modul Junun"
MASK_PATH = os.path.join(BASE_DIR, "Output/Pelatihan/data/praktik-1/batas_subdas.gpkg")

def clip_raster_inplace(raster_path, nodata_val=None):
    if not os.path.exists(raster_path):
        return
    
    tmp_path = raster_path + ".tmp.tif"
    
    # Deteksi nodata
    ds = gdal.Open(raster_path)
    if ds is None:
        return
    band1 = ds.GetRasterBand(1)
    orig_nodata = band1.GetNoDataValue()
    ds = None
    
    target_nodata = nodata_val if nodata_val is not None else (orig_nodata if orig_nodata is not None else -9999)
    
    warp_opts = gdal.WarpOptions(
        cutlineDSName=MASK_PATH,
        cropToCutline=False, # Mempertahankan grid origin & pixel alignment
        dstNodata=target_nodata
    )
    
    gdal.Warp(tmp_path, raster_path, options=warp_opts)
    
    if os.path.exists(tmp_path):
        os.replace(tmp_path, raster_path)
        print(f"  [KLIP BERHASIL] {os.path.relpath(raster_path, BASE_DIR)} (NoData={target_nodata})")

def main():
    print("==================================================================")
    print("MEMULAI PROSES CLIP RASTER BY MASK LAYER (BATAS SUB-DAS BOMPON)")
    print("==================================================================")
    
    # 1. Praktik 1 (Data terpotong)
    print("\n-> Memotong Raster Praktik 1...")
    clip_raster_inplace(f"{BASE_DIR}/Output/Pelatihan/data/praktik-1/sentinel2_l2a_20250721_10m.tif", 0)
    clip_raster_inplace(f"{BASE_DIR}/Output/Pelatihan/data/praktik-1/sentinel1_rtc_20240830_10m.tif", 0)
    clip_raster_inplace(f"{BASE_DIR}/Output/Pelatihan/data/praktik-1/copdem_glo30_30m.tif", -9999)

    # 2. Praktik 2
    print("\n-> Memotong Raster Praktik 2...")
    clip_raster_inplace(f"{BASE_DIR}/Output/Pelatihan/data/praktik-2/copdem_10m.tif", -9999)
    clip_raster_inplace(f"{BASE_DIR}/Output/Pelatihan/data/praktik-2/slope_10m.tif", -9999)
    clip_raster_inplace(f"{BASE_DIR}/Output/Pelatihan/data/praktik-2/hillshade_10m.tif", 0)
    clip_raster_inplace(f"{BASE_DIR}/Output/Pelatihan/data/praktik-2/sentinel2_l2a_20250721_10m.tif", 0)

    # 3. Praktik 4
    print("\n-> Memotong Raster Praktik 4...")
    for f in [
        "sentinel2_l2a_20250721_10m.tif",
        "sentinel2_l2a_20240813_10m.tif",
        "sentinel2_l2a_20250721_scl_10m.tif",
        "ndvi_20250721.tif",
        "bsi_20250721.tif",
        "masker_tanah_terbuka_20250721.tif",
        "ndvi_20240813.tif",
        "bsi_20240813.tif",
        "masker_tanah_terbuka_20240813.tif",
        "barest_earth_bsi_composite.tif"
    ]:
        p = f"{BASE_DIR}/Output/Pelatihan/data/praktik-4/{f}"
        nd = 0 if "masker" in f or "sentinel" in f else -9999
        clip_raster_inplace(p, nd)

    # 4. Praktik 5 (Kovariat)
    print("\n-> Memotong Raster Kovariat Praktik 5...")
    for f in glob.glob(f"{BASE_DIR}/Output/Pelatihan/data/praktik-5/kovariat/*.tif"):
        nd = 0 if "sentinel" in f or "hillshade" in f or "penggunaan" in f else -9999
        clip_raster_inplace(f, nd)

    print("\n==================================================================")
    print("SEMUA DATA RASTER TELAH BERHASIL DIKLIP MENGIKUTI BATAS SUB-DAS!")
    print("==================================================================")

if __name__ == "__main__":
    main()
