# Changelog

All notable changes to bring-back-BOLO will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2024-11-26 - Phase 2: Strategic Features

### Added
- **Complete game engine refactor** using object-oriented architecture
- **Tile-based terrain system** with 11 terrain types:
  - Deep Water, River, Swamp, Crater, Road, Forest, Rubble, Grass, Wall, Damaged Wall, Boat
  - Each terrain affects tank movement speed
  - Destructible terrain (walls, forests, swamps)
- **Resource management system**:
  - Armor (health): 0-8 points
  - Shells (ammo): 0-40 rounds
  - Mines (explosives): 0-40 mines
  - Wood (building material): 0-40 units
- **Base structures**:
  - Provide resupply for shells, mines, and armor
  - Can be captured by driving near them
  - Auto-regenerate supplies over time
  - Team-colored diamond shapes
- **Pillbox turrets**:
  - Auto-targeting defensive structures
  - Progressive fire rate (gets faster when attacked)
  - Can be captured and relocated
  - Team-colored squares
- **Mine deployment** (M key)
  - Creates craters on detonation
  - Damages nearby tanks
  - Strategic area denial
- **Advanced enemy AI**:
  - Pursuit behavior (chase player)
  - Combat engagement at range
  - Terrain-aware pathfinding
- **Camera system**:
  - Smooth scrolling that follows player
  - Map boundary clamping
- **Team system**:
  - 5 teams (Neutral, Team 1-4)
  - Color-coded entities
  - Team-based capture mechanics
- **Proper package structure**:
  - Created `src/` package directory
  - Modular `bolo_engine.py` with clear sections
  - Type hints throughout for code clarity

### Changed
- **Main.py** now serves as a clean entry point
- **Window size** standardized to 1160x1160 (square viewport)
- **Movement system** now terrain-aware with speed multipliers
- **Collision detection** improved with proper entity boundaries
- **Rendering** optimized with cached terrain surface

### Technical Improvements
- Entity-Component-System inspired architecture
- Abstract base classes for extensibility
- Dataclasses for clean data structures
- Comprehensive type annotations
- Improved code documentation with docstrings
- Configuration centralized in `Config` class

### Preserved from Phase 1
- **Original lesson/tank_game.py** - Simple educational version preserved
- All core pygame mechanics
- Basic tank controls and shooting

---

## [0.1.0] - 2024-11-XX - Phase 1: Core Mechanics

### Added
- Basic tank movement (WASD/Arrow keys)
- Simple shooting mechanics (SPACE)
- Basic enemy AI with random movement
- Obstacle collision detection
- Simple score tracking
- Game over and restart (R key)
- Educational code comments for learning

### Features
- Green player tank
- Red enemy tanks
- Gray obstacles
- Yellow bullets
- Black background

---

## Roadmap

### Phase 3: Polish (Upcoming)
- [ ] Sprite-based graphics (using Kenney assets)
- [ ] Sound effects and music
- [ ] Map editor
- [ ] LGM (Little Green Man) engineer unit
- [ ] Wood harvesting from forests
- [ ] Building system (roads, walls)
- [ ] Multiple game modes
- [ ] Improved AI with formations

### Phase 4: Multiplayer (Future)
- [ ] Local split-screen multiplayer
- [ ] Network architecture
- [ ] Lobby and matchmaking
- [ ] Full 16-player support
- [ ] Chat system
- [ ] Spectator mode

---

## Credits

**Original BOLO** by Stuart Cheshire (1987-1995)  
**bring-back-BOLO** by Code the Dream / StrayDog Syndications  
**License:** MIT
