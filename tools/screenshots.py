"""Take screenshots of the running app (needs: pip install playwright && playwright install chromium)."""
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent.parent / "docs"
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1200, "height": 900})
    pg.goto("http://127.0.0.1:5000/")
    pg.wait_for_selector(".card")
    pg.screenshot(path=str(OUT / "product-listing.png"), full_page=True)
    pg.fill("#search", "book")
    pg.wait_for_timeout(800)
    pg.screenshot(path=str(OUT / "product-search.png"), full_page=True)
    pg.goto("http://127.0.0.1:5000/product?id=1")
    pg.wait_for_selector(".detail img")
    pg.screenshot(path=str(OUT / "product-details.png"), full_page=True)
    b.close()
print("done")
