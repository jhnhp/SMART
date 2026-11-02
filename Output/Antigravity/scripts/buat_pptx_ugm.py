#!/usr/bin/env python3
"""
buat_pptx_ugm.py
Membangun file presentasi PowerPoint (.pptx) resmi Universitas Gadjah Mada (UGM)
berdasarkan naskah Markdown dan aset gambar modul.

Template acuan:
Source/(NEW) Template Presentasi UGM Opt-1 (Wide Size)_2026.pptx
"""

import os
import re
import sys
from PIL import Image
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

# Warna Resmi Identitas UGM & Visual Modul
COLOR_UGM_NAVY = RGBColor(1, 65, 107)      # #01416B - UGM Navy
COLOR_UGM_YELLOW = RGBColor(253, 212, 2)    # #FDD402 - UGM Gold/Yellow
COLOR_GOLD_ACCENT = RGBColor(180, 115, 30)  # #B4731E - Amber/Gold Eyebrow
COLOR_TEXT_MAIN = RGBColor(30, 41, 59)      # #1E293B - Slate dark body text
COLOR_TEXT_MUTED = RGBColor(100, 116, 139)  # #64748B - Slate caption / subtext
COLOR_WHITE = RGBColor(255, 255, 255)       # #FFFFFF
COLOR_LIGHT_GREY = RGBColor(226, 232, 240)  # #E2E8F0

TEMPLATE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    '..', 'Source', '(NEW) Template Presentasi UGM Opt-1 (Wide Size)_2026.pptx'
)
TEMPLATE_PATH = os.path.normpath(TEMPLATE_PATH)


def clean_latex(text):
    """Membersihkan notasi LaTeX dan mengonversinya menjadi representasi Unicode yang rapi."""
    if not text:
        return ""
    # Penggantian teks langsung
    text = text.replace(r'\mu\text{m}', 'µm')
    text = text.replace(r'\mum', 'µm')
    text = text.replace(r'\mu m', 'µm')
    text = text.replace(r'\mu', 'µ')
    text = text.replace(r'\rightarrow', '→')
    text = text.replace(r'\to', '→')
    text = text.replace(r'\le', '≤')
    text = text.replace(r'\ge', '≥')
    text = text.replace(r'\pm', '±')
    text = text.replace(r'\times', '×')
    text = text.replace(r'\approx', '≈')
    text = text.replace(r'\neq', '≠')
    text = text.replace(r'\lambda', 'λ')
    text = text.replace(r'\quad', ' ')
    text = text.replace(r'\;', ' ')
    text = text.replace(r'\,', ' ')
    text = text.replace(r'\%', '%')
    text = text.replace(r'\&', '&')
    text = text.replace(r'\_', '_')
    text = text.replace(r'\ ', ' ')
    
    # regex \text{...}, \mathrm{...}, \mathbf{...}, \mathit{...}
    text = re.sub(r'\\(?:text|mathrm|mathbf|mathit)\{([^}]+)\}', r'\1', text)
    # Hapus delimiter matematika $ ... $ dan $$ ... $$
    text = re.sub(r'\$\$([^\$]+)\$\$', r'\1', text)
    text = re.sub(r'\$([^\$]+)\$', r'\1', text)
    
    # Hapus escape karakter sisa jika ada
    text = text.replace('\\', '')
    return text.strip()


