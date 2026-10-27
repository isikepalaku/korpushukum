#!/usr/bin/env python3
"""Backup OpenViking local storage (memories + vector index) to a timestamped archive.

Why filesystem-level and not `ov backup`: `ov backup` / `ov export` require
server.auth_mode = "api_key" with a root_api_key. This server runs in `dev`
mode (bound to 127.0.0.1), so those commands return PERMISSION_DENIED.
Filesystem snapshot needs no auth and captures the same data.

Consistency: SQLite files are copied through the sqlite3 backup API (safe while
the server holds the DB open). The `viking/` tree holds the actual memory
markdown and is plain-file safe. The `vectordb/` index is copied best-effort and
can be rebuilt with `ov reindex` if it does not restore cleanly.

Usage:
    backup.py [--keep N] [--dest DIR] [--no-queue-wait] [--quiet]
Exit codes: 0 ok, 1 failure (message on stderr, so cron surfaces it).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tarfile
import tempfile
import time
from datetime import datetime
from pathlib import Path

OPENVIKING_HOME = Path(os.environ.get("OPENVIKING_HOME_DIR", Path.home() / ".openviking"))
DATA_DIR = Path(os.environ.get("OPENVIKING_DATA_DIR", OPENVIKING_HOME / "data"))
CONF_PATH = OPENVIKING_HOME / "ov.conf"
DEFAULT_DEST = Path.home() / "backups" / "openviking"
DEFAULT_KEEP = 14
ARCHIVE_MODE = 0o600


def log(msg: str, quiet: bool = False) -> None:
    line = f"[{datetime.now().isoformat(timespec='seconds')}] {msg}"
    if not quiet:
        print(line, flush=True)


def drain_queue(quiet: bool) -> None:
    """Best-effort wait for async processing so we do not snapshot mid-write."""
    exe = shutil.which("ov")
    if not exe:
        log("ov CLI not on PATH — skipping queue drain", quiet)
        return
    try:
        subprocess.run([exe, "wait"], capture_output=True, timeout=90, check=False)
        log("queue drained (best effort)", quiet)
    except subprocess.TimeoutExpired:
        log("queue drain timed out — continuing anyway", quiet)
    except Exception as e:  # never let draining block the backup
        log(f"queue drain skipped: {e}", quiet)


def copy_sqlite(src: Path, dst: Path) -> None:
    """Copy a live SQLite DB safely via the online backup API."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    source = sqlite3.connect(f"file:{src}?mode=ro", uri=True)
    try:
        target = sqlite3.connect(str(dst))
        try:
            source.backup(target)
        finally:
            target.close()
    finally:
        source.close()


def stage_tree(stage: Path, quiet: bool) -> dict[str, int]:
    """Copy storage into the staging dir. Returns per-section file counts."""
    counts: dict[str, int] = {}

    # 1. Memory filesystem (the irreplaceable part: markdown memories).
    viking_src = DATA_DIR / "viking"
    viking_dst = stage / "viking"
    if viking_src.is_dir():
        shutil.copytree(viking_src, viking_dst, symlinks=True)
        counts["viking"] = sum(1 for _ in viking_dst.rglob("*") if _.is_file())
    else:
        raise SystemExit(f"FATAL: {viking_src} missing — refusing to write an empty backup")

    # 2. SQLite databases via the backup API (queue, usage audit).
    counts["sqlite"] = 0
    for db in DATA_DIR.rglob("*.db"):
        copy_sqlite(db, stage / db.relative_to(DATA_DIR))
        counts["sqlite"] += 1
    for db in DATA_DIR.rglob("*.sqlite3"):
        copy_sqlite(db, stage / db.relative_to(DATA_DIR))
        counts["sqlite"] += 1

    # 3. Vector index — best effort; rebuildable with `ov reindex`.
    vdb_src = DATA_DIR / "vectordb"
    if vdb_src.is_dir():
        try:
            shutil.copytree(vdb_src, stage / "vectordb", symlinks=True)
            counts["vectordb"] = sum(1 for _ in (stage / "vectordb").rglob("*") if _.is_file())
        except Exception as e:
            log(f"vectordb copy incomplete ({e}) — rebuildable via `ov reindex`", quiet)
            counts["vectordb"] = 0

    # 4. Config, redacted: an archive may travel, the API key must not.
    if CONF_PATH.is_file():
        try:
            conf = json.loads(CONF_PATH.read_text())
            for section in ("vlm", "embedding"):
                if isinstance(conf.get(section), dict) and "api_key" in conf[section]:
                    conf[section]["api_key"] = "<REDACTED — re-add after restore>"
            if isinstance(conf.get("server"), dict) and "root_api_key" in conf["server"]:
                conf["server"]["root_api_key"] = "<REDACTED>"
            (stage / "ov.conf").write_text(json.dumps(conf, indent=2))
            counts["config"] = 1
        except Exception as e:
            log(f"ov.conf not included: {e}", quiet)
            counts["config"] = 0

    return counts


