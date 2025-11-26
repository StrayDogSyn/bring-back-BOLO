# 🎮 Tank Battle: Python Fundamentals in Action

## Pre-Thanksgiving Live Coding Session
**Duration:** ~60 minutes  
**Audience:** Python Essentials Novice Students  
**Vibe:** Light, engaging, "look what you can build with basics"

---

## 🎯 Learning Objectives

By the end of this session, students will see these fundamentals in action:
- **Variables & Data Types** - Storing game state (position, health, score)
- **Functions** - Organizing reusable game logic
- **Classes (Intro OOP)** - Creating game objects (Tank, Bullet, Enemy)
- **Loops** - The game loop pattern (the heartbeat of every game)
- **Conditionals** - Collision detection, game state checks
- **Lists** - Managing multiple bullets and enemies
- **Type Hints** - Making code self-documenting

---

## 🛠️ Setup Instructions (Do This BEFORE Class)

### 1. Create Virtual Environment
```bash
# Navigate to your project folder
cd tank_game

# Create virtual environment (like a clean kitchen for your project)
python -m venv .venv

# Activate it
# On Mac/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# You'll see (.venv) in your terminal - that means it's working!
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Test Installation
```bash
python -c "import pygame; print('Pygame ready!')"
```

---

## 📋 Lesson Flow (60 Minutes)

| Time | Section | Concepts Covered |
|------|---------|-----------------|
| 0-5  | Intro & Setup | Why pygame, project structure |
| 5-15 | Game Window | Variables, while loop, constants |
| 15-25 | Tank Class | Classes, __init__, methods |
| 25-35 | Movement & Shooting | Event handling, lists, conditionals |
| 35-45 | Enemies & Obstacles | More classes, simple AI |
| 45-55 | Collision Detection | Functions, conditionals, game logic |
| 55-60 | Wrap-up | Review, Q&A, challenge ideas |

---

## 🎬 Live Coding Script

### SECTION 1: Introduction (5 min)

**SAY:** "Hey everyone! Before we all scatter for turkey and awkward family questions about our career choices, let's build something fun. We're making a tank battle game using only the Python fundamentals you've been learning."

**SAY:** "Think of this like cooking - we've got our basic ingredients (variables, loops, functions, classes), and today we're making a full meal. By the end, you'll see how these 'boring' fundamentals become something you can actually play."

---

### SECTION 2: Game Window - The Foundation (10 min)

**START NEW FILE: `tank_game.py`**

**SAY:** "Every game needs a window to display in. Let's start with the absolute basics - getting something on screen."

```python
"""
Tank Battle - A Simple 2D Shooter
=================================
Demonstrates Python fundamentals through game development.
Built for Code the Dream Python Essentials.

Concepts covered:
- Variables and constants
- Functions and classes  
- Loops and conditionals
- Lists and basic OOP
"""

# ============================================================
# SECTION 1: IMPORTS
# ============================================================
# We import libraries at the top - like gathering ingredients
# before cooking. pygame handles all the game graphics and input.

import pygame
import math
import random
from typing import List, Tuple

# Initialize pygame - this "wakes up" the game engine
# Think of it like preheating your oven
pygame.init()
```

**SAY:** "We start with imports - bringing in tools we need. `pygame` is our game engine, `math` helps with angles and movement, `random` for enemy behavior, and `typing` for those helpful type hints."

```python
# ============================================================
# SECTION 2: CONSTANTS (Configuration)
# ============================================================
# Constants are variables that DON'T change during the game.
# By convention, we write them in ALL_CAPS.
# This makes our code easy to tweak - want a bigger window?
# Just change these numbers!

WINDOW_WIDTH: int = 800   # Game window width in pixels
WINDOW_HEIGHT: int = 600  # Game window height in pixels
FPS: int = 60             # Frames per second (game speed)

# Colors are tuples of (Red, Green, Blue) - each 0-255
# It's like mixing paint!
BLACK: Tuple[int, int, int] = (0, 0, 0)
WHITE: Tuple[int, int, int] = (255, 255, 255)
GREEN: Tuple[int, int, int] = (34, 139, 34)      # Forest green for player
RED: Tuple[int, int, int] = (178, 34, 34)        # Firebrick red for enemies
GRAY: Tuple[int, int, int] = (128, 128, 128)     # Gray for obstacles
YELLOW: Tuple[int, int, int] = (255, 215, 0)     # Gold for bullets

