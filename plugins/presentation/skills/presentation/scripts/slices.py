# slices.py <page.html> [outdir]
# Cuts the rendered page into 1080px-wide slices at native size, so they can be
# looked at without being shrunk. Shrinking a screenshot is how a bad chart gets
# through: the defects that shipped past a green grade were both invisible until
# someone opened the PNG at full size.
import os, sys
if len(sys.argv) < 2:
    print("Usage: python3 slices.py <page.html> [outdir]")
    sys.exit(2)
from playwright.sync_api import sync_playwright

f = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(f)) or "."
url = "file:///" + os.path.abspath(f).replace("\\", "/")
base = os.path.splitext(os.path.basename(f))[0]

with sync_playwright() as p:
    b = p.chromium.launch()
    # 1080px content column centred in a 1536px viewport, so it starts at x=228
    pg = b.new_page(viewport={"width": 1536, "height": 770}, device_scale_factor=2)
    pg.goto(url, wait_until="load"); pg.wait_for_timeout(700)
    H = pg.evaluate("document.documentElement.scrollHeight")
    y, i = 0, 1
    while y < H:
        h = min(940, H - y)
        pg.screenshot(path=os.path.join(out, "%s_sl%02d.png" % (base, i)),
                      full_page=True, clip={"x": 228, "y": y, "width": 1080, "height": h})
        y += h; i += 1
    print("%d slices, page height %dpx -> %s" % (i - 1, H, out))
    print("NOW OPEN THEM. grade.py cannot see an unreadable chart or a caption")
    print("that describes something the picture does not show.")
    b.close()
