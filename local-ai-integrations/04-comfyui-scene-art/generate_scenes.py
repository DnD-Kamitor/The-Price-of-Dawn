#!/usr/bin/env python3
"""
ComfyUI Scene Art Generator — The Price of Dawn
Batch-generates scene images and NPC portraits via ComfyUI API.

Usage:
    python3 generate_scenes.py --session 1
    python3 generate_scenes.py --npc all
    python3 generate_scenes.py --scene "archive-exterior" --output archive-exterior.png
    python3 generate_scenes.py --list

Config via env vars:
    COMFYUI_URL     — default: https://comfyui.research-ready.nl
    MTLS_CERT       — mTLS client cert path (default: /tmp/mtls_client.crt)
    MTLS_KEY        — mTLS client key path (default: /tmp/mtls_client.key)
    COMFYUI_MODEL   — SDXL model filename (default: dreamshaperXL_v21TurboDPMSDE.safetensors)
"""

import os
import sys
import json
import time
import argparse
import subprocess
from pathlib import Path
from typing import Optional

try:
    import httpx
except ImportError:
    print("pip install httpx", file=sys.stderr)
    sys.exit(1)

COMFYUI_URL = os.environ.get("COMFYUI_URL", "https://comfyui.research-ready.nl")
MTLS_CERT = os.environ.get("MTLS_CERT", "/tmp/mtls_client.crt")
MTLS_KEY = os.environ.get("MTLS_KEY", "/tmp/mtls_client.key")
COMFYUI_MODEL = os.environ.get("COMFYUI_MODEL", "dreamshaperXL_v21TurboDPMSDE.safetensors")

STYLE_SUFFIX = (
    "dark fantasy illustration, twilight atmosphere, perpetual dusk, amber light from lanterns, "
    "muted colors with amber and ochre accents, historical architecture Northern European, "
    "painterly style, detailed, cinematic composition, no sun visible in sky, "
    "atmospheric depth, fog and shadow, candles and lamplight as primary light sources"
)

NEGATIVE_PROMPT = (
    "bright daylight, sunshine, blue sky, modern elements, anime style, cartoon, "
    "oversaturated colors, photorealistic photography, watermark, signature, text, blurry, "
    "low quality, futuristic elements, dragons, elves, magic sparkles, glowing eyes, neon, flat lighting"
)

PORTRAIT_SUFFIX = (
    "portrait, upper body, facing viewer, character study, detailed face, "
    "dark fantasy illustration, twilight atmosphere, amber candlelight from below and side, "
    "muted colors with amber and ochre accents, painterly style, cinematic composition, "
    "historical Northern European setting, atmospheric depth"
)

# ---------------------------------------------------------------------------
# Scene definitions
# ---------------------------------------------------------------------------

