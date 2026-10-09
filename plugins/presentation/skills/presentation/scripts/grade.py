# -*- coding: utf-8 -*-
"""grade.py - grade an HTML artifact on WORDS PER PICTURE before it ships.

    python grade.py <file.html> [more.html ...] [--json] [--heights]

One number sorted eight reader verdicts into the exact order the reader gave
them: words per picture. Word count alone predicts nothing. So this measures
pictures against words, finds the longest stretch of prose with no picture in
it, and prints a pass/fail verdict instead of a pile of numbers.

Standard library only for parsing. Playwright is used ONLY behind --heights,
so the script runs with no browser and no server.

Console output is ASCII only (Windows consoles often use cp1252).
"""

import io
import json
import os
import re
import sys
from html.parser import HTMLParser

# ---------------------------------------------------------------- thresholds
GAP_FAIL = 450          # words with no picture in them
WPV_WARN = 85           # words per visual
WPV_FAIL = 150
SECTIONS_PER_VIEW_WARN = 6
VIEW_PX_WARN = 8000

SKIP_TAGS = ("script", "style", "head")
VOID_TAGS = set("""area base br col embed hr img input link meta param
                   source track wbr""".split())

# A "drawing" is a hand-drawn block: a bar chart, a scale, a holder. Pages use
# a wrapper (class "drawn"/"board") around several bars (class "scale"/"hold"),
# and the whole block is ONE picture to a reader, not one picture per bar. So a
# drawing element nested inside another drawing element is not counted again.
DRAW_CLASSES = ("drawn", "scale", "hold", "board")
# The bars themselves. Their tick labels are marks on the picture, not prose.
MARK_CLASSES = ("scale", "hold")

GAP_WORDS_SHOWN = 12


def ascii_only(s):
    """cp1252-safe. Fold the punctuation we actually emit, drop the rest."""
    for bad, good in ((u"—", "-"), (u"–", "-"), (u"‒", "-"),
                      (u"·", "-"), (u"•", "-"), (u"…", "..."),
                      (u"‘", "'"), (u"’", "'"), (u"“", '"'),
                      (u"”", '"'), (u" ", " "), (u" ", " "),
                      (u"×", "x"), (u"→", "->")):
        s = s.replace(bad, good)
    return s.encode("ascii", "replace").decode("ascii")


