#!/usr/bin/env python3
"""Look up an LTE Cell ID and emit a provenance JSON record + Google Maps link.

Keluaran adalah estimasi area perangkat/observasi (beserta radius akurasi), bukan
koordinat BTS. Skrip ini tidak menggambar juring sektor maupun PNG; lihat
render_cell_map.py dan render_static_cell_map.py untuk visualisasi.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
from cellid_lookup import build_lookup_record


def get_auth_headers_and_url() -> tuple[dict[str, str], str]:
    """Return headers and URL with appropriate auth (Bearer token or API key)."""
    # 1. Try service account credentials from env or standard paths
    sa_path = (
        os.environ.get("VERTEX_CREDENTIALS_PATH")
        or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        or str(Path.home() / ".hermes/etc/vertex-key.json")
    )
    if sa_path and Path(sa_path).exists():
        try:
            from google.auth.transport.requests import Request
            from google.oauth2 import service_account

            scopes = ["https://www.googleapis.com/auth/cloud-platform"]
            creds = service_account.Credentials.from_service_account_file(sa_path, scopes=scopes)
            creds.refresh(Request())
            if creds.token:
                return (
                    {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {creds.token}",
                    },
                    "https://www.googleapis.com/geolocation/v1/geolocate",
                )
        except Exception:
            pass

    # 2. Fall back to GOOGLE_API_KEY query parameter
    key = os.environ.get("GOOGLE_API_KEY")
    if key:
        return (
            {"Content-Type": "application/json"},
            "https://www.googleapis.com/geolocation/v1/geolocate?key=" + urllib.parse.quote(key, safe=""),
        )

    raise ValueError("Neither valid Google Service Account credentials nor GOOGLE_API_KEY found")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mcc", type=int, required=True)
    parser.add_argument("--mnc", type=int, required=True)
    parser.add_argument("--enb-id", type=int, required=True)
    parser.add_argument("--cid", type=int, required=True)
    parser.add_argument("--tac", type=int)
    parser.add_argument("--output", required=True, help="Lookup JSON result")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    eci = args.enb_id * 256 + args.cid
    if args.dry_run:
        print(f"eci={eci}")
        print("google_maps_link=will_be_generated_after_lookup")
        return

    try:
        headers, url = get_auth_headers_and_url()
    except ValueError as err:
        parser.error(str(err))

    source = {"mcc": args.mcc, "mnc": args.mnc, "enb_id": args.enb_id, "cid": args.cid, "radio": "lte"}
    if args.tac is not None:
        source["tac"] = args.tac
    tower = {
        "mobileCountryCode": args.mcc,
        "mobileNetworkCode": args.mnc,
        "cellId": eci,
        "radioType": "lte",
    }
    if args.tac is not None:
        tower["locationAreaCode"] = args.tac
    payload = json.dumps({"radioType": "lte", "cellTowers": [tower]}).encode()
    request = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            geolocation = json.loads(response.read())
    except urllib.error.HTTPError as exc:
        detail = exc.read()[:300].decode("utf-8", "replace").replace("\n", " ")
        raise SystemExit(f"Google Geolocation HTTP {exc.code}: {detail}")

    record = build_lookup_record(source, geolocation)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"eci={eci}")
    print("google_maps_link=" + record["google_maps_url"])
    print("sector_status=" + record["sector_status"])
    print("result=" + str(output))


if __name__ == "__main__":
    main()
