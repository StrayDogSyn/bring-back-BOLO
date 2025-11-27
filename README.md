# bring-back-BOLO 🎮

<div align="center">

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://www.python.org/downloads/)
[![Pygame](https://img.shields.io/badge/Pygame-2.1+-red.svg)](https://www.pygame.org/)
[![Status](https://img.shields.io/badge/Status-Active-yellow.svg)](#project-status)

**A faithful, modern reproduction of the classic top-down tank combat game BOLO**

![Game Screenshot](assets/screenshot.png)

*Capturing the nostalgic gameplay of the original 1987 BOLO for modern platforms*


</div>

---

## 📖 What is BOLO?

BOLO is a legendary networked multiplayer tank battle game created by **Stuart Cheshire** in 1987 for the BBC Micro, later ported to Macintosh (1989-1995). It pioneered real-time networked multiplayer gaming and combined arcade action with real-time strategy elements.

Key features of the original:
- **16-player networked multiplayer** - Revolutionary for its time
- **Strategic depth** - Capture bases, deploy pillboxes, manage resources
- **Terrain destruction** - Explosions create craters, forests can be cleared
- **LGM (Little Green Man)** - Engineer unit for building roads, walls, and placing mines
- **Emergent gameplay** - No fixed objectives, player-driven alliances and strategies

> *"Bolo is the Hindi word for communication. Bolo is about computers communicating on the network, and more importantly about humans communicating with each other, as they argue, negotiate, form alliances, agree strategies, etc."*  
> — Stuart Cheshire

---

## 🎯 Project Goals

1. **Faithful Recreation** - Capture the feel and mechanics of the original
2. **Modern Platform Support** - Windows, macOS, Linux via Python/Pygame
3. **Educational Value** - Clean, well-documented code for learning
4. **Extensibility** - Easy to modify, extend, and experiment with
5. **Multiplayer (Future)** - Eventually support networked play

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/bring-back-BOLO.git
cd bring-back-BOLO

# Create virtual environment
python -m venv .venv

# Activate (Linux/macOS)
source .venv/bin/activate
# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Download CC0 sprite assets
python scripts/download_assets.py

# Run the game!
python main.py
```

### Controls

| Key | Action |
|-----|--------|
| W / ↑ | Move Forward |
| S / ↓ | Move Backward |
| A / ← | Rotate Left |
| D / → | Rotate Right |
| SPACE | Fire Shell |
| M | Place Mine |
| ESC | Pause Game |
| R | Restart |

---

## 📁 Project Structure

```
bring-back-BOLO/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── LICENSE                 # MIT License
│
├── src/                    # Source code
│   ├── __init__.py
│   └── bolo_engine.py      # Core game engine
│
├── assets/                 # Game assets
│   └── sprites/            # Sprite images (CC0)
│
├── docs/                   # Documentation
│   ├── BOLO_RESEARCH.md    # Game mechanics research
│   └── winBOLO_reference.md # Original game reference
│
├── lesson/                 # Educational materials
│   ├── LESSON_PLAN.md      # Teaching guide
│   └── tank_game.py        # Simplified demo version
│
└── scripts/                # Utility scripts
    └── download_assets.py  # Asset downloader
```

---

## 🎮 Game Mechanics

### Terrain Types

| Terrain | Speed | Properties |
|---------|-------|------------|
| Road | 1.2x | Fastest movement |
| Grass | 0.8x | Default terrain |
| Forest | 0.4x | Slow, provides wood |
| Swamp | 0.25x | Very slow, destructible |
| Crater | 0.5x | Created by explosions |
| River | 0.3x | Needs boat for deep water |
| Wall | 0x | Blocks movement and shots |

### Structures

- **Bases** - Provide resupply (shells, mines, armor). Capturable.
- **Pillboxes** - Auto-firing defensive turrets. Capturable, relocatable.

### Resources

| Resource | Max | Source | Usage |
|----------|-----|--------|-------|
| Armor | 8 | Bases | Tank health |
| Shells | 40 | Bases | Cannon ammo |
| Mines | 40 | Bases | Explosives |
| Wood | 40 | Forests | Building |

---

## 📚 Research & References

### Open Source Implementations

| Project | Language | Notes |
|---------|----------|-------|
| [WinBolo](https://github.com/kippandrew/winbolo) | C/C++ | GPL v2, full source |
| [Orona](https://github.com/stephank/orona) | CoffeeScript | Browser-based |
| [PyBolo](https://github.com/joncox123/PyBoloPublic) | Python | 2024, closed source |

### Legal Assets (CC0)

- **[Kenney Topdown Tanks](https://opengameart.org/content/topdown-tanks)** - 86 sprites
- **[OpenGameArt Tank Sprite](https://opengameart.org/content/tank-sprite)** - Simple tank + turret

### Historical Resources

- [Internet Archive - BOLO](https://archive.org/details/BoloMacintosh)
- [Macintosh Garden](https://macintoshgarden.org/games/bolo)
- [WinBolo Wiki](http://www.winbolo.org/wiki)

---

## 🗓️ Development Roadmap

### Phase 1: Core ✅
- [x] Tile-based map rendering
- [x] Tank movement with terrain speed
- [x] Shooting mechanics
- [x] Collision detection
- [x] Basic enemy AI

### Phase 2: Strategic (In Progress)
- [x] Bases with resupply
- [x] Pillboxes with auto-targeting
- [x] Capture mechanics
- [ ] LGM engineer unit
- [ ] Wood harvesting
- [ ] Building (roads, walls)

### Phase 3: Polish
- [ ] Sprite-based graphics
- [ ] Sound effects
- [ ] Map editor
- [ ] Multiple game modes
- [ ] AI improvements

### Phase 4: Multiplayer (Future)
- [ ] Local multiplayer
- [ ] Network architecture
- [ ] Lobby/matchmaking
- [ ] Full 16-player support

---

## 🤝 Contributing

We welcome contributions! Here's how to help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'feat: add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Commit Convention

```
feat: add new feature
fix: bug fix
docs: documentation changes
style: formatting, no code change
refactor: code restructuring
test: adding tests
```

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**Asset Licenses:**
- Kenney assets: CC0 (Public Domain)
- Original BOLO graphics/sounds: © Stuart Cheshire (NOT included)

---

## 🙏 Acknowledgments

- **Stuart Cheshire** - Original BOLO creator
- **John Morrison** - WinBolo developer
- **Kenney.nl** - CC0 game assets
- **Code the Dream** - Python Essentials program
- **The BOLO Community** - Decades of maps, mods, and memories

---

<div align="center">

**Happy tanking! 🎮**

*Built with ❤️ for the Code the Dream community*

</div>
