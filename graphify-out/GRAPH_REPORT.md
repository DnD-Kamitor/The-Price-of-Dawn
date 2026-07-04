# Graph Report - .  (2026-07-02)

## Corpus Check
- Large corpus: 273 files · ~3,834,855 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder.

## Summary
- 162 nodes · 158 edges · 32 communities (12 shown, 20 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 14 edges (avg confidence: 0.83)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Ritual Endings & Pathways|Ritual Endings & Pathways]]
- [[_COMMUNITY_GM Framework & NPC Tools|GM Framework & NPC Tools]]
- [[_COMMUNITY_Session Props & Print Materials|Session Props & Print Materials]]
- [[_COMMUNITY_Core Concepts & World Systems|Core Concepts & World Systems]]
- [[_COMMUNITY_Campaign Tracking & AI Tools|Campaign Tracking & AI Tools]]
- [[_COMMUNITY_Campaign Overview & Setting|Campaign Overview & Setting]]
- [[_COMMUNITY_GM Philosophy & Scene Design|GM Philosophy & Scene Design]]
- [[_COMMUNITY_Clue Trail & Key Documents|Clue Trail & Key Documents]]
- [[_COMMUNITY_Ritual History & Deep Lore|Ritual History & Deep Lore]]
- [[_COMMUNITY_Pre-Made Characters|Pre-Made Characters]]
- [[_COMMUNITY_Session 0.5 & Dawnhalls|Session 0.5 & Dawnhalls]]
- [[_COMMUNITY_Archive Investigation Arc|Archive Investigation Arc]]
- [[_COMMUNITY_Player Onboarding|Player Onboarding]]
- [[_COMMUNITY_Edoran & Willing Path|Edoran & Willing Path]]
- [[_COMMUNITY_Combat & Reckoning|Combat & Reckoning]]
- [[_COMMUNITY_Economy & Skill Systems|Economy & Skill Systems]]
- [[_COMMUNITY_Running the Campaign|Running the Campaign]]
- [[_COMMUNITY_Healers Guild|Healers Guild]]
- [[_COMMUNITY_Merchants Compact|Merchants Compact]]
- [[_COMMUNITY_Morthis Worship|Morthis Worship]]
- [[_COMMUNITY_Erem & Ashfen Lore|Erem & Ashfen Lore]]
- [[_COMMUNITY_Session 0.5 NPCs|Session 0.5 NPCs]]
- [[_COMMUNITY_Maerin Voss|Maerin Voss]]
- [[_COMMUNITY_Session 0.5 NPCs|Session 0.5 NPCs]]
- [[_COMMUNITY_Chancellor Ostenveld|Chancellor Ostenveld]]
- [[_COMMUNITY_Laboratory Riddle|Laboratory Riddle]]
- [[_COMMUNITY_Resonance Rods Puzzle|Resonance Rods Puzzle]]
- [[_COMMUNITY_Primer Stones Puzzle|Primer Stones Puzzle]]
- [[_COMMUNITY_Session Recording|Session Recording]]
- [[_COMMUNITY_Varenhold Districts|Varenhold Districts]]
- [[_COMMUNITY_Graymere Reaches|Graymere Reaches]]
- [[_COMMUNITY_Varenhold City|Varenhold City]]

## God Nodes (most connected - your core abstractions)
1. `The Dawnborn` - 11 edges
2. `The Dawnborn (Lux Anchors)` - 10 edges
3. `Session 1: Into the Dark` - 7 edges
4. `The Price of Dawn` - 6 edges
5. `Ritual of Eternal Dawn` - 6 edges
6. `Ritual of Eternal Dawn` - 5 edges
7. `Dawnborn Consent Arc` - 5 edges
8. `Five Endings (A-E)` - 5 edges
9. `Characters` - 5 edges
10. `Session 2: The Weight of Light` - 5 edges

## Surprising Connections (you probably didn't know these)
- `Chancellor Mira Ostenveld` --semantically_similar_to--> `Dawnborn Consent Arc`  [INFERRED] [semantically similar]
  npcs.md → plot-overview.md
- `Piper TTS Pipeline` --semantically_similar_to--> `ElevenLabs NPC Voice Synthesis`  [INFERRED] [semantically similar]
  CLAUDE.md → ai-tools.md
- `OGAS NPC Format` --semantically_similar_to--> `theGreatGM Principles`  [INFERRED] [semantically similar]
  npcs.md → opencode-instructions.md
- `Discovery Quests` --references--> `The Dawnborn`  [INFERRED]
  discovery-quests.md → plot-overview.md
- `Lira Anwick` --implements--> `The Dawnborn`  [EXTRACTED]
  npcs.md → plot-overview.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Dawnborn-Ritual-Ashring Convergence** — concept_dawnborn, concept_ritual_of_eternal_dawn, location_ashring, concept_lux_anchor, concept_five_endings [INFERRED 1.00]
- **Antagonist-Faction-Consent Triad** — concept_three_layer_antagonists, faction_restorers, faction_reckoning, npc_chancellor_ostenveld, concept_consent_arc [INFERRED 1.00]
- **Knowledge-Tier-Revelation System** — concept_knowledge_tiers, concept_three_clue_rule, doc_deep_archive, concept_lux_anchor, doc_corven_sealed_letter [INFERRED 1.00]
- **Guy Sanders Combat-Puzzle-RP Structure Applied Across Sessions** —  [INFERRED 0.85]
- **Dawnborn-Ritual-Consent Core Campaign Engine** —  [INFERRED 0.95]
- **Three-Clue Puzzle Chain: Notation Key → Ritual Diagram → Inversion** —  [INFERRED 0.85]

