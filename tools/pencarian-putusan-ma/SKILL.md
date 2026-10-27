---
name: pencarian-putusan-ma
description: "Cari putusan pengadilan via API mobile Mahkamah Agung."
version: 1.0.0
author: Hermes Agent (untuk Sandre — Dit Reskrimsus Polda Sulsel, Subdit 2 Fismondev)
license: MIT
platforms: [linux, windows]
metadata:
  hermes:
    tags: [mahkamah-agung, putusan, dirput, api, penyidikan, fismondev]
---

# Pencarian Putusan — API Mobile Mahkamah Agung (Direktori Putusan)

## When to Use

Gunakan saat perlu: mencari putusan pengadilan (nama/terdakwa/nomor perkara/kata kunci), mengambil isi lengkap putusan (amar, para pihak), verifikasi status/klaim perkara, atau cross-check data yang diklaim tersangka/terlapor terhadap database putusan MA.

**Sumber key & metode:** reverse-engineer APK "Direktori Putusan MA" (go.id.mahkamahagung.dirput) via blutter, 2026-09-02. Backend = Elasticsearch.

## API

**Base:** `https://apigateway.mahkamahagung.go.id`

| Endpoint | Method | Fungsi |
|---|---|---|
| `/putusan3/mobile/pengadilan` | GET | Daftar 938 pengadilan (BADILAG, BADILUM, BADIMILTUN...) |
| `/putusan3/mobile/latest?doc=putusan` | GET | Putusan terbaru + agregasi statistik (total dokumen, amar) |
| `/putusan3/mobile/aggs_jenis_doc` | GET | Statistik jenis dokumen (Putusan 11 jt, Yurisprudensi, Rumusan Kamar...) |
| `/putusan3/mobile/pencarian?q=<keyword>&page=<n>&size=<n>` | GET | **Cari putusan** (total + results, pagination) |
| `/putusan3/mobile/detail?id=<_id>` | GET | Isi lengkap putusan (amar_lengkap, para_pihak, stat view) |

Download file putusan: `https://putusan3.mahkamahagung.go.id/direktori/download_file/` (di balik Cloudflare — akses dari browser manusia, bukan server).

## Auth (WAJIB kedua-duanya)

```bash
KEY="O3OXb3x6d8eF2j1Wtr83HlrONeQ8dPaM"        # hardcoded di libapp.so, shared secret statis
UA="Dart/3.3 (dart:io)"                        # gateway blokir UA curl/browser
```

- Tanpa header `apikey` → 403 nginx
- `apikey` nilai salah → 401 `{"message":"Unauthorized"}` (layer aplikasi)
- `apikey` benar + UA non-Dart → 403 nginx
- Catatan: endpoint publik (pengadilan/latest/aggs) dulu sempat menerima apikey nilai apa pun + UA Dart, tapi setelah WAF meng-escalate, key valid tetap yang aman.

## Cara Pakai

### Opsi 1 — Script siap pakai (disarankan)

Script ada di `scripts/dirput-api.sh` skill ini:

```bash
# salin ke ~/penyidikan/tools/ lalu jalankan:
./dirput-api.sh cari "korupsi" 1 20        # cari putusan
./dirput-api.sh cari "koperasi simpan pinjam" 1 10
./dirput-api.sh detail <_id>               # isi lengkap putusan
./dirput-api.sh link <_id>                 # info file PDF + URL download otomatis
./dirput-api.sh pengadilan                 # daftar pengadilan
./dirput-api.sh latest                     # putusan terbaru
./dirput-api.sh aggs                       # statistik dokumen
```

### ⚡ ATURAN WAJIB: URL PDF otomatis di setiap laporan putusan

Setiap kali menyampaikan hasil putusan ke pengguna, **SELALU sertakan URL PDF**:

1. Ambil `_id` dari hasil pencarian
2. Jalankan `./dirput-api.sh link <_id>` (atau format manual `https://putusan3.mahkamahagung.go.id/direktori/download_file/{file_id}/pdf/{doc_id}`)
3. Tampilkan URL PDF + URL halaman web (`https://putusan3.mahkamahagung.go.id/direktori/putusan/{doc_id}.html`) bersama nomor perkara
4. Ingatkan: PDF hanya bisa diunduh dari browser manusia (Cloudflare blokir server)

### Opsi 2 — curl langsung

```bash
KEY="O3OXb3x6d8eF2j1Wtr83HlrONeQ8dPaM"
curl -s -H "apikey: $KEY" -A "Dart/3.3 (dart:io)" \
  "https://apigateway.mahkamahagung.go.id/putusan3/mobile/pencarian?q=korupsi&page=1&size=5"
```

### Parse hasil (Python)

```python
import json, urllib.request
req = urllib.request.Request(
    "https://apigateway.mahkamahagung.go.id/putusan3/mobile/pencarian?q=korupsi&page=1&size=5",
    headers={"apikey": "O3OXb3x6d8eF2j1Wtr83HlrONeQ8dPaM", "User-Agent": "Dart/3.3 (dart:io)"})
d = json.load(urllib.request.urlopen(req, timeout=30))
total = d["data"]["total"]
for r in d["data"]["results"]:
    s = r["_source"]
    print(s.get("nomor"), "|", s.get("nama_pengadilan"), "|", s.get("tanggal_putusan"), "|", s.get("para_pihak"))
```

Struktur respons (khas Elasticsearch): `data.total`, `data.results[]._id`, `data.results[]._source.{nomor, nama_pengadilan, tanggal_putusan, tanggal_register, para_pihak, amar_lengkap, jenis_doc, keywords, stat_total_view, id}`, `data.aggs`, `data.suggests`, `data.mlt`.

