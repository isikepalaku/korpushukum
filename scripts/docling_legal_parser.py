#!/usr/bin/env python3
"""
docling_legal_parser.py
=======================
Parser Dokumen Hukum Indonesia (Undang-Undang, Perppu, PP, dll.) berbasis Docling.
Mendukung DUA mode output (Hybrid):
  1. Mode 'atomic': Karpathy LLM-Wiki format (01-moc/_Index_<KODE>.md & 02-pasal-atomik/<KODE>/Pasal_<NO>.md)
     dengan Batang Tubuh dan Penjelasan Resmi yang dijahit (stitched) per pasal.
  2. Mode 'uukb': Format resmi Obsidian Korpus UU-KB (1 berkas terpartisi dengan anchor ^pasal-X dan
     ^penjelasan-pasal-X, siap di-ingest ke 10-peraturan/ dan diproses build_chunks.py).
  3. Mode 'both': Menghasilkan kedua format sekaligus.

Penggunaan:
  python scripts/docling_legal_parser.py --pdf 30-sumber/uu.pdf --code UU_1_2024 --name "UU No. 1 Tahun 2024"
  # atau jika markdown sudah dikonversi sebelumnya:
  python scripts/docling_legal_parser.py --md input.md --code UU_1_2024 --name "UU No. 1 Tahun 2024"
"""

import os
import sys
import re
import argparse
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import yaml

# Coba import Docling
try:
    from docling.document_converter import DocumentConverter
    HAS_DOCLING = True
except ImportError:
    DocumentConverter = None
    HAS_DOCLING = False


@dataclass
class PasalData:
    nomor: str
    batang_tubuh: str = ""
    penjelasan: str = "Cukup jelas."
    is_substantive: bool = False
    ringkasan_awal: str = ""


