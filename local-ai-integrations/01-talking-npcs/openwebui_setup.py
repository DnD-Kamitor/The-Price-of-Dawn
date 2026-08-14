#!/usr/bin/env python3
"""
OpenWebUI Model Setup — The Price of Dawn
Creates 8 NPC model configs in OpenWebUI with correct system prompts, TTS, STT.

Requires:
    OPENWEBUI_URL       — default: https://openwebui.research-ready.nl
    OPENWEBUI_EMAIL     — admin account email
    OPENWEBUI_PASSWORD  — admin account password
    MTLS_CERT / MTLS_KEY — mTLS cert paths (auto-extracted from ~/Desktop/fedora.p12)

Run once to set up, re-run to update prompts.
"""

import os
import sys
import json
import re
import subprocess
from pathlib import Path

try:
    import httpx
except ImportError:
    print("pip install httpx")
    sys.exit(1)

OPENWEBUI_URL  = os.environ.get("OPENWEBUI_URL", "https://openwebui.research-ready.nl")
OPENWEBUI_EMAIL    = os.environ.get("OPENWEBUI_EMAIL", "")
OPENWEBUI_PASSWORD = os.environ.get("OPENWEBUI_PASSWORD", "")
MTLS_CERT = os.environ.get("MTLS_CERT", "/tmp/mtls_client.crt")
MTLS_KEY  = os.environ.get("MTLS_KEY",  "/tmp/mtls_client.key")

TTS_URL     = "https://tts.research-ready.nl/v1/audio/speech"
WHISPER_URL = "http://10.0.1.108:9000/v1"   # internal, OpenWebUI is in same subnet

PROMPTS_DIR = Path(__file__).parent / "npc-prompts"

NPC_CONFIGS = [
    {
        "slug":         "theron-waide",
        "display":      "Theron Waide (Archivist)",
        "model_id":     "npc-theron-waide",
        "litellm_model": "pod-fast",
        "tts_voice":    "echo",
        "tts_speed":    1.05,
        "temperature":  0.85,
        "max_tokens":   300,
        "description":  "Master Archivist. Anxious, meticulous, guilty. Tier 2: 'I know what you found'. Tier 3: 'I've read the letter'.",
    },
    {
        "slug":         "sera-voss",
        "display":      "Sera Voss (Guard Captain)",
        "model_id":     "npc-sera-voss",
        "litellm_model": "pod-fast",
        "tts_voice":    "nova",
        "tts_speed":    0.95,
        "temperature":  0.80,
        "max_tokens":   300,
        "description":  "Lowmark Guard Captain. Direct, loyal, contained. Tier 2: 'Marta'. Tier 3: 'What have you decided?'",
    },
    {
        "slug":         "lira-anwick",
        "display":      "Lira Anwick (Healer)",
        "model_id":     "npc-lira-anwick",
        "litellm_model": "pod-fast",
        "tts_voice":    "shimmer",
        "tts_speed":    0.95,
        "temperature":  0.82,
        "max_tokens":   300,
        "description":  "Healer and Dawnborn. Competent, guarded, precise. Tier 2: 'Tell me about Mira'. Tier 3: 'I read your letter'.",
    },
    {
        "slug":         "erem-wadewalker",
        "display":      "Erem the Wadewalker",
        "model_id":     "npc-erem-wadewalker",
        "litellm_model": "pod-fast",
        "tts_voice":    "echo",
        "tts_speed":    0.90,
        "temperature":  0.80,
        "max_tokens":   350,
        "description":  "Ashfen elder. Precise, patient, skeptical. Tier 2: mention 'the void between' or 'Grey Singing Reed'. Tier 3: 'We need your help with the ritual'.",
    },
    {
        "slug":         "brother-edoran",
        "display":      "Brother Edoran (Restorers)",
        "model_id":     "npc-brother-edoran",
        "litellm_model": "pod-fast",
        "tts_voice":    "alloy",
        "tts_speed":    0.85,
        "temperature":  0.83,
        "max_tokens":   350,
        "description":  "Restorers founder. Serene, certain, heartbroken. Tier 2: ask personal motivation (second/third time). Tier 3: 'What if some of them don't want to'.",
    },
    {
        "slug":         "tomas-areth",
        "display":      "Tomas Areth (Researcher)",
        "model_id":     "npc-tomas-areth",
        "litellm_model": "pod-fast",
        "tts_voice":    "onyx",
        "tts_speed":    0.90,
        "temperature":  0.78,
        "max_tokens":   350,
        "description":  "Former Spire researcher. Measured, methodical, honest. Tier 2: 'What do you actually think should happen'. Tier 3: 'Have you told anyone'.",
    },
    {
        "slug":         "chancellor-ostenveld",
        "display":      "Chancellor Ostenveld",
        "model_id":     "npc-chancellor-ostenveld",
        "litellm_model": "pod-fast",
        "tts_voice":    "onyx",
        "tts_speed":    0.90,
        "temperature":  0.75,
        "max_tokens":   300,
        "description":  "City Council head. Controlled, strategic, exhausted. Tier 2: demonstrate knowledge of ritual cost. Tier 3: 'What is your actual position?'.",
    },
    {
        "slug":         "ysel-dorn",
        "display":      "Ysel Dorn (Temple Keeper)",
        "model_id":     "npc-ysel-dorn",
        "litellm_model": "pod-fast",
        "tts_voice":    "shimmer",
        "tts_speed":    1.00,
        "temperature":  0.88,
        "max_tokens":   300,
        "description":  "Auris temple keeper. Warm, certain, unafraid. Tier 2: 'Aren't you afraid'. Tier 3: 'I don't understand how you can accept this'.",
    },
]

