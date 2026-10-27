#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Deck Paparan Eksternal Dirreskrimsus Polda Sulsel (Versi Operasional Lapangan).
Workshop OVO & OVO Finansial - Makassar, 22 Oktober 2026.
Bebas AI-slop: Kalimat lugas, fokus fakta teknis penyidikan siber/fismondev,
dan dasar hukum positif terverifikasi (KUHP 2023, KUHAP 2025, UU 1/2026, UU ITE 2024, POJK, PBI).
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

NAVY  = RGBColor(0x0A, 0x19, 0x2F)   # 10, 25, 47 Deep Navy
BLUE  = RGBColor(0x1B, 0x3B, 0x6F)   # 27, 59, 111 Slate Blue
RED   = RGBColor(0xBA, 0x1A, 0x1A)   # 186, 26, 26 Crimson
GOLD  = RGBColor(0xD4, 0xAF, 0x37)   # 212, 175, 55 Gold
DARK  = RGBColor(0x11, 0x18, 0x27)   # 17, 24, 39 Off-Black
GREY  = RGBColor(0x4B, 0x55, 0x63)   # 75, 85, 99 Cool Grey
BG_BOX= RGBColor(0xF3, 0xF4, 0xF6)   # 243, 244, 246 Light Grey
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
PALE  = RGBColor(0xC7, 0xD3, 0xE0)
FONT  = "Tahoma"

FOOTER_TEXT = "DITRESKRIMSUS POLDA SULSEL  |  WORKSHOP TERTUTUP OVO & OVO FINANSIAL  |  MAKASSAR, 22 OKT 2026"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

def rect(slide, l, t, w, h, fill, shape=MSO_SHAPE.RECTANGLE):
    sh = slide.shapes.add_shape(shape, Inches(l), Inches(t), Inches(w), Inches(h))
    sh.shadow.inherit = False
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    sh.line.fill.background()
    return sh

def textbox(slide, l, t, w, h):
    tf = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h)).text_frame
    tf.word_wrap = True
    return tf

def put(tf, text, size=14, color=DARK, bold=False, align=PP_ALIGN.LEFT, space_after=6, first=False, line_spacing=1.0):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    p.space_after = Pt(space_after)
    p.line_spacing = line_spacing
    r = p.add_run()
    r.text = text
    r.font.name = FONT
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = color
    return p

def bullets(tf, items, first=True):
    started = False
    for it in items:
        level, text = it[0], it[1]
        size = it[2] if len(it) > 2 else 15
        bold = it[3] if len(it) > 3 else False
        color = it[4] if len(it) > 4 else DARK
        p = tf.paragraphs[0] if (first and not started) else tf.add_paragraph()
        started = True
        p.space_after = Pt(8 if level == 0 else 4)
        p.line_spacing = 1.05
        prefix = "•  " if level == 0 else "   -  "
        r = p.add_run()
        r.text = prefix + text
        r.font.name = FONT
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = color

def header(slide, tracker, title):
    rect(slide, 0, 0, 13.333, 0.15, RED)
    rect(slide, 0, 0.15, 13.333, 1.1, NAVY)
    tf = textbox(slide, 0.6, 0.22, 12.1, 0.95)
    put(tf, tracker.upper(), size=11, color=GOLD, bold=True, space_after=2, first=True)
    put(tf, title, size=24, color=WHITE, bold=True, space_after=0, line_spacing=0.95)

def footer(slide, num):
    tf = textbox(slide, 0.6, 7.02, 10.5, 0.35)
    put(tf, FOOTER_TEXT, size=8.5, color=GREY, space_after=0, first=True)
    tf_num = textbox(slide, 12.0, 7.02, 0.7, 0.35)
    put(tf_num, str(num), size=10, color=NAVY, bold=True, align=PP_ALIGN.RIGHT, space_after=0, first=True)

def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text

def table(slide, rows, left, top, width, col_w, font_size=11, header_size=11, row_h=0.55, head_h=0.45):
    nr, nc = len(rows), len(rows[0])
    total_h = head_h + row_h * (nr - 1)
    shape = slide.shapes.add_table(nr, nc, Inches(left), Inches(top), Inches(width), Inches(total_h))
    tbl = shape.table
    total_w = sum(col_w)
    for i, cw in enumerate(col_w):
        tbl.columns[i].width = Emu(int(Inches(width) * cw / total_w))
    tbl.rows[0].height = Inches(head_h)
    for r in range(1, nr):
        tbl.rows[r].height = Inches(row_h)
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            cell = tbl.cell(r, c)
            cell.margin_left = Inches(0.08)
            cell.margin_right = Inches(0.08)
            cell.margin_top = Inches(0.04)
            cell.margin_bottom = Inches(0.04)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            cell.fill.fore_color.rgb = BLUE if r == 0 else (BG_BOX if r % 2 else WHITE)
            p = cell.text_frame.paragraphs[0]
            p.space_after = Pt(0)
            r_run = p.add_run()
            r_run.text = str(val)
            r_run.font.name = FONT
            r_run.font.size = Pt(header_size if r == 0 else font_size)
            r_run.font.bold = (r == 0)
            r_run.font.color.rgb = WHITE if r == 0 else DARK

