---
name: auto-visualizer
description: Ringkas data tabular CSV/Excel dan buat visualisasi grafik otomatis.
version: 1.0.0
author: Ibrahim Sandre, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [data, csv, excel, visualizer, matplotlib, seaborn, statistics]
    category: productivity
---

# Auto Data Visualizer & Summarizer Skill

Skill untuk meringkas data tabular (CSV, Excel) dan menghasilkan visualisasi grafik secara otomatis (distribusi, top frekuensi, korelasi, dan tren waktu).

## When to Use

Gunakan ketika:
- Pengguna memberikan atau merujuk file CSV / Excel dan meminta analisis data.
- Diminta visualisasi cepat (grafik batang, korelasi, histogram distribusi, tren tanggal).
- Data transaksi, rekap kasus, log panggilan, atau statistik operasional membutuhkan gambar chart visual.

## How to Run

Jalankan skrip menggunakan virtual environment `~/venvs/docs/`:

```bash
~/venvs/docs/bin/python ~/penyidikan/tools/auto-visualizer/visualize.py <path_file.csv> [--out <direktori_output>]
```

Untuk menampilkan grafik hasil ke pengguna di Telegram:
Tuliskan `MEDIA:/path/ke/grafik.png` di dalam respon.
