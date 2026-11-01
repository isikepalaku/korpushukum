---
name: legal-corpus-pipeline
description: Automates the ingestion, parsing, deduplication, categorization, lifecycle management (marking amendments/repeals), and OpenViking incremental embedding of Indonesian legal documents (UU, PP, Perpres, Permen, POJK, etc.) into Obsidian Karpathy LLM-Wiki and UU-KB corpus using Docling.
metadata:
  tags: [hukum, docling, obsidian, parser, uukb, rag, openviking, karpathy-wiki]
  category: legal-engineering
  role: legal-pipeline-engineer
---

# Legal Corpus Pipeline Skill

Skill otomatisasi untuk memproses dokumen hukum resmi Indonesia (Undang-Undang, Perppu, PP, Perpres, Permen, POJK, Putusan MK) ke dalam **Obsidian Vault (UU-KB)**, **Karpathy LLM-Wiki**, dan lapisan embedding inkremental **OpenViking**.

---

## 1. Arsitektur Dua Vault & Batasan Ketat

- **`E:\Agent\UU-KB` (`korpushukum`)**: Basis pengetahuan hukum otoritatif bersih (teks regulasi resmi, MOC, pasal atomik, chunks vektor).
  > [!IMPORTANT]
  > **Bebas dari data perkara, nama tersangka/saksi, nomor LP, mutasi rekening, atau rahasia penyidikan** (Sesuai `AGENTS.md` Aturan 7).
- **`E:\Agent\UU` (`vault hukum`)**: Ruang kerja penyidikan (kasus aktif, telaahan hukum fismondev, mindik, resume BAP). Merujuk norma hukum resmi via wikilink `[[UU ...#^pasal-X]]` ke `korpushukum`.
- **`OpenViking` (`127.0.0.1:1933`)**: Mesin recall memori cerdas yang meng-embed chunks hukum secara inkremental dari `90-log/manifest.jsonl` dan `90-log/chunks.jsonl.gz`.

---

## 2. Kapabilitas Utama

1. **Deduplikasi Cerdas (Sub-Second Pre-Check)**:
   - Memeriksa apakah ID dokumen (misal `UU 1/2024`) sudah ada di dalam korpus sebelum menjalankan Docling OCR.
   - Melewati berkas yang identik secara instan (`--skip`), atau menimpa jika diminta pengguna (`--force`).
2. **Ekstraksi Deterministik Docling + Regex**:
   - Mengekstrak tata letak PDF menjadi Markdown bersih menggunakan GPU-accelerated Docling (`RapidOCR`).
   - Memisahkan **Batang Tubuh** dan **Penjelasan Resmi** di lampiran belakang.
   - Menjahit (*stitch*) Batang Tubuh dan Penjelasan per pasal tanpa token LLM.
   - Mempertahankan penomoran pasal amandemen (seperti `Pasal 27A`, `Pasal 27B`, `Pasal 45B`, `Pasal 39D`) dan ayat turunan (`(2a)`, `(2b)`).
   - Mengoreksi kesalahan tipikal OCR hukum Indonesia (`Pasal 278` $\to$ `27B`, `Pasal 168` $\to$ `16B`, `Pasal2TA` $\to$ `27A`, `il. PASAL` $\to$ `II. PASAL`, `PASALDEMIPASAL` $\to$ `PASAL DEMI PASAL`).
3. **Manajemen Siklus Hidup Norma (Graf Simetris)**:
   - Jika dokumen baru `mengubah` dokumen lama: Dokumen lama otomatis ditandai `diubah_oleh: [ID_BARU]`, status menjadi `diubah`.
   - Jika dokumen baru `mencabut` dokumen lama: Dokumen lama otomatis ditandai `dicabut_oleh: [ID_BARU]`, status menjadi `dicabut`, dan disematkan callout bahaya `> [!CAUTION] PERATURAN INI TELAH DICABUT OLEH [[...]]`.
4. **Dual Output Generation (Hybrid)**:
   - **Mode Karpathy LLM-Wiki**:
     - `02_LEGISLATION/<KODE_UU>/Pasal_<NO>.md` (1 berkas per pasal terjahit dengan penjelasannya).
     - `01_INDEX_MOC/_Index_<KODE_UU>.md` (Daftar ringkas pasal & inti ayat 1).
     - `01_INDEX_MOC/_MASTER_INDEX.md` (Peta hierarkis seluruh peraturan untuk retrieval 2-tahap).
   - **Mode UU-KB Native**:
     - `10-peraturan/<subfolder>/<JENIS> <NO>-<TAHUN> - <JUDUL SINGKAT>.md` (1 berkas terpartisi dengan anchor unik `^pasal-X` dan `^penjelasan-pasal-X` sesuai kontrak `AGENTS.md`).