# ==================== SLIDE 1: COVER ====================
s1 = prs.slides.add_slide(BLANK)
rect(s1, 0, 0, 13.333, 7.5, NAVY)
rect(s1, 0, 0, 13.333, 0.2, RED)
rect(s1, 0.8, 1.2, 1.8, 0.08, GOLD)
tf1 = textbox(s1, 0.8, 1.5, 11.7, 3.2)
put(tf1, "WORKSHOP TERTUTUP APU-PPT — PT VISIONET INTERNASIONAL & PT INDONUSA BARA SEJAHTERA", size=12, color=GOLD, bold=True, space_after=12, first=True)
put(tf1, "PENEGAKAN HUKUM KEJAHATAN KEUANGAN SIBER:", size=32, color=WHITE, bold=True, space_after=4, line_spacing=0.95)
put(tf1, "Eksploitasi AI, Anomali QRIS, dan Mitigasi Sistemik PJP", size=26, color=WHITE, bold=False, space_after=16, line_spacing=0.95)
put(tf1, "Perspektif Teknis dan Yuridis Ditreskrimsus Polda Sulawesi Selatan", size=15, color=RGBColor(0xC7, 0xD3, 0xE0), space_after=0)

tf1_sub = textbox(s1, 0.8, 5.0, 11.7, 1.8)
put(tf1_sub, "Narasumber: Kombes Pol Taufik Herdiansyah — Direktur Reserse Kriminal Khusus Polda Sulsel", size=14, color=WHITE, bold=True, space_after=6, first=True)
put(tf1_sub, "Tempat / Waktu: Hotel Hyatt Place Makassar  |  Kamis, 22 Oktober 2026, Pukul 14.25 – 15.10 WITA", size=13, color=PALE, space_after=6)
put(tf1_sub, "Rujukan: Surat Undangan No. 338/PA-VI/C/IX/2026  |  Audiens: Divisi AML, Compliance, Public Affairs OVO", size=11, color=GREY, space_after=0)
notes(s1, "Selamat siang rekan-rekan direksi dan divisi kepatuhan OVO & OVO Finansial. "
          "Sesi Ditreskrimsus Polda Sulsel berdurasi 45 menit. Fokus paparan: membedah anatomi riil kejahatan siber finansial yang kami tangani di Makassar, "
          "bagaimana sindikat mengeksploitasi celah QRIS dan e-KYC, dasar hukum positif yang berlaku, serta 4 rekomendasi taktis agar kerja sama APH dan PJP dapat mengunci pergerakan pelaku secara real-time.")

# ==================== SLIDE 2: EXECUTIVE SUMMARY ====================
s2 = prs.slides.add_slide(BLANK)
header(s2, "Executive Briefing", "Ringkasan Eksekutif: 3 Titik Kritis Lapangan")
top_card = 1.65
card_w = 3.8
card_h = 4.9
gap = 0.35
c_data = [
    ("1. PERGESERAN MODUS", "Konsentrasi ke QRIS Mikro", 
     [("Pola aliran dana beralih dari transaksi besar antar-bank ke jutaan transaksi mikro.", 13),
      ("QRIS mendominasi 87,6% – 88,6% frekuensi deposit ilegal (data PPATK 2026).", 13),
      ("Filter statis (rule-based threshold >Rp100jt) mati kutu menghadapi pemecahan saldo bernilai kecil.", 13)]),
    ("2. INDUSTRIALISASI SIBER", "Botnet & AI di Makassar", 
     [("Sindikat beroperasi mandiri di daerah menggunakan model Cybercrime-as-a-Service (CaaS).", 13),
      ("Pengungkapan Polda Sulsel: >2.000 akun bot, 180 situs aktif, dan device farm emulator.", 13),
      ("Serangan bypass e-KYC berevolusi dari rekaman fisik ke injeksi kamera virtual langsung ke API.", 13)]),
    ("3. BOTTLENECK YURIDIS", "Kesenjangan Waktu Eksekusi", 
     [("Dana hasil kejahatan dikuras dan ditarik tunai dalam hitungan menit.", 13),
      ("Birokrasi pemblokiran konvensional membutuhkan waktu berhari-hari.", 13),
      ("KUHAP 2025 Pasal 140 ayat (7)-(9) memberi wewenang blokir seketika; butuh SOP teknis 2 jam bersama PJP.", 13)])
]
for i, (kicker, title, b_list) in enumerate(c_data):
    cx = 0.6 + i * (card_w + gap)
    rect(s2, cx, top_card, card_w, card_h, BG_BOX, MSO_SHAPE.ROUNDED_RECTANGLE)
    rect(s2, cx, top_card, card_w, 0.1, RED if i==2 else BLUE)
    tf_c = textbox(s2, cx + 0.2, top_card + 0.25, card_w - 0.4, card_h - 0.4)
    put(tf_c, kicker, size=11, color=RED if i==2 else BLUE, bold=True, space_after=3, first=True)
    put(tf_c, title, size=17, color=NAVY, bold=True, space_after=14)
    for txt, sz in b_list:
        p_c = tf_c.add_paragraph()
        p_c.space_after = Pt(8)
        p_c.line_spacing = 1.05
        r_c = p_c.add_run()
        r_c.text = "• " + txt
        r_c.font.name = FONT
        r_c.font.size = Pt(sz)
        r_c.font.color.rgb = DARK
