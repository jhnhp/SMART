"""Buat titik latih/uji tutupan material Sub-DAS Bompon untuk Praktik 5.

Sumber kelas: raster ESRI Grid `Source/Material` (1 m, EPSG:32749), hasil
PolygonToRaster dari peta tutupan material Malik (2017) yang dipakai
Fatmawati (2026) sebagai kovariat P. Nama kelas dicocokkan dengan legenda
Gambar 2.2 tesis Fatmawati (2026) berdasarkan sebaran spasial tiap kode.

Desain sampel:
- Kandidat = pusat sel grid kovariat 10 m (konstanta GRID_10M), sehingga
  setiap titik jatuh pada satu sel kovariat yang berbeda.
- Kandidat harus berada >= JARAK_TEPI m di dalam poligon kelasnya (mengurangi
  sel campuran di batas kelas) dan di dalam batas Sub-DAS.
- Sebaran merata per kelas: K-means (k = N_PER_KELAS) pada koordinat kandidat,
  lalu dipilih kandidat terdekat ke setiap pusat klaster.
- Kolom `subset`: 70/30 latih/uji acak berstrata per kelas (21/9).

Keluaran di data/praktik-5/:
- `titik_tutupan_material.gpkg` dan `.csv`: titik latih/uji (CSV dibaca notebook).
- `material_acuan_10m.tif`: peta acuan dirapatkan ke grid kovariat 10 m (modus),
  hanya untuk pembanding peta prediksi, bukan kovariat.
- `material_acuan_10m.qml`: gaya QGIS dengan warna dan nama kelas, dimuat otomatis oleh QGIS.

Jalankan:  python pelatihan_titik_tutupan_material.py
Butuh: numpy, scipy, scikit-learn, rasterio, geopandas.
"""
from pathlib import Path

import geopandas as gpd
import numpy as np
import rasterio
from scipy import ndimage
from shapely.geometry import Point
from sklearn.cluster import KMeans

AKAR = Path(__file__).resolve().parents[2]
RASTER_MATERIAL = AKAR / "Source" / "Material"
DIR_P5 = AKAR / "Output" / "Pelatihan" / "data" / "praktik-5"
# Grid kovariat 10 m Praktik 5 (sama dengan BATAS_10M pada pelatihan_siapkan_data.py). Ditulis sebagai
# konstanta karena folder kovariat/ dibangun ulang oleh uji QGIS setelah skrip ini dijalankan.
GRID_10M = rasterio.transform.from_origin(396060, 9166610, 10, 10)
UKURAN_GRID = (362, 192)  # baris, kolom
BATAS = DIR_P5 / "bompon_vektor.gpkg"
KELUARAN = DIR_P5 / "titik_tutupan_material.gpkg"
KELUARAN_CSV = DIR_P5 / "titik_tutupan_material.csv"
ACUAN_10M = DIR_P5 / "material_acuan_10m.tif"

N_PER_KELAS = 30
PROPORSI_UJI = 0.3
JARAK_TEPI = 15.0  # m
SEED = 42

# Kode raster -> nama kelas (legenda Gambar 2.2 Fatmawati, 2026; dari Malik, 2017).
# Dicocokkan lewat posisi spasial; kode 5 dan 6 berurutan terbalik dari legenda.
KELAS = {
    1: "Breksi andesit sisipan diorit",
    2: "Breksi andesit teralterasi",
    3: "Breksi andesit teralterasi, ditumpangi lapukan batupasir Menoreh",
    4: "Breksi vulkanik",
    5: "Endapan material Sumbing Muda, pasir tufan, tuff pasiran, breksi andesit",
    6: "Endapan Sumbing Muda dan endapan material longsor",
    7: "Tuff pasiran",
}
# Palet Okabe-Ito, sama dengan notebook Praktik 5 dan uji QGIS, agar peta acuan dan prediksi tampil serupa.
WARNA = {1: "#E69F00", 2: "#56B4E9", 3: "#0072B2", 4: "#009E73", 5: "#F0E442", 6: "#D55E00", 7: "#CC79A7"}


