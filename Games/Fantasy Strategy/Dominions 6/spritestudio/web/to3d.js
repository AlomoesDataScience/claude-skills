// 2D sprite project -> 3D model. Every pixel becomes part of a block (pixels of one colour
// merged into rectangles), each layer a slab at its own depth with the top layer nearest the
// viewer, each piece a free bone at its joint carrying the piece's 2D pose. Seen straight on
// (yaw 0, pitch 0) the model renders back to the original sprite, pixel for pixel.
import { decoded, layersOK, rankOf, patchHoles, nearMagenta } from "./cutout.js";

const K = 20;                                   // pixels per metre
const r6 = v => Math.round(v * 1e6) / 1e6;
const hex = (r, g, b) => [r, g, b].map(v => v.toString(16).padStart(2, "0")).join("");

// pixels of one colour -> as few rectangles as possible (greedy: run right, then down)
function rects(cells, w, h) {
  const used = new Uint8Array(w * h), out = [];
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const c = cells[y * w + x];
    if (c < 0 || used[y * w + x]) continue;
    let x1 = x;
    while (x1 + 1 < w && cells[y * w + x1 + 1] === c && !used[y * w + x1 + 1]) x1++;
    let y1 = y;
    grow: while (y1 + 1 < h) {
      for (let xx = x; xx <= x1; xx++) if (cells[(y1 + 1) * w + xx] !== c || used[(y1 + 1) * w + xx]) break grow;
      y1++;
    }
    for (let yy = y; yy <= y1; yy++) for (let xx = x; xx <= x1; xx++) used[yy * w + xx] = 1;
    out.push([x, y, x1, y1, c]);
  }
  return out;
}

// 2D pose -> free-bone pose. 2D turns are clockwise on screen (y down) = about -z in 3D;
// a mirror becomes a half turn about y (left-right) or x (up-down). Stretching has no 3D twin.
function bonePose(ps) {
  let rot = ps.rot || 0, [sx, sy] = ps.scale || [1, 1];
  if (sx < 0 && sy < 0) { rot += 180; sx = sy = 1; }
  const out = {};
  if (sx < 0) out.rot = [0, 180, rot];
  else if (sy < 0) out.rot = [180, 0, rot];
  else if (rot) out.rot = [0, 0, -rot];
  const [mx, my] = ps.move || [0, 0];
  if (mx || my) out.move = [r6(mx / K), r6(-my / K), 0];
  return out;
}

/** opt: { look: "flat" | "cel" | "wire", spacing: px between layers, thick: px, flat: true = one layer,
 *         ground: true = render it standing on the ground row (feet 2 px above the bottom) } */
