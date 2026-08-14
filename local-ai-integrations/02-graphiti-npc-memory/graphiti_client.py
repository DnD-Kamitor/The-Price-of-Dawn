#!/usr/bin/env python3
"""
Graphiti NPC Memory Client — The Price of Dawn
Stores and retrieves NPC conversation memory using Graphiti temporal knowledge graph.

Graphiti is at CT124 (10.0.1.124:8000) — internal network only.
Not reachable from outside cluster without VPN/SSH tunnel.

Usage as library:
    from graphiti_client import NPCMemory
    mem = NPCMemory()
    context = mem.get_context("theron-waide", "Kira")
    # ... conversation ...
    mem.store_exchange("theron-waide", "Kira", "session-3", "Kira told Theron she found the documents.", tier=2)
    tier = mem.get_tier("theron-waide", "Kira")

Usage as CLI:
    python3 graphiti_client.py --action get --npc theron-waide --player Kira
    python3 graphiti_client.py --action store --npc theron-waide --player Kira --session session-3 --summary "..."
    python3 graphiti_client.py --action set-tier --npc theron-waide --player Kira --tier 2
    python3 graphiti_client.py --action gm-report
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import Optional

try:
    import httpx
except ImportError:
    print("pip install httpx", file=sys.stderr)
    sys.exit(1)

GRAPHITI_BASE_URL = os.environ.get("GRAPHITI_BASE_URL", "http://10.0.1.124:8000")
GROUP_ID = "price-of-dawn"

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


class NPCMemory:
    """Client for Graphiti NPC memory store."""

    def __init__(self, base_url: str = GRAPHITI_BASE_URL, timeout: float = 8.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._available: Optional[bool] = None

    def _client(self) -> httpx.Client:
        return httpx.Client(timeout=self.timeout)

    def is_available(self) -> bool:
        if self._available is None:
            try:
                with self._client() as c:
                    resp = c.get(f"{self.base_url}/healthcheck", timeout=3.0)
                    self._available = resp.status_code < 500
            except Exception:
                self._available = False
        return self._available

    # ------------------------------------------------------------------
    # Read operations
    # ------------------------------------------------------------------

    def get_context(self, npc_slug: str, player_name: str) -> str:
        """Get formatted memory context string for system prompt injection.
        Returns 'No previous interactions recorded.' if unavailable."""
        if not self.is_available():
            return "No previous interactions recorded. [Graphiti unavailable — internal network only]"

        npc_name = NPC_DISPLAY_NAMES.get(npc_slug, npc_slug)
        query = (
            f"Previous conversations between {npc_name} and player {player_name}. "
            f"What did they discuss? What did the player reveal? What tier is unlocked? "
            f"Any secrets shared?"
        )
        try:
            with self._client() as c:
                resp = c.post(
                    f"{self.base_url}/v1/graph/search",
                    json={"query": query, "group_id": GROUP_ID, "num_results": 8},
                )
                if resp.status_code != 200:
                    return "Memory retrieval failed."
                facts = resp.json().get("results", [])
                if not facts:
                    return "No previous interactions recorded."
                lines = []
                for f in facts:
                    ts = f.get("created_at", "")[:10]
                    lines.append(f"[{ts}] {f.get('fact', '')}")
                return "\n".join(lines)
        except Exception as e:
            return f"Memory unavailable: {e}"

    def get_tier(self, npc_slug: str, player_name: str) -> int:
        """Return highest tier unlocked for this player-NPC pair (1, 2, or 3)."""
        if not self.is_available():
            return 1

        npc_name = NPC_DISPLAY_NAMES.get(npc_slug, npc_slug)
        try:
            with self._client() as c:
                resp = c.post(
                    f"{self.base_url}/v1/graph/search",
                    json={
                        "query": f"tier unlock status for player {player_name} with {npc_name}",
                        "group_id": GROUP_ID,
                        "num_results": 5,
                    },
                )
                if resp.status_code != 200:
                    return 1
                facts = resp.json().get("results", [])
                tier = 1
                for f in facts:
                    body = f.get("fact", "").lower()
                    if "tier 3" in body or "tier3" in body:
                        return 3
                    if ("tier 2" in body or "tier2" in body) and tier < 3:
                        tier = 2
                return tier
        except Exception:
            return 1

    def get_all_npc_states(self) -> dict:
        """GM report: get everything stored about all NPCs. For pre-session prep."""
        if not self.is_available():
            return {"error": "Graphiti unavailable"}

        report = {}
        for slug, name in NPC_DISPLAY_NAMES.items():
            try:
                with self._client() as c:
                    resp = c.post(
                        f"{self.base_url}/v1/graph/search",
                        json={
                            "query": f"All interactions, conversations, revelations involving {name}",
                            "group_id": GROUP_ID,
                            "num_results": 15,
                        },
                    )
                    facts = resp.json().get("results", []) if resp.status_code == 200 else []
                    report[slug] = {
                        "name": name,
                        "facts": [f.get("fact", "") for f in facts],
                        "fact_count": len(facts),
                    }
            except Exception as e:
                report[slug] = {"name": name, "error": str(e)}
        return report

    # ------------------------------------------------------------------
    # Write operations
    # ------------------------------------------------------------------

    def store_exchange(self, npc_slug: str, player_name: str, session_id: str,
                       summary: str, tier: Optional[int] = None) -> bool:
        """Store a conversation summary. Returns True if successful."""
        if not self.is_available():
            return False

        npc_name = NPC_DISPLAY_NAMES.get(npc_slug, npc_slug)
        episode_body = f"{summary}"
        if tier:
            episode_body += f" [Tier {tier} active for {player_name} with {npc_name}]"

        try:
            with self._client() as c:
                resp = c.post(
                    f"{self.base_url}/v1/graph/episodes",
                    json={
                        "name": f"{session_id}-{npc_slug}-{player_name.lower().replace(' ', '-')}-{datetime.utcnow().strftime('%H%M%S')}",
                        "episode_body": episode_body,
                        "source": "npc_client",
                        "source_description": f"NPC conversation: {npc_name} with {player_name}",
                        "reference_time": datetime.utcnow().isoformat(),
                        "group_id": GROUP_ID,
                    },
                )
                return resp.status_code in (200, 201)
        except Exception:
            return False

    def set_tier(self, npc_slug: str, player_name: str, tier: int,
                 unlock_phrase: str = "", session_id: str = "unknown") -> bool:
        """Record a tier unlock event."""
        npc_name = NPC_DISPLAY_NAMES.get(npc_slug, npc_slug)
        phrase_note = f" Unlock phrase used: '{unlock_phrase}'." if unlock_phrase else ""
        summary = (
            f"TIER UNLOCK: Player {player_name} has unlocked Tier {tier} with {npc_name}."
            f"{phrase_note} Session: {session_id}."
        )
        return self.store_exchange(npc_slug, player_name, session_id, summary, tier=tier)

    def store_world_event(self, session_id: str, event: str) -> bool:
        """Store a world event (not NPC-specific)."""
        if not self.is_available():
            return False
        try:
            with self._client() as c:
                resp = c.post(
                    f"{self.base_url}/v1/graph/episodes",
                    json={
                        "name": f"{session_id}-world-event-{datetime.utcnow().strftime('%H%M%S')}",
                        "episode_body": f"WORLD EVENT [{session_id}]: {event}",
                        "source": "gm",
                        "source_description": "GM world event log",
                        "reference_time": datetime.utcnow().isoformat(),
                        "group_id": GROUP_ID,
                    },
                )
                return resp.status_code in (200, 201)
        except Exception:
            return False


# ---------------------------------------------------------------------------
# SSH tunnel helper (for use from outside the cluster)
# ---------------------------------------------------------------------------

def open_ssh_tunnel() -> Optional[object]:
    """Open SSH tunnel to Graphiti via Proxmox jump host. Returns tunnel process."""
    import subprocess
    try:
        tunnel = subprocess.Popen([
            "ssh", "-N", "-L", "18124:10.0.1.124:8000",
            "-i", os.path.expanduser("~/.ssh/proxmox_id_ed25519"),
            "-o", "StrictHostKeyChecking=no",
            "-o", "ExitOnForwardFailure=yes",
            f"root@10.0.0.16",
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        import time
        time.sleep(2)
        if tunnel.poll() is None:
            print("[Tunnel] SSH tunnel open: localhost:18124 → Graphiti CT124:8000", file=sys.stderr)
            return tunnel
    except Exception as e:
        print(f"[Tunnel] Failed: {e}", file=sys.stderr)
    return None


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Graphiti NPC Memory CLI")
    parser.add_argument("--action", required=True,
                        choices=["get", "store", "set-tier", "gm-report", "health", "tunnel"])
    parser.add_argument("--npc",     help="NPC slug")
    parser.add_argument("--player",  help="Player name")
    parser.add_argument("--session", default=f"session-{datetime.now().strftime('%Y%m%d')}")
    parser.add_argument("--summary", help="Conversation summary to store")
    parser.add_argument("--tier",    type=int, choices=[1, 2, 3])
    parser.add_argument("--phrase",  default="", help="Unlock phrase used")
    parser.add_argument("--tunnel",  action="store_true", help="Open SSH tunnel first")
    args = parser.parse_args()

    tunnel_proc = None
    base_url = GRAPHITI_BASE_URL

    if args.tunnel or args.action == "tunnel":
        tunnel_proc = open_ssh_tunnel()
        if tunnel_proc:
            base_url = "http://localhost:18124"

    mem = NPCMemory(base_url=base_url)

    try:
        if args.action == "health":
            ok = mem.is_available()
            print(f"Graphiti {'available' if ok else 'unavailable'} at {base_url}")

        elif args.action == "tunnel":
            if tunnel_proc:
                print("Tunnel open. Ctrl+C to close.")
                tunnel_proc.wait()

        elif args.action == "get":
            if not args.npc or not args.player:
                print("--npc and --player required"); sys.exit(1)
            print(mem.get_context(args.npc, args.player))
            tier = mem.get_tier(args.npc, args.player)
            print(f"\nCurrent tier for {args.player}: {tier}")

        elif args.action == "store":
            if not args.npc or not args.player or not args.summary:
                print("--npc, --player, --summary required"); sys.exit(1)
            ok = mem.store_exchange(args.npc, args.player, args.session, args.summary, args.tier)
            print("Stored" if ok else "Failed (Graphiti unavailable?)")

        elif args.action == "set-tier":
            if not args.npc or not args.player or not args.tier:
                print("--npc, --player, --tier required"); sys.exit(1)
            ok = mem.set_tier(args.npc, args.player, args.tier, args.phrase, args.session)
            print(f"Tier {args.tier} recorded" if ok else "Failed")

        elif args.action == "gm-report":
            report = mem.get_all_npc_states()
            for slug, data in report.items():
                print(f"\n{'='*50}")
                print(f"{data.get('name', slug)} — {data.get('fact_count', 0)} facts")
                for fact in data.get("facts", []):
                    print(f"  • {fact}")
    finally:
        if tunnel_proc and tunnel_proc.poll() is None:
            tunnel_proc.terminate()


if __name__ == "__main__":
    main()
