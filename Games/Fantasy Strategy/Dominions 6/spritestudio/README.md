# Sprite Studio

A local editor for Dominions 6 sprites. You edit a 3D model made of simple shapes: pose
it, recolour it, reshape it. Then you render it to a Dominions-ready TGA and check the
result straight away.

## Start

Double-click **`Sprite Studio.desktop`** (or the **`SpriteStudio`** file) in this folder.
The editor opens in your browser. **Quit** (top right) closes it; it also closes by itself
about 3 minutes after you close the tab. Starting it again while it runs just reopens
the page.

From a terminal, `python3 server.py` runs the same thing from the source files and stops
with Ctrl+C. Either way it needs only Python 3 and Pillow (PIL). three.js is bundled in
`web/vendor/`, so no internet is needed.

### The built app

`python3 tools/build.py` rebuilds `SpriteStudio`, `Sprite Studio.desktop` and `icon.png`.
**Rebuild after changing any code**, because the app carries its own copy. `SpriteStudio`
is one file (a Python zip app). On first run it unpacks itself into
`~/.cache/sprite-studio/` and keeps its models and renders in `models/` and `output/`
next to itself. If you copy it to another folder, it starts there with the killbot as a
starter model, and Export writes into the folder above it. For a menu entry, copy
`Sprite Studio.desktop` to `~/.local/share/applications/`.

## The screen

- **Top bar:** project picker, **New…**, **Import…**, Save / Save as, Undo / Redo, the frame being edited
  (1 Idle, 2 Attack), the view (3D model, Both, Sprite), Render sprite, and Export.
  With auto-render on, the sprite re-renders about half a second after every change: the frame
  you are on first, then any other frame the change affects.
  The killbot renders in under 2 seconds.
- **3D model view:** left-drag orbits, right-drag pans, the wheel zooms. Click a part to
  select it. **Sprite camera** looks through the exact camera the sprite uses, facing
  left. The **Move / Turn** buttons (or the M / R keys) switch the gizmo. Red see-through
  shapes are cuts, blue lines are limbs, yellow dots are hand/foot targets and green dots
  are body, head and prop pivots.
  The **wire** box shows the model as a wireframe.
- **Sprite view:** the rendered TGA at 4-8×. **In game** shows black as transparent and
  magenta as shadow on grass; **Raw** shows the actual file colours.
- **Rotate bar** (above the sprite): turn the model with the slider or the ⟲/⟳ 15° and 45°
  buttons, tilt it with the tilt slider. The label warns when the unit no longer
  faces left, because Dominions uses the facing as the move direction. **Reset** goes
  back to the standard angle (−30°). **Turntable** renders 12 angles side by side for
  the current frame; click one to use it. The angle is saved with the model and applies
  to both frames.

### Left panel tabs

| Tab | What you do there |
|---|---|
| **Parts** | Every shape, grouped by the bone that carries it. Add, Duplicate (Ctrl+D), Mirror (copies to the other side, L↔R), Delete, hide (●). **Add bone** makes a new bone group: it follows the selected part's bone and turns about that part's centre (it shows in the Pose tab); move parts onto it with their **bone** box. |
| **Pose** | Per-frame pose. Body, head and props turn and move with sliders. Arms and legs are IK chains: drag their yellow handle with the gizmo, or set reach (where the hand or foot goes) and bend (which way the elbow or knee points). Feet keep level; tilt them with the foot sliders. |
| **Colors** | One row per material: colour, kind (paint, chrome, glow) and, for paint in studio style, shine, highlight and gloss. |
| **Canvas** | Look (studio = shiny metal like the killbot, cel = painted tones like the nation units, wire = pixel-art wireframe; see below), overall size, canvas size, ground row, shadow ellipse (it moves and scales with the figure when you change size, px/metre, centre x or feet row), camera yaw and pitch, light, quality, output file name, frame labels. |

### Right panel: the selected part

Name, **Shape**, colour, bone, add/cut, which frames it shows in, and its dimensions
in metres.

**Shape** changes a part into another shape (sphere, ellipsoid, capsule, roundcone, box,
torus, disc) at the same size and direction, so a round head becomes a block of the
same size. The **blocky** slider runs from 0% (smooth ellipsoids and capsules) to 100%
(sharp boxes). **Apply to** picks this part, every part on the same bone, or the whole
model. Undo restores the old shapes. Changes preview live in 3D and render on release. The **size** slider scales
the part about its centre, and **turn 15°** rotates it. **Grooves** cut ribs, fins or
teeth across the part; they appear only in the sprite render.

## New projects and importing

**New…** starts a project from:
- **Humanoid (3D):** a rigged person about 33 px tall, with posable arms and legs. Reshape and recolour it into a unit.
- **Empty (3D):** a single block.
- **Copy of the current project.**
- **From a sprite (2D):** see below.

You also pick the look (cel or studio) and the canvas size.

