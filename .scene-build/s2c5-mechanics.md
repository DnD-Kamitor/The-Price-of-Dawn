# S2C5 — Rules Reference

<details>
<summary>⚙️ Mechanics</summary>

## Quick-Reference Stat Blocks

---

### Harran Lecht (CR 4)

```
AC 15 | HP 65 | Speed 30 ft.
STR +3 | DEX +2 | CON +3 | INT +2 | WIS +0 | CHA +2
Saves: Str +5, Dex +4
Skills: Athletics +5, Perception +2, Intimidation +4

ACTIONS
Multiattack: Two longsword + one dagger, or three longsword
Longsword: +5 to hit, 1d8+3 slashing
Dagger (thrown 20/60): +4 to hit, 1d4+2 piercing

BONUS ACTIONS
Inspiring Shout (Recharge 5-6): All allies within 30 ft. regain 10 HP

REACTIONS
Tactical Retreat (1/day): Trigger — reduced to 32 HP or fewer, OR
surrounded on three sides. Effect: Harran + conscious allies within
10 ft. Disengage and move 30 ft. without provoking opportunity attacks.
```

---

### Reckoning Veteran (CR 1) ×8

```
AC 13 | HP 32 | Speed 30 ft.
STR +2 | DEX +1 | CON +2
Skills: Athletics +4, Perception +2

ACTIONS
Multiattack: Two shortsword attacks
Shortsword: +4 to hit, 1d6+2 piercing

BONUS ACTIONS
Drag: See full mechanic below.
```

---

### Aldric Stone — Retired Guard, Stone 9 (CR 1, players' side)

```
AC 13 (studded leather) | HP 32 | Speed 30 ft.
STR +2 | DEX +1 | CON +2
Skills: Athletics +4, Perception +3

ACTIONS
Multiattack: Two shortsword attacks
Shortsword: +4 to hit, 1d6+2 piercing

SPECIAL
Stone Attunement: While Aldric is in contact with Stone 9, he has
advantage on all contested Athletics checks to resist Drag.
The stone's Inversion potential remains fully active while he maintains
contact and is not incapacitated.

Priority: Aldric uses his action to resist Drag before attacking.
He will say: "I know what happens if I leave it."
```

---

## The Drag Mechanic — Full Rules

### What It Is

Drag is the Reckoning Veterans' primary tactical tool in this encounter. It is not a standard grapple — it is a targeted extraction designed to remove a Dawnborn from physical contact with their Primer Stone.

### When It Can Be Used

A Reckoning Veteran may use Drag as a bonus action when **all** of the following are true:
1. The Veteran is within 5 ft. of a Dawnborn
2. That Dawnborn is currently in physical contact with (occupying) a Primer Stone
3. The Veteran has not already used Drag as a bonus action this round

### How It Works

1. The Veteran and the targeted Dawnborn each make an **Athletics check** (contested)
   - Veteran: d20 + 4
   - Aldric (standard): d20 + 2 (or d20 + 2 with advantage if Stone Attuned, see above)
2. **On a Veteran success:** The Dawnborn is pulled 5 ft. off their Primer Stone. They are no longer in contact with it.
3. **On a Dawnborn success (tie goes to Dawnborn):** They hold their position. The Veteran may not attempt Drag again this round.

### Example in Play

> *Round 1. Veteran 1 reaches Aldric at Stone 9. V1 attacks twice (6 damage total). As a bonus action, V1 attempts Drag: rolls 14 (d20 + 4). Aldric contests: rolls 18 (d20 + 2 with advantage from Stone Attunement). Aldric holds. Stone 9 remains lit.*

> *Round 2. Both Drag Pair Veterans are adjacent to Aldric. V1 attacks (4 damage). Bonus action Drag: rolls 17. Aldric contests: rolls 12. Aldric is pulled 5 ft. off Stone 9. Stone 9 dims.*

### Player Intervention in Drag

Players can intervene in a Drag attempt in the following ways:

| Method | Mechanic |
|---|---|
| **Interpose (body block)** | A player moves between the Veteran and Aldric before the Drag is declared. The Veteran must attack the player first or move around them (costs movement). Drag cannot target Aldric through a player's occupied space. |
| **Grapple the Veteran** | Standard grapple (opposed Athletics). If successful, the grappled Veteran cannot use Drag (Drag requires free movement). |
| **Help action (Athletics)** | A player uses Help action targeting Aldric's resistance. Aldric's contested Athletics roll gains advantage. Stacks with Stone Attunement advantage (do not double-apply — use advantage from either source). |
| **Attack the Veteran before their bonus action** | If a player's attack reduces the Veteran to 0 HP before the Veteran's bonus action, the Drag does not fire. Priority targeting. |

---

## What "Stone Goes Dim" Means

When a Dawnborn is pulled off their Primer Stone and does not return before combat ends, the stone dims. This has specific mechanical consequences:

### Immediate (During Combat)
- The stone's amber core fades to near-dark.
- The dimming is visible to everyone at the Ashring — no roll required.
- Aldric's Stone Attunement trait is suspended while he is off the stone.

### Short-Term (This Session/Next)
- Any Inversion attempt made with Stone 9 unoccupied uses a **−1 penalty to the Coordination DC**.
- If players later attempt to explain the Inversion parameters to Aldric and encourage his return, he can re-attune — requires one full round of physical contact with his hand on the stone. Stone re-lights at the end of that round.
- Aldric is **shaken** after being physically dragged away. In Session 3, if players attempt to gather Dawnborn at the Ashring, Aldric needs a specific moment of player acknowledgment — someone must speak to him directly about what he did tonight — before he will stand at his stone again without hesitation. He will not name what he needs. He will be waiting for it.

