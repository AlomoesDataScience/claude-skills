// 2D cut-out projects: an imported sprite cut into pieces (a paper doll). Pieces turn, move
// and stretch about their joints, and the result is re-pixelated (RotSprite style:
// Scale2x three times, then sampled) into a new sprite of the same canvas.
//
// Model: { kind: "cutout", render: { res: [w, h], file }, recolor: { "rrggbb": "rrggbb" },
//   frames: { "1": { label, source: <PNG data URL>, pieces: [piece], pose: { name: pose } } } }
// piece: { name, px: [pixel index y*w+x], pivot: [x, y] (pixel units), parent: name | null,
//          patch: true (fill the hole the piece leaves behind), hidden }
// pose:  { rot: degrees clockwise, move: [dx, dy] pixels in the parent's space, scale: [sx, sy] }
// layers: [{ id, name }] listed top first; the top layer is drawn in front and ends up nearest
//   the viewer when the sprite is converted to 3D. piece.layer = id; bodyLayer = the layer of
//   the pixels in no piece.

let C;                                   // helpers handed over by app.js
const T = { mode: "pose", tool: "turn", cutTool: "brush", brush: 1, tol: 30, piece: -1, drag: null, box: null,
  paintTool: "pencil", color: [224, 160, 64], recent: [], fillTol: 0, rectFill: false, intoPiece: false,
  sel: null, work: null, base: null, touched: null, hover: null, saving: false, layer: null, tint: "piece" };
const HUES = ["#e0a040", "#5aa9e6", "#6cc070", "#e0605a", "#b77de8", "#4fd1c5", "#f0d050", "#e87db7", "#9aa0ff", "#c0a080"];
export const isCut = m => !!m && m.kind === "cutout";

// ------------------------------------------------------------------ images
const decoded = new Map();               // data URL -> { w, h, rgb, id }
let nextId = 1;
export async function decodeURL(url) {
  if (decoded.has(url)) return decoded.get(url);
  const img = await new Promise((ok, bad) => {
    const i = new Image(); i.onload = () => ok(i); i.onerror = () => bad(new Error("could not read the image")); i.src = url;
  });
  const c = document.createElement("canvas");
  c.width = img.width; c.height = img.height;
  const g = c.getContext("2d");
  g.drawImage(img, 0, 0);
  const d = g.getImageData(0, 0, c.width, c.height).data;
  const rgb = new Uint8Array(c.width * c.height * 3);
  for (let i = 0, j = 0; i < d.length; i += 4, j += 3) { rgb[j] = d[i]; rgb[j + 1] = d[i + 1]; rgb[j + 2] = d[i + 2]; }
  const v = { w: c.width, h: c.height, rgb, id: nextId++ };
  decoded.set(url, v);
  return v;
}
function rgbCanvas(w, h, rgb) {
  const c = document.createElement("canvas");
  c.width = w; c.height = h;
  const g = c.getContext("2d"), im = g.createImageData(w, h);
  for (let i = 0, j = 0; j < rgb.length; i += 4, j += 3) { im.data[i] = rgb[j]; im.data[i + 1] = rgb[j + 1]; im.data[i + 2] = rgb[j + 2]; im.data[i + 3] = 255; }
  g.putImageData(im, 0, 0);
  return c;
}
async function rgbURL(w, h, rgb) {
  const url = rgbCanvas(w, h, rgb).toDataURL("image/png");
  await decodeURL(url);
  return url;
}
export async function prepare(model) {
  for (const f of Object.values(model.frames)) if (f.source) await decodeURL(f.source);
}
const empty = (rgb, i) => rgb[3 * i] === 0 && rgb[3 * i + 1] === 0 && rgb[3 * i + 2] === 0;
export const nearMagenta = (r, g, b) => r >= 230 && b >= 230 && g <= 30;      // shadow, even if saved slightly off
const isShadow = (rgb, i) => nearMagenta(rgb[3 * i], rgb[3 * i + 1], rgb[3 * i + 2]);
const hex = (rgb, i) => [rgb[3 * i], rgb[3 * i + 1], rgb[3 * i + 2]].map(v => v.toString(16).padStart(2, "0")).join("");

// ------------------------------------------------------------------ model helpers
const M = () => C.S.model;
const F = (k = C.S.frame) => M().frames[k];
const res = () => M().render.res;
function frameOK(f) {
  f.pieces ||= []; f.pose ||= {};
  return f;
}
const poseOf = (f, name) => f.pose[name] || {};
export function layersOK(m = M()) {
  if (!m.layers || !m.layers.length) m.layers = [{ id: "l1", name: "Layer 1" }];
  if (!m.layers.some(l => l.id === m.bodyLayer)) m.bodyLayer = m.layers[m.layers.length - 1].id;
  return m.layers;
}
export function rankOf(m, id) {                   // 0 = bottom layer; higher = nearer the viewer
  const ls = layersOK(m);
  let i = ls.findIndex(l => l.id === id);
  if (i < 0) i = ls.findIndex(l => l.id === m.bodyLayer);
  return ls.length - 1 - i;
}
function ensurePose(f, name) { return f.pose[name] || (f.pose[name] = {}); }

// ------------------------------------------------------------------ 2D transforms [a, b, c, d, e, f]: x' = a x + c y + e, y' = b x + d y + f
const ID = [1, 0, 0, 1, 0, 0];
function localT(p, ps) {
  const r = (ps.rot || 0) * Math.PI / 180, [sx, sy] = ps.scale || [1, 1], [mx, my] = ps.move || [0, 0];
  const cs = Math.cos(r), sn = Math.sin(r), [px, py] = p.pivot;
  const a = cs * sx, b = sn * sx, c = -sn * sy, d = cs * sy;
  return [a, b, c, d, px + mx - (a * px + c * py), py + my - (b * px + d * py)];
}
const mulT = (P, L) => [P[0] * L[0] + P[2] * L[1], P[1] * L[0] + P[3] * L[1], P[0] * L[2] + P[2] * L[3],
  P[1] * L[2] + P[3] * L[3], P[0] * L[4] + P[2] * L[5] + P[4], P[1] * L[4] + P[3] * L[5] + P[5]];
const apply = (t, x, y) => [t[0] * x + t[2] * y + t[4], t[1] * x + t[3] * y + t[5]];
function invert(t) {
  const det = t[0] * t[3] - t[1] * t[2] || 1e-12;
  const a = t[3] / det, b = -t[1] / det, c = -t[2] / det, d = t[0] / det;
  return [a, b, c, d, -(a * t[4] + c * t[5]), -(b * t[4] + d * t[5])];
}
const near = (a, b) => Math.abs(a - b) < 1e-6;
const isId = t => near(t[0], 1) && near(t[1], 0) && near(t[2], 0) && near(t[3], 1) && near(t[4], 0) && near(t[5], 0);
export function worldTs(f) {
  const out = {}, byName = Object.fromEntries(f.pieces.map(p => [p.name, p]));
  const get = (p, depth) => {
    if (out[p.name]) return out[p.name];
    const par = p.parent && byName[p.parent] && depth < 32 ? get(byName[p.parent], depth + 1) : ID;
    return (out[p.name] = mulT(par, localT(p, poseOf(f, p.name))));
  };
  f.pieces.forEach(p => get(p, 0));
  return out;
}

// ------------------------------------------------------------------ re-pixelation
function scale2x(src, w, h) {
  const out = new Int32Array(w * h * 4), W = w * 2;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const P = src[y * w + x];
    const A = y > 0 ? src[(y - 1) * w + x] : -1, D = y < h - 1 ? src[(y + 1) * w + x] : -1;
    const L = x > 0 ? src[y * w + x - 1] : -1, R = x < w - 1 ? src[y * w + x + 1] : -1;
    let e0 = P, e1 = P, e2 = P, e3 = P;
    if (A !== D && L !== R) { e0 = L === A ? A : P; e1 = A === R ? R : P; e2 = L === D ? L : P; e3 = D === R ? R : P; }
    const o = 2 * y * W + 2 * x;
    out[o] = e0; out[o + 1] = e1; out[o + W] = e2; out[o + W + 1] = e3;
  }
  return out;
}
const upCache = new Map();
function hashPx(px) { let h = 2166136261; for (const v of px) h = Math.imul(h ^ v, 16777619); return (h >>> 0) + ":" + px.length; }
function upsample(src, px, w) {               // the piece alone, 8x larger, cropped to its box
  const key = src.id + "|" + hashPx(px);
  if (upCache.has(key)) return upCache.get(key);
  let x0 = 1e9, y0 = 1e9, x1 = -1, y1 = -1;
  for (const i of px) { const x = i % w, y = (i / w) | 0; x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y); }
  const bw = x1 - x0 + 1, bh = y1 - y0 + 1;
  let img = new Int32Array(bw * bh).fill(-1);
  for (const i of px) {
    if (empty(src.rgb, i)) continue;
    const x = i % w - x0, y = ((i / w) | 0) - y0;
    img[y * bw + x] = (src.rgb[3 * i] << 16) | (src.rgb[3 * i + 1] << 8) | src.rgb[3 * i + 2];
  }
  let W = bw, H = bh;
  for (let k = 0; k < 3; k++) { img = scale2x(img, W, H); W *= 2; H *= 2; }
  const v = { x0, y0, bw, bh, img, W };
  if (upCache.size > 200) upCache.clear();
  upCache.set(key, v);
  return v;
}

