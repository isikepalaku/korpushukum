---
name: cellid-map
description: "Use when a Cell ID lookup result must be mapped."
version: 1.1.0
author: Tim Fismondev Ditreskrimsus Polda Sulsel
license: Internal Polri
platforms: [linux, macos]
category: penyidikan
tags: [cellid, bts, geolokasi, osint, workpaper, leaflet, google-geolocation]
---

# Skill: Cell ID Map (pemetaan hasil lookup Cell ID)

Membungkus tool `~/penyidikan/tools/cellid-map/` (tersinkron git): lookup Cell ID LTE → JSON provenance + peta Leaflet mandiri atau PNG statis, dengan **batas pembuktian yang ketat**. Koordinat Google Geolocation adalah **estimasi area perangkat/observasi**, bukan koordinat BTS dan bukan lokasi orang.

## Format Luaran (default: ringkas)

**Aturan pengguna (tetap): bila diminta lookup Cell ID, proses lalu beri hasilnya — jangan menjelaskan atau menganalisis panjang lebar.**

Balasan default maksimal ~15 baris:
1. ECI + asumsi konversi (satu baris, mis. "LAC 337080 di luar rentang TAC → kandidat eNB ID → ECI 86292513").
2. Koordinat hasil + radius akurasi + tautan Maps.
3. Catatan identifikator hanya bila ada yang tidak sinkron (maks. 2 baris).
4. Bila koordinat sumber ikut diberikan: jarak antar-pusat (satu baris) + status kompatibel/tidak.
5. Satu baris penutup batas bukti ("estimasi area ber-radius, bukan lokasi BTS/orang").

Tanpa tabel, tanpa seksi "batas pembuktian", "celah data", atau "tindak lanjut" di chat. Analisis panjang, workpaper, tabel batas pembuktian, dan saran permintaan data ke operator tetap dibuat **di latar belakang** (berkas kerja di `~/workspace/cellid/`) tetapi **tidak ditempel ke chat** kecuali diminta eksplisit (mis. "buatkan workpaper", "jelaskan", "lampiran laporan").

Ilustrasi PNG: buat hanya bila diminta — pengambilan tile memakan waktu, dan tanpa permintaan hasil angka + tautan Maps sudah cukup.

## Kapan Digunakan

- Ada Cell ID/ECI/LAC dari dokumen operator, XLS, atau hasil ekstraksi dan perlu dipetakan untuk workpaper.
- Perlu jejak provenance (input, waktu lookup, radius akurasi, metode konversi) sebelum hasil dipakai di BAP/LHP.
- Perlu gambar peta untuk lampiran laporan atau Telegram.

**Jangan** dipakai untuk: melacak orang/perangkat tanpa dasar kewenangan; mengklaim lokasi pasti; membuat juring sektor hanya dari CID/ECI.

## Prasyarat

- `GOOGLE_API_KEY` di `~/.hermes/.env` dengan **Geolocation API** aktif. Muat dengan `set -a && . ~/.hermes/.env && set +a`.
- Python 3.11 standar (lookup hanya memakai pustaka bawaan; tidak perlu venv).
- Koneksi internet untuk lookup; basemap Leaflet/OSM dimuat saat HTML dibuka di browser.

## Batas Pembuktian (WAJIB dibaca sebelum menyimpulkan)

| Klaim | Status |
|---|---|
| Koordinat hasil Geolocation | **Estimasi area** perangkat/observasi + radius `accuracy_m`. Bukan lokasi orang, bukan koordinat BTS. |
| Juring sektor / azimuth | Hanya bila ada `azimuth_deg`, `beamwidth_deg`, dan `sector_status: "verified"` dari **data operator, site survey, atau drive test terdokumentasi**. |
| Label `LAC`/`TAC` dari alat pihak ketiga | Sering salah label. TAC LTE sah 0–65535; nilai >65535 adalah kandidat **eNB ID**. |
| eNB ID diisi sebagai TAC | **Jangan.** Merusak lookup. |

## Aturan Identifier

- LTE: `ECI = (eNB_ID × 256) + CID`. Simpan nilai sumber dan hasil hitung **terpisah** untuk jejak audit.
- **Periksa identifikator pendamping sebelum melaporkan** (temuan lapangan: satu baris ekspor operator dapat memuat angka yang tidak sinkron):
  - IMSI → MCC/MNC harus konsisten dengan prefix MSISDN (mis. IMSI 510-10 + MSISDN 0823 = Telkomsel). Bila MSIN ≠ bagian nasional MSISDN (bukan hanya 5 digit terakhir yang sama), tandai sebagai ketidaksesuaian dan minta konfirmasi operator — jangan menyimpulkan itu satu pelanggan yang sama.
  - IMEI harus 15 digit. Nilai 14 digit berarti digit cek Luhn terpotong: hitung kandidat digit cek dari 14 digit yang ada, sajikan sebagai **kandidat**, dan sebut TAC sebagai tentatif.
