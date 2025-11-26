"""
Tank Battle - A Simple 2D Shooter
=================================
Demonstrates Python fundamentals through game development.
Built for Code the Dream Python Essentials - Pre-Thanksgiving Edition!

Concepts covered:
- Variables and constants (game configuration)
- Functions (collision detection, drawing)
- Classes (Tank, Bullet, Enemy, Obstacle)
- Loops (game loop, iterating through lists)
- Conditionals (input handling, collision checks)
- Lists (managing multiple game objects)
- Type Hints (self-documenting code)

Controls:
- WASD or Arrow Keys: Move tank
- SPACE: Fire bullet
- R: Restart (when game over)

Author: Code the Dream Python Essentials
Date: November 2024
"""

# ============================================================
# SECTION 1: IMPORTS
# ============================================================
# We import libraries at the top - like gathering ingredients
# before cooking. Each library serves a specific purpose:
#   - pygame: Game engine for graphics, sound, and input
#   - math: Trigonometry for angles and movement
#   - random: Randomness for enemy behavior
#   - typing: Type hints for better code documentation

import pygame
import math
import random
from typing import List, Tuple

# Initialize pygame - this "wakes up" the game engine
# Think of it like preheating your oven before cooking
pygame.init()


# ============================================================
# SECTION 2: CONSTANTS (Configuration)
# ============================================================
# Constants are variables that DON'T change during the game.
# By convention, we write them in ALL_CAPS.
# This makes our code easy to tweak - want a bigger window?
# Just change these numbers!

# Window settings
WINDOW_WIDTH: int = 800   # Game window width in pixels
WINDOW_HEIGHT: int = 600  # Game window height in pixels
FPS: int = 60             # Frames per second (game speed)

# Colors are tuples of (Red, Green, Blue) - each value 0-255
# It's like mixing paint on a palette!
BLACK: Tuple[int, int, int] = (0, 0, 0)
WHITE: Tuple[int, int, int] = (255, 255, 255)
GREEN: Tuple[int, int, int] = (34, 139, 34)      # Forest green for player
RED: Tuple[int, int, int] = (178, 34, 34)        # Firebrick red for enemies
GRAY: Tuple[int, int, int] = (128, 128, 128)     # Gray for obstacles
YELLOW: Tuple[int, int, int] = (255, 215, 0)     # Gold for bullets

# Game balance settings - easy to adjust for difficulty
PLAYER_SPEED: int = 4           # How fast player moves (pixels per frame)
PLAYER_ROTATION_SPEED: int = 5  # How fast player turns (degrees per frame)
BULLET_SPEED: int = 8           # How fast bullets travel
ENEMY_SPEED: int = 2            # Enemy movement speed


# ============================================================
# SECTION 3: CREATE THE GAME WINDOW
# ============================================================
# This creates the actual window you'll see on screen.
# set_caption gives it a title in the title bar.

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tank Battle - Code the Dream")

# The clock helps us control game speed
# Without this, the game would run as fast as your CPU allows!
clock = pygame.time.Clock()


# ============================================================
# SECTION 4: GAME CLASSES
# ============================================================
# Classes are blueprints for game objects.
# Think of a class like a cookie cutter - it defines the shape,
# but you can make many cookies (instances) from it.


