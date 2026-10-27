import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cell_map import render_map


def test_render_map_includes_center_rings_and_verified_sector_only():
    html = render_map(
        {
            "latitude": -5.1580683,
            "longitude": 119.5742523,
            "accuracy_m": 486,
            "label": "Telkomsel LTE ECI 87305749",
            "rings_m": [450, 620, 1000],
            "azimuth_deg": 90,
            "beamwidth_deg": 120,
            "sector_label": "Sector Alpha",
        }
    )

    assert "[-5.1580683, 119.5742523]" in html
    assert "450 m" in html
    assert "620 m" in html
    assert "1000 m" in html
    assert "Sector Alpha" in html
    assert "L.polygon" in html
    assert "OpenStreetMap" in html


def test_render_map_omits_sector_when_azimuth_is_unknown():
    html = render_map(
        {
            "latitude": -5.1580683,
            "longitude": 119.5742523,
            "accuracy_m": 486,
            "label": "Cell lookup",
        }
    )

    assert "Sector direction not supplied" in html
    assert "L.polygon" not in html