## Filter Pencarian (terverifikasi 2026-09-02)

- **`jenis_doc`** = filter jenis dokumen. Nilai VALID: `putusan`, `peraturan`, `rumusan_kamar`, `rumusan_rakernas`, `restatement` (ambil dari bucket `data.aggs.jenis_doc_aggs`). Contoh: `?q=pegadaian&jenis_doc=putusan`.
- ⚠️ **"yurisprudensi" BUKAN nilai jenis_doc** — di index pencarian, dokumen yurisprudensi tersimpan sebagai `putusan` dengan penanda kaidah hukum (field `is_kaidah_hukum`, `yr_kaidah_hukum`, `yr_bidang`). Total dokumen berlabel "Yurisprudensi" di seluruh DB hanya ~21 (lihat `/aggs_jenis_doc`) dan tidak muncul di hasil pencarian.
- **Mencari contoh "yurisprudensi"** → praktik terbaik: cari kata kunci tindak pidana + filter putusan tingkat MA kasasi/PK (nomor berawalan `K/`, `PK/`), atau cari via nama terdakwa. Hasil kasasi MA yang berkekuatan hukum tetap (`is_bht: true`) itulah yang berfungsi sebagai yurisprudensi praktis.
- Aggs lain di respons (untuk filter lanjutan): `process_level_aggs` (0-3), `tahun_put_aggs`, `tahun_upl_aggs`, `pengadilan_aggs`, `pilihan_aggs` (0/1), `is_kaidah_aggs`, `shor_judicial_aggs` (amar), `kategori_aggs`.
- **URL-encode query** dengan spasi/slash: `curl -G --data-urlencode "q=1257 K/Pid.Sus/2018" "$BASE/putusan3/mobile/pencarian"` (slash di nomor perkara wajib di-encode).
- Field penting di `_source`: `nomor`, `nama_pengadilan`, `tanggal_putusan`, `tanggal_register`, `para_pihak`, `amar_lengkap`, `jenis_doc`, `keywords`, `is_bht`, `stat_total_view`, `kaidah_hukum`, `yr_kaidah_hukum`, `id`. Teks lengkap putusan = PDF via `download_file` (bukan dari API detail — API detail hanya metadata + amar).

## Skenario Pencarian (dokumentasi lengkap)

Lihat `references/skenario-pencarian.md` — 8 skenario terverifikasi live:
kata kunci/modus, nama orang, filter `jenis_doc`, filter `tp` (tingkat proses),
gabungan+pagination, detail, statistik, dan trik mencari "yurisprudensi" praktis.
Ringkasannya:

- **Multi-kata default = OR** → gunakan `AND` eksplisit untuk presisi: `q=usaha gadai AND tanpa izin`
- **Frasa kutip `"..."` TIDAK didukung**; **nomor perkara ber-`/` tidak andal** (cari via nama/kata kunci)
- **`size` maks 20** per halaman; **filter valid hanya**: `q`, `page`, `size`, `jenis_doc`, `tp`
- **`tp`**: 0=PN, 1=PT, 2=MA/kasasi, 3=PK — kombinasi `tp=2` + kata kunci = cara cari yurisprudensi praktis

## Pitfalls

1. **User-Agent wajib Dart** — curl/browser default kena 403 nginx. Header `apikey` wajib ada.
2. **Pencarian = GET** — POST ke `/pencarian` balas `{"status":false,"error":"Unknown method."}`.
3. **WAF memantau IP** — ~15 request beruntun dengan key salah/UA sama → semua request dari IP itu ditolak 401 sementara. Gunakan key valid, jangan brute-force, jaga volume (kasih jeda).
4. **`doc=putusan` saja yang terbuka** untuk `/latest` — `doc=yurisprudensi`/`peraturan` → 401.
5. **Param filter yang ada di app**: `nama_pengadilan`, `level_pengadilan`, `kategori`, `pengadilan_aggs`, `pengadilan_lc`, `amar_lengkap`, `amar_singkat_lainnya`, `filterres` (query string `key=value&`). Param kata kunci utama = `q`.
6. **APK yang beredar di mirror sering re-signed** (debug keystore `b119245a...`, stamp-cert mismatch) — untuk analisis teknis tidak masalah; untuk barang bukti integritas, verifikasi SHA-256 vs versi Play resmi.
7. Versi app: v1.0.0 (code 5/8/9 beredar) — endpoint stabil antar versi.

## Verifikasi (contoh hasil nyata 2026-09-02)

- `?q=korupsi` → total 57.579; `?q=perbankan` → total 20.685
- Detail `22/Pid.Sus/2013/PN.Mdo` (PN Manado) — KORUPSI, 1 th penjara + denda 50 jt, stat_total_view 134
- `/latest` → total 10.525.851 dokumen (data s.d. 2026-09-01)

## Batasan & Etika

- API resmi pemerintah untuk informasi publik (putusan = publik). Gunakan secukupnya untuk kepentingan penyidikan yang sah.
- Hasil API = petunjuk/verifikasi awal, BUKAN alat bukti resmi — untuk bukti formal tetap gunakan jalur resmi (salinan putusan dari pengadilan/SIPP).
- Jangan brute-force key/nomor; hormati WAF.
- Untuk scraping massal: situs putusan3 di balik Cloudflare anti-bot; API mobile ada pagination (`page`, `size`) tapi tetap batasi volume.

## File Terkait

- `scripts/dirput-api.sh` — script query API
- Analisis lengkap APK: `analisis/direktori-putusan/LAPORAN-analisis.md` (path per mesin: server Linux `~/penyidikan/analisis/...`, Windows `E:/Agent/UU/analisis/...`)
- Decompile penuh (blutter): `analisis/direktori-putusan/blutter-out/`
