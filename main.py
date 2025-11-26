#!/usr/bin/env python3
"""
bring-back-BOLO: Main Entry Point
==================================
A faithful Python recreation of the classic BOLO tank warfare game.

This is the main entry point for the game. It imports the BoloGame
engine from the src package and launches the game.

Phase 2 Features:
- Tile-based terrain system with multiple terrain types
- Resource management (armor, shells, mines, wood)
- Bases with resupply and capture mechanics
- Pillboxes with auto-targeting and progressive fire rate
- Mine deployment
- Enemy AI with pursuit and combat
- Smooth camera following player

Controls:
- WASD or Arrow Keys: Move tank
- SPACE: Fire shell
- M: Place mine
- ESC: Pause game
- R: Restart

Author: Code the Dream / StrayDog Syndications
License: MIT
Date: November 2024
"""

from src.bolo_engine import BoloGame


def main() -> None:
    """
    Main entry point for bring-back-BOLO.
    
    Initializes and runs the game loop.
    """
    print("=" * 60)
    print("🎮 bring-back-BOLO - Phase 2: Strategic Features")
    print("=" * 60)
    print("\nStarting the game...")
    print("\nControls:")
    print("  WASD/Arrows - Move tank")
    print("  SPACE       - Fire shell")
    print("  M           - Place mine")
    print("  ESC         - Pause")
    print("  R           - Restart")
    print("\nObjective:")
    print("  - Capture neutral bases (diamond shapes)")
    print("  - Destroy enemy pillboxes (squares)")
    print("  - Resupply at friendly bases")
    print("  - Manage your resources wisely!")
    print("\n" + "=" * 60)
    
    # Create and run the game
    game = BoloGame()
    game.run()
    
    print("\nThanks for playing bring-back-BOLO! 🎮")


if __name__ == "__main__":
    main()
