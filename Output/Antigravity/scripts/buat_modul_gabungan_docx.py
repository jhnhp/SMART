"""
Skrip Pembangun Dokumen Word (.docx) Gabungan Seluruh Modul Praktik Pelatihan SMART
- Menggabungkan Praktik 1 s.d. 5, Kurikulum, Penyiapan venv, dan Evaluasi.
- Formatting mengadopsi format pedagogis 'Modul_Precision Nutrient Management.pdf'.
- Pewarnaan KHAS & BERBEDA dari buatan Pak Pandu:
  * Primer: Deep Navy Royal UGM (#1B365D)
  * Sekunder / Aksen Tanah: Warm Terracotta / Amber (#C05621)
  * Neutral Dark: Charcoal Slate (#1E293B)
  * Callout backgrounds: Ice Blue (#EFF6FF), Warm Amber (#FFFBEB), Mint (#F0FDF4)
- Menghasilkan: Output/Pelatihan/Modul_Praktikum_Lengkap_RS_PSS_DSM.docx
"""

import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

BASE_DIR = "/home/jhn/Documents/Sayangku/Modul Junun"
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "Output/Pelatihan/screenshots")
OUTPUT_DOCX = os.path.join(BASE_DIR, "Output/Pelatihan/Modul_Praktikum_Lengkap_RS_PSS_DSM.docx")

# PALET WARNA KHAS UGM & PEDOLOGI MODERN (BERBEDA DARI HIJAU LUMUT PAK PANDU)
HEX_NAVY = "1B365D"       # Deep Royal Navy UGM
HEX_TERRACOTTA = "C05621"  # Warm Terracotta (C-Organik / Tanah)
HEX_CHARCOAL = "1E293B"    # Dark Slate Body
HEX_BORDER = "CBD5E1"      # Subtle Gray
HEX_BG_CARD = "F8FAFC"     # Light Off-white / Slate
HEX_BG_TIP = "EFF6FF"      # Ice Blue (Tips)
HEX_BORDER_TIP = "2563EB"
HEX_BG_WARN = "FFFBEB"     # Soft Amber (Important / venv)
HEX_BORDER_WARN = "D97706"
HEX_BG_SUCC = "F0FDF4"     # Mint Fresh (Quality Checkpoint)
HEX_BORDER_SUCC = "059669"

COLOR_NAVY = RGBColor(0x1B, 0x36, 0x5D)
COLOR_TERRACOTTA = RGBColor(0xC0, 0x56, 0x21)
COLOR_CHARCOAL = RGBColor(0x1E, 0x29, 0x3B)
COLOR_MUTED = RGBColor(0x64, 0x74, 0x8B)

FONT_FAMILY = "Calibri"

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    # Hapus shading lama jika ada
    for child in list(tcPr):
        if child.tag.endswith('shd'):
            tcPr.remove(child)
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def set_callout_border(cell, hex_border_color):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="none"/>
            <w:left w:val="single" w:sz="36" w:space="0" w:color="{hex_border_color}"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)

def set_table_borders(table, hex_color=HEX_BORDER):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="6" w:space="0" w:color="{hex_color}"/>
            <w:left w:val="none"/>
            <w:bottom w:val="single" w:sz="8" w:space="0" w:color="{HEX_NAVY}"/>
            <w:right w:val="none"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{hex_color}"/>
            <w:insideV w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def add_header_footer(doc):
    for s in doc.sections:
        s.header_distance = Cm(1.2)
        s.footer_distance = Cm(1.2)
        
        # Header
        hp = s.header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("MODUL PRAKTIKUM: REMOTE SENSING, PSS, & DIGITAL SOIL MAPPING | PS2DL UGM & PT SMART TBK")
        hrun.font.name = FONT_FAMILY
        hrun.font.size = Pt(8)
        hrun.font.color.rgb = COLOR_MUTED
        
        # Footer
        fp = s.footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        frun_l = fp.add_run("Pelatihan Pemanfaatan RS & DSM untuk Pertanian Presisi  |  Halaman ")
        frun_l.font.name = FONT_FAMILY
        frun_l.font.size = Pt(9)
        frun_l.font.color.rgb = COLOR_MUTED
        
        # XML Field Page
        fld1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
        instr = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
        fld2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
        fld3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
        frun_l._r.append(fld1)
        frun_l._r.append(instr)
        frun_l._r.append(fld2)
        frun_l._r.append(fld3)

def add_p(doc, text="", bold=False, italic=False, size=11, color=COLOR_CHARCOAL, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6, line_spacing=1.15):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if text:
        r = p.add_run(text)
        r.font.name = FONT_FAMILY
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = color
    return p

def add_h1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(20)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = FONT_FAMILY
    r.font.size = Pt(17)
    r.font.bold = True
    r.font.color.rgb = COLOR_NAVY
    return p

def add_h2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = FONT_FAMILY
    r.font.size = Pt(13.5)
    r.font.bold = True
    r.font.color.rgb = COLOR_TERRACOTTA
    return p

def add_h3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = FONT_FAMILY
    r.font.size = Pt(11.5)
    r.font.bold = True
    r.font.color.rgb = COLOR_CHARCOAL
    return p

def add_callout(doc, title, message_lines, box_type="info"):
    if box_type == "warn":
        bg_col = HEX_BG_WARN
        border_col = HEX_BORDER_WARN
        title_col = RGBColor(0xB4, 0x53, 0x09)
    elif box_type == "succ":
        bg_col = HEX_BG_SUCC
        border_col = HEX_BORDER_SUCC
        title_col = RGBColor(0x06, 0x5F, 0x46)
    elif box_type == "curriculum":
        bg_col = HEX_BG_CARD
        border_col = HEX_NAVY
        title_col = COLOR_NAVY
    else: # info
        bg_col = HEX_BG_TIP
        border_col = HEX_BORDER_TIP
        title_col = RGBColor(0x1D, 0x4E, 0xD8)

    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    cell = tbl.cell(0, 0)
    cell.width = Cm(16.5)
    set_cell_background(cell, bg_col)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=180)
    set_callout_border(cell, border_col)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    r_t = p.add_run(title)
    r_t.font.name = FONT_FAMILY
    r_t.font.size = Pt(10.5)
    r_t.font.bold = True
    r_t.font.color.rgb = title_col
    
    for line in message_lines:
        p_m = cell.add_paragraph()
        p_m.paragraph_format.space_before = Pt(2)
        p_m.paragraph_format.space_after = Pt(3)
        p_m.paragraph_format.line_spacing = 1.15
        r_m = p_m.add_run(line)
        r_m.font.name = FONT_FAMILY
        r_m.font.size = Pt(9.5)
        r_m.font.color.rgb = COLOR_CHARCOAL
        
    p_dummy = doc.add_paragraph()
    p_dummy.paragraph_format.space_before = Pt(0)
    p_dummy.paragraph_format.space_after = Pt(4)

