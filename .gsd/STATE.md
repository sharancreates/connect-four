---
updated: 2026-10-11T19:40:00+05:30
---

# Project State

## Current Position

- **Phase**: 2 - Advanced Algorithms & Heuristic Design (Week 2)
- **Active Role**: Member 1 (Algorithms & Core Logic) Deliverables Complete
- **Status**: Week 2 Member 1 work marked as DONE (Alpha-Beta pruning, 69-window heuristic evaluation, iterative deepening with time budget, test suite expansion, benchmark verification)

## Week 2 Member 1 Deliverables Summary

1. **Algorithms & Agents**:
   - `AlphaBetaAgent` (`connect4/agents/alphabeta_agent.py`): Depth-limited adversarial search with alpha-beta pruning, center-out move ordering, and optional advanced heuristic toggle.
   - `Heuristic Evaluation` (`connect4/agents/heuristic.py`): Precomputed 69 four-in-a-row sliding window evaluation (24 horizontal, 21 vertical, 24 diagonal) weighting open 3s (+5/-6), open 2s (+2/-2), center column control (+3), and terminal states.
   - `IterativeAlphaBetaAgent` (`connect4/agents/iterative_agent.py`): Time-bounded search with per-node deadline checks (`TimeUp` exception), graceful timeout fallback to deepest completed iteration, and depth tracking.

2. **CLI Integration & Registration**:
   - `main.py` and `connect4/agents/__init__.py`: Registered `iterative` (`IterativeAlphaBetaAgent`), `--time1`/`--time2` per-move time budgets, and `--heuristic1`/`--heuristic2` flags.

3. **Files Touched**:
   - `connect4/agents/alphabeta_agent.py`
   - `connect4/agents/heuristic.py`
   - `connect4/agents/iterative_agent.py`
   - `connect4/agents/__init__.py`
   - `main.py`
   - `tests/test_alphabeta.py`
   - `tests/test_heuristic.py`
   - `tests/test_iterative.py`
   - `docs/ALGORITHMS.md`
   - `README.md`
   - `.gsd/STATE.md`
   - `.gsd/ROADMAP.md`

4. **Test Suite Status**:
   - Total Tests: **34/34 passing** (`python -m pytest tests/ -v` in 1.89s).
   - Coverage: Board mechanics (10), baseline agents (4), alpha-beta parity & pruning (4), heuristic evaluation windows (9), iterative deepening & time bounds (4), instrumentation (3).

5. **Empirical Benchmark Summary**:
   - **Match (a) Heuristic Evaluation Impact**:
     `alphabeta` (depth 4, center-only) vs `alphabeta` (depth 4, heuristic enabled)
     *Winner*: **Player 2 (AlphaBeta with heuristic)** in 34 turns.
     *P1 (Center)*: 17 moves, 167.06 ms (9.83 ms/move), 1,766 nodes.
     *P2 (Heuristic)*: 17 moves, 402.53 ms (23.68 ms/move), 2,441 nodes.
   - **Match (b) Iterative Deepening vs. Fixed Depth**:
     `alphabeta` (depth 4) vs `iterative` (max depth 10, 1.0s budget)
     *Winner*: **Player 2 (Iterative)** in 20 turns.
     *P1 (AlphaBeta)*: 10 moves, 108.58 ms, 1,499 nodes.
     *P2 (Iterative)*: 10 moves, 7,119.36 ms (711.94 ms/move), 60,920 nodes.
   - **Match (c) Iterative Deepening vs. Random Baseline**:
     `random` vs `iterative` (max depth 10, 0.5s budget)
     *Winner*: **Player 2 (Iterative)** in 8 turns.
     *P1 (Random)*: 4 moves, 0.13 ms, 4 nodes.
     *P2 (Iterative)*: 4 moves, 1,019.73 ms, 8,789 nodes.

## Next Steps

- Hand off to Member 2 for MCTS (UCT) agent implementation (`connect4/agents/mcts_agent.py`) and Pygame GUI skeleton.
- Week 3: Benchmarking support, large-scale tournament evaluation, comparative plotting, and error analysis.
