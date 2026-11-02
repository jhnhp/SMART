"""Skrip pembuatan gambar tambahan untuk presentasi pelatihan.
1. M1-G07_keseimbangan-energi.png (Modul 1 Slide 4: Hukum Keseimbangan Energi Fluks)
2. M7-G05_skema-spektrometer-mandiri.png (Modul 7 Slide 15: Arsitektur Instrumen PSS Mandiri)
3. M8-G06_interval-kedalaman-globalsoilmap.png (Modul 8 Slide 12: Spline & 6 Interval GlobalSoilMap)
"""
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch

sys.path.append(os.path.join(os.path.dirname(__file__)))
import gaya
from gaya import WARNA, kanvas, kotak, nomor, panah, simpan

def g_m1_keseimbangan_energi():
    fig, ax = kanvas(10.5, 5.8, (0, 105), (0, 58))
    
    # Judul & Formula Utama
    kotak(ax, 3.0, 48.0, 99.0, 8.5, 
          "HUKUM KESEIMBANGAN ENERGI ELEKTROMAGNETIK DI PERMUKAAN BUMI\n"
          r"$E_I(\lambda) = E_R(\lambda) + E_A(\lambda) + E_T(\lambda)$  |  "
          r"$\rho(\lambda) + \alpha(\lambda) + \tau(\lambda) = 1$",
          isi=WARNA["biru_muda"], warna=WARNA["navy"], tebal=True, ukuran=9.5)
    
    # 3 Panel Objek
    lebar_panel = 31.0
    tinggi_panel = 44.0
    y_dasar = 2.0
    
    panel_info = [
        (4.0, "(a) Daun / Kanopi Vegetasi", WARNA["hijau"], 
         "• Reflektansi (ER) tinggi di NIR & Green\n"
         "• Absorbsi (EA) kuat di Red & Blue (klorofil)\n"
         "• Transmitansi (ET) tembus ke daun bawah"),
        (37.0, "(b) Permukaan Tanah Terbuka", WARNA["tanah"], 
         "• Reflektansi (ER) naik dari Visible ke SWIR\n"
         "• Absorbsi (EA) tinggi (pemanasan termal)\n"
         "• Transmitansi (ET) ~ 0 (tanah bersifat opak)"),
        (70.0, "(c) Badan Air Permukaan", WARNA["teal"], 
         "• Reflektansi (ER) rendah (~0 di inframerah)\n"
         "• Absorbsi (EA) sangat tinggi di IR\n"
         "• Transmitansi (ET) tembus di perairan jernih")
    ]
    
    for x0, judul, warna_aksen, poin in panel_info:
        # Kotak panel
        ax.add_patch(FancyBboxPatch((x0, y_dasar), lebar_panel, tinggi_panel,
                                   boxstyle="round,pad=0,rounding_size=0.8",
                                   fc=WARNA["latar"], ec=WARNA["abu_muda"], lw=1.0, zorder=1))
        # Header panel
        ax.add_patch(FancyBboxPatch((x0, y_dasar + 38.5), lebar_panel, 5.5,
                                   boxstyle="round,pad=0,rounding_size=0.8",
                                   fc=warna_aksen, ec="none", zorder=2))
        ax.text(x0 + lebar_panel / 2, y_dasar + 41.25, judul, ha="center", va="center",
                fontsize=8.5, fontweight="bold", color="white", zorder=3)
        
        # Gambar objek skematis
        cx = x0 + lebar_panel / 2
        
        # Matahari kecil di kiri atas panel
        ax.add_patch(Circle((x0 + 5.0, y_dasar + 33.0), 2.2, fc=WARNA["oranye"], ec="none", zorder=3))
        # Panah Incident EI
        panah(ax, x0 + 7.5, y_dasar + 31.0, cx, y_dasar + 20.0, warna=WARNA["oranye"], lw=2.0, skala=10)
        ax.text(cx - 5.5, y_dasar + 27.0, r"$E_I$", fontsize=9.0, fontweight="bold", color=WARNA["oranye"])
        
        if "(a)" in judul:
            # Daun elips hijau
            ax.add_patch(FancyBboxPatch((cx - 10.0, y_dasar + 17.0), 20.0, 4.0, boxstyle="round,pad=0.2",
                                       fc="#8FCB6B", ec=WARNA["hijau"], lw=1.2, zorder=3))
            ax.text(cx, y_dasar + 19.0, "Daun Hijau", ha="center", va="center", fontsize=8.0, color=WARNA["navy"], fontweight="bold", zorder=4)
            # Reflected ER ke sensor atas kanan
            panah(ax, cx, y_dasar + 20.0, x0 + lebar_panel - 5.0, y_dasar + 33.0, warna=WARNA["hijau"], lw=1.8, skala=10)
            ax.text(x0 + lebar_panel - 8.0, y_dasar + 28.0, r"$E_R$", fontsize=9.0, fontweight="bold", color=WARNA["hijau"])
            # Transmitted ET ke bawah
            panah(ax, cx, y_dasar + 17.0, cx, y_dasar + 8.5, warna="#4C9A2A", lw=1.5, putus=True, skala=10)
            ax.text(cx + 2.5, y_dasar + 12.0, r"$E_T$", fontsize=8.5, fontweight="bold", color="#4C9A2A")
            # Absorbed EA di dalam
            ax.text(cx - 10.0, y_dasar + 13.0, r"$E_A$ (Klorofil)", fontsize=7.5, color=WARNA["merah"], fontweight="bold")
        elif "(b)" in judul:
            # Lapisan tanah cokelat
            ax.add_patch(Rectangle((x0 + 3.0, y_dasar + 6.0), lebar_panel - 6.0, 14.0, fc="#D9B48F", ec=WARNA["tanah"], lw=1.2, zorder=3))
            ax.text(cx, y_dasar + 13.0, "Lapisan Tanah (0-2 mm)", ha="center", va="center", fontsize=8.0, color=WARNA["navy"], fontweight="bold", zorder=4)
            # Reflected ER
            panah(ax, cx, y_dasar + 20.0, x0 + lebar_panel - 5.0, y_dasar + 33.0, warna=WARNA["tanah"], lw=1.8, skala=10)
            ax.text(x0 + lebar_panel - 8.0, y_dasar + 28.0, r"$E_R$", fontsize=9.0, fontweight="bold", color=WARNA["tanah"])
            # Absorbed EA
            ax.text(cx, y_dasar + 9.0, r"$E_A$ (Panas Terakumulasi)", ha="center", va="center", fontsize=7.5, color=WARNA["merah"], fontweight="bold", zorder=4)
            # Transmitansi = 0
            ax.text(cx, y_dasar + 4.0, r"$E_T \approx 0$ (Opak)", ha="center", va="center", fontsize=7.5, color=WARNA["abu"], style="italic", zorder=4)
        else:
            # Lapisan air biru
            ax.add_patch(Rectangle((x0 + 3.0, y_dasar + 6.0), lebar_panel - 6.0, 14.0, fc="#DCEAF7", ec=WARNA["biru"], lw=1.2, zorder=3))
            ax.text(cx, y_dasar + 15.0, "Kolom Air Permukaan", ha="center", va="center", fontsize=8.0, color=WARNA["navy"], fontweight="bold", zorder=4)
            # Reflected ER (kecil)
            panah(ax, cx, y_dasar + 20.0, x0 + lebar_panel - 6.0, y_dasar + 32.0, warna=WARNA["biru"], lw=1.0, skala=9)
            ax.text(x0 + lebar_panel - 9.0, y_dasar + 27.0, r"$E_R$ (Kecil)", fontsize=8.0, fontweight="bold", color=WARNA["biru"])
            # Transmitted ET ke bawah air
            panah(ax, cx, y_dasar + 14.0, cx, y_dasar + 8.0, warna=WARNA["teal"], lw=1.4, putus=True, skala=9)
            ax.text(cx + 2.5, y_dasar + 10.5, r"$E_T$", fontsize=8.0, fontweight="bold", color=WARNA["teal"])
            # Absorbed EA
            ax.text(cx - 10.0, y_dasar + 10.5, r"$E_A$ (Tinggi)", fontsize=7.5, color=WARNA["merah"], fontweight="bold")
            
        # Poin teks keterangan bawah
        ax.text(x0 + 2.0, y_dasar + 1.2, poin, fontsize=6.8, color=WARNA["teks"], va="bottom", linespacing=1.2)

    simpan(fig, "modul-1", "M1-G07_keseimbangan-energi.png")

