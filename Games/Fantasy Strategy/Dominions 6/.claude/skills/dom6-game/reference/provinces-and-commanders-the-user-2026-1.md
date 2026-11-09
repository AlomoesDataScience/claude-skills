# dom6-game - Provinces and commanders (the user, 2026-10-27; checked in game)

Part of the dom6-game skill; SKILL.md links here.

## Provinces and commanders (the user, 2026-10-27; checked in game)

- **Right-click a province** to view it: its info fills the right panel. Most lines there are
  clickable (usually left-click). Provinces you can't see give less information.
- Back to the capital: left-click the god's name (title line), right-click the capital, or Home.
  Your provinces carry your flag.
- **Commanders** are the tokens on the left (those in the viewed province). Left-click selects
  (token turns white, tooltip "Name. Defend. (space) Change order..."); space opens the order
  menu; **left-click on the map moves** the selection there. A stealthy commander's order
  becomes **Sneak** and a grey arrow points to the target. Changeable until the turn ends.
- **The space order menu** (Theocratus, the start commander, turn 1) opens top-left over the
  commander column, titled with the commander's name; the map hides labels and flags while it is
  open. Groups (bars) and entries, with their tooltips:
  - *Move*: Defend "(D) ... the default order"; Patrol Province "(X) Try to find hidden enemy
    troops and reduce unrest by killing brigands"; Move; Pillage.
  - *Sacred*: Become Prophet, "spreads dominion like his pretender god but at a slower rate".
  - *Magic*: Empowerment "using large quantities of magic gems a commander can learn a new magic
    path or become better in one he already knows"; Blood Hunt "(B) ... very difficult ... without
    power in this path".
  - *Construction*: Demolish Fort, Demolish Lab (destructive, never pick these by accident).
  - Cancel at the bottom. Entries sit about 28 px apart, x≈100 (Defend y 90 ... Demolish Lab 430).
  The menu changes with the commander, the province and what has been researched.
- Prophet (space > Become Prophet; the token then reads "Prophet"): the user's rule is to name a prophet on turn 1 or 2 and let him expand (he spreads
  dominion and can claim thrones). The start commander (Theocratus the Centurion) has Become
  Prophet in his menu.
