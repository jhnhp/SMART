#!/usr/bin/env python3
"""Membuat notebook Praktik 3 dan Praktik 5 di Output/Pelatihan/data/praktik-{3,5}/.

Jalankan: python3 Output/scripts/pelatihan_buat_notebook.py [3] [5]
Pelaksanaannya dicatat di modul praktik masing-masing.
"""
import json
import os
import sys
import textwrap

AKAR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(AKAR, 'Output', 'Pelatihan', 'data')


NOMOR = 0


def sel(jenis, teks):
    teks = textwrap.dedent(teks).strip('\n')
    baris = teks.split('\n')
    sumber = [b + '\n' for b in baris[:-1]] + [baris[-1]]
    global NOMOR
    NOMOR += 1
    d = {'cell_type': jenis, 'id': f'sel-{NOMOR:03d}', 'metadata': {}, 'source': sumber}
    if jenis == 'code':
        d.update(execution_count=None, outputs=[])
    return d


def md(t):
    return sel('markdown', t)


def kode(t):
    return sel('code', t)


def tulis(nama, sel_sel):
    nb = {'cells': sel_sel, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}, 'language_info': {'name': 'python'}}, 'nbformat': 4, 'nbformat_minor': 5}
    with open(nama, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)


SIAPKAN = """
import os, sys

# Di Google Colab: pasang pustaka lalu sambungkan Drive. Di Jupyter lokal bagian ini dilewati.
if 'google.colab' in sys.modules:
    !pip -q install {paket}
    from google.colab import drive
    drive.mount('/content/drive')
    os.chdir('/content/drive/MyDrive/Pelatihan/data/praktik-{n}')   # sesuaikan dengan lokasi folder Anda

os.makedirs('hasil', exist_ok=True)
print('Folder kerja:', os.path.basename(os.getcwd()))
"""

