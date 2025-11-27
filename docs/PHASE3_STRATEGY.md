# Phase 3 Implementation Strategy - bring-back-BOLO

**Date**: November 26, 2024  
**Branch**: phase3  
**Goal**: Transform monolithic Phase 2 into modular, professional architecture

---

## Current State Assessment

### What We Have (Phase 2)
```
bring-back-BOLO/
├── main.py (70 lines)           # Clean entry point ✅
├── src/
│   ├── __init__.py (25 lines)   # Package exports ✅
│   └── bolo_engine.py (1,217 lines) # MONOLITHIC ⚠️
├── lesson/tank_game.py          # Phase 1 reference ✅
├── docs/ (multiple .md files)   # Documentation ✅
└── requirements.txt             # Dependencies ✅
```

### Strengths
✅ **Game is fully functional** - All Phase 2 features work  
✅ **Comprehensive documentation** - 6 major docs created  
✅ **Clean entry point** - main.py is well-structured  
✅ **Type hints** - 95%+ coverage  
✅ **Key bindings fixed** - All controls working  

### Weaknesses
❌ **Monolithic design** - 1,217 lines in single file  
❌ **No tests** - Zero unit tests  
❌ **No sprites** - Shape-based graphics only  
❌ **No sounds** - Silent gameplay  
❌ **Hard-coded config** - Magic numbers scattered  
❌ **No LGM system** - Missing engineer unit  
❌ **Limited modularity** - Hard to extend  

---

## Target Architecture (Kilo Code Build)

### Desired Structure
```
bring-back-BOLO/
├── main.py
├── pyproject.toml              # NEW: Modern packaging
├── requirements.txt
│
├── src/
│   ├── __init__.py
│   ├── config.py               # NEW: Dataclass configs
│   ├── enums.py                # NEW: Type-safe enums
│   │
│   ├── entities/               # NEW: Entity modules
│   │   ├── __init__.py
│   │   ├── base_entity.py      # Abstract base
│   │   ├── tank.py
│   │   ├── projectile.py       # Shell, Mine
│   │   ├── structures.py       # Pillbox, Base
│   │   └── lgm.py              # Engineer unit
│   │
│   ├── systems/                # NEW: Game systems
│   │   ├── __init__.py
│   │   ├── collision.py
│   │   ├── combat.py
│   │   ├── resources.py
│   │   └── ai.py
│   │
│   ├── world/                  # NEW: Map system
│   │   ├── __init__.py
│   │   ├── game_map.py
│   │   ├── camera.py
│   │   └── map_loader.py
│   │
│   ├── rendering/              # NEW: Rendering layer
│   │   ├── __init__.py
│   │   ├── renderer.py
│   │   ├── sprite_manager.py
│   │   └── ui.py
│   │
│   └── game.py                 # Main game class
│
├── assets/                     # NEW: Game assets
│   ├── sprites/
│   ├── sounds/
│   └── maps/
│
├── tests/                      # NEW: Unit tests
│   ├── __init__.py
│   ├── test_entities.py
│   ├── test_collision.py
│   └── test_map.py
│
└── docs/
    ├── ARCHITECTURE.md         # NEW: Technical design
    └── [existing docs]
```

---

## Migration Strategy

### Approach: Incremental Refactoring
**NOT** a complete rewrite. We'll extract and modularize in stages.

### Phase 3A: Foundation (Week 1)
**Goal**: Set up structure without breaking existing functionality

1. **Create new directory structure**
   ```bash
   mkdir src/entities src/systems src/world src/rendering tests assets
   mkdir assets/sprites assets/sounds assets/maps
   ```

2. **Extract configuration** (Day 1)
   - Create `src/config.py` with dataclasses
   - Create `src/enums.py` with TileType, Team, GamePhase
   - Keep `bolo_engine.py` working alongside new modules

3. **Extract base entity** (Day 2)
   - Create `src/entities/base_entity.py`
   - Define abstract Entity class
   - Update imports in `bolo_engine.py`

