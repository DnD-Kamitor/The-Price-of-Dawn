# 06 — Replace ElevenLabs with openedai-speech

ai-tools.md currently points to ElevenLabs (external, rate-limited, costs money after free tier).
Replace with openedai-speech at https://tts.research-ready.nl (CT301, always on, no cost, no rate limit).

---

## API Compatibility

openedai-speech is OpenAI TTS API-compatible. Any tool that works with OpenAI's TTS works with this.

**OpenAI endpoint:**
```
POST https://api.openai.com/v1/audio/speech
Authorization: Bearer {openai_key}
```

**Local replacement:**
```
POST https://tts.research-ready.nl/v1/audio/speech
Authorization: Bearer none-required   (or omit header entirely)
```

Drop-in replacement for any existing OpenAI TTS integration.

---

## Voice Reference

Standard OpenAI-compatible voices available:

| Voice ID | Character | Good for |
|----------|-----------|---------|
| alloy | Neutral, slightly warm | Narration, read-alouds, world events |
| echo | Male, medium register | NPCs: Theron Waide, Erem |
| fable | British male, slight formality | NPCs: Tomas Areth |
| onyx | Deep male | NPCs: Chancellor Ostenveld, atmospheric narration |
| nova | Female, direct | NPCs: Sera Voss, Lira Anwick |
| shimmer | Female, slightly warmer | NPCs: Lira Anwick (alternative), Ysel Dorn |

openedai-speech also supports additional voices depending on the backend model configured. Check:
```bash
curl https://tts.research-ready.nl/v1/audio/voices
```

---

## Generate Campaign Audio Files

Replace piper for audio file generation. Same quality or better, always accessible.

### Direct curl (single file)

```bash
# Generate Theron's reveal monologue opener
curl -s https://tts.research-ready.nl/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "model": "tts-1-hd",
    "input": "I found them in Year Forty-Two. I decoded what they meant over three months. I have known since then. I chose — I told myself I was protecting people from a decision they were not ready to make. I understand now that the explanation is insufficient.",
    "voice": "echo",
    "speed": 0.95
  }' \
  --output audio/theron-reveal-monologue.wav
```

### Batch generation script

Save as `tools/generate_npc_audio.sh`:

```bash
#!/usr/bin/env bash
# Generate pre-session NPC lines using openedai-speech

TTS_URL="https://tts.research-ready.nl/v1/audio/speech"
AUDIO_DIR="audio"

generate() {
  local name="$1"
  local voice="$2"
  local speed="$3"
  local text="$4"
  local outfile="$5"

  echo "Generating: $outfile"
  curl -s "$TTS_URL" \
    -H "Content-Type: application/json" \
    -d "{\"model\": \"tts-1-hd\", \"input\": $(echo "$text" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().strip()))'), \"voice\": \"$voice\", \"speed\": $speed}" \
    --output "$AUDIO_DIR/$outfile"
  sleep 0.5  # avoid hammering the API
}

# Theron Waide — key lines
generate "theron" "echo" "1.0" \
  "The Archive has been closed since the Desperate Winter. I would prefer you did not raise your voice in here." \
  "theron-archive-closed.wav"

generate "theron" "echo" "0.9" \
  "I found them in Year Forty-Two. I have known since then. I am sorry I was afraid." \
  "theron-reveal-apology.wav"

# Sera Voss — key lines
generate "sera" "nova" "0.95" \
  "I'm going to say yes. I've known since the spring." \
  "sera-decision-reveal.wav"

generate "sera" "nova" "1.0" \
  "She wanted to be a scholar. I tried to teach her the district patrol route so she'd have something practical. She was terrible at it. She'd stop to look at things." \
  "sera-marta-memory.wav"

# Lira Anwick — key lines
generate "lira" "shimmer" "0.95" \
  "Mira won't remember me clearly. She might not remember me at all. She'll have photographs. She'll have Sevra. She'll have sunlight. That last one is the thing. The last one is why." \
  "lira-mira-sunlight.wav"

# Brother Edoran — key lines
generate "edoran" "alloy" "0.85" \
  "My daughter died of grey sickness six years ago. She was seventeen. Her name was Annem." \
  "edoran-annem-reveal.wav"

# Erem — key lines
generate "erem" "echo" "0.90" \
  "The Clans will attend the ritual if you want witnesses. We will sing the Return Song. We have been practicing it every year so we would not forget. We thought someone would ask, eventually. We kept time." \
  "erem-return-song-offer.wav"

# Atmospheric narration (danny voice not available — use onyx as substitute)
generate "narration" "onyx" "0.85" \
  "Fifty years since the last sunrise. The amber lanterns of Varenhold have burned every hour of every day since. The people who were born that night are still alive. They are fifty years old now. They are the only reason the sun has not returned." \
  "narration-campaign-opener.wav"

echo "Done. Files in $AUDIO_DIR/"
```

```bash
chmod +x tools/generate_npc_audio.sh
bash tools/generate_npc_audio.sh
```

---

## Update ai-tools.md

When ready, update Section 1 of ai-tools.md:

**Find:** all references to `elevenlabs.io`
**Replace with:** `tts.research-ready.nl`

**Find:** step "Create an account at elevenlabs.io (free tier supports limited monthly characters)"
**Replace with:**
```
Use the local TTS service at https://tts.research-ready.nl — no account needed, no rate limits.
API is OpenAI TTS-compatible. See local-ai-integrations/06-openedai-tts-replace/README.md.
```

**Voice Profile table** — add a "Voice ID" column mapping each NPC to the openedai-speech voice ID from the table above.

---

## Quality Comparison

| Aspect | ElevenLabs free | openedai-speech (local) |
|--------|-----------------|------------------------|
| Rate limit | 10,000 chars/month | None |
| Latency | ~1-3s (network) | ~0.5-1s (local network) |
| Voice variety | Many custom | 6 standard |
| Custom voice cloning | Yes | Depends on backend model |
| Cost | Paid after free tier | Free (infrastructure already running) |
| Availability | External dependency | Always on |

The voice variety limitation is the main tradeoff. openedai-speech's 6 voices are enough for 8 NPCs with distinct enough differentiation. If custom voice cloning is wanted later, the backend model can be swapped.
