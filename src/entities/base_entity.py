"""
Abstract base class for all game entities.

This module defines the Entity base class that all game objects
(tanks, shells, mines, pillboxes, bases, LGM) inherit from.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Tuple
import math

import pygame

if TYPE_CHECKING:
    from src.game import GameState

# Type aliases
Position = Tuple[float, float]
TileCoord = Tuple[int, int]


@dataclass
class Entity(ABC):
    """
    Base class for all game entities.
    
    Uses dataclass for clean initialization while maintaining
    abstract method requirements. All game objects (tanks, shells,
    structures, etc.) inherit from this class.
    
    Attributes:
        x: World X coordinate in pixels
        y: World Y coordinate in pixels
        alive: Whether entity is active (False triggers removal)
        
    The _id field is automatically generated and provides unique
    identification for each entity instance.
    """
    x: float
    y: float
    _id: int = field(default_factory=lambda: Entity._generate_id(), init=False)
    alive: bool = field(default=True, init=False)
    
    # Class variable for ID generation
    _next_id: int = 0
    
    @classmethod
    def _generate_id(cls) -> int:
        """
        Generate unique entity ID.
        
        Returns:
            Monotonically increasing integer ID.
        """
        current = cls._next_id
        cls._next_id += 1
        return current
    
    @classmethod
    def reset_id_counter(cls) -> None:
        """Reset ID counter (useful for testing)."""
        cls._next_id = 0
    
    @property
    def id(self) -> int:
        """Unique entity identifier."""
        return self._id
    
    @property
    def position(self) -> Position:
        """
        Current world position as tuple.
        
        Returns:
            (x, y) tuple of current position.
        """
        return (self.x, self.y)
    
    @property
    def tile_position(self) -> TileCoord:
        """
        Grid coordinates of current tile.
        
        Converts world pixel coordinates to tile grid coordinates
        by dividing by TILE_SIZE.
        
        Returns:
            (tile_x, tile_y) tuple of grid coordinates.
        """
        from src.config import DISPLAY
        return (
            int(self.x // DISPLAY.TILE_SIZE),
            int(self.y // DISPLAY.TILE_SIZE)
        )
    
    @abstractmethod
    def update(self, game_state: GameState, dt: float) -> None:
        """
        Update entity state.
        
        Called once per frame to update entity logic, movement,
        timers, etc. Subclasses must implement this method.
        
        Args:
            game_state: Current game state for context (map, other entities, etc.)
            dt: Delta time in seconds (for framerate independence).
                 At 60 FPS, dt ≈ 0.0167 seconds.
        """
        pass
    
    @abstractmethod
    def draw(self, surface: pygame.Surface, camera_offset: Position) -> None:
        """
        Render entity to surface.
        
        Called once per frame to draw the entity. The camera_offset
        should be subtracted from entity position to get screen coordinates.
        
        Args:
            surface: Pygame surface to draw on (usually the main screen).
            camera_offset: Current camera position (cam_x, cam_y) for scrolling.
        """
        pass
    
    def destroy(self) -> None:
        """
        Mark entity for removal.
        
        Sets alive=False, which triggers removal from the game state
        at the end of the current update cycle.
        """
        self.alive = False
    
    def distance_to(self, other: Entity | Position) -> float:
        """
        Calculate distance to another entity or position.
        
        Uses Pythagorean theorem: distance = sqrt((x2-x1)² + (y2-y1)²)
        
        Args:
            other: Another Entity or a (x, y) position tuple.
        
        Returns:
            Distance in pixels.
        """
        if isinstance(other, Entity):
            other_x, other_y = other.x, other.y
        else:
            other_x, other_y = other
        
        return math.sqrt((self.x - other_x)**2 + (self.y - other_y)**2)
    
    def angle_to(self, other: Entity | Position) -> float:
        """
        Calculate angle from this entity to another entity or position.
        
        Uses arctangent2 to get direction in degrees.
        0° = East, 90° = South, 180° = West, 270° = North (standard screen coordinates).
        
        Args:
            other: Another Entity or a (x, y) position tuple.
        
        Returns:
            Angle in degrees (0-360).
        """
        if isinstance(other, Entity):
            other_x, other_y = other.x, other.y
        else:
            other_x, other_y = other
        
        dx = other_x - self.x
        dy = other_y - self.y
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)
        
        # Normalize to 0-360
        return angle_deg % 360
    
    def move_towards(self, target: Position, speed: float) -> None:
        """
        Move entity towards a target position at given speed.
        
        Useful for AI movement and homing projectiles.
        
        Args:
            target: Target (x, y) position.
            speed: Movement speed in pixels per frame.
        """
        angle = self.angle_to(target)
        angle_rad = math.radians(angle)
        
        self.x += math.cos(angle_rad) * speed
        self.y += math.sin(angle_rad) * speed
    
    def is_on_screen(self, camera_offset: Position, screen_size: Tuple[int, int], margin: int = 50) -> bool:
        """
        Check if entity is visible on screen.
        
        Useful for culling off-screen entities from rendering.
        Adds a margin to account for entity size.
        
        Args:
            camera_offset: Current camera (x, y) position.
            screen_size: Screen (width, height) in pixels.
            margin: Extra pixels around screen edge to consider visible.
        
        Returns:
            True if entity should be rendered.
        """
        cam_x, cam_y = camera_offset
        screen_w, screen_h = screen_size
        
        screen_x = self.x - cam_x
        screen_y = self.y - cam_y
        
        return (
            -margin <= screen_x <= screen_w + margin and
            -margin <= screen_y <= screen_h + margin
        )
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"{self.__class__.__name__}(id={self.id}, pos=({self.x:.1f}, {self.y:.1f}), alive={self.alive})"
    
    def __eq__(self, other: object) -> bool:
        """Equality based on entity ID."""
        if not isinstance(other, Entity):
            return NotImplemented
        return self.id == other.id
    
    def __hash__(self) -> int:
        """Hash based on entity ID (allows use in sets/dicts)."""
        return hash(self.id)
