# dom6-sprites - Rig API (rig.py)

Part of the dom6-sprites skill; SKILL.md links here.

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
