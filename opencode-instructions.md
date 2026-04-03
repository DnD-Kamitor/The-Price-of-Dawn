# OpenCode Content Expansion Playbook

## Mission Focus
- Prioritize new material that deepens lore, location detail, and scene-ready content; build on existing text instead of rewriting it.
- Preserve current canon and tone; every addition should feel like it has always belonged in *The Price of Dawn*.
- Treat deliverables as publication-ready: embedded prose, tables, and boxed text must slot directly into the Quarto book.
- Audio generation and image replacement are handled by other contributors—leave those pipelines untouched and focus entirely on textual/world-building expansions.

## Storycraft Principles
- Apply theGreatGM guidance in all narrative work: every scene carries clear stakes, NPCs have visible want/fear/lie axes, combats/add encounters include secondary objectives, openings lean on five senses, and beats are prepped for escalation.
- When outlining scenes, include encounter beats (hook → complication → escalation → resolution) so GMs can improvise confidently.
- Any new evocative text should open with grounded sensory detail (sound/smell/light/texture) before exposition.

## Player vs. GM Walls
- Player-facing files (`world-lore.md`, `pantheon.md`, `factions-guide.md`, `player-handout.md`, etc.) must stay spoiler-free; hide GM material inside the existing GM-only structure (`<details class="gm-only">`).
- Reserve ritual mechanics, Dawnborn secrets, and faction plots for GM chapters only (`gm-tools.md`, `sessionX.md`, `setting.md`, etc.).
- Maintain the separation already modeled in the repo—never leak Tier 3–4 `knowledge-tiers.md` content into general text.

## Format & Structure Requirements
- **Stat blocks:** follow the D&D 5e style already used in `session1.md`–`session5.md` (bold ability headers, inline traits, action lists). When uncertain, copy the exact Markdown structure from Session 1.
- **NPC writeups:** new named NPCs must use the OGAS format established in `npcs.md` (Overview, Goal, Approach, Stakes) plus bonds/relationships when relevant.
- **District/location writeups:** include a hook sentence, sensory snapshot, d6 table, and at least one player-available lead to keep the Living World system fed.
- **Discovery quests / downtime content:** keep parity with existing 3-per-session structure and explicitly tie each option to factions or Dawnborn consent positioning.

## Barrier & Skill Check Expansions
- Reference the `appendix.md` Skill Check table when setting DCs so campaign-wide difficulty stays coherent (Session 1–5 DC bands: 10–16 for most social/investigation gates, 15–17 for climax confrontations).
- Every new obstacle should be framed as a **Barrier** with: a plain-language description of what blocks progress, at least two approaches (roleplay path + skill check path), explicit failure fallout, and how it advances faction/consent clocks.
- Document Barriers inline where they trigger (sessions, locations, Living World tables) using mini tables or bullet lists so GMs can drop them directly into prep sheets.
- Skill check callouts should specify skill + DC + effect + consequence on failure. Whenever possible, add a secondary, non-roll solution (leveraging relationships, resources, or earlier clues) to keep agency high.
- When a Barrier ties to a faction or Dawnborn stance, note which tracker entry to update and what reputation threshold/ally is required to bypass the check entirely.

## Session & Encounter Content
- Expand session chapters with breathable boxed text and **room descriptions** that open on sensory detail (light, sound, temperature) before mechanics. If an area has moving parts (NPC routines, environmental hazards), list them in quick bullets beneath the read-aloud.
- For each new or revised scene, outline encounter beats (Hook → Complication → Escalation → Resolution) and identify which beats tie to the Living World trackers or Dawnborn consent tally.
- **Monster/foe notes** live directly under their encounter headers: include tactical guidance, secondary objectives, and how they react to parley. If reusing existing stat blocks, reference the source (`appendix.md` table or MM page); if adding a stat block, follow the Session 1 format and embed it at the end of the chapter.
- Room/encounter entries should end with quick-reference tables: `What They Want`, `What Fails Looks Like`, and `Tracker Impact` so GMs can see consequences at a glance.

## Asset Coordination
- Leave audio scripts, Piper runs, and image sourcing untouched unless explicitly asked; note any recommended snippets for the audio/image teams in TODO comments or the tracker rather than implementing them yourself.
- Keep the Asset Guard workflow in mind when expanding content (don't add unsupported media types), but defer the actual asset work to the dedicated pipelines.

## Workflow Reminders
- Each milestone (lore expansion, quest packet, barrier/skill-check update, etc.) should end with a clean commit/push per CLAUDE instructions; keep commits scoped to the milestone you completed.
- When adding tables or details, preserve the Quarto/Markdown conventions already present (pipe tables, `<details>` blocks, callouts) so downstream rendering stays stable.
- Document any assumptions inline when non-obvious—otherwise avoid extra commentary to keep the book clean.
