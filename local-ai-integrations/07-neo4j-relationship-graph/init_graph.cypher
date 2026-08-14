// =============================================================================
// The Price of Dawn — Neo4j Initial Data Load
// Run in Neo4j Browser at https://neo4j.research-ready.nl
// Or via: python3 neo4j_client.py --init
// =============================================================================

// Clear existing data (only run on fresh setup)
// MATCH (n) DETACH DELETE n;

// =============================================================================
// CONSTRAINTS AND INDEXES
// =============================================================================

CREATE CONSTRAINT npc_name IF NOT EXISTS FOR (n:NPC) REQUIRE n.name IS UNIQUE;
CREATE CONSTRAINT faction_name IF NOT EXISTS FOR (f:Faction) REQUIRE f.name IS UNIQUE;
CREATE CONSTRAINT secret_id IF NOT EXISTS FOR (s:Secret) REQUIRE s.id IS UNIQUE;
CREATE CONSTRAINT player_name IF NOT EXISTS FOR (p:Player) REQUIRE p.name IS UNIQUE;
CREATE CONSTRAINT location_name IF NOT EXISTS FOR (l:Location) REQUIRE l.name IS UNIQUE;

// =============================================================================
// NPC NODES
// =============================================================================

MERGE (:NPC {
  name: "Theron Waide",
  role: "Master Archivist",
  faction: "Archive",
  dawnborn: false,
  age: 71,
  decided: null,
  trust_level: 1,
  notes: "Found Corven documents Year 42. Guilt-ridden. Told no one for 11 years."
});

MERGE (:NPC {
  name: "Sera Voss",
  role: "Guard Captain",
  faction: "Civic Guard",
  dawnborn: true,
  age: 50,
  decided: true,
  decision_session: 0,
  notes: "Decided yes since spring before campaign begins. Protecting the information."
});

MERGE (:NPC {
  name: "Lira Anwick",
  role: "Healer",
  faction: "Independent",
  dawnborn: true,
  age: 50,
  decided: true,
  decision_session: 0,
  notes: "Has daughter Mira (3 years old). Decided yes quietly. Terrified about Mira."
});

MERGE (:NPC {
  name: "Brother Edoran",
  role: "Restorers Founder",
  faction: "Restorers",
  dawnborn: false,
  age: 68,
  decided: null,
  notes: "Lost daughter Annem to grey sickness 6 years ago. Advocates consent-based approach."
});

MERGE (:NPC {
  name: "Chancellor Ostenveld",
  role: "City Council Head",
  faction: "Civic Council",
  dawnborn: false,
  age: 57,
  decided: null,
  notes: "Managing information politically. Controlling the ritual question from civic sphere."
});

MERGE (:NPC {
  name: "Tomas Areth",
  role: "Former Spire Researcher",
  faction: "Independent",
  dawnborn: true,
  age: 52,
  decided: true,
  decision_session: 0,
  notes: "Most recently decided yes. Methodical, honest. Has not told anyone yet."
});

MERGE (:NPC {
  name: "Erem the Wadewalker",
  role: "Ashfen Elder",
  faction: "Ashfen Clans",
  dawnborn: false,
  age: 65,
  decided: null,
  notes: "Knows oral history of the ritual failure. Skeptical of city politics. Precise and patient."
});

MERGE (:NPC {
  name: "Ysel Dorn",
  role: "Temple Keeper",
  faction: "Auris Faith",
  dawnborn: true,
  age: 48,
  decided: true,
  decision_session: 0,
  notes: "Warm, certain, unafraid. Has accepted the necessity with serenity."
});

// Supporting NPCs
MERGE (:NPC {
  name: "Marta",
  role: "Missing person, connected to Sera Voss",
  faction: "Civic Guard (former)",
  dawnborn: false,
  age: 42,
  notes: "Sera's closest friend. Tier 2 unlock for Sera."
});

// =============================================================================
// FACTION NODES
// =============================================================================

MERGE (:Faction {
  name: "Civic Council",
  description: "City governance body. Controls public information about the ritual.",
  public_stance: "Investigating the historical record",
  private_stance: "Controlling the pace of disclosure"
});

MERGE (:Faction {
  name: "Arcane Spire",
  description: "Magical research institution. Has partial ritual documentation.",
  public_stance: "Academic neutrality",
  private_stance: "Protecting institutional legitimacy"
});