# Game settings - easy to adjust for difficulty
PLAYER_SPEED: int = 4          # How fast player moves
PLAYER_ROTATION_SPEED: int = 5  # How fast player turns (degrees)
BULLET_SPEED: int = 8          # How fast bullets travel
ENEMY_SPEED: int = 2           # Enemy movement speed
```

**SAY:** "Constants are like the settings menu of our game. Notice the type hints after each variable name - that colon syntax tells us (and our editor) what type of data each variable holds. It's self-documenting code!"

```python
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
```

**CHECKPOINT - RUN THE CODE:** 
```bash
python tank_game.py
```

**SAY:** "Right now it just flashes and closes - that's because we need a game loop to keep it running. Let's add that."

---

### SECTION 3: The Game Loop (5 min)

**SAY:** "Every game has a 'heartbeat' - a loop that runs continuously. It's like the main cooking timer that keeps checking: 'Is dinner ready? No? Keep cooking!'"

```python
# ============================================================
# SECTION 4: THE GAME LOOP
# ============================================================
# This is the heartbeat of every game. It runs continuously,
# doing three things:
#   1. PROCESS INPUT (what did the player do?)
#   2. UPDATE STATE (move things, check collisions)
#   3. RENDER (draw everything to screen)

def main() -> None:
    """Main game function - runs the game loop."""
    
    running: bool = True  # Controls when game exits
    
    # THE GAME LOOP - runs ~60 times per second
    while running:
        
        # ----- STEP 1: PROCESS INPUT -----
        # pygame.event.get() returns a list of everything that happened
        # (key presses, mouse clicks, window close, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # User clicked the X
                running = False
        
        # ----- STEP 2: UPDATE -----
        # (We'll add game logic here soon)
        
        # ----- STEP 3: RENDER (Draw) -----
        screen.fill(BLACK)  # Clear screen with black
        
        # Flip the display - this shows what we drew
        # Think of it like flipping a page in a flipbook
        pygame.display.flip()
        
        # Control game speed - wait to maintain 60 FPS
        clock.tick(FPS)
    
    # Clean up when done
    pygame.quit()


# This runs our main function when we execute the file
if __name__ == "__main__":
    main()
```

**CHECKPOINT - RUN THE CODE**

**SAY:** "Now we have a black window that stays open! That `while running` loop is doing its job. Click the X to close it. Now let's add something to see - our tank!"

---

### SECTION 4: The Tank Class (10 min)

**SAY:** "Classes are like blueprints. If we're building houses, a class is the architectural plan - it describes WHAT a house has and CAN DO, but isn't a house itself. When we create an 'instance', THAT'S an actual house."

**ADD BEFORE the `main()` function:**

```python
# ============================================================
# SECTION 5: GAME CLASSES
# ============================================================
# Classes are blueprints for game objects. 
# Think of a class like a cookie cutter - it defines the shape,
# but you can make many cookies (instances) from it.


