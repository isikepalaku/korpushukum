#!/usr/bin/env python3
"""
build_manifest.py
=================
Membangun dan memperbarui 90-log/manifest.jsonl dari seluruh berkas di:
  - 10-peraturan/
  - 20-putusan/

Setiap baris memuat metadata dokumen, relasi graf, daftar seksi (heading & anchor),
dan hash sha256 berkas untuk kebutuhan sinkronisasi inkremental (RAG/OpenViking).
"""

import os
import re
import json
import hashlib
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = ROOT / "90-log"
MANIFEST_PATH = LOG_DIR / "manifest.jsonl"

HEAD_RE = re.compile(r"^(#{1,4})\s+(.+?)(?:\s+\^([A-Za-z0-9-]+))?\s*$")


def parse_doc(file_path: Path):
    content = file_path.read_text(encoding="utf-8")
    fm = {}
    body = content
    if content.startswith("---"):
        end_idx = content.find("\n---", 3)
        if end_idx != -1:
            try:
                fm = yaml.safe_load(content[3:end_idx]) or {}
            except Exception:
                pass
            body = content[end_idx + 4:]

    # Hitung sections
    stack = {}
    sections = []
    buf = []

    def flush():
        if not buf:
            return
        path = " > ".join(stack[k] for k in sorted(stack) if stack.get(k)) or "(pembuka)"
        text_str = "".join(buf).strip()
        sections.append({
            "path": path,
            "anchor": cur.get("anchor"),
            "chars": len(text_str)
        })
        buf.clear()

    cur = {"title": "", "anchor": None, "level": 0}
    for line in body.split("\n"):
        m = HEAD_RE.match(line)
        if m:
            flush()
            lvl = len(m.group(1))
            stack = {k: v for k, v in stack.items() if k < lvl}
            stack[lvl] = m.group(2).strip()
            cur = {"title": m.group(2).strip(), "anchor": m.group(3), "level": lvl}
        else:
            buf.append(line + "\n")
    flush()

    file_sha256 = hashlib.sha256(content.encode("utf-8")).hexdigest()
    rel_path = file_path.relative_to(ROOT).as_posix()

    entry = {
        "id": fm.get("id", file_path.stem),
        "jenis": fm.get("jenis", ""),
        "nomor": fm.get("nomor", ""),
        "tahun": fm.get("tahun", ""),
        "judul": fm.get("judul", file_path.stem),
        "judul_singkat": fm.get("judul_singkat", ""),
        "status": fm.get("status", "berlaku"),
        "bidang": fm.get("bidang", []),
        "kelengkapan": fm.get("kelengkapan", "lengkap"),
        "verifikasi": fm.get("verifikasi", "belum"),
        "file": rel_path,
        "sumber": fm.get("sumber", ""),
        "relasi": {
            "mencabut": fm.get("mencabut", []),
            "dicabut_oleh": fm.get("dicabut_oleh", []),
            "mengubah": fm.get("mengubah", []),
            "diubah_oleh": fm.get("diubah_oleh", []),
            "terkait": fm.get("terkait", [])
        },
        "chars": len(content),
        "sections": sections,
        "sha256": file_sha256
    }
    return entry


def run():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    files = []
    for folder in ["10-peraturan", "20-putusan"]:
        p = ROOT / folder
        if p.exists():
            files.extend(sorted(p.rglob("*.md")))

    entries = []
    for f in files:
        try:
            entry = parse_doc(f)
            entries.append(entry)
        except Exception as e:
            print(f"[!] Gagal memproses {f.name}: {e}")

    # Tulis manifest.jsonl
    with open(MANIFEST_PATH, "w", encoding="utf-8") as out:
        for entry in entries:
            out.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"[OK] Berhasil memperbarui {MANIFEST_PATH} dengan {len(entries)} dokumen.")


if __name__ == "__main__":
    run()