- **Army Setup** (`t`, or the first top-bar icon) for the viewed province. A header row (province
  picture, "Pythium, 0 units in garrison", then icons: units owned here 47, supplies 1230,
  supply needed 47, siege strength 47). One row per commander: token (tooltip "Theocratus the
  Centurion"), a green box, `<set battle orders>`, and on the right four numbers (tooltips: hover the **number's
  centre**, not its icon; see dom6-tooltips): squads used / squads led without morale penalty
  (bodyguards don't count), living units led / leadership, magic beings led / magic leadership,
  and the supplies he and his units need. Header: units owned here, supplies available, supply
  needed, siege strength. Mages show their path symbols under the name on the token. Under him, one strip per
  squad (20 and 25 units, "+1 morale" = commander morale bonus), each with its own box and
  `<set battle orders>`. Exit at the bottom. Tooltips there sit over the map and often fail to read.
  `2/3` = squads used / allowed (past 3, squads lose morale; the user).
- **Battle orders**, opened by a `<set battle orders>` bar (letters are their hotkeys):
  - *Commander* ("Set battle orders for NAME"): three script bars on top (the round-by-round
    script; the last shows the main order). *Single Round Orders* add a step: Hold one turn (w),
    Attack one turn (v), Fly Attack one turn (y). *Main Order*: None (n, he decides), Stay behind
    troops (s: casts spells, fires missiles, else gets behind the rearmost unit), Attack (a),
    Retreat (r). *Target* (for Attack): none, enemy archers, cavalry, fliers, large monsters,
    closest enemy, rearmost enemies. Checkbox: Conservative magic gem usage (-) (no unscripted gem
    spells, fewer gems used for fatigue). Ok closes and the bar then shows the order.
  - *Mage scripting* (Theurg Apuleius, Pythium, turn 6): spellcasters get two more Single Round
    Orders, **Hold or Cast a spell** (AI picks the spell) and **Cast a specific spell**, and two
    more main orders, **Cast spells** and **Advance and cast spells**. Cast a specific spell
    opens **Choose spell**: every battle spell grouped by school and research level with its
    path symbols; **greyed = this mage cannot cast it** (path too low). Scroll for more (the
    Divine/priest spells are last); Exit at the bottom leaves without picking. Right-click a
    spell for its card (range, casting time, area, precision, fatigue, effect, description;
    Exit (959, 665)). A picked spell shows in the top script bar as "(Spell name)" with
    **`<del>`** at its right end to remove it. Up to five script steps, then the main order
    (the orange bar). Default for a fresh Theurg: no script, Main Order None, target none, i.e.
    the AI decides (manual p. 45: "If a commander receives no orders, the AI will assign them").
    A scripted spell falls back to an AI pick if gems are missing or no target is in range;
    gem spells need the gems in the mage's inventory before the battle. Copy a script: hover it,
    ctrl+number; then hover another commander's `<set battle orders>` and press the number.
  - *Squad* ("Set battle orders for squad"): None (the commander decides), Attack, Hold and
    attack (hold two turns; archers fire instead), Fire (until out of missiles; advances if enemies
    are close), Hold and Fire, Fire and keep distance, Retreat, Guard commander (greyed when the
    squad is too big: at most 5 bodyguards for Theocratus). Same targets. Ok closes.
  - **Position Army** (left-click a squad's box in Army Setup; also a commander's green box): the
    battlefield. My side is the lighter green on the left, the enemy's the dark green on the
    right, so the front faces right. Squads are labelled boxes ("25 Alae Legionnaires",
    "20 Velites"); the commander is a grey/white circle. **Left-click a squad (its label, not the
    circle) to select it** (it turns white; the header shows its size); **right-click the field to
    move the selected squad there**. Formations, top right, for the selected squad: Line (1300, 69),
    Sparse line (1324, 93), Double line (1323, 115), Box (1473, 68), Skirmish (1489, 92); the
    chosen one is drawn bright. The squad picture and the field don't open unit info on right-click.
    **Select by the label at the squad box's top-left corner** (a click in the middle of the
    Velites box did nothing) and check the header's unit count before giving orders: an order
    goes to whichever squad is selected. The header's `<set battle orders>` bar (524, 97) opens
    the squad order window (Attack (739, 385), Fire (731, 441), Ok (959, 631)); the window's text
    is hard to OCR, so use these positions. Army Setup then shows each squad's order under
    its size, and its small green boxes show the formation shapes.
    Exit at the bottom (959, 949).
  - Formations (manual p. 59): Box = near-square block (default); Line = one rank facing the
    enemy; Double line = two ranks; Sparse line = gaps between squares, twice as long, −1 morale;
    Skirmish = checkerboard, −1 morale (Skirmisher ability cancels it; undisciplined squads must
    use it). Line, double and sparse need a good leader. One square holds 10 size points
    (three humans).
  - **Army Setup unit strips are live**: left-click a unit = select it (it lights up), then
    left-click another squad's strip = **move it into that squad**. alt+click selects every unit
    of that type in the squad; Enter deselects. Never click a strip by accident: a missed button
    click there selects or moves troops (it happened: a Legionnaire landed in the Velites).
    Right-click a unit = its unit screen (the name is in the title bar, e.g. "Alae Legionnaire
    from Pythium"; OCR misses the title, crop it). Velite and Alae Legionnaire sprites look alike.
  - **Click the order word itself.** Once a squad has an order, its `<set battle orders>` label
    shrinks to the order ("Fire", "Attack"); only the word opens the window. Check that the
    window opened (its "Main Order" bar and Ok) before clicking inside it.
  - A lone commander's Position Army has no formations: just right-click where he stands.
    Scouts: Retreat + far rear (left edge, about x 375), so they escape at once (the user).
  - The **target column ungreys** once a main order is picked; set it too (orders read
    "Fire closest" afterwards).
  - Clicks, full screen: commander bar (645, 344); squad 1 bar (1350, 430); commander window
    Stay behind troops (790, 523), Ok (959, 771); squad window Ok (959, 631).
- Map labels are drawn on the terrain and OCR misses them: click by screen position from a
  screenshot taken at the current zoom (labels move when zooming/scrolling; press Home first).
- Start army: a commander with a small force, plus one stealthy scout. Don't move the army
  turn 1 (no scouting info yet; first reports arrive next turn), except with some awake
  pretender builds.
- Scouting: independents never search for scouts, so scouts can go anywhere; enemy nations'
  province defence and patrols can catch them. A scout hidden in a province sees it better.
- **Province reports can be wrong about numbers** (rarely 30 reported, 80 there); what kinds of
  troops are there is generally not hidden.