5. **OpenViking Incremental Loader**:
   - Hanya meng-embed dokumen/chunk yang mengalami perubahan hash SHA256 (`90-log/openviking_state.json`).
   - Otomatis memfilter penjelasan non-substantif (*"Cukup jelas."*) agar hemat kuota token embedding.

---

## 3. Hierarki Direktori Resmi (`10-peraturan/` & `20-putusan/`)

| Jenis Instrumen | Subfolder Tujuan | Contoh Format Nama File (`.md`) |
|---|---|---|
| **Undang-Undang** | `10-peraturan/01-undang-undang/` | `UU 4-2023 - P2SK.md` |
| **Perppu** | `10-peraturan/02-perppu/` | `Perppu 2-2022 - Cipta Kerja.md` |
| **Peraturan Pemerintah** | `10-peraturan/03-peraturan-pemerintah/` | `PP 7-2021 - Kemudahan dan Perlindungan Koperasi.md` |
| **Peraturan Presiden** | `10-peraturan/04-peraturan-presiden/` | `Perpres 96-2018 - Pendaftaran Penduduk.md` |
| **Peraturan Menteri** | `10-peraturan/05-peraturan-menteri/` | `Permenkop 8-2023 - Usaha Simpan Pinjam Koperasi.md` |
| **POJK & SEOJK** | `10-peraturan/06-peraturan-ojk/` | `POJK 11-2022 - Penyelenggaraan TI Bank Umum.md` |
| **Peraturan Bank Indonesia** | `10-peraturan/07-peraturan-bi/` | `PBI 23-2021 - Sistem Pembayaran.md` |
| **Peraturan Polri** | `10-peraturan/08-peraturan-polri/` | `Perpol 8-2021 - Penanganan Tindak Pidana RJ.md` |
| **Instrumen Lain (Inpres/Jukrah)** | `10-peraturan/09-instrumen-lain/` | `Inpres 18-1998 - Peningkatan Pembinaan Perkoperasian.md` |
| **Putusan Mahkamah Konstitusi** | `20-putusan/01-mahkamah-konstitusi/` | `Putusan MK 282-2025 - Penghinaan Pemerintah.md` |
| **Putusan Pengadilan Lain** | `20-putusan/02-pengadilan/` | `Putusan PN Makassar ... .md` |
| **Sumber PDF Asli** | `30-sumber/` | Nama persis sama dengan halaman markdown (ekstensi `.pdf`) |

> [!NOTE]
> **Dokumen Non-Pasal (Struktur Datar):**
> Dokumen seperti Inpres, Kepmen, Instruksi Menteri, Surat Edaran (SEOJK), dan Putusan MK yang tidak menggunakan sistem penomoran "Pasal 1, Pasal 2" wajib menggunakan frontmatter:
> `struktur_teks: datar`, `penjelasan: tidak`, `anchor_pasal: false`, `penjelasan_pasal_demi_pasal: false`.

---

## 4. Daftar Skrip di `scripts/`

- **`scripts/ingest_interactive.py`**: CLI all-in-one dengan auto-detection metadata, ekstraksi Docling, pembaruan manifest, chunking, sync OpenViking, dan opsi auto-commit.
- **`scripts/docling_legal_parser.py`**: Engine ekstraksi deterministik Docling RapidOCR, splitter Batang Tubuh vs Penjelasan, dan stitching ayat.
- **`scripts/pipeline_orchestrator.py`**: Orchestrator batch/single dengan sub-second pre-check dan sinkronisasi graf siklus hidup.
- **`scripts/build_manifest.py`**: Membangun `90-log/manifest.jsonl` lengkap dengan section offsets dan SHA256 hashes.
- **`90-log/build_chunks.py`**: Membangun `90-log/chunks.jsonl.gz` dan `40-kategori/Indeks Penjelasan.md`.
- **`scripts/openviking_ingest.py`**: Loader inkremental untuk OpenViking / Hermes Vector DB (`--check`, `--sync`, `--force`).
- **`scripts/batch_export_karpathy.py`**: Batch generator untuk seluruh folder `02_LEGISLATION/` dan `01_INDEX_MOC/`.

---

## 5. Cara Eksekusi

### 1. Ingest All-in-One (Disarankan untuk Operasional)
```powershell
python scripts/ingest_interactive.py --file "30-sumber/Nama_File.pdf" --auto-commit
```

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

## 6. Template Prompt AI Agent untuk PC
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
