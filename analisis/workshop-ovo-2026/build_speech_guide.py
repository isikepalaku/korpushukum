#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Naskah Panduan Bicara (Talking Points & Speech Guidance) DOCX
Narasumber: Dirreskrimsus Polda Sulsel (Kombes Pol Taufik Herdiansyah)
Acara: Workshop Tertutup OVO & OVO Finansial - Makassar, 22 Oktober 2026.
Berdasarkan Deck Bersih 12 Slide (Paparan_Workshop_OVO_Dirreskrimsus_Polda_Sulsel_Clean.pptx).
"""

import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

doc = Document()

# Set standard margins (A4, 2.54 cm all sides)
sections = doc.sections
for s in sections:
    s.page_width = Inches(8.27)
    s.page_height = Inches(11.69)
    s.top_margin = Inches(1.0)
    s.bottom_margin = Inches(1.0)
    s.left_margin = Inches(1.0)
    s.right_margin = Inches(1.0)

# Colors
NAVY_RGB = RGBColor(10, 25, 47)
RED_RGB = RGBColor(186, 26, 26)
DARK_RGB = RGBColor(33, 37, 41)
GREY_RGB = RGBColor(108, 117, 125)

# Styling Helper Functions
def set_para_font(p, name="Tahoma", size=11, color=DARK_RGB, bold=False, italic=False):
    for r in p.runs:
        r.font.name = name
        r.font.size = Pt(size)
        r.font.color.rgb = color
        r.font.bold = bold
        r.font.italic = italic

def add_p(text, size=11, bold=False, italic=False, color=DARK_RGB, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, line_spacing=1.15):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    r = p.add_run(text)
    r.font.name = "Tahoma"
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    return p

def add_heading_1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Tahoma"
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = NAVY_RGB
    return p

def add_heading_2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Tahoma"
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RED_RGB
    return p

def add_bullet(text, bold_prefix="", size=10.5):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        r_b.font.name = "Tahoma"
        r_b.font.size = Pt(size)
        r_b.font.bold = True
        r_b.font.color.rgb = DARK_RGB
    r_t = p.add_run(text)
    r_t.font.name = "Tahoma"
    r_t.font.size = Pt(size)
    r_t.font.color.rgb = DARK_RGB
    return p

def set_cell_shading(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color_hex)
    tcPr.append(shd)

def add_callout(quote_text, label="POIN KUNCI / CATATAN DIRRESKRIMSUS:"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = tbl.cell(0, 0)
    set_cell_shading(c, "F1F5F9")
    c.width = Inches(6.27)
    
    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(3)
    r1 = p.add_run(label + "\n")
    r1.font.name = "Tahoma"
    r1.font.size = Pt(10)
    r1.font.bold = True
    r1.font.color.rgb = RED_RGB
    
    r2 = p.add_run(f'"{quote_text}"')
    r2.font.name = "Tahoma"
    r2.font.size = Pt(10.5)
    r2.font.italic = True
    r2.font.color.rgb = DARK_RGB
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

# ==================== JUDUL & METADATA ====================
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_after = Pt(2)
r = p_title.add_run("NASKAH PANDUAN BICARA (TALKING POINTS)")
r.font.name = "Tahoma"
r.font.size = Pt(15)
r.font.bold = True
r.font.color.rgb = NAVY_RGB

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_after = Pt(14)
r = p_sub.add_run("Pemaparan Dirreskrimsus Polda Sulsel pada Workshop Tertutup OVO & OVO Finansial\nHotel Hyatt Place Makassar — Kamis, 22 Oktober 2026 (14.25 – 15.10 WITA)")
r.font.name = "Tahoma"
r.font.size = Pt(11)
r.font.bold = True
r.font.color.rgb = RED_RGB

# Meta Box
tbl_meta = doc.add_table(rows=4, cols=2)
tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_data = [
    ("Narasumber", "Kombes Pol Taufik Herdiansyah (Direktur Reserse Kriminal Khusus Polda Sulsel)"),
    ("Dasar Penugasan", "Surat Undangan PT Visionet Internasional (OVO) No. 338/PA-VI/C/IX/2026"),
    ("Tema Paparan", "Penguatan Deteksi dan Pencegahan Kejahatan Keuangan Berbasis AI di Era Digital"),
    ("Audiens Utama", "Divisi AML, Compliance, Public Affairs PT Visionet Internasional & PT Indonusa Bara Sejahtera")
]
for idx, (k, v) in enumerate(meta_data):
    row = tbl_meta.rows[idx]
    c0, c1 = row.cells[0], row.cells[1]
    c0.width, c1.width = Inches(1.8), Inches(4.47)
    set_cell_shading(c0, "E2E8F0")
    set_cell_shading(c1, "F8FAFC")
    p0 = c0.paragraphs[0]
    p0.paragraph_format.space_after = Pt(2)
    r0 = p0.add_run(k)
    r0.font.name = "Tahoma"
    r0.font.size = Pt(9.5)
    r0.font.bold = True
    p1 = c1.paragraphs[0]
    p1.paragraph_format.space_after = Pt(2)
    r1 = p1.add_run(v)
    r1.font.name = "Tahoma"
    r1.font.size = Pt(9.5)

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# ==================== STRUKTUR WAKTU 45 MENIT ====================
add_heading_1("1. PANDUAN MANAJEMEN WAKTU & STRUKTUR SESI (TOTAL 45 MENIT)")
add_p("Pemaparan dirancang padat dan interaktif agar membuka ruang komitmen konkret dari manajemen PJP. Alokasi waktu:")
add_bullet("Pembukaan, apresiasi kemitraan, dan 3 temuan kunci lapangan.", "Menit 00.00 – 05.00 (5 Menit): ")
add_bullet("Data makro PPATK, anomali lonjakan QRIS 88,6%, dan pembongkaran botnet 2.000 akun Makassar.", "Menit 05.00 – 18.00 (13 Menit): ")
add_bullet("Konstruksi KUHP 2023 pasca UU 1/2026, hak blokir seketika KUHAP 2025 Ps. 140, dan UU ITE 2024.", "Menit 18.00 – 28.00 (10 Menit): ")
add_bullet("Speed gap, problem rekening joki, dan mitigasi penangguhan 1,49 juta KPM bansos.", "Menit 28.00 – 35.00 (7 Menit): ")
add_bullet("4 rekomendasi aksi taktis (SOP blokir 2 jam, bukti digital ISO, KYM QRIS) + Roadmap 90 Hari.", "Menit 35.00 – 43.00 (8 Menit): ")
add_bullet("Penegasan prinsip kolaborasi dan transisi ke sesi tanya jawab.", "Menit 43.00 – 45.00 (2 Menit): ")

# ==================== PANDUAN PER SLIDE ====================
add_heading_1("2. NASKAH DAN PEDOMAN BICARA PER SLIDE")

# SLIDE 1
add_heading_2("Slide 1 — Cover / Judul Pembuka")
add_p("Tujuan: Mengambil kendali forum, menyapa direksi dan pimpinan kepatuhan OVO secara profesional, dan menetapkan nada kemitraan penegakan hukum.")
add_callout(
    "Selamat siang rekan-rekan direksi, pimpinan Divisi Kepatuhan, AML, dan Public Affairs OVO dan OVO Finansial. "
    "Saya hadir hari ini bukan semata-mata berbicara sebagai aparat penegak hukum yang datang membawa daftar kesalahan industri, "
    "tetapi sebagai mitra strategis dalam menjaga integritas sistem keuangan nasional. "
    "Di era di mana pelaku kejahatan memanfaatkan kecerdasan buatan dan botnet terdistribusi, pertahanan kita tidak boleh lagi berjalan sendiri-sendiri.",
    "INTONASI: Tegas, Mengayomi, dan Menegakkan Kemitraan"
)

# SLIDE 2
add_heading_2("Slide 2 — Executive Briefing: 3 Titik Kritis Lapangan")
add_p("Tujuan: Memberikan 'peta mental' kepada audiens agar memahami 3 pilar yang akan dibahas tanpa bertele-tele.")
add_bullet("Jelaskan bahwa sistem pemantauan transaksi statis (>Rp100 juta) sudah usang. Pelaku sengaja memilih transaksi receh puluhan ribu rupiah via QRIS agar lolos radar.", "1. Pergeseran ke QRIS Mikro: ")
add_bullet("Buktikan bahwa kejahatan siber di Makassar sudah berevolusi menjadi Cybercrime-as-a-Service (CaaS). Sindikat lokal mengoperasikan peternakan ribuan gawai otomatis.", "2. Industrialisasi Botnet: ")
add_bullet("Tekankan bahwa pasal pidana sudah sangat lengkap. Masalah utamanya adalah 'speed gap'—pelaku mencairkan dana dalam 5 menit, sedangkan koordinasi konvensional memakan waktu 3 sampai 5 hari.", "3. Bottleneck Eksekusi: ")

# SLIDE 3
add_heading_2("Slide 3 — Dinamika Transaksi Mencurigakan: Ledakan Kanal QRIS")
add_p("Tujuan: Membedah data intelijen keuangan PPATK 2026 dan menyadarkan OVO bahwa dompet digital/QRIS adalah sasaran empuk utama sindikat.")
add_bullet("Angka Rp86,82 Triliun pada Semester I-2026. Penurunan yang melambat (-12,9%) membuktikan sindikat tidak berhenti, melainkan beradaptasi secara cerdas.", "Angka Kunci 1: ")
add_bullet("Pangsa QRIS 87,6% – 88,6%. Transfer bank turun drastis ke 11,4%. Mengapa? Karena QRIS memberikan instant settlement dan menyamarkan nama pemilik rekening di balik nama toko fiktif.", "Angka Kunci 2: ")
add_bullet("Akumulasi deposit QRIS mencapai Rp12,36 Triliun di TW I-2026. Saldo kejahatan mengalir di gerbang pembayaran PJP.", "Angka Kunci 3: ")

# SLIDE 4
add_heading_2("Slide 4 — Studi Kasus Makassar: Sindikat Botnet 2.000 Akun")
add_p("Tujuan: Menunjukkan bukti empiris hasil penindakan Subdit V Siber Ditreskrimsus Polda Sulsel di Makassar.")
add_callout(
    "Ini temuan riil penyidik kami di Kota Makassar: sebuah device farm yang mengoperasikan lebih dari 2.000 akun bot dan mengendalikan 180 situs aktif. "
    "Mereka tidak mempekerjakan operator manusia untuk deposit manual. Mereka menggunakan emulator yang IMEI, MAC Address, dan canvas fingerprint-nya diacak. "
    "Bagi server PJP, setiap bot terbaca sebagai ponsel warga Sulsel yang sah. Uang dipecah secara smurfing melalui skema many-to-one, lalu ditarik tunai lewat agen laku pandai di pelosok daerah sebelum kita sempat menerbitkan surat pemanggilan.",
    "NARASI EMPIRIS PENYIDIKAN SIBER"
)

# SLIDE 5
add_heading_2("Slide 5 — Vektor AI: Meretas Pintu Masuk e-KYC dan Merchant")
add_p("Tujuan: Mengkritisi kelemahan teknis verifikasi PJP secara lugas dan berbasis fakta forensik digital.")
add_bullet("Pelaku tidak lagi menodongkan HP ke foto di layar komputer. Pelaku me-root perangkat dan menyuntikkan video deepfake langsung ke data pipeline API aplikasi PJP. Solusi: PJP wajib memasang client attestation dan deteksi emulator.", "Digital Injection Attack: ")
add_bullet("NIK asli hasil kebocoran data dipadukan dengan foto wajah hasil generator GANs. OCR Dukcapil mengonfirmasi data teks cocok, dan verifikasi biometrik lolos. Solusi: Verifikasi kriptografis chip e-KTP melalui sensor NFC.", "Identitas Sintetik: ")
add_bullet("Pendaftaran merchant QRIS via merchant aggregator tanpa verifikasi fisik lokasi usaha.", "Merchant Fiktif: ")

# SLIDE 6
add_heading_2("Slide 6 — Dasar Hukum Pidana Materiil Pasca UU 1/2026")
add_p("Tujuan: Memberikan kepastian hukum positif yang berlaku sejak 2 Januari 2026 (KUHP Nasional UU 1/2023 & UU 1/2026).")
add_bullet("KUHP Ps. 332 (Akses Ilegal): Menggantikan ex Ps. 30 jo. 46 UU ITE berdasarkan Pasal 622 KUHP. Ancaman pidana 6–8 tahun atau denda Kategori V–VI.", "Akses Ilegal: ")
add_bullet("KUHP Ps. 258 ayat (2): Menggantikan ex Ps. 31 jo. 47 UU ITE terkait penyadapan dan intersepsi transmisi elektronik.", "Penyadapan: ")
add_bullet("UU ITE (UU 1/2024) Ps. 27 ayat (2) jo. Ps. 45 ayat (3): Khusus tindak pidana perjudian online tetap berlaku mandiri dengan ancaman pidana 10 tahun dan/atau denda Rp10 Miliar.", "Judi Online: ")
add_bullet("KUHP Ps. 607 & 608 (TPPU): Penjara maks 15 tahun. Garis bawahi Pasal 608: Memberikan perlindungan hukum penuh bagi PJP yang taat melaporkan Transaksi Keuangan Mencurigakan (TKM) ke PPATK/Polri.", "TPPU & Proteksi Pelapor: ")

# SLIDE 7
add_heading_2("Slide 7 — Instrumen Hukum Acara: Hak Pemblokiran Seketika KUHAP 2025")
add_p("Tujuan: Menghilangkan keraguan Divisi Legal/Compliance PJP terkait legalitas pemblokiran rekening.")
add_callout(
    "Bapak dan Ibu dari tim legal, mohon perhatikan ketentuan KUHAP Baru UU 20/2025 Pasal 140 ayat (7) sampai (9). "
    "Selama ini industri ragu menahan rekening karena takut digugat nasabah dengan dalih belum ada penetapan pengadilan. "
    "Undang-undang yang baru secara tegas mengatur: dalam keadaan mendesak—khususnya kejahatan terkait teknologi informasi dan potensi larinya aset—"
    "Penyidik berhak memerintahkan pemblokiran seketika TANPA IZIN PENGADILAN terlebih dahulu. "
    "Penetapan pengadilan diajukan dalam waktu 2x24 jam setelahnya. Artinya, dasar hukum PJP untuk membekukan saldo mencurigakan atas permintaan penyidik sudah sangat kokoh.",
    "POINT OF LAW: KUHAP 2025 PASAL 140 AYAT (7)-(9)"
)

# SLIDE 8
add_heading_2("Slide 8 — Kesenjangan Kecepatan (Speed Gap) & Beban Pembuktian")
add_p("Tujuan: Mengakui kelemahan koordinasi masa lalu dan mengajak industri memangkas birokrasi penyerahan bukti elektronik.")
add_bullet("Pelaku menarik tunai uang dalam hitungan menit, sedangkan birokrasi pemblokiran bank memakan waktu berhari-hari sehingga saldo yang tersisa saat surat tiba sering kali Rp 0.", "Speed Gap Riil: ")
add_bullet("Kritisi format data mutasi dari PJP yang kerap berupa scan PDF atau printout kaku yang tidak bisa diolah mesin. Penyidik membutuhkan file terstruktur (JSON/CSV) lengkap dengan IP Public, port, dan timestamp UTC.", "Standar Data Forensik: ")

# SLIDE 9
add_heading_2("Slide 9 — Eksternalitas Sosial: Penangguhan Bansos 1,49 Juta KPM")
add_p("Tujuan: Menunjukkan sensitivitas kemanusiaan dan keadilan publik (bersinergi dengan perspektif Ombudsman RI).")
add_bullet("1,49 juta penerima bansos yang ditangguhkan sebagian besar bukan bandar atau pemain judi, melainkan korban manipulasi.", "Fakta Korban: ")
add_bullet("Calo desa meminjam KTP warga miskin berdalih bantuan beras, lalu membuka rekening penampung atau mendaftar merchant QRIS.", "Modus Calo Identitas: ")
add_bullet("Tegaskan bahwa pemblokiran sepihak tanpa mekanisme klarifikasi yang adil (due process) berpotensi melahirkan maladministrasi dan menciderai hak dasar masyarakat miskin.", "Pencegahan Maladministrasi: ")

# SLIDE 10
add_heading_2("Slide 10 — 4 Rekomendasi Aksi Sinergi Ditreskrimsus – PJP")
add_p("Tujuan: Menyampaikan proposal kerja sama taktis konkret yang menjadi output utama lokakarya.")
add_bullet("Penahanan saldo sementara maksimal 2 jam berbasis parameter digital (NIK merchant, ID transaksi, hash device).", "1. Protokol Blokir Darurat 24/7: ")
add_bullet("Penyampaian data log transaksi dalam format standar ISO/IEC 27037 dibubuhi nilai hash SHA-256 agar rantai penguasaan bukti (chain of custody) sah di persidangan.", "2. Standarisasi Bukti Digital: ")
add_bullet("Pemberlakuan velocity ceiling (batas frekuensi dan akumulasi nominal) selama 30 hari pertama bagi merchant QRIS baru, serta penonaktifan instant disbursement ke akun personal.", "3. Pengetatan KYM & Velocity: ")
add_bullet("Forum taktis berkala Ditreskrimsus, PPATK, BI Sulsel, OJK Reg 6, dan Compliance PJP untuk threat intelligence sharing.", "4. Gugus Tugas Regional Sulsel: ")

# SLIDE 11
add_heading_2("Slide 11 — Peta Jalan Implementasi Taktis (Target 90 Hari)")
add_p("Tujuan: Mengikat forum ke dalam komitmen jadwal yang terukur.")
add_bullet("Penyusunan draf SOP Protokol Darurat & registrasi Single Point of Contact (SPoC) terenkripsi.", "Bulan I (Hari 1–30): ")
add_bullet("Uji coba simulasi penahanan saldo 2 jam & integrasi format bukti log forensik SHA-256.", "Bulan II (Hari 31–60): ")
add_bullet("Kick-off Gugus Tugas Regional, penerapan velocity ceiling merchant, dan evaluasi pemadanan NIK.", "Bulan III (Hari 61–90): ")

# SLIDE 12
add_heading_2("Slide 12 — Prinsip Penutup & Sesi Diskusi")
add_p("Tujuan: Menutup dengan pernyataan pamungkas berdaya ingat tinggi dan membuka forum tanya jawab.")
add_callout(
    "Kejahatan keuangan digital bergerak dengan kecepatan algoritma. "
    "Maka pertahanan dan penegakan hukum tidak boleh tertahan oleh kelambanan birokrasi. "
    "Polda Sulawesi Selatan siap bekerja sama 24 jam sehari, 7 hari seminggu. "
    "Kuncinya hanya dua: KECEPATAN eksekusi darurat dan INTEGRITAS pembuktian digital. "
    "Terima kasih, mari kita buka sesi diskusi.",
    "KALIMAT PENUTUP DIRRESKRIMSUS"
)

# ==================== PANDUAN TANYA JAWAB ====================
add_heading_1("3. ANTISIPASI PERTANYAAN KRITIS PESERTA (Q&A HANDLING)")

qas = [
    ("Pertanyaan Legal OVO: 'Bagaimana risiko hukum PJP jika menahan saldo dalam 2 jam sebelum ada penetapan pengadilan, lalu nasabah menggugat perdata?'",
     "Jawaban Taktis: Rujuk langsung KUHAP UU 20/2025 Pasal 140 ayat (7), (8), dan (9). Pasal ini secara khusus diciptakan pembuat undang-undang untuk mengatasi kebuntuan tersebut. Syaratnya terpenuhi: dugaan tindak pidana ITE dan adanya potensi larinya aset kekayaan. Penyidik menerbitkan Surat Perintah Penyidikan dan Surat Permintaan Pemblokiran Darurat. PJP bertindak atas perintah undang-undang (Pasal 51 KUHP: tidak dipidana orang yang melakukan perbuatan untuk melaksanakan perintah jabatan yang sah). Selain itu, jika penetapan hakim ditolak, undang-undang memberi waktu 3 hari kerja untuk mencabut blokir secara terhormat."),
    
    ("Pertanyaan Engineering/AML: 'Pola botnet Makassar menyamar menggunakan IP lokal dan device spoofing. Bagaimana cara mendeteksinya di sisi server PJP?'",
     "Jawaban Taktis: Jangan hanya mengandalkan IP Address dan IMEI. Terapkan client attestation biner (seperti Play Integrity API) untuk mendeteksi apakah aplikasi berjalan di emulator atau native OS. Analisis canvas fingerprint dan perilaku interaksi sentuhan layar (touch-event cadence). Bot memiliki interval klik yang konsisten secara matematis (kurang dari 100ms per input), sedangkan sentuhan jari manusia memiliki variabilitas tekanan dan jeda mikro."),
     
    ("Pertanyaan Compliance: 'Banyak merchant QRIS didaftarkan lewat agregator pihak ketiga. Apakah PJP bertanggung jawab jika agregator meloloskan merchant fiktif?'",
     "Jawaban Taktis: Berdasarkan POJK 8/2023 Pasal 19 dan PBI 23/6/PBI/2021, PJP penyelenggara penatausahaan rekening tetap memikul tanggung jawab akhir atas due diligence (CDD/EDD) pihak ketiga (relying on third parties). PJP wajib melakukan audit kepatuhan berkala dan menetapkan penalti pencabutan izin integrasi API bagi agregator yang memproduksi merchant bodong.")
]

for q, a in qas:
    p_q = doc.add_paragraph()
    p_q.paragraph_format.space_before = Pt(6)
    p_q.paragraph_format.space_after = Pt(2)
    r_q = p_q.add_run("Q: " + q)
    r_q.font.name = "Tahoma"
    r_q.font.size = Pt(10.5)
    r_q.font.bold = True
    r_q.font.color.rgb = RED_RGB
    
    p_a = doc.add_paragraph()
    p_a.paragraph_format.space_after = Pt(6)
    r_a = p_a.add_run("A: " + a)
    r_a.font.name = "Tahoma"
    r_a.font.size = Pt(10.5)
    r_a.font.color.rgb = DARK_RGB

out_docx = "/home/ubuntu/penyidikan/analisis/workshop-ovo-2026/Naskah_Panduan_Bicara_Dirreskrimsus_Polda_Sulsel_Workshop_OVO.docx"
doc.save(out_docx)
print("SUCCESS_SAVED_DOCX:", out_docx)
