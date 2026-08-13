# 05 — n8n Living World Automation

After each session, n8n reads what happened and generates: NPC reactions, faction attitude shifts, world events. Zero GM prep time for the "world keeps moving" layer.
Service: n8n at https://n8n.research-ready.nl (CT104).

---

## What This Automates

The Living World system in `gm-tools.md` is currently manual GM work between sessions:
- Which NPCs heard about what players did?
- How do factions shift based on session events?
- What minor world events happen between sessions?

This workflow does the mechanical part. GM still decides whether to use the outputs.

---

## Trigger Options

### Option A: Gitea webhook (recommended)

When the GM commits session notes to Gitea, the workflow triggers automatically.

Gitea webhook setup:
1. Gitea repo settings > Webhooks > Add webhook
2. URL: `https://n8n.research-ready.nl/webhook/living-world-trigger`
3. Events: Push
4. Branch filter: `master`
5. Content type: JSON

The webhook payload includes the commit diff — n8n reads what changed.

### Option B: Manual trigger

GM opens n8n, clicks "Execute Workflow" after session. Simpler to set up.

---

## Workflow Architecture

```
[Gitea Webhook] or [Manual Trigger]
        |
        v
[HTTP Request: Get session diff from Gitea]
  GET https://gitea.research-ready.nl/api/v1/repos/admin/price-of-dawn/git/commits/{sha}
  Header: Authorization: token {gitea_api_token}
        |
        v
[Code node: Extract session summary from diff]
  - Parse which session file changed
  - Extract new content (+ lines from diff)
  - Summarize as "events this session" (bullet list)
        |
        v
[LiteLLM: Generate NPC reactions]
  POST https://litellm.research-ready.nl/v1/chat/completions
  Model: mistral-large-latest
  System prompt: [see NPC reaction prompt below]
  User: session events bullet list
        |
        v
[LiteLLM: Generate faction shifts]
  Same endpoint, different system prompt
        |
        v
[LiteLLM: Generate world events]
  Minor background events (weather, economics, rumor, street-level)
        |
        v
[Code node: Assemble markdown document]
  Title: Living World Report — Session N
  Sections: NPC Reactions | Faction Shifts | World Events | GM Notes
        |
        v
[HTTP Request: Commit to Gitea]
  POST new file: session-N-living-world.md
        |
        v
[Langfuse: Log the workflow run]
  Trace all LLM calls, tokens, cost
```

---

## System Prompts

### NPC Reaction Prompt

```
You are generating GM notes for a D&D 5e campaign called "The Price of Dawn."

CAMPAIGN CONTEXT:
Ten people (the Dawnborn) were born the night a ritual failed 50 years ago, keeping the sun from rising. The ritual to restore the sun requires their deaths. The party is investigating this. Key NPCs: Theron Waide (archivist, guilty), Sera Voss (guard captain, decided yes), Lira Anwick (healer, has young daughter, decided yes quietly), Brother Edoran (Restorers founder, lost daughter to grey sickness), Chancellor Ostenveld (administrator, managing information), Erem the Wadewalker (Ashfen clan, knows oral history), Tomas Areth (former Spire researcher, methodical).

SESSION EVENTS (bullet list follows):
{session_events}

TASK:
For each major NPC listed above, write 2-4 sentences describing:
1. What they heard about or observed from the session events
2. How they emotionally or practically react (consistent with their personality)
3. Any action they take before the next session

Format:
## [NPC Name]
[Reaction paragraph]
**Before next session:** [specific action or decision]

Constraints:
- Each NPC only knows what they could realistically have heard about
- NPCs do NOT learn secrets they have no access to
- Actions must be plausible within their role and personality
- Do not resolve campaign plot points — create texture, not resolution
```

### Faction Shift Prompt

```
You are generating faction attitude updates for a D&D 5e campaign called "The Price of Dawn."

FACTIONS:
- The Civic Council (power: governance; care about: stability, political control)
- The Arcane Spire (power: knowledge; care about: research legitimacy, information control)
- The Restorers (power: public sympathy; care about: the ritual proceeding with consent)
- The Grey Market (power: trade networks; care about: profit, information as currency)
- The Ashfen Clans (power: oral knowledge, ritual participation; care about: consent, proper process)

SESSION EVENTS:
{session_events}

TASK:
For each faction, note:
1. Attitude change (if any): toward the party, toward each other, toward the ritual question
2. What they did in response to session events
3. What they're positioning for next

Format:
## [Faction Name]
**Attitude shift:** [brief]
**Response:** [what they did]
**Positioning:** [what they're preparing]

Keep each section to 3-5 sentences. Be specific. Avoid vague "they're watching carefully" language.
```

### World Events Prompt

```
Generate 4-6 minor world events that happen in Varenhold between sessions.
These are background texture — not plot-relevant, but they make the world feel alive.

SESSION EVENTS (for context):
{session_events}

WORLD STATE:
- It has been dark (twilight, no sunrise) for 50 years
- Grey sickness affects roughly 15% of the population at any time
- Amber lanterns are the primary light source
- It is late autumn in the city
- The party's activities have been noticed by at least some factions

Generate events in this format:
- [Location]: [Event]. [Sensory detail that makes it feel real].

Examples of good world events:
- Lowmark: Three new grey sickness cases admitted to the Healing House. The queue outside stretched to the corner by midmorning.
- Ashring Plaza: A lantern-maker's stall caught fire. The amber workshop smell hung over the district until evening.
- Dawnhall: Unusually long line for the communal breakfast. Someone started a rumor that supply routes from the south are slower.

Avoid: events that resolve or directly reference the main plot. This is texture, not story.
```

---

## Assembling the Output Document

n8n Code node to produce the final markdown:

```javascript
const sessionNum = $('Extract session number').first().json.session;
const npcReactions = $('LiteLLM NPC reactions').first().json.choices[0].message.content;
const factionShifts = $('LiteLLM faction shifts').first().json.choices[0].message.content;
const worldEvents = $('LiteLLM world events').first().json.choices[0].message.content;
const today = new Date().toISOString().split('T')[0];

const doc = `# Living World Report — Session ${sessionNum}

*Generated: ${today}*

---

## NPC Reactions

${npcReactions}

---

## Faction Shifts

${factionShifts}

---

## World Events (between sessions)

${worldEvents}

---

*Review this before session ${sessionNum + 1}. Edit anything that contradicts player choices or campaign direction. This is a starting point, not a ruling.*
`;

return [{ json: { content: doc, filename: `session${sessionNum}-living-world.md` } }];
```

---

## Gitea Commit Node Config

```json
{
  "method": "POST",
  "url": "https://gitea.research-ready.nl/api/v1/repos/admin/price-of-dawn/contents/{{$json.filename}}",
  "authentication": "headerAuth",
  "headerName": "Authorization",
  "headerValue": "token {{$credentials.giteaApiToken}}",
  "body": {
    "message": "auto: living world report session {{$json.session}}",
    "content": "{{Buffer.from($json.content).toString('base64')}}",
    "branch": "master"
  }
}
```

---

## Langfuse Logging

Add a Langfuse node at the end of the workflow to log:
- Session number
- Token usage across all 3 LLM calls
- Total cost
- Duration

Tag all traces with `["living-world", "price-of-dawn"]` in LiteLLM metadata.

---

## GM Workflow After Trigger

1. Next morning or during session prep: open Gitea, read `session-N-living-world.md`
2. Mark which NPC reactions and world events to use (delete or comment out the rest)
3. Pull 1-2 world events into the five-senses scene opener for next session
4. If any NPC reactions conflict with player choices: override them — the document is a draft, not canon