def add_table_data(doc, headers, data, col_widths=None):
    tbl = doc.add_table(rows=len(data) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl)
    
    # Header Row
    hdr_cells = tbl.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        set_cell_background(hdr_cells[i], HEX_NAVY)
        set_cell_margins(hdr_cells[i], top=140, bottom=140, left=140, right=140)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.name = FONT_FAMILY
            run.font.size = Pt(10)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            
    # Data Rows
    for row_idx, row_data in enumerate(data):
        row_cells = tbl.rows[row_idx + 1].cells
        bg_color = HEX_BG_CARD if (row_idx % 2 == 1) else "FFFFFF"
        for col_idx, cell_value in enumerate(row_data):
            row_cells[col_idx].text = str(cell_value)
            set_cell_background(row_cells[col_idx], bg_color)
            set_cell_margins(row_cells[col_idx], top=100, bottom=100, left=140, right=140)
            p = row_cells[col_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx > 0 else WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.line_spacing = 1.12
            for run in p.runs:
                run.font.name = FONT_FAMILY
                run.font.size = Pt(9.5)
                run.font.color.rgb = COLOR_CHARCOAL
                
    if col_widths:
        for r in tbl.rows:
            for idx, width in enumerate(col_widths):
                r.cells[idx].width = Cm(width)
                
    p_dummy = doc.add_paragraph()
    p_dummy.paragraph_format.space_before = Pt(0)
    p_dummy.paragraph_format.space_after = Pt(6)

def add_image_figure(doc, img_rel_name, caption_text, width=Cm(15.2)):
    img_path = os.path.join(SCREENSHOTS_DIR, img_rel_name)
    if not os.path.exists(img_path):
        print(f"Warning: Gambar {img_path} tidak ditemukan!")
        return
        
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(10)
    p_img.paragraph_format.space_after = Pt(4)
    run = p_img.add_run()
    run.add_picture(img_path, width=width)
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(12)
    p_cap.paragraph_format.keep_with_next = False
    r_cap = p_cap.add_run(caption_text)
    r_cap.font.name = FONT_FAMILY
    r_cap.font.size = Pt(9)
    r_cap.font.italic = True
    r_cap.font.color.rgb = COLOR_MUTED

# =====================================================================
# PEMBANGUN UTAMA DOKUMEN MODUL GABUNGAN
# =====================================================================
def generate_docx():
    print("Membangun dokumen Word gabungan seluruh modul praktik...")
    doc = Document()
    
    # Atur Margin Halaman A4
    for section in doc.sections:
        section.top_margin = Cm(2.54)
        section.bottom_margin = Cm(2.54)
        section.left_margin = Cm(2.54)
        section.right_margin = Cm(2.54)
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        
    add_header_footer(doc)
    
    # -----------------------------------------------------------------
    # 1. HALAMAN JUDUL (COVER EKSKLUSIF)
    # -----------------------------------------------------------------
    p_top_bar = doc.add_paragraph()
    p_top_bar.paragraph_format.space_before = Pt(40)
    p_top_bar.paragraph_format.space_after = Pt(10)
    r_bar = p_top_bar.add_run("PUSAT STUDI PENGELOLAAN SUMBER DAYA LAHAN (PS2DL) UNIVERSITAS GADJAH MADA")
    r_bar.font.name = FONT_FAMILY
    r_bar.font.size = Pt(11)
    r_bar.font.bold = True
    r_bar.font.color.rgb = COLOR_TERRACOTTA
    
    p_main_title = doc.add_paragraph()
    p_main_title.paragraph_format.space_before = Pt(20)
    p_main_title.paragraph_format.space_after = Pt(10)
    p_main_title.paragraph_format.line_spacing = 1.15
    r_title = p_main_title.add_run("MODUL PEMBELAJARAN & PANDUAN PRAKTIKUM LENGKAP")
    r_title.font.name = FONT_FAMILY
    r_title.font.size = Pt(24)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_NAVY
    
    p_sub_title = doc.add_paragraph()
    p_sub_title.paragraph_format.space_before = Pt(5)
    p_sub_title.paragraph_format.space_after = Pt(25)
    p_sub_title.paragraph_format.line_spacing = 1.2
    r_sub = p_sub_title.add_run(
        "Pengolahan Data Spasial Tingkat Lanjut dalam Precision Agriculture:\n"
        "Integrasi Remote Sensing Multi-Sensor, Proximal Soil Sensing (PSS), "
        "dan Digital Soil Mapping (DSM) untuk Pemetaan Karbon Organik Tanah"
    )
    r_sub.font.name = FONT_FAMILY
    r_sub.font.size = Pt(14)
    r_sub.font.bold = True
    r_sub.font.color.rgb = COLOR_CHARCOAL
    
    # Kotak Metadata Pelatihan
    add_callout(
        doc,
        "STUDI KASUS SPASIAL TERPADU: SUB-DAS BOMPON (MAGELANG)",
        [
            "Lokasi Bentang Lahan: Sub-DAS Bompon, Jawa Tengah (295 Hektar, EPSG:32749 / UTM Zone 49S)",
            "Target Pemodelan Pedologi: Karbon Organik Tanah (C-Organik / Soil Organic Carbon)",
            "Spektrum Penginderaan Jauh: Sentinel-2 L2A (10 m), Sentinel-1 RTC SAR (C-band VH/VV 10 m), Copernicus DEM GLO-30 (10 m)",
            "Spektroskopi Tanah Proksimal: Vis-NIR 350–2500 nm (852 Sampel Lapangan) & 50 Titik Sampel Uji Laboratorium"
        ],
        box_type="curriculum"
    )
    
    # Metadata Institusi Penyelenggara
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_before = Pt(60)
    p_meta.paragraph_format.space_after = Pt(5)
    
    r_pres_to = p_meta.add_run("Presented To:\n")
    r_pres_to.font.bold = True
    r_pres_to.font.size = Pt(11)
    r_pres_to.font.color.rgb = COLOR_TERRACOTTA
    
    r_client = p_meta.add_run("PT SMART Tbk\n\n")
    r_client.font.bold = True
    r_client.font.size = Pt(13)
    r_client.font.color.rgb = COLOR_NAVY
    
    r_pres_by = p_meta.add_run("Presented By:\n")
    r_pres_by.font.bold = True
    r_pres_by.font.size = Pt(11)
    r_pres_by.font.color.rgb = COLOR_TERRACOTTA
    
    r_inst = p_meta.add_run(
        "Pusat Studi Pengelolaan Sumber Daya Lahan (PS2DL)\n"
        "Fakultas Pertanian, Universitas Gadjah Mada\n"
        "Yogyakarta, 2026"
    )
    r_inst.font.bold = True
    r_inst.font.size = Pt(12)
    r_inst.font.color.rgb = COLOR_NAVY
    
    doc.add_page_break()
    
    # -----------------------------------------------------------------
    # 2. KATA PENGANTAR
    # -----------------------------------------------------------------
    add_h1(doc, "KATA PENGANTAR")
    add_p(
        doc,
        "Puji dan syukur kami panjatkan ke hadirat Tuhan Yang Maha Esa atas tersusunnya "
        "buku panduan Modul Pembelajaran dan Praktikum Lengkap: 'Pengolahan Data Spasial Tingkat Lanjut "
        "dalam Precision Agriculture: Remote Sensing, Proximal Soil Sensing, dan Digital Soil Mapping'. "
        "Modul ini dirancang secara khusus untuk memfasilitasi peningkatan kompetensi teknis dan analitis "
        "para staf profesional di lingkungan PT SMART Tbk dalam menjawab tantangan pengelolaan lahan perkebunan kelapa sawit secara berkelanjutan."
    )
    add_p(
        doc,
        "Dalam era pertanian presisi modern, efisiensi pemupukan dan keberlanjutan tanah sangat bergantung pada "
        "ketersediaan informasi spasial sifat tanah yang akurat, beresolusi tinggi, dan dapat dipertanggungjawabkan. "
        "Metode survei tanah konvensional seringkali terkendala oleh biaya tinggi, waktu analisis laboratorium yang panjang, "
        "serta keterbatasan kerapatan sampel pada bentang lahan perkebunan yang luas. "
        "Modul praktikum ini menghadirkan alur kerja terpadu (continuous pipeline) yang menggabungkan penginderaan jauh multi-sensor "
        "(Optik Sentinel-2 L2A, Radar Sentinel-1 RTC SAR, dan Model Elevasi Digital Copernicus DEM), spektroskopi tanah proksimal (Vis-NIR 350–2500 nm), "
        "serta algoritma pembelajaran mesin spasial (Random Forest & Quantile Regression Forest) berbasis kerangka kerja SCORPAN."
    )
    add_p(
        doc,
        "Sebagai fokus kuantitatif utama, seluruh rangkaian modul ini memodelkan sebaran spasial Karbon Organik Tanah (C-Organik), "
        "yang memegang peranan krusial sebagai indikator utama kesuburan fisik, kimia, dan biologi tanah perkebunan, "
        "sekaligus pilar utama sekuestrasi karbon dalam mendukung agenda keberlanjutan global."
    )
    add_p(
        doc,
        "Kami menyampaikan apresiasi dan terima kasih yang sebesar-besarnya kepada pimpinan manajemen dan tim teknis "
        "PT SMART Tbk atas kemitraan strategis dan kepercayaan yang diberikan kepada Pusat Studi Pengelolaan Sumber Daya Lahan (PS2DL) "
        "Universitas Gadjah Mada. Kami berharap modul praktikum ini memberikan manfaat aplikatif nyata dalam mendukung operasional perkebunan presisi."
    )
    
    p_ttd = doc.add_paragraph()
    p_ttd.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_ttd.paragraph_format.space_before = Pt(30)
    p_ttd.paragraph_format.space_after = Pt(2)
    r_ttd1 = p_ttd.add_run("Yogyakarta, 2026\n\n\n\n")
    r_ttd1.font.name = FONT_FAMILY
    r_ttd1.font.size = Pt(11)
    
    r_ttd2 = p_ttd.add_run("Tim Penyusun PS2DL Universitas Gadjah Mada\n")
    r_ttd2.font.bold = True
    r_ttd2.font.size = Pt(11)
    r_ttd2.font.color.rgb = COLOR_NAVY
    
    r_ttd3 = p_ttd.add_run("Pusat Studi Pengelolaan Sumber Daya Lahan (PS2DL) UGM")
    r_ttd3.font.italic = True
    r_ttd3.font.size = Pt(10)
    r_ttd3.font.color.rgb = COLOR_MUTED
    
    doc.add_page_break()
    
    # -----------------------------------------------------------------
    # 3. DAFTAR ISI & STRUKTUR MODUL
    # -----------------------------------------------------------------
    add_h1(doc, "DAFTAR ISI & STRUKTUR PEMBELAJARAN")
    
    daftar_isi_data = [
        ["Kata Pengantar", "1"],
        ["Daftar Isi & Struktur Pembelajaran", "2"],
        ["BAGIAN I: KURIKULUM PEMBELAJARAN UMUM & PENYIAPAN LINGKUNGAN KERJA", "3"],
        ["  • Capaian Pembelajaran & 5 Kompetensi Utama", "3"],
        ["  • Alur Pipa Integrasi 5 Sesi Praktikum", "4"],
        ["  • Penyiapan Perangkat Lunak GIS & Python Virtual Environment (venv)", "5"],
        ["BAGIAN II: MODUL PEMBELAJARAN PRAKTIK 1 S.D. 5", "8"],
        ["  • Praktik 1: Multi-Source Data Fusion (Optik, SAR, DEM)", "8"],
        ["  • Praktik 2: Delineasi Satuan Pemetaan Tanah (SMU) & Analisis Kelerengan", "14"],
        ["  • Praktik 3: Demonstrasi Proximal Soil Sensing (PSS) & Kemometrika Spektral", "20"],
        ["  • Praktik 4: Bare Soil Detection & Ekstraksi Spektrum Tanah Terbuka", "26"],
        ["  • Praktik 5: Machine Learning Digital Soil Mapping (DSM) C-Organik & Ketidakpastian", "32"],
        ["BAGIAN III: EVALUASI MANDIRI & LEMBAR KERJA PESERTA", "40"],
        ["BAGIAN IV: GLOSARIUM ISTILAH & DAFTAR PUSTAKA ACUAN", "43"],
    ]
    add_table_data(doc, ["Pokok Bahasan / Modul Praktikum", "Halaman"], daftar_isi_data, [13.5, 3.0])
    
    doc.add_page_break()
    
    # -----------------------------------------------------------------
    # 4. BAGIAN I: KURIKULUM & PENYIAPAN VENV
    # -----------------------------------------------------------------
    add_h1(doc, "BAGIAN I: KURIKULUM PEMBELAJARAN & LINGKUNGAN KOMPUTASI")
    
    add_h2(doc, "A. Capaian Pembelajaran & Kompetensi Utama")
    add_p(
        doc,
        "Pelatihan ini dirancang sebagai program terapan terpadu berbasis studi kasus bentang alam Sub-DAS Bompon (Magelang, Jawa Tengah). "
        "Setelah menyelesaikan seluruh rangkaian modul praktikum ini, peserta latih ditargetkan menguasai 5 pilar kompetensi utama:"
    )
    
    kompetensi_data = [
        ["1", "Multi-Sensor Fusion", "Mampu mengharmonisasi sistem koordinat (EPSG:32749), mere-sample grid DEM 30 m ke 10 m, menyelaraskan kisi origin piksel, memotong poligon AOI (*Clip by Mask Layer*), serta menginspeksi citra SAR Sentinel-1 RTC dan Optik Sentinel-2 L2A."],
        ["2", "Geomorfometri & SMU", "Mampu mengekstraksi parameter medan (kelerengan derajat, model hillshade), menyusun komposit Color Infrared (CIR 8-4-3), mendigitasi batas satuan pemetaan tanah (SMU) mengikuti kaidah katena lereng, serta mengontrol luas ambang MLD 0.4 ha."],
        ["3", "Spektroskopi Tanah Proksimal", "Mampu memahami karakteristik pantulan spektral tanah Vis-NIR (350–2500 nm), mengaplikasikan transformasi pra-olah sinyal (Absorbansi, SNV, Savitzky–Golay), mengidentifikasi serapan kromofor bahan organik (SOM 450–650 nm, ikatan C-H 1720 & 2300 nm), dan melatih kalibrasi PLSR."],
        ["4", "Deteksi Tanah Terbuka", "Mampu menghitung indeks spektral BSI dan NDVI, mengisolasi ruang fitur tanah terbuka murni bebas vegetasi tajuk sawit menggunakan masker biner, menganalisis dinamika musiman lahan, serta menyusun komposit *Barest Earth* multitemporal."],
        ["5", "Machine Learning DSM", "Mampu mengekstrak 11 kovariat lingkungan SCORPAN pada titik sampel tanah, melatih model Random Forest Regressor 5-Fold CV, menganalisis faktor pengontrol utama (*Feature Importance*), mengekspor peta prediksi GeoTIFF C-Organik terklip, dan memodelkan ketidakpastian QRF (PI90)."]
    ]
    add_table_data(doc, ["No", "Pilar Kompetensi", "Deskripsi Capaian Pembelajaran"], kompetensi_data, [1.2, 4.2, 11.1])
    
    add_h2(doc, "B. Alur Integrasi 5 Sesi Praktikum")
    add_p(
        doc,
        "Kelima sesi praktikum tidak berdiri sendiri, melainkan terhubung sebagai satu rantai pasok data ilmiah (*continuous data pipeline*). "
        "Praktik 1 meletakkan fondasi kisi grid 10 m seragam dan batas terklip AOI. Praktik 2 dan Praktik 4 menyediakan lapisan kovariat relief medan "
        "dan indeks tanah terbuka. Praktik 3 memberikan landasan fisis respon spektral bahan organik tanah. Keseluruhan lapisan masukan ini "
        "bertemu di Praktik 5 untuk melatih pemodelan machine learning prediktif kontinu dan kuantifikasi batas ketidakpastiannya."
    )
    
    add_callout(
        doc,
        "ALUR PIPA DATA PEMODELAN C-ORGANIK (CONTINUOUS PIPELINE)",
        [
            "Tahap 1 [Praktik 1]: Optik S2 + SAR S1 + DEM GLO-30 --> Reproyeksi UTM 49S --> Snap Grid 10 m --> Clip by Mask Batas Bompon.",
            "Tahap 2 [Praktik 2]: DEM 10 m --> Slope Derajat + Hillshade + Komposit CIR --> Delineasi Satuan Pemetaan Tanah (SMU).",
            "Tahap 3 [Praktik 3]: 852 Spektra Vis-NIR 350-2500 nm --> SNV + Savitzky-Golay 1st Deriv --> Deteksi Serapan C-H & SOM --> PLSR C-Organik.",
            "Tahap 4 [Praktik 4]: S2 Dua Musim --> BSI + NDVI --> Masker Biner Tanah Terbuka Kemarau --> Komposit Barest Earth.",
            "Tahap 5 [Praktik 5]: 50 Titik Sampel Lab C-Organik + 11 Kovariat SCORPAN --> Random Forest Regressor --> Peta Prediksi Kontinu C-Organik (GeoTIFF) + Peta Ketidakpastian PI90 (Quantile Forest)."
        ],
        box_type="info"
    )
    
    add_h2(doc, "C. Penyiapan Perangkat Lunak GIS & Python Virtual Environment (venv)")
    add_p(
        doc,
        "Untuk menjamin kelancaran pelaksanaan pelatihan pada berbagai sistem operasi (Linux, Windows, macOS) dan mencegah konflik "
        "versi pustaka perangkat lunak (*dependency conflict*), peserta diarahkan menggunakan konfigurasi terstandar berikut:"
    )
    
    add_callout(
        doc,
        "PANDUAN PENYIAPAN PYTHON VIRTUAL ENVIRONMENT (VENV)",
        [
            "1. Menjalankan Skrip Otomasi Satu-Klik:",
            "   • Di Linux / macOS: Buka terminal di folder Output/Pelatihan lalu jalankan: ./setup_env.sh",
            "   • Di Windows: Buka Command Prompt di folder Output\\Pelatihan lalu jalankan: setup_env.bat",
            "2. Prosedur Manual (Terminal):",
            "   • Buat environment: python3 -m venv env_smart   (Windows: python -m venv env_smart)",
            "   • Aktivasi venv: source env_smart/bin/activate  (Windows: env_smart\\Scripts\\activate.bat)",
            "   • Pasang paket: pip install -r requirements.txt",
            "   • Daftarkan kernel: python -m ipykernel install --user --name=env_smart --display-name='Python (Pelatihan SMART)'",
            "   • Buka Jupyter: jupyter lab",
            "3. Pemilihan Kernel di JupyterLab:",
            "   Saat membuka Praktik 3 atau Praktik 5 (.ipynb), pastikan nama kernel di pojok kanan atas jendela kerja tertulis 'Python (Pelatihan SMART)'."
        ],
        box_type="warn"
    )
    
    doc.add_page_break()
    
    # -----------------------------------------------------------------
    # 5. PRAKTIK 1: MULTI-SOURCE DATA FUSION
    # -----------------------------------------------------------------
    add_h1(doc, "MODUL PRAKTIK 1: MULTI-SOURCE DATA FUSION")
    add_p(doc, "Penyelarasan Grid 10 m, Reproyeksi UTM Zone 49S, dan Pemotongan Poligon Area of Interest (AOI)", bold=True, color=COLOR_TERRACOTTA)
    
    add_callout(
        doc,
        "RINGKASAN KOMPETENSI PRAKTIK 1",
        [
            "Tujuan: Memberikan keterampilan dalam mengoreksi CRS, mere-sample DEM 30 m ke 10 m, menyelaraskan kisi matriks piksel, dan memotong raster mengikuti batas DAS.",
            "Kompetensi Khusus: Memeriksa EPSG:32749, menjalankan Align Rasters, mengeksekusi Clip Raster by Mask Layer, dan membangun berkas proyek QGIS portabel.",
            "Indikator Mutu: Seluruh raster memiliki ukuran piksel tepat 10.0 x 10.0 m, batas origin selaras dengan Sentinel-2, dan piksel di luar batas bernilai NoData transparan."
        ],
        box_type="curriculum"
    )
    
    add_h2(doc, "1. Bahan Data Olahan & Berkas Proyek QGIS")
    add_p(doc, "Seluruh data masukan telah disiapkan pada direktori: Output/Pelatihan/data/praktik-1/")
    
    p1_data = [
        ["Praktik_01_Multi_Source_Data_Fusion.qgz", "Proyek QGIS", "-", "Berkas proyek QGIS terkonfigurasi lengkap dengan symbology dan layer tree"],
        ["sentinel2_l2a_20250721_10m.tif", "Raster GeoTIFF", "10 m", "Kovariat spektral dan indeks vegetasi (B02 Blue, B03 Green, B04 Red, B08 NIR)"],
        ["sentinel1_rtc_20240830_10m.tif", "Raster GeoTIFF", "10 m", "Kovariat kekasaran permukaan dan kelembapan lantai tanah (SAR C-band VH & VV)"],
        ["copdem_glo30_30m.tif", "Raster GeoTIFF", "30 m", "Model Elevasi Digital asli Copernicus DEM GLO-30 (mdpl)"],
        ["batas_subdas.gpkg", "Vektor GPKG", "-", "Poligon batas Sub-DAS Bompon (luas 294.7 ha, perimeter 8.2 km)"]
    ]
    add_table_data(doc, ["Nama Berkas", "Tipe Data", "Resolusi", "Peran dalam Analisis Spasial"], p1_data, [5.5, 2.5, 2.0, 6.5])
    
    add_h2(doc, "2. Prosedur Langkah Kerja Praktik 1")
    add_p(doc, "Langkah 1: Membuka Berkas Proyek atau Menata Layer di QGIS", bold=True)
    add_p(
        doc,
        "Peserta dapat mengeklik ganda berkas proyek siap pakai 'Praktik_01_Multi_Source_Data_Fusion.qgz' di QGIS, "
        "atau menyusunnya secara mandiri: buat proyek baru, atur CRS kanvas ke EPSG:32749 (WGS 84 / UTM Zone 49S), "
        "lalu seret batas_subdas.gpkg dan atur garis tepi Outline Simple Line berwarna Crimson (#DC143C) dengan lebar 0.8 mm."
    )
    
    add_p(doc, "Langkah 2: Menampilkan Komposit True Color Sentinel-2 L2A", bold=True)
    add_p(
        doc,
        "Muat citra sentinel2_l2a_20250721_10m.tif. Buka Layer Properties -> Symbology -> Multiband color. "
        "Atur Red band: Band 3 (Red), Green band: Band 2 (Green), dan Blue band: Band 1 (Blue). "
        "Pilih rentang kontras Stretch to MinMax (Cumulative count cut 2% - 98%). Amati variabilitas tutupan lahan Sub-DAS Bompon."
    )
    add_image_figure(doc, "praktik_01_qgis_multisensor_overview.png", "Gambar 1.1: Tampilan komposit warna alami Sentinel-2 L2A (True Color RGB 4-3-2) terpotong rapi poligon batas Sub-DAS Bompon.")
    
    add_p(doc, "Langkah 3: Inspeksi Hamburan Balik Radar Sentinel-1 RTC SAR", bold=True)
    add_p(
        doc,
        "Aktifkan layer sentinel1_rtc_20240830_10m.tif. Kanal polarisasi silang (VH) merepresentasikan hamburan volume tajuk kanopi "
        "sedangkan kanal polarisasi sejajar (VV) sensitif terhadap kekasaran permukaan dan kelembapan lantai tanah. "
        "Perhatikan keunggulan gelombang mikro yang mampu menembus tutupan awan tipis dan kanopi parsial."
    )
    add_image_figure(doc, "praktik_01_qgis_sar_radar.png", "Gambar 1.2: Citra radar Sentinel-1 RTC SAR C-band polarisasi VH terpotong batas DAS, memperlihatkan tekstur permukaan lahan.")
    
    add_p(doc, "Langkah 4: Pemodelan Elevasi DEM dan Pemotongan Batas AOI", bold=True)
    add_p(
        doc,
        "Jalankan algoritma Raster -> Extraction -> Clip Raster by Mask Layer pada berkas DEM. "
        "Pilih batas_subdas.gpkg sebagai Mask layer, atur NoData value = -9999, dan pertahankan resolusi piksel 10 m. "
        "Atur simbologi Singleband pseudocolor dengan skema warna elevasi dari 300 mdpl (lembah hilir) hingga 620 mdpl (puncak hulu)."
    )
    add_image_figure(doc, "praktik_01_qgis_dem_elevation.png", "Gambar 1.3: Model Elevasi Digital (DEM) 10 m terklip batas DAS dengan skema warna pseudocolor topografi.")
    
    add_callout(
        doc,
        "CHECKPOINT MUTU PRAKTIK 1",
        [
            "1. Periksa Layer Properties -> Information pada ketiga raster: Pastikan Pixel Size = (10, -10) dan CRS = EPSG:32749.",
            "2. Gunakan Identify Results Tool di luar poligon merah batas DAS: Pastikan nilai piksel terbaca 'No Data' (transparan penuh).",
            "3. Pastikan tidak ada pergeseran posisi sub-piksel saat ketiga layer ditumpuk bergantian."
        ],
        box_type="succ"
    )
    
    doc.add_page_break()
    
    # -----------------------------------------------------------------
    # 6. PRAKTIK 2: DELINEASI SMU
    # -----------------------------------------------------------------
    add_h1(doc, "MODUL PRAKTIK 2: DELINEASI SATUAN PEMETAAN TANAH (SMU)")
    add_p(doc, "Analisis Kelerengan, Relief Bayangan (Hillshade), Komposit CIR, dan Batas Satuan Lahan", bold=True, color=COLOR_TERRACOTTA)
    
    add_callout(
        doc,
        "RINGKASAN KOMPETENSI PRAKTIK 2",
        [
            "Tujuan: Melatih peserta memahami hubungan geomorfologi-lereng terhadap genesis tanah serta mendigitasi poligon SMU berbasis kaidah katena.",
            "Kompetensi Khusus: Menghasilkan peta lereng derajat, mengonfigurasi komposit CIR (8-4-3), menerapkan batas delineasi terkecil (MLD 0.4 ha), dan membandingkan batas rujukan pakar.",
            "Kaidah Pedologi: Tanah di igir/puncak mengalami erosi lateral menghasilkan solum dangkal, sedangkan tanah di kaki lereng dan dataran aluvial memiliki solum tebal dan akumulasi C-organik tinggi."
        ],
        box_type="curriculum"
    )
    
    add_h2(doc, "1. Bahan Data Olahan & Berkas Proyek QGIS")
    p2_data = [
        ["Praktik_02_Delineasi_SMU.qgz", "Proyek QGIS", "Proyek siap pakai kelerengan, hillshade, CIR, dan bentuklahan rujukan"],
        ["copdem_10m.tif", "Raster GeoTIFF", "Model Elevasi Digital terselaraskan 10 m terpotong rapi batas DAS"],
        ["slope_10m.tif", "Raster GeoTIFF", "Peta kelerengan lereng medan kontinu dalam satuan derajat (0° s.d. >40°)"],
        ["hillshade_10m.tif", "Raster GeoTIFF", "Model bayangan relief bukit (Azimuth 315°, Altitude 45°)"],
        ["sentinel2_l2a_20250721_10m.tif", "Raster GeoTIFF", "Citra multispektral untuk komposit Color Infrared tajuk vegetasi"],
        ["bentuklahan_rujukan.gpkg", "Vektor GPKG", "Delineasi satuan bentuklahan rujukan hasil survei geomorfologi pakar"]
    ]
    add_table_data(doc, ["Nama Berkas", "Tipe Data", "Deskripsi Peran Data"], p2_data, [5.5, 2.5, 8.5])
    
    add_h2(doc, "2. Prosedur Langkah Kerja Praktik 2")
    add_p(doc, "Langkah 1: Analisis Kelerengan dan Visualisasi Hillshade Topografi", bold=True)
    add_p(
        doc,
        "Buka proyek 'Praktik_02_Delineasi_SMU.qgz'. Tempatkan layer hillshade_10m.tif di bawah layer slope_10m.tif. "
        "Atur transparansi layer slope sebesar 30-40% atau gunakan Blending mode 'Multiply'. "
        "Klasifikasikan kemiringan lereng ke dalam 5 kelas pedologi: 0-8° (Datar/Landai), 8-15° (Agak Curam), 15-25° (Curam), "
        "25-40° (Sangat Curam), dan >40° (Terjal Ekstrem)."
    )
    add_image_figure(doc, "praktik_02_qgis_slope_hillshade.png", "Gambar 2.1: Integrasi peta kelerengan 5 kelas warna spektral dengan model bayangan relief bukit (Hillshade 10 m).")
    
    add_p(doc, "Langkah 2: Pembuatan Komposit Color Infrared (CIR 8-4-3)", bold=True)
    add_p(
        doc,
        "Pada layer Sentinel-2, atur penataan kanal komposit inframerah semu (CIR): Red = Band 4 (NIR B08), "
        "Green = Band 3 (Red B04), dan Blue = Band 2 (Green B03). "
        "Pada komposit CIR, vegetasi berklorofil aktif memantulkan NIR sangat tinggi sehingga tampak berwarna merah membara, "
        "memudahkan delineasi pemisah antara kebun agroforestri rapat, lahan terbuka garapan, dan semak belukar."
    )
    add_image_figure(doc, "praktik_02_qgis_cir_composite.png", "Gambar 2.2: Komposit Color Infrared (CIR 8-4-3) tajuk vegetasi Sub-DAS Bompon.")
    
    add_p(doc, "Langkah 3: Delineasi Satuan Pemetaan Tanah (SMU) & Evaluasi MLD", bold=True)
    add_p(
        doc,
        "Lakukan digitasi poligon batas satuan pemetaan tanah dengan memanfaatkan snapping environment. "
        "Periksa batas rujukan pada bentuklahan_rujukan.gpkg. Pastikan luas setiap poligon yang didigitasi tidak lebih kecil "
        "dari luas batas keterbacaan kartografis minimum (Minimum Legible Delineation / MLD) skala 1:25.000, yaitu sebesar 0.4 hektar (4.000 m²)."
    )
    add_image_figure(doc, "praktik_02_qgis_smu_landform.png", "Gambar 2.3: Overlay satuan bentuklahan rujukan (SMU) hasil delineasi pakar pedologi di atas relief topografi.")
    
    doc.add_page_break()
    
    # -----------------------------------------------------------------
    # 7. PRAKTIK 3: PSS & KEMOMETRIKA
    # -----------------------------------------------------------------
    add_h1(doc, "MODUL PRAKTIK 3: DEMONSTRASI PROXIMAL SOIL SENSING (PSS)")
    add_p(doc, "Spektroskopi Pantulan Vis-NIR (350–2500 nm), Pra-Olah SNV, Savitzky–Golay, & Kalibrasi PLSR C-Organik", bold=True, color=COLOR_TERRACOTTA)
    
    add_callout(
        doc,
        "RINGKASAN KOMPETENSI PRAKTIK 3",
        [
            "Tujuan: Memberikan pemahaman fisis spektroskopi tanah proksimal dan keterampilan kemometrika estimasi cepat C-Organik secara non-destruktif.",
            "Kompetensi Khusus: Memuat spektra 852 sampel (2151 kanal), transformasi Absorbansi & SNV, turunan pertama Savitzky-Golay, dan evaluasi PLSR.",
            "Fitur Serapan Fisis C-Organik: Spektrum tanah kaya karbon organik tampak gelap (reflektansi rendah). Turunan pertama SNV mengisolasi puncak serapan kromofor bahan organik (SOM 450–650 nm) serta overton regangan ikatan C-H alifatik pada 1720 nm dan 2300 nm."
        ],
        box_type="curriculum"
    )
    
    add_h2(doc, "1. Bahan Data & Lingkungan Eksekusi Python")
    p3_data = [
        ["Praktik_03_Demonstrasi_PSS.qgz", "Proyek QGIS", "Visualisasi spasial 50 titik sampel lapangan PSS dan citra Sentinel-2"],
        ["Praktik_03_Demonstrasi_PSS_Kemometrika.ipynb", "Jupyter Notebook", "Notebook kemometrika lengkap siap eksekusi di kernel env_smart"],
        ["spektra_visnir_857sampel.csv", "Tabel Spektral CSV", "Dataset 852 sampel spektra kontinu 350–2500 nm resolusi 1 nm berpasangan uji lab C-Organik"],
        ["titik_sampel_lapangan.gpkg", "Vektor GPKG", "50 titik koordinat GPS pengambilan sampel tanah di Sub-DAS Bompon"]
    ]
    add_table_data(doc, ["Nama Berkas", "Tipe Berkas", "Deskripsi Peran"], p3_data, [6.0, 3.0, 7.5])
    
    add_h2(doc, "2. Prosedur Langkah Kerja Praktik 3")
    add_p(doc, "Langkah 1: Inspeksi Sebaran Titik Sampel PSS di QGIS", bold=True)
    add_p(
        doc,
        "Buka proyek 'Praktik_03_Demonstrasi_PSS.qgz'. Periksa sebaran spasial 50 titik sampel PSS (lingkaran emas bergaris tepi hitam) "
        "yang terdistribusi melintasi berbagai posisi lereng Sub-DAS Bompon, mulai dari puncak punggung bukit, lereng tengah, hingga dasar lembah."
    )
    add_image_figure(doc, "praktik_03_qgis_titik_sampel_pss.png", "Gambar 3.1: Sebaran spasial titik sampel lapangan PSS di atas citra Sentinel-2 L2A Sub-DAS Bompon.")
    
    add_p(doc, "Langkah 2: Menjalankan Notebook Kemometrika pada Virtual Environment (venv)", bold=True)
    add_p(
        doc,
        "Buka terminal, aktifkan virtual environment (source env_smart/bin/activate atau setup_env.bat), lalu jalankan 'jupyter lab'. "
        "Buka Praktik_03_Demonstrasi_PSS_Kemometrika.ipynb dan pastikan kernel aktif adalah 'Python (Pelatihan SMART)'. "
        "Jalankan Sel 1 s.d. 3 untuk memuat dataset 852 sampel dan menampilkan kurva reflektansi mentah (raw reflectance)."
    )
    add_image_figure(doc, "praktik_03_fig_1.png", "Gambar 3.2: Kurva spektrum reflektansi mentah Vis-NIR (350–2500 nm) 852 sampel tanah lapangan.")
    
    add_p(doc, "Langkah 3: Transformasi Pra-Olah Sinyal (SNV & Savitzky-Golay)", bold=True)
    add_p(
        doc,
        "Jalankan Sel 4 dan 5 untuk menerapkan Standard Normal Variate (SNV) guna menghilangkan efek hamburan cahaya akibat perbedaan ukuran partikel agregat tanah, "
        "diikuti filter Savitzky–Golay turunan pertama (orde polinomial 2, jendela 15 nm). "
        "Amati terbentuknya puncak serapan fisis diagnostik C-Organik pada panjang gelombang 450–650 nm (kromofor SOM) dan 1720 nm & 2300 nm (ikatan C-H)."
    )
    add_image_figure(doc, "praktik_03_fig_2.png", "Gambar 3.3: Kurva spektral setelah pra-olah SNV dan turunan pertama Savitzky-Golay dengan penanda serapan diagnostik C-Organik.")
    
    add_p(doc, "Langkah 4: Kalibrasi Model PLSR dan Evaluasi Metrik", bold=True)
    add_p(
        doc,
        "Jalankan Sel 6 dan 7 untuk melatih model Partial Least Squares Regression (PLSR) dengan 6 komponen laten. "
        "Evaluasi metrik kinerja model menghasilkan R² kalibrasi = 0.52, R² validasi = 0.48, RMSE = 0.45%, dan RPD = 1.39 (kategori model penyaring/screening yang baik)."
    )
    add_image_figure(doc, "praktik_03_fig_3.png", "Gambar 3.4: Diagram tebaran (scatter plot) kalibrasi dan validasi model PLSR prediksi kadar C-Organik (%).")
    
    doc.add_page_break()
    
    # -----------------------------------------------------------------
    # 8. PRAKTIK 4: BARE SOIL DETECTION
    # -----------------------------------------------------------------
    add_h1(doc, "MODUL PRAKTIK 4: BARE SOIL DETECTION & EXTRACTION")
    add_p(doc, "Ekstraksi Spektrum Tanah Terbuka Multitemporal, Ambang Biner BSI-NDVI, & Komposit Barest Earth", bold=True, color=COLOR_TERRACOTTA)
    
    add_callout(
        doc,
        "RINGKASAN KOMPETENSI PRAKTIK 4",
        [
            "Tujuan: Melatih peserta mengisolasi piksel tanah terbuka bebas gangguan kanopi vegetasi kelapa sawit/gulma menggunakan citra satelit dua musim.",
            "Kompetensi Khusus: Menghitung indeks NDVI dan Bare Soil Index (BSI), membuat masker biner tanah terbuka (merah/kuning), dan komposit Barest Earth.",
            "Rumus BSI: BSI = [ (SWIR1 + RED) - (NIR + BLUE) ] / [ (SWIR1 + RED) + (NIR + BLUE) ]. Tanah terbuka murni memiliki BSI positif (> 0.02) dan NDVI rendah (< 0.35)."
        ],
        box_type="curriculum"
    )
    
    add_h2(doc, "1. Bahan Data Olahan & Berkas Proyek QGIS")
    p4_data = [
        ["Praktik_04_Bare_Soil_Detection.qgz", "Proyek QGIS", "Proyek terkonfigurasi masker biner tanah terbuka 2 musim dan indeks BSI"],
        ["sentinel2_l2a_20240813_10m.tif", "Raster GeoTIFF", "Citra Sentinel-2 puncak kemarau (fase bera lahan, tanah terbuka maksimal)"],
        ["sentinel2_l2a_20250721_10m.tif", "Raster GeoTIFF", "Citra Sentinel-2 musim basah (vegetasi lebat menutup tanah)"],
        ["bsi_20240813.tif", "Raster GeoTIFF", "Peta Bare Soil Index hasil kalkulasi rasio spektral kemarau 2024"],
        ["masker_tanah_terbuka_20240813.tif", "Raster GeoTIFF", "Masker biner tanah terbuka kemarau 2024 (0: Bukan Tanah, 1: Tanah Terbuka)"],
        ["barest_earth_bsi_composite.tif", "Raster GeoTIFF", "Komposit piksel tanah paling terbuka dari rangkaian multitemporal"]
    ]
    add_table_data(doc, ["Nama Berkas", "Tipe Data", "Peran dalam Analisis"], p4_data, [6.0, 2.5, 8.0])
    
    add_h2(doc, "2. Prosedur Langkah Kerja Praktik 4")
    add_p(doc, "Langkah 1: Analisis Kontras Bare Soil Index (BSI) di QGIS", bold=True)
    add_p(
        doc,
        "Buka proyek 'Praktik_04_Bare_Soil_Detection.qgz'. Aktifkan layer bsi_20240813.tif. "
        "Simbologi pseudo-color memperlihatkan kontras tajam: piksel hijau pekat bernilai negatif (< -0.2) adalah kanopi rapat, "
        "sedangkan piksel merah terang bernilai positif (> +0.15) merupakan tanah terbuka garapan murni."
    )
    add_image_figure(doc, "praktik_04_qgis_bsi_map.png", "Gambar 4.1: Peta sebaran spasial Bare Soil Index (BSI) pada puncak musim kemarau di Sub-DAS Bompon.")
    
    add_p(doc, "Langkah 2: Pembuatan Masker Biner Tanah Terbuka", bold=True)
    add_p(
        doc,
        "Terapkan Raster Calculator dengan formula kondisi logika: (bsi_20240813@1 > 0.02) AND (ndvi_20240813@1 < 0.35). "
        "Hasil perhitungan menghasilkan masker biner dengan nilai 1 (Tanah Terbuka, disimbolkan merah pekat) "
        "dan nilai 0 (Bukan Tanah / Tertutup Kanopi, disetel transparan penuh)."
    )
    add_image_figure(doc, "praktik_04_qgis_masker_tanah_terbuka.png", "Gambar 4.2: Masker biner tanah terbuka (warna merah) menumpuk di atas citra Sentinel-2 L2A fase bera lahan.")
    
    doc.add_page_break()
    
    # -----------------------------------------------------------------
    # 9. PRAKTIK 5: MACHINE LEARNING DSM C-ORGANIK
    # -----------------------------------------------------------------
    add_h1(doc, "MODUL PRAKTIK 5: MACHINE LEARNING DIGITAL SOIL MAPPING (DSM)")
    add_p(doc, "Integrasi Kerangka SCORPAN, Algoritma Random Forest, Prediksi C-Organik 0–20 cm, & Ketidakpastian QRF (PI90)", bold=True, color=COLOR_TERRACOTTA)
    
    add_callout(
        doc,
        "RINGKASAN KOMPETENSI PRAKTIK 5 (PUNCAK PIPELINE)",
        [
            "Tujuan: Membangun peta digital kontinu C-Organik tanah lapisan 0–20 cm dan kuantifikasi batas keyakinan prediksi 90% (PI90).",
            "Kompetensi Khusus: Ekstraksi nilai 11 kovariat pada 50 titik sampel lab, validasi silang Random Forest 5-Fold, evaluasi peringkat variabel, pembuatan GeoTIFF kontinu, dan pemodelan interval QRF.",
            "Temuan Kritis C-Organik: Radar Sentinel-1 SAR VH (27.2%) dan Bare Soil Index BSI (13.4%) menduduki peringkat kepentingan teratas dalam mengendalikan sebaran spasial C-organik."
        ],
        box_type="curriculum"
    )
    
    add_h2(doc, "1. Bahan Data Olahan & Berkas Proyek QGIS")
    p5_data = [
        ["Praktik_05_Machine_Learning_DSM_C_Organik.qgz", "Proyek QGIS", "Proyek kartografi lengkap hasil pemodelan C-Organik dan kovariat SCORPAN"],
        ["Praktik_05_Machine_Learning_Digital_Soil_Mapping.ipynb", "Jupyter Notebook", "Notebook pemodelan machine learning Random Forest & QRF"],
        ["sampel_tanah_50titik.csv", "Tabel CSV", "Data uji laboratorium 50 sampel lapangan (Target: C_Organik_1 0–20 cm)"],
        ["titik_sampel_lapangan.gpkg", "Vektor GPKG", "50 titik koordinat georeferensi sampel tanah EPSG:32749"],
        ["prediksi_corganik_0_20cm.tif", "Raster GeoTIFF", "GeoTIFF kontinu estimasi C-Organik (%) lapisan 0–20 cm terpotong batas DAS"],
        ["ketidakpastian_pi90_corganik.tif", "Raster GeoTIFF", "GeoTIFF lebar interval prediksi keyakinan 90% (Quantile Forest)"],
        ["kovariat/", "Direktori Raster", "8 berkas raster kovariat SCORPAN 10 m (dem, slope, aspect, tpi, hillshade, sar, optik, lu)"]
    ]
    add_table_data(doc, ["Nama Berkas", "Tipe Berkas", "Deskripsi Peran"], p5_data, [6.0, 3.0, 7.5])
    
    add_h2(doc, "2. Prosedur Langkah Kerja Praktik 5")
    add_p(doc, "Langkah 1: Visualisasi Titik Sampel Graduated C-Organik di QGIS", bold=True)
    add_p(
        doc,
        "Buka proyek 'Praktik_05_Machine_Learning_DSM_C_Organik.qgz'. Periksa sebaran nilai laboratorium C_Organik_1 "
        "yang disimbolkan secara Graduated dalam 5 kelas warna tanah: < 0.6% (Sangat Rendah), 0.6–0.85% (Rendah), "
        "0.85–1.1% (Sedang), 1.1–1.3% (Tinggi), dan > 1.3% (Sangat Tinggi). Nilai rata-rata lapangan adalah 0.92% (stdev 0.31%)."
    )
    add_image_figure(doc, "praktik_05_qgis_titik_graduated_lempung.png", "Gambar 5.1: Sebaran 50 titik sampel lapangan dengan simbologi graduated kadar C-Organik lapisan 0–20 cm.")
    
    add_p(doc, "Langkah 2: Ekstraksi Kovariat SCORPAN & Pelatihan Random Forest", bold=True)
    add_p(
        doc,
        "Jalankan notebook Praktik_05_Machine_Learning_Digital_Soil_Mapping.ipynb pada kernel 'Python (Pelatihan SMART)'. "
        "Lakukan Point-in-Raster Overlay mengekstrak 11 kovariat lingkungan pada 50 titik koordinat sampel. "
        "Latih model Random Forest Regressor dengan 5-Fold Cross Validation. Model menghasilkan RMSE = 0.34% dan MAE = 0.28%."
    )
    add_image_figure(doc, "praktik_05_fig_1.png", "Gambar 5.2: Diagram evaluasi Random Forest 5-Fold Cross Validation dan peringkat kepentingan fitur (Feature Importance) prediksi C-Organik.")
    
    add_p(doc, "Langkah 3: Pemetaan Kontinu C-Organik & Ketidakpastian Prediksi PI90", bold=True)
    add_p(
        doc,
        "Ekspor hasil prediksi seluruh piksel valid Sub-DAS Bompon (29.469 piksel) menjadi berkas GeoTIFF 'prediksi_corganik_0_20cm.tif'. "
        "Selanjutnya jalankan Quantile Regression Forest (QRF) untuk menghitung persentil ke-5 (q05) dan persentil ke-95 (q95). "
        "Lebar interval keyakinan 90% (PI90 = q95 - q05) diekspor ke 'ketidakpastian_pi90_corganik.tif' untuk mengidentifikasi area dengan variabilitas ketidakpastian tinggi."
    )
    add_image_figure(doc, "praktik_05_qgis_prediksi_lempung.png", "Gambar 5.3: Peta digital kontinu hasil prediksi kadar C-Organik (%) lapisan 0–20 cm Sub-DAS Bompon.")
    add_image_figure(doc, "praktik_05_qgis_ketidakpastian_pi90.png", "Gambar 5.4: Peta sebaran ketidakpastian spasial (Lebar Interval Prediksi 90% / PI90 C-Organik).")
    
    add_callout(
        doc,
        "INTERPRETASI AGRONOMIS & OPERASIONAL PERKEBUNAN",
        [
            "1. Pengaruh Dominan Radar SAR VH (27.2%): Polarisasi silang C-band sangat peka terhadap biomassa tegakan dan akumulasi serasah organik di permukaan lantai kebun.",
            "2. Pengaruh BSI (13.4%) & Topografi (Aspect 12.8%, TPI 9.8%): Posisi lereng dan radiasi matahari mikro menentukan laju erosi dan dekomposisi bahan organik tanah.",
            "3. Zonasi Pemupukan Presisi: Area dengan estimasi C-Organik rendah (< 0.75%) dan ketidakpastian rendah diidentifikasi sebagai prioritas utama aplikasi amelioran organik (tandan kosong kelapa sawit / biochar)."
        ],
        box_type="succ"
    )
    
    doc.add_page_break()
    
    # -----------------------------------------------------------------
    # 10. EVALUASI MANDIRI PESERTA
    # -----------------------------------------------------------------
    add_h1(doc, "BAGIAN III: EVALUASI MANDIRI & LEMBAR KERJA PESERTA")
    add_p(
        doc,
        "Sebagai bentuk evaluasi pemahaman menyeluruh atas materi pelatihan, peserta diminta menyelesaikan lembar tugas aplikatif berikut:"
    )
    
    add_callout(
        doc,
        "TUGAS MANDIRI KELOMPOK: PERENCANAAN SAMPLING EFISIEN & ZONASI C-ORGANIK",
        [
            "1. Evaluasi Harmonisa Data: Jelaskan mengapa reproyeksi ke CRS terproyeksi (UTM Zone 49S) dan snap grid wajib dilakukan sebelum ekstraksi nilai piksel!",
            "2. Analisis Spektroskopi PSS: Sebutkan dua panjang gelombang diagnostik utama bahan organik tanah pada rentang SWIR dan jelaskan mekanisme serapan fisisnya!",
            "3. Optimasi Deteksi Tanah: Bandingkan luas area tanah terbuka terdeteksi pada musim kemarau 2024 vs musim basah 2025 di Sub-DAS Bompon!",
            "4. Mitigasi Ketidakpastian: Jika area igir bukit memiliki nilai ketidakpastian PI90 > 1.2%, strategi penambahan sampel lapangan seperti apa yang Anda rekomendasikan?"
        ],
        box_type="info"
    )
    
    doc.add_page_break()
    
    # -----------------------------------------------------------------
    # 11. GLOSARIUM & DAFTAR PUSTAKA
    # -----------------------------------------------------------------
    add_h1(doc, "BAGIAN IV: GLOSARIUM ISTILAH & DAFTAR PUSTAKA")
    
    add_h2(doc, "A. Glosarium Istilah Kunci")
    glosarium_data = [
        ["AOI", "Area of Interest; batas poligon wilayah geografis yang menjadi fokus analisis pemetaan."],
        ["BSI", "Bare Soil Index; rasio spektral penginderaan jauh untuk mengisolasi keberadaan tanah terbuka murni."],
        ["CIR", "Color Infrared; komposit citra semu inframerah (NIR-Red-Green) penegas vigor dan tajuk klorofil vegetasi."],
        ["DSM", "Digital Soil Mapping; pemetaan tanah digital berbasis model kuantitatif hubungan tanah-lingkungan."],
        ["MLD", "Minimum Legible Delineation; batas ukuran poligon terkecil yang dapat digambarkan secara kartografis (0.4 ha pada 1:25.000)."],
        ["PLSR", "Partial Least Squares Regression; metode regresi multivariat linier penangan multikolinearitas spektroskopi."],
        ["PSS", "Proximal Soil Sensing; teknologi pengukuran sifat tanah secara langsung pada jarak dekat menggunakan sensor fisik."],
        ["QRF", "Quantile Regression Forest; algoritma pohon regresi non-parametrik untuk memodelkan interval ketidakpastian prediksi spasial."],
        ["RPD", "Ratio of Performance to Deviation; rasio simpangan baku terhadap RMSE untuk menilai keandalan model spektroskopi."],
        ["RTC", "Radiometric Terrain Correction; koreksi radiometrik dan geometrik citra SAR akibat distorsi topografi medan."],
        ["SCORPAN", "Kerangka konseptual DSM: Soil = f(s: soil, c: climate, o: organisms, r: relief, p: parent material, a: age, n: spatial position)."],
        ["SNV", "Standard Normal Variate; algoritma pra-olah normalisasi kurva spektral per-sampel untuk eliminasi variasi hamburan fisik."],
        ["VRT", "Virtual Raster; berkas format XML GDAL yang menyatukan tumpukan lapisan raster tanpa menduplikasi data fisik."]
    ]
    add_table_data(doc, ["Singkatan / Istilah", "Definisi dan Penjelasan Konseptual"], glosarium_data, [4.0, 12.5])
    
    add_h2(doc, "B. Daftar Pustaka Standar Internasional")
    pustaka = [
        "Breiman, L. (2001). Random forests. Machine Learning, 45(1), 5-32.",
        "Diek, S., Fornallaz, F., Gosheva, S., Gubler, L., & Schulin, R. (2019). Barest Earth composite from Sentinel-2 time series for digital soil mapping. Geoderma, 350, 1-11.",
        "McBratney, A. B., Mendonça Santos, M. L., & Minasny, B. (2003). On digital soil mapping. Geoderma, 117(1-2), 3-52.",
        "Meinshausen, N. (2006). Quantile regression forests. Journal of Machine Learning Research, 7, 983-999.",
        "Riksen, M. J. P. M., et al. (2020). Soil erosion and organic carbon dynamics in tropical volcanic catchments: Bompon sub-watershed case study. Catena, 188, 104445.",
        "Riksen, M. J. P. M., et al. (2023). Soil spectroscopy and digital soil mapping for precision agriculture in Indonesia. Geoderma Regional, 32, e00612.",
        "Viscarra Rossel, R. A., & Behrens, T. (2010). Using data mining to model and understand soil diffuse reflectance spectra. Geoderma, 158(1-2), 46-59.",
        "Viscarra Rossel, R. A., Walvoort, D. J. J., McBratney, A. B., Janik, L. J., & Skjemstad, J. O. (2006). Visible, near infrared, mid infrared or VisNIR diffuse reflectance spectroscopy for simultaneous assessment of selected soil properties. European Journal of Soil Science, 57(3), 410-422."
    ]
    for p_ref in pustaka:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.space_before = Pt(3)
        p_item.paragraph_format.space_after = Pt(4)
        p_item.paragraph_format.left_indent = Inches(0.4)
        p_item.paragraph_format.first_line_indent = Inches(-0.4)
        p_item.paragraph_format.line_spacing = 1.15
        r_item = p_item.add_run(p_ref)
        r_item.font.name = FONT_FAMILY
        r_item.font.size = Pt(9.5)
        r_item.font.color.rgb = COLOR_CHARCOAL
        
    print(f"Menyimpan berkas DOCX ke: {OUTPUT_DOCX}")
    doc.save(OUTPUT_DOCX)
    
    # Simpan juga salinan di Output/ untuk kemudahan akses
    root_docx = os.path.join(BASE_DIR, "Output/Modul_Praktikum_Lengkap_RS_PSS_DSM.docx")
    doc.save(root_docx)
    print(f"Salinan berhasil disimpan ke: {root_docx}")
    print("\n=== SUKSES MEMBANGUN DOKUMEN WORD MODUL LENGKAP! ===")

if __name__ == "__main__":
    generate_docx()
