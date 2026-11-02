"""Static checks for a Dominions 6 .dm file. It cannot replace loading the mod in game.

  python3 -I check_dm.py MOD.dm [MANUAL_TEXT ...]

Pass the text of dom6modman.pdf and, for mods with events, dom6eventman.pdf (both made by
manual_text.py).

Run it from anywhere; image paths are checked relative to the .dm file's folder.
Checks:
  - every #new.../#select... block is closed by #end, and no #end is stray
  - every sprite, flag and icon file exists (paths are case sensitive)
  - every monster, weapon and armour number used by the mod is defined in it (vanilla numbers
    below 5000 / 1000 / 400 are assumed to exist)
  - #startsite, #autospell and #form names match a #name in the file
  - two-handed weapons are not given to a monster that also has a shield
  - monsters with #magicskill 9 also have #holy
  - events: a valid #rarity, a #msg under 2399 characters, the [bracketed name] that site and
    named-item commands read, event codes in the safe range -300..-5000, #req_code 0 on events
    that start a chain, a next event after every #delay, limits on always events, #req_pregame
    and #worldritrebate only with the rarities they work with, enchantment numbers defined by a
    #effect 10081 spell
  - with MANUAL_TEXT (from manual_text.py), every command appears in one of the manuals
"""
import os
import re
import sys

path = sys.argv[1]
manual = "\n".join(open(f).read() for f in sys.argv[2:]) if len(sys.argv) > 2 else None
base = os.path.dirname(os.path.abspath(path))
src = open(path).read()
lines = [l.split("--")[0].strip() for l in src.split("\n")]
code = "\n".join(lines)
errs, warns = [], []

OPEN = re.compile(r"#(newweapon|selectweapon|newarmor|selectarmor|newmonster|selectmonster|selectnametype|newsite|"
                  r"selectsite|selectnation|newnation|newspell|selectspell|newitem|selectitem|newtemplate|"
                  r"selectbless|selectsound|newevent|selectpoptype)\b")
cur = None
for n, l in enumerate(lines, 1):
    if OPEN.match(l):
        if cur:
            errs.append(f"line {n}: {l} starts while '{cur[1]}' (line {cur[0]}) is still open")
        cur = (n, l)
    elif l == "#end":
        if not cur:
            errs.append(f"line {n}: #end with nothing open")
        cur = None
if cur:
    errs.append(f"line {cur[0]}: '{cur[1]}' is never closed")

for f in re.findall(r'#(?:spr1|spr2|spr|xspr1|xspr2|unmountedspr1|unmountedspr2|flag|icon) "([^"]+)"', code):
    if not os.path.exists(os.path.join(base, f)):
        errs.append("missing image " + f)

mons = set(re.findall(r"#newmonster (\d+)", code))
weps = set(re.findall(r"#newweapon (\d+)", code))
arms = set(re.findall(r"#newarmor (\d+)", code))
MONREF = (r"#(addrecunit|addreccom|homemon|homecom|mon|com|startcom|startunittype\d|startscout|defcom\d|defunit\w*|"
          r"wallcom|wallunit|guardcom|guardunit|hero\d+|multihero\d|addgod|mountmnr|coridermnr|copystats|"
          r"summon\w*|damage|"
          r"2com|4com|5com|stealthcom|1unit|\d+d\d+units|var0units|assassin|assfollower\w+|transform|"
          r"forcetransform|killmon|kill2d6mon|killcom|\w+boost|req_\w*mnr\w*|req_\w*monsters?\w*) (\d+)")
for k, v in re.findall(MONREF, code):
    if int(v) >= 5000 and v not in mons:
        errs.append(f"#{k} {v}: monster not defined in this mod")
for v in re.findall(r"#(?:weapon|secondaryeffect\w*|copyweapon) (\d+)", code):
    if int(v) >= 1000 and v not in weps:
        errs.append(f"weapon {v} not defined in this mod")
