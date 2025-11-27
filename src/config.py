"""
Game configuration constants.

All magic numbers live here for easy tuning. Uses frozen dataclasses
to prevent accidental modification at runtime.

Key Bindings:
-------------
Movement (continuous):
    W / UP_ARROW    : Move forward
    S / DOWN_ARROW  : Move backward
    A / LEFT_ARROW  : Rotate left
    D / RIGHT_ARROW : Rotate right

Actions (single press):
    SPACE : Fire shell
    M     : Place mine
    L     : Deploy LGM (Phase 3)

System (work anytime):
    ESC : Toggle pause
    R   : Restart game (works even when dead)
"""
from dataclasses import dataclass
from typing import Tuple

# Type aliases
Color = Tuple[int, int, int]


@dataclass(frozen=True)
class DisplayConfig:
    """
    Display and rendering settings.
    
    Controls window size, framerate, and tile dimensions.
    """
    WINDOW_WIDTH: int = 1024
    WINDOW_HEIGHT: int = 768
    FPS: int = 60
    TILE_SIZE: int = 16  # Original BOLO used 16x16 tiles
    TITLE: str = "bring-back-BOLO"
    
    # UI constants
    HUD_HEIGHT: int = 40
    MINIMAP_SIZE: int = 200


@dataclass(frozen=True)
class MapConfig:
    """
    Map dimensions and settings.
    
    Defines valid map sizes and generation parameters.
    """
    DEFAULT_WIDTH: int = 64   # Smaller than original 256x256 for dev
    DEFAULT_HEIGHT: int = 48
    MAX_WIDTH: int = 256      # Original BOLO map size
    MAX_HEIGHT: int = 256
    
    # Map generation
    BORDER_WALL_THICKNESS: int = 2
    FOREST_CLUSTER_SIZE: int = 8
    WATER_FEATURE_SIZE: int = 12


@dataclass(frozen=True)
class TankConfig:
    """
    Tank properties - tuned to match original BOLO feel.
    
    These values create authentic BOLO gameplay while
    maintaining balance and fun.
    """
    MAX_ARMOR: int = 8
    MAX_SHELLS: int = 40
    MAX_MINES: int = 40
    MAX_WOOD: int = 40
    
    BASE_SPEED: float = 2.0              # Pixels per frame
    ROTATION_SPEED: float = 4.0          # Degrees per frame
    SIZE: int = 12                       # Collision radius in pixels
    
    FIRE_COOLDOWN: int = 10              # Frames between shots
    MINE_PLACE_COOLDOWN: int = 30        # Frames between mine placements
    
    # Starting resources
    START_ARMOR: int = 8
    START_SHELLS: int = 40
    START_MINES: int = 10
    START_WOOD: int = 0


@dataclass(frozen=True)
class CombatConfig:
    """
    Combat mechanics and damage values.
    
    Tuned for strategic gameplay where positioning
    and resource management matter.
    """
    SHELL_DAMAGE: int = 1                # 8 hits to kill full armor tank
    SHELL_SPEED: float = 6.0             # Fast but dodge-able
    SHELL_LIFETIME: int = 90             # Frames before despawn
    SHELL_SIZE: int = 3                  # Collision radius
    
    MINE_DAMAGE: int = 4                 # Dangerous threat
    MINE_BLAST_RADIUS: float = 30.0      # Explosion radius
    MINE_SIZE: int = 4                   # Visual size
    
    PILLBOX_DAMAGE: int = 1              # Same as shell


@dataclass(frozen=True)
class StructureConfig:
    """
    Base and Pillbox settings.
    
    Controls resupply rates, capture mechanics, and
    pillbox behavior.
    """
    # Pillbox
    PILLBOX_MAX_HEALTH: int = 16
    PILLBOX_BASE_FIRE_RATE: int = 30     # Frames between shots when calm
    PILLBOX_MIN_FIRE_RATE: int = 5       # Frames between shots when angry
    PILLBOX_RANGE: float = 150.0         # Targeting range
    PILLBOX_SIZE: int = 10               # Collision radius
    PILLBOX_ANGER_DECAY: int = 60        # Frames to cool down
    
    # Base
    BASE_RESUPPLY_INTERVAL: int = 1200   # 20 seconds at 60 FPS
    BASE_SIZE: int = 15                  # Collision radius
    BASE_CAPTURE_RANGE: float = 30.0     # Distance to capture
    
    # Resupply amounts per tick
    RESUPPLY_ARMOR: int = 1
    RESUPPLY_SHELLS: int = 5
    RESUPPLY_MINES: int = 2
    RESUPPLY_WOOD: int = 0               # Bases don't give wood


