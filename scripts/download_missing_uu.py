import urllib.request
import re
from pathlib import Path

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

targets = [
    {
        'id': 'UU 11/2008',
        'bpk_id': '38734',
        'bpk_slug': 'uu-no-11-tahun-2008',
        'out_name': 'UU 11-2008 - ITE.pdf'
    },
    {
        'id': 'UU 19/2016',
        'bpk_id': '37562',
        'bpk_slug': 'uu-no-19-tahun-2016',
        'out_name': 'UU 19-2016 - ITE Perubahan Pertama.pdf'
    }
]

for t in targets:
    url = f"https://peraturan.bpk.go.id/Details/{t['bpk_id']}/{t['bpk_slug']}"
    print(f"[*] Mengecek: {t['id']} -> {url}")
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            downloads = re.findall(r'href=[\'"](/Download/\d+/[^\'"]+)[\'"]', html)
            if not downloads:
                downloads = re.findall(r'href=[\'"](https?://peraturan\.bpk\.go\.id/Download/\d+/[^\'"]+)[\'"]', html)
            
            print(f"    Ditemukan links download: {downloads}")
            if downloads:
                dl_link = downloads[0]
                if dl_link.startswith('/'):
                    dl_link = f"https://peraturan.bpk.go.id{dl_link}"
                
                out_path = Path("30-sumber") / t['out_name']
                print(f"    Mengunduh dari {dl_link} ke {out_path}...")
                dl_req = urllib.request.Request(dl_link, headers=headers)
                with urllib.request.urlopen(dl_req, timeout=30) as dl_resp:
                    data = dl_resp.read()
                    out_path.write_bytes(data)
                    print(f"    [OK] Selesai unduh: {len(data) / 1024:.1f} KB")
            else:
                print(f"    [!] Tidak ditemukan link download di halaman {url}")
    except Exception as e:
        print(f"    [GAGAL]: {e}")
