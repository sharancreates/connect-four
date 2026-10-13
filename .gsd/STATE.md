---
updated: 2026-10-12T22:12:00+05:30
---

# Project State

## Current Position
- **Phase**: 3 - Benchmarking, GUI Integration, Analysis & Report (Week 3)
- **Active Role**: Member 1 (Algorithms & Core Logic) & Member 2 (Engineering, GUI & Evaluation)
- **Branch**: `maitri-week3`
- **Status**: ✅ Phase 3 Complete & Verified (All Plans 3.1, 3.2, 3.3, 3.3b Complete)

---

## Deliverables Summary (Phase 3 — Member 1: Plan 3.3b)

### 1. Scaling & Failure-Mode Experimentation Suite
- `experiments_cli.py`:
  - Depth-scaling benchmark measuring runtime and node expansion for plain Minimax and Alpha-Beta (with and without heuristic) from depth 3 up to depth 9 on both empty board and 8-ply mid-game positions.
  - Iterative deepening time budget deadline enforcement and rollback validation across 0.05s, 0.2s, 0.5s, and 1.0s.
  - Tactical block test verifying immediate single-move threat responses across 20 trials.
  - MCTS simulation budget sweeps (50, 200, 500, 1000 rollouts) against depth-4 Alpha-Beta over 10 games per budget with alternating sides.
- `docs/results/`:
  - `depth_scaling.csv`: Measured runtime and exact node counts across depths 3 to 9.
  - `iterative_scaling.csv`: Depth reached, nodes explored, and move choices under varying clock budgets.
  - `mcts_budget_scaling.csv`: Win/loss/draw records and average game lengths across simulation budgets.
  - `ordering_comparison.csv`: Node pruning efficiency with center-first ordering.
- `docs/figures/`:
  - `fig5_depth_scaling.png`: Log-scale time per move vs. search depth.
  - `fig6_mcts_strength.png`: MCTS win rate and lost-game length vs. simulation budget.

### 2. Academic Report (Sections 2, 3, 4, 5 & 8)
- `docs/STAGE3_REPORT_SECTIONS_2_3_4_5_8.md`:
  - **Section 2**: Formal search-problem formulation, depth-limited minimax, alpha-beta pruning, and iterative deepening specifications.
  - **Section 3**: 69-window heuristic evaluation design rationale, score weights, unit validation, and cost profile.
  - **Section 4**: Minimax vs. Alpha-Beta empirical pruning comparison (up to 97.1% pruning at depth 5), move ordering role, and iterative deepening under strict clocks.
  - **Section 5**: Theoretical vs. empirical complexity, effective branching factor ($b^* \approx N^{1/d}$ between 3.4 and 4.4), throughput (26,000 nodes/sec), memory ($O(d)$), and depth-9 cliff demonstration.
  - **Section 8**: Detailed error analysis covering horizon effect, heuristic limitations, one-move tactical guards vs. deep traps, and MCTS rollout variance at low budgets.

### 3. Presentation Slides (Member 1)
- `docs/SLIDES_MEMBER1.md`: 11-slide presentation outline with speaker notes and viva defense preparation.

---

## Deliverables Summary (Phase 3 — Member 2)

### 1. Pygame GUI Visual Polish & Live Controls (Plan 3.1)
- `connect4/core/board.py`: Added `get_winning_coordinates()` supporting horizontal, vertical, and diagonal win vector detection.
- `connect4/gui/pygame_app.py`:
  - **Winning Ray Overlay**: Dynamic neon emerald victory line connecting the 4 winning discs with accent circles.
  - **Last-Move Ring**: Prominent white circular outline and center dot on the latest placed disc (`board.last_move`).
  - **Playback Controls**: Instant Spacebar pause/resume toggle, dynamic speed scaling (keys 1–9, delay pacing 1,200ms to 25ms), and top-banner HUD.
- `gui_main.py`: Interactive CLI supporting `--mode {human-vs-ai,ai-vs-ai}`, `--agent1`, `--agent2`, `--speed`, and `--headless`.

### 2. Publication Visualizations Suite (Plan 3.2)
- `connect4/benchmark/plotter.py` & `plotter_cli.py`:
  - Headless `Agg` backend with modern publication aesthetics.
  - Generated 4 high-DPI (300 DPI) figures saved in `docs/figures/`:
    - **Figure 1**: Mean Move Latency vs. Search Depth (`fig1_execution_time_vs_depth.png`).
    - **Figure 2**: Search Space Expansion vs. Depth on Logarithmic Scale (`fig2_nodes_expanded_log_scale.png`), showcasing 98.4% branch pruning at depth 6.
    - **Figure 3**: Head-to-Head Tournament Win-Rate Matrix Heatmap (`fig3_tournament_winrate_heatmap.png`).
    - **Figure 4**: Peak Heap Memory Consumption per Algorithm (`fig4_peak_memory_footprint.png`).

### 3. Stage 3 Academic Report & Viva Defense Guide (Plan 3.3)
- `docs/STAGE3_REPORT_SECTIONS_1_6_7.md`:
  - **Section 1**: Connect Four state-space complexity ($4.53 \times 10^{12}$ reachable positions), game tree complexity ($10^{21}$), and PEAS environmental formalization.
  - **Section 6**: Controlled tournament experimental setup ($N=20$, alternating first-mover), 10-row quantitative benchmark metrics table, detailed analysis of all 4 figures, and algorithmic trade-off evaluation.
  - **Section 7**: Modular software architecture, microsecond latency & `tracemalloc` memory profiling rigor, and 60 FPS Pygame GUI design.
  - **Academic References**: Formal APA-7 bibliography.
- `docs/VIVA_TALKING_POINTS_PERSON_B.md`:
  - 3-Minute Elevator Presentation pitch.
  - Step-by-step live demo script with exact terminal commands for GUI and benchmark demonstration.
  - 6 technical viva defense questions and model answers for examiners.

---

## Touched Files (Week 3 — Member 1)
- `docs/STAGE3_REPORT_SECTIONS_2_3_4_5_8.md`
- `experiments_cli.py`
- `docs/results/depth_scaling.csv`
- `docs/results/iterative_scaling.csv`
- `docs/results/mcts_budget_scaling.csv`
- `docs/results/ordering_comparison.csv`
- `docs/figures/fig5_depth_scaling.png`
- `docs/figures/fig6_mcts_strength.png`
- `docs/SLIDES_MEMBER1.md`
- `README.md`
- `docs/ALGORITHMS.md`
- `.gsd/ROADMAP.md`
- `.gsd/STATE.md`

---

## Test Suite Status
- **53/53 tests passing** across entire codebase (`python -m pytest tests/ -q` in 26.88s).

---

## Next Steps
1. Final review with Member 2.
2. Combining report sections (Member 1 sections 2, 3, 4, 5, 8 + Member 2 sections 1, 6, 7).
3. Viva rehearsal.
4. Final submission.