4. **Add packaging** (Day 2)
   - Create `pyproject.toml`
   - Update dependencies

### Phase 3B: Entity Extraction (Week 2)
**Goal**: Separate entities into focused modules

5. **Extract Tank** (Day 3)
   - Create `src/entities/tank.py`
   - Move Tank class from `bolo_engine.py`
   - Add comprehensive docstrings
   - Write unit tests

6. **Extract Projectiles** (Day 4)
   - Create `src/entities/projectile.py`
   - Move Shell and Mine classes
   - Add tests

7. **Extract Structures** (Day 4-5)
   - Create `src/entities/structures.py`
   - Move Pillbox and Base classes
   - Add tests

### Phase 3C: Systems Layer (Week 3)
**Goal**: Extract game logic into systems

8. **Collision System** (Day 6)
   - Create `src/systems/collision.py`
   - Extract collision detection logic
   - Add spatial partitioning
   - Write comprehensive tests

9. **Combat System** (Day 7)
   - Create `src/systems/combat.py`
   - Extract damage/health logic
   - Add tests

10. **Resource System** (Day 8)
    - Create `src/systems/resources.py`
    - Extract resupply/capture logic
    - Add tests

11. **AI System** (Day 8-9)
    - Create `src/systems/ai.py`
    - Extract enemy AI behavior
    - Implement proper state machine
    - Add tests

### Phase 3D: World System (Week 4)
**Goal**: Improve map and camera systems

12. **GameMap Refactor** (Day 10)
    - Create `src/world/game_map.py`
    - Extract map logic
    - Add terrain info lookup
    - Implement forest regrowth

13. **Camera System** (Day 11)
    - Create `src/world/camera.py`
    - Extract camera logic
    - Add smooth following
    - Add zoom capability

14. **Map Loader** (Day 11)
    - Create `src/world/map_loader.py`
    - Implement CSV map format
    - Add map validation
    - Create 3-5 test maps

### Phase 3E: Rendering (Week 5)
**Goal**: Add sprite graphics and polish

15. **Sprite Manager** (Day 12-13)
    - Create `src/rendering/sprite_manager.py`
    - Download Kenney sprite sheets
    - Implement sprite loading
    - Add rotation caching
    - Maintain shape fallback

16. **UI System** (Day 14)
    - Create `src/rendering/ui.py`
    - Extract HUD rendering
    - Add minimap
    - Improve pause/game over screens

17. **Renderer** (Day 14-15)
    - Create `src/rendering/renderer.py`
    - Coordinate all rendering
    - Implement dirty rectangles
    - Optimize performance

### Phase 3F: LGM System (Week 6)
**Goal**: Add engineer unit

18. **LGM Entity** (Day 16-17)
    - Create `src/entities/lgm.py`
    - Implement LGM class
    - Add deployment mechanics
    - Add task system

19. **Building System** (Day 18)
    - Implement road building
    - Implement wall building
    - Add wood harvesting
    - Add tests

### Phase 3G: Audio & Polish (Week 7)
**Goal**: Add sound and final touches

20. **Sound Manager** (Day 19)
    - Find/create CC0 sound effects
    - Create `src/rendering/sound_manager.py`
    - Add sound playback
    - Add volume controls

21. **Testing & Bug Fixes** (Day 20-21)
    - Complete unit test suite
    - Performance profiling
    - Bug fixes
    - Documentation updates

---

## Implementation Guidelines

### Coding Standards

#### Type Hints (Required)
```python
# Good ✅
def calculate_damage(base: int, armor: int, mult: float = 1.0) -> int:
    return max(0, int((base - armor) * mult))

# Bad ❌
def calculate_damage(base, armor, mult=1.0):
    return max(0, int((base - armor) * mult))
```

