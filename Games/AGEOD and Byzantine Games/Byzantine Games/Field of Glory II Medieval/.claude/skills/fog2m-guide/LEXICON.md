# Field of Glory II Medieval - lexicon (war-language)
Game element <-> doctrine term. From the manual (PLAY.md, UNITS.md page refs) and play (battle 2).
Extend whenever something new appears.

## 1. Units -> roles
| game unit/type | arm | natural tasks | never |
|---|---|---|---|
| Knights (Superior, Heavily Armoured, Knightly Lancers) | shock cavalry | main effort: envelop, strike a disrupted unit or a flank, counterattack | charge into rough/marsh; charge a steady spear front |
| Sergeants / Cavalry (Lancers) | medium shock cavalry | flank guard, strike lesser horse and foot, pursue | trade with knights |
| Mounted Crossbowmen | mobile shooters | guard a flank, attack by fire on armour, may evade | stand in melee |
| Light Horse (javelins) | light cavalry | screen, flank guard, harass, feigned retreat (evade) | stand against heavy horse in the open |
| Spearmen / Armoured Spearmen (Defensive) | heavy foot | fixing force, block, anchor against knights | chase; charge out of line |
| Raw Spearmen | brittle heavy foot | reserve / second line, plug gaps | hold the decisive point alone |
| Kerns / Medium Foot | medium foot | rough-ground line, fix | open ground against knights |
| Crossbowmen / Longbowmen (Bowmen) | shooters | attack by fire / support by fire, stationary, concentrated | lone long-range shots; melee (longbow: none) |
| Light Archers / Light Foot | skirmishers | screen, harass, counter-screen | contact with formed troops in the open |
| Peasants (Mob) | levy | filler, absorb, delay | count as combat power |
| General (C-in-C / Sub-General) | command | command range (troop 4, field 8, great 12), rally, boost a fight | be risked except at the decisive moment |

## 2. Map -> terrain (OAKOC)
| terrain | observation/fire | movement | cover | favours |
|---|---|---|---|---|
| Open ground | full | 4 AP/square foot and mounted | none | horse, heavy foot |
| Hill (height shown in tooltip) | higher sees and fights downhill | slight | none | the side on top in melee (key terrain) |
| Tracks | full | road move | none | movement |
| Rough | - | extra AP; disorders heavy foot, severely disorders knights | some | medium/light foot (obstacle for horse) |
| Woods | blocks sight | difficult | hides units (only fog of war in FoG II) | light foot |
| Enclosures/hedges | partial | obstacle | cover for foot behind them | foot defending |

## 3. Mechanics -> effects
| game rule | doctrine effect |
|---|---|
| ZOC (primary/secondary) | fix / block - a unit in contact range can't be bypassed freely |
| Cohesion Steady > Disrupted > Fragmented > Broken | morale / unit cohesion - the real target (break, don't kill) |
| Evade (lights, non-lancer cavalry) | disengage / feigned retreat |
| Flank charge (must start behind the flank) | envelopment's payoff - assailable flank |
| Command range, generals | command and control |
| Ammo (5 good shots) | sustainment of fires - concentrate them |
| Shooting stationary, short range | attack by fire from a set position (halt, then fire) |
| Turn limit (AI wins time-out) | time - the defender trades nothing for time; we must attack |
| Whole Command move stops within 5 squares of the enemy | movement technique changes at contact - individual bounds |
| Army morale bars (% routed) | defeat condition / culmination of the enemy |

## 4. Victory -> end state
Break the French: 60% routed, or 40-59% if we have lost 25 points less - before turn 24.
Decisive conditions: their south end (Knights 1, Crossbowmen 7-8) broken, generals lost.

## 5. Control measures in grid terms
Phase line = a column by a turn ("PL B col 17, turn 6"); objective = squares or named units;
sectors by rows (N 0-10, C 11-13, S 14+); stand-off line = 5 squares from their crossbows
(outside range 4) and outside knights' 3-square reach (4 AP/square of 14).

## 6. Back-translation: task -> game actions
| doctrine task | game actions | cost | check after |
|---|---|---|---|
| fix | move into the enemy's front at stand-off or contact, face them, hold | AP; foot ~4/square | ZOC applies, still Steady |
| attack by fire | move to range (short = 2), stop, shoot the same target with every shooter | ammo 1 | target's cohesion, ammo left |
| envelop | knights move round the flank so they START behind the target's flank line, then charge next turn | 2 turns | the "flank" marker in the charge tooltip |
| screen / guard | light horse 3-4 squares off the enemy, room to evade behind | AP | out of non-light reach, or evade-safe |
| reserve | stay 1-2 squares behind the line, AP unused on purpose | 0 | still in command range |
| prepare a charge / orient on the objective | Turn to face next turn's target (8 directions); unmanoeuvrable 45 deg = 4 AP, 90 = 8 | AP | target within 45 deg of straight ahead |
| counterattack | charge a unit that just attacked and is disordered | AP | Win:Draw:Lose tooltip first |