def g_m7_skema_spektrometer():
    fig, ax = kanvas(10.5, 5.6, (0, 105), (0, 56))
    
    # Judul
    ax.text(52.5, 53.5, "ARSITEKTUR INSTRUMEN SPEKTROMETER LAPANGAN MANDIRI (CUSTOM VIS-NIR)",
            ha="center", va="center", fontsize=10.0, fontweight="bold", color=WARNA["navy"])
    
    # 4 Kotak Alur Utama
    w = 20.5
    h = 28.0
    y0 = 17.0
    
    # Blok 1: Unit Probe & Sensor
    kotak(ax, 3.0, y0, w, h, 
          "1. OPTIK & SENSOR\n\n"
          "• Probe Kontak Tanah\n"
          "• Sumber Halogen 5W\n"
          "• Sensor Spektrometer\n"
          "  Vis-NIR (410-940 nm)\n"
          "• Panel Putih 99%\n"
          "  (White Reference)",
          isi="#FAF7F2", warna=WARNA["tanah"], tebal=True, ukuran=7.8)
    
    # Blok 2: Pengendali & Mikrokontroler
    kotak(ax, 28.0, y0, w, h,
          "2. KONTROL & AKUISISI\n\n"
          "• Mikrokontroler 32-bit\n"
          "  (ESP32 / Cortex-M)\n"
          "• ADC 16-bit Presisi\n"
          "• Manajemen Daya\n"
          "  Baterai Li-ion 3.7V\n"
          "• Modul Tombol Titik",
          isi="#F3F5F9", warna=WARNA["navy"], tebal=True, ukuran=7.8)
          
    # Blok 3: Antarmuka Komunikasi
    kotak(ax, 53.0, y0, w, h,
          "3. TRANSMISI DATA\n\n"
          "• Bluetooth BLE 5.0 /\n"
          "  USB Serial Port\n"
          "• Protokol JSON/Raw\n"
          "• Geotagging Otomatis\n"
          "  GPS Ponsel/Laptop\n"
          "• Waktu Kirim: < 1 dtk",
          isi="#EDF7F6", warna=WARNA["teal"], tebal=True, ukuran=7.8)
          
    # Blok 4: Pemrosesan & Prediksi GUI
    kotak(ax, 78.0, y0, w, h,
          "4. PREDIKSI PYTHON\n\n"
          "• Dark/White Kalibrasi\n"
          "• Praolah Spektrum:\n"
          "  Savitzky-Golay + SNV\n"
          "• Model Kalibrasi:\n"
          "  PLSR / Random Forest\n"
          "• Waktu Komputasi: < 2 dtk",
          isi="#FFF7ED", warna=WARNA["oranye"], tebal=True, ukuran=7.8)
          
    # Panah penghubung antar blok
    panah(ax, 23.5, y0 + h/2, 28.0, y0 + h/2, warna=WARNA["tanah"], lw=1.6)
    panah(ax, 48.5, y0 + h/2, 53.0, y0 + h/2, warna=WARNA["navy"], lw=1.6)
    panah(ax, 73.5, y0 + h/2, 78.0, y0 + h/2, warna=WARNA["teal"], lw=1.6)
    
    # Blok Hasil Luaran di Bawah
    kotak(ax, 3.0, 3.0, 99.0, 10.5,
          "LUARAN INSTAN DI LAPANGAN (WAKTU TOTAL < 10 DETIK / TITIK):\n"
          "• Kurva Reflektansi Spektral Kontinu  |  • Estimasi Kadar Lempung (%)  |  • C-Organik (%)  |  • Kadar Air Lapang (%)\n"
          "Hasil tersimpan otomatis ke basis data GIS perkebunan bersama koordinat GPS, siap diintegrasikan ke Model DSM.",
          isi=WARNA["hijau_muda"], warna=WARNA["hijau"], tebal=False, ukuran=8.0, warna_teks=WARNA["teks"])
          
    simpan(fig, "modul-7", "M7-G05_skema-spektrometer-mandiri.png")

