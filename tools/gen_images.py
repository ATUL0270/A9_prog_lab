"""Generate simple placeholder SVG product images (no internet needed).

Usage: python tools/gen_images.py
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "frontend" / "images"
OUT.mkdir(parents=True, exist_ok=True)

ITEMS = {
    "headphones": ("Headphones", "#4263eb"),
    "keyboard": ("Keyboard", "#7048e8"),
    "watch": ("Smart Watch", "#0ca678"),
    "powerbank": ("Power Bank", "#f08c00"),
    "book-clean-code": ("Clean Code", "#d6336c"),
    "book-algorithms": ("Algorithms", "#1c7ed6"),
    "book-dbms": ("DBMS", "#e8590c"),
    "bottle": ("Water Bottle", "#0b7285"),
    "pan": ("Frying Pan", "#495057"),
    "kettle": ("Kettle", "#c92a2a"),
    "yogamat": ("Yoga Mat", "#5f3dc4"),
    "racket": ("Racket Set", "#2b8a3e"),
}

TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" width="600" height="450" viewBox="0 0 600 450">
  <rect width="600" height="450" fill="{color}"/>
  <circle cx="300" cy="190" r="80" fill="rgba(255,255,255,0.22)"/>
  <text x="300" y="320" font-family="Arial, sans-serif" font-size="40" font-weight="bold"
        fill="#fff" text-anchor="middle">{label}</text>
</svg>
"""

for name, (label, color) in ITEMS.items():
    (OUT / f"{name}.svg").write_text(TEMPLATE.format(label=label, color=color), encoding="utf-8")

print(f"Wrote {len(ITEMS)} images to {OUT}")
