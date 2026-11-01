#!/usr/bin/env python3
"""
pipeline_orchestrator.py
========================
Orchestrator Otomatis untuk Korpus Hukum Indonesia (UU-KB & Karpathy LLM-Wiki).
Menangani:
  1. Validasi duplikasi (Skip jika sudah ada, Tambah jika belum ada, Force overwrite).
  2. Ekstraksi otomatis metadata (Jenis, Nomor, Tahun, Judul, Relasi Mengubah/Mencabut).
  3. Parsing deterministik PDF/MD via Docling + Regex Stitcher.
  4. Pengelompokan berkas ke folder hierarki (10-peraturan/ & 02_LEGISLATION/).
  5. Manajemen siklus hidup norma: Memberi mark simetris 'diubah' / 'dicabut' pada peraturan terdahulu.
  6. Pembaruan otomatis MOC Kategori (40-kategori/) dan Append Audit Log (90-log/log.md).
"""

import os
import sys
import re
import argparse
import hashlib
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import yaml

# Import parser inti
from docling_legal_parser import IndonesianLegalParser

VAULT_ROOT = Path(__file__).resolve().parent.parent

FOLDER_MAPPING = {
    "UU": "10-peraturan/01-undang-undang",
    "PERPPU": "10-peraturan/02-perppu",
    "PP": "10-peraturan/03-peraturan-pemerintah",
    "PERPRES": "10-peraturan/04-peraturan-presiden",
    "PERMEN": "10-peraturan/05-peraturan-menteri",
    "PERMENKUMHAM": "10-peraturan/05-peraturan-menteri",
    "PERMENDAGRI": "10-peraturan/05-peraturan-menteri",
    "PERMENKOMINFO": "10-peraturan/05-peraturan-menteri",
    "PERMENKOMDIGI": "10-peraturan/05-peraturan-menteri",
    "PERMENKOP": "10-peraturan/05-peraturan-menteri",
    "KEPMEN": "10-peraturan/05-peraturan-menteri",
    "KEPMENKOMDIGI": "10-peraturan/05-peraturan-menteri",
    "INSTRUKSI": "10-peraturan/05-peraturan-menteri",
    "POJK": "10-peraturan/06-peraturan-ojk",
    "SEOJK": "10-peraturan/06-peraturan-ojk",
    "PBI": "10-peraturan/07-peraturan-bi",
    "PADG": "10-peraturan/07-peraturan-bi",
    "SEBI": "10-peraturan/07-peraturan-bi",
    "PERKAP": "10-peraturan/08-peraturan-polri",
    "PERPOL": "10-peraturan/08-peraturan-polri",
    "SE-KAPOLRI": "10-peraturan/08-peraturan-polri",
    "INPRES": "10-peraturan/09-instrumen-lain",
    "SKB": "10-peraturan/09-instrumen-lain",
    "JUKRAH": "10-peraturan/09-instrumen-lain",
    "PUTUSAN-MK": "20-putusan/01-mahkamah-konstitusi",
    "PUTUSAN": "20-putusan/02-pengadilan",
}


def compute_file_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def scan_existing_vault_ids(root_dir: Path) -> Dict[str, Path]:
    """Memindai seluruh dokumen dalam vault untuk membuat indeks ID -> FilePath."""
    id_map = {}
    for sub in ["10-peraturan", "20-putusan"]:
        search_path = root_dir / sub
        if not search_path.exists():
            continue
        for md_file in search_path.rglob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8")
                if content.startswith("---"):
                    end_fm = content.find("\n---", 3)
                    if end_fm != -1:
                        fm = yaml.safe_load(content[3:end_fm])
                        if isinstance(fm, dict) and "id" in fm:
                            clean_id = str(fm["id"]).strip().upper()
                            id_map[clean_id] = md_file
            except Exception:
                continue
    return id_map