@dataclass(frozen=True)
class LGMConfig:
    """
    Little Green Man (engineer) settings.
    
    The LGM is a vulnerable unit that performs construction
    and resource gathering tasks.
    """
    SPEED: float = 1.5                   # Slower than tank
    SIZE: int = 6                        # Small collision radius
    HEALTH: int = 1                      # Dies in one hit
    RESPAWN_TIME: int = 3600             # 60 seconds at 60 FPS
    
    # Building costs (in wood)
    ROAD_COST: int = 2
    WALL_COST: int = 2
    BOAT_COST: int = 5
    
    # Task durations (in frames)
    HARVEST_TIME: int = 120              # 2 seconds
    BUILD_TIME: int = 180                # 3 seconds
    MINE_DRILL_TIME: int = 240           # 4 seconds (hidden mine)
    
    # Harvest amounts
    WOOD_PER_TREE: int = 8               # Wood from one forest tile


@dataclass(frozen=True)
class AIConfig:
    """
    AI behavior tuning parameters.
    
    Controls enemy tank decision-making and aggression.
    """
    PATROL_CHANGE_INTERVAL: int = 120    # Frames between direction changes
    CHASE_RANGE: float = 200.0           # Start chasing at this distance
    ATTACK_RANGE: float = 150.0          # Start firing at this distance
    FLEE_HEALTH_THRESHOLD: int = 2       # Flee when armor this low
    FLEE_DURATION: int = 300             # Frames to flee before re-engaging
    
    # Accuracy (0.0 = perfect aim, higher = more error)
    AIM_ERROR: float = 0.1               # Radians of random aim offset
    
    # Targeting priority weights
    PRIORITY_PLAYER: float = 2.0
    PRIORITY_DAMAGED: float = 1.5
    PRIORITY_NEARBY: float = 1.2


# ============================================================================
# GLOBAL CONFIG INSTANCES
# ============================================================================
# Create singleton instances for easy import

DISPLAY = DisplayConfig()
MAP = MapConfig()
TANK = TankConfig()
COMBAT = CombatConfig()
STRUCTURE = StructureConfig()
LGM = LGMConfig()
AI = AIConfig()


# ============================================================================
# COLOR PALETTE
# ============================================================================

class Colors:
    """
    Game color palette.
    
    All colors used in the game, organized by purpose.
    Uses colors close to original BOLO for authenticity.
    """
    
    # Basic colors
    BLACK: Color = (0, 0, 0)
    WHITE: Color = (255, 255, 255)
    GRAY: Color = (128, 128, 128)
    DARK_GRAY: Color = (64, 64, 64)
    
    # Team colors (matches original BOLO palette)
    NEUTRAL: Color = (128, 128, 128)     # Gray
    TEAM_1: Color = (34, 139, 34)        # Forest Green (player default)
    TEAM_2: Color = (178, 34, 34)        # Firebrick Red (enemy)
    TEAM_3: Color = (65, 105, 225)       # Royal Blue (enemy)
    TEAM_4: Color = (218, 165, 32)       # Goldenrod Yellow (enemy)
    
    # Terrain colors (approximate original BOLO)
    DEEP_WATER: Color = (20, 60, 120)    # Dark blue
    RIVER: Color = (40, 100, 160)        # Medium blue
    SWAMP: Color = (60, 80, 40)          # Muddy brown-green
    CRATER: Color = (80, 70, 50)         # Dirt brown
    ROAD: Color = (60, 60, 60)           # Dark gray
    FOREST: Color = (20, 80, 20)         # Dark green
    RUBBLE: Color = (90, 85, 75)         # Light brown
    GRASS: Color = (50, 120, 50)         # Medium green
    WALL: Color = (100, 100, 100)        # Light gray
    DAMAGED_WALL: Color = (120, 110, 100)  # Slightly lighter
    BOAT: Color = (120, 80, 40)          # Brown
    
    # UI colors
    UI_BACKGROUND: Color = (30, 30, 30)
    UI_TEXT: Color = (255, 255, 255)
    UI_TEXT_DIM: Color = (180, 180, 180)
    UI_HEALTH_GOOD: Color = (34, 139, 34)
    UI_HEALTH_LOW: Color = (255, 165, 0)
    UI_HEALTH_CRITICAL: Color = (255, 0, 0)
    
    # Effect colors
    EXPLOSION: Color = (255, 128, 0)     # Orange
    MUZZLE_FLASH: Color = (255, 255, 0)  # Yellow
    DAMAGE_INDICATOR: Color = (255, 50, 50)  # Bright red


