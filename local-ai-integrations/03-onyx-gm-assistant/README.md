# 03 — Onyx GM Assistant

Index all campaign markdown files into Onyx. Query them at the table in natural language.
Service: Onyx at https://onyx.research-ready.nl (CT307). RAM is at 91% — monitor.

---

## What This Enables

GM types during play:
- "What are the three-clue trails for the cipher room?"
- "What does Theron know at tier 2 that players haven't found yet?"
- "What are the faction consequences if players expose Ostenveld in session 4?"
- "Which session has the ambush mechanics for the Ashring plaza?"

Onyx returns grounded answers with source citations from the actual campaign files. No hallucination risk — it quotes the documents.

---

## Setup: Index the Campaign Files

### Option A — File connector (simplest)

Onyx supports file upload. Upload all campaign .md files directly.

1. Go to https://onyx.research-ready.nl
2. Admin > Connectors > Add Connector > File Upload
3. Upload these files (in order of GM-usefulness):

```
session1.md, session2.md, session3.md, session4.md, session5.md
npcs.md
knowledge-tiers.md
factions-guide.md
setting.md
gm-tools.md
running-the-campaign.md
world-lore.md
pantheon.md
master-plot.md
plot-overview.md
deep-archive.md
crafting-and-professions.md
appendix.md
```

Do NOT index player-facing files through the public connector — keep player-safe content separate:
- player-guide.md
- player-handout.md
- discovery-quests.md

4. Create a document set called "GM Reference" containing the GM-only files.
5. Create a document set called "Player Safe" for player-facing content.

### Option B — Gitea connector (auto-syncs with commits)

1. Admin > Connectors > Gitea
2. Repo URL: https://gitea.research-ready.nl/admin/price-of-dawn  (create this repo and push campaign files)
3. File filter: `*.md`
4. Exclude paths: `local-ai-integrations/`, `docs/`
5. Sync interval: 1 hour

This keeps Onyx current as you edit files between sessions.

---

## Persona Configuration

Create a custom Onyx persona for GM use:

Name: **GM Oracle**
Instructions:
```
You are a reference assistant for the tabletop RPG campaign "The Price of Dawn."
The GM is asking you questions during session prep or live play.
Answer from the indexed documents only. Always cite which file and section your answer comes from.
If the answer requires information from multiple files, synthesize them and list all sources.
If you cannot find the answer in the documents, say so explicitly — do not guess.
Prioritize session files (session1-5.md) for encounter mechanics.
Prioritize npcs.md for NPC behavior and secrets.
Prioritize knowledge-tiers.md for what players are allowed to know.
Keep answers concise — the GM is mid-session. Lead with the direct answer, then the source.
```

Document sets: GM Reference (all GM files)
Model: litellm/mistral-large-latest (fast) or litellm/claude-sonnet-4-6 (more nuanced)

---

## GM Query Examples

### At the table (fast queries)

```
"What's the secondary objective in the ambush encounter at the Ashring gate?"
"What does Sera know about the cipher at the start of session 3?"
"List all faction consequence triggers for session 4"
"What are the grey sickness Stage 2 symptoms?"
"What's the DC for the History check to recognize the elder futhark inscription?"
```

### Session prep (deep queries)

```
"Summarize all NPC secrets that players haven't discovered yet, by NPC"
"What are the if-they-skip fallbacks for session 2?"
"What happens to Brother Edoran's arc in sessions 4 and 5 depending on whether players sided with him?"
"List all hooks that connect the cipher game to the main plot"
"What does Theron's tier 3 content reveal that would most surprise players who've only seen tier 1?"
```

---

## Between-Sessions: Player-Facing Onyx Instance

Create a second persona for players:

Name: **Varenhold Archives**
Instructions:
```
You are the Varenhold Civic Repository's public information system.
Answer only from player-safe document sets. Never reveal GM-only content.
Respond in-world — you are an archival reference system, not an AI assistant.
If asked about something restricted (ritual mechanics, NPC secrets), respond:
"That record is sealed. Restricted access only."
```

Document sets: Player Safe only.

Players can query it between sessions for world-lore questions without exposing GM secrets.

---

## RAM Warning

Onyx (CT307) is at ~91% RAM (6GB). Under load from indexing large files, it may OOM.

Mitigation:
- Index files in small batches (5 at a time), wait for indexing to complete between batches
- If OOM: `pct exec 307 -- docker compose restart` via Proxmox console
- Monitor: https://grafana.research-ready.nl (set up Prometheus alert for CT307 RAM > 85%)
- Long-term: request RAM increase for CT307 or migrate Onyx to a dedicated container

Indexing order (smallest files first to test):
1. appendix.md (small, good test)
2. running-the-campaign.md
3. npcs.md
4. session1.md, session2.md (one at a time)
5. knowledge-tiers.md
6. Remaining sessions and large files
