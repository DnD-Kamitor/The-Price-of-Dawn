---
title: "The Star-Wheel"
subtitle: "Varenhold Civic Archive — Restricted Stacks"
---

*You are standing in the restricted stacks of the Varenhold Civic Archive. The shelves are arranged radially from a central column. On the column: three brass rings, each engraved with constellation symbols. On the east wall: a star chart.*

*The rings control which shelf sections are physically accessible. You need shelf 4-17-3.*

---

<div id="star-wheel-app">

<div class="ring-selector">

<div class="ring-label">Ring 1 — First Star (West)</div>
<select id="ring1" class="ring-select">
  <option value="">— select a constellation —</option>
  <option value="vaels-crown">Vael's Crown</option>
  <option value="shepherds-eye">Shepherd's Eye</option>
  <option value="trailing-light">Trailing Light</option>
  <option value="iron-bridge">Iron Bridge</option>
  <option value="the-anvil">The Anvil</option>
  <option value="ash-crown">Ash Crown</option>
</select>

<div class="ring-label">Ring 2 — Second Star (Middle)</div>
<select id="ring2" class="ring-select">
  <option value="">— select a constellation —</option>
  <option value="vaels-crown">Vael's Crown</option>
  <option value="shepherds-eye">Shepherd's Eye</option>
  <option value="trailing-light">Trailing Light</option>
  <option value="iron-bridge">Iron Bridge</option>
  <option value="the-anvil">The Anvil</option>
  <option value="ash-crown">Ash Crown</option>
</select>

<div class="ring-label">Ring 3 — Third Star (East)</div>
<select id="ring3" class="ring-select">
  <option value="">— select a constellation —</option>
  <option value="vaels-crown">Vael's Crown</option>
  <option value="shepherds-eye">Shepherd's Eye</option>
  <option value="trailing-light">Trailing Light</option>
  <option value="iron-bridge">Iron Bridge</option>
  <option value="the-anvil">The Anvil</option>
  <option value="ash-crown">Ash Crown</option>
</select>

</div>

<div style="margin: 1.5em 0;">
<button id="turn-wheel" onclick="turnWheel()">Turn the Wheel</button>
</div>

<div id="wheel-result" style="display:none;"></div>

</div>

---

<details>
<summary>★ Star Chart — East Wall Reference</summary>

*The chart is mounted in a wide wooden frame, covering most of the east wall. Stars labeled in plain Common. One constellation is circled in red ink — a recent addition. A note below it reads: "overhead on the night of the ritual, Year 48."*

```
╔══════════════════════════════════════════════════════════════════╗
║  VARENHOLD OBSERVATORY — NIGHT SKY REFERENCE                     ║
║  Year 48, Third Month. The Dawnmark Constellation (circled).     ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  WEST ──────────────────────────────────────────────── EAST      ║
║  (rises first)                                   (rises last)    ║
║                                                                  ║
║                                                                  ║
║       ★                    ★                         ★           ║
║    VAEL'S               SHEPHERD'S                TRAILING       ║
║    CROWN                  EYE                      LIGHT         ║
║  [leftmost]            [middle]                  [rightmost]     ║
║  [anchor pt]           [pivot]                   [brightest]     ║
║                                                                  ║
║  ╔══════════════════════════════════════════════════════════╗     ║
║  ║          ← THE DAWNMARK CONSTELLATION →                 ║     ║
║  ║  West-to-east rise order: Crown, Eye, Trailing Light.   ║     ║
║  ║  The Dawnmark was directly overhead at 02:14, Year 48.  ║     ║
║  ╚══════════════════════════════════════════════════════════╝     ║
║                                                                  ║
║  [Dozens of other constellations labeled across the chart —      ║
║   only the Dawnmark is circled in red.]                          ║
╚══════════════════════════════════════════════════════════════════╝
```

*The red circle ink is in a different hand from the chart itself. Someone circled it later. Someone was working something out.*

</details>

<style>
#star-wheel-app {
  border: 2px solid #8b6914;
  border-radius: 8px;
  padding: 1.5em 2em;
  background: linear-gradient(to bottom, #fdf8ee, #fef9f0);
  margin: 1.5em 0;
  max-width: 560px;
}

.ring-selector {
  display: flex;
  flex-direction: column;
  gap: 0.75em;
}

.ring-label {
  font-weight: 700;
  font-size: 0.85em;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #5a3e10;
  margin-top: 0.5em;
}

.ring-select {
  width: 100%;
  padding: 0.5em 0.75em;
  border: 1px solid #c9a050;
  border-radius: 4px;
  background: #fffdf5;
  font-size: 1em;
  color: #2a1a00;
  cursor: pointer;
}

.ring-select:focus {
  outline: 2px solid #8b6914;
  outline-offset: 1px;
}

