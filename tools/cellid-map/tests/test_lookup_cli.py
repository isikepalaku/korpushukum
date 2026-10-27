import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_lookup_cli_dry_run_reports_link_without_creating_sector_image(tmp_path):
    output = tmp_path / "result.json"
    result = subprocess.run(
        [
            sys.executable, str(ROOT / "lookup_cellid.py"),
            "--mcc", "510", "--mnc", "10", "--enb-id", "341038", "--cid", "21",
            "--output", str(output), "--dry-run",
        ],
        text=True, capture_output=True, check=True,
    )
    assert "eci=87305749" in result.stdout
    assert "google_maps_link=will_be_generated_after_lookup" in result.stdout
    assert "static_image=" not in result.stdout
    assert "key=" not in result.stdout