class Tank:
    """
    The player's tank.
    
    Attributes:
        x, y: Position on screen (center of tank)
        angle: Direction tank is facing (in degrees)
        speed: How fast the tank moves
        size: Radius of the tank (it's drawn as a circle)
        color: RGB tuple for tank color
    """
    
    def __init__(self, x: int, y: int, color: Tuple[int, int, int]) -> None:
        """
        Initialize a new tank.
        
        Args:
            x: Starting x position
            y: Starting y position  
            color: Tank color as RGB tuple
        """
        # Position - where is the tank?
        self.x: float = x
        self.y: float = y
        
        # Direction - which way is it facing? (0 = right, 90 = down)
        self.angle: float = 0
        
        # Movement speed
        self.speed: int = PLAYER_SPEED
        self.rotation_speed: int = PLAYER_ROTATION_SPEED
        
        # Appearance
        self.size: int = 20  # Radius in pixels
        self.color: Tuple[int, int, int] = color
    
    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the tank on the given surface.
        
        We draw:
        1. A circle for the body
        2. A line for the cannon (shows direction)
        """
        # Draw tank body (circle)
        pygame.draw.circle(
            surface,           # Where to draw
            self.color,        # What color
            (int(self.x), int(self.y)),  # Position (must be integers)
            self.size          # Radius
        )
        
        # Draw cannon - a line pointing in the direction we're facing
        # We use trigonometry to find the end point of the line
        # math.radians converts degrees to radians (what math functions expect)
        cannon_length: int = self.size + 15
        end_x: float = self.x + math.cos(math.radians(self.angle)) * cannon_length
        end_y: float = self.y + math.sin(math.radians(self.angle)) * cannon_length
        
        pygame.draw.line(
            surface,
            WHITE,
            (int(self.x), int(self.y)),     # Start at tank center
            (int(end_x), int(end_y)),       # End at calculated point
            4  # Line thickness
        )
    
    def move_forward(self) -> None:
        """Move tank forward in the direction it's facing."""
        # Trigonometry! cos gives x component, sin gives y component
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
        self._keep_on_screen()
    
    def move_backward(self) -> None:
        """Move tank backward (opposite of facing direction)."""
        self.x -= math.cos(math.radians(self.angle)) * self.speed
        self.y -= math.sin(math.radians(self.angle)) * self.speed
        self._keep_on_screen()
    
    def rotate_left(self) -> None:
        """Rotate tank counter-clockwise."""
        self.angle -= self.rotation_speed
    
    def rotate_right(self) -> None:
        """Rotate tank clockwise."""
        self.angle += self.rotation_speed
    
    def _keep_on_screen(self) -> None:
        """Keep tank within window bounds (private helper method)."""
        # The underscore prefix is a Python convention meaning
        # "this method is for internal use only"
        self.x = max(self.size, min(WINDOW_WIDTH - self.size, self.x))
        self.y = max(self.size, min(WINDOW_HEIGHT - self.size, self.y))
```

**SAY:** "Notice the `__init__` method - that's the 'constructor'. It runs when we create a new tank. The `self` parameter refers to the specific tank we're working with. And see those docstrings in triple quotes? That's professional documentation."

**UPDATE `main()` to create and draw the tank:**

```python
def main() -> None:
    """Main game function - runs the game loop."""
    
    running: bool = True
    
    # Create our player tank in the center of the screen
    player = Tank(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, GREEN)
    
    while running:
        # ----- STEP 1: PROCESS INPUT -----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Check for held-down keys (continuous input)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player.move_forward()
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player.move_backward()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.rotate_left()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.rotate_right()
        
        # ----- STEP 2: UPDATE -----
        # (Coming soon: bullets, enemies, collisions)
        
        # ----- STEP 3: RENDER -----
        screen.fill(BLACK)
        player.draw(screen)  # Draw our tank!
        pygame.display.flip()
        
        clock.tick(FPS)
    
    pygame.quit()
