#!/usr/bin/env python3
"""
Neo4j NPC Relationship Graph Client — The Price of Dawn
Manages NPC relationships, player interactions, and information flow.

Usage:
    python3 neo4j_client.py --init              # Load initial graph from init_graph.cypher
    python3 neo4j_client.py --status            # Show graph summary
    python3 neo4j_client.py --player Kira --npc "Theron Waide" --session 2 --tier 2 --phrase "I know what you found"
    python3 neo4j_client.py --reveal-secret --player Kira --npc "Theron Waide" --secret theron-knew-year42 --session 2
    python3 neo4j_client.py --query "who-knows-ritual"
    python3 neo4j_client.py --query "info-travel" --from-npc "Erem the Wadewalker" --to-npc "Chancellor Ostenveld"
    python3 neo4j_client.py --query "player-interactions" --player Kira

Config via env vars:
    NEO4J_URL       — default: https://neo4j.research-ready.nl
    NEO4J_USER      — default: neo4j
    NEO4J_PASSWORD  — from KeePass: keepassxc-cli show .../price-of-dawn-credentials.kdbx "PriceOfDawn/Neo4j"
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path

try:
    from neo4j import GraphDatabase
except ImportError:
    print("pip install neo4j", file=sys.stderr)
    sys.exit(1)

NEO4J_URL      = os.environ.get("NEO4J_URL",      "bolt://10.0.1.114:7687")
NEO4J_HTTP_URL = os.environ.get("NEO4J_HTTP_URL", "https://neo4j.research-ready.nl")
NEO4J_USER     = os.environ.get("NEO4J_USER",     "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "")

CYPHER_INIT_FILE = Path(__file__).parent / "init_graph.cypher"


def get_password() -> str:
    if NEO4J_PASSWORD:
        return NEO4J_PASSWORD
    # Try KeePass
    kdbx = Path.home() / "Nextcloud/Github/InstallLocalAiPackage/price-of-dawn-credentials.kdbx"
    pwd_env = os.environ.get("KEEPASS_MASTER_PASSWORD_POD", "")
    if kdbx.exists() and pwd_env:
        result = subprocess.run(
            ["keepassxc-cli", "show", str(kdbx), "PriceOfDawn/Neo4j", "--show-protected"],
            input=pwd_env + "\n", capture_output=True, text=True
        )
        for line in result.stdout.splitlines():
            if line.startswith("Password:"):
                return line.split(":", 1)[1].strip()
    print("ERROR: Set NEO4J_PASSWORD or KEEPASS_MASTER_PASSWORD_POD", file=sys.stderr)
    sys.exit(1)


class GraphClient:
    def __init__(self):
        password = get_password()
        self.driver = GraphDatabase.driver(NEO4J_URL, auth=(NEO4J_USER, password))

    def close(self):
        self.driver.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def run(self, query: str, **params) -> list:
        with self.driver.session() as session:
            result = session.run(query, **params)
            return [dict(record) for record in result]

    # -----------------------------------------------------------------------
    # Init
    # -----------------------------------------------------------------------

    def init_from_cypher(self):
        """Load init_graph.cypher — run each statement block."""
        content = CYPHER_INIT_FILE.read_text()
        # Split on semicolons, skip comment-only blocks and MATCH/MERGE verify lines
        statements = [s.strip() for s in content.split(";")]
        run_count = 0
        skip_count = 0
        for stmt in statements:
            # Skip empty or pure comment blocks
            lines = [l for l in stmt.splitlines() if l.strip() and not l.strip().startswith("//")]
            if not lines:
                skip_count += 1
                continue
            try:
                self.run(stmt)
                run_count += 1
                # Brief label for progress
                first_line = lines[0][:60]
                print(f"  OK: {first_line}...")
            except Exception as e:
                if "already exists" in str(e).lower() or "equivalent" in str(e).lower():
                    skip_count += 1
                else:
                    print(f"  WARN: {e} — stmt: {lines[0][:60]}")
        print(f"\nLoaded: {run_count} statements, {skip_count} skipped/empty")

    # -----------------------------------------------------------------------
    # Status
    # -----------------------------------------------------------------------

    def status(self):
        counts = self.run("""
            MATCH (n)
            WITH labels(n)[0] as label, count(n) as cnt
            RETURN label, cnt ORDER BY label
        """)
        print("\n=== Graph Status ===")
        for row in counts:
            print(f"  {row['label']:20s}: {row['cnt']}")

        rels = self.run("MATCH ()-[r]->() RETURN type(r) as rel, count(r) as cnt ORDER BY cnt DESC")
        print("\n  Relationships:")
        for row in rels:
            print(f"    {row['rel']:25s}: {row['cnt']}")

    # -----------------------------------------------------------------------
    # Player interaction tracking
    # -----------------------------------------------------------------------

    def ensure_player(self, player_name: str):
        self.run("""
            MERGE (:Player {name: $name})
        """, name=player_name)

    def record_interaction(self, player: str, npc: str, session: int,
                           tier: int = 1, phrase: str = "", notes: str = ""):
        self.ensure_player(player)
        self.run("""
            MATCH (p:Player {name: $player}), (n:NPC {name: $npc})
            MERGE (p)-[r:INTERACTED {npc: $npc}]->(n)
            SET r.session = $session,
                r.tier_unlocked = $tier,
                r.unlock_phrase = $phrase,
                r.notes = $notes,
                r.updated = timestamp()
        """, player=player, npc=npc, session=session, tier=tier, phrase=phrase, notes=notes)
        print(f"Recorded: {player} ↔ {npc} (session {session}, tier {tier})")

    def reveal_secret(self, player: str, npc: str, secret_id: str, session: int):
        """Record that a player revealed a secret to an NPC."""
        self.ensure_player(player)
        # Create the revealed_to edge
        self.run("""
            MATCH (p:Player {name: $player}), (n:NPC {name: $npc}), (s:Secret {id: $secret_id})
            MERGE (p)-[:REVEALED_TO {session: $session}]->(n)
            MERGE (n)-[:NOW_KNOWS {revealed_by: $player, session: $session, source: "players"}]->(s)
        """, player=player, npc=npc, secret_id=secret_id, session=session)
        print(f"Secret '{secret_id}' revealed to {npc} by {player} in session {session}")

    # -----------------------------------------------------------------------
    # Queries
    # -----------------------------------------------------------------------

    def query_who_knows_ritual(self):
        """Who knows about the ritual cost?"""
        rows = self.run("""
            MATCH (n)-[r:KNOWS]->(s:Secret {id: "ritual-cost"})
            RETURN n.name as name, n.role as role, r.since_year as year, r.how as how
            ORDER BY r.since_year
        """)
        print("\n=== Who Knows the Ritual Cost? ===")
        for r in rows:
            year = f"Year {r['year']}" if r['year'] else "unknown"
            print(f"  {r['name']:30s} ({r['role']}) — {year}")
            if r['how']:
                print(f"    via: {r['how']}")

    def query_info_travel(self, from_npc: str, to_npc: str):
        """Shortest information path between two NPCs."""
        rows = self.run("""
            MATCH path = shortestPath(
                (a:NPC {name: $from_npc})-[*..6]-(b:NPC {name: $to_npc})
            )
            RETURN [n in nodes(path) | coalesce(n.name, labels(n)[0])] as path_names,
                   length(path) as hops
        """, from_npc=from_npc, to_npc=to_npc)
        print(f"\n=== Info Path: {from_npc} → {to_npc} ===")
        if not rows:
            print("  No path found (not connected within 6 hops)")
        for r in rows:
            print(f"  {' → '.join(r['path_names'])} ({r['hops']} hops)")

    def query_player_interactions(self, player: str):
        """All interactions for a player."""
        rows = self.run("""
            MATCH (p:Player {name: $player})-[r:INTERACTED]->(n:NPC)
            RETURN n.name as npc, n.role as role, r.session as session,
                   r.tier_unlocked as tier, r.notes as notes
            ORDER BY r.session
        """, player=player)
        print(f"\n=== {player}'s NPC Interactions ===")
        if not rows:
            print("  None recorded")
        for r in rows:
            print(f"  Session {r['session']}: {r['npc']:30s} (Tier {r['tier']})")
            if r['notes']:
                print(f"    {r['notes']}")

    def query_lowmark_npcs(self):
        """Which NPCs would hear about activity in Lowmark?"""
        rows = self.run("""
            MATCH (n:NPC)
            WHERE n.faction IN ["Civic Guard", "Civic Council"]
               OR exists { MATCH (n)-[:WORKS_AT]->(:Location {district: "Lowmark"}) }
               OR exists { MATCH (n)-[:KNOWS_PERSONALLY]->(:NPC {name: "Sera Voss"}) }
            RETURN n.name, n.role, n.faction
        """)
        print("\n=== NPCs Who Hear About Lowmark Events ===")
        for r in rows:
            print(f"  {r['n.name']:30s} ({r['n.role']})")

    def query_undiscovered_ostenveld(self):
        """Secrets Ostenveld knows that no player has figured out."""
        rows = self.run("""
            MATCH (o:NPC {name: "Chancellor Ostenveld"})-[:KNOWS]->(s:Secret)
            WHERE NOT exists { MATCH (:Player)-[:KNOWS]->(s) }
            RETURN s.id, s.content
        """)
        print("\n=== Ostenveld's Undiscovered Secrets ===")
        for r in rows:
            print(f"  [{r['s.id']}] {r['s.content']}")

    def query_session_summary(self, session: int):
        """All player-NPC activity in a given session."""
        rows = self.run("""
            MATCH (p:Player)-[r:INTERACTED]->(n:NPC)
            WHERE r.session = $session
            RETURN p.name as player, n.name as npc, r.tier_unlocked as tier, r.notes as notes
        """, session=session)
        reveal_rows = self.run("""
            MATCH (p:Player)-[r:REVEALED_TO]->(n:NPC)
            WHERE r.session = $session
            RETURN p.name as player, n.name as npc
        """, session=session)
        print(f"\n=== Session {session} Summary ===")
        print("Interactions:")
        for r in rows:
            print(f"  {r['player']} ↔ {r['npc']} (Tier {r['tier']}){' — ' + r['notes'] if r['notes'] else ''}")
        if reveal_rows:
            print("Secrets Revealed to NPCs:")
            for r in reveal_rows:
                print(f"  {r['player']} → {r['npc']}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Price of Dawn Neo4j Graph Client")
    parser.add_argument("--init", action="store_true", help="Load initial graph from init_graph.cypher")
    parser.add_argument("--status", action="store_true", help="Show graph summary")
    parser.add_argument("--player", help="Player name")
    parser.add_argument("--npc", help="NPC name")
    parser.add_argument("--session", type=int, help="Session number")
    parser.add_argument("--tier", type=int, default=1, choices=[1, 2, 3])
    parser.add_argument("--phrase", default="", help="Unlock phrase used")
    parser.add_argument("--notes", default="", help="Interaction notes")
    parser.add_argument("--reveal-secret", action="store_true", help="Record a secret revealed to NPC")
    parser.add_argument("--secret", help="Secret ID (use with --reveal-secret)")
    parser.add_argument("--query", choices=[
        "who-knows-ritual", "info-travel", "player-interactions",
        "lowmark-npcs", "undiscovered-ostenveld", "session-summary"
    ])
    parser.add_argument("--from-npc", help="Source NPC (for info-travel query)")
    parser.add_argument("--to-npc", help="Target NPC (for info-travel query)")
    args = parser.parse_args()

    try:
        with GraphClient() as g:
            if args.init:
                print(f"Loading graph from {CYPHER_INIT_FILE}...")
                g.init_from_cypher()
                g.status()

            elif args.status:
                g.status()

            elif args.reveal_secret:
                if not all([args.player, args.npc, args.secret, args.session]):
                    print("--reveal-secret requires --player, --npc, --secret, --session")
                    sys.exit(1)
                g.reveal_secret(args.player, args.npc, args.secret, args.session)

            elif args.player and args.npc and args.session:
                g.record_interaction(args.player, args.npc, args.session,
                                     args.tier, args.phrase, args.notes)

            elif args.query:
                if args.query == "who-knows-ritual":
                    g.query_who_knows_ritual()
                elif args.query == "info-travel":
                    if not args.from_npc or not args.to_npc:
                        print("--query info-travel requires --from-npc and --to-npc")
                        sys.exit(1)
                    g.query_info_travel(args.from_npc, args.to_npc)
                elif args.query == "player-interactions":
                    if not args.player:
                        print("--query player-interactions requires --player")
                        sys.exit(1)
                    g.query_player_interactions(args.player)
                elif args.query == "lowmark-npcs":
                    g.query_lowmark_npcs()
                elif args.query == "undiscovered-ostenveld":
                    g.query_undiscovered_ostenveld()
                elif args.query == "session-summary":
                    if not args.session:
                        print("--query session-summary requires --session")
                        sys.exit(1)
                    g.query_session_summary(args.session)
            else:
                parser.print_help()

    except Exception as e:
        print(f"Neo4j error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
