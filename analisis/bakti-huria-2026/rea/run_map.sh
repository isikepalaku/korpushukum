#!/usr/bin/env bash
# REA workflow+identity mapping untuk ANGGOTAKU (kasus BMT Bakti Huria)
set -u
export REA_JADX_MCP_JAR=/home/ubuntu/.local/share/rea/jadx-headless-mcp-0.7.1-all.jar
APK=/home/ubuntu/.hermes/cache/documents/doc_82d8408fc891_ANGGOTAKU.apk
OUT=/home/ubuntu/penyidikan/analisis/bakti-huria-2026/rea
cd "$OUT"
REA="npx -y rea-agents@6.4.0"

classes=(
  "com.baktihuria.mobilebmt.anggotaku.SplashActivity"
  "com.baktihuria.mobilebmt.anggotaku.ControllerActivity"
  "com.baktihuria.mobilebmt.anggotaku.utils.MyVariable"
  "com.baktihuria.mobilebmt.anggotaku.registrasi.PreRegistrasiActivity"
  "com.baktihuria.mobilebmt.anggotaku.registrasi.IsiFormulirActivity"
  "com.baktihuria.mobilebmt.anggotaku.registrasi.AktivasiActivity"
  "com.baktihuria.mobilebmt.anggotaku.registrasi.LupaPin"
  "com.baktihuria.mobilebmt.anggotaku.dashboard.akun.ForwardSMS"
  "com.baktihuria.mobilebmt.anggotaku.notification.MyFirebaseMessagingService"
)
i=0
for c in "${classes[@]}"; do
  i=$((i+1))
  f=$(printf "10-class-%02d-%s.yaml" "$i" "$(basename "$c")")
  $REA inspect-android-class "$APK" "$c" > "$f" 2>"$f.err"
  echo "DONE class $c -> $f ($(wc -c <"$f") bytes)"
done

for c in "com.baktihuria.mobilebmt.anggotaku.registrasi.AktivasiActivity" \
         "com.baktihuria.mobilebmt.anggotaku.utils.MyVariable" \
         "com.baktihuria.mobilebmt.anggotaku.SplashActivity"; do
  f=$(printf "20-xref-%s.yaml" "$(basename "$c")")
  $REA trace-android-references "$APK" "$c" > "$f" 2>"$f.err"
  echo "DONE xref $c -> $f ($(wc -c <"$f") bytes)"
done
echo "ALL DONE"
