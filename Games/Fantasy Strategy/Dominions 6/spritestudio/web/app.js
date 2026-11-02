// Sprite Studio front end: live 3D model view (three.js) + sprite renders from the Python engine.
import * as THREE from "three";
import { OrbitControls } from "three/addons/OrbitControls.js";
import { TransformControls } from "three/addons/TransformControls.js";
import { RoundedBoxGeometry } from "three/addons/RoundedBoxGeometry.js";
import { RoomEnvironment } from "three/addons/RoomEnvironment.js";
import * as Cut from "./cutout.js";
import { toModel } from "./to3d.js";

const $ = s => document.querySelector(s);
const $$ = s => [...document.querySelectorAll(s)];
const el = (tag, attrs = {}, ...kids) => {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k.startsWith("on")) e.addEventListener(k.slice(2), v);
    else if (k === "class") e.className = v;
    else if (v !== undefined && v !== null && v !== false) e.setAttribute(k, v === true ? "" : v);
  }
  for (const k of kids.flat(Infinity)) if (k !== null && k !== undefined) e.append(k.nodeType ? k : document.createTextNode(k));
  return e;
};
const r3 = v => Math.round(v * 1000) / 1000;
const clone = o => JSON.parse(JSON.stringify(o));

// ------------------------------------------------------------------ state
const S = {
  model: null, name: null, frame: "1", sel: -1, tab: "parts", view: "both",
  undo: [], redo: [], dirty: false, sprites: {}, spriteFrame: "1", renderSeq: {}, staleRun: 0,
  bg: "game", zoom: 6,
};

// ------------------------------------------------------------------ maths (mirrors engine/model.py)
const add = (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
const mul = (a, s) => [a[0] * s, a[1] * s, a[2] * s];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const len = a => Math.sqrt(dot(a, a));
const norm = a => mul(a, 1 / len(a));
const I3 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
const mm = (A, B) => A.map((r, i) => [0, 1, 2].map(j => A[i][0] * B[0][j] + A[i][1] * B[1][j] + A[i][2] * B[2][j]));
const mv = (A, v) => [dot(A[0], v), dot(A[1], v), dot(A[2], v)];
const mtv = (A, v) => [0, 1, 2].map(j => A[0][j] * v[0] + A[1][j] * v[1] + A[2][j] * v[2]);
const tr = A => [0, 1, 2].map(i => [A[0][i], A[1][i], A[2][i]]);
function euler(r) {
  const [x, y, z] = r.map(a => a * Math.PI / 180);
  const Rx = [[1, 0, 0], [0, Math.cos(x), -Math.sin(x)], [0, Math.sin(x), Math.cos(x)]];
  const Ry = [[Math.cos(y), 0, Math.sin(y)], [0, 1, 0], [-Math.sin(y), 0, Math.cos(y)]];
  const Rz = [[Math.cos(z), -Math.sin(z), 0], [Math.sin(z), Math.cos(z), 0], [0, 0, 1]];
  return mm(mm(Rx, Ry), Rz);
}
function ik(root, target, l1, l2, pole) {
  const d = sub(target, root);
  const dist = Math.min(len(d), l1 + l2 - 1e-4);
  const dn = norm(d);
  const a = (l1 * l1 + dist * dist - l2 * l2) / (2 * dist);
  const h = Math.sqrt(Math.max(l1 * l1 - a * a, 0));
  const pp = norm(sub(pole, mul(dn, dot(pole, dn))));
  return [add(add(root, mul(dn, a)), mul(pp, h)), add(root, mul(dn, dist))];
}
function frameOf(root, joint, pole) {
  const y = norm(sub(joint, root));
  let x = cross(y, pole);
  if (len(x) < 1e-9) x = Math.abs(y[2]) < 0.9 ? cross(y, [0, 0, 1]) : cross(y, [1, 0, 0]);
  x = norm(x);
  const z = cross(x, y);
  return [[x[0], y[0], z[0]], [x[1], y[1], z[1]], [x[2], y[2], z[2]]];
}
const applyT = (T, p) => add(mv(T[0], p), T[1]);
const invT = (T, p) => mtv(T[0], sub(p, T[1]));
const compose = (P, L) => [mm(P[0], L[0]), add(mv(P[0], L[1]), P[1])];
function segment(r0, j0, pole0, r, j, pole) {
  const R = mm(frameOf(r, j, pole), tr(frameOf(r0, j0, pole0)));
  return [R, sub(r, mv(R, r0))];
}
const IDT = [I3, [0, 0, 0]];

function poseOf(frameKey) {
  const f = S.model.frames[frameKey] || (S.model.frames[frameKey] = { pose: {} });
  return f.pose || (f.pose = {});
}

function solve(model, frameKey) {
  const pose = (model.frames[frameKey] || {}).pose || {};
  const T = {}, joints = {};
  const tpoint = (tg, rest) => Array.isArray(tg) ? tg : applyT(rest ? IDT : T[tg.bone], tg.point);
  for (const b of model.bones) {
    const P = b.parent ? T[b.parent] : IDT;
    const p = pose[b.name] || {};
    if (b.type === "free") {
      const R = euler(p.rot || [0, 0, 0]);
      const pv = b.pivot || [0, 0, 0], m = p.move || [0, 0, 0];
      T[b.name] = compose(P, [R, sub(add(pv, m), mv(R, pv))]);
      joints[b.name] = { pivot: applyT(T[b.name], pv) };
    } else {
      const [mid0, end0] = ik(b.root, tpoint(b.target, true), b.l1, b.l2, b.pole);
      const root = applyT(P, b.root);
      const tgt = tpoint(p.target || b.target, false);
      const pole = p.pole || b.pole;
      const [mid, end] = ik(root, tgt, b.l1, b.l2, pole);
      T[b.bones[0]] = segment(b.root, mid0, b.pole, root, mid, pole);
      T[b.bones[1]] = segment(mid0, end0, b.pole, mid, end, pole);
      if (b.end) { const Re = euler(p.end_rot || [0, 0, 0]); T[b.end] = [Re, sub(end, mv(Re, end0))]; }
      T[b.name] = T[b.bones[0]];
      joints[b.name] = { root, mid, end, target: tgt };
    }
  }
  return { T, joints };
}
const boneNames = () => {
  const out = [];
  for (const b of S.model.bones) {
    out.push(b.name);
    if (b.type === "ik") { out.push(...b.bones); if (b.end) out.push(b.end); }
  }
  return [...new Set(out.filter((n, i, a) => a.indexOf(n) === i))].filter(n => !(S.model.bones.find(b => b.name === n && b.type === "ik")));
};

// ------------------------------------------------------------------ part geometry helpers
const POINT_KEYS = ["c", "a", "b"];
function partCenter(p) {
  if (p.c) return p.c;
  return mul(add(p.a, p.b), 0.5);
}
// map a part through a point transform, a direction transform and a length scale
function mapPart(p, fp, fd, k = 1) {
  const q = clone(p);
  for (const key of POINT_KEYS) if (q[key]) q[key] = fp(q[key]);
  if (q.pin_at) q.pin_at = fp(q.pin_at);
  if (q.basis) q.basis = q.basis.map(fd);
  if (q.n) q.n = norm(fd(q.n));
  if (q.axis) q.axis = norm(fd(q.axis));
  if (q.grooves) { q.grooves.origin = fp(q.grooves.origin); q.grooves.axis = norm(fd(q.grooves.axis)); }
  if (k !== 1) {
    for (const key of ["r1", "r2", "R", "thick", "rnd", "wall"]) if (typeof q[key] === "number") q[key] *= k;
    if (typeof q.r === "number") q.r *= k; else if (Array.isArray(q.r)) q.r = mul(q.r, k);
    if (q.half) q.half = mul(q.half, k);
    if (q.grooves) { q.grooves.period *= k; q.grooves.amp *= k; }
  }
  return q;
}
const roundAll = o => JSON.parse(JSON.stringify(o, (k, v) => typeof v === "number" ? Math.round(v * 1e6) / 1e6 : v));
function movePart(p, d) { return mapPart(p, v => add(v, d), v => v); }
function scalePart(p, k) { const c = partCenter(p); return mapPart(p, v => add(c, mul(sub(v, c), k)), v => v, k); }
function rotatePart(p, R) {
  const c = partCenter(p);
  const q = mapPart(p, v => add(c, mv(R, sub(v, c))), v => mv(R, v));
  if (BASIS_TYPES.includes(q.type) && !q.basis) q.basis = tr(R);
  return q;
}
const flipName = s => s.replace(/\.L\b/g, ".__").replace(/\.R\b/g, ".L").replace(/\.__/g, ".R");
function mirrorPart(p) {
  const q = mapPart(p, v => [-v[0], v[1], v[2]], v => [-v[0], v[1], v[2]]);
  q.bone = flipName(q.bone); if (q.group) q.group = flipName(q.group);
  q.name = flipName(q.name || "part") + (flipName(q.name || "") === q.name ? " mirrored" : "");
  return q;
}
const DEFAULTS = {
  sphere: c => ({ c, r: 0.06 }),
  ellipsoid: c => ({ c, r: [0.08, 0.06, 0.05] }),
  capsule: c => ({ a: add(c, [0, -0.08, 0]), b: add(c, [0, 0.08, 0]), r: 0.03 }),
  roundcone: c => ({ a: add(c, [0, -0.1, 0]), b: add(c, [0, 0.1, 0]), r1: 0.05, r2: 0.03 }),
  box: c => ({ c, half: [0.06, 0.06, 0.06], rnd: 0.01 }),
  torus: c => ({ c, n: [0, 1, 0], R: 0.08, r: 0.02 }),
  disc: c => ({ c, axis: [0, 1, 0], r: 0.08, thick: 0.02, rnd: 0.003 }),
  cylinder: c => ({ a: add(c, [0, -0.08, 0]), b: add(c, [0, 0.08, 0]), r: 0.05, rnd: 0.004 }),
  cone: c => ({ a: add(c, [0, -0.08, 0]), b: add(c, [0, 0.08, 0]), r1: 0.06, r2: 0 }),
  tube: c => ({ a: add(c, [0, -0.08, 0]), b: add(c, [0, 0.08, 0]), r: 0.06, wall: 0.015 }),
  dome: c => ({ c, axis: [0, 1, 0], r: 0.07 }),
  wedge: c => ({ c, half: [0.06, 0.05, 0.08] }),
  pyramid: c => ({ c, half: [0.06, 0.08, 0.06] }),
  hexprism: c => ({ c, r: 0.06, thick: 0.03 }),
};
const BASIS_TYPES = ["box", "ellipsoid", "wedge", "pyramid", "hexprism"];   // turned with a basis

// ------------------------------------------------------------------ shape conversion
// Every part reduces to a centre, three local axes and half extents along them, so any
// shape can become any other at the same size and direction (round <-> blocky).
const IB = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
function axesAlong(d) {                 // orthonormal axes, the second one along d
  d = norm(d);
  const x = norm(cross(d, Math.abs(d[2]) < 0.9 ? [0, 0, 1] : [1, 0, 0]));
  return [x, d, cross(x, d)];
}
function shapeOf(p) {
  switch (p.type) {
    case "sphere": return { c: p.c, B: IB, h: [p.r, p.r, p.r] };
    case "ellipsoid": return { c: p.c, B: p.basis || IB, h: p.r.slice() };
    case "box": { const k = p.rnd || 0; return { c: p.c, B: p.basis || IB, h: p.half.map(v => v + k) }; }
    case "capsule": case "roundcone": {
      const d = sub(p.b, p.a), L = len(d);
      const r1 = p.type === "capsule" ? p.r : p.r1, r2 = p.type === "capsule" ? p.r : p.r2, rr = Math.max(r1, r2);
      return { c: mul(add(p.a, p.b), 0.5), B: L > 1e-6 ? axesAlong(d) : IB, h: [rr, L / 2 + rr, rr], r1, r2 };
    }
    case "torus": return { c: p.c, B: axesAlong(p.n), h: [p.R + p.r, p.r, p.R + p.r] };
    case "disc": return { c: p.c, B: axesAlong(p.axis), h: [p.r, p.thick / 2, p.r] };
    case "cylinder": case "tube": case "cone": {
      const d = sub(p.b, p.a), L = len(d), rr = p.type === "cone" ? Math.max(p.r1, p.r2) : p.r;
      return { c: mul(add(p.a, p.b), 0.5), B: L > 1e-6 ? axesAlong(d) : IB, h: [rr, L / 2, rr], r1: p.r1, r2: p.r2 };
    }
    case "dome": { const ax = norm(p.axis); return { c: add(p.c, mul(ax, p.r / 2)), B: axesAlong(ax), h: [p.r, p.r / 2, p.r] }; }
    case "wedge": case "pyramid": return { c: p.c, B: p.basis || IB, h: p.half.slice() };
    case "hexprism": return { c: p.c, B: p.basis || IB, h: [p.r, p.thick / 2, p.r] };
  }
}
// the axis a flat or round-topped shape stands on: the thinnest one, or the most upright on a tie
function upAxis(h, B) {
  const lo = Math.min(...h);
  const cand = [0, 1, 2].filter(k => h[k] - lo < 1e-6);
  return cand.reduce((a, k) => Math.abs(B[k][1]) > Math.abs(B[a][1]) ? k : a, cand[0]);
}
const isIdentity = B => B.every((r, i) => r.every((v, j) => Math.abs(v - (i === j ? 1 : 0)) < 1e-9));
const avg = a => a.reduce((x, y) => x + y, 0) / a.length;
function fromShape(type, s, round) {
  const { c, h, B } = s;
  const big = [0, 1, 2].reduce((a, k) => h[k] > h[a] ? k : a, 0);
  const small = [0, 1, 2].reduce((a, k) => h[k] < h[a] ? k : a, 0);
  const others = k => [0, 1, 2].filter(i => i !== k).map(i => h[i]);
  const basis = isIdentity(B) ? undefined : B.map(r => r.slice());
  switch (type) {
    case "sphere": return { c, r: avg(h) };
    case "ellipsoid": return { c, r: h.slice(), basis };
    case "box": { const k = Math.min(...h) * (round ?? 0.12); return { c, half: h.map(v => v - k), rnd: k, basis }; }
    case "capsule": case "roundcone": {
      const rr = Math.min(avg(others(big)), h[big]), e = h[big] - rr, ax = B[big];
      const q = { a: add(c, mul(ax, -e)), b: add(c, mul(ax, e)) };
      if (type === "capsule") q.r = rr; else { q.r1 = s.r1 ?? rr; q.r2 = s.r2 ?? rr * 0.7; }
      return q;
    }
    case "torus": { const r = h[small]; return { c, n: B[small].slice(), r, R: Math.max(avg(others(small)) - r, r) }; }
    case "disc": return { c, axis: B[small].slice(), r: avg(others(small)), thick: 2 * h[small], rnd: 0.003 };
    case "cylinder": case "tube": case "cone": {
      const rr = avg(others(big)), ax = B[big];
      const q = { a: add(c, mul(ax, -h[big])), b: add(c, mul(ax, h[big])) };
      if (type === "cylinder") { q.r = rr; q.rnd = Math.min(0.004, rr * 0.3); }
      else if (type === "tube") { q.r = rr; q.wall = rr * 0.3; }
      else { q.r1 = s.r1 ?? rr; q.r2 = s.r2 ?? 0; }
      return q;
    }
    case "dome": {
      const k = upAxis(h, B), ax = B[k][1] < 0 ? mul(B[k], -1) : B[k].slice();
      return { c: add(c, mul(ax, -h[k])), axis: ax, r: avg([0, 1, 2].filter(i => i !== k).map(i => h[i])) };
    }
    case "wedge": case "pyramid": return { c, half: h.slice(), basis };
    case "hexprism": {
      const k = upAxis(h, B), r = avg([0, 1, 2].filter(i => i !== k).map(i => h[i]));
      const b = [B[(k + 1) % 3], B[k], B[(k + 2) % 3]].map(v => v.slice());
      return { c, r, thick: 2 * h[k], basis: isIdentity(b) ? undefined : b };
    }
  }
}
const SHAPE_KEYS = ["c", "r", "a", "b", "r1", "r2", "half", "rnd", "basis", "n", "R", "axis", "thick", "wall"];
function convertPart(p, type, round) {
  const q = {};
  for (const [k, v] of Object.entries(p)) if (!SHAPE_KEYS.includes(k)) q[k] = v;
  q.type = type;
  for (const [k, v] of Object.entries(fromShape(type, shapeOf(p), round))) if (v !== undefined) q[k] = v;
  return roundAll(q);
}
function makeRound(p) {                  // long parts become capsules, the rest ellipsoids
  const h = shapeOf(p).h.slice().sort((a, b) => b - a);
  return convertPart(p, h[0] > 1.6 * (h[1] + h[2]) / 2 ? "capsule" : "ellipsoid");
}
function scopeIdx(scope = S.scope) {
  const p = S.model.parts[S.sel];
  if (!p) return [];
  if (scope === "all") return S.model.parts.map((_, i) => i);
  if (scope === "bone") return S.model.parts.map((q, i) => q.bone === p.bone ? i : -1).filter(i => i >= 0);
  return [S.sel];
}
function applyShape(fn) { beginEdit(); for (const i of scopeIdx()) S.model.parts[i] = fn(S.model.parts[i]); commit("shape"); }

// ------------------------------------------------------------------ history
function snapshot() { return JSON.stringify(S.model); }
function commit(label) {
  S.undo.push(S._before ?? snapshot());
  if (S.undo.length > 200) S.undo.shift();
  S.redo = [];
  S._before = null;
  S.dirty = true;
  refreshAll();
  scheduleRender();
}
function beginEdit() { if (S._before == null) S._before = snapshot(); }
function undo() { if (!S.undo.length) return; S.redo.push(snapshot()); S.model = JSON.parse(S.undo.pop()); S.dirty = true; refreshAll(); scheduleRender(); }
function redo() { if (!S.redo.length) return; S.undo.push(snapshot()); S.model = JSON.parse(S.redo.pop()); S.dirty = true; refreshAll(); scheduleRender(); }

// ------------------------------------------------------------------ 3D view
const canvas = $("#c3d");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(window.devicePixelRatio);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x101114);
scene.environment = new THREE.PMREMGenerator(renderer).fromScene(new RoomEnvironment(), 0.04).texture;
const persp = new THREE.PerspectiveCamera(35, 1, 0.01, 100);
persp.position.set(1.75, 1.6, 3.0);        // starts on the same side as the sprite camera
const ortho = new THREE.OrthographicCamera(-1, 1, 1, -1, -20, 20);
let camera = persp;
const orbit = new OrbitControls(persp, canvas);
orbit.target.set(0, 0.95, 0);
orbit.update();
scene.add(new THREE.HemisphereLight(0xdfe6ff, 0x302820, 0.9));
const sun = new THREE.DirectionalLight(0xffffff, 1.6);
sun.position.set(-1.5, 3, 2);
scene.add(sun);
const grid = new THREE.GridHelper(4, 40, 0x3a3d46, 0x24262c);
scene.add(grid);
const fwdArrow = new THREE.ArrowHelper(new THREE.Vector3(0, 0, 1), new THREE.Vector3(0, 0.002, 0), 0.5, 0x5aa9e6, 0.08, 0.05);
scene.add(fwdArrow);

