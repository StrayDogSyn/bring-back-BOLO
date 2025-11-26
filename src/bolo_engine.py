"""
bring-back-BOLO: Core Game Engine
==================================
A faithful Python recreation of the classic BOLO tank warfare game.

This module implements the core game engine, including:
- Tile-based map system with terrain types
- Entity management (tanks, bullets, pillboxes, bases)
- Resource management (shells, mines, armor, wood)
- Collision detection and damage systems
- Game loop with proper timing

Architecture follows a component-entity-system inspired pattern
for maintainability and extensibility.

Author: Code the Dream / StrayDog Syndications
License: MIT
"""

from __future__ import annotations

import math
import random
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import IntEnum, auto
from typing import Dict, List, Optional, Tuple, Protocol, Set
import pygame

# Type aliases for clarity
Position = Tuple[float, float]
TileCoord = Tuple[int, int]
Color = Tuple[int, int, int]


# =============================================================================
# SECTION 1: CONSTANTS & CONFIGURATION
# =============================================================================

class Config:
    """
    Game configuration - centralized settings for easy tuning.
    
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
    
    System (work anytime):
        ESC : Toggle pause
        R   : Restart game (works even when dead)
    """
    
    # Display
    WINDOW_WIDTH: int = 1024
    WINDOW_HEIGHT: int = 768
    FPS: int = 60
    TILE_SIZE: int = 16  # Original BOLO used 16x16 tiles
    
    # Map
    MAP_WIDTH: int = 64   # Tiles (smaller than original 256x256 for dev)
    MAP_HEIGHT: int = 48
    
    # Tank properties (tuned to match original BOLO feel)
    TANK_MAX_ARMOR: int = 8
    TANK_MAX_SHELLS: int = 40
    TANK_MAX_MINES: int = 40
    TANK_MAX_WOOD: int = 40
    TANK_BASE_SPEED: float = 2.0
    TANK_ROTATION_SPEED: float = 4.0  # Degrees per frame
    TANK_SIZE: int = 12  # Radius in pixels
    
    # Combat
    SHELL_DAMAGE: int = 1
    SHELL_SPEED: float = 6.0
    SHELL_LIFETIME: int = 90  # Frames until despawn
    MINE_DAMAGE: int = 4
    
    # Structures
    PILLBOX_MAX_HEALTH: int = 16
    PILLBOX_FIRE_RATE: int = 30  # Frames between shots (base rate)
    PILLBOX_RANGE: float = 150.0
    BASE_RESUPPLY_RATE: int = 1200  # Frames between resupply ticks (20 sec)
    
    # LGM
    LGM_SPEED: float = 1.5
    LGM_RESPAWN_TIME: int = 3600  # 60 seconds at 60 FPS
    
    # Building costs
    ROAD_COST: int = 2
    WALL_COST: int = 2
    BOAT_COST: int = 5


class TileType(IntEnum):
    """Terrain tile types matching original BOLO."""
    DEEP_WATER = 0    # Drowns tanks, needs boat
    RIVER = 1         # Shallow water, slow
    SWAMP = 2         # Very slow, destructible
    CRATER = 3        # Created by explosions
    ROAD = 4          # Fastest movement
    FOREST = 5        # Slow, provides wood
    RUBBLE = 6        # Destroyed building
    GRASS = 7         # Default terrain
    WALL = 8          # Blocks movement and shots
    DAMAGED_WALL = 9  # Half-destroyed wall
    BOAT = 10         # Moored boat


@dataclass
class TerrainInfo:
    """Properties for each terrain type."""
    name: str
    speed_multiplier: float  # 1.0 = normal, 0.5 = half speed, 0 = impassable
    passable: bool
    blocks_shots: bool
    destructible: bool
    color: Color


# Terrain lookup table
TERRAIN_DATA: Dict[TileType, TerrainInfo] = {
    TileType.DEEP_WATER: TerrainInfo("Deep Water", 0.0, False, False, False, (20, 60, 120)),
    TileType.RIVER: TerrainInfo("River", 0.3, True, False, False, (40, 100, 160)),
    TileType.SWAMP: TerrainInfo("Swamp", 0.25, True, False, True, (60, 80, 40)),
    TileType.CRATER: TerrainInfo("Crater", 0.5, True, False, False, (80, 70, 50)),
    TileType.ROAD: TerrainInfo("Road", 1.2, True, False, False, (60, 60, 60)),
    TileType.FOREST: TerrainInfo("Forest", 0.4, True, False, True, (20, 80, 20)),
    TileType.RUBBLE: TerrainInfo("Rubble", 0.6, True, False, False, (90, 85, 75)),
    TileType.GRASS: TerrainInfo("Grass", 0.8, True, False, False, (50, 120, 50)),
    TileType.WALL: TerrainInfo("Wall", 0.0, False, True, True, (100, 100, 100)),
    TileType.DAMAGED_WALL: TerrainInfo("Damaged Wall", 0.0, False, True, True, (120, 110, 100)),
    TileType.BOAT: TerrainInfo("Boat", 0.8, True, False, True, (120, 80, 40)),
}