// fill the hole a moved piece leaves, from the base pixels around it (only inside the body:
// both sides along a row, or both ends along a column, must be base pixels)
export function patchHoles(src, own, rgb, owner, w, h, moved, pieces) {
  const base = i => own[i] < 0 && !empty(src.rgb, i);
  const fills = [];
  for (let i = 0; i < w * h; i++) {
    const k = own[i];
    if (k < 0 || !moved[k] || pieces[k].patch === false) continue;
    const x = i % w, y = (i / w) | 0;
    const look = (dx, dy) => {
      for (let s = 1; s <= 10; s++) {
        const xx = x + dx * s, yy = y + dy * s;
        if (xx < 0 || yy < 0 || xx >= w || yy >= h) return null;
        const j = yy * w + xx;
        if (own[j] >= 0) continue;
        return base(j) ? [j, s] : null;
      }
      return null;
    };
    const l = look(-1, 0), r = look(1, 0), u = look(0, -1), d = look(0, 1);
    const cand = [];
    if (l && r) cand.push(l, r);
    if (u && d) cand.push(u, d);
    if (cand.length) fills.push([i, cand.reduce((a, b) => b[1] < a[1] ? b : a)[0]]);
  }
  for (const [i, j] of fills) { rgb[3 * i] = src.rgb[3 * j]; rgb[3 * i + 1] = src.rgb[3 * j + 1]; rgb[3 * i + 2] = src.rgb[3 * j + 2]; owner[i] = -1; }
}

// the posed sprite of one frame: rgb (black = transparent), owner (-2 empty, -1 base, k piece)
export function compose(key, model = M()) {
  const f = frameOK(model.frames[key]);
  const src = decoded.get(f.source);
  if (!src) return null;
  const [w, h] = [src.w, src.h], n = w * h;
  const rgb = new Uint8Array(n * 3), owner = new Int16Array(n).fill(-2), own = new Int16Array(n).fill(-1);
  f.pieces.forEach((p, k) => { for (const i of p.px) if (i >= 0 && i < n) own[i] = k; });
  for (let i = 0; i < n; i++) if (own[i] < 0 && !empty(src.rgb, i)) {
    rgb[3 * i] = src.rgb[3 * i]; rgb[3 * i + 1] = src.rgb[3 * i + 1]; rgb[3 * i + 2] = src.rgb[3 * i + 2]; owner[i] = -1;
  }
  const Ts = worldTs(f);
  const moved = f.pieces.map(p => p.hidden || !isId(Ts[p.name]));
  patchHoles(src, own, rgb, owner, w, h, moved, f.pieces);
  const rank = f.pieces.map(p => rankOf(model, p.layer)), bodyRank = rankOf(model, model.bodyLayer);
  const order = f.pieces.map((_, k) => k).sort((a, b) => rank[a] - rank[b] || a - b);   // lower layers first
  order.forEach(k => {
    const p = f.pieces[k];
    if (p.hidden) return;
    const px = p.px.filter(i => own[i] === k);
    if (!px.length) return;
    const t = Ts[p.name];
    const put = (o, r, g, b) => {
      const ow = owner[o];
      if (ow !== -2 && (ow === -1 ? bodyRank : rank[ow]) > rank[k]) return;          // a higher layer is already there
      rgb[3 * o] = r; rgb[3 * o + 1] = g; rgb[3 * o + 2] = b; owner[o] = k;
    };
    const tx = t[4], ty = t[5];
    if (near(t[0], 1) && near(t[1], 0) && near(t[2], 0) && near(t[3], 1) && near(tx, Math.round(tx)) && near(ty, Math.round(ty))) {
      const dx = Math.round(tx), dy = Math.round(ty);                // whole-pixel move: copy exactly
      for (const i of px) {
        if (empty(src.rgb, i)) continue;
        const x = i % w + dx, y = ((i / w) | 0) + dy;
        if (x >= 0 && y >= 0 && x < w && y < h) put(y * w + x, src.rgb[3 * i], src.rgb[3 * i + 1], src.rgb[3 * i + 2]);
      }
      return;
    }
    const up = upsample(src, px, w), inv = invert(t);
    const cs = [[up.x0, up.y0], [up.x0 + up.bw, up.y0], [up.x0, up.y0 + up.bh], [up.x0 + up.bw, up.y0 + up.bh]].map(([x, y]) => apply(t, x, y));
    const X0 = Math.max(0, Math.floor(Math.min(...cs.map(c => c[0])))), X1 = Math.min(w - 1, Math.ceil(Math.max(...cs.map(c => c[0]))));
    const Y0 = Math.max(0, Math.floor(Math.min(...cs.map(c => c[1])))), Y1 = Math.min(h - 1, Math.ceil(Math.max(...cs.map(c => c[1]))));
    const mine = new Set(px);
    for (let y = Y0; y <= Y1; y++) for (let x = X0; x <= X1; x++) {
      const [u, v] = apply(inv, x + 0.5, y + 0.5);
      const fu = u - 0.5, fv = v - 0.5;
      if (near(fu, Math.round(fu)) && near(fv, Math.round(fv))) {        // lands on a pixel centre: take it as is
        const sx = Math.round(fu), sy = Math.round(fv), i = sy * w + sx;
        if (sx >= 0 && sy >= 0 && sx < w && sy < h && mine.has(i) && !empty(src.rgb, i)) put(y * w + x, src.rgb[3 * i], src.rgb[3 * i + 1], src.rgb[3 * i + 2]);
        continue;
      }
      const ux = Math.floor((u - up.x0) * 8), vy = Math.floor((v - up.y0) * 8);
      if (ux < 0 || vy < 0 || ux >= up.W || vy >= up.bh * 8) continue;
      const c = up.img[vy * up.W + ux];
      if (c >= 0) put(y * w + x, c >> 16, (c >> 8) & 255, c & 255);
    }
  });
  const rc = model.recolor || {};
  if (Object.keys(rc).length) {
    for (let i = 0; i < n; i++) {
      if (owner[i] === -2) continue;
      const to = rc[hex(rgb, i)];
      if (!to) continue;
      let c = [0, 2, 4].map(k => parseInt(to.slice(k, k + 2), 16));
      if (c[0] === 0 && c[1] === 0 && c[2] === 0) c = [1, 1, 1];          // pure black would turn see-through
      rgb[3 * i] = c[0]; rgb[3 * i + 1] = c[1]; rgb[3 * i + 2] = c[2];
    }
  }
  return { w, h, rgb, owner, Ts };
}
export function spriteImage(key) { const c = compose(key); return c && rgbCanvas(c.w, c.h, c.rgb); }

export async function writeSprite(key) {
  const c = compose(key);
  if (!c) throw new Error("frame image not loaded");
  let bin = "";
  for (let i = 0; i < c.rgb.length; i += 0x8000) bin += String.fromCharCode(...c.rgb.subarray(i, i + 0x8000));
  const r = M().render;
  const j = await C.api("/api/sprite", { name: C.S.name, frame: key, file: r.file || C.S.name, w: c.w, h: c.h, rgb: btoa(bin) });
  C.S.sprites[key] = { img: rgbCanvas(c.w, c.h, c.rgb), tga: j.tga, seconds: 0 };
  return j;
}
export function composeAll() {
  for (const k of Object.keys(M().frames)) {
    const img = spriteImage(k);
    if (img) C.S.sprites[k] = { img, tga: (C.S.sprites[k] || {}).tga || "not written yet", seconds: 0 };
  }
}

// ------------------------------------------------------------------ new projects
// Dominions sprites stand with their feet two rows above the bottom of the canvas (the shadow
// may use those rows). A sprite that floats higher, or sinks lower, is moved straight up or down
// to stand there; all frames move together so idle and attack stay lined up.
function groundShift(srcs, w, h) {
  let fig = -1, sh = -1;
  for (const s of srcs) for (let i = 0; i < w * h; i++) {
    if (empty(s.rgb, i)) continue;
    const y = (i / w) | 0;
    if (isShadow(s.rgb, i)) sh = Math.max(sh, y); else fig = Math.max(fig, y);
  }
  if (fig < 0) return 0;
  return sh >= 0 ? Math.min(h - 3 - fig, h - 1 - sh) : h - 3 - fig;
}
/** Moves every frame of a 2D project (pixels, pieces, joints) so it stands on the ground row,
 * and makes near-magenta shadow exact. Returns how many rows it moved (+ = down). */
export async function placeOnGround(model = M()) {
  const [w, h] = model.render.res, frames = Object.values(model.frames).map(frameOK);
  const srcs = frames.map(f => decoded.get(f.source));
  if (srcs.some(s => !s)) throw new Error("a frame's image is not loaded");
  const dy = groundShift(srcs, w, h), urls = new Map();
  for (const f of frames) {
    if (!urls.has(f.source)) {
      const src = decoded.get(f.source), out = new Uint8Array(w * h * 3);
      for (let i = 0; i < w * h; i++) {
        const y = ((i / w) | 0) + dy;
        if (y < 0 || y >= h || empty(src.rgb, i)) continue;
        const o = 3 * (y * w + i % w);
        if (isShadow(src.rgb, i)) out.set([255, 0, 255], o); else out.set(src.rgb.subarray(3 * i, 3 * i + 3), o);
      }
      urls.set(f.source, await rgbURL(w, h, out));
    }
    f.source = urls.get(f.source);
    for (const p of f.pieces) {
      p.px = p.px.map(i => i + dy * w).filter(i => i >= 0 && i < w * h);
      p.pivot = [p.pivot[0], p.pivot[1] + dy];
    }
  }
  return dy;
}