```

**CHECKPOINT - RUN AND DRIVE AROUND!**

**SAY:** "WASD or arrow keys to move! See how the class methods let us organize our code? Instead of a mess of x += something everywhere, we have clear, named methods like `move_forward()`."

---

### SECTION 5: Bullets - Lists in Action (10 min)

**SAY:** "Now let's shoot! We'll need to track multiple bullets, so this is where lists come in. It's like keeping a shopping list that grows and shrinks."

**ADD this class after Tank:**

```python
class Bullet:
    """
    A bullet fired by a tank.
    
    Bullets travel in a straight line until they hit something
    or leave the screen.
    """
    
    def __init__(self, x: float, y: float, angle: float) -> None:
        """Create bullet at position, traveling in direction of angle."""
        self.x: float = x
        self.y: float = y
        self.angle: float = angle
        self.speed: int = BULLET_SPEED
        self.radius: int = 5
        self.color: Tuple[int, int, int] = YELLOW
    
    def update(self) -> None:
        """Move bullet forward each frame."""
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the bullet."""
        pygame.draw.circle(
            surface,
            self.color,
            (int(self.x), int(self.y)),
            self.radius
        )
    
    def is_off_screen(self) -> bool:
        """Check if bullet has left the play area."""
        return (self.x < 0 or self.x > WINDOW_WIDTH or
                self.y < 0 or self.y > WINDOW_HEIGHT)
```

**ADD this method to the Tank class:**

```python
    def shoot(self) -> Bullet:
        """
        Fire a bullet from the cannon.
        
        Returns:
            A new Bullet object traveling in tank's facing direction.
        """
        # Calculate bullet starting position (at end of cannon)
        start_x = self.x + math.cos(math.radians(self.angle)) * (self.size + 15)
        start_y = self.y + math.sin(math.radians(self.angle)) * (self.size + 15)
        return Bullet(start_x, start_y, self.angle)
```

**UPDATE `main()` to handle shooting:**

```python
def main() -> None:
    """Main game function - runs the game loop."""
    
    running: bool = True
    
    player = Tank(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, GREEN)
    
    # List to hold all active bullets
    # Lists let us manage a changing number of objects!
    bullets: List[Bullet] = []
    
    while running:
        # ----- STEP 1: PROCESS INPUT -----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # KEYDOWN fires once when key is pressed (not held)
            # Perfect for shooting - one bullet per press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(player.shoot())  # Add bullet to list
        
        # Continuous key input for movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player.move_forward()
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player.move_backward()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.rotate_left()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.rotate_right()
        
        # ----- STEP 2: UPDATE -----
        # Update all bullets
        for bullet in bullets:
            bullet.update()
        
        # Remove bullets that left the screen
        # We create a NEW list with only the bullets still on screen
        # This is called a "list comprehension" - very Pythonic!
        bullets = [b for b in bullets if not b.is_off_screen()]
        
        # ----- STEP 3: RENDER -----
        screen.fill(BLACK)
        
        # Draw all bullets
        for bullet in bullets:
            bullet.draw(screen)
        
        player.draw(screen)
        pygame.display.flip()
        
        clock.tick(FPS)
    
    pygame.quit()
```

**CHECKPOINT - SHOOT WITH SPACEBAR!**

**SAY:** "That list comprehension is chef's kiss. Instead of a clunky loop removing items, we filter the list in one clean line. `[b for b in bullets if not b.is_off_screen()]` reads almost like English: 'give me all bullets that aren't off screen.'"

---

### SECTION 6: Enemies & Obstacles (10 min)

**ADD these classes:**

```python
class Obstacle:
    """
    A wall/barrier that blocks movement and bullets.
    Simple rectangles that don't move.
    """
    
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        """Create obstacle with position and dimensions."""
        self.rect = pygame.Rect(x, y, width, height)
        self.color: Tuple[int, int, int] = GRAY
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the obstacle."""
        pygame.draw.rect(surface, self.color, self.rect)


