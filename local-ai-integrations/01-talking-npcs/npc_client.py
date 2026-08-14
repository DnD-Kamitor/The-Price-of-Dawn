#!/usr/bin/env python3
"""
NPC Chat Client — The Price of Dawn
Loads NPC system prompts, chats via LLM, speaks via openedai-speech TTS.

Usage:
    python3 npc_client.py --npc theron-waide
    python3 npc_client.py --npc sera-voss --player "Kira" --no-tts
    python3 npc_client.py --npc lira-anwick --tier 2

Config via env vars:
    OPENAI_API_KEY          — direct OpenAI (default fallback)
    LITELLM_API_KEY         — LiteLLM proxy key (preferred when available)
    LITELLM_BASE_URL        — LiteLLM proxy URL (default: https://litellm.research-ready.nl)
    TTS_BASE_URL            — TTS service (default: https://tts.research-ready.nl)
    GRAPHITI_BASE_URL       — Graphiti memory (default: http://10.0.1.124:8000)
    MTLS_CERT               — path to mTLS client cert (default: /tmp/mtls_client.crt)
    MTLS_KEY                — path to mTLS client key (default: /tmp/mtls_client.key)
"""

import os
import sys
import json
import re
import subprocess
import tempfile
import argparse
from pathlib import Path
from typing import Optional
from datetime import datetime

try:
    from openai import OpenAI
except ImportError:
    print("pip install openai httpx", file=sys.stderr)
    sys.exit(1)

try:
    import httpx
