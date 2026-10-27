#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Buat 02-MATRIKS-CELAH-PIDANA.xlsx — matriks celah pidana koperasi utk kunjungan Enrekang."""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

OUT = "/home/ubuntu/penyidikan/analisis/enrekang-2026/02-MATRIKS-CELAH-PIDANA.xlsx"

HEADERS = ["No", "Modus/Temuan Lapangan", "Indikator (gejala terlihat di lapangan)",
           "Kualifikasi", "Pasal (lex specialis)", "Unsur yang harus dibuktikan",
           "Alat bukti yang dikumpulkan saat kunjungan", "Tindak lanjut (SOP)", "Risiko lemah"]

ROWS = [
    # 1
    ["Bank gelap — menghimpun simpanan/dana masyarakat tanpa izin usaha bank (rezim perbankan)",
     "Koperasi/\"lembaga\" menerima simpanan dari NON-anggota (masyarakat umum); memakai istilah tabungan/deposito/simpanan berjangka; janji bunga rutin; ada buku tabungan/sertifikat; kantor melayani publik seperti bank",
     "Pidana (lex specialis: UU Perbankan)",
     "Ps. 46 UU 7/1992 jo 10/1998 (diubah P2SK); pasca UU 1/2026: penjara maks 15 thn dan/atau denda kat. VII",
     "(1) menghimpun dana dari masyarakat; (2) dalam bentuk simpanan; (3) tanpa izin usaha bank dari OJK. Subjek: pengurus/pemberi perintah (klausul korporasi Ps. 46(2))",
     "Formulir/brosur produk simpanan; contoh buku tabungan/sertifikat; kwitansi setoran atas nama non-anggota; rekening koran; daftar penyimpan non-anggota; foto papan nama; hasil uji pembeli (non-anggota bisa setor)",
     "Eskalasi lidik formal → koordinasi OJK → SP Lidik; amankan dokumen via prosedur KUHAP (UU 20/2025)",
     "Kuat — pasal tegas; kelemahan hanya jika entitas terbukti berizin OJK/bank"],
    # 2
    ["Koperasi open-loop tanpa izin OJK — menghimpun dana dari / menyalurkan pinjaman ke pihak selain anggota",
     "Non-anggota bisa menabung/meminjam; keanggotaan formalitas (isi formulir langsung jadi); himpun dana dari koperasi lain; terima pendanaan bank/LJK di atas batas; layanan jasa keuangan di luar simpan pinjam",
     "Pidana/administratif bergantung modus",
     "Ps. 44B UU 25/1992 (disisipkan Pasal 202 UU P2SK) jo POJK 47/2024 — wajib izin LJK OJK; himpun dana → jerat Ps. 46 UU Perbankan",
     "Koperasi memenuhi kriteria open-loop Ps. 44B(2): (a) himpun dana dari non-anggota; (b) dari anggota koperasi lain; (c) salurkan pinjaman ke non-anggota/koperasi lain; (d) pendanaan bank/LJK di atas batas; (e) layanan jasa keuangan lain; tanpa izin OJK",
     "Daftar anggota vs daftar penyimpan/peminjam (bandingkan); formulir pendaftaran anggota; bukti transaksi non-anggota; laporan keuangan; izin usaha SP Kemenkop (kalau ada) vs kegiatan riil",
     "Verifikasi ODS Kemenkop + direktori LJK OJK; koordinasi OJK; kalau himpun dana publik → arah Ps. 46 UU Perbankan",
     "Sedang — perlu bukti kuat siapa yang dilayani (uji pembeli + dokumen)"],
    # 3
    ["KSP closed-loop tanpa izin usaha simpan pinjam (Kemenkop)",
     "Koperasi berbadan hukum (SK AHU/Dinas) tapi TIDAK punya izin usaha SP dari Kemenkop/Dinas Koperasi; tetap jalankan simpan pinjam ke anggota",
     "Administratif Kemenkop (utama); pidana bila himpun dana luas",
     "Permenkop 8/2023 (wajib izin usaha SP; modal awal 500jt–2M; bunga simpanan ≤9%/thn, pinjaman ≤24%/thn)",
     "Unsur administratif: menjalankan usaha SP tanpa izin usaha SP. Bukan langsung pidana — ranah pengawasan Kemenkop",
     "Salinan izin usaha SP; SK badan hukum; realisasi kegiatan",
     "Catat temuan administratif; koordinasikan dengan Dinas Koperasi Enrekang (pembinaan/pengawasan); bukan bahan pidana langsung",
     "Lemah sbg pidana — ranah Kemenkop; jangan overcharge"],
    # 4
    ["Koperasi fiktif / badan hukum tidak sah (SK palsu / tanpa pengesahan)",
     "Tidak ditemukan di ODS Kemenkop; SK badan hukum nomor tidak cocok/tidak ada; papan nama beda dengan badan hukum; alamat tidak ditemukan; pengurus memakai identitas fiktif",
     "Pidana umum (subsider)",
     "KUHP 2023: Ps. 391–392 pemalsuan surat (6/8 thn); Ps. 492 penipuan (4 thn) bila menghimpun dana dengan tipu muslihat; gabung Ps. 46 UU Perbankan bila himpun dana",
     "Pemalsuan: membuat/memakai surat (SK/akte) palsu seolah sah & menimbulkan kerugian. Penipuan: maksud menguntungkan diri melawan hukum, nama/kedudukan palsu, tipu muslihat, menggerakkan orang menyerahkan barang/uang",
     "SK badan hukum (foto); hasil cek ODS Kemenkop; akta notaris; KTP pengurus; kwitansi; keterangan saksi anggota",
     "Verifikasi ODS dulu (jangan vonis — kasus SK \"palsu\" sering salah baca); kalau terbukti fiktif → lidik pemalsuan + penipuan",
     "Sedang — kesalahan baca nomor SK pernah menggugurkan dugaan (Pinrang Abadi)"],
    # 5
    ["Arisan online / arisan berantai berkedok koperasi",
     "Rekrut via WA/Telegram; iuran periodik; janji nilai besar di akhir; member get member; tanpa usaha riil; admin di luar pengurus koperasi",
     "Pidana (umum + ITE)",
     "KUHP 2023 Ps. 492 (penipuan); UU ITE (bila via elektronik); UU P2SK bila himpun dana tanpa izin; TPPU Ps. 3–5 bila aliran dana masif",
     "Skema ponzi: keuntungan dari dana anggota baru, bukan usaha riil; janji hasil tetap/fantastis; rekrutmen berjenjang",
     "Grup WA/Telegram (screenshot dgn hash/chain of custody); bukti transfer; tangkapan layar janji hasil; keterangan peserta",
     "Lidik penipuan; koordinasi Kominfo utk blokir konten; Satgas PASTI utk daftar ilegal",
     "Sedang — perlu bedakan arisan dgn usaha riil & tanpa janji bunga tetap"],
    # 6
    ["Investasi bodong / ponzi berkedok \"simpanan anggota\" atau \"modal usaha koperasi\"",
     "Janji bagi hasil/bunga tidak wajar (1–5%/bulan); klaim tanpa risiko; memakai tokoh masyarakat/agama; legalitas tidak jelas; kegiatan tidak sesuai izin",
     "Pidana",
     "KUHP 2023 Ps. 492 (penipuan) — 4 thn; Ps. 90 UU Pasar Modal bila pola efek; UU P2SK bila himpun dana tanpa izin; TPPU",
     "Unsur penipuan; skala korban & dana utk TPPU",
     "Materi promosi; kalkulasi janji bagi hasil; daftar korban; aliran dana; izin vs kegiatan riil",
     "Lidik + PPATK (follow the money); koordinasi Satgas PASTI",
     "Sedang — bedakan dengan usaha riil berisiko vs skema ponzi"],
    # 7
    ["Koperasi/praktik gadai ilegal (terima gadai barang sebagai mata pencaharian)",
     "Terima gadai (emas/HP/kendaraan) tanpa izin usaha pergadaian; toko emas/konter terima gadai rutin; koperasi buka unit gadai",
     "Pidana (skala kecil) / P2SK (skala besar)",
     "Ps. 273 KUHP (gadai tanpa izin sbg mata pencaharian — penjara maks 1 thn/denda kat. III); skala besar (outlet, omzet besar, himpun dana): Ps. 237 jo 305 P2SK (maks 10 thn pasca UU 1/2026); POJK 39/2024 jo 29/2025 (izin; batas transisi 12 Jan 2026)",
     "\"Sebagai mata pencaharian\" = kegiatan berulang (bukan sekali-sekali); skala menentukan pasal — jangan overcharge PKL ke pasal 5–10 thn",
     "Catatan transaksi gadai; barang jaminan di tempat; foto outlet; bukti penawaran",
     "Skala kecil → lapor OJK/Dinas dulu; skala besar → lidik Ps. 237 jo 305 P2SK",
     "Sedang — skala menentukan pasal; kesalahan kualifikasi = risiko gugur"],
    # 8
    ["Pencatatan/laporan keuangan palsu oleh pengurus (laporan RAT/neraca tidak sesuai riil)",
     "Laporan keuangan RAT fiktif; aset tercatat tak sesuai kenyataan; dana anggota dipakai pribadi; dua versi pembukuan; SHU diumumkan tapi tak dibagikan",
     "Pidana (bila LJK/entitas pembiayaan) / administratif",
     "Ps. 299 UU P2SK (pencatatan/laporan palsu entitas pembiayaan — penjara maks 3 thn/denda kat. III pasca UU 1/2026); KUHP 2023 Ps. 391 (pemalsuan surat); penggelapan Ps. 486 KUHP (4 thn) bila dana anggota dipakai pribadi",
     "Unsur sengaja membuat catatan palsu/menyesatkan; atau menguasai dana anggota melawan hak (penggelapan)",
     "Laporan keuangan vs mutasi rekening bank koperasi; berita acara RAT; keterangan pengurus/anggota; audit forensik",
     "Fokus follow the money; PPATK utk tracing; kalau closed-loop murni → koordinasi Kemenkop (administratif)",
     "Sedang — Ps. 299 P2SK terbatas entitas pembiayaan; closed-loop murni ranah Kemenkop"],
    # 9
    ["Pengurus/pengawas terpidana tindak pidana keuangan / identitas tidak cakap",
     "Pengurus pernah terpidana keuangan (seharusnya dilarang Permenkop 8/2023); NIK tidak ditemukan di dukcapil; pengurus rangkap tidak wajar; pengurus adalah \"pemilik\" tunggal (bukan dari anggota)",
     "Indikator (bukan delik berdiri sendiri)",
     "Permenkop 8/2023 (larangan pengurus terpidana tindak pidana keuangan); indikasi pemalsuan identitas (KUHP 391) / penipuan (492)",
     "Keberadaan larangan + fakta keterpidanaan/identitas fiktif; siapa pengendali riil (beneficial owner)",
     "KTP & NIK pengurus (verifikasi dukcapil); SK pengurus; riwayat perkara; AD/ART (syarat pengurus)",
     "Catat sbg indikator risiko; verifikasi identitas; arahkan ke pengendali riil utk konstruksi",
     "Lemah berdiri sendiri — pendukung delik lain"],
    # 10
    ["Bunga/tenor melampaui batas Permenkop 8/2023 (simpanan >9%/thn, pinjaman >24%/thn)",
     "Brosur produk bunga 12–24%/thn simpanan atau >24% pinjaman; denda/penalti siluman; tenor tidak transparan",
     "Administratif Kemenkop",
     "Permenkop 8/2023 Ps. terkait batas bunga (9%/24%) — sanksi administratif; BUKAN pidana langsung",
     "— (administratif)",
     "Brosur/skema produk; perjanjian pinjaman",
     "Temuan administratif → Dinas Koperasi; bahan edukasi sosialisasi (bukan pasal pidana)",
     "Lemah sbg pidana — jangan paksakan"],
    # 11
    ["Layanan keuangan digital tanpa izin ITSK (aplikasi koperasi dgn transfer/e-wallet/e-KYC)",
     "Aplikasi bisa transfer dana, bayar tagihan, dompet digital, e-KYC, P2P; dalih \"khusus anggota\"; tidak terdaftar di direktori ITSK OJK",
     "Pidana (P2SK)",
     "Ps. 213, 218, 304 UU P2SK (ITSK tanpa izin — penjara 5–10 thn + denda s.d. 1 T pasca UU 1/2026); activity-based approach (fitur, bukan pengguna)",
     "Fitur transaksional (transfer/bayar tagihan/e-KYC) = ITSK walau dalih anggota (Penjelasan POJK 3/2024)",
     "Screenshot aplikasi; uji fitur; hasil cek direktori ITSK OJK; kontrak/ToS",
     "Koordinasi OJK; kalau himpun dana juga → gabung Ps. 46 UU Perbankan",
     "Sedang — perlu bukti fitur transaksional riil"],
    # 12
    ["TPPU — aliran dana hasil usaha koperasi ilegal (follow the money)",
     "Dana simpanan mengalir ke rekening pribadi pengurus; pembelian aset atas nama keluarga; transfer ke luar negeri; struktur perusahaan cangkang",
     "Pidana (lapis kedua)",
     "UU 8/2010 Ps. 3–5 (5–20 thn) — menempatkan/mentransfer/menyamarkan hasil tindak pidana; kaitkan dgn predicate crime",
     "Predicate crime terbukti dulu; transaksi keuangan terkait hasil kejahatan; knowledge/sengaja menyamarkan",
     "Rekening koran; diagram aliran dana; data PPATK (LTKM); aset; keterangan saksi",
     "Minta analisis PPATK; gabungkan dalam berkas (konstruksi bertingkat)",
     "Kuat bila predicate terbukti; butuh data PPATK"],
]

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "CelahPidana"

