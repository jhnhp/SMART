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
INSTAL_P3 = """
# ==============================================================================
# INSTALASI DEPENDENSI (Jalankan sel ini HANYA jika pustaka belum terpasang)
# Hilangkan tanda pagar (#) pada baris di bawah untuk memasang dependensi:
# ==============================================================================
# !pip install numpy pandas matplotlib scipy scikit-learn
# Atau instal seluruh dependensi modul melalui file requirements.txt:
# !pip install -r ../../requirements.txt
"""

P3 = [
    kode(INSTAL_P3),
    md("""
    # Praktik 3. Dari Spektrum Pantulan ke Komposisi Tekstur Tanah

    ASD FieldSpec 4 merekam **spektrum pantulan** (*reflectance spectrum*), bukan nilai sifat tanah. Nilai sifat tanah baru diperoleh setelah spektrum dihubungkan dengan hasil laboratorium melalui model kalibrasi (*calibration model*). Notebook ini menelusuri jalan tersebut untuk **tekstur tanah lapisan atas** (*topsoil texture*), yaitu persentase lempung (*clay*), debu (*silt*), dan pasir (*sand*). Ketiganya adalah data komposisi (*compositional data*): jumlahnya selalu 100%, sehingga prediksinya pun harus berjumlah 100%. Karena itu, sasaran diubah dulu dengan transformasi log-rasio isometrik (*isometric log-ratio*, ILR).

    Alurnya: membaca spektrum, mengenali fitur serapan (*absorption feature*), mencoba lima praolah (*preprocessing*), melatih *Partial Least Squares Regression* (PLSR) dan *random forest*, lalu menilai hasilnya per fraksi. Seluruh notebook selesai dalam satu sampai dua menit.

    Pegangan membaca notebook: jalankan sel dari atas ke bawah dengan **Shift + Enter**, lalu baca keluarannya sebelum lanjut. Rujukan konsep ada di Modul 7, Gambar 7.3 dan 7.4.

    **Catatan data.** Pustaka spektral (*spectral library*) ini merupakan hasil pengujian sampel tanah dari Site Gunung Madu Plantation (GMP), Lampung, jadi bukan dari Sub-DAS Bompon. Kode sampel `S3 L1` ditafsirkan sebagai profil S3 lapisan 1. Model dalam notebook ini dilatih dari tanah GMP dan dipakai untuk latihan. Untuk tanah dari tempat lain, hasilnya hanya pendekatan sampai diuji dengan sampel setempat (Modul 7).
    """),
    md("## 1. Menyiapkan lingkungan kerja"),
    kode(SIAPKAN.format(paket='numpy pandas scipy scikit-learn matplotlib', n=3)),
    kode("""
    import time
    import joblib
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy.signal import savgol_filter
    from scipy.stats import pearsonr
    from sklearn.cross_decomposition import PLSRegression
    from sklearn.decomposition import PCA
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    from sklearn.base import clone
    from sklearn.model_selection import RepeatedKFold, train_test_split
    plt.rcParams.update({'figure.dpi': 110, 'axes.grid': True, 'grid.alpha': .3, 'font.size': 9})
    MULAI = time.time()
    """),
    md("""
    ## 2. Membaca pustaka spektral dan memilih lapisan 1

    Setiap baris adalah satu sampel. Kolom `w350` sampai `w2500` berisi pantulan pada setiap panjang gelombang, sedangkan kolom lainnya berisi hasil laboratorium. Setiap profil diambil sampai empat atau lima lapisan, dan lapisan dari profil yang sama saling mirip. Praktik ini hanya memakai **lapisan 1**, sehingga setiap profil diwakili satu sampel. Dengan begitu, pembagian acak latih dan uji (*random train-test split*) tidak menempatkan lapisan dari profil yang sama di kedua sisi.
    """),
    kode("""
    data = pd.read_csv('spektra_visnir_gmp.csv.gz')
    kolom_spektrum = [k for k in data.columns if k.startswith('w') and k[1:].isdigit()]
    panjang_gel = np.array([int(k[1:]) for k in kolom_spektrum], dtype=float)
    data = data.copy()
    data['profil'] = data['sampel'].str.extract(r'^(S\\d+)')[0]
    data['lapisan'] = data['sampel'].str.extract(r'L(\\d+)')[0].astype(float)
    FRAKSI = ['clay', 'silt', 'sand']          # lempung, debu, pasir

    lapisan_1 = data[data['lapisan'] == 1]
    tanpa_lab = lapisan_1[lapisan_1[FRAKSI].isna().any(axis=1)].reset_index(drop=True)
    data_l1 = lapisan_1[lapisan_1[FRAKSI].notna().all(axis=1) & (lapisan_1[FRAKSI] > 0).all(axis=1)].reset_index(drop=True)
    jumlah = data_l1[FRAKSI].sum(axis=1)

    print('Seluruh pustaka       :', len(data), 'sampel dari', data['profil'].nunique(), 'profil')
    print('Sampel per lapisan    :', data['lapisan'].value_counts().sort_index().astype(int).to_dict())
    print('Kanal                 :', len(panjang_gel), 'dari', panjang_gel.min(), 'sampai', panjang_gel.max(), 'nm')
    print('Lapisan 1 bertekstur  :', len(data_l1), 'sampel')
    print('Lapisan 1 tanpa lab   :', tanpa_lab['sampel'].tolist())
    print(f'Lempung + debu + pasir: {jumlah.min():.2f}-{jumlah.max():.2f}%')
    data_l1[FRAKSI].describe().T[['count', 'min', '50%', 'mean', 'max']].round(1)
    """),
    md("""
    Jumlah ketiga fraksi tidak selalu tepat 100% karena pembulatan di laboratorium. Sebelum dimodelkan, setiap sampel dinormalisasi agar jumlahnya tepat 100%, dengan perbandingan antarfraksi yang tetap.

    ## 3. Melihat spektrum
    """),
    kode("""
    S = data_l1[kolom_spektrum].values
    print('Beda antarkanal 350-399 nm :', round(np.abs(np.diff(S[:, panjang_gel < 400], axis=1)).mean(), 5))
    print('Beda antarkanal 400-2500 nm:', round(np.abs(np.diff(S[:, panjang_gel >= 400], axis=1)).mean(), 5))
    pilih = panjang_gel >= 400
    wl = panjang_gel[pilih]
    R = S[:, pilih]

    fig, ax = plt.subplots(1, 2, figsize=(12, 3.6), gridspec_kw={'width_ratios': [1, 2]})
    ax[0].plot(panjang_gel[1:], np.abs(np.diff(S, axis=1)).mean(axis=0), color='crimson', lw=.7)
    ax[0].set(title='Rerata beda nilai antarkanal berdekatan', xlabel='Panjang gelombang (nm)')
    urut = np.argsort(data_l1['clay'].values)
    warna = plt.cm.viridis(np.linspace(0, 1, len(urut)))
    for w, i in zip(warna, urut):
        ax[1].plot(wl, R[i], color=w, lw=.5)
    sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(data_l1['clay'].min(), data_l1['clay'].max()))
    plt.colorbar(sm, ax=ax[1], label='Lempung (%)')
    for pos, nama in [(900, 'oksida besi'), (1400, 'air/OH'), (1900, 'air'), (2205, 'kaolinit')]:
        ax[1].axvline(pos, color='k', lw=.6, ls='--'); ax[1].text(pos + 8, ax[1].get_ylim()[1] * .94, nama, fontsize=8)
    ax[1].set(title='Spektrum lapisan 1, diwarnai menurut kadar lempung', xlabel='Panjang gelombang (nm)', ylabel='Pantulan')
    plt.tight_layout(); plt.savefig('hasil/spektrum_lapisan1.png', dpi=150); plt.show()
    """),
    md("""
    Spektrum yang halus seharusnya hampir tidak berubah antarkanal yang berdekatan. Di bawah 400 nm nilainya melompat-lompat, yang menandakan derau (*noise*), sehingga pemodelan hanya memakai 400–2.500 nm. Lonjakan sempit di 1.000 nm dan 1.800 nm berada pada batas antardetektor alat.

    ## 4. Membaca fitur serapan

    Lembah di sekitar 2.205 nm berasal dari kaolinit, mineral lempung yang umum pada tanah tropis yang telah lapuk lanjut (Modul 7). Sel berikut mengukur kedalaman serapan (*absorption depth*) itu dengan garis kontinum (*continuum*) sederhana antara 2.120 nm dan 2.250 nm, lalu membandingkannya dengan kadar lempung.
    """),
    kode("""
    def kedalaman_serapan(R, wl, kiri=2120, pusat=2205, kanan=2250):
        i, c, k = [np.argmin(np.abs(wl - v)) for v in (kiri, pusat, kanan)]
        kontinum = R[:, i] + (R[:, k] - R[:, i]) * (wl[c] - wl[i]) / (wl[k] - wl[i])
        return 1 - R[:, c] / kontinum

    kedalaman = kedalaman_serapan(R, wl)
    r_lempung = np.corrcoef(kedalaman, data_l1['clay'])[0, 1]
    fig, ax = plt.subplots(figsize=(4.4, 3.4))
    ax.scatter(kedalaman, data_l1['clay'], s=14, alpha=.7)
    ax.set(xlabel='Kedalaman serapan 2.205 nm', ylabel='Lempung (%)', title=f'r = {r_lempung:.2f}')
    plt.tight_layout(); plt.savefig('hasil/fitur_serapan.png', dpi=150); plt.show()
    print('Korelasi kedalaman serapan dengan lempung:', round(r_lempung, 2))
    """),
    md("""
    ## 5. Membagi data latih dan uji

    Data dibagi sekali secara acak: 80% sebagai data latih (*training set*) dan 20% sebagai data uji (*test set*). Pembagian yang sama dipakai untuk semua praolah dan algoritme, sehingga perbandingannya adil. Data uji tidak disentuh sampai penilaian akhir.
    """),
    kode("""
    latih, uji = train_test_split(np.arange(len(data_l1)), test_size=0.2, random_state=42)
    print('Latih:', len(latih), 'sampel | Uji:', len(uji), 'sampel')
    """),
    md("""
    ## 6. Praolah spektrum

    Sebagian besar keragaman spektrum disebabkan oleh ukuran partikel dan hamburan (*scattering*), bukan komposisi kimia. Lima praolah dicoba:

    1. **RAW**, yaitu pantulan apa adanya.
    2. **SNV** (*Standard Normal Variate*), yaitu setiap spektrum dikurangi rata-ratanya lalu dibagi simpangan bakunya (Barnes et al., 1989).
    3. **MSC** (*Multiplicative Scatter Correction*), yaitu setiap spektrum diregresikan terhadap spektrum acuan, lalu dikoreksi dengan potongan dan kemiringannya (Geladi et al., 1985). Spektrum acuan dihitung dari data latih saja.
    4. **SG**, yaitu penghalusan Savitzky–Golay (*Savitzky–Golay smoothing*) dengan jendela 11 kanal (Savitzky & Golay, 1964).
    5. **SG-FD**, yaitu turunan pertama (*first derivative*) Savitzky–Golay, yang menonjolkan posisi fitur serapan.
    """),
    kode("""
    def snv(A):
        return (A - A.mean(axis=1, keepdims=True)) / A.std(axis=1, keepdims=True)

    def msc(A, acuan):
        hasil = np.empty_like(A)
        for i, baris in enumerate(A):
            miring, potong = np.polyfit(acuan, baris, 1)
            hasil[i] = (baris - potong) / miring
        return hasil

    def praolah(nama, A, acuan):
        if nama == 'RAW':
            return A
        if nama == 'SNV':
            return snv(A)
        if nama == 'MSC':
            return msc(A, acuan)
        return savgol_filter(A, window_length=11, polyorder=2, deriv=1 if nama == 'SG-FD' else 0, axis=1)

    PRAOLAH = ['RAW', 'SNV', 'MSC', 'SG', 'SG-FD']
    acuan_latih = R[latih].mean(axis=0)
    fig, ax = plt.subplots(1, 5, figsize=(14, 2.8))
    for a, nama in zip(ax, PRAOLAH):
        a.plot(wl, praolah(nama, R, acuan_latih)[::5].T, lw=.4)
        a.set(title=nama, xlabel='Panjang gelombang (nm)')
    plt.tight_layout(); plt.savefig('hasil/praolah.png', dpi=150); plt.show()
    """),
    md("""
    ## 7. Komposisi dan transformasi ILR

    Bagaimana jika setiap fraksi dimodelkan sendiri-sendiri? Sel berikut melatih tiga model PLSR terpisah untuk lempung, debu, dan pasir, lalu menjumlahkan prediksinya.
    """),
    kode("""
    Y = data_l1[FRAKSI].values / data_l1[FRAKSI].sum(axis=1).values[:, None] * 100     # tepat 100%
    A_contoh = praolah('SG-FD', R, acuan_latih)
    terpisah = np.column_stack([PLSRegression(10).fit(A_contoh[latih], Y[latih, j]).predict(A_contoh[uji]).ravel() for j in range(3)])
    total = terpisah.sum(axis=1)
    print(f'Tiga model terpisah (10 komponen, ilustrasi): jumlah prediksi {total.min():.1f}-{total.max():.1f}%')
    print('Prediksi bernilai negatif:', int((terpisah < 0).sum()))
    """),
    md("""
    Jumlahnya tidak lagi tepat 100%. Pada data ini selisihnya kecil, tetapi tidak ada yang menjaminnya. Pada tanah dengan salah satu fraksi yang sangat kecil, prediksi terpisah dapat bernilai negatif atau berjumlah jauh dari 100%. Transformasi ILR menjamin keduanya (Egozcue et al., 2003). Tiga persentase diubah menjadi dua koordinat log-rasio yang bebas bernilai berapa saja:

    - ilr₁ = √(1/2) · ln(lempung / debu)
    - ilr₂ = √(2/3) · ln(√(lempung · debu) / pasir)

    Model memprediksi kedua koordinat itu, lalu hasilnya dikembalikan menjadi persentase. Hasil kebalikan ILR selalu positif dan selalu berjumlah 100%.
    """),
    kode("""
    def ke_ilr(komposisi):
        c = komposisi / 100
        return np.column_stack([np.sqrt(1 / 2) * np.log(c[:, 0] / c[:, 1]),
                                np.sqrt(2 / 3) * np.log(np.sqrt(c[:, 0] * c[:, 1]) / c[:, 2])])

    def dari_ilr(z):
        z = np.asarray(z, float).reshape(-1, 2)
        clr = np.column_stack([z[:, 0] / np.sqrt(2) + z[:, 1] / np.sqrt(6),
                               -z[:, 0] / np.sqrt(2) + z[:, 1] / np.sqrt(6),
                               -2 * z[:, 1] / np.sqrt(6)])
        x = np.exp(clr - clr.max(axis=1, keepdims=True))
        return x / x.sum(axis=1, keepdims=True) * 100

    Z = ke_ilr(Y)
    print('Kembali utuh setelah ILR dan kebalikannya:', np.allclose(dari_ilr(Z), Y))
    pd.DataFrame(np.column_stack([Y, Z]), columns=['lempung', 'debu', 'pasir', 'ilr1', 'ilr2']).head().round(3)
    """),
    md("""
    ## 8. Melatih PLSR dan *random forest* pada setiap praolah

    Dua algoritme dibandingkan. **PLSR** adalah alat baku kemometrika (*chemometrics*) yang meringkas ribuan kanal menjadi beberapa komponen laten (*latent variables*) (Wold et al., 2001). Jumlah komponennya dipilih dengan validasi silang (*cross-validation*) 5 lipatan (*fold*) pada data latih. ***Random forest*** menggabungkan banyak pohon keputusan (*decision trees*) (Breiman, 2001) dan dilatih dengan pengaturan yang sama untuk semua praolah.

    Untuk setiap kombinasi, dihitung dua hal. **RMSE validasi silang** dihitung hanya dari data latih, dengan 5 lipatan yang diulang 3 kali, dan dipakai untuk memilih kombinasi. **Ukuran pada data uji** dihitung per fraksi:

    1. **R** (*Pearson correlation coefficient*), yaitu korelasi Pearson antara prediksi dan nilai laboratorium.
    2. **R²** (*coefficient of determination*), yaitu bagian keragaman yang dijelaskan terhadap garis 1:1, sama dengan MEC pada Modul 8. Nilainya negatif jika model lebih buruk daripada menebak rata-rata.
    3. **RMSE** (*root mean square error*) dan **MAE** (*mean absolute error*), yaitu besar galat dalam poin persen.
    4. **nRMSE** (*normalized RMSE*), yaitu RMSE dibagi jangkauan nilai uji, dalam persen.
    5. **MAPE** (*mean absolute percentage error*), yaitu rata-rata galat relatif. Nilai ini membesar pada fraksi yang kadarnya kecil seperti debu.
    """),
    kode("""
    def ukuran(y, p):
        rmse = np.sqrt(mean_squared_error(y, p))
        return {'R': pearsonr(y, p)[0], 'R2': r2_score(y, p), 'RMSE': rmse, 'nRMSE%': 100 * rmse / np.ptp(y),
                'MAE': mean_absolute_error(y, p), 'MAPE%': 100 * np.mean(np.abs((p - y) / y))}

    def rmse_komposisi(y, p):
        return np.sqrt(((y - p) ** 2).mean())

    LIPATAN = RepeatedKFold(n_splits=5, n_repeats=3, random_state=0)

    def rmse_cv(model, A, Zl, Yl):
        \"\"\"RMSE komposisi dari validasi silang 5 lipatan yang diulang 3 kali, hanya pada data latih.\"\"\"
        galat = [(dari_ilr(clone(model).fit(A[a], Zl[a]).predict(A[b])) - Yl[b]) ** 2 for a, b in LIPATAN.split(A)]
        return np.sqrt(np.concatenate(galat).mean())

    def pilih_komponen(A, Zl, Yl, kandidat=range(1, 16)):
        \"\"\"Jumlah komponen PLSR dengan RMSE validasi silang terkecil, hanya dari data latih.\"\"\"
        nilai = [rmse_cv(PLSRegression(k), A, Zl, Yl) for k in kandidat]
        return kandidat[int(np.argmin(nilai))], min(nilai), nilai

    def hutan():
        return RandomForestRegressor(n_estimators=300, max_features=0.3, random_state=42, n_jobs=-1)

    hasil, prediksi, ringkas, kurva_cv = [], {}, [], {}
    for nama_p in PRAOLAH:
        A = praolah(nama_p, R, acuan_latih)
        k, cv_pls, kurva_cv[nama_p] = pilih_komponen(A[latih], Z[latih], Y[latih])
        cv_rf = rmse_cv(hutan(), A[latih], Z[latih], Y[latih])
        for nama_m, model, cv in [('PLSR', PLSRegression(k), cv_pls), ('Random forest', hutan(), cv_rf)]:
            P = dari_ilr(model.fit(A[latih], Z[latih]).predict(A[uji]))
            prediksi[(nama_p, nama_m)] = P
            ringkas.append({'Praolah': nama_p, 'Algoritma': nama_m, 'Komponen PLSR': k if nama_m == 'PLSR' else np.nan, 'RMSE validasi silang': cv})
            for j, f in enumerate(FRAKSI):
                hasil.append({'Praolah': nama_p, 'Algoritma': nama_m, 'Fraksi': f, **ukuran(Y[uji, j], P[:, j])})
    metrik = pd.DataFrame(hasil)
    metrik.to_csv('hasil/metrik_per_fraksi.csv', index=False)
    tabel = metrik.pivot_table(index=['Praolah', 'Algoritma'], columns='Fraksi', values=['R2', 'RMSE'])
    tabel.columns = [f'{u} {f}' for u, f in tabel.columns]
    tabel = tabel[[f'{u} {f}' for u in ['R2', 'RMSE'] for f in FRAKSI]]
    tabel = tabel.join(pd.DataFrame(ringkas).set_index(['Praolah', 'Algoritma']))
    tabel.loc[[(p, m) for p in PRAOLAH for m in ['PLSR', 'Random forest']]].round(2)
    """),
    md("""
    **Cara membaca.** Kolom R2 dan RMSE berasal dari 14 sampel uji, sedangkan kolom terakhir dari validasi silang pada data latih. Perhatikan bahwa urutan kombinasi menurut data uji tidak selalu sama dengan urutan menurut validasi silang.

    ## 9. Memilih kombinasi tanpa mengintip data uji

    Godaannya adalah memilih kombinasi dengan R² uji tertinggi, lalu melaporkan R² itu. Cara itu curang: data uji ikut dipakai untuk memilih (*data leakage*), sehingga angkanya tidak lagi menggambarkan sampel yang benar-benar baru. Kombinasi dipilih dari RMSE validasi silang data latih, lalu dinilai sekali pada data uji.
    """),
    kode("""
    kv = pd.DataFrame(ringkas).sort_values('RMSE validasi silang')
    TERPILIH = tuple(kv.iloc[0][['Praolah', 'Algoritma']])
    K_PLSR = int(kv[(kv['Praolah'] == TERPILIH[0]) & (kv['Algoritma'] == 'PLSR')]['Komponen PLSR'].iloc[0])
    print('Kombinasi terpilih dari validasi silang:', TERPILIH, '| komponen PLSR untuk praolah ini:', K_PLSR)
    display(kv.round(2).reset_index(drop=True))

    # kurva jumlah komponen PLSR pada praolah terpilih; garis data uji hanya untuk peragaan
    A_t = praolah(TERPILIH[0], R, acuan_latih)
    kurva_uji = [rmse_komposisi(Y[uji], dari_ilr(PLSRegression(k).fit(A_t[latih], Z[latih]).predict(A_t[uji]))) for k in range(1, 16)]
    fig, ax = plt.subplots(figsize=(5.6, 3.2))
    ax.plot(range(1, 16), kurva_cv[TERPILIH[0]], marker='o', ms=3, label='Validasi silang data latih')
    ax.plot(range(1, 16), kurva_uji, marker='s', ms=3, ls='--', label='Data uji (hanya peragaan)')
    ax.set(xlabel='Jumlah komponen PLSR', ylabel='RMSE komposisi (%)', title=f'PLSR, praolah {TERPILIH[0]}'); ax.legend(fontsize=7)
    plt.tight_layout(); plt.savefig('hasil/pemilihan_komponen.png', dpi=150); plt.show()
    metrik[(metrik['Praolah'] == TERPILIH[0]) & (metrik['Algoritma'] == TERPILIH[1])].set_index('Fraksi').drop(columns=['Praolah', 'Algoritma']).round(2)
    """),
    md("""
    Kedua garis pada gambar tidak selalu sejalan. Jika jumlah komponen dipilih dari garis data uji, angka uji akan tampak lebih baik, tetapi tidak lagi jujur, karena model sudah disesuaikan dengan 14 sampel yang seharusnya mewakili sampel baru.
    """),
    md("""
    ## 10. Prediksi terhadap nilai laboratorium

    Panel kiri sampai tengah membandingkan prediksi dengan nilai laboratorium untuk setiap fraksi. Panel kanan menempatkan setiap sampel uji pada segitiga tekstur (*soil texture triangle*): titik kosong adalah nilai laboratorium, titik isi adalah prediksi, dan garis menghubungkan keduanya.
    """),
    kode("""
    P = prediksi[TERPILIH]
    nama_id = {'clay': 'Lempung', 'silt': 'Debu', 'sand': 'Pasir'}

    def ke_segitiga(komposisi):
        l, p = komposisi[:, 0] / 100, komposisi[:, 2] / 100
        return p + l / 2, l * np.sqrt(3) / 2         # pasir ke kanan, lempung ke atas, debu ke kiri

    fig, ax = plt.subplots(1, 4, figsize=(15, 3.6))
    for a, (j, f) in zip(ax[:3], enumerate(FRAKSI)):
        a.scatter(Y[uji, j], P[:, j], s=18)
        b = [min(Y[uji, j].min(), P[:, j].min()) - 2, max(Y[uji, j].max(), P[:, j].max()) + 2]
        a.plot(b, b, 'k--', lw=.8)
        a.set(xlabel=f'{nama_id[f]} laboratorium (%)', ylabel=f'{nama_id[f]} prediksi (%)', title=f"R² {r2_score(Y[uji, j], P[:, j]):.2f}")
    x0, y0 = ke_segitiga(Y[uji]); x1, y1 = ke_segitiga(P)
    ax[3].plot([0, 1, .5, 0], [0, 0, np.sqrt(3) / 2, 0], color='k', lw=.8)
    for i in range(len(uji)):
        ax[3].plot([x0[i], x1[i]], [y0[i], y1[i]], color='grey', lw=.6)
    ax[3].scatter(x0, y0, s=22, facecolors='none', edgecolors='k', label='Laboratorium')
    ax[3].scatter(x1, y1, s=16, color='#d95f02', label='Prediksi')
    ax[3].text(.5, np.sqrt(3) / 2 + .03, 'Lempung', ha='center'); ax[3].text(-.02, -.06, 'Debu', ha='center'); ax[3].text(1.02, -.06, 'Pasir', ha='center')
    ax[3].set_aspect('equal'); ax[3].axis('off'); ax[3].legend(fontsize=7, loc='upper right')
    plt.suptitle(f'{TERPILIH[1]} dengan praolah {TERPILIH[0]} pada {len(uji)} sampel uji')
    plt.tight_layout(); plt.savefig('hasil/prediksi_vs_laboratorium.png', dpi=150); plt.show()
    print('Jumlah setiap prediksi:', np.round(P.sum(axis=1), 6).min(), '-', np.round(P.sum(axis=1), 6).max(), '%')
    """),
    md("""
    ## 11. Seberapa stabil satu pembagian?

    Dengan 14 sampel uji, angka di atas sangat bergantung pada sampel yang kebetulan terpilih. Sel berikut mengulang pembagian 80:20 sebanyak 20 kali dengan praolah terpilih dan pengaturan model yang sama.
    """),
    kode("""
    ulang = []
    for acak in range(20):
        a, b = train_test_split(np.arange(len(Y)), test_size=0.2, random_state=acak)
        Ai = praolah(TERPILIH[0], R, R[a].mean(axis=0))
        for nama_m, model in [('PLSR', PLSRegression(K_PLSR)), ('Random forest', hutan())]:
            Pu = dari_ilr(model.fit(Ai[a], Z[a]).predict(Ai[b]))
            ulang += [{'Algoritma': nama_m, 'Fraksi': f, 'R2': r2_score(Y[b, j], Pu[:, j])} for j, f in enumerate(FRAKSI)]
    ulang = pd.DataFrame(ulang)
    fig, ax = plt.subplots(figsize=(6.4, 3))
    data_kotak = [ulang[(ulang['Algoritma'] == m) & (ulang['Fraksi'] == f)]['R2'] for f in FRAKSI for m in ['PLSR', 'Random forest']]
    ax.boxplot(data_kotak)
    ax.set_xticks(range(1, 7), [f'{nama_id[f]}\\n{m}' for f in FRAKSI for m in ['PLSR', 'RF']])
    ax.axhline(0, color='k', lw=.6); ax.set(ylabel='R² data uji', title=f'20 pembagian acak 80:20, praolah {TERPILIH[0]}')
    plt.tight_layout(); plt.savefig('hasil/stabilitas_pembagian.png', dpi=150); plt.show()
    ulang.groupby(['Fraksi', 'Algoritma'])['R2'].describe()[['min', '50%', 'max']].reindex(FRAKSI, level=0).round(2)
    """),
    md("""
    ## 12. Wilayah spektrum mana yang dipakai model?

    Kepentingan dihitung dengan permutasi (*permutation importance*) per fraksi: nilai satu wilayah spektrum pada data uji diacak, lalu diukur kenaikan MAE setiap fraksi. Kanal yang bersebelahan hampir identik, sehingga mengacak satu kanal saja hampir tidak berpengaruh karena informasinya masih ada di kanal tetangganya. Karena itu yang diacak adalah **jendela 20 nm** (*spectral window*), dengan 5 ulangan, dan satu prediksi dipakai untuk ketiga fraksi sekaligus. Perhitungan ini dibuat untuk praolah SG-FD pada kedua algoritme.
    """),
    kode("""
    LEBAR = 20
    jendela = [(a, a + LEBAR) for a in range(400, 2500, LEBAR)]
    indeks = [np.where((wl >= a) & (wl < b))[0] for a, b in jendela]

    def kepentingan_jendela(model, A_uji, Y_uji, ulang=5, seed=0):
        rng = np.random.default_rng(seed)
        dasar = np.abs(dari_ilr(model.predict(A_uji)) - Y_uji).mean(axis=0)
        naik = np.zeros((len(indeks), 3))
        for i, ii in enumerate(indeks):
            for _ in range(ulang):
                Ap = A_uji.copy()
                Ap[:, ii] = A_uji[rng.permutation(len(A_uji))][:, ii]
                naik[i] += (np.abs(dari_ilr(model.predict(Ap)) - Y_uji).mean(axis=0) - dasar) / ulang
        return pd.DataFrame(naik, columns=FRAKSI, index=[f'{a}-{b}' for a, b in jendela])

    A_fd = praolah('SG-FD', R, None)
    k_fd = int(pd.DataFrame(ringkas).query("Praolah == 'SG-FD' and Algoritma == 'PLSR'")['Komponen PLSR'].iloc[0])
    kepentingan = {}
    for nama_m, model in [('PLSR', PLSRegression(k_fd)), ('Random forest', hutan())]:
        kepentingan[nama_m] = kepentingan_jendela(model.fit(A_fd[latih], Z[latih]), A_fd[uji], Y[uji])

    tengah = [a + LEBAR / 2 for a, _ in jendela]
    fig, ax = plt.subplots(3, 2, figsize=(12, 6.4), sharex=True)
    for c, (nama_m, imp) in enumerate(kepentingan.items()):
        for r_, f in enumerate(FRAKSI):
            a = ax[r_, c]
            a.bar(tengah, imp[f], width=LEBAR * .9, color=np.where(imp[f] > 0, '#2166ac', '#b2182b'))
            for pos in (1400, 1900, 2205):
                a.axvline(pos, color='k', lw=.5, ls='--')
            a.set(title=f'{nama_m}: {nama_id[f]}', ylabel='Kenaikan MAE')
    for a in ax[-1]:
        a.set_xlabel('Panjang gelombang (nm)')
    plt.tight_layout(); plt.savefig('hasil/kepentingan_jendela.png', dpi=150); plt.show()

    teratas = pd.concat({(m, nama_id[f]): imp[f].sort_values(ascending=False).head(10).reset_index().rename(columns={'index': 'Jendela (nm)', f: 'Kenaikan MAE'})
                         for m, imp in kepentingan.items() for f in FRAKSI}, names=['Algoritma', 'Fraksi', 'Urutan'])
    teratas.to_csv('hasil/kepentingan_jendela_top10.csv')
    teratas.groupby(level=[0, 1]).head(3).round(3)
    """),
    md("""
    Batang biru menandai jendela yang, bila diacak, menaikkan galat, sedangkan batang merah berarti galat justru turun. Hasil dari 14 sampel uji ini masih kasar, sehingga yang patut diperhatikan adalah wilayah yang konsisten, misalnya di sekitar serapan air dan hidroksil (1.400 dan 1.900 nm) atau kaolinit (2.205 nm), bukan urutan jendela satu per satu.

    ## 13. Memakai model untuk sampel tanah baru

    Setelah model jadi, sampel tanah baru cukup diukur spektrumnya tanpa dianalisis di laboratorium. Ada lima langkah:

    1. **Latih model akhir dan simpan**, yaitu model dilatih ulang dengan seluruh 69 sampel memakai kombinasi terpilih, lalu disimpan ke berkas bersama semua yang diperlukan untuk memakainya: nama praolah, spektrum acuan MSC, daftar panjang gelombang, dan ringkasan sebaran spektrum pustaka.
    2. **Siapkan spektrum baru**, yaitu berkas CSV dengan kolom `sampel` dan `w350` sampai `w2500`, satu baris per sampel. Berkas `spektrum_sampel_baru.csv` adalah contohnya (*dummy*). Isinya 10 spektrum asli dari pustaka yang sama tanpa kolom laboratorium, yaitu dua sampel lapisan 1 yang memang tidak dianalisis dan delapan sampel lapisan 4 yang tidak dipakai melatih model.
    3. **Prediksi**, yaitu spektrum baru diberi praolah yang **sama persis**, dimasukkan ke model, lalu hasilnya dikembalikan menjadi persentase.
    4. **Periksa kemiripan dengan pustaka**, karena model hanya dapat dipercaya untuk spektrum yang mirip dengan spektrum yang dipakai melatihnya. Kemiripan diukur dengan jarak Mahalanobis (*Mahalanobis distance*) pada lima komponen utama spektrum pustaka (*principal component analysis*, PCA). Jarak itu dibagi jarak sampel pustaka yang terjauh, sehingga nilai di atas 1 berarti spektrum baru lebih asing daripada sampel pustaka mana pun.
    5. **Uji sebagian sampel di laboratorium**, karena kemiripan spektrum tidak menjamin prediksi benar, seperti terlihat pada sel terakhir.
    """),
    kode("""
    acuan_semua = R.mean(axis=0)
    A_semua = praolah(TERPILIH[0], R, acuan_semua)
    model_akhir = (PLSRegression(K_PLSR) if TERPILIH[1] == 'PLSR' else hutan()).fit(A_semua, Z)
    pca = PCA(n_components=5).fit(A_semua)
    skor = pca.transform(A_semua)
    paket = {'model': model_akhir, 'praolah': TERPILIH[0], 'acuan': acuan_semua, 'panjang_gel': wl, 'pca': pca,
             'ambang': np.sqrt(((skor / np.sqrt(pca.explained_variance_)) ** 2).sum(axis=1)).max()}
    joblib.dump(paket, 'hasil/model_tekstur_lapisan1.joblib')
    print('Model disimpan:', TERPILIH, '| keragaman spektrum yang diringkas lima komponen utama:', round(pca.explained_variance_ratio_.sum(), 3))
    """),
    md("""
    Fungsi berikut memuat model tersimpan, memeriksa kelengkapan kolom spektrum, memberi praolah yang sama, memprediksi, lalu menghitung jarak ke pustaka. Untuk sampel Anda sendiri, cukup ganti nama berkas pada `pd.read_csv`. Model tersimpan dapat dipakai lagi di lain waktu tanpa melatih ulang: jalankan bagian 1, sel fungsi praolah (bagian 6) dan ILR (bagian 7), lalu sel ini.
    """),
    kode("""
    def prediksi_tekstur(tabel, berkas_model='hasil/model_tekstur_lapisan1.joblib'):
        \"\"\"Prediksi lempung, debu, dan pasir untuk spektrum baru dengan model tersimpan.\"\"\"
        paket = joblib.load(berkas_model)
        kolom = [f'w{int(w)}' for w in paket['panjang_gel']]
        kurang = [k for k in kolom if k not in tabel.columns]
        if kurang:
            raise ValueError(f'{len(kurang)} kolom spektrum tidak ada, misalnya {kurang[:3]}')
        A = praolah(paket['praolah'], tabel[kolom].to_numpy(float), paket['acuan'])
        hasil = pd.DataFrame(dari_ilr(paket['model'].predict(A)).round(1), columns=['Lempung (%)', 'Debu (%)', 'Pasir (%)'])
        hasil.insert(0, 'Sampel', tabel['sampel'].values)
        skor = paket['pca'].transform(A)
        jarak = np.sqrt(((skor / np.sqrt(paket['pca'].explained_variance_)) ** 2).sum(axis=1)) / paket['ambang']
        hasil['Jarak ke pustaka'] = jarak.round(2)
        hasil['Mirip pustaka'] = np.where(jarak <= 1, 'ya', 'tidak')
        return hasil

    sampel_baru = pd.read_csv('spektrum_sampel_baru.csv')        # ganti dengan berkas spektrum Anda
    prediksi_baru = prediksi_tekstur(sampel_baru)
    prediksi_baru.to_csv('hasil/prediksi_sampel_baru.csv', index=False)
    prediksi_baru
    """),
    md("""
    **Seberapa jauh model ini berlaku untuk tanah lain?** Delapan sampel lapisan 4 dalam berkas contoh sebenarnya memiliki hasil laboratorium di pustaka, demikian pula semua sampel lapisan 2 sampai 4. Sel berikut memperlakukan lapisan-lapisan bawah itu sebagai sampel baru, lalu membandingkan prediksinya dengan hasil laboratorium. Bias adalah rata-rata selisih prediksi terhadap nilai laboratorium, sehingga nilai positif berarti prediksi cenderung terlalu tinggi.
    """),
    kode("""
    uji_lain = []
    for lap in (2, 3, 4):
        t = data[(data['lapisan'] == lap) & data[FRAKSI].notna().all(axis=1) & (data[FRAKSI] > 0).all(axis=1)]
        Yt = t[FRAKSI].values / t[FRAKSI].sum(axis=1).values[:, None] * 100
        h = prediksi_tekstur(t)
        Pt = h[['Lempung (%)', 'Debu (%)', 'Pasir (%)']].values
        baris_uji = {'Lapisan': lap, 'Sampel': len(t), 'Mirip pustaka (%)': 100 * (h['Mirip pustaka'] == 'ya').mean()}
        for j, f in enumerate(FRAKSI):
            baris_uji[f'RMSE {nama_id[f].lower()}'] = np.sqrt(((Pt[:, j] - Yt[:, j]) ** 2).mean())
            baris_uji[f'Bias {nama_id[f].lower()}'] = (Pt[:, j] - Yt[:, j]).mean()
        uji_lain.append(baris_uji)
    uji_lain = pd.DataFrame(uji_lain).round(1)
    uji_lain.to_csv('hasil/uji_lapisan_bawah.csv', index=False)
    print(f'Seluruh notebook selesai dalam {time.time() - MULAI:.0f} detik.')
    uji_lain
    """),
    md("""
    Lapisan 2 tampak cukup baik, bahkan lebih baik daripada data uji lapisan 1 di bagian 9, karena lapisan 2 berasal dari profil yang lapisan 1-nya ikut melatih model. Pada lapisan yang lebih dalam, galat dan biasnya membesar. Pada lapisan 4, lempung cenderung diduga terlalu tinggi dan pasir terlalu rendah, padahal sebagian besar spektrumnya dinilai mirip dengan pustaka, dan kedelapan sampel lapisan 4 pada berkas contoh pun lolos pemeriksaan kemiripan. Pemeriksaan kemiripan membantu menyaring spektrum yang asing, tetapi tidak menjamin prediksi benar. Karena itu, setiap kali model dipakai untuk tanah dari kebun atau kedalaman lain, kirim sebagian sampel ke laboratorium. Bila prediksinya bias, tambahkan sampel setempat ke data kalibrasi. Modul 7 menyebut cara ini *spiking*, dan pendekatan rs-local menunjukkan bahwa 12–20 sampel lokal sudah dapat meningkatkan ketelitian dan kekokohan prediksi (England & Viscarra Rossel, 2018).
    """),
    md("""
    ## Yang dibawa ke diskusi

    1. Mengapa prediksi tekstur perlu dibuat sebagai komposisi, dan apa yang terjadi bila setiap fraksi dimodelkan sendiri?
    2. Fraksi mana yang paling mudah dan paling sulit diduga dari spektrum, dan mengapa?
    3. Seberapa jauh satu angka R² dari 14 sampel uji dapat dipercaya, dilihat dari 20 pembagian acak?
    4. Wilayah spektrum mana yang dipakai model, dan apakah sesuai dengan fitur serapan pada Modul 7?
    5. Bila model ini dipakai untuk sampel dari kebun Anda, berapa sampel yang perlu dikirim ke laboratorium untuk memeriksanya?
    """),
]

