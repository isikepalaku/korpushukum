import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from static_cell_map import sector_color


def test_estimated_sector_uses_transparent_red_fill():
    assert sector_color("estimated_from_sector_numbering") == (220, 38, 38, 65)


def test_verified_sector_uses_transparent_blue_fill():
    assert sector_color("verified") == (26, 101, 191, 105)
