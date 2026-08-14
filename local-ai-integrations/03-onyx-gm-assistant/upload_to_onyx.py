#!/usr/bin/env python3
"""
Onyx Document Upload — The Price of Dawn
Uploads campaign markdown files to Onyx knowledge base for GM queries.

Service: Onyx at https://onyx.research-ready.nl (CT307, ~91% RAM — monitor)

Usage:
    python3 upload_to_onyx.py --init          # Create document sets and persona
    python3 upload_to_onyx.py --upload-gm     # Upload GM-only documents
    python3 upload_to_onyx.py --upload-player # Upload player-safe documents
    python3 upload_to_onyx.py --status        # Show indexed documents

Config via env vars:
    ONYX_URL        — default: https://onyx.research-ready.nl
    ONYX_EMAIL      — Onyx admin email
    ONYX_PASSWORD   — Onyx admin password (or set KEEPASS_MASTER_PASSWORD_POD)
    MTLS_CERT       — mTLS cert path (default: /tmp/mtls_client.crt)
    MTLS_KEY        — mTLS key path (default: /tmp/mtls_client.key)

RAM WARNING: CT307 is at ~91% RAM. Upload in small batches (max 5 files at a time).
Watch https://grafana.research-ready.nl while indexing. If OOM:
    pct exec 307 -- docker compose restart   (from Proxmox console)
"""

import os
import sys
import time
import subprocess
import argparse
from pathlib import Path

try:
    import httpx
except ImportError:
    print("pip install httpx", file=sys.stderr)
    sys.exit(1)

ONYX_URL  = os.environ.get("ONYX_URL",  "https://onyx.research-ready.nl")
ONYX_EMAIL    = os.environ.get("ONYX_EMAIL",    "")
ONYX_PASSWORD = os.environ.get("ONYX_PASSWORD", "")
MTLS_CERT = os.environ.get("MTLS_CERT", "/tmp/mtls_client.crt")
MTLS_KEY  = os.environ.get("MTLS_KEY",  "/tmp/mtls_client.key")

REPO_ROOT = Path(__file__).parent.parent.parent

# GM-only files (contain secrets, mechanics, NPC tier 2/3 info)
GM_FILES = [
    "appendix.md",           # Small — good first test
    "running-the-campaign.md",
    "npcs.md",
    "session1.md",
    "session2.md",
    "session3.md",
    "session4.md",
    "session5.md",
    "knowledge-tiers.md",
    "factions-guide.md",
    "setting.md",
    "gm-tools.md",
    "deep-archive.md",
    "crafting-and-professions.md",
    "ai-tools.md",
]

# Player-safe files (no spoilers, no GM secrets)
PLAYER_FILES = [
    "player-guide.md",
    "player-handout.md",
    "discovery-quests.md",
    "world-lore.md",
    "pantheon.md",
    "trade.md",
]

GM_PERSONA_INSTRUCTIONS = """You are a reference assistant for the tabletop RPG campaign "The Price of Dawn."
The GM is asking you questions during session prep or live play.

Answer from the indexed documents only. Always cite which file and section your answer comes from.
If the answer requires information from multiple files, synthesize them and list all sources.
If you cannot find the answer in the documents, say so explicitly — do not guess.

Priority order for sources:
- session1-5.md for encounter mechanics and pacing
- npcs.md for NPC behavior, secrets, and OGAS format
- knowledge-tiers.md for what players are allowed to know at each tier
- knowledge-tiers.md for information access rules

Keep answers concise — the GM may be mid-session. Lead with the direct answer, then the source.
For live-play queries, respond in under 50 words if possible.
For prep queries, full detail with citations."""

PLAYER_PERSONA_INSTRUCTIONS = """You are the Varenhold Civic Repository's public information system.
Answer only from player-safe document sets. Never reveal GM-only content.
Respond in-world — you are an archival reference system, not an AI assistant.
If asked about something restricted (ritual mechanics, NPC secrets, anything from GM files), respond:
"That record is sealed. Restricted access only."
Use formal archival language. Be helpful within limits."""


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
        return httpx.Client(cert=(MTLS_CERT, MTLS_KEY), verify=False, timeout=60.0)
    return httpx.Client(verify=False, timeout=60.0)