#### Docstrings (Google Style)
```python
def find_path(start: TileCoord, end: TileCoord, game_map: GameMap) -> List[TileCoord]:
    """
    Find path using A* algorithm.
    
    Args:
        start: Starting tile coordinates
        end: Target tile coordinates
        game_map: Map to pathfind on
    
    Returns:
        List of tiles forming path, empty if no path exists.
    
    Raises:
        ValueError: If coordinates out of bounds.
    """
    pass
```

#### Small Functions
- Target: < 30 lines per function
- Single Responsibility Principle
- Extract complex logic into helpers

#### Dataclasses Over Dicts
```python
# Good ✅
@dataclass
class TerrainInfo:
    name: str
    speed_multiplier: float
    passable: bool

# Bad ❌
terrain_info = {
    "name": "Grass",
    "speed": 0.8,
    "passable": True
}
```

### Testing Standards

#### Unit Test Coverage
- All entities: > 80% coverage
- All systems: > 90% coverage
- All utilities: 100% coverage

#### Test Structure
```python
def test_tank_fire_cooldown():
    """Tank should respect fire cooldown."""
    # Arrange
    tank = Tank(100, 100, Team.TEAM_1)
    game_state = create_test_game_state()
    
    # Act
    shell1 = tank.fire(game_state)
    shell2 = tank.fire(game_state)  # Immediate
    
    # Assert
    assert shell1 is not None
    assert shell2 is None  # Blocked by cooldown
```

### Performance Targets

| Metric | Target | Critical |
|--------|--------|----------|
| FPS | 60 | 30 |
| RAM | < 200 MB | < 500 MB |
| Load Time | < 2s | < 5s |
| Max Entities | 200+ | 100+ |

### Git Workflow

#### Commit Messages
```
feat: add sprite manager with rotation caching
fix: collision detection false positives
docs: update architecture documentation
refactor: extract AI into separate module
test: add unit tests for tank movement
perf: implement spatial partitioning for collision
```

#### Branch Strategy
- `phase3` - Main development branch
- `phase3-foundation` - Structure setup
- `phase3-entities` - Entity extraction
- `phase3-systems` - Systems layer
- `phase3-rendering` - Graphics/UI
- `phase3-lgm` - Engineer system

---

## Milestones & Acceptance Criteria

### Milestone 1: Foundation Complete
**Deadline**: End of Week 1

Criteria:
- [ ] New directory structure created
- [ ] `config.py` with all dataclasses
- [ ] `enums.py` with all enums
- [ ] `base_entity.py` with abstract Entity
- [ ] `pyproject.toml` configured
- [ ] Game still runs with old `bolo_engine.py`

### Milestone 2: Entities Modularized
**Deadline**: End of Week 2

Criteria:
- [ ] Tank in `entities/tank.py`
- [ ] Shell and Mine in `entities/projectile.py`
- [ ] Pillbox and Base in `entities/structures.py`
- [ ] All entities have unit tests
- [ ] Game runs with new modules
- [ ] Can delete old `bolo_engine.py`

### Milestone 3: Systems Layer Complete
**Deadline**: End of Week 3

Criteria:
- [ ] Collision system with spatial partitioning
- [ ] Combat system extracted
- [ ] Resource system extracted
- [ ] AI system with proper state machine
- [ ] All systems have > 90% test coverage
- [ ] Performance maintains 60 FPS

### Milestone 4: World System Enhanced
**Deadline**: End of Week 4

Criteria:
- [ ] GameMap in separate module
- [ ] Camera system extracted
- [ ] Map loader working (CSV format)
- [ ] 3+ playable maps
- [ ] Forest regrowth implemented
- [ ] Map editor (bonus)

### Milestone 5: Graphics & UI Polish
**Deadline**: End of Week 5

Criteria:
- [ ] Sprite manager implemented
- [ ] Kenney sprites integrated
- [ ] Shape fallback maintained
- [ ] Rotation caching working
- [ ] UI system modularized
- [ ] Minimap implemented
- [ ] HUD improved

### Milestone 6: LGM System
**Deadline**: End of Week 6

