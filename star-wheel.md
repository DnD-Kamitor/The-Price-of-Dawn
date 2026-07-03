---
title: "The Star-Wheel"
subtitle: "Varenhold Civic Archive — Restricted Stacks"
---

*Three brass rings on the central column. Each engraved with constellation symbols. Turn them to the correct west-to-east rise order of the Dawnmark — then turn the wheel.*

<div id="star-wheel-app">

<div class="wheel-container">

<div class="wheel-column">
<div class="ring-label">West Star — Ring 1</div>
<button class="spin-btn up-btn" onclick="spin(0,-1)">&#9650;</button>
<div class="wheel-viewport">
<div class="wheel-track" id="track-0"></div>
</div>
<button class="spin-btn down-btn" onclick="spin(0,1)">&#9660;</button>
</div>

<div class="wheel-divider">✦</div>

<div class="wheel-column">
<div class="ring-label">Middle Star — Ring 2</div>
<button class="spin-btn up-btn" onclick="spin(1,-1)">&#9650;</button>
<div class="wheel-viewport">
<div class="wheel-track" id="track-1"></div>
</div>
<button class="spin-btn down-btn" onclick="spin(1,1)">&#9660;</button>
</div>

<div class="wheel-divider">✦</div>

<div class="wheel-column">
<div class="ring-label">East Star — Ring 3</div>
<button class="spin-btn up-btn" onclick="spin(2,-1)">&#9650;</button>
<div class="wheel-viewport">
<div class="wheel-track" id="track-2"></div>
</div>
<button class="spin-btn down-btn" onclick="spin(2,1)">&#9660;</button>
</div>

</div>

<div class="turn-row">
<button id="turn-wheel-btn" onclick="turnWheel()">&#9881; Turn the Wheel</button>
</div>

<div id="wheel-result"></div>

</div>

---

<details>
<summary>★ Star Chart — East Wall Reference</summary>

*The chart is mounted in a wide wooden frame. Stars labeled in plain Common. One constellation is circled in red ink — recent addition. A note below reads: "overhead on the night of the ritual, Year 48."*

```
╔══════════════════════════════════════════════════════════════════╗
║  VARENHOLD OBSERVATORY — NIGHT SKY REFERENCE                     ║
║  Year 48, Third Month. The Dawnmark Constellation (circled).     ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  WEST ──────────────────────────────────────────────── EAST      ║
║  (rises first)                                   (rises last)    ║
║                                                                  ║
║       ★                    ★                         ★           ║
║    VAEL'S               SHEPHERD'S                TRAILING       ║
║    CROWN                  EYE                      LIGHT         ║
║  [leftmost]            [middle]                  [rightmost]     ║
║                                                                  ║
║  West-to-east rise order: Crown → Eye → Trailing Light           ║
╚══════════════════════════════════════════════════════════════════╝
```

</details>

<style>
#star-wheel-app {
  background: linear-gradient(160deg, #1c1000 0%, #2a1800 60%, #1c1000 100%);
  border: 2px solid #b8860b;
  border-radius: 12px;
  padding: 1.75em 1.5em 1.5em;
  max-width: 520px;
  margin: 1.5em auto;
  box-shadow: 0 6px 28px rgba(0,0,0,0.55), inset 0 1px 0 rgba(255,210,80,0.12);
}

.wheel-container {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  gap: 0.5em;
}

.wheel-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.35em;
  flex: 1;
  min-width: 0;
}

.wheel-divider {
  color: #5a3e10;
  font-size: 1.1em;
  padding-top: 3.8em;
  flex-shrink: 0;
}

