"""Render defensible Cell ID lookup maps as standalone Leaflet HTML."""

from __future__ import annotations

import html
import math
from typing import Any


EARTH_RADIUS_M = 6_371_000


def destination(latitude: float, longitude: float, bearing_deg: float, distance_m: float) -> tuple[float, float]:
    """Return point reached by a geodesic bearing and distance."""
    bearing = math.radians(bearing_deg)
    lat1 = math.radians(latitude)
    lon1 = math.radians(longitude)
    angular = distance_m / EARTH_RADIUS_M
    lat2 = math.asin(math.sin(lat1) * math.cos(angular) + math.cos(lat1) * math.sin(angular) * math.cos(bearing))
    lon2 = lon1 + math.atan2(
        math.sin(bearing) * math.sin(angular) * math.cos(lat1),
        math.cos(angular) - math.sin(lat1) * math.sin(lat2),
    )
    return math.degrees(lat2), math.degrees(lon2)


def sector_points(latitude: float, longitude: float, azimuth_deg: float, beamwidth_deg: float, radius_m: float) -> list[list[float]]:
    """Build a sector polygon. Direction is shown only when source provides it."""
    points = [[latitude, longitude]]
    start = azimuth_deg - beamwidth_deg / 2
    for step in range(25):
        bearing = start + beamwidth_deg * step / 24
        lat, lon = destination(latitude, longitude, bearing, radius_m)
        points.append([lat, lon])
    points.append([latitude, longitude])
    return points


def render_map(data: dict[str, Any]) -> str:
    """Render map HTML from validated lookup data without inventing sector direction."""
    latitude = float(data["latitude"])
    longitude = float(data["longitude"])
    accuracy = float(data["accuracy_m"])
    label = html.escape(str(data.get("label", "Cell lookup")))
    rings = [float(value) for value in data.get("rings_m", [accuracy])]
    rings = sorted({value for value in rings if value > 0})
    if not rings:
        rings = [accuracy]
    center = f"[{latitude}, {longitude}]"
    ring_js = "\n".join(
        f"L.circle({center}, {{radius: {radius}, color: '#2d8cff', weight: 2, fillOpacity: 0.03}}).addTo(map).bindTooltip('{int(radius) if radius.is_integer() else radius:g} m', {{permanent: true, direction: 'right'}});"
        for radius in rings
    )
    timestamp = html.escape(str(data.get("looked_up_at", "Lookup time not supplied")))
    detail = html.escape(str(data.get("detail", "Estimated coverage, not device location.")))
    sector_js = ""
    sector_note = "Sector direction not supplied; no sector wedge drawn."
    if "azimuth_deg" in data and "beamwidth_deg" in data:
        azimuth = float(data["azimuth_deg"])
        beamwidth = float(data["beamwidth_deg"])
        points = sector_points(latitude, longitude, azimuth, beamwidth, max(rings))
        sector_label = html.escape(str(data.get("sector_label", "Sector")))
        sector_js = f"L.polygon({points}, {{color: '#172a45', weight: 2, fillColor: '#1f3a5f', fillOpacity: 0.28}}).addTo(map).bindTooltip('{sector_label}', {{permanent: true, direction: 'center'}});"
        sector_note = f"Sector shown: azimuth {azimuth:g}°, beamwidth {beamwidth:g}°."
    return f"""<!doctype html>
<html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
<title>{label}</title>
<link rel=\"stylesheet\" href=\"https://unpkg.com/leaflet@1.9.4/dist/leaflet.css\">
<style>html,body,#map{{height:100%;margin:0}}.panel{{position:absolute;z-index:1000;top:14px;left:14px;background:#122033eF;color:#fff;padding:12px 14px;font:14px Arial;border-radius:4px;max-width:360px}}.panel h1{{font-size:16px;margin:0 0 6px}}.panel p{{margin:4px 0}}.warn{{color:#ffd26a}}</style></head>
<body><div id=\"map\"></div><section class=\"panel\"><h1>{label}</h1><p>{timestamp}</p><p>{detail}</p><p class=\"warn\">{sector_note}</p><p>OSINT estimate: verify with operator data.</p></section>
<script src=\"https://unpkg.com/leaflet@1.9.4/dist/leaflet.js\"></script>
<script>const map=L.map('map').setView({center}, 14);L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{maxZoom:19,attribution:'© OpenStreetMap contributors'}}).addTo(map);L.marker({center}).addTo(map).bindPopup('{label}<br>Accuracy ±{accuracy:g} m').openPopup();{ring_js}{sector_js}</script>
</body></html>"""
