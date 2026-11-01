---
name: legal-corpus-pipeline
description: Automates the ingestion, parsing, deduplication, categorization, lifecycle management (marking amendments/repeals), and OpenViking incremental embedding of Indonesian legal documents (UU, PP, Perpres, Permen, POJK, etc.) into Obsidian Karpathy LLM-Wiki and UU-KB corpus using Docling.
metadata:
  tags: [hukum, docling, obsidian, parser, uukb, rag, openviking]
  category: legal-engineering
  role: legal-pipeline-engineer
---

# Legal Corpus Pipeline Skill

Skill otomatisasi untuk memproses dokumen hukum resmi Indonesia (Undang-Undang, Perppu, PP, Perpres, Permen, POJK, Putusan MK) ke dalam **Obsidian Vault (UU-KB)**, **Karpathy LLM-Wiki**, dan lapisan embedding inkremental **OpenViking**.

---

## Arsitektur Dua Vault

- **`E:\Agent\UU-KB` (`korpushukum`)**: Basis pengetahuan hukum otoritatif bersih (teks undang-undang, MOC, pasal atomik, chunks vektor). **Bebas dari data perkara, nama tersangka, nomor LP, atau rahasia penyidikan.**
- **`E:\Agent\UU` (`vault hukum`)**: Ruang kerja penyidikan (kasus aktif, telaahan hukum, mindik, berita acara). Merujuk norma hukum resmi via wikilink ke `korpushukum`.
- **`OpenViking` (`127.0.0.1:1933`)**: Mesin recall memori cerdas yang meng-embed chunks hukum secara inkremental dari `90-log/manifest.jsonl` dan `90-log/chunks.jsonl.gz`.

---

## Kapabilitas Utama

1. **Deduplikasi Cerdas (Sub-Second Pre-Check)**:
   - Memeriksa apakah ID dokumen (misal `UU 1/2024`) sudah ada di dalam korpus sebelum menjalankan Docling OCR.
   - Melewati berkas yang identik secara instan (`--skip`), atau menimpa jika diminta pengguna (`--force`).
2. **Ekstraksi Deterministik Docling + Regex**:
   - Mengekstrak tata letak PDF menjadi Markdown bersih menggunakan GPU-accelerated Docling (`RapidOCR`).
   - Memisahkan **Batang Tubuh** dan **Penjelasan Resmi** di lampiran belakang.
   - Menjahit (*stitch*) Batang Tubuh dan Penjelasan per pasal tanpa token LLM.
   - Mempertahankan penomoran pasal amandemen (seperti `Pasal 27A`, `Pasal 27B`, `Pasal 45B`, `Pasal 39D`) dan ayat turunan (`(2a)`, `(2b)`).
   - Mengoreksi kesalahan tipikal OCR hukum Indonesia (`Pasal 278` $\to$ `27B`, `Pasal 168` $\to$ `16B`).
3. **Manajemen Siklus Hidup Norma (Graf Simetris)**:
   - Jika dokumen baru `mengubah` dokumen lama: Dokumen lama otomatis ditandai `diubah_oleh: [ID_BARU]`, status menjadi `diubah`.
   - Jika dokumen baru `mencabut` dokumen lama: Dokumen lama otomatis ditandai `dicabut_oleh: [ID_BARU]`, status menjadi `dicabut`, dan disematkan callout bahaya `> [!CAUTION] PERATURAN INI TELAH DICABUT OLEH [[...]]`.
4. **Dual Output Generation (Hybrid)**:
   - **Mode Karpathy LLM-Wiki**:
     - `02_LEGISLATION/<KODE_UU>/Pasal_<NO>.md` (1 berkas per pasal terjahit dengan penjelasannya).
     - `01_INDEX_MOC/_Index_<KODE_UU>.md` (Daftar ringkas pasal & inti ayat 1).
     - `01_INDEX_MOC/_MASTER_INDEX.md` (Peta hierarkis seluruh peraturan untuk retrieval 2-tahap).
   - **Mode UU-KB Native**:
     - `10-peraturan/<subfolder>/<JENIS> <NO>-<THN> - <JUDUL>.md` (1 berkas terpartisi dengan anchor unik `^pasal-X` dan `^penjelasan-pasal-X` sesuai kontrak `AGENTS.md`).
5. **OpenViking Incremental Loader**:
   - Hanya meng-embed dokumen/chunk yang mengalami perubahan hash SHA256 (`90-log/openviking_state.json`).
   - Otomatis memfilter penjelasan non-substantif (*"Cukup jelas."*) agar hemat token.

---

## Cara Eksekusi

### 1. Ingest Interaktif / All-in-One (Disarankan)
Jalankan skrip pembantu interaktif:
```powershell
python scripts/ingest_interactive.py --file "30-sumber/Nama_File.pdf" --auto-commit
```
Skrip ini otomatis mendeteksi metadata, memanggil Docling, memperbarui manifest, me-rebuild chunks vektor, dan menyinkronkan state OpenViking.

### 2. Ingest Langsung via Pipeline Orchestrator
```powershell
& "C:\Users\ibrah\AppData\Roaming\uv\tools\docling\Scripts\python.exe" scripts/pipeline_orchestrator.py `
  --file "30-sumber/Nama_File.pdf" `
  --mode both
```

### 3. Ingest Batch Seluruh Direktori
```powershell
& "C:\Users\ibrah\AppData\Roaming\uv\tools\docling\Scripts\python.exe" scripts/pipeline_orchestrator.py `
  --dir "30-sumber" `
  --mode both
```

### 4. Sinkronisasi Inkremental OpenViking
```powershell
# Cek perbedaan dokumen/chunk yang berubah (dry-run):
python scripts/openviking_ingest.py --check

# Sinkronisasi dan update state:
python scripts/openviking_ingest.py --sync
```

---

## Template Prompt AI Agent untuk PC
Bila Anda ingin memerintahkan AI Agent manapun di PC untuk menambahkan peraturan baru:

```markdown
Kamu bertugas menambahkan dokumen regulasi baru ke dalam repositori knowledge base hukum ini (korpushukum) menggunakan pipeline yang sudah tersedia di folder `scripts/`.

### Lingkungan & Konfigurasi PC:
- Repositori: `korpushukum` (E:\Agent\UU-KB)
- Vault Kerja Kasus: `vault hukum` (E:\Agent\UU)
- Parser: Docling via uv tool yang sudah terpasang di:
  `C:\Users\ibrah\AppData\Roaming\uv\tools\docling\Scripts\python.exe`

---

### Tugas:
Ekstrak dan masukkan dokumen regulasi hukum berikut ke dalam repositori:

1. Path Berkas Sumber (PDF / Dokumen):
   `<PATH_FILE_PDF_ATAU_MD>`

2. Metadata Regulasi:
   - Jenis: `<UU / PP / PERPRES / PERMEN / POJK / PERPOL / KEP-MENTERI>`
   - Nomor: `<NOMOR>`
   - Tahun: `<TAHUN>`
   - Kode Dokumen: `<CONTOH: PERMENKOP_8_2023>`
   - Judul Lengkap: `<JUDUL LENGKAP RESMI>`
   - Judul Singkat: `<JUDUL SINGKAT, maks 52 karakter>`
   - Bidang: `<keuangan / pidana / siber / pertanahan / tipidter / umum>`

---

### Perintah Eksekusi:
Jalankan skrip all-in-one berikut:
python scripts/ingest_interactive.py --file "<PATH_FILE_PDF_ATAU_MD>" --auto-commit
```
