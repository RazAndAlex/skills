---
name: presentation
description: "Build an evidence page that helps the reader understand work and make a decision. Six phases with gates: measured data, one question, pictures, plain-English writing, script checks and visual review, then delivery. Writing helpers are optional."
---

# Presentation

A page that reports work to the reader and shows the evidence behind it.

If `~/.claude/presentation.local.md` exists, read it first; it holds the local reader's preferences and overrides the defaults here.

The test is whether the reader understands the work well enough to disagree with it.

Why this rule exists: readers report that long walls of text make their eyes glaze over, and they stop reading.

## How this skill works

This file holds the phases and gates. Optional writing helpers improve the prose in phase 4. Scripts in `scripts/` measure pictures and catch AI tells. They cannot judge whether a chart is readable, so phase 5 also requires visual review.

A phase that fails its gate repeats. Resolve script paths relative to this skill's directory and keep generated pages and data in the project.

## Phase 1: the claim has to come from data

Before writing a sentence, have the numbers. Generate every chart from a data file so figures in the prose match their source.

Write an extraction and build script. Keep the data file and a `build.*` script beside the page so it can be rebuilt later.

- Gate: every number on the page exists in the data file, and the build script turns that file into markup. A number typed by hand fails.

## Phase 2: one question and a plain title

The reader decides whether to open the page from its title.

- A section answers a question. Count headed sections and check whether they answer the same question.
- Length is part of the promise. Keep each page short enough to scan, with orienting numbers visible without scrolling.
- Several questions need several short pages inside one artifact.
- Two pages that share the same structure and differ only in the opening are one option.
- The title names the subject in plain words and adds the main number when useful, such as "Build time this week: 38 minutes of 67".
- Slogans, teasing verdicts and bare labels such as "Sprint 7 Recap" fail. Put the finding in the first sentence under the heading.
- Use the same rule for section headings.
- An eyebrow names the project and the kind of page as `PROJECT / KIND`, using words the reader recognises.
- Put provenance near the top: what was read, how much, where it came from and where the result went.

- Gate: state the one question in a sentence, then check every headed section against it. A second question needs another page.

## Phase 3: build it as pictures with prose between them

Lead with the visual. A finding has an id, one declarative sentence the reader could dispute, two or three sentences of detail, and a picture.

- Show the source. Quote the evidence or screenshot the defect and mark it.
- Annotate screenshots. A band, ring or arrow should point to the thing the caption names.
- Crop evidence screenshots instead of shrinking them. Render crops at native pixel width in a box with `overflow-x: auto` when they exceed the column.
- For a whole screen of a design option, show the full screen at the column width and let a click open it at life size.
- Compare options in a grid cropped to the regions where they differ. Make each preview clickable for inspection at life size.
- Separate similar full-screen examples clearly so the reader can see where one ends and another begins.
- A caption must describe what its picture actually shows.
- A choice shows every option side by side and names one recommendation with a reason.
- Encode values as length. Label marks directly instead of requiring a colour legend.
- Group by what the reader does.
- Put any error in the work near the top and explain its effect.

- Gate: every claim has a picture, quote or number beside it.

### Read earlier artifacts before building

Read earlier artifacts in the project and recover the conventions the reader accepted. Use a reading tool if available; otherwise open the files or URLs. A worker may read several and report the conventions.

Keep paragraphs short, around 66 characters per line where practical. Use cards, grids and bands when they help the comparison. Quote the reader verbatim with a citation. Write counts as "N of M" beside the target, with a file path, line number or source link for each claim.

Use `.band` for major sections, `.tag` for the eyebrow and `.cards` for option groups. Define their styles in the page or a project stylesheet. The grader checks for `class="band` as well as the data and build files.

### Build on the good page by subtracting

When the reader points to a page that works, start there and remove what the new page does not need. Each new control or label needs a reason.

Why this rule exists: readers describe dense tile grids as hard to read, a lot of items that say nothing.

A dense grid of short labels still requires a lot of reading. Label the evidence directly. Any control that moves the reader away from a location must provide a way back.

Read `references/page-rules.md` before building. It adds four rules: show status as a count or a named state; end the page on a decision only the reader can make; respect the APCA type floor; and leave three more things off the page.

## Phase 4: write plain English

