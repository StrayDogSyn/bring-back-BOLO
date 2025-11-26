# Developer Guide - bring-back-BOLO

## Architecture Overview

bring-back-BOLO Phase 2 uses a clean, object-oriented architecture inspired by Entity-Component-System (ECS) patterns, making the codebase maintainable and extensible.

## Code Structure

```
bring-back-BOLO/
├── main.py                    # Entry point - launches game
├── src/                       # Source package
│   ├── __init__.py           # Package exports
│   └── bolo_engine.py        # Core game engine (1182 lines)
├── lesson/                    # Educational materials
│   └── tank_game.py          # Phase 1 simple version
├── phase2/                    # Phase 2 reference
│   ├── bolo_engine.py        # Original Phase 2 code
│   └── README.md             # Phase 2 documentation
└── docs/                      # Documentation
    ├── BOLO_RESEARCH.md      # Original game research
    └── DEVELOPER_GUIDE.md    # This file
```

## bolo_engine.py Sections

The engine is organized into 5 clear sections:

### Section 1: Constants & Configuration (Lines 1-143)
- `Config` class: All game tuning parameters
- `TileType` enum: Terrain types
- `TerrainInfo` dataclass: Terrain properties
- `TERRAIN_DATA` dict: Terrain lookup table
- `Team` enum: Team system
- `TEAM_COLORS` dict: Visual team identification

### Section 2: Entity System (Lines 144-674)
Base classes and game objects:
- `Entity` (abstract base): All game objects inherit from this
- `Resources` dataclass: Tank resource container
- `Tank`: Player and AI-controlled tanks
- `Shell`: Projectiles fired by tanks/pillboxes
- `Mine`: Explosive mines
- `Pillbox`: Auto-targeting turrets
- `Base`: Resupply and capture points

### Section 3: Map System (Lines 675-813)
- `GameMap`: Tile-based terrain management
  - Efficient rendering with cached surfaces
  - Terrain modification (damage, build)
  - Random map generation

### Section 4: Game State (Lines 814-956)
- `GameState`: Central coordinator
  - Entity lifecycle management
  - Collision detection
  - Camera control
  - Game rules enforcement

### Section 5: Main Game Class (Lines 957-1182)
- `BoloGame`: Main controller
  - Initialization
  - Game loop (input → update → render)
  - Event handling
  - UI rendering

## Key Design Patterns

### 1. Entity-Component Pattern
All game objects inherit from `Entity` base class:
```python
class Entity(ABC):
    def __init__(self, x: float, y: float)
    @abstractmethod
    def update(self, game_state: GameState) -> None
    @abstractmethod
    def draw(self, surface: pygame.Surface, camera_offset: Position) -> None
```

Benefits:
- Uniform interface for game loop
- Easy to add new entity types
- Clean separation of concerns

### 2. Dataclasses for Configuration
```python
@dataclass
class TerrainInfo:
    name: str
    speed_multiplier: float
    passable: bool
    blocks_shots: bool
    destructible: bool
    color: Color
```

Benefits:
- Immutable configuration
- Type safety
- Self-documenting

### 3. Centralized Game State
```python
class GameState:
    def __init__(self):
        self.game_map: GameMap
        self.entities: List[Entity]
        self.player: Optional[Tank]
        # ... etc
```

Benefits:
- Single source of truth
- Easy to serialize (for save games)
- Clear data flow

## Adding New Features

### Adding a New Entity Type

1. **Create the class** inheriting from `Entity`:
```python
class NewEntity(Entity):
    def __init__(self, x: float, y: float, team: Team) -> None:
        super().__init__(x, y)
        self.team = team
        # ... custom attributes
    
    def update(self, game_state: GameState) -> None:
        # Your logic here
        pass
    
    def draw(self, surface: pygame.Surface, camera_offset: Position) -> None:
        # Rendering code
        pass
```

2. **Add to GameState** spawn logic in `_setup_game()` or dynamically

