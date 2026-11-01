#!/usr/bin/env python3
"""build_chunks.py — bangun chunk siap-embed dari korpus UU-KB.

Jalankan:  python 90-log/build_chunks.py
Output  :  90-log/chunks.jsonl.gz      (satu JSON per baris; artefak turunan, tidak di-commit)
           90-log/chunks-stats.json    (ringkasan; di-commit)
           01-moc/Indeks Penjelasan.md
Butuh   :  Python 3.10+ (stdlib saja)
"""
import gzip
import hashlib
import json
import os
import re
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 90-log/.. = root vault
MAX_CHARS = 1800
MIN_SUBSTANTIVE = 30
TODAY = date.today().isoformat()

HEAD_RE = re.compile(r"^(#{1,4})\s+(.+?)(?:\s+\^([A-Za-z0-9-]+))?\s*$")
CUKUP = re.compile(r"^cukup\s+jelas[\.\s]*$", re.I)


def parse(path):
    s = open(path, encoding="utf-8").read()
    if not s.startswith("---"):
        return {}, s
    end = s.find("\n---", 3)
    fm = {}
    for line in s[3:end].splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            v = m.group(2).strip()
            fm[m.group(1)] = [x.strip().strip('"') for x in v[1:-1].split(",") if x.strip()] \
                if v.startswith("[") else v.strip('"')
    return fm, s[end + 4:]


def sections(body):
    stack, out, buf = {}, [], []
    cur = {"title": "", "anchor": None, "level": 0}

    def flush():
        if not buf:
            return
        path = " > ".join(stack[k] for k in sorted(stack) if stack.get(k)) or "(pembuka)"
        out.append({"path": path, "title": cur["title"], "anchor": cur["anchor"],
                    "text": "".join(buf).strip()})
        buf.clear()

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
    return out


def split_text(text, limit=MAX_CHARS):
    if len(text) <= limit:
        return [text]
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    pieces, cur = [], ""
    for p in paras:
        if not cur:
            cur = p
        elif len(cur) + len(p) + 2 <= limit:
            cur += "\n\n" + p
        else:
            pieces.append(cur)
            cur = p
    if cur:
        pieces.append(cur)
    # paragraf tunggal kepanjangan -> potong per kalimat
    fixed = []
    for p in pieces:
        if len(p) <= limit:
            fixed.append(p)
            continue
        sents = re.split(r"(?<=[\.;])\s+", p)
        buf = ""
        for s in sents:
            if len(buf) + len(s) + 1 <= limit:
                buf = (buf + " " + s).strip()
            else:
                if buf:
                    fixed.append(buf)
                buf = s
        if buf:
            fixed.append(buf)
    # batas keras: potong di batas kata bila masih kepanjangan
    hard = []
    for p in fixed:
        while len(p) > limit * 1.4:
            cut = p.rfind(" ", 0, int(limit * 1.2))
            if cut < limit * 0.5:
                cut = int(limit * 1.2)
            hard.append(p[:cut].strip())
            p = p[cut:].strip()
        if p:
            hard.append(p)
    return [f for f in hard if f.strip()]


def kind_of(path):
    p = path.lower()
    if p.startswith("peta penjelasan") or "> peta penjelasan" in p:
        return "lewati"
    if p.startswith("batang tubuh"):
        return "batang-tubuh"
    if "pasal demi pasal" in p:
        return "penjelasan-pasal"
    if "i. umum" in p:
        return "penjelasan-umum"
    if p.startswith("penjelasan"):
        return "penjelasan"
    return "isi"


def pasal_of(anchor, title, path):
    for cand in (anchor or "", title or "", path or ""):
        m = re.search(r"pasal[- ]([0-9]+[a-z]*)", cand, re.I)
        if m:
            val = m.group(1).upper()
            return int(val) if val.isdigit() else val
    return None