# ---------------------------------------------------------------------------------------------
# PRAKTIK 5
# ---------------------------------------------------------------------------------------------
# Pengaturan CatBoost dipakai di seluruh notebook Praktik 5. allow_writing_files=False mencegah folder
# log catboost_info/ di folder peserta. one_hot_max_size=10 membuat kategori
# dengan paling banyak 10 nilai dikodekan one-hot di dalam CatBoost; kategori yang lebih beragam
# tetap memakai ordered target statistics. Dengan nilai bawaan (2) pelatihan sekitar tujuh sampai
# delapan kali lebih lama tanpa kenaikan akurasi pada data ini (sel pembanding di C2; dicatat di modul).
CATBOOST_P5 = "dict(iterations=300, depth=4, learning_rate=0.08, one_hot_max_size=10, random_seed=0, verbose=0, allow_writing_files=False)"

INSTAL_P5 = """
# ==============================================================================
# INSTALASI DEPENDENSI (Jalankan sel ini HANYA jika pustaka belum terpasang)
# Hilangkan tanda pagar (#) pada baris di bawah untuk memasang dependensi:
# ==============================================================================
# !pip install numpy pandas matplotlib scipy scikit-learn rasterio catboost imbalanced-learn
# Atau instal seluruh dependensi modul melalui file requirements.txt:
# !pip install -r ../../requirements.txt
"""