const root = new THREE.Group();
scene.add(root);
const boneLayer = new THREE.Group();
scene.add(boneLayer);
const gizmo = new TransformControls(persp, canvas);
gizmo.setSize(0.8);
scene.add(gizmo);
gizmo.addEventListener("dragging-changed", e => { orbit.enabled = !e.value; if (e.value) beginEdit(); else gizmoDone(); });
gizmo.addEventListener("objectChange", () => gizmoLive());

const geoCache = new Map();
const matCache = new Map();
function colorOf(m) { const c = m.color || [0.7, 0.7, 0.7]; return new THREE.Color(c[0], c[1], c[2]); }
function material3d(name, part, selected) {
  const m = S.model.materials[name] || { kind: "paint", color: [1, 0, 1] };
  const style = (S.model.render || {}).style || "studio";
  const wire = $("#wire3d").checked;
  const key = [name, JSON.stringify(m), style, part.op === "cut", selected, wire].join("|");
  if (matCache.has(key)) return matCache.get(key);
  let mat;
  if (part.op === "cut") mat = new THREE.MeshBasicMaterial({ color: 0xff4040, transparent: true, opacity: 0.28, depthWrite: false });
  else if (m.kind === "glow" || m.kind === "flat") mat = new THREE.MeshBasicMaterial({ color: colorOf(m) });
  else if (style === "cel") mat = new THREE.MeshToonMaterial({ color: colorOf(m) });
  else if (m.kind === "chrome") mat = new THREE.MeshStandardMaterial({ color: colorOf(m), metalness: 1, roughness: 0.18 });
  else mat = new THREE.MeshStandardMaterial({ color: colorOf(m), metalness: 0.35, roughness: 0.5 });
  if (selected && mat.emissive) { mat.emissive = new THREE.Color(0xe0a040); mat.emissiveIntensity = 0.45; }
  if (selected && !mat.emissive) { mat = mat.clone(); mat.color = new THREE.Color(0xffd080); }
  if (wire) mat.wireframe = true;
  matCache.set(key, mat);
  return mat;
}
const Y = new THREE.Vector3(0, 1, 0), Z = new THREE.Vector3(0, 0, 1);
const v3 = a => new THREE.Vector3(a[0], a[1], a[2]);
function orient(obj, from, dir) { obj.quaternion.setFromUnitVectors(from, v3(norm(dir))); }
function basisMatrix(b) { return new THREE.Matrix4().makeBasis(v3(b[0]), v3(b[1]), v3(b[2])); }

// one THREE object per part, placed in rest coordinates (the bone group carries the pose)
function partObject(p, i, selected) {
  const mat = material3d(p.mat, p, selected);
  const o = new THREE.Group();
  const mesh = (geo, setup) => { const m = new THREE.Mesh(geo, mat); m.userData.part = i; if (setup) setup(m); o.add(m); return m; };
  const cen = partCenter(p);
  o.position.set(...cen);
  const rel = a => sub(a, cen);
  switch (p.type) {
    case "sphere": mesh(new THREE.SphereGeometry(p.r, 20, 14)); break;
    case "ellipsoid": mesh(new THREE.SphereGeometry(1, 24, 16), m => { m.scale.set(...p.r); });
      if (p.basis) o.quaternion.setFromRotationMatrix(basisMatrix(p.basis)); break;
    case "capsule": {
      const d = sub(p.b, p.a), L = len(d);
      mesh(new THREE.CapsuleGeometry(p.r, Math.max(L, 1e-4), 6, 14), m => { if (L > 1e-6) orient(m, Y, d); });
      break;
    }
    case "roundcone": {
      const d = sub(p.b, p.a), L = len(d);
      mesh(new THREE.SphereGeometry(p.r1, 16, 12), m => m.position.set(...rel(p.a)));
      mesh(new THREE.SphereGeometry(p.r2, 16, 12), m => m.position.set(...rel(p.b)));
      if (L > 1e-6) mesh(new THREE.CylinderGeometry(p.r2, p.r1, L, 16, 1, true), m => orient(m, Y, d));
      break;
    }
    case "box": {
      const h = p.half, rnd = p.rnd || 0;
      const g = new RoundedBoxGeometry(2 * (h[0] + rnd), 2 * (h[1] + rnd), 2 * (h[2] + rnd), 2, Math.max(rnd, 0.0005));
      mesh(g);
      if (p.basis) o.quaternion.setFromRotationMatrix(basisMatrix(p.basis));
      break;
    }
    case "torus": mesh(new THREE.TorusGeometry(p.R, p.r, 10, 28), m => orient(m, Z, p.n)); break;
    case "disc": mesh(new THREE.CylinderGeometry(p.r, p.r, p.thick, 24), m => orient(m, Y, p.axis)); break;
    case "cylinder": case "cone": case "tube": {
      const d = sub(p.b, p.a), L = Math.max(len(d), 1e-4);
      let g;
      if (p.type === "cylinder") g = new THREE.CylinderGeometry(p.r, p.r, L, 20);
      else if (p.type === "cone") g = new THREE.CylinderGeometry(p.r2, p.r1, L, 20);
      else {
        const ri = Math.max(p.r - p.wall, 1e-4), h = L / 2;
        g = new THREE.LatheGeometry([[ri, -h], [p.r, -h], [p.r, h], [ri, h], [ri, -h]].map(([x, y]) => new THREE.Vector2(x, y)), 24);
      }
      const m = mesh(g, m => { if (len(d) > 1e-6) orient(m, Y, d); });
      if (p.type === "tube") { m.material = mat.clone(); m.material.side = THREE.DoubleSide; }
      break;
    }
    case "dome": {
      const g = new THREE.Group();
      g.add(new THREE.Mesh(new THREE.SphereGeometry(p.r, 20, 10, 0, Math.PI * 2, 0, Math.PI / 2), mat));
      g.add(new THREE.Mesh(new THREE.CircleGeometry(p.r, 20).rotateX(Math.PI / 2), mat));
      g.children.forEach(m => m.userData.part = i);
      orient(g, Y, p.axis); o.add(g);
      break;
    }
    case "wedge": case "pyramid": case "hexprism": {
      let g;
      if (p.type === "wedge") {
        const [hx, hy, hz] = p.half;
        g = new THREE.BoxGeometry(2 * hx, 2 * hy, 2 * hz);
        const pos = g.attributes.position;
        for (let k = 0; k < pos.count; k++) if (pos.getY(k) > 0 && pos.getZ(k) > 0) pos.setZ(k, -hz);   // cut the top front edge
        g.computeVertexNormals();
      } else if (p.type === "pyramid") {
        g = new THREE.ConeGeometry(1, 1, 4, 1).rotateY(Math.PI / 4).scale(p.half[0] / Math.SQRT1_2, 2 * p.half[1], p.half[2] / Math.SQRT1_2);
      } else g = new THREE.CylinderGeometry(p.r, p.r, p.thick, 6);
      mesh(g);
      if (p.basis) o.quaternion.setFromRotationMatrix(basisMatrix(p.basis));
      break;
    }
  }
  o.userData.part = i;
  return o;
}

