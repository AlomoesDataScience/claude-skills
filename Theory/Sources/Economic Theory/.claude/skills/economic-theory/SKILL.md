---
name: economic-theory
description: "the user's own economic theory (THE USER.md), the classics (Smith, Mill, Marx) as searchable text, and paradigm notes from the economics portal (PARADIGMS.md). Use when discussing economics, looking up a classic, or designing economies, markets or production for our games."
keywords: "adam, wealth, nations, john, stuart, principles, political, economy, karl, capital, volumes, i-iii, words, map, onto, engine, division, labour, value, prices, crises, rent, trade, money, credit, distribution, paradigms, design, goals, real, supply, chains, fog, market, debt, bonds, stocks, derivatives, multiple, systems, work, plans, add, theories, discusses, the user's theory, sustainability, agents decide, posted price, critics, charisma, listeners, information cost, reports, bookkeeping, complaints, fixers, savvy, chain, feudal, manorial, distributist, distributism, calculation in kind, neurath, inca, planned, material balances, gosplan, kornai, soft budget, stakhanov, emulation, parecon, lange, market socialism, mixed, gift economy, physiocracy, mercantilism, georgism, chartalism, austrian, post-keynesian, portal, wikipedia, capitalism, category, rentier, finance capitalism, state capitalism, gentlemanly capitalism, comprador"
---

# Economic theory shelf

Status 2026-11-09: all PDFs converted to `.txt` (Smith 786 pages, bookmarked; Mill 726; Capital
I 546, II 321 and III 588 - II and III bookmarked). Summaries are Claude's words.

## Read first
1. **THE USER.md** - the user's own theory in his words (2026-11-09): sustainability is the aim; agents decide (prices
   are deals); savvy sees the chain; fixers; critics and listeners set policy; information costs labour;
   complaints are the fast news; how feudal and distributist should work. His word beats the books for our games.
2. **PARADIGMS.md** - each economic system (market, planned, mixed, feudal, distributist/in kind, cooperative,
   presets) with how it works, where it works, where it fails, plus contested assumptions and mechanics a game can
   simulate. From 26 Wikipedia pages kept as text in `wiki/` (grep them for quotes). Category:Capitalism
   (2026-11-15): `wiki/capitalism/capitalism-index.json` tiers all 114 members (A 50 pulled as text, B 41 on
   demand, C 23 no); 7 subcategories listed, not followed. Not yet read into PARADIGMS.md.
3. The books below for depth. The 4X engine's own model: the engine4x-economy skill.

## The books

- **Smith, The Wealth of Nations** (`Wealth-Nations.pdf`): division of labour as the source of
  productivity, limited by the size of the market; prices around a natural price; self-interest
  coordinated by competition; wages, profit and rent; critique of mercantilism; the roles of
  the state (defence, justice, public works).
- **Mill, Principles of Political Economy** (`principlesofpoli00mill.pdf`): production follows
  natural laws but **distribution is a social choice**; rent, wages, comparative advantage in
  trade, the stationary state, co-operatives; a liberal reformer's economics. The old scan's text is
  poor OCR; use **`Mill-Principles-Laughlin-1885.txt`** (Gutenberg 30107, Laughlin's 1885 abridged
  college edition, added 2026-11-09, clean text, `=== page N` = PDF page). Pages: Of Property and
  Communism 200 (p.203: communal labour works "under the eye... of the whole community" - public
  opinion as the motive, the theory behind our distributist paradigm); Wages 222; Profits 268; Rent
  288; Value 304; Money 351; Credit 397-419; Inconvertible paper 419; Excess of supply 443;
  International trade 456; Interest 528; Falling profits 591; Stationary state 607; Futurity of the
  labouring classes (co-operation) 615; Taxation 637-702; National debt 702; Government interference 711.
- **Marx, Capital I** (`Capital-Volume-I.pdf`): commodities, use and exchange value, labour
  theory of value, surplus value, the working day, machinery, accumulation and the reserve army.
  **II**: circulation and turnover of capital, reproduction schemes (the sectors that make means
  of production vs consumer goods). **III**: profit rate and its tendency to fall, credit and
  fictitious capital, interest, ground rent, crises.

## the user's design goals these feed (Projects/Our Games/4x Game Engine/Economics, Finance)

- Economy "like real life": a production queue you set goals for ("cookie clicker" at empire
  scale), jobs assigned by market, self-assignment or the state; semi-abstract logistics.
- Paradigms of distribution: market with currency, distributionist (take what you need),
  state-assigned; Mill's "distribution is a choice" is the theory behind making them swappable.
- **Fog of market**: you only know stock levels you pay to check.
- Finance: debt, bonds, stock markets, derivatives whose prices swell with demand for get-rich
  schemes (Marx III's credit and fictitious capital; Smith on paper money).
- Real resource supply chains (Gear City, Avorion, Europa Universalis V named as references);
  replicators that still cost upkeep, knowledge and training (human capital, Smith's division
  of labour). Several systems must be able to win.

## Related skills
- engine4x-economy (Projects/Our Games/4x Game Engine): how the engine models all this, and its findings.
- engine4x-design: The user's full game vision. political-theory: his Critique of the West (critics, ideology).
- wiki-scout: how the wiki/ pages were pulled. Further scrapes follow its index-first standard (`scout.py index`).