def parse_markdown(md_file):
    """Mengurai naskah markdown presentasi menjadi struktur data per slide."""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Ekstraksi metadata sesi
    pemateri_m = re.search(r'\*\*Pemateri:\*\*\s*(.+)', content)
    pemateri = pemateri_m.group(1).strip() if pemateri_m else ''
    
    institusi_m = re.search(r'\*\*Institusi:\*\*\s*(.+)', content)
    institusi = institusi_m.group(1).strip() if institusi_m else 'Universitas Gadjah Mada'

    # Pisahkan blok slide
    slide_chunks = [s for s in re.split(r'\n(?=### SLIDE\s+\d+:)', content) if s.strip().startswith('### SLIDE')]
    
    slides = []
    base_dir = os.path.dirname(md_file)
    
    for chunk in slide_chunks:
        header_m = re.search(r'### SLIDE\s+(\d+):\s*([^\n]+)', chunk)
        slide_num = int(header_m.group(1)) if header_m else 0
        header_title = header_m.group(2).strip() if header_m else ''
        
        # Kategori
        cat_m = re.search(r'\*\s*\*\*Kategori:\*\*\s*([^\n]+)', chunk)
        kategori = clean_latex(cat_m.group(1).strip()) if cat_m else ''
        
        # Judul & Subjudul
        if slide_num == 1:
            title_m = re.search(r'\*\s*\*\*Judul Utama:\*\*\s*([^\n]+)', chunk)
            title = clean_latex(title_m.group(1).strip()) if title_m else header_title
            
            sub_m = re.search(r'\*\s*\*\*Sub-judul:\*\*\s*([^\n]+)', chunk)
            subtitle = clean_latex(sub_m.group(1).strip()) if sub_m else ''
            
            ident_m = re.search(r'\*\s*\*\*Identitas:\*\*\s*([^\n]+)', chunk)
            identitas = clean_latex(ident_m.group(1).strip()) if ident_m else ''
        else:
            title_m = re.search(r'\*\s*\*\*Judul:\*\*\s*([^\n]+)', chunk)
            title = clean_latex(title_m.group(1).strip()) if title_m else header_title
            subtitle = ''
            identitas = ''
            
        # Gambar & Caption
        img_m = re.search(r'!\[([^\]]*)\]\(([^)]+)\)', chunk)
        if img_m:
            img_alt = clean_latex(img_m.group(1).strip())
            img_rel_path = img_m.group(2).strip()
            img_abs = os.path.normpath(os.path.join(base_dir, img_rel_path))
            if not os.path.exists(img_abs):
                img_abs = None
                caption = None
            else:
                # Cari caption khusus di bawah gambar (*Gambar X.X: ...*)
                cap_m = re.search(r'!\[[^\]]*\]\([^)]+\)\s*\n\s*\*([^*]+)\*', chunk)
                if cap_m:
                    caption = clean_latex(cap_m.group(1).strip())
                else:
                    caption = img_alt
        else:
            img_abs = None
            caption = None
            
        # Catatan Pemateri (Speaker Notes)
        notes_m = re.search(r'\*\s*\*\*Catatan Pemateri[^\*]*\*\*[:\s]*([\s\S]+?)(?=\n---|\Z)', chunk)
        notes = ''
        if notes_m:
            raw_notes = notes_m.group(1).strip()
            note_lines = []
            for nl in raw_notes.split('\n'):
                nl_clean = nl.strip()
                if nl_clean.startswith('>'):
                    nl_clean = nl_clean.lstrip('>').strip()
                if nl_clean.startswith('\"') and nl_clean.endswith('\"') and len(nl_clean) > 2:
                    nl_clean = nl_clean[1:-1].strip()
                if nl_clean:
                    note_lines.append(nl_clean)
            notes = clean_latex(' '.join(note_lines).replace('\"\"', '\"'))
            
        # Poin Paparan
        points_m = re.search(r'\*\s*\*\*Poin Paparan:\*\*([\s\S]*?)(?=\*\s*\*\*Catatan Pemateri|\n---|\Z)', chunk)
        points_lines = []
        if points_m:
            raw_pts = points_m.group(1).strip().split('\n')
            for pl in raw_pts:
                pl_str = pl.rstrip()
                if not pl_str.strip():
                    continue
                leading_spaces = len(pl_str) - len(pl_str.lstrip(' '))
                line_content = pl_str.strip()
                
                level = 0
                if leading_spaces >= 4:
                    level = 1
                if leading_spaces >= 8:
                    level = 2
                    
                cleaned_line = re.sub(r'^(?:[\*\-\+]|\d+\.)\s*', '', line_content)
                cleaned_line = clean_latex(cleaned_line)
                if cleaned_line:
                    points_lines.append((level, cleaned_line))
                    
        slides.append({
            'num': slide_num,
            'header': header_title,
            'kategori': kategori,
            'title': title,
            'subtitle': subtitle,
            'identitas': identitas,
            'img_path': img_abs,
            'caption': caption,
            'notes': notes,
            'points': points_lines
        })
        
    return pemateri, institusi, slides


