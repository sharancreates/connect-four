# Phase 2 Research: Monte Carlo Tree Search, Benchmarking, and Pygame Architecture

> **Focus:** Member 2 (Engineering, GUI & Evaluation) deliverables for Week 2  
> **Date:** 2026-10-11

---

## 1. Monte Carlo Tree Search (MCTS) for Connect Four

### Core Algorithm (4 Phases per Iteration)
1. **Selection**:
   Traverse from root to an expandable node using the Upper Confidence bound applied to Trees (UCT):
   $$\text{UCT}(i) = \frac{w_i}{n_i} + C_p \sqrt{\frac{\ln N}{n_i}}$$
   where:
   - $w_i$ = total reward / utility backpropagated through node $i$ (from perspective of current player)
   - $n_i$ = visit count of child node $i$
   - $N$ = visit count of parent node
   - $C_p = \sqrt{2} \approx 1.414$ = exploration constant balancing exploitation vs. exploration.
2. **Expansion**:
   If a node is not terminal and has untried legal actions, pick an untried action, apply it to a copied board state, and create a new child `MCTSNode`.
3. **Simulation (Rollout)**:
   Simulate self-play from the expanded state until a terminal condition (win/loss/draw) is reached.
   - Default rollout policy: Uniform random move selection from legal columns.
   - Playout depth bound (e.g. up to 42 plies max).
4. **Backpropagation**:
   Propagate the simulation outcome (+1 for win, -1 for loss, 0 for draw) back up the search path to the root, updating visits $n_i$ and value $w_i$.

### Dual-Mode Budgeting
Per `[DECISION-003]`, MCTS must support:
- `simulations`: Fixed iteration count (e.g. 500-1000 rollouts) for deterministic benchmarking.
- `time_limit`: Wall-clock budget (e.g. 0.20s per move) checking `time.perf_counter() < deadline` after each iteration, allowing head-to-head competition against Alpha-Beta under equal thinking times.

---

## 2. Multi-Game Benchmarking Harness (`BenchmarkRunner`)

### Requirements
- Execute $N$ games between Agent A and Agent B (e.g. 10, 20, 50 games).
- Alternate first-player turn: Agent A starts in odd games (Player 1), Agent B starts in even games (Player 1) to eliminate first-mover advantage bias.
- Deterministic seeding for reproducibility across runs.
- Log aggregate outcomes:
  - Win rate % for Agent A and Agent B, Draw rate %.
  - Average decision time (ms) per move and per game.
  - Average nodes expanded / simulations per move.
  - Peak memory allocated via `tracemalloc`.

---

## 3. Pygame GUI Architecture (`Connect4Pygame`)

### Architecture
- Decoupled from core game engine: uses `connect4.core.Board` and polymorphic `Agent` instances.
- Standard Connect Four dimensions:
  - 7 columns $\times$ 6 rows, square size 100px $\rightarrow$ board width 700px, board height 700px (600px grid + 100px header).
  - Colors: Blue board (`#0055D4`), Black slots (`#0F172A`), Red disc (`#EF4444` for Player 1), Yellow disc (`#FACC15` for Player 2).
- Event handling:
  - `MOUSEMOTION`: Render floating disc in header tracking cursor column.
  - `MOUSEBUTTONDOWN`: Drop disc into hovered column if legal.
  - AI Turn Handling: Run agent's `select_move(board)` without freezing the UI loop.
- Non-blocking headless test mode: Allow GUI logic verification in CI / headless environments without opening an actual X/DirectX window.
