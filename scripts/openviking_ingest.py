#!/usr/bin/env python3
"""
openviking_ingest.py
====================
Pipeline Ingestion Inkremental untuk OpenViking / Vector Database
berdasarkan 90-log/manifest.jsonl dan 90-log/chunks.jsonl.gz.

Cara Penggunaan:
  1. Cek perubahan inkremental (dry-run):
     python scripts/openviking_ingest.py --check

  2. Ekstrak payload chunk yang berubah untuk di-embed:
     python scripts/openviking_ingest.py --sync --out 90-log/to_embed.jsonl

  3. Paksa sinkronisasi ulang seluruh korpus:
     python scripts/openviking_ingest.py --sync --force
"""

import os
import sys
import json
import gzip
import argparse
from pathlib import Path
from typing import Dict, List, Set, Any

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "90-log" / "manifest.jsonl"
CHUNKS_PATH = ROOT / "90-log" / "chunks.jsonl.gz"
STATE_PATH = ROOT / "90-log" / "openviking_state.json"


def load_state() -> Dict[str, Any]:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"docs": {}, "synced_at": None, "total_chunks_synced": 0}


def save_state(state: Dict[str, Any]):
    from datetime import datetime
    state["synced_at"] = datetime.now().isoformat()
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def load_manifest() -> Dict[str, Dict[str, Any]]:
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(f"Manifest tidak ditemukan di {MANIFEST_PATH}. Jalankan scripts/build_manifest.py.")
    docs = {}
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                d = json.loads(line)
                docs[d["id"]] = d
    return docs


def compute_incremental_diff(force: bool = False):
    manifest = load_manifest()
    state = load_state()
    synced_docs = state.get("docs", {})

    added_doc_ids = []
    modified_doc_ids = []
    unchanged_doc_ids = []
    deleted_doc_ids = [doc_id for doc_id in synced_docs if doc_id not in manifest]

    for doc_id, doc in manifest.items():
        if force or doc_id not in synced_docs:
            added_doc_ids.append(doc_id)
        elif synced_docs[doc_id].get("sha256") != doc.get("sha256"):
            modified_doc_ids.append(doc_id)
        else:
            unchanged_doc_ids.append(doc_id)

    target_doc_ids = set(added_doc_ids + modified_doc_ids)
    return {
        "manifest": manifest,
        "state": state,
        "added": added_doc_ids,
        "modified": modified_doc_ids,
        "unchanged": unchanged_doc_ids,
        "deleted": deleted_doc_ids,
        "targets": target_doc_ids
    }


def get_incremental_chunks(target_doc_ids: Set[str], filter_cukup_jelas: bool = True) -> List[Dict[str, Any]]:
    if not target_doc_ids:
        return []

    if not CHUNKS_PATH.exists():
        raise FileNotFoundError(f"File chunks tidak ditemukan di {CHUNKS_PATH}. Jalankan python 90-log/build_chunks.py.")

    selected_chunks = []
    with gzip.open(CHUNKS_PATH, "rt", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            chunk = json.loads(line)
            doc_id = chunk.get("doc_id")

            if doc_id in target_doc_ids:
                # Sesuai aturan AGENTS.md: lewati penjelasan "Cukup jelas" dari embedding
                if filter_cukup_jelas and chunk.get("kind") == "penjelasan-pasal" and not chunk.get("substantive"):
                    continue
                selected_chunks.append(chunk)

    return selected_chunks


def main():
    parser = argparse.ArgumentParser(description="OpenViking Incremental Legal Chunks Ingestion Loader")
    parser.add_argument("--check", action="store_true", help="Cek dokumen & chunk yang berubah tanpa melakukan sync")
    parser.add_argument("--sync", action="store_true", help="Jalankan sinkronisasi dan catat state inkremental")
    parser.add_argument("--force", action="store_true", help="Paksa seluruh dokumen di-sync ulang (reset state)")
    parser.add_argument("--out", type=str, default="", help="Path file keluaran JSONL untuk payload embedding yang baru")
    args = parser.parse_args()

    diff = compute_incremental_diff(force=args.force)

    print("=" * 70)
    print("[*] STATUS INKREMENTAL KORPUS HUKUM (OPENVIKING)")
    print("=" * 70)
    print(f"Total Dokumen di Manifest : {len(diff['manifest'])}")
    print(f"  - Dokumen Baru          : {len(diff['added'])}")
    print(f"  - Dokumen Diubah        : {len(diff['modified'])}")
    print(f"  - Dokumen Tidak Berubah : {len(diff['unchanged'])} (Dilewati secara instan)")
    print(f"  - Dokumen Dihapus       : {len(diff['deleted'])}")
    print("-" * 70)

    if diff["added"]:
        print(f"Dokumen baru : {diff['added'][:10]}{'...' if len(diff['added']) > 10 else ''}")
    if diff["modified"]:
        print(f"Dokumen diubah: {diff['modified'][:10]}{'...' if len(diff['modified']) > 10 else ''}")

    chunks_to_embed = get_incremental_chunks(diff["targets"])
    print(f"[*] Jumlah chunk yang perlu di-embed: {len(chunks_to_embed):,} chunk.")

    if args.out and chunks_to_embed:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            for c in chunks_to_embed:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")
        print(f"[OK] Payload embedding berhasil ditulis ke: {out_path}")

    if args.sync:
        state = diff["state"]
        for doc_id, doc in diff["manifest"].items():
            state["docs"][doc_id] = {
                "sha256": doc.get("sha256"),
                "file": doc.get("file"),
                "status": doc.get("status")
            }
        for del_id in diff["deleted"]:
            state["docs"].pop(del_id, None)

        state["total_chunks_synced"] = len(chunks_to_embed)
        save_state(state)
        print(f"[OK] State inkremental OpenViking berhasil diperbarui di {STATE_PATH}")


if __name__ == "__main__":
    main()

