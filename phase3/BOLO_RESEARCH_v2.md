# BOLO Research Findings - Complete Reference

## Executive Summary

BOLO is a networked multiplayer tank battle game created by **Stuart Cheshire** in 1987 (BBC Micro), later ported to Macintosh (1989-1995). It pioneered real-time networked multiplayer gaming and combined arcade action with real-time strategy elements.

---

## 📚 Available Open Source Resources

### Source Code Repositories

| Project | Language | License | Status | URL |
|---------|----------|---------|--------|-----|
| **WinBolo** | C/C++ | GPL v2 | Reference | github.com/kippandrew/winbolo |
| **LinBolo** | C | GPL v2 | Reference | github.com/i68040/linbolo |
| **Orona** | CoffeeScript | GPL v2 | Playable | github.com/stephank/orona |
| **PyBolo** | Python 3 | Proprietary* | Active 2024 | github.com/joncox123/PyBoloPublic |
| **Lobo** | NetLogo | Open | Educational | github.com/earwig/lobo |
| **Bolorama** | ? | Open | NAT Helper | github.com/astrospark/bolorama |

*PyBolo is closed source but provides excellent documentation on architecture decisions.

### Asset Sources (Legal, CC0)

| Source | Content | License | URL |
|--------|---------|---------|-----|
| **Kenney Topdown Tanks** | 86 sprites, tanks, tiles | CC0 | opengameart.org/content/topdown-tanks |
| **OpenGameArt Tank Sprite** | Simple tank + turret | CC0 | opengameart.org/content/tank-sprite |
| **OpenGameArt Tilesets** | Terrain tiles | Various CC0 | opengameart.org/content/tilesets-6 |

**⚠️ IMPORTANT:** Original BOLO graphics and sounds © 1993 Stuart Cheshire. Do NOT use without permission.

---

## 🎮 Core Game Mechanics

### Tank Properties

```
Attribute       | Description
----------------|------------------------------------------
Armor           | 8 units (40 shells to kill @ 5 damage each)
Shells          | Max 40, 4 damage per hit
Mines           | Max 40, can be placed or drilled
Speed           | Variable based on terrain
Rotation        | Smooth, analog-style
```

### Terrain Types & Movement

| Tile Type | Movement Speed | Properties |
|-----------|---------------|------------|
| **Road** | Fastest (1.0x) | Built by LGM, connects areas |
| **Grass** | Medium (0.7x) | Default open terrain |
| **Forest** | Slow (0.4x) | Provides wood, regrows over time |
| **Swamp** | Very Slow (0.3x) | Takes 4 shells to destroy |
| **Crater** | Slow (0.5x) | Created by explosions |
| **Water (shallow)** | Slow | Boat required for deep |
| **Water (deep)** | N/A | Drowns tank without boat |
| **Wall** | Impassable | Built by LGM, blocks shots |

### Structures

#### Bases (Refueling Stations)
- Provide: Shells, Mines, Armor repair
- Regenerate stock over time (1 unit per 20 sec per player)
- Can be captured (shoot to 0 health, touch to capture)
- Cannot be moved

#### Pillboxes (Defensive Turrets)
- Auto-fire at enemies
- Increase fire rate when attacked (progressive difficulty)
- Can be captured, picked up, and relocated by LGM
- 16 units of health

### LGM (Little Green Man / Engineer)

The LGM is a small builder unit that exits the tank to perform tasks:

| Action | Cost | Description |
|--------|------|-------------|
| Harvest Wood | 0 | Collect from forests |
| Build Road | 2 wood | Speeds up movement |
| Build Wall | 2 wood | Blocks movement and shots |
| Build Boat | 5 wood | Allows water traversal |
| Place Mine | 1 mine | Hidden explosive |
| Drill Mine | 1 mine | Permanent, invisible mine |
| Capture Pillbox | 0 | Pick up neutral/destroyed pill |
| Place Pillbox | 0 | Deploy carried pillbox |

**Vulnerability:** LGM can be killed. Replacement parachutes in after ~60 seconds.

### Resource System

```
Resource   | Source              | Max  | Usage
-----------|---------------------|------|------------------
Wood       | Harvest forests     | 40   | Building structures
Shells     | Bases               | 40   | Firing cannon
Mines      | Bases               | 40   | Planting explosives
Armor      | Bases               | 8    | Health points
```

