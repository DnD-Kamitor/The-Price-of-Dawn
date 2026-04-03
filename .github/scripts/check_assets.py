#!/usr/bin/env python3
"""CI helper that enforces the campaign's asset format rules."""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Dict, Iterable

DIRECTORY_RULES: Dict[str, set[str]] = {
    "images": {".png"},
    "docs/images": {".png"},
    "audio": {".wav", ".txt"},
}

ALLOWED_SIDEFILES = {Path("images/GENERATE-THESE.md")}

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
RIFF_HEADER = b"RIFF"
WAVE_HEADER = b"WAVE"


def iter_files(directory: Path) -> Iterable[Path]:
    for path in directory.rglob("*"):
        if path.is_file():
            yield path.resolve()


def ensure_directory_formats() -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    summary: dict[str, int] = {key: 0 for key in DIRECTORY_RULES}
    for directory, allowed_exts in DIRECTORY_RULES.items():
        base = Path(directory)
        if not base.exists():
            continue
        for path in iter_files(base):
            rel_path = path.relative_to(Path.cwd())
            if rel_path in ALLOWED_SIDEFILES:
                continue
            ext = path.suffix.lower()
            if ext not in allowed_exts:
                errors.append(
                    f"{rel_path} is {ext or 'extensionless'} but only {sorted(allowed_exts)} are allowed"
                )
                continue
            if ext == ".png" and not is_png(path):
                errors.append(f"{rel_path} is not a valid PNG (bad signature)")
            elif ext == ".wav" and not is_wav(path):
                errors.append(
                    f"{rel_path} is not a valid WAV (missing RIFF/WAVE header)"
                )
            summary[directory] += 1
    return errors, summary


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
    errors, summary = ensure_directory_formats()

    if errors:
        print("Asset validation failed:")
        for issue in errors:
            print(f" - {issue}")
        return 1

    print(
        "Asset validation passed ("
        f"images: {summary.get('images', 0)}, "
        f"docs/images: {summary.get('docs/images', 0)}, "
        f"audio: {summary.get('audio', 0)} files)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
