"""Cell ID lookup records with a Google Maps link and cautious sector hypothesis."""

from __future__ import annotations

import urllib.parse
from datetime import datetime, timezone
from typing import Any


def build_lookup_record(source: dict[str, Any], geolocation: dict[str, Any]) -> dict[str, Any]:
    """Create one provenance-rich record from source identifiers and API response."""
    location = geolocation["location"]
    accuracy = float(geolocation["accuracy"])
    latitude = float(location["lat"])
    longitude = float(location["lng"])
    cid = source.get("cid")
    eci = source.get("eci")
    if eci is None and source.get("enb_id") is not None and cid is not None:
        eci = int(source["enb_id"]) * 256 + int(cid)
    record: dict[str, Any] = {
        "latitude": latitude,
        "longitude": longitude,
        "accuracy_m": accuracy,
        "mcc": int(source["mcc"]),
        "mnc": int(source["mnc"]),
        "radio": str(source.get("radio", "lte")),
        "eci": int(eci) if eci is not None else None,
        "label": f"LTE ECI {eci}" if eci is not None else "Cell ID lookup",
        "visualization_scope": "device_location_estimate",
        "looked_up_at": datetime.now(timezone.utc).isoformat(),
        "google_maps_url": "https://www.google.com/maps/search/?" + urllib.parse.urlencode(
            {"api": 1, "query": f"{latitude},{longitude}"}
        ),
    }
    if source.get("enb_id") is not None:
        record["enb_id"] = int(source["enb_id"])
    # CI identifies a serving cell but does not establish a BTS coordinate or azimuth.
    # The Geolocation response represents an estimated device/observation area.
    if cid is not None:
        record["cid"] = int(cid)
    record["sector_status"] = "not_applicable"
    return record