class IndonesianLegalParser:
    def __init__(
        self,
        source_path: str,
        kode_uu: str,
        nama_resmi: str,
        judul_singkat: Optional[str] = None,
        nomor: Optional[int] = None,
        tahun: Optional[int] = None,
        bidang: str = "pidana",
        jenis: str = "UU",
        is_pdf: bool = True
    ):
        self.source_path = Path(source_path)
        self.kode_uu = kode_uu.strip().replace(" ", "_")
        self.nama_resmi = nama_resmi.strip()
        self.judul_singkat = judul_singkat.strip() if judul_singkat else self._derive_short_name(self.nama_resmi)
        self.bidang = bidang.lower().strip()
        self.jenis = jenis.strip().upper()
        self.is_pdf = is_pdf

        # Infer nomor & tahun bila tidak diberikan
        self.nomor, self.tahun = self._infer_nomor_tahun(nomor, tahun, self.nama_resmi, self.kode_uu)

        self.raw_markdown = ""
        self.pembuka_raw = ""
        self.batang_tubuh_raw = ""
        self.penjelasan_raw = ""
        self.penjelasan_umum_raw = ""
        self.penjelasan_pasal_raw = ""
        self.pasal_dict: Dict[str, PasalData] = {}

    @staticmethod
    def _infer_nomor_tahun(nomor: Optional[int], tahun: Optional[int], name: str, code: str) -> Tuple[int, int]:
        n, t = nomor, tahun
        if n is None or t is None:
            # Cari dari teks misal "Nomor 1 Tahun 2024" atau "UU 1/2024"
            m = re.search(r"(?:Nomor|No\.?)\s*(\d+)\s+Tahun\s+(\d{4})", name, re.IGNORECASE)
            if m:
                n = n or int(m.group(1))
                t = t or int(m.group(2))
            else:
                m2 = re.search(r"(\d+)[/_](\d{4})", code)
                if m2:
                    n = n or int(m2.group(1))
                    t = t or int(m2.group(2))
        return n or 1, t or date.today().year

    @staticmethod
    def _derive_short_name(name: str) -> str:
        # Pangkas awalan umum
        clean = re.sub(r"^(?:Undang-Undang|UU)\s+(?:Republik Indonesia\s+)?(?:Nomor\s+\d+\s+Tahun\s+\d+\s+)?(?:tentang\s+)?", "", name, flags=re.I).strip()
        return clean[:50] if clean else name[:50]

    def load_document(self) -> str:
        """Memuat teks baik via Docling DocumentConverter (PDF) atau langsung dari Markdown."""
        if not self.source_path.exists():
            raise FileNotFoundError(f"File tidak ditemukan: {self.source_path}")

        if self.is_pdf or self.source_path.suffix.lower() == ".pdf":
            print(f"[*] Menjalankan Docling DocumentConverter pada: {self.source_path.name}...")
            if not HAS_DOCLING:
                raise RuntimeError(
                    "Pustaka 'docling' tidak ditemukan di environment ini.\n"
                    "Gunakan Python uv environment dengan Docling, misal:\n"
                    r'& "C:\Users\ibrah\AppData\Roaming\uv\tools\docling\Scripts\python.exe" scripts/docling_legal_parser.py ...'
                )
            converter = DocumentConverter()
            result = converter.convert(str(self.source_path))
            self.raw_markdown = result.document.export_to_markdown()
        else:
            print(f"[*] Membaca file Markdown langsung dari: {self.source_path.name}...")
            text = self.source_path.read_text(encoding="utf-8")
            if text.startswith("---"):
                end_fm = text.find("\n---", 3)
                if end_fm != -1:
                    text = text[end_fm + 4:].strip()
            self.raw_markdown = text

        return self.raw_markdown

    @staticmethod
    def normalize_legal_ocr(text: str) -> str:
        """Memperbaiki kesalahan OCR umum pada teks perundang-undangan Indonesia."""
        # Perbaiki variasi kata 'Pasal' akibat OCR
        text = re.sub(r"(?im)\b(?:Pasil|PasaT|Pasa1)\b", "Pasal", text)
        # Perbaiki typo OCR spesifik seperti 'Pasal2TA' -> 'Pasal 27A'
        text = re.sub(r"(?im)\bPasal\s*2TA\b", "Pasal 27A", text)
        # Perbaiki typo OCR Penjelasan
        text = re.sub(r"(?im)\bPASALDEMIPASAL\b", "PASAL DEMI PASAL", text)
        text = re.sub(r"(?im)^#{0,4}\s*il\.\s*PASAL", "## II. PASAL", text)
        text = re.sub(r"(?im)\bTET\\ITANG\b", "TENTANG", text)
        text = re.sub(r"(?im)\bTAHVN\b", "TAHUN", text)
        # Perbaiki 'Pasal' yang menempel langsung dengan angka: 'Pasal27' -> 'Pasal 27'
        text = re.sub(r"(?im)\bPasal(\d+[A-Za-z]?)\b", r"Pasal \1", text)
        # Perbaiki angka '8' yang sebenarnya huruf 'B' pada penomoran pasal sisipan
        text = re.sub(r"(?im)(^#*\s*(?:\*\*)?Pasal\s+16)8\b", r"\1B", text)
        text = re.sub(r"(?im)(^#*\s*(?:\*\*)?Pasal\s+27)8\b", r"\1B", text)
        text = re.sub(r"(?im)(^#*\s*(?:\*\*)?Pasal\s+45)8\b", r"\1B", text)
        text = re.sub(r"(?im)\bPasal\s+278\b", "Pasal 27B", text)
        text = re.sub(r"(?im)\bPasal\s+168\b", "Pasal 16B", text)
        return text

    def clean_noise(self, text: str) -> str:
        """Membersihkan watermark, penomoran halaman, running header, dan noise OCR."""
        text = self.normalize_legal_ocr(text)
        # Hilangkan SK Sekretariat Negara
        cleaned = re.sub(r"(?im)^SK\s+No\s+[0-9A-Z]+.*$", "", text)
        # Hilangkan nomor halaman di tengah "- 2 -"
        cleaned = re.sub(r"(?m)^\s*-\s*\d+\s*-\s*$", "", cleaned)
        # Hilangkan running header berulang PRESIDEN REPUBLIK INDONESIA
        cleaned = re.sub(r"(?im)^PRES!DEN\s+REP[I|!]JBUK.*$", "", cleaned)
        cleaned = re.sub(r"(?im)^PRESIDEN\s+REPUBLIK\s+INDONESIA\s*$", "", cleaned)
        # Hilangkan tag komentar/HTML dari konversi Docling
        cleaned = re.sub(r"<!--\s*Start of picture text\s*-->.*?<!--\s*End of picture text\s*-->", "", cleaned, flags=re.DOTALL)
        cleaned = re.sub(r"<!--.*?-->", "", cleaned)
        cleaned = re.sub(r"<\/?sup>", "", cleaned)
        cleaned = re.sub(r"<\/?sub>", "", cleaned)
        cleaned = re.sub(r"<\/?br\s*\/?>", " ", cleaned)
        # Hilangkan karakter OCR aneh
        cleaned = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", cleaned)
        # Normalisasi spasi dan baris baru
        cleaned = re.sub(r"[ \t]+", " ", cleaned)
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
        return cleaned.strip()

    def split_sections(self):
        """Memisahkan Batang Tubuh dengan Bagian Penjelasan."""
        cleaned = self.clean_noise(self.raw_markdown)

        # Pola penanda awal Penjelasan Undang-Undang
        split_pattern = re.compile(
            r"(?im)(?:^#{1,3}\s*Penjelasan\b|^PENJELASAN\s+(?:ATAS\s+)?UNDANG-UNDANG|^#{0,3}\s*I[\.\s]+UMUM\b)",
            re.MULTILINE
        )
        match = split_pattern.search(cleaned)

        if match:
            idx = match.start()
            self.batang_tubuh_raw = cleaned[:idx].strip()
            self.penjelasan_raw = cleaned[idx:].strip()

            # Pisahkan Penjelasan I. UMUM dan II. PASAL DEMI PASAL
            p_pasal_match = re.search(
                r"(?im)(?:^#{0,4}\s*II[\.\s]+PASAL\s*DEMI\s*PASAL|^II[\.\s]+PASAL\s*DEMI\s*PASAL)",
                self.penjelasan_raw
            )
            if p_pasal_match:
                p_idx = p_pasal_match.start()
                self.penjelasan_umum_raw = self.penjelasan_raw[:p_idx].strip()
                self.penjelasan_pasal_raw = self.penjelasan_raw[p_idx:].strip()
            else:
                self.penjelasan_umum_raw = self.penjelasan_raw
                self.penjelasan_pasal_raw = ""
        else:
            self.batang_tubuh_raw = cleaned
            self.penjelasan_raw = ""
            self.penjelasan_umum_raw = ""
            self.penjelasan_pasal_raw = ""

    def parse_pasal(self):
        """Memotong Batang Tubuh per pasal (mendukung Pasal 1, 27A, 45B, dll)."""
        # Tangkap pola pasal di awal baris (mendukung Pasal 27, 27A, 27B, 45B, dll)
        pattern = re.compile(
            r"(?im)^#{0,6}\s*(?:\*\*)?Pasal\s+([0-9]+[A-Za-z]*)(?:\*\*)?\b[^\n]*\n",
            re.MULTILINE
        )
        matches = list(pattern.finditer(self.batang_tubuh_raw))

        if not matches:
            # Coba pola UU Perubahan: "Ketentuan Pasal 5 diubah..."
            alt_pattern = re.compile(
                r"(?im)(?:^|\n)(?:[0-9]+\.\s*)?(?:Ketentuan\s+)?Pasal\s+([0-9]+[A-Za-z]*)\s+(?:diubah|dihapus|ditambah)[^\n]*\n",
                re.MULTILINE
            )
            matches = list(alt_pattern.finditer(self.batang_tubuh_raw))

        if matches:
            # Ambil bagian pembuka sebelum pasal pertama (Konsiderans: Menimbang, Mengingat, Memutuskan)
            self.pembuka_raw = self.batang_tubuh_raw[:matches[0].start()].strip()

            for i, match in enumerate(matches):
                no_pasal = match.group(1).upper()
                start_pos = match.end()
                end_pos = matches[i + 1].start() if (i + 1) < len(matches) else len(self.batang_tubuh_raw)

                isi_pasal = self.batang_tubuh_raw[start_pos:end_pos].strip()

                # Ringkasan baris non-kosong pertama untuk MOC
                first_line = ""
                for line in isi_pasal.splitlines():
                    ls = line.strip().lstrip("#").strip()
                    if ls and not ls.lower().startswith("ayat"):
                        first_line = ls
                        break
                    elif ls and not first_line:
                        first_line = ls

                ringkasan = (first_line[:130] + "...") if len(first_line) > 130 else first_line

                self.pasal_dict[no_pasal] = PasalData(
                    nomor=no_pasal,
                    batang_tubuh=isi_pasal,
                    ringkasan_awal=ringkasan
                )
        else:
            print("[!] Peringatan: Tidak ditemukan pasal dengan regex standar pada batang tubuh.")

    def parse_and_stitch_penjelasan(self):
        """Mengekstrak penjelasan per pasal dan menjahitnya ke masing-masing pasal."""
        if not self.penjelasan_pasal_raw:
            return

        # Pola pencocokan pasal di bagian penjelasan (mendukung Pasal 27, 27A, 45B, dll)
        pattern = re.compile(
            r"(?im)^#{0,6}\s*(?:\*\*)?(?:Pasal|Angka\s+\d+\s*\n\s*(?:#{0,6}\s*)?Pasal)\s+([0-9]+[A-Za-z]*)(?:\*\*)?\b[^\n]*\n",
            re.MULTILINE
        )
        matches = list(pattern.finditer(self.penjelasan_pasal_raw))

        for i, match in enumerate(matches):
            no_pasal = match.group(1).upper()
            start_pos = match.end()
            end_pos = matches[i + 1].start() if (i + 1) < len(matches) else len(self.penjelasan_pasal_raw)

            isi_penjelasan = self.penjelasan_pasal_raw[start_pos:end_pos].strip()
            is_cukup_jelas = bool(re.match(r"^cukup\s+jelas[\.\s]*$", isi_penjelasan, re.I))

            if no_pasal in self.pasal_dict:
                self.pasal_dict[no_pasal].penjelasan = isi_penjelasan if isi_penjelasan else "Cukup jelas."
                self.pasal_dict[no_pasal].is_substantive = not is_cukup_jelas and len(isi_penjelasan) > 20
            else:
                # Jika pasal tidak ada di batang tubuh (misal pasal baru di UU perubahan)
                self.pasal_dict[no_pasal] = PasalData(
                    nomor=no_pasal,
                    batang_tubuh="(Teks tidak ditemukan dalam ekstraksi batang tubuh)",
                    penjelasan=isi_penjelasan,
                    is_substantive=not is_cukup_jelas and len(isi_penjelasan) > 20,
                    ringkasan_awal=f"Pasal {no_pasal}"
                )

    def _get_sorted_pasal_keys(self) -> List[str]:
        def sort_key(p_no: str):
            num_part = re.findall(r"\d+", p_no)
            alpha_part = re.findall(r"[A-Za-z]+", p_no)
            num = int(num_part[0]) if num_part else 0
            alpha = alpha_part[0] if alpha_part else ""
            return (num, alpha)
        return sorted(self.pasal_dict.keys(), key=sort_key)

    def export_atomic_mode(self, out_dir: str):
        """Mode Karpathy LLM-Wiki: 1 berkas per pasal + Map of Content."""
        base = Path(out_dir)
        leg_dir = base / "02-pasal-atomik" / self.kode_uu
        moc_dir = base / "01-moc"

        leg_dir.mkdir(parents=True, exist_ok=True)
        moc_dir.mkdir(parents=True, exist_ok=True)

        sorted_keys = self._get_sorted_pasal_keys()

        moc_content = [
            "---",
            f"id: MOC_{self.kode_uu}",
            f"judul: \"Map of Content - {self.nama_resmi}\"",
            f"kode_uu: {self.kode_uu}",
            "type: moc",
            f"tags: [moc, hukum/{self.bidang}, uu/{self.kode_uu.lower()}]",
            f"last_updated: {date.today().isoformat()}",
            "---\n",
            f"# {self.nama_resmi} ({self.kode_uu})\n",
            "> Map of Content untuk penelusuran ringkas pasal hukum oleh AI/LLM.\n",
            "## Daftar Pasal\n"
        ]

        for p_no in sorted_keys:
            p_data = self.pasal_dict[p_no]
            file_name = f"Pasal_{p_no}.md"
            file_path = leg_dir / file_name

            fm = {
                "id": f"{self.kode_uu}_Pasal_{p_no}",
                "uu_induk": self.nama_resmi,
                "kode_uu": self.kode_uu,
                "pasal": p_no,
                "status": "BERLAKU_AKTIF",
                "substantive_explanation": p_data.is_substantive,
                "tags": [
                    f"hukum/{self.bidang}",
                    f"uu/{self.kode_uu.lower()}"
                ]
            }

            body = (
                "---\n"
                f"{yaml.dump(fm, sort_keys=False, allow_unicode=True)}"
                "---\n\n"
                f"# Pasal {p_no} — {self.nama_resmi}\n\n"
                "## Batang Tubuh\n\n"
                f"{p_data.batang_tubuh}\n\n"
                "## Penjelasan Resmi\n\n"
                f"{p_data.penjelasan}\n"
            )

            file_path.write_text(body, encoding="utf-8")
            moc_content.append(f"- [[Pasal_{p_no}]]: {p_data.ringkasan_awal}")

        # Tulis MOC
        moc_path = moc_dir / f"_Index_{self.kode_uu}.md"
        moc_path.write_text("\n".join(moc_content), encoding="utf-8")
        print(f"[OK] Mode Atomic: Berhasil membuat {len(sorted_keys)} file di: {leg_dir}")
        print(f"[OK] Mode Atomic: MOC tersimpan di: {moc_path}")

    def export_uukb_mode(self, out_dir: str, target_file_path: Optional[str] = None):
        """Mode UU-KB Native: 1 berkas per UU terpartisi sesuai AGENTS.md."""
        safe_short = re.sub(r'[/\\:*?"<>|]', "", self.judul_singkat).strip()

        if target_file_path:
            file_path = Path(target_file_path)
        else:
            base = Path(out_dir)
            target_dir = base / "10-peraturan" / "01-undang-undang"
            target_dir.mkdir(parents=True, exist_ok=True)
            doc_filename = f"{self.jenis} {self.nomor}-{self.tahun} - {safe_short}.md"
            file_path = target_dir / doc_filename

        sorted_keys = self._get_sorted_pasal_keys()

        # Frontmatter standar AGENTS.md
        fm = {
            "id": f"{self.jenis} {self.nomor}/{self.tahun}",
            "jenis": self.jenis,
            "lembaga": "Undang-Undang" if self.jenis == "UU" else self.jenis,
            "nomor": self.nomor,
            "tahun": self.tahun,
            "judul": self.nama_resmi,
            "judul_singkat": safe_short,
            "status": "berlaku",
            "status_bpk": "Berlaku",
            "bidang": [self.bidang],
            "tags": [f"jenis/{self.jenis.lower()}", f"bidang/{self.bidang}", "status/berlaku"],
            "kelengkapan": "lengkap",
            "verifikasi": "belum",
            "penjelasan": "ada" if self.penjelasan_raw else "tidak",
            "penjelasan_pasal_demi_pasal": bool(self.penjelasan_pasal_raw),
            "penjelasan_normatif": False,
            "struktur_teks": "terpartisi",
            "anchor_pasal": True,
            "last_updated": date.today().isoformat()
        }

        # Format Batang Tubuh dengan anchor
        bt_lines = [
            "---\n" + yaml.dump(fm, sort_keys=False, allow_unicode=True) + "---\n",
            "## Batang Tubuh\n",
            f"**{self.nama_resmi}**\n"
        ]

        if self.pembuka_raw:
            cleaned_pembuka = re.sub(r"(?im)^##\s*Batang\s+Tubuh\s*\n+", "", self.pembuka_raw).strip()
            if cleaned_pembuka:
                bt_lines.append(cleaned_pembuka + "\n")

        for p_no in sorted_keys:
            p_data = self.pasal_dict[p_no]
            anchor = f"^pasal-{p_no.lower()}"
            bt_lines.append(f"### Pasal {p_no} {anchor}\n")
            bt_lines.append(p_data.batang_tubuh + "\n")

        # Format Penjelasan dengan anchor
        bt_lines.append("## Penjelasan\n")
        if self.penjelasan_umum_raw:
            cleaned_umum = re.sub(r"(?im)^###\s*I\.\s*Umum\s*\n+", "", self.penjelasan_umum_raw).strip()
            bt_lines.append("### I. Umum\n")
            if cleaned_umum:
                bt_lines.append(cleaned_umum + "\n")

        if self.penjelasan_pasal_raw:
            bt_lines.append("### II. Pasal demi Pasal\n")
            for p_no in sorted_keys:
                p_data = self.pasal_dict[p_no]
                anchor = f"^penjelasan-pasal-{p_no.lower()}"
                bt_lines.append(f"#### Pasal {p_no} {anchor}\n")
                bt_lines.append(p_data.penjelasan + "\n")

        # Peta Penjelasan (Tabel Referensi Anchor)
        bt_lines.append("## Peta Penjelasan\n")
        bt_lines.append("| Pasal | Penjelasan | Substantif |")
        bt_lines.append("|---|---|:---:|")
        for p_no in sorted_keys:
            p_data = self.pasal_dict[p_no]
            sub_icon = "✓" if p_data.is_substantive else "-"
            bt_lines.append(f"| [[#^pasal-{p_no.lower()}|Pasal {p_no}]] | [[#^penjelasan-pasal-{p_no.lower()}|Penjelasan]] | {sub_icon} |")

        file_path.write_text("\n".join(bt_lines), encoding="utf-8")
        print(f"[OK] Mode UU-KB: Berhasil membuat berkas korpus di: {file_path}")

    def execute(self, mode: str = "both", out_dir: str = "."):
        self.load_document()
        self.split_sections()
        self.parse_pasal()
        self.parse_and_stitch_penjelasan()

        print(f"[*] Total pasal terdeteksi: {len(self.pasal_dict)}")

        if mode in ("atomic", "both"):
            self.export_atomic_mode(out_dir)
        if mode in ("uukb", "both"):
            self.export_uukb_mode(out_dir)