let boneGroups = {}, partObjs = [], handles = [];
function rebuild3d() {
  root.clear();
  boneGroups = {};
  partObjs = [];
  if (!S.model || Cut.isCut(S.model)) return;
  const { T, joints } = solve(S.model, S.frame);
  const showCuts = $("#showCuts").checked;
  S.model.parts.forEach((p, i) => {
    const fr = p.frames;
    if (p.hidden || (fr && fr.length && !fr.includes(S.frame))) { partObjs[i] = null; return; }
    if (p.op === "cut" && !showCuts && i !== S.sel) { partObjs[i] = null; return; }
    let g = boneGroups[p.bone];
    if (!g) {
      g = boneGroups[p.bone] = new THREE.Group();
      g.matrixAutoUpdate = false;
      const t = T[p.bone] || IDT;
      const R = t[0], v = t[1];
      g.matrix.set(R[0][0], R[0][1], R[0][2], v[0], R[1][0], R[1][1], R[1][2], v[1], R[2][0], R[2][1], R[2][2], v[2], 0, 0, 0, 1);
      root.add(g);
    }
    const o = partObject(p, i, i === S.sel);
    g.add(o);
    partObjs[i] = o;
  });
  root.updateMatrixWorld(true);
  drawBones(joints);
  attachGizmo();
}

function drawBones(joints) {
  boneLayer.clear();
  handles = [];
  if (!$("#showBones").checked) return;
  const lineMat = new THREE.LineBasicMaterial({ color: 0x5aa9e6, depthTest: false, transparent: true, opacity: 0.8 });
  const dot3 = (p, color, r = 0.025, data) => {
    const m = new THREE.Mesh(new THREE.SphereGeometry(r, 12, 8), new THREE.MeshBasicMaterial({ color, depthTest: false, transparent: true, opacity: 0.9 }));
    m.position.set(...p); m.renderOrder = 10; if (data) m.userData.handle = data;
    boneLayer.add(m); return m;
  };
  for (const b of S.model.bones) {
    const j = joints[b.name];
    if (b.type === "ik") {
      const g = new THREE.BufferGeometry().setFromPoints([v3(j.root), v3(j.mid), v3(j.end)]);
      const line = new THREE.Line(g, lineMat); line.renderOrder = 9; boneLayer.add(line);
      dot3(j.mid, 0x5aa9e6, 0.015);
      handles.push(dot3(j.target, 0xffd040, 0.03, { bone: b.name, kind: "target" }));
    } else {
      handles.push(dot3(j.pivot, 0x60e0a0, 0.028, { bone: b.name, kind: "free" }));
    }
  }
}

// gizmo: parts tab moves/turns the selected part; pose tab moves IK targets and free bones
let gizmoProxy = new THREE.Object3D();
scene.add(gizmoProxy);
let gizmoInfo = null;
function attachGizmo() {
  gizmo.detach();
  gizmoInfo = null;
  if (Cut.isCut(S.model)) return;
  if (S.tab === "pose" && S.poseHandle) {
    const h = handles.find(o => o.userData.handle.bone === S.poseHandle);
    if (!h) return;
    gizmoProxy.position.copy(h.position);
    gizmoProxy.quaternion.identity();
    gizmoInfo = { kind: "pose", bone: S.poseHandle, start: h.position.clone(), startQ: new THREE.Quaternion() };
    gizmo.attach(gizmoProxy);
  } else if (S.tab === "parts" && S.sel >= 0 && partObjs[S.sel]) {
    const o = partObjs[S.sel];
    const wp = new THREE.Vector3(); o.getWorldPosition(wp);
    gizmoProxy.position.copy(wp);
    gizmoProxy.quaternion.identity();
    gizmoInfo = { kind: "part", start: wp.clone(), base: clone(S.model.parts[S.sel]) };
    gizmo.attach(gizmoProxy);
  }
}
function boneT(name) { return solve(S.model, S.frame).T[name] || IDT; }
function gizmoLive() {
  if (!gizmoInfo) return;
  const wp = gizmoProxy.position.toArray();
  if (gizmoInfo.kind === "part") {
    const i = S.sel, T = boneT(S.model.parts[i].bone);
    if (gizmo.mode === "translate") {
      const d = sub(invT(T, wp), invT(T, gizmoInfo.start.toArray()));
      S.model.parts[i] = movePart(gizmoInfo.base, d);
    } else {
      const q = gizmoProxy.quaternion;
      const m = new THREE.Matrix4().makeRotationFromQuaternion(q).elements;
      const Rw = [[m[0], m[4], m[8]], [m[1], m[5], m[9]], [m[2], m[6], m[10]]];
      const R = mm(mm(tr(T[0]), Rw), T[0]);          // world turn expressed in rest coordinates
      S.model.parts[i] = rotatePart(gizmoInfo.base, R);
    }
    updatePartObject(i);
  } else {
    const b = S.model.bones.find(x => x.name === gizmoInfo.bone);
    const pose = poseOf(S.frame);
    const pb = pose[b.name] || (pose[b.name] = {});
    if (b.type === "ik") {
      const tg = pb.target || b.target;
      if (Array.isArray(tg)) pb.target = wp.map(r3);
      else pb.target = { bone: tg.bone, point: invT(boneT(tg.bone), wp).map(r3) };
    } else if (gizmo.mode === "translate") {
      const P = b.parent ? boneT(b.parent) : IDT;
      const base = (gizmoInfo.baseMove ??= (pb.move || [0, 0, 0]).slice());
      const d = sub(invT(P, wp), invT(P, gizmoInfo.start.toArray()));
      pb.move = add(base, d).map(r3);
    } else {
      const base = (gizmoInfo.baseRot ??= new THREE.Quaternion().setFromEuler(new THREE.Euler(...(pb.rot || [0, 0, 0]).map(a => a * Math.PI / 180), "XYZ")));
      const q = gizmoProxy.quaternion.clone().multiply(base);
      const e = new THREE.Euler().setFromQuaternion(q, "XYZ");
      pb.rot = [e.x, e.y, e.z].map(a => Math.round(a * 1800 / Math.PI) / 10);
    }
    rebuild3dKeepGizmo();
    renderPose(true);
  }
}
function rebuild3dKeepGizmo() {
  const keep = gizmoInfo;
  const pos = gizmoProxy.position.clone(), q = gizmoProxy.quaternion.clone();
  rebuild3d();
  gizmoInfo = keep; gizmoProxy.position.copy(pos); gizmoProxy.quaternion.copy(q);
  gizmo.attach(gizmoProxy);
}
function updatePartObject(i) {
  const old = partObjs[i];
  if (!old) return rebuild3dKeepGizmo();
  const o = partObject(S.model.parts[i], i, i === S.sel);
  old.parent.add(o); old.parent.remove(old);
  partObjs[i] = o;
}
function gizmoDone() {
  if (gizmoInfo && gizmoInfo.kind === "part") S.model.parts[S.sel] = roundAll(S.model.parts[S.sel]);
  commit("gizmo");
}

function resize3d() {
  const w = canvas.clientWidth, h = canvas.clientHeight;
  if (!w || !h) return;
  if (canvas.width !== Math.floor(w * devicePixelRatio) || canvas.height !== Math.floor(h * devicePixelRatio)) {
    renderer.setSize(w, h, false);
  }
  persp.aspect = w / h; persp.updateProjectionMatrix();
  const f = camera === ortho && spriteFrame();
  const span = f ? Math.max(f.halfH, f.halfW * h / w) * 1.04 : 1.25;
  if (ortho.top !== span || ortho.right !== span * w / h) {
    ortho.left = -span * w / h; ortho.right = span * w / h; ortho.top = span; ortho.bottom = -span; ortho.updateProjectionMatrix();
  }
}
// the render canvas in camera space, as the engine maps it: pixel (u, v) <-> ((u - cx) / K, (y0 - v) / K)
function spriteFrame() {
  const r = S.model.render || {}, [w, h] = r.res || [64, 64];
  const K = (r.px_per_m ?? (r.style === "studio" ? 34 / 1.88 : 34.6 / 1.73)) * (r.scale ?? 1);
  const cx = r.cx ?? w / 2, y0 = r.y0 ?? h - 2.4;
  return { centre: [(w / 2 - cx) / K, (y0 - h / 2) / K, 0], halfW: w / 2 / K, halfH: h / 2 / K };
}
function loop() {
  if (!document.body.classList.contains("mode2d")) { resize3d(); renderer.render(scene, camera); }
  requestAnimationFrame(loop);
}

// sprite camera: same yaw/pitch as the engine, orthographic
const canvasBox = new THREE.LineLoop(new THREE.BufferGeometry(), new THREE.LineBasicMaterial({ color: 0x8a8f9c, transparent: true, opacity: 0.6, depthTest: false }));
canvasBox.visible = false; canvasBox.renderOrder = 9;
scene.add(canvasBox);
function useSpriteCam(on) {
  if (on) {
    const r = S.model.render || {};
    const yaw = (r.yaw ?? -30) * Math.PI / 180, pitch = (r.pitch ?? 9) * Math.PI / 180;
    // engine: p_cam = A @ p_model with A = Rx(pitch) @ Ry(yaw); the camera looks down -z_cam
    const Ry = [[Math.cos(yaw), 0, Math.sin(yaw)], [0, 1, 0], [-Math.sin(yaw), 0, Math.cos(yaw)]];
    const Rx = [[1, 0, 0], [0, Math.cos(pitch), -Math.sin(pitch)], [0, Math.sin(pitch), Math.cos(pitch)]];
    const A = mm(Rx, Ry);
    const back = mtv(A, [0, 0, 1]), up = mtv(A, [0, 1, 0]);
    const f = spriteFrame(), target = mtv(A, f.centre);       // centre of the render canvas
    ortho.position.set(...add(target, mul(back, 8)));
    // outline of the sprite canvas, so it is clear what the render will show
    const corner = (sx, sy) => new THREE.Vector3(...mtv(A, [f.centre[0] + sx * f.halfW, f.centre[1] + sy * f.halfH, 0]));
    canvasBox.geometry.dispose();
    canvasBox.geometry = new THREE.BufferGeometry().setFromPoints([corner(-1, -1), corner(1, -1), corner(1, 1), corner(-1, 1)]);
    canvasBox.visible = true;
    ortho.up.set(...up);
    ortho.lookAt(...target);
    ortho.near = -40; ortho.far = 40; ortho.updateProjectionMatrix();
    camera = ortho;
    resize3d();
    orbit.enabled = false;
    gizmo.camera = ortho;
  } else {
    camera = persp; orbit.enabled = true; gizmo.camera = persp;
    canvasBox.visible = false;
  }
  $("#btnSpriteCam").classList.toggle("on", on);
  $("#btnFreeCam").classList.toggle("on", !on);
}