export async function cutoutModel(name, images, opt = {}) {
  // images: [{ frame, url }] (decoded data URLs). One image fills both frames.
  const dec = await Promise.all(images.map(i => decodeURL(i.url)));
  const { w, h } = dec[0];
  if (dec.some(d => d.w !== w || d.h !== h)) throw new Error("the idle and attack images have different sizes");
  const byFrame = {};
  images.forEach(i => byFrame[i.frame] = i.url);
  if (!byFrame["1"]) byFrame["1"] = images[0].url;
  if (!byFrame["2"]) byFrame["2"] = byFrame["1"];
  const label = k => ({ 1: "Idle", 2: "Attack" })[k] || k;
  const model = {
    kind: "cutout", name, render: { res: [w, h], file: name }, recolor: {},
    frames: Object.fromEntries(Object.keys(byFrame).sort().map(k => [k, { label: label(k), source: byFrame[k], pieces: [], pose: {} }])),
  };
  if (opt.ground) await placeOnGround(model);
  return model;
}

// ------------------------------------------------------------------ canvas size
// "pad": keep the pixels, add/remove border (centred, feet stay at the bottom).
// "scale": stretch the sprite to the new size (whole pixels when doubling).
export async function resizeCanvas(n, how) {
  const [w, h] = res();
  if (n === w && n === h) return;
  C.beginEdit();
  const kx = n / w, ky = n / h, dx = Math.floor((n - w) / 2), dy = n - h;
  const from = (x, y) => {
    const sx = how === "scale" ? Math.floor((x + 0.5) / kx) : x - dx, sy = how === "scale" ? Math.floor((y + 0.5) / ky) : y - dy;
    return sx >= 0 && sy >= 0 && sx < w && sy < h ? sy * w + sx : -1;
  };
  for (const f of Object.values(M().frames)) {
    frameOK(f);
    const src = decoded.get(f.source);
    const rgb = new Uint8Array(n * n * 3), own = new Int16Array(w * h).fill(-1);
    f.pieces.forEach((p, k) => p.px.forEach(i => own[i] = k));
    const px = f.pieces.map(() => []);
    for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) {
      const o = from(x, y);
      if (o < 0) continue;
      const i = y * n + x;
      rgb[3 * i] = src.rgb[3 * o]; rgb[3 * i + 1] = src.rgb[3 * o + 1]; rgb[3 * i + 2] = src.rgb[3 * o + 2];
      if (own[o] >= 0) px[own[o]].push(i);
    }
    f.source = await rgbURL(n, n, rgb);
    f.pieces.forEach((p, k) => {
      p.px = px[k];
      p.pivot = how === "scale" ? [p.pivot[0] * kx, p.pivot[1] * ky] : [p.pivot[0] + dx, p.pivot[1] + dy];
    });
    if (how === "scale") for (const ps of Object.values(f.pose)) if (ps.move) ps.move = [Math.round(ps.move[0] * kx), Math.round(ps.move[1] * ky)];
  }
  M().render.res = [n, n];
  C.commit("canvas size");
}

// ------------------------------------------------------------------ editor view
const $ = s => document.querySelector(s);
let view = { z: 8, ox: 0, oy: 0 };
let live = null;                          // composite being dragged (current frame)
export function draw() {
  const cv = $("#c2d");
  if (!cv || !M() || !isCut(M())) return;
  const dpr = window.devicePixelRatio || 1;
  const cw = cv.clientWidth, ch = cv.clientHeight;
  if (!cw || !ch) return;
  if (cv.width !== Math.round(cw * dpr) || cv.height !== Math.round(ch * dpr)) { cv.width = Math.round(cw * dpr); cv.height = Math.round(ch * dpr); }
  const g = cv.getContext("2d");
  g.setTransform(dpr, 0, 0, dpr, 0, 0);
  g.imageSmoothingEnabled = false;
  g.fillStyle = "#101114"; g.fillRect(0, 0, cw, ch);
  const f = frameOK(F()), [w, h] = res();
  const z = Math.max(1, Math.floor(Math.min((cw - 40) / w, (ch - 70) / h)));
  view = { z, ox: Math.round((cw - w * z) / 2), oy: Math.round((ch - h * z) / 2 + 14) };
  const { ox, oy } = view;
  for (let y = 0; y < h; y += 4) for (let x = 0; x < w; x += 4) {          // checkerboard = transparent
    g.fillStyle = ((x + y) / 4) % 2 ? "#26282f" : "#1d1f25";
    g.fillRect(ox + x * z, oy + y * z, 4 * z, 4 * z);
  }
  const src = decoded.get(f.source);
  if (!src) return;
  const cut = T.mode === "cut", paint = T.mode === "paint";
  const comp = cut || paint ? null : (live || compose(C.S.frame));
  const pix = paint ? (T.work || src.rgb) : cut ? src.rgb : comp.rgb;
  const im = g.createImageData(w, h);
  for (let i = 0; i < w * h; i++) {
    if (empty(pix, i)) continue;
    const sh = isShadow(pix, i);
    im.data[4 * i] = sh ? 120 : pix[3 * i]; im.data[4 * i + 1] = sh ? 40 : pix[3 * i + 1]; im.data[4 * i + 2] = sh ? 120 : pix[3 * i + 2];
    im.data[4 * i + 3] = sh ? 140 : 255;
  }
  const off = document.createElement("canvas");
  off.width = w; off.height = h;
  off.getContext("2d").putImageData(im, 0, 0);
  g.drawImage(off, ox, oy, w * z, h * z);
  const Ts = comp ? comp.Ts : null;
  if (paint) { drawPaintOverlay(g, w, h); return; }
  if (cut && T.tint === "layer") {                                      // tint every pixel by its layer
    const ls = layersOK(), own = ownMap(), hue = id => HUES[Math.max(0, ls.findIndex(l => l.id === id)) % HUES.length];
    g.globalAlpha = 0.45;
    for (let i = 0; i < w * h; i++) {
      if (empty(src.rgb, i) || isShadow(src.rgb, i)) continue;
      g.fillStyle = hue(own[i] >= 0 ? f.pieces[own[i]].layer || M().bodyLayer : M().bodyLayer);
      g.fillRect(ox + (i % w) * z, oy + ((i / w) | 0) * z, z, z);
    }
    g.globalAlpha = 1;
  } else if (cut) {                                                     // tint each piece's pixels
    f.pieces.forEach((p, k) => {
      g.fillStyle = HUES[k % HUES.length];
      g.globalAlpha = k === T.piece ? 0.6 : 0.35;
      for (const i of p.px) g.fillRect(ox + (i % w) * z, oy + ((i / w) | 0) * z, z, z);
    });
    g.globalAlpha = 1;
  } else if (T.piece >= 0 && f.pieces[T.piece]) {                       // outline the selected piece
    g.strokeStyle = "#ffd080"; g.lineWidth = 1;
    g.beginPath();
    for (let i = 0; i < w * h; i++) {
      if (comp.owner[i] !== T.piece) continue;
      const x = i % w, y = (i / w) | 0, X = ox + x * z, Y = oy + y * z;
      if (x === 0 || comp.owner[i - 1] !== T.piece) { g.moveTo(X + 0.5, Y); g.lineTo(X + 0.5, Y + z); }
      if (x === w - 1 || comp.owner[i + 1] !== T.piece) { g.moveTo(X + z - 0.5, Y); g.lineTo(X + z - 0.5, Y + z); }
      if (y === 0 || comp.owner[i - w] !== T.piece) { g.moveTo(X, Y + 0.5); g.lineTo(X + z, Y + 0.5); }
      if (y === h - 1 || comp.owner[i + w] !== T.piece) { g.moveTo(X, Y + z - 0.5); g.lineTo(X + z, Y + z - 0.5); }
    }
    g.stroke();
  }
  // joints and the links to their parents
  const jointAt = p => cut ? p.pivot : apply(Ts[p.name], p.pivot[0], p.pivot[1]);
  const byName = Object.fromEntries(f.pieces.map(p => [p.name, p]));
  g.lineWidth = 2; g.strokeStyle = "#5aa9e6aa";
  for (const p of f.pieces) {
    const q = byName[p.parent];
    if (!q) continue;
    const [ax, ay] = jointAt(p), [bx, by] = jointAt(q);
    g.beginPath(); g.moveTo(ox + ax * z, oy + ay * z); g.lineTo(ox + bx * z, oy + by * z); g.stroke();
  }
  f.pieces.forEach((p, k) => {
    const [x, y] = jointAt(p);
    g.beginPath(); g.arc(ox + x * z, oy + y * z, k === T.piece ? 6 : 4, 0, Math.PI * 2);
    g.fillStyle = k === T.piece ? "#ffd040" : HUES[k % HUES.length]; g.fill();
    g.strokeStyle = "#000a"; g.lineWidth = 1.5; g.stroke();
  });
  if (T.box) {
    const [x0, y0, x1, y1] = T.box;
    g.strokeStyle = "#ffd080"; g.setLineDash([4, 3]);
    g.strokeRect(ox + Math.min(x0, x1) * z, oy + Math.min(y0, y1) * z, (Math.abs(x1 - x0) + 1) * z, (Math.abs(y1 - y0) + 1) * z);
    g.setLineDash([]);
  }
  g.fillStyle = "#9a9ca5"; g.font = "12px system-ui";
  g.fillText(`${w}×${h} px · ${cut ? "Cut: showing the original pixels" : "Pose"} · zoom ${z}×`, ox, oy + h * z + 16);
}

