---
name: legal-corpus-pipeline
description: Automates the ingestion, parsing, deduplication, categorization, and lifecycle management (marking amendments/repeals) of Indonesian legal documents (UU, PP, Perpres, Permen, POJK, etc.) into Obsidian Karpathy LLM-Wiki and UU-KB corpus using Docling.
metadata:
  tags: [hukum, docling, obsidian, parser, uukb, rag]
  category: legal-engineering
  role: legal-pipeline-engineer
---

# Legal Corpus Pipeline Skill

Skill otomatisasi untuk memproses dokumen hukum resmi Indonesia (Undang-Undang, Perppu, PP, Perpres, Permen, POJK, Putusan MK) ke dalam **Obsidian Vault (UU-KB)** dan **Karpathy LLM-Wiki**.

## Kapabilitas Utama

1. **Deduplikasi Cerdas (Skip Duplikat / Tambah Baru)**:
   - Memeriksa apakah ID dokumen (misal `UU 1/2024`) sudah ada di dalam korpus sebelum menjalankan Docling OCR.
   - Melewati secara instan berkas yang sudah ada (`--skip`), atau menimpa jika diminta pengguna (`--force`).
2. **Ekstraksi Deterministik Docling + Regex**:
   - Mengekstrak tata letak PDF menjadi Markdown bersih menggunakan GPU-accelerated Docling (`RapidOCR`).
   - Memisahkan **Batang Tubuh** dan **Penjelasan Resmi** di lampiran belakang.
   - Menjahit (stitch) Batang Tubuh dan Penjelasan per pasal tanpa memanggil token LLM.
   - Mengoreksi kesalahan tipikal OCR hukum Indonesia (misal: `Pasal 278` $\to$ `Pasal 27B`, `Pasal 168` $\to$ `Pasal 16B`, `Pasal2TA` $\to$ `Pasal 27A`).
3. **Manajemen Siklus Hidup Norma (Amandemen & Pencabutan)**:
   - **Simetri Graf**:
     - Jika dokumen baru `mengubah` dokumen lama: Dokumen lama otomatis ditandai `diubah_oleh: [ID_BARU]`, status menjadi `diubah`, dan tanggal diperbarui.
     - Jika dokumen baru `mencabut` dokumen lama: Dokumen lama otomatis ditandai `dicabut_oleh: [ID_BARU]`, status menjadi `dicabut`, dan disematkan callout bahaya `> [!CAUTION] PERATURAN INI TELAH DICABUT OLEH [[...]]`.
4. **Dual Output Generation (Hybrid)**:
   - **Mode Karpathy LLM-Wiki**:
     - `02_LEGISLATION/<KODE_UU>/Pasal_<NO>.md` (1 berkas mandiri per pasal, terjahit dengan penjelasannya).
     - `01_INDEX_MOC/_Index_<KODE_UU>.md` (Daftar ringkas pasal & inti ayat 1 untuk navigasi hemat token LLM).
   - **Mode UU-KB Native**:
     - `10-peraturan/<jenis-folder>/<JENIS> <NO>-<THN> - <JUDUL>.md` (1 berkas terpartisi dengan anchor unik `^pasal-X` dan `^penjelasan-pasal-X` sesuai kontrak `AGENTS.md`).
5. **Pembaruan MOC Kategori & Audit Log**:
   - Menambahkan dokumen baru ke tabel `40-kategori/<Bidang>.md`.
   - Mencatat ke log append-only `90-log/log.md`.

---

## Cara Eksekusi

Jalankan orchestrator menggunakan interpreter Python uv yang telah memiliki dependensi `docling`:

### 1. Ingest Satu File (PDF atau MD)
```powershell
& "C:\Users\ibrah\AppData\Roaming\uv\tools\docling\Scripts\python.exe" scripts/pipeline_orchestrator.py `
  --file "30-sumber/Nama_File_UU.pdf" `
  --mode both
```

### 2. Ingest Seluruh Direktori (Batch)
```powershell
& "C:\Users\ibrah\AppData\Roaming\uv\tools\docling\Scripts\python.exe" scripts/pipeline_orchestrator.py `
  --dir "30-sumber" `
  --mode both
```

### 3. Paksa Timpa (Force Overwrite Dokumen yang Sudah Ada)
```powershell
& "C:\Users\ibrah\AppData\Roaming\uv\tools\docling\Scripts\python.exe" scripts/pipeline_orchestrator.py `
  --file "30-sumber/Nama_File_UU.pdf" `
  --force `
  --mode both
```

---

## SOP Otomatisasi untuk Agent

Ketika pengguna meminta untuk memproses atau menambahkan dokumen hukum:

1. **Periksa Sumber**: Cek apakah berkas ada di `30-sumber/` atau path yang diberikan pengguna.
2. **Jalankan Pipeline Orchestrator**:
   Gunakan perintah PowerShell di atas dengan `run_command`.
3. **Review Hasil**:
   - Konfirmasi apakah dokumen baru berhasil diproses atau dilewati (skip).
   - Pastikan relasi `mengubah` atau `mencabut` telah merambat ke dokumen terkait.
4. **Update Chunks (Opsional)**:
   Bila pengguna menginginkan pembaruan database vektor RAG siap-embed, jalankan:
   ```powershell
   python 90-log/build_chunks.py
   ```
5. **Laporkan ke Pengguna**:
   Berikan ringkasan ringkas berisi ID dokumen, jumlah pasal yang diekstrak, status keberlakuan, dan tautan ke Map of Content atau berkas korpus.