def add_formatted_bullet(text_frame, line_text, level=0, is_first=False, font_size=Pt(13), font_name='Calibri'):
    """Menambahkan baris bullet point dengan pemformatan tebal (bold) untuk kata kunci."""
    p = text_frame.paragraphs[0] if is_first else text_frame.add_paragraph()
    p.space_after = Pt(5) if level == 0 else Pt(3)
    p.space_before = Pt(2) if level == 0 else Pt(0)
    
    # Bullet symbol
    if level == 0:
        bullet_sym = '•  '
        sub_size = font_size
    elif level == 1:
        bullet_sym = '    –  '
        sub_size = Pt(font_size.pt - 1.2)
    else:
        bullet_sym = '        ▪  '
        sub_size = Pt(font_size.pt - 2.0)
        
    # Run awalan bullet
    r_sym = p.add_run()
    r_sym.text = bullet_sym
    r_sym.font.name = font_name
    r_sym.font.size = sub_size
    r_sym.font.color.rgb = COLOR_UGM_NAVY if level == 0 else COLOR_TEXT_MUTED
    
    # Parse **bold**
    tokens = re.split(r'(\*\*[^*]+\*\*)', line_text)
    for tok in tokens:
        if not tok:
            continue
        run = p.add_run()
        run.font.name = font_name
        run.font.size = sub_size
        if tok.startswith('**') and tok.endswith('**') and len(tok) >= 4:
            run.text = tok[2:-2]
            run.font.bold = True
            run.font.color.rgb = COLOR_UGM_NAVY
        else:
            run.text = tok
            run.font.bold = False
            run.font.color.rgb = COLOR_TEXT_MAIN


