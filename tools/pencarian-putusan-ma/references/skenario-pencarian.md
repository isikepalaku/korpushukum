# Skenario Pencarian Putusan — Dokumentasi Terverifikasi (2026-09-02)

Semua skenario di bawah **diuji live** terhadap `apigateway.mahkamahagung.go.id` dengan key valid.
Auth wajib: header `apikey: O3OXb3x6d8eF2j1Wtr83HlrONeQ8dPaM` + `User-Agent: Dart/3.3 (dart:io)`.

Base URL: `https://apigateway.mahkamahagung.go.id/putusan3/mobile/pencarian`

---

## Ringkasan perilaku mesin pencari (ELASTICSEARCH)

| Perilaku | Hasil uji |
|---|---|
| Kata tunggal | `q=korupsi` → 57.579 dokumen |
| Multi-kata default | **OR** (union) — `q=pegadaian ilegal` → 65.505 (lebih besar dari `pegadaian` saja 53.041) |
| Operator `AND` eksplisit | **Bekerja** — `q=korupsi AND perbankan` → 2.673 (irisan presisi) |
| Operator `OR` eksplisit | **Bekerja** — `q=korupsi OR perbankan` → 75.591 (gabungan) |
| Frasa bertanda kutip `"..."` | **TIDAK didukung** — `q="usaha gadai tanpa izin"` → 0 |
| Nomor perkara (dengan `/`) | **Tidak andal** — tokenizer memecah `/`, hasil melebar (ribuan match tidak relevan) |
| Pencarian nama orang | **Bekerja** — `q=MAHARI` → ketemu kasusnya |
| Pagination | `page=1..N`, **size maksimum 20** (size=50/100 tetap balas 20) |

**Implikasi praktis:**
- Untuk presisi gunakan **`AND`**: `q=gadai AND izin AND pidana`
- Cari orang → nama (bisa tanpa gelar, tanpa spasi berlebih)
- Cari nomor perkara → jangan langsung; cari via nama/kata kunci lalu ambil `_id` dari hasil, atau cari komponen unik nomor (mis. `q=1318 K/Pid` tetap melebar — tidak disarankan)

---

## SKENARIO 1 — Cari putusan berdasarkan kata kunci tindak pidana/modus

```bash
KEY="O3OXb3x6d8eF2j1Wtr83HlrONeQ8dPaM"; UA="Dart/3.3 (dart:io)"
B="https://apigateway.mahkamahagung.go.id/putusan3/mobile/pencarian"

# Modus tunggal
curl -s -H "apikey: $KEY" -A "$UA" "$B?q=korupsi&page=1&size=20"

# Modus presisi (AND)
curl -s -G -H "apikey: $KEY" -A "$UA" \
  --data-urlencode "q=usaha gadai AND tanpa izin" \
  --data "page=1" --data "size=20" "$B"
```

Hasil uji: `korupsi AND perbankan` → 2.673; `usaha gadai AND tanpa izin` → presisi tinggi.

## SKENARIO 2 — Cari putusan atas nama orang (terdakwa/para pihak)

```bash
curl -s -G -H "apikey: $KEY" -A "$UA" \
  --data-urlencode "q=MAHARI" --data "page=1" --data "size=20" "$B"
```

Catatan: nama dicocokkan di seluruh teks; hasil paling relevan biasanya di urutan atas. Untuk nama umum, kombinasikan dengan kata kunci lain (`q=MAHARI AND gadai`).

## SKENARIO 3 — Filter jenis dokumen (`jenis_doc`)

Nilai valid (dari bucket `data.aggs.jenis_doc_aggs`): `putusan`, `peraturan`, `rumusan_kamar`, `rumusan_rakernas`, `restatement`.
⚠️ "yurisprudensi" BUKAN nilai valid — yurisprudensi tersimpan sebagai putusan ber-kaidah.

```bash
curl -s -H "apikey: $KEY" -A "$UA" "$B?q=korupsi&jenis_doc=putusan&page=1&size=20"
# uji: korupsi 57.579 → korupsi+putusan 57.439 (minus peraturan/rumusan/restatement)
```

## SKENARIO 4 — Filter tingkat proses (`tp`)

Nilai: `0` (PN/pertama), `1` (PT/banding), `2` (MA/kasasi), `3` (PK) — sesuai bucket `process_level_aggs`.

```bash
# Hanya kasasi MA (paling relevan untuk yurisprudensi)
curl -s -H "apikey: $KEY" -A "$UA" "$B?q=korupsi&tp=2&page=1&size=20"
# uji: korupsi+tp=1 → 13.428; korupsi+tp=2 → 9.783
```

## SKENARIO 5 — Gabungan filter + pagination

```bash
# Kasasi MA tentang korupsi perbankan, halaman 2
curl -s -G -H "apikey: $KEY" -A "$UA" \
  --data-urlencode "q=korupsi AND perbankan" \
  --data "page=2" --data "size=20" \
  --data "tp=2" --data "jenis_doc=putusan" "$B"
```

## SKENARIO 6 — Ambil detail putusan