footer(s2, 2)
notes(s2, "Tiga poin ini adalah peta navigasi diskusi kita hari ini. Pertama, pelaku tahu sistem perbankan memantau transaksi besar, "
          "sehingga mereka memecah transaksi menjadi puluhan ribu transaksi kecil via QRIS. Kedua, mereka menggunakan infrastruktur otomatisasi canggih "
          "di level daerah. Ketiga, hambatan hukum terbesar bukan ketiadaan pasal, melainkan 'speed gap' antara kecepatan bot pelaku dengan birokrasi surat blokir.")

# ==================== SLIDE 3: DATA PPATK & ANOMALI QRIS ====================
s3 = prs.slides.add_slide(BLANK)
header(s3, "Fakta Makro", "Dinamika Transaksi Mencurigakan: Ledakan Kanal QRIS")
top_m = 1.55
m_w = 2.8
m_h = 1.8
m_gap = 0.3
metrics = [
    ("Rp 86,82 T", "Perputaran Dana Judol\n(Semester I-2026)", "Melambat (-12,9%) vs periode lalu (-43%). Indikasi adaptasi modus."),
    ("87,6% – 88,6%", "Pangsa Deposit via QRIS", "Lonjakan mutlak. Kanal transfer rekening bank terpangkas tinggal 11,4%."),
    ("Rp 12,36 T", "Akumulasi Deposit QRIS\n(Triwulan I-2026)", "Likuiditas deposit ilegal terkonsentrasi masif di gerbang pembayaran mikro PJP."),
    ("1,49 Juta", "KPM Bansos Ditangguhkan", "Dampak sosial masif: identitas warga rentan dicatut joki rekening & merchant.")
]
for i, (val, lbl, note_m) in enumerate(metrics):
    mx = 0.6 + i * (m_w + m_gap)
    rect(s3, mx, top_m, m_w, m_h, NAVY, MSO_SHAPE.ROUNDED_RECTANGLE)
    tf_m = textbox(s3, mx + 0.15, top_m + 0.2, m_w - 0.3, m_h - 0.3)
    put(tf_m, val, size=24, color=GOLD, bold=True, align=PP_ALIGN.CENTER, space_after=3, first=True)
    put(tf_m, lbl, size=11, color=WHITE, bold=True, align=PP_ALIGN.CENTER, space_after=0)
    
    # Sub text below card
    tf_sub = textbox(s3, mx, top_m + m_h + 0.15, m_w, 1.2)
    put(tf_sub, note_m, size=11, color=GREY, space_after=0, first=True)

# Bottom Takeaway Box
rect(s3, 0.6, 4.95, 12.13, 1.85, BG_BOX, MSO_SHAPE.ROUNDED_RECTANGLE)
rect(s3, 0.6, 4.95, 0.1, 1.85, RED)
tf_take = textbox(s3, 0.9, 5.05, 11.6, 1.7)
put(tf_take, "ANALISIS INTELIJEN KEUANGAN (PPATK 2026):", size=13, color=RED, bold=True, space_after=3, first=True)
bullets(tf_take, [
    (0, "Penurunan nilai total transaksi yang melambat mengonfirmasi terjadinya resiliensi operasional sindikat.", 12),
    (0, "Sistem pembayaran mikro nirsentuh dimanfaatkan karena faktor interoperabilitas instan, nama merchant kamuflase, dan instant settlement.", 12),
    (0, "Pelaku tidak lagi memindahkan uang secara vertikal (bank to bank), melainkan secara horizontal menyebar melalui ribuan merchant QRIS.", 12)
], first=False)
footer(s3, 3)
notes(s3, "Bapak Ibu dari AML OVO, perhatikan angka 88,6%. Mengapa sindikat beralih ke QRIS? "
          "Karena QRIS menutupi identitas penerima asli di layar pengguna — yang tampil hanya nama warung fiktif seperti 'Kopi Berkah' atau 'Toko Pulsa Jaya'. "
          "Selain itu ada fitur instant settlement, sehingga begitu korban atau pemain menyetor dana, saldo otomatis cair dan langsung diputar sebelum audit bank berjalan.")

# ==================== SLIDE 4: STUDI KASUS MAKASSAR ====================
s4 = prs.slides.add_slide(BLANK)
header(s4, "Fakta Lapangan", "Studi Kasus Polda Sulsel: Sindikat Botnet 2.000 Akun Makassar")
tf_top4 = textbox(s4, 0.6, 1.5, 12.13, 1.1)
put(tf_top4, "Penindakan Subdit V Siber Ditreskrimsus Polda Sulsel mengungkap fasilitas peternakan peranti (device farm) aktif di Kota Makassar yang mengendalikan 180 situs dan mengoperasikan >2.000 akun bot otomatis.", size=14, color=DARK, bold=True, space_after=0, first=True)