except ImportError:
    print("pip install httpx", file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

PROMPTS_DIR = Path(__file__).parent / "npc-prompts"
TTS_BASE_URL = os.environ.get("TTS_BASE_URL", "https://tts.research-ready.nl")
GRAPHITI_BASE_URL = os.environ.get("GRAPHITI_BASE_URL", "http://10.0.1.124:8000")
MTLS_CERT = os.environ.get("MTLS_CERT", "/tmp/mtls_client.crt")
MTLS_KEY = os.environ.get("MTLS_KEY", "/tmp/mtls_client.key")

LITELLM_BASE_URL = os.environ.get("LITELLM_BASE_URL", "https://litellm.research-ready.nl")
LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen3:14b")

# NPC voice assignments
NPC_VOICES = {
    "theron-waide":         {"voice": "echo",    "speed": 1.05},
    "sera-voss":            {"voice": "nova",    "speed": 0.95},
    "lira-anwick":          {"voice": "shimmer", "speed": 0.95},
    "erem-wadewalker":      {"voice": "echo",    "speed": 0.90},
    "brother-edoran":       {"voice": "alloy",   "speed": 0.85},
    "tomas-areth":          {"voice": "onyx",    "speed": 0.90},
    "chancellor-ostenveld": {"voice": "onyx",    "speed": 0.90},
    "ysel-dorn":            {"voice": "shimmer", "speed": 1.00},
}

NPC_DISPLAY_NAMES = {
    "theron-waide":         "Theron Waide",
    "sera-voss":            "Sera Voss",
    "lira-anwick":          "Lira Anwick",
    "erem-wadewalker":      "Erem the Wadewalker",
    "brother-edoran":       "Brother Edoran",
    "tomas-areth":          "Tomas Areth",
    "chancellor-ostenveld": "Chancellor Ostenveld",
    "ysel-dorn":            "Ysel Dorn",
}

# ---------------------------------------------------------------------------
# mTLS cert setup
# ---------------------------------------------------------------------------

def ensure_mtls_cert():
    """Extract mTLS cert from fedora.p12 if not already done."""
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

def get_httpx_client() -> httpx.Client:
    ensure_mtls_cert()
    if os.path.exists(MTLS_CERT) and os.path.exists(MTLS_KEY):
        return httpx.Client(cert=(MTLS_CERT, MTLS_KEY), verify=False, timeout=30)
    return httpx.Client(verify=False, timeout=30)

# ---------------------------------------------------------------------------
# LLM client
# ---------------------------------------------------------------------------

def get_llm_client() -> tuple[OpenAI, str]:
    """Return (OpenAI client, model name).
    Priority: LiteLLM (pod key) → Ollama local → OpenAI direct."""
    if LITELLM_API_KEY:
        client = OpenAI(api_key=LITELLM_API_KEY, base_url=f"{LITELLM_BASE_URL}/v1")
        model = "pod-fast"
        print(f"[LLM] LiteLLM proxy → pod-fast", file=sys.stderr)
    else:
        # Ollama is OpenAI-compatible via /v1 endpoint
        client = OpenAI(api_key="ollama", base_url=f"{OLLAMA_BASE_URL}/v1")
        model = OLLAMA_MODEL
        print(f"[LLM] Ollama local → {model}", file=sys.stderr)
    return client, model

# ---------------------------------------------------------------------------
# System prompt loading
# ---------------------------------------------------------------------------

def load_system_prompt(npc_slug: str, tier: int = 1, player_name: str = "the investigator") -> str:
    """Load NPC system prompt from markdown file, inject memory placeholder."""
    prompt_file = PROMPTS_DIR / f"{npc_slug}.md"
    if not prompt_file.exists():
        available = [f.stem for f in PROMPTS_DIR.glob("*.md")]
        print(f"ERROR: No prompt file for '{npc_slug}'. Available: {available}", file=sys.stderr)
        sys.exit(1)

    content = prompt_file.read_text()

    # Extract the system prompt from inside the ```...``` block
    match = re.search(r"```\n(.*?)```", content, re.DOTALL)
    if match:
        prompt = match.group(1).strip()
    else:
        # No code fence — use entire content after the header
        prompt = content

    # Inject player name and retrieve Graphiti memory
    memory = get_graphiti_memory(npc_slug, player_name)
    prompt = prompt.replace("{{GRAPHITI_MEMORY}}", memory)
    prompt = prompt.replace("[player_name]", player_name)

    # If tier > 1, add explicit tier instruction at end of prompt
    if tier >= 2:
        prompt += f"\n\n[SESSION CONTEXT: This player has already unlocked Tier {tier}. Start the conversation in Tier {tier} mode — do not require them to say the unlock phrase again.]"

    return prompt

# ---------------------------------------------------------------------------
# Graphiti memory
# ---------------------------------------------------------------------------

def get_graphiti_memory(npc_slug: str, player_name: str) -> str:
    """Retrieve relevant memory from Graphiti. Returns empty string if unavailable."""
    try:
        with get_httpx_client() as client:
            resp = client.post(
                f"{GRAPHITI_BASE_URL}/v1/graph/search",
                json={
                    "query": f"Previous conversations and interactions between {NPC_DISPLAY_NAMES.get(npc_slug, npc_slug)} and player {player_name}. Tier unlocks. Secrets revealed.",
                    "group_id": "price-of-dawn",
                    "num_results": 6,
                },
                timeout=5.0,
            )
            if resp.status_code == 200:
                facts = resp.json().get("results", [])
                if facts:
                    lines = [f"[{f.get('created_at','')[:10]}] {f['fact']}" for f in facts]
                    return "\n".join(lines)
    except Exception:
        pass
    return "No previous interactions recorded."

def store_graphiti_memory(npc_slug: str, player_name: str, session_id: str, summary: str):
    """Store conversation summary in Graphiti. Silently skips if unavailable."""
    try:
        with get_httpx_client() as client:
            client.post(
                f"{GRAPHITI_BASE_URL}/v1/graph/episodes",
                json={
                    "name": f"{session_id}-{npc_slug}-{player_name.lower().replace(' ','-')}",
                    "episode_body": summary,
                    "source": "npc_client",
                    "source_description": f"NPC conversation: {NPC_DISPLAY_NAMES.get(npc_slug, npc_slug)} with {player_name}",
                    "reference_time": datetime.utcnow().isoformat(),
                    "group_id": "price-of-dawn",
                },
                timeout=5.0,
            )
    except Exception:
        pass

# ---------------------------------------------------------------------------
# TTS
# ---------------------------------------------------------------------------

def speak(text: str, npc_slug: str) -> bool:
    """Send text to openedai-speech and play via aplay. Returns True if successful."""
    voice_config = NPC_VOICES.get(npc_slug, {"voice": "alloy", "speed": 1.0})

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        with get_httpx_client() as client:
            resp = client.post(
                f"{TTS_BASE_URL}/v1/audio/speech",
                json={
                    "model": "tts-1",
                    "input": text,
                    "voice": voice_config["voice"],
                    "speed": voice_config["speed"],
                },
                timeout=30.0,
            )
            if resp.status_code != 200 or len(resp.content) < 100:
                return False
            with open(tmp_path, "wb") as f:
                f.write(resp.content)

        # Try aplay, then paplay, then mpv
        for player in ["aplay", "paplay", "mpv --no-video"]:
            cmd = player.split() + [tmp_path]
            result = subprocess.run(cmd, capture_output=True)
            if result.returncode == 0:
                return True
        return False
    except Exception as e:
        print(f"[TTS] Error: {e}", file=sys.stderr)
        return False
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass

# ---------------------------------------------------------------------------
# Conversation summarizer (for Graphiti storage)
# ---------------------------------------------------------------------------

def summarize_conversation(messages: list[dict], npc_name: str, player_name: str,
                            client: OpenAI, model: str) -> str:
    """Generate a 2-3 sentence summary of the conversation for Graphiti storage."""
    if len(messages) < 2:
        return ""
    convo_text = "\n".join(
        f"{'Player' if m['role']=='user' else npc_name}: {m['content']}"
        for m in messages if m["role"] != "system"
    )
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{
                "role": "user",
                "content": f"Summarize this NPC conversation in 2-3 sentences. Focus on: what the player revealed, what the NPC revealed, any trust level changes, any unlock phrases used.\n\nConversation:\n{convo_text}"
            }],
            max_tokens=150,
            temperature=0.3,
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return f"{player_name} had a conversation with {npc_name}."

