# UU-KB — Vault Database Hukum (AI Knowledge Base)

Folder ini adalah **calon vault baru**: korpus undang-undang Indonesia yang bersih,
siap dipakai sebagai feed AI (RAG / embedding / query), terpisah dari vault kerja
`E:/Agent/UU` yang berisi data lidik kasus.

## Instruksi copy (untuk Komandan)

Salin **seluruh isi** `E:\Agent\UU` ke folder ini (`E:\Agent\UU-KB`), **kecuali** folder
`.git` (jangan bawa riwayat/remote repositori kasus). Pilih salah satu:

### Opsi A — robocopy (disarankan, cepat & bisa exclude)

```cmd
robocopy "E:\Agent\UU" "E:\Agent\UU-KB" /E /XD "E:\Agent\UU\.git" /NFL /NDL /NP
```

### Opsi B — Explorer

1. Buka `E:\Agent\UU`
2. Aktifkan *View → Show → Hidden items*, lalu **hapus centang** folder `.git`
3. `Ctrl+A` → `Ctrl+C` → buka `E:\Agent\UU-KB` → `Ctrl+V`

### Setelah copy selesai

- File `README-COPY.md` ini **tetap ada** di folder tujuan (penanda lokasi yang benar).
- Konfirmasi ke Hermes: "sudah dicopy".
- Hermes lalu akan: audit isi, buang materi kasus/lidik & artefak berat, susun ulang
  skema per-aturan (frontmatter + wikilink + index), siapkan ekspor mesin-readable
  (JSONL/parquet chunk untuk embedding), lalu git init + repo private baru.

## Batas tanggung jawab (penting)

- **JANGAN** menyalin `.git` — remote `vault-hukum` memuat riwayat data perkara.
- Setelah copy, isi folder ini masih **campuran** (kasus, mindik, analisis, raw).
  Pembersihan dilakukan pada tahap berikutnya, bukan sebelum copy.