class Team(IntEnum):
    """Player/structure team affiliations."""
    NEUTRAL = 0
    TEAM_1 = 1
    TEAM_2 = 2
    TEAM_3 = 3
    TEAM_4 = 4


# Team colors for rendering
TEAM_COLORS: Dict[Team, Color] = {
    Team.NEUTRAL: (128, 128, 128),
    Team.TEAM_1: (34, 139, 34),   # Forest Green
    Team.TEAM_2: (178, 34, 34),   # Firebrick Red
    Team.TEAM_3: (65, 105, 225),  # Royal Blue
    Team.TEAM_4: (218, 165, 32),  # Goldenrod
}


# =============================================================================
# SECTION 2: ENTITY SYSTEM
# =============================================================================

class Entity(ABC):
    """
    Base class for all game entities.
    
    Entities are objects in the game world with position, lifecycle,
    and optional rendering. This provides a common interface for
    the game loop to process all objects uniformly.
    """
    
    _next_id: int = 0
    
    def __init__(self, x: float, y: float) -> None:
        self.id: int = Entity._next_id
        Entity._next_id += 1
        self.x: float = x
        self.y: float = y
        self.alive: bool = True
    
    @property
    def position(self) -> Position:
        return (self.x, self.y)
    
    @property
    def tile_position(self) -> TileCoord:
        """Get the tile coordinates this entity occupies."""
        return (int(self.x // Config.TILE_SIZE), int(self.y // Config.TILE_SIZE))
    
    @abstractmethod
    def update(self, game_state: "GameState") -> None:
        """Update entity state for this frame."""
        pass
    
    @abstractmethod
    def draw(self, surface: pygame.Surface, camera_offset: Position) -> None:
        """Render the entity to the given surface."""
        pass
    
    def destroy(self) -> None:
        """Mark entity for removal."""
        self.alive = False


@dataclass
class Resources:
    """Container for tank resources."""
    armor: int = Config.TANK_MAX_ARMOR
    shells: int = Config.TANK_MAX_SHELLS
    mines: int = Config.TANK_MAX_MINES
    wood: int = 0


class Tank(Entity):
    """
    Player-controlled tank entity.
    
    The tank is the primary player unit with movement, combat,
    and resource management capabilities.
    """
    
    def __init__(self, x: float, y: float, team: Team) -> None:
        super().__init__(x, y)
        self.team: Team = team
        self.angle: float = 0.0  # Facing direction in degrees
        self.resources: Resources = Resources()
        self.speed: float = Config.TANK_BASE_SPEED
        self.size: int = Config.TANK_SIZE
        
        # State flags
        self.is_moving: bool = False
        self.has_boat: bool = False
        
        # LGM state
        self.lgm_deployed: bool = False
        self.lgm_position: Optional[Position] = None
        self.lgm_respawn_timer: int = 0
        
        # Carried items
        self.carried_pillboxes: List["Pillbox"] = []
        
        # Firing cooldown
        self.fire_cooldown: int = 0
        self.fire_rate: int = 10  # Frames between shots
    
    def update(self, game_state: "GameState") -> None:
        """Process tank logic for this frame."""
        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1
        
        if self.lgm_respawn_timer > 0:
            self.lgm_respawn_timer -= 1
            if self.lgm_respawn_timer == 0:
                self.lgm_deployed = False
    
    def move_forward(self, game_state: "GameState") -> None:
        """Move tank forward in facing direction."""
        terrain_speed = self._get_terrain_speed(game_state)
        if terrain_speed <= 0:
            return
        
        dx = math.cos(math.radians(self.angle)) * self.speed * terrain_speed
        dy = math.sin(math.radians(self.angle)) * self.speed * terrain_speed
        
        new_x = self.x + dx
        new_y = self.y + dy
        
        if self._can_move_to(new_x, new_y, game_state):
            self.x = new_x
            self.y = new_y
            self.is_moving = True
    
    def move_backward(self, game_state: "GameState") -> None:
        """Move tank backward."""
        terrain_speed = self._get_terrain_speed(game_state)
        if terrain_speed <= 0:
            return
        
        dx = math.cos(math.radians(self.angle)) * self.speed * terrain_speed * 0.6
        dy = math.sin(math.radians(self.angle)) * self.speed * terrain_speed * 0.6
        
        new_x = self.x - dx
        new_y = self.y - dy
        
        if self._can_move_to(new_x, new_y, game_state):
            self.x = new_x
            self.y = new_y
            self.is_moving = True
    
    def rotate_left(self) -> None:
        """Rotate tank counter-clockwise."""
        self.angle = (self.angle - Config.TANK_ROTATION_SPEED) % 360
    
    def rotate_right(self) -> None:
        """Rotate tank clockwise."""
        self.angle = (self.angle + Config.TANK_ROTATION_SPEED) % 360
    
    def fire(self, game_state: "GameState") -> Optional["Shell"]:
        """Fire a shell if able. Returns the shell entity or None."""
        if self.fire_cooldown > 0 or self.resources.shells <= 0:
            return None
        
        self.resources.shells -= 1
        self.fire_cooldown = self.fire_rate
        
        # Spawn shell at cannon tip
        cannon_length = self.size + 8
        shell_x = self.x + math.cos(math.radians(self.angle)) * cannon_length
        shell_y = self.y + math.sin(math.radians(self.angle)) * cannon_length
        
        return Shell(shell_x, shell_y, self.angle, self.team, self.id)
    
    def place_mine(self, game_state: "GameState") -> Optional["Mine"]:
        """Drop a mine at current position if able."""
        if self.resources.mines <= 0:
            return None
        
        self.resources.mines -= 1
        return Mine(self.x, self.y, self.team)
    
    def take_damage(self, amount: int) -> None:
        """Apply damage to the tank."""
        self.resources.armor -= amount
        if self.resources.armor <= 0:
            self.destroy()
    
    def resupply(self, base: "Base") -> None:
        """Resupply from a friendly base."""
        self.resources.armor = min(Config.TANK_MAX_ARMOR, self.resources.armor + 1)
        self.resources.shells = min(Config.TANK_MAX_SHELLS, self.resources.shells + 5)
        self.resources.mines = min(Config.TANK_MAX_MINES, self.resources.mines + 2)
    
    def _get_terrain_speed(self, game_state: "GameState") -> float:
        """Get movement speed multiplier for current terrain."""
        tile = game_state.game_map.get_tile(*self.tile_position)
        terrain = TERRAIN_DATA.get(tile, TERRAIN_DATA[TileType.GRASS])
        
        # Check for boat on water
        if tile in (TileType.DEEP_WATER, TileType.RIVER) and not self.has_boat:
            if tile == TileType.DEEP_WATER:
                return 0.0  # Would drown
        
        return terrain.speed_multiplier
    
    def _can_move_to(self, x: float, y: float, game_state: "GameState") -> bool:
        """Check if tank can move to position."""
        # Bounds check
        if x < self.size or x > game_state.game_map.pixel_width - self.size:
            return False
        if y < self.size or y > game_state.game_map.pixel_height - self.size:
            return False
        
        # Terrain check
        tile_x = int(x // Config.TILE_SIZE)
        tile_y = int(y // Config.TILE_SIZE)
        tile = game_state.game_map.get_tile(tile_x, tile_y)
        terrain = TERRAIN_DATA.get(tile, TERRAIN_DATA[TileType.GRASS])
        
        if not terrain.passable:
            # Special case: boat allows water passage
            if tile == TileType.DEEP_WATER and self.has_boat:
                return True
            return False
        
        return True
    
    def draw(self, surface: pygame.Surface, camera_offset: Position) -> None:
        """Render the tank."""
        screen_x = int(self.x - camera_offset[0])
        screen_y = int(self.y - camera_offset[1])
        
        color = TEAM_COLORS.get(self.team, (100, 100, 100))
        
        # Tank body
        pygame.draw.circle(surface, color, (screen_x, screen_y), self.size)
        
        # Tank outline
        pygame.draw.circle(surface, (40, 40, 40), (screen_x, screen_y), self.size, 2)
        
        # Cannon
        cannon_length = self.size + 10
        end_x = screen_x + math.cos(math.radians(self.angle)) * cannon_length
        end_y = screen_y + math.sin(math.radians(self.angle)) * cannon_length
        pygame.draw.line(surface, (200, 200, 200), (screen_x, screen_y), 
                        (int(end_x), int(end_y)), 4)
        pygame.draw.line(surface, (60, 60, 60), (screen_x, screen_y), 
                        (int(end_x), int(end_y)), 2)


class Shell(Entity):
    """
    Projectile fired by tanks and pillboxes.
    
    Shells travel in a straight line and deal damage on impact.
    """
    
    def __init__(self, x: float, y: float, angle: float, 
                 team: Team, owner_id: int) -> None:
        super().__init__(x, y)
        self.angle: float = angle
        self.team: Team = team
        self.owner_id: int = owner_id
        self.speed: float = Config.SHELL_SPEED
        self.damage: int = Config.SHELL_DAMAGE
        self.lifetime: int = Config.SHELL_LIFETIME
        self.radius: int = 3
    
    def update(self, game_state: "GameState") -> None:
        """Move shell and check for impacts."""
        # Move
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
        
        # Lifetime
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.destroy()
            return
        
        # Terrain collision
        tile = game_state.game_map.get_tile(*self.tile_position)
        terrain = TERRAIN_DATA.get(tile, TERRAIN_DATA[TileType.GRASS])
        if terrain.blocks_shots:
            # Damage destructible terrain
            if terrain.destructible:
                game_state.game_map.damage_tile(*self.tile_position)
            self.destroy()
            return
        
        # Bounds check
        if (self.x < 0 or self.x > game_state.game_map.pixel_width or
            self.y < 0 or self.y > game_state.game_map.pixel_height):
            self.destroy()
    
    def draw(self, surface: pygame.Surface, camera_offset: Position) -> None:
        """Render the shell."""
        screen_x = int(self.x - camera_offset[0])
        screen_y = int(self.y - camera_offset[1])
        
        pygame.draw.circle(surface, (255, 200, 50), (screen_x, screen_y), self.radius)
        pygame.draw.circle(surface, (255, 255, 200), (screen_x, screen_y), 
                          self.radius - 1)


class Mine(Entity):
    """
    Explosive mine that detonates on contact.
    
    Mines can be visible (dropped) or hidden (drilled by LGM).
    """
    
    def __init__(self, x: float, y: float, team: Team, hidden: bool = False) -> None:
        super().__init__(x, y)
        self.team: Team = team
        self.hidden: bool = hidden
        self.damage: int = Config.MINE_DAMAGE
        self.radius: int = 6
        self.detection_radius: int = 4  # Distance at which hidden mines become visible
    
    def update(self, game_state: "GameState") -> None:
        """Check for detonation triggers."""
        pass  # Collision handled by game state
    
    def detonate(self, game_state: "GameState") -> None:
        """Explode the mine, affecting nearby entities and terrain."""
        # Create crater in terrain
        game_state.game_map.set_tile(*self.tile_position, TileType.CRATER)
        self.destroy()
    
    def draw(self, surface: pygame.Surface, camera_offset: Position) -> None:
        """Render the mine (if visible)."""
        if self.hidden:
            return  # Don't draw hidden mines (except to owner team)
        
        screen_x = int(self.x - camera_offset[0])
        screen_y = int(self.y - camera_offset[1])
        
        pygame.draw.circle(surface, (60, 60, 60), (screen_x, screen_y), self.radius)
        pygame.draw.circle(surface, (40, 40, 40), (screen_x, screen_y), 
                          self.radius - 2)


class Pillbox(Entity):
    """
    Automated defensive turret.
    
    Pillboxes auto-fire at enemies within range. They can be
    captured, picked up by an LGM, and repositioned.
    """
    
    def __init__(self, x: float, y: float, team: Team = Team.NEUTRAL) -> None:
        super().__init__(x, y)
        self.team: Team = team
        self.health: int = Config.PILLBOX_MAX_HEALTH
        self.fire_rate: int = Config.PILLBOX_FIRE_RATE
        self.fire_cooldown: int = 0
        self.range: float = Config.PILLBOX_RANGE
        self.size: int = 8
        self.active: bool = True  # False when picked up
        
        # Progressive fire rate (increases when attacked)
        self.aggression: int = 0
    
    def update(self, game_state: "GameState") -> None:
        """Process pillbox AI."""
        if not self.active:
            return
        
        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1
        
        # Decay aggression over time
        if self.aggression > 0 and random.random() < 0.01:
            self.aggression = max(0, self.aggression - 1)
        
        # Find and engage targets
        if self.fire_cooldown <= 0:
            target = self._find_target(game_state)
            if target:
                shell = self._fire_at(target)
                if shell:
                    game_state.add_entity(shell)
    
    def _find_target(self, game_state: "GameState") -> Optional[Tank]:
        """Find nearest enemy tank in range."""
        best_target: Optional[Tank] = None
        best_distance: float = float('inf')
        
        for entity in game_state.entities:
            if isinstance(entity, Tank) and entity.team != self.team:
                dist = math.sqrt((entity.x - self.x)**2 + (entity.y - self.y)**2)
                if dist < self.range and dist < best_distance:
                    best_target = entity
                    best_distance = dist
        
        return best_target
    
    def _fire_at(self, target: Tank) -> Optional[Shell]:
        """Fire at target tank."""
        angle = math.degrees(math.atan2(target.y - self.y, target.x - self.x))
        
        # Adjusted fire rate based on aggression
        adjusted_rate = max(5, self.fire_rate - self.aggression * 3)
        self.fire_cooldown = adjusted_rate
        
        return Shell(self.x, self.y, angle, self.team, self.id)
    
    def take_damage(self, amount: int) -> None:
        """Apply damage and increase aggression."""
        self.health -= amount
        self.aggression = min(8, self.aggression + 1)  # Get angrier when shot
        
        if self.health <= 0:
            self.team = Team.NEUTRAL
            self.health = 0
            self.active = False
    
    def capture(self, new_team: Team) -> None:
        """Capture the pillbox for a new team."""
        self.team = new_team
        self.health = Config.PILLBOX_MAX_HEALTH // 2
        self.active = True
        self.aggression = 0
    
    def draw(self, surface: pygame.Surface, camera_offset: Position) -> None:
        """Render the pillbox."""
        if not self.active:
            return
        
        screen_x = int(self.x - camera_offset[0])
        screen_y = int(self.y - camera_offset[1])
        
        color = TEAM_COLORS.get(self.team, (100, 100, 100))
        
        # Square pillbox body
        rect = pygame.Rect(screen_x - self.size, screen_y - self.size,
                          self.size * 2, self.size * 2)
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, (40, 40, 40), rect, 2)
        
        # Health indicator (inner square)
        health_ratio = self.health / Config.PILLBOX_MAX_HEALTH
        inner_size = int(self.size * health_ratio)
        if inner_size > 0:
            inner_rect = pygame.Rect(screen_x - inner_size, screen_y - inner_size,
                                    inner_size * 2, inner_size * 2)
            pygame.draw.rect(surface, (200, 200, 200), inner_rect)


class Base(Entity):
    """
    Refueling and resupply station.
    
    Bases provide shells, mines, and armor repair. They slowly
    regenerate supplies and can be captured by enemy tanks.
    """
    
    def __init__(self, x: float, y: float, team: Team = Team.NEUTRAL) -> None:
        super().__init__(x, y)
        self.team: Team = team
        self.health: int = 16
        self.size: int = 16
        
        # Stock levels
        self.shells: int = 20
        self.mines: int = 10
        self.armor: int = 8
        
        # Regeneration timer
        self.regen_timer: int = Config.BASE_RESUPPLY_RATE
    
    def update(self, game_state: "GameState") -> None:
        """Regenerate supplies over time."""
        self.regen_timer -= 1
        if self.regen_timer <= 0:
            self.regen_timer = Config.BASE_RESUPPLY_RATE
            
            # Regenerate supplies
            self.shells = min(40, self.shells + 1)
            self.mines = min(20, self.mines + 1)
            self.armor = min(16, self.armor + 1)
    
    def resupply_tank(self, tank: Tank) -> bool:
        """Attempt to resupply a friendly tank. Returns True if any resupply occurred."""
        if tank.team != self.team:
            return False
        
        resupplied = False
        
        # Armor first (most important)
        if tank.resources.armor < Config.TANK_MAX_ARMOR and self.armor > 0:
            transfer = min(1, self.armor, Config.TANK_MAX_ARMOR - tank.resources.armor)
            tank.resources.armor += transfer
            self.armor -= transfer
            resupplied = True
        
        # Then shells
        if tank.resources.shells < Config.TANK_MAX_SHELLS and self.shells > 0:
            transfer = min(5, self.shells, Config.TANK_MAX_SHELLS - tank.resources.shells)
            tank.resources.shells += transfer
            self.shells -= transfer
            resupplied = True
        
        # Then mines
        if tank.resources.mines < Config.TANK_MAX_MINES and self.mines > 0:
            transfer = min(2, self.mines, Config.TANK_MAX_MINES - tank.resources.mines)
            tank.resources.mines += transfer
            self.mines -= transfer
            resupplied = True
        
        return resupplied
    
    def take_damage(self, amount: int) -> None:
        """Apply damage to base."""
        self.health -= amount
        if self.health <= 0:
            self.team = Team.NEUTRAL
            self.health = 1
    
    def capture(self, new_team: Team) -> None:
        """Capture the base for a new team."""
        self.team = new_team
        self.health = 8
    
    def draw(self, surface: pygame.Surface, camera_offset: Position) -> None:
        """Render the base."""
        screen_x = int(self.x - camera_offset[0])
        screen_y = int(self.y - camera_offset[1])
        
        color = TEAM_COLORS.get(self.team, (100, 100, 100))
        
        # Diamond shape for base
        points = [
            (screen_x, screen_y - self.size),
            (screen_x + self.size, screen_y),
            (screen_x, screen_y + self.size),
            (screen_x - self.size, screen_y),
        ]
        pygame.draw.polygon(surface, color, points)
        pygame.draw.polygon(surface, (40, 40, 40), points, 2)
        
        # Supply indicator in center
        supply_level = (self.shells + self.mines + self.armor) / 68  # Max total
        indicator_size = int(self.size * 0.5 * supply_level)
        if indicator_size > 0:
            pygame.draw.circle(surface, (200, 200, 200), 
                             (screen_x, screen_y), indicator_size)


# =============================================================================
# SECTION 3: MAP SYSTEM
# =============================================================================

class GameMap:
    """
    Tile-based game map with terrain management.
    
    The map is a 2D grid of tiles, each with terrain properties
    that affect movement, combat, and construction.
    """
    
    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.tiles: List[List[TileType]] = [
            [TileType.GRASS for _ in range(width)] 
            for _ in range(height)
        ]
        
        # Cached terrain surface for efficient rendering
        self._terrain_surface: Optional[pygame.Surface] = None
        self._dirty: bool = True
    
    @property
    def pixel_width(self) -> int:
        return self.width * Config.TILE_SIZE
    
    @property
    def pixel_height(self) -> int:
        return self.height * Config.TILE_SIZE
    
    def get_tile(self, x: int, y: int) -> TileType:
        """Get tile type at grid coordinates."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return TileType.WALL  # Out of bounds treated as wall
    
    def set_tile(self, x: int, y: int, tile_type: TileType) -> None:
        """Set tile type at grid coordinates."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[y][x] = tile_type
            self._dirty = True
    
    def damage_tile(self, x: int, y: int) -> None:
        """Apply damage to a tile (for destructible terrain)."""
        tile = self.get_tile(x, y)
        
        if tile == TileType.WALL:
            self.set_tile(x, y, TileType.DAMAGED_WALL)
        elif tile == TileType.DAMAGED_WALL:
            self.set_tile(x, y, TileType.RUBBLE)
        elif tile == TileType.FOREST:
            self.set_tile(x, y, TileType.GRASS)
        elif tile == TileType.SWAMP:
            self.set_tile(x, y, TileType.CRATER)
    
    def generate_random(self) -> None:
        """Generate a random map for testing."""
        for y in range(self.height):
            for x in range(self.width):
                # Border walls
                if x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1:
                    self.tiles[y][x] = TileType.WALL
                else:
                    # Random terrain
                    r = random.random()
                    if r < 0.05:
                        self.tiles[y][x] = TileType.FOREST
                    elif r < 0.08:
                        self.tiles[y][x] = TileType.RIVER
                    elif r < 0.10:
                        self.tiles[y][x] = TileType.SWAMP
                    elif r < 0.12:
                        self.tiles[y][x] = TileType.WALL
                    else:
                        self.tiles[y][x] = TileType.GRASS
        
        # Add some roads
        mid_y = self.height // 2
        for x in range(5, self.width - 5):
            self.tiles[mid_y][x] = TileType.ROAD
        
        mid_x = self.width // 2
        for y in range(5, self.height - 5):
            self.tiles[y][mid_x] = TileType.ROAD
        
        self._dirty = True
    
    def render(self, surface: pygame.Surface, camera_offset: Position, 
               viewport_size: Tuple[int, int]) -> None:
        """Render visible portion of map to surface."""
        # Rebuild cached surface if dirty
        if self._dirty or self._terrain_surface is None:
            self._rebuild_terrain_surface()
        
        # Calculate visible tile range
        start_x = max(0, int(camera_offset[0] // Config.TILE_SIZE))
        start_y = max(0, int(camera_offset[1] // Config.TILE_SIZE))
        end_x = min(self.width, start_x + viewport_size[0] // Config.TILE_SIZE + 2)
        end_y = min(self.height, start_y + viewport_size[1] // Config.TILE_SIZE + 2)
        
        # Calculate source rect on terrain surface
        src_x = int(camera_offset[0])
        src_y = int(camera_offset[1])
        src_rect = pygame.Rect(src_x, src_y, viewport_size[0], viewport_size[1])
        
        # Blit visible portion
        surface.blit(self._terrain_surface, (0, 0), src_rect)
    
    def _rebuild_terrain_surface(self) -> None:
        """Rebuild the cached terrain surface."""
        self._terrain_surface = pygame.Surface(
            (self.pixel_width, self.pixel_height)
        )
        
        for y in range(self.height):
            for x in range(self.width):
                tile = self.tiles[y][x]
                terrain = TERRAIN_DATA.get(tile, TERRAIN_DATA[TileType.GRASS])
                
                rect = pygame.Rect(
                    x * Config.TILE_SIZE,
                    y * Config.TILE_SIZE,
                    Config.TILE_SIZE,
                    Config.TILE_SIZE
                )
                pygame.draw.rect(self._terrain_surface, terrain.color, rect)
                
                # Add subtle grid lines
                pygame.draw.rect(self._terrain_surface, 
                               (terrain.color[0] - 10, 
                                terrain.color[1] - 10, 
                                terrain.color[2] - 10), 
                               rect, 1)
        
        self._dirty = False


# =============================================================================
# SECTION 4: GAME STATE
# =============================================================================

class GameState:
    """
    Central game state manager.
    
    Coordinates all game systems including entities, map,
    physics, and game rules.
    """
    
    def __init__(self) -> None:
        self.game_map: GameMap = GameMap(Config.MAP_WIDTH, Config.MAP_HEIGHT)
        self.entities: List[Entity] = []
        self.pending_entities: List[Entity] = []  # Added during update loop
        
        # Player reference
        self.player: Optional[Tank] = None
        
        # Camera
        self.camera_x: float = 0.0
        self.camera_y: float = 0.0
        
        # Game state
        self.paused: bool = False
        self.game_over: bool = False
        self.score: int = 0
    
    def add_entity(self, entity: Entity) -> None:
        """Add an entity to be spawned next frame."""
        self.pending_entities.append(entity)
    
    def remove_dead_entities(self) -> None:
        """Clean up destroyed entities."""
        self.entities = [e for e in self.entities if e.alive]
    
    def update(self) -> None:
        """Process one frame of game logic."""
        if self.paused or self.game_over:
            return
        
        # Add pending entities
        self.entities.extend(self.pending_entities)
        self.pending_entities.clear()
        
        # Update all entities
        for entity in self.entities:
            entity.update(self)
        
        # Process collisions
        self._process_collisions()
        
        # Clean up dead entities
        self.remove_dead_entities()
        
        # Update camera to follow player
        if self.player and self.player.alive:
            self._update_camera()
    
    def _process_collisions(self) -> None:
        """Handle entity collisions."""
        # Shell vs Tank
        for entity in self.entities:
            if isinstance(entity, Shell) and entity.alive:
                for other in self.entities:
                    if isinstance(other, Tank) and other.alive:
                        if other.id == entity.owner_id:
                            continue  # Can't shoot yourself
                        if other.team == entity.team:
                            continue  # Team damage off (configurable)
                        
                        dist = math.sqrt((entity.x - other.x)**2 + 
                                        (entity.y - other.y)**2)
                        if dist < other.size + entity.radius:
                            other.take_damage(entity.damage)
                            entity.destroy()
                            break
        
        # Shell vs Pillbox
        for entity in self.entities:
            if isinstance(entity, Shell) and entity.alive:
                for other in self.entities:
                    if isinstance(other, Pillbox) and other.alive and other.active:
                        if other.team == entity.team:
                            continue
                        
                        dist = math.sqrt((entity.x - other.x)**2 + 
                                        (entity.y - other.y)**2)
                        if dist < other.size + entity.radius:
                            other.take_damage(entity.damage)
                            entity.destroy()
                            break
        
        # Tank vs Mine
        for entity in self.entities:
            if isinstance(entity, Mine) and entity.alive:
                for other in self.entities:
                    if isinstance(other, Tank) and other.alive:
                        if other.team == entity.team:
                            continue
                        
                        dist = math.sqrt((entity.x - other.x)**2 + 
                                        (entity.y - other.y)**2)
                        if dist < other.size + entity.radius:
                            other.take_damage(entity.damage)
                            entity.detonate(self)
                            break
        
        # Tank vs Base (for resupply/capture)
        for entity in self.entities:
            if isinstance(entity, Tank) and entity.alive:
                for other in self.entities:
                    if isinstance(other, Base):
                        dist = math.sqrt((entity.x - other.x)**2 + 
                                        (entity.y - other.y)**2)
                        if dist < entity.size + other.size:
                            if other.team == entity.team:
                                other.resupply_tank(entity)
                            elif other.team == Team.NEUTRAL:
                                other.capture(entity.team)
    
    def _update_camera(self) -> None:
        """Center camera on player."""
        if self.player:
            target_x = self.player.x - Config.WINDOW_WIDTH // 2
            target_y = self.player.y - Config.WINDOW_HEIGHT // 2
            
            # Smooth camera movement
            self.camera_x += (target_x - self.camera_x) * 0.1
            self.camera_y += (target_y - self.camera_y) * 0.1
            
            # Clamp to map bounds
            self.camera_x = max(0, min(self.game_map.pixel_width - Config.WINDOW_WIDTH, 
                                      self.camera_x))
            self.camera_y = max(0, min(self.game_map.pixel_height - Config.WINDOW_HEIGHT, 
                                      self.camera_y))
    
    @property
    def camera_offset(self) -> Position:
        return (self.camera_x, self.camera_y)


# =============================================================================
# SECTION 5: MAIN GAME CLASS
# =============================================================================

class BoloGame:
    """
    Main game controller.
    
    Handles initialization, the main game loop, input processing,
    and rendering coordination.
    """
    
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("bring-back-BOLO")
        
        self.screen: pygame.Surface = pygame.display.set_mode(
            (Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)
        )
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.running: bool = True
        
        self.game_state: GameState = GameState()
        self.font: pygame.font.Font = pygame.font.Font(None, 24)
        
        self._setup_game()
    
    def _setup_game(self) -> None:
        """Initialize game objects for a new game."""
        # Generate map
        self.game_state.game_map.generate_random()
        
        # Spawn player
        player = Tank(
            Config.MAP_WIDTH * Config.TILE_SIZE // 4,
            Config.MAP_HEIGHT * Config.TILE_SIZE // 2,
            Team.TEAM_1
        )
        self.game_state.player = player
        self.game_state.entities.append(player)
        
        # Spawn some enemies
        for i in range(3):
            enemy = Tank(
                Config.MAP_WIDTH * Config.TILE_SIZE * 3 // 4,
                Config.MAP_HEIGHT * Config.TILE_SIZE // 4 + i * 100,
                Team.TEAM_2
            )
            enemy.angle = 180  # Face left
            self.game_state.entities.append(enemy)
        
        # Spawn bases
        base1 = Base(200, 200, Team.TEAM_1)
        base2 = Base(Config.MAP_WIDTH * Config.TILE_SIZE - 200, 200, Team.TEAM_2)
        base_neutral = Base(Config.MAP_WIDTH * Config.TILE_SIZE // 2, 
                           Config.MAP_HEIGHT * Config.TILE_SIZE // 2)
        self.game_state.entities.extend([base1, base2, base_neutral])
        
        # Spawn pillboxes
        for i in range(4):
            pill = Pillbox(
                150 + i * 200,
                Config.MAP_HEIGHT * Config.TILE_SIZE - 150,
                Team.NEUTRAL
            )
            self.game_state.entities.append(pill)
    
    def run(self) -> None:
        """Main game loop."""
        while self.running:
            self._handle_events()
            self._update()
            self._render()
            self.clock.tick(Config.FPS)
        
        pygame.quit()
    
    def _handle_events(self) -> None:
        """Process input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)
    
    def _handle_keydown(self, key: int) -> None:
        """
        Handle single key press events.
        
        Some keys (ESC, R) should work regardless of player state,
        while others (SPACE, M) require an alive player.
        """
        # Global keys - work regardless of player state
        if key == pygame.K_ESCAPE:
            self.game_state.paused = not self.game_state.paused
            return
        elif key == pygame.K_r:
            # Restart game - works even when player is dead
            self.game_state = GameState()
            self._setup_game()
            return
        
        # Player-specific keys - require alive player
        player = self.game_state.player
        if not player or not player.alive:
            return
        
        if key == pygame.K_SPACE:
            shell = player.fire(self.game_state)
            if shell:
                self.game_state.add_entity(shell)
        elif key == pygame.K_m:
            mine = player.place_mine(self.game_state)
            if mine:
                self.game_state.add_entity(mine)
    
    def _update(self) -> None:
        """Update game state."""
        if self.game_state.paused:
            return
        
        player = self.game_state.player
        if player and player.alive:
            # Continuous key input
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player.move_forward(self.game_state)
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player.move_backward(self.game_state)
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player.rotate_left()
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player.rotate_right()
        
        # Simple enemy AI
        for entity in self.game_state.entities:
            if isinstance(entity, Tank) and entity.team == Team.TEAM_2:
                self._simple_enemy_ai(entity)
        
        self.game_state.update()
    
    def _simple_enemy_ai(self, enemy: Tank) -> None:
        """Basic enemy behavior for testing."""
        player = self.game_state.player
        if not player or not player.alive:
            return
        
        # Calculate angle to player
        dx = player.x - enemy.x
        dy = player.y - enemy.y
        target_angle = math.degrees(math.atan2(dy, dx))
        
        # Rotate towards player
        angle_diff = (target_angle - enemy.angle + 180) % 360 - 180
        if abs(angle_diff) > 5:
            if angle_diff > 0:
                enemy.rotate_right()
            else:
                enemy.rotate_left()
        
        # Move and shoot if facing player
        dist = math.sqrt(dx*dx + dy*dy)
        if abs(angle_diff) < 30:
            if dist > 150:
                enemy.move_forward(self.game_state)
            if dist < 300 and random.random() < 0.03:
                shell = enemy.fire(self.game_state)
                if shell:
                    self.game_state.add_entity(shell)
    
    def _render(self) -> None:
        """Render the game."""
        # Clear screen
        self.screen.fill((0, 0, 0))
        
        # Render map
        self.game_state.game_map.render(
            self.screen, 
            self.game_state.camera_offset,
            (Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)
        )
        
        # Render entities (sorted by type for proper layering)
        for entity in sorted(self.game_state.entities, 
                           key=lambda e: (isinstance(e, Tank), isinstance(e, Shell))):
            entity.draw(self.screen, self.game_state.camera_offset)
        
        # Render UI
        self._render_ui()
        
        pygame.display.flip()
    
    def _render_ui(self) -> None:
        """Render heads-up display."""
        player = self.game_state.player
        if not player:
            return
        
        # Resource display (only show if player is alive)
        if player.alive:
            ui_text = (
                f"Armor: {player.resources.armor}/{Config.TANK_MAX_ARMOR}  "
                f"Shells: {player.resources.shells}/{Config.TANK_MAX_SHELLS}  "
                f"Mines: {player.resources.mines}/{Config.TANK_MAX_MINES}  "
                f"Wood: {player.resources.wood}/{Config.TANK_MAX_WOOD}"
            )
            text_surface = self.font.render(ui_text, True, (255, 255, 255))
            self.screen.blit(text_surface, (10, 10))
        
        # Controls hint
        controls = "WASD: Move | SPACE: Fire | M: Mine | ESC: Pause | R: Restart"
        controls_surface = self.font.render(controls, True, (200, 200, 200))
        self.screen.blit(controls_surface, (10, Config.WINDOW_HEIGHT - 30))
        
        # Game Over overlay (when player is dead)
        if not player.alive:
            # Semi-transparent overlay
            overlay = pygame.Surface((Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            # Game Over text
            game_over_font = pygame.font.Font(None, 72)
            game_over_text = game_over_font.render("GAME OVER", True, (255, 50, 50))
            game_over_rect = game_over_text.get_rect(
                center=(Config.WINDOW_WIDTH // 2, Config.WINDOW_HEIGHT // 2 - 40)
            )
            self.screen.blit(game_over_text, game_over_rect)
            
            # Restart instruction
            restart_text = self.font.render("Press R to Restart", True, (255, 255, 255))
            restart_rect = restart_text.get_rect(
                center=(Config.WINDOW_WIDTH // 2, Config.WINDOW_HEIGHT // 2 + 20)
            )
            self.screen.blit(restart_text, restart_rect)
        
        # Pause overlay (when game is paused and player is alive)
        elif self.game_state.paused:
            pause_text = self.font.render("PAUSED - Press ESC to Continue", True, (255, 255, 0))
            pause_rect = pause_text.get_rect(
                center=(Config.WINDOW_WIDTH // 2, Config.WINDOW_HEIGHT // 2)
            )
            self.screen.blit(pause_text, pause_rect)


# =============================================================================
# ENTRY POINT
# =============================================================================

def main() -> None:
    """Entry point for the game."""
    game = BoloGame()
    game.run()


if __name__ == "__main__":
    main()