chunks, stats_doc = [], []
for base in ("10-peraturan", "20-putusan"):
    for dp, _, fs in os.walk(os.path.join(ROOT, base)):
        for f in sorted(fs):
            if not f.endswith(".md"):
                continue
            p = os.path.join(dp, f)
            fm, body = parse(p)
            rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
            doc_id = fm.get("id", "")
            n_sub = n_cukup = n_chunks_doc = n_pasal = 0
            for sec in sections(body):
                k = kind_of(sec["path"])
                if k == "lewati":
                    continue
                pasal = pasal_of(sec["anchor"], sec["title"], sec["path"])
                sec_sub = len(sec["text"]) >= MIN_SUBSTANTIVE and not CUKUP.match(sec["text"].strip())
                if k == "penjelasan-pasal":
                    n_pasal += 1
                    if sec_sub:
                        n_sub += 1
                    else:
                        n_cukup += 1
                for i, piece in enumerate(split_text(sec["text"])):
                    if not piece.strip():
                        continue
                    substantive = (sec_sub if k == "penjelasan-pasal"
                                   else len(piece) >= MIN_SUBSTANTIVE and not CUKUP.match(piece.strip()))
                    cid = f"{doc_id}|{sec['anchor'] or k}|{i}"
                    chunks.append({
                        "chunk_id": cid,
                        "doc_id": doc_id,
                        "jenis": fm.get("jenis", ""),
                        "nomor": fm.get("nomor", ""),
                        "tahun": fm.get("tahun", ""),
                        "status": fm.get("status", ""),
                        "bidang": fm.get("bidang", []),
                        "path": sec["path"],
                        "anchor": sec["anchor"],
                        "kind": k,
                        "pasal": pasal,
                        "part": i,
                        "substantive": substantive,
                        "chars": len(piece),
                        "sha256": hashlib.sha256(piece.encode("utf-8")).hexdigest()[:16],
                        "text": piece,
                    })
                    n_chunks_doc += 1
            stats_doc.append({"doc_id": doc_id, "file": rel, "chunks": n_chunks_doc,
                              "pasal_berpenjelasan": n_pasal,
                              "penjelasan_substantif": n_sub, "penjelasan_cukup_jelas": n_cukup})

# tulis chunk
out_gz = os.path.join(ROOT, "90-log", "chunks.jsonl.gz")
with gzip.open(out_gz, "wt", encoding="utf-8", compresslevel=9) as fh:
    for c in chunks:
        fh.write(json.dumps(c, ensure_ascii=False) + "\n")

by_kind = {}
for c in chunks:
    by_kind[c["kind"]] = by_kind.get(c["kind"], 0) + 1
stats = {
    "generated": TODAY,
    "total_chunks": len(chunks),
    "by_kind": by_kind,
    "substantive_penjelasan": sum(1 for c in chunks if c["kind"] == "penjelasan-pasal" and c["substantive"]),
    "cukup_jelas": sum(1 for c in chunks if c["kind"] == "penjelasan-pasal" and not c["substantive"]),
    "avg_chars": round(sum(c["chars"] for c in chunks) / max(1, len(chunks))),
    "max_chars": max((c["chars"] for c in chunks), default=0),
    "docs": len(stats_doc),
    "source": "sections[] dari frontmatter heading (## / ### / ####)",
}
json.dump(stats, open(os.path.join(ROOT, "90-log", "chunks-stats.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

# halaman indeks penjelasan
rows = [d for d in stats_doc if d["pasal_berpenjelasan"]]
rows.sort(key=lambda d: (-d["penjelasan_substantif"], d["doc_id"]))
lines = ["---", 'judul: "Indeks Penjelasan"', "jenis: indeks", "tags: [indeks, penjelasan]",
         f"last_updated: {TODAY}", "---", "",
         "# Indeks Penjelasan", "",
         "Penjelasan resmi (I. UMUM / II. PASAL DEMI PASAL) sudah dipartisi per pasal dengan anchor "
         "`^penjelasan-pasal-N`. Halaman ini merangkum **kualitas** penjelasan: berapa pasal yang "
         "punya penjelasan substantif versus hanya \"Cukup jelas\".", "",
         "| Dokumen | Pasal berpenjelasan | Substantif | Cukup jelas | % substantif |",
         "| --- | --- | --- | --- | --- |"]
for d in rows:
    total = d["pasal_berpenjelasan"]
    pct = round(100 * d["penjelasan_substantif"] / max(1, total))
    link = d["file"].split("/")[-1][:-3]
    lines.append(f"| [[{link}]] | {total} | {d['penjelasan_substantif']} | "
                 f"{d['penjelasan_cukup_jelas']} | {pct}% |")
lines += ["",
          "## Cara memakai", "",
          "```markdown",
          "![[UU 4-2023 - P2SK#^penjelasan-pasal-44]]      kutip penjelasan Pasal 44 (transclusion)",
          "[[UU 4-2023 - P2SK#^pasal-44]]                  rujuk norma Pasal 44",
          "```", "",
          "Chunk mesin: `90-log/chunks.jsonl.gz` (satu baris JSON per chunk; field `kind`, `pasal`, "
          "`substantive`, `path`, `anchor`). Regenerasi: `python 90-log/build_chunks.py`.", ""]
os.makedirs(os.path.join(ROOT, "01-moc"), exist_ok=True)
open(os.path.join(ROOT, "01-moc", "Indeks Penjelasan.md"), "w", encoding="utf-8",
     newline="\n").write("\n".join(lines))

print(json.dumps(stats, ensure_ascii=False, indent=1))
print("chunks:", out_gz, f"({os.path.getsize(out_gz)/1024/1024:.1f} MB)")
print("indeks penjelasan:", len(rows), "dokumen")
