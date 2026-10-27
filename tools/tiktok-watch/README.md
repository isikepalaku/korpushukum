# TikTok Watch — OSINT Lidik

Kolektor terbatas untuk konten TikTok publik yang memuat indikasi kejahatan sektor keuangan. Output adalah **petunjuk OSINT, bukan alat bukti**.

## Batas penggunaan

- Ambil hanya konten publik, ber-volume rendah: maksimum 30 video per kata kunci.
- Jangan memasukkan cookie, nomor rekening, nomor telepon, atau data korban ke Git.
- Jangan menghapus konten sumber; dokumentasikan URL, waktu akses, dan metode akuisisi sebelum tindakan prosedural.
- Hasil wajib diverifikasi lewat sumber primer, pemeriksaan, atau permintaan data yang sah.

## Siapkan lingkungan

```bash
uv venv ~/venvs/tiktok-watch
uv pip install --python ~/venvs/tiktok-watch/bin/python -r requirements.txt
~/venvs/tiktok-watch/bin/python -m playwright install chromium
```

Simpan `msToken` TikTok melalui vault/secret manager, lalu ekspor hanya untuk sesi terminal aktif:

```bash
export TIKTOK_MS_TOKEN='...'
```

Jangan tempel token di chat, berkas, riwayat shell, atau Git.

## Jalankan

Periksa kata kunci tanpa akses TikTok:

```bash
~/venvs/tiktok-watch/bin/python run_collection.py --dry-run
```

Koleksi terbatas:

```bash
~/venvs/tiktok-watch/bin/python run_collection.py --limit 10
```

Output: `data/leads.jsonl` (sengaja diabaikan Git).

## Indikator prioritas

`tugas_berkomisi`, `deposit`, `profit_pasti`, `investasi`, `pinjol`, dan nomor telepon. Prioritas tinggi berarti minimal tiga indikator pada caption; tetap bukan penetapan tindak pidana.
