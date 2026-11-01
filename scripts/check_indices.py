import os
import glob
from pathlib import Path
import yaml

peraturan_files = list(Path('10-peraturan').glob('*/*.md'))
moc_files = list(Path('01_INDEX_MOC').glob('_Index_*.md'))
legislation_dirs = [d for d in Path('02_LEGISLATION').iterdir() if d.is_dir()]

print(f"Total berkas di 10-peraturan: {len(peraturan_files)}")
print(f"Total indeks MOC di 01_INDEX_MOC: {len(moc_files)}")
print(f"Total folder UU di 02_LEGISLATION: {len(legislation_dirs)}")

peraturan_with_articles = []
peraturan_datar = []

for p in sorted(peraturan_files):
    text = p.read_text(encoding='utf-8')
    fm = {}
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            try:
                fm = yaml.safe_load(parts[1])
            except Exception:
                pass
    st = fm.get('struktur_teks', '')
    doc_id = fm.get('id', p.stem)
    if st == 'terpartisi':
        peraturan_with_articles.append((p, doc_id))
    else:
        peraturan_datar.append((p, doc_id))

print(f"Dokumen terpartisi (memiliki pasal-pasal): {len(peraturan_with_articles)}")
print(f"Dokumen struktur datar (non-pasal: Inpres, Jukrah, dll): {len(peraturan_datar)}")

# Map expected MOC filename
moc_names = {f.name: f for f in moc_files}
missing_moc = []
matched_moc = []

for p, doc_id in peraturan_with_articles:
    parts = doc_id.split()
    if len(parts) >= 2:
        num_year = parts[1].replace('/', '_')
        code = f"{parts[0]}_{num_year}"
    else:
        code = doc_id.replace(' ', '_').replace('/', '_')
    expected_moc = f"_Index_{code}.md"
    if expected_moc in moc_names:
        matched_moc.append((doc_id, expected_moc))
    else:
        missing_moc.append((doc_id, expected_moc, p.name))

print(f"\nStatus Kecocokan Indeks:")
print(f"- Terpartisi yang SUDAH memiliki file indeks MOC: {len(matched_moc)}")
print(f"- Terpartisi yang BELUM memiliki file indeks MOC: {len(missing_moc)}")

if missing_moc:
    print("\nDaftar yang belum memiliki MOC:")
    for m in missing_moc:
        print(f"  - {m[0]} ({m[2]}) -> dicari: {m[1]}")

# Also check 01-undang-undang specifically
uu_files = list(Path('10-peraturan/01-undang-undang').glob('*.md'))
print(f"\nKhusus Kategori 'Undang-Undang' (UU):")
print(f"- Total berkas UU di 10-peraturan/01-undang-undang: {len(uu_files)}")
uu_missing = []
for p in uu_files:
    text = p.read_text(encoding='utf-8')
    fm = yaml.safe_load(text.split('---', 2)[1]) if text.startswith('---') else {}
    doc_id = fm.get('id', p.stem)
    parts = doc_id.split()
    num_year = parts[1].replace('/', '_') if len(parts) >= 2 else doc_id
    code = f"UU_{num_year}"
    expected = f"_Index_{code}.md"
    if expected not in moc_names:
        uu_missing.append((doc_id, expected, p.name))

print(f"- Total berkas UU yang punya MOC: {len(uu_files) - len(uu_missing)}")
print(f"- UU tanpa MOC: {len(uu_missing)}")
if uu_missing:
    for u in uu_missing:
        print(f"  - {u[0]}: {u[1]}")

