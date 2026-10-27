import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from static_cell_map import build_geometry, project_to_image


def test_project_to_image_places_center_in_middle():
    x, y = project_to_image(
        latitude=-5.1580683,
        longitude=119.5742523,
        center_latitude=-5.1580683,
        center_longitude=119.5742523,
        zoom=14,
        logical_width=640,
        logical_height=640,
        scale=2,
    )
    assert (x, y) == (640.0, 640.0)


def test_build_geometry_marks_sector_as_estimate_when_explicitly_requested():
    geometry = build_geometry(
        {
            "latitude": -5.1580683,
            "longitude": 119.5742523,
            "accuracy_m": 486,
            "rings_m": [450, 620, 1000],
            "azimuth_deg": 0,
            "beamwidth_deg": 120,
            "sector_status": "estimated_from_sector_numbering",
        }
    )
    assert [ring["radius_m"] for ring in geometry["rings"]] == [450.0, 620.0, 1000.0]
    assert geometry["sector"]["status"] == "estimated_from_sector_numbering"
    assert len(geometry["sector"]["points"]) == 27
    assert geometry["sector"]["points"][0] == geometry["sector"]["points"][-1]


def test_build_geometry_does_not_invent_a_sector():
    geometry = build_geometry(
        {"latitude": -5.1580683, "longitude": 119.5742523, "accuracy_m": 486}
    )
    assert geometry["sector"] is None
