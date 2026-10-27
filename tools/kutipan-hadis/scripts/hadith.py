#!/usr/bin/env python3
"""
CLI Tool for Hadith API (fawazahmed0/hadith-api)
Fetches, searches, and displays Hadith in Arabic, Indonesian, and English with gradings.
"""

import argparse
import json
import os
import random
import sys
import urllib.error
import urllib.request

CACHE_DIR = os.path.expanduser("~/.cache/hadith-api")
CDN_BASE = "https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1"
RAW_BASE = "https://raw.githubusercontent.com/fawazahmed0/hadith-api/1"

BOOKS_INFO = {
    "bukhari": {"name": "Sahih al-Bukhari", "last": 7563, "has_ind": True},
    "muslim": {"name": "Sahih Muslim", "last": 7563, "has_ind": True},
    "abudawud": {"name": "Sunan Abu Dawud", "last": 5274, "has_ind": True},
    "tirmidhi": {"name": "Jami' at-Tirmidhi", "last": 3956, "has_ind": True},
    "nasai": {"name": "Sunan an-Nasa'i", "last": 5758, "has_ind": True},
    "ibnmajah": {"name": "Sunan Ibn Majah", "last": 4341, "has_ind": True},
    "malik": {"name": "Muwatta Malik", "last": 1858, "has_ind": True},
    "nawawi": {"name": "Forty Hadith an-Nawawi", "last": 42, "has_ind": False},
    "qudsi": {"name": "Forty Hadith Qudsi", "last": 40, "has_ind": False},
    "dehlawi": {"name": "Forty Hadith Shah Waliullah", "last": 40, "has_ind": False},
}

BOOK_ALIASES = {
    "bukhari": "bukhari",
    "shahih bukhari": "bukhari",
    "sahih bukhari": "bukhari",
    "muslim": "muslim",
    "shahih muslim": "muslim",
    "sahih muslim": "muslim",
    "abudawud": "abudawud",
    "abu dawud": "abudawud",
    "abu daud": "abudawud",
    "tirmidhi": "tirmidhi",
    "at-tirmidhi": "tirmidhi",
    "tirmidzi": "tirmidhi",
    "nasai": "nasai",
    "an-nasai": "nasai",
    "ibnmajah": "ibnmajah",
    "ibnu majah": "ibnmajah",
    "malik": "malik",
    "muwatta": "malik",
    "nawawi": "nawawi",
    "arbain": "nawawi",
    "qudsi": "qudsi",
    "dehlawi": "dehlawi",
}


def normalize_book(name: str) -> str:
    key = name.strip().lower()
    return BOOK_ALIASES.get(key, key)


def fetch_url(url: str, timeout: int = 10) -> dict | None:
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; HadithCli/1.0)"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None


def fetch_edition_hadith(edition: str, number: int) -> dict | None:
    for base in [CDN_BASE, RAW_BASE]:
        url = f"{base}/editions/{edition}/{number}.json"
        data = fetch_url(url)
        if data:
            return data
    return None


def get_cached_book(book: str) -> dict | None:
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = os.path.join(CACHE_DIR, f"ind-{book}.min.json")
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    # Download and cache
    for base in [CDN_BASE, RAW_BASE]:
        url = f"{base}/editions/ind-{book}.min.json"
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (compatible; HadithCli/1.0)"}
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                content = resp.read()
                data = json.loads(content.decode("utf-8"))
                with open(cache_file, "w", encoding="utf-8") as f:
                    f.write(content.decode("utf-8"))
                return data
        except Exception:
            continue
    return None