steps = [
    ("1. DEVICE FARM & SPOOFING", "Ribuan emulator perangkat ponsel dioperasikan paralel. Skrip memanipulasi IMEI, MAC Address, resolusi layar, dan canvas fingerprinting.", "Status: Unik di mata PJP"),
    ("2. ROTASI JARINGAN", "Trafik dilewatkan VPN komersial dan IP Residensial lokal Sulsel secara dinamis. Menghilangkan pola koneksi anomali terpusat.", "Status: Bypass Anti-DDoS"),
    ("3. OTOMASI TRANSAKSI", "Konsol kendali tunggal memerintahkan bot login, verifikasi saldo, dan eksekusi deposit secara simultan tanpa campur tangan manusia.", "Status: Kecepatan Robotik"),
    ("4. SMURFING & STRUCTURING", "Dana mikro dialirkan ke ratusan rekening penampung sementara (skema many-to-one), dijaga di bawah ambang pelaporan TKM.", "Status: Lolos Threshold"),
    ("5. PENCAIRAN TUNAI CEPAT", "Saldo dialihkan (one-to-many) ke rekening joki/e-wallet, lalu ditarik tunai di agen laku pandai dan ATM regional Makassar & sekitarnya.", "Status: Saldo Lenyap")
]
w_st = 2.25
gap_st = 0.22
top_st = 2.8
for i, (st_t, st_d, st_tag) in enumerate(steps):
    sx = 0.6 + i * (w_st + gap_st)
    rect(s4, sx, top_st, w_st, 3.8, BG_BOX, MSO_SHAPE.ROUNDED_RECTANGLE)
    rect(s4, sx, top_st, w_st, 0.45, BLUE)
    tf_h = textbox(s4, sx + 0.08, top_st + 0.08, w_st - 0.16, 0.35)
    put(tf_h, f"TAHAP {i+1}", size=11, color=WHITE, bold=True, align=PP_ALIGN.CENTER, space_after=0, first=True)
    
    tf_b = textbox(s4, sx + 0.12, top_st + 0.55, w_st - 0.24, 2.5)
    put(tf_b, st_t, size=11.5, color=NAVY, bold=True, space_after=6, first=True)
    put(tf_b, st_d, size=10.5, color=DARK, space_after=0, line_spacing=1.05)
    
    # Tag bottom
    rect(s4, sx + 0.1, top_st + 3.25, w_st - 0.2, 0.4, WHITE)
    tf_tag = textbox(s4, sx + 0.1, top_st + 3.3, w_st - 0.2, 0.3)
    put(tf_tag, st_tag, size=9.5, color=RED, bold=True, align=PP_ALIGN.CENTER, space_after=0, first=True)

footer(s4, 4)
notes(s4, "Ini bukan teori, ini hasil penggerebekan fisik penyidik kami di Makassar. "
          "Pelaku tidak lagi menggunakan 10 orang mengetik manual di laptop. Mereka punya rak-rak server mini berisi ribuan emulator Android. "
          "Setiap emulator punya nomor IMEI palsu dan seolah-olah berlokasi di kecamatan-kecamatan berbeda di Sulsel karena menggunakan IP residensial. "
          "Dari ribuan bot ini, uang mengalir ke akun penampung, lalu ditarik tunai lewat agen laku pandai di pinggiran Makassar.")

# ==================== SLIDE 5: VEKTOR EKSPLOITASI AI & E-KYC ====================
s5 = prs.slides.add_slide(BLANK)
header(s5, "Modus Siber Lanjutan", "Vektor AI: Meretas Pintu Masuk e-KYC dan Merchant")
rows_s5 = [
    ["Vektor Serangan", "Metode Operasional Pelaku", "Celah Kerentanan PJP", "Langkah Konter Siber"],
    ["Digital Injection Attack", "Rooting peranti & injeksi driver virtual camera ke data pipeline API", "Aplikasi mempercayai input kamera tanpa cek integritas biner", "Client attestation, deteksi emulator, TLS pinning"],
    ["Deepfake Real-Time", "Sintesis wajah ekspresif berbasis GANs (gerak mata, mulut, gestur kepala)", "Verifikasi liveness pasif konvensional gagal baca artefak AI", "Analisis spektral pixel & tantangan gestur acak 3D"],
    ["Identitas Sintetik", "Kombinasi NIK valid bocor + foto wajah sintetis rekayasa AI", "Verifikasi OCR Dukcapil cocok, namun data foto tidak terikat NFC", "Validasi kriptografis chip e-KTP melalui sensor NFC"],
    ["Dormant Takeover", "Mengambil alih akun nasabah pasif melalui rekayasa prosedur re-KYC", "Akun lama punya trust-score tinggi & lolos fraud filter awal", "Analisis biometrik perilaku & deteksi lonjakan histori"],
    ["Merchant Fiktif QRIS", "Mendirikan PT cangkang/kios sembako palsu via merchant aggregator", "Uji tuntas pedagang (KYM) formalitas tanpa audit fisik/lapangan", "Penerapan velocity ceiling 30 hari & freeze auto-settle"]
]
table(s5, rows_s5, left=0.6, top=1.65, width=12.13, col_w=[2.2, 3.8, 3.2, 2.93], font_size=10, header_size=10.5, row_h=0.85, head_h=0.45)
footer(s5, 5)
notes(s5, "Tabel ini membedah bagaimana AI digunakan pelaku. Serangan paling berbahaya hari ini adalah Digital Injection. "
          "Pelaku tidak lagi menodongkan HP ke foto di layar laptop (presentation attack), tapi membypass hardware kamera dengan driver virtual. "
          "Data video deepfake disuntik langsung ke API verifikasi aplikasi OVO. Jika sistem PJP tidak memvalidasi integritas biner aplikasi (client attestation), "
          "sistem akan tertipu 100% dan menganggap verifikasi tersebut sah.")