def extract_metadata_heuristics(sample_text: str, filename: str) -> Dict[str, Any]:
    """Mengekstraksi metadata dokumen secara otomatis dari teks pembuka dan nama berkas."""
    meta = {
        "jenis": "UU",
        "nomor": 1,
        "tahun": date.today().year,
        "id": "",
        "judul": "",
        "judul_singkat": "",
        "bidang": "umum",
        "mengubah": [],
        "mencabut": []
    }

    # 1. Deteksi Jenis
    for j in sorted(FOLDER_MAPPING.keys(), key=len, reverse=True):
        if re.search(rf"\b{j}\b", filename, re.I) or re.search(rf"\b{j}\b", sample_text[:1000], re.I):
            meta["jenis"] = j
            break

    # 2. Deteksi Nomor dan Tahun
    m_no_thn = re.search(r"(?:NOMOR|NO\.?)\s*(\d+)\s+TAHUN\s+(\d{4})", sample_text[:2000], re.I)
    if not m_no_thn:
        m_no_thn = re.search(r"(\d+)[-_](\d{4})", filename)

    if m_no_thn:
        meta["nomor"] = int(m_no_thn.group(1))
        meta["tahun"] = int(m_no_thn.group(2))

    meta["id"] = f"{meta['jenis']} {meta['nomor']}/{meta['tahun']}".upper()

    # 3. Deteksi Judul
    m_tentang = re.search(r"(?im)^\s*TENTANG\s*\n+([^\n]+(?:\n[^\n]+){1,3})", sample_text[:3000])
    if m_tentang:
        j_raw = m_tentang.group(1).replace("\n", " ").strip()
        meta["judul"] = re.sub(r"\s+", " ", j_raw)
    else:
        # Fallback dari nama file
        clean_name = Path(filename).stem
        parts = clean_name.split(" - ", 1)
        meta["judul"] = parts[1] if len(parts) > 1 else clean_name

    meta["judul_singkat"] = meta["judul"][:48].strip()

    # 4. Deteksi Bidang Hukum
    txt_lower = (sample_text[:4000] + " " + meta["judul"]).lower()
    if any(k in txt_lower for k in ["siber", "informasi dan transaksi elektronik", "ite", "data pribadi", "elektronik", "telekomunikasi"]):
        meta["bidang"] = "siber"
    elif any(k in txt_lower for k in ["bank", "perbankan", "keuangan", "ojk", "pasar modal", "asuransi", "pinjaman"]):
        meta["bidang"] = "keuangan"
    elif any(k in txt_lower for k in ["kuhp", "pidana", "tindak pidana", "kriminal", "kejahatan"]):
        meta["bidang"] = "pidana"
    elif any(k in txt_lower for k in ["lingkungan", "kehutanan", "tambang", "mineral", "batubara", "perikanan", "tipidter"]):
        meta["bidang"] = "tipidter"
    elif any(k in txt_lower for k in ["tanah", "agraria", "hak tanggungan", "pertanahan"]):
        meta["bidang"] = "pertanahan"

    # 5. Deteksi Relasi Perubahan (Mengubah)
    # Contoh: "PERUBAHAN KEDUA ATAS UNDANG-UNDANG NOMOR 11 TAHUN 2008..."
    m_ubah = re.finditer(r"(?:Perubahan.*?atas\s+)?(Undang-Undang|UU|Peraturan Pemerintah|PP)\s+(?:Nomor|No\.?)\s*(\d+)\s+Tahun\s+(\d{4})", sample_text[:3000], re.I)
    for u in m_ubah:
        u_jenis = "UU" if "undang" in u.group(1).lower() or "uu" == u.group(1).lower() else "PP"
        u_id = f"{u_jenis} {u.group(2)}/{u.group(3)}"
        if u_id != meta["id"] and u_id not in meta["mengubah"]:
            meta["mengubah"].append(u_id)

    # 6. Deteksi Relasi Pencabutan (Mencabut)
    # Biasanya ada di Ketentuan Penutup: "...dicabut dan dinyatakan tidak berlaku"
    m_cabut = re.finditer(r"(Undang-Undang|UU|Peraturan Pemerintah|PP)\s+(?:Nomor|No\.?)\s*(\d+)\s+Tahun\s+(\d{4})[^\n\.\;]*?(?:dicabut\s+dan\s+dinyatakan\s+tidak\s+berlaku)", sample_text[-4000:], re.I)
    for c in m_cabut:
        c_jenis = "UU" if "undang" in c.group(1).lower() or "uu" == c.group(1).lower() else "PP"
        c_id = f"{c_jenis} {c.group(2)}/{c.group(3)}"
        if c_id != meta["id"] and c_id not in meta["mencabut"]:
            meta["mencabut"].append(c_id)

    return meta