class Grader(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.skip = 0
        self.stack = []          # [tag, is_counted_drawing, is_mark]
        self.in_draw = 0         # open drawing elements
        self.in_mark = 0         # open bars/ticks: their text is the picture

        self.words = 0
        self.photos = 0
        self.drawings = 0
        self.h2 = 0
        self.views = 0

        # picture-free gap
        self.run = 0             # words since the last visual
        self.run_start = ""      # first words of the current run
        self.worst = 0
        self.worst_start = ""
        self.gaps = []

    # -- gaps -------------------------------------------------------------
    def visual(self):
        """A picture was passed: close the current stretch of prose."""
        self.gaps.append(self.run)
        if self.run > self.worst:
            self.worst = self.run
            self.worst_start = self.run_start
        self.run = 0
        self.run_start = ""      # the next stretch starts where its text does

    # -- tags -------------------------------------------------------------
    def _start(self, tag, attrs, void):
        d = dict(attrs)
        classes = (d.get("class") or "").split()

        if tag in SKIP_TAGS:
            self.skip += 1

        is_draw = False
        is_mark = False
        if self.skip == 0:
            if tag == "img":
                self.photos += 1
                self.visual()
            elif tag == "svg" or any(c in DRAW_CLASSES for c in classes):
                if self.in_draw == 0:
                    self.drawings += 1
                    self.visual()
                    is_draw = True
                if tag == "svg" or any(c in MARK_CLASSES for c in classes):
                    is_mark = True
            if tag == "h2":
                self.h2 += 1
            if "data-view" in d or "view" in classes:
                self.views += 1

        if not void and tag not in VOID_TAGS:
            self.stack.append([tag, is_draw, is_mark])
            if is_draw:
                self.in_draw += 1
            if is_mark:
                self.in_mark += 1

    def handle_starttag(self, tag, attrs):
        self._start(tag, attrs, False)

    def handle_startendtag(self, tag, attrs):
        self._start(tag, attrs, True)

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS and self.skip > 0:
            self.skip -= 1
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                for item in self.stack[i:]:
                    if item[1]:
                        self.in_draw -= 1
                    if item[2]:
                        self.in_mark -= 1
                del self.stack[i:]
                return

    def handle_data(self, data):
        # A bar's own tick label is part of the picture, not prose the reader
        # has to wade through, so it is not counted. The caption under a
        # drawing IS prose and is counted.
        if self.skip or self.in_mark:
            return
        w = data.split()
        if not w:
            return
        if not self.run_start:
            self.run_start = " ".join(w[:GAP_WORDS_SHOWN])
        elif len(self.run_start.split()) < GAP_WORDS_SHOWN:
            need = GAP_WORDS_SHOWN - len(self.run_start.split())
            self.run_start += " " + " ".join(w[:need])
        self.words += len(w)
        self.run += len(w)


def measure(path):
    src = io.open(path, encoding="utf-8", errors="replace").read()
    g = Grader()
    g.feed(src)
    g.close()
    g.visual()                       # last picture -> end of document

    visuals = g.photos + g.drawings
    views = g.views if g.views else 1
    r = {
        "file": path,
        "words": g.words,
        "photos": g.photos,
        "drawings": g.drawings,
        "visuals": visuals,
        "words_per_visual": (round(float(g.words) / visuals, 1)
                             if visuals else None),
        "worst_gap": g.worst,
        "worst_gap_starts": ascii_only(g.worst_start),
        "top_gaps": sorted(g.gaps, reverse=True)[:3],
        "sections": g.h2,
        "views": views,
        "sections_per_view": round(float(g.h2) / views, 1),
        "heights": None,
        "clipped": None,
    }
    return r


# ------------------------------------------------------------------ verdict
def verdict(r):
    """Return (lines, failed). Each line says what to do, in plain English."""
    lines = []
    failed = False

    gap = r["worst_gap"]
    if gap > GAP_FAIL:
        failed = True
        lines.append(("FAIL", "%d words run with no picture in them (limit %d). "
                              "Add a photograph or a drawing here: \"%s\""
                      % (gap, GAP_FAIL, r["worst_gap_starts"] or "(start of the page)")))
    else:
        lines.append(("PASS", "longest picture-free stretch is %d words (limit %d)"
                      % (gap, GAP_FAIL)))

    wpv = r["words_per_visual"]
    if wpv is None:
        failed = True
        lines.append(("FAIL", "%d words and not one picture. This page cannot be read. "
                              "Add pictures until there is one every %d words."
                      % (r["words"], WPV_WARN)))
    elif wpv > WPV_FAIL:
        failed = True
        lines.append(("FAIL", "%.1f words per picture (limit %d). Cut words or add about "
                              "%d more pictures."
                      % (wpv, WPV_FAIL, _need(r, WPV_WARN))))
    elif wpv > WPV_WARN:
        lines.append(("WARN", "%.1f words per picture (comfortable is %d). About %d more "
                              "pictures would bring it under."
                      % (wpv, WPV_WARN, _need(r, WPV_WARN))))
    else:
        lines.append(("PASS", "%.1f words per picture (comfortable is %d)" % (wpv, WPV_WARN)))

    spv = r["sections_per_view"]
    if spv > SECTIONS_PER_VIEW_WARN:
        lines.append(("WARN", "%.1f sections per view (%d h2 across %d view(s)). Each section "
                              "is a question; split the page or drop questions until it is %d."
                      % (spv, r["sections"], r["views"], SECTIONS_PER_VIEW_WARN)))
    else:
        lines.append(("PASS", "%.1f sections per view (%d h2 across %d view(s))"
                      % (spv, r["sections"], r["views"])))

    if r["heights"]:
        # Height is reported, never graded. The 8000px ceiling that used to live here was
        # invented, and the reader verdicts it was tested on contradict it: the accepted page is
        # 10,694px and the page that read slowly is 5,673px, so height does not
        # separate them at all. Words per picture does. A threshold that would fail the
        # accepted page and pass the rejected one is worse than no threshold, and R5
        # says draw only what was measured.
        tallest = max(h for _, h in r["heights"])
        lines.append(("NOTE", "tallest view is %dpx, %.1f screens. For scale: the page you "
                              "like is 10694px and the one you cannot read is 5673px, so "
                              "this number is context, not a grade."
                      % (tallest, tallest / 770.0)))

    if r["clipped"] is not None:
        if r["clipped"]:
            failed = True
            for c in r["clipped"]:
                lines.append(("FAIL", "a label is cut off at %dpx wide and the page does not say "
                                      "so: \"%s\" needs %dpx but has %dpx. Widen it or shorten "
                                      "the text." % (c["width"], ascii_only(c["text"]),
                                                     c["scroll"], c["client"])))
        else:
            lines.append(("PASS", "no clipped labels at 1536 or 400 wide"))

    return lines, failed


def _need(r, target):
    """How many more visuals to reach `target` words per visual."""
    import math
    want = int(math.ceil(r["words"] / float(target)))
    return max(0, want - r["visuals"])


# ------------------------------------------------------------------ heights
CLIP_JS = r"""() => {
  /* A label is only CUT OFF if the excess is not painted anywhere the reader can get to.
     scrollWidth > clientWidth alone does not mean that: with the default overflow:visible
     the text spills out of its box and is still fully legible. So measure where the text
     is actually painted (a Range over its contents) against the first ancestor that really
     clips - and treat a genuine scroller as reachable, not cut off. */
  var vw = document.documentElement.clientWidth;
  var bad = [];
  var all = document.querySelectorAll('body *');
  for (var i = 0; i < all.length; i++) {
    var e = all[i];
    if (e.tagName === 'SCRIPT' || e.tagName === 'STYLE') continue;
    if (!e.getClientRects().length) continue;
    var t = (e.textContent || '').replace(/\s+/g, ' ').trim();
    if (!t) continue;
    var own = false;
    for (var k = 0; k < e.childNodes.length; k++)
      if (e.childNodes[k].nodeType === 3 && e.childNodes[k].textContent.trim()) own = true;
    if (!own) continue;                       /* report the node holding the text, not its wrappers */
    var limit = vw, why = 'the viewport', scroller = false;
    for (var p2 = e; p2; p2 = p2.parentElement) {
      var st = getComputedStyle(p2);
      var ox = st.overflowX;
      if (ox === 'visible') continue;
      if (ox === 'auto' || ox === 'scroll') { scroller = true; break; }
      var rc = p2.getBoundingClientRect();
      limit = Math.min(limit, rc.right);
      why = p2.tagName.toLowerCase() + (p2.className ? '.' + p2.className : '');
      break;
    }
    if (scroller) continue;                   /* reachable by scrolling it */
    var r = document.createRange(); r.selectNodeContents(e);
    var box = r.getBoundingClientRect();
    if (box.width === 0) continue;
    if (box.right > limit + 1)
      bad.push({text: t.slice(0, 50), scroll: Math.round(box.right),
                client: Math.round(limit), tag: e.tagName.toLowerCase(),
                cls: e.className || '', why: why});
  }
  return bad;
}"""

SHOW_JS = """(idx) => {
  var vs = document.querySelectorAll('[data-view], .view');
  for (var i = 0; i < vs.length; i++) {
    if (i === idx) { vs[i].removeAttribute('hidden'); vs[i].style.display = ''; }
    else { vs[i].setAttribute('hidden', ''); vs[i].style.display = 'none'; }
  }
  var v = vs[idx];
  return v.id || v.getAttribute('data-view') || ('view ' + (idx + 1));
}"""

COUNT_JS = "() => document.querySelectorAll('[data-view], .view').length"


def with_browser(path, r):
    from playwright.sync_api import sync_playwright
    url = "file:///" + os.path.abspath(path).replace("\\", "/")
    heights = []
    clipped = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for width in (1536, 400):
            pg = b.new_page(viewport={"width": width, "height": 770})
            pg.goto(url, wait_until="load")
            pg.wait_for_timeout(300)
            n = pg.evaluate(COUNT_JS)
            for i in range(max(n, 1)):
                name = pg.evaluate(SHOW_JS, i) if n else "whole page"
                pg.wait_for_timeout(120)
                tall = pg.evaluate("document.documentElement.scrollHeight")
                if width == 1536:
                    heights.append((ascii_only(str(name)), int(tall)))
                for c in pg.evaluate(CLIP_JS):
                    c["width"] = width
                    c["view"] = ascii_only(str(name))
                    clipped.append(c)
            pg.close()
        b.close()
    r["heights"] = heights
    r["clipped"] = clipped
    return r


# ------------------------------------------------------------------- output
def show(r):
    out = []
    out.append("=" * 72)
    out.append(r["file"])
    out.append("=" * 72)
    out.append("  words ................ %d" % r["words"])
    out.append("  photos ............... %d" % r["photos"])
    out.append("  drawings ............. %d" % r["drawings"])
    out.append("  visuals .............. %d" % r["visuals"])
    out.append("  words per visual ..... %s"
               % ("%.1f" % r["words_per_visual"] if r["words_per_visual"] is not None
                  else "no visuals"))
    out.append("  worst gap ............ %d words   (next: %s)"
               % (r["worst_gap"], ", ".join(str(g) for g in r["top_gaps"][1:]) or "-"))
    out.append("  it starts at ......... \"%s\""
               % (r["worst_gap_starts"] or "(start of the page)"))
    out.append("  sections (h2) ........ %d" % r["sections"])
    out.append("  views ................ %d" % r["views"])
    if r["heights"]:
        out.append("  view heights at 1536 .")
        for n, h in r["heights"]:
            out.append("      %-22s %6dpx  %.1f screens" % (n[:22], h, h / 770.0))
    out.append("")
    lines, failed = verdict(r)
    for tag, msg in lines:
        first = True
        for chunk in wrap(msg, 62):
            out.append("  %-5s %s" % (tag if first else "", chunk))
            first = False
    out.append("")
    out.append("  VERDICT: %s" % ("FAIL - do not ship this page" if failed
                                  else "ship it"))
    out.append("")
    return "\n".join(out), failed


def wrap(text, width):
    words, line, lines = text.split(), "", []
    for w in words:
        if line and len(line) + 1 + len(w) > width:
            lines.append(line)
            line = w
        else:
            line = (line + " " + w) if line else w
    if line:
        lines.append(line)
    return lines


def main(argv):
    files = [a for a in argv if not a.startswith("--")]
    as_json = "--json" in argv
    heights = "--heights" in argv
    if not files:
        sys.stdout.write("Usage: " + __doc__.split("\n\n")[1].strip() + "\n")
        return 2

    results, any_fail = [], False
    for f in files:
        if not os.path.exists(f):
            sys.stdout.write("missing file: %s\n" % f)
            any_fail = True
            continue
        r = measure(f)
        if heights:
            try:
                with_browser(f, r)
            except Exception as e:
                sys.stdout.write("  (--heights skipped for %s: %s)\n"
                                 % (f, ascii_only(str(e))[:160]))
        text, failed = show(r)
        # Check that the page can be rebuilt from data and uses section bands.
        d = os.path.dirname(os.path.abspath(f))
        names = os.listdir(d)
        has_data = any(n.endswith(".json") for n in names)
        has_build = any(n.startswith("build.") for n in names)
        src = open(f, encoding="utf-8", errors="replace").read()
        has_bands = 'class="band' in src
        if not (has_data and has_build):
            failed = True
            text += ("\n  FAIL  no data file and build script next to the page (Phase 1). "
                     "Write data.json and build.py, then build the page from them.")
        if not has_bands:
            failed = True
            text += ("\n  FAIL  the page does not use the house grammar (band, tag, cards). "
                     "Define .band, .tag and .cards in the page or a project stylesheet.")
        if not (has_data and has_build and has_bands):
            text = text.replace("VERDICT: ship it", "VERDICT: FAIL - do not ship this page")
        r["verdict"] = [{"level": t, "say": ascii_only(m)} for t, m in verdict(r)[0]]
        r["failed"] = failed
        results.append(r)
        any_fail = any_fail or failed
        if not as_json:
            sys.stdout.write(ascii_only(text) + "\n")

    if as_json:
        sys.stdout.write(json.dumps(results, indent=2, ensure_ascii=True) + "\n")
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
