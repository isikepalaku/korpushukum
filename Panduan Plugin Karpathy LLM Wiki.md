---
title: "Panduan Plugin Karpathy LLM Wiki"
aliases: [Panduan Plugin, llm-wiki plugin, karpathywiki]
tags: [plugin, obsidian, schema, konfigurasi]
type: dokumentasi
source: "catatan otomatis plugin + pengalaman pemasangan di vault ini"
last_updated: 2026-09-14
related: ["AGENTS.md", "INDEX"]
---

# Panduan Plugin Karpathy LLM Wiki (Obsidian)

Halaman ini menggantikan catatan otomatis berbahasa Inggris *"Welcome to Karpathy LLM Wiki"* yang dibuat plugin pada saat pemasangan. Isi teknisnya dipertahankan, diterjemahkan, dan disesuaikan dengan konvensi vault ini.

> **Catatan penting:** di server Linux (`~/penyidikan/`) plugin ini **tidak** dijalankan. Server memakai Hermes yang membaca/menulis berkas secara langsung. Plugin hanya hidup di komputer utama (Windows, `E:/Agent/UU`) yang punya Obsidian.

## Mengaktifkan LLM di plugin (komputer utama)

Catatan otomatis lama menandai `llm_config_status: failed` — artinya LLM plugin belum dikonfigurasi saat itu. Langkah aktivasi:

1. **Settings → Karpathy LLM Wiki → LLM Provider**
2. Pilih provider, isi API key, pilih model
3. **Test Connection** — harus ✅ sebelum lanjut
4. **Save Settings**, lalu jalankan perintah `Karpathy LLM Wiki: Recreate Wiki Welcome Note` bila ingin catatan bawaan dibuat ulang

## Perintah plugin (Ctrl/Cmd + P → cari "Karpathy LLM Wiki")

- `Ingest multiple files` — pilih N catatan sumber; plugin mengekstraksi entitas/konsep dan menulis halaman wiki.
- `Ingest single source` — sama, untuk satu berkas.
- `Ingest from folder` — menelan seluruh isi folder.
- `Query Wiki` — panel chat kanan untuk bertanya terhadap isi wiki.
- `Lint wiki` — pipeline lint (tautan mati, orphan, duplikat).
- `View Ingestion History` — daftar hasil tiap ingest.
- `Recreate Wiki Welcome Note` — membuat ulang catatan bawaan.

## Struktur yang ditulis plugin vs konvensi vault ini

Plugin menyimpan semua di bawah `wiki/` dengan nama Inggris; vault ini memakai penamaan Indonesia. **Penamaan vault yang berlaku.**

- `entities/` → vault: **`entitas/`**
- `concepts/` → vault: **`konsep/`**
- `sources/` → vault: tidak dipakai sebagai folder tersendiri; sumber mentah tinggal di `Hukum Pidana/` dan `Hukum Keuangan/` (lapisan RAW), sedangkan sintesis disimpan di **`kasus/`**
- `schema/` → vault: **`AGENTS.md`** (schema berbasis berkas, bukan folder)
- `index.md`, `log.md` → sama, dipertahankan

### Lapisan Schema

Bila Schema diaktifkan (Settings → Karpathy LLM Wiki → Schema), plugin memelihara `wiki/schema/` berisi kosakata terkontrol (kategori tag, template seksi, tipe entitas/konsep). Ingest lalu terikat pada kosakata itu sehingga tag tidak mengarang bebas; usulan kosakata baru muncul di laporan Lint untuk disetujui/ditolak; perubahan kosakata menulis ulang halaman terkait dengan cadangan di `.llm-wiki-backups/schema/`. Di vault ini schema sudah dikelola manual melalui `AGENTS.md`, jadi Schema plugin **sebaiknya tidak diaktifkan bersamaan** agar tidak ada dua sumber aturan.

### Graf wikilink

Setiap `[[wikilink]]` adalah relasi yang ditetapkan saat ingest. Plugin memakai graf ini (bukan embedding) untuk retrieval query — sehingga graf wikilink yang terawat **adalah** indeks pencariannya. Menambah/mengedit tautan secara manual langsung berpengaruh pada query berikutnya.

## Risiko yang harus dijaga

| Risiko | Konsekuensi | Tindakan |
|---|---|---|
| Auto Maintenance plugin menulis `index.md`/`log.md` | Menimpa katalog hasil kurasi manual (mis. entry log terselip di luar urutan kronologis) | Matikan auto maintenance di mesin Windows, atau periksa diff sebelum commit |
| Dua "penulis" aktif (plugin di Windows + agent di server) | Konflik git pada halaman yang sama | Satu halaman = satu penulis; pull sebelum kerja |
| Ingest plugin di mesin yang salah | Halaman penamaan Inggris masuk `wiki/` | Ingest plugin hanya di Windows, tetap pakai `entitas/konsep/kasus` |

## Terkait

- `AGENTS.md` — schema utama vault
- `INDEX.md` — MOC dokumen sumber
- Panduan plugin: `github.com/green-dalii/obsidian-llm-wiki`
