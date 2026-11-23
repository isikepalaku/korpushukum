---
judul: "Log Perubahan Korpus"
jenis: log
tags: [log]
last_updated: 2026-11-03
---

# Log Korpus

## [2026-10-28] restrukturisasi | vault kerja → korpus hukum murni

- Sumber: salinan vault kerja `E:/Agent/UU` (116 MB, 269 md bercampur data perkara).
- Dipindah ke struktur hirarki: **127 dokumen** (113 peraturan + 14 putusan).
- Dinormalisasi: frontmatter seragam (id, jenis, nomor, tahun, status, relasi, bidang, kelengkapan, verifikasi),
  nama berkas `<JENIS> <nomor>-<tahun> - <singkat>.md`, H1 + blok status, `Relevansi lidik` dibuang.
- Dari 6 duplikat/keputusan editorial: 2 duplikat id (UU 21/2008, UU 1/2026) → versi terpendek diarsipkan;
  4 halaman dossier multi-peraturan/referensi lidik → diarsipkan.
- 10 peraturan yang hanya tersedia PDF/HTML dibuatkan **stub** (`kelengkapan: sumber-pdf-saja`) + berkas sumber.
- Materi non-hukum (analisis kasus, mindik BAP, tools, raw BAP/mutasi, wiki kasus/konsep, profil, panduan plugin)
  dikeluarkan ke `E:/Agent/UU-KB-arsip/` — tidak dihapus, tetap bisa dirujuk.
- Dibuat: `INDEX.md`, `40-kategori/*` (per bidang), `50-glosarium/Glosarium.md`, `AGENTS.md`, `README.md`,
  `90-log/manifest.jsonl`.
- Status: `verifikasi: belum` untuk seluruh dokumen — verifikasi JDIH BPK belum dijalankan.

## [2026-10-28] ekstraksi | 10 berkas sumber menjadi teks penuh

- Ekstraksi via `pymupdf4llm 2.0` (9 PDF) + `bs4+markdownify` dengan tabel diratakan (1 HTML).
- 10 halaman stub (`kelengkapan: sumber-pdf-saja`) kini `lengkap`, total **327.119 karakter** teks.
  - POJK 18/2017 58.137 · SEOJK 8/2015 80.320 · POJK 65/2016 56.585 · POJK 1/2013 31.440 · UU 4/1996 27.915 · POJK 19/2018 22.327 · UU 1/1946 28.026 · POJK 42/2017 10.696 · INPRES 4/1984 4.688 · INPRES 18/1998 3.881.
- Catatan kualitas: SEOJK 8/2015 memakai struktur angka Romawi (bukan "Pasal") — wajar untuk surat edaran;
  UU 4/1996 berasal dari HTML Word, tabel layout diratakan agar alur teks terbaca.
- `parser` + `parsed_at` dicatat di frontmatter tiap halaman; `90-log/manifest.jsonl` diperbarui.
- Sisa stub: 0. Seluruh 127 dokumen kini punya teks.

## [2026-10-28] verifikasi | status 127 dokumen ke JDIH BPK

- Sumber: `peraturan.bpk.go.id` — URL detail dipetakan dari **sitemap per tahun** (7.458 kunci slug),
  bukan pencarian situs (mesin pencari BPK tidak presisi).
- **95 dokumen terverifikasi** (status + tanggal + relasi resmi). 32 tidak tersedia di BPK (lihat bawah).
- Hasil status: **115 berlaku, 6 dicabut, 6 perlu verifikasi** (sebelumnya 119/1/7).
- **5 koreksi status** dari BPK: `INPRES 4/1984`, `PERMENKOMINFO 19/2014`, `PERMENKUMHAM 10/2013`,
  `POJK 1/2013`, `POJK 19/2018` → semuanya **Tidak Berlaku** (dicabut).
