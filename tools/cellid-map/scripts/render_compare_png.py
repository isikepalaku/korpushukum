#!/usr/bin/env python3
"""Ilustrasi kerja PNG dari dua pusat estimasi (basemap OSM, bukan Google Static Maps).

Dipakai untuk lampiran laporan/Telegram ketika hasil Google Geolocation hanya berupa
estimasi area dan PNG statis Google tidak boleh dipakai. Label batas pembuktian
("bukan bukti lokasi orang") selalu dicetak di gambar.

Contoh:
  python3 render_compare_png.py \
    --a-lat -2.9531734 --a-lon 120.1363376 --a-acc 594.89 --a-label "A - pusat estimasi Google Geolocation" \
    --b-lat -2.962020  --b-lon 120.148320  --b-label "B - koordinat sumber (radius tidak diketahui)" \
    --title "Cell ID ECI 86292513 - Telkomsel LTE" \
    --note "Keduanya ter-reverse-geocode ke Kel. Battang, Kec. Wara Barat, Kota Palopo" \
    --output cellid-86292513-compare.png
"""
from __future__ import annotations

import argparse
import math
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

TILE = 256
UA = {"User-Agent": "hermes-workpaper/1.0 (investigative map illustration)"}
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def world_px(lat: float, lon: float, z: int) -> tuple[float, float]:
    n = 2 ** z * TILE
    x = (lon + 180.0) / 360.0 * n
    lat_r = math.radians(lat)
    y = (1 - math.log(math.tan(lat_r) + 1 / math.cos(lat_r)) / math.pi) / 2 * n
    return x, y


def m_per_px(lat: float, z: int) -> float:
    return 156543.03392 * math.cos(math.radians(lat)) / (2 ** z)


def haversine(a_lat, a_lon, b_lat, b_lon) -> float:
    r = 6371008.8
    p1, p2 = math.radians(a_lat), math.radians(b_lat)
    dp = math.radians(b_lat - a_lat)
    dl = math.radians(b_lon - a_lon)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--a-lat", type=float, required=True)
    ap.add_argument("--a-lon", type=float, required=True)
    ap.add_argument("--a-acc", type=float, default=None, help="radius akurasi meter (opsional)")
    ap.add_argument("--a-label", default="A - pusat estimasi")
    ap.add_argument("--b-lat", type=float, default=None)
    ap.add_argument("--b-lon", type=float, default=None)
    ap.add_argument("--b-label", default="B - koordinat sumber")
    ap.add_argument("--title", default="Cell ID - ilustrasi kerja, BUKAN bukti lokasi orang")
    ap.add_argument("--note", default="")
    ap.add_argument("--zoom", type=int, default=15)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    z = args.zoom
    pts = [(args.a_lat, args.a_lon, args.a_acc, args.a_label, (45, 122, 255))]
    if args.b_lat is not None and args.b_lon is not None:
        pts.append((args.b_lat, args.b_lon, None, args.b_label, (255, 138, 32)))

    px = [world_px(p[0], p[1], z) for p in pts]
    acc_px = (args.a_acc or 0) / m_per_px(args.a_lat, z)
    margin = 190
    x0 = min(p[0] for p in px) - acc_px - margin
    x1 = max(p[0] for p in px) + acc_px + margin
    y0 = min(p[1] for p in px) - acc_px - margin
    y1 = max(p[1] for p in px) + acc_px + margin
    w, h = int(x1 - x0), int(y1 - y0)

    canvas = Image.new("RGB", (w, h), (238, 238, 232))
    for tx in range(int(x0 // TILE), int(x1 // TILE) + 1):
        for ty in range(int(y0 // TILE), int(y1 // TILE) + 1):
            url = f"https://tile.openstreetmap.org/{z}/{tx}/{ty}.png"
            tmp = Path(f"/tmp/tile-{z}-{tx}-{ty}.png")
            try:
                tmp.write_bytes(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read())
                canvas.paste(Image.open(tmp).convert("RGB"), (int(tx * TILE - x0), int(ty * TILE - y0)))
            except Exception as exc:  # noqa: BLE001
                print(f"tile {tx},{ty} gagal: {exc}")

    draw = ImageDraw.Draw(canvas, "RGBA")
    font = ImageFont.truetype(FONT_BOLD, 20)
    small = ImageFont.truetype(FONT_REG, 17)

    for lat, lon, acc, label, colour in pts:
        x, y = world_px(lat, lon, z)
        cx, cy = x - x0, y - y0
        if acc:
            r = acc / m_per_px(lat, z)
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour + (230,), width=3, fill=colour + (38,))
            draw.line([cx, cy - 11, cx + r, cy - 11], fill=colour + (230,), width=2)
            draw.text((cx + r / 2 - 24, cy - 32), f"{int(acc)} m", font=small, fill=colour + (255,))
        draw.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=colour + (255,), outline=(255, 255, 255, 255), width=3)
        tw = draw.textlength(label, font=small)
        draw.rectangle([cx + 11, cy - 18, cx + 21 + tw, cy + 12], fill=(18, 32, 51, 215))
        draw.text((cx + 16, cy - 14), label, font=small, fill=(255, 255, 255, 255))

    def wrap(text: str, font_obj, max_w: int) -> list[str]:
        words, lines_out, cur = text.split(), [], ""
        for word in words:
            trial = f"{cur} {word}".strip()
            if draw.textlength(trial, font=font_obj) <= max_w or not cur:
                cur = trial
            else:
                lines_out.append(cur)
                cur = word
        if cur:
            lines_out.append(cur)
        return lines_out

    raw_lines = [args.title]
    desc = f"A: {args.a_lat:.7f}, {args.a_lon:.7f}" + (f" (akurasi +/-{args.a_acc:g} m)" if args.a_acc else "")
    if args.b_lat is not None:
        desc += f"   B: {args.b_lat:.7f}, {args.b_lon:.7f}"
    raw_lines.append(desc)
    if args.b_lat is not None:
        raw_lines.append(f"Jarak pusat A-B = {haversine(args.a_lat, args.a_lon, args.b_lat, args.b_lon):.0f} m. " + args.note)
    elif args.note:
        raw_lines.append(args.note)

    lines: list[str] = []
    for i, line in enumerate(raw_lines):
        lines.extend(wrap(line, font if i == 0 else small, w - 28))

    credit = (f"Basemap (c) OpenStreetMap contributors, zoom {z}. "
              "Cincin = radius akurasi, bukan batas sel atau lokasi perangkat.")
    credit_lines = wrap(credit, small, w - 28)

    band = 26 * len(lines) + 22 * len(credit_lines) + 30
    out = Image.new("RGB", (w, h + band), (14, 24, 38))
    out.paste(canvas, (0, band))
    d2 = ImageDraw.Draw(out)
    y = 10
    for i, line in enumerate(lines):
        d2.text((14, y), line, font=font if i == 0 else small, fill=(255, 255, 255) if i == 0 else (198, 214, 235))
        y += 26
    y = h + band - 22 * len(credit_lines) - 6
    for line in credit_lines:
        d2.text((14, y), line, font=small, fill=(160, 176, 196))
        y += 22
    out.save(args.output)
    print(f"wrote {args.output} {out.size}")


if __name__ == "__main__":
    main()