# ==================== SLIDE 6: DASAR HUKUM PIDANA MATERIIL ====================
s6 = prs.slides.add_slide(BLANK)
header(s6, "Konstruksi Hukum", "Dasar Hukum Pidana Materiil Pasca UU 1/2026")
rows_s6 = [
    ["Regulasi & Pasal", "Perbuatan Pidana / Kualifikasi Delik", "Ancaman Pidana Pasca Penyesuaian UU 1/2026", "Status Harmonisasi"],
    ["KUHP (UU 1/2023)\nPasal 332", "Akses Ilegal: Mengakses sistem elektronik milik orang lain tanpa hak / menerobos pengamanan", "Penjara maks. 6–8 tahun atau denda Kategori V–VI (s.d. Rp2 Miliar)", "Pengalihan resmi dari ex Ps. 30 jo. 46 UU ITE (Lampiran KUHP Ps. 622)"],
    ["KUHP (UU 1/2023)\nPasal 258 ayat (2)", "Penyadapan & Intersepsi: Menyiarkan atau menyebarluaskan hasil intersepsi transmisi elektronik", "Penjara paling lama 10 tahun atau denda Kategori VI", "Pengalihan resmi dari ex Ps. 31 jo. 47 UU ITE"],
    ["KUHP (UU 1/2023)\nPasal 426", "Perjudian: Menawarkan, memberi kesempatan main judi sebagai mata pencaharian", "Penjara paling lama 9 tahun atau denda Kategori VI (Rp2 Miliar)", "Lex generalis penjerat pengelola & fasilitas perjudian"],
    ["UU ITE (UU 1/2024)\nPs. 27 (2) jo. 45 (3)", "Muatan Perjudian: Mendistribusikan / membuat dapat diaksesnya dokumen elektronik judi", "Penjara paling lama 10 tahun dan/atau denda paling banyak Rp 10 Miliar", "Tetap berlaku mandiri (tidak dicabut KUHP, ancaman diperberat)"],
    ["KUHP (UU 1/2023)\nPasal 492 & 486", "Penipuan (nama palsu, tipu muslihat) & Penggelapan dana nasabah", "Penjara paling lama 4 tahun atau denda Kategori V / Kategori IV", "Menjerat joki rekening, merchant fiktif, & perantara bayangan"],
    ["KUHP (UU 1/2023)\nPasal 607 & 608", "TPPU: Menempatkan, mentransfer, menyamarkan harta hasil tindak pidana", "Penjara maks. 15 tahun & denda Kategori VII. Ps. 608: Proteksi pelapor APU-PPT", "Kodifikasi materiil ex Ps. 3, 4, 5 UU 8/2010. PJP pelapor dilindungi hukum"]
]
table(s6, rows_s6, left=0.6, top=1.55, width=12.13, col_w=[2.2, 3.7, 3.2, 3.03], font_size=9.5, header_size=10.5, row_h=0.7, head_h=0.45)
footer(s6, 6)
notes(s6, "Bapak Ibu, per 2 Januari 2026, KUHP Nasional UU 1/2023 dan UU Penyesuaian Pidana UU 1/2026 resmi berlaku penuh. "
          "Perhatikan: Pasal 30 UU ITE tentang illegal access dan Pasal 31 tentang intersepsi sudah dicabut dan dialihkan ke Pasal 332 dan 258 KUHP. "
          "Namun untuk konten judi online, Pasal 27 ayat (2) jo. Pasal 45 ayat (3) UU 1/2024 tetap berlaku dengan denda hingga Rp10 Miliar. "
          "Kabar baik untuk OVO: Pasal 608 KUHP secara eksplisit melindungi PJP pelapor dari jeratan pidana pencucian uang saat melaporkan TKM.")

# ==================== SLIDE 7: HUKUM ACARA & PEMBLOKIRAN CEPAT ====================
s7 = prs.slides.add_slide(BLANK)
header(s7, "Instrumen Penyidik", "Hukum Acara: Mandat Pemblokiran Mendasar KUHAP 2025")
rows_s7 = [
    ["Dasar Hukum Acara", "Kewenangan Penyidik", "Ketentuan Operasional & Syarat Batas Waktu"],
    ["KUHAP (UU 20/2025)\nPasal 140 ayat (1)–(6)", "Pemblokiran Rekening & Aset oleh Penyidik", "Wajib izin Ketua Pengadilan Negeri; jangka waktu 1 tahun, dapat diperpanjang 2x6 bulan."],
    ["KUHAP (UU 20/2025)\nPasal 140 ayat (7)–(9)", "Pemblokiran Dalam Keadaan Mendesak (Emergency Freeze)", "DAPAT DILAKUKAN TANPA IZIN PENGADILAN. Syarat: (a) potensi dialihkannya aset, (b) tindak pidana siber/ITE, (c) kejahatan terorganisasi. Izin susulan diajukan maks. 2x24 jam."],
    ["KUHAP (UU 20/2025)\nPasal 140 ayat (10)–(13)", "Penetapan Pengadilan & Jaminan Kepastian Hukum", "Ketua PN menerbitkan penetapan maks. 2x24 jam. Jika ditolak, pemblokiran wajib dibuka resmi dalam 3 hari kerja. Menjamin perlindungan hukum bagi pihak bank/PJP."],
    ["UU ITE (UU 1/2024)\nPasal 43 ayat (5) huruf l", "Perintah Pemutusan Akses Akun & Dompet Digital", "Penyidik berwenang memerintahkan PSE memutus akses sementara akun medsos, rekening bank, uang elektronik, dan aset digital terkait tindak pidana."],
    ["UU 8/2010 (UU TPPU)\nPasal 71 & Pasal 74", "Perintah Pemblokiran Khusus TPPU & Kewenangan Penyidik Asal", "Ketentuan hukum acara pemblokiran harta kekayaan hasil kejahatan tetap berlaku penuh bagi penyidik Polri sebagai penyidik tindak pidana asal."]
]
table(s7, rows_s7, left=0.6, top=1.65, width=12.13, col_w=[2.3, 3.8, 6.03], font_size=10, header_size=10.5, row_h=0.85, head_h=0.45)
footer(s7, 7)
notes(s7, "Ini pasal paling krusial dalam paparan saya: KUHAP Baru UU 20/2025 Pasal 140 ayat (7) sampai (9). "
          "Seringkali perbankan atau PJP menolak membekukan rekening karena takut digugat perdata jika belum ada penetapan pengadilan. "
          "Undang-undang baru sudah memberi payung hukum: dalam situasi darurat kejahatan ITE dan potensi pelarian aset, "
          "Penyidik berhak meminta pemblokiran seketika TANPA IZIN PENGADILAN di awal. Persetujuan hakim baru menyusul dalam 2x24 jam. "
          "Artinya, PJP aman secara hukum untuk menahan saldo mencurigakan atas permintaan resmi penyidik.")