- Relasi antar-peraturan diambil ulang dari BPK (lebih lengkap dari kurasi manual): 73 dokumen punya
  blok relasi, termasuk `mencabut_sebagian` (baru). Contoh: UU 4/2023 `mengubah` 22 peraturan.
- Field baru/terisi: `status_bpk` (label mentah), `ditetapkan`/`berlaku_mulai` (ISO dari BPK),
  `sumber` (URL detail BPK kanonik, URL lama non-BPK dipindah ke `sumber_alternatif`),
  `verifikasi: sudah|tidak-tersedia`, `verifikasi_sumber`, `verifikasi_tanggal`.
- Rujukan sumber `sumber: JDIH BPK` dipetakan ke URL kanonik untuk 95 dokumen.
- 32 dokumen tidak terverifikasi:
  - 14 putusan MK — tidak terindeks di JDIH BPK (sumbernya mkri.id), ditandai `tidak-tersedia`.
  - 5 SEOJK (8/2015, 19/2023, 5/2024, 6/2024, 20/2024) — tidak ada di sitemap BPK.
  - 5 POJK (33/2024, 36/2024, 39/2024, 40/2024, 33/2025) — nomor tidak ada di sitemap BPK.
  - 3 Kepmenkomdigi (140/142/219/2026), 1 Instruksi Menteri Kominfo 1/2023, 1 PP 33/2026.
  - SKB 2021 (Pedoman UU ITE) dan JUKRAH 2021 — bukan jenis peraturan terindeks BPK.
- Verifikasi YAML: 127/127 valid; wikilink 0 rusak; tag `status/*` disinkronkan ulang.

## [2026-10-28] struktur | partisi batang tubuh vs penjelasan + anchor pasal

- Masalah: teks "PENJELASAN" (I. UMUM / II. PASAL DEMI PASAL) selalu di akhir halaman, panjang, dan
  berubah antar amandemen sehingga sulit dirujuk presisi.
- Solusi (Obsidian-flavored): partisi per heading —
  `## Batang Tubuh` / `### Pasal N ^pasal-N` / `## Penjelasan` / `### I. Umum` /
  `### II. Pasal demi Pasal` / `#### Pasal N ^penjelasan-pasal-N` / `## Peta Penjelasan`.
- 81 dokumen terpartisi; **5.541 anchor `^pasal-N`** dan **4.461 anchor `^penjelasan-pasal-N`**.
  46 dokumen tanpa penjelasan (POJK/SEOJK/putusan).
- Heading liar hasil ekstraksi PDF (`## Cukup jelas …`) diubah jadi teks tebal agar outline tidak kacau.
- `90-log/manifest.jsonl` kini memuat `sections[]` (`path`, `anchor`, `chars`) → chunk RAG tidak perlu
  menebak batas pasal; contoh UU 42/1999 = 87 section.
- Frontmatter baru: `penjelasan`, `penjelasan_pasal_demi_pasal`, `penjelasan_normatif: false`,
  `struktur_teks: terpartisi`, `anchor_pasal`.
- Pengaman: setiap file dibandingkan panjang teks sebelum/sesudah; bila menyusut >1% file dilewati
  (percobaan pertama sempat memangkas teks karena logika partisi salah → di-rollback dari git, lalu
  skrip ditulis ulang konservatif). Hasil akhir: tidak ada file menyusut >0,5%.
- Plugin `karpathywiki` dinonaktifkan di vault ini (membuat scaffolding `wiki/` yang mengotori korpus).
- AGENTS.md + README: aturan kutip/embed anchor, larangan menyalin teks penjelasan, strategi chunk.

## [2026-10-28] ekspor mesin | chunker + indeks kualitas penjelasan