function drawPaintOverlay(g, w, h) {
  const { z, ox, oy } = view;
  if (z >= 6) {                                                         // pixel grid
    g.strokeStyle = "#ffffff14"; g.lineWidth = 1;
    g.beginPath();
    for (let x = 0; x <= w; x++) { g.moveTo(ox + x * z + 0.5, oy); g.lineTo(ox + x * z + 0.5, oy + h * z); }
    for (let y = 0; y <= h; y++) { g.moveTo(ox, oy + y * z + 0.5); g.lineTo(ox + w * z, oy + y * z + 0.5); }
    g.stroke();
  }
  if (T.hover && !T.drag && ["pencil", "eraser", "line", "rect"].includes(T.paintTool)) {
    const r = T.brush, x0 = T.hover[0] - ((r - 1) >> 1), y0 = T.hover[1] - ((r - 1) >> 1);
    g.strokeStyle = "#ffd080"; g.lineWidth = 1;
    g.strokeRect(ox + x0 * z + 0.5, oy + y0 * z + 0.5, r * z - 1, r * z - 1);
  }
  if (T.sel) {
    const [x0, y0, x1, y1] = T.sel;
    g.strokeStyle = "#ffffff"; g.setLineDash([4, 3]); g.lineWidth = 1;
    g.strokeRect(ox + x0 * z + 0.5, oy + y0 * z + 0.5, (x1 - x0 + 1) * z - 1, (y1 - y0 + 1) * z - 1);
    g.strokeStyle = "#000"; g.lineDashOffset = 3.5;
    g.strokeRect(ox + x0 * z + 0.5, oy + y0 * z + 0.5, (x1 - x0 + 1) * z - 1, (y1 - y0 + 1) * z - 1);
    g.setLineDash([]); g.lineDashOffset = 0;
  }
  g.fillStyle = "#9a9ca5"; g.font = "12px system-ui";
  const at = T.hover ? ` · pixel ${T.hover[0]}, ${T.hover[1]}` : "";
  g.fillText(`${w}×${h} px · Paint: editing frame ${C.S.frame}'s pixels · zoom ${z}×${at}`, ox, oy + h * z + 16);
}

// ------------------------------------------------------------------ paint mode
// Edits the frame's own pixels. Black (0,0,0) is see-through and magenta is shadow in
// Dominions, so the eraser paints black and picked pure black becomes (10,10,10).
const EMPTY = [0, 0, 0], SHADOW = [255, 0, 255];
const sameC = (a, b) => a[0] === b[0] && a[1] === b[1] && a[2] === b[2];
function pxAt([fx, fy], clamp) {
  const [w, h] = res();
  let x = Math.floor(fx), y = Math.floor(fy);
  if (clamp) { x = Math.max(0, Math.min(w - 1, x)); y = Math.max(0, Math.min(h - 1, y)); }
  return x >= 0 && y >= 0 && x < w && y < h ? [x, y] : null;
}
function getPx(buf, x, y) { const i = 3 * (y * res()[0] + x); return [buf[i], buf[i + 1], buf[i + 2]]; }
function setPx(buf, x, y, c) {
  const [w, h] = res();
  if (x < 0 || y < 0 || x >= w || y >= h) return;
  const i = y * w + x;
  buf[3 * i] = c[0]; buf[3 * i + 1] = c[1]; buf[3 * i + 2] = c[2];
  if (T.touched) T.touched.add(i);
}
function stampAt(buf, [x, y], c) {
  const r = T.brush, x0 = x - ((r - 1) >> 1), y0 = y - ((r - 1) >> 1);
  for (let j = 0; j < r; j++) for (let i = 0; i < r; i++) setPx(buf, x0 + i, y0 + j, c);
}
function lineCells([x0, y0], [x1, y1]) {                              // Bresenham
  const out = [], dx = Math.abs(x1 - x0), dy = -Math.abs(y1 - y0), sx = x0 < x1 ? 1 : -1, sy = y0 < y1 ? 1 : -1;
  let err = dx + dy;
  for (;;) {
    out.push([x0, y0]);
    if (x0 === x1 && y0 === y1) return out;
    const e2 = 2 * err;
    if (e2 >= dy) { err += dy; x0 += sx; }
    if (e2 <= dx) { err += dx; y0 += sy; }
  }
}
function floodFill(buf, [x, y], c) {
  const [w, h] = res(), orig = Uint8Array.from(buf), s = getPx(orig, x, y), tol = T.fillTol;
  if (sameC(s, c)) return;
  const close = i => Math.abs(orig[3 * i] - s[0]) + Math.abs(orig[3 * i + 1] - s[1]) + Math.abs(orig[3 * i + 2] - s[2]) <= tol;
  const seen = new Uint8Array(w * h), stack = [y * w + x];
  seen[y * w + x] = 1;
  while (stack.length) {
    const i = stack.pop(), cx = i % w, cy = (i / w) | 0;
    setPx(buf, cx, cy, c);
    for (const [ddx, ddy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
      const nx = cx + ddx, ny = cy + ddy, j = ny * w + nx;
      if (nx < 0 || ny < 0 || nx >= w || ny >= h || seen[j] || !close(j)) continue;
      seen[j] = 1; stack.push(j);
    }
  }
}
function shapeCells(a, b, tool) {
  if (tool === "line") return lineCells(a, b);
  const x0 = Math.min(a[0], b[0]), x1 = Math.max(a[0], b[0]), y0 = Math.min(a[1], b[1]), y1 = Math.max(a[1], b[1]), out = [];
  for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++)
    if (T.rectFill || x === x0 || x === x1 || y === y0 || y === y1) out.push([x, y]);
  return out;
}
function setColor(c) {
  T.color = sameC(c, EMPTY) ? [10, 10, 10] : c.slice();
  T.recent = [T.color, ...T.recent.filter(r => !sameC(r, T.color))].slice(0, 12);
  if (T.paintTool === "eraser" || T.paintTool === "picker" || T.paintTool === "select") T.paintTool = "pencil";
  renderToolbar(); renderPieces();
}
// piece ownership as one array, so pixels that move or flip take their piece along
function ownMap() {
  const [w, h] = res(), own = new Int16Array(w * h).fill(-1);
  F().pieces.forEach((p, k) => p.px.forEach(i => own[i] = k));
  return own;
}
function setOwnMap(own) { F().pieces.forEach((p, k) => { p.px = []; }); own.forEach((k, i) => { if (k >= 0) F().pieces[k].px.push(i); }); }
function paintDown(e, at) {
  if (T.saving) return;
  const f = F(), src = decoded.get(f.source), p = pxAt(at);
  const tool = e.altKey ? "picker" : e.button === 2 ? "eraser" : T.paintTool;
  if (tool === "picker") { if (p) { const c = getPx(src.rgb, ...p); if (sameC(c, EMPTY)) { T.paintTool = "eraser"; renderToolbar(); } else setColor(c); } return; }
  if (!p && tool !== "select") return;
  if (tool !== "select") C.beginEdit();                               // selecting alone is not an edit
  T.base = Uint8Array.from(src.rgb); T.work = Uint8Array.from(src.rgb); T.touched = new Set();
  if (tool === "pencil" || tool === "eraser") {
    const c = tool === "eraser" ? EMPTY : T.color;
    stampAt(T.work, p, c);
    T.drag = { kind: "stroke", c, last: p };
  } else if (tool === "fill") {
    floodFill(T.work, p, T.color);
    finishPaint("fill");
    return;
  } else if (tool === "line" || tool === "rect") {
    T.drag = { kind: "shape", tool, a: p };
    for (const q of shapeCells(p, p, tool)) stampAt(T.work, q, T.color);
  } else {                                                              // select / move
    const q = pxAt(at, true);
    if (T.sel && q[0] >= T.sel[0] && q[0] <= T.sel[2] && q[1] >= T.sel[1] && q[1] <= T.sel[3]) {
      C.beginEdit();
      const [x0, y0, x1, y1] = T.sel, [w] = res(), own = ownMap(), float = [];
      for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) {
        const c = getPx(T.work, x, y);
        if (sameC(c, EMPTY)) continue;
        float.push({ x, y, c, k: own[y * w + x] });
        setPx(T.base, x, y, EMPTY);
      }
      T.work = Uint8Array.from(T.base);
      T.drag = { kind: "move", start: q, float, own, d: [0, 0] };
      for (const fl of float) setPx(T.work, fl.x, fl.y, fl.c);
    } else {
      T.work = null; T.base = null;
      T.sel = [q[0], q[1], q[0], q[1]];
      T.drag = { kind: "select", a: q };
    }
  }
  draw();
}
function paintMove(e) {
  const at = toPix(e), d = T.drag;
  T.hover = pxAt(at);
  if (!d) { draw(); return; }
  if (d.kind === "stroke") {
    const p = pxAt(at, true);
    for (const q of lineCells(d.last, p)) stampAt(T.work, q, d.c);
    d.last = p;
  } else if (d.kind === "shape") {
    T.work = Uint8Array.from(T.base);
    for (const q of shapeCells(d.a, pxAt(at, true), d.tool)) stampAt(T.work, q, T.color);
  } else if (d.kind === "select") {
    const q = pxAt(at, true);
    T.sel = [Math.min(d.a[0], q[0]), Math.min(d.a[1], q[1]), Math.max(d.a[0], q[0]), Math.max(d.a[1], q[1])];
  } else if (d.kind === "move") {
    const q = pxAt(at, true);
    d.d = [q[0] - d.start[0], q[1] - d.start[1]];
    T.work = Uint8Array.from(T.base);
    for (const fl of d.float) setPx(T.work, fl.x + d.d[0], fl.y + d.d[1], fl.c);
  }
  draw();
}
function paintUp() {
  const d = T.drag;
  if (!d) return;
  T.drag = null;
  if (d.kind === "select") { renderToolbar(); draw(); return; }
  if (d.kind === "move") {
    const [w, h] = res(), own = d.own;
    for (const fl of d.float) own[fl.y * w + fl.x] = -1;
    for (const fl of d.float) {
      const x = fl.x + d.d[0], y = fl.y + d.d[1];
      if (x >= 0 && y >= 0 && x < w && y < h) own[y * w + x] = fl.k;
    }
    setOwnMap(own);
    T.sel = [T.sel[0] + d.d[0], T.sel[1] + d.d[1], T.sel[2] + d.d[0], T.sel[3] + d.d[1]];
  }
  finishPaint(d.kind);
}
async function finishPaint(label) {
  const f = F(), [w, h] = res(), work = T.work;
  T.saving = true;
  try {
    if (T.intoPiece && f.pieces[T.piece] && T.touched && T.touched.size) {     // new pixels join the selected piece
      const own = ownMap();
      for (const i of T.touched) if (own[i] < 0 && !empty(work, i)) own[i] = T.piece;
      setOwnMap(own);
    }
    f.source = await rgbURL(w, h, work);
  } finally {
    T.work = null; T.base = null; T.touched = null; T.saving = false;
  }
  C.commit(label);
}
function selEdit(fn, label) {
  if (!T.sel || T.saving) return;
  const src = decoded.get(F().source);
  C.beginEdit();
  T.work = Uint8Array.from(src.rgb);
  fn(T.sel);
  finishPaint(label);
}
function selFlip(horiz) {
  selEdit(([x0, y0, x1, y1]) => {
    const [w] = res(), own = ownMap(), src = Uint8Array.from(T.work), nown = Int16Array.from(own);
    for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) {
      const sx = horiz ? x0 + x1 - x : x, sy = horiz ? y : y0 + y1 - y;
      setPx(T.work, x, y, getPx(src, sx, sy));
      nown[y * w + x] = own[sy * w + sx];
    }
    setOwnMap(nown);
  }, "flip");
}
function selClear() { selEdit(([x0, y0, x1, y1]) => { for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) setPx(T.work, x, y, EMPTY); }, "clear"); }
const toHex = c => "#" + c.map(v => v.toString(16).padStart(2, "0")).join("");
function renderPalette(box) {
  const { el } = C, src = decoded.get(F().source);
  const swatch = (c, title, onclick, extra = "") => el("span", { class: "swatch" + extra, title, style: `background:${toHex(c)}`, onclick });
  const cur = el("input", { type: "color", value: toHex(T.color) });
  cur.addEventListener("change", () => setColor([1, 3, 5].map(i => parseInt(cur.value.slice(i, i + 2), 16))));
  const counts = new Map();
  if (src) for (let i = 0; i < src.w * src.h; i++) if (!empty(src.rgb, i)) { const k = hex(src.rgb, i); counts.set(k, (counts.get(k) || 0) + 1); }
  const pal = [...counts.entries()].sort((a, b) => b[1] - a[1]).map(([k]) => [0, 2, 4].map(j => parseInt(k.slice(j, j + 2), 16)));
  const num = (v, set, min, max) => { const n = el("input", { type: "number", min, max, value: v, style: "width:56px" }); n.addEventListener("change", () => set(+n.value)); return n; };
  const chk = (v, set, label) => { const c = el("input", { type: "checkbox", checked: v }); c.addEventListener("change", () => set(c.checked)); return el("label", { class: "chk" }, c, label); };
  box.append(el("div", { class: "palette" },
    el("div", { class: "row" }, el("span", { class: "swatch big", style: `background:${toHex(T.color)}` }), cur,
      el("span", { class: "hint", style: "margin:0" }, toHex(T.color))),
    el("div", { class: "row" },
      swatch([60, 60, 66], "transparent (eraser): black in the file", () => { T.paintTool = "eraser"; renderToolbar(); renderPieces(); }, " clear"),
      el("span", { class: "hint", style: "margin:0" }, "see-through"),
      swatch(SHADOW, "shadow: magenta in the file", () => setColor(SHADOW)), el("span", { class: "hint", style: "margin:0" }, "shadow")),
    T.recent.length ? el("div", {}, el("h4", {}, "Recent"), el("div", { class: "swatches" }, T.recent.map(c => swatch(c, toHex(c), () => setColor(c))))) : "",
    el("h4", {}, `This frame's colours (${pal.length})`),
    el("div", { class: "swatches" }, pal.map(c => swatch(c, toHex(c), () => setColor(c), sameC(c, T.color) ? " on" : ""))),
    el("div", { class: "group" },
      el("div", { class: "row" }, "fill tolerance", num(T.fillTol, v => T.fillTol = v, 0, 200)),
      el("div", { class: "row" }, chk(T.rectFill, v => T.rectFill = v, "filled rectangles")),
      el("div", { class: "row" }, chk(T.intoPiece, v => T.intoPiece = v, "new pixels join the selected piece")))));
}

