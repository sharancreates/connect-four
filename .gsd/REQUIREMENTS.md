---
milestone: v1.0
updated: 2026-10-10T14:45:00+05:30
---

# Requirements

## Overview
Requirements derived from the Adani University ECSCT24301 Stage 1 Proposal and Work Distribution Plan.

---

## Functional Requirements

| ID | Requirement | Source | Phase | Owner | Status |
|----|-------------|--------|-------|-------|--------|
| REQ-01 | Setup modular repository package layout, dependencies, and coding conventions | Proposal Sec 8 | 1 | Member 2 | Complete |
| REQ-02 | Implement Connect Four 6x7 board state, gravity drop, legal moves, win & draw detection | Proposal Sec 4, 5 | 1 | Member 1 / Shared | Complete |
| REQ-03 | Build Random-move baseline agent sampling uniformly from legal columns | Proposal Sec 7 | 1 | Member 1 / Shared | Complete |
| REQ-04 | Build plain Minimax agent (no pruning) measuring raw node expansions | Proposal Sec 7 | 1 | Member 1 / Shared | Complete |
| REQ-05 | Implement node, execution time, and memory instrumentation wrapper (`tracemalloc`, `perf_counter`) | Proposal Sec 8 | 1 | Member 2 | Complete |
| REQ-06 | Build interactive CLI game loop (Human-vs-Agent, Agent-vs-Agent, Human-vs-Human) | Dist. Plan W1 | 1 | Member 2 | Complete |
| REQ-07 | Draft formal PEAS characterization and academic problem statement documentation | Proposal Sec 3, 4 | 1 | Member 2 | Complete |
| REQ-08 | Implement Alpha-Beta pruning with depth-limited heuristic evaluation function | Proposal Sec 7 | 2 | Member 1 | Pending |
| REQ-09 | Implement Monte Carlo Tree Search (UCT selection, rollout, backpropagation) | Proposal Sec 7 | 2 | Member 2 | Pending |
| REQ-10 | Build interactive Pygame GUI interface with click-to-drop and move visualization | Proposal Sec 8 | 2-3 | Member 2 | Pending |
| REQ-11 | Automated multi-game benchmark suite generating comparative metrics & plots | Proposal Sec 8 | 3 | Member 2 | Pending |

---

## Non-Functional Requirements

| ID | Requirement | Category | Phase | Status |
|----|-------------|----------|-------|--------|
| NFR-01 | Unit test coverage for core board rules and agent move validity | Reliability | 1 | Complete |
| NFR-02 | Move decision latency instrumentation with sub-millisecond precision | Performance | 1 | Complete |
| NFR-03 | Deterministic and reproducible seeding for random and MCTS rollouts | Reproducibility | 1-2 | Complete |
| NFR-04 | Clean CLI interface with clear visual board rendering and input validation | Usability | 1 | Complete |

---

## Traceability Matrix (Week 1 / Phase 1)

| Requirement | Plans | Tests | Status |
|-------------|-------|-------|--------|
| REQ-01 | Plan 1.1 | Verification of package imports | Complete |
| REQ-02 | Plan 1.2 | `test_board.py` | Complete |
| REQ-03 | Plan 1.2 | `test_agents.py` | Complete |
| REQ-04 | Plan 1.2 | `test_agents.py` | Complete |
| REQ-05 | Plan 1.3 | `test_instrumentation.py` | Complete |
| REQ-06 | Plan 1.3 | `test_game_loop.py` & CLI smoke tests | Complete |
| REQ-07 | Plan 1.1 | `docs/PEAS_AND_PROBLEM_STATEMENT.md` | Complete |