// picking
const ray = new THREE.Raycaster();
let downAt = null;
canvas.addEventListener("pointerdown", e => { downAt = [e.clientX, e.clientY]; });
canvas.addEventListener("pointerup", e => {
  if (!downAt || Math.hypot(e.clientX - downAt[0], e.clientY - downAt[1]) > 4 || gizmo.dragging) return;
  const r = canvas.getBoundingClientRect();
  ray.setFromCamera(new THREE.Vector2(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1), camera);
  if (S.tab === "pose") {
    const hit = ray.intersectObjects(handles, false)[0];
    if (hit) { S.poseHandle = hit.object.userData.handle.bone; renderPose(); attachGizmo(); return; }
  }
  const hits = ray.intersectObjects(root.children, true).filter(h => h.object.userData.part !== undefined);
  const solid = hits.find(h => S.model.parts[h.object.userData.part].op !== "cut") || hits[0];
  if (solid) select(solid.object.userData.part, true);
});

// ------------------------------------------------------------------ selection + part list
function select(i, scroll) {
  if (Cut.isCut(S.model)) return;
  S.sel = i;
  if (S.tab !== "parts" && i >= 0) setTab("parts");
  rebuild3d();
  renderTree(scroll);
  renderInspector();
}
function matSwatch(name) {
  const m = S.model.materials[name];
  const c = m ? m.color.map(v => Math.round(Math.min(1, v) * 255)) : [255, 0, 255];
  return `rgb(${c.join(",")})`;
}
function renderTree(scroll) {
  const box = $("#partTree");
  box.innerHTML = "";
  const f = $("#partFilter").value.toLowerCase();
  const byBone = {};
  S.model.parts.forEach((p, i) => {
    if (f && !(`${p.name} ${p.type} ${p.mat} ${p.bone}`.toLowerCase().includes(f))) return;
    (byBone[p.bone] ||= []).push(i);
  });
  const order = [...new Set([...boneNames(), ...Object.keys(byBone)])];
  for (const bone of order) {
    const list = byBone[bone] || [];
    if (!list.length && (f || !S.model.bones.some(b => b.name === bone && b.type === "free"))) continue;
    const open = !!f || list.includes(S.sel);
    const d = el("details", { open },
      el("summary", {}, el("b", {}, bone), ` · ${list.length}`),
      list.length ? null : el("p", { class: "hint" }, "No parts yet: pick this bone in a part's “bone” box."),
      list.map(i => {
        const p = S.model.parts[i];
        return el("div", { class: "prow" + (i === S.sel ? " sel" : "") + (p.hidden ? " hid" : ""), "data-i": i, onclick: () => select(i) },
          el("span", { class: "sw", style: `background:${matSwatch(p.mat)}` }),
          el("span", { class: "nm" }, p.name || `${p.type} ${i}`),
          p.op === "cut" ? el("span", { class: "cut" }, "cut") : null,
          p.frames && p.frames.length ? el("span", { class: "ty" }, "f" + p.frames.join(",")) : null,
          el("span", { class: "ty" }, p.type),
          el("span", { class: "eye", title: "hide/show", onclick: e => { e.stopPropagation(); beginEdit(); p.hidden = !p.hidden; commit("hide"); } }, p.hidden ? "◌" : "●"));
      }));
    box.append(d);
  }
  if (scroll) { const s = box.querySelector(".prow.sel"); if (s) s.scrollIntoView({ block: "nearest" }); }
}

// ------------------------------------------------------------------ inspector
function numInput(value, onchange, step = 0.005) {
  const i = el("input", { type: "number", step, value: r3(value) });
  i.addEventListener("focus", beginEdit);
  i.addEventListener("input", () => { const v = parseFloat(i.value); if (!isNaN(v)) onchange(v, false); });
  i.addEventListener("change", () => { const v = parseFloat(i.value); if (!isNaN(v)) { onchange(v, true); } });
  return i;
}
function field(label, ...inputs) { return el("div", { class: "field" }, el("label", {}, label), el("div", { class: "vec" }, inputs)); }
function vecField(label, obj, key, step) {
  return field(label, [0, 1, 2].map(k => numInput(obj[key][k], (v, done) => { obj[key][k] = v; liveOrCommit(done); }, step)));
}
function numField(label, obj, key, step) {
  return field(label, numInput(obj[key], (v, done) => { obj[key] = v; liveOrCommit(done); }, step));
}
function liveOrCommit(done) {
  if (done) commit("edit");
  else if (S.sel >= 0) updatePartObject(S.sel);
}
function selectField(label, value, options, onchange) {
  const s = el("select", {}, options.map(o => el("option", { value: o, selected: o === value }, o)));
  s.addEventListener("change", () => { beginEdit(); onchange(s.value); commit("edit"); });
  return field(label, s);
}
function renderInspector() {
  const box = $("#inspector");
  box.innerHTML = "";
  const p = S.model && S.model.parts[S.sel];
  if (!p) { box.append(el("p", { class: "hint" }, "Click a part in the 3D view or the list.")); return; }
  const nameIn = el("input", { type: "text", value: p.name || "" });
  nameIn.addEventListener("change", () => { beginEdit(); p.name = nameIn.value; commit("rename"); });
  box.append(field("name", nameIn));
  box.append(shapeGroup(p));
  box.append(selectField("color", p.mat, Object.keys(S.model.materials), v => { p.mat = v; }));
  box.append(selectField("bone", p.bone, boneNames(), v => { p.bone = v; if (p.group) p.group = v; }));
  box.append(selectField("op", p.op || "add", ["add", "cut"], v => { p.op = v; }));
  const fr = el("div", { class: "vec" }, Object.keys(S.model.frames).map(k => {
    const c = el("input", { type: "checkbox", checked: !p.frames || !p.frames.length || p.frames.includes(k) });
    c.addEventListener("change", () => {
      beginEdit();
      const all = Object.keys(S.model.frames);
      let cur = p.frames && p.frames.length ? p.frames.slice() : all.slice();
      cur = c.checked ? [...new Set([...cur, k])] : cur.filter(x => x !== k);
      if (cur.length === all.length) delete p.frames; else p.frames = cur;
      commit("frames");
    });
    return el("label", { class: "chk" }, c, (S.model.frames[k].label || k));
  }));
  box.append(field("shows in", fr));

  const g = el("div", { class: "group" }, el("h4", {}, "Shape (metres)"));
  const P = { sphere: [["c", "centre"], ["r", "radius"]], ellipsoid: [["c", "centre"], ["r", "radii"]],
    capsule: [["a", "end A"], ["b", "end B"], ["r", "radius"]], roundcone: [["a", "end A"], ["b", "end B"], ["r1", "radius A"], ["r2", "radius B"]],
    box: [["c", "centre"], ["half", "half size"], ["rnd", "rounding"]], torus: [["c", "centre"], ["n", "axis"], ["R", "ring radius"], ["r", "tube radius"]],
    disc: [["c", "centre"], ["axis", "axis"], ["r", "radius"], ["thick", "thickness"], ["rnd", "rounding"]],
    cylinder: [["a", "end A"], ["b", "end B"], ["r", "radius"], ["rnd", "rounding"]],
    cone: [["a", "base"], ["b", "tip"], ["r1", "base radius"], ["r2", "tip radius"]],
    tube: [["a", "end A"], ["b", "end B"], ["r", "outer radius"], ["wall", "wall"]],
    dome: [["c", "base centre"], ["axis", "up"], ["r", "radius"]],
    wedge: [["c", "centre"], ["half", "half size"]], pyramid: [["c", "centre"], ["half", "half size"]],
    hexprism: [["c", "centre"], ["r", "corner radius"], ["thick", "thickness"]] }[p.type];
  for (const [k, label] of P) {
    if (p[k] === undefined) p[k] = DEFAULTS[p.type]([0, 0, 0])[k] ?? 0;
    g.append(Array.isArray(p[k]) ? vecField(label, p, k, 0.005) : numField(label, p, k, 0.002));
  }
  // size slider: scales the part about its centre
  const base = { part: null };
  const sz = el("input", { type: "range", min: 25, max: 300, value: 100 });
  const szv = el("span", {}, "100%");
  sz.addEventListener("pointerdown", () => { beginEdit(); base.part = clone(p); });
  sz.addEventListener("input", () => {
    if (!base.part) { beginEdit(); base.part = clone(S.model.parts[S.sel]); }
    szv.textContent = sz.value + "%";
    S.model.parts[S.sel] = scalePart(base.part, sz.value / 100);
    updatePartObject(S.sel);
  });
  sz.addEventListener("change", () => { S.model.parts[S.sel] = roundAll(S.model.parts[S.sel]); base.part = null; commit("scale"); });
  g.append(field("size", el("div", { class: "slider", style: "grid-template-columns:1fr 44px" }, sz, szv)));
  const turn = (ax, deg) => () => {
    beginEdit();
    const R = euler(ax === "x" ? [deg, 0, 0] : ax === "y" ? [0, deg, 0] : [0, 0, deg]);
    S.model.parts[S.sel] = roundAll(rotatePart(S.model.parts[S.sel], R));
    commit("turn");
  };
  g.append(field("turn 15°", el("div", { class: "btns" },
    ["x", "y", "z"].flatMap(ax => [el("button", { onclick: turn(ax, -15) }, ax + "−"), el("button", { onclick: turn(ax, 15) }, ax + "+")]))));
  box.append(g);

  const gr = el("div", { class: "group" }, el("h4", {}, "Grooves (ribs, fins, teeth)"));
  const has = el("input", { type: "checkbox", checked: !!p.grooves });
  has.addEventListener("change", () => {
    beginEdit();
    if (has.checked) p.grooves = { origin: partCenter(p).slice(), axis: [0, 1, 0], period: 0.03, amp: 0.006 };
    else delete p.grooves;
    commit("grooves");
  });
  gr.append(field("ribbed", has));
  if (p.grooves) {
    gr.append(vecField("axis", p.grooves, "axis", 0.1), numField("spacing", p.grooves, "period", 0.002), numField("depth", p.grooves, "amp", 0.001));
    gr.append(el("p", { class: "hint" }, "Grooves only show in the sprite render."));
  }
  box.append(gr);

  const adv = el("div", { class: "group" }, el("h4", {}, "Advanced"));
  const grpIn = el("input", { type: "text", value: p.group || "" , placeholder: p.bone });
  grpIn.addEventListener("change", () => { beginEdit(); if (grpIn.value) p.group = grpIn.value; else delete p.group; commit("group"); });
  adv.append(field("cut group", grpIn));
  adv.append(el("p", { class: "hint" }, "A cut removes material from the parts listed before it in the same cut group."));
  box.append(adv);
}

// Shape group: change shape type (keeping size and direction) and round <-> blocky,
// for this part, every part on its bone, or the whole model.
function shapeGroup(p) {
  const g = el("div", { class: "group" }, el("h4", {}, "Shape"));
  S.scope = S.scope || "part";
  const scopes = [["part", "This part"], ["bone", `Bone "${p.bone}"`], ["all", "Whole model"]];
  g.append(el("div", { class: "scopebar" }, el("span", { class: "hint", style: "margin:0" }, "apply to"),
    el("span", { class: "seg" }, scopes.map(([k, label]) => el("button", {
      class: S.scope === k ? "on" : "", title: `Changes ${scopeIdx(k).length} part(s)`,
      onclick: () => { S.scope = k; renderInspector(); } }, label)))));
  const cur = S.scope === "part" ? p.type : null;
  g.append(el("div", { class: "shapebtns" }, Object.keys(DEFAULTS).map(t => el("button", {
    class: cur === t ? "on" : "", title: `Make ${S.scope === "part" ? "it" : "them"} a ${t}, same size and direction`,
    onclick: () => applyShape(q => q.type === t ? q : convertPart(q, t)) }, t))));
  // round <-> blocky slider: 0 = smooth ellipsoids/capsules, 100 = sharp boxes
  const base = { parts: null };
  const bl = el("input", { type: "range", min: 0, max: 100, value: S.scope === "part" ? blockiness(p) : 50 });
  const blv = el("span", {}, bl.value + "%");
  bl.addEventListener("pointerdown", () => { beginEdit(); base.parts = scopeIdx().map(i => [i, clone(S.model.parts[i])]); });
  bl.addEventListener("input", () => {
    if (!base.parts) { beginEdit(); base.parts = scopeIdx().map(i => [i, clone(S.model.parts[i])]); }
    blv.textContent = bl.value + "%";
    const v = bl.value / 100;
    for (const [i, q] of base.parts) S.model.parts[i] = v < 0.02 ? makeRound(q) : convertPart(q, "box", 1 - v);
    if (base.parts.length === 1) updatePartObject(base.parts[0][0]); else rebuild3dKeepGizmo();
  });
  bl.addEventListener("change", () => { base.parts = null; commit("blockiness"); });
  g.append(field("blocky", el("div", { class: "slider", style: "grid-template-columns:1fr 44px" }, bl, blv)));
  g.append(el("p", { class: "hint" }, "0% = smooth (ellipsoids, capsules) · 100% = sharp boxes. Use Undo to go back."));
  return g;
}
function blockiness(p) {
  if (p.type !== "box") return 0;
  const h = shapeOf(p).h, k = p.rnd || 0;
  return Math.round(100 * (1 - k / Math.min(...h)));
}

