// injected after main.js: once the inspector has prepared its data, render every object's
// detail overlay and send it, with the object's computed fields, to the local dump server
(function () {
  const KINDS = [["units", "unitdata"], ["spells", "spelldata"], ["items", "itemdata"], ["weapons", "wpndata"],
                 ["armor", "armordata"], ["sites", "sitedata"], ["mercs", "mercdata"], ["events", "eventdata"],
                 ["nations", "nationdata"]];
  const ref = x => x && typeof x === "object" ? (x.id !== undefined ? { id: x.id, name: x.fullname || x.name || x.nationname } : null) : x;
  function flat(o) {
    const r = {};
    for (const k in o) {
      const v = o[k];
      if (v == null || typeof v === "function" || k.startsWith("jQuery")) continue;
      if (typeof v !== "object") r[k] = v;
      else if (Array.isArray(v)) r[k] = v.map(x => (x && typeof x === "object" && x.id === undefined) ? flat1(x) : ref(x));
      else if (v.id !== undefined) r[k] = ref(v);
      else r[k] = flat1(v);
    }
    return r;
  }
  function flat1(o) {             // one level for plain sub-objects (random paths, unit counts...)
    const r = {};
    for (const k in o) { const v = o[k]; if (v == null || typeof v === "function") continue; r[k] = typeof v === "object" ? (Array.isArray(v) ? v.map(ref) : ref(v)) : v; }
    return r;
  }
  async function post(kind, body) {
    await fetch("/dump/" + kind, { method: "POST", body: JSON.stringify(body) });
  }
  async function dumpAll() {
    DMI.Options["Show ids"] = 1; DMI.Options["Show modding info"] = 1;
    const ctx = DMI.modctx;
    for (const [kind, key] of KINDS) {
      const list = ctx[key] || [];
      const out = [];
      for (const o of list) {
        let html = "";
        try { html = o.renderOverlay ? o.renderOverlay(o) : ""; } catch (e) { html = "RENDER ERROR " + e; }
        let data = {};
        try { data = flat(o); } catch (e) { data = { error: String(e) }; }
        out.push({ data, html: typeof html === "string" ? html : (html && html.outerHTML) || "" });
      }
      await post(kind, out);
    }
    await post("messages", { loadedmods: ctx.loadedmods || [], messages });
    await post("done", { keys: Object.keys(ctx) });
  }
  // the mod parser reports problems only on the console: keep them
  const messages = [], log = console.log.bind(console);
  console.log = function (...a) {
    const t = a.map(String).join(" ");
    if (/^(ERROR|WARNING)/.test(t)) messages.push(t);
    log(...a);
  };
  // a crash while loading would leave the page hanging: report it instead
  window.addEventListener("error", e => post("error", { e: String(e.message), where: `${e.filename}:${e.lineno}`, messages }));
  if (DMI.Utils && DMI.Utils.error) {                 // errors the site shows on the page
    const uerr = DMI.Utils.error;
    DMI.Utils.error = function (msg) { messages.push("SITE ERROR: " + String(msg).replace(/<[^>]+>/g, " ")); return uerr.apply(this, arguments); };
  }
  // site bug: some mod commands (e.g. #coastcom) store one value where the nation code expects a
  // list, and preparing nations then crashes. Wrap such values in lists first, and say so.
  if (DMI.MNation && DMI.MNation.prepareData_PostMod) {
    const prep = DMI.MNation.prepareData_PostMod;
    DMI.MNation.prepareData_PostMod = function () {
      const nations = DMI.modctx.nationdata || [], listKeys = new Set();
      for (const o of nations) for (const k in o) if (Array.isArray(o[k])) listKeys.add(k);
      for (const o of nations) for (const k of listKeys) {
        if (o[k] != null && !Array.isArray(o[k])) {
          messages.push(`WORKAROUND: nation ${o.id} ${k} = ${o[k]} was a single value; made it a list (site bug)`);
          o[k] = [o[k]];
        }
      }
      return prep.apply(this, arguments);
    };
  }
  const orig = DMI.initGrids;
  DMI.initGrids = function () { orig.apply(this, arguments); setTimeout(() => dumpAll().catch(e => post("error", { e: String(e), stack: e.stack })), 300); };
})();
