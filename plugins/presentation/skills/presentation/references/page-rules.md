# Page rules: status, ending, type floor

These rules add to the ones in `SKILL.md`. Read them before building a page.

## Status is a named state or a count

Basecamp threw out percent-done because the to-do list grows as the work goes on, so the number lies in the direction that flatters. A dot that has not moved is a raised hand.

Give named states with counts drawn to scale ("3 need a browser opened, 3 need your hand, 2 need your opinion"). A count of what is waiting goes *up* when more is found. A percentage cannot do that.

## The page arrives, and it ends on a decision

Cockburn 2001: hallways make good information radiators and web pages do not, because opening a page costs more effort than people will spend. 25% of employees use the BI tools their company bought, unchanged across seven years of the same survey (BARC, 214 companies, 2022). Every format that survived is tied to an obligation: somebody must look, must speak, or may stop the line. So hand the page to the reader, and give them a decision only they can make.

## Type floor (APCA)

Not machine-checked; the grader does not read CSS. APCA ties the smallest size to contrast, so the floor is a pair:

| At | Nothing a person must read goes below |
|---|---|
| Lc 90 | 18px/300, 14px/400 |
| Lc 75, the minimum for a column of body text | 24px/300, 18px/400, 16px/500, 14px/700 |
| Lc 60, text that is not body or column text | 24px/400, 21px/500, 18px/600, 16px/700 |

13px is for incidental text only, never body. `scripts/apca.py` measures the Lc value.

## Three more things to leave off the page

- No `object-fit:cover` on a screenshot, and no whole-page thumbnail of a very tall page. Both crop away the evidence the caption points at. Crop to the region the caption names.
- No hero that takes a screen without answering anything.
- No content hidden at mobile width.

## Sources

- `evidence.md`: every source behind these rules, with URLs and sample sizes.
- `page-shape.md`: markup for the finding unit, drawn bars and a mark on a screenshot.