// ------------------------------------------------------------------ pose panel
function slider(label, value, min, max, step, onlive, ondone) {
  const r = el("input", { type: "range", min, max, step, value });
  const n = el("input", { type: "number", min, max, step, value: r3(value) });
  r.addEventListener("pointerdown", beginEdit);
  r.addEventListener("input", () => { beginEdit(); n.value = r.value; onlive(parseFloat(r.value)); });
  r.addEventListener("change", ondone);
  n.addEventListener("focus", beginEdit);
  n.addEventListener("change", () => { r.value = n.value; onlive(parseFloat(n.value)); ondone(); });
  return el("div", { class: "slider" }, el("span", {}, label), r, n);
}
function renderPose(valuesOnly) {
  if (valuesOnly && S.tab !== "pose") return;
  const box = $("#poseList");
  box.innerHTML = "";
  const pose = poseOf(S.frame);
  const live = () => rebuild3dKeepGizmo();
  const done = () => commit("pose");
  for (const b of S.model.bones) {
    const pb = pose[b.name] || {};
    const set = (key, idx, def) => v => {
      const q = pose[b.name] || (pose[b.name] = {});
      if (!q[key]) q[key] = clone(def);
      q[key][idx] = v;
      live();
    };
    const card = el("div", { class: "bone", style: S.poseHandle === b.name ? "outline:1px solid #e0a040" : "" },
      el("h4", {}, el("span", { style: "cursor:pointer", onclick: () => { S.poseHandle = b.name; renderPose(); attachGizmo(); } }, b.name),
        el("small", {}, b.type === "ik" ? "reach (IK)" : "turn / move"),
        el("button", { onclick: () => { beginEdit(); delete pose[b.name]; commit("reset bone"); } }, "reset")));
    if (b.type === "free") {
      const rot = pb.rot || [0, 0, 0], move = pb.move || [0, 0, 0];
      ["x", "y", "z"].forEach((ax, k) => card.append(slider(`turn ${ax}`, rot[k], -180, 180, 1, set("rot", k, [0, 0, 0]), done)));
      ["x", "y", "z"].forEach((ax, k) => card.append(slider(`move ${ax}`, move[k], -1, 1, 0.005, set("move", k, [0, 0, 0]), done)));
    } else {
      const tg = pb.target || b.target;
      if (Array.isArray(tg)) {
        ["x", "y", "z"].forEach((ax, k) => card.append(slider(`reach ${ax}`, tg[k], -1.5, 2.5, 0.005, set("target", k, tg), done)));
      } else {
        card.append(el("p", { class: "hint" }, `holds a point on “${tg.bone}”. Drag the handle to move the grip point.`));
        ["x", "y", "z"].forEach((ax, k) => card.append(slider(`grip ${ax}`, tg.point[k], -1.5, 2.5, 0.005, v => {
          const q = pose[b.name] || (pose[b.name] = {});
          if (!q.target) q.target = clone(tg);
          q.target.point[k] = v; live();
        }, done)));
      }
      const pole = pb.pole || b.pole;
      ["x", "y", "z"].forEach((ax, k) => card.append(slider(`bend ${ax}`, pole[k], -1, 1, 0.05, set("pole", k, b.pole), done)));
      if (b.end) {
        const er = pb.end_rot || [0, 0, 0];
        ["x", "y", "z"].forEach((ax, k) => card.append(slider(`${b.end} ${ax}`, er[k], -90, 90, 1, set("end_rot", k, [0, 0, 0]), done)));
      }
    }
    box.append(card);
  }
}

// ------------------------------------------------------------------ materials panel
const toHex = c => "#" + c.map(v => Math.round(Math.max(0, Math.min(1, v)) * 255).toString(16).padStart(2, "0")).join("");
const fromHex = h => [1, 3, 5].map(i => Math.round(parseInt(h.slice(i, i + 2), 16) / 255 * 1000) / 1000);
function renderMaterials() {
  const box = $("#matList");
  box.innerHTML = "";
  const used = {};
  S.model.parts.forEach(p => used[p.mat] = (used[p.mat] || 0) + 1);
  for (const [name, m] of Object.entries(S.model.materials)) {
    const col = el("input", { type: "color", value: toHex(m.color) });
    col.addEventListener("focus", beginEdit);
    col.addEventListener("input", () => { beginEdit(); m.color = fromHex(col.value); matCache.clear(); rebuild3d(); });
    col.addEventListener("change", () => commit("color"));
    const kind = el("select", { title: "flat = exactly this colour, no light (sprites converted to 3D)" }, ["paint", "chrome", "glow", "flat"].map(k => el("option", { selected: k === m.kind }, k)));
    kind.addEventListener("change", () => { beginEdit(); m.kind = kind.value; matCache.clear(); commit("kind"); });
    const del = el("button", { title: used[name] ? "in use" : "delete", disabled: !!used[name], onclick: () => { beginEdit(); delete S.model.materials[name]; commit("delete color"); } }, "×");
    const row = el("div", { class: "mat" }, col, el("span", {}, name, el("small", { style: "color:#9a9ca5" }, `  ${used[name] || 0} parts`)), kind, del);
    if (m.kind === "paint" && (S.model.render || {}).style !== "cel") {
      const ex = el("div", { class: "extra" });
      for (const [k, label, def, step] of [["refl", "shine", 0.4, 0.02], ["spec", "highlight", 0.45, 0.05], ["gloss", "gloss", 30, 1]]) {
        const n = el("input", { type: "number", step, value: m[k] ?? def });
        n.addEventListener("change", () => { beginEdit(); m[k] = parseFloat(n.value); commit("mat"); });
        ex.append(label, n);
      }
      row.append(ex);
    }
    box.append(row);
  }
}

// ------------------------------------------------------------------ canvas panel
function renderCanvas() {
  const box = $("#canvasForm");
  box.innerHTML = "";
  const r = S.model.render || (S.model.render = {});
  // the shadow ellipse moves and scales with the figure when the size, centre or feet row change
  let start = null;
  const follow = (key, x, done) => {
    if (!["scale", "px_per_m", "cx", "y0"].includes(key) || !Array.isArray(r.shadow)) return;
    start ||= { sh: r.shadow.slice(), v: r[key], cx: r.cx, y0: r.y0 };
    const { sh, v, cx, y0 } = start, k = key === "scale" || key === "px_per_m" ? (v > 0 ? x / v : 1) : 1;
    const dx = key === "cx" ? x - v : 0, dy = key === "y0" ? x - v : 0;
    const [w, h] = r.res || [64, 64];
    const n = sh.map((s, i) => Math.max(0, Math.min((i % 2 ? h : w) - 1, Math.round(i % 2 ? y0 + dy + (s - y0) * k : cx + dx + (s - cx) * k))));
    if (n[3] - n[1] < 1) n[3] = n[1] + 1;
    r.shadow = n;
    if (done) start = null;
  };
  const opt = (label, key, def, step, help) => {
    if (r[key] === undefined) r[key] = def;
    const f = Array.isArray(r[key]) ? field(label, r[key].map((v, k) => numInput(v, (x, done) => { r[key][k] = x; if (done) commit("canvas"); }, step)))
      : field(label, numInput(r[key], (x, done) => { follow(key, x, done); r[key] = x; if (done) commit("canvas"); if (key === "yaw" || key === "pitch") { if (camera === ortho) useSpriteCam(true); } }, step));
    if (help) f.title = help;
    return f;
  };
  const style = el("select", {}, ["studio", "cel", "wire"].map(s => el("option", { selected: (r.style || "studio") === s }, s)));
  style.addEventListener("change", () => { beginEdit(); r.style = style.value; matCache.clear(); commit("style"); });
  const file = el("input", { type: "text", value: r.file || S.name });
  file.addEventListener("change", () => { beginEdit(); r.file = file.value.toLowerCase().replace(/[^a-z0-9_-]/g, ""); commit("file"); });
  box.append(el("h4", {}, "Look"), field("style", style),
    el("p", { class: "hint" }, "studio = shiny metal (killbot) · cel = painted tones (nation units) · wire = pixel-art wireframe"),
    r.style === "wire" ? wireOptions(r) : "",
    el("div", { class: "group" }, el("h4", {}, "Size and framing"),
      opt("size ×", "scale", 1, 0.02, "multiplies how big the model is in the sprite"),
      opt("px / metre", "px_per_m", 18.085, 0.1),
      canvasSizeField(r.res || [64, 64], [["pad", "keep the model's size (more or less room)"], ["scale", "grow or shrink the model with it"]], resizeModelCanvas),
      opt("centre x", "cx", 32, 0.5, "pixel column of the model origin"),
      opt("feet row", "y0", 61.6, 0.1, "pixel row of the ground"),
      opt("shadow", "shadow", [20, 60, 46, 63], 1, "magenta ellipse: left, top, right, bottom")),
    el("div", { class: "group" }, el("h4", {}, "Camera and light"),
      opt("yaw °", "yaw", -30, 1, "-30 = facing left, three-quarter view"),
      opt("pitch °", "pitch", 9, 1),
      opt("light dir", "light", [-0.55, 0.75, 0.55], 0.05),
      opt("outline rgb", "outline", [20, 18, 24], 1),
      opt("gamma", "gamma", 0.85, 0.01),
      opt("quality", "ss", 5, 1, "supersampling: 2 fast draft, 5 final")),
    el("div", { class: "group" }, el("h4", {}, "Output"), field("file name", file),
      el("p", { class: "hint" }, "Frames are written as <file>1.tga (idle) and <file>2.tga (attack)."),
      ...Object.entries(S.model.frames).map(([k, f]) => {
        const lab = el("input", { type: "text", value: f.label || k });
        lab.addEventListener("change", () => { beginEdit(); f.label = lab.value; commit("label"); });
        const halo = el("input", { type: "checkbox", checked: !!f.halo });
        halo.addEventListener("change", () => { beginEdit(); f.halo = halo.checked; commit("halo"); });
        return field(`frame ${k}`, lab, el("label", { class: "chk", title: "soft glow ring around lights (cel style)" }, halo, "halo"));
      })));
}

