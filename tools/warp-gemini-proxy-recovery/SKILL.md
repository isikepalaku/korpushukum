---
name: warp-gemini-proxy-recovery
description: Use when Gemini API blocks the VPS IP or WARP route breaks.
version: 1.0.0
author: Bripka Ibrahim Sandre (dibantu Hermes)
license: MIT
metadata:
  hermes:
    tags: [gemini, proxy, warp, cloudflare, networking, vps, telegram]
    related_skills: [hermes-gateway-ops, hermes-agent]
---

# WARP Proxy Recovery untuk Gemini API di VPS

## When to Use

- `generativelanguage.googleapis.com` membalas `400 FAILED_PRECONDITION: User location is not supported for the API use.`
- Gemini mati padahal API key valid, setelah WARP/`warp-svc` restart, update, atau reboot.
- Telegram gateway mulai `httpx.ProxyError: 502 Bad Gateway` setelah proxy dipasang.
- Ada rencana memindahkan VPS ke region lain **karena** Gemini diblokir — baca bagian “Jangan buang uang” dulu.

## Ringkasan singkat

Proxy WARP di `127.0.0.1:40000` dipasang sebagai `HTTPS_PROXY`/`HTTP_PROXY` di `~/.hermes/.env`, dengan `NO_PROXY` panjang yang mengecualikan Telegram dan semua layanan lokal. Tanpa `NO_PROXY` itu, Telegram mati dengan 502.

## Diagnosis dulu, jangan asal ganti konfigurasi

Bedakan tiga penyebab yang gejalanya mirip:

| Gejala | Penyebab sebenarnya | Obat |
|---|---|---|
| `400 FAILED_PRECONDITION` "User location is not supported" | IP keluar kelas **hosting/datacenter**, bukan negara | rute WARP |
| `404 ... no longer available to new users` | nama model usang | ganti nama model |
| `403 PERMISSION_DENIED` / API key invalid | kunci salah/kadaluarsa | kunci baru |