MERGE (:Faction {
  name: "Restorers",
  description: "Advocate for ritual proceeding with full consent of all Dawnborn.",
  public_stance: "The sun must return, but only with consent",
  private_stance: "Edoran knows some Dawnborn have already decided; needs all ten"
});

MERGE (:Faction {
  name: "Ashfen Clans",
  description: "Marsh people. Hold oral history of the original ritual failure.",
  public_stance: "We remember what the city has forgotten",
  private_stance: "Will not participate without proper consent process"
});

MERGE (:Faction {
  name: "Grey Market",
  description: "Varenhold trade and information networks. Everything has a price.",
  public_stance: "We trade goods and information",
  private_stance: "Selling information about Dawnborn movements to highest bidder"
});

MERGE (:Faction {
  name: "Auris Faith",
  description: "Religion centered on the return of light. Prophecy-focused.",
  public_stance: "The sun will return when the price is paid",
  private_stance: "Ysel Dorn has accepted; broader temple politically divided"
});

// =============================================================================
// LOCATION NODES
// =============================================================================

MERGE (:Location {name: "Archive", district: "Civic Quarter", description: "City records archive where Theron works"});
MERGE (:Location {name: "Lowmark", district: "Lowmark", description: "Working-class district. Dawnhall feeding program."});
MERGE (:Location {name: "Dawnhall", district: "Lowmark", description: "Communal hall. Feeding program. Cipher room below."});
MERGE (:Location {name: "Healing House", district: "Lowmark", description: "Lira Anwick's practice"});
MERGE (:Location {name: "Ashfen Marshes", district: "Outside city", description: "Home of the Ashfen clans"});
MERGE (:Location {name: "Ashring Plaza", district: "Civic Quarter", description: "Stone circle plaza, ritual significance"});
MERGE (:Location {name: "Civic Hall", district: "Civic Quarter", description: "Ostenveld's seat of power"});
MERGE (:Location {name: "Auris Temple", district: "Temple District", description: "Ysel Dorn's temple"});
MERGE (:Location {name: "Spire", district: "Academic Quarter", description: "Arcane research tower"});

// =============================================================================
// SECRET / INFORMATION NODES
// =============================================================================

MERGE (:Secret {
  id: "ritual-cost",
  content: "The sun restoration ritual requires the willing or unwilling deaths of all 10 Dawnborn.",
  tier: 2,
  location_found: "Archive shelf 4-17-3",
  document: "Corven's sealed documents"
});

MERGE (:Secret {
  id: "corvens-letter",
  content: "Corven's final letter admitting he was uncertain the ritual would work — and that he knew the cost.",
  tier: 3,
  location_found: "Archive shelf 4-17-3"
});

MERGE (:Secret {
  id: "theron-knew-year42",
  content: "Theron Waide found and decoded the ritual cost documents in Year 42 — and told no one for 11 years.",
  tier: 2,
  unlock_phrase: "I know what you found"
});

MERGE (:Secret {
  id: "lira-daughter",
  content: "Lira Anwick has a 3-year-old daughter named Mira. Mira was born after Lira received her death notice.",
  tier: 2,
  unlock_phrase: "Tell me about Mira"
});

MERGE (:Secret {
  id: "edoran-daughter",
  content: "Brother Edoran lost his daughter Annem to grey sickness 6 years ago. This is why he founded the Restorers.",
  tier: 2
});

MERGE (:Secret {
  id: "sera-decision",
  content: "Sera Voss decided yes — the ritual should proceed — since last spring. She is protecting this decision.",
  tier: 2,
  unlock_phrase: "Marta"
});

MERGE (:Secret {
  id: "lira-decision",
  content: "Lira Anwick decided yes, for Mira's future. This contradicts her outward carefulness.",
  tier: 2
});

MERGE (:Secret {
  id: "tomas-decision",
  content: "Tomas Areth has decided yes, most recently of the Dawnborn. He hasn't told anyone yet.",
  tier: 2,
  unlock_phrase: "What do you actually think should happen"
});

MERGE (:Secret {
  id: "ysel-acceptance",
  content: "Ysel Dorn has fully accepted the ritual. She finds serenity in it rather than fear.",
  tier: 2,
  unlock_phrase: "Aren't you afraid"
});

MERGE (:Secret {
  id: "cipher-room-exists",
  content: "There is a sealed cipher room beneath Dawnhall with ritual documentation carved into the walls.",
  tier: 1
});

MERGE (:Secret {
  id: "oral-history-failure",
  content: "The Ashfen oral history records that the original ritual failed because one Dawnborn withdrew consent at the last moment.",
  tier: 3
});