// ------------------------------------------------------------------ mouse
function toPix(e) {
  const r = $("#c2d").getBoundingClientRect();
  return [(e.clientX - r.left - view.ox) / view.z, (e.clientY - r.top - view.oy) / view.z];
}
function newPiece(at) {
  const f = F();
  let n = f.pieces.length + 1;
  while (f.pieces.some(p => p.name === "piece " + n)) n++;
  const ls = layersOK();
  f.pieces.push({ name: "piece " + n, px: [], pivot: at ? [Math.floor(at[0]) + 0.5, Math.floor(at[1]) + 0.5] : [res()[0] / 2, res()[1] / 2], parent: null, patch: true,
    layer: ls.some(l => l.id === T.layer) ? T.layer : M().bodyLayer });
  T.piece = f.pieces.length - 1;
}
function assign(indices, k) {                // give pixels to piece k (or back to the base with k = -1)
  const f = F(), set = new Set(indices);
  f.pieces.forEach((p, j) => { if (j !== k) p.px = p.px.filter(i => !set.has(i)); });
  if (k >= 0) f.pieces[k].px = [...new Set([...f.pieces[k].px, ...indices])].sort((a, b) => a - b);
}
function brushAt([fx, fy]) {
  const [w, h] = res(), src = decoded.get(F().source), out = [];
  const r = T.brush, x0 = Math.floor(fx - (r - 1) / 2), y0 = Math.floor(fy - (r - 1) / 2);
  for (let y = y0; y < y0 + r; y++) for (let x = x0; x < x0 + r; x++)
    if (x >= 0 && y >= 0 && x < w && y < h && !empty(src.rgb, y * w + x)) out.push(y * w + x);
  return out;
}
function wand([fx, fy]) {
  const [w, h] = res(), src = decoded.get(F().source).rgb;
  const x = Math.floor(fx), y = Math.floor(fy);
  if (x < 0 || y < 0 || x >= w || y >= h || empty(src, y * w + x)) return [];
  const s = y * w + x, seen = new Set([s]), stack = [s];
  const dist = (a, b) => Math.abs(src[3 * a] - src[3 * b]) + Math.abs(src[3 * a + 1] - src[3 * b + 1]) + Math.abs(src[3 * a + 2] - src[3 * b + 2]);
  while (stack.length) {
    const i = stack.pop(), cx = i % w, cy = (i / w) | 0;
    for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
      const nx = cx + dx, ny = cy + dy, j = ny * w + nx;
      if (nx < 0 || ny < 0 || nx >= w || ny >= h || seen.has(j) || empty(src, j) || dist(s, j) > T.tol) continue;
      seen.add(j); stack.push(j);
    }
  }
  return [...seen];
}
function pieceAt([fx, fy]) {
  const [w, h] = res(), x = Math.floor(fx), y = Math.floor(fy);
  if (x < 0 || y < 0 || x >= w || y >= h) return -1;
  if (T.mode === "cut") return F().pieces.findIndex(p => p.px.includes(y * w + x));
  const c = compose(C.S.frame);
  return c.owner[y * w + x];
}
function onDown(e) {
  if (!isCut(M())) return;
  e.preventDefault();
  try { $("#c2d").setPointerCapture(e.pointerId); } catch { /* synthetic test events */ }
  const at = toPix(e), f = F();
  if (T.mode === "paint") return paintDown(e, at);
  if (e.altKey) { const k = pieceAt(at); if (k >= 0) { T.piece = k; C.refresh(); } return; }
  if (T.mode === "cut") {
    const remove = e.button === 2 || T.cutTool === "eraser";
    if (T.cutTool === "joint") {
      if (T.piece < 0) return;
      C.beginEdit(); f.pieces[T.piece].pivot = [Math.floor(at[0]) + 0.5, Math.floor(at[1]) + 0.5]; C.commit("joint");
      return;
    }
    C.beginEdit();
    if (!remove && T.piece < 0) newPiece(at);
    if (T.cutTool === "box") { T.box = [Math.floor(at[0]), Math.floor(at[1]), Math.floor(at[0]), Math.floor(at[1])]; T.drag = { kind: "box", remove }; draw(); return; }
    const pixels = T.cutTool === "wand" ? wand(at) : brushAt(at);
    assign(pixels, remove ? -1 : T.piece);
    if (T.cutTool === "wand") { C.commit("wand"); return; }
    T.drag = { kind: "paint", remove };
    draw();
    return;
  }
  // pose mode: grab a piece (or the selected piece's joint) and turn / move / stretch it
  const comp = compose(C.S.frame);
  let k = pieceAt(at), tool = T.tool;
  const sel = f.pieces[T.piece];
  if (sel) {
    const [jx, jy] = apply(comp.Ts[sel.name], sel.pivot[0], sel.pivot[1]);
    if (Math.hypot(at[0] - jx, at[1] - jy) * view.z < 9) { k = T.piece; tool = "move"; }
  }
  if (k < 0) { T.piece = -1; C.refresh(); return; }
  T.piece = k;
  const p = f.pieces[k];
  const pv = apply(comp.Ts[p.name], p.pivot[0], p.pivot[1]);
  const par = (p.parent && comp.Ts[p.parent]) || ID;
  C.beginEdit();
  T.drag = { kind: tool, k, start: at, pv, parInv: invert([par[0], par[1], par[2], par[3], 0, 0]), pose0: JSON.parse(JSON.stringify(poseOf(f, p.name))) };
  C.refresh();
}
function onMove(e) {
  if (T.mode === "paint" && isCut(M())) return paintMove(e);
  const d = T.drag;
  if (!d) return;
  const at = toPix(e), f = F();
  if (d.kind === "box") { T.box[2] = Math.floor(at[0]); T.box[3] = Math.floor(at[1]); draw(); return; }
  if (d.kind === "paint") { assign(brushAt(at), d.remove ? -1 : T.piece); draw(); return; }
  const p = f.pieces[d.k], ps = ensurePose(f, p.name), p0 = d.pose0;
  if (d.kind === "turn") {
    const a0 = Math.atan2(d.start[1] - d.pv[1], d.start[0] - d.pv[0]), a1 = Math.atan2(at[1] - d.pv[1], at[0] - d.pv[0]);
    let r = (p0.rot || 0) + (a1 - a0) * 180 / Math.PI;
    r = ((r + 540) % 360) - 180;
    ps.rot = e.shiftKey ? Math.round(r / 15) * 15 : Math.round(r);
  } else if (d.kind === "move") {
    const [dx, dy] = apply(d.parInv, at[0] - d.start[0], at[1] - d.start[1]);
    const m0 = p0.move || [0, 0];
    ps.move = [Math.round(m0[0] + dx), Math.round(m0[1] + dy)];
  } else {
    const r0 = Math.hypot(d.start[0] - d.pv[0], d.start[1] - d.pv[1]) || 1, r1 = Math.hypot(at[0] - d.pv[0], at[1] - d.pv[1]);
    const s0 = p0.scale || [1, 1], k = Math.max(0.1, r1 / r0);
    ps.scale = [Math.round(s0[0] * k * 100) / 100, Math.round(s0[1] * k * 100) / 100];
  }
  live = compose(C.S.frame);
  draw();
  C.liveSprite();
  renderInspector();
}
function onUp() {
  if (T.mode === "paint") return paintUp();
  const d = T.drag;
  if (!d) return;
  T.drag = null; live = null;
  if (d.kind === "box") {
    const [x0, y0, x1, y1] = T.box, [w, h] = res(), src = decoded.get(F().source).rgb, px = [];
    T.box = null;
    for (let y = Math.max(0, Math.min(y0, y1)); y <= Math.min(h - 1, Math.max(y0, y1)); y++)
      for (let x = Math.max(0, Math.min(x0, x1)); x <= Math.min(w - 1, Math.max(x0, x1)); x++) if (!empty(src, y * w + x)) px.push(y * w + x);
    assign(px, d.remove ? -1 : T.piece);
  }
  C.commit(d.kind);
}

