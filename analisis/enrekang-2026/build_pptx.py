#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Buat 04-MATERI-SOSIALISASI-SATGAS-PASTI.pptx — 14 slide sosialisasi koperasi."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

OUT = "/home/ubuntu/penyidikan/analisis/enrekang-2026/04-MATERI-SOSIALISASI-SATGAS-PASTI.pptx"

NAVY = RGBColor(0x1F, 0x4E, 0x79)
RED = RGBColor(0xC0, 0x39, 0x2B)
GREEN = RGBColor(0x1E, 0x8E, 0x3E)
DARK = RGBColor(0x33, 0x33, 0x33)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GOLD = RGBColor(0xF3, 0x9C, 0x12)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

def add_slide(title_text=None, subtitle=None, bg=WHITE, title_color=NAVY):
    s = prs.slides.add_slide(BLANK)
    # background
    from pptx.oxml.ns import qn
    solid = s.background.fill
    solid.solid()
    solid.fore_color.rgb = bg
    if title_text:
        tb = s.shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(12.1), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        r = p.add_run(); r.text = title_text
        r.font.size = Pt(32); r.font.bold = True; r.font.color.rgb = title_color
        if subtitle:
            p2 = tf.add_paragraph()
            r2 = p2.add_run(); r2.text = subtitle
            r2.font.size = Pt(14); r2.font.color.rgb = RGBColor(0x77, 0x77, 0x77); r2.italic = True
    return s

def add_bullets(slide, items, top=1.6, left=0.7, width=12.0, height=5.2, size=18, color=DARK):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    first = True
    for it in items:
        if isinstance(it, tuple):
            text, lvl = it
        else:
            text, lvl = it, 0
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.text = ""
        bullet = "•  " if lvl == 0 else "–  "
        r = p.add_run(); r.text = bullet + text
        r.font.size = Pt(size if lvl == 0 else size - 2)
        r.font.color.rgb = color if lvl == 0 else RGBColor(0x55, 0x55, 0x55)
        p.space_after = Pt(6)
    return tb

def add_footer(slide, text="Satgas PASTI — Polda Sulsel · Sosialisasi Koperasi Sehat vs Ilegal · Enrekang, 8 September 2026"):
    tb = slide.shapes.add_textbox(Inches(0.6), Inches(7.0), Inches(12.1), Inches(0.4))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = text
    r.font.size = Pt(10); r.font.color.rgb = RGBColor(0x99, 0x99, 0x99)

def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text

# 1 — Judul
s = add_slide(bg=NAVY)
tb = s.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.3), Inches(3.5))
tf = tb.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; r = p.add_run(); r.text = "KOPERASI SEHAT vs KOPERASI ILEGAL"
r.font.size = Pt(44); r.font.bold = True; r.font.color.rgb = WHITE
p.alignment = PP_ALIGN.CENTER
p2 = tf.add_paragraph(); r2 = p2.add_run()
r2.text = "Sosialisasi & pemeriksaan kelengkapan koperasi\nSatgas PASTI (Satuan Tugas Pemberantasan Aktivitas Keuangan Ilegal)\nKab. Enrekang — 8 September 2026"
r2.font.size = Pt(20); r2.font.color.rgb = GOLD
p2.alignment = PP_ALIGN.CENTER
p3 = tf.add_paragraph(); r3 = p3.add_run()
r3.text = "Kepolisian Daerah Sulawesi Selatan"
r3.font.size = Pt(16); r3.font.color.rgb = WHITE
p3.alignment = PP_ALIGN.CENTER
notes(s, "Sapa hadirin: pengurus & anggota koperasi, perangkat desa/kelurahan. Perkenalan singkat Satgas PASTI. Tekankan: kehadiran kami untuk melindungi, membantu koperasi agar sehat & tidak disalahgunakan.")

# 2 — Apa itu koperasi
s = add_slide("Apa itu Koperasi?", "UU No. 25 Tahun 1992 tentang Perkoperasian")
add_bullets(s, [
    "Koperasi = badan usaha milik BERSAMA para anggotanya, berdasar asas kekeluargaan",
    "Tujuan: mensejahterakan anggota, bukan mencari untung sebesar-besarnya",
    "Keuntungan koperasi disebut SISA HASIL USAHA (SHU) — dibagi ke anggota sesuai jasanya",
    "Yang punya koperasi: ANGGOTA. Keputusan lewat Rapat Anggota Tahunan (RAT)",
    "Koperasi dibentuk dengan AKTA NOTARIS dan disahkan badan hukum oleh pemerintah (Kemenkumham/Dinas Koperasi)",
])
notes(s, "Jelaskan beda koperasi vs PT/CV vs bank. Koperasi itu milik anggota. Kata kunci: RAT, SHU, badan hukum.")

