---
name: image-gen
description: Use for any visual asset a page, app or brand needs, such as a logo, icon set, mascot, illustration, hero or product image, background, texture, social share card or empty-state art. Draws it as a real image through a Codex worker running OpenAI's image model, with transparent cutouts that layer into the layout. Reach for it before hand-coding SVG or CSS art, and whenever a design would look richer with real imagery.
---

# Image gen

You are the designer and a Codex worker is the brush. You plan the assets, write every prompt, judge every result and write all the frontend code. The brush receives one prompt, draws one image with its built-in image tool, and stops. `scripts/draw.py` runs the brush and collects the file for you.

Requirements: the Codex CLI signed in with a ChatGPT plan, and Python 3 with Pillow. When `codex` is missing, tell the user that drawing needs the Codex CLI and give them the prompts you wrote.

## Steps

Paths below are relative to this skill's base directory.

1. **Plan the kit.** List every asset the work needs, and give each one a file name, a role (cutout, background, texture, logo, icon, illustration) and its size on screen. Done when every asset has a name, a role and a size.
2. **Write the anchor prompt.** The anchor is the first asset drawn, and every later asset copies its style. Pick the asset that carries most of the look, usually the main subject. Write its prompt in the schema from [PROMPTS.md](PROMPTS.md). Done when the prompt fills use case, asset type, subject, style, lighting, background and constraints.
3. **Draw the anchor.**
   ```
   python scripts/draw.py --prompt-file anchor.txt --out <project>/assets/raw/anchor.png --transparent
   ```
   Done when the script prints a JSON line with `"ok": true`.
4. **Look at it.** Open the PNG and check the subject, the style, the edges, and that any text in it is text you asked for. When it misses, change one thing in the prompt and draw again. Done when you would ship it.
5. **Draw the set.** Every other prompt names the anchor as "Image 1" and its style reference, and passes `--ref <anchor.png>`. Run one draw per asset, all in parallel as background processes. Done when every asset from step 1 has a PNG you have looked at.
6. **Clean up.**
   ```
   python scripts/cleanup.py <project>/assets/raw/*.png --outdir <project>/assets
   ```
   It trims empty borders, removes the coloured fringe on transparent edges and writes webp. Done when every asset has a webp.
7. **Place.** Use the webp files in the code and view the page rendered at its real size. Done when every asset reads correctly in place.

## Working notes

- One draw takes about a minute and 30k to 65k Codex tokens. Parallel draws finish together.
- Keep words out of images. Set wordmarks, labels and headlines in code with a real font and draw only the mark or the picture.
- To edit an existing image, pass it with `--ref` and write the prompt as "change only X, keep everything else unchanged".
- Keep the raw PNGs beside the webp files so any asset can be redrawn or re-cleaned later. A redraw never replaces an existing file: it lands as `mug-2.png`, and the JSON line's `out` gives the real path.
- `draw.py --help` lists the model and timeout options. The default model is `gpt-6-luna`, and `IMAGE_GEN_MODEL` overrides it.
