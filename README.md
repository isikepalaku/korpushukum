---
judul: "Korpus Hukum Indonesia — README"
jenis: meta
tags: [meta]
last_updated: 2026-11-03
---

# Korpus Hukum Indonesia (UU-KB)

Basis pengetahuan peraturan Indonesia yang disiapkan sebagai **feed AI**: satu berkas per peraturan,
frontmatter seragam, relasi antar-peraturan eksplisit, dan pemisahan tegas dari data perkara.

**Isi saat ini:** 133 dokumen — 119 peraturan
dan 14 putusan MK.

## Mulai dari mana

| Kebutuhan | Buka |
| --- | --- |
| Katalog lengkap | [[INDEX]] |
| Per bidang hukum | [[Pidana]], [[Keuangan]], [[Siber]], [[Tipidter]] |
| Istilah & definisi | [[Glosarium]] |
| Aturan pemeliharaan | `AGENTS.md` |
| Riwayat perubahan | `90-log/log.md` |

## Mengutip & menautkan (pola baku)

```markdown
Norma:        [[UU 4-2023 - P2SK#^pasal-44]]
Penjelasan:   [[UU 4-2023 - P2SK#^penjelasan-pasal-44]]
Kutip utuh:   ![[UU 4-2023 - P2SK#^penjelasan-pasal-44]]
```

Penjelasan resmi tinggal di halaman induknya (satu sumber kebenaran) — catatan analisis cukup
menjadi transklusi. Dengan begitu: teks tidak terduplikasi, perubahan penjelasan ikut terbaca di semua
tempat, dan chunk RAG tetap punya `anchor` unik.

## Untuk pipeline AI

- `90-log/manifest.jsonl` — satu baris per dokumen: `id`, `jenis`, `nomor`, `tahun`, `judul`, `status`,
  `bidang[]`, `relasi{}`, `file`, `kelengkapan`, `chars`, `sha256` teks. Pakai untuk incremental embedding.
- `90-log/chunks.jsonl.gz` — **26.116 chunk** siap embed (rata-rata 842 char, maks 2.504). Pisah
  `batang-tubuh` (7.607) / `penjelasan-umum` (1.661) / `penjelasan-pasal` (6.576) / `isi` (10.261) /
  `penjelasan` (11). Regenerasi: `python 90-log/build_chunks.py`.
- Penjelasan "Cukup jelas" ditandai `substantive: false` (2.660 chunk) supaya tidak mengotori retrieval,
  sedangkan penjelasan berkonten substantif berjumlah 3.916 chunk.
- `01-moc/Indeks Penjelasan.md` — dokumen mana yang penjelasannya substantif vs formalitas.
- Teks pasal ada di badan markdown (di bawah H1). Frontmatter YAML = metadata yang sudah bersih.
- Dokumen `kelengkapan: sumber-pdf-saja` **belum punya teks** — jangan di-embed sebelum diekstrak.

## Struktur

```
01-moc/          MOC per regulasi & MOC per bidang hukum
02-pasal-atomik/ pasal atomik terjahit batang tubuh + penjelasan
10-peraturan/    peraturan perundang-undangan (per jenis, hierarki UU 12/2011)
20-putusan/      putusan MK & pengadilan
30-sumber/       PDF/HTML asli
50-glosarium/    istilah + pasal sumber
90-log/          log.md, manifest.jsonl
```

## Batasan yang jujur

- Status keberlakuan: `verifikasi: belum` = belum dicek ulang ke JDIH BPK. Jangan dikutip sebagai
  kepastian hukum tanpa verifikasi.
- Relasi antar-peraturan diambil dari judul resmi ("Perubahan ... atas ...") + kurasi manual; rantai
  perubahan panjang bisa belum lengkap.