function wireOptions(r) {
  const pick = (label, key, opts, def, help) => {
    const s = el("select", {}, opts.map(([v, t]) => el("option", { value: v, selected: (r[key] ?? def) === v }, t)));
    s.addEventListener("change", () => { beginEdit(); r[key] = s.value; commit("wire"); });
    const f = field(label, s); if (help) f.title = help; return f;
  };
  const hex = c => "#" + c.map(v => Math.round(v).toString(16).padStart(2, "0")).join("");
  const unhex = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
  // line colour: each part's own colour, or one colour for everything
  const one = Array.isArray(r.wire_color);
  const lineMode = el("select", {}, [["material", "part colours"], ["one", "one colour"]].map(([v, t]) =>
    el("option", { value: v, selected: (one ? "one" : "material") === v }, t)));
  const lineCol = el("input", { type: "color", value: hex(one ? r.wire_color : [90, 230, 255]) });
  lineMode.addEventListener("change", () => { beginEdit(); r.wire_color = lineMode.value === "one" ? unhex(lineCol.value) : "material"; commit("wire"); });
  lineCol.addEventListener("change", () => { beginEdit(); r.wire_color = unhex(lineCol.value); commit("wire"); });
  const hasFill = Array.isArray(r.fill);
  const fillMode = el("select", {}, [["none", "none (hollow)"], ["material", "part colours"], ["one", "one colour"]].map(([v, t]) =>
    el("option", { value: v, selected: (r.fill === "material" ? "material" : hasFill ? "one" : "none") === v }, t)));
  const fillCol = el("input", { type: "color", value: hex(hasFill ? r.fill : [18, 30, 44]) });
  fillMode.addEventListener("change", () => {
    beginEdit(); r.fill = { none: null, material: "material", one: unhex(fillCol.value) }[fillMode.value]; commit("wire");
  });
  fillCol.addEventListener("change", () => { beginEdit(); r.fill = unhex(fillCol.value); fillMode.value = "one"; commit("wire"); });
  const dim = el("input", { type: "number", min: 0.1, max: 1, step: 0.05, value: r.hidden_dim ?? 0.42 });
  dim.addEventListener("change", () => { beginEdit(); r.hidden_dim = parseFloat(dim.value); commit("wire"); });
  return el("div", { class: "group" }, el("h4", {}, "Wireframe"),
    field("lines", el("div", { class: "vec" }, lineMode, lineCol)),
    pick("outline", "wire_by", [["group", "each piece"], ["bone", "each bone"], ["part", "every part"]], "group",
      "piece = parts that are cut/merged together; every part = most lines"),
    pick("hidden", "hidden", [["dim", "dimmed"], ["show", "shown"], ["hide", "left out"]], "dim",
      "lines of parts behind other parts"),
    field("dim to", dim),
    field("fill", el("div", { class: "vec" }, fillMode, fillCol)),
    el("p", { class: "hint" }, "Fill: part colours paints what is in front in its own colours (only hidden lines show over it); one colour paints the body behind the lines, e.g. dark blue with cyan lines for a hologram."));
}

// canvas size: Dominions takes square sprites of these sizes
const SIZES = [8, 16, 32, 64, 128];
function canvasSizeField(res, modes, onApply) {
  const [w, h] = res;
  const ok = w === h && SIZES.includes(w);
  const size = el("select", {}, ok ? null : el("option", { value: "", selected: true, disabled: true }, `${w} × ${h} (not a Dominions size)`),
    SIZES.map(n => el("option", { value: n, selected: ok && n === w }, `${n} × ${n}`)));
  const how = el("select", {}, modes.map(([v, t]) => el("option", { value: v }, t)));
  const apply = el("button", { onclick: () => { const n = +size.value; if (n && (n !== w || n !== h)) onApply(n, how.value); } }, "Apply");
  return el("div", {}, field("canvas", size, apply), field("resizing", how),
    el("p", { class: "hint" }, "Dominions takes square sprites of 8, 16, 32, 64 or 128 px: humans 64, size 4+ monsters 128."));
}
function resizeModelCanvas(n, how) {
  beginEdit();
  const r = S.model.render, [w, h] = r.res || [64, 64];
  const k = how === "scale" ? n / w : 1;
  const cx = r.cx ?? w / 2, y0 = r.y0 ?? h - 2.4;
  const ncx = how === "scale" ? cx * n / w : cx + (n - w) / 2, ny0 = n - (h - y0);
  const sh = r.shadow === undefined ? [20, 60, 46, 63] : r.shadow;
  if (sh) r.shadow = sh.map((v, i) => Math.max(0, Math.min(n - 1, Math.round(i % 2 ? ny0 + (v - y0) * k : ncx + (v - cx) * k))));
  if (how === "scale") r.px_per_m = (r.px_per_m ?? 34 / 1.88) * k;
  r.cx = Math.round(ncx * 10) / 10; r.y0 = Math.round(ny0 * 10) / 10; r.res = [n, n];
  commit("canvas size");
}

// ------------------------------------------------------------------ sprites
let renderTimer = null;
function scheduleRender() {
  if (!$("#autoRender").checked) return;
  clearTimeout(renderTimer);
  if (Cut.isCut(S.model)) renderTimer = setTimeout(() => Object.keys(S.model.frames).forEach(k => renderSprite(k)), 600);
  else renderTimer = setTimeout(renderStale, 500);
}
// what a frame's sprite depends on: a pose edit in one frame leaves the other frame current
const spriteKey = k => JSON.stringify([S.name, S.model.materials, S.model.bones, S.model.parts, S.model.render, S.model.frames[k]]);
const isStale = k => !S.sprites[k] || (!Cut.isCut(S.model) && S.sprites[k].key !== spriteKey(k));
// the frame on screen first, then any other frame an edit (canvas, shadow, parts...) has made out of date
async function renderStale() {
  const run = ++S.staleRun;
  for (const k of [S.frame, ...Object.keys(S.model.frames).filter(k => k !== S.frame)]) {
    if (run !== S.staleRun) return;
    if (k === S.frame || isStale(k)) await renderSprite(k);
  }
}
async function renderSprite(frame, ss) {
  const seq = S.renderSeq[frame] = (S.renderSeq[frame] || 0) + 1;
  const st = $("#renderStatus");
  st.className = "status"; st.textContent = `rendering frame ${frame}…`;
  if (Cut.isCut(S.model)) {                // 2D projects are drawn in the page; the server only writes the files
    try {
      const j = await Cut.writeSprite(frame);
      st.textContent = `frame ${frame} → ${j.tga}`;
      drawSprites();
    } catch (e) { st.className = "status bad"; st.textContent = "Saving the sprite failed: " + e.message; }
    return;
  }
  const model = clone(S.model); model.name = S.name;
  const key = spriteKey(frame);
  try {
    const res = await fetch("/api/render", { method: "POST", body: JSON.stringify({ model, frame, ss }) });
    const j = await res.json();
    if (j.error) throw new Error(j.error);
    if (j.skipped) return;                       // a newer render of this frame replaced it
    if (seq !== S.renderSeq[frame]) return;
    S.sprites[frame] = { url: j.png, tga: j.tga, seconds: j.seconds, key, img: await loadImage(j.png) };
    st.textContent = `frame ${frame}: ${j.seconds}s → ${j.tga}`;
    drawSprites();
  } catch (e) {
    st.className = "status bad"; st.textContent = "Render failed: " + e.message;
  }
}
async function renderPreview(frame, ss, tag, edit) {
  const model = clone(S.model); model.name = S.name;
  if (edit) edit(model.render || (model.render = {}));
  const j = await api("/api/render", { model, frame, ss, tag });
  return loadImage(j.png + "&r=" + Date.now());
}
const loadImage = url => new Promise((ok, bad) => { const i = new Image(); i.onload = () => ok(i); i.onerror = bad; i.src = url; });
function spriteCanvas(img, zoom) {
  const c = document.createElement("canvas");
  c.width = img.width; c.height = img.height;
  const g = c.getContext("2d");
  g.drawImage(img, 0, 0);
  const d = g.getImageData(0, 0, c.width, c.height), px = d.data;
  for (let i = 0; i < px.length; i += 4) {
    const r = px[i], gg = px[i + 1], b = px[i + 2];
    const x = (i / 4) % c.width, y = Math.floor(i / 4 / c.width);
    const isBlack = r === 0 && gg === 0 && b === 0, isMag = r === 255 && gg === 0 && b === 255;
    if (S.bg === "raw") continue;
    let bg;
    if (S.bg === "checker") bg = ((x >> 2) + (y >> 2)) % 2 ? [92, 92, 100] : [70, 70, 78];
    else bg = [86, 104, 58];
    if (isBlack) { px[i] = bg[0]; px[i + 1] = bg[1]; px[i + 2] = bg[2]; }
    else if (isMag) { px[i] = bg[0] * 0.55; px[i + 1] = bg[1] * 0.55; px[i + 2] = bg[2] * 0.55; }
  }
  g.putImageData(d, 0, 0);
  c.style.width = img.width * zoom + "px";
  c.style.height = img.height * zoom + "px";
  return c;
}
function drawSprites() {
  const big = $("#spriteBig");
  const cur = S.sprites[S.spriteFrame] || S.sprites[S.frame];
  const holder = big.parentElement;
  if (cur) {
    const c = spriteCanvas(cur.img, S.zoom);
    c.id = "spriteBig";
    holder.replaceChild(c, $("#spriteBig"));
    $("#spriteCap").textContent = `frame ${S.spriteFrame} · ${cur.img.width}×${cur.img.height} · ${cur.tga}`;
  }
  const row = $("#spriteRow");
  row.innerHTML = "";
  for (const k of Object.keys(S.model.frames)) {
    const s = S.sprites[k];
    const cell = el("div", { class: "cell" + (k === S.spriteFrame ? " on" : ""), onclick: () => { S.spriteFrame = k; drawSprites(); } });
    if (s) cell.append(spriteCanvas(s.img, 2)); else cell.append(el("div", { class: "hint" }, "—"));
    cell.append(el("div", { class: "cap" }, `${k} ${S.model.frames[k].label || ""} (1× shown 2×)`));
    row.append(cell);
  }
}

// ------------------------------------------------------------------ frames, tabs, views
function renderFrameTabs() {
  const box = $("#frameTabs");
  box.innerHTML = "";
  for (const [k, f] of Object.entries(S.model.frames)) {
    box.append(el("button", { class: k === S.frame ? "on" : "", onclick: () => { S.frame = k; S.spriteFrame = k; refreshAll(); drawSprites(); if (isStale(k)) scheduleRender(); } }, `${k} ${f.label || ""}`));
  }
}
function setTab(t) {
  S.tab = t;
  $$("#leftTabs button").forEach(b => b.classList.toggle("on", b.dataset.tab === t));
  $$("aside#left section").forEach(s => s.hidden = s.dataset.panel !== t);
  if (t === "pose" && !Cut.isCut(S.model)) renderPose();
  attachGizmo();
}
function refreshAll() {
  if (!S.model) return;
  const cut = Cut.isCut(S.model);
  document.body.classList.toggle("mode2d", cut);
  $("#dirty").hidden = !S.dirty;
  $("#btnUndo").disabled = !S.undo.length;
  $("#btnRedo").disabled = !S.redo.length;
  if (cut) { Cut.refresh(); renderFrameTabs(); drawSprites(); return; }
  if (S.sel >= S.model.parts.length) S.sel = -1;
  matCache.clear();
  rebuild3d();
  renderTree();
  renderInspector();
  renderPose();
  renderMaterials();
  renderCanvas();
  renderFrameTabs();
  drawSprites();
  syncRotateBar();
}
function toast(msg) { const t = $("#toast"); t.textContent = msg; t.hidden = false; clearTimeout(t._t); t._t = setTimeout(() => t.hidden = true, 2600); }

// ------------------------------------------------------------------ load / save / export
async function api(path, body) {
  const res = await fetch(path, body ? { method: "POST", body: JSON.stringify(body) } : undefined);
  const j = await res.json();
  if (j.error) throw new Error(j.error);
  return j;
}
async function loadModelList(select) {
  const { models, mods } = await api("/api/models");
  S.mods = mods;
  const s = $("#modelSel");
  s.innerHTML = "";
  for (const m of models) s.append(el("option", { value: m, selected: m === select }, m));
  return models;
}
async function openModel(name) {
  if (S.dirty && !confirm("Discard unsaved changes?")) { $("#modelSel").value = S.name; return; }
  S.model = await api("/api/model?name=" + encodeURIComponent(name));
  if (Cut.isCut(S.model)) await Cut.prepare(S.model);
  S.name = name; S.undo = []; S.redo = []; S.dirty = false; S.sel = -1; S.sprites = {};
  S.frame = Object.keys(S.model.frames)[0]; S.spriteFrame = S.frame;
  if (!Cut.isCut(S.model)) frameCamera();
  refreshAll();
  for (const k of Object.keys(S.model.frames)) await renderSprite(k);
}
// aim the free camera at the model and back off for big ones (a human needs no change)
function frameCamera() {
  const pts = [];
  for (const p of S.model.parts || []) for (const k of ["c", "a", "b"]) if (p[k]) pts.push(p[k]);
  if (!pts.length) return;
  const lo = [0, 1, 2].map(i => Math.min(...pts.map(q => q[i]))), hi = [0, 1, 2].map(i => Math.max(...pts.map(q => q[i])));
  const c = lo.map((v, i) => (v + hi[i]) / 2), size = Math.max(hi[0] - lo[0], hi[1] - lo[1]);
  const k = size > 1.9 ? size / 1.8 * 1.6 : 1;
  orbit.target.set(c[0], Math.max(c[1], 0.95), c[2]);
  if (k === 1) orbit.target.set(0, 0.95, 0);
  persp.position.set(orbit.target.x + 1.75 * k, orbit.target.y + 0.65 * k, orbit.target.z + 3.0 * k);
  orbit.update();
}
async function save(asName) {
  const name = asName || S.name;
  await api("/api/model?name=" + encodeURIComponent(name), S.model);
  S.name = name; S.dirty = false;
  await loadModelList(name);
  refreshAll();
  toast(`Saved models/${name}.json`);
}
async function exportSprites() {
  const r = S.model.render || {};
  const file = r.file || S.name;
  const dir = prompt(`Copy the rendered TGAs into which folder? (a path inside ${S.mods || "the folder above Sprite Studio"}, e.g. your mod's folder)`, r.export_dir || S.name);
  if (!dir) return;
  for (const k of Object.keys(S.model.frames)) await renderSprite(k);
  const files = Object.keys(S.model.frames).map(k => `${file}${k}.tga`);
  const j = await api("/api/export", { name: S.name, dir, files });
  if (r.export_dir !== dir) { beginEdit(); r.export_dir = dir; commit("export dir"); }
  toast("Exported " + j.copied.join(", "));
}

