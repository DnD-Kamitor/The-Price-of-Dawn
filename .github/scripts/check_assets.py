#!/usr/bin/env python3
"""CI helper that enforces the campaign's asset format rules."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys
from typing import Iterable, List

DIRECTORY_RULES = {
    "images": {".png"},
    "docs/images": {".png"},
    "audio": {".wav"},
}

ALLOWED_SIDEFILES = {Path("images/GENERATE-THESE.md")}

FORBIDDEN_GLOBS = ["*.svg", "*.gif", "*.jpg", "*.jpeg", "*.webp", "*.bmp"]

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
RIFF_HEADER = b"RIFF"
WAVE_HEADER = b"WAVE"


def run_git_ls_files(args: Iterable[str]) -> List[Path]:
    cmd = ["git", "ls-files", "-z", "--", *args]
    result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE)
    output = result.stdout.decode("utf-8", "ignore").split("\0")
    return [Path(entry) for entry in output if entry]


def ensure_directory_formats() -> list[str]:
    errors: list[str] = []
    for directory, allowed_exts in DIRECTORY_RULES.items():
        files = run_git_ls_files([directory])
        for path in files:
            if path in ALLOWED_SIDEFILES:
                continue
            ext = path.suffix.lower()
            if ext not in allowed_exts:
                errors.append(
                    f"{path} is {ext or 'extensionless'} but only {sorted(allowed_exts)} are allowed"
                )
            elif ext == ".png" and not is_png(path):
                errors.append(f"{path} is not a valid PNG (bad signature)")
            elif ext == ".wav" and not is_wav(path):
                errors.append(f"{path} is not a valid WAV (missing RIFF/WAVE header)")
    return errors


def ensure_no_forbidden_globs() -> list[str]:
    errors: list[str] = []
    files = run_git_ls_files(FORBIDDEN_GLOBS)
    for path in files:
        errors.append(f"{path} uses a forbidden format")
    return errors


def is_png(path: Path) -> bool:
    try:
        with path.open("rb") as handle:
            return handle.read(len(PNG_SIGNATURE)) == PNG_SIGNATURE
    except FileNotFoundError:
        return False


def is_wav(path: Path) -> bool:
    try:
        with path.open("rb") as handle:
            header = handle.read(12)
            return header.startswith(RIFF_HEADER) and header[8:12] == WAVE_HEADER
    except FileNotFoundError:
        return False


def main() -> int:
    errors = ensure_directory_formats()
    errors.extend(ensure_no_forbidden_globs())

    if errors:
        print("Asset validation failed:")
        for issue in errors:
            print(f" - {issue}")
        return 1

    png_total = len(run_git_ls_files(["*.png"]))
    wav_total = len(run_git_ls_files(["audio"]))
    print(
        f"Asset validation passed ({png_total} PNGs, {wav_total} tracked audio files)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
