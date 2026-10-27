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
