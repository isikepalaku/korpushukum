---
title: "Template Kasus"
aliases: [Template Lidik]
tags: [template, kasus, lidik]
type: template
---

# Template Halaman Kasus (wiki/kasus/)

> Salin file ini untuk tiap kasus baru. Isi semua seksi; hapus yang tidak relevan. Frontmatter WAJIB.

```markdown
---
title: "Kasus: <nama/subjek>"
aliases: [<nama pendek>]
tags: [kasus, lidik, <domain>]
type: kasus
source: "<sumber OSINT/dokumen>"
last_updated: <YYYY-MM-DD>
related: ["<entitas/konsep terkait>", ...]
status: "Lidik OSINT awal / Menunggu verifikasi / Lidik aktif"
---

# Kasus: <nama/subjek>

## Ringkasan
<1-3 kalimat: apa targetnya, penilaian awal, status verifikasi. Ingat: terdaftar = presumsi sah; jangan vonis.>

## Profil
- <Identitas: badan hukum, izin, lokasi, produk, kontak>

## Sinyal positif (legitimasi)
- ✅ <terdaftar, izin ada, operasi aktif, RAT, dll.>

## Gap izin & titik verifikasi
1. <gap izin #1 — KEMENKOP/OJK/BI>
2. <closed vs open loop>
3. <titik risiko operasional>

## Laporan/dugaan (dengan penilaian kredibilitas)
| Sumber | Klaim | Penilaian |
|---|---|---|
| <sumber> | <klaim> | <kredibel? verifikasi?> |

## Konstruksi hukum (tentatif — verification-first)
| Temuan (jika terbukti) | Pasal | Ancaman pasca UU 1/2026 |
|---|---|---|
| <temuan> | <pasal lex specialis> | <ancaman> |

## Langkah verifikasi (checklist)
1. <verifikasi izin>
2. <uji beli / uji registrasi app>
3. <closed/open loop>
4. <follow the money>

## Status
<...>

## Terkait
- [[<entitas>]] · [[<konsep>]]
```

## Aturan
- **Verifikasi dulu, jangan vonis.** Status selalu mencantumkan tahap lidik.
- Ancaman pidana → versi **pasca UU 1/2026** + asas **lex specialis**.
- Setiap ingest: update `wiki/index.md` (baris kasus) + `wiki/log.md` (entry `## [YYYY-MM-DD] ingest | <kasus>`).