# ============================================================================
# TERRAIN PROPERTIES
# ============================================================================

@dataclass(frozen=True)
class TerrainInfo:
    """
    Properties for each terrain type.
    
    Defines how terrain affects gameplay mechanics like
    movement, combat, and building.
    """
    name: str
    speed_multiplier: float  # 0.0 = impassable, 1.0 = normal, >1.0 = faster
    passable: bool           # Can tank drive through?
    blocks_shots: bool       # Do shells stop here?
    destructible: bool       # Can terrain be damaged?
    color: Color             # Render color (if no sprite)
    
    # Forest regrowth
    regrows: bool = False
    regrow_time: int = 0     # Frames until regrowth
    
    # Resource harvesting
    provides_wood: bool = False
    wood_amount: int = 0


# Terrain lookup table - import from src.enums for TileType
from src.enums import TileType

TERRAIN: dict[TileType, TerrainInfo] = {
    TileType.DEEP_WATER: TerrainInfo(
        name="Deep Water",
        speed_multiplier=0.0,
        passable=False,
        blocks_shots=False,
        destructible=False,
        color=Colors.DEEP_WATER,
    ),
    TileType.RIVER: TerrainInfo(
        name="River",
        speed_multiplier=0.3,
        passable=True,
        blocks_shots=False,
        destructible=False,
        color=Colors.RIVER,
    ),
    TileType.SWAMP: TerrainInfo(
        name="Swamp",
        speed_multiplier=0.25,
        passable=True,
        blocks_shots=False,
        destructible=True,
        color=Colors.SWAMP,
    ),
    TileType.CRATER: TerrainInfo(
        name="Crater",
        speed_multiplier=0.5,
        passable=True,
        blocks_shots=False,
        destructible=False,
        color=Colors.CRATER,
    ),
    TileType.ROAD: TerrainInfo(
        name="Road",
        speed_multiplier=1.2,
        passable=True,
        blocks_shots=False,
        destructible=False,
        color=Colors.ROAD,
    ),
    TileType.FOREST: TerrainInfo(
        name="Forest",
        speed_multiplier=0.4,
        passable=True,
        blocks_shots=False,
        destructible=True,
        color=Colors.FOREST,
        regrows=True,
        regrow_time=18000,  # 5 minutes at 60 FPS
        provides_wood=True,
        wood_amount=LGM.WOOD_PER_TREE,
    ),
    TileType.RUBBLE: TerrainInfo(
        name="Rubble",
        speed_multiplier=0.6,
        passable=True,
        blocks_shots=False,
        destructible=False,
        color=Colors.RUBBLE,
    ),
    TileType.GRASS: TerrainInfo(
        name="Grass",
        speed_multiplier=0.8,
        passable=True,
        blocks_shots=False,
        destructible=False,
        color=Colors.GRASS,
    ),
    TileType.WALL: TerrainInfo(
        name="Wall",
        speed_multiplier=0.0,
        passable=False,
        blocks_shots=True,
        destructible=True,
        color=Colors.WALL,
    ),
    TileType.DAMAGED_WALL: TerrainInfo(
        name="Damaged Wall",
        speed_multiplier=0.0,
        passable=False,
        blocks_shots=True,
        destructible=True,
        color=Colors.DAMAGED_WALL,
    ),
    TileType.BOAT: TerrainInfo(
        name="Boat",
        speed_multiplier=0.8,
        passable=True,
        blocks_shots=False,
        destructible=True,
        color=Colors.BOAT,
    ),
}