// ------------------------------------------------------------------ panels
function seg(items, cur, onpick, title) {
  return C.el("span", { class: "seg", title }, items.map(([k, label, tip]) =>
    C.el("button", { class: cur === k ? "on" : "", title: tip || "", onclick: () => onpick(k) }, label)));
}
export function renderToolbar() {
  const bar = $("#tools2d");
  bar.innerHTML = "";
  const { el } = C;
  bar.append(seg([["pose", "Pose", "drag pieces to turn, move or stretch them"], ["cut", "Cut", "paint which pixels belong to which piece"],
    ["paint", "Paint", "edit the pixels themselves"]], T.mode, m => { T.mode = m; T.sel = null; T.work = null; C.refresh(); }));
  if (T.mode === "paint") {
    bar.append(seg([["pencil", "Pencil", "B"], ["eraser", "Eraser", "E: paints see-through"], ["fill", "Fill", "G: flood fill"], ["line", "Line", "L"],
      ["rect", "Rect", "R"], ["picker", "Pick", "I: take a colour (or Alt-click)"], ["select", "Select", "M: drag a box, then drag inside it to move"]],
    T.paintTool, t => { T.paintTool = t; renderToolbar(); }));
    if (["pencil", "eraser", "line", "rect"].includes(T.paintTool)) bar.append(seg([[1, "1px"], [2, "2px"], [3, "3px"]], T.brush, b => { T.brush = b; renderToolbar(); }));
    if (T.sel) bar.append(el("span", { class: "seg" },
      el("button", { title: "mirror the selection left-right", onclick: () => selFlip(true) }, "Flip ↔"),
      el("button", { title: "mirror the selection up-down", onclick: () => selFlip(false) }, "Flip ↕"),
      el("button", { title: "Delete", onclick: () => selClear() }, "Clear"),
      el("button", { title: "Esc", onclick: () => { T.sel = null; renderToolbar(); draw(); } }, "Deselect")));
    bar.append(el("span", { class: "lbl" }, "right-click erases · Alt-click picks a colour"));
  } else if (T.mode === "pose") {
    bar.append(seg([["turn", "Turn"], ["move", "Move"], ["stretch", "Stretch"]], T.tool, t => { T.tool = t; renderToolbar(); }, "what dragging a piece does"),
      el("span", { class: "lbl" }, "drag a piece · drag its yellow joint to move it · Shift snaps 15° · Alt-click picks"));
  } else {
    bar.append(seg([["brush", "Brush"], ["box", "Box"], ["wand", "Wand", "same-coloured area"], ["eraser", "Eraser"], ["joint", "Joint", "click where the selected piece turns"]],
      T.cutTool, t => { T.cutTool = t; renderToolbar(); }));
    if (T.cutTool === "brush" || T.cutTool === "eraser") bar.append(seg([[1, "1px"], [2, "2px"], [3, "3px"]], T.brush, b => { T.brush = b; renderToolbar(); }));
    if (T.cutTool === "wand") {
      const tol = el("input", { type: "range", min: 0, max: 200, value: T.tol, title: "colour tolerance" });
      tol.oninput = () => { T.tol = +tol.value; };
      bar.append(el("span", { class: "lbl" }, "tolerance"), tol);
    }
    bar.append(el("span", { class: "lbl" }, "tint"), seg([["piece", "Pieces"], ["layer", "Layers"]], T.tint, t => { T.tint = t; renderToolbar(); draw(); }, "colour the pixels by piece or by layer"),
      el("span", { class: "lbl" }, "right-click removes"));
  }
}
function renderPieces() {
  const box = $("#cutPieces"), { el } = C, f = F();
  box.innerHTML = "";
  if (T.mode === "paint") renderPalette(box);
  box.append(el("p", { class: "hint" }, T.mode === "paint" ? "Pieces (painted pixels keep their piece; tick the box above to add new ones to the selected piece):" : T.mode === "cut"
    ? "Cut: pick a piece, then paint its pixels (Brush, Box, Wand). Set its Joint where it bends. Pixels in no piece stay put."
    : "Pose: drag a piece to turn it about its joint. Switch to Cut to change which pixels belong to which piece."));
  box.append(el("div", { class: "row" },
    el("button", { onclick: () => { C.beginEdit(); newPiece(); T.mode = "cut"; C.commit("new piece"); } }, "New piece"),
    el("button", { disabled: T.piece < 0, onclick: () => deletePiece() }, "Delete"),
    el("button", { disabled: T.piece < 1, title: "draw behind the piece above", onclick: () => order(-1) }, "▲"),
    el("button", { disabled: T.piece < 0 || T.piece >= f.pieces.length - 1, title: "draw in front", onclick: () => order(1) }, "▼")));
  const pieceRow = (p, k) => el("div", { class: "prow" + (k === T.piece ? " sel" : "") + (p.hidden ? " hid" : ""), onclick: () => { T.piece = k; T.layer = p.layer || M().bodyLayer; C.refresh(); } },
    el("span", { class: "sw", style: `background:${HUES[k % HUES.length]}` }),
    el("span", { class: "nm" }, p.name),
    p.parent ? el("span", { class: "ty" }, "on " + p.parent) : null,
    el("span", { class: "ty" }, p.px.length + " px"),
    el("span", { class: "eye", title: "hide/show", onclick: e => { e.stopPropagation(); C.beginEdit(); p.hidden = !p.hidden; C.commit("hide"); } }, p.hidden ? "◌" : "●"));
  box.append(renderLayers(pieceRow));
  if (!f.pieces.length) box.append(el("p", { class: "hint" }, "No pieces yet. Press New piece, or switch to Cut and paint."));
  box.append(el("p", { class: "hint" }, "Within a layer, lower in the list = drawn in front. Pieces on a parent follow it."));
}
// Layers, top (nearest you) first, each with its pieces; the body (pixels in no piece) sits on one of them.
function renderLayers(pieceRow) {
  const { el } = C, m = M(), f = F(), ls = layersOK();
  if (!ls.some(l => l.id === T.layer)) T.layer = m.bodyLayer;
  const edit = (label, fn) => { C.beginEdit(); fn(); C.commit(label); };
  const box = el("div", { class: "layers" },
    el("div", { class: "row" }, el("h4", { style: "margin:0;flex:1" }, "Layers"),
      el("button", { title: "add a layer above the active one", onclick: () => edit("new layer", () => {
        let n = ls.length + 1;
        while (ls.some(l => l.id === "l" + n)) n++;
        const at = Math.max(0, ls.findIndex(l => l.id === T.layer));
        ls.splice(at, 0, { id: "l" + n, name: "Layer " + n });
        T.layer = "l" + n;
      }) }, "+ Layer")),
    el("p", { class: "hint", style: "margin-top:0" }, "Top layer = drawn in front, and nearest you when converted to 3D. New pieces go on the active layer."));
  ls.forEach((l, i) => {
    const on = l.id === T.layer;
    const head = el("div", { class: "lhead" + (on ? " on" : ""), onclick: () => { T.layer = l.id; renderPieces(); } },
      el("span", { class: "sw", style: `background:${HUES[i % HUES.length]}` }),
      el("b", { class: "nm", title: "double-click to rename", ondblclick: e => {
        e.stopPropagation();
        const n = prompt("Layer name", l.name);
        if (n && n.trim()) edit("rename layer", () => l.name = n.trim());
      } }, l.name),
      el("button", { title: "move up (nearer)", disabled: i === 0, onclick: e => { e.stopPropagation(); edit("layer order", () => { ls.splice(i, 1); ls.splice(i - 1, 0, l); }); } }, "▲"),
      el("button", { title: "move down (farther)", disabled: i === ls.length - 1, onclick: e => { e.stopPropagation(); edit("layer order", () => { ls.splice(i, 1); ls.splice(i + 1, 0, l); }); } }, "▼"),
      el("button", { title: "delete the layer (its pieces move to the layer below, or above)", disabled: ls.length < 2, onclick: e => {
        e.stopPropagation();
        edit("delete layer", () => {
          const to = (ls[i + 1] || ls[i - 1]).id;
          for (const fr of Object.values(m.frames)) for (const p of fr.pieces || []) if ((p.layer || m.bodyLayer) === l.id) p.layer = to;
          if (m.bodyLayer === l.id) m.bodyLayer = to;
          ls.splice(i, 1);
          if (T.layer === l.id) T.layer = to;
        });
      } }, "×"));
    const rows = f.pieces.map((p, k) => (p.layer || m.bodyLayer) === l.id ? pieceRow(p, k) : null).filter(Boolean);
    if (m.bodyLayer === l.id) rows.unshift(el("div", { class: "prow body", title: "the pixels that belong to no piece" },
      el("span", { class: "sw", style: "background:#777" }), el("span", { class: "nm" }, "body (pixels in no piece)")));
    box.append(el("div", { class: "layer" + (on ? " on" : "") }, head, ...rows));
  });
  const body = el("select", {}, ls.map(l => el("option", { value: l.id, selected: l.id === m.bodyLayer }, l.name)));
  body.addEventListener("change", () => edit("body layer", () => m.bodyLayer = body.value));
  box.append(C.field("body on", body));
  return box;
}
function deletePiece() {
  const f = F(), p = f.pieces[T.piece];
  if (!p) return;
  C.beginEdit();
  f.pieces.splice(T.piece, 1);
  delete f.pose[p.name];
  f.pieces.forEach(q => { if (q.parent === p.name) q.parent = p.parent || null; });
  T.piece = Math.min(T.piece, f.pieces.length - 1);
  C.commit("delete piece");
}
function order(d) {
  const f = F(), k = T.piece, j = k + d;
  if (k < 0 || j < 0 || j >= f.pieces.length) return;
  C.beginEdit();
  [f.pieces[k], f.pieces[j]] = [f.pieces[j], f.pieces[k]];
  T.piece = j;
  C.commit("order");
}
function bbox(px) {
  const w = res()[0];
  let x0 = 1e9, y0 = 1e9, x1 = -1, y1 = -1;
  for (const i of px) { const x = i % w, y = (i / w) | 0; x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y); }
  return px.length ? [x1 - x0 + 1, y1 - y0 + 1] : [0, 0];
}
function renderInspector() {
  const box = $("#inspector"), { el, field, numInput } = C, f = F(), p = f.pieces[T.piece];
  box.innerHTML = "";
  if (!p) { box.append(el("p", { class: "hint" }, "Click a piece in the editor or the list.")); return; }
  const done = label => (v, fin) => { if (fin) C.commit(label); else { live = compose(C.S.frame); draw(); C.liveSprite(); } };
  const name = el("input", { type: "text", value: p.name });
  name.addEventListener("change", () => {
    const n = name.value.trim();
    if (!n || f.pieces.some(q => q !== p && q.name === n)) { name.value = p.name; return; }
    C.beginEdit();
    if (f.pose[p.name]) { f.pose[n] = f.pose[p.name]; delete f.pose[p.name]; }   // keep its pose and children linked
    f.pieces.forEach(q => { if (q.parent === p.name) q.parent = n; });
    p.name = n;
    C.commit("rename");
  });
  const parent = el("select", {}, [el("option", { value: "" }, "(none: stays with the body)"),
    ...f.pieces.filter(q => q !== p).map(q => el("option", { value: q.name, selected: q.name === p.parent }, q.name))]);
  parent.addEventListener("change", () => { C.beginEdit(); p.parent = parent.value || null; C.commit("parent"); });
  const patch = el("input", { type: "checkbox", checked: p.patch !== false });
  patch.addEventListener("change", () => { C.beginEdit(); p.patch = patch.checked; C.commit("patch"); });
  const ls = layersOK();
  const layer = el("select", {}, ls.map(l => el("option", { value: l.id, selected: l.id === (p.layer || M().bodyLayer) }, l.name)));
  layer.addEventListener("change", () => { C.beginEdit(); p.layer = layer.value; T.layer = layer.value; C.commit("layer"); });
  box.append(field("name", name), field("layer", layer), field("attached to", parent),
    field("fill hole", el("label", { class: "chk", title: "when the piece moves, fill the gap it leaves in the body with the colours around it" }, patch, "patch the gap it leaves")),
    field("joint x,y", ...[0, 1].map(k => numInput(p.pivot[k], (v, fin) => { p.pivot[k] = v; done("joint")(v, fin); }, 0.5))));
  const ps = poseOf(f, p.name);
  const set = (key, idx, def) => v => { const q = ensurePose(f, p.name); if (idx == null) q[key] = v; else { q[key] ||= def.slice(); q[key][idx] = v; } };
  const [bw, bh] = bbox(p.px), sc = ps.scale || [1, 1];
  const g = el("div", { class: "group" }, el("h4", {}, `Pose · frame ${C.S.frame}`),
    field("turn °", numInput(ps.rot || 0, (v, fin) => { set("rot")(v); done("turn")(v, fin); }, 1)),
    field("move x,y", ...[0, 1].map(k => numInput((ps.move || [0, 0])[k], (v, fin) => { set("move", k, [0, 0])(Math.round(v)); done("move")(v, fin); }, 1))),
    field("width px", numInput(Math.round(bw * Math.abs(sc[0])), (v, fin) => { if (bw) set("scale", 0, [1, 1])(Math.sign(sc[0] || 1) * Math.max(1, v) / bw); done("size")(v, fin); }, 1)),
    field("height px", numInput(Math.round(bh * Math.abs(sc[1])), (v, fin) => { if (bh) set("scale", 1, [1, 1])(Math.sign(sc[1] || 1) * Math.max(1, v) / bh); done("size")(v, fin); }, 1)),
    field("flip", el("label", { class: "chk" }, (() => {
      const c = el("input", { type: "checkbox", checked: sc[0] < 0 });
      c.addEventListener("change", () => { C.beginEdit(); const q = ensurePose(f, p.name); q.scale = [Math.abs(sc[0]) * (c.checked ? -1 : 1), sc[1]]; C.commit("flip"); });
      return c;
    })(), "mirror left-right")),
    el("div", { class: "btns" }, el("button", { onclick: () => { C.beginEdit(); delete f.pose[p.name]; C.commit("reset piece"); } }, "Reset pose")));
  box.append(g, el("div", { class: "group" }, el("h4", {}, "Pixels"),
    el("p", { class: "hint" }, `${p.px.length} pixels, ${bw}×${bh} px before stretching.`),
    el("div", { class: "btns" }, el("button", { onclick: () => { C.beginEdit(); p.px = []; C.commit("clear piece"); } }, "Clear pixels"))));
}
function renderPose() {
  const box = $("#cutPose"), { el, slider } = C, f = F();
  box.innerHTML = "";
  box.append(el("p", { class: "hint" }, `Pose for frame ${C.S.frame}. Drag pieces in the editor, or use the sliders.`),
    el("div", { class: "row" },
      el("button", { onclick: () => copyFrame("pose") }, "Copy pose from other frame"),
      el("button", { onclick: () => { C.beginEdit(); f.pose = {}; C.commit("reset pose"); } }, "Reset frame")));
  const liveFn = () => { live = compose(C.S.frame); draw(); C.liveSprite(); };
  const fin = () => C.commit("pose");
  f.pieces.forEach((p, k) => {
    const ps = poseOf(f, p.name), set = fn => v => { fn(ensurePose(f, p.name), v); liveFn(); };
    box.append(el("div", { class: "bone", style: k === T.piece ? "outline:1px solid #e0a040" : "" },
      el("h4", {}, el("span", { style: "cursor:pointer", onclick: () => { T.piece = k; C.refresh(); } }, p.name),
        el("button", { onclick: () => { C.beginEdit(); delete f.pose[p.name]; C.commit("reset piece"); } }, "reset")),
      slider("turn", ps.rot || 0, -180, 180, 1, set((q, v) => q.rot = v), fin),
      slider("move x", (ps.move || [0, 0])[0], -64, 64, 1, set((q, v) => q.move = [v, (q.move || [0, 0])[1]]), fin),
      slider("move y", (ps.move || [0, 0])[1], -64, 64, 1, set((q, v) => q.move = [(q.move || [0, 0])[0], v]), fin),
      slider("size %", Math.round(Math.abs((ps.scale || [1, 1])[0]) * 100), 10, 400, 1,
        set((q, v) => { const s = q.scale || [1, 1]; q.scale = [Math.sign(s[0] || 1) * v / 100, Math.sign(s[1] || 1) * v / 100]; }), fin)));
  });
}
function copyFrame(what) {
  const keys = Object.keys(M().frames).filter(k => k !== C.S.frame);
  const from = keys.length === 1 ? keys[0] : prompt("Copy from which frame? " + keys.join(", "), keys[0]);
  const src = from && M().frames[from];
  if (!src) return;
  C.beginEdit();
  const f = F();
  if (what === "pose") f.pose = JSON.parse(JSON.stringify(src.pose || {}));
  else { f.source = src.source; f.pieces = JSON.parse(JSON.stringify(src.pieces || [])); f.pose = JSON.parse(JSON.stringify(src.pose || {})); }
  C.commit("copy frame");
}
function palette() {
  const count = new Map();
  for (const f of Object.values(M().frames)) {
    const src = decoded.get(f.source);
    if (!src) continue;
    for (let i = 0; i < src.w * src.h; i++) if (!empty(src.rgb, i) && !isShadow(src.rgb, i)) { const h = hex(src.rgb, i); count.set(h, (count.get(h) || 0) + 1); }
  }
  return [...count.entries()].sort((a, b) => b[1] - a[1]);
}
function renderColors() {
  const box = $("#cutColors"), { el } = C, rc = M().recolor || (M().recolor = {});
  box.innerHTML = "";
  const all = palette();
  box.append(el("p", { class: "hint" }, `Replace any colour of the sprite. ${all.length} colours, most used first.`),
    el("div", { class: "row" }, el("button", { onclick: () => { C.beginEdit(); M().recolor = {}; C.commit("reset colours"); } }, "Reset all colours")));
  for (const [h, n] of all.slice(0, 64)) {
    const to = el("input", { type: "color", value: "#" + (rc[h] || h) });
    to.addEventListener("input", () => { C.beginEdit(); rc[h] = to.value.slice(1); live = compose(C.S.frame); draw(); C.liveSprite(); });
    to.addEventListener("change", () => C.commit("recolour"));
    box.append(el("div", { class: "mat" },
      el("span", { class: "sw", style: `background:#${h};width:30px;height:22px;border-radius:3px;display:inline-block`, title: "#" + h }),
      el("span", {}, "#" + h, el("small", { style: "color:#9a9ca5" }, `  ${n} px`)), to,
      el("button", { title: "back to the original", disabled: !rc[h], onclick: () => { C.beginEdit(); delete rc[h]; C.commit("reset colour"); } }, "×")));
  }
  if (all.length > 64) box.append(el("p", { class: "hint" }, `…and ${all.length - 64} rarer colours.`));
}
function renderCanvasPanel() {
  const box = $("#cutCanvas"), { el, field } = C, r = M().render;
  box.innerHTML = "";
  const file = el("input", { type: "text", value: r.file || C.S.name });
  file.addEventListener("change", () => { C.beginEdit(); r.file = file.value.toLowerCase().replace(/[^a-z0-9_-]/g, ""); C.commit("file"); });
  box.append(el("div", { class: "group", style: "margin-top:0;border:0;padding-top:0" }, el("h4", {}, "3D"),
    el("p", { class: "hint" }, "Turn this sprite into a 3D model: pixels become blocks, each layer a slab (top layer nearest you), each piece a bone you can pose. Your 2D project stays as it is."),
    el("div", { class: "btns" }, el("button", { class: "primary", onclick: () => C.convert() }, "Convert to 3D…"))));
  box.append(el("div", { class: "group", style: "margin-top:0;border:0;padding-top:0" }, el("h4", {}, "Placement"),
    el("p", { class: "hint" }, "Dominions sprites stand with their feet 2 px above the bottom of the canvas. This moves a floating sprite (every frame, with its pieces) down onto that row, and cleans up off-magenta shadow."),
    el("div", { class: "btns" }, el("button", { onclick: async () => {
      C.beginEdit();
      try {
        const dy = await placeOnGround();
        C.commit("ground");
        C.toast(dy ? `Moved ${Math.abs(dy)} px ${dy > 0 ? "down" : "up"}.` : "Already standing on the ground row.");
      } catch (e) { alert(e.message); }
    } }, "Stand on the ground row"))));
  box.append(el("h4", {}, "Canvas"), C.canvasSizeField(r.res, [["pad", "keep pixel size (add or trim border)"], ["scale", "stretch the sprite to fit"]],
    (n, how) => resizeCanvas(n, how)));
  box.append(el("div", { class: "group" }, el("h4", {}, "Output"), field("file name", file),
    el("p", { class: "hint" }, "Frames are written as <file>1.tga (idle) and <file>2.tga (attack)."),
    ...Object.entries(M().frames).map(([k, f]) => {
      const lab = el("input", { type: "text", value: f.label || k });
      lab.addEventListener("change", () => { C.beginEdit(); f.label = lab.value; C.commit("label"); });
      const pick = el("input", { type: "file", accept: ".tga,.png,.bmp,.gif,.webp", hidden: true });
      pick.addEventListener("change", async () => {
        const file = pick.files[0];
        if (!file) return;
        try {
          const img = await C.decodeFile(file);
          if (img.w !== r.res[0] || img.h !== r.res[1]) throw new Error(`that image is ${img.w}×${img.h}; this project is ${r.res[0]}×${r.res[1]}`);
          await decodeURL(img.png);
          C.beginEdit(); f.source = img.png; f.pieces = []; f.pose = {}; C.commit("replace image");
        } catch (e) { alert(e.message); }
      });
      return el("div", {}, field(`frame ${k}`, lab), el("div", { class: "btns", style: "margin:0 0 8px 84px" },
        el("button", { title: "load a different image for this frame (its pieces are cleared)", onclick: () => pick.click() }, "Replace image…"),
        el("button", { title: "copy the image, pieces and pose of the other frame", onclick: () => { C.S.frame = k; copyFrame("all"); } }, "Copy other frame"), pick));
    })));
}
export function refresh() {
  live = null;
  if (T.piece >= F().pieces.length) T.piece = F().pieces.length - 1;
  renderToolbar();
  renderPieces();
  renderPose();
  renderColors();
  renderCanvasPanel();
  renderInspector();
  composeAll();
  draw();
}
export function selectNone() { T.piece = -1; refresh(); }
export function key(e) {
  const k = e.key.toLowerCase();
  if (T.mode === "paint" && !e.ctrlKey && !e.metaKey && !e.altKey) {
    const tools = { b: "pencil", e: "eraser", g: "fill", l: "line", r: "rect", i: "picker", m: "select" };
    if (tools[k]) { T.paintTool = tools[k]; renderToolbar(); return true; }
    if (k === "delete" && T.sel) { selClear(); return true; }
    if (k === "escape" && T.sel) { T.sel = null; renderToolbar(); draw(); return true; }
  }
  if (k === "delete") { deletePiece(); return true; }
  if (k === "escape") { selectNone(); return true; }
  return false;
}
export function deleteSelected() { deletePiece(); }

