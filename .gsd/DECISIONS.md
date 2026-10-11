# DECISIONS.md — Architecture Decision Records

> **Purpose**: Log significant technical decisions and their rationale.

---

## [DECISION-001] Package Architecture & Modularity

**Date**: 2026-10-10
**Status**: Accepted

### Context
The Connect Four project is developed by a two-member team with distinct roles:
- Member 1: Algorithms & Search (Minimax, Alpha-Beta, Heuristics)
- Member 2: Engineering, Evaluation & GUI (Game engine scaffolding, CLI, Instrumentation, MCTS, Pygame GUI)
To prevent code merge conflicts and facilitate independent testing, the codebase must adhere to strict modular boundaries.

### Decision
Structure the codebase under a top-level `connect4` package:
- `connect4.core`: State representation, legal move generation, transition, goal checks.
- `connect4.agents`: Polymorphic agent interface (`Agent`) with subclasses (`RandomAgent`, `MinimaxAgent`, `AlphaBetaAgent`, `MCTSAgent`).
- `connect4.benchmark`: Performance measurement (`MetricsTracker`, profiling wrapper for node expansions, time, and memory).
- `connect4.cli`: Console game loop and interactive runner.
- `connect4.gui`: Pygame frontend (Week 2/3).

### Rationale
Clear separation of concerns enables Member 1 and Member 2 to develop and unit-test components concurrently without tight coupling.

### Consequences
Agents must adhere to the `Agent.select_move(board)` contract and use the shared `Board` API.

---

## [DECISION-002] Instrumentation & Profiling Architecture

**Date**: 2026-10-10
**Status**: Accepted

### Context
Member 2 is responsible for benchmarking search algorithms. Algorithms must report nodes expanded, wall-clock decision time, and memory usage without altering algorithmic logic.

### Decision
Implement a reusable `MetricsTracker` context manager / wrapper in `connect4.benchmark.instrumentation` that leverages Python's built-in `time.perf_counter()` and `tracemalloc`. Integrate a `NodeCounter` callback or property in the search agents so expansions are recorded transparently.

### Rationale
Using standard library tools avoids heavy external dependencies while guaranteeing microsecond time accuracy and byte-level memory tracking.

---

## [DECISION-003] MCTS Search Budget & Playout Architecture

**Date**: 2026-10-11
**Status**: Accepted

### Context
Member 2 is implementing Monte Carlo Tree Search (MCTS with UCT). To fairly benchmark MCTS against depth-limited Alpha-Beta pruning, MCTS needs to operate under comparable resource and "thinking time" budgets.

### Decision
Support dual-mode budget allocation in `MCTSAgent`:
1. `simulations: int` (e.g. 500-1000 rollouts per move) for deterministic rollout budgets.
2. `time_limit: float` (e.g. 0.20s per move) using wall-clock time checking during tree search.
Employ UCT selection with exploration constant $C_p = \sqrt{2} \approx 1.414$, random/light rollouts, and backpropagation of $\pm 1$ terminal utility.

### Rationale
Allows both reproducible step-based testing and realistic time-bounded competition against Alpha-Beta under equal thinking time constraints.

---

## [DECISION-004] Automated Multi-Game Benchmark & GUI Architecture

**Date**: 2026-10-11
**Status**: Accepted

### Context
Week 2 requires extending the benchmarking harness to auto-run many seeded agent-vs-agent matches and record win/draw/loss rates alongside node/simulation counts, as well as beginning the Pygame GUI skeleton.

### Decision
1. Create `connect4.benchmark.runner` (`BenchmarkRunner`) to orchestrate multi-game matches with alternating first-mover turns, random seeds, and tabular metric summaries.
2. Build `connect4.gui.app` (`Connect4Pygame`) with visual 6x7 grid rendering, hover disc tracking, click-to-drop input, and turn management.

