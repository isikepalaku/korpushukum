"""Create static, attributed Cell ID map images from a Google basemap."""

from __future__ import annotations

import math
from io import BytesIO
from typing import Any

from PIL import Image, ImageDraw, ImageFont

from cell_map import destination, sector_points

TILE_SIZE = 256.0


def project_to_image(
    *, latitude: float, longitude: float, center_latitude: float, center_longitude: float,
    zoom: int, logical_width: int, logical_height: int, scale: int,
) -> tuple[float, float]:
    """Project WGS84 coordinates onto a Web-Mercator static-map image."""
    def world(lon: float, lat: float) -> tuple[float, float]:
        lat = max(min(lat, 85.05112878), -85.05112878)
        size = TILE_SIZE * (2 ** zoom)
        x = (lon + 180.0) / 360.0 * size
        y = (1.0 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2.0 * size
        return x, y

    x, y = world(longitude, latitude)
    cx, cy = world(center_longitude, center_latitude)
    return ((logical_width / 2 + x - cx) * scale, (logical_height / 2 + y - cy) * scale)


def _circle_points(latitude: float, longitude: float, radius_m: float) -> list[list[float]]:
    return [list(destination(latitude, longitude, bearing, radius_m)) for bearing in range(0, 361, 10)]


def build_geometry(data: dict[str, Any]) -> dict[str, Any]:
    """Build rings and optional sector geometry; never infer sector direction."""
    latitude = float(data["latitude"])
    longitude = float(data["longitude"])
    accuracy = float(data["accuracy_m"])
    radii = sorted({float(item) for item in data.get("rings_m", [accuracy]) if float(item) > 0})
    sector = None
    if "azimuth_deg" in data and "beamwidth_deg" in data:
        sector = {
            "points": sector_points(latitude, longitude, float(data["azimuth_deg"]), float(data["beamwidth_deg"]), max(radii)),
            "status": str(data.get("sector_status", "verified")),
        }
    return {
        "center": [latitude, longitude],
        "rings": [{"radius_m": radius, "points": _circle_points(latitude, longitude, radius)} for radius in radii],
        "sector": sector,
    }


def _pixels(points: list[list[float]], data: dict[str, Any], zoom: int, logical_width: int, logical_height: int, scale: int) -> list[tuple[float, float]]:
    return [project_to_image(
        latitude=lat, longitude=lon, center_latitude=float(data["latitude"]), center_longitude=float(data["longitude"]),
        zoom=zoom, logical_width=logical_width, logical_height=logical_height, scale=scale,
    ) for lat, lon in points]


def sector_color(status: str) -> tuple[int, int, int, int]:
    """Use red with low opacity for any unverified sector hypothesis."""
    return (26, 101, 191, 105) if status == "verified" else (220, 38, 38, 65)


def draw_overlays(image: Image.Image, data: dict[str, Any], *, zoom: int, logical_width: int, logical_height: int, scale: int) -> Image.Image:
    """Draw rings, labelled centre, and an explicitly classified sector overlay."""
    image = image.convert("RGBA")
    geometry = build_geometry(data)
    draw = ImageDraw.Draw(image, "RGBA")
    font = ImageFont.load_default()
    for ring in geometry["rings"]:
        pixels = _pixels(ring["points"], data, zoom, logical_width, logical_height, scale)
        draw.line(pixels, fill=(35, 130, 255, 230), width=3 * scale, joint="curve")
        label_x, label_y = pixels[0]
        draw.rectangle((label_x + 6, label_y - 16, label_x + 80, label_y + 5), fill=(10, 25, 45, 210))
        draw.text((label_x + 10, label_y - 14), f"{ring['radius_m']:g} m", fill="white", font=font)
    if geometry["sector"]:
        points = _pixels(geometry["sector"]["points"], data, zoom, logical_width, logical_height, scale)
        color = sector_color(geometry["sector"]["status"])
        draw.polygon(points, fill=color)
        draw.line(points, fill=(220, 38, 38, 220), width=3 * scale, joint="curve")
    center = project_to_image(
        latitude=float(data["latitude"]), longitude=float(data["longitude"]),
        center_latitude=float(data["latitude"]), center_longitude=float(data["longitude"]),
        zoom=zoom, logical_width=logical_width, logical_height=logical_height, scale=scale,
    )
    x, y = center
    draw.ellipse((x - 8 * scale, y - 8 * scale, x + 8 * scale, y + 8 * scale), fill=(255, 255, 255, 255), outline=(190, 0, 0, 255), width=3 * scale)
    _draw_panel(image, data, font)
    return image.convert("RGB")


def _draw_panel(image: Image.Image, data: dict[str, Any], font: ImageFont.ImageFont) -> None:
    status = str(data.get("sector_status", "no_sector"))
    status_label = {
        "verified": "SECTOR: VERIFIED TECHNICAL DATA",
        "estimated_from_sector_numbering": "SECTOR: ESTIMATE FROM CI NUMBERING — UNVERIFIED",
        "no_sector": "SECTOR: NOT DRAWN — AZIMUTH UNKNOWN",
    }.get(status, "SECTOR: UNVERIFIED")
    lines = [
        str(data.get("label", "Cell ID lookup")),
        f"Lat {float(data['latitude']):.6f}  Lon {float(data['longitude']):.6f}",
        f"Accuracy ±{float(data['accuracy_m']):g} m",
        status_label,
        "Estimate only; not device/person location.",
    ]
    draw = ImageDraw.Draw(image, "RGBA")
    width = max(draw.textlength(line, font=font) for line in lines) + 24
    height = len(lines) * 16 + 18
    x, y = 16, image.height - height - 18
    draw.rounded_rectangle((x, y, x + width, y + height), radius=8, fill=(10, 22, 40, 230), outline=(255, 255, 255, 130), width=1)
    for index, line in enumerate(lines):
        color = (255, 210, 90) if "UNVERIFIED" in line else (255, 255, 255)
        draw.text((x + 12, y + 10 + index * 16), line, fill=color, font=font)