---

## 🗺️ Map Format (Original BOLO)

The original BOLO map format uses a run-length encoded binary format:

```
Header:
  - Map size: 256x256 tiles
  - Pill positions (up to 16)
  - Base positions (up to 16)
  - Start positions (up to 16 players)

Tile Data (RLE compressed):
  - Tile type byte (0-15)
  - Run length byte
```

### Tile Type Values (WinBolo)

```python
TILE_TYPES = {
    0x00: "BUILDING",      # Solid wall/building
    0x01: "RIVER",         # Deep water
    0x02: "SWAMP",         # Slow movement
    0x03: "CRATER",        # Explosion damage
    0x04: "ROAD",          # Fast movement
    0x05: "FOREST",        # Slow, provides wood
    0x06: "RUBBLE",        # Destroyed building
    0x07: "GRASS",         # Normal terrain
    0x08: "HALFBUILDING",  # Damaged building
    0x09: "BOAT",          # Moored boat
    0x0A: "SWAMP_DAMAGED", # Damaged swamp
    0x0B: "CRATER_DEEP",   # Deep crater
    # ... additional types
}
```

---

## 🌐 Networking Architecture

### Original BOLO (AppleTalk)
- Peer-to-peer using AppleTalk NBP (Name Binding Protocol)
- Up to 16 players
- LAN only (pre-Internet era)

### WinBolo (Client/Server)
- Central server architecture
- Internet play via tracker service
- Game state synchronized across clients

### PyBolo (Modern Approach - 2024)
Key innovations worth noting:
1. **Input-only transmission** - Clients only send keystrokes to server
2. **Authoritative server** - Server runs complete game simulation
3. **Clock synchronization** - Critical for smooth gameplay
4. **Anti-cheat by design** - Clients can't manipulate game state

---

## 🎯 Victory Conditions

Original BOLO had no fixed end condition. Modern implementations add:

1. **Base Control** - Capture all bases
2. **Pillbox Control** - Capture all pillboxes  
3. **Elimination** - Destroy all enemy tanks (temporary, respawn exists)
4. **Territory Control** - Percentage-based map control
5. **Time Limit** - Most points when time expires

---

## 🔧 Implementation Priorities

### Phase 1: Core (MVP)
- [ ] Tile-based map rendering
- [ ] Tank movement with terrain speed modifiers
- [ ] Basic shooting mechanics
- [ ] Simple collision detection
- [ ] Single-player with dummy enemies

### Phase 2: Strategic Elements
- [ ] Bases with resupply
- [ ] Pillboxes with auto-targeting AI
- [ ] Capture mechanics
- [ ] Health/armor system
- [ ] Ammunition limits

### Phase 3: LGM & Building
- [ ] LGM unit deployment
- [ ] Wood harvesting from forests
- [ ] Building roads and walls
- [ ] Mine placement
- [ ] Forest regrowth over time

### Phase 4: Multiplayer
- [ ] Basic networking (2 players)
- [ ] Server-authoritative architecture
- [ ] Lobby/matchmaking
- [ ] Full 16-player support

---

## 📖 Key Design Philosophies

From Stuart Cheshire's original documentation:

> "Bolo is the Hindi word for communication. Bolo is about computers communicating on the network, and more importantly about humans communicating with each other, as they argue, negotiate, form alliances, agree strategies, etc."

The game succeeds because it:
1. **Rewards strategy over reflexes** - Slow tanks, tactical positioning
2. **Enables cooperation** - Team play is essential at high levels
3. **Provides persistent consequences** - Terrain changes, resource management
4. **Supports emergent gameplay** - No fixed objectives, player-driven goals

---

## 🔗 Reference Links

### Official/Historical
- Internet Archive BOLO: archive.org/details/BoloMacintosh
- Macintosh Garden: macintoshgarden.org/games/bolo
- WinBolo Wiki: winbolo.org/wiki

### Community
- TV Tropes: tvtropes.org/pmwiki/pmwiki.php/VideoGame/Bolo1987
- Codex Gamicus: gamicus.fandom.com/wiki/Bolo

### Technical
- WinBolo Source: github.com/kippandrew/winbolo
- Orona (Browser): github.com/stephank/orona
- PyBolo (Python): github.com/joncox123/PyBoloPublic

---

*Document compiled: November 2024*
*For: bring-back-BOLO capstone project*
