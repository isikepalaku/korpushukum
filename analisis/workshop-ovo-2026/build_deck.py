#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bangun draft paparan slide PPTX:
"Penegakan Hukum Kejahatan Keuangan Berbasis AI & Eksploitasi Ekosistem Pembayaran Digital"
Ditreskrimsus Polda Sulawesi Selatan — Workshop Tertutup OVO & OVO Finansial, 22 Okt 2026.
"""
import copy
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

NAVY  = RGBColor(0x0B, 0x25, 0x45)
NAVY2 = RGBColor(0x13, 0x31, 0x5C)
RED   = RGBColor(0xB3, 0x26, 0x1E)
GOLD  = RGBColor(0xC8, 0xA2, 0x27)
LIGHT = RGBColor(0xEE, 0xF2, 0xF6)
ROWA  = RGBColor(0xF7, 0xF9, 0xFB)
DARK  = RGBColor(0x1B, 0x28, 0x33)
GREY  = RGBColor(0x55, 0x63, 0x6E)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
FONT  = "Tahoma"

FOOTER = ("Ditreskrimsus Polda Sulawesi Selatan  |  Workshop Tertutup OVO & OVO Finansial  |  "
          "Makassar, 22 Oktober 2026")

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def _tf(shape):
    tf = shape.text_frame
    tf.word_wrap = True
    return tf


def rect(slide, l, t, w, h, fill, line=None):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(l), Inches(t), Inches(w), Inches(h))
    sh.shadow.inherit = False
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid()
        sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(1)
    return sh


def textbox(slide, l, t, w, h):
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    return _tf(tb)


def put(tf, runs, size=16, color=DARK, bold=False, align=PP_ALIGN.LEFT,
        space_after=6, space_before=0, first=False, line_spacing=1.0, font=FONT):
    """runs: str atau list of (text, bold, color, size) tuple."""
    p = tf.paragraphs[0] if (first and not tf.paragraphs[0].runs and tf.paragraphs[0].text == "") \
        else tf.add_paragraph()
    p.alignment = align
    p.space_after = Pt(space_after)
    p.space_before = Pt(space_before)
    p.line_spacing = line_spacing
    if isinstance(runs, str):
        runs = [(runs, bold, color, size)]
    for item in runs:
        text, b, c, s = (list(item) + [bold, color, size])[:4] if isinstance(item, tuple) else item
        r = p.add_run()
        r.text = text
        r.font.name = font
        r.font.size = Pt(s)
        r.font.bold = b
        r.font.color.rgb = c
    return p


def bullets(tf, items, first=True):
    """items: list of (level, text, size, bold, color) atau (level, text)."""
    started = False
    for it in items:
        level, text = it[0], it[1]
        size, bold, color = 15, False, DARK
        if len(it) >= 5:
            size, bold, color = it[2], bool(it[3]), it[4]
        elif len(it) == 4:
            if isinstance(it[3], RGBColor):
                size, color = it[2], it[3]
            else:
                size, bold = it[2], bool(it[3])
        elif len(it) == 3:
            size = it[2]
        p = tf.paragraphs[0] if (first and not started) else tf.add_paragraph()
        started = True
        p.level = level
        p.space_after = Pt(7 if level == 0 else 4)
        p.line_spacing = 1.05
        mark = "\u25aa  " if level == 0 else "\u2013  "
        r = p.add_run()
        r.text = mark + text
        r.font.name = FONT
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = color


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def header(slide, eyebrow, title):
    rect(slide, 0, 0, 13.333, 0.12, RED)
    rect(slide, 0, 0.12, 13.333, 1.02, NAVY)
    tf = textbox(slide, 0.55, 0.16, 12.3, 0.95)
    put(tf, eyebrow.upper(), size=10.5, color=GOLD, bold=True, space_after=1, first=True)
    put(tf, title, size=20, color=WHITE, bold=True, space_after=0, line_spacing=0.95)


def footer(slide, num):
    tf = textbox(slide, 0.55, 7.03, 11.0, 0.35)
    put(tf, FOOTER, size=8.5, color=GREY, space_after=0, first=True)
    tf2 = textbox(slide, 12.2, 7.03, 0.7, 0.35)
    put(tf2, str(num), size=10, color=NAVY, bold=True, align=PP_ALIGN.RIGHT, space_after=0, first=True)


def table(slide, rows, left, top, width, col_w, font_size=10.5,
          header_size=10.5, row_h=0.42, head_h=0.42):
    nr, nc = len(rows), len(rows[0])
    shape = slide.shapes.add_table(nr, nc, Inches(left), Inches(top),
                                   Inches(width), Inches(head_h + row_h * (nr - 1)))
    tbl = shape.table
    tbl.first_row = True
    total = sum(col_w)
    for i, cw in enumerate(col_w):
        tbl.columns[i].width = Emu(int(Inches(width) * cw / total))
    tbl.rows[0].height = Inches(head_h)
    for r in range(1, nr):
        tbl.rows[r].height = Inches(row_h)
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            cell = tbl.cell(r, c)
            cell.margin_left = Inches(0.06)
            cell.margin_right = Inches(0.06)
            cell.margin_top = Inches(0.02)
            cell.margin_bottom = Inches(0.02)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            cell.fill.fore_color.rgb = NAVY2 if r == 0 else (ROWA if r % 2 else WHITE)
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.space_after = Pt(0)
            run = p.add_run()
            run.text = str(val)
            run.font.name = FONT
            run.font.size = Pt(header_size if r == 0 else font_size)
            run.font.bold = (r == 0)
            run.font.color.rgb = WHITE if r == 0 else DARK
    return tbl


def section(slide, kicker, title, sub, num):
    rect(slide, 0, 0, 13.333, 7.5, NAVY)
    rect(slide, 0.0, 2.55, 1.0, 0.1, RED)
    tf = textbox(slide, 1.0, 2.0, 11.5, 2.6)
    put(tf, kicker.upper(), size=12, color=GOLD, bold=True, space_after=6, first=True)
    put(tf, title, size=34, color=WHITE, bold=True, space_after=10, line_spacing=0.95)
    put(tf, sub, size=14, color=RGBColor(0xC7, 0xD3, 0xE0), space_after=0)
    tf2 = textbox(slide, 1.0, 6.5, 6.0, 0.5)
    put(tf2, FOOTER, size=8.5, color=RGBColor(0x8A, 0x9B, 0xAD), space_after=0, first=True)
    tf3 = textbox(slide, 12.2, 6.5, 0.7, 0.5)
    put(tf3, str(num), size=10, color=GOLD, bold=True, align=PP_ALIGN.RIGHT, space_after=0, first=True)


# ============================== SLIDE 1 — COVER ==============================
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, 13.333, 7.5, NAVY)
rect(s, 0, 0, 13.333, 0.16, RED)
rect(s, 0.9, 1.05, 1.5, 0.09, GOLD)
tf = textbox(s, 0.9, 1.3, 11.6, 3.4)
put(tf, "WORKSHOP TERTUTUP — PT VISIONET INTERNASIONAL (OVO) & PT INDONUSA BARA SEJAHTERA (OVO FINANSIAL)",
    size=11.5, color=GOLD, bold=True, space_after=12, first=True)
put(tf, "Penegakan Hukum Kejahatan Keuangan Berbasis Kecerdasan Buatan",
    size=30, color=WHITE, bold=True, space_after=2, line_spacing=0.95)
put(tf, "dan Eksploitasi Ekosistem Pembayaran Digital", size=30, color=WHITE, bold=True,
    space_after=14, line_spacing=0.95)
put(tf, "Penguatan Deteksi dan Pencegahan Kejahatan Keuangan Berbasis AI di Era Digital",
    size=15, color=RGBColor(0xC7, 0xD3, 0xE0), space_after=0)
tf = textbox(s, 0.9, 4.9, 11.6, 1.6)
put(tf, "Hotel Hyatt Place, Kota Makassar  \u2022  Kamis, 22 Oktober 2026  \u2022  13.40\u201314.25 WITA",
    size=13, color=WHITE, bold=True, space_after=8, first=True)
put(tf, "Narasumber: Kombes Pol Taufik Herdiansyah — Direktur Reserse Kriminal Khusus Polda Sulawesi Selatan",
    size=12.5, color=RGBColor(0xC7, 0xD3, 0xE0), space_after=0)
tf = textbox(s, 0.9, 6.7, 11.6, 0.5)
put(tf, "Bahan paparan disusun dari data intelijen keuangan PPATK (2026), hasil penindakan Ditreskrimsus Polda Sulsel, "
        "dan telaah regulasi sektor jasa keuangan.", size=9, color=RGBColor(0x8A, 0x9B, 0xAD), space_after=0, first=True)
notes(s, "Slide pembuka. Sapaan resmi kepada pimpinan OVO dan OVO Finansial. Tekankan tiga hal: (1) kami datang "
         "sebagai penegak hukum sekaligus mitra kepatuhan; (2) materi fokus pada dua kata kunci — kecepatan dan "
         "integritas bukti; (3) seluruh rekomendasi di akhir paparan dirancang agar dapat dieksekusi pada tingkat teknis.")

# ============================== SLIDE 2 — KERANGKA ==============================
s = prs.slides.add_slide(BLANK)
header(s, "Kerangka paparan", "Enam Poros Bahasan")
tf = textbox(s, 0.6, 1.45, 12.1, 5.4)
bullets(tf, [
    (0, "Dinamika makro Transaksi Keuangan Mencurigakan (TKM) dan transformasi vektor transaksi ilegal", 16, True),
    (1, "Data perputaran dana perjudian daring, pergeseran kanal deposit ke QRIS, dan eksternalitas sosialnya", 13),
    (0, "Studi kasus regional Sulawesi Selatan: rekonstruksi botnet dan sindikasi keuangan", 16, True),
    (1, "Penindakan 180 situs dan lebih dari 2.000 akun bot di Kota Makassar serta arsitektur aliran dananya", 13),
    (0, "Vektor eksploitasi AI terhadap ekosistem pembayaran", 16, True),
    (1, "Manipulasi e-KYC, serangan injeksi, identitas sintetik, akun dorman, merchant fiktif, dan agregator", 13),
    (0, "Kerangka hukum: pidana materiil, hukum acara, dan regulasi APU-PPT", 16, True),
    (1, "KUHP (UU 1/2023) pasca UU 1/2026, KUHAP (UU 20/2025), UU ITE jo. UU 1/2024, UU TPPU, UU PDP, POJK, dan PBI", 13),
    (0, "Tantangan yuridis dan dampak kebijakan publik", 16, True),
    (1, "Kesenjangan kecepatan (speed gap), beban pembuktian, dan penangguhan bansos 1,49 juta KPM", 13),
    (0, "Rekomendasi aksi sinergi Ditreskrimsus Polda Sulsel dan industri sistem pembayaran", 16, True),
    (1, "Protokol tanggap darurat pemblokiran, standardisasi bukti digital, pengetatan KYM, dan gugus tugas regional", 13),
])
footer(s, 2)
notes(s, "Sampaikan bahwa setiap bagian ditutup dengan implikasi praktis: apa yang dapat segera dikerjakan bersama. "
         "Bagian hukum sengaja diletakkan sebelum rekomendasi agar setiap usulan punya dasar normatif yang jelas.")

# ============================== SLIDE 3 — SECTION I ==============================
s = prs.slides.add_slide(BLANK)
section(s, "Bagian I", "Dinamika Makro TKM dan Transformasi Vektor Transaksi Ilegal",
        "Dari aliran dana tunggal bernilai besar menuju fragmentasi transaksi mikro berfrekuensi tinggi.", 3)
notes(s, "Bagian ini menjelaskan mengapa paradigma pengawasan statis kehilangan daya. Gunakan data PPATK sebagai "
         "konteks nasional sebelum masuk ke kasus regional.")

# ============================== SLIDE 4 — DATA ==============================
s = prs.slides.add_slide(BLANK)
header(s, "Bagian I \u2022 Data intelijen keuangan", "Indikator Makro Transaksi Keuangan Mencurigakan")
table(s, [
    ["Indikator", "Sem. I-2025", "Sem. I-2026 / TW I-2026", "Implikasi penegakan hukum"],
    ["Perputaran dana perjudian daring", "Rp99,67 triliun", "Rp86,82 triliun",
     "Kontraksi 12,9% \u2014 melambat dibanding 43% periode sebelumnya"],
    ["Akumulasi nilai deposit (TW I-2026)", "Data tidak tersedia", "Rp10,59 triliun",
     "Total perputaran triwulan pertama Rp40,3 triliun"],
    ["Akumulasi deposit kanal QRIS", "Data tidak tersedia", "Rp12,36 triliun",
     "Likuiditas ilegal terkonsentrasi pada gerbang pembayaran mikro"],
    ["Pangsa frekuensi deposit QRIS", "Minoritas", "87,6% \u2013 88,6%",
     "Pergeseran mutlak dari transfer antar-rekening bank (11,4%)"],
    ["KPM bansos ditangguhkan", "Data tidak tersedia", "1,49 juta KPM",
     "Eksternalitas sosial atas eksploitasi data masyarakat rentan"],
], left=0.6, top=1.4, width=12.1, col_w=[3.0, 1.9, 2.4, 4.6], font_size=10, row_h=0.62)
tf = textbox(s, 0.6, 6.55, 12.1, 0.4)
put(tf, "Sumber: data intelijen keuangan PPATK (2026) sebagaimana dihimpun dalam bahan riset internal Ditreskrimsus "
        "Polda Sulsel. Angka pembanding periode sebelumnya digunakan sebagai indikator arah, bukan proyeksi.",
    size=9, color=GREY, space_after=0, first=True)
footer(s, 4)
notes(s, "Poin kunci: perlambatan kontraksi bukan kabar baik, melainkan indikasi adaptasi modus. Deposit QRIS "
         "mendominasi frekuensi (87,6%\u201388,6%) sementara nilai perputaran menurun \u2014 artinya pelaku bergerak "
         "ke transaksi mikro berjumlah besar. Ini yang menghancurkan efektivitas ambang batas pelaporan statis.")

# ============================== SLIDE 5 — PERGESERAN VEKTOR ==============================
s = prs.slides.add_slide(BLANK)
header(s, "Bagian I \u2022 Pergeseran vektor", "Mengapa QRIS Menjadi Kanal Dominan")
tf = textbox(s, 0.6, 1.45, 12.1, 5.4)
bullets(tf, [
    (0, "Karakteristik arsitektural QRIS yang dieksploitasi:", 16, True),
    (1, "Interoperabilitas lintas bank dan penyedia jasa pembayaran (PJP) \u2014 menembus batas sistem perbankan konvensional", 13),
    (1, "Pemindaian kode meniadakan input manual nomor rekening/nomor ponsel sehingga gagal transfer akibat salah input hilang", 13),
    (1, "Penyelesaian dana seketika (instant settlement) \u2014 likuiditas berpindah ke dompet pedagang secara real-time", 13),
    (1, "Antarmuka hanya menampilkan nama komersial pedagang (merchant trading name); pemilik dana sesungguhnya tersembunyi", 13),
    (0, "Konsekuensi analitis bagi penyidikan:", 16, True),
    (1, "Transaksi dipecah menjadi unit mikro berfrekuensi tinggi, tersebar, dan beroperasi 24/7", 13),
    (1, "Pola tidak lagi ditandai aliran tunggal bernilai besar, melainkan ribuan transaksi di bawah ambang pelaporan otomatis", 13),
    (1, "Rekonstruksi aliran dana bergantung pada analisis graf relasi akun\u2013peranti\u2013waktu, bukan pada pembacaan mutasi linier", 13),
    (0, "Implikasi kebijakan: pengawasan berbasis aturan statis (rule-based threshold) harus dilengkapi pemantauan perilaku adaptif", 15, True, RED),
])
footer(s, 5)
notes(s, "Tekankan bahwa QRIS bukan masalah, melainkan kanal yang disalahgunakan. Yang dibutuhkan bukan penolakan "
         "kanal, tetapi penajaman pemantauan: device fingerprinting, analisis graf, dan velocity control.")

# ============================== SLIDE 6 — SECTION II ==============================
s = prs.slides.add_slide(BLANK)
section(s, "Bagian II", "Studi Kasus Regional Sulawesi Selatan",
        "Rekonstruksi botnet dan sindikasi kejahatan keuangan: dari kejahatan siber manual menuju otomatisasi.", 6)
notes(s, "Bagian ini berisi fakta penindakan kewilayahan. Fungsinya menunjukkan bahwa modus tingkat transnasional "
         "sudah direplikasi di daerah, sehingga kebutuhan dukungan teknis industri menjadi konkret.")

# ============================== SLIDE 7 — BOTNET ==============================
s = prs.slides.add_slide(BLANK)
header(s, "Bagian II \u2022 Fakta penindakan", "Sindikat Botnet Makassar: Akhir Era Kejahatan Manual")
tf = textbox(s, 0.6, 1.42, 12.1, 5.4)
bullets(tf, [
    (0, "Penindakan Subdit V Cybercrime Ditreskrimsus Polda Sulsel: lebih dari 2.000 akun bot terotomatisasi, mengendalikan 180 situs aktif", 15, True),
    (0, "Bukti replikasi model Cybercrime-as-a-Service (CaaS) di tingkat daerah \u2014 modul kejahatan otomatis tidak lagi monopoli sindikat transnasional", 15, True),
    (0, "Arsitektur teknis: peternakan peranti (device farm) dengan ribuan emulator perangkat seluler", 15, True),
    (1, "Penyamaran identitas perangkat keras: manipulasi IMEI, MAC address, resolusi layar, hingga canvas fingerprinting", 13),
    (1, "Akibatnya setiap akun bot terbaca sistem pemantauan PJP sebagai perangkat fisik sah dan unik", 13),
    (0, "Netralisasi anomali geolokasi dan topologi jaringan", 15, True),
    (1, "Lalu lintas melalui VPN komersial, simpul keluar jaringan privat, dan alamat IP residensial yang dirotasi berkala", 13),
    (1, "Ilusi ribuan koneksi lokal dari masyarakat umum \u2014 mematikan peringatan berbasis frekuensi IP", 13),
    (0, "Dari satu konsol kendali: login, cek saldo, klaim promosi, dan transfer deposit dijalankan paralel", 15, True),
    (0, "Konsekuensi pembuktian: satu berkas perkara menuntut penelusuran forensik ribuan riwayat transaksi pada puluhan penyelenggara jasa sistem pembayaran", 15, True, RED),
])
footer(s, 7)
notes(s, "Ini momen kredibilitas: kami menunjukkan angka penindakan. Lanjutkan dengan penjelasan mengapa skala "
         "seperti ini membutuhkan format data dari PJP yang terbaca mesin, bukan tangkapan layar.")

# ============================== SLIDE 8 — ANATOMI ALIRAN DANA ==============================
s = prs.slides.add_slide(BLANK)
header(s, "Bagian II \u2022 Anatomi aliran dana", "Structuring dan Smurfing: Pencucian Dana Mikro")
labels = [
    "Ribuan bot\nmengirim dana mikro",
    "Akun penampung\n(layering accounts)",
    "Dompet digital &\nrekening pihak ketiga",
    "Rekening joki\n(money mules)",
    "Pencairan tunai:\nagen laku pandai, ATM, ritel",
]
left = 0.5
width = 2.42
for i, lab in enumerate(labels):
    sh = s.shapes.add_shape(MSO_SHAPE.CHEVRON, Inches(left), Inches(1.5), Inches(width), Inches(1.35))
    sh.shadow.inherit = False
    sh.fill.solid()
    sh.fill.fore_color.rgb = NAVY if i % 2 == 0 else NAVY2
    sh.line.fill.background()
    tfc = _tf(sh)
    tfc.vertical_anchor = MSO_ANCHOR.MIDDLE
    lines = lab.split("\n")
    for j, ln in enumerate(lines):
        p = tfc.paragraphs[0] if j == 0 else tfc.add_paragraph()
        p.alignment = PP_ALIGN.CENTER
        p.space_after = Pt(0)
        r = p.add_run()
        r.text = ln
        r.font.name = FONT
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = WHITE
    left += width + 0.02
tf = textbox(s, 0.6, 3.15, 12.1, 3.7)
bullets(tf, [
    (0, "Skema many-to-one lalu one-to-many:", 15, True),
    (1, "Ribuan akun mengirim nominal rendah ke sejumlah akun penampung; saldo dipecah kembali ke dompet digital dan rekening pihak ketiga", 13),
    (1, "Nilai transaksi dijaga selalu di bawah batas pelaporan otomatis TKM pada regulasi perbankan dan PJP", 13),
    (0, "Pemutusan rantai audit digital:", 15, True),
    (1, "Pencairan tunai melalui agen laku pandai, ATM, dan gerai ritel waralaba di Makassar serta kabupaten penyangga", 13),
    (1, "Fragmentasi menghadirkan beban pembuktian kompleks bagi penyelidik daerah", 13),
    (0, "Titik intervensi yang tersedia bagi industri:", 15, True, RED),
    (1, "Profil kecepatan transaksi (velocity) dan akumulasi nominal per merchant baru", 13, RED),
    (1, "Deteksi pola many-to-one pada merchant yang mengaku ritel mikro \u2014 miskonstruksi klasifikasi risiko pedagang", 13, RED),
])
footer(s, 8)
notes(s, "Gunakan alur chevron untuk menjelaskan lima tahap. Tegaskan bahwa tahap 1\u20133 ada di dalam sistem PJP, "
         "dan justru di situlah industri memiliki data paling lengkap: relasi akun, peranti, dan sesi.")

# ============================== SLIDE 9 — SECTION III ==============================
s = prs.slides.add_slide(BLANK)
section(s, "Bagian III", "Vektor Eksploitasi AI terhadap Ekosistem Pembayaran",
        "Manipulasi e-KYC, serangan injeksi, identitas sintetik, akun dorman, dan merchant fiktif berbasis agregator.", 9)
notes(s, "Bagian ini paling teknis. Sampaikan bahwa ancaman utamanya bukan deepfake yang terlihat, melainkan "
         "integritas saluran data pada aplikasi yang menerima verifikasi.")

# ============================== SLIDE 10 — E-KYC ==============================
s = prs.slides.add_slide(BLANK)
header(s, "Bagian III \u2022 e-KYC", "Evolusi Serangan Verifikasi Identitas Digital")
tf = textbox(s, 0.6, 1.42, 12.1, 5.4)
bullets(tf, [
    (0, "Pergeseran dari serangan penyajian ke serangan injeksi digital:", 15, True),
    (1, "Presentation attack: topeng silikon, pasfoto resolusi tinggi, rekaman video layar \u2014 dipatahkan liveness detection berbasis persepsi kedalaman dan tekstur kulit", 13),
    (1, "Digital injection attack: peranti di-root/jailbreak, modul kamera virtual dipasang, video sintetis disuntikkan langsung ke API verifikasi", 13),
    (1, "Sensor optik kamera fisik dipintas sepenuhnya, sehingga tidak ada distorsi lensa yang dapat dibaca sistem PJP", 13),
    (0, "Kapabilitas deepfake real-time (GANs dan arsitektur difusi):", 15, True),
    (1, "Menirukan perintah verifikasi dinamis: kedipan mata, anggukan kepala, gerakan mulut saat melafalkan frasa acak, perubahan pencahayaan mikro pada pupil", 13),
    (0, "Hulu kerentanan: identitas sebagai komoditas", 15, True),
    (1, "Kebocoran data kependudukan menyediakan NIK valid; identitas dirakit ulang dari elemen yang masing-masing terlihat sah", 13),
    (1, "Akibatnya modul OCR lolos karena data tekstual cocok dengan basis data kependudukan, sementara wajah sintetis lolos pencocokan biometrik", 13),
    (0, "Kesimpulan teknis: pertahanan pada titik masuk harus memverifikasi integritas aplikasi dan peranti, bukan hanya memeriksa citra wajah", 15, True, RED),
])
footer(s, 10)
notes(s, "Analoginya: presentasi attack menyerang kamera; injection attack menyerang pipa data. Karena itu ISO/IEC "
         "30107-3 Level 2 saja tidak cukup \u2014 perlu client attestation, deteksi emulator, dan TLS pinning.")

# ============================== SLIDE 11 — MATRIKS VEKTOR ==============================
s = prs.slides.add_slide(BLANK)
header(s, "Bagian III \u2022 Matriks ancaman", "Vektor Serangan, Target Kerentanan, dan Pertahanan Lanjutan")
table(s, [
    ["Vektor serangan digital", "Karakteristik teknis", "Target kerentanan pada PJP", "Mekanisme pertahanan lanjutan"],
    ["Presentation attack (2D/3D replay)", "Pemutaran video, foto HD, atau topeng silikon",
     "Sensor optik kamera depan; pengujian keaktifan visual statis",
     "Passive liveness detection terakreditasi ISO/IEC 30107-3 Level 2"],
    ["Digital injection attack", "Driver kamera virtual dan modifikasi biner aplikasi",
     "Saluran transmisi data internal; pemintasan sensor fisik",
     "Client attestation, deteksi emulator, dan TLS pinning"],
    ["Real-time deepfake synthesis", "Mikro-ekspresi dan sinkronisasi gerak bibir berbasis GANs",
     "Verifikasi tatap muka digital (video call onboarding)",
     "Analisis spektral artefak grafis AI dan tantangan gestur multi-aksial"],
    ["Synthetic identity fabrication", "NIK asli dari kebocoran data dipadukan wajah hasil AI",
     "Modul OCR dan pencocokan biometrik lintas basis data",
     "Otentikasi kriptografis chip e-KTP melalui pembacaan sensor NFC"],
    ["Dormant account takeover", "Pembajakan kredensial via rekayasa proses verifikasi ulang",
     "Prosedur pengaturan ulang kata sandi dan validasi data lama",
     "Analisis biometrik perilaku dan telemetri peranti terikat"],
], left=0.6, top=1.4, width=12.1, col_w=[2.5, 3.1, 3.0, 3.5], font_size=9.5, header_size=10, row_h=0.78)
footer(s, 11)
notes(s, "Matriks ini dapat langsung dipakai tim AML/Compliance OVO sebagai checklist kesenjangan kontrol. "
         "Kolom terakhir adalah baseline minimum, bukan daftar lengkap.")

# ============================== SLIDE 12 — IDENTITAS SINTETIK ==============================
s = prs.slides.add_slide(BLANK)
header(s, "Bagian III \u2022 Identitas dan akun", "Identitas Sintetik dan Pengambilalihan Akun Dorman")
tf = textbox(s, 0.6, 1.42, 12.1, 5.4)
bullets(tf, [
    (0, "Identitas sintetik: menggabungkan NIK valid hasil kebocoran data dengan citra wajah artifisial hasil generator AI", 15, True),
    (1, "Data tekstual terkonfirmasi cocok dengan basis data kependudukan; elemen visual mengelabui algoritma pengenalan wajah", 13),
    (0, "Akun dorman sebagai target bernilai tinggi", 15, True),
    (1, "Akun tanpa riwayat transaksi lama memiliki skor reputasi historis yang bersih dari penyaringan risiko", 13),
    (1, "Pengambilalihan dilakukan melalui prosedur pemulihan akun atau pembaruan data nasabah (re-KYC) berbasis dokumen palsu dan video deepfake", 13),
    (1, "Setelah dikuasai, akun langsung diintegrasikan ke ekosistem penampungan likuiditas tanpa memicu peringatan transaksi baru", 13),
    (0, "Pembacaan yuridis:", 15, True),
    (1, "Pengumpulan dan pengungkapan data pribadi tanpa hak serta pemalsuan data pribadi \u2014 UU 27/2022 (PDP) Pasal 65, 67, dan 68", 13),
    (1, "Akses ilegal terhadap sistem elektronik \u2014 KUHP Pasal 332 (menggantikan UU ITE Pasal 30 jo. Pasal 46)", 13),
    (1, "Penipuan dengan nama atau kedudukan palsu \u2014 KUHP Pasal 492; pemalsuan dokumen kependudukan \u2014 UU 24/2013 Pasal 93\u201396", 13),
    (0, "Catatan penyidikan: identitas sintetik membuat korban tidak pernah menyadari dirinya tercatat sebagai nasabah", 14, True, RED),
])
footer(s, 12)
notes(s, "Penting disampaikan: banyak 'nasabah' dalam laporan TKM adalah korban pencatutan. Ini dasar mengapa "
         "pemblokiran harus disertai mekanisme klarifikasi \u2014 bahasan pada Bagian V.")

# ============================== SLIDE 13 — MERCHANT FIKTIF ==============================
s = prs.slides.add_slide(BLANK)
header(s, "Bagian III \u2022 Merchant dan agregator", "Merchant Fiktif, Korporasi Cangkang, dan Agregator QRIS")
tf = textbox(s, 0.6, 1.42, 12.1, 5.4)
bullets(tf, [
    (0, "Pendaftaran merchant tanpa aktivitas komersial riil:", 15, True),
    (1, "Korporasi cangkang dan toko UMKM fiktif mengajukan fasilitas QRIS dengan melampirkan izin usaha palsu atau identitas perorangan milik joki", 13),
    (1, "Entitas diklaim bergerak pada perdagangan komoditas harian atau produk digital yang tidak pernah ada", 13),
    (1, "Setelah verifikasi administratif awal disetujui, fasilitas penerimaan pembayaran aktif diterbitkan", 13),
    (0, "Eskalasi melalui gerbang pembayaran dan perantara pendaftaran merchant:", 15, True),
    (1, "Kemitraan dengan agregator yang menerapkan uji tuntas pedagang (Know Your Merchant/KYM) secara minim", 13),
    (1, "Akses ke API penerbitan QRIS diperoleh tanpa verifikasi faktual keberadaan usaha", 13),
    (0, "Dampak pada transparansi pembayaran:", 15, True),
    (1, "Pembayar hanya melihat nama komersial pedagang; pemilik manfaat akhir (beneficial owner) sepenuhnya tersembunyi", 13),
    (1, "Instant settlement mempercepat perpindahan dana sebelum siklus audit berkala", 13),
    (0, "Kewajiban hukum yang bersinggungan: POJK 8/2023 (CDD/EDD dan pemantauan berkelanjutan), POJK 22/2023 (pelindungan konsumen), dan ketentuan Bank Indonesia tentang PJP serta QRIS", 14, True, RED),
])
footer(s, 13)
notes(s, "Ini bagian paling langsung bersinggungan dengan OVO sebagai PJP dan akuisisi merchant. Sampaikan bahwa "
         "kontrol KYM agregator adalah titik leverage termurah untuk memutus aliran dana judi.")

# ============================== SLIDE 14 — SECTION IV ==============================
s = prs.slides.add_slide(BLANK)
section(s, "Bagian IV", "Kerangka Hukum Penindakan",
        "Dasar hukum pidana materiil, hukum acara, dan regulasi APU-PPT yang berlaku pasca UU 1/2026.", 14)
notes(s, "Bagian ini wajib presisi. Setiap pasal yang disebut sudah diverifikasi pada teks undang-undang di "
         "basis data hukum internal. Ingatkan bahwa KUHP (UU 1/2023) berlaku sejak 2 Januari 2026 dan mengalihkan "
         "sejumlah pasal UU ITE.")

# ============================== SLIDE 15 — PIDANA MATERIIL ==============================
s = prs.slides.add_slide(BLANK)
header(s, "Bagian IV \u2022 Pidana materiil", "Delik Inti pada KUHP (UU 1/2023, berlaku 2 Januari 2026)")
table(s, [
    ["Pasal", "Inti delik", "Catatan pengalihan dari UU ITE", "Ancaman pasca UU 1/2026"],
    ["KUHP Ps. 332", "Akses ilegal komputer dan/atau sistem elektronik milik orang lain",
     "Menggantikan UU ITE Ps. 30 jo. Ps. 46", "Penjara maks. 6\u20138 tahun atau denda kat. V\u2013VI"],
    ["KUHP Ps. 258", "Penyadapan transmisi informasi elektronik; menyiarkan hasilnya",
     "Menggantikan UU ITE Ps. 31 jo. Ps. 47", "Penjara maks. 10 tahun (ayat 2)"],
    ["KUHP Ps. 426", "Perjudian: menawarkan atau memberi kesempatan main judi",
     "Lex generalis terhadap UU ITE Ps. 27 ayat (2)", "Penjara maks. 9 tahun atau denda kat. VI (Rp2 miliar)"],
    ["KUHP Ps. 492", "Penipuan: nama/kedudukan palsu, tipu muslihat, rangkaian kata bohong",
     "Delik umum untuk modus pinjol, merchant, dan joki rekening", "Penjara maks. 4 tahun atau denda kat. V"],
    ["KUHP Ps. 486", "Penggelapan barang yang dikuasai bukan karena tindak pidana",
     "Relevan pada penyalahgunaan dana nasabah", "Penjara maks. 4 tahun atau denda kat. IV"],
], left=0.6, top=1.4, width=12.1, col_w=[1.7, 4.2, 3.5, 2.7], font_size=9.5, header_size=10, row_h=0.72)
tf = textbox(s, 0.6, 6.5, 12.1, 0.5)
put(tf, "Catatan: pemidanaan pasca UU 1/2026 \u2014 pidana penjara dan denda yang semula kumulatif menjadi alternatif; "
        "denda dikonversi ke kategori Pasal 79 KUHP; batas penjara tanpa alternatif 15 tahun.",
    size=9, color=GREY, space_after=0, first=True)
footer(s, 15)
notes(s, "Jika ditanya mengapa tidak lagi memakai Pasal 30 UU ITE: KUHP Pasal 622 (ketentuan peralihan) mencabut "
         "sejumlah pasal UU ITE dan mengalihkan pengacuannya ke KUHP, termasuk Pasal 30 dan Pasal 46 UU ITE ke "
         "Pasal 332 KUHP. Contoh lain: UU ITE Ps. 31 dan 47 menjadi KUHP Ps. 258 ayat (2).")

# ============================== SLIDE 16 — PIDANA SEKTORAL ==============================
s = prs.slides.add_slide(BLANK)
header(s, "Bagian IV \u2022 Pidana sektoral", "TPPU, UU ITE yang Masih Berlaku, dan Delik Sektoral Lainnya")
table(s, [
    ["Dasar hukum", "Inti delik", "Ancaman"],
    ["KUHP Ps. 607 ayat (1) huruf a dan b",
     "TPPU: menempatkan, mentransfer, menyamarkan hasil tindak pidana; menyembunyikan asal usul harta kekayaan",
     "Penjara maks. 15 tahun dan denda kat. VII"],
    ["KUHP Ps. 607 ayat (1) huruf c",
     "Menerima atau menguasai harta kekayaan yang diduga hasil tindak pidana",
     "Penjara maks. 5 tahun dan denda kat. VI"],
    ["KUHP Ps. 608",
     "Pengecualian bagi pihak pelapor yang melaksanakan kewajiban pelaporan APU-PPT",
     "Perlindungan hukum bagi PJP yang melapor"],
    ["UU ITE Ps. 27 ayat (2) (UU 1/2024)",
     "Mendistribusikan/membuat dapat diaksesnya informasi elektronik bermuatan perjudian",
     "Penjara maks. 10 tahun dan/atau denda maks. Rp10 miliar \u2014 Ps. 45 ayat (3) UU 1/2024"],
    ["UU ITE Ps. 28 ayat (1) jo. Ps. 45A ayat (1)",
     "Menyebarkan pemberitahuan bohong atau informasi menyesatkan yang merugikan konsumen dalam transaksi elektronik",
     "Penjara maks. 6 tahun dan/atau denda maks. Rp1 miliar"],
    ["UU ITE Ps. 32, 33, 34, 35 jo. Ps. 48\u201351 ayat (1)",
     "Interferensi data, gangguan sistem, penyalahgunaan perangkat, dan pemalsuan data elektronik",
     "Penjara maks. 10\u201312 tahun"],
    ["UU PDP (UU 27/2022) Ps. 67 dan Ps. 68",
     "Pengumpulan/pengungkapan data pribadi tanpa hak; pemalsuan data pribadi",
     "Penjara maks. 4 tahun/Rp4 M; maks. 6 tahun/Rp6 M"],
    ["UU P2SK (UU 4/2023) Ps. 306",
     "Penyelenggara/pelaku usaha sektor keuangan melanggar ketentuan APU-PPT",
     "Penjara dan/atau denda (kini alternatif dan berkategori)"],
], left=0.6, top=1.4, width=12.1, col_w=[3.3, 5.6, 3.2], font_size=9, header_size=9.5, row_h=0.6)
tf = textbox(s, 0.6, 6.62, 12.1, 0.4)
put(tf, "Catatan peralihan: KUHP Pasal 622 mencabut dan mengalihkan pengacuan sejumlah pasal UU ITE ke KUHP "
        "(Ps. 30 dan 46 \u2192 Ps. 332; Ps. 31 dan 47 \u2192 Ps. 258 ayat (2)). Judi online tetap dijerat "
        "berdasarkan Pasal 27 ayat (2) UU ITE dan Pasal 426 KUHP.",
    size=8.5, color=GREY, space_after=0, first=True)
footer(s, 16)
notes(s, "Poin penting bagi OVO: KUHP Pasal 608 adalah dasar perlindungan bagi pihak pelapor \u2014 pelaporan TKM "
         "tidak boleh menjadi dasar pemidanaan pelapor yang taat. Ini argumen untuk memperkuat budaya pelaporan. "
         "Perhatikan pula ketentuan peralihan: sejumlah pasal UU ITE sudah dicabut dan dialihkan ke KUHP, sehingga "
         "surat dakwaan wajib memeriksa pengacuan pasal yang berlaku pada saat perbuatan dilakukan.")

# ============================== SLIDE 17 — UU 1/2026 ==============================
s = prs.slides.add_slide(BLANK)
header(s, "Bagian IV \u2022 Penyesuaian pidana", "Bagaimana UU 1/2026 Mengubah Peta Ancaman Hukuman")
tf = textbox(s, 0.6, 1.42, 12.1, 5.4)
bullets(tf, [
    (0, "Fungsi undang-undang: menyelaraskan ancaman pidana pada undang-undang sektoral dengan sistem pemidanaan KUHP Nasional", 15, True),
    (0, "Empat perubahan pokok:", 15, True),
    (1, "Pidana minimum khusus (\u201cpaling singkat X tahun\u201d) dihapus pada delik sektoral; dikecualikan untuk korupsi, terorisme, HAM berat, dan TPPU", 13),
    (1, "Sanksi penjara dan denda yang semula kumulatif (dan) menjadi alternatif (atau)", 13),
    (1, "Denda dikonversi ke kategori Pasal 79 KUHP \u2014 Kategori I Rp1 juta hingga Kategori VIII Rp50 miliar", 13),
    (1, "Penjara lebih dari 15 tahun tanpa alternatif dibatasi 15 tahun; pidana seumur hidup tanpa alternatif menjadi 20 tahun", 13),
    (0, "Konsekuensi bagi penyidikan dan penuntutan:", 15, True),
    (1, "Fokus bergeser dari panjang pidana badan ke kombinasi pemidanaan, pencabutan hak, dan pemulihan aset", 13),
    (1, "Penerapan asas lex specialis menjadi wajib: pilih pasal sektoral paling spesifik sebelum pasal umum KUHP", 13),
    (1, "Konstruksi berlapis (perbarengan dan penyertaan) tetap relevan untuk menjangkau pemberi perintah dan pemilik manfaat akhir", 13),
    (0, "Contoh terverifikasi: UU 42/1999 Ps. 35 \u2014 penjara maks. 5 tahun dan/atau denda Kategori IV; Ps. 36 \u2014 penjara maks. 2 tahun dan/atau denda Kategori III", 14, True, RED),
])
footer(s, 17)
notes(s, "Pesan strategis: hukuman badan bukan lagi satu-satunya daya paksa. Untuk kejahatan keuangan terorganisasi, "
         "efek jera lebih besar datang dari pemblokiran aset, pencabutan hak, dan tindak lanjut TPPU.")

# ============================== SLIDE 18 — HUKUM ACARA ==============================
s = prs.slides.add_slide(BLANK)
header(s, "Bagian IV \u2022 Hukum acara", "Kewenangan Penyidik: Pemblokiran, Pemutusan Akses, dan Penyadapan")
table(s, [
    ["Dasar hukum", "Kewenangan", "Syarat dan batas waktu"],
    ["KUHAP Ps. 140 ayat (1), (2), (3), dan (6)",
     "Pemblokiran oleh Penyidik, Penuntut Umum, atau Hakim atas objek terkait tindak pidana",
     "Harus mendapat izin ketua pengadilan negeri; jangka waktu 1 tahun, dapat diperpanjang 2 kali untuk 6 bulan"],
    ["KUHAP Ps. 140 ayat (7), (8), dan (9)",
     "Pemblokiran dalam keadaan mendesak tanpa izin ketua pengadilan negeri",
     "Meliputi potensi dialihkannya harta kekayaan, tindak pidana terkait informasi dan transaksi elektronik, dan permufakatan terorganisasi; persetujuan diminta paling lama 2\u00d724 jam"],
    ["KUHAP Ps. 140 ayat (10), (11), (12), dan (13)",
     "Penetapan ketua pengadilan negeri dan penolakan permohonan",
     "Penetapan paling lama 2\u00d724 jam; bila ditolak, pemblokiran dibuka paling lama 3 hari kerja"],
    ["KUHAP Ps. 136 ayat (1)",
     "Penyadapan untuk kepentingan penyidikan",
     "Tata cara diatur dengan undang-undang mengenai penyadapan"],
    ["UU ITE Ps. 43 ayat (5) huruf l",
     "Memerintahkan penyelenggara sistem elektronik memutus akses sementara: akun media sosial, rekening bank, uang elektronik, dan/atau aset digital",
     "Dalam rangka penyidikan tindak pidana di bidang ITE (perubahan UU 1/2024)"],
    ["UU ITE Ps. 42 dan Ps. 44",
     "Penyidikan tindak pidana ITE dan kedudukan alat bukti elektronik",
     "Penggeledahan/penyitaan sistem elektronik atas izin ketua pengadilan negeri"],
    ["UU 8/2010 Ps. 71 dan Ps. 74",
     "Kewenangan penyidik memerintahkan pemblokiran harta kekayaan serta kewenangan penyidik tindak pidana asal",
     "Tidak termasuk pasal yang dialihkan \u2014 tetap berlaku untuk prosedur TPPU"],
], left=0.6, top=1.4, width=12.1, col_w=[3.1, 5.3, 3.7], font_size=8.5, header_size=9.5, row_h=0.62)
footer(s, 18)
notes(s, "Ini slide kunci untuk rekomendasi selanjutnya. Jalur pemblokiran mendesak SUDAH tersedia dalam norma; "
         "yang belum ada adalah prosedur teknis dan kanal komunikasi 24/7 antara penyidik dan PJP. "
         "Sebutkan bahwa Pasal 3, 4, dan 5 UU TPPU dialihkan ke KUHP Pasal 607, sementara ketentuan acara seperti "
         "Pasal 71 dan Pasal 74 tetap berlaku.")

# ============================== SLIDE 19 — REGULASI APU-PPT ==============================
s = prs.slides.add_slide(BLANK)
header(s, "Bagian IV \u2022 Regulasi sektor", "Kerangka APU-PPT dan Arsitektur Deteksi Berbasis Machine Learning")
table(s, [
    ["Regulasi", "Pokok pengaturan", "Implikasi operasional"],
    ["POJK 8/2023",
     "Penerapan program APU, PPT, dan PPPSPM di sektor jasa keuangan",
     "Pendekatan berbasis risiko, CDD/EDD, pemantauan transaksi berkelanjutan, pelaporan TKM"],
    ["POJK 24/2025",
     "Pengelolaan rekening pada bank umum",
     "Dasar tata kelola pembukaan dan pengelolaan rekening dalam kerangka follow the money"],
    ["POJK 40/2024",
     "Layanan pendanaan bersama berbasis teknologi informasi (LPBBTI)",
     "Kepatuhan penyelenggara fintech lending dan pengendalian risiko identitas"],
    ["POJK 22/2023",
     "Pelindungan konsumen dan masyarakat di sektor jasa keuangan",
     "Transparansi dasar pemblokiran dan mekanisme keberatan nasabah"],
    ["PBI 22/23/2020 dan PBI 23/6/PBI/2021",
     "Sistem pembayaran dan penyedia jasa pembayaran (termasuk QRIS)",
     "Kepatuhan PJP, tata kelola merchant, dan pengawasan kanal pembayaran"],
    ["UU 27/2022 (PDP)",
     "Pelindungan data pribadi (Pasal 65\u201368)",
     "Kewajiban pengendali data atas data nasabah yang diproses untuk verifikasi"],
], left=0.6, top=1.4, width=12.1, col_w=[2.6, 4.4, 5.0], font_size=9, header_size=9.5, row_h=0.66)
tf = textbox(s, 0.6, 6.55, 12.1, 0.4)
put(tf, "Catatan teknis: pemantauan berbasis ambang statis tidak memadai menghadapi modus terotomatisasi. "
        "Diperlukan lapisan telemetri peranti, verifikasi kriptografis, analitik graf relasi akun, dan biometrik perilaku.",
    size=9, color=GREY, space_after=0, first=True)
footer(s, 19)
notes(s, "Sebutkan bahwa arsitektur deteksi idealnya bertingkat: (1) telemetri peranti dan verifikasi kriptografis "
         "saat masuk; (2) analitik graf relasi akun\u2013peranti\u2013merchant; (3) biometrik perilaku untuk deteksi "
         "pengambilalihan akun. Sistem rule-based tetap dipakai, tetapi sebagai pelengkap, bukan tulang punggung.")

# ============================== SLIDE 20 — SECTION V ==============================
s = prs.slides.add_slide(BLANK)
section(s, "Bagian V", "Tantangan Yuridis dan Dampak Kebijakan Publik",
        "Kesenjangan kecepatan, beban pembuktian, atribusi lintas yurisdiksi, dan hak warga negara.", 20)
notes(s, "Bagian ini jujur tentang hambatan di sisi kami sendiri. Kredibilitas paparan justru naik bila "
         "keterbatasan aparat diakui terbuka, karena itu prasyarat kerja sama.")

# ============================== SLIDE 21 — SPEED GAP ==============================
s = prs.slides.add_slide(BLANK)
header(s, "Bagian V \u2022 Tantangan yuridis", "Kesenjangan Kecepatan antara Modus dan Prosedur Hukum")
tf = textbox(s, 0.6, 1.42, 12.1, 5.4)
bullets(tf, [
    (0, "Kecepatan pelaku: dana dipindahkan, dipecah, dan dicairkan menjadi uang tunai dalam hitungan menit melalui otomatisasi", 15, True),
    (0, "Kecepatan prosedur: penyidik terikat KUHAP serta hukum perbankan dalam memohon pembukaan data rahasia nasabah dan penghentian transaksi", 15, True),
    (1, "Administrasi surat perintah pemblokiran, koordinasi permohonan izin ke pengadilan negeri, dan verifikasi kepatuhan internal PJP memerlukan rentang waktu berhari-hari", 13),
    (1, "Ketika surat perintah tiba pada PJP, saldo rekening penampung telah dikosongkan", 13),
    (0, "Kehati-hatian industri yang memperlambat eksekusi", 15, True),
    (1, "Kekhawatiran atas risiko gugatan perdata atau tuntutan wanprestasi dari pemilik rekening yang sah", 13),
    (1, "Ketiadaan kesepakatan format notifikasi dan pembagian tanggung jawab hukum antara aparat dan PJP", 13),
    (0, "Temuan penting: hambatan bukan pada norma", 15, True, RED),
    (1, "KUHAP Pasal 140 ayat (7) sampai (9) sudah membuka jalur pemblokiran mendesak tanpa izin ketua pengadilan negeri, dengan persetujuan diminta dalam 2\u00d724 jam", 13, True, RED),
    (1, "Yang belum tersedia adalah prosedur teknis, kanal komunikasi 24/7, dan format parameter digital yang dapat dieksekusi PJP dalam hitungan jam", 13, True, RED),
    (0, "Atribusi lintas yurisdiksi: server command and control di luar negeri, rantai proksi berlapis, dan layanan perutean anonim menyulitkan pembuktian hingga pemilik manfaat akhir", 15, True),
    (0, "Konsekuensi pembuktian: satu berkas perkara memuat ribuan transaksi pada puluhan PJP dengan format data yang berbeda-beda", 15, True),
])
footer(s, 21)
notes(s, "Kalimat kunci: 'Normanya sudah ada; yang kami butuhkan adalah kanal eksekusinya.' Ini membuka jalan ke "
         "rekomendasi protokol tanggap darurat.")

# ============================== SLIDE 22 — DAMPAK PUBLIK ==============================
s = prs.slides.add_slide(BLANK)
header(s, "Bagian V \u2022 Dampak kebijakan publik", "Externalitas Sosial: Penangguhan Bansos 1,49 Juta KPM")
tf = textbox(s, 0.6, 1.42, 12.1, 5.4)
bullets(tf, [
    (0, "Pemadanan data intelijen transaksi mencurigakan PPATK dengan basis data penerima bantuan sosial Kementerian Sosial", 15, True),
    (1, "Penangguhan penyaluran hak bantuan terhadap 1,49 juta Keluarga Penerima Manfaat (KPM) yang terindikasi transaksi perjudian daring", 13),
    (0, "Risiko yang harus dikelola bersama:", 15, True),
    (1, "Sanksi otomatis berbasis analitika finansial tanpa diimbangi mekanisme klarifikasi yang adil berpotensi menciderai hak konstitusional warga yang tidak bersalah", 13),
    (1, "Sebagian besar nama dalam laporan adalah korban manipulasi: pencatutan fotokopi e-KTP dengan dalih bantuan tunai, penyewaan rekening dengan kompensasi kecil, dan kebocoran data kependudukan", 13),
    (1, "Rekening korban kemudian dikuasai sindikat sebagai simpul penampungan aliran dana ilegal", 13),
    (0, "Persinggungan dengan tata kelola industri pembayaran:", 15, True),
    (1, "Pemblokiran akun tanpa dasar pembuktian yang memadai memunculkan risiko komplain konsumen dan gugatan layanan", 13),
    (1, "Kewajiban transparansi dasar pemutusan layanan dan penyediaan kanal keberatan nasabah \u2014 POJK 22/2023", 13),
    (0, "Kesimpulan: penegakan hukum dan perlindungan sosial harus berjalan bersamaan; korban tidak boleh diperlakukan sebagai pelaku", 15, True, RED),
])
footer(s, 22)
notes(s, "Sampaikan bahwa kerja sama dengan PJP juga bermanfaat untuk memisahkan profil korban eksploitasi dari "
         "operator kejahatan, sehingga penargetan sanksi menjadi lebih presisi dan beban pengaduan turun.")

# ============================== SLIDE 23 — SECTION VI ==============================
s = prs.slides.add_slide(BLANK)
section(s, "Bagian VI", "Rekomendasi Aksi Sinergi Ditreskrimsus Polda Sulsel dan Industri Sistem Pembayaran",
        "Empat inisiatif yang dapat langsung dieksekusi, lengkap dengan dasar hukum dan pihak penanggung jawab.", 23)
notes(s, "Empat inisiatif ini sengaja dirumuskan operasional agar dapat ditindaklanjuti tanpa menunggu perubahan "
         "regulasi. Setiap inisiatif memuat dasar hukum dan keluaran yang terukur.")

# ============================== SLIDE 24 — R1 ==============================
s = prs.slides.add_slide(BLANK)
header(s, "Bagian VI \u2022 Rekomendasi 1", "Protokol Tanggap Darurat Pemblokiran Saldo Terintegrasi")
tf = textbox(s, 0.6, 1.42, 12.1, 5.4)
bullets(tf, [
    (0, "Jalur koordinasi terenkripsi (dedicated secure channel) antara penyelidik Ditreskrimsus dan Divisi Kepatuhan serta AML PJP, beroperasi 24 jam sehari dan 7 hari seminggu", 14, True),
    (0, "Dalam situasi darurat, penyidik menerbitkan surat pemberitahuan penghentian sementara berbasis parameter digital awal:", 14, True),
    (1, "Identitas transaksi, NIK pedagang, dan sidik jari digital peranti (device hash)", 13),
    (1, "PJP menahan saldo dalam jangka waktu maksimal 2 jam, disusul penyampaian berkas penetapan pemblokiran resmi dari pengadilan negeri sesuai tenggat perundang-undangan", 13),
    (0, "Dasar hukum yang menjadi fondasi:", 14, True),
    (1, "KUHAP Pasal 140 ayat (7) sampai (9) \u2014 pemblokiran dalam keadaan mendesak tanpa izin ketua pengadilan negeri, dengan alasan: potensi dialihkannya harta kekayaan, tindak pidana terkait informasi dan transaksi elektronik, serta permufakatan tindak pidana terorganisasi", 12.5),
    (1, "UU ITE Pasal 43 ayat (5) huruf l \u2014 perintah pemutusan akses sementara terhadap rekening bank, uang elektronik, dan aset digital", 12.5),
    (0, "Prasyarat tata kelola yang perlu disepakati:", 14, True),
    (1, "Format notifikasi standar, jejak audit lengkap, klausul pembagian tanggung jawab hukum, serta kontak tunggal (single point of contact) per PJP", 13),
    (1, "Mekanisme koreksi cepat bila penahanan saldo tidak dilanjutkan dengan penetapan pengadilan \u2014 perlindungan bagi kedua pihak", 13),
])
footer(s, 24)
notes(s, "Rekomendasi unggulan. Tekankan bahwa ini bukan permintaan pemblokiran tanpa dasar, melainkan penahanan "
         "saldo berbasis parameter digital dengan tenggat 2 jam dan pengesahan pengadilan menyusul \u2014 persis "
         "skema yang dibuka oleh KUHAP Pasal 140 ayat (7) sampai (9).")

# ============================== SLIDE 25 — R2 ==============================
s = prs.slides.add_slide(BLANK)
header(s, "Bagian VI \u2022 Rekomendasi 2", "Standardisasi Berkas Forensik Bukti Digital")
tf = textbox(s, 0.6, 1.42, 12.1, 5.4)
bullets(tf, [
    (0, "Menyusun pedoman pengemasan alat bukti digital (standardized digital evidence packaging) selaras ISO/IEC 27037 dan UU ITE Pasal 44", 14, True),
    (0, "Atribut wajib pada setiap berkas riwayat transaksi dan log sistem yang diserahkan PJP kepada kepolisian:", 14, True),
    (1, "IP address sumber dan tujuan, port, timestamp berstandar UTC terkalibrasi, device hardware ID, session ID, serta lokasi registrasi geografis", 13),
    (0, "Penguatan integritas bukti:", 14, True),
    (1, "Nilai sidik jari digital (cryptographic hash SHA-256) dan tanda tangan digital bersertifikasi pada saat ekstraksi data", 13),
    (1, "Berita acara serah terima dan penelusuran penguasaan bukti elektronik (chain of custody) dari PJP ke penyidik", 13),
    (0, "Format dan layanan yang diusulkan:", 14, True),
    (1, "Berkas mesin-terbaca (CSV/JSON) untuk analisis, disertai berkas PDF tersegel untuk keperluan persidangan", 13),
    (1, "SLA penyediaan data, template surat permintaan baku, dan penunjukan pejabat penghubung di kedua pihak", 13),
    (0, "Manfaat: berkas perkara tahan uji di persidangan, memangkas gugatan atas keabsahan bukti, dan mempercepat analisis lintas PJP", 14, True, RED),
])
footer(s, 25)
notes(s, "Kaitkan dengan pengalaman nyata: perbedaan format data antar PJP adalah penyebab utama lambatnya "
         "rekonstruksi aliran dana. Standardisasi ini menguntungkan industri karena mengurangi permintaan berulang.")

# ============================== SLIDE 26 — R3 ==============================
s = prs.slides.add_slide(BLANK)
header(s, "Bagian VI \u2022 Rekomendasi 3", "Pengetatan Pengawasan Agregator dan Pengendalian Likuiditas Merchant")
tf = textbox(s, 0.6, 1.42, 12.1, 5.4)
bullets(tf, [
    (0, "Verifikasi faktual atas kepemilikan aset usaha fisik atau eksistensi platform niaga digital yang sah pada setiap pendaftaran merchant baru", 14, True),
    (0, "Khusus merchant aggregator: uji tuntas pedagang (KYM) berjenjang, audit sampling berkala, dan pengawasan kualitas data onboarding", 14, True),
    (0, "Mitigasi merchant fiktif berumur pendek:", 14, True),
    (1, "Pembatasan akumulasi nominal dan kecepatan transaksi (velocity ceiling) selama 30 hari pertama masa operasional pedagang", 13),
    (1, "Penonaktifan fitur transfer pencairan otomatis (instant auto-disbursement) menuju dompet digital perorangan sebelum entitas membuktikan profil transaksi yang konsisten", 13),
    (0, "Pengendalian kanal QRIS:", 14, True),
    (1, "Setiap kode QRIS yang diproduksi agregator dipetakan secara kaku ke domain situs resmi berizin untuk mencegah penyisipan kode pembayaran pada situs perjudian daring aktif", 13),
    (1, "Pemantauan risiko pedagang berkelanjutan (merchant risk profiling) dengan indikator: pembeli berulang berjumlah kecil, nominal seragam, waktu transaksi tidak wajar", 13),
    (0, "Dasar hukum dan kewajiban yang mengikat: POJK 8/2023 (CDD/EDD, pemantauan berkelanjutan), POJK 22/2023, serta ketentuan Bank Indonesia tentang PJP dan QRIS", 14, True, RED),
])
footer(s, 26)
notes(s, "Poin ini paling konkret untuk OVO. Velocity ceiling 30 hari adalah kontrol berbiaya rendah dengan dampak "
         "besar terhadap merchant fiktif, karena sindikat biasanya memutar dana besar dalam waktu singkat.")

# ============================== SLIDE 27 — R4 ==============================
s = prs.slides.add_slide(BLANK)
header(s, "Bagian VI \u2022 Rekomendasi 4", "Pembentukan Gugus Tugas Intelijen Keuangan Siber Wilayah")
tf = textbox(s, 0.6, 1.42, 12.1, 5.4)
bullets(tf, [
    (0, "Gugus tugas taktis anti-kejahatan siber finansial regional Sulawesi Selatan yang diprakarsai Polda Sulawesi Selatan", 14, True),
    (0, "Komposisi: Ditreskrimsus Polda Sulsel, perwakilan PPATK, Kantor Perwakilan Bank Indonesia Sulawesi Selatan, OJK Regional 6 Sulselbar, dan pimpinan divisi kepatuhan PJP", 14, True),
    (0, "Fungsi yang dijalankan:", 14, True),
    (1, "Pertukaran intelijen ancaman (threat intelligence sharing) secara berkala mengenai modus yang sedang bergerak di daerah", 13),
    (1, "Evaluasi pergeseran modus operandi berbasis AI pada tingkat kewilayahan", 13),
    (1, "Penyelarasan model machine learning internal industri dengan temuan penindakan kepolisian", 13),
    (1, "Penyelenggaraan simulasi bersama penanganan insiden kejahatan keuangan digital berintensitas tinggi (latihan meja)", 13),
    (0, "Tata kelola: penunjukan penanggung jawab pada masing-masing lembaga, siklus pertemuan tetap, laporan hasil kepada pimpinan, dan perlindungan atas kerahasiaan data yang dipertukarkan", 14, True),
    (0, "Keluaran yang diharapkan dalam 90 hari: satu kesepakatan kerja sama, satu daftar indikator peringatan dini bersama, dan satu laporan penilaian ancaman regional", 14, True, RED),
])
footer(s, 27)
notes(s, "Fungsi gugus tugas bukan menambah forum seremonial, melainkan menyatukan data ancaman dan indikator "
         "peringatan dini. Sebutkan pula bahwa gugus tugas dapat menjadi wadah uji coba protokol tanggap darurat.")

# ============================== SLIDE 28 — ROADMAP ==============================
s = prs.slides.add_slide(BLANK)
header(s, "Bagian VI \u2022 Peta jalan", "Rencana Tindak Lanjut 90 Hari Pertama")
table(s, [
    ["Tahap", "Aktivitas", "Keluaran"],
    ["0\u201330 hari", "Penyusunan draf protokol tanggap darurat pemblokiran dan penetapan jalur komunikasi terenkripsi",
     "Draf SOP beserta lampiran format notifikasi dan parameter digital"],
    ["0\u201330 hari", "Pemetaan penanggung jawab dan kontak siaga 24/7 pada kedua pihak",
     "Daftar kontak terverifikasi dan bagan eskalasi"],
    ["30\u201360 hari", "Uji coba protokol melalui simulasi penahanan saldo 2 jam",
     "Berita acara uji coba dan daftar perbaikan prosedur"],
    ["30\u201360 hari", "Penyusunan standar format data bukti digital selaras ISO/IEC 27037",
     "Template data, SLA penyediaan data, dan template surat permintaan"],
    ["60\u201390 hari", "Penerapan pengetatan KYM merchant baru dan pembatasan kecepatan transaksi",
     "Kebijakan internal PJP dan indikator pemantauan pedagang"],
    ["60\u201390 hari", "Pembentukan gugus tugas intelijen keuangan siber regional dan rapat perdana",
     "Kesepakatan kerja sama, indikator peringatan dini bersama, laporan penilaian ancaman"],
], left=0.6, top=1.4, width=12.1, col_w=[1.7, 6.4, 4.0], font_size=9.5, header_size=10, row_h=0.78)
footer(s, 28)
notes(s, "Tutup bagian rekomendasi dengan komitmen jadwal. Sarankan pembentukan kelompok kerja kecil (3\u20135 orang "
         "per lembaga) yang bertemu dua minggu sekali agar target 90 hari realistis.")

# ============================== SLIDE 29 — PENUTUP ==============================
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, 13.333, 7.5, NAVY)
rect(s, 0, 0, 13.333, 0.16, RED)
tf = textbox(s, 1.0, 1.2, 11.3, 4.6)
put(tf, "PENUTUP", size=12, color=GOLD, bold=True, space_after=14, first=True)
put(tf, "Kolaborasi aparat penegak hukum dan industri sistem pembayaran adalah prasyarat, bukan pilihan.",
    size=24, color=WHITE, bold=True, space_after=16, line_spacing=0.98)
put(tf, "Dua kata kunci yang menyatukan seluruh rekomendasi:", size=15,
    color=RGBColor(0xC7, 0xD3, 0xE0), space_after=10)
put(tf, [("\u25aa Kecepatan \u2014 ", True, GOLD, 16),
         ("protokol tanggap darurat berbasis KUHAP Pasal 140 ayat (7) sampai (9) untuk menutup kesenjangan waktu pemblokiran.", False, WHITE, 14)],
    space_after=8)
put(tf, [("\u25aa Integritas \u2014 ", True, GOLD, 16),
         ("standardisasi bukti digital bersertifikasi hash dan tanda tangan digital agar setiap berkas perkara tahan uji.", False, WHITE, 14)],
    space_after=18)
put(tf, "Terima kasih  \u2014  ruang diskusi dan tanya jawab", size=18, color=WHITE, bold=True, space_after=0)
tf2 = textbox(s, 1.0, 6.4, 11.3, 0.7)
put(tf2, "Kombes Pol Taufik Herdiansyah \u2014 Direktur Reserse Kriminal Khusus, Kepolisian Daerah Sulawesi Selatan",
    size=11, color=RGBColor(0x8A, 0x9B, 0xAD), space_after=0, first=True)
notes(s, "Tutup dengan tiga ajakan: (1) menyepakati protokol tanggap darurat dalam 30 hari; (2) menunjuk kontak "
         "tunggal siaga 24/7; (3) menjadwalkan simulasi bersama. Siapkan jawaban atas kemungkinan pertanyaan PJP "
         "mengenai perlindungan hukum atas pemblokiran mendesak \u2014 jawabannya KUHAP Pasal 140 ayat (7) sampai (13) "
         "beserta mekanisme koreksi bila permohonan ditolak.")

out = "/home/ubuntu/penyidikan/analisis/workshop-ovo-2026/Draf_Paparan_Kejahatan_Keuangan_Berbasis_AI_Ditreskrimsus_Polda_Sulsel.pptx"
import os
os.makedirs(os.path.dirname(out), exist_ok=True)
prs.save(out)
print("SAVED:", out, "| slides:", len(prs.slides.__iter__.__self__._sldIdLst))
