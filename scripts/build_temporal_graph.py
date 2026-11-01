#!/usr/bin/env python3
"""
scripts/build_temporal_graph.py
==============================
Membangun graf temporal dan keterhubungan amandemen antar-pasal atomik di 02-pasal-atomik/.
Menambahkan metadata frontmatter pada setiap berkas Pasal_<NO>.md:
  - status_berlaku: berlaku | diubah | dicabut
  - diamandemen_oleh: ["[[02-pasal-atomik/<KODE_BARU>/Pasal_<NO>|<ID_BARU> Pasal <NO>]]"]
  - mengamandemen: ["[[02-pasal-atomik/<KODE_LAMA>/Pasal_<NO>|<ID_LAMA> Pasal <NO>]]"]
"""

import os
import re
from pathlib import Path
import yaml

VAULT_ROOT = Path(".")
ATOMIC_DIR = VAULT_ROOT / "02-pasal-atomik"
PERATURAN_DIR = VAULT_ROOT / "10-peraturan"

def clean_code_id(raw_id: str) -> str:
    cleaned = raw_id.replace("/", "_").replace("-", "_").replace(" ", "_").replace(".", "_")
    return re.sub(r"_+", "_", cleaned).strip("_")

def load_doc_relations():
    doc_map = {} # code_id -> {id, file, mengubah, diubah_oleh, mencabut, dicabut_oleh, status}
    for p in PERATURAN_DIR.glob("**/*.md"):
        txt = p.read_text(encoding="utf-8")
        if not txt.startswith("---"):
            continue
        idx = txt.find("---", 3)
        if idx == -1:
            continue
        try:
            fm = yaml.safe_load(txt[3:idx])
            if isinstance(fm, dict):
                raw_id = str(fm.get("id", p.stem))
                code = clean_code_id(raw_id)
                doc_map[code] = {
                    "id": raw_id,
                    "file": p,
                    "status": fm.get("status", "berlaku"),
                    "mengubah": [clean_code_id(x) for x in fm.get("mengubah", [])],
                    "diubah_oleh": [clean_code_id(x) for x in fm.get("diubah_oleh", [])],
                    "mencabut": [clean_code_id(x) for x in fm.get("mencabut", [])],
                    "dicabut_oleh": [clean_code_id(x) for x in fm.get("dicabut_oleh", [])],
                }
        except Exception:
            continue
    return doc_map

