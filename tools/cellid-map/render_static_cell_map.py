#!/usr/bin/env python3
"""Render a Google Static Maps Cell ID image with defensible overlays."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).parent / "src"))
from static_cell_map import draw_overlays


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Lookup JSON path")
    parser.add_argument("--output", required=True, help="PNG output path")
    parser.add_argument("--zoom", type=int, default=14)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    required = {"latitude", "longitude", "accuracy_m"}
    missing = sorted(required - data.keys())
    if missing:
        parser.error("input is missing: " + ", ".join(missing))
    if args.dry_run:
        print("request_ready=google_static_map_hybrid")
        return

    key = os.environ.get("GOOGLE_API_KEY")
    if not key:
        parser.error("GOOGLE_API_KEY is not configured")
    logical_width = 640
    logical_height = 640
    scale = 2
    params = {
        "center": f"{float(data['latitude'])},{float(data['longitude'])}",
        "zoom": str(args.zoom),
        "size": f"{logical_width}x{logical_height}",
        "scale": str(scale),
        "maptype": "hybrid",
        "key": key,
    }
    request_url = "https://maps.googleapis.com/maps/api/staticmap?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(request_url, timeout=45) as response:
            content_type = response.headers.get("Content-Type", "")
            raw = response.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read()[:300].decode("utf-8", "replace").replace("\n", " ")
        raise SystemExit(f"Google Static Maps HTTP {exc.code}: {detail}")
    if not raw.startswith(b"\x89PNG\r\n\x1a\n"):
        raise SystemExit(f"Google Static Maps did not return PNG ({content_type})")
    image = Image.open(BytesIO(raw))
    rendered = draw_overlays(image, data, zoom=args.zoom, logical_width=logical_width, logical_height=logical_height, scale=scale)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    rendered.save(output, "PNG")
    print(f"wrote={output}")
    print(f"dimensions={rendered.width}x{rendered.height}")


if __name__ == "__main__":
    main()
