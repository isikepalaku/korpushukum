---
judul: "Korpus Hukum Indonesia — README"
jenis: meta
tags: [meta]
last_updated: 2026-10-28
---

# Korpus Hukum Indonesia (UU-KB)

Basis pengetahuan peraturan Indonesia yang disiapkan sebagai **feed AI**: satu berkas per peraturan,
frontmatter seragam, relasi antar-peraturan eksplisit, dan pemisahan tegas dari data perkara.

**Isi saat ini:** 127 dokumen — 113 peraturan
dan 14 putusan MK.

## Mulai dari mana

| Kebutuhan | Buka |
| --- | --- |
| Katalog lengkap | [[INDEX]] |
| Per bidang hukum | [[Pidana]], [[Keuangan]], [[Siber]], [[Tipidter]] |
| Istilah & definisi | [[Glosarium]] |
| Aturan pemeliharaan | `AGENTS.md` |
| Riwayat perubahan | `90-log/log.md` |

## Untuk pipeline AI

- `90-log/manifest.jsonl` — satu baris per dokumen: `id`, `jenis`, `nomor`, `tahun`, `judul`, `status`,
  `bidang[]`, `relasi{}`, `file`, `kelengkapan`, `chars`, `sha256` teks. Pakai untuk incremental embedding.
- Teks pasal ada di badan markdown (di bawah H1). Frontmatter YAML = metadata yang sudah bersih.
- Dokumen `kelengkapan: sumber-pdf-saja` **belum punya teks** — jangan di-embed sebelum diekstrak.

## Struktur

```
10-peraturan/    peraturan perundang-undangan (per jenis, hierarki UU 12/2011)
20-putusan/      putusan MK & pengadilan
30-sumber/       PDF/HTML asli
40-kategori/     MOC per bidang hukum
50-glosarium/    istilah + pasal sumber
90-log/          log.md, manifest.jsonl
```

## Batasan yang jujur

- Status keberlakuan: `verifikasi: belum` = belum dicek ulang ke JDIH BPK. Jangan dikutip sebagai
  kepastian hukum tanpa verifikasi.
- Relasi antar-peraturan diambil dari judul resmi ("Perubahan ... atas ...") + kurasi manual; rantai
  perubahan panjang bisa belum lengkap.