// =============================================================================
// NPC-TO-SECRET KNOWS RELATIONSHIPS
// =============================================================================

MATCH (n:NPC {name: "Theron Waide"}), (s:Secret {id: "ritual-cost"})
MERGE (n)-[:KNOWS {since_year: 42, how: "decoded Corven's sealed documents", reveals_at_tier: 2}]->(s);

MATCH (n:NPC {name: "Theron Waide"}), (s:Secret {id: "corvens-letter"})
MERGE (n)-[:KNOWS {since_year: 42, how: "found with the documents", reveals_at_tier: 3}]->(s);

MATCH (n:NPC {name: "Theron Waide"}), (s:Secret {id: "theron-knew-year42"})
MERGE (n)-[:KNOWS {since_year: 42, reveals_at_tier: 2}]->(s);

MATCH (n:NPC {name: "Brother Edoran"}), (s:Secret {id: "ritual-cost"})
MERGE (n)-[:KNOWS {since_year: 43, how: "obtained via contact from estate sale of Corven papers", reveals_at_tier: 1}]->(s);

MATCH (n:NPC {name: "Chancellor Ostenveld"}), (s:Secret {id: "ritual-cost"})
MERGE (n)-[:KNOWS {since_year: 44, how: "political channels", reveals_at_tier: 3}]->(s);

MATCH (n:NPC {name: "Ysel Dorn"}), (s:Secret {id: "ritual-cost"})
MERGE (n)-[:KNOWS {since_year: 48, how: "Edoran shared documentation", reveals_at_tier: 1}]->(s);

MATCH (n:NPC {name: "Sera Voss"}), (s:Secret {id: "ritual-cost"})
MERGE (n)-[:KNOWS {since_year: 50, how: "council briefing", reveals_at_tier: 2}]->(s);

MATCH (n:NPC {name: "Sera Voss"}), (s:Secret {id: "sera-decision"})
MERGE (n)-[:KNOWS {since_year: 53, reveals_at_tier: 2}]->(s);

MATCH (n:NPC {name: "Lira Anwick"}), (s:Secret {id: "lira-daughter"})
MERGE (n)-[:KNOWS {reveals_at_tier: 2}]->(s);

MATCH (n:NPC {name: "Lira Anwick"}), (s:Secret {id: "lira-decision"})
MERGE (n)-[:KNOWS {since_year: 53, reveals_at_tier: 2}]->(s);

MATCH (n:NPC {name: "Brother Edoran"}), (s:Secret {id: "edoran-daughter"})
MERGE (n)-[:KNOWS {reveals_at_tier: 2}]->(s);

MATCH (n:NPC {name: "Tomas Areth"}), (s:Secret {id: "tomas-decision"})
MERGE (n)-[:KNOWS {since_year: 53, reveals_at_tier: 2}]->(s);

MATCH (n:NPC {name: "Ysel Dorn"}), (s:Secret {id: "ysel-acceptance"})
MERGE (n)-[:KNOWS {reveals_at_tier: 2}]->(s);

MATCH (n:NPC {name: "Erem the Wadewalker"}), (s:Secret {id: "oral-history-failure"})
MERGE (n)-[:KNOWS {how: "Ashfen oral tradition, 50 years of clan memory", reveals_at_tier: 3}]->(s);

// =============================================================================
// NPC-TO-NPC RELATIONSHIPS
// =============================================================================

MATCH (a:NPC {name: "Theron Waide"}), (b:NPC {name: "Sera Voss"})
MERGE (a)-[:KNOWS_PERSONALLY {relationship: "professional respect, limited personal contact", trust: 6, contact_frequency: "monthly"}]->(b);

MATCH (a:NPC {name: "Sera Voss"}), (b:NPC {name: "Theron Waide"})
MERGE (a)-[:KNOWS_PERSONALLY {relationship: "institutional contact", trust: 5, contact_frequency: "monthly"}]->(b);

MATCH (a:NPC {name: "Brother Edoran"}), (b:NPC {name: "Ysel Dorn"})
MERGE (a)-[:TRUSTS {relationship: "ideological ally, shared faith background", trust: 9, contact_frequency: "weekly"}]->(b);

MATCH (a:NPC {name: "Ysel Dorn"}), (b:NPC {name: "Brother Edoran"})
MERGE (a)-[:TRUSTS {relationship: "respected colleague, theological differences accepted", trust: 8}]->(b);

