---
judul: "Aturan Pemeliharaan Korpus Hukum"
jenis: meta
tags: [meta]
last_updated: 2026-10-28
---

# AGENTS.md — Aturan Pemeliharaan Korpus Hukum

Vault ini adalah **basis pengetahuan hukum Indonesia untuk konsumsi AI**. Satu berkas = satu
peraturan/putusan. Fokus: teks otoritatif + metadata yang bisa dipercaya mesin. Bukan catatan kasus.

## Struktur wajib

```
10-peraturan/01-undang-undang/      UU
10-peraturan/02-perppu/             Perppu
10-peraturan/03-peraturan-pemerintah/  PP
10-peraturan/04-peraturan-presiden/ Perpres
10-peraturan/05-peraturan-menteri/  Permen/Permenkop/Kepmen/Instruksi Menteri
10-peraturan/06-peraturan-ojk/      POJK, SEOJK
10-peraturan/07-peraturan-bi/       PBI/PADG/SEBI
10-peraturan/08-peraturan-polri/    Perkap, Perpol, SE Kapolri
10-peraturan/09-instrumen-lain/     Inpres, SKB, Jukrah
20-putusan/01-mahkamah-konstitusi/  Putusan MK (uji materi)
20-putusan/02-pengadilan/           Putusan pengadilan lain
30-sumber/                          PDF/HTML asli (nama sama dengan halaman markdown)
40-kategori/                        MOC per bidang hukum (Dataview + daftar statis)
50-glosarium/                       Istilah + pasal sumber
90-log/                             log.md (append-only) + manifest JSONL
```

## Kontrak frontmatter (wajib, urutan bebas)

```yaml
id: "UU 4/2023"          # <JENIS> <nomor>/<tahun>; unik di seluruh vault
jenis: UU                # UU|PERPPU|PP|PERPRES|INPRES|PERMEN*|KEPMEN*|INSTRUKSI|POJK|SEOJK|PBI|PERKAP|SE-KAPOLRI|SKB|JUKRAH|PUTUSAN-MK
lembaga: "Undang-Undang"
nomor: 4
tahun: 2023
judul: "Pengembangan dan Penguatan Sektor Keuangan"
judul_singkat: "P2SK"
status: berlaku          # berlaku|diubah|dicabut|belum-berlaku|berlaku-sebagian|perlu-verifikasi
status_catatan: "..."    # hanya bila perlu penjelasan status
ditetapkan: 2023-01-12   # opsional, ISO
berlaku_mulai: 2023-01-12 # opsional, ISO
mencabut: []             # daftar id
dicabut_oleh: []         # daftar id
mengubah: []             # daftar id
diubah_oleh: []          # daftar id
terkait: []              # daftar id (rujukan/hubungan lain)
bidang: [keuangan]       # pidana|keuangan|siber|tipidter|pertanahan|umum
tags: [jenis/uu, bidang/keuangan, status/berlaku]
sumber: "https://peraturan.bpk.go.id/..."   # URL JDIH bila ada
kelengkapan: lengkap     # lengkap|sumber-pdf-saja
verifikasi: belum        # belum|sebagian|sudah  (verifikasi ke JDIH BPK)
last_updated: 2026-10-28
```

## Aturan isi

1. **Teks otoritatif dulu.** Jangan menambah ringkasan/tafsiran sebelum teks pasal ada. Bila menulis
   ringkasan, letakkan di bagian `## Ringkasan` dan tandai jelas sebagai ringkasan (bukan kutipan).
2. **Jangan mengarang.** Nomor/tahun/judul/status harus berasal dari dokumen atau JDIH BPK. Bila ragu:
   `status: perlu-verifikasi`, `verifikasi: belum`, dan tulis alasannya di `status_catatan`.
3. **Relasi graf harus simetris.** Bila A `mengubah` B, maka B `diubah_oleh` A. Bila A `mencabut` B,
   maka B `dicabut_oleh` A dan `status: dicabut`.
4. **Nama berkas** = `<JENIS> <nomor>-<tahun> - <judul singkat>.md` (judul singkat ≤ 52 karakter,
   tanpa `/ : * ? " < > |`). Wikilink memakai nama berkas tanpa `.md`.
5. **Sumber PDF** disimpan di `30-sumber/` dengan nama sama (beda ekstensi) dan dirujuk dari `sumber:`.
6. **Berkas stub** (`kelengkapan: sumber-pdf-saja`) hanya boleh diisi setelah ekstraksi teks; jangan
   dibiarkan seolah lengkap.
7. **Tanpa data perkara.** Nama tersangka/saksi, nomor LP, mutasi rekening, hasil OSINT tidak masuk vault.

## Alur kerja

- **INGEST**: ekstrak teks → normalisasi frontmatter di atas → simpan PDF ke `30-sumber/` → perbarui
  `40-kategori/` dan `INDEX.md` → tambah entri di `90-log/log.md` → commit.
- **QUERY**: baca `INDEX.md` → `40-kategori/<bidang>.md` → halaman peraturan → kutip dengan `[[id]]` + pasal.
- **LINT**: cek id duplikat, link mati, relasi asimetris, `status` kosong, stub menua, frontmatter rusak,
  dan `last_updated` usang. Laporkan sebelum mengubah.
- **VERIFIKASI STATUS**: cocokkan `status` ke JDIH BPK; setelah dicek ubah `verifikasi: sudah`.

## Sinkronisasi

Vault ini git repo (`origin` → repo private terpisah dari vault kerja). Setiap operasi yang mengubah
isi wajib diakhiri commit + push. Plugin Obsidian Git menjalankan auto commit/pull sebagai jaring pengaman.
