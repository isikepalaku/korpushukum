---
judul: "Log Perubahan Korpus"
jenis: log
tags: [log]
last_updated: 2026-10-28
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