```bash
curl -s -H "apikey: $KEY" -A "$UA" \
  "https://apigateway.mahkamahagung.go.id/putusan3/mobile/detail?id=<_id>"
```

Field penting respons: `nomor`, `nama_pengadilan`, `tanggal_putusan`, `para_pihak`, `amar_lengkap`, `is_bht` (berkekuatan hukum tetap), `stat_total_view`, `kaidah_hukum`, `yr_kaidah_hukum`, `keywords`. Teks lengkap = PDF via `download_file` (bukan dari API ini).

## SKENARIO 7 — Endpoint statistik

```bash
curl -s -H "apikey: $KEY" -A "$UA" "https://apigateway.mahkamahagung.go.id/putusan3/mobile/pengadilan"   # 938 pengadilan
curl -s -H "apikey: $KEY" -A "$UA" "https://apigateway.mahkamahagung.go.id/putusan3/mobile/latest?doc=putusan"  # terbaru + aggs
curl -s -H "apikey: $KEY" -A "$UA" "https://apigateway.mahkamahagung.go.id/putusan3/mobile/aggs_jenis_doc"      # jenis dokumen
```

## SKENARIO 8 — Mencari "yurisprudensi" praktis untuk suatu tindak pidana

Karena kategori yurisprudensi tidak ter-index sebagai jenis_doc, pendekatan yang terbukti:

```bash
# 1. Cari putusan kasasi/PK (MA) dengan kata kunci modus
curl -s -G -H "apikey: $KEY" -A "$UA" \
  --data-urlencode "q=usaha gadai AND tanpa izin" \
  --data "page=1" --data "size=20" --data "tp=2" --data "jenis_doc=putusan" "$B"

# 2. Ambil detail, cek is_bht=true & kaidah_hukum
curl -s -H "apikey: $KEY" -A "$UA" ".../detail?id=<_id>"
```

Contoh nyata ditemukan: `2097 K/Pid.Sus/2014` (MAHARI — keywords "izin","usaha"), `1257 K/Pid.Sus/2018` (WAHIDIN), `1318 K/Pid/2015` (MISRANSYAH, BHT).

## SKENARIO 9 — URL download PDF (format TERVERIFIKASI 2026-09-02)

Format URL PDF dari halaman putusan web (dikonfirmasi dari halaman terindex + uji 403/404):

```
https://putusan3.mahkamahagung.go.id/direktori/download_file/{FILE_ID}/pdf/{DOC_ID}
```

- `{FILE_ID}` = `file_uploads[].id` dari endpoint `/detail` (32 hex)
- `{DOC_ID}` = `id`/`_id` dokumen (id yang sama dipakai di `/direktori/putusan/{id}.html`)
- **Tanpa path, tanpa nama file, tanpa ekstensi** — format lama yang memakai path/nama file = 404
- Halaman putusan: `https://putusan3.mahkamahagung.go.id/direktori/putusan/{DOC_ID}.html`
- ⚠️ **Cloudflare anti-bot**: server/datacenter IP diblokir (403) untuk URL download PDF — hanya bisa diunduh dari browser manusia (HP/komputer rumah). URL yang salah format → 404 dari app (lolos CF), URL benar → 403 CF → tanda format sudah benar.

Contoh terverifikasi (dari web): `.../download_file/11f11bbe62459a50bf2b323034363333/pdf/11f11bbe624379c88096323034363333` (176 K/PDT/2026)

✅ **KONFIRMASI PENGGUNA (2026-09-02):** URL format ini berhasil — `691 K/Pid/2018` → `.../download_file/3e5626dd7600a7d224cb32b1c6670e65/pdf/zaec6199384a18a49a08323033323034` langsung mendownload PDF dari browser HP. Format FINAL.

Script: `./dirput-api.sh link <id>` otomatis menampilkan URL ini.

## Batasan yang sudah terbukti

1. `size` maksimum 20 per halaman (nilai lebih besar diabaikan).
2. Frasa kutip tidak didukung; multi-kata default OR → selalu pakai `AND` untuk presisi.
3. Pencarian nomor perkara ber-`/` tidak andal (tokenizer).
4. Filter lain (tahun, pengadilan, amar, kaidah) TIDAK tersedia sebagai query param di API mobile — hanya `q`, `page`, `size`, `jenis_doc`, `tp` yang terverifikasi.
5. WAF: jaga volume, jeda antar request, key valid wajib.
6. **NOISE kata umum (teruji 2026-09-02):** kata seperti `usaha`, `izin`, `gadai`, `gelap` muncul di banyak dokumen lintas topik — query `kegiatan AND usaha AND gadai` (3.662 hasil) memunculkan kasus Migas/narkotika di urutan atas karena full-text match frasa "kegiatan usaha ... tanpa izin", bukan karena topik gadai. **Verifikasi relevansi via field `keywords`** (ringkasan tema per dokumen) — jangan percaya urutan hasil. Istilah lebih spesifik (`jual gadai`, `usaha pergadaian`) + `AND` + cek keywords = hasil lebih tajam.