# ==================== SLIDE 8: SPEED GAP & DILEMA LAPANGAN ====================
s8 = prs.slides.add_slide(BLANK)
header(s8, "Evaluasi Sistemik", "Kesenjangan Kecepatan (Speed Gap) & Beban Pembuktian")
# Left Card: Modus Pelaku
rect(s8, 0.6, 1.6, 5.8, 5.0, BG_BOX, MSO_SHAPE.ROUNDED_RECTANGLE)
rect(s8, 0.6, 1.6, 5.8, 0.45, RED)
tf_l8 = textbox(s8, 0.8, 1.68, 5.4, 0.35)
put(tf_l8, "KECEPATAN SIKLUS PELAKU: HITUNGAN MENIT", size=12, color=WHITE, bold=True, space_after=0, first=True)
tf_lb = textbox(s8, 0.8, 2.2, 5.4, 4.2)
bullets(tf_lb, [
    (0, "Otomasi bot mengeksekusi transfer ribuan pecahan saldo secara simultan.", 13),
    (0, "Dana hasil kejahatan langsung ditarik tunai (cash-out) melalui gerai ritel dan agen laku pandai pinggiran kota.", 13),
    (0, "Infrastruktur server C2 berada di luar negeri (offshore bulletproof hosting) dengan rantai proxy berlapis.", 13),
    (0, "Akun dan merchant fiktif langsung dibuang (disposable) setelah saldo terkuras.", 13)
])

# Right Card: Prosedur APH
rect(s8, 6.9, 1.6, 5.8, 5.0, BG_BOX, MSO_SHAPE.ROUNDED_RECTANGLE)
rect(s8, 6.9, 1.6, 5.8, 0.45, NAVY)
tf_r8 = textbox(s8, 7.1, 1.68, 5.4, 0.35)
put(tf_r8, "PROSEDUR HUKUM KONVENSIONAL: HITUNGAN HARI", size=12, color=WHITE, bold=True, space_after=0, first=True)
tf_rb = textbox(s8, 7.1, 2.2, 5.4, 4.2)
bullets(tf_rb, [
    (0, "Administrasi surat permintaan data dan izin sita/blokir memerlukan paraf berjenjang.", 13),
    (0, "Proses validasi kepatuhan internal perbankan/PJP kerap memakan waktu 3–7 hari kerja.", 13),
    (0, "Format data mutasi transaksi yang diserahkan PJP ke penyidik tidak seragam (PDF hasil printout kaku vs file raw JSON/CSV).", 13),
    (0, "Hasil akhir: Saat surat blokir resmi terbit, saldo rekening penampung telah Rp 0 (likuiditas lenyap).", 13, True, RED)
])
footer(s8, 8)
notes(s8, "Lihat perbandingannya: di sisi kiri, bot memindahkan dana dalam 5 menit. Di sisi kanan, birokrasi penyidikan butuh 3-5 hari. "
          "Akibatnya apa? Pemblokiran menjadi sia-sia karena saldo sudah nol. Selain itu, ketika kami meminta data log transaksi ke berbagai PJP, "
          "ada yang kirim PDF gambar buram, ada yang kirim Excel terpotong. Penyidik kehabisan waktu hanya untuk merapikan data, bukan memburu pelaku.")

# ==================== SLIDE 9: DAMPAK SOSIAL & MALADMINISTRASI ====================
s9 = prs.slides.add_slide(BLANK)
header(s9, "Dampak Publik", "Eksternalitas Sosial: Penangguhan Bansos 1,49 Juta KPM")
tf_top9 = textbox(s9, 0.6, 1.5, 12.13, 1.1)
put(tf_top9, "Pemadanan data intelijen transaksi PPATK dengan Kemensos berujung pemutusan hak 1,49 juta penerima bansos. Investigasi membuktikan mayoritas nama yang tercatat adalah KORBAN eksploitasi sindikat, bukan pemain aktif.", size=13.5, color=DARK, bold=True, space_after=0, first=True)