# ---------------------------------------------------------------------------------------------
# PRAKTIK 3
# ---------------------------------------------------------------------------------------------
P3 = [
    md("""
    # Praktik 3. Dari Spektrum Pantulan ke Sifat Tanah

    ASD FieldSpec 4 merekam **spektrum pantulan**, bukan nilai sifat tanah. Nilai sifat tanah baru diperoleh setelah spektrum dihubungkan dengan hasil laboratorium melalui model kalibrasi. Notebook ini menelusuri jalan tersebut dengan pustaka spektral vis-NIR 350–2.500 nm: membaca spektrum, mengenali fitur serapan, memberi praolah, lalu melatih dan menilai model *Partial Least Squares Regression* (PLSR).

    Pegangan membaca notebook: jalankan sel dari atas ke bawah dengan **Shift + Enter**, lalu baca keluarannya sebelum lanjut. Rujukan konsep ada di Modul 7, Gambar 7.3 dan 7.4.

    **Catatan data.** Pustaka ini merupakan hasil pengujian sampel tanah dari Site Gunung Madu Plantation (GMP), Lampung, jadi bukan dari Sub-DAS Bompon. Kode sampel `S3 L2` ditafsirkan sebagai profil S3 lapisan 2. Model dalam notebook ini dilatih dari tanah GMP dan dipakai untuk latihan. Untuk tanah dari tempat lain, hasilnya hanya pendekatan sampai diuji dengan sampel setempat (Modul 7).
    """),
    md("## 1. Menyiapkan lingkungan kerja"),
    kode(SIAPKAN.format(paket='numpy pandas scipy scikit-learn matplotlib', n=3)),
    kode("""
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy.signal import savgol_filter
    from sklearn.cross_decomposition import PLSRegression
    from sklearn.model_selection import GroupKFold, GroupShuffleSplit, KFold, cross_val_predict
    plt.rcParams.update({'figure.dpi': 110, 'axes.grid': True, 'grid.alpha': .3, 'font.size': 9})
    """),
    md("""
    ## 2. Membaca pustaka spektral

    Setiap baris adalah satu sampel. Kolom `w350` sampai `w2500` berisi pantulan pada setiap panjang gelombang, sedangkan kolom lainnya berisi hasil laboratorium.
    """),
    kode("""
    data = pd.read_csv('spektra_visnir_gmp.csv.gz')
    kolom_spektrum = [k for k in data.columns if k.startswith('w') and k[1:].isdigit()]
    kolom_lab = [k for k in data.columns if k not in kolom_spektrum and k != 'sampel']
    panjang_gel = np.array([int(k[1:]) for k in kolom_spektrum], dtype=float)
    data = data.copy()
    data['profil'] = data['sampel'].str.extract(r'^(S\\d+)')[0]

    print('Sampel :', len(data))
    print('Profil :', data['profil'].nunique())
    print('Lapisan per profil:', data.groupby('profil').size().value_counts().sort_index().to_dict())
    print('Kanal  :', len(panjang_gel), 'dari', panjang_gel.min(), 'sampai', panjang_gel.max(), 'nm')
    print('Sifat tanah:', kolom_lab)
    data[['sampel', 'profil', 'c_organik', 'n_total', 'clay', 'sand', 'ph_h2o', 'kpk', 'p_tersedia']].head(6)
    """),
    md("""
    **Periksa datanya dulu.** Dua hal perlu diketahui sebelum memodelkan: sampel yang tidak memiliki hasil laboratorium, dan nilai yang tidak mungkin secara fisik. Sampel tanpa hasil laboratorium tidak dapat dipakai melatih model, tetapi berguna pada Bagian 11.
    """),
    kode("""
    tanpa_lab = data[data['clay'].isna()].reset_index(drop=True)
    print('Sampel tanpa hasil laboratorium:', tanpa_lab['sampel'].tolist())
    print('C-organik bernilai 0:')
    print(data.loc[data['c_organik'] == 0, ['sampel', 'c_organik', 'n_total']].to_string(index=False))

    # C-organik 0 tidak mungkin pada tanah yang N-totalnya 0,11, sehingga diperlakukan sebagai data kosong
    data.loc[data['c_organik'] == 0, 'c_organik'] = np.nan

    data_lab = data[data['clay'].notna()].reset_index(drop=True)
    profil = data_lab['profil'].values
    data_lab[['c_organik', 'n_total', 'clay', 'silt', 'sand', 'ph_h2o', 'kpk', 'p_tersedia', 'k_tersedia']].describe().T[['count', 'min', '50%', 'mean', 'max', 'std']].round(2)
    """),
    md("## 3. Melihat spektrum"),
    kode("""
    urut = data_lab.dropna(subset=['c_organik']).sort_values('c_organik')
    contoh = urut.iloc[[2, len(urut) // 2, -1]]
    S = data_lab[kolom_spektrum].values
    fig, ax = plt.subplots(1, 2, figsize=(11, 3.4))
    for _, b in contoh.iterrows():
        ax[0].plot(panjang_gel, b[kolom_spektrum].values.astype(float), lw=.9, label=f"{b['sampel']}, C-organik {b['c_organik']:.2f}%")
    ax[0].set(title='Tiga sampel dengan C-organik berbeda', xlabel='Panjang gelombang (nm)', ylabel='Pantulan'); ax[0].legend()
    ax[1].plot(panjang_gel[1:], np.abs(np.diff(S, axis=1)).mean(axis=0), color='crimson', lw=.7)
    ax[1].set(title='Rerata beda nilai antarkanal berdekatan', xlabel='Panjang gelombang (nm)')
    plt.tight_layout(); plt.savefig('hasil/spektrum_contoh.png', dpi=150); plt.show()
    print('Beda antarkanal 350-399 nm:', round(np.abs(np.diff(S[:, panjang_gel < 400], axis=1)).mean(), 5))
    print('Beda antarkanal 400-2500 nm:', round(np.abs(np.diff(S[:, panjang_gel >= 400], axis=1)).mean(), 5))
    """),
    md("""
    Spektrum yang halus seharusnya hampir tidak berubah antarkanal yang berdekatan. Di bawah 400 nm, nilainya melompat-lompat, yang menandakan derau, sehingga pemodelan hanya memakai 400–2.500 nm. Lonjakan sempit di 1.000 nm dan 1.800 nm berada tepat pada batas antardetektor alat, sedangkan lonjakan lainnya mengikuti tepi fitur serapan.
    """),
    kode("""
    pilih = panjang_gel >= 400
    wl = panjang_gel[pilih]
    R = data_lab[kolom_spektrum].values[:, pilih]

    fig, ax = plt.subplots(figsize=(9, 3.6))
    ada = np.where(data_lab['c_organik'].notna())[0]
    urut_c = ada[np.argsort(data_lab['c_organik'].values[ada])]
    warna = plt.cm.viridis(np.linspace(0, 1, len(urut_c)))
    for w, i in zip(warna, urut_c):
        ax.plot(wl, R[i], color=w, lw=.35, alpha=.7)
    sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(data_lab['c_organik'].min(), data_lab['c_organik'].max()))
    plt.colorbar(sm, ax=ax, label='C-organik (%)')
    for pos, nama in [(900, 'oksida besi'), (1400, 'air/OH'), (1900, 'air'), (2205, 'kaolinit')]:
        ax.axvline(pos, color='k', lw=.6, ls='--'); ax.text(pos + 8, ax.get_ylim()[1] * .94, nama, fontsize=8)
    ax.set(title='Spektrum setiap sampel', xlabel='Panjang gelombang (nm)', ylabel='Pantulan')
    plt.tight_layout(); plt.savefig('hasil/spektrum_semua_sampel.png', dpi=150); plt.show()
    """),
    md("""
    ## 4. Membaca fitur serapan

    Posisi serapan yang ditandai di atas mengikuti Modul 7 (Molin & Tavares, 2019). Dua hubungan diuji di sini. Yang pertama adalah kedalaman serapan kaolinit di sekitar 2.205 nm terhadap kadar lempung, dengan garis kontinum sederhana antara 2.120 nm dan 2.250 nm. Yang kedua adalah pantulan wilayah tampak terhadap C-organik, karena Modul 4 menyebut bahan organik menurunkan pantulan pada wilayah tersebut.
    """),
    kode("""
    def kedalaman_serapan(R, wl, kiri=2120, pusat=2205, kanan=2250):
        i, c, k = [np.argmin(np.abs(wl - v)) for v in (kiri, pusat, kanan)]
        kontinum = R[:, i] + (R[:, k] - R[:, i]) * (wl[c] - wl[i]) / (wl[k] - wl[i])
        return 1 - R[:, c] / kontinum

    kedalaman = kedalaman_serapan(R, wl)
    tampak = R[:, (wl >= 550) & (wl <= 700)].mean(axis=1)
    m_c = data_lab['c_organik'].notna().values
    r_lempung = np.corrcoef(kedalaman, data_lab['clay'])[0, 1]
    r_corg = np.corrcoef(tampak[m_c], data_lab['c_organik'][m_c])[0, 1]
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.5))
    ax[0].scatter(kedalaman, data_lab['clay'], s=10, alpha=.6)
    ax[0].set(xlabel='Kedalaman serapan 2.205 nm', ylabel='Lempung (%)', title=f'r = {r_lempung:.2f}')
    ax[1].scatter(tampak[m_c], data_lab['c_organik'][m_c], s=10, alpha=.6, color='#8c510a')
    ax[1].set(xlabel='Rerata pantulan 550-700 nm', ylabel='C-organik (%)', title=f'r = {r_corg:.2f}')
    plt.tight_layout(); plt.savefig('hasil/fitur_serapan.png', dpi=150); plt.show()
    print('Korelasi kedalaman serapan dengan lempung:', round(r_lempung, 2))
    print('Korelasi pantulan tampak dengan C-organik:', round(r_corg, 2))
    """),
    md("""
    ## 5. Praolah spektrum

    Sebagian besar keragaman spektrum disebabkan oleh ukuran partikel dan hamburan, bukan komposisi kimia (Barnes et al., 1989). *Standard Normal Variate* (SNV) meredam gangguan tersebut, sedangkan turunan pertama Savitzky–Golay menajamkan fitur serapan. Keduanya dihitung per spektrum, sehingga tidak ada informasi yang bocor antarsampel.
    """),
    kode("""
    def snv(A):
        return (A - A.mean(axis=1, keepdims=True)) / A.std(axis=1, keepdims=True)

    def turunan(A):
        return savgol_filter(A, window_length=21, polyorder=2, deriv=1, axis=1)

    praolah = {'Pantulan mentah': lambda A: A,
               'SNV': snv,
               'SNV + turunan pertama': lambda A: turunan(snv(A))}

    fig, ax = plt.subplots(1, 3, figsize=(12, 3))
    for a, (nama, f) in zip(ax, praolah.items()):
        a.plot(wl, f(R)[::12].T, lw=.4)
        a.set(title=nama, xlabel='Panjang gelombang (nm)')
    plt.tight_layout(); plt.savefig('hasil/praolah.png', dpi=150); plt.show()
    """),
    md("""
    Korelogram memperlihatkan wilayah spektrum yang berhubungan dengan sifat tanah, sebelum dan sesudah praolah.
    """),
    kode("""
    def korelogram(A, y):
        return np.array([np.corrcoef(A[:, j], y)[0, 1] for j in range(A.shape[1])])

    fig, ax = plt.subplots(1, 2, figsize=(11, 3), sharey=True)
    for a, t in zip(ax, ['c_organik', 'clay']):
        m = data_lab[t].notna().values
        a.plot(wl, korelogram(R[m], data_lab[t][m]), lw=.9, label='Pantulan mentah')
        a.plot(wl, korelogram(turunan(snv(R))[m], data_lab[t][m]), lw=.6, label='SNV + turunan')
        a.axhline(0, color='k', lw=.5); a.set(title=t, xlabel='Panjang gelombang (nm)', ylabel='r'); a.legend()
    plt.tight_layout(); plt.savefig('hasil/korelogram.png', dpi=150); plt.show()
    """),
    md("""
    ## 6. Ukuran ketelitian

    Fungsi berikut menghitung ukuran pada Modul 7 dan Modul 8. MEC adalah bagian keragaman yang dijelaskan terhadap garis 1:1 dan bernilai negatif jika model lebih buruk daripada menebak rata-rata. RPD adalah simpangan baku dibagi RMSE. RPIQ adalah jangkauan antarkuartil dibagi RMSE.
    """),
    kode("""
    def ukuran(y, p):
        y, p = np.asarray(y, float), np.asarray(p, float).ravel()
        e = p - y
        rmse = np.sqrt(np.mean(e ** 2))
        return {'ME': e.mean(), 'RMSE': rmse,
                'MEC': 1 - np.sum(e ** 2) / np.sum((y - y.mean()) ** 2),
                'R2': np.corrcoef(y, p)[0, 1] ** 2,
                'RPD': y.std(ddof=1) / rmse,
                'RPIQ': (np.percentile(y, 75) - np.percentile(y, 25)) / rmse}
    """),
    md("""
    ## 7. Cara membagi data menentukan angka yang dilaporkan

    Ini bagian terpenting dari notebook. Sampel dari satu profil, yaitu lapisan-lapisan pada satu titik, saling mirip. Bandingkan dua cara validasi silang pada model yang sama:

    1. **Acak per sampel**, lapisan dari profil yang sama dapat masuk data latih sekaligus data uji.
    2. **Per profil**, semua lapisan satu profil selalu berada di sisi yang sama. Inilah yang paling mendekati keadaan ketika model dipakai pada titik baru.
    """),
    kode("""
    A = turunan(snv(R))
    N_KOMP = 8
    baris = []
    for t in ['c_organik', 'clay']:
        m = data_lab[t].notna().values
        y = data_lab[t].values[m]
        pls = PLSRegression(N_KOMP)
        p1 = cross_val_predict(pls, A[m], y, cv=KFold(5, shuffle=True, random_state=1))
        p2 = cross_val_predict(pls, A[m], y, cv=GroupKFold(5), groups=profil[m])
        baris.append({'Sifat': t, 'Skema': '1. Acak per sampel', **ukuran(y, p1)})
        baris.append({'Sifat': t, 'Skema': '2. Per profil', **ukuran(y, p2)})
    bocoran = pd.DataFrame(baris).round(2)
    bocoran.to_csv('hasil/perbandingan_skema_validasi.csv', index=False)
    bocoran
    """),
    md("""
    **Diskusi.** Skema pertama memberi angka lebih baik karena model melihat lapisan lain dari profil yang sama saat dilatih. Selisihnya tampak jelas pada lempung. Mulai sekarang semua penilaian memakai pembagian **per profil**.

    ## 8. Memilih praolah dan jumlah komponen

    Jumlah komponen laten terlalu sedikit membuat model kurang pas, terlalu banyak membuatnya hafal derau. Pilihan dibuat hanya dengan data kalibrasi. Sepertiga profil disisihkan sebagai data uji dan tidak disentuh sampai Bagian 9, mengikuti pegangan dua pertiga dan sepertiga dalam Modul 7.
    """),
    kode("""
    SASARAN = 'c_organik'     # ganti dengan 'clay', 'sand', 'ph_h2o', atau 'kpk'
    m = data_lab[SASARAN].notna().values
    y, pr, Rm = data_lab[SASARAN].values[m], profil[m], R[m]

    pisah = GroupShuffleSplit(n_splits=1, test_size=1/3, random_state=7)
    i_kal, i_uji = next(pisah.split(Rm, groups=pr))
    print('Kalibrasi:', len(i_kal), 'sampel dari', len(set(pr[i_kal])), 'profil')
    print('Uji      :', len(i_uji), 'sampel dari', len(set(pr[i_uji])), 'profil')

    komp = range(1, 21)
    fig, ax = plt.subplots(figsize=(6.5, 3.4))
    terbaik = {}
    for nama, f in praolah.items():
        B = f(Rm)
        rmse = [ukuran(y[i_kal], cross_val_predict(PLSRegression(k), B[i_kal], y[i_kal], cv=GroupKFold(5), groups=pr[i_kal]))['RMSE'] for k in komp]
        ax.plot(komp, rmse, marker='o', ms=3, label=nama)
        terbaik[nama] = (int(np.argmin(rmse)) + 1, min(rmse))
    ax.set(xlabel='Jumlah komponen', ylabel='RMSE validasi silang', title=SASARAN); ax.legend()
    plt.tight_layout(); plt.savefig('hasil/pemilihan_komponen.png', dpi=150); plt.show()
    pd.DataFrame(terbaik, index=['komponen terbaik', 'RMSE']).T.round(3)
    """),
    md("""
    ## 9. Model akhir dan penilaian pada profil yang belum pernah dilihat

    Setelah satu penilaian, pembagian yang sama diulang 20 kali dengan profil uji yang berbeda. Hasilnya menunjukkan seberapa jauh satu angka dapat bergantung pada profil yang kebetulan terpilih.
    """),
    kode("""
    nama_pilih = min(terbaik, key=lambda k: terbaik[k][1])
    k_pilih = terbaik[nama_pilih][0]
    f = praolah[nama_pilih]
    print('Praolah terpilih:', nama_pilih, '| komponen:', k_pilih)

    model = PLSRegression(k_pilih).fit(f(Rm)[i_kal], y[i_kal])
    p_uji = model.predict(f(Rm)[i_uji]).ravel()
    u_uji = ukuran(y[i_uji], p_uji)

    fig, ax = plt.subplots(figsize=(4.4, 4.2))
    ax.scatter(y[i_uji], p_uji, s=14, alpha=.7)
    b = [min(y[i_uji].min(), p_uji.min()), max(y[i_uji].max(), p_uji.max())]
    ax.plot(b, b, 'k--', lw=.8)
    ax.set(xlabel=f'{SASARAN} laboratorium', ylabel=f'{SASARAN} prediksi', title=f"MEC {u_uji['MEC']:.2f} | RMSE {u_uji['RMSE']:.2f} | RPD {u_uji['RPD']:.2f}")
    plt.tight_layout(); plt.savefig('hasil/prediksi_vs_laboratorium.png', dpi=150); plt.show()

    ulang = []
    for acak in range(20):
        a, c = next(GroupShuffleSplit(n_splits=1, test_size=1/3, random_state=acak).split(Rm, groups=pr))
        ulang.append(ukuran(y[c], PLSRegression(k_pilih).fit(f(Rm)[a], y[a]).predict(f(Rm)[c]))['MEC'])
    print(f'MEC dari 20 pembagian: terendah {min(ulang):.2f}, median {np.median(ulang):.2f}, tertinggi {max(ulang):.2f}')
    pd.Series(u_uji).round(3)
    """),
    md("""
    ## 10. Semua sifat tanah dalam satu tabel

    Sifat yang memiliki fitur serapan langsung umumnya lebih mudah dikalibrasi. Hara tersedia, KTK, dan pH tidak memiliki fitur sendiri, sehingga keberhasilannya bergantung pada kovariasi setempat (Modul 7). Tabel berikut memakai validasi silang per profil pada seluruh sampel. Jumlah komponen dipilih hanya dari data latih pada setiap putaran, sehingga angkanya tidak dibuat optimistis oleh pemilihan itu. Agar cepat, spektrum diambil setiap 5 nm.
    """),
    kode("""
    def cv_bersarang(X, y, gr, kandidat=range(1, 13)):
        p = np.zeros(len(y))
        for latih, uji in GroupKFold(5).split(X, groups=gr):
            nilai = [ukuran(y[latih], cross_val_predict(PLSRegression(k), X[latih], y[latih], cv=GroupKFold(4), groups=gr[latih]))['RMSE'] for k in kandidat]
            k = kandidat[int(np.argmin(nilai))]
            p[uji] = PLSRegression(k).fit(X[latih], y[latih]).predict(X[uji]).ravel()
        return p

    A5 = turunan(snv(R))[:, ::5]
    ringkas = []
    for t in ['c_organik', 'n_total', 'clay', 'silt', 'sand', 'ph_h2o', 'kpk', 'p_tersedia', 'k_tersedia']:
        m = data_lab[t].notna().values
        yt = data_lab[t].values[m]
        ringkas.append({'Sifat': t, 'n': int(m.sum()), 'Rata-rata': yt.mean(), **ukuran(yt, cv_bersarang(A5[m], yt, profil[m]))})
    ringkas = pd.DataFrame(ringkas).round(3)
    ringkas.to_csv('hasil/metrik_semua_sifat.csv', index=False)
    ringkas
    """),
    md("""
    ## 11. Memakai model pada spektrum baru

    Inilah yang terjadi setelah demonstrasi alat: spektrum baru diberi praolah **yang sama**, lalu dimasukkan ke model. Sembilan sampel yang tidak memiliki hasil laboratorium menjadi contoh yang pas, karena keadaannya sama dengan sampel baru. Nilai prediksinya tidak dapat diperiksa, dan galatnya kira-kira sebesar RMSE pada tabel di atas. Spektrum hasil demonstrasi dapat dimasukkan dengan cara yang sama jika sudah berupa tabel 350–2.500 nm, tetapi hasilnya hanya pendekatan, karena model belajar dari tanah GMP.
    """),
    kode("""
    model_akhir = PLSRegression(k_pilih).fit(f(Rm), y)
    R_baru = tanpa_lab[kolom_spektrum].values[:, pilih]
    prediksi_baru = pd.DataFrame({'Sampel': tanpa_lab['sampel'], f'Prediksi {SASARAN}': model_akhir.predict(f(R_baru)).ravel()}).round(2)
    prediksi_baru.to_csv('hasil/prediksi_sampel_tanpa_lab.csv', index=False)
    prediksi_baru
    """),
    md("""
    ## 12. Pengayaan: bagaimana jika hanya punya kanal Sentinel-2?

    Spektrum dirata-ratakan ke enam kanal lebar Sentinel-2 dengan pendekatan lebar kanal persegi (bukan fungsi respons sensor yang sebenarnya). Bandingkan kedua sifat: kehilangan informasi akibat kanal lebar tidak sama pada setiap sifat. Data ini tetap merupakan pengukuran dekat di laboratorium, sehingga belum memuat gangguan atmosfer dan penutup lahan yang dihadapi citra satelit.
    """),
    kode("""
    kanal = {'B02': (458, 523), 'B03': (543, 578), 'B04': (650, 680), 'B08': (785, 900), 'B11': (1565, 1655), 'B12': (2100, 2280)}
    S2 = np.column_stack([R[:, (wl >= a) & (wl <= b)].mean(axis=1) for a, b in kanal.values()])
    banding = []
    for t in ['c_organik', 'clay']:
        m = data_lab[t].notna().values
        yt = data_lab[t].values[m]
        banding.append({'Sifat': t, 'Data': 'Spektrum penuh', **ukuran(yt, cv_bersarang(A5[m], yt, profil[m]))})
        banding.append({'Sifat': t, 'Data': 'Enam kanal gaya Sentinel-2', **ukuran(yt, cv_bersarang(S2[m], yt, profil[m], kandidat=range(1, 7)))})
    pd.DataFrame(banding).round(3)
    """),
]

