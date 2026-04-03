# The Price of Dawn - Campaign Reference

Apply theGreatGM (Graeme Sherwood / TPGtbaGGM) principles throughout: every scene has stakes, NPCs want/fear/lie, encounters have secondary objectives, five-senses scene openings, encounter beats.

---

## Current State

All 30 original milestones complete. The book is fully built and publication-ready.

### File Structure

| File | Status | Notes |
|---|---|---|
| `index.md` | Complete | Immersive prose opener; audio player embedded |
| `player-guide.md` | Complete | Full session zero: safety tools, 6 archetypes, 5 group questions, spoiler map |
| `world-lore.md` | Complete | 250-year timeline, 5 powers expanded, culture, "The Last Day Before" testimonies |
| `pantheon.md` | Complete | 6 gods with temples, worship, named priests, playing-a-cleric guidance, Auris schism detail |
| `factions-guide.md` | Complete | Public knowledge + full interaction guide (access checks, loyalty costs, point of no return) |
| `player-handout.md` | Complete | Pre-session standalone document |
| `setting.md` | Complete | 6 districts (sensory + locations + d6 + hook), ritual deep mechanics, faction internals, grey sickness 3-stage |
| `npcs.md` | Complete | All 10 Dawnborn OGAS + 8 supporting NPCs + relationship web table |
| `trade.md` | Complete | Currency, prices, amber workshops, black market, trade routes |
| `session1.md`–`session5.md` | Complete | All fully expanded with pacing, puzzles, riddles, combat, stat blocks; session5 has 6 epilogues |
| `running-the-campaign.md` | Complete | GM philosophy + VTT/one-shot/3-session adaptations, player types, tone calibration |
| `ai-tools.md` | Complete | Three-tier AI character prompts for all 8 major NPCs |
| `gm-tools.md` | Complete | Session prep cards, district d10 tables, Living World system, theGreatGM methods |
| `deep-archive.md` | Complete | 10 historical docs, 6 Corven docs, 6 NPC journals, 8 unsent letters, 5 Ashfen oral histories, 3 essays |
| `discovery-quests.md` | Complete | Between-session player quests (3 per session × 5 sessions) |
| `session-recording.md` | Complete | Session-to-book guide, Corven's Notebook artifact, character grounding exercises |
| `knowledge-tiers.md` | Complete | 4-tier information system for 8 topics; Tier 3-4 contains campaign secrets |
| `crafting-and-professions.md` | Complete | 5 professions with full tables; background knowledge auto-unlocks |
| `appendix.md` | Complete | Quick reference: DCs, NPC roster, stat block index, price table, ritual reference |
| `images/` | Complete | SVG placeholders replaced with PNG art per GENERATE-THESE.md prompts |
| `audio/` | In progress | TTS via piper-sample-generator; opener + Graymere overview + Twilight City narration |

---

## Execution Notes

- Commit and push after each milestone
- Preserve all existing content; these are expansions, not rewrites
- All GM-only content (ritual mechanics, NPC secrets, faction plots) stays in GM chapters
- Player-facing chapters (world-lore, pantheon, factions-guide, player-handout) get no spoilers
- Apply theGreatGM principles: stakes in every scene, NPCs with want/fear/lie, secondary objectives in all combats, five-senses openings, encounter beats
- When adding stat blocks, use D&D 5e format matching sessions 1-4
- When adding named NPCs, use OGAS format matching npcs.md
- Asset Guard workflow runs `python3 .github/scripts/check_assets.py` on CI to enforce PNG-only art in `images/` + `docs/images/` and WAV-only audio in `audio/`

---

## Audio Generation with Piper

The campaign book supports embedded audio via piper-sample-generator. Audio files live in `audio/` (project root) and are automatically copied to `docs/audio/` on `quarto render` via the `resources` entry in `_quarto.yml`.

### Tool Location

```
/home/chris/Documents/Projects/piper-sample-generator/
```

Available voices (all in `voices/`):
- `en_US-danny-low.onnx` — **Preferred for this campaign.** Deepest available male voice. Use for atmospheric narration and serious read-alouds.
- `en_US-ryan-high.onnx` — Deep American male, high quality. Slight rasp reads as older; use for elder narrators.
- `en_US-lessac-medium.onnx` — American female voice, medium quality. Lighter tone.
- `models/en-us-libritts-high.pt` — Multi-speaker PyTorch model, supports speaker blending. Requires more memory.

### Quick Start

```bash
cd /home/chris/Documents/Projects/piper-sample-generator
source .venv/bin/activate

python3 generate_samples.py "Your text here." \
  --model voices/en_US-danny-low.onnx \
  --max-samples 1 \
  --length-scales 1.4 \
  --output-dir /home/chris/Documents/Projects/visualization-curriculum/audio/
```

Output: `audio/0.wav` (22050 Hz, 16-bit mono). Rename immediately to something descriptive.

### Repository Helper

Inside this repo, `tools/generate_audio.py` wraps the command above and automatically writes to `audio/`:

```bash
python3 tools/generate_audio.py \
  --text-file audio/scripts/world-lore-page1.txt \
  --output-name world-lore-page1.wav
```

Set `PIPER_ROOT` or `PIPER_VOICE` env vars to override defaults.

### Key Arguments

| Argument | What it does |
|---|---|
| `--max-samples N` | How many wav files to generate (cycles through variation parameters) |
| `--length-scales 0.75 1.0 1.25` | Speaking speed: <1 faster, >1 slower; use 1.4 with danny for maximum gravitas |
| `--noise-scales 0.667 0.9` | Voice variability; default 0.667 |
| `--model path` | Use `.onnx` for single voice, `.pt` for multi-speaker generator |
| `--output-dir path` | Where to write wav files (always use absolute path to `audio/`) |

### Naming Convention

Pattern: `[location-or-npc]-[brief-description].wav`

Examples:
- `opening-line.wav` — campaign opener read-aloud
- `session1-archive-opening.wav` — Session 1 five-senses opener
- `sera-voss-intro.wav` — Sera's first appearance read-aloud
- `ashring-plaza-description.wav` — atmospheric location description

### Embedding in Markdown

```html
<audio controls style="width:100%;margin:0.5em 0 1.5em 0;">
  <source src="audio/filename.wav" type="audio/wav">
</audio>
```

The `src` path is always relative to the document root (`audio/filename.wav`). Works correctly across all chapters.

### What to Record

- **Campaign & history narration** — player-safe primers for chapters like `index.md`, `world-lore.md`, and `setting.md`
- **Five-senses scene openers** at the start of each session (GMs can play these to open the scene)
- **Key NPC introductions** — the first sentence a major NPC speaks
- **Read-aloud passages** — any text marked as GM read-aloud to players
- **Atmospheric location descriptions** — the Ashring plaza, the Lowmark Healing House, the Archive

Do not record: GM-only content, mechanical rules text, or anything containing campaign secrets (audio files are served in the public `docs/` directory — treat them as player-visible at all times).