for v in re.findall(r"#(?:armor|copyarmor) (\d+)", code):
    if int(v) >= 400 and v not in arms:
        errs.append(f"armour {v} not defined in this mod")
names = set(re.findall(r'#name "([^"]+)"', code))
for k, nm in re.findall(r'#(startsite|autospell|form) "([^"]+)"', code):
    if nm not in names:
        warns.append(f'#{k} "{nm}": no #name in this mod (fine only if it is a vanilla name)')

# per-monster checks
twoh = set()
for m in re.finditer(r"#newweapon (\d+)(.*?)#end", code, re.S):
    if "#twohanded" in m.group(2):
        twoh.add(m.group(1))
shields = set()
for m in re.finditer(r"#newarmor (\d+)(.*?)#end", code, re.S):
    if re.search(r"#type 4\b", m.group(2)):
        shields.add(m.group(1))
VANILLA_2H = {"2", "5", "11", "14", "18", "7", "257", "258", "259", "165"}   # pike, halberd, great sword, maul...
VANILLA_SHIELD = {"1", "2", "3", "4"}
for m in re.finditer(r"#newmonster (\d+)(.*?)#end", code, re.S):
    body = m.group(2)
    nm = re.search(r'#name "([^"]+)"', body)
    nm = nm.group(1) if nm else m.group(1)
    w = set(re.findall(r"#weapon (\d+)", body))
    a = set(re.findall(r"#armor (\d+)", body))
    if (w & (twoh | VANILLA_2H)) and (a & (shields | VANILLA_SHIELD)):
        errs.append(f"{nm}: two-handed weapon together with a shield")
    if re.search(r"#magicskill 9 \d", body) and "#holy" not in body:
        errs.append(f"{nm}: priest levels without #holy")
    if re.search(r"#custommagic (\d+)", body):
        for mask in re.findall(r"#custommagic (\d+)", body):
            if int(mask) == 65536:
                errs.append(f"{nm}: #custommagic with only the priest bit crashes the game")

# events
RARITIES = {0, 1, 2, 5, -1, -2, 10, 11, 12, 13}
ALWAYS = {0, 5, 10, 13}
NOT_LIMITS = {"#req_pop0ok", "#req_indepok", "#req_voidok", "#req_targforeignok", "#req_story"}
CODE_CMDS = r"#(code|code2|codedelay|codedelay2|resetcode|resetcodedelay|resetcodedelay2|req_code|req_notcode|" \
            r"req_anycode|req_notanycode|req_nearbycode|req_nearowncode) (-?\d+)"
BRACKET = [(r"#req_(?:site|foundsite|hiddensite|nearbysite|claimedthrone|unclaimedthrone) [01]\b", "a site name"),
           (r"#revealsite\b", "a site name"),
           (r"#(?:addsite|maybeaddsite|hiddensite|maybehiddensite|removesite) -1\b", "a site name"),
           (r"#magicitem 9\b", "an item name"), (r"#addequip 9\b", "an item name")]
ench_def = set()
for m in re.finditer(r"#(?:newspell|selectspell)(.*?)#end", code, re.S):
    if re.search(r"#effect 1008[1245]\b", m.group(1)):          # 10081 global; DE also uses 10082/4/5
        ench_def.update(re.findall(r"#damage (\d+)", m.group(1)))
events = [(code.count("\n", 0, m.start()) + 1, m.group(1), m.group(2))
          for m in re.finditer(r"^(#newevent|#selectevent[^\n]*)\n(.*?)^#end", code, re.S | re.M)]