def main() -> None:
    rng = np.random.default_rng(SEED)

    with rasterio.open(RASTER_MATERIAL) as src:
        mat = src.read(1)
        nodata = src.nodata
        tf_mat = src.transform
        crs = src.crs
    valid = mat != nodata

    # Jarak (m) setiap piksel 1 m ke tepi kelasnya sendiri.
    jarak = np.zeros(mat.shape, dtype=np.float32)
    for k in KELAS:
        m = mat == k
        jarak[m] = ndimage.distance_transform_edt(m, sampling=abs(tf_mat.a))[m]

    # Pusat sel grid kovariat 10 m.
    assert crs.to_epsg() == 32749, "Raster material harus memakai EPSG:32749 seperti kovariat"
    rows, cols = np.mgrid[0 : UKURAN_GRID[0], 0 : UKURAN_GRID[1]]
    xs, ys = rasterio.transform.xy(GRID_10M, rows.ravel(), cols.ravel())
    xs, ys = np.asarray(xs), np.asarray(ys)

    r_m, c_m = rasterio.transform.rowcol(tf_mat, xs, ys)
    r_m, c_m = np.asarray(r_m), np.asarray(c_m)
    di_dalam = (r_m >= 0) & (r_m < mat.shape[0]) & (c_m >= 0) & (c_m < mat.shape[1])
    xs, ys, r_m, c_m = xs[di_dalam], ys[di_dalam], r_m[di_dalam], c_m[di_dalam]
    ok = valid[r_m, c_m] & (jarak[r_m, c_m] >= JARAK_TEPI)

    batas = gpd.read_file(BATAS, layer="batas_subdas").to_crs(crs).union_all()
    kand = gpd.GeoDataFrame(
        {"kode": mat[r_m[ok], c_m[ok]].astype(int)},
        geometry=gpd.points_from_xy(xs[ok], ys[ok]),
        crs=crs,
    )
    kand = kand[kand.within(batas)].reset_index(drop=True)

    baris = []
    for k, nama in KELAS.items():
        sub = kand[kand.kode == k]
        xy = np.column_stack([sub.geometry.x, sub.geometry.y])
        if len(xy) < N_PER_KELAS:
            raise RuntimeError(f"Kandidat kelas {k} hanya {len(xy)}")
        km = KMeans(n_clusters=N_PER_KELAS, n_init=10, random_state=SEED).fit(xy)
        pilih = []
        for c in km.cluster_centers_:
            urut = np.argsort(((xy - c) ** 2).sum(axis=1))
            pilih.append(next(i for i in urut if i not in pilih))
        n_uji = round(N_PER_KELAS * PROPORSI_UJI)
        subset = np.array(["latih"] * (N_PER_KELAS - n_uji) + ["uji"] * n_uji)
        rng.shuffle(subset)
        for i, s in zip(pilih, subset):
            x, y = xy[i]
            baris.append(
                {"kode": k, "material": nama, "subset": s, "x": x, "y": y,
                 "jarak_tepi_m": float(jarak[rasterio.transform.rowcol(tf_mat, x, y)]),
                 "geometry": Point(x, y)}
            )

    out = gpd.GeoDataFrame(baris, crs=crs)
    out.insert(0, "id", [f"M{k}-{i + 1:02d}" for k, g in out.groupby("kode") for i in range(len(g))])
    try:
        KELUARAN.unlink(missing_ok=True)
        out.to_file(KELUARAN, layer="titik_tutupan_material", driver="GPKG")
        print(f"Tersimpan: {KELUARAN.name} ({len(out)} titik)")
    except PermissionError:
        print(f"PERINGATAN: {KELUARAN.name} sedang dibuka aplikasi lain dan tidak ditimpa.")
    out.drop(columns="geometry").round({"x": 2, "y": 2, "jarak_tepi_m": 1}).to_csv(KELUARAN_CSV, index=False)
    print(out.groupby(["kode", "subset"]).size().unstack())
    print(f"Tersimpan: {KELUARAN_CSV.name}")
    peta_acuan_10m(mat, nodata, tf_mat, crs)


def tulis_qml(jalur: Path) -> None:
    """Gaya QGIS (Paletted/Unique values) dengan warna dan nama kelas. QGIS memuatnya otomatis
    bila namanya sama dengan raster. Tabel warna GeoTIFF tidak dipakai karena selalu berisi
    256 entri, sehingga legenda QGIS menampilkan nilai 0-255."""
    entri = "\n".join(f'        <paletteEntry value="{k}" label="{k}. {v}" alpha="255" color="{WARNA[k].lower()}"/>' for k, v in KELAS.items())
    jalur.write_text(f"""<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.34.13" styleCategories="Symbology">
  <pipe>
    <rasterrenderer type="paletted" band="1" alphaBand="-1" nodataColor="" opacity="1">
      <colorPalette>
{entri}
      </colorPalette>
    </rasterrenderer>
    <brightnesscontrast brightness="0" contrast="0" gamma="1"/>
    <huesaturation colorizeGreen="128" saturation="0" colorizeBlue="128" grayscaleMode="0" colorizeStrength="100" invertColors="0" colorizeOn="0" colorizeRed="255"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
""", encoding="utf-8")


def peta_acuan_10m(mat, nodata, tf_mat, crs) -> None:
    """Rapatkan peta 1 m ke grid kovariat 10 m dengan kelas terbanyak (modus) per sel."""
    from rasterio.enums import Resampling
    from rasterio.warp import reproject

    tujuan = np.zeros(UKURAN_GRID, dtype=np.uint8)
    reproject(mat, tujuan, src_transform=tf_mat, src_crs=crs, src_nodata=nodata,
              dst_transform=GRID_10M, dst_crs=crs, dst_nodata=0, resampling=Resampling.mode)
    profil = dict(driver="GTiff", height=UKURAN_GRID[0], width=UKURAN_GRID[1], count=1, dtype="uint8",
                  crs=crs, transform=GRID_10M, nodata=0, compress="deflate")
    with rasterio.open(ACUAN_10M, "w", **profil) as d:
        d.write(tujuan, 1)
    tulis_qml(ACUAN_10M.with_suffix(".qml"))
    kelas, n = np.unique(tujuan[tujuan > 0], return_counts=True)
    print(f"Tersimpan: {ACUAN_10M.name}", dict(zip(kelas.tolist(), n.tolist())))


if __name__ == "__main__":
    main()
