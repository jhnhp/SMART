"""Merapikan data mentah Sub-DAS Bompon menjadi satu GeoPackage dan tabel CSV.

Jalankan dari folder mana pun:
    python3 "Source/Data Bompon/skrip/rapikan_data_bompon.py"

Masukan : Source/Data Bompon/mentah/   (data asli, tidak diubah)
Keluaran: Source/Data Bompon/bompon.gpkg
          Source/Data Bompon/tabel/*.csv

Semua layer keluaran memakai WGS 84 / UTM zona 49S (EPSG:32749).
Rincian keputusan pembersihan dicatat di README.md.
"""
import csv
import math
import os
import re
import shutil
import subprocess
import tempfile
import zipfile
from collections import defaultdict

from osgeo import ogr, osr

ogr.UseExceptions()
osr.UseExceptions()

DASAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MENTAH = os.path.join(DASAR, "mentah")
GPKG = os.path.join(DASAR, "bompon.gpkg")
TABEL = os.path.join(DASAR, "tabel")

UTM = osr.SpatialReference()
UTM.ImportFromEPSG(32749)
WGS = osr.SpatialReference()
WGS.ImportFromEPSG(4326)
WGS.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
KE_UTM = osr.CoordinateTransformation(WGS, UTM)
KE_WGS = osr.CoordinateTransformation(UTM, WGS)

LERENG_URUT = ["Datar", "Landai", "Agak Curam", "Curam", "Sangat Curam"]
BENTUKLAHAN = [
    "Interfluve",
    "Lereng Atas Perbukitan",
    "Lereng Tengah Perbukitan",
    "Lereng Bawah Perbukitan",
    "Lereng Kaki Koluvial",
    "Dataran Koluvial",
]
PENGGUNAAN = ["Agroforestri", "Tegalan", "Sawah", "Permukiman"]


# ---------------------------------------------------------------- utilitas
def p(*bagian):
    return os.path.join(MENTAH, *bagian)


def buka(path, layer=None):
    ds = ogr.Open(path)
    lyr = ds.GetLayer(layer) if layer is not None else ds.GetLayer(0)
    return ds, lyr


def buat_layer(ds, nama, geom, fields):
    lyr = ds.CreateLayer(nama, UTM, geom, options=["GEOMETRY_NAME=geom", "FID=fid"])
    for fnama, ftipe in fields:
        lyr.CreateField(ogr.FieldDefn(fnama, ftipe))
    return lyr


def tulis(lyr, geom, **nilai):
    f = ogr.Feature(lyr.GetLayerDefn())
    for k, v in nilai.items():
        if v is not None:
            f.SetField(k, v)
    f.SetGeometry(geom)
    lyr.CreateFeature(f)


def ke_utm(geom, srs):
    g = geom.Clone()
    if srs is not None and not srs.IsSame(UTM):
        srs = srs.Clone()
        srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
        g.Transform(osr.CoordinateTransformation(srs, UTM))
    return g


def jadikan_multi(g):
    if g.GetGeometryType() in (ogr.wkbPolygon, ogr.wkbPolygon25D):
        return ogr.ForceToMultiPolygon(g)
    if g.GetGeometryType() in (ogr.wkbLineString, ogr.wkbLineString25D):
        return ogr.ForceToMultiLineString(g)
    return g


def luas_ha(g):
    return round(g.GetArea() / 10000.0, 4)


def titik_utm(lon, lat):
    x, y, _ = KE_UTM.TransformPoint(lon, lat)
    g = ogr.Geometry(ogr.wkbPoint)
    g.AddPoint_2D(x, y)
    return g


def lonlat(g):
    lon, lat, _ = KE_WGS.TransformPoint(g.GetX(), g.GetY())
    return round(lon, 7), round(lat, 7)


def elevasi(nilai):
    try:
        v = float(nilai)
    except (TypeError, ValueError):
        return None
    return None if v == 0 else round(v, 1)