# ---------------------------------------------------------------------------
# mTLS
# ---------------------------------------------------------------------------

def ensure_mtls_cert():
    if os.path.exists(MTLS_CERT) and os.path.exists(MTLS_KEY):
        return
    p12 = Path.home() / "Desktop" / "fedora.p12"
    if not p12.exists():
        print("WARNING: fedora.p12 not found — mTLS cert not extracted", file=sys.stderr)
        return
    pwd = "Research-mTLS-2024!"
    subprocess.run(["openssl", "pkcs12", "-in", str(p12), "-clcerts", "-nokeys",
                    "-out", MTLS_CERT, "-passin", f"pass:{pwd}"], capture_output=True)
    subprocess.run(["openssl", "pkcs12", "-in", str(p12), "-nocerts", "-nodes",
                    "-out", MTLS_KEY, "-passin", f"pass:{pwd}"], capture_output=True)

def get_client() -> httpx.Client:
    ensure_mtls_cert()
    cert = (MTLS_CERT, MTLS_KEY) if os.path.exists(MTLS_CERT) else None
    return httpx.Client(cert=cert, verify=False, timeout=30)

# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

def get_token(client: httpx.Client) -> str:
    if not OPENWEBUI_EMAIL or not OPENWEBUI_PASSWORD:
        print("ERROR: Set OPENWEBUI_EMAIL and OPENWEBUI_PASSWORD", file=sys.stderr)
        sys.exit(1)
    resp = client.post(
        f"{OPENWEBUI_URL}/api/v1/auths/signin",
        json={"email": OPENWEBUI_EMAIL, "password": OPENWEBUI_PASSWORD},
    )
    if resp.status_code != 200:
        print(f"Auth failed: {resp.text}", file=sys.stderr)
        sys.exit(1)
    token = resp.json().get("token", "")
    print(f"[Auth] Signed in as {OPENWEBUI_EMAIL}")
    return token

# ---------------------------------------------------------------------------
# Prompt loading
# ---------------------------------------------------------------------------

