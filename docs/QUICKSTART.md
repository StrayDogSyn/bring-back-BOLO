# Quick Start Guide - bring-back-BOLO

## 🚀 Get Playing in 2 Minutes

### Step 1: Install Python
Make sure you have Python 3.10+ installed:
```bash
python --version
# Should show: Python 3.10.x or higher
```

### Step 2: Clone and Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/bring-back-BOLO.git
cd bring-back-BOLO

# Create virtual environment
python -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Run the Game!
```bash
python main.py
```

That's it! The game window should open.

---

## 🎮 How to Play

### Your First Match

1. **You are the GREEN tank** in the bottom-left area
2. **RED tanks are enemies** - destroy them!
3. **Diamond shapes are bases** - drive near them to capture and resupply
4. **Square shapes are pillboxes** - auto-firing turrets (dangerous!)

### Controls

| Key | Action |
|-----|--------|
| **W** or **↑** | Move forward |
| **S** or **↓** | Move backward |
| **A** or **←** | Rotate left |
| **D** or **→** | Rotate right |
| **SPACE** | Fire shell |
| **M** | Drop mine |
| **ESC** | Pause game |
| **R** | Restart game |

### HUD (Top of Screen)
```
Armor: 8/8  Shells: 40/40  Mines: 40/40  Wood: 0/40
```
- **Armor** = Your health (0 = death)
- **Shells** = Cannon ammunition
- **Mines** = Explosives you can drop
- **Wood** = Building material (Phase 3 feature)

---

## 🎯 Objectives & Strategy

### Basic Tactics

1. **Capture the neutral base** (gray diamond in center)
   - Drive your tank near it
   - It turns green (your color)
   - Now you can resupply there!

2. **Resupply at friendly bases**
   - Drive near a green base
   - Your armor, shells, and mines automatically refill
   - Bases regenerate supplies slowly

3. **Avoid enemy pillboxes**
   - Red squares = enemy pillboxes
   - They auto-fire at you with high accuracy
   - Destroy them from a distance or capture them

4. **Use terrain tactically**
   - **Roads** (dark gray) = fast movement
   - **Grass** (green) = normal speed
   - **Forest** (dark green) = slow but provides cover
   - **Water** (blue) = blocks movement unless you have a boat
   - **Walls** (gray) = blocks movement and shots

### Advanced Tactics

- **Mine placement**: Drop mines (M key) in choke points or near bases
- **Kiting**: Fire while retreating to avoid damage
- **Base control**: Capturing all bases wins by resource starvation
- **Pillbox capture**: Destroy enemy pillboxes by reducing their health to 0, then drive near to capture

---

## 🐛 Troubleshooting

### Game won't start
```bash
# Make sure virtual environment is activated
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Reinstall pygame
pip install --upgrade pygame
```

### "Module not found" error
```bash
# Make sure you're in the project root directory
cd bring-back-BOLO

# Install requirements again
pip install -r requirements.txt
```

### Performance issues (lag)
1. Lower the FPS in `src/bolo_engine.py`:
   ```python
   class Config:
       FPS: int = 30  # Lower from 60
   ```

2. Reduce map size:
   ```python
   class Config:
       MAP_WIDTH: int = 32   # Half size
       MAP_HEIGHT: int = 24
   ```

### Window too small/large
Edit `src/bolo_engine.py`:
```python
class Config:
    WINDOW_WIDTH: int = 1280  # Your preferred width
    WINDOW_HEIGHT: int = 960  # Your preferred height
```

---

## 📚 Next Steps

Once you're comfortable with the basics:

1. **Read [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)** - Learn the code architecture
2. **Check [CHANGELOG.md](../CHANGELOG.md)** - See what's new in Phase 2
3. **Explore Phase 3 features** - Coming soon (LGM, building, sprites)
4. **Contribute** - Fork and add your own features!

---

## 🎓 Learning Resources

### For Beginners
- **lesson/tank_game.py** - Simplified Phase 1 version with lots of comments
- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Pygame Documentation](https://www.pygame.org/docs/)

### For Advanced Users
- **src/bolo_engine.py** - Full Phase 2 engine with advanced patterns
- [Type Hints Guide](https://docs.python.org/3/library/typing.html)
- [Game Architecture Patterns](https://gameprogrammingpatterns.com/)

---

## 💡 Tips & Tricks

### Keyboard Shortcuts
- Hold **W + A** = Move forward while turning left (arc movement)
- Tap **S** briefly = Quick reverse to dodge shots
- Spam **SPACE** near bases = Rapid fire with infinite ammo

### Combat Tips
- Lead your shots against moving enemies
- Use terrain for cover (forests, walls)
- Retreat to friendly bases when low on armor
- Mines are great for base defense

### Map Control
- The center base is strategically important (equidistant to all)
- Control at least 2 bases for sustainable warfare
- Pillboxes provide automatic defense - capture them!

---

## 🤝 Get Help

- **Issues**: [GitHub Issues](https://github.com/yourusername/bring-back-BOLO/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/bring-back-BOLO/discussions)
- **Email**: your-email@example.com

---

**Happy tanking! 🎮**

*Now go capture those bases and dominate the battlefield!*