SCENES = {
    # Session 1 — The Archive
    "session1-archive-exterior": {
        "prompt": "Varenhold civic archive building, stone facade, tall arched windows with amber candlelight within, evening twilight sky with no sun, cobblestone plaza, few people passing, lanterns on iron posts",
        "output": "session1-archive-exterior.png",
        "landscape": True,
    },
    "session1-archive-stacks": {
        "prompt": "Interior of ancient library archive, tall wooden shelving units disappearing into darkness above, single archivist figure with a lamp walking between shelves, dust motes in amber light, rows of numbered boxes and leather-bound registers, stone floor, cold atmosphere",
        "output": "session1-archive-stacks.png",
        "landscape": True,
    },
    "session1-sealed-documents": {
        "prompt": "Close view of old wooden archive shelf, a small locked metal box among paper files, dust disturbed, candlelight casting long shadows, fingers reaching toward the box, sense of long concealment, discovery moment",
        "output": "session1-sealed-documents.png",
        "landscape": True,
    },
    # Session 2 — Lowmark
    "session2-dawnhall-exterior": {
        "prompt": "Large communal hall exterior, stone building with a carved sunrise relief above the door (faded), people gathering outside carrying food and supplies, amber lamplight at windows, working-class district street, fog at ground level",
        "output": "session2-dawnhall-exterior.png",
        "landscape": True,
    },
    "session2-cipher-room": {
        "prompt": "Hidden basement room, stone walls with carved runes and symbols, a ritual circle inlaid in floor, candle stubs everywhere long burned out, dust, silence, discovered after long hiding, single lantern brought by investigators illuminating the carvings",
        "output": "session2-cipher-room.png",
        "landscape": True,
    },
    "session2-sera-patrol": {
        "prompt": "Guard captain figure in patrol coat standing at district gate at night, amber street lanterns, working-class street beyond, figure is watchful but relaxed, weight of long duty on shoulders",
        "output": "session2-sera-patrol.png",
        "landscape": True,
    },
    # Session 3 — Ashfen
    "session3-ashfen-approach": {
        "prompt": "Travellers on a raised causeway through marshland, water on both sides, reed beds, grey-green fog, no sun, diffuse ambient twilight light, distant wayshrine visible, isolation and silence",
        "output": "session3-ashfen-approach.png",
        "landscape": True,
    },
    "session3-clan-camp": {
        "prompt": "Ashfen marsh encampment, low tents and reed shelters, firelight at center, clan members working, surrounded by marsh, a Wadewalker elder figure standing at edge looking outward, practical, sustainable, long-inhabited",
        "output": "session3-clan-camp.png",
        "landscape": True,
    },
    "session3-stone-circle": {
        "prompt": "Ancient stone circle in moorland, large standing stones with amber lichen, twilight sky, ritual marks visible on stone surfaces, empty circle, sense of waiting",
        "output": "session3-stone-circle.png",
        "landscape": True,
    },
    # Session 4 — Decisions
    "session4-lira-healing-room": {
        "prompt": "Small healing practice room, shelves of medicinal supplies, examination table, candle lamp, healer figure near window looking out at the city, a child's small shoe visible on a shelf, medical competence and personal weight",
        "output": "session4-lira-healing-room.png",
        "landscape": True,
    },
    "session4-restorers-meeting": {
        "prompt": "Candlelit meeting room, circle of seated figures in plain clothes, one standing figure addressing them, former priest bearing, maps and documents on a table, serious purpose, not threatening, underground gathering but lawful in intent",
        "output": "session4-restorers-meeting.png",
        "landscape": True,
    },
    # Session 5 — Ritual
    "session5-ritual-site": {
        "prompt": "Stone circle at night prepared for ritual, candles placed at each stone, ten standing figures in positions around the circle, Ashfen clan surrounding as witnesses, no audience beyond that, weight of ceremony, amber candlelight",
        "output": "session5-ritual-site.png",
        "landscape": True,
    },
    "session5-first-sunrise": {
        "prompt": "Single shaft of warm gold light breaking through clouds for first time in fifty years, figures shielding eyes, stone circle illuminated, fog burning off, first sunrise in a generation, overwhelming warmth and light contrast against the long darkness",
        "output": "session5-first-sunrise.png",
        "landscape": True,
    },
}

NPC_PORTRAITS = {
    "theron-waide": {
        "prompt": "elderly scholar, 70s, thin anxious expression, archival dust on dark clothing, wire-rimmed glasses, oil lamp in hand, library background",
        "output": "npc-portrait-theron-waide.png",
    },
    "sera-voss": {
        "prompt": "50s woman, guard captain, direct steady gaze, practical patrol uniform, weathered but not harsh, short grey-brown hair, district street background",
        "output": "npc-portrait-sera-voss.png",
    },
    "lira-anwick": {
        "prompt": "50s woman healer, capable hands visible, guarded expression warming slightly, medical apron, tired but fully present, healing room background",
        "output": "npc-portrait-lira-anwick.png",
    },
    "brother-edoran": {
        "prompt": "68 year old man, former priest bearing, calm accepting eyes, simple robes, slightly southern features, hands folded, candlelit meeting room background",
        "output": "npc-portrait-brother-edoran.png",
    },
    "chancellor-ostenveld": {
        "prompt": "57 year old man, formal administrator, controlled expression hiding exhaustion, quality clothing without ostentation, northern European features, civic office background",
        "output": "npc-portrait-chancellor-ostenveld.png",
    },
    "erem-wadewalker": {
        "prompt": "Ashfen elder, precise patient expression, marsh practical clothing, long grey braided hair, weathered face, marsh reeds visible background",
        "output": "npc-portrait-erem-wadewalker.png",
    },
    "tomas-areth": {
        "prompt": "middle-aged researcher, methodical measured expression, academic clothing, honest eyes, bookshelves in background, slight nervousness held in check",
        "output": "npc-portrait-tomas-areth.png",
    },
    "ysel-dorn": {
        "prompt": "woman temple keeper, warm certain expression, unafraid bearing, temple robes with Auris sun symbol (stylized, no light), stone temple background",
        "output": "npc-portrait-ysel-dorn.png",
    },
}

