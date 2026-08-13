# 07 — Neo4j NPC Relationship Graph

The static relationship web table in npcs.md becomes a live, queryable graph. Track how relationships evolve as the campaign progresses.
Service: Neo4j at https://neo4j.research-ready.nl (CT114).

---

## What This Enables

- Query: "Which NPCs know about Theron's secret?" → graph traversal answer
- Query: "If Ostenveld hears about the cipher discovery, which other NPCs does he tell?" → relationship path
- Track faction loyalty drift per player action
- Visual relationship map for session 5 (show players the web at the end)

---

## Initial Data Load

### Node types

```cypher
// NPC nodes
CREATE (:NPC {name: "Theron Waide", role: "Master Archivist", faction: "Archive", dawnborn: false, tier_accessible: [1,2,3]})
CREATE (:NPC {name: "Sera Voss", role: "Guard Captain", faction: "Civic Guard", dawnborn: true, tier_accessible: [1,2,3]})
CREATE (:NPC {name: "Lira Anwick", role: "Healer", faction: "Independent", dawnborn: true, tier_accessible: [1,2,3]})
CREATE (:NPC {name: "Brother Edoran", role: "Restorers Founder", faction: "Restorers", dawnborn: false, tier_accessible: [1,2,3]})
CREATE (:NPC {name: "Chancellor Ostenveld", role: "City Council Head", faction: "Civic Council", dawnborn: false, tier_accessible: [1,2,3]})
CREATE (:NPC {name: "Tomas Areth", role: "Former Spire Researcher", faction: "Independent", dawnborn: true, tier_accessible: [1,2,3]})
CREATE (:NPC {name: "Erem the Wadewalker", role: "Ashfen Elder", faction: "Ashfen Clans", dawnborn: false, tier_accessible: [1,2,3]})
CREATE (:NPC {name: "Ysel Dorn", role: "Temple Keeper", faction: "Auris Faith", dawnborn: true, tier_accessible: [1,2,3]})

// Faction nodes
CREATE (:Faction {name: "Civic Council", description: "City governance"})
CREATE (:Faction {name: "Arcane Spire", description: "Magical research institution"})
CREATE (:Faction {name: "Restorers", description: "Advocates for ritual with consent"})
CREATE (:Faction {name: "Ashfen Clans", description: "Marsh people with oral history"})
CREATE (:Faction {name: "Grey Market", description: "Information and trade networks"})
CREATE (:Faction {name: "Auris Faith", description: "Religion of light and return"})

// Information nodes (secrets, facts, things NPCs know)
CREATE (:Secret {id: "ritual-cost", content: "The ritual requires deaths of all 10 Dawnborn", known_since_year: 3})
CREATE (:Secret {id: "corvens-letter", content: "Corven's final letter admitting his uncertainty", location: "shelf 4-17-3"})
CREATE (:Secret {id: "theron-knew-year42", content: "Theron found the documents in Year 42 and told no one for 11 years"})
CREATE (:Secret {id: "lira-daughter", content: "Lira Anwick has a 3-year-old daughter named Mira"})
CREATE (:Secret {id: "edoran-daughter", content: "Brother Edoran lost his daughter Annem to grey sickness 6 years ago"})
CREATE (:Secret {id: "sera-decision", content: "Sera Voss decided yes since spring"})
CREATE (:Secret {id: "lira-decision", content: "Lira Anwick decided yes"})
CREATE (:Secret {id: "tomas-decision", content: "Tomas Areth decided yes (most recent)"})
```

### Relationship types

```cypher
// Knows relationships (who knows what secret)
MATCH (n:NPC {name: "Theron Waide"}), (s:Secret {id: "ritual-cost"})
CREATE (n)-[:KNOWS {since_year: 42, how: "decoded Corven's sealed documents"}]->(s)

MATCH (n:NPC {name: "Theron Waide"}), (s:Secret {id: "theron-knew-year42"})
CREATE (n)-[:KNOWS {since_year: 42}]->(s)

MATCH (n:NPC {name: "Brother Edoran"}), (s:Secret {id: "ritual-cost"})
CREATE (n)-[:KNOWS {since_year: 43, how: "obtained copy from estate sale through contact"}]->(s)

MATCH (n:NPC {name: "Chancellor Ostenveld"}), (s:Secret {id: "ritual-cost"})
CREATE (n)-[:KNOWS {since_year: 44, how: "obtained through political contact"}]->(s)

MATCH (n:NPC {name: "Ysel Dorn"}), (s:Secret {id: "ritual-cost"})
CREATE (n)-[:KNOWS {since_year: 48, how: "Edoran shared documents"}]->(s)

// NPC-to-NPC relationships
MATCH (a:NPC {name: "Theron Waide"}), (b:NPC {name: "Sera Voss"})
CREATE (a)-[:KNOWS_PERSONALLY {relationship: "professional respect, limited personal contact", trust: 6}]->(b)

MATCH (a:NPC {name: "Brother Edoran"}), (b:NPC {name: "Ysel Dorn"})
CREATE (a)-[:TRUSTS {relationship: "ideological ally, shared faith background", trust: 9}]->(b)

MATCH (a:NPC {name: "Chancellor Ostenveld"}), (b:NPC {name: "Theron Waide"})
CREATE (a)-[:KNOWS_PROFESSIONALLY {relationship: "institutional contact, mutual wariness", trust: 4}]->(b)

// Faction memberships
MATCH (n:NPC {name: "Brother Edoran"}), (f:Faction {name: "Restorers"})
CREATE (n)-[:LEADS]->(f)

MATCH (n:NPC {name: "Chancellor Ostenveld"}), (f:Faction {name: "Civic Council"})
CREATE (n)-[:LEADS]->(f)

MATCH (n:NPC {name: "Erem the Wadewalker"}), (f:Faction {name: "Ashfen Clans"})
CREATE (n)-[:REPRESENTS]->(f)
```