class LegalCorpusPipeline:
    def __init__(self, root_dir: Path = VAULT_ROOT, force: bool = False, mode: str = "both"):
        self.root_dir = root_dir
        self.force = force
        self.mode = mode
        self.existing_ids = scan_existing_vault_ids(self.root_dir)

    def mark_target_regulation(self, target_id: str, actor_id: str, relation_type: str):
        """
        Memberi mark simetris pada peraturan terdahulu:
          - relation_type 'diubah_oleh': ubah status ke 'diubah', tambahkan actor_id ke diubah_oleh.
          - relation_type 'dicabut_oleh': ubah status ke 'dicabut', tambahkan actor_id ke dicabut_oleh, sematkan callout peringatan.
        """
        target_path = self.existing_ids.get(target_id.upper())
        if not target_path or not target_path.exists():
            print(f"[!] Target {target_id} tidak ditemukan di dalam korpus saat ini (relasi dicatat di dokumen baru).")
            return

        try:
            content = target_path.read_text(encoding="utf-8")
            if not content.startswith("---"):
                return

            end_fm = content.find("\n---", 3)
            if end_fm == -1:
                return

            fm_raw = content[3:end_fm]
            body = content[end_fm + 4:]
            fm = yaml.safe_load(fm_raw)
            if not isinstance(fm, dict):
                return

            modified = False
            today_str = date.today().isoformat()

            if relation_type == "diubah_oleh":
                cur_diubah = fm.get("diubah_oleh") or []
                if isinstance(cur_diubah, str):
                    cur_diubah = [cur_diubah]
                if actor_id not in cur_diubah:
                    cur_diubah.append(actor_id)
                    fm["diubah_oleh"] = cur_diubah
                    if fm.get("status") == "berlaku":
                        fm["status"] = "diubah"
                    fm["last_updated"] = today_str
                    modified = True
                    print(f"[GRAPH] Peraturan {target_id} ditandai 'diubah' oleh {actor_id}")

            elif relation_type == "dicabut_oleh":
                cur_dicabut = fm.get("dicabut_oleh") or []
                if isinstance(cur_dicabut, str):
                    cur_dicabut = [cur_dicabut]
                if actor_id not in cur_dicabut:
                    cur_dicabut.append(actor_id)
                    fm["dicabut_oleh"] = cur_dicabut
                    fm["status"] = "dicabut"
                    fm["last_updated"] = today_str
                    modified = True

                    # Tambahkan callout peringatan di awal Batang Tubuh jika belum ada
                    if "TELAH DICABUT OLEH" not in body:
                        warning_banner = (
                            f"\n> [!CAUTION] PERATURAN INI TELAH DICABUT OLEH [[{actor_id}]]\n"
                            f"> Seluruh ketentuan di bawah ini sudah tidak berlaku secara hukum.\n\n"
                        )
                        # Sematkan setelah heading ## Batang Tubuh
                        if "## Batang Tubuh" in body:
                            body = body.replace("## Batang Tubuh\n", f"## Batang Tubuh\n{warning_banner}", 1)
                        else:
                            body = warning_banner + body

                    print(f"[GRAPH] Peraturan {target_id} ditandai 'DICABUT' oleh {actor_id}")

            if modified:
                new_file_text = "---\n" + yaml.dump(fm, sort_keys=False, allow_unicode=True) + "---\n" + body
                target_path.write_text(new_file_text, encoding="utf-8")

        except Exception as e:
            print(f"[!] Gagal memperbarui status relasi target {target_id}: {e}")

    def update_category_moc(self, bidang: str, doc_id: str, safe_name: str, jenis: str, status: str):
        """Menambahkan entri baru ke tabel statis 40-kategori/<bidang>.md."""
        cat_file = self.root_dir / "40-kategori" / f"{bidang.capitalize()}.md"
        if not cat_file.exists():
            return

        try:
            content = cat_file.read_text(encoding="utf-8")
            if f"[[{safe_name}" in content or f"| {doc_id} |" in content:
                return  # Sudah ada dalam tabel

            new_row = f"| {doc_id} | [[{safe_name}|{safe_name}]] | {jenis} | {status} |"
            
            # Cari posisi tabel daftar statis
            table_header = "| ID | Judul | Jenis | Status |"
            if table_header in content:
                parts = content.split(table_header, 1)
                sub_parts = parts[1].split("\n", 2)
                # sub_parts[0] = sisa baris header, sub_parts[1] = garis pembatas | --- |, sub_parts[2] = baris data
                updated_table = f"{parts[0]}{table_header}{sub_parts[0]}\n{sub_parts[1]}\n{new_row}\n{sub_parts[2]}"
                cat_file.write_text(updated_table, encoding="utf-8")
                print(f"[MOC] Menambahkan {doc_id} ke MOC 40-kategori/{bidang.capitalize()}.md")
        except Exception as e:
            print(f"[!] Gagal memperbarui MOC kategori: {e}")

    def append_audit_log(self, doc_id: str, action: str, details: str):
        """Mencatat aktivitas pipeline ke 90-log/log.md (append-only)."""
        log_file = self.root_dir / "90-log" / "log.md"
        if not log_file.exists():
            return

        today_str = date.today().isoformat()
        log_entry = (
            f"\n## [{today_str}] {action} | {doc_id}\n\n"
            f"- {details}\n"
            f"- Pipeline: Docling + Deterministic Regex Stitcher + Relational Graph Syncer.\n"
        )
        try:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
            print(f"[LOG] Mencatat perubahan ke 90-log/log.md")
        except Exception as e:
            print(f"[!] Gagal menulis log: {e}")

    def process_file(self, file_path: Path, manual_meta: Optional[Dict[str, Any]] = None) -> bool:
        """Memproses satu berkas PDF atau MD secara menyeluruh."""
        print(f"\n{'='*70}\n[*] Memeriksa berkas: {file_path.name}")

        is_pdf = file_path.suffix.lower() == ".pdf"

        # Pre-check instan dari nama berkas untuk mencegah konversi Docling yang mahal jika duplikat
        pre_inferred = extract_metadata_heuristics("", file_path.name)
        if manual_meta and "id" in manual_meta:
            pre_id = manual_meta["id"].upper()
        else:
            pre_id = pre_inferred["id"]

        if pre_id and pre_id in self.existing_ids and not self.force:
            existing_path = self.existing_ids[pre_id]
            if existing_path.exists():
                print(f"[SKIP (Fast)] Dokumen {pre_id} SUDAH ADA di korpus:")
                print(f"             -> {existing_path.relative_to(self.root_dir)}")
                print("             Gunakan flag --force jika ingin menimpa (overwrite).")
                return False

        # Baca sampel untuk deteksi metadata penuh
        if is_pdf:
            # Gunakan DocumentConverter Docling jika PDF
            temp_parser = IndonesianLegalParser(
                source_path=str(file_path),
                kode_uu="TEMP",
                nama_resmi="TEMP",
                is_pdf=True
            )
            raw_text = temp_parser.load_document()
        else:
            raw_text = file_path.read_text(encoding="utf-8")

        # Ekstraksi metadata otomatis
        inferred = extract_metadata_heuristics(raw_text, file_path.name)
        if manual_meta:
            inferred.update({k: v for k, v in manual_meta.items() if v is not None})

        doc_id = inferred["id"]
        print(f"[*] ID Dokumen: {doc_id} | Jenis: {inferred['jenis']} | Bidang: {inferred['bidang']}")

        # 1. Validasi Duplikasi
        existing_path = self.existing_ids.get(doc_id)
        if existing_path and existing_path.exists() and not self.force:
            print(f"[SKIP] Dokumen {doc_id} SUDAH ADA di korpus:")
            print(f"       -> {existing_path.relative_to(self.root_dir)}")
            print("       Gunakan flag --force jika ingin menimpa (overwrite).")
            return False

        # 2. Siapkan Parameter Parser
        kode_clean = doc_id.replace(" ", "_").replace("/", "_")
        parser = IndonesianLegalParser(
            source_path=str(file_path),
            kode_uu=kode_clean,
            nama_resmi=inferred["judul"],
            judul_singkat=inferred["judul_singkat"],
            nomor=inferred["nomor"],
            tahun=inferred["tahun"],
            bidang=inferred["bidang"],
            is_pdf=is_pdf
        )

        # 3. Eksekusi Parsing & Ekspor
        parser.execute(mode=self.mode, out_dir=str(self.root_dir))
        self.existing_ids[doc_id] = self.root_dir / FOLDER_MAPPING.get(inferred["jenis"], "10-peraturan/01-undang-undang") / f"{inferred['jenis']} {inferred['nomor']}-{inferred['tahun']} - {inferred['judul_singkat']}.md"

        # 4. Sinkronisasi Siklus Hidup Norma (Amandemen & Pencabutan)
        for target_ubah in inferred.get("mengubah", []):
            self.mark_target_regulation(target_ubah, doc_id, "diubah_oleh")

        for target_cabut in inferred.get("mencabut", []):
            self.mark_target_regulation(target_cabut, doc_id, "dicabut_oleh")

        # 5. Sinkronisasi MOC Kategori & Audit Log
        safe_title = f"{inferred['jenis']} {inferred['nomor']}-{inferred['tahun']} - {inferred['judul_singkat']}"
        self.update_category_moc(inferred["bidang"], doc_id, safe_title, inferred["jenis"], "berlaku")
        self.append_audit_log(
            doc_id=doc_id,
            action="ingest-auto",
            details=f"Inisiasi dokumen {doc_id} ({inferred['judul'][:60]}...). Mengubah: {inferred['mengubah']}, Mencabut: {inferred['mencabut']}."
        )

        print(f"[SUCCESS] Selesai memproses {doc_id}")
        return True

    def run_directory(self, input_dir: Path):
        """Memproses seluruh file PDF dalam suatu direktori."""
        if not input_dir.exists():
            raise FileNotFoundError(f"Direktori {input_dir} tidak ditemukan.")

        pdf_files = list(input_dir.glob("*.pdf")) + list(input_dir.glob("*.PDF"))
        print(f"[*] Ditemukan {len(pdf_files)} berkas PDF di {input_dir}")

        sukses, skip = 0, 0
        for pdf in pdf_files:
            try:
                res = self.process_file(pdf)
                if res:
                    sukses += 1
                else:
                    skip += 1
            except Exception as e:
                print(f"[ERROR] Gagal memproses {pdf.name}: {e}")

        print(f"\n{'='*70}\n[SUMMARY] Selesai: {sukses} berhasil diproses, {skip} dilewati (duplikat).")


