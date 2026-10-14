---
milestone: v1.0
version: 1.0.0
updated: 2026-10-12T07:58:00+05:30
---

# Roadmap

> **Current Phase:** Phase 3 - Benchmarking, GUI Integration, Analysis & Report (Week 3)
> **Status:** ✅ Complete (All Milestones & Member 2 Deliverables Verified)

## Must-Haves (from SPEC)

- [x] Standard 6x7 Connect Four engine with complete rule enforcement
- [x] Baseline Random Agent and baseline plain Minimax Agent
- [x] Benchmarking instrumentation wrapper (time, memory, nodes expanded)
- [x] CLI game loop supporting Human-vs-Agent and Agent-vs-Agent
- [x] Comprehensive PEAS and Problem Statement documentation
- [x] Alpha-Beta pruning with heuristic evaluation (Week 2 - Member 1)
- [x] Monte Carlo Tree Search (MCTS / UCT) agent (Week 2 - Member 2)
- [x] Interactive Pygame GUI interface skeleton (Week 2-3 - Member 2)
- [x] Comprehensive benchmarking harness, visualizations, and final report (Week 3)

---

## Phases

### Phase 1: Environment, Baselines & Game Engine (Week 1)
**Status:** ✅ Complete
**Objective:** Deliver working Connect Four core engine, baseline agents (Random, Plain Minimax), CLI game loop, instrumentation wrapper, and PEAS documentation.
**Requirements:** REQ-01, REQ-02, REQ-03, REQ-04, REQ-05, REQ-06, REQ-07

**Plans:**
- [x] Plan 1.1: Project scaffolding, package structure, coding conventions, and PEAS documentation
- [x] Plan 1.2: Core board representation, game rules, Random baseline agent, and plain Minimax agent
- [x] Plan 1.3: Benchmarking instrumentation wrapper (time/memory/node counts) and CLI game loop

---

### Phase 2: Advanced Algorithms & Heuristic Design (Week 2)
**Status:** ✅ Complete
**Objective:** Implement Alpha-Beta pruning, depth-limited heuristics, MCTS (UCT), and Pygame GUI skeleton.
**Requirements:** REQ-08, REQ-09, REQ-10
**Depends on:** Phase 1

**Plans:**
- [x] Plan 2.1: Alpha-Beta pruning with iterative deepening and heuristic evaluation (Member 1)
- [x] Plan 2.2: Monte Carlo Tree Search with UCT selection and playouts (Member 2)
- [x] Plan 2.3: Pygame GUI skeleton with board rendering and multi-game benchmark runner (Member 2)

---

### Phase 3: Benchmarking, GUI Integration, Analysis & Report (Week 3)
**Status:** ✅ Complete
**Objective:** Finish GUI visual polish with live controls, build publication plotting engine, run comparative benchmarks, and complete Stage 3 academic report and viva guide.
**Requirements:** REQ-11
**Depends on:** Phase 2

**Plans:**
- [x] Plan 3.1: Interactive Pygame GUI Polish & Controls (Member 2)
- [x] Plan 3.2: Comparative Visualizations Suite & Figures Generation (Member 2)
- [x] Plan 3.3: Stage 3 Academic Report (Sections 1, 6, 7) & Viva Defense Guide (Member 2)
- [x] Plan 3.3b: Scaling & failure-mode experimentation, error analysis (Sections 2, 3, 4, 5, 8), and slide outline (Member 1)

---

## Progress Summary

| Phase | Status | Plans | Complete |
|-------|--------|-------|----------|
| 1 | ✅ | 3/3 | 100% |
| 2 | ✅ | 3/3 | 100% |
| 3 | ✅ | 4/4 | 100% |

---

## Timeline

| Phase | Started | Completed | Duration |
|-------|---------|-----------|----------|
| 1 | 2026-10-10 | 2026-10-10 | 1 day |
| 2 | 2026-10-11 | 2026-10-12 | 2 days |
| 3 | 2026-10-12 | 2026-10-12 | 1 day |