---

## Player State Tracking

As the campaign progresses, add relationship edges from players to NPCs:

```cypher
// Player nodes
CREATE (:Player {name: "Kira", character: "Investigator", faction_alignment: null})
CREATE (:Player {name: "Aldric", character: "Scholar", faction_alignment: null})

// Track player-NPC interactions
MATCH (p:Player {name: "Kira"}), (n:NPC {name: "Theron Waide"})
CREATE (p)-[:INTERACTED {session: 2, tier_unlocked: 2, unlock_phrase: "I know what you found", notes: "Kira pushed Theron to admit the eleven years"}]->(n)

// Track what players revealed to NPCs (information flow)
MATCH (p:Player {name: "Kira"}), (n:NPC {name: "Theron Waide"}), (s:Secret {id: "sera-decision"})
CREATE (p)-[:REVEALED_TO {session: 3}]->(n)
CREATE (n)-[:NOW_KNOWS {revealed_by: "Kira", session: 3}]->(s)
```

---

## Useful Queries (run in Neo4j Browser)

### Who knows about the ritual cost?

```cypher
MATCH (n)-[:KNOWS]->(s:Secret {id: "ritual-cost"})
RETURN n.name, n.role, r.since_year, r.how
ORDER BY r.since_year
```

### What does Ostenveld know that the players haven't figured out he knows?

```cypher
MATCH (chancellor:NPC {name: "Chancellor Ostenveld"})-[:KNOWS]->(s:Secret)
WHERE NOT EXISTS {
  MATCH (:Player)-[:KNOWS]->(s)
}
RETURN s.id, s.content
```

### Shortest path between two NPCs (how information would travel)

```cypher
MATCH path = shortestPath(
  (a:NPC {name: "Erem the Wadewalker"})-[*]-(b:NPC {name: "Chancellor Ostenveld"})
)
RETURN path
```

### Which NPCs would hear about a player action in Lowmark district?

```cypher
MATCH (n:NPC)
WHERE n.faction IN ["Civic Guard", "Civic Council"]
   OR exists { MATCH (n)-[:KNOWS_PERSONALLY]->(m:NPC {name: "Sera Voss"}) }
RETURN n.name, n.role
```

### Faction attitude summary

```cypher
MATCH (f:Faction)<-[:LEADS|REPRESENTS]-(n:NPC)
OPTIONAL MATCH (p:Player)-[r:INTERACTED]->(n)
RETURN f.name, collect(n.name) as npcs, count(r) as player_interactions
ORDER BY player_interactions DESC
```

---

## Session-End Update Ritual

After each session, run these updates:

```cypher
// If players revealed information to an NPC this session
MATCH (n:NPC {name: "TARGET_NPC"}), (s:Secret {id: "SECRET_ID"})
MERGE (n)-[:NOW_KNOWS {session: SESSION_NUM, source: "players"}]->(s)

// If a player-NPC tier was unlocked
MATCH (p:Player {name: "PLAYER"})-[r:INTERACTED]->(n:NPC {name: "NPC"})
SET r.tier_unlocked = NEW_TIER

// If faction attitude shifted
MATCH (:Player)-[r:FACTION_ATTITUDE]->(f:Faction {name: "FACTION"})
SET r.attitude = NEW_VALUE, r.last_changed_session = SESSION_NUM
```

---

## Visualization

Neo4j Browser at https://neo4j.research-ready.nl renders the graph visually.

For a player-facing relationship web at end of session 5:
1. Run a full MATCH query
2. Export as SVG from Neo4j Bloom (if available) or screenshot the Browser view
3. Add to the session 5 epilogue handout

Alternatively: use Superset or Metabase to create a simpler relationship table view for between-session GM reference.