d_cards = [
    ("PENCATUTAN IDENTITAS", "Data e-KTP warga miskin dikumpulkan calo berkedok sembako, lalu dijual ke sindikat untuk registrasi akun judi/merchant."),
    ("JARINGAN JOKI REKENING", "Warga desa disewakan buku tabungan & akun e-wallet senilai Rp100rb–Rp300rb, dikuasai penuh operator kejahatan."),
    ("KEBOCORAN DATA DUKCAPIL", "NIK sah digunakan mencetak profil identitas sintetik untuk membobol verifikasi e-KYC perbankan dan PJP."),
    ("RISIKO MALADMINISTRASI", "Ombudsman RI menyoroti ketiadaan due process of law dan mekanisme sanggahan cepat bagi warga miskin yang terzalimi.")
]
top_dc = 2.7
w_dc = 5.85
h_dc = 1.95
for i, (dt, dd) in enumerate(d_cards):
    r_idx = i // 2
    c_idx = i % 2
    dx = 0.6 + c_idx * (w_dc + 0.43)
    dy = top_dc + r_idx * (h_dc + 0.3)
    rect(s9, dx, dy, w_dc, h_dc, BG_BOX, MSO_SHAPE.ROUNDED_RECTANGLE)
    rect(s9, dx, dy, 0.08, h_dc, RED if i==3 else BLUE)
    tf_d = textbox(s9, dx + 0.25, dy + 0.2, w_dc - 0.45, h_dc - 0.4)
    put(tf_d, dt, size=14, color=NAVY, bold=True, space_after=4, first=True)
    put(tf_d, dd, size=12, color=DARK, space_after=0, line_spacing=1.1)
footer(s9, 9)
notes(s9, "Di forum ini hadir juga Ombudsman RI. Kami ingin tegaskan: penegakan hukum tidak boleh membabi buta. "
          "1,49 juta penerima bansos yang ditangguhkan itu sebagian besar adalah korban. Fotokopi KTP mereka dipinjam calo, "
          "rekening mereka disewa pemuda kampung seharga 100 ribu. Jika PJP memutus akun tanpa mekanisme klarifikasi, "
          "kita memutus urat nadi orang miskin yang tidak tahu apa-apa. Di sini pentingnya verifikasi lapangan dan sanggahan cepat.")

# ==================== SLIDE 10: 4 REKOMENDASI TAKTIS ====================
s10 = prs.slides.add_slide(BLANK)
header(s10, "Solusi Kolaboratif", "4 Rekomendasi Aksi Sinergi Ditreskrimsus Polda Sulsel – PJP")
r_top = 1.6
r_w = 5.85
r_h = 2.45
recs = [
    ("1. PROTOKOL BLOKIR DARURAT 24/7 (2 JAM)",
     "Membangun jalur terenkripsi khusus antara Subdit Siber Polda Sulsel & Tim Compliance OVO.",
     "Penyidik menerbitkan notifikasi awalan berbasis parameter digital (NIK merchant, ID transaksi, hash device). PJP langsung menahan saldo maks. 2 jam; penetapan izin pengadilan menyusul sesuai KUHAP Ps. 140 (7)-(9)."),
    ("2. STANDARISASI BUKTI FORENSIK DIGITAL",
     "Pengemasan alat bukti digital selaras ISO/IEC 27037 dan Pasal 44 UU ITE.",
     "PJP menyerahkan riwayat log transaksi dalam format terstruktur (JSON/CSV) lengkap dengan IP Public, port, timestamp UTC terkalibrasi, hardware ID, dan nilai hash SHA-256 untuk menjaga chain of custody."),
    ("3. PENGETATAN UJI TUNTAS MERCHANT (KYM)",
     "Pemberantasan merchant QRIS fiktif hasil kongkalikong agregator nakal.",
     "Audit faktual tempat usaha, penerapan batas kecepatan & akumulasi nominal (velocity ceiling) selama 30 hari pertama, serta memblokir transfer auto-settlement instan ke e-wallet pribadi."),
    ("4. GUGUS TUGAS INTELIJEN SIBER REGIONAL",
     "Forum taktis gabungan: Polda Sulsel, PPATK, BI Sulsel, OJK Reg 6, dan Compliance PJP.",
     "Pertukaran threat intelligence rutin, simulasi penanganan insiden gabungan (tabletop exercise), dan penyelarasan model machine learning internal PJP dengan tipologi kejahatan lokal Sulsel.")
]
for i, (rt, rsub, rdesc) in enumerate(recs):
    r_idx = i // 2
    c_idx = i % 2
    rx = 0.6 + c_idx * (r_w + 0.43)
    ry = r_top + r_idx * (r_h + 0.25)
    rect(s10, rx, ry, r_w, r_h, BG_BOX, MSO_SHAPE.ROUNDED_RECTANGLE)
    rect(s10, rx, ry, 0.1, r_h, RED if i==0 else NAVY)
    tf_r = textbox(s10, rx + 0.25, ry + 0.15, r_w - 0.45, r_h - 0.3)
    put(tf_r, rt, size=13.5, color=RED if i==0 else NAVY, bold=True, space_after=3, first=True)
    put(tf_r, rsub, size=11, color=DARK, bold=True, space_after=4)
    put(tf_r, rdesc, size=10.5, color=GREY, space_after=0, line_spacing=1.05)
