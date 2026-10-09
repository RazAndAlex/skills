#!/usr/bin/env python3
"""Run one Codex image-generation turn and collect its PNG output."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from PIL import Image


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    prompt = p.add_mutually_exclusive_group(required=True)
    prompt.add_argument("--prompt-file", type=Path)
    prompt.add_argument("--prompt")
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--ref", action="append", default=[], type=Path)
    p.add_argument("--transparent", action="store_true")
    p.add_argument("--model", default=os.environ.get("IMAGE_GEN_MODEL", "gpt-6-luna"))
    p.add_argument("--effort", default="low")
    p.add_argument("--timeout", type=float, default=300)
    return p


def main() -> int:
    args = parser().parse_args()
    start = time.monotonic()
    thread_id = None
    try:
        codex = shutil.which("codex")
        if not codex:
            raise RuntimeError("codex CLI not found on PATH")
        prompt = args.prompt_file.read_text(encoding="utf-8") if args.prompt_file else args.prompt
        refs = [Path(r).expanduser().resolve(strict=True) for r in args.ref]
        instruction = "You are an image generation worker. Do exactly this and nothing else.\n"
        for i, ref in enumerate(refs, 1):
            instruction += f"Call view_image on {ref} so it is Image {i}.\n"
        instruction += "Call the built-in image_gen tool exactly once. Pass the prompt between the markers verbatim: do not rewrite, expand or shorten it."
        if args.transparent:
            instruction += " Ask for a transparent background and keep the alpha."
        instruction += "\nReply with the single word DONE. Do not search for, copy or move the image: the caller collects it.\n<<<PROMPT\n" + prompt + "\nPROMPT>>>"

        with tempfile.TemporaryDirectory(prefix="codex-image-") as temp:
            cmd = [codex, "exec", "--json", "--skip-git-repo-check", "-s", "read-only", "-m", args.model,
                   "-c", f'model_reasoning_effort="{args.effort}"', "-C", temp]
            for ref in refs:
                folder = str(ref.parent)
                if folder not in [x for i, x in enumerate(cmd) if i > 0]:
                    cmd.extend(["--add-dir", folder])
            cmd.append("-")
            try:
                proc = subprocess.run(cmd, input=instruction, text=True, capture_output=True,
                                      timeout=args.timeout, encoding="utf-8", errors="replace")
            except subprocess.TimeoutExpired as e:
                raise RuntimeError(f"codex timed out after {args.timeout:g} seconds") from e
            tokens = None
            events = []
            for line in proc.stdout.splitlines():
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                events.append(event)
                typ = event.get("type")
                if typ in ("thread.started", "thread-started"):
                    thread_id = event.get("thread_id") or event.get("thread", {}).get("id")
                elif typ in ("turn.completed", "turn-completed"):
                    usage = event.get("usage") or event.get("token_usage") or {}
                    tokens = usage.get("total_tokens")
                    if tokens is None:
                        tokens = (usage.get("input_tokens", 0) or 0) + (usage.get("output_tokens", 0) or 0)
            if proc.returncode:
                detail = proc.stderr.strip() or f"codex exited with status {proc.returncode}"
                raise RuntimeError(detail[-1500:])
            if not thread_id:
                raise RuntimeError("Codex JSONL did not include a thread-started event")
            home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()
            generated = home / "generated_images" / str(thread_id)
            pngs = list(generated.glob("*.png")) if generated.is_dir() else []
            if not pngs:
                raise RuntimeError(f"no PNG found for thread {thread_id} in {generated}")
            source = max(pngs, key=lambda p: p.stat().st_mtime_ns)
            out = args.out.expanduser().resolve()
            out.parent.mkdir(parents=True, exist_ok=True)
            # A redraw keeps the earlier take: mug.png becomes mug-2.png, mug-3.png, ...
            n = 2
            while out.exists():
                out = out.with_name(f"{args.out.stem}-{n}{out.suffix}")
                n += 1
            shutil.copy2(source, out)
            with Image.open(out) as im:
                rgba = im.mode == "RGBA"
                alpha_min = im.getchannel("A").getextrema()[0] if rgba else None
                result = {"ok": True, "out": str(out), "width": im.width, "height": im.height,
                          "alpha": bool(rgba and alpha_min == 0), "seconds": round(time.monotonic() - start, 3),
                          "tokens": tokens, "model": args.model, "thread_id": thread_id}
            if args.transparent and not result["alpha"]:
                result["warning"] = "requested transparency but output alpha minimum is not 0"
            print(json.dumps(result, ensure_ascii=False))
            return 0
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e), "thread_id": thread_id}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.exit(main())
