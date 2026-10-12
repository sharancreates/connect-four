# Research & Technical Specification — Phase 3 (Person B)

## Context & Objectives
Phase 3 finishes the Connect Four AI project deliverables for Person B (Member 2: Engineering, GUI & Evaluation).
The primary objectives are:
1. **Pygame GUI Visual Polish & Live Controls**:
   - Winning 4-in-a-row ray overlay: compute exact winning cell indices and draw an antialiased line or connected glow vector between disc centers.
   - Last-move circular highlight/ring: visually highlight the most recent move so users easily spot AI drops.
   - Interactive playback speed and pause controls: spacebar toggle, numeric speed adjustment (1 to 9), delay pacing.
   - Flexible CLI launch: support human-vs-ai, ai-vs-human, and ai-vs-ai demo modes.
2. **Automated Publication Visualizations**:
   - Module `connect4/benchmark/plotter.py` generating 4 high-DPI charts saved into `docs/figures/`:
     - Figure 1: Search Latency (Wall-clock Time) vs. Depth / Simulation Budget.
     - Figure 2: Search Expansions (Nodes / Simulations) vs. Depth (Logarithmic Scale showing Alpha-Beta pruning power).
     - Figure 3: Head-to-Head Win-Rate Heatmap across all agent pairs.
     - Figure 4: Peak Memory Consumption across agents.
3. **Academic Stage 3 Report & Viva Presentation Guide**:
   - `docs/STAGE3_REPORT_SECTIONS_1_6_7.md`: Sections 1, 6, 7 & APA references adhering to Adani University FEST AI-ML syllabus.
   - `docs/VIVA_TALKING_POINTS_PERSON_B.md`: Live demonstration script and viva defense talking points for examiners.

## Technical Details

### 1. Board Winning Coordinates Helper
In `connect4/core/board.py`:
- `get_winning_coordinates() -> Optional[List[Tuple[int, int]]]`:
  - When the game is terminal with a winner, locates the 4 coordinates `[(r1, c1), (r2, c2), (r3, c3), (r4, c4)]` forming the horizontal, vertical, or diagonal 4-in-a-row.
  - Returns coordinates in order from start to end so that drawing lines is clean.

### 2. GUI Rendering Upgrades
In `connect4/gui/pygame_app.py`:
- Convert board grid coordinates `(r, c)` to pixel coordinates:
  - Center `X = c * SQUARESIZE + SQUARESIZE // 2`
  - Center `Y = (r + 1) * SQUARESIZE + SQUARESIZE // 2`
- Draw last move ring: `pygame.draw.circle(screen, COLOR_HIGHLIGHT, center, RADIUS - 4, width=4)`.
- Draw winning line: `pygame.draw.line(screen, COLOR_WIN_LINE, start_center, end_center, width=8)`.
- State tracking:
  - `self.paused: bool = False` (toggled by `K_SPACE`).
  - `self.ai_delay: int = 500` ms (adjusted via keys `1`-`9`).
  - Mode support: `mode: str = "human-vs-ai" | "ai-vs-ai"`.

### 3. Matplotlib Headless Plotter
In `connect4/benchmark/plotter.py`:
- Use `matplotlib.use("Agg")` to support running in headless CI and automated test environments.
- Provide cached empirical baseline data from benchmark tournaments and allow running live sweeps via `--live`.
- Save clean, publication-ready PNG files (300 DPI) to `docs/figures/`.

### 4. Git Branch Strategy
- Working on isolated branch `person-b-week-3`.
- Commit messages strictly adhere to Conventional Commits without "GSD" in commit messages.
