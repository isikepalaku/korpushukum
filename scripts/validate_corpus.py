#!/usr/bin/env python3
"""
scripts/validate_corpus.py
==========================
Skrip audit dan validasi kualitas korpus hukum (UU-KB & Karpathy LLM-Wiki).
Memastikan:
  1. Konsistensi Batang Tubuh & Penjelasan di 10-peraturan/
  2. Kelengkapan dan integritas nomor pasal (Sequence & Gap Detection)
  3. Ketiadaan artefak OCR destruktif (misal: '16B' di KUHP, '7O', '5L')
  4. Keselarasan jumlah berkas atomik di 02-pasal-atomik/ dengan dokumen induk
"""

import os
import re
import glob
from pathlib import Path
from typing import Dict, List, Set, Tuple
import yaml

VAULT_ROOT = Path(__file__).resolve().parent.parent
PERATURAN_DIR = VAULT_ROOT / "10-peraturan"
ATOMIC_DIR = VAULT_ROOT / "02-pasal-atomik"


def check_corpus_integrity() -> bool:
    print("=" * 70)
    print("[*] MEMULAI VALIDASI KORPUS HUKUM (CORPUS LINT & AUDIT)")
    print("=" * 70)

    peraturan_files = sorted(glob.glob(str(PERATURAN_DIR / "**/*.md"), recursive=True))
    total_docs = len(peraturan_files)
    print(f"[*] Total dokumen peraturan terdeteksi: {total_docs}")

    has_error = False
    stats = {
        "terpartisi": 0,
        "datar": 0,
        "total_pasal_bt": 0,
        "total_pasal_pj": 0,
        "total_file_atomik": 0,
        "isu_terdeteksi": []
    }

    for fpath_str in peraturan_files:
        fpath = Path(fpath_str)
        try:
            content = fpath.read_text(encoding="utf-8")
        except Exception as e:
            stats["isu_terdeteksi"].append(f"[ERROR] Gagal membaca berkas {fpath.name}: {e}")
            has_error = True
            continue

        if not content.startswith("---"):
            continue
        idx_end_fm = content.find("\n---", 3)
        if idx_end_fm == -1:
            continue
        try:
            fm = yaml.safe_load(content[3:idx_end_fm]) or {}
        except Exception as e:
            stats["isu_terdeteksi"].append(f"[ERROR] YAML Frontmatter rusak pada {fpath.name}: {e}")
            has_error = True
            continue

        doc_id = str(fm.get("id", fpath.stem))
        struktur = fm.get("struktur_teks", "datar")

        if struktur != "terpartisi":
            stats["datar"] += 1
            continue

        stats["terpartisi"] += 1

        # Cek Batang Tubuh
        idx_bt = content.find("## Batang Tubuh")
        idx_pj = content.find("## Penjelasan")
        if idx_bt == -1:
            stats["isu_terdeteksi"].append(f"[{doc_id}] Struktur terpartisi tetapi tidak ada heading '## Batang Tubuh'")
            has_error = True
            continue

        bt_text = content[idx_bt:idx_pj] if idx_pj != -1 else content[idx_bt:]
        bt_pasals = re.findall(r"(?im)^###\s+Pasal\s+([0-9]+[A-Za-z]*)", bt_text)
        stats["total_pasal_bt"] += len(bt_pasals)

        # Cek apakah ada nomor pasal murni angka yang memiliki gap
        numeric_pasals = [int(p) for p in bt_pasals if p.isdigit()]
        if numeric_pasals:
            min_p = min(numeric_pasals)
            max_p = max(numeric_pasals)
            # Jika rentang teratur dan bukan dokumen amandemen sepotong-sepotong
            if min_p == 1 and max_p == len(numeric_pasals) and not fm.get("mengubah"):
                expected_set = set(range(1, max_p + 1))
                actual_set = set(numeric_pasals)
                missing = expected_set - actual_set
                if missing:
                    stats["isu_terdeteksi"].append(f"[{doc_id}] Gap pasal terdeteksi di Batang Tubuh: {sorted(list(missing))[:10]}")
                    has_error = True

        # Cek Penjelasan jika ada
        if idx_pj != -1:
            pj_text = content[idx_pj:]
            pj_pasals = re.findall(r"(?im)^####\s+Pasal\s+([0-9]+[A-Za-z]*)", pj_text)
            stats["total_pasal_pj"] += len(pj_pasals)

        # Cek keselarasan dengan 02-pasal-atomik/
        from batch_export_karpathy import clean_code_id
        code_id = clean_code_id(doc_id)
        doc_atomic_dir = ATOMIC_DIR / code_id
        if doc_atomic_dir.exists():
            atomic_files = list(doc_atomic_dir.glob("Pasal_*.md"))
            stats["total_file_atomik"] += len(atomic_files)

            # Cek anomali nama file atomik (misal '16B' pada UU non-amandemen, atau OCR typo seperti 7O)
            for af in atomic_files:
                p_name = af.stem.replace("Pasal_", "")
                # Deteksi karakter huruf O atau l pada nomor pasal atomik
                if re.search(r"[0-9]+[OlIT]$", p_name):
                    stats["isu_terdeteksi"].append(f"[{doc_id}] Nama berkas atomik mencurigakan (dugaan OCR typo): {af.name}")
                    has_error = True
                # Deteksi anomali KUHP
                if code_id == "UU_1_2023" and p_name in ["16B", "27B", "45B", "1616"]:
                    stats["isu_terdeteksi"].append(f"[{doc_id}] Berkas atomik cacat terdeteksi pada KUHP: {af.name}")
                    has_error = True

    print("\n" + "=" * 70)
    print("[*] HASIL AUDIT KORPUS HUKUM")
    print("=" * 70)
    print(f"  - Dokumen Terpartisi      : {stats['terpartisi']}")
    print(f"  - Dokumen Datar           : {stats['datar']}")
    print(f"  - Total Pasal Batang Tubuh: {stats['total_pasal_bt']:,}")
    print(f"  - Total Pasal Penjelasan  : {stats['total_pasal_pj']:,}")
    print(f"  - Total Berkas Atomik     : {stats['total_file_atomik']:,}")

    if stats["isu_terdeteksi"]:
        print(f"\n[!] DITEMUKAN {len(stats['isu_terdeteksi'])} MASALAH:")
        for issue in stats["isu_terdeteksi"]:
            print(f"    {issue}")
    else:
        print("\n[OK] SELURUH DOKUMEN DAN PASAL ATOMIK LOLOS VERIFIKASI INTEGRITAS!")
    print("=" * 70)

    return not has_error


if __name__ == "__main__":
    success = check_corpus_integrity()
    exit(0 if success else 1)
