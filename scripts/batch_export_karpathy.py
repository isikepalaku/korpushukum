#!/usr/bin/env python3
"""
batch_export_karpathy.py
========================
Mengekspor seluruh dokumen terpartisi (72 peraturan) dari 10-peraturan/
ke format Karpathy LLM-Wiki:
  - 02_LEGISLATION/<KODE_DOKUMEN>/Pasal_<NO>.md (terjahit Batang Tubuh + Penjelasan)
  - 01_INDEX_MOC/_Index_<KODE_DOKUMEN>.md (MOC daftar ringkas per pasal)
  - 01_INDEX_MOC/_MASTER_INDEX.md (Master MOC seluruh regulasi)
"""

import os
import sys
import re
import glob
import time
from pathlib import Path
import yaml

# Import parser inti
sys.path.insert(0, str(Path(__file__).resolve().parent))
from docling_legal_parser import IndonesianLegalParser

VAULT_ROOT = Path(__file__).resolve().parent.parent


def clean_code_id(raw_id: str) -> str:
    """Mengubah ID seperti 'UU 1/2024' atau 'POJK 18/POJK.03/2017' menjadi slug aman untuk folder."""
    clean = re.sub(r"[/\\.\s]+", "_", raw_id.strip()).strip("_")
    return clean


def run_batch_export():
    print("=" * 70)
    print("[*] MEMULAI BATCH EXPORT KARPATHY LEGAL WIKI")
    print("=" * 70)

    start_time = time.time()
    peraturan_files = glob.glob(str(VAULT_ROOT / "10-peraturan/**/*.md"), recursive=True)

    # Filter hanya dokumen yang sudah 'terpartisi'
    target_docs = []
    for fpath_str in peraturan_files:
        fpath = Path(fpath_str)
        try:
            content = fpath.read_text(encoding="utf-8")
            if content.startswith("---"):
                end_fm = content.find("\n---", 3)
                if end_fm != -1:
                    fm = yaml.safe_load(content[3:end_fm])
                    if isinstance(fm, dict) and fm.get("struktur_teks") == "terpartisi":
                        target_docs.append((fpath, fm))
        except Exception as e:
            continue

    print(f"[*] Ditemukan {len(target_docs)} dokumen berstatus 'terpartisi'.")

    out_root = VAULT_ROOT
    moc_dir = out_root / "01_INDEX_MOC"
    leg_dir = out_root / "02_LEGISLATION"
    moc_dir.mkdir(parents=True, exist_ok=True)
    leg_dir.mkdir(parents=True, exist_ok=True)

    sukses = 0
    gagal = 0
    total_pasal = 0
    master_index_entries = []

    for idx, (fpath, fm) in enumerate(target_docs, 1):
        raw_id = str(fm.get("id", fpath.stem))
        code_id = clean_code_id(raw_id)
        nama_resmi = str(fm.get("judul", fpath.stem))
        judul_singkat = str(fm.get("judul_singkat", fpath.stem))
        nomor = fm.get("nomor")
        tahun = fm.get("tahun")
        bidang = fm.get("bidang", ["umum"])
        bidang_str = bidang[0] if isinstance(bidang, list) and bidang else str(bidang)

        print(f"[{idx}/{len(target_docs)}] Memproses: {raw_id} — {judul_singkat}...", end="", flush=True)

        try:
            parser = IndonesianLegalParser(
                source_path=str(fpath),
                kode_uu=code_id,
                nama_resmi=nama_resmi,
                judul_singkat=judul_singkat,
                nomor=nomor,
                tahun=tahun,
                bidang=bidang_str,
                is_pdf=False
            )
            parser.load_document()
            parser.split_sections()
            parser.parse_pasal()
            parser.parse_and_stitch_penjelasan()

            num_pasal = len(parser.pasal_dict)
            if num_pasal > 0:
                parser.export_atomic_mode(str(out_root))
                sukses += 1
                total_pasal += num_pasal
                print(f" OK ({num_pasal} pasal)")

                master_index_entries.append({
                    "id": raw_id,
                    "code": code_id,
                    "judul": nama_resmi,
                    "singkat": judul_singkat,
                    "bidang": bidang_str,
                    "pasal_count": num_pasal
                })
            else:
                print(" LEWATI (0 pasal terdeteksi)")
                gagal += 1

        except Exception as e:
            print(f" GAGAL ({e})")
            gagal += 1

    # Buat Master Index MOC
    print("\n[*] Membuat _MASTER_INDEX.md...")
    master_lines = [
        "---",
        "id: MASTER_INDEX_MOC",
        "judul: \"Master Map of Content - Korpus Hukum Indonesia\"",
        "type: master-moc",
        "tags: [moc, master, hukum]",
        "last_updated: " + time.strftime("%Y-%m-%d"),
        "---\n",
        "# Master Map of Content (Karpathy Legal Wiki)\n",
        f"> Indeks hierarkis seluruh peraturan ({len(master_index_entries)} peraturan, {total_pasal:,} pasal atomik).\n",
        "Gunakan berkas ini untuk *retrieval 2 tahap* (Level 1: Pilih UU dari tabel di bawah, Level 2: Baca MOC UU terkait).\n",
        "## Daftar Peraturan & Indeks MOC\n",
        "| ID Regulasi | Judul Singkat | Bidang | Jumlah Pasal | Map of Content (MOC) |",
        "|---|---|---|:---:|---|"
    ]

    # Urutkan berdasarkan ID
    master_index_entries.sort(key=lambda x: x["id"])
    for item in master_index_entries:
        moc_link = f"[[_Index_{item['code']}]]"
        master_lines.append(
            f"| **{item['id']}** | {item['singkat']} | `{item['bidang']}` | {item['pasal_count']} | {moc_link} |"
        )

    master_file = moc_dir / "_MASTER_INDEX.md"
    master_file.write_text("\n".join(master_lines), encoding="utf-8")

    elapsed = time.time() - start_time
    print("=" * 70)
    print(f"[OK] BATCH EXPORT SELESAI DALAM {elapsed:.2f} DETIK")
    print(f"    - Berhasil diekspor : {sukses} peraturan")
    print(f"    - Gagal / Kosong    : {gagal} peraturan")
    print(f"    - Total Pasal Atomik: {total_pasal:,} file markdown di 02_LEGISLATION/")
    print(f"    - Total Indeks MOC  : {sukses} file di 01_INDEX_MOC/")
    print(f"    - Master Index      : {master_file}")
    print("=" * 70)


if __name__ == "__main__":
    run_batch_export()