// ------------------------------------------------------------------ wiring
$("#modelSel").addEventListener("change", e => openModel(e.target.value));
$("#btnSave").onclick = () => save();
$("#btnSaveAs").onclick = () => {
  const n = prompt("Save as (lowercase letters, digits, - and _):", S.name + "_copy");
  if (n) save(n.toLowerCase());
};
$("#btnUndo").onclick = undo;
$("#btnRedo").onclick = redo;
$("#btnRender").onclick = () => renderSprite(S.frame);
$("#btnExport").onclick = () => exportSprites().catch(e => alert(e.message));
$$("#viewSeg button").forEach(b => b.onclick = () => {
  $$("#viewSeg button").forEach(x => x.classList.toggle("on", x === b));
  $("#views").className = { "3d": "v3d", both: "both", sprite: "vsprite" }[b.dataset.view];
});
$$("#leftTabs button").forEach(b => b.onclick = () => setTab(b.dataset.tab));
$$("#bgSeg button").forEach(b => b.onclick = () => { S.bg = b.dataset.bg; $$("#bgSeg button").forEach(x => x.classList.toggle("on", x === b)); drawSprites(); });
$$("#zoomSeg button").forEach(b => b.onclick = () => { S.zoom = +b.dataset.z; $$("#zoomSeg button").forEach(x => x.classList.toggle("on", x === b)); drawSprites(); });
$$("#gizmoSeg button").forEach(b => b.onclick = () => { gizmo.setMode(b.dataset.g); $$("#gizmoSeg button").forEach(x => x.classList.toggle("on", x === b)); attachGizmo(); });
$("#btnSpriteCam").onclick = () => useSpriteCam(true);
$("#btnFreeCam").onclick = () => useSpriteCam(false);
$("#showCuts").onchange = () => rebuild3d();
$("#showBones").onchange = () => rebuild3d();
$("#wire3d").onchange = () => { matCache.clear(); rebuild3d(); };

// ------------------------------------------------------------------ rotate the sprite
// Turning = camera yaw (-30 is the standard Dominions three-quarter view facing left),
// tilt = camera pitch. Both are saved with the model and used for every frame.
const wrapYaw = a => ((a + 180) % 360 + 360) % 360 - 180;
function syncRotateBar() {
  const r = S.model.render || {};
  const yaw = r.yaw ?? -30, pitch = r.pitch ?? 9;
  $("#yawSlider").value = yaw; $("#pitchSlider").value = pitch;
  const left = yaw < 0 && yaw > -180;
  $("#angleLbl").innerHTML = "";
  $("#angleLbl").append(`turn ${Math.round(yaw)}° · tilt ${Math.round(pitch)}° `,
    el("span", { style: `color:var(${left ? "--ok" : "--bad"})`, title: left ? "" : "Dominions units must face left; the game uses the facing as the move direction" },
      left ? "faces left" : "faces right/front ⚠"));
}
function setAngle(key, v, done) {
  beginEdit();
  const r = S.model.render || (S.model.render = {});
  r[key] = key === "yaw" ? wrapYaw(v) : Math.max(-10, Math.min(60, v));
  syncRotateBar();
  if (camera === ortho) useSpriteCam(true);
  if (done) { commit("rotate"); if (!$("#turntable").hidden) markTurntable(); }
}
$("#yawSlider").oninput = e => setAngle("yaw", +e.target.value, false);
$("#yawSlider").onchange = e => setAngle("yaw", +e.target.value, true);
$("#pitchSlider").oninput = e => setAngle("pitch", +e.target.value, false);
$("#pitchSlider").onchange = e => setAngle("pitch", +e.target.value, true);
$$("#rotateBar [data-turn]").forEach(b => b.onclick = () => setAngle("yaw", ((S.model.render || {}).yaw ?? -30) + +b.dataset.turn, true));
$("#btnFacing").onclick = () => setAngle("yaw", -30, true);
const TURNTABLE = [-150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180];
function markTurntable() {
  const yaw = (S.model.render || {}).yaw ?? -30;
  $$("#turntable .cell").forEach(c => c.classList.toggle("on", +c.dataset.yaw === wrapYaw(yaw)));
}
async function turntable() {
  const box = $("#turntable");
  if (!box.hidden && box.dataset.busy !== "1") { box.hidden = true; $("#btnTurntable").classList.remove("on"); return; }
  box.hidden = false; box.dataset.busy = "1"; box.innerHTML = "";
  $("#btnTurntable").classList.add("on");
  const frame = S.spriteFrame;
  for (const yaw of TURNTABLE) {
    const cell = el("div", { class: "cell", "data-yaw": yaw, title: `Use turn ${yaw}°`, onclick: () => setAngle("yaw", yaw, true) },
      el("div", { class: "cap" }, "…"), el("div", { class: "cap" }, `${yaw}°`));
    box.append(cell);
    try {
      const img = await renderPreview(frame, 2, "yaw" + yaw, r => { r.yaw = yaw; });
      cell.replaceChild(spriteCanvas(img, 2), cell.firstChild);
    } catch (e) { cell.firstChild.textContent = "failed"; }
  }
  box.dataset.busy = "0";
  markTurntable();
}
$("#btnTurntable").onclick = () => turntable();
$("#partFilter").oninput = () => renderTree();
for (const t of Object.keys(DEFAULTS)) $("#addType").append(el("option", {}, t));
$("#btnAdd").onclick = () => {
  beginEdit();
  const t = $("#addType").value;
  const ref = S.model.parts[S.sel];
  const c = ref ? add(partCenter(ref), [0.06, 0, 0.06]) : [0, 1.0, 0.25];
  const bone = ref ? ref.bone : (boneNames()[0] || "body");
  const mat = ref ? ref.mat : Object.keys(S.model.materials)[0];
  S.model.parts.push({ type: t, ...DEFAULTS[t](c.map(r3)), mat, bone, name: `new ${t}` });
  S.sel = S.model.parts.length - 1;
  commit("add");
};
$("#btnDup").onclick = () => {
  if (S.sel < 0) return;
  beginEdit();
  const q = movePart(S.model.parts[S.sel], [0.03, 0, 0.03]);
  q.name = (q.name || q.type) + " copy";
  S.model.parts.splice(S.sel + 1, 0, roundAll(q));
  S.sel += 1;
  commit("duplicate");
};
$("#btnMirror").onclick = () => {
  if (S.sel < 0) return;
  beginEdit();
  const q = mirrorPart(S.model.parts[S.sel]);
  if (!boneNames().includes(q.bone)) q.bone = S.model.parts[S.sel].bone;
  S.model.parts.splice(S.sel + 1, 0, roundAll(q));
  S.sel += 1;
  commit("mirror");
};
$("#btnDel").onclick = () => {
  if (S.sel < 0) return;
  beginEdit();
  S.model.parts.splice(S.sel, 1);
  S.sel = Math.min(S.sel, S.model.parts.length - 1);
  commit("delete");
};
// a new free bone: follows the selected part's bone and turns about that part's centre
$("#btnAddBone").onclick = () => {
  const n = $("#newBoneName").value.trim().replace(/\s+/g, "_").replace(/[^A-Za-z0-9_.-]/g, "");
  const taken = new Set([...boneNames(), ...S.model.bones.map(b => b.name)]);
  if (!n) { $("#newBoneName").focus(); return; }
  if (taken.has(n)) { alert(`There is already a bone called “${n}”.`); return; }
  beginEdit();
  const ref = S.model.parts[S.sel];
  const parent = ref ? ref.bone : (boneNames()[0] || null);
  const pp = S.model.bones.find(b => b.name === parent && b.type === "free");
  const pivot = ref ? partCenter(ref) : (pp && pp.pivot) || [0, 1, 0];
  S.model.bones.push({ name: n, type: "free", parent, pivot: pivot.map(r3) });
  $("#newBoneName").value = "";
  commit("add bone");
};
$("#newBoneName").onkeydown = e => { if (e.key === "Enter") $("#btnAddBone").click(); };
$("#btnAddMat").onclick = () => {
  const n = $("#newMatName").value.trim().toLowerCase().replace(/[^a-z0-9_]/g, "_");
  if (!n || S.model.materials[n]) return;
  beginEdit();
  S.model.materials[n] = { kind: "paint", color: [0.6, 0.6, 0.62], refl: 0.3 };
  $("#newMatName").value = "";
  commit("add color");
};
$("#btnCopyPose").onclick = () => {
  const keys = Object.keys(S.model.frames).filter(k => k !== S.frame);
  const from = keys.length === 1 ? keys[0] : prompt("Copy the pose from which frame? " + keys.join(", "), keys[0]);
  if (!from || !S.model.frames[from]) return;
  beginEdit();
  S.model.frames[S.frame].pose = clone(S.model.frames[from].pose || {});
  commit("copy pose");
};
$("#btnResetPose").onclick = () => { beginEdit(); S.model.frames[S.frame].pose = {}; commit("reset pose"); };
window.addEventListener("keydown", e => {
  if (e.target.matches("input, select, textarea")) return;
  const k = e.key.toLowerCase();
  if ((e.ctrlKey || e.metaKey) && k === "z") { e.preventDefault(); e.shiftKey ? redo() : undo(); }
  else if ((e.ctrlKey || e.metaKey) && k === "y") { e.preventDefault(); redo(); }
  else if ((e.ctrlKey || e.metaKey) && k === "s") { e.preventDefault(); save(); }
  else if (Cut.isCut(S.model)) { if (Cut.key(e)) e.preventDefault(); }
  else if ((e.ctrlKey || e.metaKey) && k === "d") { e.preventDefault(); $("#btnDup").click(); }
  else if (k === "delete") $("#btnDel").click();
  else if (k === "escape") { S.poseHandle = null; select(-1); }
  else if (k === "m") $$("#gizmoSeg button")[0].click();
  else if (k === "r") $$("#gizmoSeg button")[1].click();
});
window.addEventListener("beforeunload", e => { if (S.dirty) { e.preventDefault(); e.returnValue = ""; } });
// the built app quits a few minutes after its last page is gone; tell it we are still here
setInterval(() => fetch("/api/ping").catch(() => {}), 30000);
$("#btnQuit").onclick = async () => {
  if (S.dirty && !confirm("You have unsaved changes. Quit anyway?")) return;
  S.dirty = false;
  await fetch("/api/quit", { method: "POST", body: "{}" }).catch(() => {});
  document.body.innerHTML = '<p style="margin:40px;grid-column:1/-1">Sprite Studio has closed. You can close this tab.</p>';
};

