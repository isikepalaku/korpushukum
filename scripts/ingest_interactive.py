#!/usr/bin/env python3
"""
ingest_interactive.py
=====================
CLI Interaktif / Otomatisasi untuk menambahkan dokumen regulasi baru
ke dalam korpushukum (E:\\Agent\\UU-KB) sesuai SOP resmi.

Menjalankan alur lengkap:
  1. Ekstraksi Docling GPU RapidOCR (scripts/docling_legal_parser.py)
  2. Manajemen Graf Siklus Hidup & MOC (scripts/pipeline_orchestrator.py)
  3. Pembaruan Manifest Dokumen (scripts/build_manifest.py)
  4. Pembaruan Chunks RAG Vektor (90-log/build_chunks.py)
  5. Sinkronisasi State Inkremental OpenViking (scripts/openviking_ingest.py)

Penggunaan:
  python scripts/ingest_interactive.py
  (atau dengan argumen langsung: python scripts/ingest_interactive.py --file "path/to/doc.pdf")
"""

import os
import sys
import re
import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCLING_PYTHON = r"C:\Users\ibrah\AppData\Roaming\uv\tools\docling\Scripts\python.exe"
SCRIPTS_DIR = ROOT / "scripts"


def run_command(cmd, desc=""):
    if desc:
        print(f"[*] {desc}...")
    res = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8", errors="ignore")
    if res.returncode != 0:
        print(f"[!] Error saat {desc}:")
        print(res.stderr or res.stdout)
        return False
    if res.stdout.strip():
        # Print summary output
        lines = res.stdout.strip().splitlines()
        for l in lines[-8:]:
            print(f"    {l}")
    return True


def auto_detect_metadata(filename: str):
    base = Path(filename).stem
    # Pola: JENIS NOMOR-TAHUN - JUDUL
    m = re.search(r"^(UU|PERPPU|PP|PERPRES|PERMEN\w*|KEPMEN\w*|POJK|SEOJK|PBI|PERKAP|PERPOL|INPRES|JUKRAH|PUTUSAN-MK)\s+([0-9A-Za-z\/\.-]+)[ -]+(\d{4})?(?:\s*-\s*(.+))?", base, re.I)
    jenis = ""
    nomor = ""
    tahun = ""
    judul_singkat = ""

    if m:
        jenis = m.group(1).upper()
        nomor_raw = m.group(2)
        tahun_raw = m.group(3) or ""
        judul_singkat = (m.group(4) or "").strip()

        if "-" in nomor_raw and not tahun_raw:
            parts = nomor_raw.split("-")
            nomor = parts[0]
            tahun = parts[1]
        else:
            nomor = nomor_raw
            tahun = tahun_raw
    else:
        # Coba deteksi nomor dan tahun bebas
        m_num = re.search(r"(?:No\.?|Nomor)\s*([0-9A-Za-z]+)", base, re.I)
        m_thn = re.search(r"(?:Tahun|Thn|\b20\d{2}\b|\b19\d{2}\b)", base, re.I)
        if m_num:
            nomor = m_num.group(1)
        if m_thn:
            thn_match = re.search(r"\b(19\d{2}|20\d{2})\b", base)
            if thn_match:
                tahun = thn_match.group(1)

    return jenis, nomor, tahun, judul_singkat


