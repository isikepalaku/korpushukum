"""TikTok OSINT lead collector. Public-content leads only; not evidence."""

from __future__ import annotations

import asyncio
import json
import re
from pathlib import Path
from typing import Any, AsyncIterable, Callable, Iterable

INDICATORS: dict[str, tuple[str, ...]] = {
    "tugas_berkomisi": ("kerja paruh waktu", "tugas berkomisi", "komisi harian", "like dan share"),
    "deposit": ("deposit", "setor dana", "top up", "upgrade member"),
    "profit_pasti": ("profit pasti", "profit harian pasti", "untung pasti", "tanpa risiko", "cuan pasti"),
    "investasi": ("investasi", "imbal hasil", "return harian"),
    "pinjol": ("pinjol", "pelunasan pinjaman", "pemutihan pinjol", "hapus data pinjol"),
}
PHONE_PATTERN = re.compile(r"(?<!\d)(?:\+62|62|0)8[1-9](?:[\s.-]?\d){7,11}(?!\d)")


def load_watchlist(path: Path) -> list[str]:
    """Read unique, non-blank keywords while preserving first-seen spelling."""
    keywords: list[str] = []
    seen: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        keyword = line.strip()
        identity = keyword.casefold()
        if keyword and identity not in seen:
            keywords.append(keyword)
            seen.add(identity)
    return keywords


def find_indicators(text: str) -> list[str]:
    lowered = text.casefold()
    found = [name for name, terms in INDICATORS.items() if any(term in lowered for term in terms)]
    if PHONE_PATTERN.search(text):
        found.append("nomor_telepon")
    return found


def build_lead(raw: dict[str, Any], *, query: str, collected_at: str) -> dict[str, Any]:
    """Normalize a TikTok video object into a reviewable OSINT lead."""
    author = raw.get("author") or {}
    stats = raw.get("stats") or {}
    video_id = str(raw.get("id", ""))
    username = str(author.get("uniqueId", ""))
    caption = str(raw.get("desc", ""))
    indicators = find_indicators(caption)
    priority = "high" if len(indicators) >= 3 else "medium" if indicators else "low"
    return {
        "schema_version": 1,
        "evidence_status": "osint_lead_not_evidence",
        "collected_at": collected_at,
        "query": query,
        "platform": "tiktok",
        "video_id": video_id,
        "username": username,
        "source_url": f"https://www.tiktok.com/@{username}/video/{video_id}",
        "caption": caption,
        "created_at_unix": raw.get("createTime"),
        "indicators": indicators,
        "priority": priority,
        "engagement": {
            "likes": stats.get("diggCount", 0),
            "comments": stats.get("commentCount", 0),
            "shares": stats.get("shareCount", 0),
            "plays": stats.get("playCount", 0),
        },
    }


def collect_query(
    video_source: Callable[[str, int], AsyncIterable[dict[str, Any]]],
    *,
    query: str,
    count: int,
    collected_at: str,
) -> list[dict[str, Any]]:
    """Collect at most ``count`` public video objects from an injected source."""
    async def _collect() -> list[dict[str, Any]]:
        leads: list[dict[str, Any]] = []
        async for raw in video_source(query, count):
            leads.append(build_lead(raw, query=query, collected_at=collected_at))
            if len(leads) == count:
                break
        return leads

    return asyncio.run(_collect())


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    """Append lead records as UTF-8 JSON Lines."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        for record in records:
            stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
