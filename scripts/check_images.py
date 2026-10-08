"""Check that every object in the size table has a valid PNG in images/."""
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_DIMENSION = 256

table = re.search(r'size_table = "([^"]+)"', (ROOT / "src/shared.liquid").read_text()).group(1)
expected = set()
for entry in table.split(";"):
    name = entry.split("|")[1].lower().replace(" ", "-").replace("bunch-of-", "")
    expected.add(name)

images = {p.stem: p for p in (ROOT / "images").glob("*.png")}
errors = []

for name in sorted(expected - images.keys()):
    errors.append(f"missing image: images/{name}.png")
for name in sorted(images.keys() - expected):
    errors.append(f"unused image: images/{name}.png")

for name, path in sorted(images.items()):
    header = path.read_bytes()[:24]
    if header[:8] != PNG_SIGNATURE:
        errors.append(f"not a PNG: {path.name}")
        continue
    width, height = struct.unpack(">II", header[16:24])
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        errors.append(f"{path.name} is {width}x{height}, larger than {MAX_DIMENSION}x{MAX_DIMENSION}")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"{len(images)} images OK")
