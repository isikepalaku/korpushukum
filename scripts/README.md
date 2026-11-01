# Indonesian Legal Docling Parser (UU-KB & Karpathy LLM-Wiki)

Modul Python mandiri, deterministik, dan bebas token LLM untuk mengekstrak PDF perundang-undangan Indonesia menggunakan **Docling** dan memecahnya menjadi berkas Markdown atomik untuk Obsidian Vault / LLM Knowledge Base.

---

## 🚀 Fitur Utama

1. **Konversi PDF Terstruktur**: Memanfaatkan `docling` untuk mengekstrak teks, tabel, dan hirarki dokumen tanpa kehilangan struktur ayat dan pasal.
2. **Deterministic Regex Splitter (0 Token LLM)**:
   - Memisahkan bagian **Batang Tubuh** (Konsiderans, Bab, Pasal, Ayat) dari bagian **Penjelasan Resmi** di lampiran belakang.
   - Memisahkan Penjelasan **I. UMUM** dan **II. PASAL DEMI PASAL**.
3. **Legal OCR Error Repair Engine**:
   - Memperbaiki kesalahan umum OCR pada dokumen hukum Indonesia (misal: `Pasil` $\to$ `Pasal`, `Pasal2TA` $\to$ `Pasal 27A`, `Pasal 278` $\to$ `Pasal 27B`, `Pasal 168` $\to$ `Pasal 16B`).
4. **Stitching Batang Tubuh & Penjelasan**:
   - Menjahit teks penjelasan resmi langsung ke dalam pasal terkait.
   - Menandai secara otomatis apakah penjelasan bersifat substantif atau *"Cukup jelas"*.
5. **Dukungan Dual-Mode Output (Hybrid)**:
   - **Mode `atomic` (Karpathy LLM-Wiki)**:
     - Output: `02_LEGISLATION/<KODE_UU>/Pasal_<NO>.md`
     - Indeks ringkas (Map of Content): `01_INDEX_MOC/_Index_<KODE_UU>.md` untuk pencarian hemat token oleh LLM.
   - **Mode `uukb` (Korpus Obsidian UU-KB)**:
     - Output: `10-peraturan/01-undang-undang/<JENIS> <NO>-<TAHUN> - <JUDUL>.md`
     - Dilengkapi frontmatter YAML standar `AGENTS.md` serta heading dengan anchor unik (`^pasal-X` dan `^penjelasan-pasal-X`).
   - **Mode `both` (Default)**: Menghasilkan kedua format sekaligus.

---

## 📦 Persyaratan & Instalasi

### Menggunakan Python Virtual Environment Lokal
```bash
pip install -r requirements.txt
```

### Menggunakan Lingkungan uv Docling yang Sudah Ada di Sistem
Pada sistem Anda, Docling telah tersedia di:
```powershell
& "C:\Users\ibrah\AppData\Roaming\uv\tools\docling\Scripts\python.exe" scripts/docling_legal_parser.py --help
```

---

## 🛠️ Panduan Penggunaan CLI

### 1. Eksekusi dari File PDF Asli
```powershell
python scripts/docling_legal_parser.py `
  --pdf "30-sumber/UU 1-2024 - ITE Perubahan Kedua.pdf" `
  --code "UU_1_2024" `
  --name "Undang-Undang Nomor 1 Tahun 2024 tentang Perubahan Kedua UU ITE" `
  --short-name "ITE Perubahan Kedua" `
  --nomor 1 `
  --tahun 2024 `
  --bidang "siber" `
  --mode both
```

### 2. Eksekusi dari File Markdown yang Sudah Diekstrak
```powershell
python scripts/docling_legal_parser.py `
  --md "10-peraturan/01-undang-undang/UU 1-2024 - ITE Perubahan Kedua.md" `
  --code "UU_1_2024" `
  --name "Perubahan Kedua atas Undang-Undang Nomor 11 Tahun 2008 tentang ITE" `
  --mode atomic `
  --out "."
```

---

## 📂 Struktur Output Mode Atomic (`--mode atomic`)

```text
Obsidian_Vault/
├── 01_INDEX_MOC/
│   └── _Index_UU_1_2024.md         <-- Ringkasan 1 baris per pasal (sangat hemat token LLM)
└── 02_LEGISLATION/
    └── UU_1_2024/
        ├── Pasal_5.md              <-- Batang Tubuh + Penjelasan Resmi dijahit
        ├── Pasal_27.md
        ├── Pasal_27A.md
        ├── Pasal_27B.md
        └── ...
```

Format tiap berkas `Pasal_<NO>.md`:
```markdown
---
id: UU_1_2024_Pasal_27A
uu_induk: Perubahan Kedua atas UU Informasi dan Transaksi Elektronik
kode_uu: UU_1_2024
pasal: 27A
status: BERLAKU_AKTIF
substantive_explanation: false
tags:
  - hukum/siber
  - uu/uu_1_2024
---

# Pasal 27A — Perubahan Kedua atas UU Informasi dan Transaksi Elektronik

## Batang Tubuh
Setiap Orang dengan sengaja menyerang kehormatan atau nama baik orang lain...

## Penjelasan Resmi
Cukup jelas.
```