# 3 — Koperasi yang boleh simpan pinjam
s = add_slide("Simpan Pinjam di Koperasi: ADA ATURANNYA", "Siapa yang boleh dilayani = penentu sah/tidaknya")
add_bullets(s, [
    ("Aturan utama: koperasi hanya boleh menghimpun simpanan & memberi pinjaman kepada ANGGOTANYA", 0),
    ("Izin yang wajib ada:", 0),
    ("Koperasi Simpan Pinjam (KSP) / USP: izin usaha simpan pinjam dari Kemenkop/Dinas Koperasi", 1),
    ("Koperasi yang layani NON-ANGGOTA (masyarakat umum): wajib izin dari OJK", 1),
    ("Yang penting dicatat: BADAN HUKUM ≠ IZIN USAHA SIMPAN PINJAM", 0),
    ("Ada SK badan hukum saja belum cukup untuk menjalankan usaha simpan pinjam", 1),
])
notes(s, "Ini pesan inti. Analogikan: punya KTP (badan hukum) tidak otomatis boleh buka bank. Koperasi yang terima tabungan dari orang luar = sudah keluar dari aturan koperasi.")

# 4 — Ciri koperasi SEHAT
s = add_slide("Ciri Koperasi SEHAT", "Ini yang kami harapkan ada di setiap koperasi")
add_bullets(s, [
    "✔ Punya badan hukum sah (SK pengesahan) & terdaftar di sistem ODS Kemenkop",
    "✔ Punya izin usaha simpan pinjam (kalau menjalankan simpan pinjam)",
    "✔ Melayani ANGGOTA saja — setiap calon anggota lewat prosedur resmi (simpanan pokok, RAT)",
    "✔ Mengadakan RAT setiap tahun & laporan keuangan bisa diperiksa",
    "✔ Bunga wajar: simpanan maks. 9%/tahun, pinjaman maks. 24%/tahun",
    "✔ Dana dikelola transparan, tercatat, dan dipertanggungjawabkan",
], color=GREEN)
notes(s, "Berikan apresiasi kepada koperasi yang sudah sehat. Sebutkan bahwa pemeriksaan hari ini adalah pembinaan, bukan mencari-cari kesalahan.")

# 5 — Ciri koperasi BERMASALAH / ILEGAL
s = add_slide("Ciri Koperasi BERMASALAH / ILEGAL", "Waspadai 7 tanda ini")
add_bullets(s, [
    "1. Terima tabungan / simpanan dari MASYARAKAT UMUM (bukan anggota)",
    "2. Janji bunga / bagi hasil TIDAK WAJAR (mis. 5-10% per bulan) — mustahil dari usaha riil",
    "3. Badan hukum / izin tidak jelas — tidak ada di ODS Kemenkop atau OJK",
    "4. Kegiatan TIDAK SESUAI izin (punya izin toko, jalannya bank)",
    "5. Rekrut anggota model 'member get member' / arisan berantai / janji nilai besar di akhir",
    "6. Pengurus tidak bisa menunjukkan RAT, laporan keuangan, atau SK badan hukum",
    "7. Aplikasi bisa transfer/pinjam online padahal tidak terdaftar di OJK",
], color=RED)
notes(s, "Baca perlahan satu per satu, beri contoh nyata dari daerah (KOSIPA Sulselbar, KSP gagal bayar nasional). Tekankan tanda #1 dan #2 paling sering dipakai menipu.")

