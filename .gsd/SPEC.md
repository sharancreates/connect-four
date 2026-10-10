# SPEC.md — Project Specification

> **Status**: `FINALIZED`
>
> ⚠️ **Planning Lock**: No code may be written until this spec is marked `FINALIZED`.

## Vision
Build a rigorous, modular, and empirically benchmarked Connect Four AI system comparing deterministic adversarial search (Minimax with Alpha-Beta pruning and depth-limited heuristics) against simulation-driven search (Monte Carlo Tree Search with UCT), evaluated against baseline agents in a standardized 6x7 grid environment.

## Goals
1. **Engine & CLI Foundation**: Create a fast, robust 6x7 Connect Four board representation, rule engine, and versatile CLI game loop supporting Human-vs-Agent, Agent-vs-Agent, and Human-vs-Human modes.
2. **Deterministic Adversarial Search**: Implement a baseline plain Minimax agent (quantifying raw state-space explosion) followed by an optimized Alpha-Beta pruning agent with iterative deepening and heuristic board evaluation.
3. **Statistical Simulation Search**: Implement a Monte Carlo Tree Search (MCTS) agent with UCT selection, rollout playout policy, and backpropagation.
4. **Empirical Benchmarking & Instrumentation**: Build comprehensive instrumentation capturing wall-clock decision time, peak/current memory allocation (`tracemalloc`), and nodes/simulations expanded per move and across full games.
5. **Interactive GUI & Academic Deliverables**: Deliver an engaging interactive demo, automated benchmarking suite with comparative visualizations, and academic documentation adhering to the Adani University ECSCT24301 specification.

## Non-Goals (Out of Scope)
- Deep reinforcement learning or neural network training (e.g., AlphaZero neural policy/value nets).
- Online client-server multiplayer networking.
- Non-standard board dimensions or Connect Four variants (e.g., PopOut, 8x8).

## Constraints
- **Language & Runtime**: Python 3.10+ / 3.11.
- **Core Dependencies**: NumPy for vectorized board manipulation, `time` / `tracemalloc` for profiling, `matplotlib` for analysis plots.
- **Rules**: Standard vertical 6-row by 7-column grid; gravity disc drop; 4-in-a-row horizontally, vertically, or diagonally wins; full board without 4-in-a-row results in a draw.
- **Architecture**: Strict modular separation between game representation (`connect4.core`), agents (`connect4.agents`), benchmarking harness (`connect4.benchmark`), and interfaces (`connect4.cli`, `connect4.gui`).

## Success Criteria
- [x] Connect Four board representation correctly handles legal moves, gravity transitions, win detection (horizontal, vertical, diagonal), and draw conditions with 100% test pass rate.
- [x] Comprehensive CLI game loop allows interactive play (human vs. agent) and automated matches (agent vs. agent) with clear board visualization and turn statistics.
- [x] Benchmarking instrumentation wrapper reliably measures wall-clock time (`time.perf_counter`), memory consumption (`tracemalloc`), and node expansion counts.
- [x] Baseline Random agent and plain Minimax agent are operational and playable via CLI, successfully recording baseline node-expansion counts (Week 1 Milestone).
- [x] Complete PEAS specification and problem statement documentation prepared and structured.

## Work Distribution (Team of 2 | 3-Week Sprint)
- **Member 1 (Algorithms & Core Logic)**: Core search algorithms (plain Minimax, Alpha-Beta pruning, iterative deepening, heuristic evaluation function), state-space write-up, and error analysis.
- **Member 2 (Engineering, GUI & Evaluation - Current Focus)**: Repository structure & conventions, CLI game loop, time/memory/node instrumentation wrapper, MCTS integration, Pygame GUI demo, comparative benchmark runner, PEAS & problem statement write-up.

---

*Last updated: 2026-10-10*
