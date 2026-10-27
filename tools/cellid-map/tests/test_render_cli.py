import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_cli_writes_html_from_lookup_json(tmp_path):
    source = tmp_path / "lookup.json"
    output = tmp_path / "map.html"
    source.write_text(json.dumps({
        "latitude": -5.1580683,
        "longitude": 119.5742523,
        "accuracy_m": 486,
        "label": "Telkomsel LTE ECI 87305749",
        "rings_m": [450, 620, 1000],
    }))

    result = subprocess.run(
        [sys.executable, str(ROOT / "render_cell_map.py"), "--input", str(source), "--output", str(output)],
        text=True,
        capture_output=True,
        check=True,
    )

    assert output.exists()
    assert "wrote=" in result.stdout
    assert "Telkomsel LTE ECI 87305749" in output.read_text()
