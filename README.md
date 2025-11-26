# bring-back-BOLO

A faithful, modern reproduction of the classic top-down tank combat game BOLO.

![Gameplay preview - bring-back-BOLO](assets/screenshot.png)

*Figure: early prototype / artistic preview — replace `assets/screenshot.png` with a higher-resolution image as available.*

This repository contains research notes, prototypes, and design assets intended to reproduce and modernize the original game's core mechanics and multiplayer experience.

## Project Overview

- **Goal:** Recreate the original BOLO gameplay while providing a clean, extensible codebase for modern platforms (desktop and web).
- **Scope:** Movement, combat, map/objective systems, simple AI, and low-latency multiplayer networking.
- **Status:** Work in progress — design notes and early prototypes are available in the repository.

## Why this project

BOLO was memorable for its simple, tactical top-down tank combat on LAN. This project aims to capture that satisfying gameplay loop (movement, fire control, map control, and team coordination) and make it available to modern audiences and contributors.

## Repository contents (high level)

- `README.md` — Project summary and contributor guide (this file).
- `LICENSE` — Project license.
- `winBOLO.md` — Legacy notes and references about the original game.

Planned additions (not all present yet):

- `src/` — Game source code and prototypes (Python/Pygame or other engines).
- `assets/` — Art, audio, and map data.
- `docs/` — Design documents, gameplay references, and contributor guides.

## High-level features (planned)

- Tank movement and responsive input.
- Projectile, damage, and health systems tuned to match the original behavior.
- Map/objective support (capture, escort, domination-style modes).
- Local and networked multiplayer with a low-latency focus.
- Mod-friendly data/layout for easy community expansions.

## Getting started (contributors)

1. Fork this repository and create a short issue describing your planned change.
2. Create a branch with a descriptive name, e.g., `feat/ai-pathfinding` or `fix/controls`.
3. Implement your change, keep commits focused, and include a short demo (screenshot, recording, or test) when applicable.
4. Open a pull request targeting `main` with a clear description of what changed and why.

If and when build scripts are added, a concrete `How to build` section will be provided with exact commands for the chosen language and engine.

### How to build (Windows PowerShell)

The steps below show a minimal PowerShell workflow to prepare a Python development environment and run a Python prototype (adjust the final run command to your project entry point, e.g., `tank_game.py` or `src/main.py`).

- Prerequisites: Install Python 3.10+ and ensure `python` is on your PATH.
- Recommended: use a virtual environment to keep dependencies isolated.

1. Create a virtual environment

```powershell
python -m venv .venv
```

1. Activate the virtual environment (PowerShell)

```powershell
.\.venv\Scripts\Activate.ps1
# If execution policy blocks activation, run (temporary for shell):
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

1. Upgrade pip and install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

1. Run the prototype

```powershell
# Example: run an example entry point if present
python tank_game.py
# or
python -m src.main
```

Notes:

- If the project splits runtime and dev dependencies, install dev tools with `pip install -r requirements-dev.txt`.
- Replace `tank_game.py` / `src.main` with the actual entry point in this repository.

## Development guidelines

- Open an issue before starting large work so we can agree on scope.
- Keep PRs small and focused; include tests or a demo where reasonable.
- Follow consistent formatting and code conventions used by the codebase.

## How to help

- Playtest prototypes and report gameplay differences from the original.
- Contribute code, maps, assets, or documentation.
- Help improve CI, packaging, and cross-platform build steps.

## Acknowledgements & references

- See `winBOLO.md` for legacy material and reference notes about the original game.

## License

- See the `LICENSE` file in the repository root for license terms.

## Contact & contribution

- For questions or collaboration: open an issue, start a discussion, or submit a pull request.

---

Updated README: professional overview, contributor guidance, and next steps.