def g_m8_interval_spline():
    fig, ax = kanvas(10.5, 5.8, (0, 105), (0, 58))
    
    # Judul
    ax.text(52.5, 54.0, "HARMONISASI KEDALAMAN TANAH: DARI SAMPEL LAPANGAN KE INTERVAL BAKU GLOBALSOILMAP",
            ha="center", va="center", fontsize=9.2, fontweight="bold", color=WARNA["navy"])
            
    # Kolom 1: Horizon Lapangan
    ax.text(17.5, 49.0, "(a) Lapisan Sampel Lapangan\n(Interval Horizon Tidak Seragam)", 
            ha="center", va="center", fontsize=7.8, fontweight="bold", color=WARNA["tanah"])
    # Gambar profil tanah lapangan
    skala_z = 0.20 # 200 cm = 40 satuan
    z0 = 44.0
    
    horizons = [
        (0, 15, "0–15 cm (Ap)", 32.0, "#CDB27A"),
        (15, 45, "15–45 cm (Bt1)", 48.0, "#B5763F"),
        (45, 90, "45–90 cm (Bt2)", 55.0, "#8C5A3C"),
        (90, 150, "90–150 cm (BC)", 42.0, "#A9863F"),
        (150, 200, "150–200 cm (C)", 28.0, "#CDB89A")
    ]
    for top, bot, label, val, c in horizons:
        y_atas = z0 - top * skala_z
        y_bawah = z0 - bot * skala_z
        ax.add_patch(Rectangle((6.0, y_bawah), 23.0, y_atas - y_bawah, fc=c, ec=WARNA["navy"], lw=0.8, alpha=0.9))
        ax.text(17.5, (y_atas + y_bawah) / 2, f"{label}\nLempung: {val:.0f}%", ha="center", va="center", fontsize=7.2, color="white" if val > 40 else WARNA["navy"], fontweight="bold")
    
    # Kolom 2: Kurva Spline Kontinu
    ax.text(52.5, 49.0, "(b) Equal-Area Quadratic Spline\n(Fungsi Kontinu Bebas Undak)", 
            ha="center", va="center", fontsize=7.8, fontweight="bold", color=WARNA["teal"])
    # Plot kurva
    ax.plot([40.0, 65.0], [z0 - 200*skala_z, z0 - 200*skala_z], color=WARNA["abu"], lw=0.6)
    ax.plot([40.0, 40.0], [z0, z0 - 200*skala_z], color=WARNA["abu"], lw=0.8)
    
    # Titik kurva spline realistis
    zs = np.linspace(0, 200, 200)
    # Kurva mulus lempung meningkat ke Bt lalu turun di C
    clay_spline = 30.0 + 26.0 * (1.0 / (1.0 + np.exp(-(zs - 25)/15.0))) * np.exp(-zs/160.0)
    # Normalkan ke koordinat plot
    x_spline = 40.0 + (clay_spline / 70.0) * 23.0
    y_spline = z0 - zs * skala_z
    ax.plot(x_spline, y_spline, color=WARNA["teal"], lw=2.2, label="Spline Fit")
    
    # Anotasi kedalaman
    for depth in [0, 50, 100, 150, 200]:
        y_pos = z0 - depth * skala_z
        ax.text(38.5, y_pos, f"-{depth}", ha="right", va="center", fontsize=6.8, color=WARNA["abu"])
        ax.plot([39.0, 40.0], [y_pos, y_pos], color=WARNA["abu"], lw=0.8)
    ax.text(51.5, z0 - 200*skala_z - 2.5, "Kadar Lempung (%) ->", ha="center", va="center", fontsize=7.0, color=WARNA["teal"])
    
    # Kolom 3: 6 Interval GlobalSoilMap
    ax.text(87.5, 49.0, "(c) Standar GlobalSoilMap\n(6 Interval Kedalaman Baku)", 
            ha="center", va="center", fontsize=7.8, fontweight="bold", color=WARNA["navy"])
            
    gsm_layers = [
        (0, 5, "0–5 cm", 31.2, "#D9B48F"),
        (5, 15, "5–15 cm", 34.8, "#CDB27A"),
        (15, 30, "15–30 cm", 44.5, "#B5763F"),
        (30, 60, "30–60 cm", 53.8, "#8C5A3C"),
        (60, 100, "60–100 cm", 51.2, "#9C7650"),
        (100, 200, "100–200 cm", 35.6, "#CDB89A")
    ]
    for top, bot, label, val, c in gsm_layers:
        y_atas = z0 - top * skala_z
        y_bawah = z0 - bot * skala_z
        ax.add_patch(Rectangle((76.0, y_bawah), 23.0, y_atas - y_bawah, fc=c, ec=WARNA["navy"], lw=0.8))
        ax.text(87.5, (y_atas + y_bawah) / 2, f"{label} (Lempung: {val:.1f}%)", ha="center", va="center", 
                fontsize=7.0, color="white" if val > 42 else WARNA["navy"], fontweight="bold")
                
    # Panah antar tahap
    panah(ax, 30.5, 24.0, 37.5, 24.0, warna=WARNA["teal"], lw=1.5)
    panah(ax, 66.5, 24.0, 74.0, 24.0, warna=WARNA["navy"], lw=1.5)
    
    simpan(fig, "modul-8", "M8-G06_interval-kedalaman-globalsoilmap.png")

if __name__ == "__main__":
    gaya.atur()
    g_m1_keseimbangan_energi()
    g_m7_skema_spektrometer()
    g_m8_interval_spline()
