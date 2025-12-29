# Replit Codex: Leyline Idle RPG (RPG Maker-Style Structure)

This codex describes how to stand up a miniature idle RPG on Replit using an **RPG Maker-style** scene/actor/event structure. It links in-world maps to a simplified "real life" grid and leyline-inspired spiritual structure. The focus is a lightweight prototype that can be expanded later.

## 1) Core Concept
- **Player loop:** the game progresses passively (time-based ticks) while the player invests energy into grid nodes, harvests resonance, and unlocks sigils.
- **World model:** a 2D grid of tiles representing physical locations; certain tiles are **Ley Nodes** with extra bonuses and sigil effects.
- **Aesthetic:** use the provided sigil-style visuals as overlays for nodes, resonance flows, and ritual animations.

## 2) Replit Project Layout
```
.
├─ index.html          # Splash + canvas overlay for sigil/line renders
├─ main.js             # Game loop, scene manager, data models
├─ styles.css          # Neon/astral UI theme
├─ data/
│  ├─ grid.json        # Tile definitions + leyline metadata
│  └─ sigils.json      # Sigil art references and stat effects
└─ assets/             # Optional: upload sigil sprites/PNGs from reference image
```

**RPG Maker parallels**
- **SceneManager:** handles transitions between title, map, ritual UI, and codex screens.
- **Actors:** player avatar and familiars; actors have stats, energy, and traits.
- **Events:** scripted interactions on grid tiles (e.g., "Touch Ley Node" → start ritual mini-event).
- **Switches/Variables:** global flags for unlocks (e.g., `SW_UNLOCK_SIGIL_03`, `VAR_RESONANCE_POOL`).
- **Common Events:** reusable flows like daily reset, resonance payout, or ritual animation.

## 3) Data: Grid + Leylines
Create `data/grid.json` with tiles and node metadata:
```json
{
  "width": 6,
  "height": 4,
  "tiles": [
    { "id": "A1", "type": "city",  "ley": false },
    { "id": "A2", "type": "forest","ley": true, "node": "north-sigil" },
    { "id": "A3", "type": "river", "ley": false },
    { "id": "A4", "type": "desert","ley": true, "node": "mirror-line" }
  ],
  "leylines": [
    { "path": ["A2","A4"], "element": "aether", "bonus": 0.12 },
    { "path": ["B1","B3","B4"], "element": "water", "bonus": 0.08 }
  ]
}
```
- **`tiles`** use IDs to map to a 2D matrix; any tile with `"ley": true` can host rituals.
- **`leylines`** describe connective routes; apply the bonus when a player has touched every node in a path.

## 4) Data: Sigils + Resonance
Create `data/sigils.json` to mirror the glowing sigils from the reference art. Each sigil grants passive modifiers.
```json
[
  {
    "id": "north-sigil",
    "name": "Polar Gate",
    "element": "aether",
    "sprite": "assets/sigil_polar.png",
    "effects": { "resonanceRate": 0.15, "ritualSpeed": 0.1 }
  },
  {
    "id": "mirror-line",
    "name": "Mirror Line",
    "element": "shadow",
    "sprite": "assets/sigil_mirror.png",
    "effects": { "resonanceRate": 0.08, "critChance": 0.05 }
  }
]
```

## 5) Main Game Loop (idle-friendly)
In `main.js`, implement a tick loop (30–60 FPS for visuals; slower logical ticks for economy):
```js
const TICK_MS = 1000; // logical tick every second
let state = {
  time: 0,
  resonance: 0,
  actors: { player: { energy: 100, regen: 2, traits: ["seer"] } },
  grid: loadGrid(),
  sigils: loadSigils(),
  switches: {},
};

function tick() {
  state.time += 1;
  const passive = calcResonance(state);
  state.resonance += passive;
  applyDailyReset(state);
  renderHUD(state);
}
setInterval(tick, TICK_MS);
```
- **calcResonance:** base rate + bonuses from claimed Ley Nodes + leyline completions + active sigils.
- **applyDailyReset:** common event that refreshes rituals and node charges at UTC midnight.
- **renderHUD:** draw resonance flow and sigil overlays on the canvas.

## 6) Scene & Event Hooks
RPG Maker-like functions to keep structure familiar:
```js
class SceneManager {
  static change(scene) { currentScene = scene; scene.start(); }
}

class SceneMap {
  start() { drawGrid(state.grid); }
  onTileClick(tileId) {
    const tile = getTile(tileId);
    if (tile.ley) SceneManager.change(new SceneRitual(tile));
  }
}

class SceneRitual {
  constructor(tile) { this.tile = tile; }
  start() { playSigilAnimation(this.tile.node); startRitualTimer(this.tile); }
}
```
- **Common Event examples:**
  - `EV_TOUCH_LEY_NODE`: grants resonance burst, checks leyline completion.
  - `EV_UNLOCK_SIGIL`: toggles `switches[sigilId] = true` and updates HUD.
  - `EV_EXPORT_CODex`: writes current unlocks to localStorage for persistence.

## 7) Real-Life Grid Link (lightweight)
- Map **real coordinates** to tiles by rounding GPS lat/long into a coarse grid (e.g., 0.01° bins). In Replit, stub a function that accepts coordinates and picks the nearest tile.
- Keep privacy-safe: only store rounded bins and never raw precise locations.
- Offer an offline fallback: if the browser cannot access location, fall back to a fictional seed that still maps to the same grid layout.

## 8) Leyline Visualization
- Use a HTML5 canvas overlay in `index.html` to draw **glowing lines and sigil bursts** similar to the reference art. Layer additive blending (`ctx.globalCompositeOperation = "screen"`) and blurred strokes for ethereal look.
- Animate ritual completion by scaling sigil sprites from 0.6→1.1→1.0 with easing and a vertical blue flame particle trail.

## 9) Balancing Notes
- Keep **short session rewards** (10–30 seconds) for tapping a node, but let **long idle** ticks accumulate resonance via sigil bonuses.
- Introduce **diminishing returns** on spamming the same node; reward visiting multiple ley paths.
- Add **traits** (e.g., `"geomancer"`, `"dream-hacker"`) that modify resonance on specific elements.

## 10) Fast Start Checklist (Replit)
1. Create a new **HTML/CSS/JS** Replit.
2. Add the files from the layout above; paste the loop/scene snippets into `main.js`.
3. Upload the sigil sprites exported from the reference image into `assets/` and wire them in `sigils.json`.
4. Open the webview; verify the canvas draws grid tiles, leyline paths, and sigil overlays.
5. Tune `calcResonance` and ritual timers until idle gain feels smooth.

## 11) Extending the Codex
- Add a **Codex UI** page listing unlocked sigils, leylines, and their lore blurbs.
- Add **Familiars** as auto-runners that gather resonance on a schedule.
- Add **Seasonal Events**: rotate leyline elements weekly and change bonuses to keep the idle loop fresh.

> Use this codex as a scaffold: it keeps the RPG Maker feel (scenes, actors, events) while embracing an idle loop and leyline-connected world-building.