## Communities (32 total, 20 thin omitted)

### Community 0 - "Ritual Endings & Pathways"
Cohesion: 0.11
Nodes (21): Five Endings (A-E), Inversion Pathway, Primer Stone, Six Endings (A-F), Three Alternative Paths, Three-Layer Antagonist Structure, Tomas Asymmetry, Transfer Method (+13 more)

### Community 1 - "GM Framework & NPC Tools"
Cohesion: 0.11
Nodes (18): GM Character Interview Framework, Living World System, OGAS System, Sera Voss, Session 1 OGAS Quick-Reference Cards, Lira Anwick, Tomas Areth, Cormac Drell (+10 more)

### Community 2 - "Session Props & Print Materials"
Cohesion: 0.14
Nodes (17): GitBook Props — Session 1, GitBook Props — Session 2, Moral Dilemma Engine, Three-Clue Rule, Gestalt Characters (Dual Class), Guy Sanders Scene Structure (Combat-Puzzle-RP), Session 1 Player Props, Session 1: Into the Dark (+9 more)

### Community 3 - "Core Concepts & World Systems"
Cohesion: 0.17
Nodes (13): Dawnborn Consent Arc, The Dawnborn, Grey Sickness, Four-Tier Knowledge System, Lux Anchor Mechanism, Three-Clue Rule, Discovery Quests, Knowledge Tiers (+5 more)

### Community 4 - "Campaign Tracking & AI Tools"
Cohesion: 0.17
Nodes (13): Dawnborn Reaction Tracker, ElevenLabs NPC Voice Synthesis, 5-Room Structure, Living World System, Moral Dilemma Scorecard, OGAS NPC Format, theGreatGM Principles, AI Tools (+5 more)

### Community 5 - "Campaign Overview & Setting"
Cohesion: 0.20
Nodes (11): The Price of Dawn, Amber Economy, Piper TTS Pipeline, Skill-Passive / Skill-Reveal System, CLAUDE.md Campaign Reference, Crafting and Professions, Factions Guide, Campaign Index (+3 more)

### Community 6 - "GM Philosophy & Scene Design"
Cohesion: 0.20
Nodes (10): Consequence Tracking, Running the Campaign — GM Philosophy, Tone Calibration (3 Levels), Jaret, Senna Kard, Six Endings Matrix (A-F), Shops — Varenhold, Campaign Tracker (+2 more)

### Community 7 - "Clue Trail & Key Documents"
Cohesion: 0.22
Nodes (10): Primer Anchor, Vault Door Sequence (Elder Futhark), Corven's Notation Key, Ritual Diagram — Inversion Pathway (Tier 3), Corven's Final Letter, Collaborative Novel Format, Corven's Notebook (Intelligence-9 Artifact), Dawnborn Consent Status Grid (+2 more)

### Community 8 - "Ritual History & Deep Lore"
Cohesion: 0.25
Nodes (9): Ritual of Eternal Dawn, Corven's Sealed Letter, Deep Archive, Training Session (Session 0.5), Ashfen, Lowmark Dawnhall, Archmagister Corven, Maerin Voss (+1 more)

### Community 9 - "Pre-Made Characters"
Cohesion: 0.33
Nodes (6): Davan Stout (Fighter), Ilessa Thorn (Wizard), Maren Ashveil (Rogue), Teor Seld (Ranger), Vella Mourne (Bard), Characters

### Community 10 - "Session 0.5 & Dawnhalls"
Cohesion: 0.40
Nodes (5): GitBook Props — Session 0.5, Props & Handouts — Session 0.5, Ilya Ren, Session 0.5: The Bell Beneath the Dawnhall, Dawnhalls

### Community 11 - "Archive Investigation Arc"
Cohesion: 0.40
Nodes (5): Theron Waide, Sealed Drawer (Shelf 4-17-3), Reckoning Guard Orders, Theron's Journal — Day 4,017, Partial Ritual Path

## Knowledge Gaps
- **70 isolated node(s):** `Grey Sickness`, `Sera Voss`, `Cormac Drell`, `Erem`, `Maerin Voss` (+65 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `The Dawnborn` connect `Core Concepts & World Systems` to `Ritual History & Deep Lore`, `Ritual Endings & Pathways`, `Campaign Overview & Setting`?**
  _High betweenness centrality (0.093) - this node is a cross-community bridge._
- **Why does `Session 5: The Price of Dawn` connect `Session Props & Print Materials` to `Archive Investigation Arc`, `Clue Trail & Key Documents`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._
- **Why does `Ritual Diagram — Inversion Pathway (Tier 3)` connect `Clue Trail & Key Documents` to `Session Props & Print Materials`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `The Dawnborn` (e.g. with `Grey Sickness` and `Discovery Quests`) actually correct?**
  _`The Dawnborn` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Grey Sickness`, `Sera Voss`, `Cormac Drell` to the rest of the system?**
  _76 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Ritual Endings & Pathways` be split into smaller, more focused modules?**
  _Cohesion score 0.10952380952380952 - nodes in this community are weakly interconnected._
- **Should `GM Framework & NPC Tools` be split into smaller, more focused modules?**
  _Cohesion score 0.1111111111111111 - nodes in this community are weakly interconnected._