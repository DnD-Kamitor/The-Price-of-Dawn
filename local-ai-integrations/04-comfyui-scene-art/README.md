# 04 — ComfyUI Scene Art Generation

Generate atmospheric scene images from five-senses descriptions. Pre-gen before sessions or improvise at the table.
Service: ComfyUI at https://comfyui.research-ready.nl (CT300, GPU node).

---

## Use Cases

**Pre-session (recommended):** Generate art for all session scenes, load into a folder, display as players enter each scene.

**At the table:** GM improvises a location, types the five-senses description into ComfyUI, image ready within 30-60 seconds. Display while doing recap.

**Player-discovered locations:** Players describe a place they're searching. Generate it. Show it. No other tool does this.

---

## Style Prompt Template

Use this as the positive prompt prefix for all campaign images. Establishes visual tone consistency across all generated art.

```
[SCENE DESCRIPTION HERE],
dark fantasy illustration, twilight atmosphere, perpetual dusk, amber light from lanterns,
muted colors with amber and ochre accents, historical architecture Northern European,
painterly style, detailed, cinematic composition, no sun visible in sky,
atmospheric depth, fog and shadow, candles and lamplight as primary light sources
```

Negative prompt (use for all):
```
bright daylight, sunshine, blue sky, modern elements, anime style, cartoon,
oversaturated colors, photorealistic photography, watermark, signature,
futuristic elements, fantasy tropes (dragons, elves visible)
```

---

## Per-Session Scene Prompts

### Session 1 — The Archive

**Scene 1: Archive exterior at dusk**
```
Varenhold civic archive building, stone facade, tall arched windows with amber candlelight within,
evening twilight sky with no sun, cobblestone plaza, few people passing, lanterns on iron posts,
[style template]
```

**Scene 2: Inside the archive stacks**
```
Interior of ancient library archive, tall wooden shelving units disappearing into darkness above,
single archivist figure with a lamp walking between shelves, dust motes in amber light,
rows of numbered boxes and leather-bound registers, stone floor, cold atmosphere,
[style template]
```

**Scene 3: Shelf 4-17-3 — the sealed documents**
```
Close view of old wooden archive shelf, a small locked metal box among paper files,
dust disturbed, candlelight casting long shadows, fingers reaching toward the box,
sense of long concealment, discovery moment, [style template]
```

### Session 2 — Lowmark District

**Scene 1: Dawnhall exterior at morning**
```
Large communal hall exterior, stone building with a carved sunrise relief above the door (faded),
people gathering outside carrying food and supplies, amber lamplight at windows,
working-class district street, fog at ground level, [style template]
```

**Scene 2: Cipher room discovery**
```
Hidden basement room, stone walls with carved runes and symbols, a ritual circle inlaid in floor,
candle stubs everywhere long burned out, dust, silence, discovered after long hiding,
single lantern brought by investigators illuminating the carvings, [style template]
```

**Scene 3: Sera Voss in the Lowmark patrol**
```
Guard captain figure in patrol coat standing at district gate at night, amber street lanterns,
working-class street beyond, figure is watchful but relaxed, weight of long duty on shoulders,
[style template]
```

### Session 3 — The Ashfen Marshes

**Scene 1: Ashfen approach**
```
Travellers on a raised causeway through marshland, water on both sides, reed beds, grey-green fog,
no sun, diffuse ambient twilight light, distant wayshrine visible, isolation and silence,
[style template]
```

**Scene 2: Saltgrass Clan camp**
```
Ashfen marsh encampment, low tents and reed shelters, firelight at center, clan members working,
surrounded by marsh, a Wadewalker elder figure standing at edge looking outward,
practical, sustainable, long-inhabited, [style template]
```

**Scene 3: The stone circle (Ashring)**
```
Ancient stone circle in moorland, large standing stones with amber lichen, twilight sky,
ritual marks visible on stone surfaces, empty circle, sense of waiting, [style template]
```

### Session 4 — The Dawnborn Decisions

**Scene 1: Lira's healing room**
```
Small healing practice room, shelves of medicinal supplies, examination table, candle lamp,
healer figure near window looking out at the city, a child's small shoe visible on a shelf,
medical competence and personal weight, [style template]
```

**Scene 2: The Restorers' meeting**
```
Candlelit meeting room, circle of seated figures in plain clothes, one standing figure addressing them,
former priest bearing, maps and documents on a table, serious purpose, not threatening,
underground gathering but lawful in intent, [style template]
```

### Session 5 — The Ritual

**Scene 1: The ritual site at Ashring**
```
Stone circle at night prepared for ritual, candles placed at each stone, ten standing figures
in positions around the circle, Ashfen clan surrounding as witnesses, no audience beyond that,
weight of ceremony, amber candlelight, [style template]
```

**Scene 2: The moment of return**
```
Single shaft of warm gold light breaking through clouds for first time in fifty years,
figures shielding eyes, stone circle illuminated, fog burning off, first sunrise in a generation,
overwhelming warmth and light contrast against the long darkness, [style template]
```

---

## ComfyUI Workflow Setup

### Recommended workflow: SDXL + ControlNet

1. Load a SDXL base model (if not already in ComfyUI model folder)
2. Recommended models for this style:
   - DreamShaper XL (painterly, atmospheric)
   - Juggernaut XL (detailed architecture)
3. Steps: 30-40
4. CFG: 7-8
5. Sampler: DPM++ 2M Karras
6. Resolution: 1024x768 (landscape) or 768x1024 (portrait/NPC)
7. Seed: save seeds of good results for consistency per location

### NPC Portrait Workflow

For NPC portraits, add to prompt:
```
portrait of [character description], upper body, facing viewer,
character study, detailed face, [NPC-specific descriptors],
[style template without scene description]
```

NPC-specific descriptors:
- Theron Waide: "elderly scholar, 70s, thin, anxious expression, archival dust on clothing, wire-rimmed glasses, lamp in hand"
- Sera Voss: "50s woman, guard captain, direct gaze, practical uniform, weathered but not harsh, short grey-brown hair"
- Brother Edoran: "68 years old male, former priest bearing, calm eyes, simple robes, slightly southern features, hands folded"
- Lira Anwick: "50s woman healer, capable hands, guarded expression warming slightly, medical apron, tired but present"
- Chancellor Ostenveld: "57 years old male, formal administrator, controlled expression, quality clothing without ostentation, northern European features, exhausted behind the eyes"

### API Access (for automation)

ComfyUI has a REST API. Automate pre-gen before sessions:

```bash
# POST to ComfyUI API to queue a prompt
curl -X POST https://comfyui.research-ready.nl/prompt \
  -H "Content-Type: application/json" \
  -d @workflow.json

# Check queue status
curl https://comfyui.research-ready.nl/queue

# Download result
curl https://comfyui.research-ready.nl/history/{prompt_id}
```

Save workflow JSON files to `local-ai-integrations/04-comfyui-scene-art/workflows/` as you build them.

---

## File Naming Convention

Match existing campaign image convention:
```
session1-archive-exterior.png
session1-archive-stacks.png
session2-dawnhall-exterior.png
session3-ashfen-approach.png
session5-ritual-site.png
npc-portrait-sera-voss.png
npc-portrait-theron-waide.png
```

Drop into `images/` folder in campaign repo. Asset guard enforces PNG format — ComfyUI outputs PNG by default.
