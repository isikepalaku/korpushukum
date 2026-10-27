#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Buat 03-CHECKLIST-KELENGKAPAN-KOPERASI.docx — tabel isian lapangan."""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

OUT = "/home/ubuntu/penyidikan/analisis/enrekang-2026/03-CHECKLIST-KELENGKAPAN-KOPERASI.docx"

doc = Document()

# Margin
for s in doc.sections:
    s.left_margin = Cm(1.5)
    s.right_margin = Cm(1.5)
    s.top_margin = Cm(1.5)
    s.bottom_margin = Cm(1.5)

style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(10)

# Judul
t = doc.add_paragraph()
t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run("CHECKLIST KELENGKAPAN KOPERASI — KUNJUNGAN SATGAS PASTI\nKab. Enrekang, 8 September 2026")
r.bold = True
r.font.size = Pt(14)
r.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)

sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
rs = sub.add_run("Pemeriksaan kelengkapan administrasi & legalitas — verifikasi dulu, jangan langsung vonis. Terdaftar = presumsi sah.")
rs.italic = True
rs.font.size = Pt(9)

# Identitas koperasi
doc.add_heading("A. Identitas Koperasi", level=2)
ident = doc.add_table(rows=8, cols=2)
ident.style = "Table Grid"
ident.alignment = WD_TABLE_ALIGNMENT.CENTER
ident_rows = [
    ("Nama koperasi", ""), ("Alamat kantor", ""), ("Nama ketua pengurus", ""),
    ("No. HP pengurus", ""), ("Jenis koperasi (KSP/KSPPS/USP/sektor riil)", ""),
    ("No. SK Badan Hukum & tanggal", ""), ("NIK Koperasi (ODS Kemenkop)", ""),
    ("Kegiatan usaha utama (dari AD/ART)", ""),
]
for i, (k, v) in enumerate(ident_rows):
    ident.cell(i, 0).text = k
    ident.cell(i, 1).text = v
    for cell in (ident.cell(i, 0), ident.cell(i, 1)):
        for p in cell.paragraphs:
            p.paragraph_format.space_after = Pt(2)
for i in range(8):
    ident.cell(i, 0).width = Cm(6)
    ident.cell(i, 1).width = Cm(11.5)
    for p in ident.cell(i, 0).paragraphs:
        for run in p.runs:
            run.bold = True

# Tabel checklist
doc.add_heading("B. Checklist Kelengkapan", level=2)

def add_checklist(title, items):
    doc.add_heading(title, level=3)
    tbl = doc.add_table(rows=len(items) + 1, cols=5)
    tbl.style = "Table Grid"
    hdr = tbl.rows[0].cells
    for c, h in enumerate(["No", "Item yang diperiksa", "Dasar hukum", "Ada/Tidak", "Catatan & nomor bukti (foto?)"]):
        hdr[c].text = h
        for p in hdr[c].paragraphs:
            for run in p.runs:
                run.bold = True
    for i, item in enumerate(items, 1):
        row = tbl.rows[i].cells
        row[0].text = str(i)
        row[1].text = item[0]
        row[2].text = item[1]
        row[3].text = ""
        row[4].text = ""
    widths = [Cm(0.8), Cm(7.2), Cm(4.0), Cm(1.8), Cm(3.7)]
    for row in tbl.rows:
        for c, w in enumerate(widths):
            row.cells[c].width = w
    return tbl

add_checklist("B1. Legalitas Badan Hukum", [
    ("Akta pendirian koperasi (notaris)", "UU 25/1992; PP 7/2021"),
    ("SK pengesahan badan hukum (Kemenkumham/AHU/Dinas Koperasi)", "UU 25/1992 Ps. 9-12; PP 7/2021"),
    ("Perubahan AD/ART terakhir + SK pengesahannya", "UU 25/1992"),
    ("Kesesuaian nama di papan nama/kantor dengan SK badan hukum", "UU 25/1992"),
    ("Terdaftar di ODS Kemenkop (nik.kop.go.id) — catat NIK & status sertifikat", "Verifikasi registri"),
])

add_checklist("B2. Identitas & Kewenangan Pengurus/Pengawas", [
    ("KTP & NIK ketua/sekretaris/bendahara (verifikasi dukcapil)", "UU 25/1992; Permenkop 8/2023"),
    ("SK pengangkatan pengurus & masa jabatan", "UU 25/1992 Ps. 29-33"),
    ("Pengurus bukan terpidana tindak pidana keuangan", "Permenkop 8/2023 (larangan)"),
    ("Rekening atas nama koperasi (bukan pribadi)", "UU 25/1992"),
    ("Pengendali riil (beneficial owner) — siapa yang memutuskan", "Catatan lidik"),
])

