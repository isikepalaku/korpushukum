# Cell ID Map

Membuat peta Leaflet mandiri dari hasil lookup Cell ID: marker pusat, cincin radius, panel informasi, dan—hanya bila tersedia dari sumber teknis—juring sektor/azimuth.

## Jalankan

```bash
python3 render_cell_map.py \
  --input example_lookup.json \
  --output output/cell-87305749.html
```

Buka berkas HTML di browser. Basemap OpenStreetMap dan Leaflet dimuat saat browser memiliki koneksi internet.

## Input JSON minimum

```json
{
  "latitude": -5.1580683,
  "longitude": 119.5742523,
  "accuracy_m": 486,
  "label": "Telkomsel LTE — ECI 87305749"
}
```

Opsional:
- `rings_m`: jarak cincin dalam meter, misalnya `[450, 620, 1000]`.
- `looked_up_at`, `detail`: jejak provenance hasil.
- `azimuth_deg`, `beamwidth_deg`, `sector_label`: juring sektor. Jangan mengisi dari tebakan atau dari CID saja; harus berasal dari data operator, site survey, atau sumber teknis yang dapat diuji.

## Static PNG (Google Maps)

Untuk gambar Telegram/workpaper dengan basemap hybrid atau satelit, aktifkan **Maps Static API** di Google Cloud lalu jalankan:

```bash
set -a && . ~/.hermes/.env && set +a
python3 render_static_cell_map.py \
  --input example_estimated_sector.json \
  --output output/cell-map.png
```

`render_static_cell_map.py` mengambil basemap Google Static Maps, lalu menggambar cincin radius, marker, juring, dan panel status secara lokal. Key tidak ditulis ke output, log, atau URL yang dicetak. Pakai hanya untuk **koordinat BTS** yang telah diverifikasi, bukan respons Google Geolocation dari data sel/Wi-Fi.

Juring harus mencantumkan `azimuth_deg`, `beamwidth_deg`, dan `sector_status: "verified"` yang berasal dari operator/site survey/drive test terdokumentasi. Jangan membuat juring dari CI, ECI, atau respons Geolocation.

## Lookup otomatis: tautan lokasi

Gunakan satu perintah berikut untuk LTE bila tersedia eNB ID dan CID:

```bash
set -a && . ~/.hermes/.env && set +a
python3 lookup_cellid.py \
  --mcc 510 --mnc 10 --enb-id 341038 --cid 21 \
  --output /tmp/cellid-result.json
```

Perintah menghasilkan ECI yang dihitung, Google Maps link, dan JSON provenance. Google Geolocation mengembalikan **estimasi area lokasi perangkat/observasi beserta radius akurasinya**, bukan koordinat BTS; karena itu lookup otomatis tidak membuat PNG cincin ataupun juring sektor.

Gunakan visualisasi sektor hanya bila memiliki koordinat BTS dan azimuth/beamwidth dari operator, site survey, atau drive test yang terdokumentasi. Jangan masukkan eNB ID sebagai TAC.

## Batas pembuktian

Koordinat Geolocation adalah estimasi beserta radius akurasi. Peta ini bukan bukti lokasi perangkat, pelanggan, atau koordinat BTS pasti. Cantumkan input sumber, waktu lookup, ECI/TAC, radius, dan metode konversi sebelum dipakai dalam workpaper.