export function toModel(cut, opt) {
  const [w, h] = cut.render.res, cx = w / 2;
  // the ground (y = 0) goes under the figure's lowest pixel, so a sprite that floats on its
  // canvas still stands on the 3D floor; y0 maps it back to the same rows when rendered
  let low = -1;
  for (const f of Object.values(cut.frames)) {
    const src = decoded.get(f.source);
    if (!src) continue;
    for (let i = 0; i < w * h; i++) {
      const r = src.rgb[3 * i], g = src.rgb[3 * i + 1], b = src.rgb[3 * i + 2];
      if ((r || g || b) && !nearMagenta(r, g, b)) low = Math.max(low, (i / w) | 0);
    }
  }
  const y0 = low >= 0 ? low + 1 : h - 2;
  const drop = opt.ground ? h - 2 - y0 : 0;                // rows the rendered sprite moves down
  const X = u => r6((u - cx) / K), Y = v => r6((y0 - v) / K);
  const m = JSON.parse(JSON.stringify(cut));
  layersOK(m);
  const rank = id => opt.flat ? 0 : rankOf(m, id);
  const bodyRank = rank(m.bodyLayer);
  const Z = r => r6(r * opt.spacing / K), half = r6(opt.thick / 2 / K);
  const rc = m.recolor || {};
  const materials = {}, parts = [], bones = [{ name: "body", type: "free", parent: null, pivot: [0, Y(h / 2), Z(bodyRank)] }];
  const frames = {};
  let shadow = null;
  const keys = Object.keys(m.frames);
  const same = keys.every(k => m.frames[k].source === m.frames[keys[0]].source &&
    JSON.stringify(m.frames[k].pieces || []) === JSON.stringify(m.frames[keys[0]].pieces || []));
  const sets = same ? [keys] : keys.map(k => [k]);
  for (const ks of sets) {
    const f = m.frames[ks[0]], src = decoded.get(f.source), pieces = f.pieces || [];
    if (!src) throw new Error(`frame ${ks[0]}'s image is not loaded`);
    const suffix = same ? "" : ` (${ks[0]})`;
    const bone = k => k < 0 ? "body" : pieces[k].name + suffix;
    // bones, parents first
    const done = new Set(), byName = Object.fromEntries(pieces.map((p, k) => [p.name, k]));
    const addBone = (k, depth = 0) => {
      if (done.has(k)) return;
      done.add(k);
      const p = pieces[k], par = p.parent in byName && depth < 32 ? byName[p.parent] : -1;
      if (par >= 0) addBone(par, depth + 1);
      bones.push({ name: bone(k), type: "free", parent: bone(par), pivot: [X(p.pivot[0]), Y(p.pivot[1]), Z(rank(p.layer))] });
    };
    pieces.forEach((_, k) => addBone(k));
    // pixel owners and colours
    const n = w * h, own = new Int16Array(n).fill(-1);
    pieces.forEach((p, k) => p.px.forEach(i => own[i] = k));
    const colour = i => {
      const c = [src.rgb[3 * i], src.rgb[3 * i + 1], src.rgb[3 * i + 2]], to = rc[hex(...c)];
      return to ? [0, 2, 4].map(j => parseInt(to.slice(j, j + 2), 16)) : c;
    };
    const cells = new Map();                         // owner -> colour index per pixel
    const pal = [], palIdx = new Map();
    const put = (key, i, c) => {
      if (!cells.has(key)) cells.set(key, new Int32Array(n).fill(-1));
      const hx = hex(...c);
      if (!palIdx.has(hx)) { palIdx.set(hx, pal.length); pal.push(c); }
      cells.get(key)[i] = palIdx.get(hx);
    };
    let sx0 = 1e9, sy0 = 1e9, sx1 = -1, sy1 = -1;
    for (let i = 0; i < n; i++) {
      const r = src.rgb[3 * i], g = src.rgb[3 * i + 1], b = src.rgb[3 * i + 2];
      if (!r && !g && !b) continue;
      if (nearMagenta(r, g, b)) {                    // the sprite's own shadow becomes the render shadow
        const x = i % w, y = (i / w) | 0;
        sx0 = Math.min(sx0, x); sy0 = Math.min(sy0, y); sx1 = Math.max(sx1, x); sy1 = Math.max(sy1, y);
        continue;
      }
      put(own[i], i, colour(i));
    }
    if (sx1 >= 0 && !shadow) shadow = [sx0, sy0, sx1, sy1];
    // gaps in the body behind pieces that sit on nearer layers, filled so turning them shows no hole
    if (!opt.flat) {
      const rgb = new Uint8Array(n * 3), owner = new Int16Array(n).fill(-2);
      patchHoles(src, own, rgb, owner, w, h, pieces.map(p => rank(p.layer) > bodyRank), pieces);
      for (let i = 0; i < n; i++) if (owner[i] === -1) put("patch", i, colour(i));
    }
    for (const [key, grid] of cells) {
      const k = key === "patch" ? -1 : key, p = pieces[k];
      const z = Z(key === "patch" || k < 0 ? bodyRank : rank(p.layer));
      const name = key === "patch" ? "body fill" : k < 0 ? "body" : p.name;
      rects(grid, w, h).forEach(([x0, yA, x1, yB, ci], j) => {
        const c = pal[ci], mat = "c" + hex(...c);
        materials[mat] ||= { kind: opt.look === "cel" ? "paint" : "flat", color: c.map(v => r6(v / 255)) };
        const part = { name: `${name} ${j + 1}`, type: "box", c: [X((x0 + x1 + 1) / 2), Y((yA + yB + 1) / 2), z],
          half: [r6((x1 - x0 + 1) / 2 / K), r6((yB - yA + 1) / 2 / K), half], rnd: 0, mat, bone: bone(k), group: name + suffix };
        if (!same) part.frames = ks.slice();
        if (p && p.hidden) part.hidden = true;
        parts.push(part);
      });
    }
    for (const fk of ks) {
      const fr = m.frames[fk], pose = {};
      for (const p of fr.pieces || []) {
        const bp = bonePose((fr.pose || {})[p.name] || {});
        if (bp.rot || bp.move) pose[p.name + suffix] = bp;
      }
      frames[fk] = { label: fr.label || fk, pose };
    }
  }
  if (!parts.length) throw new Error("the sprite has no pixels to convert");
  if (shadow && drop) shadow = shadow.map((v, i) => i % 2 ? Math.max(0, Math.min(h - 1, v + drop)) : v);
  const render = { style: opt.look === "wire" ? "wire" : "cel", res: [w, h], px_per_m: K, cx, y0: y0 + drop, yaw: 0, pitch: 0,
    ss: opt.look === "wire" ? 4 : 3, shadow, file: (cut.render.file || cut.name || "sprite") + "_3d", free_rows: 2 };
  if (opt.look === "flat") render.outline = false;
  if (opt.look === "wire") Object.assign(render, { wire_by: "bone", wire_color: "material", hidden: "hide", fill: "material" });
  return { notes: `Converted from the 2D project ${cut.name || ""}: ${parts.length} blocks.`, render, materials, bones, parts, frames };
}
