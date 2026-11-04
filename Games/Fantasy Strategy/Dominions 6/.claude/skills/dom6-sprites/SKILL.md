---
name: dom6-sprites
description: Make Dominions 6 unit sprites (TGA, black-transparent, magenta-shadow, facing left) by modelling the unit as a signed-distance 3D figure and rendering it with painted cel shading, posed after a Dominions Enhanced unit. Use whenever the user asks for a unit/commander/mage/summon/mech picture or sprite for a Dominions mod, wants a sprite changed (pose, colours, proportions, contrast), or wants an image "converted" into a Dominions-ready sprite.
---

# Dominions 6 sprite building

Sprites are not drawn by hand: each unit is a small 3D model built from SDF
primitives on a shared human rig, ray-marched in pure Python, cel-shaded into
4 tones, supersampled, inked, and written as a 24-bit TGA. Changing a pose or
a colour is a parameter edit and a re-render (~5-15 s per unit on 12 cores).

## Dominions 6 sprite format (from dom6modman.pdf)

- TGA (24/32-bit, uncompressed or RLE) or PNG. Use 24-bit RGB TGA.
- 24-bit: pure black `(0,0,0)` is transparent, pure magenta `(255,0,255)` is shadow.
  Never let figure pixels be pure black or pure magenta (the renderer clamps them).
- Canvas sides of 8/16/32/64/128. Humans: 64x64. Size 4+ units/mechs: 128x128. Long
  beasts and vehicles may use 128x64 like Dominions Enhanced tigers and chariots.
- Nation flag: one 128x128 `flag.tga` (pole may run to the bottom edge, no shadow).
- `#spr1` = normal image (`<unit>1.tga`), `#spr2` = attack image (`<unit>2.tga`).
- Filenames are case-sensitive; keep them lowercase, no spaces.
- **Sprites face LEFT** — the game reads the facing as the move direction. This is a
  hard requirement from the user.
- Feet on row RES-3 (row 61 on 64x64), two free rows below except the magenta
  shadow ellipse.
- Scale: a human is ~35 px tall on 64x64 (Dominions Enhanced humans: head top ~row
  26, feet row 61, head ~7 px, shoulders ~10 px). Bigger sizes scale up from that:
  size 3 ~45 px, size 4 ~52-56 px, size 6 ~70 px, size 8 ~85 px (on 128x128).

## Sprite Studio (interactive editor)