### Long-Term (Session 4+)
- If Stone 9 was dim at the end of this scene and players do not address Aldric's attunement before Session 4, **Ending B (full Inversion, no deaths) now requires 9/10 minimum** instead of 10/10. This is trackable. Players will feel it.
- Full details in s2c5-outcomes.md.

---

## Inspiring Shout — Full Rules

**Recharge:** Roll a d6 at the start of Harran's turn. On a 5 or 6, Inspiring Shout is available.

**Trigger (GM guidance):** Harran uses Inspiring Shout when three Veterans have been dropped. He does not save it for a more optimal moment — he uses it precisely when the remaining Veterans are in danger of breaking.

**Effect:** All allied creatures within 30 ft. that can hear Harran regain 10 HP immediately. This is not magical healing — it does not bypass immunity to healing. It represents second-wind and formation discipline.

**Interaction with Tactical Retreat:** Harran cannot use Inspiring Shout and Tactical Retreat in the same bonus action. If three Veterans are down and Harran is also at half HP, he must choose. He will choose Tactical Retreat — he knows when a position is lost.

---

## Tactical Retreat — Full Rules

**Trigger:** One of:
- Harran is reduced to 32 HP or fewer (half of 65)
- Harran is surrounded on three sides by hostile creatures (three adjacent squares/hexes occupied by enemies)

**Effect:**
- Harran and all **conscious** allied creatures within 10 ft. of him may immediately Disengage as a free action on his turn
- They then each move up to 30 ft. without provoking opportunity attacks
- This movement must be used to move away from the encounter, not to reposition within it

**What it looks like:** Not a rout. Not panic. A measured step back, then a clean withdrawal in formation. Veterans do not run. They move at walking pace with weapons at their sides. Harran says his exit line. They leave.

**What it does not do:** Tactical Retreat does not teleport anyone through player-occupied spaces. If players form a complete encirclement with no gap, Harran cannot retreat cleanly and must attempt a different exit (push through, surrender, or — per his character — buy time with dialogue).

::: {.prop-alt-ink}
**GM NOTE:** Harran does not die at the Ashring in Session 2. He is not built for that. If players somehow have him at 0 HP through unusual means (massive burst damage in one round), have him stabilize at 1 HP and Tactical Retreat fire anyway. Narratively: he takes the hit, staggers, uses the retreat on the very edge of consciousness. He is important in Sessions 3-5. Do not let him die here.
:::

---

## Chancellor's Letter — Mechanics

### When It Arrives

After Harran's Tactical Retreat and the Veterans have cleared the Ashring perimeter — **one full beat of quiet** after the combat ends before Sera Moth appears. Allow players the silence. Let the adrenaline settle. Let someone say something, or not say something. Then:

A young woman appears on the east road — the road Harran's column just used, coming from the opposite direction. She is moving quickly but not running. She wears the Chancellor's administrative badge on her coat lapel. Her name is Sera Moth, and she has been moving toward the Ashring for an hour, having been sent by the Chancellor before Harran arrived. She did not know this was going to be a combat zone.

She looks at the state of the Ashring. She says nothing about what she sees.

She hands the sealed letter to the nearest player.

> "From Chancellor Ostenveld. She asked me to wait for your response, if you have one."

### The Letter

The letter is sealed with the Chancellor's personal seal, not the official city seal. The distinction matters — this is not a formal communication. It is a personal one.

Read aloud:

> *To the investigators I hired:*
>
> *Rationing begins in seven days. The Granary Council has agreed on a structure that should hold through the third month. It will not hold through the sixth. I have done the arithmetic you have not seen — the numbers do not improve.*
>
> *I am sorry it has come to this. I hired you because I hoped you would find something I could use to make it come to something else. I am told you have been thorough.*
>
> *Tell me what you have found. I am ready to hear it.*
>
> *— Chancellor Esveth Ostenveld*

### What the Letter Changes

**Nothing mechanically.** Players still have all the knowledge they had before. The investigation continues in Session 3.

**Everything tonally.** The Chancellor just told them the clock is real. Seven days to rationing. Six months to collapse. Harran said "six months" as he left. The Chancellor says "six months" in writing. These are not different estimates — they are the same estimate, arrived at independently. Harran was not bluffing.

### Player Response to Sera Moth

Sera Moth will wait. She is a junior aide and she takes her instructions seriously. If players ask what the Chancellor knows, she says: *"I carry correspondence. I don't read it."* (She has read it. She does not say this.)

If players ask her to stay while they draft a reply: she does. If players dismiss her: she bows and leaves. She will be back in Session 3 with whatever the Chancellor needs next.

---

## DC Reference Summary

| Check | DC | What It Reveals |
|---|---|---|
| Perception (stones dimming on arrival) | 13 passive | Stones dim when Harran's column approaches |
| Insight (Harran lying) | 14 | His right hand moves to the sword hilt |
| Insight (Harran genuinely angry) | 12 | Voice drops, goes very quiet |
| Athletics (resist Drag, Aldric) | Contested vs. +4 | Hold position at Stone 9 |
| Athletics (player Help for Aldric) | — | Gives Aldric advantage on his contested roll |
| Insight (Harran touched by daughter mention) | 10 | He pauses. Two seconds. It's real. |
| History (Emergency Powers charter) | 12 | Charter grants jurisdiction over ritual sites in emergency declarations; does not grant authority to physically remove Dawnborn from non-restricted civic spaces |

</details>