Write page copy in English. The writing pass is required; helper skills are optional.

If `bro`, `unslop` and an STE100-style rewriting skill such as `ste-writing` are installed, run them in that order. Use their names as exposed by the current skill list. `bro` and `unslop` come from [pstack in Cursor's plugins](https://github.com/cursor/plugins/tree/main/pstack). Use the STE-style skill's general-prose mode if available, so the page keeps its voice.

If any helper is unavailable, apply this built-in pass:

1. State the result or decision early.
2. Use one main idea per sentence. Split sentences the reader has to reread.
3. Name the actor and use active verbs: "the checker found two failures".
4. Prefer plain words such as "use", "help" and "because".
5. Replace jargon with a concrete description. Define necessary terms on first use.
6. Delete filler, promotional claims, vague attributions and stacked hedges.
7. Remove chatbot phrases, forced contrasts, slogans and decorative punctuation.
8. Preserve quoted speech exactly, including typos. Keep source citations beside claims.

Run `scripts/slop.py` either way. It is the floor for the writing check, and it protects `<blockquote>` text.

- Gate: record either the helper sequence or the built-in pass, then require the prose gate from `slop.py`. The script checks prose patterns; it cannot prove that a helper ran.

## Phase 5: grade it, then look at it

These commands run from the skill directory:

```sh
python3 scripts/grade.py  <page.html> --heights
python3 scripts/slop.py   <page.html>
python3 scripts/slices.py <page.html>
```

The scripts require Python 3. `grade.py --heights`, `shot.py` and `slices.py` also require Playwright with Chromium. Install them if absent:

```sh
python3 -m pip install playwright
python3 -m playwright install chromium
```

`grade.py` measures the longest picture-free stretch, failing above 450 words, and words per picture, warning above 85 and failing above 150. It also checks sections per view, data/build files and page bands. With `--heights`, it checks clipping at 1536 and 400 pixels wide. If it reports that browser checks were skipped, resolve the dependency and rerun before passing the gate.

`slop.py` checks the sentences and protects every `<blockquote>`. `shot.py <page.html>` captures wide and phone sizes. `slices.py` produces crops for inspection. `apca.py --demo` prints the bundled contrast examples.

Open every slice at full size. Check that values read correctly and each caption matches its picture. Click every control as the reader would.

- Gate: `grade.py` says ship it, `slop.py` says the prose gate passed, browser checks ran, and every slice was visually reviewed.

Do not game the grader. Fix a bad words-per-picture score with useful pictures or fewer words. Splitting one chart into several counted elements does not improve the page.

### Check status claims against receipts

Read every sentence that states the status of code or work: "passes", "written", "shipped", "merged", "fixed" or "runs on Windows". Put its receipt beside it: command and exit code, file, commit or link.

If the receipt is missing, label the claim planned or unverified. A status claim without evidence fails the gate.

## Phase 6: deliver with the decision on top

If a publishing tool is available and publication is authorised, publish the page and return its URL. Otherwise save a self-contained HTML page in the project and return a file link.

The top of the page uses this order:

```text
SETTLED     what is already decided, dated, in the reader's words
DECIDE      the call the reader needs to make
NEXT        what happens now
UNDERSTAND  the explanation
```

Carry earlier decisions forward with their dates and exact wording. Put familiar material below a clear divider or cut it. Make new material easy to find. Use the same order in the reply.

### Close completed decisions

When the reader makes the call, remove the pending-decision heading, option cards and recommendation markers. Replace them with what was decided, what it produced and any work still available.

Why this rule exists: a page that still shows a recommendation after the reader decided looks stale, and readers ask for it to be fixed.

- Gate: the reader can see the decision without scrolling. The reply is a few lines and a link; longer evidence belongs on the page.

## Presenting finished work to a decision maker

Lead with what the work is, what it cost, what it proves and what is worth doing next.

Assume no prior knowledge. Define each necessary term where it first appears. Provide an executive account for a non-technical reader and a technical path for a reader who wants to inspect the design.

Compare what was done with what was planned. Include deviations and open problems. The page must stand on its own for someone who did not follow the work.

## Scope

Use `design-round` when the question is which visual design to choose. Use this skill when the question is what the work found or produced.

Each page answers one question. The phases are gates, so the evidence determines the layout.
