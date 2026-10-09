# Building the page

The concrete shape. Read this while writing the HTML.

---

## Before writing anything

1. Write the question in one sentence. If two sentences are needed, it is two pages.
2. List the numbers that answer it. These go above the fold, drawn to scale.
3. List the evidence that exists. A finding with no picture is a one-line entry, not a
   section — do not pad it up to look like the ones that have proof.
4. Decide the one decision the page ends on.

## The five parts, in order

**Provenance line.** Project, body of work, date, scope, in one line of mono at 14–15px,
above the title. `NORTHWIND · SHELL AUDIT · 2 MARCH 2026 · 32 FINDINGS`. The
reader must be able to tell which project and which body of work this reports on without
scrolling. A page that opens straight onto a decision headline gets mistaken for something
the project produced about itself.

**Title.** States the stake. See the title rule in `SKILL.md`.

**The orienting numbers, drawn to scale, above the fold.** Two bars: the whole set split
once, then the part that matters blown up to full width. Label each segment directly inside
or beside it. No colour key.

**Sections.** One `<h2>` per question. Each carries a mono eyebrow naming the question and a
display-face line stating its answer: `WHAT IS WAITING ON YOU` / `Eight, and three of them
cost you one sentence`.

**The unit.** Every finding is the same markup so the frame is decoded once:

```html
<div class="defect">
  <div class="hd"><span class="id">08</span><span class="claim">The close button is a
    smudge, and only the front tab has one.</span></div>
  <p class="cap">Two or three sentences. No more.</p>
  <figure>
    <span class="shot"><img src="…"><span class="mark ring" style="…"></span></span>
    <figcaption>Ringed, that is the close button.</figcaption>
  </figure>
</div>
```

The claim is one declarative sentence the reader could argue with. Findings with no picture
use the same markup with the figure omitted and no padding sentences.

**The decision.** Two or three routes, what each clears, which one would be taken and why.
One is marked as the recommendation.

---

## Type

| Element | Size / weight |
|---|---|
| Body | 16px/400 at Lc 92, or the pair for the contrast actually used |
| Captions, secondary prose | 15–16px |
| The claim sentence | 20–22px, display face |
| Section title | clamp(27px, 3.9vw, 38px), display face, weight 400 |
| `h1` | clamp(28px, 3.4vw, 40px), max-width 30ch |
| Mono eyebrows, provenance | 14–15px |

The size floor is a size/weight pair at a measured contrast, not a single number — the table
is in `SKILL.md`, and none of it is machine-checked. Measure the pair before shrinking
anything. Mono is for literals, ids, dates and scale labels. Nothing goes below 13px, and
13px is for incidental text only. No label is smaller or fainter than what it labels.

Measure widths in `ch`: body 66–72ch, the lede 34ch, the title 30ch.

---

## Pictures

**The mark is the evidence.** A ring, an amber band, or a filled overlay drawn on top of the
screenshot, absolutely positioned over the region, with the caption naming it: "ringed, that
is the close button". A raw crop with a caption underneath is weaker.

```css
.mark { position:absolute; border:2px solid var(--amber); border-radius:3px;
        box-shadow:0 0 0 9999px rgba(13,12,20,.45); pointer-events:none; }
```

**Never `object-fit:cover`.** It exists to make a picture fill a box attractively, which is
the opposite of what proof needs. Use `max-height` with `width:auto` so the image keeps its
aspect ratio and the annotated detail survives.

**Crop to the defect, not to the window.** A whole-page thumbnail of a very tall page proves
nothing at the size it will be seen.

**Wide evidence keeps its natural width.** A 2592px strip squeezed into a 310px phone column
is a 12px sliver. Let the figure scroll horizontally on narrow screens, park it on its mark,
and put a `swipe →` cue in the caption. Nothing is hidden at mobile width.

---

## Drawings

Only what was measured. A drawing stands in for a photograph where a number was read off the
running thing; never where behaviour was only read out of source.

Segments in a flex row, width as a percentage of the real quantity, the label inside the
segment. Two states of emphasis at most — the part that needs the reader, and everything
else:

```css
.scale { display:flex; gap:2px; height:52px; }
.scale span { display:flex; align-items:center; padding:0 13px; }
```

Stack the segments vertically below 620px and drop each label underneath at full width. A
label squeezed inside an 84px segment truncates to `3 · a brows…` and the drawing stops
saying anything.

Comparing two heights: put both bars in holds of equal height so they share a baseline.
Otherwise a label that wraps to a third line lifts one bar and the comparison is a lie.

---

## What to measure before drawing

Open the thing at **1536x770** and read back real numbers: pane widths, row heights, column
counts, character counts at the width where truncation starts. A defect proven at the level
of a single character is the strongest evidence available — at 62 columns the line reads
"recalled", at 61 it reads "recalle", and nothing says so.

---

## Structure the page by what a person does

Group findings by the reader's action, not by code area or commit: "Opening something",
"Moving something", "Closing something", "Reading something". Or by what each one needs from
the reader: "stopped on a measurement", "stopped on your hand", "stopped on your opinion".

Put "what I got wrong" near the top. A section that voids the author's previous round in
plain words earns more credit than a section listing missing evidence, because it is about
the author being wrong rather than about the data being thin.

---

## Counting the page

Before running the grader, count by hand:

- `<h2>` elements — that is how many questions the page asks. Over 6 per view is a WARN.
- Total words divided by number of pictures — over 85 is a WARN, over 150 a FAIL.
- The longest run of words with no picture in it — over 450 is a FAIL.
- With `--heights`: text that cannot be seen or reached at 1536 or 400 wide is a FAIL. The
  check measures where the text is actually painted against the first ancestor that really
  clips it, and counts a horizontal scroller as reachable. The trap: an element overflowing
  its box is not the same thing as text being cut off, because under `overflow: visible` it
  spills out and stays readable. View height is printed as a NOTE and never graded.

If several questions are genuinely in scope, build several short pages inside one artifact,
each reachable from a picker at the top. Never one long page that changes topic partway
down. The user reads "answers one question" as a promise about scrolling.

---

## Use the product's own colours

A recap in generic report greys reads as something made elsewhere about the product. Take
the palette and the display face from the thing being reported on. Review scaffolding —
grader output, threshold annotations, notes to self — never appears inside a specimen in the
product's own tokens.