- **Jangan menganggap `Age`/freshness sebagai waktu observasi.** Baris ekspor sering tidak memuat timestamp koleksi; catat itu sebagai celah data karena posisi tidak dapat diikat ke jam tertentu tanpa timestamp.
- API Google membutuhkan **ECI penuh** pada `cellId`, bukan CID sektor 8-bit.
- Bila sumber memberi angka besar berlabel `LAC/TAC` (>65535) bersama CID kecil (contoh `340432` dan `33`): perlakukan sementara sebagai kandidat eNB ID, hitung ECI, lakukan lookup, dan **laporkan asumsinya secara eksplisit**. Jangan menyebutnya TAC dan jangan mengklaim kepastian BTS.

## Cara Menjalankan

### 1. Lookup LTE

```bash
set -a && . ~/.hermes/.env && set +a
python3 ~/penyidikan/tools/cellid-map/lookup_cellid.py \
  --mcc 510 --mnc 10 --enb-id 341038 --cid 21 \
  --output /tmp/cellid.json
```

Keluaran: `eci`, `google_maps_link`, `sector_status`, `result`. Opsi `--dry-run` menghitung ECI tanpa memanggil API (tanpa kredensial).

### 2. Peta Leaflet mandiri

```bash
python3 ~/penyidikan/tools/cellid-map/render_cell_map.py \
  --input /tmp/cellid.json --output output/cell-<eci>.html
```

### 3. PNG statis (basemap Google) — hanya untuk koordinat BTS terverifikasi

```bash
set -a && . ~/.hermes/.env && set +a
python3 ~/penyidikan/tools/cellid-map/render_static_cell_map.py \
  --input <json> --output output/<nama>.png
```

Jangan memakai PNG statis untuk respons Geolocation dari data sel/Wi-Fi; peruntukannya koordinat BTS yang sudah diverifikasi.

### 4. Ilustrasi PNG perbandingan (basemap OSM) — untuk lampiran/Telegram

Bila hasil Geolocation hanya estimasi area dan PNG statis Google tidak boleh dipakai (poin 3), buat ilustrasi dari tile OpenStreetMap dengan marker + cincin radius dan label eksplisit "bukan bukti lokasi orang":

```bash
python3 ~/.hermes/skills/penyidikan/cellid-map/scripts/render_compare_png.py \
  --a-lat -2.9531734 --a-lon 120.1363376 --a-acc 594.89 --a-label "A - pusat estimasi Google Geolocation" \
  --b-lat -2.962020  --b-lon 120.148320  --b-label "B - koordinat yang diberikan sumber" \
  --title "Cell ID ECI 86292513 - Telkomsel LTE - ilustrasi kerja, BUKAN bukti lokasi orang" \
  --note "Keduanya ter-reverse-geocode ke Kel. Battang, Kec. Wara Barat, Kota Palopo." \
  --output output/cellid-<eci>-compare.png
```

Memerlukan `PIL` (tersedia di python3 sistem). Label batas pembuktian dan kredit basemap selalu dicetak di gambar, jadi ilustrasi tidak dapat dipakai seolah-olah bukti titik. Jarak antar-pusat dihitung skrip dan dicetak di header.

**Selisih pusat vs radius akurasi:** bila jarak antar-pusat (mis. koordinat sumber vs hasil lookup baru) melebihi `accuracy_m`, nyatakan kedua pusat "tidak kompatibel sebagai titik yang sama" — hanya tumpang tindih sebagian sebagai area.

**Kerucut yurisdiksi label area:** reverse geocode Google (bahasa `id`) adalah acuan label kelurahan/kecamatan; batas desa OpenStreetMap sering berbeda (temuan: OSM menempatkan titik yang sama di desa berbeda). Bila keduanya berselisih, catat sebagai kontradiksi dan pakai Google/Kemendagri — jangan kutip desa OSM sebagai fakta.

## Medan JSON

Wajib: `latitude`, `longitude`, `accuracy_m`, `label`. Opsional: `rings_m`, `looked_up_at`, `detail`, serta `azimuth_deg`/`beamwidth_deg`/`sector_label` (hanya bila terverifikasi).

## Pitfall

- Lookup **tidak** menghasilkan PNG atau juring sektor; keluaran `sector_status: not_applicable`. Juring hanya digambar bila datanya terverifikasi.
- Kunci API masuk ke URL permintaan (wajib untuk endpoint ini) — jangan mencetak URL mentah yang memuat `key`; skrip hanya mencetak Maps link tanpa kunci.
- `output/*.png` di-`.gitignore`; yang ter-track hanya berkas HTML contoh. Artefak lidik yang memuat identifikator sensitif disimpan di luar repo.
- Koordinat presisi dan identifikator telekomunikasi **tidak** disimpan ke halaman `wiki/` yang tersinkron GitHub.

## Verifikasi

```bash
cd ~/penyidikan/tools/cellid-map && python3 -m pytest tests -q
```

Selesai bila: test lulus, JSON memuat `accuracy_m` dan `looked_up_at`, peta terbuka di browser, dan laporan mencantumkan input sumber, ECI/TAC, radius akurasi, metode konversi, serta pernyataan batas pembuktian.

## Referensi

- Tool dan README kanonik: `~/penyidikan/tools/cellid-map/README.md`
- `scripts/render_compare_png.py` — ilustrasi PNG dua pusat estimasi pada basemap OSM (jarak, cincin radius, label batas pembuktian).
- Aturan Google API (kuota, pembatasan key, validasi identifier): skill `google-cloud-investigation-apis`