**Import…** takes:
- a Sprite Studio model (`.json`), or
- any Dominions sprite (`.tga` or `.png`). Choose `name1.tga` and `name2.tga` together to get both frames. A single file fills both frames, so you can re-pose the attack from the idle.

  Imported sprites are stood on the ground row (feet 2 px above the bottom, as Dominions
  expects; tick it off to keep the file's placement), and off-magenta shadow such as
  (248, 0, 248) is cleaned to exact magenta. For a project imported earlier, Canvas →
  **Stand on the ground row** does the same, and Convert to 3D has the same checkbox. The
  3D model always stands on the floor; in the 3D view, **Sprite camera** shows exactly the
  render canvas (outlined), so what you see there is where the sprite lands.

  A sprite asks how to come in:
  - **2D sprite:** cut it into pieces and set its layers first, then convert it from Canvas → **Convert to 3D…**.
  - **3D objects, flat:** converted right away, everything on one layer.

## 2D sprite projects (cut-out)

An imported sprite opens in the **Editor** view as a paper doll:

1. **Cut** mode shows the original pixels. Press **New piece**, then paint its pixels:
   - **Brush** (1-3 px) paints them.
   - **Box** drags a rectangle.
   - **Wand** picks a same-coloured area; the slider sets the tolerance.
   - Right-click or **Eraser** gives pixels back to the body.
   - **Joint** sets where the piece turns: a shoulder, an elbow, the hand holding a weapon.

   Each piece gets its own tint. Pixels in no piece are the body and stay put.
2. **Pose** mode: drag a piece to **Turn** it about its joint (Shift snaps to 15°). Use **Move** or **Stretch** instead, or drag the yellow joint to move it. Alt-click selects the piece under the pointer.
3. The right panel has exact numbers:
   - turn in degrees
   - move x, y in pixels
   - **width and height in pixels**
   - flip (mirror left-right)
   - **attached to:** a forearm on the upper arm follows it
   - **fill hole:** patches the gap a moved piece leaves in the body from the colours around it
4. **Paint** mode edits the pixels themselves:
   - **Pencil** (B), **Eraser** (E, paints see-through), **Fill** (G, with a tolerance), **Line** (L), **Rect** (R, outline or filled) and **Pick** (I, or Alt-click any tool).
   - **Select** (M): drag a box, then drag inside it to move those pixels (they keep their piece). The selection can be flipped ↔ or ↕, or cleared (Delete).
   - **Palette:** the frame's own colours, recent colours, a colour picker, and see-through and shadow swatches.
   - Right-click erases. Brush sizes are 1-3 px; Ctrl+Z undoes a stroke.
   - Each frame has its own image, so painting the idle frame leaves the attack frame alone.
5. **Layers** (Pieces tab): every piece, and the body, sits on a layer:
   - The top layer is drawn in front, and is nearest you when the sprite becomes 3D.
   - **+ Layer** adds one; ▲ ▼ reorder; × deletes (its pieces move down a layer); double-click renames.
   - New pieces go on the active layer; the inspector's **layer** moves a piece; **body on** sets the body's layer.
   - Cut mode's **tint: Layers** colours every pixel by its layer.
6. **Colors** lists every colour in the sprite; replace any of them.
7. **Canvas** sets the canvas size, the file name, and each frame's image. **Copy other frame** starts the attack frame from the idle one.

## Sprite to 3D

Canvas → **Convert to 3D…** (or Import → 3D objects) makes a new 3D project from a 2D one:

- **Blocks:** every pixel becomes part of a block; pixels of one colour are merged into rectangles (a 64×64 sprite is about 500 blocks).
- **Layers:** each layer is a slab, set **layer gap** px apart, with the top layer nearest you. **Thickness** is how deep each block is.
- **Pieces → bones:** each piece becomes a bone at its joint. Its 2D turns, moves and flips carry over to both frames. Stretching does not.
- **Gaps:** body gaps behind pieces on nearer layers are filled, so turning a piece shows no hole.
- **Shadow:** the sprite's magenta shadow becomes the render's shadow ellipse.

The **look** can be:
- **wireframe:** the 3D view shows a wireframe; the sprite shows what is in front, in its
  own colours (Canvas → fill "part colours"; pick "none" for a hollow outline sprite).
- **flat colours:** `flat` materials, no outline. Seen straight on (turn 0°, tilt 0°), the render matches the original sprite pixel for pixel, apart from the shadow's shape.
- **cel shaded:** painted materials that shade on their sides when turned.

The new project starts straight on; use the rotate bar to turn it.

Turned pieces are re-pixelated RotSprite-style: Scale2x three times, then sampled. Moves by whole pixels, 90° turns and flips copy the pixels exactly. Pieces are cut per frame, because the idle and attack images differ.

## Canvas size

Canvas → **canvas** offers the sizes Dominions accepts: square 8, 16, 32, 64 or 128 px. Humans use 64; size 4+ monsters use 128. **Resizing** decides what happens to the unit:
- *keep the model's size* adds or trims room around it (feet stay on the ground row).
- *grow or shrink the model* scales it with the canvas.

For 2D projects, the same two choices pad or stretch the pixels.

## Wireframe look

Canvas → style **wire** draws a 1-pixel outline around each piece instead of shading.

- **lines:** each part's own colour, or one colour for everything.
- **outline:** each piece (parts cut or merged together), each bone, or every single part.
- **hidden:** what happens to lines of parts behind other parts. They can be dimmed
  (by "dim to"), shown at full strength, or left out.
- **fill:** none leaves the sprite hollow (lines only). **Part colours** paints whatever is
  in front in its own colour, so a converted sprite renders as its original pixels (only
  hidden lines are drawn over it). **One colour** paints the body behind the lines: dark
  blue with cyan lines makes a hologram.

## Files

```
SpriteStudio           the built app (tools/build.py); Sprite Studio.desktop + icon.png launch it
server.py              local web server (models, renders, export)
engine/sdf.py          shapes (signed distance functions), copied from the killbot generator
engine/model.py        model files -> posed scene (bones, IK, cuts)
engine/render.py       ray marcher + sprite post-processing; also a command line:
                         python3 -I engine/render.py models/killbot.json 1 out.tga [--ss=5]
web/                   the page (index.html, app.js, cutout.js = 2D projects, to3d.js = sprite to 3D,
                       style.css, vendor/three.js)
models/<name>.json     your models; each save keeps the previous version in models/.history/
output/<name>/         renders: <file>1.tga, <file>2.tga (+ .png previews)
tools/import_killbot.py  converts ../killbot/killbot.py into models/killbot.json
tools/build.py, tools/launcher.py  build the SpriteStudio app
tools/release.py       packages dist/SpriteStudio-<version>-linux.zip and -windows.zip for release
                       (MANUAL.md is made from this README without the developer sections). The
                       Windows zip bundles the embeddable Python 3.14 + Pillow (downloaded once
                       into .downloads/, SHA-256 pinned) and starts via "Sprite Studio.bat" ->
                       python\pythonw.exe app\start.py (tools/winstart.py). The renderer uses
                       spawn workers where fork is missing; SPRITESTUDIO_SPAWN=1 tests that on Linux.
```

**Export…** copies the frame TGAs into a folder you name inside `Dominions 6/` (the folder above spritestudio)
(e.g. `killbot`). It overwrites files with the same name there.

## Model file format

```jsonc
{
  "render":   { "style": "studio", "res": [64, 64], "px_per_m": 18.085, "scale": 1, ... },
  "materials": { "chrome": { "kind": "chrome", "color": [0.95, 0.97, 1.0] }, ... },
  "bones": [
    { "name": "body", "type": "free", "parent": null, "pivot": [0, 0.95, 0] },
    { "name": "leg.L", "type": "ik", "parent": "body", "root": [0.1, 0.95, 0],
      "target": [0.19, 0.085, 0.13], "pole": [0.15, 0, 1], "l1": 0.45, "l2": 0.44,
      "bones": ["thigh.L", "shin.L"], "end": "foot.L" },
    { "name": "arm.R", "type": "ik", ..., "target": { "bone": "gun", "point": [...] } }
  ],
  "parts": [
    { "name": "head brow ridge", "type": "capsule", "a": [...], "b": [...], "r": 0.016,
      "mat": "chrome", "bone": "head", "op": "add", "frames": ["2"] }
  ],
  "frames": { "1": { "label": "Idle", "pose": {} },
              "2": { "label": "Attack", "pose": { "gun": { "rot": [0, -20, 25] } } } }
}
```

Wireframe settings live in `render` too: `"style": "wire"`, `"wire_color": "material" | [r,g,b]`,
`"wire_by": "group" | "bone" | "part"`, `"hidden": "dim" | "show" | "hide"`,
`"hidden_dim": 0.42`, `"fill": null | "material" | [r,g,b]`.

Coordinates are metres: y is up, x is the unit's left, z is its front, and the feet
stand at y = 0. Parts are written in the rest pose; bones carry them into each frame's
pose. Shape types are sphere, ellipsoid, capsule, roundcone, box, torus, disc, cylinder,
cone (r2 = 0 is pointed), tube (hollow, `wall` thick), dome (half sphere on `c`, bulging
along `axis`), wedge (a box with its top front edge cut off), pyramid and hexprism (`r` to
the corners, `thick` along its own y). A
part with `"op": "cut"` removes material from the parts listed before it in the same
cut group. `"pin": [r, g, b]` forces one pixel of a tiny light, such as an eye, to that
colour so it survives shrinking to 64 px.

## Testing hook

`index.html?wait=9000` holds the page's load event for 9 s and copies the 3D canvas into
an image. Headless Firefox screenshots skip WebGL canvases, so this lets them capture
the 3D view. Other URL options: `model=`, `tab=`, `sel=`, `view=`, `cam=sprite`,
`wire=1` (3D wireframe), `turntable=1`, `frame=2`, `new=1` (open the New dialog), and for 2D
projects `mode=cut|pose|paint`, `piece=N`, `tool=wand`, `tint=layer`, `convert=1`,
`color=r,g,b`, `sel=x0,y0,x1,y1`, `drag=x0,y0,x1,y1` (sends a real pointer drag, in pixels). Turntable previews go to `output/<name>/preview/`.

## Planned next

- Import the mad-science units (cel style) from `madscience/units.py`.
