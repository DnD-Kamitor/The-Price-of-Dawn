# 01 — Talking NPCs with Voice

Players and GM speak to NPCs. NPCs respond in character, in their voice.
Uses: OpenWebUI + Whisper STT + LiteLLM + openedai-speech TTS.

---

## Voice Assignment per NPC

openedai-speech uses OpenAI-compatible voice IDs.
Standard voices: alloy, echo, fable, onyx, nova, shimmer.

| NPC | Voice | Speed | Why |
|-----|-------|-------|-----|
| Chancellor Ostenveld | onyx | 0.90 | Deep, controlled, minimal movement |
| Theron Waide | echo | 1.05 | Anxious, slightly fast, academic |
| Sera Voss | nova | 0.95 | Direct, working-class, no performance |
| Tomas Areth | fable | 0.90 | Formal, deliberate, never rushed |
| Lira Anwick | shimmer | 0.95 | Careful, clipped when guarded |
| Brother Edoran | alloy | 0.85 | Serene, unhurried, priestly cadence |
| Erem the Wadewalker | echo | 0.90 | Precise, measured, never hedges |
| Ysel Dorn | shimmer | 1.00 | Warm faith, open |

### Test a voice (curl)

```bash
curl -s https://tts.research-ready.nl/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "model": "tts-1",
    "input": "The Archive has been closed since the Desperate Winter. I would prefer you did not raise your voice in here.",
    "voice": "echo",
    "speed": 1.05
  }' \
  --output test-theron.wav && aplay test-theron.wav
```

---

## OpenWebUI Workspace Setup

One workspace per NPC. Each workspace = isolated system prompt + model config + voice settings.

### Step 1: Create a Model in OpenWebUI

1. Go to https://openwebui.research-ready.nl
2. Admin Panel > Models > Add Model
3. Settings per NPC:

```
Model ID:       npc-theron-waide
Display Name:   Theron Waide (Archivist)
Base Model:     litellm/mistral-large-latest   (fast enough for real-time)
System Prompt:  [paste from 01-talking-npcs/npc-prompts/theron-waide.md]
Temperature:    0.85
Max tokens:     300   (NPCs don't monologue — short answers force interaction)
```

4. Under Advanced > TTS:
   - Enable TTS: ON
   - TTS URL: https://tts.research-ready.nl/v1/audio/speech
   - Voice: echo (match table above)
   - Speed: 1.05

5. Repeat for each NPC.

### Step 2: Enable Whisper STT in OpenWebUI

Admin Panel > Audio:
- STT Engine: Whisper (OpenAI-compatible)
- STT URL: http://10.0.1.108:9000/v1  (internal — OpenWebUI is in same subnet)
- Model: whisper-1
- Language: en

### Step 3: Create a Workspace per NPC

Admin Panel > Workspaces > New:
- Name: "Sera Voss — Lowmark Captain"
- Default Model: npc-sera-voss
- Share: specific users (players by Authentik account) or link

Give players the workspace URL. They open it, hit the mic button, speak.

---

## Model Selection

Use LiteLLM aliases. At the table: prioritize low latency.

| Use case | Model alias | Why |
|----------|-------------|-----|
| At the table (real-time) | mistral-large-latest | ~1.5s latency, good instruction following |
| Between sessions (quality) | claude-sonnet-4-6 | Better nuance, tier system handling |
| Fallback | llama3-70b | Fully local, no rate limit |

Configure model aliases in LiteLLM at https://litellm.research-ready.nl.

---

## Latency Budget

Target: player speaks → NPC voice starts playing < 4 seconds.

| Step | Expected latency |
|------|-----------------|
| Whisper transcription | 0.5–1.0s |
| LiteLLM (mistral-large, 200 token response) | 1.0–2.0s |
| openedai-speech synthesis | 0.5–1.0s |
| OpenWebUI audio start | 0.2s |
| **Total** | **2.2–4.2s** |

If latency too high: switch model to llama3-70b (local inference, no network hop to provider).

---

## Langfuse Tracing

Every NPC exchange gets traced automatically if LiteLLM has Langfuse configured.

In Langfuse: filter by `tags = ["npc"]` to see only campaign traces.

Add tag in LiteLLM model config:
```yaml
model_list:
  - model_name: npc-theron-waide
    litellm_params:
      model: mistral/mistral-large-latest
      metadata:
        tags: ["npc", "theron-waide", "price-of-dawn"]
```

Between sessions: review traces to see what players asked NPCs, what information they probed, which secrets they got close to. Use this to adjust session prep.

---

## NPC Prompt Files

See `npc-prompts/` folder. One file per NPC. Each file contains:
- Tier 1/2/3 system prompt (from ai-tools.md, reformatted for OpenWebUI)
- Voice instructions embedded in system prompt
- Hard RULES block (never break 4th wall, tier unlock logic)
- Graphiti memory injection point (placeholder — filled at runtime)

Files:
- [theron-waide.md](npc-prompts/theron-waide.md)
- [sera-voss.md](npc-prompts/sera-voss.md)
- [lira-anwick.md](npc-prompts/lira-anwick.md)
- [erem-wadewalker.md](npc-prompts/erem-wadewalker.md)
- [brother-edoran.md](npc-prompts/brother-edoran.md)
- [tomas-areth.md](npc-prompts/tomas-areth.md)
- [chancellor-ostenveld.md](npc-prompts/chancellor-ostenveld.md)
- [ysel-dorn.md](npc-prompts/ysel-dorn.md)