export function setup(ctx) {
  C = ctx;
  const cv = $("#c2d");
  cv.addEventListener("pointerdown", onDown);
  cv.addEventListener("pointermove", onMove);
  cv.addEventListener("pointerleave", () => { if (T.hover) { T.hover = null; draw(); } });
  cv.addEventListener("pointerup", onUp);
  cv.addEventListener("pointercancel", onUp);
  cv.addEventListener("contextmenu", e => e.preventDefault());
  new ResizeObserver(() => draw()).observe(cv);
}
// URL test hook: ?mode=cut&piece=0&tool=wand
export function testHook(q) {
  if (q.get("mode")) T.mode = q.get("mode");
  if (q.get("piece")) T.piece = +q.get("piece");
  if (q.get("tool")) T[{ cut: "cutTool", paint: "paintTool" }[T.mode] || "tool"] = q.get("tool");
  if (q.get("sel")) T.sel = q.get("sel").split(",").map(Number);
  if (q.get("hover")) T.hover = q.get("hover").split(",").map(Number);
  if (q.get("tint")) T.tint = q.get("tint");
  if (q.get("ground")) placeOnGround().then(dy => { window.__groundDy = dy; C.refresh(); });
  if (q.get("color")) T.color = q.get("color").split(",").map(Number);
  if (q.get("drag")) setTimeout(() => {                // real pointer events: drag=x0,y0,x1,y1 in pixels
    const [x0, y0, x1, y1] = q.get("drag").split(",").map(Number), cv = $("#c2d"), r = cv.getBoundingClientRect();
    const at = (x, y) => ({ clientX: r.left + view.ox + (x + 0.5) * view.z, clientY: r.top + view.oy + (y + 0.5) * view.z, button: 0, pointerId: 1, bubbles: true });
    cv.dispatchEvent(new PointerEvent("pointerdown", at(x0, y0)));
    for (let k = 1; k <= 8; k++) cv.dispatchEvent(new PointerEvent("pointermove", at(x0 + (x1 - x0) * k / 8, y0 + (y1 - y0) * k / 8)));
    cv.dispatchEvent(new PointerEvent("pointerup", at(x1, y1)));
  }, 400);
  C.refresh();
}
// test hook: the pure parts, for node
export { decoded };
export const _test = { localT, mulT, apply, invert, scale2x, compose, decoded, lineCells, floodFill, shapeCells, stampAt, T, setModel: m => { C = { S: { model: m, frame: "1" } }; } };
