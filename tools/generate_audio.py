#!/usr/bin/env python3
"""Generate narration audio for The Price of Dawn using Piper."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import shutil
import tempfile
from pathlib import Path

DEFAULT_PIPER_ROOT = Path(
    os.environ.get(
        "PIPER_ROOT", "/home/chris/Documents/Projects/piper-sample-generator"
    )
)
DEFAULT_VOICE = os.environ.get("PIPER_VOICE", "voices/en_US-danny-low.onnx")
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent.parent / "audio"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render narrated audio snippets via piper-sample-generator"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="Inline text to narrate")
    group.add_argument(
        "--text-file",
        type=Path,
        help="Path to a UTF-8 text file whose contents will be narrated",
    )
    parser.add_argument(
        "--output-name",
        required=True,
        help="Filename (within the output directory) for the generated WAV",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory to write WAV files (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--piper-root",
        type=Path,
        default=DEFAULT_PIPER_ROOT,
        help="Path to the piper-sample-generator checkout",
    )
    parser.add_argument(
        "--voice",
        default=DEFAULT_VOICE,
        help="Model path relative to --piper-root or an absolute path",
    )
    parser.add_argument(
        "--length-scale",
        type=float,
        default=1.4,
        help="Length scale parameter passed to Piper (default: 1.4)",
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        default=1,
        help="Maximum number of samples Piper should emit (default: 1)",
    )
    return parser.parse_args()


def resolve_voice(voice_arg: str, piper_root: Path) -> Path:
    voice_path = Path(voice_arg)
    if not voice_path.is_absolute():
        voice_path = piper_root / voice_path
    return voice_path


def load_text(args: argparse.Namespace) -> str:
    if args.text_file:
        return args.text_file.read_text(encoding="utf-8").strip()
    return args.text.strip()


def main() -> int:
    args = parse_args()
    piper_root = args.piper_root.resolve()
    voice_path = resolve_voice(args.voice, piper_root)
    text = load_text(args)

    if not text:
        print("No text provided for narration", file=sys.stderr)
        return 1
    if not piper_root.exists():
        print(f"Piper root not found: {piper_root}", file=sys.stderr)
        return 1
    if not voice_path.exists():
        print(f"Voice model not found: {voice_path}", file=sys.stderr)
        return 1

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    target_path = output_dir / args.output_name

    venv_python = piper_root / ".venv" / "bin" / "python3"
    python_cmd = str(venv_python) if venv_python.exists() else "python3"

    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = [
            python_cmd,
            "-m",
            "piper_sample_generator",
            text,
            "--model",
            str(voice_path),
            "--max-samples",
            str(args.max_samples),
            "--length-scales",
            str(args.length_scale),
            "--output-dir",
            tmpdir,
        ]
        subprocess.run(cmd, check=True, cwd=piper_root)

        tmp_wav = Path(tmpdir) / "0.wav"
        if not tmp_wav.exists():
            print("Piper did not produce output (expected 0.wav)", file=sys.stderr)
            return 1
        shutil.move(tmp_wav, target_path)

    print(f"Wrote {target_path.relative_to(Path.cwd())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
