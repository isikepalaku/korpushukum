---
name: tiktok-watch
description: "Use when collecting public TikTok OSINT leads."
version: 1.0.0
author: Tim Fismondev Ditreskrimsus Polda Sulsel
license: Internal Polri
platforms: [linux, macos]
category: penyidikan
tags: [tiktok, osint, lidik, jasa-keuangan, leads]
---

# Skill: TikTok Watch (koleksi lead OSINT publik)

Membungkus `~/penyidikan/tools/tiktok-watch/`: kolektor ber-volume rendah atas konten TikTok **publik** untuk indikasi kejahatan sektor jasa keuangan. Output adalah **petunjuk OSINT, bukan alat bukti**.

## Kapan Digunakan

- Perlu memantau kata kunci lidik (pinjol, investasi, kerja paruh waktu, lelang) untuk menemukan indikasi awal.
- Perlu lead untuk diverifikasi lewat sumber primer sebelum tindakan prosedural.

## Batas Penggunaan (wajib dipatuhi)

- Hanya konten **publik**, volume rendah: maksimum **30 video per kata kunci**.
- **Jangan** memasukkan cookie, nomor rekening, nomor telepon, atau data korban ke Git.
- Jangan menghapus konten sumber; dokumentasikan URL, waktu akses, dan metode akuisisi lebih dulu.
- Setiap lead wajib diverifikasi lewat sumber primer/pemeriksaan/permintaan data yang sah.

## Lingkungan (sudah siap di server ini)

- venv: `~/venvs/tiktok-watch` (berisi `TikTokApi` + Playwright; chromium sudah terpasang).
- Token `msToken` hanya lewat variabel sesi: `export TIKTOK_MS_TOKEN='...'`. **Jangan** tempel ke chat, berkas, riwayat shell, atau Git.

## Menjalankan

```bash
cd ~/penyidikan/tools/tiktok-watch

# cek kata kunci tanpa menyentuh TikTok
~/venvs/tiktok-watch/bin/python run_collection.py --dry-run

# koleksi terbatas
~/venvs/tiktok-watch/bin/python run_collection.py --limit 10
```

Daftar kata kunci: `watchlist.txt`. Keluaran: `data/leads.jsonl` (sengaja di-`.gitignore`).

## Indikator Prioritas

`tugas_berkomisi`, `deposit`, `profit_pasti`, `investasi`, `pinjol`, nomor telepon. Prioritas tinggi = minimal tiga indikator pada caption — **tetap bukan penetapan tindak pidana**.

## Verifikasi

```bash
cd ~/penyidikan/tools/tiktok-watch && python3 -m pytest tests -q   # 5 test
```

Selesai bila: `--dry-run` mencetak kata kunci tanpa galat, hasil tersimpan di `data/leads.jsonl`, dan tidak ada token/identitas korban yang tertulis ke berkas atau repo.

## Referensi

- `~/penyidikan/tools/tiktok-watch/README.md`
