"""
Game enumerations for type safety and clarity.

This module defines all enum types used throughout the game,
providing type-safe constants and clear intent.
"""
from enum import IntEnum, auto


class TileType(IntEnum):
    """
    Terrain tile types matching original BOLO.
    
    Each tile type has different properties affecting
    movement speed, passability, and destructibility.
    """
    DEEP_WATER = 0    # Impassable without boat, kills tank
    RIVER = 1         # Slow movement, passable
    SWAMP = 2         # Very slow, destructible
    CRATER = 3        # Created by explosions, slow movement
    ROAD = 4          # Fastest movement (1.2x speed)
    FOREST = 5        # Slow, destructible, provides wood, regrows
    RUBBLE = 6        # Result of destroyed walls
    GRASS = 7         # Default terrain (0.8x speed)
    WALL = 8          # Impassable, blocks shots, destructible
    DAMAGED_WALL = 9  # Partially destroyed wall
    BOAT = 10         # Allows deep water crossing


class Team(IntEnum):
    """
    Player/structure team affiliations.
    
    Teams determine friendly fire, capture mechanics,
    and visual color coding.
    """
    NEUTRAL = 0   # Gray - Can be captured by anyone
    TEAM_1 = 1    # Green - Player's default team
    TEAM_2 = 2    # Red - Primary enemy
    TEAM_3 = 3    # Blue - Secondary enemy
    TEAM_4 = 4    # Yellow - Tertiary enemy


class GamePhase(IntEnum):
    """
    Game state machine phases.
    
    Controls high-level game flow and input handling.
    """
    MENU = auto()       # Main menu, settings, map selection
    PLAYING = auto()    # Active gameplay
    PAUSED = auto()     # Game paused (ESC)
    GAME_OVER = auto()  # Player defeated


class EntityType(IntEnum):
    """
    Entity classification for collision layers.
    
    Used for efficient collision detection via
    spatial partitioning and layer filtering.
    """
    TANK = auto()
    SHELL = auto()
    MINE = auto()
    PILLBOX = auto()
    BASE = auto()
    LGM = auto()       # Little Green Man (engineer)


class AIState(IntEnum):
    """
    AI behavior states for enemy tanks.
    
    State machine controls enemy tank decision-making.
    """
    IDLE = auto()      # Waiting, no targets
    PATROL = auto()    # Random movement
    CHASE = auto()     # Moving toward enemy
    ATTACK = auto()    # Firing at target
    FLEE = auto()      # Low health retreat
    CAPTURE = auto()   # Moving to capture objective


class LGMTask(IntEnum):
    """
    LGM (engineer) task types.
    
    Defines what action the deployed engineer is performing.
    """
    IDLE = auto()          # No current task
    HARVEST = auto()       # Getting wood from forest
    BUILD_ROAD = auto()    # Constructing road tile
    BUILD_WALL = auto()    # Constructing wall tile
    BUILD_BOAT = auto()    # Building boat for deep water
    PLACE_MINE = auto()    # Placing visible mine
    DRILL_MINE = auto()    # Placing hidden mine
    CAPTURE_PILL = auto()  # Capturing pillbox
    PLACE_PILL = auto()    # Deploying pillbox