**Penting:** Indonesia dan Singapura **ADA** di daftar wilayah resmi Gemini API (https://ai.google.dev/gemini-api/docs/available-regions). Jadi jangan menyimpulkan geo-block nasional dari pesan itu — yang ditolak Google adalah **ASN/IP hosting**. Bukti: request dari IP Tencent Cloud ditolak, request yang sama lewat WARP diterima 200.

Jangan juga mengejar DNS. Mengganti resolver ke `1.1.1.1` atau DoH **tidak mengubah IP keluar** — Google menilai IP asal koneksi TCP, bukan resolver.

Tes pembeda cepat (butuh `GOOGLE_API_KEY` di `~/.hermes/.env`):

```bash
set -a; . ~/.hermes/.env; set +a
# langsung — harapan: 400 FAILED_PRECONDITION bila IP hosting bermasalah
curl -s -m 20 -o /dev/null -w 'direct HTTP %{http_code}\n' \
  "https://generativelanguage.googleapis.com/v1beta/models?key=${GOOGLE_API_KEY}"
# via WARP — harapan: 200 bila rute WARP sehat
curl -s -m 25 -x http://127.0.0.1:40000 -o /dev/null -w 'warp HTTP %{http_code}\n' \
  "https://generativelanguage.googleapis.com/v1beta/models?key=${GOOGLE_API_KEY}"
```

Kalau `direct` 400 dan `warp` 200 → kasus skill ini. Kalau keduanya 400 → WARP mati atau IP WARP juga diblok.

## Prasyarat: WARP dalam mode proxy, bukan TUN penuh

```bash
warp-cli --accept-tos status
warp-cli --accept-tos settings | grep -iE 'Mode|Protocol'
```

Harus ada `Mode: WarpProxy on port 40000`. Mode proxy berarti **opt-in per aplikasi** — hanya klien yang diberi `-x http://127.0.0.1:40000` (atau env proxy) yang lewat WARP. Ini yang diinginkan: OpenViking, DeepSeek, CDP, Telegram tetap langsung.

Kalau mode belum proxy:

```bash
warp-cli --accept-tos mode proxy
warp-cli --accept-tos proxy port 40000
```

## Konfigurasi Hermes (jalur yang dipakai di mesin ini)

Backup dulu, lalu tambahkan ke `~/.hermes/.env`:

```bash
cp ~/.hermes/.env ~/.hermes/.env.bak-$(date +%Y%m%d-%H%M%S)
```

```
HTTPS_PROXY=http://127.0.0.1:40000
HTTP_PROXY=http://127.0.0.1:40000
NO_PROXY=127.0.0.1,localhost,::1,43.173.14.8,43.173.33.125,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,.local,.internal,telegram.org,.telegram.org,t.me,.t.me,openrouter.ai,.openrouter.ai,clariohub.id,.clariohub.id,nousresearch.com,.nousresearch.com,cloudflare.com,.cloudflare.com
```

### Kenapa `NO_PROXY` sepanjang itu — jangan dipangkas

- **`telegram.org`/`.telegram.org`/`t.me`** — WARP tidak meneruskan `api.telegram.org` dengan baik; tanpa bypass muncul `httpx.ProxyError: 502 Bad Gateway` berulang dan bot jadi rapuh/mati. Ini kegagalan yang paling sering terulang.
- **`43.173.14.8`** — IP VPS ini sendiri (9Router/DeepSeek di `:20128`). Kalau tidak di-bypass, panggilan model ikut masuk WARP dan bisa 502.
- **`127.0.0.1`, `localhost`, `::1`** — OpenViking (`:1933`), CDP Chrome, daemon lokal.
- **CIDR `10/8`, `172.16/12`, `192.168/16`** — jaringan internal Tencent/VPC.
- **domain provider lain** (`openrouter.ai`, `clariohub.id`, `nousresearch.com`) — tidak perlu lewat WARP; memaksa lewat WARP menambah latensi + titik gagal.
- **`cloudflare.com`** — mencegah loop bila WARP sendiri butuh koneksi ke Cloudflare.

Matcher Hermes (`agent/proxy_bypass.py`) mendukung CIDR (`ip_network`), wildcard `*.domain`, dan suffix `.domain`. Stdlib `proxy_bypass_environment` **tidak** mendukung CIDR — jangan pakai itu untuk menguji.

### Verifikasi matriks bypass — WAJIB sebelum restart

Jalankan `scripts/verify_no_proxy.py` dari skill ini untuk memastikan Telegram bypass dan Gemini **tidak** bypass. Jangan restart gateway dengan `NO_PROXY` yang belum diuji — bot bisa mati dan sesi chat putus.

## Restart gateway — batas yang harus diketahui

**Agent tidak bisa me-restart gateway dari dalam sesi.** Hermes memblokir `systemctl --user restart hermes-gateway`, `hermes gateway restart`, `setsid`, `systemd-run`, dan cron job yang memuat perintah itu (proteksi `#30719`, mencegah loop SIGTERM-respawn di bawah systemd). Semua jalan akan balas: *"Blocked: command or referenced script cannot restart..."*.

Jadi: **minta user menjalankan dari SSH/shell luar**.

```bash
systemctl --user restart hermes-gateway
# atau yang sekaligus memverifikasi:
bash ~/.hermes/scripts/warp-restart-verify.sh
```

Jangan buang beberapa tool call mencoba setsid/systemd-run/`hermes gateway restart` — sudah pasti diblokir.

### `proxy_url` Telegram vs env global

`telegram.proxy_url` di `config.yaml` (atau env `TELEGRAM_PROXY`) membuat adapter Telegram **selalu** memakai proxy itu, mengalahkan `NO_PROXY`. Jangan set itu kalau tujuan hanya Gemini. Biarkan Telegram langsung.

## Verifikasi setelah restart — cek empat hal

```bash
PID=$(systemctl --user show -p MainPID --value hermes-gateway)
echo "active=$(systemctl --user is-active hermes-gateway) PID=$PID"
ps -o lstart= -p $PID

# 1. .env benar-benar dimuat
grep -iE 'Proxy detected' ~/.hermes/logs/agent.log | tail -3
# 2. Telegram — 502 harus berhenti SETELAH waktu start di atas
grep -iE 'ProxyError|502 Bad Gateway' ~/.hermes/logs/agent.log | tail -5
grep -iE 'Connected to Telegram|telegram connected' ~/.hermes/logs/agent.log | tail -3
# 3. Gemini dari env gateway
set -a; . ~/.hermes/.env; set +a
curl -s -m 45 -o /tmp/g.json -w 'HTTP %{http_code}\n' -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key=${GOOGLE_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{"contents":[{"parts":[{"text":"Balas satu kata: PONG"}]}],"generationConfig":{"maxOutputTokens":200}}'
head -c 300 /tmp/g.json
# 4. IP keluar
curl -s -m 15 -x http://127.0.0.1:40000 https://api.ipify.org; echo
```

Kriteria lulus: `Proxy detected: http://127.0.0.1:40000`, `Connected to Telegram (polling mode)`, tidak ada 502 setelah waktu restart, Gemini `HTTP 200` dengan `candidates` berisi teks, IP keluar = IP Cloudflare (bukan IP Tencent).

Catatan: `/proc/$PID/environ` **tidak** akan menampilkan `HTTPS_PROXY` — Hermes memuat `.env` ke `os.environ` setelah proses start (`load_hermes_dotenv`). Itu normal, bukan tanda gagal. Buktinya ada di log (`Proxy detected`), bukan di `/proc`.

## Pitfall yang sudah memakan waktu

1. **Jangan pindah VPS ke Singapura untuk urusan ini.** Indonesia & Singapura sama-sama didukung Gemini; IP cloud Singapura (Tencent/Alibaba/AWS) kemungkinan besar ditolak dengan pesan identik. Pindah region hanya masuk akal untuk latensi, atau ke provider yang IP-nya bukan kelas hosting.
2. **DNS bukan obat.** Ganti resolver ke `1.1.1.1`/DoH tidak mengubah IP keluar.
3. **`gemini-2.5-flash` pensiun** untuk kunci baru (`404 no longer available to new users`). Pakai `gemini-3.8-flash`. Cek nama model aktual via `GET /v1beta/models` sebelum menyalahkan jaringan.
4. **`thinking` menghabiskan `maxOutputTokens`.** Dengan `maxOutputTokens: 50` respons bisa balik `finishReason: MAX_TOKENS` dan `content.parts` kosong, dengan `thoughtsTokenCount` ~47. Bukan error. Naikkan ke 200+ untuk uji yang membaca teks.
5. **Model lewat 9Router/DeepSeek berlabel `gemini/...` belum tentu Gemini asli.** Endpoint OpenAI-chat-completions mengembalikan `chatcmpl-` dan `model`, bukan bentuk respons Gemini. Jangan jadikan bukti bahwa API key Gemini jalan — uji langsung ke `generativelanguage.googleapis.com`.
6. **WARP mati = Gemini mati.** `warp-svc` tidak auto-start setelah reboot pada sebagian instalasi. Tambahkan pemeriksaan ke watchdog bila Gemini penting.
7. **Kerahasiaan.** Trafik lewat Cloudflare. Untuk bahan perkara sensitif, pertimbangkan kebijakan tersendiri sebelum merutekan lewat WARP.

## Kalau WARP tetap gagal

Urutan eskalasi:

1. `warp-cli --accept-tos disconnect && sleep 3 && warp-cli --accept-tos connect` lalu ulangi tes.
2. Cek IP WARP yang keluar (`curl -x ... https://api.ipify.org`) — kalau IP yang keluar sama dengan IP VPS, WARP tidak benar-benar meneruskan.
3. Alternatif: **Vertex AI** dengan service account (`VERTEX_CREDENTIALS_PATH`) — penagihan & aturan lokasi berbeda, sering tidak kena filter IP yang sama. Halaman resmi Google sendiri mengarahkan kasus "wilayah tidak didukung" ke Gemini Enterprise Agent Platform (Vertex).
4. Alternatif terakhir: proxy residensial (bukan datacenter — Webshare/DC proxy biasanya tetap diblok).
