# 02 — Graphiti NPC Persistent Memory

NPCs remember what players told them. Across sessions. Across weeks.
Service: Graphiti temporal memory at CT124 (10.0.1.124:8000), MCP-enabled.

---

## What Graphiti Does

Graphiti is a temporal knowledge graph with MCP interface. It stores facts as episodes tied to a timestamp and a source entity. When you query it, you get back relevant facts with their temporal context: "In session 2, Sera Voss was told that the players found the cipher. In session 3, she was told the players confronted Theron."

This is not simple key-value memory. It can answer: "What does Theron know about what the players have told him?" and return a ranked, deduplicated summary appropriate for injecting into a system prompt.

---

## Schema Design

### Entities (node types)

```
NPC          - name, role, tier_unlocked (per player)
Player       - name, character_name
Session      - session_number, date, summary
Fact         - content, confidence, source
```

### Episode format (what to store after each exchange)

```json
{
  "name": "player-npc-exchange",
  "episode_body": "Player Kira told Theron Waide that the party found Corven's sealed documents at shelf 4-17-3. Theron confirmed this and revealed he has known about the documents since Year 42. Tier 2 unlocked for this player.",
  "source": "openwebui",
  "source_description": "Between-session NPC chat / at-table exchange",
  "reference_time": "2026-08-13T19:30:00",
  "group_id": "price-of-dawn"
}
```

### How to store an episode (API call)

```bash
curl -X POST http://10.0.1.124:8000/v1/graph/episodes \
  -H "Content-Type: application/json" \
  -d '{
    "name": "session3-kira-theron-exchange",
    "episode_body": "Player Kira told Theron Waide that the party found Corven sealed documents at shelf 4-17-3. Theron confirmed he knew since Year 42. Tier 2 unlocked for Kira.",
    "source": "openwebui",
    "source_description": "Session 3 at-table exchange",
    "reference_time": "2026-08-13T19:30:00",
    "group_id": "price-of-dawn"
  }'
```

### How to retrieve memory for system prompt injection

```bash
# Get relevant memory for Theron before a conversation with player Kira
curl -X POST http://10.0.1.124:8000/v1/graph/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What has Theron Waide discussed with player Kira? What tier is unlocked?",
    "group_id": "price-of-dawn",
    "num_results": 5
  }'
```

Response is a list of facts with timestamps. Inject into the NPC system prompt at the `{{GRAPHITI_MEMORY}}` placeholder.

---

## Integration with OpenWebUI

OpenWebUI supports tools/functions. Create a custom tool that:
1. Before each NPC conversation starts: queries Graphiti for relevant memory → injects into system prompt
2. After each NPC response: posts a summary of the exchange to Graphiti

### Tool script (Python, register in OpenWebUI Tools)

```python
import httpx
import json
from datetime import datetime

GRAPHITI_URL = "http://10.0.1.124:8000"
GROUP_ID = "price-of-dawn"

async def get_npc_memory(npc_name: str, player_name: str) -> str:
    """Retrieve Graphiti memory for an NPC-player pair. Returns string for system prompt injection."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{GRAPHITI_URL}/v1/graph/search",
            json={
                "query": f"What has {npc_name} discussed with {player_name}? Previous exchanges, tier unlocks, secrets revealed.",
                "group_id": GROUP_ID,
                "num_results": 8
            },
            timeout=5.0
        )
        if resp.status_code != 200:
            return ""
        facts = resp.json().get("results", [])
        if not facts:
            return "No previous interactions recorded."
        lines = []
        for f in facts:
            ts = f.get("created_at", "")[:10]
            lines.append(f"[{ts}] {f['fact']}")
        return "\n".join(lines)


async def store_npc_exchange(
    npc_name: str,
    player_name: str,
    session_id: str,
    summary: str
) -> None:
    """Store a summary of an NPC exchange in Graphiti."""
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{GRAPHITI_URL}/v1/graph/episodes",
            json={
                "name": f"{session_id}-{npc_name.lower().replace(' ','-')}-{player_name.lower()}",
                "episode_body": summary,
                "source": "openwebui",
                "source_description": f"NPC conversation: {npc_name} with {player_name}",
                "reference_time": datetime.utcnow().isoformat(),
                "group_id": GROUP_ID
            },
            timeout=5.0
        )
```

---

## Tier State Tracking

Track which tier each player has unlocked per NPC. Store this as a Graphiti fact:

```json
{
  "episode_body": "Player Kira has unlocked Tier 2 with Theron Waide. Unlock phrase used: 'I know what you found'. Date: session 3.",
  "name": "tier-unlock-kira-theron-tier2"
}
```

Query this at conversation start to determine which tier to start the NPC in.

```python
async def get_tier(npc_name: str, player_name: str) -> int:
    """Returns current tier (1, 2, or 3) for this player-NPC pair."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{GRAPHITI_URL}/v1/graph/search",
            json={
                "query": f"tier unlock status for player {player_name} with NPC {npc_name}",
                "group_id": GROUP_ID,
                "num_results": 3
            }
        )
        facts = resp.json().get("results", [])
        tier = 1
        for f in facts:
            body = f.get("fact", "").lower()
            if "tier 3" in body:
                tier = 3
            elif "tier 2" in body and tier < 3:
                tier = 2
        return tier
```

---

## GM Memory Dashboard

Query Graphiti before each session to get a full summary of what each NPC knows:

```bash
# What does Theron know about what players have told him?
curl -X POST http://10.0.1.124:8000/v1/graph/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "All interactions and information shared with Theron Waide",
    "group_id": "price-of-dawn",
    "num_results": 20
  }' | jq '.results[].fact'
```

This is your session-prep shortcut: run before each session for every major NPC, get a narrative summary of what the players have revealed.

---

## MCP Integration (Claude Code access)

Graphiti exposes an MCP server. Add to Claude Code settings to query NPC memory directly from this conversation:

```json
{
  "mcpServers": {
    "graphiti": {
      "url": "http://10.0.1.124:8000/mcp",
      "type": "sse"
    }
  }
}
```

Then from Claude Code: query Graphiti to get NPC states before expanding a session or writing NPC dialogue.