.ring-label {
  color: #b8860b;
  font-size: 0.65em;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  text-align: center;
  line-height: 1.3;
  min-height: 2em;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

.spin-btn {
  background: linear-gradient(to bottom, #3a2500, #2a1800);
  color: #b8860b;
  border: 1px solid #5a3e10;
  width: 100%;
  padding: 0.4em 0;
  cursor: pointer;
  font-size: 0.8em;
  border-radius: 5px;
  transition: background 0.12s, color 0.12s;
  line-height: 1;
}

.spin-btn:hover {
  background: linear-gradient(to bottom, #5a3e10, #3a2500);
  color: #f0c040;
  border-color: #b8860b;
}

.spin-btn:active {
  background: #7a5418;
}

.wheel-viewport {
  width: 100%;
  height: 192px;
  overflow: hidden;
  position: relative;
  border: 2px solid #5a3e10;
  border-radius: 6px;
  background: #0a0600;
  box-shadow: inset 0 3px 10px rgba(0,0,0,0.7);
}

.wheel-viewport::before {
  content: '';
  position: absolute;
  top: 64px;
  height: 64px;
  left: 0;
  right: 0;
  border-top: 1px solid #b8860b;
  border-bottom: 1px solid #b8860b;
  background: rgba(184,134,11,0.06);
  pointer-events: none;
  z-index: 2;
}

.wheel-viewport::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to bottom,
    rgba(10,6,0,0.8) 0%,
    transparent 28%,
    transparent 72%,
    rgba(10,6,0,0.8) 100%
  );
  pointer-events: none;
  z-index: 3;
}

.wheel-track {
  position: absolute;
  width: 100%;
  will-change: transform;
}

.wheel-item {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #5a3e10;
  font-size: 0.78em;
  font-weight: 600;
  font-family: 'Palatino Linotype', Georgia, serif;
  padding: 0 0.4em;
  line-height: 1.25;
  user-select: none;
}

.wheel-item.active {
  color: #f0c040;
  font-size: 0.86em;
  text-shadow: 0 0 10px rgba(240,192,64,0.5);
}

.turn-row {
  text-align: center;
  margin-top: 1.4em;
}

#turn-wheel-btn {
  background: linear-gradient(to bottom, #8a6018, #5a3e10);
  color: #f0c040;
  border: 1px solid #b8860b;
  padding: 0.65em 2.2em;
  font-size: 1em;
  font-weight: 700;
  border-radius: 6px;
  cursor: pointer;
  letter-spacing: 0.05em;
  font-family: 'Palatino Linotype', Georgia, serif;
  box-shadow: 0 3px 10px rgba(0,0,0,0.5);
  transition: background 0.15s, box-shadow 0.15s, transform 0.1s;
}

#turn-wheel-btn:hover {
  background: linear-gradient(to bottom, #aa7820, #7a5418);
  box-shadow: 0 3px 16px rgba(184,134,11,0.35);
}

#turn-wheel-btn:active {
  transform: translateY(1px);
  box-shadow: 0 1px 6px rgba(0,0,0,0.5);
}

#wheel-result {
  margin-top: 1.25em;
}

.result-success {
  border-left: 4px solid #2d9e5f;
  background: rgba(45,158,95,0.08);
  color: #a8d8b8;
  padding: 1em 1.25em;
  border-radius: 0 6px 6px 0;
}

.result-partial {
  border-left: 4px solid #c9922a;
  background: rgba(201,146,42,0.08);
  color: #c9a050;
  padding: 1em 1.25em;
  border-radius: 0 6px 6px 0;
}

.result-failure {
  border-left: 4px solid #9e2d2d;
  background: rgba(158,45,45,0.08);
  color: #c08080;
  padding: 1em 1.25em;
  border-radius: 0 6px 6px 0;
}

.result-heading {
  font-weight: 700;
  font-size: 0.88em;
  text-transform: uppercase;
  letter-spacing: 0.09em;
  margin-bottom: 0.6em;
}

.shelf-contents {
  margin-top: 1em;
  border-top: 1px solid rgba(45,158,95,0.3);
  padding-top: 1em;
}

.document-block {
  border: 1px solid rgba(45,158,95,0.25);
  border-radius: 4px;
  padding: 1em 1.25em;
  background: rgba(0,0,0,0.25);
  margin-top: 0.75em;
  font-family: 'Palatino Linotype', Georgia, serif;
  font-size: 0.88em;
  line-height: 1.65;
  color: #b8d4c0;
}

.notation-grid {
  font-family: monospace;
  font-size: 0.78em;
  white-space: pre;
  background: rgba(0,0,0,0.35);
  border: 1px solid rgba(45,158,95,0.2);
  color: #90b89a;
  padding: 0.75em 1em;
  border-radius: 4px;
  margin-top: 0.5em;
  overflow-x: auto;
}
</style>