# ---------------------------------------------------------------------------
# Main chat loop
# ---------------------------------------------------------------------------

def chat(npc_slug: str, player_name: str, tier: int, use_tts: bool, session_id: str):
    npc_name = NPC_DISPLAY_NAMES.get(npc_slug, npc_slug)
    print(f"\n{'='*60}")
    print(f"  {npc_name}")
    print(f"  Player: {player_name} | Tier: {tier} | TTS: {'on' if use_tts else 'off'}")
    print(f"{'='*60}")
    print(f"  Type your message. 'quit' to exit. 'tier2'/'tier3' to unlock.")
    print(f"{'='*60}\n")

    client, model = get_llm_client()
    system_prompt = load_system_prompt(npc_slug, tier, player_name)

    messages = [{"role": "system", "content": system_prompt}]

    try:
        while True:
            try:
                user_input = input(f"{player_name}: ").strip()
            except (EOFError, KeyboardInterrupt):
                break

            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit", "q"):
                break

            # Local tier upgrade shortcut (testing convenience)
            if user_input.lower() in ("tier2", "unlock tier2"):
                tier = 2
                system_prompt = load_system_prompt(npc_slug, tier, player_name)
                messages[0] = {"role": "system", "content": system_prompt}
                print(f"[Tier 2 unlocked for {npc_name}]")
                continue
            if user_input.lower() in ("tier3", "unlock tier3"):
                tier = 3
                system_prompt = load_system_prompt(npc_slug, tier, player_name)
                messages[0] = {"role": "system", "content": system_prompt}
                print(f"[Tier 3 unlocked for {npc_name}]")
                continue

            messages.append({"role": "user", "content": user_input})

            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=300,
                    temperature=0.85,
                )
                reply = response.choices[0].message.content.strip()
            except Exception as e:
                print(f"[LLM Error] {e}", file=sys.stderr)
                continue

            messages.append({"role": "assistant", "content": reply})

            print(f"\n{npc_name}: {reply}\n")

            if use_tts:
                speak(reply, npc_slug)

    finally:
        # Store conversation summary in Graphiti
        if len(messages) > 2:
            summary = summarize_conversation(messages, npc_name, player_name, client, model)
            if summary:
                store_graphiti_memory(npc_slug, player_name, session_id, summary)
                print(f"\n[Memory stored: {summary[:80]}...]")

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Price of Dawn NPC Chat Client")
    parser.add_argument("--npc", required=True, choices=list(NPC_VOICES.keys()),
                        help="NPC slug to chat with")
    parser.add_argument("--player", default="the investigator",
                        help="Player character name (for memory tracking)")
    parser.add_argument("--tier", type=int, default=1, choices=[1, 2, 3],
                        help="Starting tier (1=stranger, 2=trusted, 3=vulnerable)")
    parser.add_argument("--no-tts", action="store_true",
                        help="Disable TTS voice output")
    parser.add_argument("--session", default=f"session-{datetime.now().strftime('%Y%m%d')}",
                        help="Session ID for memory tagging")
    parser.add_argument("--list", action="store_true",
                        help="List available NPCs")
    args = parser.parse_args()

    if args.list:
        print("Available NPCs:")
        for slug, name in NPC_DISPLAY_NAMES.items():
            voices = NPC_VOICES[slug]
            print(f"  {slug:30s} {name:30s} voice={voices['voice']}")
        return

    chat(
        npc_slug=args.npc,
        player_name=args.player,
        tier=args.tier,
        use_tts=not args.no_tts,
        session_id=args.session,
    )

if __name__ == "__main__":
    main()