add_checklist("B3. Izin Usaha (kunci penentu rezim)", [
    ("Izin Usaha Simpan Pinjam (Kemenkop/Dinas Koperasi) — utk KSP/KSPPS/USP/USPPS closed-loop", "Permenkop 8/2023"),
    ("Izin usaha LJK dari OJK — bila open-loop (layani non-anggota)", "Ps. 44B UU 25/1992 jo P2SK; POJK 47/2024"),
    ("Terdaftar/berizin di direktori OJK (LJK/pergadaian/ITSK) bila relevan", "Direktori OJK"),
    ("NPWP koperasi & NIB (OSS) — konfirmasi ke OSS/DJP bila data kosong", "PP 7/2021"),
    ("Kegiatan riil sesuai izin usaha (bukan kegiatan lain)", "UU 25/1992; POJK 47/2024"),
])

add_checklist("B4. Keanggotaan & Uji Non-Anggota", [
    ("Buku daftar anggota & jumlah anggota", "UU 25/1992 Ps. 44; Permenkop 8/2023"),
    ("Simpanan pokok & wajib anggota (ada bukti setoran)", "UU 25/1992"),
    ("UJI PEMBELI: non-anggota mencoba menabung — berhasil/tidak?", "Uji lapangan"),
    ("UJI PEMINJAM: non-anggota mencoba meminjam — berhasil/tidak?", "Uji lapangan"),
    ("Syarat jadi anggota (formulir, simpanan pokok) — formalitas atau riil?", "UU 25/1992 Ps. 18-22"),
])

add_checklist("B5. Kesehatan Usaha & Laporan", [
    ("Rapat Anggota Tahunan 2 tahun terakhir (berita acara)", "UU 25/1992 Ps. 23-27"),
    ("Laporan keuangan (neraca, laba-rugi, SHU) audited/tidak", "Permenkop 2/2024 (akuntansi koperasi)"),
    ("SHU dibagikan sesuai keputusan RAT", "UU 25/1992 Ps. 45"),
    ("Kesehatan koperasi (peringkat) — catat", "Penilaian Kemenkop"),
    ("Laporan keuangan konsisten dgn mutasi rekening bank", "Catatan lidik"),
])

add_checklist("B6. Produk, Bunga & Metode Tagih", [
    ("Jenis produk simpanan/pinjaman (brosur/skema)", "Permenkop 8/2023"),
    ("Bunga simpanan ≤ 9%/thn; pinjaman ≤ 24%/thn", "Permenkop 8/2023"),
    ("Janji bagi hasil/bunga tidak wajar (indikasi ponzi)", "Referensi Satgas PASTI"),
    ("Metode penagihan (ada debt collector/ancaman?)", "KUHP 482/483; UU ITE; POJK 22/2023"),
    ("Aplikasi digital: fitur transfer/bayar tagihan/e-KYC?", "Ps. 213/218/304 P2SK; POJK 3/2024"),
])

add_checklist("B7. Kepatuhan Lain & Status", [
    ("Papan nama & alamat sesuai domisili", "UU 25/1992"),
    ("Anggota aktif vs total (banyak anggota pasif?)", "Catatan lidik"),
    ("Status di Satgas PASTI/alert OJK (cek daftar)", "ojk.go.id"),
    ("Kaitan dgn koperasi payung/KOSIPA/KDMP Merah Putih (sebutkan)", "Konteks daerah"),
    ("Keluhan masyarakat/anggota (catat narasi)", "Catatan lidik"),
])

doc.add_heading("C. Hasil & Tindak Lanjut", level=2)
hasil = doc.add_table(rows=5, cols=2)
hasil.style = "Table Grid"
hasil_rows = [
    ("Kesimpulan verifikasi (terdaftar sah / indikasi masalah administratif / indikasi pidana)", ""),
    ("Temuan yang menjadi bahan edukasi sosialisasi", ""),
    ("Temuan yang dieskalasi ke penyidik (SP Lidik/koordinasi OJK-Dinas)", ""),
    ("Dokumentasi (jumlah foto/arsip yang diamankan)", ""),
    ("Nama petugas pemeriksa & tanggal", ""),
]
for i, (k, v) in enumerate(hasil_rows):
    hasil.cell(i, 0).text = k
    hasil.cell(i, 1).text = v
    for cell in (hasil.cell(i, 0), hasil.cell(i, 1)):
        for p in cell.paragraphs:
            p.paragraph_format.space_after = Pt(2)
for i in range(5):
    hasil.cell(i, 0).width = Cm(7)
    hasil.cell(i, 1).width = Cm(10.5)
    for p in hasil.cell(i, 0).paragraphs:
        for run in p.runs:
            run.bold = True

foot = doc.add_paragraph()
foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
rf = foot.add_run("Dokumen kerja Satgas PASTI — Fismondev Polda Sulsel. Verifikasi registri resmi sebelum menarik kesimpulan.")
rf.italic = True
rf.font.size = Pt(8)

doc.save(OUT)
print("OK — tables:", len(doc.tables))
