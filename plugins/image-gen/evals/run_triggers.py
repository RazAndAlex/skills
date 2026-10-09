#!/usr/bin/env python3
"""Measure whether Claude Code invokes the image-gen skill for prompt evals."""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import json
import os
import queue
import shutil
import subprocess
import tempfile
import threading
import time
from pathlib import Path
from typing import Any


EVALS_DIR = Path(__file__).resolve().parent
REPO_ROOT = EVALS_DIR.parent
FIXTURE = EVALS_DIR / "fixture"
_PRINT_LOCK = threading.Lock()


def _tool_uses(event: dict[str, Any]):
    """Yield (name, input) pairs from Claude stream-json message events."""
    message = event.get("message", event)
    if not isinstance(message, dict):
        return
    content = message.get("content", [])
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                yield block.get("name"), block.get("input", {})


def _kill_tree(proc: subprocess.Popen[str]) -> None:
    if proc.poll() is not None:
        return
    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/PID", str(proc.pid), "/T", "/F"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    else:
        proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()


def run_one(item: dict[str, Any], rep: int, args: argparse.Namespace, claude: str) -> dict[str, Any]:
    started = time.monotonic()
    row: dict[str, Any] = {
        "id": item["id"],
        "rep": rep,
        "should_trigger": item["should_trigger"],
        "triggered": False,
        "seconds": 0.0,
        "first_tool": None,
        "error": None,
    }
    with tempfile.TemporaryDirectory(prefix="claude-trigger-", ignore_cleanup_errors=True) as temp:
        shutil.copytree(FIXTURE, Path(temp), dirs_exist_ok=True)
        command = [
            claude, "-p", item["prompt"], "--plugin-dir", str(args.plugin),
            "--model", args.model, "--output-format", "stream-json", "--verbose",
        ]
        try:
            with tempfile.TemporaryFile(mode="w+t", encoding="utf-8") as stderr_file:
                proc = subprocess.Popen(
                    command,
                    cwd=temp,
                    stdout=subprocess.PIPE,
                    stderr=stderr_file,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    bufsize=1,
                )
                lines: queue.Queue[str | None] = queue.Queue()
                def read_stdout() -> None:
                    assert proc.stdout is not None
                    for output_line in proc.stdout:
                        lines.put(output_line)
                    lines.put(None)

                reader = threading.Thread(target=read_stdout, daemon=True)
                reader.start()
                deadline = started + args.timeout
                try:
                    while True:
                        remaining = deadline - time.monotonic()
                        if remaining <= 0:
                            row["error"] = f"timeout after {args.timeout:g}s"
                            _kill_tree(proc)
                            break
                        try:
                            line = lines.get(timeout=min(remaining, 0.5))
                        except queue.Empty:
                            if proc.poll() is not None:
                                break
                            continue
                        if line is None:
                            proc.wait()
                            if proc.returncode:
                                stderr_file.seek(0)
                                error_text = stderr_file.read().strip()
                                row["error"] = error_text or f"claude exited {proc.returncode}"
                            break
                        try:
                            event = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        if event.get("type") == "result" and isinstance(event.get("result"), str):
                            row["result"] = event["result"][:400]
                        for name, tool_input in _tool_uses(event):
                            if row["first_tool"] is None:
                                row["first_tool"] = name
                            if name == "Skill" and isinstance(tool_input, dict):
                                skill = tool_input.get("skill", "")
                                if isinstance(skill, str) and skill.endswith("image-gen"):
                                    row["triggered"] = True
                                    _kill_tree(proc)
                                    break
                        if row["triggered"]:
                            break
                finally:
                    if proc.poll() is None:
                        _kill_tree(proc)
        except FileNotFoundError:
            row["error"] = f"claude executable not found: {claude}"
        except Exception as exc:  # Preserve an eval result even for subprocess/parser errors.
            row["error"] = f"{type(exc).__name__}: {exc}"
    row["seconds"] = round(time.monotonic() - started, 3)
    return row


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", type=Path, default=EVALS_DIR / "triggers.json")
    parser.add_argument("--only", help="comma-separated eval ids")
    parser.add_argument("--reps", type=int, default=1)
    parser.add_argument("--concurrency", type=int, default=4)
    parser.add_argument("--model", default="opus")
    parser.add_argument("--plugin", type=Path, default=REPO_ROOT, help="plugin folder to load (default: this repo)")
    parser.add_argument("--timeout", type=float, default=240)
    args = parser.parse_args()
    if args.reps < 1 or args.concurrency < 1 or args.timeout <= 0:
        parser.error("--reps and --concurrency must be positive; --timeout must be positive")
    try:
        items = json.loads(args.file.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        parser.error(f"cannot read eval file {args.file}: {exc}")
    if not isinstance(items, list):
        parser.error("input must be a JSON list")
    for index, item in enumerate(items):
        if (not isinstance(item, dict) or not isinstance(item.get("id"), str)
                or not isinstance(item.get("prompt"), str)
                or not isinstance(item.get("should_trigger"), bool)):
            parser.error(f"item {index} must have string id/prompt and boolean should_trigger")
    if args.only:
        wanted = {part.strip() for part in args.only.split(",") if part.strip()}
        items = [item for item in items if item["id"] in wanted]
        missing = wanted - {item["id"] for item in items}
        if missing:
            parser.error(f"unknown id(s): {', '.join(sorted(missing))}")
    claude = shutil.which("claude")
    if not claude:
        parser.error("claude executable not found on PATH")

    tasks = [(item, rep) for item in items for rep in range(1, args.reps + 1)]
    results: list[dict[str, Any]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        futures = [pool.submit(run_one, item, rep, args, claude) for item, rep in tasks]
        for future in concurrent.futures.as_completed(futures):
            row = future.result()
            results.append(row)
            with _PRINT_LOCK:
                print(json.dumps(row, ensure_ascii=False), flush=True)

    now = dt.datetime.now()
    result_dir = EVALS_DIR / "results"
    result_dir.mkdir(parents=True, exist_ok=True)
    output = result_dir / f"{now:%Y-%m-%d_%H%M}.jsonl"
    # Preserve same-minute results rather than overwrite them.
    suffix = 1
    while output.exists():
        output = result_dir / f"{now:%Y-%m-%d_%H%M}_{suffix}.jsonl"
        suffix += 1
    with output.open("w", encoding="utf-8") as handle:
        for row in results:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    positives = [r for r in results if r["should_trigger"]]
    negatives = [r for r in results if not r["should_trigger"]]
    misses = [r for r in positives if not r["triggered"]]
    false_positives = [r for r in negatives if r["triggered"]]
    version = subprocess.run([claude, "--version"], capture_output=True, text=True, check=False)
    print(f"claude --version: {(version.stdout or version.stderr).strip()}")
    print(f"model: {args.model}")
    print(f"plugin: {args.plugin}")
    print(f"date: {now:%Y-%m-%d %H:%M:%S}")
    print(f"results: {output}")
    print(f"recall: {sum(r['triggered'] for r in positives)}/{len(positives)}")
    print(f"false positives: {len(false_positives)}")
    print("misses: " + (", ".join(f"{r['id']} rep {r['rep']}" for r in misses) or "none"))
    print("false positive ids: " + (", ".join(f"{r['id']} rep {r['rep']}" for r in false_positives) or "none"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