def get_hadith_detail(book: str, number: int) -> dict:
    book = normalize_book(book)
    if book not in BOOKS_INFO:
        raise ValueError(f"Kitab '{book}' tidak dikenal. Pilihan: {', '.join(BOOKS_INFO.keys())}")

    info = BOOKS_INFO[book]
    # Fetch Arabic
    ara_data = fetch_edition_hadith(f"ara-{book}", number)

    # Fetch Translation (Indonesian if available, else English)
    trans_data = None
    trans_lang = "ind"
    if info["has_ind"]:
        trans_data = fetch_edition_hadith(f"ind-{book}", number)
    if not trans_data:
        trans_data = fetch_edition_hadith(f"eng-{book}", number)
        trans_lang = "eng"

    arabic_text = ""
    trans_text = ""
    grades = []
    section_name = ""
    section_no = None

    if ara_data and "hadiths" in ara_data and ara_data["hadiths"]:
        h = ara_data["hadiths"][0]
        arabic_text = h.get("text", "").strip()
        sec_dict = ara_data.get("metadata", {}).get("section", {})
        if sec_dict:
            section_no = list(sec_dict.keys())[0]
            section_name = sec_dict[section_no]

    if trans_data and "hadiths" in trans_data and trans_data["hadiths"]:
        h = trans_data["hadiths"][0]
        trans_text = h.get("text", "").strip()
        grades = h.get("grades", [])
        if not section_name:
            sec_dict = trans_data.get("metadata", {}).get("section", {})
            if sec_dict:
                section_no = list(sec_dict.keys())[0]
                section_name = sec_dict[section_no]

    return {
        "book": book,
        "book_name": info["name"],
        "hadithnumber": number,
        "section_no": section_no,
        "section_name": section_name,
        "arabic": arabic_text,
        "translation": trans_text,
        "translation_lang": trans_lang,
        "grades": grades,
    }


def format_hadith_markdown(item: dict) -> str:
    lines = []
    header = f"**{item['book_name']} No. {item['hadithnumber']}**"
    if item.get("section_name"):
        header += f" *(Bab/Kitab: {item['section_name']})*"
    lines.append(header)
    lines.append("")

    if item.get("arabic"):
        lines.append("```text")
        lines.append(item["arabic"])
        lines.append("```")
        lines.append("")

    if item.get("translation"):
        lines.append("**Terjemahan:**")
        lang_note = " *(Bahasa Inggris)*" if item.get("translation_lang") == "eng" else ""
        lines.append(f"> {item['translation']}{lang_note}")
        lines.append("")
    else:
        lines.append("*(Catatan: Nomor ini merupakan penomoran judul bab/isnad terusan tanpa matan mandiri dalam database. Silakan gunakan hadis sebelum/sesudahnya atau 'hadith search'.)*")
        lines.append("")

    if item.get("grades"):
        grade_str = ", ".join(f"{g.get('name')}: {g.get('grade')}" for g in item["grades"] if g.get("grade"))
        if grade_str:
            lines.append(f"**Derajat/Hukum Hadis:** {grade_str}")
    elif item["book"] in ["bukhari", "muslim"]:
        lines.append(f"**Derajat/Hukum Hadis:** Sahih ({item['book_name']})")

    return "\n".join(lines)


def cmd_get(args):
    book = normalize_book(args.book)
    num = args.number
    item = get_hadith_detail(book, num)
    if args.json:
        print(json.dumps(item, ensure_ascii=False, indent=2))
    else:
        print(format_hadith_markdown(item))


def cmd_random(args):
    if args.book:
        book = normalize_book(args.book)
    else:
        book = random.choice(["bukhari", "muslim", "abudawud", "tirmidhi"])

    if book not in BOOKS_INFO:
        raise ValueError(f"Kitab '{book}' tidak dikenal.")

    data = get_cached_book(book)
    if data and "hadiths" in data:
        non_empty = [h["hadithnumber"] for h in data["hadiths"] if h.get("text", "").strip()]
        if non_empty:
            num = random.choice(non_empty)
        else:
            num = random.randint(1, BOOKS_INFO[book]["last"])
    else:
        num = random.randint(1, BOOKS_INFO[book]["last"])

    item = get_hadith_detail(book, num)
    if args.json:
        print(json.dumps(item, ensure_ascii=False, indent=2))
    else:
        print(format_hadith_markdown(item))


