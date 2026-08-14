# Local AI Integrations — Memory

## Status

| Integration | Code | Tested | Notes |
|---|---|---|---|
| 01-talking-npcs | DONE | YES | npc_client.py working end-to-end; openwebui_setup.py ready (needs admin creds) |
| 02-graphiti-npc-memory | DONE | NO | graphiti_client.py done; CT124 unreachable from outside cluster |
| 03-onyx-gm-assistant | DONE | NO | upload_to_onyx.py ready; needs ONYX_EMAIL + ONYX_PASSWORD |
| 04-comfyui-scene-art | DONE | NO | generate_scenes.py + ComfyUI workflow JSONs; needs COMFYUI_URL access |
| 05-n8n-living-world | DONE | NO | living-world-workflow.json importable to n8n; needs Gitea API token + LiteLLM key |
| 06-openedai-tts-replace | DONE | YES | ai-tools.md updated, audio/ files exist, npc_client.py uses it |
| 07-neo4j-relationship-graph | DONE | NO | init_graph.cypher + neo4j_client.py; needs NEO4J_PASSWORD |

## Working Services (confirmed)

- **Ollama local**: `localhost:11434` — qwen3:14b (primary NPC), phi4, gemma3:27b, deepseek-r1:14b, llama3.1:8b, nomic-embed-text
- **openedai-speech TTS**: `https://tts.research-ready.nl` — no auth required, mTLS not needed
  - Voices working: alloy, echo, shimmer, nova, onyx
  - Voice NOT working: fable (returns 44-byte error response — skip it)
- **mTLS cert**: auto-extracted from `~/Desktop/fedora.p12` (password: `Research-mTLS-2024!`) to `/tmp/mtls_client.crt` + `/tmp/mtls_client.key`
- **Graphiti**: `http://10.0.1.124:8000` — internal cluster only, unreachable from outside without SSH tunnel through `root@10.0.0.16`
- **LiteLLM**: `https://litellm.research-ready.nl` — needs API key (`pod-fast`, `pod-quality` aliases requested)
- **OpenWebUI**: `https://openwebui.research-ready.nl` — admin credentials unknown

## KeePass DB

- Path: `/home/chris/Nextcloud/Github/InstallLocalAiPackage/price-of-dawn-credentials.kdbx`
- Master password: env var `KEEPASS_MASTER_PASSWORD_POD` = `DndBaby100!`
- CLI: `keepassxc-cli show price-of-dawn-credentials.kdbx "PriceOfDawn/LiteLLM" --password`

## NPC Audio Files Generated (in audio/)

- theron-archive-greeting.wav, theron-reveal-knew.wav, theron-apology.wav
- sera-decision.wav, sera-marta.wav, sera-enough.wav
- lira-mira-sunlight.wav, lira-decided.wav
- edoran-annem.wav, edoran-consent.wav
- erem-return-song.wav, ostenveld-managing.wav
- tomas-decided.wav (onyx, NOT fable — fable broken)
- ysel-not-afraid.wav, ysel-sunlight-worth.wav
- narration-campaign-opener.wav

## NPC Client Usage

```bash
# Basic: chat with Theron via Ollama (no TTS)
cd local-ai-integrations/01-talking-npcs
python3 npc_client.py --npc theron-waide --player "Kira" --no-tts

# With TTS (openedai-speech):
python3 npc_client.py --npc sera-voss --player "Kira"

# With LiteLLM (faster, when API key available):
LITELLM_API_KEY=sk-xxx python3 npc_client.py --npc theron-waide --player "Kira"

# OpenWebUI setup (needs admin credentials):
OPENWEBUI_EMAIL=admin@... OPENWEBUI_PASSWORD=... python3 openwebui_setup.py
```

## All Integrations DONE — Pending Credentials/Access

To activate each integration, need:
- **03-onyx**: `ONYX_EMAIL` + `ONYX_PASSWORD` in KeePass `PriceOfDawn/Onyx`
- **04-comfyui**: ComfyUI URL accessible (test with `curl https://comfyui.research-ready.nl/system_stats`)
- **05-n8n**: import `living-world-workflow.json`, set Gitea token + LiteLLM key credentials
- **07-neo4j**: `NEO4J_PASSWORD` from KeePass `PriceOfDawn/Neo4j`, then `python3 neo4j_client.py --init`
- **01 OpenWebUI**: `OPENWEBUI_EMAIL` + `OPENWEBUI_PASSWORD`, then run `openwebui_setup.py`
- **02 Graphiti**: SSH tunnel or cluster access, then `graphiti_client.py --action health`