- `90-log/build_chunks.py` (stdlib, jalan mandiri: `python 90-log/build_chunks.py`).
- Output `90-log/chunks.jsonl.gz` — **24,185 chunk**, rata-rata 917 char,
  maks 2504: `batang-tubuh` 7,511 ·
  `penjelasan-umum` 1,767 ·
  `penjelasan-pasal` 5,773 ·
  `isi` 9,126. Cakupan 96,5% teks (sisanya tabel Peta Penjelasan yang sengaja
  dilewati). Artefak turunan → masuk `.gitignore`.
- Penjelasan "Cukup jelas" ditandai `substantive: false` (2,170 chunk) agar tidak
  mengotori retrieval; penjelasan substantif: 3,603 chunk.
- `40-kategori/Indeks Penjelasan.md` — 57 peraturan dengan tabel pasal berpenjelasan / substantif /
  cukup jelas / persentase. Contoh: UU 6/2023 Cipta Kerja 456 pasal (54% substantif),
  UU 4/2023 P2SK 329 pasal (56%), UU 20/2025 KUHAP 362 pasal (28%).
- Koreksi struktur: 9 putusan MK yang sempat dipartisi dikembalikan ke `struktur_teks: datar` —
  putusan hanya *mengutip* Penjelasan pasal, bukan punya bagian penjelasan sendiri.
- `chunks-stats.json` di-commit sebagai penanda versi ekspor.

## [2026-11-01] ingest-auto | UU 5/2026

- Inisiasi dokumen UU 5/2026 (Kepolisian Perubahan Ketiga...). Mengubah: ['UU 2/2002', 'UU 2/2022', 'UU 6/2023', 'UU 20/2023'], Mencabut: [].
- Pipeline: Docling + Deterministic Regex Stitcher + Relational Graph Syncer.

## [2026-11-01] ingest-auto | UU 11/2008

- Inisiasi dokumen UU 11/2008 (ITE...). Mengubah: [], Mencabut: [].
- Pipeline: Docling + Deterministic Regex Stitcher + Relational Graph Syncer.

## [2026-11-01] ingest-auto | UU 28/2011

- Inisiasi dokumen UU 28/2011 (ITE Perubahan Pertama...). Mengubah: ['PP 68/1998'], Mencabut: [].
- Pipeline: Docling + Deterministic Regex Stitcher + Relational Graph Syncer.

## [2026-11-01] ingest-auto | UU 19/2016

- Inisiasi dokumen UU 19/2016 (ITE Perubahan Pertama...). Mengubah: ['UU 11/2008'], Mencabut: [].
- Pipeline: Docling + Deterministic Regex Stitcher + Relational Graph Syncer.

## [2026-11-01] ingest-auto | UU 10/1998

- Inisiasi dokumen UU 10/1998 (Perbankan 1998...). Mengubah: ['UU 7/1992', 'UU 13/1968'], Mencabut: [].
- Pipeline: Docling + Deterministic Regex Stitcher + Relational Graph Syncer.

## [2026-11-01] INGEST | POJK 6/2026

- Menambahkan regulasi operasional POJK 6/2026 tentang POJK 6-2026 - Perilaku Penyampai Informasi Sektor Jasa Keuangan
- Pipeline: Docling + Deterministic Regex Stitcher + Relational Graph Syncer.

## [2026-11-01] INGEST | POJK 7/2026

- Menambahkan regulasi operasional POJK 7/2026 tentang POJK 7-2026 - Modal Minimum BPR
- Pipeline: Docling + Deterministic Regex Stitcher + Relational Graph Syncer.

## [2026-11-01] INGEST | POJK 8/2026

- Menambahkan regulasi operasional POJK 8/2026 tentang POJK 8-2026 - Pelaporan Data Transaksi LPBBTI
- Pipeline: Docling + Deterministic Regex Stitcher + Relational Graph Syncer.

## [2026-11-01] INGEST | PERPOL 8/2021

- Menambahkan regulasi operasional PERPOL 8/2021 tentang PERPOL 8-2021 - Penanganan Tindak Pidana Keadilan Restoratif
- Pipeline: Docling + Deterministic Regex Stitcher + Relational Graph Syncer.