def build_powerpoint(md_file, output_pptx):
    """Membangun file PPTX dari Markdown dengan template resmi UGM."""
    if not os.path.exists(TEMPLATE_PATH):
        raise FileNotFoundError(f"Template UGM tidak ditemukan di: {TEMPLATE_PATH}")
        
    pemateri, institusi, slides = parse_markdown(md_file)
    print(f"\n=======================================================")
    print(f"Membangun: {os.path.basename(output_pptx)}")
    print(f"Pemateri: {pemateri}")
    print(f"Total Slide: {len(slides)}")
    print(f"=======================================================")
    
    prs = pptx.Presentation(TEMPLATE_PATH)
    
    # 1. Konfigurasi Slide 1 (Cover Slide dari Slide 0 bawaan template)
    cover_data = slides[0]
    slide0 = prs.slides[0]
    
    for shape in slide0.shapes:
        # TextBox 357 (id 358) adalah Judul Utama di template
        if shape.shape_id == 358 or shape.name == 'TextBox 357':
            shape.top = Inches(1.85)
            shape.width = Inches(9.80)
            shape.height = Inches(2.30)
            tf = shape.text_frame
            tf.word_wrap = True
            tf.clear()
            p = tf.paragraphs[0]
            p.text = cover_data['title']
            p.font.name = 'Gama-Sans-Bold'
            p.font.size = Pt(30 if len(cover_data['title']) > 70 else 33)
            p.font.bold = True
            p.font.color.rgb = COLOR_UGM_YELLOW
            
        # TextBox 372 (id 373) adalah Sub-judul & Info Pemateri di template
        elif shape.shape_id == 373 or shape.name == 'TextBox 372':
            shape.left = Inches(0.56)
            shape.top = Inches(4.35)
            shape.width = Inches(9.00)
            shape.height = Inches(2.30)
            tf = shape.text_frame
            tf.word_wrap = True
            tf.clear()
            
            # Sub-judul
            p1 = tf.paragraphs[0]
            p1.text = cover_data['subtitle']
            p1.font.name = 'Gama-Sans-Regular'
            p1.font.size = Pt(15)
            p1.font.color.rgb = COLOR_WHITE
            p1.space_after = Pt(14)
            
            # Nama Pemateri
            p2 = tf.add_paragraph()
            p2.text = pemateri if pemateri else cover_data['identitas']
            p2.font.name = 'Gama-Sans-Bold'
            p2.font.size = Pt(15)
            p2.font.bold = True
            p2.font.color.rgb = COLOR_UGM_YELLOW
            p2.space_after = Pt(4)
            
            # Afiliasi & Kolaborasi
            p3 = tf.add_paragraph()
            p3.text = f"{institusi} & PT SMART Tbk"
            p3.font.name = 'Gama-Sans-Regular'
            p3.font.size = Pt(13)
            p3.font.color.rgb = COLOR_LIGHT_GREY
            
    # Catatan Pemateri Cover
    if cover_data['notes']:
        slide0.notes_slide.notes_text_frame.text = cover_data['notes']
        
    # 2. Hapus slide bawaan template index 1, 2, 3
    slide_ids = list(prs.slides._sldIdLst)
    for sldId in slide_ids[1:]:
        prs.part.drop_rel(sldId.rId)
        prs.slides._sldIdLst.remove(sldId)
        
    # 3. Bangun Slide 2 hingga Selesai menggunakan Layout 1 (Title and Content)
    layout_content = prs.slide_layouts[1]
    
    for s_idx, sdata in enumerate(slides[1:], start=2):
        slide = prs.slides.add_slide(layout_content)
        
        # Hapus Content Placeholder 2 bawaan layout agar bersih dan terkendali bebas
        if len(slide.placeholders) > 1:
            c_ph = slide.placeholders[1]
            sp_elem = c_ph._element
            sp_elem.getparent().remove(sp_elem)
            
        # Setup Judul Slide
        title_shape = slide.shapes.title
        title_shape.left = Inches(0.92)
        title_shape.top = Inches(0.35)
        title_shape.width = Inches(10.20)
        title_shape.height = Inches(1.35)
        
        tf_title = title_shape.text_frame
        tf_title.word_wrap = True
        tf_title.clear()
        
        # Eyebrow Kategori
        if sdata['kategori']:
            p_cat = tf_title.paragraphs[0]
            p_cat.text = sdata['kategori'].upper()
            p_cat.font.name = 'Calibri'
            p_cat.font.size = Pt(11)
            p_cat.font.bold = True
            p_cat.font.color.rgb = COLOR_GOLD_ACCENT
            p_cat.space_after = Pt(2)
            p_main = tf_title.add_paragraph()
        else:
            p_main = tf_title.paragraphs[0]
            
        p_main.text = sdata['title']
        p_main.font.name = 'Calibri'
        p_main.font.size = Pt(22 if len(sdata['title']) > 55 else 24)
        p_main.font.bold = True
        p_main.font.color.rgb = COLOR_UGM_NAVY
        
        # Setup Speaker Notes
        if sdata['notes']:
            slide.notes_slide.notes_text_frame.text = sdata['notes']
            
        # Tentukan Tata Letak Konten (Dengan Gambar vs Tanpa Gambar)
        has_image = bool(sdata['img_path'] and os.path.exists(sdata['img_path']))
        
        if has_image:
            # === LAYOUT 2 KOLOM (TEKS KIRI + GAMBAR KANAN) ===
            left_w = Inches(5.85)
            left_h = Inches(4.85)
            left_t = Inches(1.85)
            left_l = Inches(0.92)
            
            tb_left = slide.shapes.add_textbox(left_l, left_t, left_w, left_h)
            tf_body = tb_left.text_frame
            tf_body.word_wrap = True
            tf_body.margin_left = Inches(0)
            tf_body.margin_right = Inches(0)
            tf_body.margin_top = Inches(0)
            tf_body.margin_bottom = Inches(0)
            
            # Skala font adaptif berdasarkan jumlah butir paparan
            num_points = len(sdata['points'])
            if num_points <= 5:
                base_pt = Pt(13)
            elif num_points <= 8:
                base_pt = Pt(12)
            else:
                base_pt = Pt(11)
                
            for i, (lvl, pt_text) in enumerate(sdata['points']):
                add_formatted_bullet(tf_body, pt_text, level=lvl, is_first=(i == 0), font_size=base_pt)
                
            # Kolom Gambar Kanan
            col_right_l = Inches(7.05)
            max_img_w = Inches(5.35)
            max_img_h = Inches(4.15)
            
            try:
                with Image.open(sdata['img_path']) as img:
                    orig_w, orig_h = img.size
                aspect = orig_w / orig_h
                
                if (orig_w / max_img_w.inches) > (orig_h / max_img_h.inches):
                    final_w = max_img_w
                    final_h = Inches(max_img_w.inches / aspect)
                else:
                    final_h = max_img_h
                    final_w = Inches(max_img_h.inches * aspect)
                    
                img_left = col_right_l + Inches((max_img_w.inches - final_w.inches) / 2)
                img_top = Inches(1.85)
                
                slide.shapes.add_picture(sdata['img_path'], img_left, img_top, width=final_w, height=final_h)
                
                # Caption di bawah gambar
                if sdata['caption']:
                    cap_box = slide.shapes.add_textbox(col_right_l, img_top + final_h + Inches(0.08), max_img_w, Inches(0.65))
                    c_tf = cap_box.text_frame
                    c_tf.word_wrap = True
                    c_tf.margin_left = Inches(0)
                    c_tf.margin_right = Inches(0)
                    c_tf.margin_top = Inches(0)
                    c_p = c_tf.paragraphs[0]
                    c_p.text = sdata['caption']
                    c_p.font.name = 'Calibri'
                    c_p.font.size = Pt(9.5)
                    c_p.font.italic = True
                    c_p.font.color.rgb = COLOR_TEXT_MUTED
            except Exception as e:
                print(f"  [PERINGATAN] Gagal menyisipkan gambar pada slide {s_idx}: {e}")
                
        else:
            # === LAYOUT TANPA GAMBAR (1 KOLOM LEBAR ATAU 2 KOLOM TEKS) ===
            num_points = len(sdata['points'])
            
            if num_points >= 5:
                # Dua kolom teks seimbang
                mid = (num_points + 1) // 2
                col1_points = sdata['points'][:mid]
                col2_points = sdata['points'][mid:]
                
                # Kolom 1
                tb1 = slide.shapes.add_textbox(Inches(0.92), Inches(1.85), Inches(5.50), Inches(4.85))
                tf1 = tb1.text_frame
                tf1.word_wrap = True
                tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = Inches(0)
                for i, (lvl, pt_text) in enumerate(col1_points):
                    add_formatted_bullet(tf1, pt_text, level=lvl, is_first=(i == 0), font_size=Pt(12.5))
                    
                # Kolom 2
                tb2 = slide.shapes.add_textbox(Inches(6.85), Inches(1.85), Inches(5.50), Inches(4.85))
                tf2 = tb2.text_frame
                tf2.word_wrap = True
                tf2.margin_left = tf2.margin_right = tf2.margin_top = tf2.margin_bottom = Inches(0)
                for i, (lvl, pt_text) in enumerate(col2_points):
                    add_formatted_bullet(tf2, pt_text, level=lvl, is_first=(i == 0), font_size=Pt(12.5))
                    
            else:
                # Kolom lebar tunggal (Data-dense clean)
                tb_wide = slide.shapes.add_textbox(Inches(0.92), Inches(1.85), Inches(11.20), Inches(4.85))
                tf_wide = tb_wide.text_frame
                tf_wide.word_wrap = True
                tf_wide.margin_left = tf_wide.margin_right = tf_wide.margin_top = tf_wide.margin_bottom = Inches(0)
                for i, (lvl, pt_text) in enumerate(sdata['points']):
                    add_formatted_bullet(tf_wide, pt_text, level=lvl, is_first=(i == 0), font_size=Pt(14))

    # Pastikan direktori tujuan tersedia
    os.makedirs(os.path.dirname(os.path.abspath(output_pptx)), exist_ok=True)
    prs.save(output_pptx)
    print(f"-> Sukses tersimpan: {output_pptx} ({os.path.getsize(output_pptx):,} bytes)")


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pres_dir = os.path.join(base_dir, 'Presentasi')
    
    file_mappings = [
        ('PPT_01_Prof_Junun_Bagian_1-3.md', 'PPT_01_Prof_Junun_Bagian_1-3.pptx'),
        ('PPT_02_Dr_Anggri_Bagian_4_dan_6.md', 'PPT_02_Dr_Anggri_Bagian_4_dan_6.pptx'),
        ('PPT_03_Dr_Retnadi_Bagian_5.md', 'PPT_03_Dr_Retnadi_Bagian_5.pptx'),
        ('PPT_04_Pak_Pandu_Bagian_7.md', 'PPT_04_Pak_Pandu_Bagian_7.pptx'),
        ('PPT_05_Dr_Guruh_Bagian_8.md', 'PPT_05_Dr_Guruh_Bagian_8.pptx'),
    ]
    
    print("================================================================")
    print("MEMULAI GENERASI 5 FILE PRESENTASI RESMI UGM (WIDE SIZE 16:9)")
    print("================================================================")
    
    for md_name, pptx_name in file_mappings:
        md_path = os.path.join(pres_dir, md_name)
        pptx_path = os.path.join(pres_dir, pptx_name)
        if not os.path.exists(md_path):
            print(f"[ERROR] Berkas markdown {md_name} tidak ditemukan!")
            continue
        build_powerpoint(md_path, pptx_path)

    print("\n================================================================")
    print("SELURUH 5 BERKAS PRESENTASI BERHASIL DIBANGUN LENGKAP!")
    print("================================================================")


if __name__ == '__main__':
    main()