def main():
    print("[*] Membaca relasi dokumen dari 10-peraturan/...")
    doc_map = load_doc_relations()
    print(f"[*] Terindeks {len(doc_map)} dokumen di doc_map.")
    
    # Kumpulkan seluruh folder di 02-pasal-atomik
    atomic_folders = [f for f in ATOMIC_DIR.iterdir() if f.is_dir()]
    print(f"[*] Ditemukan {len(atomic_folders)} folder regulasi di 02-pasal-atomik/.")

    # 1. Bangun peta amandemen antar folder: (folder_lama, pasal) -> (folder_baru, pasal, id_baru)
    # Dan sebaliknya: (folder_baru, pasal) -> (folder_lama, pasal, id_lama)
    amended_by_map = {} # (folder_lama, p_no) -> list of (folder_baru, p_no, id_baru)
    amends_map = {}     # (folder_baru, p_no) -> list of (folder_lama, p_no, id_lama)

    for code_baru, doc_info in doc_map.items():
        folder_baru = ATOMIC_DIR / code_baru
        if not folder_baru.exists():
            continue

        pasal_files_baru = list(folder_baru.glob("Pasal_*.md"))
        pasal_dict_baru = {}
        for pf in pasal_files_baru:
            m = re.match(r"Pasal_([0-9]+[A-Za-z]*)\.md", pf.name)
            if m:
                pasal_dict_baru[m.group(1).upper()] = (pf, m.group(1))

        # Jika dokumen ini mengubah dokumen lain
        for code_lama in doc_info["mengubah"]:
            folder_lama = ATOMIC_DIR / code_lama
            if not folder_lama.exists():
                # Coba cari variasi nama folder
                candidates = [f for f in atomic_folders if f.name.lower() == code_lama.lower()]
                if candidates:
                    folder_lama = candidates[0]
                else:
                    continue

            pasal_files_lama = list(folder_lama.glob("Pasal_*.md"))
            id_lama = doc_map.get(folder_lama.name, {}).get("id", folder_lama.name)
            id_baru = doc_info["id"]

            for pf_lama in pasal_files_lama:
                m_lama = re.match(r"Pasal_([0-9]+[A-Za-z]*)\.md", pf_lama.name)
                if not m_lama:
                    continue
                p_no = m_lama.group(1)
                p_no_upper = p_no.upper()

                if p_no_upper in pasal_dict_baru:
                    # Amandemen cocok per nomor pasal!
                    _, p_baru_actual = pasal_dict_baru[p_no_upper]
                    key_lama = (folder_lama.name, p_no)
                    key_baru = (folder_baru.name, p_baru_actual)

                    amended_by_map.setdefault(key_lama, []).append((folder_baru.name, p_baru_actual, id_baru))
                    amends_map.setdefault(key_baru, []).append((folder_lama.name, p_no, id_lama))

    print(f"[*] Terdeteksi {len(amended_by_map)} pasal terdahulu yang diamandemen.")
    print(f"[*] Terdeteksi {len(amends_map)} pasal amandemen yang mengamandemen pasal induk.")

    # 2. Update frontmatter di setiap berkas 02-pasal-atomik/
    total_updated = 0
    total_files = 0

    for folder in atomic_folders:
        code = folder.name
        doc_status = doc_map.get(code, {}).get("status", "berlaku")

        for pf in folder.glob("Pasal_*.md"):
            total_files += 1
            m = re.match(r"Pasal_([0-9]+[A-Za-z]*)\.md", pf.name)
            if not m:
                continue
            p_no = m.group(1)

            txt = pf.read_text(encoding="utf-8")
            if not txt.startswith("---"):
                continue
            idx = txt.find("---", 3)
            if idx == -1:
                continue

            try:
                fm = yaml.safe_load(txt[3:idx])
                if not isinstance(fm, dict):
                    continue
                body = txt[idx+3:]

                modified = False
                key = (code, p_no)

                # Cek amandemen oleh peraturan baru
                diamandemen = amended_by_map.get(key, [])
                mengamandemen = amends_map.get(key, [])

                # Tentukan status berlaku
                if diamandemen:
                    current_status = "diubah"
                elif doc_status in ["dicabut"]:
                    current_status = "dicabut"
                else:
                    current_status = "berlaku"

                diamandemen_links = [
                    f"[[02-pasal-atomik/{b_fold}/Pasal_{b_p}|{b_id} Pasal {b_p}]]"
                    for b_fold, b_p, b_id in diamandemen
                ]
                mengamandemen_links = [
                    f"[[02-pasal-atomik/{l_fold}/Pasal_{l_p}|{l_id} Pasal {l_p}]]"
                    for l_fold, l_p, l_id in mengamandemen
                ]

                if fm.get("status_berlaku") != current_status:
                    fm["status_berlaku"] = current_status
                    modified = True

                if fm.get("diamandemen_oleh") != diamandemen_links:
                    fm["diamandemen_oleh"] = diamandemen_links
                    modified = True

                if fm.get("mengamandemen") != mengamandemen_links:
                    fm["mengamandemen"] = mengamandemen_links
                    modified = True

                if modified:
                    new_txt = "---\n" + yaml.dump(fm, sort_keys=False, allow_unicode=True) + "---" + body
                    pf.write_text(new_txt, encoding="utf-8")
                    total_updated += 1

            except Exception as e:
                print(f"[!] Error processing {pf}: {e}")

    print("=" * 60)
    print(f"[OK] PEMBARUAN TEMPORAL GRAPH SELESAI")
    print(f"    - Total Berkas Diperiksa : {total_files:,}")
    print(f"    - Total Berkas Diperbarui: {total_updated:,}")
    print("=" * 60)

if __name__ == "__main__":
    main()