def main():
    parser = argparse.ArgumentParser(description="Ingest Regulasi Baru ke Korpus Hukum")
    parser.add_argument("--file", type=str, default="", help="Path file PDF atau Markdown sumber")
    parser.add_argument("--jenis", type=str, default="", help="Jenis regulasi (UU, PP, PERMEN, POJK, dll)")
    parser.add_argument("--nomor", type=str, default="", help="Nomor regulasi")
    parser.add_argument("--tahun", type=str, default="", help="Tahun regulasi")
    parser.add_argument("--name", type=str, default="", help="Judul lengkap resmi regulasi")
    parser.add_argument("--short-name", type=str, default="", help="Judul singkat (maks 52 karakter)")
    parser.add_argument("--bidang", type=str, default="", help="Bidang hukum (keuangan/pidana/siber/pertanahan/umum)")
    parser.add_argument("--auto-commit", action="store_true", help="Otomatis git commit dan push setelah selesai")
    args = parser.parse_args()

    print("=" * 70)
    print("   INGESTION PIPELINE REGULASI BARU — KORPUS HUKUM INDONESIA")
    print("=" * 70)

    file_path_str = args.file
    if not file_path_str:
        file_path_str = input("Masukkan path file regulasi (PDF / Markdown): ").strip().strip('"')

    file_path = Path(file_path_str).resolve()
    if not file_path.exists():
        print(f"[!] File tidak ditemukan: {file_path}")
        sys.exit(1)

    det_jenis, det_nomor, det_tahun, det_short = auto_detect_metadata(file_path.name)

    jenis = args.jenis or det_jenis
    if not jenis:
        jenis = input(f"Jenis Regulasi (UU/PP/PERPRES/PERMEN/POJK/PERPOL) [deteksi: {det_jenis}]: ").strip() or det_jenis

    nomor = args.nomor or det_nomor
    if not nomor:
        nomor = input(f"Nomor Regulasi [deteksi: {det_nomor}]: ").strip() or det_nomor

    tahun = args.tahun or det_tahun
    if not tahun:
        tahun = input(f"Tahun Regulasi [deteksi: {det_tahun}]: ").strip() or det_tahun

    short_name = args.short_name or det_short
    if not short_name:
        short_name = input(f"Judul Singkat (maks 52 karakter) [deteksi: {det_short}]: ").strip() or det_short

    full_name = args.name
    if not full_name:
        full_name = input("Judul Lengkap Resmi Peraturan: ").strip() or f"{jenis} {nomor} Tahun {tahun}"

    bidang = args.bidang
    if not bidang:
        bidang = input("Bidang Hukum (keuangan/pidana/siber/pertanahan/umum) [default: umum]: ").strip() or "umum"

    code_id = f"{jenis.upper()}_{nomor}_{tahun}"

    print("-" * 70)
    print("KONFIRMASI PARAMETER:")
    print(f"  File Sumber   : {file_path}")
    print(f"  Kode Dokumen  : {code_id}")
    print(f"  ID Regulasi   : {jenis.upper()} {nomor}/{tahun}")
    print(f"  Judul Singkat : {short_name}")
    print(f"  Bidang        : {bidang}")
    print("-" * 70)

    # Langkah 1: Jalankan Ekstraksi Docling / Markdown
    is_pdf = file_path.suffix.lower() == ".pdf"
    python_exec = DOCLING_PYTHON if (is_pdf and Path(DOCLING_PYTHON).exists()) else sys.executable

    cmd_parser = [
        python_exec,
        str(SCRIPTS_DIR / "docling_legal_parser.py"),
        "--code", code_id,
        "--name", full_name,
        "--short-name", short_name,
        "--nomor", str(nomor),
        "--tahun", str(tahun),
        "--bidang", bidang,
        "--mode", "both"
    ]
    if is_pdf:
        cmd_parser.extend(["--pdf", str(file_path)])
    else:
        cmd_parser.extend(["--md", str(file_path)])

    if not run_command(cmd_parser, f"Mengekstrak naskah hukum menggunakan Docling"):
        print("[!] Gagal pada tahap ekstraksi teks.")
        sys.exit(1)

    # Langkah 2: Perbarui Graf Relasi & Master Index
    cmd_manifest = [sys.executable, str(SCRIPTS_DIR / "build_manifest.py")]
    run_command(cmd_manifest, "Memperbarui 90-log/manifest.jsonl")

    cmd_chunks = [sys.executable, str(ROOT / "90-log" / "build_chunks.py")]
    run_command(cmd_chunks, "Memperbarui 90-log/chunks.jsonl.gz & Indeks Penjelasan")

    # Langkah 3: Sinkronisasi State Inkremental OpenViking
    cmd_viking = [sys.executable, str(SCRIPTS_DIR / "openviking_ingest.py"), "--sync"]
    run_command(cmd_viking, "Menyinkronkan state inkremental OpenViking")

    # Langkah 4: Git Commit & Push (bila diminta)
    commit_msg = f"feat(regulasi): add {jenis.upper()} {nomor}/{tahun} tentang {short_name}"
    print("=" * 70)
    print(f"[SUCCESS] Regulasi {jenis.upper()} {nomor}/{tahun} berhasil di-ingest ke korpushukum!")
    print(f"Lokasi Berkas:")
    print(f"  - Korpus Terpartisi : 10-peraturan/.../{jenis.upper()} {nomor}-{tahun} - {short_name}.md")
    print(f"  - Pasal Atomik      : 02_LEGISLATION/{code_id}/Pasal_*.md")
    print(f"  - Indeks MOC        : 01_INDEX_MOC/_Index_{code_id}.md")
    print("=" * 70)

    if args.auto_commit:
        run_command(["git", "add", "-A"], "Git add")
        run_command(["git", "commit", "-m", commit_msg], "Git commit")
        run_command(["git", "push", "origin", "main"], "Git push origin main")
        print("[OK] Perubahan telah berhasil di-push ke GitHub!")
    else:
        print("\nUntuk melakukan commit dan push ke GitHub, jalankan:")
        print(f'  git add -A; git commit -m "{commit_msg}"; git push origin main')


if __name__ == "__main__":
    main()