# ---------------------------------------------------------------------------
# mTLS
# ---------------------------------------------------------------------------

def ensure_mtls_cert():
    if os.path.exists(MTLS_CERT) and os.path.exists(MTLS_KEY):
        return True
    p12 = Path.home() / "Desktop" / "fedora.p12"
    if not p12.exists():
        return False
    pwd = "Research-mTLS-2024!"
    subprocess.run(["openssl", "pkcs12", "-in", str(p12), "-clcerts", "-nokeys",
                    "-out", MTLS_CERT, "-passin", f"pass:{pwd}"], capture_output=True)
    subprocess.run(["openssl", "pkcs12", "-in", str(p12), "-nocerts", "-nodes",
                    "-out", MTLS_KEY, "-passin", f"pass:{pwd}"], capture_output=True)
    return os.path.exists(MTLS_CERT)

def get_client() -> httpx.Client:
    ensure_mtls_cert()
    if os.path.exists(MTLS_CERT) and os.path.exists(MTLS_KEY):
        return httpx.Client(cert=(MTLS_CERT, MTLS_KEY), verify=False, timeout=120.0)
    return httpx.Client(verify=False, timeout=120.0)

# ---------------------------------------------------------------------------
# ComfyUI API
# ---------------------------------------------------------------------------

def build_workflow(prompt_text: str, negative: str, landscape: bool, seed: int = -1,
                   portrait_mode: bool = False) -> dict:
    """Build ComfyUI workflow dict from prompt text."""
    if seed == -1:
        import random
        seed = random.randint(0, 2**31)

    w, h = (1024, 768) if landscape else (768, 1024)
    if portrait_mode:
        w, h = 768, 1024

    full_prompt = prompt_text + ",\n" + (PORTRAIT_SUFFIX if portrait_mode else STYLE_SUFFIX)

    return {
        "1": {"inputs": {"ckpt_name": COMFYUI_MODEL},
              "class_type": "CheckpointLoaderSimple"},
        "2": {"inputs": {"text": full_prompt, "clip": ["1", 1]},
              "class_type": "CLIPTextEncode"},
        "3": {"inputs": {"text": negative, "clip": ["1", 1]},
              "class_type": "CLIPTextEncode"},
        "4": {"inputs": {"width": w, "height": h, "batch_size": 1},
              "class_type": "EmptyLatentImage"},
        "5": {"inputs": {
                "seed": seed, "steps": 35, "cfg": 7.5,
                "sampler_name": "dpmpp_2m", "scheduler": "karras",
                "denoise": 1.0, "model": ["1", 0],
                "positive": ["2", 0], "negative": ["3", 0],
                "latent_image": ["4", 0]},
              "class_type": "KSampler"},
        "6": {"inputs": {"samples": ["5", 0], "vae": ["1", 2]},
              "class_type": "VAEDecode"},
        "7": {"inputs": {"filename_prefix": "pod", "images": ["6", 0]},
              "class_type": "SaveImage"},
    }


def queue_prompt(client: httpx.Client, workflow: dict) -> Optional[str]:
    """Submit workflow to ComfyUI queue. Returns prompt_id."""
    try:
        resp = client.post(
            f"{COMFYUI_URL}/prompt",
            json={"prompt": workflow},
        )
        if resp.status_code == 200:
            data = resp.json()
            return data.get("prompt_id")
        print(f"  Queue failed: {resp.status_code} {resp.text[:200]}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  Queue error: {e}", file=sys.stderr)
        return None


