#!/usr/bin/env python3
"""Verifikasi matriks NO_PROXY dengan matcher milik Hermes sendiri.

Jalankan SEBELUM restart gateway: memastikan Telegram & layanan lokal bypass
proxy WARP, sementara Gemini tetap lewat proxy. Exit 1 bila ada yang salah.

Pakai:  python3 verify_no_proxy.py [path-ke-.env]
"""
import sys
from pathlib import Path

HERMES_AGENT = Path.home() / ".hermes" / "hermes-agent"
sys.path.insert(0, str(HERMES_AGENT))

try:
    from agent.proxy_bypass import should_bypass_proxy, no_proxy_entries
except Exception as exc:  # noqa: BLE001
    print(f"GAGAL import agent.proxy_bypass: {exc}")
    print(f"Pastikan repo ada di {HERMES_AGENT}")
    raise SystemExit(2)

# (host, harus_bypass, keterangan)
CASES = [
    ("api.telegram.org", True, "Telegram WAJIB bypass (hindari 502)"),
    ("https://api.telegram.org/bot123/getMe", True, "URL Telegram utuh"),
    ("t.me", True, "link Telegram"),
    ("127.0.0.1", True, "OpenViking :1933 / CDP"),
    ("localhost", True, "daemon lokal"),
    ("10.1.2.3", True, "CIDR 10/8 jaringan internal"),
    ("192.168.1.1", True, "CIDR 192.168/16"),
    ("openrouter.ai", True, "provider lain, tidak perlu WARP"),
    ("clariohub.id", True, "provider lain"),
    ("generativelanguage.googleapis.com", False, "Gemini HARUS lewat WARP"),
    ("ai.google.dev", False, "Google lewat WARP"),
    ("api.openai.com", False, "API eksternal lewat WARP"),
]


def read_no_proxy(env_path: Path) -> str:
    for line in env_path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if line.startswith("NO_PROXY="):
            return line.split("=", 1)[1].strip()
    return ""


def main() -> int:
    env_path = Path(sys.argv[1] if len(sys.argv) > 1 else Path.home() / ".hermes" / ".env")
    if not env_path.exists():
        print(f"GAGAL: {env_path} tidak ditemukan")
        return 2
    no_proxy = read_no_proxy(env_path)
    if not no_proxy:
        print(f"GAGAL: tidak ada baris NO_PROXY di {env_path}")
        return 2

    entries = no_proxy_entries(no_proxy)
    print(f"{env_path}  |  {len(entries)} entri NO_PROXY\n")

    failures = 0
    for host, expected, note in CASES:
        got = should_bypass_proxy(host, no_proxy_value=no_proxy)
        ok = got == expected
        failures += 0 if ok else 1
        print(f"{'OK   ' if ok else 'GAGAL'} {host:42s} bypass={str(got):5s} "
              f"(harap {str(expected):5s})  {note}")

    print()
    if failures:
        print(f"{failures} KASUS GAGAL — jangan restart gateway sebelum diperbaiki.")
        return 1
    print("SEMUA BENAR — aman untuk restart gateway.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