def load_prompt(slug: str) -> str:
    prompt_file = PROMPTS_DIR / f"{slug}.md"
    if not prompt_file.exists():
        print(f"WARNING: No prompt file for {slug}", file=sys.stderr)
        return f"You are {slug}, a character in The Price of Dawn D&D campaign."
    content = prompt_file.read_text()
    match = re.search(r"```\n(.*?)```", content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return content

# ---------------------------------------------------------------------------
# Model creation / update
# ---------------------------------------------------------------------------

def upsert_model(client: httpx.Client, token: str, npc: dict):
    headers = {"Authorization": f"Bearer {token}"}
    system_prompt = load_prompt(npc["slug"])

    model_body = {
        "id":          npc["model_id"],
        "name":        npc["display"],
        "base_model_id": f"litellm/{npc['litellm_model']}",
        "meta": {
            "description": npc["description"],
            "capabilities": {"vision": False},
        },
        "params": {
            "system":      system_prompt,
            "temperature": npc["temperature"],
            "max_tokens":  npc["max_tokens"],
            "stream_response": True,
        },
        "info": {
            "tts": {
                "engine": "openai",
                "url":    TTS_URL,
                "voice":  npc["tts_voice"],
                "speed":  npc["tts_speed"],
            },
            "stt": {
                "engine": "openai",
                "url":    WHISPER_URL,
                "model":  "whisper-1",
                "language": "en",
            },
        },
    }

    # Try update first, then create
    resp = client.get(f"{OPENWEBUI_URL}/api/v1/models/{npc['model_id']}", headers=headers)
    if resp.status_code == 200:
        resp = client.post(
            f"{OPENWEBUI_URL}/api/v1/models/{npc['model_id']}/update",
            headers=headers, json=model_body,
        )
        verb = "Updated"
    else:
        resp = client.post(
            f"{OPENWEBUI_URL}/api/v1/models/create",
            headers=headers, json=model_body,
        )
        verb = "Created"

    if resp.status_code in (200, 201):
        print(f"[{verb}] {npc['display']} ({npc['model_id']})")
    else:
        print(f"[FAIL]  {npc['display']}: {resp.status_code} {resp.text[:120]}")

# ---------------------------------------------------------------------------
# Workspace creation
# ---------------------------------------------------------------------------

def create_workspaces(client: httpx.Client, token: str):
    headers = {"Authorization": f"Bearer {token}"}

    # GM workspace — all NPCs
    gm_workspace = {
        "name": "Price of Dawn — GM",
        "description": "GM access to all NPC models. Full tier system.",
        "models": [npc["model_id"] for npc in NPC_CONFIGS],
        "permissions": {"chat": True, "vision": False, "image_generation": False},
    }

    # Player workspace — NPCs without GM-only notes visible
    player_workspace = {
        "name": "Price of Dawn — Players",
        "description": "Between-session NPC chat. Use the in-world unlock phrases to access deeper tiers.",
        "models": [npc["model_id"] for npc in NPC_CONFIGS],
        "permissions": {"chat": True, "vision": False, "image_generation": False},
    }

    for ws in [gm_workspace, player_workspace]:
        resp = client.post(
            f"{OPENWEBUI_URL}/api/v1/workspaces",
            headers=headers, json=ws,
        )
        status = "Created" if resp.status_code in (200, 201) else f"Failed ({resp.status_code})"
        print(f"[Workspace] {ws['name']}: {status}")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=== OpenWebUI NPC Setup — The Price of Dawn ===\n")

    with get_client() as client:
        token = get_token(client)

        print("\n--- Creating/updating NPC models ---")
        for npc in NPC_CONFIGS:
            upsert_model(client, token, npc)

        print("\n--- Creating workspaces ---")
        create_workspaces(client, token)

    print("\nDone. Verify at:", OPENWEBUI_URL)
    print("\nNPC model IDs:")
    for npc in NPC_CONFIGS:
        print(f"  {npc['model_id']:35s}  {npc['display']}")

if __name__ == "__main__":
    main()