`Games/Fantasy Strategy/Dominions 6/spritestudio/` is a local web editor (`python3 server.py`) for the same
kind of SDF models, stored as JSON (`models/<name>.json`): live 3D view, pose with IK
handles, recolour, reshape, render and export TGAs. Its engine (`engine/`) has a
`studio` look (the chrome killbot) and a `cel` look (this skill's renderer). Use it when
the user wants to edit a unit by hand; see its README for the model format.

## Environment

Only system `python3` with PIL. **No numpy, no pip** (a venv without pip fails).
Everything is pure Python + `multiprocessing.Pool`. Run scripts with `python3 -I`.
The pool uses every core; set `SPRITE_WORKERS=6` (or fewer) when memory is short, e.g. while
Firefox and the game are open (each worker holds the whole model).

## Files

- `scripts/palette.py` — header: imports, material ids, `PALETTE` (lit, shade, deep
  per material) and `EMISSIVE` (edge, core colours for glowing materials). Add new
  materials here (extend the tuple and the `range(1, N)`).
- `scripts/sdf_core.py` — vectors, primitives (`sphere capsule roundcone ellipsoid
  box grooves`), `Group` (add/cut/finish), `ik`, `perp`, `front_side`.
- `scripts/rig.py` — the human rig and part library (see API below).
- `scripts/render.py` — camera (yaw -30, pitch 8, orthographic), shading, ray
  marcher, sprite post-process (ink, outline, shadow, halo, free rows), `main`.
- `scripts/build.sh UNITS_FILE OUT_SCRIPT OUTDIR [unit...]` — concatenates
  palette + sdf_core + rig + your units file + render into one standalone script and
  runs it. Keep that standalone script next to the sprites so they can be redrawn.
- `scripts/refsheet.py` — contact sheet of spr1/spr2 pairs from a mod folder, to pick stances.
- `scripts/compare.py` — side-by-side zoomed sheet (new sprite vs. reference, or a roster).
- `scripts/check.py` — validates size/mode/free rows and prints figure bounds and height.
- `scripts/inspect_pose.py GEN.py UNIT OUT.png [--zoom 3] [--poses 1] [--views sprite,front,side]` —
  renders the model large (zoom x resolution) through the sprite camera, face-on and in profile,
  next to the real 64 px sprite. Use it when a limb, hand or prop vanishes in the small sprite:
  it shows what hides what. ~40 s per view at zoom 3. Lesson from it: hand and foot targets are
  world positions, so on hovering units (`body=(0, 0.3, 0)`) add the hover height to them too.
- `examples/madscience_units.py` — 40 worked units plus a flag: troopers, militia, commanders,
  mages, robots, monsters, a 128x128 war droid (two marks), clones, heroes, lightning
  casters, a hovering flyer, power-armoured tesla troopers and an immobile 128x128
  tesla pylon (a non-human build), quadrupeds (gene hound, lion/goat/serpent chimera),
  vehicles (motorcycle with seated rider, 128x128 truck) and the nation banner.
  Copy patterns from here first.
- `examples/rgm_mech_size8.py` — older standalone generator for a size-8 mech (yaw -40,
  own camera block); `examples/killbot_and_painting.py` — standalone generator that
  also renders a large 900x900 "picture" next to the sprite.

## Workflow

1. **Read the request and references.** Look at any images the user dropped (convert
   .webp with PIL and Read the PNG). Note what must survive at 35 px: silhouette,
   2-3 main colours, the weapon, one signature detail. Fine details become 1-2 px.
2. **Pick a stance reference** from Dominions Enhanced
   (`Games/Fantasy Strategy/Dominions 6/Dominions Enhanced/<nation>/<unit>1.tga` / `2.tga`). Use `refsheet.py`, view it,
   then zoom the chosen pair with `compare.py`. Cite it next to the unit's POSES
   (e.g. `# (venedia admiral)`). User preference: scientists/mages calm in spr1,
   active casting in spr2 (not a plain standing pose); warriors copy the reference's
   guard and attack. Vanilla sprites (idle and attack PNGs for every unit) are in the
   `dom6-inspector` skill: `inspector.py sprite "<unit>"` prints their paths; Dominions
   Enhanced stays the stance source the user asked for.
3. **Write the unit** in a units file: a `b_<unit>(R)` build function and a `UNITS`
   entry with `poses={"1": {...}, "2": {...}}`. Start from the closest example unit.
4. **Render and compare:** `build.sh units.py gen.py OUT unit` then
   `compare.py sheet.png 4 OUT/unit1.tga,REF1.tga,OUT/unit2.tga,REF2.tga`, Read the
   sheet, fix, repeat. Zoom (crop + 5-6x) to check details; also look at 1x.
5. **Check** with `check.py`, then copy the TGAs and the standalone generator into
   the nation folder. Report what was made and that it is untested in-game.

## Rig API (rig.py)

Coordinates are model metres, y up, x = the unit's LEFT, z = its front. The camera
turns the unit's front 30° toward screen-left, so its right side (−x) is the far
side and screen-left is "forward".

- `W(f, y, d)` — point `f` m screen-left of the body axis, height `y`, `d` m toward
  the viewer. Use it for hand and foot targets. 1 px ≈ 0.05 m at human scale.
- `aim(elev, side=0)` — unit direction pointing screen-left raised `elev` degrees
  (>90 leans back toward screen-right; negative points down). Weapon directions.
- `FEET(f_right, f_left, d_right, d_left)` — ankle targets for `"feet"`.
- Pose keys: `feet`, `body` (offset of the upper body, e.g. `(0,-0.08,0.03)` to drop
  into a lunge), `lean` (deg, tips toward screen-left), `twist` (deg about y;
  negative turns the chest toward screen-left), `nod` (head), `splay`, `knee`,
  `hand_r`, `hand_l`, `pole_r`, `pole_l` (elbow pole directions), plus any custom
  keys your build function reads (`blade`, `gun`, `fire`, …), and `halo=True` to give
  big glowing things a soft glow ring.
- `Rig` methods: `R.body(g)` for torso parts modelled upright (pelvis 0.92, chest
  1.3, shoulders 1.4); `R.head(g)` for head parts (head centre `HEAD_C`, radii
  `HEAD_R`); `R.world(g)` for things placed in world space (arms, weapons).
- Parts: `legs(R, thigh, shin, boot, lt, boot_top, bare, extra)`,
  `arm(R, s, hand, upper, fore, glove, at, pole, extra, sh_w)` (s = −1 right, +1 left;
  returns shoulder, elbow, wrist, forearm dir, hand centre), `face`, `hair_short`,
  `eyes`, `lumpy` (bumpy hair/rags), `shell` (bands/trim cut from a surface),
  `cone_skirt` (coats, robes, capes with z-limits), `disc` (flat cylinder),
  `limb`.
- Equipment: `sword`, `rifle(k=thickness)`, `pistol`, `flash` (muzzle flash),
  `bolt` (lightning), `blade_basis(d)` (flat of a blade facing the viewer),
  `bar_basis(d)`. In the examples: `torus`, `plate` (shields), `flask`, `syringe`,
  `goggles`, `oriented_ellipsoid` (portals), `robe_body`, `trooper_*`, `lightning`
  (forked bolt; use `kinks=5, amp≈0.1, branches≤1` for hand-cast bolts so they read as
  zig-zags, not a fuzzy band), `cable` (wires as capsule chains).
- Flyers/hover: raise the upper body with `body=(0, 0.32, 0)` and set the ankle targets
  above the ground (y 0.35-0.5) so the legs dangle over the shadow.
- Non-human builds (towers, machines) can ignore the rig: just add groups with
  `R.world(g)` and give the poses empty dicts plus custom keys.
- Unit options: `scale` (size relative to a 1.73 m human), `res` (64, 128 or (w, h)),
  `shadow` (x0, x1 of the shadow ellipse, or None), `cx`, `y0`, `yaw`/`pitch` (re-aim the
  camera, e.g. yaw 0 for a face-on flag), `free_rows=False` (let a pole reach the
  bottom), `file` (output name prefix if it differs from the key). A pose key of `""`
  writes a single `<name>.tga` (flags).
- Beasts and vehicles: `Q(f, y, s)` places points along a heading `QF` (screen-left,
  turned 17° to the viewer; `QS` is the side facing the viewer). `beast(R, k, fur, paw,
  bulk)` builds a quadruped from pose keys `c` (body centre), `pitch`, `feet` (4 x (f,y,s)),
  `qhead` makes muzzled heads with an opening jaw, `chain` tapers tails/necks/horns,
  `wheel` makes tyres. Seated riders: `twist=-43` faces the rider along `QF`, `body`
  drops the pelvis onto the seat, `knee` points the knees forward-up.

## Lessons learned (avoid repeating these)

- **Contrast beats detail.** A dark rifle across white armour vanished until it was
  ~1.5x thicker, held further from the body (depth gap → ink outline) and coloured
  near-black with mid-grey furniture (so it also shows against the black background).
- Copper next to skin reads as skin (a copper stole looked like bare chest): use gold
  or a contrasting trim on robes.
- A giant boxy helmet (box + large rounding) looks like a TV head; keep helmet half-size
  ≤ head radii and rounding ≤ 0.03.
- All-dark power armour becomes a blob: light steel plates with copper trim and a dark
  undersuit read far better.
- Quadrupeds read as lanky dogs/hyenas unless they are bulky (`bulk` 1.45-1.5) with the
  body lowered so the legs bend; grafted extra heads need a thick neck and a head ≥ 0.065
  or they look like pipes.
- White coats shaded with the blue-grey COAT tones read as blue; use LABW (neutral white)
  when the user wants no blue.
- Grey hair on a white coat disappears: use a blue-grey. Light-on-light and
  dark-on-black need a tone shift or an outline.
- Weapons held on the far (right) side hide behind the body: bring them toward the
  viewer (`d` > 0.2) or into the left hand.
- `Group.cut` subtracts from the **whole group** — put a hood/cutaway in its own group
  or it will also delete the visor under it.
- Helmets sitting too low hide the face; keep the helmet's lower edge above y≈1.62.
- Thin layered plates: the outer plate's thickness + rounding must stay below the
  inner layers' offset, or the inner stripe/emblem is buried.
- `lean` < 25° barely reads at 35 px; hunched creatures need 30-36° plus a raised
  `nod`.
- Emissive parts get no shading; ink around them uses a darker shade of their own
  colour; use `halo` only on frames with big lights (shots, spells), not for eyes.
- 1-px features (unibrows, buttons, stitches) are noise — the user removed a
  unibrow. Prefer bigger, simpler shapes.
- At 35 px, ink only where a nearer part overlaps a clearly farther one; full
  contour inking turns into noise.
- When the user names a real-world reference (Gundam, Star Wars, a cartoon), make
  it recognisable but use neutral file names; the user renames things to avoid
  clashes.

## User preferences seen so far

- Facing left, always. Accuracy to the user's reference images over sample units.
- Parody looks become generic units: the Rick-like hero was renamed `chaosscientist`
  (brown trousers and belt visible under an open coat, no blue at all). Avoid character
  names in files.
- Realistic proportions, not cartoony.
- Stances copied from Dominions Enhanced; each unit gets an idle and an attack frame.
- Output into the nation folder (`Games/Fantasy Strategy/Dominions 6/Mods/<nation>/`) with the generator script.

## Related skills
dom6-modding, art direction (memory), spritestudio.
Also (2026-11-03): art-direction memory (cheap Dominions-style sprites).