#turn-wheel {
  background: #5a3e10;
  color: #fdf8ee;
  border: none;
  padding: 0.6em 1.8em;
  font-size: 1em;
  font-weight: 700;
  border-radius: 4px;
  cursor: pointer;
  letter-spacing: 0.05em;
}

#turn-wheel:hover {
  background: #7a5418;
}

.result-success {
  border-left: 4px solid #1f6e4a;
  background: #f0faf4;
  padding: 1em 1.25em;
  border-radius: 0 6px 6px 0;
  margin-top: 1em;
}

.result-partial {
  border-left: 4px solid #c9922a;
  background: #fdf8ee;
  padding: 1em 1.25em;
  border-radius: 0 6px 6px 0;
  margin-top: 1em;
}

.result-failure {
  border-left: 4px solid #7a1a1a;
  background: #fdf5f5;
  padding: 1em 1.25em;
  border-radius: 0 6px 6px 0;
  margin-top: 1em;
}

.result-heading {
  font-weight: 700;
  font-size: 0.82em;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 0.5em;
}

.shelf-contents {
  margin-top: 1em;
  border-top: 1px solid #c9a050;
  padding-top: 1em;
}

.document-block {
  border: 1px solid #c9a050;
  border-radius: 4px;
  padding: 1em 1.25em;
  background: #fffdf5;
  margin-top: 0.75em;
  font-family: 'Palatino Linotype', Georgia, serif;
  font-size: 0.95em;
  line-height: 1.6;
}

.notation-grid {
  font-family: monospace;
  font-size: 0.88em;
  white-space: pre;
  background: #f5f0e8;
  border: 1px solid #c9a050;
  padding: 0.75em 1em;
  border-radius: 4px;
  margin-top: 0.5em;
  overflow-x: auto;
}
</style>

<script>
var attempts = 0;

function turnWheel() {
  var r1 = document.getElementById('ring1').value;
  var r2 = document.getElementById('ring2').value;
  var r3 = document.getElementById('ring3').value;
  var result = document.getElementById('wheel-result');

  if (!r1 || !r2 || !r3) {
    result.style.display = 'block';
    result.innerHTML = '<div class="result-failure"><div class="result-heading">The rings resist.</div><p>All three rings must be set before the wheel responds.</p></div>';
    return;
  }

  var correct = ['vaels-crown', 'shepherds-eye', 'trailing-light'];
  var chosen = [r1, r2, r3];
  var matches = chosen.filter(function(v, i) { return v === correct[i]; }).length;

  result.style.display = 'block';

  if (matches === 3) {
    result.innerHTML = successHTML();
  } else if (matches === 2) {
    result.innerHTML = partialHTML(chosen, correct);
  } else {
    attempts++;
    result.innerHTML = failureHTML(attempts);
  }
}