MATCH (a:NPC {name: "Chancellor Ostenveld"}), (b:NPC {name: "Theron Waide"})
MERGE (a)-[:KNOWS_PROFESSIONALLY {relationship: "institutional contact, mutual wariness", trust: 4, contact_frequency: "quarterly"}]->(b);

MATCH (a:NPC {name: "Chancellor Ostenveld"}), (b:NPC {name: "Brother Edoran"})
MERGE (a)-[:KNOWS_PROFESSIONALLY {relationship: "political adversary on ritual question, outward civility", trust: 3}]->(b);

MATCH (a:NPC {name: "Theron Waide"}), (b:NPC {name: "Tomas Areth"})
MERGE (a)-[:KNOWS_PROFESSIONALLY {relationship: "academic overlap at Spire, Theron respects Tomas's caution", trust: 7}]->(b);

MATCH (a:NPC {name: "Erem the Wadewalker"}), (b:NPC {name: "Chancellor Ostenveld"})
MERGE (a)-[:KNOWS_PERSONALLY {relationship: "tense negotiations over Ashfen participation rights, deep mutual mistrust", trust: 2}]->(b);

MATCH (a:NPC {name: "Lira Anwick"}), (b:NPC {name: "Ysel Dorn"})
MERGE (a)-[:KNOWS_PERSONALLY {relationship: "healer and temple keeper, overlapping community service in Lowmark", trust: 7}]->(b);

// =============================================================================
// FACTION MEMBERSHIPS / LEADERSHIP
// =============================================================================

MATCH (n:NPC {name: "Brother Edoran"}), (f:Faction {name: "Restorers"})
MERGE (n)-[:LEADS {since_year: 47}]->(f);

MATCH (n:NPC {name: "Chancellor Ostenveld"}), (f:Faction {name: "Civic Council"})
MERGE (n)-[:LEADS {since_year: 48}]->(f);

MATCH (n:NPC {name: "Erem the Wadewalker"}), (f:Faction {name: "Ashfen Clans"})
MERGE (n)-[:REPRESENTS {role: "Elder and spokesman for clan council"}]->(f);

MATCH (n:NPC {name: "Ysel Dorn"}), (f:Faction {name: "Auris Faith"})
MERGE (n)-[:LEADS {role: "Temple Keeper, public face of faith in Varenhold"}]->(f);

MATCH (n:NPC {name: "Sera Voss"}), (f:Faction {name: "Civic Council"})
MERGE (n)-[:REPORTS_TO {relationship: "Civic Guard falls under Council authority"}]->(f);

// =============================================================================
// LOCATION ASSOCIATIONS
// =============================================================================

MATCH (n:NPC {name: "Theron Waide"}), (l:Location {name: "Archive"})
MERGE (n)-[:WORKS_AT]->(l);

MATCH (n:NPC {name: "Lira Anwick"}), (l:Location {name: "Healing House"})
MERGE (n)-[:WORKS_AT]->(l);

MATCH (n:NPC {name: "Chancellor Ostenveld"}), (l:Location {name: "Civic Hall"})
MERGE (n)-[:WORKS_AT]->(l);

MATCH (n:NPC {name: "Ysel Dorn"}), (l:Location {name: "Auris Temple"})
MERGE (n)-[:WORKS_AT]->(l);

MATCH (n:NPC {name: "Erem the Wadewalker"}), (l:Location {name: "Ashfen Marshes"})
MERGE (n)-[:LIVES_IN]->(l);

// =============================================================================
// SECRET LOCATIONS
// =============================================================================

MATCH (s:Secret {id: "corvens-letter"}), (l:Location {name: "Archive"})
MERGE (s)-[:LOCATED_AT {sublocation: "shelf 4-17-3"}]->(l);

MATCH (s:Secret {id: "cipher-room-exists"}), (l:Location {name: "Dawnhall"})
MERGE (s)-[:LOCATED_AT {sublocation: "basement, sealed room"}]->(l);

// =============================================================================
// VERIFY LOAD
// =============================================================================

// Run these after loading to verify:
// MATCH (n:NPC) RETURN count(n) as npc_count;           // Expect: 9
// MATCH (f:Faction) RETURN count(f) as faction_count;  // Expect: 6
// MATCH (s:Secret) RETURN count(s) as secret_count;    // Expect: 12
// MATCH (r:KNOWS) RETURN count(r) as knows_count;      // Expect: ~16
// MATCH (l:Location) RETURN count(l) as loc_count;     // Expect: 9