# ---------------------------------------------------------------------------------------------
# PRAKTIK 5
# ---------------------------------------------------------------------------------------------
P5 = [
    md("""
    # Praktik 5. Machine Learning untuk Digital Soil Mapping

    Notebook ini melanjutkan kovariat yang disiapkan di QGIS, lalu mengikuti persamaan SCORPAN pada Modul 8: mempelajari fungsi yang menghubungkan sifat tanah di titik sampel dengan kondisi lingkungannya, menilai fungsi tersebut secara jujur, lalu menerapkannya ke seluruh piksel Sub-DAS Bompon.

    Notebook dibagi menjadi tiga bagian:

    - **Bagian A**, Machine Learning untuk DSM;
    - **Bagian B**, penyiapan dan pemilihan kovariat berdasarkan SCORPAN;
    - **Bagian C**, pembangunan model DSM.

    Satu hal perlu dipegang sejak awal: hanya ada 50 titik, sedangkan DEM yang dipakai berasal dari data global 30 m. Jangan menganggap model pasti berhasil hanya karena petanya terlihat meyakinkan. Biarkan angka validasi yang berbicara.
    """),
    md("## Menyiapkan lingkungan kerja"),
    kode(SIAPKAN.format(paket='numpy pandas scipy scikit-learn matplotlib rasterio quantile-forest', n=5)),
    kode("""
    import glob
    import warnings
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import rasterio
    from sklearn.cluster import KMeans
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.inspection import permutation_importance
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import GroupKFold, KFold, cross_val_predict, train_test_split
    from sklearn.neighbors import NearestNeighbors
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from quantile_forest import RandomForestQuantileRegressor
    plt.rcParams.update({'figure.dpi': 110, 'font.size': 9})
    warnings.filterwarnings('ignore', category=UserWarning)
    """),
    md("""
    # Bagian A. Machine Learning untuk DSM

    ## A1. Membaca data sampel dan kovariat

    Berkas `sampel_tanah_bompon.csv` memuat hasil laboratorium 50 titik pada dua kedalaman. Akhiran `_1` berarti 0–20 cm dan `_2` berarti 20–40 cm. Folder `kovariat/` berisi satu GeoTIFF untuk setiap kovariat, semuanya pada grid 10 m yang sama.
    """),
    kode("""
    sampel = pd.read_csv('sampel_tanah_bompon.csv')
    jalur = sorted(glob.glob('kovariat/*.tif'))
    nama_kov = [os.path.basename(p)[:-4] for p in jalur]
    susunan = []
    for p in jalur:
        with rasterio.open(p) as r:
            susunan.append(r.read(1))
            transform, crs, tinggi, lebar = r.transform, r.crs, r.height, r.width
    kubus = np.stack(susunan)      # kovariat x baris x kolom
    print('Titik sampel :', len(sampel))
    print('Kovariat     :', len(nama_kov), nama_kov)
    print('Ukuran grid  :', kubus.shape[1:], '| CRS', crs)
    sampel[['Titik', 'x', 'y', 'C_Organik_1', 'C_Organik_2', 'Bahan_Organik_1', 'Bahan_Organik_2', 'Lempung_1', 'pH_H2O_1', 'KPK_1']].describe().T[['count', 'min', 'mean', 'max', 'std']].round(2)
    """),
    md("""
    **Periksa datanya.** Sasaran latihan ini adalah C-organik, jadi kolom itulah yang diperiksa lebih dulu. Berkas sumber memiliki dua kolom bernama `C_Organik_1`. Yang kedua diberi nama `C_Organik_2`, dan sel berikut mengujinya: bahan organik lazim dihitung dari C-organik dengan faktor 1,724, sehingga pasangan kolom yang benar seharusnya mengikuti rasio itu.

    Pada berkas asli, C-organik Titik 49 tercatat 0,08% dan 0,16%, padahal bahan organiknya 1,13% dan 1,27%. Karena diduga salah ukur, untuk latihan ini nilainya sudah diperbaiki menjadi 0,66% dan 0,74%, yaitu bahan organik dibagi 1,724. Jadi sel berikut seharusnya tidak lagi menemukan titik yang menyimpang.
    """),
    kode("""
    rasio_1 = sampel['Bahan_Organik_1'] / sampel['C_Organik_1']
    rasio_2 = sampel['Bahan_Organik_2'] / sampel['C_Organik_2']
    print('Median rasio bahan organik / C-organik:', round(rasio_1.median(), 3), 'dan', round(rasio_2.median(), 3))
    ragu = sampel[((rasio_1 - 1.724).abs() > 0.09) | ((rasio_2 - 1.724).abs() > 0.09)]
    print('Titik yang rasionya menyimpang:')
    print(ragu[['Titik', 'C_Organik_1', 'Bahan_Organik_1', 'C_Organik_2', 'Bahan_Organik_2']].to_string(index=False))
    """),
    md("""
    Kolom KPK juga memiliki banyak nilai kosong, karena nilai 0 pada berkas sumber dianggap tidak mungkin secara fisik.

    ## A2. Mengambil nilai kovariat di titik sampel

    Langkah ini disebut *overlay*. Hasilnya adalah tabel pemodelan: satu baris per titik, berisi nilai tanah dan semua nilai kovariat.
    """),
    kode("""
    baris, kolom = rasterio.transform.rowcol(transform, sampel['x'].values, sampel['y'].values)
    baris, kolom = np.array(baris), np.array(kolom)
    tabel = pd.DataFrame(kubus[:, baris, kolom].T, columns=nama_kov)
    tabel.to_csv('hasil/tabel_kovariat_di_titik.csv', index=False)
    tabel.describe().T[['min', 'mean', 'max']].round(2)
    """),
    md("""
    ## A3. Model pertama: latih, uji, dan bahaya *overfitting*

    Sasaran latihan adalah **C-organik 0–20 cm** (`C_Organik_1`). Bagi data menjadi 80% latih dan 20% uji, lalu latih *random forest* dengan semua kovariat numerik. Bandingkan nilainya pada data latih dan data uji.
    """),
    kode("""
    def ukuran(y, p):
        y, p = np.asarray(y, float), np.asarray(p, float)
        e = p - y
        return {'ME': e.mean(), 'MAE': np.abs(e).mean(), 'RMSE': np.sqrt((e ** 2).mean()),
                'MEC': 1 - (e ** 2).sum() / ((y - y.mean()) ** 2).sum(),
                'R2': np.corrcoef(y, p)[0, 1] ** 2}

    SASARAN = 'C_Organik_1'    # silakan coba: C_Organik_2, Lempung_1, Pasir_1, pH_H2O_1
    numerik = [k for k in nama_kov if not k.startswith('kat_')]
    y = sampel[SASARAN].values

    X_latih, X_uji, y_latih, y_uji = train_test_split(tabel[numerik], y, test_size=.2, random_state=42)
    rf = RandomForestRegressor(n_estimators=500, random_state=42).fit(X_latih, y_latih)
    pd.DataFrame({'Data latih': ukuran(y_latih, rf.predict(X_latih)), 'Data uji': ukuran(y_uji, rf.predict(X_uji))}).T.round(2)
    """),
    md("""
    **Diskusi.** Angka pada data latih hampir selalu indah karena model menghafal. Hanya angka pada data uji yang boleh dibaca sebagai kemampuan model. Pembagian tunggal seperti ini juga rapuh: dengan 10 titik uji, hasilnya sangat bergantung pada titik yang kebetulan terpilih. Jalankan sel berikut untuk melihat betapa besar pengaruhnya.
    """),
    kode("""
    hasil = []
    for acak in range(30):
        a, b, c, d = train_test_split(tabel[numerik], y, test_size=.2, random_state=acak)
        m = RandomForestRegressor(n_estimators=200, random_state=0, n_jobs=-1).fit(a, c)
        hasil.append(ukuran(d, m.predict(b))['MEC'])
    plt.figure(figsize=(5, 2.6)); plt.hist(hasil, bins=12, color='#35978f'); plt.axvline(0, color='k')
    plt.xlabel('MEC data uji'); plt.ylabel('Jumlah percobaan'); plt.title('Hasil 30 pembagian acak yang berbeda')
    plt.tight_layout(); plt.savefig('hasil/sebaran_mec_pembagian_tunggal.png', dpi=150); plt.show()
    print(f'MEC terendah {min(hasil):.2f}, median {np.median(hasil):.2f}, tertinggi {max(hasil):.2f}')
    """),
    md("""
    # Bagian B. Penyiapan dan pemilihan kovariat

    ## B1. Memetakan kovariat ke faktor SCORPAN

    Isi tabel berikut mengikuti Tabel 8.1. Kolom terakhir adalah alasan pedologisnya untuk C-organik, yaitu kriteria pertama pemilihan kovariat. Alasan itu adalah hipotesis yang belum tentu terbukti pada data ini. Perhatikan faktor yang kosong: tidak ada data iklim karena hampir tidak bervariasi di wilayah sekecil ini, dan peta bahan induk belum tersedia.
    """),
    kode("""
    faktor = pd.DataFrame([
        ('ndvi_2024', 'o', 'Sentinel-2', 'Vegetasi kemarau, masukan bahan organik'),
        ('ndvi_2025', 'o', 'Sentinel-2', 'Vegetasi kemarau, masukan bahan organik'),
        ('kat_penggunaan_lahan', 'o', 'Foto udara', 'Pengelolaan, pengolahan, dan masukan bahan organik'),
        ('twi', 'r', 'DEM GLO-30', 'Lokasi basah memperlambat dekomposisi'),
        ('lereng', 'r', 'DEM GLO-30', 'Erosi mengangkut lapisan atas'),
        ('tpi', 'r', 'DEM GLO-30', 'Punggungan kehilangan, lembah menerima material'),
        ('tri', 'r', 'DEM GLO-30', 'Kekasaran medan'),
        ('elevasi', 'r', 'DEM GLO-30', 'Posisi umum dalam lanskap'),
        ('arah_utara', 'r', 'DEM GLO-30', 'Arah hadap, penerimaan cahaya dan kelembapan'),
        ('jarak_sungai', 'r', 'Peta sungai', 'Kedekatan dengan alur dan endapan'),
        ('kat_bentuklahan', 'r/p', 'Peta riset', 'Proses geomorfologi dan bahan'),
        ('bsi_2024', 'o/s', 'Sentinel-2', 'Keterbukaan tanah'),
        ('bi_2024', 'o/s', 'Sentinel-2', 'Bahan organik menurunkan pantulan bila tanah terbuka'),
        ('cmr_2024', 'o/s', 'Sentinel-2', 'Rasio SWIR, peka terhadap sisa tanaman dan lempung'),
        ('sar_vv', 'o/r', 'Sentinel-1', 'Kekasaran dan kelembapan permukaan, bentuk medan'),
        ('sar_vh', 'o', 'Sentinel-1', 'Hamburan volume vegetasi'),
    ], columns=['Kovariat', 'Faktor', 'Sumber', 'Alasan'])
    faktor
    """),
    md("""
    ## B2. Membuang kovariat yang saling berkorelasi

    Kovariat yang sangat mirip cukup diwakili salah satunya. Urutan pada daftar `prioritas` menyatakan penilaian pedologis untuk C-organik: masukan dari vegetasi dan kebasahan didahulukan, lalu erosi dan posisi lanskap. Kovariat di depan dipertahankan lebih dulu. Korelasi dihitung dari seluruh piksel di dalam Sub-DAS, bukan dari 50 titik saja, agar lebih stabil. Korelasi dengan nilai tanah sengaja **tidak** dipakai untuk memilih, karena dengan 50 titik cara itu mudah menangkap hubungan kebetulan.
    """),
    kode("""
    dalam = kubus[nama_kov.index('kat_bentuklahan')] > 0     # piksel di dalam Sub-DAS
    piksel = pd.DataFrame(kubus[:, dalam].T, columns=nama_kov)
    r_pix = piksel[numerik].corr(method='spearman')

    fig, ax = plt.subplots(figsize=(6.4, 5.4))
    g = ax.imshow(r_pix, cmap='RdBu_r', vmin=-1, vmax=1)
    ax.set_xticks(range(len(numerik)), numerik, rotation=90); ax.set_yticks(range(len(numerik)), numerik)
    for i in range(len(numerik)):
        for j in range(len(numerik)):
            ax.text(j, i, f'{r_pix.iloc[i, j]:.1f}', ha='center', va='center', fontsize=6)
    plt.colorbar(g, label='Korelasi Spearman'); plt.tight_layout(); plt.savefig('hasil/korelasi_kovariat.png', dpi=150); plt.show()

    prioritas = ['ndvi_2024', 'twi', 'lereng', 'jarak_sungai', 'elevasi', 'arah_utara', 'cmr_2024', 'sar_vv', 'sar_vh', 'bi_2024', 'bsi_2024', 'ndvi_2025', 'tpi', 'tri']
    AMBANG = 0.8
    terpilih = []
    for k in prioritas:
        if all(abs(r_pix.loc[k, t]) < AMBANG for t in terpilih):
            terpilih.append(k)
        else:
            lawan = max(terpilih, key=lambda t: abs(r_pix.loc[k, t]))
            print(f'{k:12s} dibuang: r = {r_pix.loc[k, lawan]:.2f} dengan {lawan}')
    print('Terpilih:', terpilih)
    """),
    md("""
    ## B3. Menambahkan kovariat kategorik

    *Random forest* di scikit-learn memerlukan angka, sehingga kategori diubah menjadi kolom 0/1 (*one-hot*). Kolom untuk kelas yang tidak memiliki titik sampel tetap dibuat, karena model tetap harus memprediksi piksel kelas tersebut.
    """),
    kode("""
    label_bl = {1: 'Interfluve', 2: 'Lereng Atas', 3: 'Lereng Tengah', 4: 'Lereng Bawah', 5: 'Lereng Kaki Koluvial', 6: 'Dataran Koluvial'}
    label_pl = {1: 'Agroforestri', 2: 'Tegalan', 3: 'Sawah', 4: 'Permukiman'}

    def siapkan_X(df):
        X = df[terpilih].copy()
        for k, v in label_bl.items():
            X['bl_' + v] = (df['kat_bentuklahan'].astype(int) == k).astype(float)
        for k, v in label_pl.items():
            X['pl_' + v] = (df['kat_penggunaan_lahan'].astype(int) == k).astype(float)
        return X

    X = siapkan_X(tabel)
    print('Jumlah titik per bentuklahan:', tabel['kat_bentuklahan'].astype(int).map(label_bl).value_counts().to_dict())
    print('Jumlah titik per penggunaan lahan:', tabel['kat_penggunaan_lahan'].astype(int).map(label_pl).value_counts().to_dict())
    print('Ukuran tabel pemodelan:', X.shape)
    X.assign(**{SASARAN: y}).to_csv('hasil/tabel_pemodelan.csv', index=False)
    """),
    md("""
    # Bagian C. Pembangunan model DSM

    ## C1. Skema validasi

    Dua skema dibandingkan. **Acak** membagi titik secara acak ke dalam lima kelompok. **Spasial** mengelompokkan titik yang berdekatan menjadi lima blok, lalu menyisihkan satu blok setiap putaran, sehingga data uji tidak punya tetangga dekat di data latih.
    """),
    kode("""
    blok = KMeans(n_clusters=5, n_init=10, random_state=0).fit_predict(sampel[['x', 'y']])
    fig, ax = plt.subplots(figsize=(3.4, 5))
    with rasterio.open('kovariat/lereng.tif') as r:
        ax.imshow(np.where(dalam, kubus[nama_kov.index('lereng')], np.nan), extent=[r.bounds.left, r.bounds.right, r.bounds.bottom, r.bounds.top], cmap='Greys')
    ax.scatter(sampel.x, sampel.y, c=blok, cmap='tab10', s=26, edgecolor='k', lw=.3)
    ax.set_title('Lima blok validasi spasial'); ax.axis('off')
    plt.tight_layout(); plt.savefig('hasil/blok_validasi.png', dpi=150); plt.show()
    print('Jumlah titik per blok:', np.bincount(blok))
    """),
    md("""
    ## C2. Membandingkan model dengan pembanding yang paling sederhana

    Model harus dibandingkan dengan sesuatu. Pembanding paling sederhana adalah **menebak rata-rata**, yaitu MEC mendekati 0. Pembanding kedua adalah **rata-rata per bentuklahan**, yang setara dengan peta tanah konvensional: setiap satuan peta diberi satu nilai. Jika model yang rumit tidak mengalahkan keduanya, kerumitan itu belum memberi manfaat.
    """),
    kode("""
    class RataKelas:
        \"\"\"Memprediksi rata-rata per kelas bentuklahan, seperti satuan pada peta tanah.\"\"\"
        def fit(self, X, y):
            kolom = [c for c in X.columns if c.startswith('bl_')]
            self.kolom, self.umum = kolom, y.mean()
            self.nilai = {c: y[X[c].values == 1].mean() if (X[c].values == 1).any() else y.mean() for c in kolom}
            return self
        def predict(self, X):
            p = np.full(len(X), self.umum)
            for c in self.kolom:
                p[X[c].values == 1] = self.nilai[c]
            return p

    class RataUmum:
        def fit(self, X, y):
            self.n = y.mean(); return self
        def predict(self, X):
            return np.full(len(X), self.n)

    def model_baru(nama):
        if nama == 'Menebak rata-rata': return RataUmum()
        if nama == 'Rata-rata per bentuklahan': return RataKelas()
        if nama == 'Regresi linear': return make_pipeline(StandardScaler(), LinearRegression())
        return RandomForestRegressor(n_estimators=500, min_samples_leaf=3, max_features=.5, random_state=0, n_jobs=-1)

    def validasi(nama, X, y, iris):
        p = np.zeros(len(y))
        for latih, uji in iris:
            p[uji] = model_baru(nama).fit(X.iloc[latih], y[latih]).predict(X.iloc[uji])
        return p

    iris_acak = list(KFold(5, shuffle=True, random_state=0).split(X))
    iris_spasial = list(GroupKFold(5).split(X, groups=blok))
    baris = []
    for nama in ['Menebak rata-rata', 'Rata-rata per bentuklahan', 'Regresi linear', 'Random forest']:
        for skema, iris in [('Acak', iris_acak), ('Spasial', iris_spasial)]:
            u = ukuran(y, validasi(nama, X, y, iris))
            if nama == 'Menebak rata-rata':
                u['R2'] = np.nan      # prediksi hampir konstan, korelasinya tidak bermakna
            baris.append({'Model': nama, 'Validasi': skema, **u})
    metrik = pd.DataFrame(baris).round(2)
    metrik.to_csv(f'hasil/metrik_validasi_{SASARAN}.csv', index=False)
    metrik
    """),
    md("""
    **Cara membaca.** MEC di bawah 0 berarti prediksi lebih buruk daripada menebak rata-rata. Baris "Menebak rata-rata" sedikit di bawah nol karena setiap putaran memakai rata-rata data latihnya, bukan rata-rata seluruh titik; itulah patokan yang harus dilampaui. Kolom R² tidak peka terhadap bias (Tabel 8.3), sehingga jangan membacanya sendirian.

    ## C3. Apakah sifat tanah lain lebih mudah diprediksi?
    """),
    kode("""
    baris = []
    for t in ['C_Organik_1', 'C_Organik_2', 'Lempung_1', 'Lempung_2', 'Pasir_1', 'Debu_1', 'pH_H2O_1']:
        yt = sampel[t].values
        pa = validasi('Random forest', X, yt, iris_acak)
        ps = validasi('Random forest', X, yt, iris_spasial)
        pk = validasi('Rata-rata per bentuklahan', X, yt, iris_spasial)
        baris.append({'Sifat': t, 'Rerata': yt.mean(), 'SD': yt.std(ddof=1), 'RMSE spasial': ukuran(yt, ps)['RMSE'],
                      'MEC RF acak': ukuran(yt, pa)['MEC'], 'MEC RF spasial': ukuran(yt, ps)['MEC'], 'MEC per bentuklahan': ukuran(yt, pk)['MEC']})
    semua = pd.DataFrame(baris).round(2)
    semua.to_csv('hasil/metrik_semua_sifat.csv', index=False)
    semua
    """),
    md("""
    ## C4. Kovariat apa yang dipakai model, dan bolehkah dipercaya?

    Tingkat kepentingan dihitung dengan permutasi pada data di luar blok latih. Jika MEC model mendekati atau di bawah nol, urutan ini tidak boleh ditafsirkan sebagai temuan pedologis: model yang tidak mampu memprediksi tidak dapat memberi tahu apa yang mengendalikan tanah (Wadoux, Samuel-Rosa, et al., 2020).
    """),
    kode("""
    pent = []
    for latih, uji in iris_spasial:
        m = model_baru('Random forest').fit(X.iloc[latih], y[latih])
        pent.append(permutation_importance(m, X.iloc[uji], y[uji], n_repeats=20, random_state=0, scoring='neg_root_mean_squared_error').importances_mean)
    pent = pd.Series(np.mean(pent, axis=0), index=X.columns).sort_values()
    fig, ax = plt.subplots(figsize=(6, 4.4))
    ax.barh(pent.index, pent.values, color=['#b2182b' if v < 0 else '#2166ac' for v in pent.values])
    ax.axvline(0, color='k', lw=.6); ax.set(xlabel='Kenaikan RMSE saat kovariat diacak', title=f'Kepentingan kovariat, {SASARAN}')
    plt.tight_layout(); plt.savefig('hasil/kepentingan_kovariat.png', dpi=150); plt.show()
    """),
    md("""
    ## C5. Model akhir dan peta prediksi

    Model akhir dilatih dengan semua titik memakai *quantile regression forest* (QRF), sehingga setiap piksel memperoleh median dan interval prediksi 90%. Peta ini tetap dibuat meskipun validasinya lemah, karena tujuan latihan adalah menguasai alur kerja dan belajar membacanya secara kritis.
    """),
    kode("""
    qrf = RandomForestQuantileRegressor(n_estimators=500, min_samples_leaf=3, max_features=.5, random_state=0, n_jobs=-1)
    qrf.fit(X, y)
    X_piksel = siapkan_X(piksel)[X.columns]
    q = qrf.predict(X_piksel, quantiles=[.05, .5, .95])

    def ke_peta(nilai):
        peta = np.full((tinggi, lebar), np.nan, dtype='float32')
        peta[dalam] = nilai
        return peta

    def simpan(peta, nama):
        with rasterio.open(f'hasil/{nama}.tif', 'w', driver='GTiff', height=tinggi, width=lebar, count=1, dtype='float32', crs=crs, transform=transform, nodata=-9999, compress='deflate') as d:
            d.write(np.where(np.isnan(peta), -9999, peta), 1)

    peta_median, peta_pi90 = ke_peta(q[:, 1]), ke_peta(q[:, 2] - q[:, 0])
    simpan(peta_median, f'prediksi_{SASARAN}')
    simpan(peta_pi90, f'pi90_{SASARAN}')

    fig, ax = plt.subplots(1, 2, figsize=(8, 5.4))
    a = ax[0].imshow(peta_median, cmap='YlOrBr'); ax[0].set_title(f'Prediksi median {SASARAN} (%)'); plt.colorbar(a, ax=ax[0], shrink=.7)
    b = ax[1].imshow(peta_pi90, cmap='magma_r'); ax[1].set_title('Lebar interval prediksi 90% (PI90)'); plt.colorbar(b, ax=ax[1], shrink=.7)
    for x in ax: x.axis('off')
    plt.tight_layout(); plt.savefig('hasil/peta_prediksi_dan_pi90.png', dpi=150); plt.show()
    print(f'Rentang pengamatan {y.min():.2f}-{y.max():.2f} | rentang prediksi median {np.nanmin(peta_median):.2f}-{np.nanmax(peta_median):.2f} | PI90 rata-rata {np.nanmean(peta_pi90):.2f}')
    """),
    md("""
    Bandingkan rentang prediksi dengan rentang pengamatan yang dicetak di atas. *Random forest* merata-ratakan banyak pohon, sehingga petanya cenderung lebih sempit dan lebih halus daripada keragaman tanah yang sebenarnya.

    ## C6. Menilai interval prediksi dengan PICP

    Jika interval 90% itu jujur, sekitar 90% titik uji seharusnya berada di dalamnya.
    """),
    kode("""
    def picp(iris):
        masuk = np.zeros(len(y), bool)
        for latih, uji in iris:
            m = RandomForestQuantileRegressor(n_estimators=300, min_samples_leaf=3, max_features=.5, random_state=0, n_jobs=-1).fit(X.iloc[latih], y[latih])
            qq = m.predict(X.iloc[uji], quantiles=[.05, .95])
            masuk[uji] = (y[uji] >= qq[:, 0]) & (y[uji] <= qq[:, 1])
        return masuk.mean()

    print(f'PICP validasi acak   : {picp(iris_acak):.2f}')
    print(f'PICP validasi spasial: {picp(iris_spasial):.2f}')
    """),
    md("""
    ## C7. Wilayah keberlakuan model

    Indeks ketidakmiripan (DI) mengukur jarak setiap piksel ke titik latih terdekat dalam ruang kovariat. Meyer dan Pebesma (2021) membobot jarak ini dengan tingkat kepentingan kovariat. Karena tingkat kepentingan pada Bagian C4 tidak dapat dipercaya, di sini semua kovariat numerik diberi bobot sama. Ambangnya diturunkan dari DI titik latih saat titik-titik dari blok yang sama disisihkan. Ini penerapan sederhana untuk peragaan.
    """),
    kode("""
    skala = StandardScaler().fit(X[terpilih])
    Zt, Zp = skala.transform(X[terpilih]), skala.transform(X_piksel[terpilih])
    jarak_latih = NearestNeighbors(n_neighbors=len(Zt)).fit(Zt).kneighbors(Zt)[0][:, 1:]
    d_rata = jarak_latih.mean()
    di_titik = np.array([np.linalg.norm(Zt[blok != blok[i]] - Zt[i], axis=1).min() for i in range(len(Zt))]) / d_rata
    ambang = np.percentile(di_titik, 75) + 1.5 * (np.percentile(di_titik, 75) - np.percentile(di_titik, 25))
    di_piksel = NearestNeighbors(n_neighbors=1).fit(Zt).kneighbors(Zp)[0].ravel() / d_rata
    aoa = (di_piksel <= ambang).astype('float32')
    simpan(ke_peta(di_piksel), f'di_{SASARAN}')
    simpan(ke_peta(aoa), f'aoa_{SASARAN}')
    print(f'Ambang DI {ambang:.2f} | {100 * aoa.mean():.1f}% piksel berada di dalam wilayah keberlakuan')
    plt.figure(figsize=(3.8, 5)); plt.imshow(ke_peta(aoa), cmap='RdYlGn', vmin=0, vmax=1); plt.axis('off'); plt.title('Hijau: di dalam AOA')
    plt.tight_layout(); plt.savefig('hasil/aoa.png', dpi=150); plt.show()
    """),
    md("""
    ## C8. Melihat residual

    Residual yang masih berkelompok menandakan ada proses yang belum tertangkap kovariat. Moran's I dihitung dari residual validasi spasial dengan bobot kebalikan jarak. Nilai mendekati 0 berarti residual tidak berpola.
    """),
    kode("""
    res = y - validasi('Random forest', X, y, iris_spasial)
    xy = sampel[['x', 'y']].values
    D = np.hypot(*(xy[:, None, :] - xy[None, :, :]).transpose(2, 0, 1))
    W = np.where(D > 0, 1 / np.where(D == 0, 1, D), 0)
    z = res - res.mean()
    moran = len(z) / W.sum() * (W * np.outer(z, z)).sum() / (z ** 2).sum()
    fig, ax = plt.subplots(figsize=(3.8, 5))
    batas = np.abs(res).max()
    g = ax.scatter(xy[:, 0], xy[:, 1], c=res, cmap='RdBu', vmin=-batas, vmax=batas, s=36, edgecolor='k', lw=.3)
    plt.colorbar(g, label='Residual (%)'); ax.set_title(f"Residual, Moran's I = {moran:.2f}"); ax.axis('off')
    plt.tight_layout(); plt.savefig('hasil/residual.png', dpi=150); plt.show()
    pd.DataFrame({'Titik': sampel['Titik'], 'x': sampel.x, 'y': sampel.y, 'residual': res.round(2)}).to_csv(f'hasil/residual_{SASARAN}.csv', index=False)
    """),
    md("""
    ## Yang dibawa ke QGIS dan ke presentasi

    Folder `hasil/` kini berisi peta prediksi, PI90, DI, AOA, tabel metrik, dan gambar. Buka GeoTIFF-nya di QGIS (Modul Praktik 5, tahap terakhir), tumpangkan dengan peta SMU dari Praktik 2, lalu siapkan jawaban untuk tiga pertanyaan berikut:

    1. Seberapa baik model ini dibandingkan pembanding sederhananya?
    2. Di mana peta ini paling tidak bisa dipercaya?
    3. Data apa yang paling mungkin memperbaiki hasilnya: titik sampel tambahan, DEM yang lebih rinci, atau peta bahan induk?
    """),
]


if __name__ == '__main__':
    pilih = sys.argv[1:] or ['3', '5']
    if '3' in pilih:
        tulis(os.path.join(DATA, 'praktik-3', 'Praktik_3_Spektrum_ke_Sifat_Tanah.ipynb'), P3)
    if '5' in pilih:
        tulis(os.path.join(DATA, 'praktik-5', 'Praktik_5_Machine_Learning_DSM.ipynb'), P5)
    print('Notebook ditulis:', pilih)
