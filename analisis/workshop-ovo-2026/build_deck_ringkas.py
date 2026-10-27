#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Versi RINGKAS (13 slide) paparan Workshop Tertutup OVO — Ditreskrimsus Polda Sulsel.
Prinsip: slide hanya memuat kata kunci; uraian panjang dipindah ke catatan pembicara."""

import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

NAVY  = RGBColor(0x0B, 0x25, 0x45)
NAVY2 = RGBColor(0x13, 0x31, 0x5C)
RED   = RGBColor(0xB3, 0x26, 0x1E)
GOLD  = RGBColor(0xC8, 0xA2, 0x27)
ROWA  = RGBColor(0xF7, 0xF9, 0xFB)
DARK  = RGBColor(0x1B, 0x28, 0x33)
GREY  = RGBColor(0x55, 0x63, 0x6E)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
PALE  = RGBColor(0xC7, 0xD3, 0xE0)
FONT  = "Tahoma"
FOOTER = "Ditreskrimsus Polda Sulsel  |  Workshop Tertutup OVO & OVO Finansial  |  Makassar, 22 Oktober 2026"

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


def put(tf, text, size=16, color=DARK, bold=False, align=PP_ALIGN.LEFT,
        space_after=8, first=False, line_spacing=1.0):
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
        size = it[2] if len(it) > 2 else 18
        bold = it[3] if len(it) > 3 else False
        color = it[4] if len(it) > 4 else DARK
        p = tf.paragraphs[0] if (first and not started) else tf.add_paragraph()
        started = True
        p.space_after = Pt(10 if level == 0 else 6)
        p.line_spacing = 1.05
        mark = "\u25aa  " if level == 0 else "\u2013  "
        r = p.add_run()
        r.text = mark + text
        r.font.name = FONT
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = color


def header(slide, eyebrow, title):
    rect(slide, 0, 0, 13.333, 0.14, RED)
    rect(slide, 0, 0.14, 13.333, 1.1, NAVY)
    tf = textbox(slide, 0.55, 0.2, 12.3, 1.0)
    put(tf, eyebrow.upper(), size=11, color=GOLD, bold=True, space_after=2, first=True)
    put(tf, title, size=24, color=WHITE, bold=True, space_after=0, line_spacing=0.95)


def footer(slide, num):
    tf = textbox(slide, 0.55, 7.02, 11.0, 0.35)
    put(tf, FOOTER, size=8.5, color=GREY, space_after=0, first=True)
    tf2 = textbox(slide, 12.2, 7.02, 0.7, 0.35)
    put(tf2, str(num), size=10, color=NAVY, bold=True, align=PP_ALIGN.RIGHT, space_after=0, first=True)


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def table(slide, rows, left, top, width, col_w, font_size=13, header_size=13,
          row_h=0.62, head_h=0.5):
    nr, nc = len(rows), len(rows[0])
    shape = slide.shapes.add_table(nr, nc, Inches(left), Inches(top), Inches(width),
                                   Inches(head_h + row_h * (nr - 1)))
    tbl = shape.table
    total = sum(col_w)
    for i, cw in enumerate(col_w):
        tbl.columns[i].width = Emu(int(Inches(width) * cw / total))
    tbl.rows[0].height = Inches(head_h)
    for r in range(1, nr):
        tbl.rows[r].height = Inches(row_h)
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            cell = tbl.cell(r, c)
            cell.margin_left = Inches(0.08)
            cell.margin_right = Inches(0.08)
            cell.margin_top = Inches(0.03)
            cell.margin_bottom = Inches(0.03)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            cell.fill.fore_color.rgb = NAVY2 if r == 0 else (ROWA if r % 2 else WHITE)
            p = cell.text_frame.paragraphs[0]
            p.space_after = Pt(0)
            run = p.add_run()
            run.text = str(val)
            run.font.name = FONT
            run.font.size = Pt(header_size if r == 0 else font_size)
            run.font.bold = (r == 0)
            run.font.color.rgb = WHITE if r == 0 else DARK


def cards(slide, items, top=1.7, height=1.75, cols=2, gap=0.35, left=0.6, width=12.1):
    cw = (width - gap * (cols - 1)) / cols
    for i, (title, desc) in enumerate(items):
        r, c = divmod(i, cols)
        x = left + c * (cw + gap)
        y = top + r * (height + gap)
        rect(slide, x, y, cw, height, ROWA, MSO_SHAPE.ROUNDED_RECTANGLE)
        rect(slide, x, y, 0.09, height, RED)
        tf = textbox(slide, x + 0.28, y + 0.16, cw - 0.45, height - 0.3)
        put(tf, title, size=16, color=NAVY, bold=True, space_after=4, first=True)
        put(tf, desc, size=12.5, color=DARK, space_after=0, line_spacing=1.05)


def metrics(slide, items, top=2.0, height=2.3, cols=4, gap=0.3, left=0.6, width=12.1):
    cw = (width - gap * (cols - 1)) / cols
    for i, (big, small) in enumerate(items):
        x = left + i * (cw + gap)
        rect(slide, x, top, cw, height, NAVY, MSO_SHAPE.ROUNDED_RECTANGLE)
        tf = textbox(slide, x + 0.15, top + 0.35, cw - 0.3, height - 0.5)
        put(tf, big, size=26, color=GOLD, bold=True, align=PP_ALIGN.CENTER,
            space_after=8, first=True)
        put(tf, small, size=12, color=WHITE, align=PP_ALIGN.CENTER, space_after=0,
            line_spacing=1.05)


# ============================ 1. COVER ============================
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, 13.333, 7.5, NAVY)
rect(s, 0, 0, 13.333, 0.18, RED)
rect(s, 0.9, 1.1, 1.6, 0.1, GOLD)
tf = textbox(s, 0.9, 1.4, 11.5, 3.2)
put(tf, "WORKSHOP TERTUTUP OVO & OVO FINANSIAL", size=13, color=GOLD, bold=True,
    space_after=14, first=True)
put(tf, "Kejahatan Keuangan Berbasis AI", size=40, color=WHITE, bold=True,
    space_after=2, line_spacing=0.95)
put(tf, "dan Eksploitasi Ekosistem Pembayaran Digital", size=40, color=WHITE, bold=True,
    space_after=0, line_spacing=0.95)
tf = textbox(s, 0.9, 4.85, 11.5, 1.8)
put(tf, "Kombes Pol Taufik Herdiansyah \u2014 Dirreskrimsus Polda Sulawesi Selatan", size=15,
    color=WHITE, bold=True, space_after=8, first=True)
put(tf, "Hotel Hyatt Place, Makassar  \u2022  Kamis, 22 Oktober 2026  \u2022  14.25\u201315.10 WITA",
    size=13, color=PALE, space_after=0)
tf = textbox(s, 0.9, 6.75, 11.5, 0.5)
put(tf, "Versi ringkas \u2014 catatan pembicara memuat uraian lengkap dan dasar hukum.",
    size=9, color=RGBColor(0x8A, 0x9B, 0xAD), space_after=0, first=True)
notes(s, "Versi ringkas: slide memuat kata kunci, pembicara memaparkan. Waktu 45 menit; alokasi: 5 menit temuan "
         "utama, 15 menit modus dan vektor AI, 10 menit kerangka hukum, 10 menit tantangan, 5 menit rekomendasi. "
         "Bila waktu tersisa sedikit, slide 6\u20137 (dasar hukum) dapat dibahas ringkas dan ditawarkan sebagai lampiran.")

# ============================ 2. TIGA TEMUAN ============================
s = prs.slides.add_slide(BLANK)
header(s, "Ringkasan", "Tiga Temuan Utama")
tf = textbox(s, 0.6, 1.9, 12.1, 4.6)
bullets(tf, [
    (0, "Modus bergeser ke transaksi mikro lewat QRIS", 24, True),
    (1, "Pengawasan berbasis ambang batas statis tidak lagi efektif", 17),
    (0, "Pelaku bergerak otomatis dan lebih cepat dari verifikasi manual", 24, True),
    (1, "Bot, deepfake, dan identitas sintetik menggantikan kejahatan manual", 17),
    (0, "Norma hukum sudah cukup \u2014 yang kurang adalah kanal eksekusinya", 24, True),
    (1, "Belum ada prosedur blokir cepat 24/7 dan standar bukti digital", 17),
])
footer(s, 2)
notes(s, "Temuan pertama: deposit judi online terkonsentrasi pada QRIS (87,6\u201388,6% frekuensi), sementara nilai "
         "perputaran menurun 12,9%. Artinya pelaku berpindah ke transaksi mikro bernilai kecil tapi sangat banyak, "
         "sehingga ambang pelaporan otomatis dilewati. Temuan kedua: penindakan di Makassar menunjukkan 2.000+ akun "
         "bot dan 180 situs \u2014 kejahatan manual sudah berakhir. Temuan ketiga: KUHAP Pasal 140 ayat (7)\u2013(9) "
         "sebenarnya sudah memberi jalan pemblokiran mendesak; hambatannya prosedural dan teknis, bukan normatif. "
         "Di sinilah industri dapat membantu.")

# ============================ 3. ANGKA KUNCI ============================
s = prs.slides.add_slide(BLANK)
header(s, "Data kunci", "Empat Angka yang Menggambarkan Persoalan")
metrics(s, [
    ("Rp86,82 T", "Perputaran dana judi online\nSemester I-2026\n(turun 12,9%; sebelumnya 43%)"),
    ("87,6\u201388,6%", "Frekuensi deposit judi online\nmelalui kanal QRIS\n(transfer bank tinggal 11,4%)"),
    ("2.000+", "Akun bot terotomatisasi\ndi Kota Makassar,\nmengendalikan 180 situs aktif"),
    ("1,49 juta", "Keluarga Penerima Manfaat\nbansos ditangguhkan\nakibat pemadanan data"),
], top=2.0, height=2.55)
tf = textbox(s, 0.6, 5.0, 12.1, 1.6)
bullets(tf, [
    (0, "Deposit QRIS tercatat Rp12,36 triliun pada triwulan pertama 2026", 15, True),
    (0, "Perlambatan kontraksi = indikasi adaptasi modus, bukan keberhasilan pemberantasan", 15, True, RED),
], first=True)
tf = textbox(s, 0.6, 6.55, 12.1, 0.4)
put(tf, "Sumber: data intelijen keuangan PPATK (2026); hasil penindakan Subdit V Cybercrime Ditreskrimsus Polda Sulsel.",
    size=9, color=GREY, space_after=0, first=True)
footer(s, 3)
notes(s, "Sampaikan angka tanpa membaca tabel. Tekankan dua hal: (1) nilai perputaran menurun tetapi frekuensi "
         "QRIS mendominasi \u2014 modus bergeser ke pecahan kecil; (2) 1,49 juta KPM adalah korban pencatutan "
         "identitas dan penyewaan rekening, bukan pelaku. Angka ini menjadi dasar mengapa penargetan sanksi harus "
         "presisi dan disertai mekanisme klarifikasi.")

# ============================ 4. ANATOMI SERANGAN ============================
s = prs.slides.add_slide(BLANK)
header(s, "Modus", "Anatomi Serangan: Dari Bot ke Uang Tunai")
tf = textbox(s, 0.6, 1.85, 12.1, 4.9)
bullets(tf, [
    (0, "Peternakan peranti: ribuan emulator, spoofing IMEI, MAC, dan canvas fingerprint", 20, True),
    (0, "Penyamaran jaringan: VPN komersial dan IP residensial yang dirotasi", 20, True),
    (0, "Penyaringan likuiditas: pemecahan dana (structuring, smurfing) di bawah ambang pelaporan", 20, True),
    (0, "Skema dua arah: many-to-one ke akun penampung, lalu one-to-many ke dompet digital", 20, True),
    (0, "Pencairan: rekening joki, agen laku pandai, ATM, dan gerai ritel", 20, True),
    (0, "Satu berkas perkara = ribuan transaksi pada puluhan penyelenggara jasa pembayaran", 20, True, RED),
])
footer(s, 4)
notes(s, "Jelaskan alur lima tahap. Titik penting bagi OVO: tahap peternakan peranti dan penyaringan likuiditas "
         "terjadi di dalam sistem PJP, sehingga data relasi akun\u2013peranti\u2013waktu ada di tangan industri. "
         "Sebut bahwa penindakan Subdit V Cybercrime menemukan replikasi model Cybercrime-as-a-Service di tingkat "
         "daerah \u2014 modul otomatis tidak lagi monopoli sindikat transnasional.")

# ============================ 5. EMPAT VEKTOR AI ============================
s = prs.slides.add_slide(BLANK)
header(s, "Vektor eksploitasi AI", "Empat Serangan Terhadap Pintu Masuk Digital")
cards(s, [
    ("1. Injeksi kamera virtual",
     "Perangkat di-root, kamera virtual dipasang, video deepfake disuntik ke API verifikasi; sensor fisik dipintas."),
    ("2. Identitas sintetik",
     "NIK asli hasil kebocoran data dipadukan wajah buatan AI; OCR dan pencocokan biometrik lolos."),
    ("3. Pengambilalihan akun dorman",
     "Akun pasif dengan reputasi bersih dibajak melalui rekayasa proses verifikasi ulang (re-KYC)."),
    ("4. Merchant fiktif lewat agregator",
     "Korporasi cangkang dan toko fiktif memperoleh fasilitas QRIS karena uji tuntas KYM lemah."),
], top=1.75, height=1.8)
tf = textbox(s, 0.6, 5.6, 12.1, 1.2)
bullets(tf, [
    (0, "Pertahanan yang dituntut: verifikasi integritas aplikasi, chip e-KTP via NFC, dan biometrik perilaku", 17, True),
], first=True)
footer(s, 5)
notes(s, "Inti slide: serangan tidak lagi menyerang kamera, melainkan pipa data aplikasi. Karena itu liveness "
         "detection bersertifikasi ISO/IEC 30107-3 saja tidak memadai tanpa client attestation, deteksi emulator, "
         "dan TLS pinning. Untuk merchant: pembatasan nominal dan kecepatan transaksi pada 30 hari pertama serta "
         "penonaktifan pencairan otomatis ke dompet perorangan adalah kontrol termurah untuk memutus aliran dana.")

# ============================ 6. DASAR HUKUM PIDANA ============================
s = prs.slides.add_slide(BLANK)
header(s, "Dasar hukum \u2022 pidana", "Konstruksi Delik: KUHP Berlaku Sejak 2 Januari 2026")
table(s, [
    ["Pasal", "Perbuatan", "Ancaman (kata kunci)"],
    ["KUHP Ps. 332", "Akses ilegal sistem elektronik (dulu UU ITE Ps. 30 jo. 46)", "Maks. 6\u20138 tahun"],
    ["KUHP Ps. 258", "Penyadapan transmisi elektronik dan menyiarkan hasilnya", "Maks. 10 tahun"],
    ["KUHP Ps. 426", "Perjudian: memberi kesempatan main judi", "Maks. 9 tahun / denda kat. VI"],
    ["KUHP Ps. 492", "Penipuan: nama atau kedudukan palsu, tipu muslihat", "Maks. 4 tahun"],
    ["KUHP Ps. 607", "TPPU: menyamarkan hasil tindak pidana", "Maks. 15 tahun / denda kat. VII"],
    ["UU ITE Ps. 27 (2)", "Informasi elektronik bermuatan perjudian", "Maks. 10 tahun / Rp10 miliar"],
    ["UU PDP Ps. 67\u201368", "Data pribadi tanpa hak dan pemalsuan data pribadi", "Maks. 4\u20136 tahun"],
], left=0.6, top=1.7, width=12.1, col_w=[2.3, 6.3, 4.0], font_size=12.5, header_size=13,
   row_h=0.55, head_h=0.5)
tf = textbox(s, 0.6, 6.6, 12.1, 0.4)
put(tf, "Pasca UU 1/2026: penjara dan denda menjadi alternatif, denda dikonversi ke kategori Pasal 79 KUHP, "
        "batas penjara tanpa alternatif 15 tahun.", size=9, color=GREY, space_after=0, first=True)
footer(s, 6)
notes(s, "Poin penting yang sering ditanyakan: KUHP Pasal 622 mencabut dan mengalihkan pengacuan sejumlah pasal UU "
         "ITE \u2014 Pasal 30 dan 46 menjadi KUHP Pasal 332; Pasal 31 dan 47 menjadi KUHP Pasal 258 ayat (2). "
         "Judi online tetap dijerat Pasal 27 ayat (2) UU ITE (ancaman Pasal 45 ayat (3) UU 1/2024) dan Pasal 426 "
         "KUHP. Delik TPPU yang semula Pasal 2, 3, 4, dan 5 UU 8/2010 kini terkodifikasi pada KUHP Pasal 607 dan "
         "608; Pasal 608 justru melindungi pihak pelapor yang menjalankan kewajiban APU-PPT.")

# ============================ 7. DASAR HUKUM ACARA ============================
s = prs.slides.add_slide(BLANK)
header(s, "Dasar hukum \u2022 acara", "Kewenangan Penyidik yang Sudah Tersedia")
table(s, [
    ["Dasar hukum", "Kewenangan", "Syarat kunci"],
    ["KUHAP Ps. 140 (2) dan (6)", "Pemblokiran oleh penyidik, penuntut umum, atau hakim",
     "Izin ketua pengadilan negeri; jangka 1 tahun, diperpanjang 2\u00d76 bulan"],
    ["KUHAP Ps. 140 (7)\u2013(9)", "Pemblokiran dalam keadaan mendesak tanpa izin ketua pengadilan negeri",
     "Alasan: potensi pengalihan harta, TP terkait ITE, permufakatan terorganisasi; persetujuan maks. 2\u00d724 jam"],
    ["UU ITE Ps. 43 (5) huruf l", "Perintah pemutusan akses sementara",
     "Rekening bank, uang elektronik, dan aset digital"],
    ["UU TPPU Ps. 71 dan 74", "Perintah pemblokiran harta dan kewenangan penyidik tindak pidana asal",
     "Tetap berlaku untuk prosedur TPPU"],
], left=0.6, top=1.75, width=12.1, col_w=[2.9, 4.6, 4.6], font_size=12, header_size=12.5,
   row_h=0.85, head_h=0.5)
tf = textbox(s, 0.6, 6.35, 12.1, 0.6)
put(tf, "Kesimpulan normatif: jalur pemblokiran cepat sudah diatur undang-undang \u2014 yang belum ada adalah "
        "prosedur teknis dan kanal komunikasi 24/7 antara penyidik dan penyedia jasa pembayaran.",
    size=13, color=RED, bold=True, space_after=0, first=True)
footer(s, 7)
notes(s, "Slide terpenting untuk rekomendasi. Baca Pasal 140 ayat (7) sampai (9) KUHAP sebagai fondasi: dalam "
         "keadaan mendesak \u2014 termasuk potensi dialihkannya harta kekayaan dan tindak pidana terkait informasi "
         "dan transaksi elektronik \u2014 pemblokiran dapat dilakukan tanpa izin ketua pengadilan negeri, dengan "
         "persetujuan diminta paling lama 2\u00d724 jam; bila ditolak, blokir dibuka paling lama 3 hari kerja. "
         "Ini memberi kepastian hukum bagi PJP yang mengeksekusi. Tambahkan bahwa UU ITE Pasal 43 ayat (5) huruf l "
         "memberi kewenangan memerintahkan pemutusan akses sementara atas rekening, uang elektronik, dan aset digital.")

# ============================ 8. KENAPA LAMBAT ============================
s = prs.slides.add_slide(BLANK)
header(s, "Tantangan", "Mengapa Pemblokiran Selalu Terlambat")
tf = textbox(s, 0.6, 1.9, 12.1, 4.6)
bullets(tf, [
    (0, "Pelaku memindahkan dan mencairkan dana dalam hitungan menit", 22, True),
    (0, "Prosedur kami berjalan dalam hitungan hari", 22, True),
    (1, "Administrasi rahasia bank, izin pengadilan, dan verifikasi internal PJP", 16),
    (0, "Kehati-hatian industri memperlambat eksekusi", 22, True),
    (1, "Kekhawatiran gugatan perdata atas pemblokiran rekening", 16),
    (0, "Hambatan bukan pada norma, melainkan pada kesiapan eksekusi", 22, True, RED),
])
footer(s, 8)
notes(s, "Sampaikan terbuka bahwa hambatan ada di sisi kami juga. Contoh konkret: ketika surat perintah tiba, saldo "
         "rekening penampung sudah kosong. Sisi industri: tidak ada format notifikasi baku, tidak ada kontak siaga, "
         "dan tidak ada klausul pembagian tanggung jawab. Sebutkan juga hambatan atribusi \u2014 server command and "
         "control di luar yurisdiksi dan rantai proksi berlapis menyulitkan pembuktian sampai pemilik manfaat akhir.")

# ============================ 9. DAMPAK PUBLIK ============================
s = prs.slides.add_slide(BLANK)
header(s, "Dampak", "Ketika Penegakan Hukum Menyentuh Warga Miskin")
tf = textbox(s, 0.6, 1.9, 12.1, 4.6)
bullets(tf, [
    (0, "1,49 juta KPM ditangguhkan dari bansos, sebagian besar adalah korban", 21, True),
    (1, "Pencatutan e-KTP, penyewaan rekening, dan kebocoran data kependudukan", 16),
    (0, "Sanksi otomatis tanpa mekanisme klarifikasi berisiko menciderai hak warga", 21, True),
    (0, "Bagi industri: pemblokiran tanpa dasar memadai memicu komplain dan gugatan", 21, True),
    (0, "Penegakan hukum dan perlindungan sosial harus berjalan bersamaan", 21, True, RED),
])
footer(s, 9)
notes(s, "Bagian ini menunjukkan kesadaran atas eksternalitas. Tekankan bahwa kerja sama dengan PJP justru membantu "
         "memisahkan profil korban eksploitasi dari operator kejahatan, sehingga sanksi lebih presisi dan beban "
         "pengaduan nasabah turun. Rujuk kewajiban transparansi dasar pemutusan layanan dan kanal keberatan "
         "sebagaimana diatur POJK 22/2023 tentang perlindungan konsumen.")

# ============================ 10. REKOMENDASI 1-3 ============================
s = prs.slides.add_slide(BLANK)
header(s, "Rekomendasi", "Tiga Langkah yang Bisa Dimulai Segera")
cards(s, [
    ("1. Protokol blokir 24/7",
     "Kanal terenkripsi penyidik\u2013kepatuhan PJP. Penahanan saldo maksimal 2 jam atas parameter digital "
     "(ID transaksi, NIK pedagang, device hash), disusul penetapan pengadilan. Dasar: KUHAP Ps. 140 (7)\u2013(9)."),
    ("2. Standar bukti digital",
     "Format mesin-terbaca dengan IP, port, timestamp UTC, device ID, session ID, hash SHA-256, dan tanda tangan "
     "digital. Selaras ISO/IEC 27037 dan UU ITE Ps. 44."),
    ("3. KYM merchant dan velocity",
     "Verifikasi faktual merchant baru, batas nominal dan kecepatan transaksi 30 hari pertama, dan penonaktifan "
     "pencairan otomatis ke dompet perorangan."),
], top=1.8, height=3.4, cols=3, gap=0.3)
tf = textbox(s, 0.6, 5.6, 12.1, 1.2)
bullets(tf, [
    (0, "Dasar kewajiban industri: POJK 8/2023 (CDD/EDD dan pemantauan berkelanjutan) serta ketentuan BI tentang PJP dan QRIS", 14, True),
    (0, "Prasyarat: format notifikasi baku, jejak audit, pembagian tanggung jawab hukum, kontak tunggal per PJP", 14),
], first=True)
footer(s, 10)
notes(s, "Sampaikan bahwa protokol blokir 2 jam bukan pemblokiran tanpa dasar, melainkan penahanan saldo berbasis "
         "parameter digital dengan pengesahan pengadilan menyusul \u2014 persis skema yang dibuka KUHAP Pasal 140 "
         "ayat (7) sampai (9). Untuk standar bukti: tujuannya agar berkas perkara tahan uji dan permintaan data "
         "tidak berulang. Untuk KYM: velocity ceiling 30 hari adalah kontrol termurah yang paling berdampak pada "
         "merchant fiktif berumur pendek.")

# ============================ 11. REKOMENDASI 4 + 90 HARI ============================
s = prs.slides.add_slide(BLANK)
header(s, "Rekomendasi", "Gugus Tugas Regional dan Peta Jalan 90 Hari")
tf = textbox(s, 0.6, 1.8, 12.1, 3.2)
bullets(tf, [
    (0, "Gugus tugas intelijen keuangan siber regional: Polda Sulsel, PPATK, BI Sulsel, OJK Regional 6, kepatuhan PJP", 19, True),
    (1, "Pertukaran intelijen ancaman, evaluasi modus AI, penyelarasan model machine learning, simulasi bersama", 15),
], first=True)
table(s, [
    ["Tahap", "Yang dikerjakan", "Keluaran"],
    ["0\u201330 hari", "Draf protokol blokir darurat dan pemetaan kontak siaga 24/7", "Draf SOP dan daftar kontak"],
    ["30\u201360 hari", "Simulasi penahanan saldo 2 jam dan penyusunan standar data bukti", "Berita acara uji coba dan template"],
    ["60\u201390 hari", "Pengetatan KYM merchant dan pembentukan gugus tugas serta rapat perdana", "Kebijakan internal dan kesepakatan kerja sama"],
], left=0.6, top=4.0, width=12.1, col_w=[1.8, 6.5, 3.8], font_size=12, header_size=12.5,
   row_h=0.68, head_h=0.5)
footer(s, 11)
notes(s, "Tutup bagian rekomendasi dengan komitmen jadwal dan struktur pengawasan. Usulkan kelompok kerja kecil "
         "3\u20135 orang per lembaga yang bertemu dua minggu sekali. Untuk gugus tugas, sebut fungsi konkretnya: "
         "satu daftar indikator peringatan dini bersama dan satu laporan penilaian ancaman regional dalam 90 hari.")

# ============================ 12. PENUTUP ============================
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, 13.333, 7.5, NAVY)
rect(s, 0, 0, 13.333, 0.18, RED)
tf = textbox(s, 1.0, 1.9, 11.3, 4.0)
put(tf, "Kolaborasi aparat penegak hukum dan industri adalah prasyarat, bukan pilihan.",
    size=30, color=WHITE, bold=True, space_after=22, first=True, line_spacing=0.98)
put(tf, "\u25aa  Kecepatan \u2014 protokol blokir darurat berbasis KUHAP Pasal 140 ayat (7)\u2013(9)",
    size=18, color=GOLD, bold=True, space_after=12)
put(tf, "\u25aa  Integritas \u2014 standar bukti digital ber-hash dan tertandatangan",
    size=18, color=GOLD, bold=True, space_after=12)
put(tf, "Terima kasih \u2014 ruang diskusi", size=20, color=WHITE, bold=True, space_after=0)
tf2 = textbox(s, 1.0, 6.4, 11.3, 0.6)
put(tf2, "Kombes Pol Taufik Herdiansyah \u2014 Dirreskrimsus Polda Sulawesi Selatan", size=11,
    color=RGBColor(0x8A, 0x9B, 0xAD), space_after=0, first=True)
notes(s, "Tiga ajakan penutup: (1) menyepakati protokol blokir darurat dalam 30 hari; (2) menunjuk kontak tunggal "
         "siaga 24/7; (3) menjadwalkan simulasi penahanan saldo. Antisipasi pertanyaan PJP mengenai perlindungan "
         "hukum atas pemblokiran mendesak \u2014 jawab dengan KUHAP Pasal 140 ayat (7) sampai (13): ada alasan "
         "mendesak yang diakui undang-undang, tenggat 2\u00d724 jam untuk persetujuan, dan kewajiban membuka blokir "
         "dalam 3 hari kerja bila permohonan ditolak.")

# ============================ 13. LAMPIRAN ============================
s = prs.slides.add_slide(BLANK)
header(s, "Lampiran", "Daftar Dasar Hukum \u2014 Bahan Tanya Jawab (Tidak Dipaparkan)")
table(s, [
    ["Kelompok", "Dasar hukum"],
    ["Pidana materiil", "KUHP Ps. 332, 258, 426, 492, 486, 607, dan 608; UU ITE Ps. 27 (2), 28 (1), 32\u201335 jo. 48\u201351 (1); UU PDP Ps. 65, 67, 68"],
    ["Hukum acara", "KUHAP Ps. 136 dan 140; UU ITE Ps. 42, 43 (5) huruf l, dan 44; UU TPPU Ps. 71 dan 74"],
    ["Penyesuaian pidana", "UU 1/2026: penghapusan minimum khusus, penjara atau denda, kategori denda Ps. 79 KUHP, batas 15 tahun"],
    ["Regulasi sektor", "POJK 8/2023; POJK 24/2025; POJK 40/2024; POJK 22/2023; PBI 22/23/2020; PBI 23/6/PBI/2021; UU P2SK Ps. 306"],
    ["Standar teknis", "ISO/IEC 27037 (bukti digital) dan ISO/IEC 30107-3 Level 1\u20132 (liveness detection)"],
], left=0.6, top=1.8, width=12.1, col_w=[2.6, 9.5], font_size=11.5, header_size=12.5,
   row_h=0.85, head_h=0.5)
footer(s, 13)
notes(s, "Lampiran rujukan. Jangan dipaparkan di depan; gunakan bila ada pertanyaan detail mengenai pasal atau "
         "standar. Seluruh pengacuan pasal KUHP telah diperiksa terhadap teks undang-undang, termasuk lampiran "
         "KUHP Pasal 622 mengenai pengalihan pengacuan sejumlah pasal UU ITE dan Pasal 2 sampai 5 UU TPPU.")

out = "/home/ubuntu/penyidikan/analisis/workshop-ovo-2026/Ringkas_Paparan_Kejahatan_Keuangan_Berbasis_AI_Ditreskrimsus_Polda_Sulsel.pptx"
os.makedirs(os.path.dirname(out), exist_ok=True)
prs.save(out)
print("SAVED:", out, "| slides:", len(prs.slides._sldIdLst))
