#!/usr/bin/env bash
# Cron wrapper untuk backup OpenViking.
#
# Pola watchdog: DIAM kalau sukses (stdout kosong → scheduler tidak kirim apa-apa),
# BERISIK kalau gagal. Ditambah heartbeat singkat tiap hari Minggu supaya ada
# bukti job masih hidup tanpa spam harian.
#
# Semua hasil selalu dicatat ke $LOG, jadi riwayat tetap ada walau stdout kosong.

set -uo pipefail

PY="${OPENVIKING_PY:-/home/ubuntu/venvs/openviking/bin/python}"
SCRIPT="${BACKUP_SCRIPT:-/home/ubuntu/penyidikan/tools/openviking-backup/backup.py}"
DEST="${BACKUP_DEST:-/home/ubuntu/backups/openviking}"
KEEP="${BACKUP_KEEP:-14}"
LOG="$DEST/backup.log"

mkdir -p "$DEST"

out="$("$PY" "$SCRIPT" --dest "$DEST" --keep "$KEEP" 2>&1)"
rc=$?

printf '[%s] rc=%s %s\n' "$(date -Is)" "$rc" "$out" >> "$LOG"

# Jaga log tetap kecil: simpan 500 baris terakhir.
if [ "$(wc -l < "$LOG")" -gt 500 ]; then
  tail -n 500 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
fi

if [ "$rc" -ne 0 ]; then
  echo "⚠️ Backup OpenViking GAGAL (rc=$rc)"
  echo
  echo "$out"
  echo
  echo "Data: $HOME/.openviking/data — log: $LOG"
  exit 0   # exit 0 agar teks di atas yang terkirim, bukan notice crash mentah
fi

# Heartbeat mingguan (Minggu) — bukti job masih hidup.
if [ "$(date +%u)" = "7" ]; then
  latest="$(ls -1t "$DEST"/openviking-*.tar.gz 2>/dev/null | head -n1)"
  count="$(ls -1 "$DEST"/openviking-*.tar.gz 2>/dev/null | wc -l)"
  echo "✅ Backup OpenViking mingguan: OK"
  echo
  echo "$out"
  [ -n "$latest" ] && echo && echo "Arsip terbaru: $(basename "$latest") ($(du -h "$latest" | cut -f1)) — total $count arsip tersimpan."
fi

exit 0