def main():
    parser = argparse.ArgumentParser(
        description="Parser PDF UU Indonesia ke format Obsidian Karpathy LLM-Wiki dan UU-KB Korpus."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--pdf", help="Path ke file PDF Undang-Undang.")
    group.add_argument("--md", help="Path ke file Markdown jika sudah diekstrak.")

    parser.add_argument("--code", required=True, help="Kode unik UU (misal: UU_1_2024 atau UU_ITE_2024).")
    parser.add_argument("--name", required=True, help="Nama lengkap resmi UU.")
    parser.add_argument("--short-name", help="Judul singkat untuk nama file UU-KB.")
    parser.add_argument("--nomor", type=int, help="Nomor UU (integer).")
    parser.add_argument("--tahun", type=int, help="Tahun penetapan UU (integer).")
    parser.add_argument("--bidang", default="pidana", help="Bidang hukum (pidana, siber, keuangan, dll).")
    parser.add_argument("--mode", choices=["atomic", "uukb", "both"], default="both",
                        help="Mode ekspor: 'atomic' (Karpathy Wiki), 'uukb' (Korpus AGENTS.md), atau 'both'.")
    parser.add_argument("--out", default=".", help="Direktori root output (default: workspace saat ini).")

    args = parser.parse_args()

    src = args.pdf if args.pdf else args.md
    is_pdf = bool(args.pdf)

    app = IndonesianLegalParser(
        source_path=src,
        kode_uu=args.code,
        nama_resmi=args.name,
        judul_singkat=args.short_name,
        nomor=args.nomor,
        tahun=args.tahun,
        bidang=args.bidang,
        is_pdf=is_pdf
    )
    app.execute(mode=args.mode, out_dir=args.out)


if __name__ == "__main__":
    main()