def kode_sampel(nama):
    m = re.match(r"\s*([ABCabc])\s*(\d+)", nama or "")
    return (m.group(1).upper() + m.group(2)) if m else None


def baca_kml(teks):
    """Kembalikan daftar (nama, waktu, jenis_geom, [(lon, lat), ...]) dari teks KML."""
    hasil = []
    for pm in re.findall(r"<Placemark\b.*?</Placemark>", teks, re.S):
        nama = re.search(r"<name>(.*?)</name>", pm, re.S)
        waktu = re.search(r"<when>(.*?)</when>", pm, re.S)
        for jenis in ("Point", "LineString"):
            blok = re.search(rf"<{jenis}>.*?<coordinates>(.*?)</coordinates>", pm, re.S)
            if blok:
                koordinat = []
                for tok in blok.group(1).split():
                    nilai = tok.split(",")
                    koordinat.append((float(nilai[0]), float(nilai[1])))
                hasil.append((nama.group(1).strip() if nama else "", waktu.group(1).strip() if waktu else None, jenis, koordinat))
                break
    return hasil


def kml_dari(path):
    if path.lower().endswith(".kmz"):
        with zipfile.ZipFile(path) as z:
            return z.read("doc.kml").decode("utf-8")
    with open(path, encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------- isi MPK
def ekstrak_mpk(tujuan):
    subprocess.run(
        ["7z", "x", "-y", f"-o{tujuan}", p("Survei", "ArcGIS", "Survei.mpk")],
        check=True,
        stdout=subprocess.DEVNULL,
    )
    return tujuan


# ---------------------------------------------------------------- layer poligon/garis
def salin_poligon(out, nama, path, layer, petakan, urut=None):
    """petakan: fungsi(feature) -> dict atribut keluaran (tanpa luas_ha)."""
    ds, src = buka(path, layer)
    srs = src.GetSpatialRef()
    baris = []
    for f in src:
        g = f.GetGeometryRef()
        if g is None or g.IsEmpty():
            continue
        g = jadikan_multi(ke_utm(g, srs))
        if not g.IsValid():
            g = g.MakeValid()
            g = jadikan_multi(g)
        baris.append((petakan(f), g))
    if urut:
        baris.sort(key=urut)
    contoh = baris[0][0]
    fields = [(k, ogr.OFTString if isinstance(v, str) or v is None else ogr.OFTReal) for k, v in contoh.items()]
    fields.append(("luas_ha", ogr.OFTReal))
    lyr = buat_layer(out, nama, ogr.wkbMultiPolygon, fields)
    for atr, g in baris:
        tulis(lyr, g, luas_ha=luas_ha(g), **atr)
    return len(baris)


def larutkan(out, nama, path, layer, kolom_sumber, kolom_tujuan, urutan, petakan_nilai=lambda v: v):
    """Gabungkan (dissolve) poligon berdasarkan satu atribut kelas."""
    ds, src = buka(path, layer)
    srs = src.GetSpatialRef()
    kelompok = defaultdict(list)
    for f in src:
        g = f.GetGeometryRef()
        if g is None or g.IsEmpty():
            continue
        kelompok[petakan_nilai(f.GetField(kolom_sumber))].append(ke_utm(g, srs))
    lyr = buat_layer(out, nama, ogr.wkbMultiPolygon, [(kolom_tujuan, ogr.OFTString), ("luas_ha", ogr.OFTReal)])
    for kelas in sorted(kelompok, key=lambda k: urutan.index(k.split(" (")[0]) if k.split(" (")[0] in urutan else 99):
        koleksi = ogr.Geometry(ogr.wkbMultiPolygon)
        for g in kelompok[kelas]:
            g = jadikan_multi(g)
            for i in range(g.GetGeometryCount()):
                koleksi.AddGeometry(g.GetGeometryRef(i))
        gabung = jadikan_multi(koleksi.UnionCascaded())
        tulis(lyr, gabung, luas_ha=luas_ha(gabung), **{kolom_tujuan: kelas})
    return len(kelompok)


def salin_garis(out, nama, sumber, petakan):
    """sumber: daftar (path, layer)."""
    baris = []
    for path, layer in sumber:
        ds, src = buka(path, layer)
        srs = src.GetSpatialRef()
        for f in src:
            g = f.GetGeometryRef()
            if g is not None and not g.IsEmpty():
                baris.append((petakan(f, path), jadikan_multi(ke_utm(g, srs))))
    fields = [(k, ogr.OFTString) for k in baris[0][0]] + [("panjang_m", ogr.OFTReal)]
    lyr = buat_layer(out, nama, ogr.wkbMultiLineString, fields)
    for atr, g in baris:
        tulis(lyr, g, panjang_m=round(g.Length(), 1), **atr)
    return len(baris)


# ---------------------------------------------------------------- titik sampel
def urai_keterangan(ket):
    """'Agroforestri Lereng Tengah Perbukitan Agak Curam' -> (PL, LF, lereng)."""
    ket = ket.replace("Datang", "Datar").strip()  # salah ketik pada A12
    pl = next(x for x in PENGGUNAAN if ket.startswith(x))
    sisa = ket[len(pl):].strip()
    lf = next(x for x in BENTUKLAHAN if sisa.startswith(x))
    lereng = sisa[len(lf):].strip()
    assert lereng in LERENG_URUT, ket
    return ket, pl, lf, lereng


def titik_rencana(out, mpk):
    ds, src = buka(os.path.join(mpk, "v104", "data_ta.gdb"), "baru_sampel")
    srs = src.GetSpatialRef()
    baris = []
    for f in src:
        ket, pl, lf, lereng = urai_keterangan(f.GetField("Keterangan"))
        baris.append((f.GetField("Kode_sampel"), f.GetField("Tim"), ket, pl, lf, lereng, ke_utm(f.GetGeometryRef(), srs)))
    baris.sort(key=lambda r: (r[0][0], int(r[0][1:])))
    fields = [("kode", ogr.OFTString), ("tim", ogr.OFTString), ("satuan_lahan", ogr.OFTString),
              ("penggunaan_lahan", ogr.OFTString), ("bentuklahan", ogr.OFTString), ("kelas_lereng", ogr.OFTString)]
    lyr = buat_layer(out, "titik_sampel_rencana", ogr.wkbPoint, fields)
    for kode, tim, ket, pl, lf, lereng, g in baris:
        tulis(lyr, g, kode=kode, tim=tim, satuan_lahan=ket, penggunaan_lahan=pl, bentuklahan=lf, kelas_lereng=lereng)
    return {r[0]: r for r in baris}


def titik_lapangan(out, rencana):
    rekaman = []  # (kode, nama_asli, tim, waktu, elev, lon, lat, sumber)
    for berkas, tim in [("Tim A sampling.csv", "A"), ("Peta 1 Tim C.csv", "C"), ("Peta 2 tim C.csv", "C")]:
        with open(p("Sampling", berkas), encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                rekaman.append((kode_sampel(r["Title"]), r["Title"].strip(), tim, r["Date Created"],
                                elevasi(r.get("Elevation")), float(r["Longitude"]), float(r["Latitude"]), f"Sampling/{berkas}"))
    for nama, waktu, jenis, koord in baca_kml(kml_dari(p("Sampling", "Tim B - Survei Bompon.kmz"))):
        if jenis == "Point":
            rekaman.append((kode_sampel(nama), nama, "B", waktu, None, koord[0][0], koord[0][1],
                            "Sampling/Tim B - Survei Bompon.kmz"))

    bantu = [r for r in rekaman if r[0] is None]          # 'Tanda tempat' -> titik bantu
    sampel = sorted((r for r in rekaman if r[0]), key=lambda r: (r[0][0], int(r[0][1:]), r[3] or ""))
    per_kode = defaultdict(list)
    for r in sampel:
        per_kode[r[0]].append(r)

    fields = [("kode", ogr.OFTString), ("nama_asli", ogr.OFTString), ("tim", ogr.OFTString),
              ("waktu", ogr.OFTString), ("elevasi_gps_m", ogr.OFTReal), ("jarak_ke_rencana_m", ogr.OFTReal),
              ("status", ogr.OFTString), ("sumber_berkas", ogr.OFTString)]
    lyr = buat_layer(out, "titik_sampel_lapangan", ogr.wkbPoint, fields)
    tabel = []
    for kode in sorted(per_kode, key=lambda k: (k[0], int(k[1:]))):
        grup = per_kode[kode]
        geoms = [titik_utm(r[5], r[6]) for r in grup]
        # rekaman ganda yang berjarak < 25 m dianggap satu kunjungan yang tercatat dua kali
        dipakai, sumber_gabung = [], defaultdict(list)
        for r, g in zip(grup, geoms):
            induk = next((i for i, (_, gi) in enumerate(dipakai) if g.Distance(gi) < 25), None)
            if induk is None:
                dipakai.append((r, g))
                sumber_gabung[len(dipakai) - 1].append(r[7])
            else:
                sumber_gabung[induk].append(r[7])
        konflik = len(dipakai) > 1
        for i, (r, g) in enumerate(dipakai):
            jarak = round(g.Distance(rencana[kode][6]), 1) if kode in rencana else None
            if konflik:
                status = "ganda-berbeda lokasi (perlu konfirmasi)"
            elif len(sumber_gabung[i]) > 1:
                status = "digabung dari rekaman ganda"
            else:
                status = "tunggal"
            sumber = "; ".join(dict.fromkeys(sumber_gabung[i]))
            tulis(lyr, g, kode=kode, nama_asli=r[1], tim=r[2], waktu=r[3], elevasi_gps_m=r[4],
                  jarak_ke_rencana_m=jarak, status=status, sumber_berkas=sumber)
            lon, lat = lonlat(g)
            tabel.append([kode, r[1], r[2], r[3], round(g.GetX(), 2), round(g.GetY(), 2), lon, lat, r[4], jarak, status, sumber])
    with open(os.path.join(TABEL, "titik_sampel_lapangan.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["kode", "nama_asli", "tim", "waktu", "x_utm49s", "y_utm49s", "lon", "lat",
                    "elevasi_gps_m", "jarak_ke_rencana_m", "status", "sumber_berkas"])
        w.writerows(tabel)
    return len(tabel), bantu


def titik_survei(out, bantu):
    rekaman = []
    s1 = "Survei 1 (Februari 2025)"
    s2 = "Survei 2 (Februari 2025)"
    for berkas in ["Titik 1.kmz", "Rute 1.kmz"]:
        for nama, waktu, jenis, koord in baca_kml(kml_dari(p("Survei", "Data Survei", "Survei 1", berkas))):
            if jenis == "Point":
                rekaman.append((nama, waktu, None, koord[0][0], koord[0][1], s1, f"Survei/Data Survei/Survei 1/{berkas}"))
    for berkas in ["Intan bawah.csv", "Nur titik.csv", "Rute atas.csv"]:
        with open(p("Survei", "Data Survei", "Survei 2", berkas), encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                rekaman.append((r["Title"].strip(), r["Date Created"], elevasi(r.get("Elevation")),
                                float(r["Longitude"]), float(r["Latitude"]), s2, f"Survei/Data Survei/Survei 2/{berkas}"))
    for r in bantu:
        rekaman.append((r[1], r[3], r[4], r[5], r[6], "Sampling (titik bantu Tim C)", r[7]))

    fields = [("nama", ogr.OFTString), ("waktu", ogr.OFTString), ("elevasi_gps_m", ogr.OFTReal),
              ("kegiatan", ogr.OFTString), ("sumber_berkas", ogr.OFTString)]
    lyr = buat_layer(out, "titik_survei", ogr.wkbPoint, fields)
    tabel, terlihat = [], set()
    for nama, waktu, elev, lon, lat, kegiatan, sumber in rekaman:
        kunci = (nama, round(lon, 6), round(lat, 6))
        if kunci in terlihat:  # duplikat persis lintas format
            continue
        terlihat.add(kunci)
        g = titik_utm(lon, lat)
        tulis(lyr, g, nama=nama, waktu=waktu, elevasi_gps_m=elev, kegiatan=kegiatan, sumber_berkas=sumber)
        tabel.append([nama, waktu, kegiatan, round(g.GetX(), 2), round(g.GetY(), 2), round(lon, 7), round(lat, 7), elev, sumber])
    with open(os.path.join(TABEL, "titik_survei.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["nama", "waktu", "kegiatan", "x_utm49s", "y_utm49s", "lon", "lat", "elevasi_gps_m", "sumber_berkas"])
        w.writerows(tabel)
    return len(tabel)


def fasilitas(out):
    lyr = buat_layer(out, "fasilitas_pengamatan", ogr.wkbPoint, [("jenis", ogr.OFTString), ("sumber_berkas", ogr.OFTString)])
    n = 0
    for berkas, jenis in [("St_Hujan.shp", "Stasiun hujan"), ("SPAS.shp", "Stasiun pengamat arus sungai (SPAS)"),
                          ("Plot Erosi.shp", "Plot erosi"), ("embung_point.shp", "Embung")]:
        ds, src = buka(p("SHP Bompon", berkas))
        for f in src:
            tulis(lyr, ke_utm(f.GetGeometryRef(), src.GetSpatialRef()), jenis=jenis, sumber_berkas=f"SHP Bompon/{berkas}")
            n += 1
    return n


def desa_rbi(out, mpk):
    """Batas desa RBI 1:25.000 untuk Kabupaten Magelang (konteks peta lokasi)."""
    ds, src = buka(os.path.join(mpk, "commondata", "rbi_magelang", "ADMINISTRASIDESA_AR_25K.shp"))
    srs = src.GetSpatialRef()
    lyr = buat_layer(out, "rbi_desa_magelang", ogr.wkbMultiPolygon,
                     [("desa", ogr.OFTString), ("kecamatan", ogr.OFTString), ("luas_ha", ogr.OFTReal)])
    n = 0
    for f in src:
        if f.GetField("WADMKK") not in ("Kabupaten Magelang", "Magelang"):
            continue
        g = jadikan_multi(ke_utm(f.GetGeometryRef(), srs))
        g.FlattenTo2D()
        if not g.IsValid():
            g = jadikan_multi(g.MakeValid())
        tulis(lyr, g, desa=f.GetField("NAMOBJ"), kecamatan=f.GetField("WADMKC"), luas_ha=luas_ha(g))
        n += 1
    return n


def tabel_rencana(rencana):
    with open(os.path.join(TABEL, "titik_sampel_rencana.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["kode", "tim", "satuan_lahan", "penggunaan_lahan", "bentuklahan", "kelas_lereng", "x_utm49s", "y_utm49s", "lon", "lat"])
        for kode, tim, ket, pl, lf, lereng, g in rencana.values():
            lon, lat = lonlat(g)
            w.writerow([kode, tim, ket, pl, lf, lereng, round(g.GetX(), 2), round(g.GetY(), 2), lon, lat])


# ---------------------------------------------------------------- utama
def main():
    if os.path.exists(GPKG):
        os.remove(GPKG)
    os.makedirs(TABEL, exist_ok=True)
    out = ogr.GetDriverByName("GPKG").CreateDataSource(GPKG)
    ringkas = {}
    tmp = tempfile.mkdtemp(prefix="bompon_mpk_")
    try:
        mpk = ekstrak_mpk(tmp)
        ringkas["batas_subdas"] = salin_poligon(out, "batas_subdas", p("SHP Bompon", "Batas_Bompon.shp"), None,
                                                lambda f: {"nama": "Sub-DAS Bompon"})
        ringkas["batas_dusun"] = salin_poligon(out, "batas_dusun", p("SHP Bompon", "Batas_Dusun_Bompon.shp"), None,
                                               lambda f: {"dusun": f.GetField("Dusun")}, urut=lambda r: r[0]["dusun"])
        ringkas["bentuklahan"] = salin_poligon(out, "bentuklahan", os.path.join(mpk, "commondata", "shp_ta", "Landform.shp"), None,
                                               lambda f: {"bentuklahan": f.GetField("LF")},
                                               urut=lambda r: BENTUKLAHAN.index(r[0]["bentuklahan"]))
        ringkas["penggunaan_lahan"] = salin_poligon(out, "penggunaan_lahan", os.path.join(mpk, "commondata", "shp_ta", "Digit_PL.shp"), None,
                                                    lambda f: {"penggunaan_lahan": f.GetField("PL")},
                                                    urut=lambda r: PENGGUNAAN.index(r[0]["penggunaan_lahan"]))
        ringkas["kelas_lereng"] = larutkan(out, "kelas_lereng", os.path.join(mpk, "v104", "data_ta.gdb"), "slope_lidar25",
                                           "Slope", "kelas_lereng", LERENG_URUT)
        ringkas["longsor"] = salin_poligon(out, "longsor", "/vsizip/" + p("Longsor", "Shp Longsor Bompon.zip") + "/Longsor_Bompon.shp", None,
                                           lambda f: {"kelas": f.GetField("Kelas")}, urut=lambda r: r[0]["kelas"])
        ringkas["sungai"] = salin_garis(out, "sungai", [(p("SHP Bompon", "Sungai_2020.shp"), None)],
                                        lambda f, _: {"jenis": f.GetField("keterangan").replace("Intermitten", "intermiten").replace("Perennial", "perenial")})
        ringkas["jalan"] = salin_garis(out, "jalan", [(p("SHP Bompon", "Jalan_2020.shp"), None)],
                                       lambda f, _: {"kelas": f.GetField("Kelas")})
        ringkas["rute_survei"] = salin_garis(out, "rute_survei", [(os.path.join(mpk, "v104", "data_ta.gdb"), "Rute")],
                                             lambda f, _: {"sumber_berkas": "Survei/ArcGIS/Survei.mpk (data_ta.gdb/Rute)"})
        ringkas["fasilitas_pengamatan"] = fasilitas(out)
        ringkas["rbi_desa_magelang"] = desa_rbi(out, mpk)
        rencana = titik_rencana(out, mpk)
        ringkas["titik_sampel_rencana"] = len(rencana)
        tabel_rencana(rencana)
        ringkas["titik_sampel_lapangan"], bantu = titik_lapangan(out, rencana)
        ringkas["titik_survei"] = titik_survei(out, bantu)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    out = None

    for k, v in ringkas.items():
        print(f"{k:24s} {v:4d} fitur")
    ds, b = buka(GPKG, "batas_subdas")
    fitur = b.GetNextFeature()
    g = fitur.GetGeometryRef()
    minx, maxx, miny, maxy = g.GetEnvelope()
    lo1, la1 = lonlat(ogr.CreateGeometryFromWkt(f"POINT ({minx} {miny})"))
    lo2, la2 = lonlat(ogr.CreateGeometryFromWkt(f"POINT ({maxx} {maxy})"))
    print(f"luas Sub-DAS: {luas_ha(g):.2f} ha; bujur {lo1:.4f}–{lo2:.4f} BT; lintang {abs(la2):.4f}–{abs(la1):.4f} LS")


if __name__ == "__main__":
    main()
