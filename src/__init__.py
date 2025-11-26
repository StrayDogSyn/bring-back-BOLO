"""
bring-back-BOLO: Source Package
================================
Core game engine and utilities for the BOLO tank warfare game.

Author: Code the Dream / StrayDog Syndications
License: MIT
"""

__version__ = "0.2.0"  # Phase 2: Strategic Features
__author__ = "Code the Dream / StrayDog Syndications"

from .bolo_engine import (
    BoloGame,
    GameState,
    Tank,
    Shell,
    Mine,
    Pillbox,
    Base,
    Config,
    Team,
    TileType,
)

__all__ = [
    "BoloGame",
    "GameState",
    "Tank",
    "Shell",
    "Mine",
    "Pillbox",
    "Base",
    "Config",
    "Team",
    "TileType",
]
