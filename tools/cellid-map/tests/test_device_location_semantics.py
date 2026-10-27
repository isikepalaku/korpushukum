import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cellid_lookup import build_lookup_record


def test_geolocation_record_is_device_area_not_tower_geometry():
    record = build_lookup_record(
        {"mcc": 510, "mnc": 10, "enb_id": 341038, "cid": 21, "radio": "lte"},
        {"location": {"lat": -5.1580683, "lng": 119.5742523}, "accuracy": 486},
    )

    assert record["visualization_scope"] == "device_location_estimate"
    assert record["sector_status"] == "not_applicable"
    assert "azimuth_deg" not in record
    assert "beamwidth_deg" not in record
    assert "rings_m" not in record
