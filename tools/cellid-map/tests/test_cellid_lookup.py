import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cellid_lookup import build_lookup_record


def test_lookup_record_includes_google_maps_link_without_tower_sector_geometry():
    record = build_lookup_record(
        {"mcc": 510, "mnc": 10, "enb_id": 341038, "cid": 21, "radio": "lte"},
        {"location": {"lat": -5.1580683, "lng": 119.5742523}, "accuracy": 486},
    )

    assert record["eci"] == 87305749
    assert record["google_maps_url"] == "https://www.google.com/maps/search/?api=1&query=-5.1580683%2C119.5742523"
    assert record["visualization_scope"] == "device_location_estimate"
    assert record["sector_status"] == "not_applicable"
    assert "azimuth_deg" not in record
    assert "beamwidth_deg" not in record
    assert "rings_m" not in record


def test_lookup_record_does_not_create_sector_when_cid_is_unavailable():
    record = build_lookup_record(
        {"mcc": 510, "mnc": 10, "eci": 87305749, "radio": "lte"},
        {"location": {"lat": -5.1580683, "lng": 119.5742523}, "accuracy": 486},
    )
    assert "azimuth_deg" not in record
    assert record["sector_status"] == "not_applicable"
