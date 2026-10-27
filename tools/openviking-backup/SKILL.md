---
name: openviking-backup
description: "Use when backing up, restoring, or validating OpenViking storage (memories, vector index) on the local server."
version: 1.0.0
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [openviking, backup, restore, memory, cron, watchdog]
---

# OpenViking Backup & Restore

Backup dan restore storage OpenViking lokal (`~/.openviking/data`): memori
markdown, indeks vektor, dan SQLite queue/usage-audit.

## Kenapa filesystem, bukan `ov backup`

`ov backup` dan `ov export` **menolak jalan** di server mode `dev`:

```
[PERMISSION_DENIED] Admin API requires api_key mode with root_api_key configured.
Development mode does not support account or user management.
```

Keduanya butuh `server.auth_mode = "api_key"` + `root_api_key` di `ov.conf`.
Server lokal yang hanya bind `127.0.0.1` tidak butuh auth, jadi jalur
filesystem dipakai — tanpa auth, dan menangkap data yang sama.

## Isi storage (peta)

| Path | Isi | Nilai |
|------|-----|-------|
| `data/viking/` | memori markdown (AGFS) | **Tidak tergantikan** |
| `data/vectordb/` | indeks vektor | Bisa dibangun ulang (`ov reindex`) |
| `data/_system/queue/queue.db` | antrean async (SQLite) | Rendah |
| `data/_system/usage_audit/*.sqlite3` | audit pemakaian (SQLite) | Rendah |

## Pakai

```bash
# Jalankan backup manual
python3 ~/penyidikan/tools/openviking-backup/backup.py

# Opsi
python3 .../backup.py --dest ~/backups/openviking --keep 14 --quiet --no-queue-wait
```

Wrapper cron (pola watchdog — diam kalau sukses, berisik kalau gagal,
heartbeat tiap Minggu):

```bash
bash ~/penyidikan/tools/openviking-backup/run-backup.sh
```

Dipasang sebagai cron Hermes: job `Backup Harian OpenViking`, `no_agent`,
harian 02:00 WITA, script `~/.hermes/scripts/openviking-backup.sh`
(dispatcher tipis → implementasi kanonik di `~/penyidikan/tools/`).

## Aturan konsistensi

- **SQLite wajib lewat `sqlite3` backup API**, bukan `cp`. Server memegang DB
  terbuka dengan WAL aktif; `cp` bisa menghasilkan snapshot robek. `backup.py`
  sudah memakai `.backup()`.
- **`viking/` aman disalin** sebagai file biasa.
- **Drain antrean dulu** (`ov wait`) supaya tidak memotret saat penulisan;
  dibungkus best-effort agar kegagalan drain tidak menggagalkan backup.
- **Redaksi rahasia.** `ov.conf` disalin dengan `api_key` diganti
  `<REDACTED>`; arsip bisa berpindah tempat, API key tidak boleh ikut.
  Arsip dan direktori backup bermode `0600`/`0700`.

## Verifikasi backup

```bash
cd ~/backups/openviking && sha256sum -c openviking-*.tar.gz.sha256
tar -tzf openviking-<stamp>.tar.gz | wc -l
```

## Prosedur restore penuh

```bash
systemctl --user stop openviking
mv ~/.openviking/data ~/.openviking/data.broken
tar -xzf openviking-<stamp>.tar.gz -C /tmp/ov-restore
cp -a /tmp/ov-restore/data ~/.openviking/data
systemctl --user start openviking
ov health && ov status
ov tree viking://user/default/memories/ -L 4 -o json | grep -c rel_path
```

Isi ulang `api_key` di `~/.openviking/ov.conf` setelah restore (di-redact di arsip).

**Restore memori saja** (indeks dibangun ulang):

```bash
systemctl --user stop openviking
rm -rf ~/.openviking/data/viking
cp -a /tmp/ov-restore/data/viking ~/.openviking/data/viking
systemctl --user start openviking
ov reindex viking://user/default/memories
```

## Pitfalls

- **`storage.workspace` default `./data` relatif CWD.** Kalau `openviking-server`
  dijalankan dengan cwd di dalam folder git, database runtime mendarat di repo
  dan ikut ter-commit. Selalu patok absolut di `ov.conf`, dan blokir `data/` di
  `.gitignore` repo sebagai jaring pengaman.
- **Hitung dulu file sebelum percaya restore.** `MANIFEST.json` di dalam arsip
  mencatat `counts.viking`; bandingkan dengan hasil `ov tree`. Backup yang
  "berhasil" tapi berisi 0 memori harus dianggap gagal — `backup.py` menolak
  menulis arsip kalau `data/viking` tidak ada.
- **Ada lebih dari satu direktori `data`.** Menjalankan server manual dan lewat
  systemd dengan cwd berbeda menghasilkan dua workspace. Cari yang asli dengan
  `find / -path "*/memories/*" -name "*.md"` sebelum memindah atau menghapus.
- **`ov task list -o json` mencetak baris `cmd: ...` sebelum JSON** — buang baris
  pertama sebelum `json.loads`.
- **Backup ≠ git sync vault.** Arsip `.tar.gz` biner tidak masuk repo vault;
  simpan di `~/backups/` dan cukup mirror *script*-nya ke `~/penyidikan/tools/`.
