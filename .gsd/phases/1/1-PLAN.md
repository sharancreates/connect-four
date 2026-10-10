# Plan 1: Week 1 — Environment, Baselines & Game Engine (Member 2 Scope)

> **Owner:** Member 2 (Engineering, GUI & Evaluation) + Baseline Integration
> **Objective:** Deliver folder structure, coding conventions, PEAS & problem statement documentation, instrumentation wrapper (time/memory/nodes), CLI game loop, and functional baseline agents (Random & Plain Minimax) achieving the Week 1 milestone.

## Tasks

### Task 1: Scaffolding, Conventions, and PEAS Documentation
- Create `docs/CODING_CONVENTIONS.md`.
- Create `docs/PEAS_AND_PROBLEM_STATEMENT.md`.
- Establish package layout: `connect4/core/`, `connect4/agents/`, `connect4/benchmark/`, `connect4/cli/`.

### Task 2: Core Board Representation & Baseline Agents
- Implement `connect4/core/board.py`: 6x7 grid, drop disc, legal moves, win & draw checks.
- Implement `connect4/agents/base.py`: Base abstract agent.
- Implement `connect4/agents/random_agent.py`: Uniform random mover.
- Implement `connect4/agents/minimax_agent.py`: Depth-limited plain minimax (no pruning) measuring raw node expansions.

### Task 3: Benchmarking Instrumentation Wrapper
- Implement `connect4/benchmark/instrumentation.py`: MetricsTracker context manager and decorator capturing `time.perf_counter()`, `tracemalloc` memory delta/peak, and node expansion counts.

### Task 4: Command-Line Game Loop & Entrypoint
- Implement `connect4/cli/game_loop.py` & `main.py`: Interactive CLI with board visualization, turn stats, human-vs-agent and agent-vs-agent modes.

### Task 5: Testing & Verification
- Unit test suite in `tests/`: `test_board.py`, `test_agents.py`, `test_instrumentation.py`, `test_game_loop.py`.
- Run tests and capture baseline expansion numbers for the Week 1 milestone report.
