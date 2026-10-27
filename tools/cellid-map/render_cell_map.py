#!/usr/bin/env python3
"""Create a standalone Leaflet visualisation from a Cell ID lookup JSON file."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
from cell_map import render_map


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Lookup JSON path")
    parser.add_argument("--output", required=True, help="HTML output path")
    args = parser.parse_args()

    source = Path(args.input)
    output = Path(args.output)
    data = json.loads(source.read_text(encoding="utf-8"))
    required = {"latitude", "longitude", "accuracy_m"}
    missing = sorted(required - data.keys())
    if missing:
        parser.error("input is missing: " + ", ".join(missing))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_map(data), encoding="utf-8")
    print(f"wrote={output}")


if __name__ == "__main__":
    main()