def write_restore_notes(stage: Path, counts: dict[str, int]) -> None:
    (stage / "RESTORE.md").write_text(
        "# OpenViking backup — cara restore\n\n"
        f"Dibuat: {datetime.now().isoformat(timespec='seconds')}\n\n"
        "## Isi arsip\n"
        f"- `viking/` — {counts.get('viking', 0)} file: memori markdown (bagian terpenting)\n"
        f"- `vectordb/` — {counts.get('vectordb', 0)} file: indeks vektor (bisa dibangun ulang)\n"
        f"- file SQLite — {counts.get('sqlite', 0)}: queue + usage audit\n"
        "- `ov.conf` — konfigurasi dengan `api_key` DI-REDACT (isi ulang manual)\n\n"
        "## Prosedur restore penuh\n"
        "```bash\n"
        "systemctl --user stop openviking\n"
        "mv ~/.openviking/data ~/.openviking/data.broken\n"
        "tar -xzf openviking-<tanggal>.tar.gz -C /tmp/ov-restore\n"
        "mv /tmp/ov-restore/data ~/.openviking/data\n"
        "systemctl --user start openviking && ov health && ov status\n"
        "```\n\n"
        "## Restore memori saja (tanpa indeks)\n"
        "```bash\n"
        "tar -xzf openviking-<tanggal>.tar.gz -C /tmp/ov-restore\n"
        "systemctl --user stop openviking\n"
        "rm -rf ~/.openviking/data/viking\n"
        "cp -a /tmp/ov-restore/data/viking ~/.openviking/data/viking\n"
        "systemctl --user start openviking\n"
        "ov reindex viking://user/default/memories\n"
        "```\n\n"
        "## Verifikasi setelah restore\n"
        "```bash\n"
        "ov tree viking://user/default/memories/ -L 4 -o json | grep -c rel_path\n"
        "ov status\n"
        "```\n\n"
        "Catatan: `storage.workspace` di `~/.openviking/ov.conf` HARUS absolut\n"
        "(`~/.openviking/data`). Default `./data` relatif CWD dan bisa mendarat di\n"
        "dalam folder git mana pun yang menjadi cwd server.\n"
    )
    counts["notes"] = 1


def prune(dest: Path, keep: int, quiet: bool) -> int:
    archives = sorted(dest.glob("openviking-*.tar.gz"), key=lambda p: p.stat().st_mtime, reverse=True)
    removed = 0
    for old in archives[keep:]:
        try:
            old.unlink()
            (dest / f"{old.name}.sha256").unlink(missing_ok=True)
            removed += 1
        except Exception as e:
            log(f"could not prune {old.name}: {e}", quiet)
    return removed


def main() -> int:
    ap = argparse.ArgumentParser(description="Backup OpenViking local storage.")
    ap.add_argument("--dest", default=str(DEFAULT_DEST))
    ap.add_argument("--keep", type=int, default=DEFAULT_KEEP)
    ap.add_argument("--no-queue-wait", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    quiet = args.quiet
    dest = Path(args.dest).expanduser()
    dest.mkdir(parents=True, exist_ok=True)
    os.chmod(dest, 0o700)

    if not DATA_DIR.is_dir():
        print(f"FATAL: {DATA_DIR} not found", file=sys.stderr)
        return 1

    if not args.no_queue_wait:
        drain_queue(quiet)

    stamp = datetime.now().strftime("%Y%m%d-%H%M")
    archive = dest / f"openviking-{stamp}.tar.gz"

    work = Path(tempfile.mkdtemp(prefix="ovbackup-"))
    try:
        stage = work / "data"
        stage.mkdir()
        counts = stage_tree(stage, quiet)
        write_restore_notes(stage, counts)

        manifest = {
            "created": datetime.now().isoformat(timespec="seconds"),
            "data_dir": str(DATA_DIR),
            "counts": counts,
            "total_files": sum(v for k, v in counts.items() if k != "notes"),
        }
        (stage / "MANIFEST.json").write_text(json.dumps(manifest, indent=2))

        # Deterministic-ish archive; no compression on already-compact blobs is
        # slower to write, so use gzip but let it work on the whole stage.
        with tarfile.open(archive, "w:gz") as tf:
            tf.add(stage, arcname="data")

        os.chmod(archive, ARCHIVE_MODE)
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        (dest / f"{archive.name}.sha256").write_text(f"{digest}  {archive.name}\n")

        size_mb = archive.stat().st_size / 1024 / 1024
        log(
            f"OK {archive.name} ({size_mb:.1f} MB, {manifest['total_files']} file, "
            f"viking={counts.get('viking', 0)}) sha256={digest[:16]}…",
            quiet,
        )
        removed = prune(dest, args.keep, quiet)
        if removed:
            log(f"pruned {removed} arsip lama (keep={args.keep})", quiet)
        return 0
    except Exception as e:
        print(f"FATAL: backup failed: {e}", file=sys.stderr)
        return 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