codes, ench_missing = set(), set()
for k, (n, head, body) in enumerate(events):
    msg = re.search(r'#msg "(.*?)"', body, re.S)
    nm = f"event at line {n}" + (f' ("{msg.group(1)[:30]}...")' if msg else "")
    cmds = set(re.findall(r"^#[a-z0-9_]+", body, re.M))
    rar = re.search(r"^#rarity (-?\d+)", body, re.M)
    delayed = k > 0 and re.search(r"^#delay(25|50)? ", events[k - 1][2], re.M)    # reached only by the delay
    if head == "#newevent":
        if not rar:
            warns.append(f"{nm}: no #rarity (Dominions Enhanced has a few such events; set one)")
        if not msg and "#notext" not in cmds:
            warns.append(f"{nm}: no #msg")
    r = int(rar.group(1)) if rar else None
    if r is not None and r not in RARITIES:
        errs.append(f"{nm}: #rarity {r} is not a listed rarity")
    if msg and len(msg.group(1)) > 2399:
        errs.append(f"{nm}: #msg is {len(msg.group(1))} characters (max 2399)")
    for pat, what in BRACKET:
        if re.search(pat, body) and not (msg and re.search(r"\[[^\]]+\]\s*$", msg.group(1))):
            errs.append(f"{nm}: {re.search(pat, body).group(0)} needs {what} in [brackets] at the end of #msg")
    sets_code = False
    for c, v in re.findall(CODE_CMDS, body):
        v = int(v)
        codes.add(v)
        if v != 0 and not -5000 <= v <= -300:
            warns.append(f"{nm}: event code {v} is outside the safe range -300..-5000")
        if c in ("code", "code2", "codedelay", "codedelay2") and v != 0:
            sets_code = True
    if sets_code and "#req_code" not in cmds:
        warns.append(f"{nm}: sets an event code without #req_code (use #req_code 0 so it cannot break a running chain)")
    if re.search(r"#flagland 1\b", body) and not sets_code:
        warns.append(f"{nm}: #flagland 1 needs an event code in the province")
    if re.search(r"^#delay(25|50)? ", body, re.M) and k == len(events) - 1:
        errs.append(f"{nm}: #delay needs a next event in the file")
    if (r in ALWAYS and head == "#newevent" and not delayed and "#id" not in cmds
            and not [c for c in cmds if c.startswith("#req_") and c not in NOT_LIMITS]):
        warns.append(f"{nm}: always event (rarity {r}) with no limiting requirement fires everywhere every month")
    if "#req_pregame" in cmds and r not in (0, 5):
        errs.append(f"{nm}: #req_pregame needs rarity 0 or 5")
    if "#worldritrebate" in cmds and r not in (11, 12):
        errs.append(f"{nm}: #worldritrebate only works with rarity 11 or 12")
    if "#incunrest" in cmds:
        warns.append(f"{nm}: #incunrest is only in the manual's example; the listed command is #unrest")
    for v in re.findall(r"#(?:req_ench|req_noench|req_myench|req_friendlyench|req_hostileench|req_enchdom|req_enchtarget|"
                        r"req_enchnearby|nationench|assownerench) (\d+)", body):
        if v not in ench_def:
            ench_missing.add(int(v))
if ench_missing:
    warns.append("enchantment numbers used by events but not made by an enchantment spell here "
                 f"(fine if vanilla or another mod's): {sorted(ench_missing)}")

if manual is not None:
    for c in sorted(set(re.findall(r"^#[a-z0-9_]+", code, re.M))):
        base_c = re.sub(r"\d+[a-d]?$", "", c)                       # #hero3 -> #hero, #defunit1b -> #defunit
        if not re.search(re.escape(c) + r"\b", manual) and not re.search(re.escape(base_c), manual):
            warns.append(f"{c} is not in the manual text")

for e in errs:
    print("ERROR", e)
for w in warns:
    print("warn ", w)
print(f"{len(mons)} monsters, {len(weps)} weapons, {len(arms)} armours, {code.count('#newspell')} spells, "
      f"{code.count('#newitem')} items, {len(events)} events: {len(errs)} errors, {len(warns)} warnings")
if codes - {0}:
    print("event codes used:", sorted(codes - {0}))
sys.exit(1 if errs else 0)