function successHTML() {
  return '<div class="result-success">' +
    '<div class="result-heading" style="color:#1f6e4a;">✓ The shelves shift.</div>' +
    '<p>A low mechanical tone moves through the floor. The shelves rotate on their column — a quarter turn, then stop. Shelf 4-17-3 is directly in front of you. The brass fittings catch the lantern light.</p>' +
    '<p><em>The brass is recently polished. The oil in the mechanism is fresh. Someone has been maintaining this room for eleven years.</em></p>' +
    '<div class="shelf-contents">' +
    '<strong>Contents of shelf 4-17-3:</strong>' +
    '<div class="document-block">' +
    '<p style="font-size:0.8em;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#5a3e10;">Corven\'s Public Notes — Technical Summary</p>' +
    '<p><em>[Several pages of dense formal notation, bound with dark cord. The cover bears the Archive\'s filing stamp: "Ritual of Eternal Dawn — Technical Documentation — Archmagister A. Corven." Filed Year 48. Not opened since.]</em></p>' +
    '<hr style="border:none;border-top:1px solid #c9a050;margin:0.75em 0;">' +
    '<p><strong>RITUAL OF ETERNAL DAWN — TECHNICAL SUMMARY</strong><br><em>Archmagister A. Corven — Filed for Archive Record</em></p>' +
    '<p>The mechanism employed in the Year 48 ritual attempt draws on distributed sympathetic resonance — a configuration in which the anchor points for the ritual\'s energy are distributed across multiple sites rather than concentrated at a central point.</p>' +
    '<p>This approach was chosen specifically because concentrated application at a single anchor risks cascade failure. The distributed model is more stable under load, though it requires precise calibration across all points simultaneously.</p>' +
    '<p>The living conduit mechanism was selected as the most reliable method for maintaining the distributed sympathetic anchors over time. Theoretical alternatives were considered and rejected.</p>' +
    '<p><strong>The ritual did not fail in the manner first reported.</strong></p>' +
    '<p>Further details are encoded in the supplementary notation. The key to that notation is provided separately, in three portions.</p>' +
    '<p><em>[The document ends here. The next several pages are dense notation — unreadable without the Notation Key.]</em></p>' +
    '</div>' +
    '<div class="document-block" style="margin-top:1em;">' +
    '<p style="font-size:0.8em;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#5a3e10;">Fragment I — Corven\'s Private Notation Key</p>' +
    '<p><em>[A single sheet of paper in a careful, precise hand. At the top: "Notation Reference — Section I of III." Along the right edge, the grid clearly continues but the page stops.]</em></p>' +
    '<div class="notation-grid">' +
    '╔══════════════════════════════════════════════════════════════╗\n' +
    '║  CORVEN PRIVATE NOTATION — FRAGMENT I OF III                  ║\n' +
    '║  Section I: Base Symbols (partial — see Sections II, III)     ║\n' +
    '╠══════════════════════════════════════════════════════════════╣\n' +
    '║                                                              ║\n' +
    '║   ✦ = T     ◈ = E     ⬡ = N     ⬟ = L     ⬠ = I            ║\n' +
    '║   ◆ = G     ◇ = H     ○ = B     ● = R     ◎ = S            ║\n' +
    '║                                                              ║\n' +
    '║   [continues →] Section II: ⊕ ⊗ ⊙ △ ▽ ▲ ▼ □ ■ ▪ ▸         ║\n' +
    '║   [continues →] Section III: remaining symbols               ║\n' +
    '║                                                              ║\n' +
    '╠══════════════════════════════════════════════════════════════╣\n' +
    '║                                                              ║\n' +
    '║  TWO PLAIN-LANGUAGE NOTES (in Corven\'s hand):                ║\n' +
    '║                                                              ║\n' +
    '║  Note 1:                                                     ║\n' +
    '║  "The weight borne willingly is not the same weight as the   ║\n' +
    '║   weight imposed. This is not a philosophical observation.   ║\n' +
    '║   It is an engineering specification."                       ║\n' +
    '║                                                              ║\n' +
    '║  Note 2:                                                     ║\n' +
    '║  "The mechanism will not function as designed if the         ║\n' +
    '║   distinction is collapsed."                                 ║\n' +
    '║                                                              ║\n' +
    '╚══════════════════════════════════════════════════════════════╝' +
    '</div>' +
    '</div>' +
    '</div>' +
    '</div>';
}

function partialHTML(chosen, correct) {
  var names = {
    'vaels-crown': "Vael's Crown",
    'shepherds-eye': "Shepherd's Eye",
    'trailing-light': "Trailing Light",
    'iron-bridge': "Iron Bridge",
    'the-anvil': "The Anvil",
    'ash-crown': "Ash Crown"
  };
  var wrongIdx = chosen.map(function(v, i) { return v !== correct[i] ? i + 1 : null; }).filter(Boolean);
  return '<div class="result-partial">' +
    '<div class="result-heading" style="color:#8b6914;">◐ Close — the shelves move, but not enough.</div>' +
    '<p>The mechanism engages. The shelves rotate partway. Sections 4-17-1 and 4-17-2 are now accessible — but not 4-17-3. The correct shelf is one ring setting away.</p>' +
    '<p><em>Ring ' + wrongIdx.join(' is wrong. Ring ') + ' is wrong.</em> Try adjusting it.</p>' +
    '</div>';
}

function failureHTML(n) {
  var msgs = [
    '<div class="result-heading" style="color:#7a1a1a;">✗ The shelves rotate — wrong configuration.</div><p>A grinding resistance, then motion. The shelves turn on their column — a full rotation, slow, deliberate, like something heavy that\'s been asked to move against its preference. When they stop, everything has shifted. Thirty minutes of work to get them back to a starting position.</p><p><em>Whoever operates the wheel: one level of exhaustion from the mechanism\'s feedback.</em></p>',
    '<div class="result-heading" style="color:#7a1a1a;">✗ The shelves rotate again.</div><p>The mechanism responds to intent, not just position. A second wrong configuration sends everything turning again. Thirty more minutes. Another level of exhaustion on the operator.</p><p><em>From somewhere below — distant footsteps. Someone heard the shelves move.</em></p>',
    '<div class="result-heading" style="color:#7a1a1a;">✗ The mechanism locks.</div><p>This time the rings don\'t move after the rotation. A faint resistance when you try — not mechanical, something else. The wheel won\'t respond.</p><p>The footsteps from below are getting closer.<br><br>Theron Waide appears at the doorway. His coat is slightly askew. There is ink on his sleeve. He looks at the shelves, then at the rings, then at you.<br><br><em>"I\'ve known the configuration since Corven sealed this room,"</em> he says. <em>"I have not been able to set it myself."</em><br><br>He crosses to the column and sets all three rings without looking at the star chart.</p>'
  ];
  var idx = Math.min(n - 1, msgs.length - 1);
  return '<div class="result-failure">' + msgs[idx] + '</div>';
}
</script>
