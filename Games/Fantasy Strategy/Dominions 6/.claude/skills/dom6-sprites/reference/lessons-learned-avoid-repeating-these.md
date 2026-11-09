# dom6-sprites - Lessons learned (avoid repeating these)

Part of the dom6-sprites skill; SKILL.md links here.

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