// ------------------------------------------------------------------ new projects and import
const cleanName = s => s.toLowerCase().replace(/\.[a-z0-9]+$/, "").replace(/[^a-z0-9_-]+/g, "_").replace(/^_+|_+$/g, "").slice(0, 64);
async function uniqueName(base) {
  const { models } = await api("/api/models");
  let n = cleanName(base) || "untitled", k = 2;
  const stem = n;
  while (models.includes(n)) n = `${stem}_${k++}`;
  return n;
}
async function decodeFile(file) {
  const buf = new Uint8Array(await file.arrayBuffer());
  let bin = "";
  for (let i = 0; i < buf.length; i += 0x8000) bin += String.fromCharCode(...buf.subarray(i, i + 0x8000));
  try { return await api("/api/decode", { data: btoa(bin) }); }
  catch (e) { throw new Error(`${file.name}: ${e.message}`); }
}
// sprite files -> 2D project; "<name>1.tga" is the idle frame and "<name>2.tga" the attack
async function spriteProject(name, files, ground = true) {
  const imgs = await Promise.all(files.map(decodeFile));
  return Cut.cutoutModel(name, imgs.map((im, i) => {
    const m = files[i].name.match(/(\d)\.[a-z0-9]+$/i);
    return { frame: m && ["1", "2"].includes(m[1]) ? m[1] : String(i + 1), url: im.png };
  }), { ground });
}
function humanoidModel(style, size) {
  const k = Math.min(1, size / 64);
  const mats = { skin: { kind: "paint", color: [0.86, 0.68, 0.55] }, cloth: { kind: "paint", color: [0.36, 0.42, 0.56] },
    dark: { kind: "paint", color: [0.24, 0.2, 0.18] }, hair: { kind: "paint", color: [0.32, 0.22, 0.14] } };
  const bones = [{ name: "body", type: "free", parent: null, pivot: [0, 0.95, 0] }, { name: "head", type: "free", parent: "body", pivot: [0, 1.5, 0] }];
  const parts = [
    { name: "pelvis", type: "ellipsoid", c: [0, 0.95, 0], r: [0.16, 0.11, 0.11], mat: "cloth", bone: "body" },
    { name: "torso", type: "ellipsoid", c: [0, 1.25, 0], r: [0.19, 0.25, 0.12], mat: "cloth", bone: "body" },
    { name: "neck", type: "capsule", a: [0, 1.44, 0], b: [0, 1.54, 0.005], r: 0.045, mat: "skin", bone: "head" },
    { name: "head", type: "ellipsoid", c: [0, 1.65, 0.01], r: [0.085, 0.11, 0.1], mat: "skin", bone: "head" },
    { name: "hair", type: "ellipsoid", c: [0, 1.7, -0.012], r: [0.09, 0.08, 0.095], mat: "hair", bone: "head" },
  ];
  for (const [side, sx] of [["L", 1], ["R", -1]]) {
    const leg = { name: `leg.${side}`, type: "ik", parent: "body", root: [0.09 * sx, 0.93, 0], target: [0.11 * sx, 0.09, 0.02], pole: [0, 0, 1],
      l1: 0.44, l2: 0.43, bones: [`thigh.${side}`, `shin.${side}`], end: `foot.${side}` };
    const arm = { name: `arm.${side}`, type: "ik", parent: "body", root: [0.2 * sx, 1.43, 0], target: [0.25 * sx, 0.9, 0.06], pole: [0.3 * sx, 0, -1],
      l1: 0.3, l2: 0.27, bones: [`upperarm.${side}`, `forearm.${side}`] };
    bones.push(leg, arm);
    const [knee, ankle] = ik(leg.root, leg.target, leg.l1, leg.l2, leg.pole).map(v => v.map(r3));
    const [elbow, wrist] = ik(arm.root, arm.target, arm.l1, arm.l2, arm.pole).map(v => v.map(r3));
    parts.push(
      { name: `thigh ${side}`, type: "capsule", a: leg.root, b: knee, r: 0.07, mat: "cloth", bone: `thigh.${side}` },
      { name: `shin ${side}`, type: "capsule", a: knee, b: ankle, r: 0.055, mat: "cloth", bone: `shin.${side}` },
      { name: `boot ${side}`, type: "box", c: add(ankle, [0, -0.035, 0.04]).map(r3), half: [0.045, 0.035, 0.09], rnd: 0.012, mat: "dark", bone: `foot.${side}` },
      { name: `upper arm ${side}`, type: "capsule", a: arm.root, b: elbow, r: 0.05, mat: "cloth", bone: `upperarm.${side}` },
      { name: `forearm ${side}`, type: "capsule", a: elbow, b: wrist, r: 0.042, mat: "skin", bone: `forearm.${side}` },
      { name: `hand ${side}`, type: "sphere", c: add(wrist, mul(norm(sub(wrist, elbow)), 0.03)).map(r3), r: 0.04, mat: "skin", bone: `forearm.${side}` });
  }
  return { materials: mats, bones, parts, frames: { 1: { label: "Idle", pose: {} }, 2: { label: "Attack", pose: {} } },
    render: { style, res: [size, size], px_per_m: Math.round(34 / 1.88 * k * 1000) / 1000, cx: size / 2, y0: size - 2.4,
      shadow: [size / 2 - 13 * k, size - 4, size / 2 + 13 * k, size - 1].map(Math.round) } };
}
function emptyModel(style, size) {
  const m = humanoidModel(style, size);
  m.materials = { paint: { kind: "paint", color: [0.62, 0.64, 0.68] } };
  m.bones = [{ name: "body", type: "free", parent: null, pivot: [0, 0.6, 0] }];
  m.parts = [{ name: "block", type: "box", c: [0, 0.6, 0], half: [0.15, 0.3, 0.1], rnd: 0.02, mat: "paint", bone: "body" }];
  return m;
}
async function saveAndOpen(name, model) {
  model.name = name;
  if (!model.render.file || model.render.file === S.name) model.render.file = name;
  await api("/api/model?name=" + encodeURIComponent(name), model);
  S.dirty = false;
  await loadModelList(name);
  await openModel(name);
  toast(`Created ${name}`);
}
function syncNewDialog() {
  const kind = $("#newForm").kind.value;
  $("#newStyleRow").hidden = $("#newSizeRow").hidden = !["humanoid", "empty"].includes(kind);
  $("#newFileRow").hidden = $("#newGroundRow").hidden = kind !== "sprite";
  $("#newHint").textContent = kind === "sprite" ? "Pick one sprite, or its idle and attack files together (name1.tga + name2.tga)." : "";
}
$("#btnNew").onclick = () => {
  if (S.dirty && !confirm("You have unsaved changes. Start a new project anyway?")) return;
  $("#newName").value = ""; $("#newFile").value = "";
  syncNewDialog();
  $("#newDlg").showModal();
};
$("#newKind").addEventListener("change", syncNewDialog);
$("#newDlg").addEventListener("close", async () => {
  if ($("#newDlg").returnValue !== "ok") return;
  const kind = $("#newForm").kind.value, files = [...$("#newFile").files];
  try {
    const name = await uniqueName($("#newName").value || (files[0] && files[0].name.replace(/[12]?\.[a-z0-9]+$/i, "")) || "new");
    const style = $("#newStyle").value, size = +$("#newSize").value;
    let model;
    if (kind === "humanoid") model = humanoidModel(style, size);
    else if (kind === "empty") model = emptyModel(style, size);
    else if (kind === "copy") model = clone(S.model);
    else {
      if (!files.length) throw new Error("Pick the sprite file(s) to start from.");
      model = await spriteProject(name, files, $("#newGround").checked);
    }
    await saveAndOpen(name, model);
  } catch (e) { alert(e.message); }
});
$("#btnImport").onclick = () => {
  if (S.dirty && !confirm("You have unsaved changes. Import anyway?")) return;
  $("#importFile").click();
};
// Convert dialog: from a 2D project (layers or flat), or right after picking sprite files to import
let convFor = null;                         // { cut: 2D model, name } or { files }
function openConvert(what) {
  convFor = what;
  const imp = !!what.files;
  $("#convTitle").textContent = imp ? "Import sprite" : "Convert to 3D";
  $("#convFiles").textContent = imp ? what.files.map(f => f.name).join(" + ") : "Makes a new 3D project next to this one.";
  $("#convHow2d").hidden = !imp;
  $("#convHowLayers").hidden = imp;
  $("#convForm").how.value = imp ? "2d" : "layers";
  syncConvert();
  $("#convDlg").showModal();
}
function syncConvert() {
  const how = $("#convForm").how.value;
  $("#convOpts").hidden = how === "2d";
  $("#convGapRow").hidden = how !== "layers";
  $("#convOk").textContent = how === "2d" ? "Import" : "Create 3D model";
}
$("#convHow").addEventListener("change", syncConvert);
$("#convDlg").addEventListener("close", async () => {
  if ($("#convDlg").returnValue !== "ok" || !convFor) return;
  const how = $("#convForm").how.value, what = convFor;
  convFor = null;
  try {
    const base = what.files ? what.files[0].name.replace(/[12]?\.[a-z0-9]+$/i, "") : what.name;
    let cut = what.cut;
    if (what.files) cut = await spriteProject(cleanName(base) || "sprite", what.files, $("#convGround").checked);
    if (how === "2d") {
      const name = await uniqueName(base);
      cut.render.file = name;
      return await saveAndOpen(name, cut);
    }
    const look = $("#convLook").value;
    const model = toModel(cut, { look, flat: how === "flat", ground: $("#convGround").checked, spacing: Math.max(1, +$("#convGap").value || 3), thick: Math.max(1, +$("#convThick").value || 2) });
    const name = await uniqueName(base + "_3d");
    model.render.file = name;
    await saveAndOpen(name, model);
    if (look === "wire") { $("#wire3d").checked = true; matCache.clear(); rebuild3d(); }
    toast(`Created ${name}: ${model.parts.length} blocks. Turn it with the rotate bar.`);
  } catch (e) { alert(e.message); }
});
$("#importFile").addEventListener("change", async () => {
  const files = [...$("#importFile").files];
  $("#importFile").value = "";
  try {
    const imgs = files.filter(f => !/\.json$/i.test(f.name));
    if (imgs.length > 2) throw new Error("Import one sprite at a time (or its two frames).");
    if (imgs.length && imgs.length === files.length) return openConvert({ files: imgs });
    let last = null;
    for (const f of files.filter(f => /\.json$/i.test(f.name))) {
      const m = JSON.parse(await f.text());
      if (!m.frames || !(Cut.isCut(m) || (m.parts && m.bones))) throw new Error(`${f.name} is not a Sprite Studio model`);
      last = await uniqueName(f.name);
      m.name = last;
      await api("/api/model?name=" + encodeURIComponent(last), m);
    }
    if (last) { S.dirty = false; await loadModelList(last); await openModel(last); toast(`Imported as ${last}`); }
    if (imgs.length) openConvert({ files: imgs });           // models and a sprite picked together
  } catch (e) { alert(e.message); }
});
Cut.setup({ S, el, field, numInput, slider, beginEdit, commit, api, decodeFile, canvasSizeField, toast,
  convert: async () => {
    if (S.dirty) await save();             // the 2D project is kept; save it before switching to the 3D one
    openConvert({ cut: clone(S.model), name: S.name });
  },
  refresh: () => refreshAll(),
  liveSprite: () => { S.sprites[S.frame] = { ...(S.sprites[S.frame] || {}), img: Cut.spriteImage(S.frame) }; drawSprites(); } });

// ------------------------------------------------------------------ start
(async () => {
  loop();
  const params = new URLSearchParams(location.search);
  const models = await loadModelList();
  const first = params.get("model") || (models.includes("killbot") ? "killbot" : models[0]);
  if (first) { $("#modelSel").value = first; await openModel(first); }
  if (params.get("frame")) { S.frame = S.spriteFrame = params.get("frame"); refreshAll(); }
  if (Cut.isCut(S.model)) Cut.testHook(params);
  if (params.get("new")) $("#btnNew").click();
  if (params.get("convert") && Cut.isCut(S.model)) openConvert({ cut: clone(S.model), name: S.name });
  if (params.get("view")) $$(`#viewSeg button[data-view="${params.get("view")}"]`)[0]?.click();
  if (params.get("tab")) setTab(params.get("tab"));
  if (params.get("cam") === "sprite") useSpriteCam(true);
  if (params.get("sel")) select(+params.get("sel"), true);
  if (params.get("wire")) { $("#wire3d").checked = true; matCache.clear(); rebuild3d(); }
  if (params.get("turntable")) turntable();
  window.__ready = true;
  if (params.get("wait")) {            // test hook: headless screenshots skip WebGL canvases, so show a copy
    await new Promise(r => setTimeout(r, 800));
    renderer.render(scene, camera);
    const im = el("img", { src: canvas.toDataURL(), style: "position:absolute;inset:0;width:100%;height:100%;pointer-events:none" });
    $("#view3d").append(im);
  }
})();
