#!/usr/bin/env python3
"""Membuat gambar lebar untuk sampul modul praktik dari data sebenarnya: alur dari citra sampai peta prediksi."""
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from osgeo import gdal, ogr
from matplotlib.colors import LightSource, ListedColormap

gdal.UseExceptions()
ogr.UseExceptions()
AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D = os.path.join(AKAR, 'Output', 'Pelatihan', 'data')
KELUAR = os.path.join(AKAR, 'Output', 'assets', 'pelatihan', 'sampul_alur_bompon.png')
# palet tutupan material Praktik 5 (Okabe-Ito), kode 1 sampai 7
WARNA_MATERIAL = ['#E69F00', '#56B4E9', '#0072B2', '#009E73', '#F0E442', '#D55E00', '#CC79A7']


def baca(jalur, band=None):
    ds = gdal.Open(jalur)
    return ds.ReadAsArray() if band is None else ds.GetRasterBand(band).ReadAsArray()


def rentang(a, p=(2, 98)):
    lo, hi = np.nanpercentile(a, p)
    return np.clip((a - lo) / (hi - lo), 0, 1)


def garis(gpkg, layer):
    out = []
    ds = ogr.Open(gpkg)
    for f in ds.GetLayerByName(layer):
        g = f.GetGeometryRef()
        for i in range(g.GetGeometryCount()):
            p = g.GetGeometryRef(i)
            cincin = [p] if p.GetGeometryName() == 'LINEARRING' else [p.GetGeometryRef(j) for j in range(p.GetGeometryCount())]
            for c in cincin:
                out.append(np.array(c.GetPoints())[:, :2])
    return out


def main():
    p1, p5 = os.path.join(D, 'praktik-1'), os.path.join(D, 'praktik-5')
    ref = gdal.Open(os.path.join(p1, 'sentinel2_l2a_20250721_10m.tif'))
    gt = ref.GetGeoTransform()
    ex = [gt[0], gt[0] + gt[1] * ref.RasterXSize, gt[3] + gt[5] * ref.RasterYSize, gt[3]]
    a = ref.ReadAsArray()
    swir = np.dstack([rentang(a[8]), rentang(a[6]), rentang(a[1])])
    nir = np.dstack([rentang(a[6]), rentang(a[2]), rentang(a[1])])
    dem = baca(os.path.join(p5, 'kovariat', 'elevasi.tif')).astype(float)
    hs = LightSource(315, 45).hillshade(dem, vert_exag=3, dx=10, dy=10)
    pred = baca(os.path.join(p5, 'hasil-contoh', 'prediksi_material.tif')).astype(float)
    pred[pred == 0] = np.nan
    batas = garis(os.path.join(p1, 'bompon_vektor.gpkg'), 'batas_subdas')
    smu = garis(os.path.join(p5, 'smu_akhir.gpkg'), 'smu_akhir')

    fig, ax = plt.subplots(1, 4, figsize=(12, 5.68), dpi=170)
    fig.subplots_adjust(0, 0, 1, 1, 0.006, 0)
    ax[0].imshow(nir, extent=ex, interpolation='bilinear')
    ax[1].imshow(swir, extent=ex, interpolation='bilinear')
    ax[2].imshow(hs, extent=ex, cmap='gray', interpolation='bilinear')
    for c in smu:
        ax[2].plot(c[:, 0], c[:, 1], color='#ffd500', lw=.45)
    ax[3].imshow(hs, extent=ex, cmap='gray', interpolation='bilinear', alpha=.55)
    ax[3].imshow(pred, extent=ex, cmap=ListedColormap(WARNA_MATERIAL), vmin=.5, vmax=7.5, interpolation='nearest')
    for i, x in enumerate(ax):
        for c in batas:
            x.plot(c[:, 0], c[:, 1], color='#ffd500' if i < 3 else '#01416b', lw=1.3)
        x.set_xlim(ex[0], ex[1]); x.set_ylim(ex[2], ex[3]); x.axis('off')
    os.makedirs(os.path.dirname(KELUAR), exist_ok=True)
    fig.savefig(KELUAR, facecolor='white')
    print('ditulis', KELUAR)


if __name__ == '__main__':
    main()
