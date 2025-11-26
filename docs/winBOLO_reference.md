# winBOLO — Reference: original BOLO design and reproduction notes

Version: 1.0 — Objective reference for reproducing the original BOLO gameplay in a teaching project.

This document summarizes the gameplay systems, design patterns, legal/asset considerations, and an incremental roadmap appropriate for reproducing the original BOLO (a top‑down, tile‑based tank combat game) as a classroom‑friendly Python project.

## 1. Historical summary

- Origin: BOLO (first released in the late 1980s) is an overhead, real‑time tank combat game created by Stuart Cheshire and later widely played on Macintosh networks.
- Notable features: simultaneous multiplayer (up to 16 players in some versions), tile maps, pillboxes and bases, fuel/ammo management, and light building mechanics via a non‑combat unit (commonly called the Little Green Man or LGM).

## 2. High‑level gameplay model

- Perspective: top‑down, tile/grid world.
- Player object: a single tank controlled by one player (position, heading, health, ammo, fuel).
- Objectives: capture or defend pillboxes and bases, eliminate enemy tanks, and control territory via map objectives.
- Resources: fuel and ammunition are consumables; bases provide resupply.
- Construction: optional LGM unit that can place roads, bridges, or walls (advanced feature).

## 3. Core mechanics and rules (reference)

- Movement: tanks rotate and move forward/back along heading; movement can be grid‑aligned or continuous with collision against impassable terrain.
- Combat: firing spawns projectiles (bullets/ shells) that travel in straight lines and deal damage on impact; collisions with terrain or entities should be resolved deterministically.
- Fuel & ammo: firing and moving consume resources; entering a friendly base replenishes them.
- Pillboxes: map‑placed defensive emplacements that can fire on enemies and be captured by players.
- Map editing: community maps were historically supported; maps are a first‑class data artifact (see Section 6).

## 4. Data model (recommended)

- Map: 2D grid of tile IDs. Each tile stores terrain type and optional metadata (owner, health for structures).
- Entities: object model with per‑entity state including unique ID, type (Tank, Bullet, Pillbox, Base, LGM), position (x,y or tile coords), heading, velocity, health, and owner/team.
- State update: authoritative server or single‑player game should run a fixed update loop: process inputs → apply physics/movement → resolve collisions and combat → apply game rules (capture, respawn) → render.

## 5. Suggested incremental implementation roadmap

### Minimum viable product (MVP)
- Single‑player or local multiplayer.
- Tank movement, shooting, simple projectile collision, and a basic map.

### Phase 1
- Add ammo/fuel counters and a base tile that refills resources.
- Add neutral pillboxes that fire and can be damaged/captured.

### Phase 2
- Add simple AI for enemy tanks or pillboxes (distance/LOS targeting).
- Add map persistence (CSV, JSON, or custom text format) and a small set of sample maps.

### Phase 3 (advanced / optional)
- Implement LGM building actions (roads/bridges) and more advanced capture logic.
- Add basic networking (client/server): authoritative server handles world state; clients send input commands.
- Support more players, latency compensation, and tick synchronization as classroom time allows.

## 6. Map format and level design (guidance)

- Keep the first map format human‑readable (CSV or simple ASCII). Example CSV row: `0,0,1,1,2` where each number is a tile type index.
- Provide a tile palette mapping (index → terrain type) and a small legend in the repo.
- For student exercises, include a `maps/` folder with annotated example maps and a simple reader utility that converts CSV to runtime tile arrays.

## 7. Asset & licensing guidance

- Original BOLO assets (graphics/sound) are typically copyrighted; do not include them unless you have explicit permission or an appropriate license.
- Use permissively licensed or public‑domain assets for classroom code. Good sources include free asset packs on itch.io, CraftPix (free section), OpenGameArt.org (check licence per asset), and similar collections. Always verify license terms before redistribution.
- Prefer providing an `assets/` folder populated with clearly licensed art (or simple placeholder shapes) so students can run examples without legal risk.

## 8. Reference implementations and resources

- Orona / WinBolo derivatives: open‑source implementations exist (some under GPL). Study them for architecture and rules but heed their license terms if you plan to reuse code or assets.
- osgameclones.com and OpenGameArt are useful catalogs for related games and assets.

## 9. Networking notes (teaching considerations)

- For classroom use, prefer a staged approach: local single‑player → local multiplayer (splitscreen/hotseat) → simple 2‑player networking (UDP/TCP) → authoritative server model for multiple players.
- Key teaching topics: serialization of inputs, authoritative state updates, latency handling (client prediction vs. server reconciliation), and deterministic vs. non‑deterministic simulation.

## 10. Suggested project structure (starter skeleton)

Recommended minimal layout:

```
bring-back-BOLO/
├─ src/
│  ├─ main.py           # simple entry point / demo runner
│  ├─ game.py           # game loop, state manager
│  ├─ entities.py       # Tank, Bullet, Pillbox, Base, LGM classes
│  └─ map_loader.py     # CSV/JSON map loader
├─ assets/              # permissively licensed art + audio
├─ maps/                # example map files (CSV)
├─ requirements.txt
└─ README.md
```

## 11. Classroom exercises and milestones

- Exercise 1: Implement tank movement and rotation; display simple placeholder sprite.
- Exercise 2: Add projectile firing and collision detection; implement health/damage.
- Exercise 3: Implement a base tile that refuels the tank; show resource UI (ammo/fuel).
- Exercise 4: Create an example map and a small map editor to paint tiles.
- Advanced: Add simple networking; implement authoritative server tick and client input sync.

## 12. Legal & ethical note

- Respect copyright: do not redistribute original BOLO assets unless you hold rights.
- When using third‑party assets, include license attribution where required and document sources in the repository.

## 13. Next steps for this repo

- Decide whether to include a permissively licensed starter asset pack in `assets/`.
- Add a small `src/main.py` demo that loads a sample map and demonstrates movement/shooting.
- Optionally provide a separate `requirements-dev.txt` with developer tools (formatters, linters, test tools).

---

References & further reading
- WinBolo/Orona repositories (search for "Orona Bolo" / "WinBolo") — reference implementations (check GPL terms).
- OpenGameArt.org and itch.io — asset sources (verify licenses per asset).
