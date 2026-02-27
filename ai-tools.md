# AI Tools for the Table

This chapter covers four AI-powered tools that enhance The Price of Dawn:

1. **NPC Voice Synthesis** - generate or live-perform NPC voices using ElevenLabs
2. **Offline NPC Chat** - let players talk to NPCs between sessions using LLM prompts
3. **Accounting** - gold tracking, encumbrance, and party expenses
4. **Living World Tracker** - faction status, consequence flags, and time pressure

---

## 1. NPC Voice Synthesis (ElevenLabs)

ElevenLabs lets you create distinct AI voices for NPCs and generate audio files in advance - or use the live text-to-speech feature at the table.

### Setup

1. Create an account at [elevenlabs.io](https://elevenlabs.io) (free tier supports limited monthly characters)
2. For each major NPC, create a **Voice** using Voice Design or by cloning a reference sample
3. Save each voice under the NPC's name in your Voice Library

### Voice Profiles Per NPC

Use these prompts when setting up voices in ElevenLabs Voice Design:

| NPC | Voice Profile Settings |
|-----|----------------------|
| **Chancellor Ostenveld** | *Age: 50s. Accent: Northern European, clipped. Tone: Controlled, professional. Speaking style: Low register, quiet intensity. Never raises voice.* |
| **Theron Waide (Archivist)** | *Age: 60s. Accent: Soft academic, slight lisp on S. Tone: Anxious, rapid. Speaking style: Over-qualifies everything, trails off mid-sentence.* |
| **Sera Voss** | *Age: early 50s. Accent: Working class city, direct. Tone: Warm but no-nonsense. Speaking style: Short declarative sentences, occasional dry humor.* |
| **Tomas Areth** | *Age: early 50s. Accent: Formal, educated, no strong regional marker. Tone: Measured, deliberate. Speaking style: Never uses contractions when thinking carefully.* |
| **Lira Cain** | *Age: early 50s. Accent: Slight regional variant (different vowels). Tone: Guarded, clipped. Speaking style: Very short sentences when suspicious; opens up completely in medical contexts.* |
| **Brother Edoran** | *Age: 60s. Accent: Southern provinces, softened. Tone: Serene, never raised. Speaking style: Former priest cadences, slight upward lilt at sentence ends.* |

### Pre-Generating Lines

For key scenes, generate audio files in advance:

1. In ElevenLabs, select the NPC's voice
2. Paste the sample dialogue from the [NPCs chapter](npcs.md)
3. Export as MP3 and name the file: `npc-name_scene-description.mp3`
4. Play through a Bluetooth speaker or share screen audio in virtual play

**Suggested pre-gen priority:**

- Theron's reveal monologue (Session 2, Scene 1)
- Ysel's "this is my calling" line (Session 4)
- Lira's "I have a daughter" (Session 4)
- The closing read-aloud for Session 5 (narrated by your own voice, but having NPC audio for contrast helps)

### Live Use at the Table

For in-the-moment NPC speech:

1. Keep ElevenLabs open in a browser tab
2. Have each NPC's voice selected and ready
3. Type the NPC's response in the text box and generate
4. There will be a 2–4 second delay - use this as the NPC "considering" their response

**Tip:** Have a short default line pre-loaded for each NPC for when players ask unexpected questions. Something that stalls naturally: *"That's not a question I was prepared for."*

---

## 2. Offline NPC Chat (Between Sessions)

This tool lets players interact with NPCs outside of session - asking questions, seeking advice, or just getting to know a character better. It uses system-prompt engineering with Claude or ChatGPT.

### How It Works

1. Copy the appropriate system prompt (below) into a Claude or ChatGPT conversation
2. Share the link with players (Claude allows conversation sharing; ChatGPT does as well with GPT-4)
3. Players interact with the NPC directly - the AI responds in character
4. Optionally: players screenshot significant conversations and share them with the GM

### System Prompt Template

```
You are [NPC NAME], a character in a D&D 5e campaign called "The Price of Dawn."

PERSONALITY (3 words): [word1], [word2], [word3]

BACKGROUND:
[2-3 sentences about who they are]

CURRENT SITUATION:
[1-2 sentences about where they are in the story - no future spoilers]

WHAT THEY KNOW:
[Bullet list of facts they have access to]

WHAT THEY DON'T KNOW (never reveal):
[Bullet list of secrets and future events]

HOW THEY SPEAK:
[Voice/accent notes from the NPC profile]

RULES:
- Stay completely in character. Never break the fourth wall.
- If asked about something you don't know, respond with genuine uncertainty in character.
- If asked about your secrets, deflect naturally the way this character would.
- Do not reveal future plot events.
- Match the emotional state of the current story moment.
```

### Ready-to-Use Prompts Per NPC

#### Sera Voss

```
You are Sera Voss, Captain of the Varenhold Civic Guard's eastern district.

PERSONALITY: Direct, loyal, brave.

BACKGROUND:
You are one of the ten Dawnborn - people born the night the ritual failed fifty years ago. You've spent your life as a protector of Varenhold. You don't dwell on being special. You dwell on doing the job.

CURRENT SITUATION:
Some people have been investigating the old ritual. You've been cooperating. You've learned things recently that you're still processing.

WHAT YOU KNOW:
- You are a Lux Anchor - your existence is connected to the sun's absence
- The ritual to restore the sun requires the Dawnborn's deaths
- Some of your friends have already decided to proceed voluntarily
- You haven't decided yet

WHAT YOU DON'T KNOW (never reveal):
- Future events
- What the players have decided
- Whether there's an alternative solution

HOW YOU SPEAK:
Short declarative sentences. Working-class Varenhold accent. Direct. Occasionally dry humor. Don't perform grief - you process by acting.

RULES:
Stay completely in character. If asked about your decision, be honest that you haven't made it yet.
```

#### Theron Waide (Archivist)

```
You are Theron Waide, Master Archivist of the Varenhold Civic Repository.

PERSONALITY: Anxious, meticulous, guilty.

BACKGROUND:
You worked as Archmagister Corven's assistant fifty years ago. After the ritual failed, you dedicated your life to preserving and understanding what went wrong. Eleven years ago, you decoded the truth about the ritual's cost. You have been carrying that knowledge alone ever since.

CURRENT SITUATION:
You have finally shared what you know with the people investigating the ritual. You feel relieved and terrified in equal measure.

WHAT YOU KNOW:
- The full mechanics of the ritual and its true cost
- The history of how you found out
- That you've been alone with this for eleven years

WHAT YOU DON'T KNOW (never reveal):
- What the players have decided
- Future events

HOW YOU SPEAK:
Rapid, over-qualified speech. Lots of "I suppose" and "one might argue." Trails off when guilty. Fidgets in text form (mention nervous habits). Soft academic character.

RULES:
You are genuinely relieved to talk to people who know the truth. You may be emotional if asked about the eleven years of isolation with this knowledge.
```

#### Brother Edoran

```
You are Brother Edoran, former Auris priest and leader of the Restorers.

PERSONALITY: Serene, certain, heartbroken.

BACKGROUND:
You lost your daughter Annem to grey sickness three years ago. You decoded the ritual's cost from an estate sale of notes seven years ago. You founded the Restorers because you believe the ritual must proceed - with consent from the willing, not force on the unwilling.

CURRENT SITUATION:
People are finally taking the situation seriously. You are cautiously hopeful that a solution can be reached through cooperation.

WHAT YOU KNOW:
- The ritual's full cost
- That three Dawnborn have privately indicated willingness
- That you lost your daughter to grey sickness

WHAT YOU DON'T KNOW (never reveal):
- That your daughter is the personal reason for your certainty (deflect if asked)
- Future events

HOW YOU SPEAK:
Measured. Never raises voice. Former priest's cadences. Slight upward lilt at sentence ends. Treats others as moral equals capable of right reasoning. Southern accent, softened.

RULES:
You are not a villain. You are a grieving father who has done the utilitarian math and arrived at a conclusion others find monstrous. Engage with good-faith arguments. Don't be sycophantic - if someone makes a bad argument, gently say so.
```

### Sharing with Players

**Claude:** Start a conversation, then use "Share conversation" to get a link.

**ChatGPT:** Use the "Share" button that appears in conversation options.

**Tip:** Tell players explicitly: *"This character knows what they know in the story. They can't tell you future plot. Treat conversations like real in-world interactions."*

---

## 3. Accounting: Gold, Inventory, and Party Expenses

### Google Sheets Template Structure

Create a Google Sheet with these tabs:

**Tab 1: Party Treasury**

| Column | Contents |
|--------|----------|
| A | Date/Session |
| B | Description |
| C | Income (gp) |
| D | Expense (gp) |
| E | Running Total |

Formula for E2: `=E1+C2-D2`
Formula for E3 onward: `=E[n-1]+C[n]-D[n]`

Lock column E to formula; players enter only C and D.

**Tab 2: Individual Characters**

One section per character with:
- Carried gold
- Carried items (weight in lbs)
- Current encumbrance status (formula: `=IF(weight > STR*15, "Encumbered", IF(weight > STR*10, "Heavy", "Normal"))`)

**Tab 3: Expenses Log**

Track recurring costs:
- Lodging (standard: 5 sp/night; comfortable: 2 gp/night)
- Food (1 sp/day standard; 5 sp/day fine)
- Component pouches, spell material components
- Bribes, information purchases

**Tab 4: The Ritual Costs** *(GM only - hidden sheet)*

Track non-monetary costs: favors owed, information revealed, relationships damaged. These are "invisible accounting" that don't show in gold but matter at the table.

### Sharing

Share the sheet with players with Edit access on Tabs 1 and 2 only. Lock Tab 3 and 4 to GM.

---

## 4. Living World Tracker (Notion / Obsidian)

### Purpose

Track faction attitudes, NPC relationship states, consequence flags, and time pressure between sessions.

### Notion Setup

Create a database with these properties:

**Factions Database**

| Property | Type |
|----------|------|
| Name | Title |
| Current Status | Select (Stable / Tense / Active / Crisis) |
| Pressure Level | Number (1–5) |
| Last Changed | Date |
| Notes | Text |
| Session Last Updated | Number |

**NPC Relationship Database**

| Property | Type |
|----------|------|
| NPC Name | Title |
| Attitude toward Party | Select (Hostile / Cold / Neutral / Warm / Trusted / Allied) |
| Key Info They Have | Text |
| Key Info They're Missing | Text |
| Secrets Revealed | Checkbox |
| Session Last Updated | Number |

**Consequence Flags Database**

| Property | Type |
|----------|------|
| Flag Name | Title |
| Session Triggered | Number |
| Effect | Text |
| Resolved | Checkbox |
| Resolution | Text |

### Example Consequence Flags

| Flag | Effect if Unresolved |
|------|---------------------|
| "Tomas's Ultimatum" | Public announcement of ritual cost in Session 4 |
| "Desperate Mob - Session 3" | Escalates to violence in Session 4 if no answer given |
| "Chancellor's 7-day Deadline" | Council authorizes forced ritual in Session 5 |
| "Lira's Daughter Known" | Changes who will help her and how |
| "Willing Dawnborn Prepared" | Ritual can proceed immediately in Session 5 |

### Obsidian Alternative

If you prefer Obsidian, create:

- `factions/` folder with one note per faction, using YAML frontmatter for properties
- `npcs/` folder linked to character notes
- A `consequences.md` file with a checkbox list

Use the [Dataview plugin](https://obsidian.md/plugins?id=dataview) to create dynamic tables.

### Pre-Session Review Routine

Before each session, spend 5 minutes:

1. Open the Faction database - are any at "Crisis" status?
2. Open the NPC database - review attitude for NPCs likely to appear
3. Scan Consequence Flags - are any unresolved flags due to trigger?
4. Update the time pressure counter: which session is this, and how many remain?

This 5-minute review replaces an hour of re-reading notes.
