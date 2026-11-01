#!/usr/bin/env python3
"""
normalize_unpartitioned.py
==========================
Memproses 41 berkas peraturan yang belum terpartisi di 10-peraturan/:
1. Mengidentifikasi berkas yang memiliki struktur pasal (Group 1 - ~25 regulasi).
2. Mempartisi ulang berkas menjadi standar UU-KB (## Batang Tubuh, ### Pasal X ^pasal-x, ## Penjelasan, ## Peta Penjelasan)
   dan mengupdate frontmatter menjadi struktur_teks: terpartisi, anchor_pasal: true.
3. Mengekspor langsung ke format Karpathy LLM-Wiki (02_LEGISLATION/ & 01_INDEX_MOC/).
4. Untuk dokumen non-pasal (Instruksi, Kepmen, SE, Inpres - ~10 regulasi):
   Menstandarkan frontmatter ke struktur_teks: datar, anchor_pasal: false sesuai AGENTS.md aturan 8.
5. Memperbarui _MASTER_INDEX.md.
"""

import os
import sys
import re
import glob
import time
from pathlib import Path
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from docling_legal_parser import IndonesianLegalParser
from batch_export_karpathy import clean_code_id

VAULT_ROOT = Path(__file__).resolve().parent.parent


def run_normalization():
    print("=" * 70)
    print("[*] MEMULAI NORMALISASI 41 DOKUMEN BELUM TERPARTISI")
    print("=" * 70)

    peraturan_files = glob.glob(str(VAULT_ROOT / "10-peraturan/**/*.md"), recursive=True)

    non_terpartisi = []
    for fpath_str in peraturan_files:
        fpath = Path(fpath_str)
        try:
            content = fpath.read_text(encoding="utf-8")
            if content.startswith("---"):
                end_fm = content.find("\n---", 3)
                if end_fm != -1:
                    fm = yaml.safe_load(content[3:end_fm])
                    if isinstance(fm, dict) and fm.get("struktur_teks") != "terpartisi":
                        non_terpartisi.append((fpath, fm, content[end_fm + 4:]))
        except Exception:
            continue

    print(f"[*] Ditemukan {len(non_terpartisi)} dokumen non-terpartisi.\n")

    berhasil_partisi = 0
    dijadikan_datar = 0
    pasal_baru_total = 0

    for idx, (fpath, fm, body) in enumerate(non_terpartisi, 1):
        raw_id = str(fm.get("id", fpath.stem))
        code_id = clean_code_id(raw_id)
        nama_resmi = str(fm.get("judul", fpath.stem))
        judul_singkat = str(fm.get("judul_singkat", fpath.stem))
        nomor = fm.get("nomor")
        tahun = fm.get("tahun")
        bidang = fm.get("bidang", ["umum"])
        bidang_str = bidang[0] if isinstance(bidang, list) and bidang else str(bidang)
        jenis = str(fm.get("jenis", "UU"))

        print(f"[{idx:02d}/{len(non_terpartisi)}] {raw_id:<20} | ", end="", flush=True)

        # Cek apakah memiliki pasal
        pasal_matches = re.findall(r"(?im)^#{0,6}\s*(?:\*\*)?Pasal\s+([0-9]+[A-Za-z]?)", body)
        
        if len(pasal_matches) >= 1:
            # Group 1: Mengandung pasal -> Lakukan partisi penuh
            try:
                parser = IndonesianLegalParser(
                    source_path=str(fpath),
                    kode_uu=code_id,
                    nama_resmi=nama_resmi,
                    judul_singkat=judul_singkat,
                    nomor=nomor,
                    tahun=tahun,
                    bidang=bidang_str,
                    jenis=jenis,
                    is_pdf=False
                )
                parser.load_document()
                parser.split_sections()
                parser.parse_pasal()
                parser.parse_and_stitch_penjelasan()

                num_pasal = len(parser.pasal_dict)
                if num_pasal > 0:
                    # 1. Update berkas di 10-peraturan/ (UU-KB Native in-place)
                    parser.export_uukb_mode(str(VAULT_ROOT), target_file_path=str(fpath))
                    # 2. Ekspor ke 02_LEGISLATION/ & 01_INDEX_MOC/ (Karpathy Wiki)
                    parser.export_atomic_mode(str(VAULT_ROOT))

                    berhasil_partisi += 1
                    pasal_baru_total += num_pasal
                    print(f"PARTISI SUKSES ({num_pasal} pasal)")
                else:
                    # Fallback jika gagal regex split
                    print("GAGAL SPLIT PASAL -> Jadikan Datar")
                    _mark_datar(fpath, fm, body)
                    dijadikan_datar += 1
            except Exception as e:
                print(f"ERROR: {e}")
                _mark_datar(fpath, fm, body)
                dijadikan_datar += 1
        else:
            # Group 2 / 3: Dokumen non-pasal (Instruksi, Kepmen, SE, Inpres, Ringkasan)
            _mark_datar(fpath, fm, body)
            dijadikan_datar += 1
            print("NON-PASAL -> Ditandai 'struktur_teks: datar'")

    print("\n" + "=" * 70)
    print("[*] MEMPERBARUI MASTER INDEX MOC...")
    from batch_export_karpathy import run_batch_export
    # Re-run batch export untuk meregenerasi _MASTER_INDEX.md lengkap
    run_batch_export()

    print("=" * 70)
    print(f"[OK] NORMALISASI SELESAI:")
    print(f"    - Berhasil dipartisi & diekspor atomik: {berhasil_partisi} regulasi")
    print(f"    - Dinormalisasi ke struktur_teks datar: {dijadikan_datar} instrumen")
    print(f"    - Tambahan pasal atomik               : {pasal_baru_total:,} pasal")
    print("=" * 70)


def _mark_datar(fpath: Path, fm: dict, body: str):
    """Menandai dokumen non-pasal sebagai struktur_teks: datar sesuai AGENTS.md aturan 8."""
    fm["struktur_teks"] = "datar"
    fm["anchor_pasal"] = False
    fm["penjelasan"] = "tidak"
    fm["penjelasan_normatif"] = False
    fm["last_updated"] = time.strftime("%Y-%m-%d")

    new_content = "---\n" + yaml.dump(fm, sort_keys=False, allow_unicode=True) + "---\n" + body
    fpath.write_text(new_content, encoding="utf-8")


if __name__ == "__main__":
    run_normalization()