def cmd_search(args):
    query = args.query.strip().lower()
    books = [normalize_book(b) for b in args.books.split(",")] if args.books else list(BOOKS_INFO.keys())
    books = [b for b in books if b in BOOKS_INFO and BOOKS_INFO[b]["has_ind"]]

    matches = []
    for b in books:
        data = get_cached_book(b)
        if not data or "hadiths" not in data:
            continue
        book_title = BOOKS_INFO[b]["name"]
        for h in data["hadiths"]:
            txt = h.get("text", "")
            if query in txt.lower():
                matches.append({
                    "book": b,
                    "book_name": book_title,
                    "hadithnumber": h.get("hadithnumber"),
                    "text": txt,
                    "grades": h.get("grades", [])
                })
                if len(matches) >= args.limit and not args.all:
                    break
        if len(matches) >= args.limit and not args.all:
            break

    if args.json:
        print(json.dumps({"query": query, "count": len(matches), "results": matches}, ensure_ascii=False, indent=2))
        return

    print(f"Ditemukan {len(matches)} hadis dengan kata kunci: '{args.query}'\n")
    for i, m in enumerate(matches, 1):
        if args.full:
            item = get_hadith_detail(m["book"], m["hadithnumber"])
            print(f"--- [Hasil {i}] ---")
            print(format_hadith_markdown(item))
            print()
        else:
            snippet = m["text"][:160] + "..." if len(m["text"]) > 160 else m["text"]
            grades_txt = ""
            if m.get("grades"):
                grades_txt = f" | {m['grades'][0].get('grade')}"
            print(f"{i}. **{m['book_name']} No. {m['hadithnumber']}**{grades_txt}")
            print(f"   \"{snippet}\"\n")


def cmd_books(args):
    print("Daftar Kitab Hadis Tersedia (fawazahmed0/hadith-api):")
    print("-----------------------------------------------------")
    for k, v in BOOKS_INFO.items():
        lang = "Arab, Indonesia, Inggris" if v["has_ind"] else "Arab, Inggris"
        print(f"- {k.ljust(10)}: {v['name']} (Total: {v['last']:,} hadis | Bahasa: {lang})")


def main():
    parser = argparse.ArgumentParser(description="Hadith CLI - Hadith API tool")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # get
    p_get = subparsers.add_parser("get", help="Ambil hadis berdasarkan kitab dan nomor")
    p_get.add_argument("book", help="Nama kitab (misal: bukhari, muslim, abudawud, tirmidhi)")
    p_get.add_argument("number", type=int, help="Nomor hadis")
    p_get.add_argument("--json", action="store_true", help="Output format JSON")
    p_get.set_defaults(func=cmd_get)

    # random
    p_rand = subparsers.add_parser("random", help="Ambil hadis acak")
    p_rand.add_argument("book", nargs="?", default=None, help="Nama kitab (opsional)")
    p_rand.add_argument("--json", action="store_true", help="Output format JSON")
    p_rand.set_defaults(func=cmd_random)

    # search
    p_search = subparsers.add_parser("search", help="Cari hadis berdasarkan kata kunci terjemahan")
    p_search.add_argument("query", help="Kata kunci pencarian")
    p_search.add_argument("--books", "-b", help="Daftar kitab dipisah koma (default: semua kitab bahasa Indonesia)")
    p_search.add_argument("--limit", "-n", type=int, default=5, help="Batas jumlah hasil (default: 5)")
    p_search.add_argument("--all", action="store_true", help="Tampilkan semua hasil tanpa batas")
    p_search.add_argument("--full", action="store_true", help="Tampilkan teks lengkap dan matan Arab")
    p_search.add_argument("--json", action="store_true", help="Output format JSON")
    p_search.set_defaults(func=cmd_search)

    # books
    p_books = subparsers.add_parser("books", help="Daftar kitab yang didukung")
    p_books.set_defaults(func=cmd_books)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
