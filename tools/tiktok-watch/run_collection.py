#!/usr/bin/env python3
"""Collect low-volume public TikTok OSINT leads from a controlled watchlist."""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from tiktok_watch import build_lead, load_watchlist, write_jsonl

ROOT = Path(__file__).parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--watchlist", type=Path, default=ROOT / "watchlist.txt")
    parser.add_argument("--output", type=Path, default=ROOT / "data" / "leads.jsonl")
    parser.add_argument("--limit", type=int, default=10, help="maximum videos per query; 1–30")
    parser.add_argument("--dry-run", action="store_true", help="print queries only; no TikTok request")
    return parser.parse_args()


async def collect(args: argparse.Namespace, queries: list[str]) -> int:
    try:
        from TikTokApi import TikTokApi
    except ImportError as error:
        raise RuntimeError("TikTokApi belum terpasang. Jalankan ./setup.sh terlebih dahulu.") from error

    ms_token = os.environ.get("TIKTOK_MS_TOKEN")
    if not ms_token:
        raise RuntimeError("TIKTOK_MS_TOKEN belum tersedia. Jangan tempel cookie di shell history atau berkas watchlist.")

    collected_at = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    records = []
    async with TikTokApi() as api:
        await api.create_sessions(
            ms_tokens=[ms_token],
            num_sessions=1,
            sleep_after=3,
            browser=os.getenv("TIKTOK_BROWSER", "chromium"),
        )
        for query in queries:
            cursor = 0
            gathered = 0
            while gathered < args.limit:
                response = await api.make_request(
                    url="https://www.tiktok.com/api/search/item/full/",
                    params={"keyword": query, "count": min(10, args.limit - gathered), "cursor": cursor, "source": "search_video"},
                )
                items = response.get("item_list", [])
                for raw in items:
                    records.append(build_lead(raw, query=query, collected_at=collected_at))
                    gathered += 1
                    if gathered == args.limit:
                        break
                if not response.get("has_more") or not items:
                    break
                cursor = response.get("cursor", 0)
    write_jsonl(args.output, records)
    return len(records)


def main() -> int:
    args = parse_args()
    if not 1 <= args.limit <= 30:
        raise SystemExit("--limit harus 1 sampai 30.")
    queries = load_watchlist(args.watchlist)
    if args.dry_run:
        print("\n".join(queries))
        return 0
    try:
        count = asyncio.run(collect(args, queries))
    except RuntimeError as error:
        print(f"Gagal: {error}", file=sys.stderr)
        return 2
    print(f"Tersimpan {count} petunjuk OSINT di {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