# 6 — Bahaya koperasi ilegal (kasus nyata)
s = add_slide("Kenapa Ini Berbahaya? (Kasus Nyata)", "Yang sudah terjadi di sekitar kita")
add_bullets(s, [
    "KSP besar gagal bayar (Indosurya, Sejahtera Bersama, Pracico, Intidana): ratusan ribu korban, kerugian triliunan rupiah",
    "KOSIPA Sulselbar (2025): diduga 30 tahun tanpa badan hukum sah, menghimpun dana dari ±100 koperasi",
    "Koperasi Merah Putih di daerah: koperasi baru yang sah — rawan disalahgunakan orang yang bukan pengurus asli",
    "Ciri korban: masyarakat menitipkan uang karena percaya tokoh/iming-iming, lalu uangnya tidak kembali",
    "Yang menanggung risiko: BAPAK/IBU sendiri — uang simpanan di koperasi TIDAK dijamin LPS seperti bank",
])
notes(s, "Gunakan kasus lokal: KOSIPA sudah dilaporkan ke Polda Sulsel. Koperasi Merah Putih adalah program pemerintah — sah, tapi pastikan pengurusnya benar.")

# 7 — Cara cek legalitas (praktis dari HP)
s = add_slide("Cara Cek: Koperasi Ini Sah atau Tidak?", "Bisa dicek sendiri dari HP")
add_bullets(s, [
    "1. Cek badan hukum koperasi: buka nik.kop.go.id (ODS Kemenkop) → masukkan nama/NIK koperasi",
    "2. Cek koperasi/layanan keuangan berizin: www.ojk.go.id → direktori LJK / fintech",
    "3. Cek daftar yang DIBLOKIR Satgas PASTI: laman info terkini OJK",
    "4. Tanya Dinas Koperasi & UKM Kab. Enrekang (pembina koperasi di daerah)",
    "5. Kalau ragu: hubungi OJK 157 (bebas pulsa) atau Satgas PASTI (WA 0811-571-571)",
    "Ingat: terdaftar = sah (sampai terbukti sebaliknya). Yang TIDAK terdaftar = patut diwaspadai",
])
notes(s, "Demo langsung kalau ada sinyal. Tekankan: jangan hanya percaya brosur/plakat — cek sendiri di sistem resmi.")

# 8 — Uang di koperasi vs bank
s = add_slide("Penting: Koperasi BUKAN Bank", "Jangan tertukar!")
add_bullets(s, [
    "Bank: lembaga keuangan berizin OJK, simpanannya DIJAMIN LPS (maks. Rp 2 miliar per nasabah)",
    "Koperasi: milik anggota, simpanan TIDAK dijamin LPS — risikonya ditanggung anggota",
    "Kalau ada 'koperasi' yang berperilaku seperti bank (terima tabungan umum, kasih bunga tetap, punya ATM/aplikasi transfer) tapi tidak berizin bank/OJK → itu modus 'bank gelap'",
    "Istilah yang menipu: 'simpanan berjangka', 'deposito koperasi', 'jaminan 100% aman'",
])
notes(s, "Tegaskan perbedaan mendasar. Banyak korban mengira uangnya 'seaman bank'.")

# 9 — Konsekuensi hukum (bahasa sederhana)
s = add_slide("Ada Konsekuensi Hukumnya", "Bagi pengurus/pihak yang melanggar")
add_bullets(s, [
    "Menghimpun dana masyarakat tanpa izin (bank gelap) → pidana penjara hingga 15 tahun",
    "Koperasi layani non-anggota tanpa izin OJK → wajib izin OJK; melanggar = pelanggaran serius",
    "Menipu dengan janji bunga/arisan (investasi bodong) → pidana penjara",
    "Memalsukan SK/akta/laporan koperasi → pidana pemalsuan surat",
    "Bunga di atas batas (simpanan >9%, pinjaman >24%) → pelanggaran aturan Kemenkop (ditegur/dibina dulu)",
    "Kami hadir untuk MENCEGAH — bukan sekadar menghukum. Koperasi sehat dilindungi, yang nakal ditindak",
])
notes(s, "Sampaikan dengan bijak: hukum berat untuk penipu, bukan untuk koperasi kecil yang kurang administrasi. Koperasi yang kurang tertib akan DIBINA, bukan langsung dipidana.")

# 10 — Peran Satgas PASTI
s = add_slide("Apa itu Satgas PASTI?", "Sinergi 12+ kementerian/lembaga")
add_bullets(s, [
    "Satgas PASTI = Satuan Tugas Pemberantasan Aktivitas Keuangan Ilegal (sebelumnya Satgas Waspada Investasi)",
    "Anggota: OJK, Polri, Kejaksaan, BI, PPATK, Kemenkop, Kominfo, Kemendagri, dll.",
    "Sejak 2017 s.d. 2025: 14.000+ entitas keuangan ilegal dihentikan (investasi ilegal, pinjol ilegal, gadai ilegal)",
    "Tugas di daerah: patroli, sosialisasi, dan menghentikan entitas yang merugikan masyarakat",
    "Kami (Polri) hadir di Enrekang dalam rangka tugas Satgas PASTI — sosialisasi & pemeriksaan kelengkapan",
])
notes(s, "Perkenalkan siapa tim di ruangan. Jelaskan dasar kehadiran: tugas satgas, bukan operasi represif.")