header_fill = PatternFill("solid", fgColor="1F4E79")
header_font = Font(bold=True, color="FFFFFF", size=11)
wrap = Alignment(wrap_text=True, vertical="top")
thin = Side(style="thin", color="BBBBBB")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

for c, h in enumerate(HEADERS, 1):
    cell = ws.cell(row=1, column=c, value=h)
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = Alignment(wrap_text=True, vertical="center")
    cell.border = border

band = PatternFill("solid", fgColor="EAF1F8")
for r, row in enumerate(ROWS, 2):
    for c, v in enumerate(row, 1):
        cell = ws.cell(row=r, column=c, value=v)
        cell.alignment = wrap
        cell.border = border
        if r % 2 == 0:
            cell.fill = band
    ws.cell(row=r, column=1).alignment = Alignment(horizontal="center", vertical="top")

widths = [5, 34, 40, 20, 38, 40, 38, 30, 26]
for i, w in enumerate(widths, 1):
    ws.column_dimensions[get_column_letter(i)].width = w
ws.freeze_panes = "C2"
ws.auto_filter.ref = f"A1:I{len(ROWS)+1}"
ws.row_dimensions[1].height = 30

# Sheet 2: Petunjuk
ws2 = wb.create_sheet("Petunjuk")
notes = [
    ("PETUNJUK PENGGUNAAN MATRIKS", True),
    ("1. Matriks ini utk persiapan kunjungan Satgas PASTI ke Kab. Enrekang (8 Sep 2026) — bukan surat dakwaan.", False),
    ("2. Setiap pasal telah diverifikasi terhadap file vault hukum ~/penyidikan/ (grep ke UU asli). Ancaman pidana ditulis PASCA UU 1/2026.", False),
    ("3. Aturan emas: verifikasi legalitas DULU (ODS Kemenkop, direktori OJK, daftar Satgas PASTI), baru susun unsur. Terdaftar = presumsi sah.", False),
    ("4. Lex specialis: UU P2SK & UU sektoral lebih dulu dari KUHP. KUHP = subsider.", False),
    ("5. Closed-loop = Kemenkop (Permenkop 8/2023). Open-loop = OJK (Ps. 44B UU 25/1992 jo POJK 47/2024). Melayani non-anggota = keluar rezim koperasi.", False),
    ("6. Beda skala gadai: kecil Ps. 273 KUHP (1 thn) vs besar Ps. 237 jo 305 P2SK (maks 10 thn pasca UU 1/2026). Jangan overcharge.", False),
    ("7. Fokus bongkar sisi PENGHIMPUNAN DANA (di situ pidana penjara berat), bukan sekadar bunga/tenor.", False),
    ("8. Uji pembeli di lapangan: utus calon NON-anggota mencoba menabung/meminjam — catat respons + bukti.", False),
    ("9. Sumber: vault hukum (UU 25/1992, UU P2SK 4/2023 jo 4/2026, Permenkop 8/2023, POJK 47/2024, POJK 39/2024 jo 29/2025, UU Perbankan, KUHP UU 1/2023, UU 1/2026, UU 8/2010), Peta Pidana SJK, Referensi Satgas PASTI.", False),
    ("10. Dokumen terkait: 01-REGULASI-KOPERASI.md (inventaris), 03-CHECKLIST (isian lapangan), 05-AGENDA (alur SOP).", False),
]
for r, (txt, bold) in enumerate(notes, 1):
    cell = ws2.cell(row=r, column=1, value=txt)
    cell.alignment = wrap
    if bold:
        cell.font = Font(bold=True, size=12, color="1F4E79")
ws2.column_dimensions["A"].width = 130

wb.save(OUT)
print("OK — sheet:", wb.sheetnames, "| baris data CelahPidana:", ws.max_row - 1)
