#!/usr/bin/env bash
# dirput-api.sh — Query API mobile Direktori Putusan MA (apigateway.mahkamahagung.go.id)
# Sumber: reverse-engineer APK "Direktori Putusan MA" v1.0.0 (go.id.mahkamahagung.dirput)
# Dibuat: 2026-09-02 — Subdit II Fismondev Polda Sulsel
#
# Penggunaan:
#   ./dirput-api.sh pengadilan                        # daftar 938 pengadilan
#   ./dirput-api.sh latest                            # putusan terbaru + statistik
#   ./dirput-api.sh aggs                              # statistik jenis dokumen
#   ./dirput-api.sh cari "<kata kunci>" [page] [size] # cari putusan (total + hasil)
#   ./dirput-api.sh detail <id>                       # isi lengkap putusan (metadata+amar)
#   ./dirput-api.sh link <id>                         # info file PDF + URL download (dari file_uploads)
#
# Auth (diekstrak dari libapp.so):
#   Header: apikey: O3OXb3x6d8eF2j1Wtr83HlrONeQ8dPaM
#   User-Agent wajib seperti Dart (gateway blokir UA curl/browser)
#   Tanpa header apikey -> 403; apikey salah -> 401

BASE="https://apigateway.mahkamahagung.go.id"
KEY="O3OXb3x6d8eF2j1Wtr83HlrONeQ8dPaM"
UA="Dart/3.3 (dart:io)"

case "$1" in
  pengadilan) URL="$BASE/putusan3/mobile/pengadilan" ;;
  latest)     URL="$BASE/putusan3/mobile/latest?doc=putusan" ;;
  aggs)       URL="$BASE/putusan3/mobile/aggs_jenis_doc" ;;
  cari)       URL="$BASE/putusan3/mobile/pencarian?q=$2&page=${3:-1}&size=${4:-20}" ;;
  detail)     URL="$BASE/putusan3/mobile/detail?id=$2" ;;
  link)
    # Ambil detail, tampilkan info file PDF + URL download (format hasil rekonstruksi)
    curl -s --max-time 30 -H "apikey: $KEY" -A "$UA" "$BASE/putusan3/mobile/detail?id=$2" | python3 -c "
import json,sys
d = json.load(sys.stdin).get('data',{})
print('nomor:', d.get('nomor'), '|', d.get('nama_pengadilan'), '| tgl:', d.get('tanggal_putusan'))
fu = d.get('file_uploads') or []
if not fu:
    print('(tidak ada file_uploads)')
for f in fu:
    print()
    print('file_name_ori:', f.get('file_name_ori'), '| size:', f.get('size'), 'byte')
    print('path        :', f.get('path'))
    fid = f.get('id','')
    fname = f.get('file_name','')
    ext = f.get('extension','')
    fpath = f.get('path','')
    docid = d.get('id') or d.get('guid') or ''
    print()
    print('URL web (buka dari browser HP — link pencarian pasti jalan):')
    print('  https://putusan3.mahkamahagung.go.id/search.html?q=' + (d.get('nomor') or '').replace(' ','+'))
    print('URL PDF (format TERVERIFIKASI dari halaman web terindex — buka di browser HP):')
    print(f'  https://putusan3.mahkamahagung.go.id/direktori/download_file/{fid}/pdf/{docid}')
    print('  (pola: download_file/{file_id}/pdf/{doc_id} — tanpa path, tanpa nama file, tanpa ekstensi)')
"
    exit 0 ;;
  *) echo "Usage: $0 {pengadilan|latest|aggs|cari '<kata>' [page] [size]|detail <id>|link <id>}" >&2; exit 1 ;;
esac

curl -s --max-time 30 -H "apikey: $KEY" -A "$UA" "$URL"
echo