## [2026-11-01] INGEST | SKB 229/2021

- Menambahkan regulasi operasional SKB 229/2021 tentang SKB 229-2021 - Pedoman Implementasi UU ITE
- Pipeline: Docling + Deterministic Regex Stitcher + Relational Graph Syncer.

## [2026-11-01] INGEST | SE-KAPOLRI 2/2021

- Menambahkan regulasi operasional SE-KAPOLRI 2/2021 tentang SE-KAPOLRI 2-2021 - Penerapan UU ITE Ruang Digital
- Pipeline: Docling + Deterministic Regex Stitcher + Relational Graph Syncer.

## [2026-11-01] ingest-auto | PERMEN-ESDM 20/2021

- Inisiasi dokumen PERMEN-ESDM 20/2021 (Peraturan Menteri Energi dan Sumber Daya Mineral Nomor 20 Ta...). Mengubah: [], Mencabut: [].
- Pipeline: Docling + Deterministic Regex Stitcher + Relational Graph Syncer.

## [2026-11-01] ingest-auto | PERMEN-ESDM 11/2022

- Inisiasi dokumen PERMEN-ESDM 11/2022 (Peraturan Menteri Energi dan Sumber Daya Mineral Nomor 11 Ta...). Mengubah: ['PERMEN-ESDM 20/2021'], Mencabut: [].
- Pipeline: Docling + Deterministic Regex Stitcher + Relational Graph Syncer.

## [2026-11-02] verifikasi & deduplikasi | Siber (SKB 229/2021, UU 28/2011, Kepmenkomdigi, Instruksi)

- Resolusi anomali `01-moc/Siber.md`: tabel statis diselaraskan dari 23 baris menjadi tepat 21 baris sesuai frontmatter `jumlah: 21`.
  - Menghapus entri duplikat `SKB 2021` (disatukan ke berkas kanonikal `SKB 229/2021` - Keputusan Bersama Menkominfo 229/2021, Jaksa Agung 154/2021, Kapolri KB/2/VI/2021).
  - Menghapus entri phantom `UU 28/2011` yang salah dilabeli "ITE Perubahan Pertama" (perubahan pertama ITE yang sah adalah `UU 19/2016` yang sudah lengkap di vault).
- Deduplikasi berkas:
  - Dihapus: `10-peraturan/09-instrumen-lain/SKB 2021 - Pedoman Implementasi UU ITE.md` (id digabung ke `SKB 229/2021`).
  - Dihapus: `10-peraturan/08-peraturan-polri/SE-KAPOLRI 2-2021 - Penerapan UU ITE Ruang Digital.md` (duplikat draft dari `SE-KAPOLRI 2-2021 - Penegakan Hukum UU ITE.md`).
- Verifikasi dokumen:
  - `KEPMENKOMDIGI 140/2026`: status `berlaku`, verifikasi `sudah` (JDIH Komdigi).
  - `KEPMENKOMDIGI 142/2026`: status `diubah`, `diubah_oleh: [KEPMENKOMDIGI 219/2026]`, verifikasi `sudah` (JDIH Komdigi).
  - `KEPMENKOMDIGI 219/2026`: status `berlaku`, `mengubah: [KEPMENKOMDIGI 142/2026]`, verifikasi `sudah` (JDIH Komdigi).
  - `INSTRUKSI 1/2023`: diverifikasi sebagai Instruksi Menteri Kominfo No. 1 Tahun 2023 (bukan Inpres), status `berlaku`, verifikasi `sudah` (Kemenkominfo).
  - `SKB 229/2021`: status `berlaku`, verifikasi `sudah` (Menkominfo / Kejagung / Polri).
- Sinkronisasi `INDEX.md`, `90-log/manifest.jsonl` (133 dokumen bebas duplikat ID), dan `90-log/build_chunks.py`.

