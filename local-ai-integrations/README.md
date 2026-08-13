# Local AI Stack — Price of Dawn Integrations

All services run on the research-ready.nl stack (InstallLocalAiPackage).
mTLS cert required for browser access — run `bash scripts/certfix.sh` once.

## Priority Order (fun/immersion impact)

| # | Integration | Impact | Effort | Status |
|---|-------------|--------|--------|--------|
| 1 | [Talking NPCs with Voice](01-talking-npcs/README.md) | 5/5 | Medium | TODO |
| 2 | [Graphiti NPC Persistent Memory](02-graphiti-npc-memory/README.md) | 5/5 | Medium | TODO |
| 3 | [Onyx GM Assistant](03-onyx-gm-assistant/README.md) | 4/5 | Low | TODO |
| 4 | [ComfyUI Scene Art](04-comfyui-scene-art/README.md) | 4/5 | Low | TODO |
| 5 | [n8n Living World Automation](05-n8n-living-world/README.md) | 4/5 | High | TODO |
| 6 | [Replace ElevenLabs with openedai-speech](06-openedai-tts-replace/README.md) | 3/5 | Low | TODO |
| 7 | [Neo4j NPC Relationship Graph](07-neo4j-relationship-graph/README.md) | 3/5 | High | TODO |

## Service Map (quick reference)

| Service | URL | Internal IP | Purpose |
|---------|-----|-------------|---------|
| OpenWebUI | https://openwebui.research-ready.nl | 10.0.1.106 | NPC chat interface + voice |
| Whisper STT | https://whisper.research-ready.nl | 10.0.1.108:9000 | Player speech to text |
| openedai-speech TTS | https://tts.research-ready.nl | 10.0.3.101:8001 | Text to NPC voice audio |
| LiteLLM | https://litellm.research-ready.nl | 10.0.2.205 | LLM proxy (24 models) |
| Graphiti | internal only | 10.0.1.124:8000 | Temporal NPC memory (MCP) |
| Onyx | https://onyx.research-ready.nl | 10.0.3.107 | RAG search over campaign docs |
| ComfyUI | https://comfyui.research-ready.nl | 10.0.3.100 | Scene image generation |
| n8n | https://n8n.research-ready.nl | 10.0.1.104 | Workflow automation |
| Neo4j | https://neo4j.research-ready.nl | 10.0.1.114 | NPC relationship graph |
| Langfuse | https://langfuse.research-ready.nl | 10.0.1.112 | LLM call tracing + cost |
| Gitea | https://gitea.research-ready.nl | 10.0.2.200 | Campaign doc version control |

## Full Voice Pipeline Architecture

```
AT THE TABLE
============
GM laptop mic
  --> OpenWebUI voice input (Web Speech API or Whisper integration)
  --> Whisper API (CT108, port 9000) - speech-to-text
  --> LiteLLM (CT205) with NPC system prompt loaded
        - Model: mistral-large or llama3-70b (fast, low latency)
        - System prompt: NPC character file from 01-talking-npcs/npc-prompts/
        - Session context: last 10 exchanges + Graphiti memory summary
  --> openedai-speech (CT301, port 8001) - text to NPC voice audio
        - Voice: NPC-specific (see 01-talking-npcs/README.md voice table)
        - Speed: 0.95 (slightly slow = gravitas)
  --> OpenWebUI plays audio through speakers
  --> Langfuse logs full trace (model, tokens, latency, cost)
  --> Graphiti stores exchange (npc, player_name, summary, session_id)

BETWEEN SESSIONS
================
Player browser --> OpenWebUI NPC workspace (shared URL)
  --> Same pipeline minus Whisper (text input)
  --> Graphiti stores with session_id = "between-session-N"
  --> GM reviews conversation log in Langfuse before next session
      (look for: what secrets did players probe? what did they learn?)
```
