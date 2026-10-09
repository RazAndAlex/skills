#!/usr/bin/env python3
"""Trim transparent margins, remove cutout fringes, and encode WebP."""
from __future__ import annotations

import argparse
import glob
import json
from pathlib import Path

import numpy as np
from PIL import Image


def dilate_rgb(rgb: np.ndarray, core: np.ndarray, steps: int) -> tuple[np.ndarray, np.ndarray]:
    """Propagate core colour outward by `steps` pixels; return colours and the reached mask."""
    h, w = core.shape
    known = core.copy()
    colours = rgb.copy()
    # Frontier expansion avoids overwriting original core samples.
    for _ in range(steps):
        prev = known.copy()
        accum = np.zeros((h, w, 3), dtype=np.uint32)
        count = np.zeros((h, w), dtype=np.uint8)
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)):
            sy0, sy1 = max(0, -dy), min(h, h - dy)
            sx0, sx1 = max(0, -dx), min(w, w - dx)
            dy0, dy1 = max(0, dy), min(h, h + dy)
            dx0, dx1 = max(0, dx), min(w, w + dx)
            src = prev[sy0:sy1, sx0:sx1]
            accum[dy0:dy1, dx0:dx1] += colours[sy0:sy1, sx0:sx1] * src[..., None]
            count[dy0:dy1, dx0:dx1] += src
        newly = (~known) & (count > 0)
        if not newly.any():
            break
        colours[newly] = (accum[newly] / count[newly, None]).astype(np.uint8)
        known[newly] = True
    return colours, known & ~core


def expand_inputs(values: list[str]) -> list[Path]:
    result = []
    seen = set()
    for value in values:
        hits = glob.glob(value, recursive=True)
        for hit in (hits if hits else [value]):
            p = Path(hit).expanduser()
            if p.is_file() and p.resolve() not in seen:
                seen.add(p.resolve())
                result.append(p)
    return result


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("inputs", nargs="+")
    p.add_argument("--outdir", required=True, type=Path)
    p.add_argument("--max", type=int, default=2048, dest="max_side")
    p.add_argument("--quality", type=int, default=90)
    p.add_argument("--pad", type=int, default=2)
    p.add_argument("--no-trim", action="store_true")
    p.add_argument("--core", type=int, default=240, help="alpha at or above this counts as solid body")
    p.add_argument("--band", type=int, default=2, help="edge width in pixels whose colour is corrected")
    args = p.parse_args()
    paths = expand_inputs(args.inputs)
    if not paths:
        p.error("no input files matched")
    args.outdir.mkdir(parents=True, exist_ok=True)
    for src in paths:
        with Image.open(src) as original:
            before = list(original.size)
            image = original.copy()
        if image.mode == "RGBA":
            arr = np.asarray(image).copy()
            alpha = arr[..., 3]
            if not args.no_trim:
                ys, xs = np.nonzero(alpha > 8)
                if len(xs):
                    left = max(0, int(xs.min()) - args.pad)
                    top = max(0, int(ys.min()) - args.pad)
                    right = min(image.width, int(xs.max()) + 1 + args.pad)
                    bottom = min(image.height, int(ys.max()) + 1 + args.pad)
                    arr = arr[top:bottom, left:right]
                    alpha = arr[..., 3]
            # Generated cutouts keep their solid body at alpha 250-254, rarely 255.
            core = alpha >= args.core
            if core.any():
                colours, band = dilate_rgb(arr[..., :3], core, args.band)
                # Only the thin edge band is recoloured; soft shadows and vapour keep their colour.
                band &= alpha > 0
                arr[..., :3][band] = colours[band]
            image = Image.fromarray(arr, "RGBA")
        out = (args.outdir / f"{src.stem}.webp").resolve()
        if args.max_side > 0 and max(image.size) > args.max_side:
            scale = args.max_side / max(image.size)
            size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
            image = image.resize(size, Image.Resampling.LANCZOS)
        image.save(out, "WEBP", quality=args.quality, alpha_quality=100, method=6)
        print(json.dumps({"in": str(src.resolve()), "out": str(out), "size_before": before,
                          "size_after": list(image.size), "bytes": out.stat().st_size}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