def get_password() -> str:
    if ONYX_PASSWORD:
        return ONYX_PASSWORD
    kdbx = Path.home() / "Nextcloud/Github/InstallLocalAiPackage/price-of-dawn-credentials.kdbx"
    env_pwd = os.environ.get("KEEPASS_MASTER_PASSWORD_POD", "")
    if kdbx.exists() and env_pwd:
        result = subprocess.run(
            ["keepassxc-cli", "show", str(kdbx), "PriceOfDawn/Onyx", "--show-protected"],
            input=env_pwd + "\n", capture_output=True, text=True
        )
        for line in result.stdout.splitlines():
            if line.startswith("Password:"):
                return line.split(":", 1)[1].strip()
    print("ERROR: Set ONYX_EMAIL and ONYX_PASSWORD (or KEEPASS_MASTER_PASSWORD_POD)", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Onyx API
# ---------------------------------------------------------------------------

class OnyxClient:
    def __init__(self, client: httpx.Client):
        self.client = client
        self.token = None

    def login(self, email: str, password: str):
        resp = self.client.post(
            f"{ONYX_URL}/auth/token",
            data={"username": email, "password": password}
        )
        if resp.status_code != 200:
            # Try alternative auth endpoint
            resp = self.client.post(
                f"{ONYX_URL}/api/auth/login",
                json={"email": email, "password": password}
            )
        if resp.status_code != 200:
            print(f"Auth failed: {resp.status_code} {resp.text[:200]}", file=sys.stderr)
            sys.exit(1)
        data = resp.json()
        self.token = data.get("access_token") or data.get("token", "")
        print(f"Authenticated as {email}")

    def headers(self) -> dict:
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def upload_file(self, filepath: Path) -> bool:
        """Upload a single file to Onyx file connector."""
        if not filepath.exists():
            print(f"  SKIP: {filepath.name} (not found)")
            return False

        content = filepath.read_text(encoding="utf-8")
        try:
            resp = self.client.post(
                f"{ONYX_URL}/api/manage/admin/connector/file/upload",
                headers=self.headers(),
                files={"files": (filepath.name, content.encode(), "text/markdown")},
            )
            if resp.status_code in (200, 201):
                print(f"  Uploaded: {filepath.name}")
                return True
            else:
                print(f"  FAIL: {filepath.name} — {resp.status_code} {resp.text[:100]}")
                return False
        except Exception as e:
            print(f"  ERROR: {filepath.name} — {e}")
            return False

    def create_connector(self, name: str, is_public: bool = False) -> int:
        """Create a file connector. Returns connector_id."""
        resp = self.client.post(
            f"{ONYX_URL}/api/manage/admin/connector",
            headers=self.headers(),
            json={
                "name": name,
                "source": "file",
                "input_type": "load_state",
                "connector_specific_config": {"file_locations": []},
                "refresh_freq": None,
                "prune_freq": None,
                "is_public": is_public,
            }
        )
        if resp.status_code in (200, 201):
            cid = resp.json().get("id")
            print(f"  Created connector '{name}' (id={cid})")
            return cid
        print(f"  Connector create failed: {resp.status_code} {resp.text[:100]}")
        return -1

    def create_credential(self) -> int:
        """Create empty file credential."""
        resp = self.client.post(
            f"{ONYX_URL}/api/manage/credential",
            headers=self.headers(),
            json={"credential_json": {}, "admin_public": True}
        )
        if resp.status_code in (200, 201):
            cid = resp.json().get("id")
            return cid
        return -1

    def create_persona(self, name: str, instructions: str,
                       document_set_ids: list[int] = None) -> bool:
        """Create an Onyx persona."""
        resp = self.client.post(
            f"{ONYX_URL}/api/admin/persona",
            headers=self.headers(),
            json={
                "name": name,
                "description": f"Price of Dawn — {name}",
                "system_text": instructions,
                "document_set_ids": document_set_ids or [],
                "llm_model_provider_override": None,
                "llm_model_version_override": None,
                "num_chunks": 10,
                "is_public": True,
            }
        )
        if resp.status_code in (200, 201):
            print(f"  Created persona '{name}'")
            return True
        print(f"  Persona create failed: {resp.status_code} {resp.text[:100]}")
        return False

    def list_documents(self):
        """List indexed documents."""
        resp = self.client.get(
            f"{ONYX_URL}/api/manage/admin/connector/indexing-status",
            headers=self.headers()
        )
        if resp.status_code == 200:
            return resp.json()
        return []


# ---------------------------------------------------------------------------
# Upload batches
# ---------------------------------------------------------------------------

def upload_files_in_batches(onyx: OnyxClient, filenames: list[str], batch_size: int = 5):
    """Upload files in small batches with pause between batches (RAM protection)."""
    success = 0
    for i in range(0, len(filenames), batch_size):
        batch = filenames[i:i + batch_size]
        print(f"\nBatch {i // batch_size + 1}: {', '.join(batch)}")
        for filename in batch:
            filepath = REPO_ROOT / filename
            if onyx.upload_file(filepath):
                success += 1
        if i + batch_size < len(filenames):
            print("  Pausing 10s between batches (RAM protection)...")
            time.sleep(10)
    return success


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Onyx Document Upload for Price of Dawn")
    parser.add_argument("--init", action="store_true",
                        help="Create connectors and personas (run once)")
    parser.add_argument("--upload-gm", action="store_true",
                        help="Upload GM-only campaign documents")
    parser.add_argument("--upload-player", action="store_true",
                        help="Upload player-safe documents")
    parser.add_argument("--status", action="store_true",
                        help="Show indexing status")
    parser.add_argument("--batch-size", type=int, default=4,
                        help="Files per batch (default 4 — RAM protection)")
    args = parser.parse_args()

    if not ONYX_EMAIL:
        print("ERROR: Set ONYX_EMAIL env var", file=sys.stderr)
        sys.exit(1)

    password = get_password()

    with get_client() as http_client:
        onyx = OnyxClient(http_client)
        onyx.login(ONYX_EMAIL, password)

        if args.init:
            print("\n=== Creating connectors and personas ===")
            print("Creating GM connector...")
            gm_id = onyx.create_connector("Price of Dawn — GM Reference", is_public=False)
            print("Creating Player connector...")
            player_id = onyx.create_connector("Price of Dawn — Player Safe", is_public=True)
            print("Creating personas...")
            onyx.create_persona("GM Oracle", GM_PERSONA_INSTRUCTIONS)
            onyx.create_persona("Varenhold Archives", PLAYER_PERSONA_INSTRUCTIONS)
            print("\nInit complete. Now run --upload-gm and --upload-player")

        elif args.upload_gm:
            print(f"\n=== Uploading {len(GM_FILES)} GM files (batch size {args.batch_size}) ===")
            print("RAM WARNING: CT307 at ~91%. Monitor grafana.research-ready.nl")
            n = upload_files_in_batches(onyx, GM_FILES, args.batch_size)
            print(f"\nDone: {n}/{len(GM_FILES)} files uploaded")

        elif args.upload_player:
            print(f"\n=== Uploading {len(PLAYER_FILES)} player-safe files ===")
            n = upload_files_in_batches(onyx, PLAYER_FILES, args.batch_size)
            print(f"\nDone: {n}/{len(PLAYER_FILES)} files uploaded")

        elif args.status:
            docs = onyx.list_documents()
            print(f"\n=== Indexing Status ({len(docs)} connectors) ===")
            for d in docs:
                name = d.get("name", "unknown")
                status = d.get("last_status", "unknown")
                count = d.get("docs_indexed", 0)
                print(f"  {name:35s} {status:15s} {count} docs")
        else:
            parser.print_help()


if __name__ == "__main__":
    main()
