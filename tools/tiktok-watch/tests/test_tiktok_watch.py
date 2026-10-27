import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from tiktok_watch import build_lead, collect_query, load_watchlist, write_jsonl


def test_load_watchlist_removes_blank_and_duplicate_keywords(tmp_path):
    watchlist = tmp_path / "watchlist.txt"
    watchlist.write_text("pinjol Makassar\n\nPinjol Makassar\n investasi Sulsel \n", encoding="utf-8")

    assert load_watchlist(watchlist) == ["pinjol Makassar", "investasi Sulsel"]


def test_build_lead_flags_high_risk_finance_content():
    raw = {
        "id": "video-123",
        "desc": "Kerja paruh waktu. Deposit dulu, profit harian pasti. WA 0812 3456 7890",
        "createTime": 1_789_000_000,
        "author": {"uniqueId": "akun.contoh"},
        "stats": {"diggCount": 12, "commentCount": 3, "shareCount": 4, "playCount": 500},
    }

    lead = build_lead(raw, query="kerja paruh waktu Makassar", collected_at="2026-09-13T12:00:00Z")

    assert lead["source_url"] == "https://www.tiktok.com/@akun.contoh/video/video-123"
    assert lead["priority"] == "high"
    assert {"tugas_berkomisi", "deposit", "profit_pasti", "nomor_telepon"} <= set(lead["indicators"])
    assert lead["evidence_status"] == "osint_lead_not_evidence"


def test_write_jsonl_appends_one_valid_json_object_per_line(tmp_path):
    output = tmp_path / "leads.jsonl"
    write_jsonl(output, [{"video_id": "1"}, {"video_id": "2"}])

    assert [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()] == [
        {"video_id": "1"},
        {"video_id": "2"},
    ]


def test_collect_query_normalizes_only_requested_number_of_videos():
    async def videos(_query, count):
        for index in range(count + 1):
            yield {
                "id": str(index),
                "desc": "deposit profit pasti",
                "author": {"uniqueId": "akun"},
                "stats": {},
            }

    leads = collect_query(videos, query="pinjol Makassar", count=2, collected_at="2026-09-13T12:00:00Z")

    assert [lead["video_id"] for lead in leads] == ["0", "1"]
    assert all(lead["query"] == "pinjol Makassar" for lead in leads)


def test_dry_run_reports_unique_watchlist_queries(tmp_path):
    watchlist = tmp_path / "watchlist.txt"
    watchlist.write_text("pinjol Makassar\nPINJOL MAKASSAR\ninvestasi Sulsel\n", encoding="utf-8")
    runner = Path(__file__).resolve().parents[1] / "run_collection.py"

    result = subprocess.run(
        [sys.executable, str(runner), "--dry-run", "--watchlist", str(watchlist)],
        capture_output=True,
        check=True,
        text=True,
    )

    assert result.stdout.splitlines() == ["pinjol Makassar", "investasi Sulsel"]