## [2026-11-03] normalisasi & audit integritas | pasal atomik & heading terpartisi

- Normalisasi heading Batang Tubuh & Penjelasan:
  - Perbaikan anomali heading dan OCR pada KUHP (UU 1/2023), UU Migas (UU 22/2001), UU Hak Tanggungan (UU 4/1996), UU ITE (UU 11/2008), dan PP 71/2019.
  - Heading formal (### Pasal X ^pasal-x dan #### Pasal X ^penjelasan-pasal-x) dipulihkan secara presisi.
- Ekspor ulang & regenerasi pasal atomik (02-pasal-atomik/):
  - Total 7.619 berkas atomik diperbarui dan diselaraskan dengan dokumen induk dan penjelasannya.
  - Pembersihan berkas atomik stale/orphan sebelum ekspor batch.
- Pembaruan parser & tooling:
  - scripts/docling_legal_parser.py: peningkatan heuristik regex OCR, handling nomor pasal inline, normalisasi angka romawi/karakter mirip OCR, dan deteksi heading formal markdown.
  - Penambahan skrip audit mandiri scripts/validate_corpus.py (Sequence & Gap Detection, verifikasi integritas 119 peraturan & 7.619 pasal atomik).
- Sinkronisasi metadata korpus:
  - INDEX.md, README.md, 01-moc/*, 90-log/manifest.jsonl, dan 90-log/chunks-stats.json.

## [2026-11-23] lint & perawatan | utang lint korpus (41 ERROR -> 1)

- `scripts/build_temporal_graph.py`: urutan glob dan daftar tautan di-`sorted()` agar deterministik (sebelumnya tiap run menulis ulang ±260 berkas atomik dengan urutan acak). Satu kali normalisasi 59 berkas atomik (hanya urutan baris; isi tidak berubah).
- Frontmatter partisi dilengkapi pada 18 dokumen datar tanpa penjelasan (`penjelasan_pasal_demi_pasal: false`; `penjelasan_normatif: false` pada 5 dokumen yang belum memuatnya): INPRES 4/1984 & 18/1998, INSTRUKSI 1/2023, KEPMENKOMDIGI 140/142/219-2026, PERMENKOMINFO 5/2020, 10/2021, 19/2014, PERPRES 82/2022, PERPOL 8/2021, POJK 6/7/8-2026, SEOJK 6/2024 & 8/2015, SE-KAPOLRI 2/2021, SKB 229/2021.
- UU 1/1946: judul pasal 1-17 diubah menjadi heading beranchor `^pasal-N` (teks tidak diubah). UU 3/2004: `anchor_pasal` dikoreksi ke `false` (undang-undang perubahan dengan Pasal I-III; 8 berkas atomik UU_3_2004 berasal dari kutipan pasal yang diubah -> perlu parse ulang).
- Relasi: UU 6/2023 `diubah_oleh` dikurangi UU 14/2025, 16/2025, 18/2025, 5/2026, 65/2024, 66/2024 (teks hanya mengutip "sebagaimana telah diubah dengan UU 6/2023", bukan mengubahnya); UU 1/2025 `diubah_oleh` dikurangi UU 16/2025 (sama). UU 10/1998 dilengkapi `mengubah: UU 7/1992` dan `diubah_oleh: UU 4/2023, UU 6/2023` (simetri).
- Sisa: JUKRAH 1/2021 (nama berkas tak sesuai id, judul "HALAMAN 1", folder atomik & indeks ganda `JUKRAH_1_2021` / `JUKRAH_2021`) — butuh kurasi manual.


## [2026-11-23] perbaikan JUKRAH 1/2021 & penataan UU 3/2004

- JUKRAH 1/2021 (Tugas A):
  - Nama berkas dan sumber PDF diselaraskan dengan kontrak: `10-peraturan/09-instrumen-lain/JUKRAH 1-2021 - Izin Presiden dan Mendagri.md` dan `30-sumber/JUKRAH 1-2021 - Izin Presiden dan Mendagri.pdf`.
  - Transkripsi teks otoritatif secara faithful dari dokumen asli (8 halaman) yang terdiri dari Surat Telegram Kapolri (hal 1–2) dan Lampiran Surat Kabareskrim B/5308/IX/RES.7.5./2020/Bareskrim tanggal 17 September 2020 (hal 3–8).
  - Mengoreksi judul artefak OCR lama ("HALAMAN 1") menjadi judul substantif: `Petunjuk dan Arahan terkait Permohonan Persetujuan Tertulis Presiden dan Mendagri`.
  - Mengatur `struktur_teks: datar`, `anchor_pasal: false`, `penjelasan: tidak`, `penjelasan_pasal_demi_pasal: false`, `status: perlu-verifikasi`, `verifikasi: belum`.
  - Nomor ST dicatat `ST/[?]48/VIII/RES.7.5./2021` karena digit kedua terpotong/ambigu (`[?]48` pada hal 1 dan hal 2) tanpa manipulasi/spekulasi nomor.
  - Menghapus folder pasal atomik duplikat (`02-pasal-atomik/JUKRAH_1_2021/` dan `02-pasal-atomik/JUKRAH_2021/`) dan berkas MOC duplikat (`01-moc/_Index_JUKRAH_1_2021.md` dan `01-moc/_Index_JUKRAH_2021.md`), serta membersihkan rujukannya di `01-moc/Umum.md`, `01-moc/_MASTER_INDEX.md`, dan `INDEX.md`.
- UU 3/2004 (Tugas B):
  - Mengunduh sumber PDF resmi dari JDIH BPK (36 halaman) ke `30-sumber/UU 3-2004 - BI Perubahan.pdf` dan memverifikasi kelengkapan naskah.
  - Memperbaiki parsing Batang Tubuh: menghapus heading `## Penjelasan` dan `### I. Umum` palsu yang tersisip di tengah kalimat Angka 6 (perubahan Pasal 34), sehingga teks Angka 6 s.d. 21, Pasal II, dan Pasal III kembali utuh ke Batang Tubuh.
  - Menambahkan heading formal `### Pasal <N> ^pasal-<n>` pada 20 pasal kutipan di dalam Pasal I (Pasal 4, 6, 7, 10, 11, 34, 38, 40, 41, 47, 48, 52, 54, 55, 58, 58A, 60, 62, 77, 77A).
  - Membersihkan sisa artefak OCR header halaman pada pergantian halaman di beberapa pasal.
  - Mempartisi bagian Penjelasan resmi menjadi `### I. Umum` dan `### II. Pasal demi Pasal` dengan heading `#### Pasal <N> ^penjelasan-pasal-<n>` untuk seluruh 20 pasal, dilengkapi tabel `## Peta Penjelasan`.
  - Memperbarui frontmatter partisi: `struktur_teks: terpartisi`, `anchor_pasal: true`, `penjelasan: ada`, `penjelasan_pasal_demi_pasal: true`.
  - Menyelaraskan pasal atomik di `02-pasal-atomik/UU_3_2004/` (tepat 20 berkas atomik sesuai 20 heading pasal batang tubuh) dan memperbarui `01-moc/_Index_UU_3_2004.md` serta `01-moc/_MASTER_INDEX.md`.
  - Memverifikasi simetri relasi dengan `UU 23/1999` (`mengubah: ["UU 23/1999"]` pada UU 3/2004 dan `diubah_oleh: [..., "UU 3/2004", ...]` pada UU 23/1999).
- Sinkronisasi metadata korpus & verifikasi:
  - Ekspor ulang `90-log/manifest.jsonl`, `90-log/chunks.jsonl.gz`, `90-log/chunks-stats.json`, dan `01-moc/Indeks Penjelasan.md`.
  - Regenerasi temporal graph melalui `scripts/build_temporal_graph.py`.
  - Audit `scripts/validate_corpus.py`: 0 issues detected across all 119 regulations & 7,627 atomic files.
  - Audit `scripts/lint_korpus.py`: 0 ERROR across all 133 documents.


## [2026-11-23] ingest | UU 3/2026 tentang Pelindungan Saksi dan Korban

- Sumber PDF disalin ke `30-sumber/UU 3-2026 - Pelindungan Saksi dan Korban.pdf` (62 halaman).
- Ekstraksi via Docling (`scripts/ingest_interactive.py` + `scripts/docling_legal_parser.py`):
  - Korpus terpartisi: `10-peraturan/01-undang-undang/UU 3-2026 - Pelindungan Saksi dan Korban.md` (78 pasal, lengkap dengan Penjelasan Umum & Pasal demi Pasal).
  - Pasal atomik: 78 berkas di `02-pasal-atomik/UU_3_2026/`.
  - Indeks MOC: `01-moc/_Index_UU_3_2026.md`.
- Metadata & relasi: `ditetapkan: 2026-05-20`, `berlaku_mulai: 2026-05-20`, `mencabut: [UU 13/2006, UU 31/2014]`, `bidang: [pidana]`, `status: berlaku`.
- Sinkronisasi `INDEX.md`, `01-moc/Pidana.md`, `90-log/manifest.jsonl` (134 dokumen), `90-log/chunks.jsonl.gz`, `01-moc/Indeks Penjelasan.md`, dan state inkremental OpenViking.

## [2026-11-23] ingest | 11 regulasi koperasi & Kopdes Merah Putih (2025–2026)

- Sumber: `peraturan.go.id` (hasil pencarian `koperasi` untuk regulasi substantif 2025–2026), diunduh ke `30-sumber/`.
- Ekstraksi via Docling (`scripts/docling_legal_parser.py`) dengan penempatan terstruktur di `10-peraturan/05-peraturan-menteri/` dan `10-peraturan/09-instrumen-lain/` serta pasal atomik di `02-pasal-atomik/` + indeks di `01-moc/`:
  - `PERMENKUM 13/2025` — Pengesahan Koperasi (32 pasal)
  - `PERMENKOP 1/2025` — Dana Bergulir Mock Up Kopdes Merah Putih (25 pasal)
  - `PERMENKOP 7/2025` — OTK Lembaga Pengelola Dana Bergulir Koperasi (123 pasal)
  - `PERMENKOP 9/2025` — Dana Bergulir Kopdes Merah Putih (19 pasal)
  - `PERMENDESPDT 10/2025` — Persetujuan Kades Pembiayaan Kopdes Merah Putih (11 pasal)
  - `PERMENKEU 49/2025` — Tata Cara Pinjaman Pendanaan Kopdes Merah Putih (14 pasal)
  - `PERMENKEU 63/2025` — Penggunaan SAL 2025 Pendanaan Kopdes Merah Putih (6 pasal)
  - `PERMENKEU 15/2026` — Penyaluran DAU/DBH/Dana Desa Gerai Kopdes Merah Putih (12 pasal)
  - `PERMENKOP 4/2026` — Pembangunan Pasar Rakyat oleh Koperasi (44 pasal)
  - `PERMENKOP 6/2026` — Pedoman Bantuan Pemerintah Kemenkop (20 pasal)
  - `PERBAGI 10/2026` — Penggunaan Produk Dalam Negeri dan Pelibatan UMKM/Koperasi/Kopdes (19 pasal)
- Sinkronisasi `INDEX.md`, `01-moc/Keuangan.md`, `90-log/manifest.jsonl` (145 dokumen), `90-log/chunks.jsonl.gz`, `90-log/openviking_state.json`, dan validasi `scripts/validate_corpus.py` (131 peraturan, 8.030 berkas atomik, 0 error).
