# Skills

Six Claude Code skills for making images, comparing designs, reporting work, checking plans and plain writing.

| Skill | What it does |
|---|---|
| image-gen | Draw image assets through the Codex CLI. |
| presentation | Turn finished work into a short page a reader can decide on. Charts come from data files, and two scripts check the pictures and the prose before it ships. |
| design-round | Build distinct visual options and review them side by side. |
| reach-check | Check whether a plan can reach its goal before running it. |
| ste-writing | Rewrite English prose into ASD-STE100 Simplified Technical English. By [Ege Çelebi](https://github.com/woosal1337/blog), MIT. |
| its-writing | The same pass for Italian prose. Adapted from Ege Çelebi's ste-writing, MIT. |

## Install

```sh
claude plugin marketplace add RazAndAlex/skills
claude plugin install presentation@razandalex-skills
```

Replace `presentation` with any skill name from the table. Each skill is a separate plugin. Start a new Claude Code session after installing.

For a local checkout:

```sh
claude plugin marketplace add /path/to/skills
claude plugin install presentation@razandalex-skills
```

## Requirements

Presentation's scripts need Python 3. Screenshot and layout checks also need Playwright and Chromium:

```sh
python3 -m pip install playwright
python3 -m playwright install chromium
```

Image generation needs the signed-in Codex CLI, Pillow and numpy. See [image-gen's README](plugins/image-gen/README.md).

## Optional helpers

[pstack](https://github.com/cursor/plugins/tree/main/pstack), from Cursor's plugins, provides `bro` and `unslop`. [Matt Pocock's skills](https://github.com/mattpocock/skills) provide engineering workflows if installed.

Presentation works without these helpers. It includes a plain-English writing pass and `scripts/slop.py` checks the prose either way.

## License

MIT. ste-writing is Ege Çelebi's work and its-writing is adapted from it; each folder carries his MIT license. The image-gen prompt template includes attribution to its Apache-2.0 source in [PROMPTS.md](plugins/image-gen/skills/image-gen/PROMPTS.md).