<script>
(function() {
  var OPTIONS = ["Vael's Crown", "Shepherd's Eye", "Trailing Light", "Iron Bridge", "The Anvil", "Ash Crown"];
  var N = OPTIONS.length;
  var ITEM_H = 64;
  var indices = [0, 0, 0];
  var busy = [false, false, false];
  var attempts = 0;

  function buildTracks() {
    for (var r = 0; r < 3; r++) {
      var track = document.getElementById('track-' + r);
      if (!track) continue;
      // Extended: [clone_of_last, item0..item(N-1), clone_of_first]
      var ext = [N - 1];
      for (var i = 0; i < N; i++) ext.push(i);
      ext.push(0);
      for (var j = 0; j < ext.length; j++) {
        var div = document.createElement('div');
        div.className = 'wheel-item';
        div.textContent = OPTIONS[ext[j]];
        track.appendChild(div);
      }
      _setPos(r, false);
      _updateActive(r);
    }
  }

  function _setPos(r, animated) {
    var track = document.getElementById('track-' + r);
    if (!track) return;
    var y = (indices[r] + 1) * ITEM_H;
    track.style.transition = animated ? 'transform 0.27s cubic-bezier(0.4,0,0.2,1)' : 'none';
    track.style.transform = 'translateY(-' + y + 'px)';
  }

  function _updateActive(r) {
    var track = document.getElementById('track-' + r);
    if (!track) return;
    var items = track.querySelectorAll('.wheel-item');
    var activePos = indices[r] + 1;
    for (var i = 0; i < items.length; i++) {
      if (i === activePos) {
        items[i].classList.add('active');
      } else {
        items[i].classList.remove('active');
      }
    }
  }

  window.spin = function(r, dir) {
    if (busy[r]) return;
    busy[r] = true;

    var track = document.getElementById('track-' + r);
    if (!track) { busy[r] = false; return; }

    if (dir === -1 && indices[r] === 0) {
      // Wrap up: animate to clone_of_last (position 0)
      track.style.transition = 'transform 0.27s cubic-bezier(0.4,0,0.2,1)';
      track.style.transform = 'translateY(0px)';
      indices[r] = N - 1;
      setTimeout(function() {
        _setPos(r, false);
        _updateActive(r);
        busy[r] = false;
      }, 290);
    } else if (dir === 1 && indices[r] === N - 1) {
      // Wrap down: animate to clone_of_first (position N+1)
      track.style.transition = 'transform 0.27s cubic-bezier(0.4,0,0.2,1)';
      track.style.transform = 'translateY(-' + ((N + 1) * ITEM_H) + 'px)';
      indices[r] = 0;
      setTimeout(function() {
        _setPos(r, false);
        _updateActive(r);
        busy[r] = false;
      }, 290);
    } else {
      indices[r] = indices[r] + dir;
      _setPos(r, true);
      _updateActive(r);
      setTimeout(function() { busy[r] = false; }, 290);
    }
  };

  window.turnWheel = function() {
    var correct = [0, 1, 2]; // Vael's Crown, Shepherd's Eye, Trailing Light
    var matches = 0;
    for (var i = 0; i < 3; i++) {
      if (indices[i] === correct[i]) matches++;
    }
    var result = document.getElementById('wheel-result');
    if (!result) return;

    if (matches === 3) {
      result.innerHTML = successHTML();
    } else if (matches === 2) {
      var wrongRing = 0;
      for (var j = 0; j < 3; j++) { if (indices[j] !== correct[j]) wrongRing = j + 1; }
      result.innerHTML = partialHTML(wrongRing);
    } else {
      attempts++;
      result.innerHTML = failureHTML(attempts);
    }
  };

  function successHTML() {
    return '<div class="result-success">' +
      '<div class="result-heading" style="color:#2d9e5f;">&#10003; The shelves shift.</div>' +
      '<p>A low mechanical tone moves through the floor. The shelves rotate on their column — a quarter turn, deliberate, then stop. Shelf 4-17-3 is directly in front of you.</p>' +
      '<p><em>The brass is recently polished. The oil is fresh. Someone has maintained this room for eleven years.</em></p>' +
      '<div class="shelf-contents">' +
      '<strong>Contents of shelf 4-17-3:</strong>' +
      '<div class="document-block">' +
      '<p style="font-size:0.78em;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#6bac84;">Corven\'s Public Notes — Technical Summary</p>' +
      '<p><em>[Several pages of formal notation, bound with dark cord. Filing stamp: "Ritual of Eternal Dawn — Technical Documentation — Archmagister A. Corven." Filed Year 48. Not opened since.]</em></p>' +
      '<p><strong>RITUAL OF ETERNAL DAWN — TECHNICAL SUMMARY</strong></p>' +
      '<p>The mechanism employed in the Year 48 ritual attempt draws on distributed sympathetic resonance — anchor points distributed across multiple sites rather than concentrated at a single point.</p>' +
      '<p>The living conduit mechanism was selected as the most reliable method for maintaining the distributed sympathetic anchors over time. Theoretical alternatives were considered and rejected.</p>' +
      '<p><strong>The ritual did not fail in the manner first reported.</strong></p>' +
      '<p>Further details are encoded in the supplementary notation. The key is provided separately, in three portions.</p>' +
      '<p><em>[The remaining pages are dense notation — unreadable without the Notation Key.]</em></p>' +
      '</div>' +
      '<div class="document-block" style="margin-top:0.75em;">' +
      '<p style="font-size:0.78em;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:#6bac84;">Fragment I — Corven\'s Private Notation Key</p>' +
      '<p><em>[A single sheet, careful hand. "Notation Reference — Section I of III." The grid clearly continues beyond the page edge.]</em></p>' +
      '<div class="notation-grid">' +
      '╔══════════════════════════════════════════════════╗\n' +
      '║  CORVEN NOTATION — FRAGMENT I OF III              ║\n' +
      '╠══════════════════════════════════════════════════╣\n' +
      '║  ✦=T  ◈=E  ⬡=N  ⬟=L  ⬠=I                       ║\n' +
      '║  ◆=G  ◇=H  ○=B  ●=R  ◎=S                       ║\n' +
      '║  [Section II & III carry remaining symbols]       ║\n' +
      '╠══════════════════════════════════════════════════╣\n' +
      '║  Note 1:                                          ║\n' +
      '║  "The weight borne willingly is not the same     ║\n' +
      '║   weight as the weight imposed. This is not a    ║\n' +
      '║   philosophical observation. It is an            ║\n' +
      '║   engineering specification."                    ║\n' +
      '║                                                   ║\n' +
      '║  Note 2:                                          ║\n' +
      '║  "The mechanism will not function as designed    ║\n' +
      '║   if the distinction is collapsed."              ║\n' +
      '╚══════════════════════════════════════════════════╝' +
      '</div>' +
      '</div>' +
      '</div>' +
      '</div>';
  }

  function partialHTML(wrongRing) {
    return '<div class="result-partial">' +
      '<div class="result-heading" style="color:#c9922a;">&#9680; The shelves move — not enough.</div>' +
      '<p>The mechanism engages. Shelves shift. Sections 4-17-1 and 4-17-2 become accessible — but not 4-17-3. One ring is wrong.</p>' +
      '<p><em>Ring ' + wrongRing + ' is not correct. The correct shelf is one setting away.</em></p>' +
      '</div>';
  }

  function failureHTML(n) {
    var msgs = [
      '<div class="result-heading" style="color:#9e2d2d;">&#10007; The shelves rotate — wrong configuration.</div><p>A grinding resistance, then motion. The shelves turn on their column — full rotation, slow and deliberate. When they stop, everything has shifted. Thirty minutes of work to restore a starting position.</p><p><em>Whoever operated the wheel: one level of exhaustion.</em></p>',
      '<div class="result-heading" style="color:#9e2d2d;">&#10007; The shelves rotate again.</div><p>A second wrong configuration. Thirty more minutes. Another level of exhaustion on the operator.</p><p><em>From somewhere below — distant footsteps. Someone heard the shelves move.</em></p>',
      '<div class="result-heading" style="color:#9e2d2d;">&#10007; The mechanism locks.</div><p>The rings resist when you try them. Something beyond mechanical — the wheel will not respond.</p><p>The footsteps are closer now. Theron Waide appears in the doorway. Coat slightly askew. Ink on his sleeve. He looks at the shelves, then the rings, then you.</p><p><em>"I\'ve known the configuration since Corven sealed this room. I have not been able to set it myself."</em></p><p>He crosses to the column and sets all three rings without looking at the star chart.</p>'
    ];
    var idx = Math.min(n - 1, msgs.length - 1);
    return '<div class="result-failure">' + msgs[idx] + '</div>';
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', buildTracks);
  } else {
    buildTracks();
  }
})();
</script>
