#!/usr/bin/env python3
"""
buat_infografis_requirements.py
Merender infografis profesional resolusi tinggi (.png) tentang Minimum dan Recommended Requirements
untuk Pelatihan Remote Sensing, Proximal Soil Sensing, dan Digital Soil Mapping.
Palet Warna Khas UGM: Deep Royal Navy (#1B365D), Warm Terracotta/Amber (#C05621), Emerald (#059669).
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_DIR = "/home/jhn/Documents/Sayangku/Modul Junun/Output/Pelatihan"
os.makedirs(OUTPUT_DIR, exist_ok=True)
IMG_PATH_1 = os.path.join(OUTPUT_DIR, "infografis_system_requirements.png")
IMG_PATH_2 = os.path.join(OUTPUT_DIR, "screenshots", "infografis_system_requirements.png")
IMG_PATH_ROOT = os.path.join("/home/jhn/Documents/Sayangku/Modul Junun/Output", "infografis_system_requirements.png")

def create_infographic():
    fig = plt.figure(figsize=(16, 9), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1600)
    ax.set_ylim(0, 900)
    ax.axis('off')

    font_main = 'Ubuntu' if 'Ubuntu' in [f.name for f in plt.matplotlib.font_manager.fontManager.ttflist] else 'DejaVu Sans'

    # 1. Background Kanvas
    bg_rect = patches.Rectangle((0, 0), 1600, 900, facecolor='#F8FAFC', edgecolor='none')
    ax.add_patch(bg_rect)

    # Aksen Top Banner Gradient (Warm Terracotta)
    top_bar = patches.Rectangle((0, 890), 1600, 10, facecolor='#C05621', edgecolor='none')
    ax.add_patch(top_bar)

    # 2. Header Section
    # Pill Institusi
    pill = patches.FancyBboxPatch((70, 825), 620, 32, boxstyle="round,pad=3,rounding_size=16",
                                  facecolor='#1B365D', edgecolor='none')
    ax.add_patch(pill)
    ax.text(380, 841, "PUSAT STUDI PENGELOLAAN SUMBER DAYA LAHAN (PS2DL) UGM & PT SMART TBK",
            ha='center', va='center', fontsize=9.5, fontweight='bold', color='#FFFFFF', fontfamily=font_main)

    # Judul Utama
    ax.text(70, 785, "SPESIFIKASI PERANGKAT KERJA (SYSTEM REQUIREMENTS)",
            ha='left', va='center', fontsize=22, fontweight='heavy', color='#1B365D', fontfamily=font_main)
    
    # Subjudul
    ax.text(70, 755, "Panduan Kesiapan Laptop Peserta untuk Menjalankan Jupyter Notebook (RS-PSS-DSM) & QGIS Desktop",
            ha='left', va='center', fontsize=11.5, color='#64748B', fontfamily=font_main)

    # Garis Pembatas Header Halus
    line_h = patches.Rectangle((70, 735), 1460, 2, facecolor='#CBD5E1', edgecolor='none')
    ax.add_patch(line_h)

    # =========================================================================
    # 3. KARTU KIRI: MINIMUM REQUIREMENTS
    # =========================================================================
    card_x1 = 70
    card_y1 = 250
    card_w = 710
    card_h = 465

    # Bayangan kartu 1
    shadow1 = patches.FancyBboxPatch((card_x1 + 3, card_y1 - 3), card_w, card_h, boxstyle="round,pad=0,rounding_size=16",
                                     facecolor='#E2E8F0', edgecolor='none', alpha=0.7)
    ax.add_patch(shadow1)

    # Badan kartu 1
    card1 = patches.FancyBboxPatch((card_x1, card_y1), card_w, card_h, boxstyle="round,pad=0,rounding_size=16",
                                   facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=1.5)
    ax.add_patch(card1)

    # Header Card 1 (Amber / Minimal)
    card1_header = patches.FancyBboxPatch((card_x1, card_y1 + card_h - 75), card_w, 75,
                                          boxstyle="round,pad=0,rounding_size=16",
                                          facecolor='#FFFBEB', edgecolor='#FCD34D', linewidth=1.2)
    ax.add_patch(card1_header)
    ax.add_patch(patches.Rectangle((card_x1, card_y1 + card_h - 75), card_w, 30, facecolor='#FFFBEB', edgecolor='none'))

    # Judul Card 1
    ax.text(card_x1 + 30, card_y1 + card_h - 32, "MINIMUM REQUIREMENTS",
            ha='left', va='center', fontsize=15, fontweight='heavy', color='#92400E', fontfamily=font_main)
    ax.text(card_x1 + 30, card_y1 + card_h - 55, "Standar batas minimal agar seluruh alur praktikum dapat berjalan",
            ha='left', va='center', fontsize=10, color='#B45309', fontfamily=font_main)

    # Badge Kategori
    badge1 = patches.FancyBboxPatch((card_x1 + card_w - 185, card_y1 + card_h - 48), 160, 26,
                                    boxstyle="round,pad=2,rounding_size=13",
                                    facecolor='#FEF3C7', edgecolor='#F59E0B', linewidth=1)
    ax.add_patch(badge1)
    ax.text(card_x1 + card_w - 105, card_y1 + card_h - 35, "EKSEKUSI TUNGGAL",
            ha='center', va='center', fontsize=8.5, fontweight='bold', color='#B45309', fontfamily=font_main)

    # Komponen Card 1 (Items)
    items_min = [
        ("PROSESOR (CPU)", "Dual-Core 64-bit @ 2.0 GHz+", "Intel Core i3 (Gen 6+), AMD Ryzen 3, atau Celeron Modern"),
        ("MEMORI (RAM)", "4 GB RAM", "Mampu menjalankan notebook; tutup aplikasi lain saat proses berat"),
        ("PENYIMPANAN", "5 GB Ruang Kosong", "Diperlukan untuk environment Python, pustaka, dan data raster"),
        ("SISTEM OPERASI", "Windows 10/11 (64-bit), Linux, macOS", "Arsitektur 64-bit wajib untuk pustaka rasterio & geospatial"),
        ("KONEKSI INTERNET", "Minimal 5 Mbps Stabil", "Diperlukan di awal untuk unduh pustaka pip & query STAC API")
    ]

    item_y = card_y1 + card_h - 115
    for label, val, desc in items_min:
        bullet = patches.FancyBboxPatch((card_x1 + 30, item_y - 12), 24, 24, boxstyle="round,pad=1,rounding_size=6",
                                        facecolor='#FEF3C7', edgecolor='#F59E0B', linewidth=1)
        ax.add_patch(bullet)
        ax.text(card_x1 + 42, item_y, "-", ha='center', va='center', fontsize=12, fontweight='bold', color='#D97706')

        ax.text(card_x1 + 65, item_y + 4, label, ha='left', va='center', fontsize=9, fontweight='bold', color='#64748B', fontfamily=font_main)
        ax.text(card_x1 + 220, item_y + 4, val, ha='left', va='center', fontsize=11, fontweight='bold', color='#1E293B', fontfamily=font_main)
        ax.text(card_x1 + 220, item_y - 14, desc, ha='left', va='center', fontsize=8.5, color='#64748B', fontfamily=font_main)

        ax.plot([card_x1 + 30, card_x1 + card_w - 30], [item_y - 28, item_y - 28], color='#F1F5F9', lw=1.2)
        item_y -= 62

    # Kotak Catatan Minimum
    note1 = patches.FancyBboxPatch((card_x1 + 25, card_y1 + 18), card_w - 50, 48, boxstyle="round,pad=2,rounding_size=8",
                                  facecolor='#FFFBEB', edgecolor='#FDE68A', linewidth=1)
    ax.add_patch(note1)
    ax.text(card_x1 + 40, card_y1 + 42, "Catatan Penggunaan Spek Minimal:",
            ha='left', va='center', fontsize=8.5, fontweight='bold', color='#92400E', fontfamily=font_main)
    ax.text(card_x1 + 40, card_y1 + 28, "Tutup QGIS Desktop saat menjalankan pelatihan Random Forest 500 pohon di Praktik 5 agar RAM tidak penuh.",
            ha='left', va='center', fontsize=8, color='#B45309', fontfamily=font_main)


    # =========================================================================
    # 4. KARTU KANAN: RECOMMENDED REQUIREMENTS
    # =========================================================================
    card_x2 = 820

    # Bayangan kartu 2
    shadow2 = patches.FancyBboxPatch((card_x2 + 3, card_y1 - 3), card_w, card_h, boxstyle="round,pad=0,rounding_size=16",
                                     facecolor='#E2E8F0', edgecolor='none', alpha=0.7)
    ax.add_patch(shadow2)

    # Badan kartu 2 (Highlight Border Green)
    card2 = patches.FancyBboxPatch((card_x2, card_y1), card_w, card_h, boxstyle="round,pad=0,rounding_size=16",
                                   facecolor='#FFFFFF', edgecolor='#059669', linewidth=2.0)
    ax.add_patch(card2)

    # Header Card 2 (Emerald / Recommended)
    card2_header = patches.FancyBboxPatch((card_x2, card_y1 + card_h - 75), card_w, 75,
                                          boxstyle="round,pad=0,rounding_size=16",
                                          facecolor='#ECFDF5', edgecolor='#6EE7B7', linewidth=1.2)
    ax.add_patch(card2_header)
    ax.add_patch(patches.Rectangle((card_x2, card_y1 + card_h - 75), card_w, 30, facecolor='#ECFDF5', edgecolor='none'))

    # Judul Card 2
    ax.text(card_x2 + 30, card_y1 + card_h - 32, "RECOMMENDED REQUIREMENTS",
            ha='left', va='center', fontsize=15, fontweight='heavy', color='#065F46', fontfamily=font_main)
    ax.text(card_x2 + 30, card_y1 + card_h - 55, "Konfigurasi optimal untuk multitasking lancar tanpa kendala lag",
            ha='left', va='center', fontsize=10, color='#047857', fontfamily=font_main)

    # Badge Kategori
    badge2 = patches.FancyBboxPatch((card_x2 + card_w - 195, card_y1 + card_h - 48), 170, 26,
                                    boxstyle="round,pad=2,rounding_size=13",
                                    facecolor='#059669', edgecolor='none')
    ax.add_patch(badge2)
    ax.text(card_x2 + card_w - 110, card_y1 + card_h - 35, "MULTITASKING LANCAR",
            ha='center', va='center', fontsize=8.5, fontweight='bold', color='#FFFFFF', fontfamily=font_main)

    # Komponen Card 2 (Items)
    items_rec = [
        ("PROSESOR (CPU)", "Quad-Core / Hexa-Core 64-bit", "Intel Core i5/i7 (Gen 10+), AMD Ryzen 5/7, atau Apple M1/M2/M3"),
        ("MEMORI (RAM)", "8 GB – 16 GB RAM", "Bebas membuka JupyterLab + QGIS 3 + Browser secara bersamaan"),
        ("PENYIMPANAN", "10 GB+ Ruang Kosong (SSD)", "Solid State Drive mempercepat loading citra satelit & DEMNAS"),
        ("RESOLUSI LAYAR", "Full HD (1920 x 1080) IPS", "Sangat nyaman untuk pembacaan peta spektral & kartografi"),
        ("KONEKSI INTERNET", "15 – 25 Mbps Stabil", "Unduh paket cepat dan akses query satelit realtime responsif")
    ]

    item_y = card_y1 + card_h - 115
    for label, val, desc in items_rec:
        bullet = patches.FancyBboxPatch((card_x2 + 30, item_y - 12), 24, 24, boxstyle="round,pad=1,rounding_size=6",
                                        facecolor='#DCFCE7', edgecolor='#10B981', linewidth=1)
        ax.add_patch(bullet)
        ax.text(card_x2 + 42, item_y, "+", ha='center', va='center', fontsize=12, fontweight='bold', color='#059669')

        ax.text(card_x2 + 65, item_y + 4, label, ha='left', va='center', fontsize=9, fontweight='bold', color='#64748B', fontfamily=font_main)
        ax.text(card_x2 + 220, item_y + 4, val, ha='left', va='center', fontsize=11, fontweight='bold', color='#1E293B', fontfamily=font_main)
        ax.text(card_x2 + 220, item_y - 14, desc, ha='left', va='center', fontsize=8.5, color='#64748B', fontfamily=font_main)

        ax.plot([card_x2 + 30, card_x2 + card_w - 30], [item_y - 28, item_y - 28], color='#F1F5F9', lw=1.2)
        item_y -= 62

    # Kotak Keunggulan Recommended
    note2 = patches.FancyBboxPatch((card_x2 + 25, card_y1 + 18), card_w - 50, 48, boxstyle="round,pad=2,rounding_size=8",
                                  facecolor='#ECFDF5', edgecolor='#A7F3D0', linewidth=1)
    ax.add_patch(note2)
    ax.text(card_x2 + 40, card_y1 + 42, "Performa Komputasi Pelatihan:",
            ha='left', va='center', fontsize=8.5, fontweight='bold', color='#065F46', fontfamily=font_main)
    ax.text(card_x2 + 40, card_y1 + 28, "Fitting Quantile Regression Forest selesai dalam 3–8 detik; prediksi 29.469 piksel Sub-DAS Bompon instan.",
            ha='left', va='center', fontsize=8, color='#047857', fontfamily=font_main)


    # =========================================================================
    # 5. AREA BAWAH: 3 KARTU SOROTAN TEKNIS
    # =========================================================================
    bottom_y = 65
    bottom_h = 160
    bottom_w = 466

    # --- KARTU 1: VERSI PYTHON ---
    bx1 = 70
    b_card1 = patches.FancyBboxPatch((bx1, bottom_y), bottom_w, bottom_h, boxstyle="round,pad=0,rounding_size=12",
                                     facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=1.2)
    ax.add_patch(b_card1)
    top_bc1 = patches.Rectangle((bx1, bottom_y + bottom_h - 6), bottom_w, 6, facecolor='#1B365D', edgecolor='none')
    ax.add_patch(top_bc1)

    tag1 = patches.FancyBboxPatch((bx1 + 25, bottom_y + bottom_h - 36), 65, 18, boxstyle="round,pad=2,rounding_size=5",
                                  facecolor='#1B365D', edgecolor='none')
    ax.add_patch(tag1)
    ax.text(bx1 + 57.5, bottom_y + bottom_h - 27, "PYTHON", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#FFFFFF', fontfamily=font_main)

    ax.text(bx1 + 100, bottom_y + bottom_h - 27, "VERSI PYTHON TERSTANDAR",
            ha='left', va='center', fontsize=10.5, fontweight='heavy', color='#1B365D', fontfamily=font_main)
    ax.text(bx1 + 25, bottom_y + bottom_h - 58, "Gunakan Python 3.10 atau 3.11 (64-bit)",
            ha='left', va='center', fontsize=10.5, fontweight='bold', color='#1E293B', fontfamily=font_main)
    ax.text(bx1 + 25, bottom_y + bottom_h - 86,
            "- Pustaka biner (wheels) rasterio & quantile-forest\n  tersedia resmi tanpa perlu Visual C++ compiler.\n- Hindari Python 3.13 untuk meminimalkan kendala build.",
            ha='left', va='top', fontsize=8.8, color='#64748B', fontfamily=font_main, linespacing=1.35)

    # --- KARTU 2: SOFTWARE & DEPENDENSI ---
    bx2 = 566
    b_card2 = patches.FancyBboxPatch((bx2, bottom_y), bottom_w, bottom_h, boxstyle="round,pad=0,rounding_size=12",
                                     facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=1.2)
    ax.add_patch(b_card2)
    top_bc2 = patches.Rectangle((bx2, bottom_y + bottom_h - 6), bottom_w, 6, facecolor='#C05621', edgecolor='none')
    ax.add_patch(top_bc2)

    tag2 = patches.FancyBboxPatch((bx2 + 25, bottom_y + bottom_h - 36), 50, 18, boxstyle="round,pad=2,rounding_size=5",
                                  facecolor='#C05621', edgecolor='none')
    ax.add_patch(tag2)
    ax.text(bx2 + 50, bottom_y + bottom_h - 27, "QGIS", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#FFFFFF', fontfamily=font_main)

    ax.text(bx2 + 85, bottom_y + bottom_h - 27, "GIS & VIRTUAL ENVIRONMENT",
            ha='left', va='center', fontsize=10.5, fontweight='heavy', color='#C05621', fontfamily=font_main)
    ax.text(bx2 + 25, bottom_y + bottom_h - 58, "QGIS 3.28 LTR s.d. 3.34+ LTR & venv",
            ha='left', va='center', fontsize=10.5, fontweight='bold', color='#1E293B', fontfamily=font_main)
    ax.text(bx2 + 25, bottom_y + bottom_h - 86,
            "- Gunakan virtual environment terisolasi (env_smart)\n  melalui skrip setup_env.sh atau setup_env.bat.\n- Paket: numpy, pandas, rasterio, scikit-learn, scipy.",
            ha='left', va='top', fontsize=8.8, color='#64748B', fontfamily=font_main, linespacing=1.35)

    # --- KARTU 3: DUKUNGAN CLOUD ---
    bx3 = 1063
    b_card3 = patches.FancyBboxPatch((bx3, bottom_y), bottom_w, bottom_h, boxstyle="round,pad=0,rounding_size=12",
                                     facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=1.2)
    ax.add_patch(b_card3)
    top_bc3 = patches.Rectangle((bx3, bottom_y + bottom_h - 6), bottom_w, 6, facecolor='#059669', edgecolor='none')
    ax.add_patch(top_bc3)

    tag3 = patches.FancyBboxPatch((bx3 + 25, bottom_y + bottom_h - 36), 55, 18, boxstyle="round,pad=2,rounding_size=5",
                                  facecolor='#059669', edgecolor='none')
    ax.add_patch(tag3)
    ax.text(bx3 + 52.5, bottom_y + bottom_h - 27, "CLOUD", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#FFFFFF', fontfamily=font_main)

    ax.text(bx3 + 90, bottom_y + bottom_h - 27, "DUKUNGAN GOOGLE COLAB",
            ha='left', va='center', fontsize=10.5, fontweight='heavy', color='#059669', fontfamily=font_main)
    ax.text(bx3 + 25, bottom_y + bottom_h - 58, "Solusi Peserta Laptop Spek Rendah",
            ha='left', va='center', fontsize=10.5, fontweight='bold', color='#1E293B', fontfamily=font_main)
    ax.text(bx3 + 25, bottom_y + bottom_h - 86,
            "- Seluruh notebook kompatibel dengan Google Colab.\n- Dilengkapi blok otomatis 'if google.colab in sys'.\n- Manfaatkan RAM 12 GB gratis di cloud tanpa instalasi.",
            ha='left', va='top', fontsize=8.8, color='#64748B', fontfamily=font_main, linespacing=1.35)

    # 6. Footer Mini
    ax.text(800, 25, "PS2DL Fakultas Pertanian UGM — Modul Pelatihan Remote Sensing & Digital Soil Mapping PT SMART Tbk (2026)",
            ha='center', va='center', fontsize=8.5, color='#94A3B8', fontfamily=font_main)

    print(f"Menyimpan infografis ke: {IMG_PATH_1}")
    plt.savefig(IMG_PATH_1, dpi=150, facecolor='#F8FAFC', bbox_inches='tight', pad_inches=0.1)
    
    print(f"Menyimpan salinan ke: {IMG_PATH_2}")
    plt.savefig(IMG_PATH_2, dpi=150, facecolor='#F8FAFC', bbox_inches='tight', pad_inches=0.1)

    print(f"Menyimpan salinan ke root: {IMG_PATH_ROOT}")
    plt.savefig(IMG_PATH_ROOT, dpi=150, facecolor='#F8FAFC', bbox_inches='tight', pad_inches=0.1)

    plt.close()
    print("=== Infografis Berhasil Dibuat dengan Sukses! ===")

if __name__ == "__main__":
    create_infographic()