P5 = [
    kode(INSTAL_P5),
    md("""
    # Praktik 5. Machine Learning untuk Digital Soil Mapping

    Notebook ini memetakan **tutupan material**, yaitu bahan induk tanah (*parent material*), di Sub-DAS Bompon dengan pembelajaran mesin (*machine learning*). Sasarannya kategorik: tujuh kelas material pada peta Malik (2017), yang juga dipakai Fatmawati (2026) sebagai kovariat bahan induk. Alurnya mengikuti persamaan SCORPAN pada Modul 8: mempelajari hubungan antara kelas di titik sampel dan kondisi lingkungannya, menilai hubungan itu secara jujur, lalu menerapkannya ke seluruh piksel.

    Model utama adalah **CatBoost** (Prokhorenkova et al., 2018), algoritme *gradient boosting* yang dapat membaca kovariat kategorik secara langsung. *Random forest* dipakai sebagai pembanding.

    Notebook dibagi menjadi tiga bagian:

    - **Bagian A**, Machine Learning untuk DSM;
    - **Bagian B**, penyiapan dan pemilihan kovariat berdasarkan SCORPAN;
    - **Bagian C**, pembangunan model DSM.

    Satu hal perlu dipegang sejak awal: kelas di 210 titik diambil dari **peta**, bukan dari pengamatan lapangan. Ukuran ketelitian di notebook ini menyatakan seberapa baik model mereproduksi peta Malik (2017) dari kovariat, bukan seberapa benar peta itu di lapangan.
    """),
    md("## Menyiapkan lingkungan kerja"),
    kode(SIAPKAN.format(paket='numpy pandas scipy scikit-learn matplotlib rasterio catboost imbalanced-learn', n=5)),
    kode("""
    import glob
    import shutil
    import textwrap
    import time
    import warnings
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    from matplotlib.patches import Patch
    import rasterio
    from catboost import CatBoostClassifier
    from imblearn.over_sampling import SMOTE, SMOTENC
    from sklearn.cluster import KMeans
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score, cohen_kappa_score, confusion_matrix, f1_score, precision_score, recall_score
    from sklearn.model_selection import GroupKFold, StratifiedKFold, train_test_split
    from sklearn.neighbors import NearestNeighbors
    from sklearn.preprocessing import StandardScaler
    plt.rcParams.update({'figure.dpi': 110, 'font.size': 9})
    warnings.filterwarnings('ignore', category=UserWarning)
    warnings.filterwarnings('ignore', category=FutureWarning)
    """),
    md("""
    # Bagian A. Machine Learning untuk DSM

    ## A1. Membaca titik sampel dan kovariat

    Berkas `titik_tutupan_material.csv` memuat 210 titik, 30 titik untuk setiap kelas. Titik ditempatkan di pusat sel grid kovariat 10 m, sekurang-kurangnya 15 m di dalam poligon kelasnya, dan disebar merata di setiap kelas. Kolom `subset` membagi titik menjadi 21 titik latih (*training data*) dan 9 titik uji (*test data*) per kelas. Folder `kovariat/` berisi satu GeoTIFF untuk setiap kovariat, sedangkan `material_acuan_10m.tif` adalah peta Malik (2017) pada grid yang sama, yang hanya dipakai sebagai pembanding.
    """),
    kode("""
    titik = pd.read_csv('titik_tutupan_material.csv')
    jalur = sorted(glob.glob('kovariat/*.tif'))
    nama_kov = [os.path.basename(p)[:-4] for p in jalur]
    susunan = []
    for p in jalur:
        with rasterio.open(p) as r:
            susunan.append(r.read(1).astype('float32'))
            transform, crs, tinggi, lebar, batas_grid = r.transform, r.crs, r.height, r.width, r.bounds
    kubus = np.stack(susunan)      # kovariat x baris x kolom
    with rasterio.open('material_acuan_10m.tif') as r:
        acuan = r.read(1)
    dalam = kubus[nama_kov.index('kat_bentuklahan')] > 0     # piksel di dalam Sub-DAS

    KELAS = titik.drop_duplicates('kode').set_index('kode')['material'].sort_index()
    WARNA = {1: '#E69F00', 2: '#56B4E9', 3: '#0072B2', 4: '#009E73', 5: '#F0E442', 6: '#D55E00', 7: '#CC79A7'}
    PETA_WARNA = ListedColormap([WARNA[k] for k in KELAS.index])
    luas_ha = pd.Series(np.bincount(acuan[dalam], minlength=len(KELAS) + 1)[1:] * 100 / 1e4, index=KELAS.index)
    y = titik['kode'].values

    print('Titik    :', len(titik))
    print('Kovariat :', len(nama_kov), nama_kov)
    print('Grid     :', kubus.shape[1:], '| CRS', crs)
    pd.DataFrame({'Material': KELAS, 'Titik': titik['kode'].value_counts().sort_index(),
                  'Luas pada peta (ha)': luas_ha.round(1), 'Luas (%)': (100 * luas_ha / luas_ha.sum()).round(1)})
    """),
    md("""
    Perhatikan bahwa setiap kelas memiliki 30 titik, padahal luasnya sangat berbeda. Kelas 1 hanya sekitar 3% wilayah, sedangkan kelas 2 sekitar seperempatnya. Akibat rancangan sampel seimbang (*balanced sampling*) ini dibahas pada Bagian C5 dan C6.

    ## A2. Mengambil nilai kovariat di titik sampel

    Langkah ini disebut penumpangan (*overlay*). Hasilnya adalah tabel pemodelan: satu baris per titik, berisi kelas material dan semua nilai kovariat. Tabel di bawah menampilkan median setiap kovariat numerik per kelas.
    """),
    kode("""
    baris, kolom = rasterio.transform.rowcol(transform, titik['x'].values, titik['y'].values)
    tabel = pd.DataFrame(kubus[:, np.array(baris), np.array(kolom)].T, columns=nama_kov)
    tabel.insert(0, 'kode', y)
    tabel.to_csv('hasil/tabel_kovariat_di_titik.csv', index=False)
    numerik = [k for k in nama_kov if not k.startswith('kat_')]
    tabel.groupby('kode')[numerik].median().T.round(2)
    """),
    md("""
    ## A3. Model pertama: latih, uji, dan bahaya *overfitting*

    Pakai pembagian yang sudah disiapkan di kolom `subset`: 147 titik latih dan 63 titik uji. Latih CatBoost dengan kovariat numerik saja, lalu bandingkan ketelitiannya pada data latih dan data uji.

    **Akurasi keseluruhan** (*overall accuracy*, OA) adalah proporsi titik yang kelasnya ditebak benar. Karena ada tujuh kelas dengan jumlah titik sama, menebak sembarang hanya memberi akurasi sekitar 1/7 = 0,14. **Kappa Cohen** (*Cohen's kappa*) menyatakan seberapa jauh akurasi melampaui kesepakatan yang terjadi karena kebetulan (*chance agreement*). **Presisi makro**, **recall makro**, dan **F1 makro** (*macro-averaged precision, recall, and F1-score*) adalah rata-rata presisi, recall, dan F1 ketujuh kelas, sehingga kelas yang selalu salah ikut menurunkan nilainya. Arti presisi dan recall setiap kelas dijelaskan pada Bagian C3.
    """),
    kode(f"""
    def ukuran(y, p):
        return {{'Akurasi': accuracy_score(y, p), 'Kappa': cohen_kappa_score(y, p),
                'Presisi makro': precision_score(y, p, average='macro', zero_division=0),
                'Recall makro': recall_score(y, p, average='macro', zero_division=0),
                'F1 makro': f1_score(y, p, average='macro', zero_division=0)}}

    PENGATURAN_CATBOOST = {CATBOOST_P5}

    def catboost_baru(**atur):
        \"\"\"CatBoost dengan pengaturan yang sama di seluruh notebook; atur menimpa pengaturan bawaan.\"\"\"
        return CatBoostClassifier(**{{**PENGATURAN_CATBOOST, **atur}})

    latih = (titik['subset'] == 'latih').values
    cb = catboost_baru().fit(tabel.loc[latih, numerik], y[latih])
    pd.DataFrame({{'Data latih': ukuran(y[latih], cb.predict(tabel.loc[latih, numerik]).ravel()),
                  'Data uji': ukuran(y[~latih], cb.predict(tabel.loc[~latih, numerik]).ravel())}}).T.round(2)
    """),
    md("""
    **Diskusi.** Ketelitian pada data latih hampir selalu indah karena model menghafal. Hanya angka pada data uji yang boleh dibaca sebagai kemampuan model. Pembagian tunggal (*single train-test split*) juga rapuh, karena hasilnya bergantung pada titik yang kebetulan terpilih sebagai data uji. Sel berikut mengulang pembagian 70/30 secara acak sebanyak 30 kali.
    """),
    kode("""
    hasil = []
    for acak in range(30):
        a, b = train_test_split(np.arange(len(y)), test_size=.3, stratify=y, random_state=acak)
        m = catboost_baru().fit(tabel.loc[a, numerik], y[a])
        hasil.append(accuracy_score(y[b], m.predict(tabel.loc[b, numerik]).ravel()))
    plt.figure(figsize=(5, 2.6)); plt.hist(hasil, bins=10, color='#35978f')
    plt.axvline(1 / 7, color='k', ls='--', lw=.8); plt.text(1 / 7, plt.ylim()[1] * .9, ' menebak', fontsize=8)
    plt.xlabel('Akurasi data uji'); plt.ylabel('Jumlah percobaan'); plt.title('Hasil 30 pembagian acak yang berbeda')
    plt.tight_layout(); plt.savefig('hasil/sebaran_akurasi_pembagian_tunggal.png', dpi=150); plt.show()
    print(f'Akurasi terendah {min(hasil):.2f}, median {np.median(hasil):.2f}, tertinggi {max(hasil):.2f}')
    """),
    md("""
    # Bagian B. Penyiapan dan pemilihan kovariat

    ## B1. Memetakan kovariat ke faktor SCORPAN

    Kali ini sasaran pemodelan adalah faktor **p**, yaitu bahan induk itu sendiri. Karena itu peta material tidak dapat dipakai sebagai kovariat. Yang dipelajari adalah seberapa jauh faktor lain, terutama relief (r) dan data penginderaan jauh (o, s), mencerminkan material di bawahnya. Kolom terakhir adalah alasan geomorfologis atau pedologisnya. Alasan itu adalah hipotesis yang belum tentu terbukti pada data ini.
    """),
    kode("""
    faktor = pd.DataFrame([
        ('elevasi', 'r', 'DEMNAS', 'Satuan material menempati posisi yang berbeda dalam lanskap'),
        ('lereng', 'r', 'DEMNAS', 'Batuan yang tahan pelapukan cenderung membentuk lereng terjal'),
        ('tpi', 'r', 'DEMNAS', 'Punggungan dan lembah; endapan mengisi bagian yang rendah'),
        ('tri', 'r', 'DEMNAS', 'Kekasaran medan yang dipengaruhi ketahanan batuan'),
        ('twi', 'r', 'DEMNAS', 'Zona penerimaan aliran dan penimbunan endapan'),
        ('arah_utara', 'r', 'DEMNAS', 'Arah hadap; kaitannya dengan material diduga lemah'),
        ('jarak_sungai', 'r', 'Peta sungai', 'Endapan longsor dan koluvial berada di sepanjang alur'),
        ('kat_bentuklahan', 'r', 'Peta riset', 'Bentuklahan mencerminkan proses dan bahan penyusunnya'),
        ('kat_penggunaan_lahan', 'o', 'Foto udara', 'Penggunaan lahan dapat mengikuti kondisi tanah dari material'),
        ('ndvi_2024', 'o', 'Sentinel-2', 'Kerapatan vegetasi yang mungkin berbeda menurut material'),
        ('ndvi_2025', 'o', 'Sentinel-2', 'Kerapatan vegetasi yang mungkin berbeda menurut material'),
        ('bsi_2024', 'o/s', 'Sentinel-2', 'Keterbukaan tanah'),
        ('bi_2024', 'o/s', 'Sentinel-2', 'Kecerahan permukaan, terkait warna tanah bila terbuka'),
        ('cmr_2024', 'o/s', 'Sentinel-2', 'Rasio SWIR yang peka terhadap mineral lempung hasil alterasi'),
        ('sar_vv', 'o/r', 'Sentinel-1', 'Kekasaran dan kelembapan permukaan, bentuk medan'),
        ('sar_vh', 'o', 'Sentinel-1', 'Hamburan volume vegetasi'),
    ], columns=['Kovariat', 'Faktor', 'Sumber', 'Alasan'])
    faktor
    """),
    md("""
    ## B2. Korelasi Pearson antarkovariat

    Kovariat yang sangat mirip membawa informasi yang hampir sama. Korelasi Pearson (*Pearson correlation coefficient*, r) mengukur kemiripan linear dua kovariat, dari −1 sampai 1. Korelasi dihitung dari seluruh piksel di dalam Sub-DAS, bukan dari 210 titik saja, agar stabil. Pasangan dengan |r| ≥ 0,8 dicatat di sini, tetapi belum dibuang. Kovariat mana yang dipertahankan dari setiap pasangan diputuskan pada Bagian C4, setelah tingkat kepentingannya bagi model diketahui.
    """),
    kode("""
    piksel = pd.DataFrame(kubus[:, dalam].T, columns=nama_kov)
    r_pix = piksel[numerik].corr(method='pearson')

    fig, ax = plt.subplots(figsize=(6.4, 5.4))
    g = ax.imshow(r_pix, cmap='RdBu_r', vmin=-1, vmax=1)
    ax.set_xticks(range(len(numerik)), numerik, rotation=90); ax.set_yticks(range(len(numerik)), numerik)
    for i in range(len(numerik)):
        for j in range(len(numerik)):
            ax.text(j, i, f'{r_pix.iloc[i, j]:.1f}', ha='center', va='center', fontsize=6)
    plt.colorbar(g, label='Korelasi Pearson'); plt.tight_layout(); plt.savefig('hasil/korelasi_kovariat.png', dpi=150); plt.show()

    AMBANG_R = 0.8
    pasangan = [(a, b, r_pix.loc[a, b]) for i, a in enumerate(numerik) for b in numerik[i + 1:] if abs(r_pix.loc[a, b]) >= AMBANG_R]
    pd.DataFrame(pasangan, columns=['Kovariat 1', 'Kovariat 2', 'r Pearson']).round(2)
    """),
    md("""
    ## B3. Kovariat kategorik

    Bentuklahan dan penggunaan lahan adalah kategori, bukan angka. Kode 1 sampai 6 pada `kat_bentuklahan` hanyalah nama, sehingga Dataran Koluvial (6) tidak "lebih besar" daripada Interfluve (1). Ada dua cara memasukkannya ke model:

    1. **One-hot** (*one-hot encoding*), yaitu setiap kelas kategori menjadi kolom 0/1 tersendiri. Cara ini diperlukan oleh *random forest* di scikit-learn.
    2. **Langsung sebagai kategori** (*native categorical feature handling*), yaitu kolom berisi nama kelas dan model mengolahnya sendiri. Inilah keunggulan CatBoost. Kategori dengan sedikit nilai dikodekan *one-hot* di dalam model (parameter `one_hot_max_size`), sedangkan kategori dengan banyak nilai, misalnya kode blok kebun, diubah menjadi statistik sasaran berurutan (*ordered target statistics*) yang dirancang agar nilai sasaran tidak bocor ke dalam model (Prokhorenkova et al., 2018).

    Sel berikut menyiapkan kedua bentuk tabel dan memeriksa sebaran titik per kategori.
    """),
    kode("""
    LABEL = {'kat_bentuklahan': {1: 'Interfluve', 2: 'Lereng Atas', 3: 'Lereng Tengah', 4: 'Lereng Bawah', 5: 'Lereng Kaki Koluvial', 6: 'Dataran Koluvial'},
             'kat_penggunaan_lahan': {1: 'Agroforestri', 2: 'Tegalan', 3: 'Sawah', 4: 'Permukiman'}}
    KAT = list(LABEL)

    def siapkan_X(df, kolom):
        \"\"\"Tabel prediktor untuk CatBoost: kovariat numerik apa adanya, kategori sebagai nama kelas.\"\"\"
        X = df[kolom].copy()
        for k in kolom:
            if k in KAT:
                X[k] = df[k].astype(int).map(LABEL[k])
        return X

    def satu_panas(X):
        \"\"\"Tabel prediktor untuk random forest: setiap kelas kategori menjadi kolom 0/1.\"\"\"
        X = X.copy()
        for k in [c for c in X.columns if c in KAT]:
            for nilai in LABEL[k].values():
                X[f'{k}={nilai}'] = (X[k] == nilai).astype(float)
            X = X.drop(columns=k)
        return X

    semua = numerik + KAT
    X_semua = siapkan_X(tabel, semua)
    print('Tabel CatBoost:', X_semua.shape, '| tabel random forest (one-hot):', satu_panas(X_semua).shape)
    print('Titik per penggunaan lahan:', X_semua['kat_penggunaan_lahan'].value_counts().to_dict())
    pd.crosstab(X_semua['kat_bentuklahan'], titik['kode'].rename('kelas material'), margins=True, margins_name='Jumlah')
    """),
    md("""
    # Bagian C. Pembangunan model DSM

    ## C1. Skema validasi

    Tiga skema validasi silang (*cross-validation*) dibandingkan:

    1. **Acak** (*stratified random k-fold cross-validation*), yaitu titik dibagi acak ke dalam lima lipatan (*fold*) dengan jumlah per kelas yang seimbang.
    2. **Blok spasial** (*spatial block cross-validation*), yaitu wilayah dibagi menjadi blok persegi 400 m dan setiap blok utuh masuk ke satu lipatan. Titik uji tidak memiliki tetangga dekat di data latih, tetapi kelas yang sama masih terwakili di blok lain.
    3. **Zona** (*leave-cluster-out cross-validation*), yaitu titik dikelompokkan menjadi lima zona besar dengan *k-means*. Skema ini meniru penerapan model ke wilayah yang benar-benar baru, misalnya kebun tetangga.

    Rujukan konsepnya ada pada Modul 8, Gambar 8.2.
    """),
    kode("""
    SISI_BLOK = 400
    blok = (np.floor((titik['x'].values - batas_grid.left) / SISI_BLOK).astype(int) * 100
            + np.floor((titik['y'].values - batas_grid.bottom) / SISI_BLOK).astype(int))
    zona = KMeans(n_clusters=5, n_init=10, random_state=0).fit_predict(titik[['x', 'y']])
    iris = {'Acak': list(StratifiedKFold(5, shuffle=True, random_state=0).split(tabel, y)),
            'Blok spasial': list(GroupKFold(5).split(tabel, y, groups=blok)),
            'Zona': list(GroupKFold(5).split(tabel, y, groups=zona))}

    fig, ax = plt.subplots(1, 3, figsize=(9, 5))
    latar = np.where(dalam, kubus[nama_kov.index('lereng')], np.nan)
    luasan = [batas_grid.left, batas_grid.right, batas_grid.bottom, batas_grid.top]
    for a, (skema, lipatan) in zip(ax, iris.items()):
        nomor = np.zeros(len(y), int)
        for i, (_, uji) in enumerate(lipatan):
            nomor[uji] = i
        a.imshow(latar, extent=luasan, cmap='Greys'); a.scatter(titik.x, titik.y, c=nomor, cmap='tab10', vmin=0, vmax=9, s=12, edgecolor='k', lw=.3)
        a.set_title(skema); a.axis('off')
        hilang = [sorted(set(KELAS.index) - set(y[latih])) for latih, _ in lipatan]
        print(f'{skema:13s} titik uji per lipatan {[len(u) for _, u in lipatan]} | kelas yang tidak ada di data latih: {hilang}')
    plt.suptitle('Lipatan validasi (warna = nomor lipatan)'); plt.tight_layout(); plt.savefig('hasil/skema_validasi.png', dpi=150); plt.show()
    """),
    md("""
    ## C2. Membandingkan model dengan pembanding sederhana

    Model harus dibandingkan dengan sesuatu. Ada dua pembanding sederhana (*baseline*):

    1. **Kelas terbanyak** (*majority class*), yaitu selalu menebak kelas yang paling banyak di data latih.
    2. **Kelas terbanyak per bentuklahan**, yaitu setiap bentuklahan diberi satu kelas material, seperti satuan pada peta konvensional.

    Setelah itu, *random forest* (dengan *one-hot*) dan CatBoost dilatih dengan ke-16 kovariat. Jika model yang rumit tidak mengalahkan pembanding sederhana, kerumitan itu belum memberi manfaat.
    """),
    kode("""
    class KelasTerbanyak:
        def fit(self, X, y):
            self.kelas = pd.Series(y).mode()[0]; return self
        def predict(self, X):
            return np.full(len(X), self.kelas)

    class KelasPerBentuklahan:
        \"\"\"Satu kelas material untuk setiap bentuklahan, seperti satuan pada peta konvensional.\"\"\"
        def fit(self, X, y):
            s = pd.Series(y, index=X.index)
            self.umum = s.mode()[0]
            self.peta = s.groupby(X['kat_bentuklahan']).agg(lambda v: v.mode()[0]).to_dict()
            return self
        def predict(self, X):
            return X['kat_bentuklahan'].map(self.peta).fillna(self.umum).astype(int).values

    class RFSatuPanas:
        \"\"\"Random forest; kategori diubah menjadi one-hot lebih dulu.\"\"\"
        def fit(self, X, y):
            self.m = RandomForestClassifier(n_estimators=500, random_state=0, n_jobs=-1).fit(satu_panas(X), y)
            self.classes_ = self.m.classes_; return self
        def predict(self, X):
            return self.m.predict(satu_panas(X))
        def predict_proba(self, X):
            return self.m.predict_proba(satu_panas(X))

    class CatBoostKategori:
        \"\"\"CatBoost yang membaca kolom kategori secara langsung.\"\"\"
        def __init__(self, **atur):
            self.atur = atur
        def fit(self, X, y):
            self.m = catboost_baru(**self.atur).fit(X, y, cat_features=[k for k in X.columns if k in KAT])
            self.classes_ = self.m.classes_; return self
        def predict(self, X):
            return self.m.predict(X).ravel()
        def predict_proba(self, X):
            return self.m.predict_proba(X)

    def validasi(buat_model, kolom, skema):
        \"\"\"Validasi silang: prediksi dan peluang setiap titik saat lipatannya disisihkan, beserta model tiap lipatan.\"\"\"
        X = siapkan_X(tabel, kolom)
        p, peluang, model = np.zeros(len(y), int), np.zeros((len(y), len(KELAS))), []
        for latih, uji in iris[skema]:
            m = buat_model().fit(X.iloc[latih], y[latih])
            p[uji] = m.predict(X.iloc[uji])
            if hasattr(m, 'predict_proba'):
                peluang[np.ix_(uji, np.asarray(m.classes_) - 1)] = m.predict_proba(X.iloc[uji])
            model.append(m)
        return p, peluang, model

    MODEL = {'Kelas terbanyak': KelasTerbanyak, 'Kelas terbanyak per bentuklahan': KelasPerBentuklahan,
             'Random forest (one-hot)': RFSatuPanas, 'CatBoost': CatBoostKategori}
    hasil_cv, baris = {}, []
    for nama, buat in MODEL.items():
        for skema in iris:
            hasil_cv[(nama, skema)] = validasi(buat, semua, skema)
            baris.append({'Model': nama, 'Validasi': skema, **ukuran(y, hasil_cv[(nama, skema)][0])})
    metrik = pd.DataFrame(baris).round(2)
    metrik.to_csv('hasil/metrik_validasi_material.csv', index=False)
    metrik.set_index(['Model', 'Validasi']).loc[list(MODEL)]
    """),
    md("""
    **Cara membaca.** Akurasi 0,14 setara dengan menebak sembarang. Karena jumlah titik per kelas sama, kappa di sini hanyalah skala lain dari akurasi, yaitu (akurasi − 1/7) / (1 − 1/7), dan recall makro persis sama dengan akurasi. Presisi makro dapat berbeda dari keduanya, karena turun bila model sering menebak sebuah kelas yang sebenarnya bukan kelas itu. Bandingkan ketiga skema: selisih antara validasi acak dan blok spasial menunjukkan seberapa besar akurasi acak terbantu oleh titik tetangga, sedangkan skema zona menunjukkan apa yang terjadi bila model dipakai di wilayah yang belum pernah dilihatnya.

    **Apakah cara CatBoost mengodekan kategori (*categorical encoding*) berpengaruh?** Notebook ini memakai `one_hot_max_size=10`, sehingga kedua kovariat kategorik (6 dan 4 kelas) dikodekan *one-hot* di dalam CatBoost. Dengan nilai bawaannya, yaitu 2, CatBoost memakai statistik sasaran berurutan untuk keduanya. Sel berikut membandingkan kedua cara pada validasi blok spasial.
    """),
    kode("""
    for nama, atur in [('one-hot di dalam CatBoost (one_hot_max_size=10)', {}), ('statistik sasaran (one_hot_max_size=2, bawaan)', {'one_hot_max_size': 2})]:
        mulai = time.time()
        p = validasi(lambda: CatBoostKategori(**atur), semua, 'Blok spasial')[0]
        print(f'{nama:50s} akurasi {accuracy_score(y, p):.2f} | F1 makro {f1_score(y, p, average="macro"):.2f} | {time.time() - mulai:.0f} detik')
    """),
    md("""
    ## C3. Kelas mana yang tertukar?

    Akurasi keseluruhan menyembunyikan perbedaan antarkelas. Matriks kebingungan (*confusion matrix*, dalam penginderaan jauh juga disebut *error matrix*) menampilkan, untuk setiap kelas sebenarnya (baris), ke kelas mana titik-titiknya ditebak (kolom). Dari matriks itu dihitung tiga ukuran per kelas:

    1. **Recall** (*recall* atau *sensitivity*), yaitu proporsi titik suatu kelas yang ditebak benar. Dalam penilaian ketelitian peta penginderaan jauh, ukuran ini disebut *producer's accuracy*, karena menyatakan seberapa lengkap pembuat peta menangkap kelas itu.
    2. **Presisi** (*precision*), yaitu proporsi tebakan suatu kelas yang memang benar. Ukuran ini disebut *user's accuracy*, karena menyatakan seberapa besar peluang pengguna peta menemukan kelas itu di lapangan bila peta menyebutkannya.
    3. **F1** (*F1-score*), yaitu rata-rata harmonik (*harmonic mean*) presisi dan recall.

    Hasil di bawah berasal dari CatBoost dengan 16 kovariat pada validasi blok spasial.
    """),
    kode("""
    def gambar_matriks(mk, judul, berkas):
        fig, ax = plt.subplots(figsize=(4.8, 4.2))
        ax.imshow(mk / mk.sum(axis=1, keepdims=True), cmap='Blues', vmin=0, vmax=1)
        for i in range(len(KELAS)):
            for j in range(len(KELAS)):
                ax.text(j, i, mk[i, j], ha='center', va='center', fontsize=8, color='white' if mk[i, j] > 15 else 'black')
        ax.set_xticks(range(len(KELAS)), KELAS.index); ax.set_yticks(range(len(KELAS)), KELAS.index)
        ax.set(xlabel='Kelas tebakan', ylabel='Kelas sebenarnya', title=judul)
        plt.tight_layout(); plt.savefig(berkas, dpi=150); plt.show()

    def laporan_per_kelas(y, p):
        return pd.DataFrame({'Material': KELAS, 'Titik': np.bincount(y, minlength=len(KELAS) + 1)[1:],
                             "Recall (producer's accuracy)": recall_score(y, p, labels=KELAS.index, average=None, zero_division=0),
                             "Presisi (user's accuracy)": precision_score(y, p, labels=KELAS.index, average=None, zero_division=0),
                             'F1': f1_score(y, p, labels=KELAS.index, average=None, zero_division=0)}, index=KELAS.index).round(2)

    p_cb = hasil_cv[('CatBoost', 'Blok spasial')][0]
    gambar_matriks(confusion_matrix(y, p_cb, labels=KELAS.index), 'CatBoost, 16 kovariat, validasi blok spasial', 'hasil/matriks_kebingungan.png')
    laporan_per_kelas(y, p_cb)
    """),
    md("""
    ## C4. Memilih kovariat: tingkat kepentingan dan korelasi Pearson

    Kovariat untuk model akhir dipilih dengan dua informasi:

    1. **Tingkat kepentingan** (*variable importance*), dihitung dengan permutasi (*permutation importance*): nilai satu kovariat di data uji diacak, lalu diukur seberapa besar akurasi turun. Semakin besar penurunannya, semakin penting kovariat itu bagi model. Permutasi dilakukan pada lipatan blok spasial, yaitu pada data yang tidak dipakai melatih model, karena kepentingan yang dihitung dari data latih dapat memberi nilai tinggi pada kovariat yang hanya membantu model menghafal (Meyer et al., 2019).
    2. **Korelasi Pearson** dari Bagian B2, untuk menemukan kovariat yang saling menggantikan.

    Sebagai perbandingan, ditampilkan pula kepentingan bawaan CatBoost (*built-in feature importance*, PredictionValuesChange), yang dihitung dari data latih.
    """),
    kode("""
    def kepentingan_permutasi(model, X, y_uji, ulang=10, seed=0):
        \"\"\"Penurunan akurasi rata-rata saat satu kovariat diacak.\"\"\"
        rng = np.random.default_rng(seed)
        dasar = accuracy_score(y_uji, model.predict(X))
        turun = {}
        for k in X.columns:
            nilai = []
            for _ in range(ulang):
                Xp = X.copy()
                Xp[k] = rng.permutation(Xp[k].values)
                nilai.append(dasar - accuracy_score(y_uji, model.predict(Xp)))
            turun[k] = np.mean(nilai)
        return pd.Series(turun)

    model_cb = hasil_cv[('CatBoost', 'Blok spasial')][2]
    per_lipatan = pd.DataFrame([kepentingan_permutasi(m, X_semua.iloc[uji], y[uji]) for m, (_, uji) in zip(model_cb, iris['Blok spasial'])])
    bawaan = pd.DataFrame([m.m.get_feature_importance() for m in model_cb], columns=semua).mean()
    kepentingan = pd.DataFrame({'Permutasi': per_lipatan.mean(), 'Simpangan antarlipatan': per_lipatan.std(),
                                'Bawaan CatBoost (%)': bawaan}).sort_values('Permutasi', ascending=False)

    fig, ax = plt.subplots(figsize=(6, 4.6))
    urut = kepentingan.iloc[::-1]
    ax.barh(urut.index, urut['Permutasi'], xerr=urut['Simpangan antarlipatan'], color=['#b2182b' if v <= 0 else '#2166ac' for v in urut['Permutasi']], error_kw={'lw': .6})
    ax.axvline(0, color='k', lw=.6); ax.set(xlabel='Penurunan akurasi saat kovariat diacak', title='Kepentingan kovariat (validasi blok spasial)')
    plt.tight_layout(); plt.savefig('hasil/kepentingan_kovariat.png', dpi=150); plt.show()
    kepentingan.round(3)
    """),
    md("""
    Aturan pemilihan:

    1. Urutkan kovariat menurut kepentingan permutasi, dari yang terbesar.
    2. Buang kovariat yang kepentingannya ≤ 0, karena mengacaknya tidak menurunkan akurasi pada data yang belum pernah dilihat model.
    3. Telusuri dari atas. Kovariat numerik yang berkorelasi |r| ≥ 0,8 dengan kovariat yang sudah terpilih dibuang, sehingga dari setiap pasangan yang mirip hanya yang lebih penting yang dipertahankan.

    Kovariat kategorik hanya diperiksa dengan aturan 2.
    """),
    kode("""
    def pilih_kovariat(kepentingan_permutasi, r, ambang=AMBANG_R):
        terpilih, keputusan = [], {}
        for k, v in kepentingan_permutasi.sort_values(ascending=False).items():
            if v <= 0:
                keputusan[k] = f'dibuang: kepentingan <= 0 ({v:.4f})'
                continue
            lawan = [t for t in terpilih if k in r.index and t in r.index and abs(r.loc[k, t]) >= ambang]
            if lawan:
                keputusan[k] = f'dibuang: r = {r.loc[k, lawan[0]]:.2f} dengan {lawan[0]} yang lebih penting'
                continue
            terpilih.append(k)
            keputusan[k] = 'dipakai'
        return terpilih, keputusan

    terpilih, keputusan = pilih_kovariat(kepentingan['Permutasi'], r_pix)
    hasil_terpilih = {skema: validasi(CatBoostKategori, terpilih, skema) for skema in ['Acak', 'Blok spasial']}
    banding = []
    for label, kolom, sumber in [('Semua kovariat', semua, {s: hasil_cv[('CatBoost', s)] for s in hasil_terpilih}), ('Kovariat terpilih', terpilih, hasil_terpilih)]:
        for skema in hasil_terpilih:
            banding.append({'Kovariat': label, 'Jumlah': len(kolom), 'Validasi': skema, **ukuran(y, sumber[skema][0])})
    print('Kovariat terpilih:', terpilih)
    display(pd.Series(keputusan, name='Keputusan').to_frame())
    pd.DataFrame(banding).round(2)
    """),
    md("""
    **Catatan kejujuran.** Kovariat di atas dipilih memakai lipatan yang sama dengan yang dipakai untuk menilainya, sehingga angka "Kovariat terpilih" sedikit optimistis. Cara yang ketat adalah memilih kovariat di dalam setiap lipatan, hanya dari data latihnya (*nested cross-validation*). Sel berikut melakukannya. Perhatikan juga apakah kovariat yang terpilih sama dari satu lipatan ke lipatan lain.
    """),
    kode("""
    p_nested, pilihan_per_lipatan = np.zeros(len(y), int), []
    for latih, uji in iris['Blok spasial']:
        imp = []
        for a, b in GroupKFold(4).split(latih, y[latih], groups=blok[latih]):
            m = CatBoostKategori().fit(X_semua.iloc[latih[a]], y[latih[a]])
            imp.append(kepentingan_permutasi(m, X_semua.iloc[latih[b]], y[latih[b]], ulang=5))
        pilih, _ = pilih_kovariat(pd.DataFrame(imp).mean(), r_pix)
        pilihan_per_lipatan.append(pilih)
        X_pilih = siapkan_X(tabel, pilih)
        p_nested[uji] = CatBoostKategori().fit(X_pilih.iloc[latih], y[latih]).predict(X_pilih.iloc[uji])
    print('Nested, validasi blok spasial:', {k: round(v, 2) for k, v in ukuran(y, p_nested).items()})
    for i, s in enumerate(pilihan_per_lipatan, 1):
        print(f'Lipatan {i}: {len(s)} kovariat, {s}')
    """),
    md("""
    ## C5. Bagaimana jika datanya tidak seimbang (*imbalanced data*)?

    Data latihan ini sengaja seimbang: setiap kelas memiliki 30 titik. Di lapangan keadaan itu jarang terjadi. Bila titik disebar acak di seluruh kebun, jumlah titik setiap kelas kira-kira sebanding dengan luasnya, sehingga kelas yang sempit hanya memperoleh sedikit titik. Model lalu cenderung mengabaikan kelas tersebut, karena salah menebaknya hampir tidak menurunkan akurasi keseluruhan.

    Sel berikut menirukan keadaan itu. Pada setiap lipatan blok spasial, titik latih dikurangi sehingga jumlahnya sebanding dengan luas kelas pada peta acuan, sedangkan data uji tidak diubah. Tiga cara dibandingkan:

    1. **Tanpa penanganan**.
    2. **Bobot kelas** (*class weighting*), yaitu kesalahan pada kelas yang sedikit titiknya diberi bobot lebih besar. CatBoost menyediakannya lewat `auto_class_weights='Balanced'`: bobot setiap kelas sama dengan jumlah titik kelas terbanyak dibagi jumlah titik kelas itu.
    3. **SMOTE-NC** (*Synthetic Minority Over-sampling Technique–Nominal Continuous*), yaitu titik sintetis (*synthetic samples*) dibuat untuk kelas yang sedikit dengan menginterpolasi antara sebuah titik dan tetangganya di ruang kovariat (Chawla et al., 2002). Akhiran NC berarti kovariat kategorik ikut ditangani: titik sintetis mengambil kategori yang paling sering di antara tetangganya.

    Penyeimbangan (*resampling*) **hanya** dilakukan pada data latih setiap lipatan. Jika titik sintetis dibuat sebelum data dibagi, informasi dari titik uji ikut masuk ke data latih (*data leakage*) dan akurasinya menjadi semu. Untuk sasaran kontinu, misalnya nilai C-organik tinggi yang jarang dijumpai, padanannya adalah SMOGN (*SMOTE for regression with Gaussian noise*; Branco et al., 2017).
    """),
    kode("""
    porsi = luas_ha / luas_ha.max()

    def kurangi_sebanding_luas(idx, seed):
        \"\"\"Ambil sebagian titik dari idx sehingga jumlah per kelas sebanding dengan luas kelas.\"\"\"
        rng = np.random.default_rng(seed)
        simpan = []
        for k in KELAS.index:
            anggota = idx[y[idx] == k]
            n = max(1, int(round(len(anggota) * porsi[k])))
            simpan.extend(rng.choice(anggota, n, replace=False))
        return np.sort(simpan)

    def smote_nc(X, yy):
        \"\"\"Tambah titik sintetis sampai setiap kelas sama banyak dengan kelas terbanyak.\"\"\"
        jumlah = pd.Series(yy).value_counts()
        sasaran = {k: jumlah.max() for k, n in jumlah.items() if 2 <= n < jumlah.max()}   # kelas dengan 1 titik tidak dapat diinterpolasi
        if not sasaran:
            return X, yy
        k_tetangga = min(5, min(jumlah[k] for k in sasaran) - 1)
        kolom_kat = [i for i, c in enumerate(X.columns) if c in KAT]
        if kolom_kat:
            alat = SMOTENC(categorical_features=kolom_kat, sampling_strategy=sasaran, k_neighbors=k_tetangga, random_state=0)
        else:
            alat = SMOTE(sampling_strategy=sasaran, k_neighbors=k_tetangga, random_state=0)
        return alat.fit_resample(X, yy)

    X_t = siapkan_X(tabel, terpilih)
    CARA = ['Tanpa penanganan', 'Bobot kelas', 'SMOTE-NC']
    rekap, recall_kelas = [], []
    for ulang in range(3):
        p = {c: np.zeros(len(y), int) for c in CARA}
        for latih, uji in iris['Blok spasial']:
            s = kurangi_sebanding_luas(latih, ulang)
            p['Tanpa penanganan'][uji] = CatBoostKategori().fit(X_t.iloc[s], y[s]).predict(X_t.iloc[uji])
            p['Bobot kelas'][uji] = CatBoostKategori(auto_class_weights='Balanced').fit(X_t.iloc[s], y[s]).predict(X_t.iloc[uji])
            Xs, ys = smote_nc(X_t.iloc[s].reset_index(drop=True), y[s])
            p['SMOTE-NC'][uji] = CatBoostKategori().fit(Xs, ys).predict(X_t.iloc[uji])
        for c in CARA:
            rekap.append({'Cara': c, **ukuran(y, p[c])})
            recall_kelas.append(pd.Series(recall_score(y, p[c], labels=KELAS.index, average=None), index=KELAS.index, name=c))
    contoh = kurangi_sebanding_luas(iris['Blok spasial'][0][0], 0)
    print('Contoh jumlah titik latih per kelas setelah dikurangi:', pd.Series(y[contoh]).value_counts().sort_index().to_dict())
    recall_rata = pd.concat(recall_kelas, axis=1).T.groupby(level=0).mean().loc[CARA]
    fig, ax = plt.subplots(figsize=(6.4, 3))
    recall_rata.T.plot.bar(ax=ax, color=['#bdbdbd', '#2166ac', '#b2182b'], width=.8)
    ax.set(xlabel='Kelas material', ylabel='Recall', title='Recall per kelas, rata-rata tiga ulangan'); ax.legend(fontsize=7)
    plt.xticks(rotation=0); plt.tight_layout(); plt.savefig('hasil/recall_data_tidak_seimbang.png', dpi=150); plt.show()
    display(recall_rata.round(2))
    pd.DataFrame(rekap).groupby('Cara').mean().loc[CARA].round(2)
    """),
    md("""
    Penyeimbangan juga mengubah **luas** setiap kelas pada peta. Sel berikut melatih model dengan seluruh titik yang dikurangi sebanding luas, lalu membandingkan proporsi kelas pada peta hasilnya dengan peta acuan. Baris pertama memakai sampel seimbang 30 titik per kelas seperti pada model akhir.
    """),
    kode("""
    X_piksel_t = siapkan_X(piksel, terpilih)
    s = kurangi_sebanding_luas(np.arange(len(y)), 0)
    Xs, ys = smote_nc(X_t.iloc[s].reset_index(drop=True), y[s])
    pilihan = {'Sampel seimbang (30 per kelas)': CatBoostKategori().fit(X_t, y),
               'Sebanding luas, tanpa penanganan': CatBoostKategori().fit(X_t.iloc[s], y[s]),
               'Sebanding luas, bobot kelas': CatBoostKategori(auto_class_weights='Balanced').fit(X_t.iloc[s], y[s]),
               'Sebanding luas, SMOTE-NC': CatBoostKategori().fit(Xs, ys)}
    proporsi = {'Peta acuan': luas_ha / luas_ha.sum()}
    for nama, m in pilihan.items():
        proporsi[nama] = pd.Series(m.predict(X_piksel_t)).value_counts(normalize=True).reindex(KELAS.index, fill_value=0)
    (100 * pd.DataFrame(proporsi).T).round(1)
    """),
    md("""
    ## C6. Model akhir dan peta tutupan material

    Model akhir adalah CatBoost dengan kovariat terpilih. Ketelitiannya tidak dapat dinilai dari titik yang dipakai untuk melatihnya, sehingga yang dilaporkan adalah hasil validasi blok spasial dengan kovariat dan pengaturan yang sama (Bagian C4). Inilah penilaian ketelitian yang lazim menyertai sebuah peta kelas: matriks kebingungan, *producer's accuracy* dan *user's accuracy* setiap kelas, serta ukuran keseluruhannya.
    """),
    kode("""
    p_akhir = hasil_terpilih['Blok spasial'][0]
    gambar_matriks(confusion_matrix(y, p_akhir, labels=KELAS.index), 'Model akhir, validasi blok spasial', 'hasil/matriks_kebingungan_model_akhir.png')
    laporan_akhir = laporan_per_kelas(y, p_akhir)
    laporan_akhir.to_csv('hasil/laporan_per_kelas_model_akhir.csv')
    print('Ukuran keseluruhan:', {k: round(v, 2) for k, v in ukuran(y, p_akhir).items()})
    laporan_akhir
    """),
    md("""
    Peta dibuat dengan melatih model yang sama pada seluruh 210 titik. Setiap piksel memperoleh kelas dengan peluang tertinggi beserta nilai peluang itu.
    """),
    kode("""
    model_akhir = pilihan['Sampel seimbang (30 per kelas)']
    P = model_akhir.predict_proba(X_piksel_t)            # peluang setiap kelas untuk setiap piksel
    kelas_piksel = np.asarray(model_akhir.classes_)[P.argmax(axis=1)]
    peluang_maks = P.max(axis=1)
    entropi = -(P * np.log(np.clip(P, 1e-12, 1))).sum(axis=1) / np.log(P.shape[1])

    def ke_peta(nilai):
        peta = np.full((tinggi, lebar), np.nan, dtype='float32')
        peta[dalam] = nilai
        return peta

    def simpan(peta, nama, kelas=False):
        \"\"\"Simpan GeoTIFF. Peta kelas disimpan sebagai bilangan bulat dengan nodata 0.\"\"\"
        isi = np.nan_to_num(peta, nan=0 if kelas else -9999).astype('uint8' if kelas else 'float32')
        with rasterio.open(f'hasil/{nama}.tif', 'w', driver='GTiff', height=tinggi, width=lebar, count=1, dtype=isi.dtype,
                           crs=crs, transform=transform, nodata=0 if kelas else -9999, compress='deflate') as d:
            d.write(isi, 1)

    peta_kelas = ke_peta(kelas_piksel)
    simpan(peta_kelas, 'prediksi_material', kelas=True)
    # gaya QGIS peta acuan dipakai ulang, agar peta prediksi tampil dengan warna dan nama kelas yang sama
    shutil.copy('material_acuan_10m.qml', 'hasil/prediksi_material.qml')
    simpan(ke_peta(peluang_maks), 'peluang_maks_material')
    simpan(ke_peta(entropi), 'entropi_material')

    fig, ax = plt.subplots(1, 2, figsize=(10, 5.6))
    ax[0].imshow(np.where(dalam, acuan, np.nan), cmap=PETA_WARNA, vmin=.5, vmax=7.5, interpolation='nearest'); ax[0].set_title('Peta acuan (Malik, 2017)')
    ax[1].imshow(peta_kelas, cmap=PETA_WARNA, vmin=.5, vmax=7.5, interpolation='nearest'); ax[1].set_title('Prediksi CatBoost')
    for a in ax: a.axis('off')
    fig.legend(handles=[Patch(color=WARNA[k], label=textwrap.fill(f'{k}. {v}', 34)) for k, v in KELAS.items()], loc='center right', fontsize=7, labelspacing=1)
    plt.tight_layout(rect=(0, 0, .7, 1)); plt.savefig('hasil/peta_prediksi_material.png', dpi=150); plt.show()

    sama = kelas_piksel == acuan[dalam]
    print(f'Kesesuaian dengan peta acuan: {100 * sama.mean():.1f}% piksel')
    pd.DataFrame({'Material': KELAS, 'Acuan (ha)': luas_ha.round(1),
                  'Prediksi (ha)': (pd.Series(kelas_piksel).value_counts().reindex(KELAS.index, fill_value=0) * 100 / 1e4).round(1),
                  'Kesesuaian per kelas acuan (%)': [round(100 * sama[acuan[dalam] == k].mean(), 1) for k in KELAS.index]})
    """),
    md("""
    Bandingkan luas prediksi dengan luas acuan. Model akhir dilatih dengan jumlah titik yang sama untuk setiap kelas, sehingga model menganggap ketujuh kelas sama umumnya. Akibatnya, kelas yang sempit cenderung diprediksi terlalu luas dan kelas yang luas terlalu sempit. Inilah sisi lain dari persoalan pada Bagian C5.

    ## C7. Seberapa yakin model, dan apakah keyakinannya dapat dipercaya?

    Untuk sasaran kategorik, ketidakpastian (*uncertainty*) dinyatakan dengan peluang kelas (*class probability*). Peluang tertinggi yang rendah berarti model ragu di antara beberapa kelas. Entropi (*entropy*) meringkas sebaran peluang ke semua kelas: 0 berarti model yakin penuh pada satu kelas, sedangkan 1 berarti semua kelas sama mungkin. Peluang itu baru berguna bila jujur atau terkalibrasi (*well-calibrated*), yaitu bila titik yang diprediksi dengan peluang tinggi memang lebih sering benar. Sel berikut memeriksanya dengan prediksi validasi blok spasial.
    """),
    kode("""
    p_t, peluang_t, model_t = hasil_terpilih['Blok spasial']
    benar = p_t == y
    kelompok = pd.cut(peluang_t.max(axis=1), [0, .3, .5, .7, 1.0], include_lowest=True)
    keyakinan = pd.DataFrame({'Peluang tertinggi': kelompok, 'Benar': benar}).groupby('Peluang tertinggi', observed=False)['Benar']
    display(keyakinan.agg(['count', 'mean']).rename(columns={'count': 'Jumlah titik', 'mean': 'Proporsi benar'}).round(2))

    fig, ax = plt.subplots(1, 2, figsize=(7.4, 5))
    a = ax[0].imshow(ke_peta(peluang_maks), cmap='viridis', vmin=0, vmax=1); ax[0].set_title('Peluang kelas tertinggi'); plt.colorbar(a, ax=ax[0], shrink=.7)
    b = ax[1].imshow(ke_peta(entropi), cmap='magma_r', vmin=0, vmax=1); ax[1].set_title('Entropi (0 yakin, 1 ragu)'); plt.colorbar(b, ax=ax[1], shrink=.7)
    for x in ax: x.axis('off')
    plt.tight_layout(); plt.savefig('hasil/peta_peluang_entropi.png', dpi=150); plt.show()
    print(f'Rata-rata peluang tertinggi {peluang_maks.mean():.2f} | piksel dengan peluang >= 0,7: {100 * (peluang_maks >= .7).mean():.1f}%')
    """),
    md("""
    ## C8. Wilayah keberlakuan model (*area of applicability*)

    Indeks ketidakmiripan (*dissimilarity index*, DI) mengukur jarak setiap piksel ke titik latih terdekat dalam ruang kovariat. Mengikuti Meyer dan Pebesma (2021), setiap kovariat diberi bobot sesuai kepentingannya dari Bagian C4, sehingga kovariat yang tidak berpengaruh tidak ikut menentukan. Di sini hanya kovariat numerik yang dipakai. Ambangnya diturunkan dari DI titik latih terhadap titik di lipatan blok lain. Ini penerapan sederhana untuk peragaan.
    """),
    kode("""
    num_t = [k for k in terpilih if k in numerik]
    bobot = kepentingan.loc[num_t, 'Permutasi'].clip(lower=0).values
    skala = StandardScaler().fit(tabel[num_t])
    Zt, Zp = skala.transform(tabel[num_t]) * bobot, skala.transform(piksel[num_t]) * bobot
    d_rata = NearestNeighbors(n_neighbors=len(Zt)).fit(Zt).kneighbors(Zt)[0][:, 1:].mean()
    lipatan = np.zeros(len(y), int)
    for i, (_, uji) in enumerate(iris['Blok spasial']):
        lipatan[uji] = i
    di_titik = np.array([np.linalg.norm(Zt[lipatan != lipatan[i]] - Zt[i], axis=1).min() for i in range(len(Zt))]) / d_rata
    ambang = np.percentile(di_titik, 75) + 1.5 * (np.percentile(di_titik, 75) - np.percentile(di_titik, 25))
    di_piksel = NearestNeighbors(n_neighbors=1).fit(Zt).kneighbors(Zp)[0].ravel() / d_rata
    aoa = (di_piksel <= ambang).astype('float32')
    simpan(ke_peta(di_piksel), 'di_material')
    simpan(ke_peta(aoa), 'aoa_material')
    print(f'Ambang DI {ambang:.2f} | {100 * aoa.mean():.1f}% piksel berada di dalam wilayah keberlakuan')
    plt.figure(figsize=(3.8, 5)); plt.imshow(ke_peta(aoa), cmap='RdYlGn', vmin=0, vmax=1); plt.axis('off'); plt.title('Hijau: di dalam AOA')
    plt.tight_layout(); plt.savefig('hasil/aoa.png', dpi=150); plt.show()
    """),
    md("""
    ## C9. Di mana model salah?

    Peta kesesuaian (*agreement map*) membandingkan peta prediksi dengan peta acuan piksel demi piksel. Titik menunjukkan hasil validasi blok spasial, yaitu benar atau salahnya tebakan saat blok titik itu disisihkan. Perhatikan apakah kesalahan mengumpul di kelas tertentu, di dekat batas kelas, atau di bagian wilayah tertentu.
    """),
    kode("""
    kesesuaian = ke_peta(np.where(sama, 1, 2))
    simpan(kesesuaian, 'kesesuaian_material', kelas=True)
    fig, ax = plt.subplots(figsize=(4.6, 6.4))
    ax.imshow(kesesuaian, extent=luasan, cmap=ListedColormap(['#a6d96a', '#fdae61']), vmin=.5, vmax=2.5, interpolation='nearest')
    ax.scatter(titik.x[benar], titik.y[benar], s=10, c='#1a9850', edgecolor='k', lw=.3, label='Titik benar (validasi spasial)')
    ax.scatter(titik.x[~benar], titik.y[~benar], s=14, c='#d73027', marker='x', lw=1, label='Titik salah')
    fig.legend(handles=[Patch(color='#a6d96a', label='Prediksi = acuan'), Patch(color='#fdae61', label='Prediksi berbeda')] + ax.get_legend_handles_labels()[0], fontsize=7, loc='lower center', ncol=2)
    ax.axis('off'); ax.set_title('Kesesuaian prediksi dengan peta acuan')
    plt.tight_layout(rect=(0, .08, 1, 1)); plt.savefig('hasil/kesesuaian_dan_kesalahan.png', dpi=150); plt.show()
    pd.DataFrame({'Material': KELAS, 'Titik salah (validasi spasial)': pd.Series(y[~benar]).value_counts().reindex(KELAS.index, fill_value=0)})
    """),
    md("""
    ## Yang dibawa ke QGIS dan ke presentasi

    Folder `hasil/` kini berisi peta kelas (`prediksi_material.tif`), peta peluang dan entropi, DI, AOA, peta kesesuaian, tabel metrik, dan gambar. Buka GeoTIFF-nya di QGIS (Modul Praktik 5, tahap terakhir), tumpangkan dengan peta SMU dari Praktik 2, lalu siapkan jawaban untuk pertanyaan berikut:

    1. Seberapa baik CatBoost dibandingkan pembanding sederhananya, dan pada skema validasi yang mana?
    2. Kelas mana yang paling sering tertukar, dan di mana peta ini paling tidak dapat dipercaya?
    3. Jika sampel di kebun tidak seimbang, cara penanganan mana yang dipilih, dan apa akibatnya pada luas setiap kelas di peta?
    """),
]


if __name__ == '__main__':
    pilih = sys.argv[1:] or ['3', '5']
    if '3' in pilih:
        tulis(os.path.join(DATA, 'praktik-3', 'Praktik_3_Spektrum_ke_Sifat_Tanah.ipynb'), P3)
    if '5' in pilih:
        tulis(os.path.join(DATA, 'praktik-5', 'Praktik_5_Machine_Learning_DSM.ipynb'), P5)
    print('Notebook ditulis:', pilih)
