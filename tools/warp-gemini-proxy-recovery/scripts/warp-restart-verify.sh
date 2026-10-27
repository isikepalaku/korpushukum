#!/bin/bash
# Restart hermes-gateway agar .env proxy WARP terbaca, lalu verifikasi.
#
# WAJIB dijalankan dari shell LUAR gateway (SSH). Agent tidak bisa menjalankan ini
# dari dalam sesi chat: Hermes memblokir restart gateway (proteksi #30719).
#
# Pakai:  bash ~/.hermes/scripts/warp-restart-verify.sh
set -u
LOG="$HOME/.hermes/cache/scratch/warp-restart-result.log"
: >"$LOG"
exec >>"$LOG" 2>&1
echo "=== $(date -Is) mulai ==="

echo "--- 1. Konfigurasi .env ---"
grep -nE '^(HTTPS?_PROXY|NO_PROXY)=' "$HOME/.hermes/.env" || echo "GAGAL: baris proxy tidak ditemukan"

echo "--- 2. Restart gateway ---"
systemctl --user restart hermes-gateway
sleep 18

echo "--- 3. Status gateway ---"
echo "active=$(systemctl --user is-active hermes-gateway)"
PID=$(systemctl --user show -p MainPID --value hermes-gateway)
echo "MainPID=$PID  start=$(ps -o lstart= -p "$PID" 2>/dev/null)"

echo "--- 4. Cek log: proxy detected ---"
grep -iE 'Proxy detected' "$HOME/.hermes/logs/agent.log" | tail -5 || echo "(tidak ada)"

echo "--- 5. Cek log: ProxyError/502 ---"
grep -iE 'ProxyError|502 Bad Gateway' "$HOME/.hermes/logs/agent.log" | tail -8 || echo "(tidak ada error 502)"

echo "--- 6. Cek log: Telegram connected ---"
grep -iE 'Connected to Telegram|telegram connected' "$HOME/.hermes/logs/agent.log" | tail -5 || echo "(tidak ada)"

echo "--- 7. Uji Gemini generateContent (dengan proxy WARP) ---"
set -a; . "$HOME/.hermes/.env"; set +a
curl -s -m 45 -o /tmp/gem_test.json -w 'HTTP %{http_code}\n' \
  -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key=${GOOGLE_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{"contents":[{"parts":[{"text":"Balas satu kata: PONG"}]}],"generationConfig":{"maxOutputTokens":200}}'
head -c 400 /tmp/gem_test.json
echo

echo "--- 8. Uji Telegram bypass (harus tidak lewat proxy) ---"
curl -s -m 20 -o /dev/null -w 'telegram HTTP %{http_code}\n' https://api.telegram.org/

echo "--- 9. IP keluar via proxy ---"
curl -s -m 20 -x http://127.0.0.1:40000 https://api.ipify.org; echo
echo "--- 10. IP keluar direct ---"
curl -s -m 15 https://api.ipify.org; echo

echo "=== $(date -Is) selesai ==="
cat "$LOG"
