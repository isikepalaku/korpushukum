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