# 11 — Yang kami periksa hari ini
s = add_slide("Yang Kami Periksa Hari Ini", "Pemeriksaan kelengkapan — transparan & untuk kebaikan bersama")
add_bullets(s, [
    "1. SK badan hukum & akta (legalitas)",
    "2. Izin usaha simpan pinjam / izin OJK (kalau ada)",
    "3. Identitas pengurus (KTP/NIK)",
    "4. Buku anggota & RAT",
    "5. Laporan keuangan & produk (bunga)",
    "Hasilnya: kalau lengkap → apresiasi. Kalau kurang → kami bantu arahkan ke Dinas Koperasi. Kalau ada indikasi pidana → ditindaklanjuti sesuai hukum.",
])
notes(s, "Jelaskan alur pemeriksaan dengan checklist. Suasana harus bersahabat: ini pembinaan + perlindungan masyarakat.")

# 12 — Yang bisa dilakukan masyarakat
s = add_slide("Apa yang Bisa Bapak/Ibu Lakukan?", "Lindungi diri & keluarga")
add_bullets(s, [
    "Sebelum menabung/menitipkan uang: CEK dulu (nik.kop.go.id / OJK 157 / Dinas Koperasi)",
    "Waspada janji bunga tinggi — tidak ada usaha legal yang kasih 5-10%/bulan tanpa risiko",
    "Jangan tergiur 'member get member' / arisan berantai / undian berhadiah",
    "Simpan bukti setoran & dokumen — kalau ada masalah, bukti itu penting",
    "Lapor kalau curiga: Satgas PASTI (satgaspasti@ojk.go.id / WA 0811-571-571), OJK 157, atau kantor polisi terdekat",
])
notes(s, "Ajak interaksi: tanya pengalaman warga. Bagikan nomor kontak. Tekankan: malu bertanya sesat di jalan.")

# 13 — Kontak & layanan pengaduan
s = add_slide("Kontak & Layanan Pengaduan", "Simpan nomor ini")
kontak = [
    ("OJK", "157 (bebas pulsa) · konsumen@ojk.go.id"),
    ("Satgas PASTI", "WA 0811-571-571 · satgaspasti@ojk.go.id · IG @satgas_pasti"),
    ("Dinas Koperasi Kab. Enrekang", "Kantor Dinas Koperasi, UKM, Tenaga Kerja & Transmigrasi"),
    ("Kepolisian", "Kantor Polisi terdekat / Polres Enrekang · 110"),
]
y = 1.8
for nama, kontak_txt in kontak:
    tb = s.shapes.add_textbox(Inches(1.0), Inches(y), Inches(11.3), Inches(0.9))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = nama
    r.font.bold = True; r.font.size = Pt(20); r.font.color.rgb = NAVY
    p2 = tf.add_paragraph()
    r2 = p2.add_run(); r2.text = kontak_txt
    r2.font.size = Pt(16); r2.font.color.rgb = DARK
    y += 1.15
notes(s, "Pastikan kontak Dinas Koperasi Enrekang sesuai kondisi terkini saat kunjungan (koordinasi awal dengan dinas).")

# 14 — Penutup
s = add_slide(bg=NAVY)
tb = s.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.3), Inches(3.0))
tf = tb.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = "Koperasi Sehat = Masyarakat Sejahtera"
r.font.size = Pt(40); r.font.bold = True; r.font.color.rgb = WHITE
p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER
r2 = p2.add_run(); r2.text = "Mari bersama menjaga koperasi di Kab. Enrekang tetap sehat, jujur, dan bermanfaat bagi anggota.\n\nTerima kasih — silakan bertanya!"
r2.font.size = Pt(20); r2.font.color.rgb = GOLD
notes(s, "Sesi tanya jawab. Bagikan lembar kontak & checklist mandiri kalau tersedia. Tutup dengan doa/ucapan terima kasih.")

prs.save(OUT)
print("OK — slides:", len(prs.slides.__iter__.__self__._sldIdLst))
