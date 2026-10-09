# image-gen

A Claude Code plugin that lets Claude draw real images. Claude plans the assets and writes every prompt. A Codex worker runs OpenAI's image model, draws one image per prompt and stops. The result is a set of transparent cutouts, logos, icons, textures and backgrounds that Claude layers into the page it is building.

Claude uses it by itself when frontend or brand work needs a picture. You do not have to ask for it.

## What you need

- [Codex CLI](https://github.com/openai/codex), signed in with a ChatGPT plan. The built-in image tool needs no API key.
- Python 3 with Pillow and numpy: `pip install pillow numpy`

## Install

```
claude plugin marketplace add RazAndAlex/skills
claude plugin install image-gen@razandalex-skills
```

Start a new Claude Code session after installing.

## How a set gets made

1. Claude lists the assets the page needs, for example a mug, beans and steam for a coffee hero.
2. It draws the first one, the anchor, and looks at it.
3. It draws the rest with the anchor as a style reference, so the set matches.
4. `cleanup.py` trims each image, removes the coloured fringe on transparent edges and writes webp.
5. Claude places the files in the page and checks them in the browser.

Each image takes about a minute and 30k to 65k Codex tokens. Images drawn in parallel finish together.

## Files

| Path | What it is |
|---|---|
| `skills/image-gen/SKILL.md` | The steps Claude follows |
| `skills/image-gen/PROMPTS.md` | The prompt template, with a worked example |
| `skills/image-gen/scripts/draw.py` | Runs one Codex draw and saves the PNG |
| `skills/image-gen/scripts/cleanup.py` | Trims, fixes edges, writes webp |
| `evals/` | Counts how often Claude loads the skill on its own |

## The session reminder

Claude sees a skill as one line in a list, and a busy list hides it. So the plugin also adds a 45-word note at the start of every session. The note tells Claude that it can draw and when to do it. The text is in `hooks/reminder.txt`, and `hooks/hooks.json` prints it through a SessionStart hook.

To switch the reminder off, delete the `hooks` folder. The skill keeps working without it.

## Checking that Claude reaches for it

A skill only runs when Claude decides it fits, so this repo measures that. `evals/triggers.json` holds 20 requests about a small landing page. Twelve should make Claude draw, and only one of those says "image". Eight are plain code work that should leave the skill alone.

```
python evals/run_triggers.py
```

It runs each request through `claude -p` and prints how many of the twelve loaded the skill and how many of the eight loaded it by mistake.

Results on Opus 5.5, Claude Code 2.1.280, 23 September 2026, one run per request:

| Version | Loaded (of 12) | Loaded by mistake (of 8) |
|---|---|---|
| First skill description | 1 | 0 |
| Current description | 6 | 0 |
| Current description and the reminder | 10 | 0 |

## License

MIT. The prompt template is adapted from the `imagegen` skill that ships with the Codex CLI (Apache-2.0).