class Tank:
    """
    The player's tank.
    
    A tank has position, direction, and can move and shoot.
    This demonstrates object-oriented programming (OOP) basics:
    - Attributes store data (x, y, angle)
    - Methods define behavior (move, rotate, shoot)
    
    Attributes:
        x, y: Position on screen (center of tank)
        angle: Direction tank is facing (in degrees, 0 = right)
        speed: How fast the tank moves
        rotation_speed: How fast the tank turns
        size: Radius of the tank (it's drawn as a circle)
        color: RGB tuple for tank color
    """
    
    def __init__(self, x: int, y: int, color: Tuple[int, int, int]) -> None:
        """
        Initialize a new tank.
        
        The __init__ method is called automatically when we create
        a new Tank object. It's like the "birth" of the tank.
        
        Args:
            x: Starting x position (horizontal)
            y: Starting y position (vertical)
            color: Tank color as RGB tuple
        """
        # Position - where is the tank on the screen?
        self.x: float = x
        self.y: float = y
        
        # Direction - which way is it facing?
        # 0 degrees = right, 90 = down, 180 = left, 270 = up
        self.angle: float = 0
        
        # Movement properties
        self.speed: int = PLAYER_SPEED
        self.rotation_speed: int = PLAYER_ROTATION_SPEED
        
        # Appearance properties
        self.size: int = 20  # Radius in pixels
        self.color: Tuple[int, int, int] = color
    
    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the tank on the given surface.
        
        We draw two shapes:
        1. A circle for the tank body
        2. A line for the cannon (shows which way we're aiming)
        
        Args:
            surface: The pygame surface to draw on (usually the screen)
        """
        # Draw tank body as a circle
        pygame.draw.circle(
            surface,                           # Where to draw
            self.color,                        # What color
            (int(self.x), int(self.y)),       # Position (must be integers!)
            self.size                          # Radius
        )
        
        # Draw cannon - a line pointing in the direction we're facing
        # We use trigonometry to find the endpoint of the line:
        #   cos(angle) gives the x component
        #   sin(angle) gives the y component
        # math.radians() converts degrees to radians (what trig functions expect)
        cannon_length: int = self.size + 15
        end_x: float = self.x + math.cos(math.radians(self.angle)) * cannon_length
        end_y: float = self.y + math.sin(math.radians(self.angle)) * cannon_length
        
        pygame.draw.line(
            surface,
            WHITE,
            (int(self.x), int(self.y)),       # Start at tank center
            (int(end_x), int(end_y)),         # End at calculated point
            4                                  # Line thickness in pixels
        )
    
    def move_forward(self) -> None:
        """
        Move tank forward in the direction it's facing.
        
        Uses trigonometry: if we're facing at angle θ,
        moving forward means adding cos(θ) to x and sin(θ) to y.
        """
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
        self._keep_on_screen()  # Don't let tank escape!
    
    def move_backward(self) -> None:
        """
        Move tank backward (opposite of facing direction).
        
        Same math as forward, but we subtract instead of add.
        """
        self.x -= math.cos(math.radians(self.angle)) * self.speed
        self.y -= math.sin(math.radians(self.angle)) * self.speed
        self._keep_on_screen()
    
    def rotate_left(self) -> None:
        """Rotate tank counter-clockwise (decreasing angle)."""
        self.angle -= self.rotation_speed
    
    def rotate_right(self) -> None:
        """Rotate tank clockwise (increasing angle)."""
        self.angle += self.rotation_speed
    
    def shoot(self) -> "Bullet":
        """
        Fire a bullet from the cannon.
        
        The bullet starts at the end of the cannon and travels
        in the direction the tank is facing.
        
        Returns:
            A new Bullet object traveling in tank's facing direction.
        """
        # Calculate bullet starting position (at end of cannon)
        cannon_length: int = self.size + 15
        start_x: float = self.x + math.cos(math.radians(self.angle)) * cannon_length
        start_y: float = self.y + math.sin(math.radians(self.angle)) * cannon_length
        return Bullet(start_x, start_y, self.angle)
    
    def _keep_on_screen(self) -> None:
        """
        Keep tank within window bounds.
        
        This is a 'private' helper method - the underscore prefix is
        a Python convention meaning "this is for internal use only."
        
        We clamp x and y to stay within the window, accounting for
        the tank's size so it doesn't stick halfway off-screen.
        """
        # max() ensures we're not less than the minimum
        # min() ensures we're not more than the maximum
        self.x = max(self.size, min(WINDOW_WIDTH - self.size, self.x))
        self.y = max(self.size, min(WINDOW_HEIGHT - self.size, self.y))


class Bullet:
    """
    A bullet fired by a tank.
    
    Bullets travel in a straight line at constant speed until
    they hit something or leave the screen.
    
    Attributes:
        x, y: Current position
        angle: Direction of travel (in degrees)
        speed: How fast it moves
        radius: Size for collision detection
        color: RGB tuple for bullet color
    """
    
    def __init__(self, x: float, y: float, angle: float) -> None:
        """
        Create a bullet at position, traveling in direction of angle.
        
        Args:
            x: Starting x position
            y: Starting y position
            angle: Direction of travel in degrees
        """
        self.x: float = x
        self.y: float = y
        self.angle: float = angle
        self.speed: int = BULLET_SPEED
        self.radius: int = 5
        self.color: Tuple[int, int, int] = YELLOW
    
    def update(self) -> None:
        """
        Move bullet forward each frame.
        
        Called once per game loop iteration to advance the bullet.
        """
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the bullet as a small circle."""
        pygame.draw.circle(
            surface,
            self.color,
            (int(self.x), int(self.y)),
            self.radius
        )
    
    def is_off_screen(self) -> bool:
        """
        Check if bullet has left the play area.
        
        Returns:
            True if bullet is outside window bounds, False otherwise.
        """
        return (self.x < 0 or 
                self.x > WINDOW_WIDTH or
                self.y < 0 or 
                self.y > WINDOW_HEIGHT)


class Obstacle:
    """
    A wall/barrier that blocks movement and bullets.
    
    Obstacles are simple rectangles that don't move.
    They provide cover and make the game more strategic.
    
    Attributes:
        rect: Pygame Rect object storing position and dimensions
        color: RGB tuple for obstacle color
    """
    
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        """
        Create obstacle with position and dimensions.
        
        Args:
            x: Left edge x position
            y: Top edge y position
            width: Width in pixels
            height: Height in pixels
        """
        # pygame.Rect is a convenient class for rectangle operations
        # It provides built-in collision detection and positioning
        self.rect = pygame.Rect(x, y, width, height)
        self.color: Tuple[int, int, int] = GRAY
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the obstacle as a filled rectangle."""
        pygame.draw.rect(surface, self.color, self.rect)


class Enemy:
    """
    An enemy tank with simple AI behavior.
    
    Enemies patrol the arena in random directions and can be
    destroyed by the player's bullets. They will hurt the player
    on contact.
    
    Attributes:
        x, y: Current position
        size: Radius for collision detection and drawing
        color: RGB tuple for enemy color
        speed: Movement speed
        direction: Current facing/movement direction in degrees
        move_timer: Frames until next direction change
    """
    
    def __init__(self, x: int, y: int) -> None:
        """
        Create enemy at the specified position.
        
        Args:
            x: Starting x position
            y: Starting y position
        """
        self.x: float = x
        self.y: float = y
        self.size: int = 18
        self.color: Tuple[int, int, int] = RED
        self.speed: int = ENEMY_SPEED
        
        # AI behavior: start facing a random cardinal direction
        # random.choice picks one item from a list
        self.direction: int = random.choice([0, 90, 180, 270])
        
        # Timer counts frames until we pick a new direction
        self.move_timer: int = 0
    
    def update(self) -> None:
        """
        Move enemy with simple patrol AI.
        
        Behavior:
        - Move in current direction
        - Periodically change to a new random direction
        - Bounce off walls
        """
        # Increment timer and maybe change direction
        self.move_timer += 1
        if self.move_timer > random.randint(60, 120):  # Every 1-2 seconds
            self.direction = random.choice([0, 90, 180, 270])
            self.move_timer = 0
        
        # Move in current direction
        self.x += math.cos(math.radians(self.direction)) * self.speed
        self.y += math.sin(math.radians(self.direction)) * self.speed
        
        # Bounce off walls (simple reflection)
        if self.x < self.size or self.x > WINDOW_WIDTH - self.size:
            self.direction = 180 - self.direction  # Reverse horizontal
            self.x = max(self.size, min(WINDOW_WIDTH - self.size, self.x))
        
        if self.y < self.size or self.y > WINDOW_HEIGHT - self.size:
            self.direction = -self.direction  # Reverse vertical
            self.y = max(self.size, min(WINDOW_HEIGHT - self.size, self.y))
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw enemy tank with direction indicator."""
        # Body
        pygame.draw.circle(
            surface,
            self.color,
            (int(self.x), int(self.y)),
            self.size
        )
        
        # Direction indicator (smaller cannon than player)
        end_x: float = self.x + math.cos(math.radians(self.direction)) * (self.size + 8)
        end_y: float = self.y + math.sin(math.radians(self.direction)) * (self.size + 8)
        pygame.draw.line(
            surface,
            WHITE,
            (int(self.x), int(self.y)),
            (int(end_x), int(end_y)),
            3
        )


# ============================================================
# SECTION 5: HELPER FUNCTIONS
# ============================================================
# Functions that perform specific tasks.
# These keep our main game loop clean and make code reusable.


def check_circle_collision(x1: float, y1: float, r1: int,
                           x2: float, y2: float, r2: int) -> bool:
    """
    Check if two circles are overlapping.
    
    This is the Pythagorean theorem in action!
    Distance between centers = sqrt((x2-x1)² + (y2-y1)²)
    If distance < sum of radii, circles overlap.
    
    Args:
        x1, y1, r1: First circle's center position and radius
        x2, y2, r2: Second circle's center position and radius
    
    Returns:
        True if circles overlap, False otherwise.
    """
    distance: float = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance < (r1 + r2)


def check_circle_rect_collision(cx: float, cy: float, radius: int,
                                rect: pygame.Rect) -> bool:
    """
    Check if a circle overlaps with a rectangle.
    
    Algorithm:
    1. Find the point on the rectangle closest to the circle's center
    2. Check if that point is inside the circle
    
    Args:
        cx, cy: Circle center position
        radius: Circle radius
        rect: Pygame Rect object
    
    Returns:
        True if circle and rectangle overlap, False otherwise.
    """
    # Find closest point on rectangle to circle center
    # max/min clamps the point to rectangle bounds
    closest_x: float = max(rect.left, min(cx, rect.right))
    closest_y: float = max(rect.top, min(cy, rect.bottom))
    
    # Check if closest point is within circle
    distance: float = math.sqrt((cx - closest_x) ** 2 + (cy - closest_y) ** 2)
    return distance < radius


def draw_text(surface: pygame.Surface, text: str, x: int, y: int,
              color: Tuple[int, int, int] = WHITE, size: int = 24) -> None:
    """
    Draw text on the screen.
    
    Args:
        surface: Where to draw (usually screen)
        text: The string to display
        x, y: Position for top-left of text
        color: Text color (default white)
        size: Font size in points (default 24)
    """
    font = pygame.font.Font(None, size)  # None = pygame default font
    text_surface = font.render(text, True, color)  # True = anti-aliasing
    surface.blit(text_surface, (x, y))


# ============================================================
# SECTION 6: MAIN GAME FUNCTION
# ============================================================


def main() -> None:
    """
    Main game function - contains the game loop.
    
    The game loop is the heartbeat of every game. It runs continuously
    (60 times per second in our case) and does three things:
    
    1. PROCESS INPUT - What did the player do?
    2. UPDATE STATE - Move things, check collisions, update game logic
    3. RENDER - Draw everything to the screen
    
    This pattern is sometimes called the "game loop" or "main loop"
    and is used in virtually every video game ever made.
    """
    # ---- GAME STATE VARIABLES ----
    # These track the overall state of the game
    running: bool = True          # False = exit game
    game_over: bool = False       # True = player lost
    score: int = 0                # Points earned
    
    # ---- CREATE GAME OBJECTS ----
    
    # Player tank - centered on screen
    player = Tank(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, GREEN)
    
    # Lists to hold multiple objects
    # Lists are perfect for this - we can add/remove items dynamically!
    bullets: List[Bullet] = []
    enemies: List[Enemy] = []
    obstacles: List[Obstacle] = []
    
    # Spawn initial enemies in the top portion of the screen
    for _ in range(3):  # underscore = we don't need the loop variable
        enemies.append(Enemy(
            random.randint(50, WINDOW_WIDTH - 50),
            random.randint(50, 150)
        ))
    
    # Create obstacle layout
    # These provide cover and make gameplay more interesting
    obstacles.append(Obstacle(150, 200, 100, 20))   # Top left horizontal
    obstacles.append(Obstacle(550, 200, 100, 20))   # Top right horizontal
    obstacles.append(Obstacle(300, 350, 20, 150))   # Left vertical
    obstacles.append(Obstacle(480, 350, 20, 150))   # Right vertical
    
    # ========================================
    # THE GAME LOOP - Runs ~60 times per second
    # ========================================
    while running:
        
        # ---- STEP 1: PROCESS INPUT ----
        # pygame.event.get() returns all events since last check
        # Events are things like key presses, mouse clicks, window close
        
        for event in pygame.event.get():
            # Window close button
            if event.type == pygame.QUIT:
                running = False
            
            # KEYDOWN fires once when a key is pressed (not held)
            # This is perfect for actions that should happen once,
            # like shooting or restarting
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bullets.append(player.shoot())
                if event.key == pygame.K_r and game_over:
                    # Restart by calling main() again
                    # This is a simple approach - resets everything
                    return main()
        
        # Only process gameplay if not game over
        if not game_over:
            # Check for HELD keys (continuous input)
            # get_pressed() returns current state of ALL keys
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player.move_forward()
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player.move_backward()
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player.rotate_left()
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player.rotate_right()
            
            # ---- STEP 2: UPDATE GAME STATE ----
            
            # Update all bullets (move them forward)
            for bullet in bullets:
                bullet.update()
            
            # Update all enemies (AI movement)
            for enemy in enemies:
                enemy.update()
            
            # ---- COLLISION DETECTION ----
            
            # Track what needs to be removed
            # We can't remove items while iterating, so we collect them first
            bullets_to_remove: List[Bullet] = []
            enemies_to_remove: List[Enemy] = []
            
            # Check bullet-enemy collisions
            for bullet in bullets:
                for enemy in enemies:
                    if check_circle_collision(
                        bullet.x, bullet.y, bullet.radius,
                        enemy.x, enemy.y, enemy.size
                    ):
                        bullets_to_remove.append(bullet)
                        enemies_to_remove.append(enemy)
                        score += 100  # Award points!
            
            # Remove destroyed objects
            for bullet in bullets_to_remove:
                if bullet in bullets:  # Safety check
                    bullets.remove(bullet)
            for enemy in enemies_to_remove:
                if enemy in enemies:
                    enemies.remove(enemy)
            
            # Remove bullets that hit obstacles or left screen
            # This is a LIST COMPREHENSION - a Pythonic way to filter lists
            # It reads: "keep bullets that haven't hit obstacles and aren't off screen"
            bullets = [b for b in bullets if not any(
                check_circle_rect_collision(b.x, b.y, b.radius, obs.rect)
                for obs in obstacles
            ) and not b.is_off_screen()]
            
            # Check player-enemy collision (game over!)
            for enemy in enemies:
                if check_circle_collision(
                    player.x, player.y, player.size,
                    enemy.x, enemy.y, enemy.size
                ):
                    game_over = True
            
            # Spawn new enemies when all are destroyed (endless mode)
            if len(enemies) == 0:
                for _ in range(3):
                    enemies.append(Enemy(
                        random.randint(50, WINDOW_WIDTH - 50),
                        random.randint(50, 150)
                    ))
        
        # ---- STEP 3: RENDER (DRAW) ----
        # We draw in layers: background first, then objects, then UI
        
        # Clear screen with black
        screen.fill(BLACK)
        
        # Draw obstacles (background layer)
        for obstacle in obstacles:
            obstacle.draw(screen)
        
        # Draw bullets
        for bullet in bullets:
            bullet.draw(screen)
        
        # Draw enemies
        for enemy in enemies:
            enemy.draw(screen)
        
        # Draw player (on top so they're always visible)
        player.draw(screen)
        
        # Draw UI (score and controls)
        draw_text(screen, f"Score: {score}", 10, 10)
        draw_text(screen, "WASD/Arrows: Move | SPACE: Shoot", 10, WINDOW_HEIGHT - 30)
        
        # Game over overlay
        if game_over:
            draw_text(
                screen, "GAME OVER",
                WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2 - 20,
                RED, 48
            )
            draw_text(
                screen, f"Final Score: {score}",
                WINDOW_WIDTH // 2 - 70, WINDOW_HEIGHT // 2 + 30
            )
            draw_text(
                screen, "Press R to Restart",
                WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2 + 60
            )
        
        # Flip the display buffer
        # This shows everything we just drew
        # (Double buffering prevents screen flicker)
        pygame.display.flip()
        
        # Control game speed
        # tick(60) means "wait enough time to achieve 60 FPS"
        clock.tick(FPS)
    
    # Clean shutdown
    pygame.quit()


# ============================================================
# SECTION 7: PROGRAM ENTRY POINT
# ============================================================
# This is a Python convention. When you run a file directly,
# __name__ is set to "__main__". When you import it, it's not.
# This lets us use this file as both a runnable program AND
# an importable module.

if __name__ == "__main__":
    main()