def main():
    cli = argparse.ArgumentParser(
        description="Pipeline Otomatis Korpus Hukum Indonesia: Parsing, Deduplikasi, Klasifikasi, dan Lifecycle Tracking."
    )
    group = cli.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", help="Path ke satu berkas PDF atau MD.")
    group.add_argument("--dir", help="Path ke direktori berisi kumpulan PDF UU (misal: 30-sumber).")

    cli.add_argument("--force", action="store_true", help="Paksa parsing ulang meskipun dokumen sudah ada di korpus.")
    cli.add_argument("--mode", choices=["atomic", "uukb", "both"], default="both",
                     help="Target output: atomic (Karpathy-Wiki), uukb (AGENTS.md), atau both (default).")

    # Override opsional
    cli.add_argument("--code", help="Override Kode UU.")
    cli.add_argument("--name", help="Override Judul Resmi.")
    cli.add_argument("--bidang", help="Override Bidang Hukum (pidana, siber, keuangan, tipidter, pertanahan, umum).")

    args = cli.parse_args()

    manual_meta = {}
    if args.code:
        manual_meta["id"] = args.code
    if args.name:
        manual_meta["judul"] = args.name
    if args.bidang:
        manual_meta["bidang"] = args.bidang

    pipeline = LegalCorpusPipeline(force=args.force, mode=args.mode)

    if args.file:
        pipeline.process_file(Path(args.file), manual_meta=manual_meta if manual_meta else None)
    elif args.dir:
        pipeline.run_directory(Path(args.dir))


if __name__ == "__main__":
    main()

