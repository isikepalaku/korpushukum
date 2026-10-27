---
name: kutipan-hadis
description: Cari dan kutip hadis Rasulullah SAW via Hadith API.
version: 0.1.0
author: Ibrahim Sandre (isikepalaku), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hadith, islam, sunnah, kutipan, hadis]
    related_skills: [grounded-citations]
---

# Kutipan Hadis Rasulullah SAW Skill

Skill untuk mencari, mengambil, memverifikasi, dan mengutip sabda Rasulullah SAW dari sumber primer kitab-kitab hadis mu'tabar menggunakan database `fawazahmed0/hadith-api`. Menyediakan matan berbahasa Arab lengkap dengan harakat, terjemahan resmi bahasa Indonesia, rujukan bab, dan derajat/penilaian keshahihan hadis (takhrij/grading).

## When to Use

- Pengguna meminta kutipan hadis Rasulullah SAW (misal: hadis tentang niat, sedekah, amanah, kejujuran, penipuan, dll.).
- Pengguna meminta hadis spesifik berdasarkan nama perawi dan nomor (misal: HR. Bukhari No. 1, HR. Muslim No. 55).
- Pengguna meminta hadis acak untuk renungan/nasihat harian.
- Dibutuhkan teks Arab asli beserta terjemahan terpercaya dan status takhrij (Sahih, Hasan, dll.).

**Don't use for:**
- Tafsir Al-Qur'an (gunakan sumber tafsir kanonik).
- Fatwa fikih kontemporer kompleks tanpa dalil hadis spesifik.

## Prerequisites

- Python 3.8+ (tersedia bawaan di server).
- CLI `hadith` tersedia di `~/.local/bin/hadith` atau langsung dieksekusi via `python3 ~/.hermes/skills/research/kutipan-hadis/scripts/hadith.py`.
- Akses internet ke CDN jsdelivr / GitHub raw untuk unduhan pertama (data otomatis di-cache di `~/.cache/hadith-api/`).

## How to Run

Jalankan via Hermes tool `terminal`:

```bash
# 1. Mengambil hadis spesifik (Arab + Terjemahan Indonesia + Derajat)
terminal(command="hadith get bukhari 1")

# 2. Mencari hadis berdasarkan kata kunci
terminal(command="hadith search 'jujur' --limit 3")

# 3. Mengambil hadis acak
terminal(command="hadith random bukhari")

# 4. Melihat daftar kitab yang didukung
terminal(command="hadith books")
```

## Quick Reference

| Perintah | Deskripsi |
|---|---|
| `hadith get <kitab> <nomor>` | Ambil hadis nomor tertentu (matan Arab, terjemahan, derajat) |
| `hadith search "<kata_kunci>"` | Cari teks hadis di semua kitab terjemahan Indonesia |
| `hadith search "<kata_kunci>" --books bukhari,muslim` | Cari terbatas pada Shahih Bukhari & Shahih Muslim |
| `hadith search "<kata_kunci>" --limit 5 --full` | Cari dan tampilkan teks Arab lengkap |
| `hadith random [kitab]` | Ambil satu hadis acak dari kitab tertentu |
| `hadith books` | Tampilkan 10 kitab yang didukung beserta jumlah hadis |

### Daftar Kitab & Cakupan

- `bukhari` : Sahih al-Bukhari (7.563 hadis) — Arab & Indonesia
- `muslim` : Sahih Muslim (7.563 hadis) — Arab & Indonesia
- `abudawud` : Sunan Abu Dawud (5.274 hadis) — Arab & Indonesia (disertai takhrij Al-Albani dkk.)
- `tirmidhi` : Jami' at-Tirmidhi (3.956 hadis) — Arab & Indonesia (disertai takhrij Al-Albani dkk.)
- `nasai` : Sunan an-Nasa'i (5.758 hadis) — Arab & Indonesia (disertai takhrij)
- `ibnmajah` : Sunan Ibn Majah (4.341 hadis) — Arab & Indonesia (disertai takhrij)
- `malik` : Muwatta Malik (1.858 hadis) — Arab & Indonesia
- `nawawi` : Arba'in an-Nawawi (42 hadis) — Arab & Inggris
- `qudsi` : Hadits Qudsi (40 hadis) — Arab & Inggris
- `dehlawi` : Arba'in Syah Waliullah (40 hadis) — Arab & Inggris

## Format Standar Kutipan Hadis (Telegram)

Sajikan kutipan hadis kepada pengguna secara tertib, khidmat, dan terverifikasi:

1. **Identitas Perawi & Nomor:**  
   `**HR. [Nama Kitab] No. [Nomor]** *(Bab: [Nama Bab/Kitab])*`
2. **Matan Teks Arab:**  
   Tampilkan teks Arab berharakat di dalam code block ```text ... ``` agar rapi dan mudah dibaca di Telegram.
3. **Terjemahan Bahasa Indonesia:**  
   Tampilkan terjemahan lengkap dengan tanda kutip atau blockquote `> ...`.
4. **Derajat / Keshahihan (Takhrij):**  
   Tuliskan status hadis (misal: *Sahih (HR. Bukhari)* atau *Sahih menurut Syaikh Al-Albani*).
5. **Faedah / Konteks Singkat (Opsional):**  
   1–2 kalimat hikmah relevan jika diminta atau mendukung topik perbincangan.

## Procedure

1. **Identifikasi Permintaan:**
   Tentukan apakah pengguna mencari topik umum (misal: sedekah), perawi tertentu, atau nomor hadis spesifik.
2. **Pencarian / Pengambilan:**
   - Bila nomor diketahui: jalankan `terminal(command="hadith get <kitab> <nomor>")`.
   - Bila berdasarkan topik: jalankan `terminal(command="hadith search '<kata_kunci>' --limit 3")`, pilih hadis yang paling pas, lalu ambil versi lengkapnya.
3. **Verifikasi Keshahihan:**
   Periksa field derajat/grades. Utamakan hadis berderajat Sahih atau Hasan.
4. **Sajikan Jawaban:**
   Tampilkan sesuai **Format Standar Kutipan Hadis** di atas tanpa memotong makna matan.

## Pitfalls

- **Perbedaan Penomoran Hadis:** Penomoran hadis di API mengikuti penomoran standar internasional (Fathul Bari untuk Bukhari, Syarah Muslim untuk Muslim). Bila nomor rujukan pengguna berbeda cetakan, gunakan `hadith search` dengan frasa kunci dari matan.
- **Hadits Nawawi/Qudsi:** Hanya memiliki terjemahan Inggris di repositori asli. Saat mengutip hadis Arba'in, sertakan teks Arab dan terjemahkan matannya ke bahasa Indonesia yang fasih.
- **Cache Pertama:** Panggilan pencarian pertama akan mengunduh file JSON kitab (~4-6 MB per kitab). Proses ini hanya berlangsung 1 kali karena otomatis tersimpan di `~/.cache/hadith-api/`.

## Verification

Jalankan pengujian cepat untuk memastikan alat bekerja:
```bash
hadith get bukhari 1
hadith search "niat" --books bukhari --limit 1
```
Output harus menyajikan matan Arab `إِنَّمَا الْأَعْمَالُ بِالنِّيَّاتِ...`, terjemahan, dan rujukan Sahih al-Bukhari No. 1.
