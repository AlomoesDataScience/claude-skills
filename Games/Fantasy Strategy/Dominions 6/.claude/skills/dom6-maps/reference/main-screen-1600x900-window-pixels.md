# dom6-maps - Main screen (1600x900 window pixels)

Part of the dom6-maps skill; SKILL.md links here.

## Main screen (1600x900 window pixels)

| Control | Where | Notes |
|---|---|---|
| Nation of player 1, 2, 3... | x 150, y 22, 56, 90... (+34 each) | green dropdowns, one per player |
| Players (2-30) | 394, 20 | list rows 20 px apart, "2 Players" at y 47 |
| Layout | 394, 50 | layouts for that player count (3 players: only Default Layout) |
| Age | 394, 80 | Early (107), Middle (127), Late (147), All (167); filters the nation lists |
| Map art | 394, 110 | Default Map Art |
| Toggle Hide Settings | 1511, 20 | hides the panels to see the map |
| Change Viewed Season / Layer | 1511, 50 / 80 | winter look; surface or cave plane |
| Advanced Settings | 1511, 110 | terrain and border frequencies (GeneratorSettings.cs) |
| Export Map Files | 1511, 140 | asks a name (field 800,450; OK 799,492) |
| Generate New Map | 1511, 170 | ~2-3 s for 3 players |
| Quit | 1565, 880 | never press Enter while it has focus |

Nation lists: 9 "Generic ..." entries, then vanilla nations of the age, then `DE -` (Dominions
Enhanced), `MOD -` (ModNations.xml, the user's nations), `BZ -` (Bozmod). The list (400 px tall,
scrollbar at x 283) does not take the mouse wheel: drag its scrollbar with `drag --slow` in the
same `seq` as the click that opens it. Player 1's list opens at y 37-433; each later player's list
starts 34 px lower.

On the map: capitals carry the nation name, thrones are labelled "Throne". Province dots are
coloured by terrain (white plains, green forest, gold farm, blue water...); lines are borders:
yellow standard, blue river, purple mountain pass, dark red impassable/cliff, orange road.