footer(s10, 10)
notes(s10, "Empat rekomendasi ini adalah output utama yang kami tawarkan kepada manajemen OVO. "
          "Poin 1: Mari buat hotline darurat penyidik-OVO. Jika ada transaksi judol berjalan, tahan saldo dalam 2 jam pertama. "
          "Poin 2: Seragamkan log bukti digital dengan hash SHA-256 agar langsung sah di pengadilan. "
          "Poin 3: Batasi pencairan otomatis QRIS baru selama 30 hari pertama (velocity ceiling) untuk membunuh bisnis merchant fiktif. "
          "Poin 4: Bentuk Gugus Tugas Intelijen Keuangan Siber di Makassar.")

# ==================== SLIDE 11: ROADMAP 90 HARI ====================
s11 = prs.slides.add_slide(BLANK)
header(s11, "Implementasi", "Peta Jalan Implementasi Taktis (Target 90 Hari)")
rows_s11 = [
    ["Fase / Waktu", "Fokus Aktivitas Kerja Bersama", "Indikator Keberhasilan / Deliverable", "Penanggung Jawab"],
    ["Fase I\n(Hari 1 – 30)", "• Finalisasi draf SOP Protokol Tanggap Darurat 24/7\n• Penetapan Single Point of Contact (SPoC) terenkripsi\n• Inventarisasi format data ekstraksi bukti digital", "Tandatangan Perjanjian Kerja Sama Taktis & Register SPoC Terverifikasi", "Ditreskrimsus Polda Sulsel & Divisi Legal/Compliance OVO"],
    ["Fase II\n(Hari 31 – 60)", "• Simulasi Tabletop Exercise penahanan saldo 2 jam\n• Integrasi format bukti log forensik ISO/IEC 27037\n• Penyesuaian rule fraud engine OVO terhadap temuan botnet", "Berita Acara Uji Coba Simulasi & Template Log Terstandarisasi", "Subdit V Siber, PPATK, dan Tim Engineering/AML OVO"],
    ["Fase III\n(Hari 61 – 90)", "• Kick-off Gugus Tugas Intelijen Siber Finansial Regional\n• Pemberlakuan velocity ceiling bagi agregator merchant QRIS\n• Evaluasi berkala data pemadanan NIK bansos Sulsel", "Laporan Penilaian Ancaman Regional & Penurunan Transaksi Judol QRIS", "Polda Sulsel, Bank Indonesia, OJK Sulselbar, PJP"]
]
table(s11, rows_s11, left=0.6, top=1.65, width=12.13, col_w=[1.8, 4.3, 3.5, 2.53], font_size=10, header_size=10.5, row_h=1.35, head_h=0.45)
footer(s11, 11)
notes(s11, "Kami tidak ingin pertemuan hari ini berhenti pada wacana seremonial. Kami tawarkan peta jalan 90 hari terukur. "
          "Bulan pertama kita bereskan SOP darurat dan tunjuk nomor kontak siaga 24 jam. Bulan kedua kita gelar simulasi penahanan saldo 2 jam "
          "antara penyidik dan server OVO. Bulan ketiga kita luncurkan Gugus Tugas Regional bersama BI dan OJK. Ini konkret dan dapat dieksekusi.")

# ==================== SLIDE 12: PENUTUP ====================
s12 = prs.slides.add_slide(BLANK)
rect(s12, 0, 0, 13.333, 7.5, NAVY)
rect(s12, 0, 0, 13.333, 0.2, RED)
tf12 = textbox(s12, 1.0, 1.6, 11.33, 4.6)
put(tf12, "PRINSIP PENUTUP", size=13, color=GOLD, bold=True, space_after=12, first=True)
put(tf12, "\"Kejahatan keuangan siber bergerak dengan kecepatan algoritma; pertahanan dan penegakan hukum tidak boleh tertahan oleh kelambanan birokrasi.\"", size=25, color=WHITE, bold=True, space_after=20, line_spacing=0.98)

put(tf12, "Dua Pilar Kolaborasi:", size=16, color=PALE, bold=True, space_after=10)
put(tf12, "1. KECEPATAN (SPEED)  — Eksekusi protokol blokir darurat berbasis KUHAP 2025 Pasal 140 ayat (7)-(9).", size=15, color=GOLD, bold=True, space_after=8)
put(tf12, "2. INTEGRITAS (EVIDENCE) — Standarisasi bukti digital forensik ber-hash SHA-256 yang absolut di persidangan.", size=15, color=GOLD, bold=True, space_after=22)

put(tf12, "Sekian dan Terima Kasih. Forum Diskusi & Tanya Jawab Dibuka.", size=16, color=WHITE, bold=True, space_after=0)

tf12_f = textbox(s12, 1.0, 6.4, 11.33, 0.6)
put(tf12_f, "Kombes Pol Taufik Herdiansyah  |  Direktur Reserse Kriminal Khusus Polda Sulawesi Selatan", size=11, color=GREY, space_after=0, first=True)
notes(s12, "Penutup resmi. Buka sesi tanya jawab dengan audiens. Siapkan jawaban terkait teknis legal standing pemblokiran darurat, "
          "mekanisme kompensasi jika terjadi kesalahan blokir (remedy), dan tata cara permintaan data log forensik sesuai Perkap.")

# Save presentation
out_path = "/home/ubuntu/penyidikan/analisis/workshop-ovo-2026/Paparan_Workshop_OVO_Dirreskrimsus_Polda_Sulsel_Clean.pptx"
prs.save(out_path)
print("SUCCESS_SAVED:", out_path, "| slides:", len(prs.slides))
