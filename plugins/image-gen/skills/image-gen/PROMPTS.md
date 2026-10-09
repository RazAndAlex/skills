# Writing image prompts

Read this when you write a prompt for `draw.py`. The schema is adapted from the `imagegen` skill that ships with the Codex CLI (Apache-2.0).

## Schema

Use the lines that help and leave out the rest. Keep each line short and concrete.

```text
Use case: <slug from the list below>
Asset type: <where the asset goes, e.g. "transparent cutout for a landing page hero">
Input images: <Image 1: role; Image 2: role>
Subject: <the main subject, counted and described>
Style/medium: <photo, 3D render, flat illustration, ink, ...>
Composition/framing: <angle, crop, where the subject sits, empty space to leave>
Lighting/mood: <light direction and quality>
Color palette: <named colours, or "match Image 1">
Materials/textures: <surface detail>
Background: <"fully transparent" for cutouts, or the backdrop>
Text (verbatim): "<exact text>"
Constraints: <what must be true, e.g. "no text, only a faint contact shadow">
```

## Use cases

- `product-mockup`: objects and products, the usual choice for cutouts.
- `stylized-concept`: 3D or stylised renders, mascots, decorative objects.
- `illustration-story`: drawn scenes and spot illustrations.
- `photorealistic-natural`: photographic backgrounds and lifestyle scenes.
- `logo-brand`: marks and symbols. Draw the mark alone and set the name in code.
- `ui-mockup`: an interface picture used as an illustration.
- `precise-object-edit`: change one element of an existing image passed with `--ref`.
- `style-transfer`: a new subject in the style of an image passed with `--ref`.

## Rules that change the result

- **Transparent cutouts:** write `Background: fully transparent` and call `draw.py --transparent`. Ask for "only a faint contact shadow" when the object has to sit on a surface in the layout.
- **Matching sets:** every prompt after the anchor starts its `Input images` line with "Image 1 is the style reference for lighting, render quality and colour temperature", and its `Style/medium` line with "match Image 1".
- **Layers:** describe a layer by what sits under it ("sits above the mug in Image 1; match its light direction") so light and scale agree.
- **Text:** spell exact text in `Text (verbatim)` and keep it to a few words. Everything else in the prompt says "no text".
- **Edits:** name the one change and list what stays: "change only the rim colour to copper; keep shape, lighting and background unchanged".
- **Redraws:** change one line per redraw, so you can tell which line fixed or broke the result.

## Worked example: an anchor and two layers

Anchor, drawn first:

```text
Use case: product-mockup
Asset type: transparent cutout for a landing page hero, layered over a dark background
Subject: a matte charcoal ceramic coffee mug with a thin brass rim, three-quarter view from slightly above, filled with black coffee showing a faint crema ring
Style/medium: soft studio product render
Lighting/mood: gentle rim light from upper left, warm and calm
Composition/framing: mug centred, small margin on every side
Background: fully transparent, with only a faint contact shadow under the base kept in the alpha
Constraints: no text, no logo, no saucer, no steam, no props
```

The steam comes as its own layer so the page can animate it.

A layer drawn against it with `--ref mug.png`:

```text
Use case: product-mockup
Asset type: transparent overlay layer that sits above the mug in Image 1
Input images: Image 1 shows the mug this steam rises from; match its light direction
Subject: three thin, soft wisps of rising steam
Composition/framing: tall and narrow, wisps start at the bottom centre and drift up and slightly right
Style/medium: soft white vapour, semi-transparent, fading to fully transparent at the top
Background: fully transparent
Constraints: steam only, nothing else in the image
```