3. **Handle collisions** in `GameState._process_collisions()`

### Adding a New Terrain Type

1. **Add to TileType enum**:
```python
class TileType(IntEnum):
    # ... existing types
    NEW_TERRAIN = 11
```

2. **Add terrain data**:
```python
TERRAIN_DATA[TileType.NEW_TERRAIN] = TerrainInfo(
    name="New Terrain",
    speed_multiplier=0.7,
    passable=True,
    blocks_shots=False,
    destructible=True,
    color=(R, G, B)
)
```

3. **Update map generation** if needed

### Adding a New Resource Type

1. **Update Resources dataclass**:
```python
@dataclass
class Resources:
    armor: int = Config.TANK_MAX_ARMOR
    shells: int = Config.TANK_MAX_SHELLS
    mines: int = Config.TANK_MAX_MINES
    wood: int = 0
    new_resource: int = 0  # Add here
```

2. **Update UI rendering** in `BoloGame._render_ui()`

3. **Update base resupply** logic if needed

## Performance Optimization

### Current Optimizations
1. **Cached terrain surface** - Only rebuilds when map changes
2. **Viewport culling** - Only renders visible tiles
3. **Entity pooling** - Reuses shell/mine objects (future)

### Profiling Tips
```python
import cProfile
cProfile.run('game.run()', 'output.prof')
```

Analyze with:
```bash
python -m pstats output.prof
```

## Testing Strategy

### Unit Tests (Future)
```python
def test_tank_movement():
    tank = Tank(100, 100, Team.TEAM_1)
    initial_x = tank.x
    tank.move_forward(mock_game_state)
    assert tank.x != initial_x
```

### Integration Tests
- Map generation produces valid terrain
- Collision detection works correctly
- Resource management enforces limits

## Common Tasks

### Adjusting Game Balance
Edit `Config` class values:
```python
class Config:
    TANK_BASE_SPEED: float = 2.0  # Slower = 1.5, Faster = 3.0
    SHELL_DAMAGE: int = 1          # More damage = 2
    PILLBOX_FIRE_RATE: int = 30    # Faster fire = 20
```

### Changing Map Size
```python
class Config:
    MAP_WIDTH: int = 64   # Tiles
    MAP_HEIGHT: int = 48
```

### Adding Debug Visualization
In `BoloGame._render()`:
```python
# Show collision boxes
for entity in self.game_state.entities:
    if isinstance(entity, Tank):
        pygame.draw.circle(screen, (255, 0, 0), 
                         (entity.x, entity.y), entity.size, 1)
```

## Best Practices

1. **Type Hints**: Always use type hints for parameters and returns
2. **Docstrings**: Document all public methods
3. **Constants**: Use Config class, not magic numbers
4. **Enums**: Use enums for discrete states (TileType, Team)
5. **Immutability**: Prefer dataclasses for read-only data
6. **Separation**: Keep rendering separate from logic

## Debugging Tips

### Visual Debugging
```python
# In Tank.draw()
# Show facing direction
pygame.draw.line(surface, (255, 0, 0), 
                (screen_x, screen_y), 
                (end_x, end_y), 2)

# Show tile position
font = pygame.font.Font(None, 12)
text = font.render(f"{self.tile_position}", True, (255, 255, 255))
surface.blit(text, (screen_x - 20, screen_y - 30))
```

### Console Logging
```python
# In GameState.update()
if frame_count % 60 == 0:  # Every second
    print(f"Entities: {len(self.entities)}, Player Armor: {self.player.resources.armor}")
```

## Contributing

When contributing code:
1. Follow existing code style
2. Add type hints
3. Write docstrings
4. Test manually
5. Update CHANGELOG.md

## Resources

- [Pygame Documentation](https://www.pygame.org/docs/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Original BOLO Research](BOLO_RESEARCH.md)
- [WinBolo Source](https://github.com/kippandrew/winbolo)

---

**Questions?** Open an issue or check the README.md

**Happy tanking!** 🎮
