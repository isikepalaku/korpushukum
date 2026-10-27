import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_static_cli_creates_png_without_revealing_key(tmp_path):
    source = tmp_path / "lookup.json"
    output = tmp_path / "map.png"
    source.write_text(json.dumps({
        "latitude": -5.1580683,
        "longitude": 119.5742523,
        "accuracy_m": 486,
        "label": "Test cell",
    }))

    result = subprocess.run(
        [sys.executable, str(ROOT / "render_static_cell_map.py"), "--input", str(source), "--output", str(output), "--dry-run"],
        text=True,
        capture_output=True,
        check=True,
    )

    assert "request_ready" in result.stdout
    assert "key=" not in result.stdout
    assert not output.exists()
