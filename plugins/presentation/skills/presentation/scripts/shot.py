import sys, os
if len(sys.argv) < 2:
    print("Usage: python3 shot.py <page.html>")
    sys.exit(2)
from playwright.sync_api import sync_playwright
f = sys.argv[1]; url = "file:///" + os.path.abspath(f).replace("\\", "/")
with sync_playwright() as p:
    b = p.chromium.launch()
    for w, tag in ((1536, "wide"), (400, "phone")):
        pg = b.new_page(viewport={"width": w, "height": 770}, device_scale_factor=2)
        pg.goto(url, wait_until="load"); pg.wait_for_timeout(700)
        h = pg.evaluate("document.documentElement.scrollHeight")
        pg.screenshot(path="shot_%s_full.png" % tag, full_page=True)
        print(tag, w, "height", h, "%.1f screens" % (h/770.0))
        pg.close()
    b.close()