def wait_for_completion(client: httpx.Client, prompt_id: str, timeout: int = 300) -> Optional[dict]:
    """Poll until prompt completes. Returns history entry or None."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            resp = client.get(f"{COMFYUI_URL}/history/{prompt_id}")
            if resp.status_code == 200:
                history = resp.json()
                if prompt_id in history:
                    return history[prompt_id]
        except Exception:
            pass
        time.sleep(3)
    return None


def download_output(client: httpx.Client, history_entry: dict, output_path: Path) -> bool:
    """Download generated image from ComfyUI."""
    try:
        outputs = history_entry.get("outputs", {})
        for node_id, node_out in outputs.items():
            images = node_out.get("images", [])
            if images:
                img = images[0]
                filename = img["filename"]
                subfolder = img.get("subfolder", "")
                resp = client.get(
                    f"{COMFYUI_URL}/view",
                    params={"filename": filename, "subfolder": subfolder, "type": "output"},
                )
                if resp.status_code == 200:
                    output_path.write_bytes(resp.content)
                    return True
    except Exception as e:
        print(f"  Download error: {e}", file=sys.stderr)
    return False


def generate_image(client: httpx.Client, prompt: str, output_name: str,
                   landscape: bool = True, portrait_mode: bool = False,
                   output_dir: Path = None) -> bool:
    """Generate a single image. Returns True on success."""
    if output_dir is None:
        output_dir = Path(__file__).parent.parent.parent / "images"

    output_path = output_dir / output_name
    print(f"  Generating: {output_name}...")

    workflow = build_workflow(prompt, NEGATIVE_PROMPT, landscape,
                              portrait_mode=portrait_mode)
    prompt_id = queue_prompt(client, workflow)
    if not prompt_id:
        print(f"  FAILED: Could not queue prompt for {output_name}")
        return False

    print(f"  Queued: {prompt_id[:8]}... waiting...", end="", flush=True)
    history = wait_for_completion(client, prompt_id)
    if not history:
        print(" TIMEOUT")
        return False

    print(" done. Downloading...", end="", flush=True)
    success = download_output(client, history, output_path)
    if success:
        print(f" saved to images/{output_name}")
    else:
        print(" DOWNLOAD FAILED")
    return success

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Price of Dawn ComfyUI Scene Generator")
    parser.add_argument("--session", type=int, choices=[1, 2, 3, 4, 5],
                        help="Generate all scenes for a session")
    parser.add_argument("--npc", help="Generate NPC portrait: name or 'all'")
    parser.add_argument("--scene", help="Generate specific scene by key")
    parser.add_argument("--output", help="Output filename (with --scene)")
    parser.add_argument("--list", action="store_true", help="List all available scenes")
    parser.add_argument("--output-dir", default=None, help="Output directory (default: ../../images/)")
    args = parser.parse_args()

    if args.list:
        print("Scenes:")
        for key, s in SCENES.items():
            print(f"  {key:40s} → {s['output']}")
        print("\nNPC Portraits:")
        for key, p in NPC_PORTRAITS.items():
            print(f"  {key:40s} → {p['output']}")
        return

    output_dir = Path(args.output_dir) if args.output_dir else None

    with get_client() as client:
        # Check ComfyUI is reachable
        try:
            resp = client.get(f"{COMFYUI_URL}/system_stats", timeout=10)
            if resp.status_code != 200:
                print(f"ComfyUI not responding at {COMFYUI_URL}")
                sys.exit(1)
            print(f"ComfyUI connected: {COMFYUI_URL}")
        except Exception as e:
            print(f"Cannot reach ComfyUI: {e}")
            sys.exit(1)

        if args.session:
            prefix = f"session{args.session}-"
            session_scenes = {k: v for k, v in SCENES.items() if k.startswith(prefix)}
            if not session_scenes:
                print(f"No scenes found for session {args.session}")
                sys.exit(1)
            print(f"\nGenerating {len(session_scenes)} scenes for session {args.session}:")
            results = []
            for key, scene in session_scenes.items():
                ok = generate_image(client, scene["prompt"], scene["output"],
                                    scene.get("landscape", True), output_dir=output_dir)
                results.append((key, ok))
            print(f"\nSummary: {sum(1 for _, ok in results if ok)}/{len(results)} succeeded")

        elif args.npc:
            targets = NPC_PORTRAITS if args.npc == "all" else {
                args.npc: NPC_PORTRAITS.get(args.npc)
            }
            if not targets or None in targets.values():
                print(f"NPC '{args.npc}' not found. Available: {list(NPC_PORTRAITS.keys())}")
                sys.exit(1)
            print(f"\nGenerating {len(targets)} NPC portrait(s):")
            for key, portrait in targets.items():
                generate_image(client, portrait["prompt"], portrait["output"],
                               landscape=False, portrait_mode=True, output_dir=output_dir)

        elif args.scene:
            scene = SCENES.get(args.scene)
            if not scene:
                print(f"Scene '{args.scene}' not found. Use --list to see options.")
                sys.exit(1)
            output_name = args.output or scene["output"]
            generate_image(client, scene["prompt"], output_name,
                           scene.get("landscape", True), output_dir=output_dir)

        else:
            parser.print_help()


if __name__ == "__main__":
    main()