class Enemy:
    """
    An enemy tank with simple AI.
    Moves in a pattern and can be destroyed.
    """
    
    def __init__(self, x: int, y: int) -> None:
        """Create enemy at position."""
        self.x: float = x
        self.y: float = y
        self.size: int = 18
        self.color: Tuple[int, int, int] = RED
        self.speed: int = ENEMY_SPEED
        self.direction: int = random.choice([0, 90, 180, 270])  # Cardinal directions
        self.move_timer: int = 0  # Counts frames until direction change
    
    def update(self) -> None:
        """Move enemy with simple patrol AI."""
        # Change direction periodically (every 60-120 frames)
        self.move_timer += 1
        if self.move_timer > random.randint(60, 120):
            self.direction = random.choice([0, 90, 180, 270])
            self.move_timer = 0
        
        # Move in current direction
        self.x += math.cos(math.radians(self.direction)) * self.speed
        self.y += math.sin(math.radians(self.direction)) * self.speed
        
        # Bounce off walls
        if self.x < self.size or self.x > WINDOW_WIDTH - self.size:
            self.direction = 180 - self.direction  # Reverse horizontal
            self.x = max(self.size, min(WINDOW_WIDTH - self.size, self.x))
        if self.y < self.size or self.y > WINDOW_HEIGHT - self.size:
            self.direction = -self.direction  # Reverse vertical
            self.y = max(self.size, min(WINDOW_HEIGHT - self.size, self.y))
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw enemy tank."""
        pygame.draw.circle(
            surface,
            self.color,
            (int(self.x), int(self.y)),
            self.size
        )
        # Draw a simple direction indicator
        end_x = self.x + math.cos(math.radians(self.direction)) * (self.size + 8)
        end_y = self.y + math.sin(math.radians(self.direction)) * (self.size + 8)
        pygame.draw.line(
            surface,
            WHITE,
            (int(self.x), int(self.y)),
            (int(end_x), int(end_y)),
            3
        )
```

---

### SECTION 7: Collision Detection & Scoring (10 min)

**SAY:** "Now the fun part - making things interact! Collision detection is just asking: 'Are these two things overlapping?'"

**ADD these helper functions before `main()`:**

```python
# ============================================================
# SECTION 6: HELPER FUNCTIONS
# ============================================================

def check_circle_collision(x1: float, y1: float, r1: int,
                           x2: float, y2: float, r2: int) -> bool:
    """
    Check if two circles are overlapping.
    
    This is the Pythagorean theorem in action!
    If the distance between centers is less than the sum of radii,
    they're touching.
    
    Args:
        x1, y1, r1: First circle's center and radius
        x2, y2, r2: Second circle's center and radius
    
    Returns:
        True if circles overlap, False otherwise
    """
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance < (r1 + r2)


def check_circle_rect_collision(cx: float, cy: float, radius: int,
                                rect: pygame.Rect) -> bool:
    """
    Check if a circle overlaps with a rectangle.
    
    We find the closest point on the rectangle to the circle's center,
    then check if that point is within the circle.
    """
    # Find closest point on rectangle to circle center
    closest_x = max(rect.left, min(cx, rect.right))
    closest_y = max(rect.top, min(cy, rect.bottom))
    
    # Check distance from closest point to circle center
    distance = math.sqrt((cx - closest_x) ** 2 + (cy - closest_y) ** 2)
    return distance < radius


def draw_text(surface: pygame.Surface, text: str, x: int, y: int, 
              color: Tuple[int, int, int] = WHITE, size: int = 24) -> None:
    """Draw text on the screen."""
    font = pygame.font.Font(None, size)  # None = default font
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))
```

**FINAL VERSION of `main()`:**

```python
def main() -> None:
    """Main game function - runs the game loop."""
    
    running: bool = True
    game_over: bool = False
    score: int = 0
    
    # Create player
    player = Tank(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, GREEN)
    
    # Create game objects using lists
    bullets: List[Bullet] = []
    enemies: List[Enemy] = []
    obstacles: List[Obstacle] = []
    
    # Spawn initial enemies
    for _ in range(3):  # Start with 3 enemies
        enemies.append(Enemy(
            random.randint(50, WINDOW_WIDTH - 50),
            random.randint(50, 150)  # Spawn in top area
        ))
    
    # Create some obstacles
    obstacles.append(Obstacle(150, 200, 100, 20))   # Horizontal wall
    obstacles.append(Obstacle(550, 200, 100, 20))   # Horizontal wall
    obstacles.append(Obstacle(300, 350, 20, 150))   # Vertical wall
    obstacles.append(Obstacle(480, 350, 20, 150))   # Vertical wall
    
    while running:
        # ----- STEP 1: PROCESS INPUT -----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bullets.append(player.shoot())
                if event.key == pygame.K_r and game_over:
                    # Restart game
                    return main()  # Simple restart by calling main() again
        
        if not game_over:
            # Movement input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player.move_forward()
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player.move_backward()
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player.rotate_left()
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player.rotate_right()
            
            # ----- STEP 2: UPDATE -----
            
            # Update bullets
            for bullet in bullets:
                bullet.update()
            
            # Update enemies
            for enemy in enemies:
                enemy.update()
            
            # Check bullet-enemy collisions
            bullets_to_remove: List[Bullet] = []
            enemies_to_remove: List[Enemy] = []
            
            for bullet in bullets:
                for enemy in enemies:
                    if check_circle_collision(
                        bullet.x, bullet.y, bullet.radius,
                        enemy.x, enemy.y, enemy.size
                    ):
                        bullets_to_remove.append(bullet)
                        enemies_to_remove.append(enemy)
                        score += 100
            
            # Remove destroyed objects
            for bullet in bullets_to_remove:
                if bullet in bullets:
                    bullets.remove(bullet)
            for enemy in enemies_to_remove:
                if enemy in enemies:
                    enemies.remove(enemy)
            
            # Check bullet-obstacle collisions
            bullets = [b for b in bullets if not any(
                check_circle_rect_collision(b.x, b.y, b.radius, obs.rect)
                for obs in obstacles
            ) and not b.is_off_screen()]
            
            # Check player-enemy collision (game over condition)
            for enemy in enemies:
                if check_circle_collision(
                    player.x, player.y, player.size,
                    enemy.x, enemy.y, enemy.size
                ):
                    game_over = True
            
            # Spawn new enemy if all destroyed (endless mode)
            if len(enemies) == 0:
                for _ in range(3):
                    enemies.append(Enemy(
                        random.randint(50, WINDOW_WIDTH - 50),
                        random.randint(50, 150)
                    ))
        
        # ----- STEP 3: RENDER -----
        screen.fill(BLACK)
        
        # Draw obstacles first (background layer)
        for obstacle in obstacles:
            obstacle.draw(screen)
        
        # Draw bullets
        for bullet in bullets:
            bullet.draw(screen)
        
        # Draw enemies
        for enemy in enemies:
            enemy.draw(screen)
        
        # Draw player
        player.draw(screen)
        
        # Draw UI
        draw_text(screen, f"Score: {score}", 10, 10)
        draw_text(screen, "WASD/Arrows: Move | SPACE: Shoot", 10, WINDOW_HEIGHT - 30)
        
        if game_over:
            draw_text(screen, "GAME OVER", WINDOW_WIDTH // 2 - 80, 
                     WINDOW_HEIGHT // 2 - 20, RED, 48)
            draw_text(screen, f"Final Score: {score}", WINDOW_WIDTH // 2 - 70,
                     WINDOW_HEIGHT // 2 + 30)
            draw_text(screen, "Press R to Restart", WINDOW_WIDTH // 2 - 80,
                     WINDOW_HEIGHT // 2 + 60)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()


if __name__ == "__main__":
    main()
```

---

## 🎯 Wrap-Up Discussion Points (5 min)

**SAY:** "Look what we built in under an hour! Let's review what fundamentals made this possible:"

1. **Variables** - Stored all our game state (positions, scores, colors)
2. **Constants** - Made configuration easy to change
3. **Functions** - Organized collision logic into reusable pieces
4. **Classes** - Created blueprints for Tank, Bullet, Enemy, Obstacle
5. **Loops** - The game loop runs 60 times per second, `for` loops iterate through lists
6. **Conditionals** - Check collisions, handle game over, process input
7. **Lists** - Managed multiple bullets and enemies dynamically
8. **Type Hints** - Made our code self-documenting

---

## 🚀 Challenge Ideas for Students

If students want to expand on their own:

1. **Easy:** Change colors and speeds
2. **Medium:** Add health bar (player takes multiple hits)
3. **Medium:** Make enemies shoot back
4. **Hard:** Add levels with different obstacle layouts
5. **Hard:** Add power-ups (speed boost, triple shot)

---

## 🐛 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "No module named pygame" | Activate venv, run `pip install pygame` |
| Window immediately closes | Make sure game loop is running |
| Tank not moving | Check key bindings, ensure `move_forward()` is called |
| Bullets not appearing | Verify SPACE triggers `player.shoot()` |
| Collision not working | Check radius values in collision functions |

---

## 📁 File Structure

```
tank_game/
├── .venv/              # Virtual environment (don't edit)
├── requirements.txt    # Dependencies
├── tank_game.py        # Main game file
└── LESSON_PLAN.md      # This file
```

---

**Happy Thanksgiving, Code the Dream! 🦃🎮**