Criteria:
- [ ] LGM entity functional
- [ ] Deployment from tank works
- [ ] Wood harvesting implemented
- [ ] Road building works
- [ ] Wall building works
- [ ] LGM respawn working
- [ ] Tests for LGM tasks

### Milestone 7: Release Ready
**Deadline**: End of Week 7

Criteria:
- [ ] Sound effects added (8+ sounds)
- [ ] All unit tests passing
- [ ] Performance profiled and optimized
- [ ] Documentation complete
- [ ] No critical bugs
- [ ] README updated
- [ ] CHANGELOG updated

---

## Risk Assessment

### Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Breaking existing functionality | High | Medium | Incremental refactor, keep old code temporarily |
| Performance regression | High | Low | Profile early, optimize, maintain benchmarks |
| Merge conflicts | Medium | Low | Small, frequent commits |
| Sprite loading issues | Medium | Medium | Maintain shape fallback |
| Test maintenance burden | Low | High | Focus on critical paths first |

### Schedule Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Scope creep | High | Medium | Strict milestone adherence |
| Underestimated complexity | Medium | High | Buffer time in estimates |
| Dependency issues | Low | Low | Pin versions in requirements.txt |

---

## Success Criteria

### Technical Success
✅ All Phase 2 features still work  
✅ Code is modular (< 300 lines per file)  
✅ > 80% unit test coverage  
✅ 60 FPS performance maintained  
✅ Type hints throughout (95%+)  
✅ Comprehensive documentation  

### Feature Success
✅ Sprite graphics working  
✅ Sound effects integrated  
✅ LGM system functional  
✅ Multiple maps loadable  
✅ Map editor (bonus)  
✅ AI improvements  

### Educational Success
✅ Code demonstrates professional patterns  
✅ Architecture is clear and teachable  
✅ Documentation explains design decisions  
✅ Tests serve as usage examples  

---

## Next Steps

### Immediate Actions (Today)

1. **Create Foundation Branch**
   ```bash
   git checkout -b phase3-foundation
   ```

2. **Create Directory Structure**
   ```bash
   mkdir -p src/{entities,systems,world,rendering}
   mkdir -p tests assets/{sprites,sounds,maps}
   touch src/config.py src/enums.py
   touch src/entities/__init__.py
   touch src/systems/__init__.py
   touch src/world/__init__.py
   touch src/rendering/__init__.py
   ```

3. **Create `pyproject.toml`**
   - Modern Python packaging
   - Project metadata
   - Dependencies

4. **Start `config.py`**
   - Extract all constants from `bolo_engine.py`
   - Create dataclass configs
   - Document all settings

5. **Start `enums.py`**
   - Extract all enums
   - Add comprehensive docstrings
   - Make type-safe

---

## Resources

### Documentation
- **Kilo Code Build Prompt** - This document's source
- **PHASE2_INTEGRATION.md** - Current state reference
- **docs/DEVELOPER_GUIDE.md** - Existing architecture docs

### Assets
- **Kenney Topdown Tanks** - https://kenney.nl/assets/topdown-tanks-redux
- **OpenGameArt Sounds** - https://opengameart.org/
- **FreeSound** - https://freesound.org/ (CC0 sounds)

### Reference Implementations
- **WinBolo** - https://github.com/kippandrew/winbolo
- **Orona** - https://github.com/stephank/orona

---

## Conclusion

Phase 3 is a **refactoring and enhancement** project, not a rewrite. We're taking a functional monolith and transforming it into a professional, modular codebase while adding new features.

**Key Principles**:
1. **Incremental** - Small, tested steps
2. **Backward Compatible** - Keep game working
3. **Test-Driven** - Write tests as we go
4. **Performance-Aware** - Profile and optimize
5. **Documentation-First** - Explain design decisions

**Timeline**: 7 weeks (flexible based on progress)

**End Goal**: A professional, extensible, well-tested BOLO recreation that serves as both an excellent game and an educational codebase for the Code the Dream community.

---

**Let's build this right!** 🎮🚀

